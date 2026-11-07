"""CUDA-resident Langevin mechanics with topology supplied at reaction ticks."""
from functools import lru_cache

import numpy as np

from .motion import InertialMotion
from .native_forces import SOURCE as FORCE_SOURCE, pack_terms
from .resident_fields import SOURCE as FIELD_SOURCE, CaptureField, SegmentField
from .resident_ports import SOURCE as PORT_SOURCE, LipidPorts


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

LOCAL Vec orientation(const double* pos, const Index* ends, Index particle) {
    if (ends[0] < 0) return {0., 0.};
    Vec u = between(pos, ends[0], ends[1]);
    Vec v = between(pos, ends[2], ends[3]);
    double lu = at_least(sqrt(dot(u,u)), 1e-8);
    double lv = at_least(sqrt(dot(v,v)), 1e-8);
    u = {u.x/lu, u.y/lu};
    v = {v.x/lv, v.y/lv};
    double cosine = dot(u, v);
    double scale = (particle == ends[0] ? 8. : -8.)/lu;
    return {scale*(v.x-cosine*u.x), scale*(v.y-cosine*u.y)};
}

ENTRY void kick(const double* pos, double* vel, double* force, const double* old,
                double* displacement, int n, double half_kick,
                const int* heads, const int* next, double width, int nx, int ny,
                const Index* offsets, const Index* refs, const Index* pairs,
                const Index* kinds, const double* contact, const double* springs,
                const double* angles, Index spring_count, Index kind_count,
                const Index* alignments, bool reactive, const double* capture,
                bool has_capture, const double* ports, const double* barrier,
                bool mixed, double box_x, double box_y, bool advance) {
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
    if (reactive) {
        Vec term = orientation(pos, alignments+4*i, i);
        if (has_capture) {
            term.x += capture[2*i];
            term.y += capture[2*i+1];
        }
        if (mixed) {
            term.x += ports[2*i]; term.y += ports[2*i+1];
            term.x += barrier[2*i]; term.y += barrier[2*i+1];
        }
        total.x += term.x;
        total.y += term.y;
    }
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

    module = cp.RawModule(code=FORCE_SOURCE + SOURCE + FIELD_SOURCE + PORT_SOURCE,
                          options=('--std=c++11', '--fmad=false'))
    names = ('drift', 'clear_cells', 'bin_particles', 'order_cells', 'kick', 'capture_field',
             'clear_segment_measure', 'measure_segments', 'segment_field',
             'lipid_geometry', 'lipid_scores', 'lipid_derivatives', 'lipid_force')
    return tuple(module.get_function(name) for name in names)


def _grid(size):
    return ((size + 127) // 128,)


def _bin_particles(kernels, pos, n, cells, grid):
    clear, bin_particles, order = kernels
    heads, links, width, nx, ny = grid
    clear(_grid(cells), (128,), (heads, cells))
    bin_particles(_grid(n), (128,), (pos, heads, links, n, width, nx, ny))
    order(_grid(cells), (128,), (heads, links, cells))


def mixed_field_snapshot(chemistry):
    """Evaluate the ported mixed force families on a frozen snapshot."""
    import cupy as cp

    n = np.int32(len(chemistry.pos))
    width = np.float64(chemistry.contact.max())
    nx, ny = (np.int32(np.ceil(length/width)) for length in chemistry.box)
    cells = np.int32(int(nx)*int(ny))
    pos = cp.asarray(chemistry.pos)
    grid = (cp.empty(cells, dtype=cp.int32), cp.empty(n, dtype=cp.int32), width, nx, ny)
    kernels = _kernels(cp.cuda.Device().id)
    _bin_particles(kernels[1:4], pos, n, cells, grid)
    capture = CaptureField(cp, chemistry, chemistry.capture)
    segment = SegmentField(cp, chemistry)
    ports = LipidPorts(cp, chemistry)
    capture.launch(kernels[5], pos, n, grid)
    segment.launch(kernels[6:9], pos, n, grid)
    ports.launch(kernels[9:], pos, n, grid)
    return np.stack((capture.output.get(), segment.output.get(), ports.output.get()))


class ResidentLangevinMotion(InertialMotion):
    """Keep geometry, topology and intermediate forces on the GPU between steps."""

    def __init__(self, chemistry, rng, settings, model, reaction_every):
        super().__init__(chemistry, rng, settings)
        try:
            import cupy as cp
        except ImportError as exc:
            raise RuntimeError('Resident CUDA mechanics require CuPy and a CUDA runtime') from exc
        self.cp = cp
        self.stream = cp.cuda.Stream(non_blocking=True)
        self.reactive = model != 'mixing'
        self.mixed = model == 'mixed_synthesis'
        self.block_steps = min(25, reaction_every) if self.reactive else 25
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
        # A single contiguous download publishes the state and its stability check.
        self.state = cp.empty((7, count), dtype=cp.float64)
        self.device = tuple(self.state[:6].reshape(3, count, 2))
        self.displacement = self.state[6]
        self.noise = cp.empty((self.block_steps, count, 2), dtype=cp.float64)
        self.half_dt = np.float64(dt/2)
        self.half_kick = np.float64(dt/(2*self.mass))
        self.decay = np.float64(np.exp(-self.gamma*dt))
        self.sigma = np.float64(np.sqrt(
            c.config['temperature']/self.mass*(1-self.decay*self.decay)))
        self.topology = None
        self.terms = None
        self.alignment_state = None
        self.alignments = cp.empty((count if self.reactive else 0, 4), dtype=cp.int64)
        self.capture = None
        self.ports = LipidPorts(cp, c) if self.mixed else None
        self.barrier = SegmentField(cp, c) if self.mixed else None
        self.kind_state = c.kinds.copy()
        self._update_topology(c)
        self.box = tuple(map(np.float64, c.box))
        pos, velocities, force = self.device
        pos.set(c.pos)
        velocities.set(self.velocities)
        if self.force is not None:
            force.set(self.force)

    def _update_topology(self, c):
        topology = (c.springs, c.angles)
        if self.topology is None or any(
            not np.array_equal(old, new) for old, new in zip(self.topology, topology)
        ):
            packed = pack_terms(len(c.pos), [], c.kinds, c.contact, *topology)
            if self.terms is None:
                self.terms = tuple(self.cp.asarray(term) for term in packed)
            else:
                buffers = list(self.terms)
                for index in (0, 1, 5, 6):
                    source, destination = packed[index], buffers[index]
                    if source.shape == destination.shape:
                        destination.set(source)
                    else:
                        # Captured CUDA graphs hold raw pointers and scalar counts.
                        self.graph = None
                        buffers[index] = self.cp.asarray(source)
                self.terms = tuple(buffers)
            self.topology = tuple(array.copy() for array in topology)
        if not self.reactive:
            return
        if self.mixed:
            if not np.array_equal(c.kinds, self.kind_state):
                self.terms[3].set(c.kinds)
                self.kind_state = c.kinds.copy()
            self.ports.update(c)
            if self.barrier.update(c):
                self.graph = None
            catalyst = c.capture
        else:
            catalyst = None if c.assembly is None else c.assembly.catalyst
        if catalyst is not None:
            if self.capture is None:
                self.capture = CaptureField(self.cp, c, catalyst)
            else:
                self.capture.update(c, catalyst)
        state = (c.rungs, c.pairing)
        if self.alignment_state is not None and all(
            np.array_equal(old, new) for old, new in zip(self.alignment_state, state)
        ):
            return
        aligned = np.full((len(c.pos), 4), -1, dtype=np.int64)
        sites = np.flatnonzero(c.pairing >= 0)
        if len(sites):
            ends = c.rungs[sites]
            aligned[ends[:, 0]] = aligned[ends[:, 1]] = np.column_stack(
                (ends, c.rungs[c.pairing[sites]]))
        self.alignments.set(aligned)
        self.alignment_state = tuple(array.copy() for array in state)

    def _force(self, advance):
        pos, vel, force = self.device
        kick = self.kernels[4]
        grid = self.heads, self.next, self.width, self.nx, self.ny
        if self.width:
            _bin_particles(self.kernels[1:4], pos, self.count, self.cells, grid)
        if self.capture is not None:
            self.capture.launch(self.kernels[5], pos, self.count, grid)
        if self.mixed:
            self.barrier.launch(self.kernels[6:9], pos, self.count, grid)
            self.ports.launch(self.kernels[9:], pos, self.count, grid)
        kick(_grid(self.count), (128,), (
            pos, vel, force, self.old, self.displacement, self.count, self.half_kick,
            self.heads, self.next, self.width, self.nx, self.ny, *self.terms,
            np.int64(len(self.terms[5])), np.int64(len(self.terms[4])),
            self.alignments, np.bool_(self.reactive),
            self.old if self.capture is None else self.capture.output,
            np.bool_(self.capture is not None),
            self.old if self.ports is None else self.ports.output,
            self.old if self.barrier is None else self.barrier.output,
            np.bool_(self.mixed), *self.box, np.bool_(advance)))

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
            elif self.force is None:
                self._update_topology(c)
            if self.force is None:
                self._force(False)
                self.force_evaluations += 1
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
            host = self.state.get()
            displacement = float(host[6].max())
            if displacement > 1.:
                # The scheduler has not advanced. Keep its last valid checkpoint.
                rng.bit_generator.state = rng_state
                self.force_evaluations = evaluations
                self.graph = None
                self.device = None
                raise FloatingPointError('Inertial integrator unstable; reduce dt, never clip motion')
            c.pos, self.velocities, self.force = host[:6].reshape(3, len(c.pos), 2)
            if self.mixed:
                c._views()
        self.max_displacement = max(self.max_displacement, displacement)
        self.steps += steps
        self.force_evaluations += steps
