"""Device forces for local capture and segment repulsion in mixed synthesis."""
import numpy as np


SOURCE = r"""
LOCAL Vec capture_pair(const double* pos, int i, int j, const Index* sites,
                       const Index* ligands, const double* activity, double energy,
                       double width2, double reach2) {
    const Index* site = sites+2*i;
    const Index* ligand = ligands+2*j;
    if (site[0] < 0 || site[0] != ligand[0] || !(site[1] & ligand[1]))
        return {0., 0.};
    Vec d = between(pos, i, j);
    double r2 = dot(d,d);
    if (r2 >= reach2) return {0., 0.};
    double scale = activity[i]*energy*exp(-r2/(2*width2))/width2;
    return {scale*d.x, scale*d.y};
}

ENTRY void capture_field(const double* pos, int n, const Index* sites,
                         const Index* ligands, const double* activity,
                         double energy, double sigma, const Index* partner, bool live,
                         double spring, const int* heads,
                         const int* next, double cell, int nx, int ny, double* out) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i >= n) return;
    Vec total = {0., 0.};
    Index bound = live ? partner[i] : -1;
    if (bound >= 0) {
        Vec d = between(pos,i,bound);
        double length = sqrt(dot(d,d));
        double scale = spring*length/at_least(length,1e-8);
        total = {scale*d.x,scale*d.y};
    } else if (energy != 0. && (sites[2*i] >= 0 || ligands[2*i] >= 0)) {
        double r = 3*sigma, x = pos[2*i], y = pos[2*i+1];
        int left = cell_axis(x-r,cell,nx), right = cell_axis(x+r,cell,nx);
        int bottom = cell_axis(y-r,cell,ny), top = cell_axis(y+r,cell,ny);
        for (int row = bottom; row <= top; ++row) {
            for (int col = left; col <= right; ++col) {
                for (int j = heads[row*nx+col]; j >= 0; j = next[j]) {
                    if (i == j || (live && partner[j] >= 0)) continue;
                    Vec a = capture_pair(pos,i,j,sites,ligands,activity,energy,sigma*sigma,r*r);
                    Vec b = capture_pair(pos,j,i,sites,ligands,activity,energy,sigma*sigma,r*r);
                    total.x += a.x-b.x;
                    total.y += a.y-b.y;
                }
            }
        }
    }
    out[2*i] = total.x;
    out[2*i+1] = total.y;
}

ENTRY void measure_segments(const double* pos, const Index* edges, int count,
                            unsigned long long* longest2) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i >= count) return;
    Vec d = between(pos,edges[2*i],edges[2*i+1]);
    // Nonnegative IEEE-754 values are ordered by their unsigned bit pattern.
    atomicMax(longest2, static_cast<unsigned long long>(__double_as_longlong(dot(d,d))));
}

ENTRY void clear_segment_measure(unsigned long long* longest2) {
    *longest2 = 0;
}

LOCAL Vec repel(const double* pos, Index a, Index b, Index probe, int role,
                double radius, double stiffness) {
    Vec d = between(pos,a,b), w = between(pos,a,probe);
    double t = fmin(1.,fmax(0.,dot(w,d)/at_least(dot(d,d),1e-16)));
    Vec q = {w.x-t*d.x,w.y-t*d.y};
    double distance = sqrt(dot(q,q));
    if (distance >= radius) return {0.,0.};
    double scale = stiffness*(radius-distance)/at_least(distance,1e-10);
    double weight = role == 0 ? -(1-t) : (role == 1 ? -t : 1.);
    return {weight*(scale*q.x),weight*(scale*q.y)};
}

ENTRY void segment_field(const double* pos, int n, const Index* edges,
                         const Index* offsets, const Index* incident, const bool* probes,
                         const unsigned long long* longest2, double radius, double stiffness,
                         const int* heads, const int* next, double cell, int nx, int ny,
                         double* out) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i >= n) return;
    Vec total = {0.,0.};
    double x = pos[2*i], y = pos[2*i+1];
    if (probes[i]) {
        // Conservative search only. The actual force reads one segment and one bead.
        double reach = radius+sqrt(__longlong_as_double(*longest2));
        int left = cell_axis(x-reach,cell,nx), right = cell_axis(x+reach,cell,nx);
        int bottom = cell_axis(y-reach,cell,ny), top = cell_axis(y+reach,cell,ny);
        for (int row = bottom; row <= top; ++row) {
            for (int col = left; col <= right; ++col) {
                for (int j = heads[row*nx+col]; j >= 0; j = next[j]) {
                    for (Index k = offsets[j]; k < offsets[j+1]; ++k) {
                        Index e = incident[k];
                        if (edges[2*e] != j) continue;
                        Vec term = repel(pos,j,edges[2*e+1],i,2,radius,stiffness);
                        total.x += term.x;
                        total.y += term.y;
                    }
                }
            }
        }
    }
    for (Index k = offsets[i]; k < offsets[i+1]; ++k) {
        Index e = incident[k], a = edges[2*e], b = edges[2*e+1];
        Index j = a == i ? b : a;
        double u = pos[2*j], v = pos[2*j+1];
        int left = cell_axis(fmin(x,u)-radius,cell,nx), right = cell_axis(fmax(x,u)+radius,cell,nx);
        int bottom = cell_axis(fmin(y,v)-radius,cell,ny), top = cell_axis(fmax(y,v)+radius,cell,ny);
        for (int row = bottom; row <= top; ++row) {
            for (int col = left; col <= right; ++col) {
                for (int p = heads[row*nx+col]; p >= 0; p = next[p]) {
                    if (!probes[p]) continue;
                    Vec term = repel(pos,a,b,p,a == i ? 0 : 1,radius,stiffness);
                    total.x += term.x;
                    total.y += term.y;
                }
            }
        }
    }
    out[2*i] = total.x;
    out[2*i+1] = total.y;
}
"""


def capture_descriptors(c, cap, live=False):
    """Freeze local eligibility for the interval between two reaction ticks."""
    n = len(c.pos)
    sites = np.full((n, 2), -1, dtype=np.int64)
    ligands = np.full((n, 2), -1, dtype=np.int64)
    activity = np.zeros(n)
    atoms = np.flatnonzero(cap.owners >= 0)
    owners = cap.owners[atoms]
    free = (c.pairing[owners] < 0) & (live | (cap.site_bound[owners] < 0))
    atoms, owners = atoms[free], owners[free]
    sites[atoms, 0] = c.bits[owners]
    sites[atoms, 1] = 3
    activity[atoms] = cap.activity[owners]
    free_ligands = (cap.categories >= 0) & (live | (cap.atom_bound < 0))
    ligands[free_ligands, 0] = cap.categories[free_ligands]
    ligands[free_ligands, 1] = 1
    if c.config.get('capture_cooperativity', False):
        sites[atoms, 1] = cap.allowed_groups[owners] @ np.array([1, 2], dtype=np.int64)
        ligands[free_ligands, 1] <<= cap.material_group[free_ligands]
    return sites, ligands, activity


def segment_descriptors(c):
    edges = np.array([(a, b) for a, b, _, _ in c.lipids.links], dtype=np.int64).reshape(-1, 2)
    endpoints = edges.ravel()
    offsets = np.empty(len(c.pos)+1, dtype=np.int64)
    offsets[0] = 0
    np.cumsum(np.bincount(endpoints, minlength=len(c.pos)), out=offsets[1:])
    incident = np.argsort(endpoints, kind='stable').astype(np.int64)//2
    probes = np.zeros(len(c.pos), dtype=np.bool_)
    rungs = c.host.rungs
    probes[rungs[rungs[:, 1] >= 0].ravel()] = True
    return edges, offsets, incident, probes


class CaptureField:
    """Keep device buffer addresses stable across reaction ticks."""

    def __init__(self, cp, chemistry, capture, partner=None):
        cfg = chemistry.config
        self.descriptors = capture_descriptors(chemistry, capture, live=partner is not None)
        self.buffers = tuple(cp.asarray(row) for row in self.descriptors)
        self.params = tuple(map(np.float64, (
            cfg['food_ligand_energy'], cfg['food_ligand_width'])))
        self.occupancy = (self.buffers[0] if partner is None else partner,
                          np.bool_(partner is not None), np.float64(capture.stiffness))
        self.output = cp.empty_like(chemistry.pos, dtype=cp.float64)

    def update(self, chemistry, capture):
        descriptors = capture_descriptors(chemistry, capture, live=self.occupancy[1])
        for old, new, buffer in zip(self.descriptors, descriptors, self.buffers):
            if not np.array_equal(old, new):
                buffer.set(new)
        self.descriptors = descriptors

    def launch(self, kernel, pos, n, grid):
        kernel(((int(n)+127)//128,), (128,), (
            pos, n, *self.buffers, *self.params, *self.occupancy, *grid, self.output))


class SegmentField:
    """Device-owned topology and scratch for segment repulsion."""

    def __init__(self, cp, chemistry):
        cfg = chemistry.config
        self.cp = cp
        self.descriptors = segment_descriptors(chemistry)
        self.segments = tuple(cp.asarray(row) for row in self.descriptors)
        self.segment_params = tuple(map(np.float64, (
            cfg['bound_barrier_radius'], cfg['bound_barrier_stiffness'])))
        self.longest2 = cp.empty(1, dtype=cp.uint64)
        self.output = cp.zeros_like(chemistry.pos, dtype=cp.float64)

    def update(self, chemistry):
        descriptors = segment_descriptors(chemistry)
        buffers = list(self.segments)
        resized = False
        for index, (old, new) in enumerate(zip(self.descriptors, descriptors)):
            if old.shape != new.shape:
                buffers[index] = self.cp.asarray(new)
                resized = True
            elif not np.array_equal(old, new):
                buffers[index].set(new)
        self.segments = tuple(buffers)
        self.descriptors = descriptors
        if resized and not len(descriptors[0]):
            self.output.fill(0.)
        return resized

    def launch(self, kernels, pos, n, grid):
        clear, measure, segment = kernels
        count = len(self.segments[0])
        if not count or self.segment_params[0] <= 0:
            return
        clear((1,), (1,), (self.longest2,))
        measure(((count+127)//128,), (128,), (pos, self.segments[0],
                                             np.int32(count), self.longest2))
        segment(((int(n)+127)//128,), (128,), (pos, n, *self.segments, self.longest2,
                                               *self.segment_params, *grid, self.output))
