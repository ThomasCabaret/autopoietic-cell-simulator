"""CUDA-resident Langevin mechanics for the nonreactive mixing model."""
from functools import lru_cache

import numpy as np

from .motion import InertialMotion
from .native_forces import SOURCE as FORCE_SOURCE, pack_terms


SOURCE = r"""
LOCAL int cell_axis(double x, double width, int count) {
    // Outside a soft wall, bin at the edge but evaluate actual distances.
    return int(fmax(0.0, fmin(x/width, double(count-1))));
}

ENTRY void drift(double* pos, double* vel, const double* force, double* old,
                 const double* noise, int noise_offset, int n,
                 double half_dt, double half_kick, double decay, double sigma) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i >= 2*n) return;
    double v = vel[i] + force[i]*half_kick;
    double p = pos[i] + v*half_dt;
    v = decay*v + sigma*noise[noise_offset+i];
    old[i] = pos[i];
    pos[i] = p + v*half_dt;
    vel[i] = v;
}

ENTRY void clear_cells(int* heads, int cells) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i < cells) heads[i] = -1;
}

ENTRY void bin_particles(const double* pos, int* heads, int* next, int n,
                         double width, int nx, int ny) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i >= n) return;
    int x = cell_axis(pos[2*i], width, nx);
    int y = cell_axis(pos[2*i+1], width, ny);
    next[i] = atomicExch(heads+y*nx+x, i);
}

ENTRY void order_cells(int* heads, int* next, int cells) {
    int cell = blockIdx.x*blockDim.x+threadIdx.x;
    if (cell >= cells) return;
    // Each cell has one writer. Order by particle ID for deterministic sums,
    // independently of atomic insertion order and with no occupancy cap.
    int sorted = -1;
    for (int i = heads[cell]; i >= 0;) {
        int rest = next[i];
        int* link = &sorted;
        while (*link >= 0 && *link < i) link = next+*link;
        next[i] = *link;
        *link = i;
        i = rest;
    }
    heads[cell] = sorted;
}

ENTRY void kick(const double* pos, double* vel, double* force, const double* old,
                double* displacement, int n, double half_kick,
                const int* heads, const int* next, double width, int nx, int ny,
                const Index* offsets, const Index* refs, const Index* pairs,
                const Index* kinds, const double* contact, const double* springs,
                const double* angles, Index spring_count, Index kind_count,
                double box_x, double box_y, bool advance) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i >= n) return;
    Vec total = {0., 0.};
    double px = pos[2*i], py = pos[2*i+1];
    if (width > 0.) {
        int x = cell_axis(px, width, nx), y = cell_axis(py, width, ny);
        for (int row = max(0, y-1); row <= min(ny-1, y+1); ++row) {
            for (int col = max(0, x-1); col <= min(nx-1, x+1); ++col) {
                for (int j = heads[row*nx+col]; j >= 0; j = next[j]) {
                    if (i == j) continue;
                    int a = min(i, j), b = max(i, j);
                    double radius = contact[kinds[a]*kind_count+kinds[b]];
                    Vec d = between(pos, a, b);
                    if (dot(d, d) >= radius*radius) continue;
                    Vec term = contact_force(d, radius, 80., i == a ? -1. : 1.);
                    total.x += term.x;
                    total.y += term.y;
                }
            }
        }
    }
    total = particle_force(i, pos, offsets, refs, pairs, kinds, contact, springs,
                           angles, 0, spring_count, kind_count, 80., total);
    force[2*i] = total.x + 100*(fmax(-px, 0.) - fmax(px-box_x, 0.));
    force[2*i+1] = total.y + 100*(fmax(-py, 0.) - fmax(py-box_y, 0.));
    if (!advance) return;
    vel[2*i] += force[2*i]*half_kick;
    vel[2*i+1] += force[2*i+1]*half_kick;
    Vec d = {px-old[2*i], py-old[2*i+1]};
    double moved = sqrt(dot(d, d));
    if (!isfinite(moved) || !isfinite(vel[2*i]) || !isfinite(vel[2*i+1]))
        moved = 2.;
    displacement[i] = fmax(displacement[i], moved);
}
"""


@lru_cache(maxsize=None)
def _kernels(device):
    import cupy as cp

    module = cp.RawModule(code=FORCE_SOURCE + SOURCE, options=('--std=c++11', '--fmad=false'))
    return tuple(module.get_function(name) for name in
                 ('drift', 'clear_cells', 'bin_particles', 'order_cells', 'kick'))


def _grid(size):
    return ((size + 127) // 128,)


class ResidentMixingMotion(InertialMotion):
    """Keep geometry, topology and intermediate forces on the GPU between steps."""

    block_steps = 25

    def __init__(self, chemistry, rng, settings):
        super().__init__(chemistry, rng, settings)
        try:
            import cupy as cp
        except ImportError as exc:
            raise RuntimeError('Resident CUDA mechanics require CuPy and a CUDA runtime') from exc
        self.cp = cp
        self.stream = cp.cuda.Stream(non_blocking=True)
        self.device = None
        self.graph = None

    def restore(self, state):
        super().restore(state)
        self.graph = None
        self.device = None

    def _upload(self, c, dt):
        cp = self.cp
        self.kernels = _kernels(cp.cuda.Device().id)
        count = len(c.pos)
        max_index = np.iinfo(np.int32).max
        if 2*self.block_steps*count > max_index:
            raise ValueError('Resident CUDA noise buffer exceeds the index range')
        self.count = np.int32(count)
        self.width = np.float64(c.contact.max())
        shape = tuple(int(np.ceil(length / self.width)) for length in c.box) if self.width else (1, 1)
        if shape[0]*shape[1] > max_index:
            raise ValueError('Resident CUDA grid exceeds the index range')
        self.nx, self.ny = map(np.int32, shape)
        self.cells = np.int32(int(self.nx)*int(self.ny))
        self.heads = cp.empty(self.cells, dtype=cp.int32)
        self.next = cp.empty(count, dtype=cp.int32)
        self.old = cp.empty_like(c.pos, dtype=cp.float64)
        self.displacement = cp.zeros(count, dtype=cp.float64)
        self.noise = cp.empty((self.block_steps, count, 2), dtype=cp.float64)
        self.half_dt = np.float64(dt/2)
        self.half_kick = np.float64(dt/(2*self.mass))
        self.decay = np.float64(np.exp(-self.gamma*dt))
        self.sigma = np.float64(np.sqrt(
            c.config['temperature']/self.mass*(1-self.decay*self.decay)))
        self.terms = tuple(cp.asarray(term) for term in pack_terms(
            count, [], c.kinds, c.contact, c.springs, c.angles))
        self.box = tuple(map(np.float64, c.box))
        self.device = (cp.asarray(c.pos), cp.asarray(self.velocities),
                       cp.empty_like(self.old) if self.force is None else cp.asarray(self.force))
        if self.force is None:
            self._force(False)
            self.force_evaluations += 1

    def _force(self, advance):
        pos, vel, force = self.device
        _, clear, bin_particles, order, kick = self.kernels
        if self.width:
            clear(_grid(self.cells), (128,), (self.heads, self.cells))
            bin_particles(_grid(self.count), (128,), (
                pos, self.heads, self.next, self.count, self.width, self.nx, self.ny))
            order(_grid(self.cells), (128,), (self.heads, self.next, self.cells))
        kick(_grid(self.count), (128,), (
            pos, vel, force, self.old, self.displacement, self.count, self.half_kick,
            self.heads, self.next, self.width, self.nx, self.ny, *self.terms,
            np.int64(len(self.terms[5])), np.int64(len(self.terms[4])), *self.box, np.bool_(advance)))

    def _launch_steps(self, steps):
        drift = self.kernels[0]
        pos, vel, force = self.device
        for step in range(steps):
            drift(_grid(2*self.count), (128,), (
                pos, vel, force, self.old, self.noise, np.int32(step*2*self.count),
                self.count, self.half_dt, self.half_kick, self.decay, self.sigma))
            self._force(True)

    def advance_block(self, c, rng, dt, steps):
        """Advance a bounded block; expose a consistent host state on return."""
        rng_state = rng.bit_generator.state
        evaluations = self.force_evaluations
        with self.stream:
            if self.device is None:
                self._upload(c, dt)
            self.displacement.fill(0.)
            for offset in range(0, steps, self.block_steps):
                count = min(self.block_steps, steps-offset)
                noise = rng.normal(size=(count, len(c.pos), 2))
                self.noise[:count].set(noise)
                if count == self.block_steps:
                    if self.graph is None:
                        self.stream.begin_capture()
                        self._launch_steps(count)
                        self.graph = self.stream.end_capture()
                    self.graph.launch(self.stream)
                else:
                    self._launch_steps(count)
            displacement = float(self.displacement.get().max())
            if displacement > 1.:
                # The scheduler has not advanced. Keep its last valid checkpoint.
                rng.bit_generator.state = rng_state
                self.force_evaluations = evaluations
                self.graph = None
                self.device = None
                raise FloatingPointError('Inertial integrator unstable; reduce dt, never clip motion')
            c.pos, self.velocities, self.force = (array.get() for array in self.device)
        self.max_displacement = max(self.max_displacement, displacement)
        self.steps += steps
        self.force_evaluations += steps
