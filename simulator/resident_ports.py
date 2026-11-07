"""Resident lipid forces with shared geometry and endpoint force projection."""
import numpy as np


SOURCE = r"""
struct PortGeometry {
    Vec head[2], tail[2], normal;
    double length;
};
static_assert(sizeof(PortGeometry) == 11*sizeof(double), "Port geometry layout");

ENTRY void lipid_geometry(const double* pos, int n, const Index* topology,
                          double short_length, PortGeometry* geometry, double* output) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i >= n) return;
    output[2*i] = output[2*i+1] = 0.;
    Index tail = topology[3*i];
    if (tail < 0) return;
    Vec d = between(pos,i,tail);
    double r = at_least(sqrt(dot(d,d)),1e-8);
    PortGeometry g;
    g.normal = {d.x/r,d.y/r};
    g.length = r;
    Vec tangent = {-g.normal.y,g.normal.x};
    for (int face = 0; face < 2; ++face) {
        double s = 2*face-1;
        g.head[face] = {pos[2*i]+s*.5*tangent.x,pos[2*i+1]+s*.5*tangent.y};
        g.tail[face] = {pos[2*tail]+s*short_length/2*tangent.x,
                        pos[2*tail+1]+s*short_length/2*tangent.y};
    }
    geometry[i] = g;
}

LOCAL void port_delta(const PortGeometry& own, const PortGeometry& other, int face,
                      Vec& head, Vec& tail) {
    int b = 1-face;
    head = {other.head[b].x-own.head[face].x,other.head[b].y-own.head[face].y};
    tail = {other.tail[b].x-own.tail[face].x,other.tail[b].y-own.tail[face].y};
}

LOCAL void project_port(const PortGeometry& own, int face, Vec h, Vec t, double scale,
                        double short_length, Vec& head, Vec& tail) {
    h = {scale*h.x,scale*h.y};
    t = {scale*t.x,scale*t.y};
    double s = 2*face-1;
    Vec v = {s*(.5*h.y+short_length/2*t.y),-s*(.5*h.x+short_length/2*t.x)};
    double normal = dot(v,own.normal);
    Vec correction = {(v.x-normal*own.normal.x)/own.length,
                      (v.y-normal*own.normal.y)/own.length};
    head.x += h.x-correction.x;
    head.y += h.y-correction.y;
    tail.x += t.x+correction.x;
    tail.y += t.y+correction.y;
}

// Competitive passes collect S, then sum(p/D²), then apply the derivative.
// Additive ports run just the final pass with multiplier one.
template<int stage>
LOCAL void lipid_ports(const double* pos, int i, const Index* topology,
                       const PortGeometry* geometry, double short_length, double epsilon,
                       double width, bool competitive, const int* heads, const int* next,
                       double cell, int nx, int ny, double* scores, double* derivatives,
                       double* output) {
    Index tail = topology[3*i];
    if (tail < 0) return;
    const PortGeometry& own = geometry[i];
    const Index* partners = topology+3*i+1;
    double reach = 1+4*width, x = pos[2*i], y = pos[2*i+1];
    double cutoff = exp(-8.), denominator = 2*width*width;
    double sums[2] = {0.,0.};
    Vec f_head = {0.,0.}, f_tail = {0.,0.};
    if (partners[0] < 0 || partners[1] < 0) {
        int left = cell_axis(x-reach,cell,nx), right = cell_axis(x+reach,cell,nx);
        int bottom = cell_axis(y-reach,cell,ny), top = cell_axis(y+reach,cell,ny);
        for (int row = bottom; row <= top; ++row) {
            for (int col = left; col <= right; ++col) {
                for (int j = heads[row*nx+col]; j >= 0; j = next[j]) {
                    if (i == j || j == partners[0] || j == partners[1] || topology[3*j] < 0) continue;
                    Vec d = between(pos,i,j);
                    if (dot(d,d) >= reach*reach) continue;
                    for (int face = 0; face < 2; ++face) {
                        int a = 2*i+face, b = 2*j+1-face;
                        if (partners[face] >= 0 || topology[3*j+2-face] >= 0) continue;
                        Vec h,t;
                        port_delta(own,geometry[j],face,h,t);
                        double z = (dot(h,h)+dot(t,t))/denominator;
                        if (z >= 8.) continue;
                        double e = exp(-z), multiplier = 1.;
                        if (competitive) {
                            double p = (e-cutoff*(9.-z))/(1-9*cutoff);
                            if (stage == 0) {
                                sums[face] += p;
                                continue;
                            }
                            double d = 1+scores[a]+scores[b]-2*p;
                            if (stage == 1) {
                                sums[face] += p/(d*d);
                                continue;
                            }
                            multiplier = 1/d-derivatives[a]-derivatives[b]+2*p/(d*d);
                        }
                        double scale = epsilon/(width*width)*(e-cutoff)*multiplier;
                        project_port(own,face,h,t,scale,short_length,f_head,f_tail);
                    }
                }
            }
        }
    }
    if (stage < 2) {
        double* target = stage == 0 ? scores : derivatives;
        target[2*i] = sums[0];
        target[2*i+1] = sums[1];
        return;
    }
    Vec b_head = {0.,0.}, b_tail = {0.,0.};
    for (int face = 0; face < 2; ++face) {
        Index j = partners[face];
        if (j < 0) continue;
        Vec h,t;
        port_delta(own,geometry[j],face,h,t);
        double stiffness = epsilon*(1-cutoff)/(width*width);
        project_port(own,face,h,t,stiffness,short_length,b_head,b_tail);
    }
    output[2*i] = f_head.x+b_head.x;
    output[2*i+1] = f_head.y+b_head.y;
    output[2*tail] = f_tail.x+b_tail.x;
    output[2*tail+1] = f_tail.y+b_tail.y;
}

#define PORT_PASS(name, stage) \
ENTRY void name(const double* pos, int n, const Index* topology, \
                const PortGeometry* geometry, double short_length, double epsilon, \
                double width, bool competitive, const int* heads, const int* next, \
                double cell, int nx, int ny, double* scores, double* derivatives, double* out) { \
    int i = blockIdx.x*blockDim.x+threadIdx.x; \
    if (i < n) lipid_ports<stage>(pos,i,topology,geometry,short_length,epsilon,width, \
                                   competitive,heads,next,cell,nx,ny,scores,derivatives,out); \
}

PORT_PASS(lipid_scores, 0)
PORT_PASS(lipid_derivatives, 1)
PORT_PASS(lipid_force, 2)
"""


def port_topology(chemistry):
    topology = np.full((len(chemistry.pos), 3), -1, dtype=np.int64)
    for head, tail in chemistry.lipids.rungs.items():
        topology[head, 0] = tail
    for i, j, a, b in chemistry.lipids.links:
        topology[i, 1+a] = j
        topology[j, 1+b] = i
    return topology


class LipidPorts:
    def __init__(self, cp, chemistry):
        cfg = chemistry.config
        self.params = tuple(map(np.float64, (
            cfg['short_length'], cfg['dock_energy'], cfg['dock_width'])))
        self.competitive = np.bool_(cfg['free_port_potential'] == 'competitive')
        self.topology = port_topology(chemistry)
        self.buffer = cp.asarray(self.topology)
        self.geometry = cp.empty((len(chemistry.pos), 11), dtype=cp.float64)
        self.output = cp.empty_like(chemistry.pos, dtype=cp.float64)
        self.scores = cp.empty_like(self.output)
        self.derivatives = cp.empty_like(self.output)

    def update(self, chemistry):
        topology = port_topology(chemistry)
        if not np.array_equal(self.topology, topology):
            self.buffer.set(topology)
            self.topology = topology

    def launch(self, kernels, pos, n, grid):
        geometry, scores, derivatives, force = kernels
        blocks = ((int(n)+127)//128,)
        geometry(blocks, (128,), (pos, n, self.buffer, self.params[0],
                                  self.geometry, self.output))
        args = (pos, n, self.buffer, self.geometry, *self.params, self.competitive,
                *grid, self.scores, self.derivatives, self.output)
        if self.competitive:
            scores(blocks, (128,), args)
            derivatives(blocks, (128,), args)
        force(blocks, (128,), args)
