"""GPU proposal, reservation and commit for local precursor capture."""

SOURCE = r"""
LOCAL unsigned long long capture_hash(unsigned long long x) {
    x = (x ^ (x >> 30))*0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27))*0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

LOCAL unsigned long long capture_key(unsigned long long seed, unsigned long long tick,
                                     int site, int atom) {
    return capture_hash(seed ^ capture_hash(tick+0x9e3779b97f4a7c15ULL)
                        ^ ((static_cast<unsigned long long>(site) << 32) | unsigned(atom)));
}

LOCAL double capture_uniform(unsigned long long word) {
    return double(word >> 11)*(1./9007199254740992.);
}

ENTRY void release_capture(int n, const Index* sites, const double* activity,
                           Index* partner, unsigned long long* claims, int* chosen,
                           unsigned long long* tick, unsigned long long seed,
                           double interval, double off_rate, unsigned long long* counts) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i >= n) return;
    claims[i] = ~0ULL;
    chosen[i] = -1;
    if (sites[2*i] < 0) return;
    Index j = partner[i];
    if (j < 0) return;
    double rate = activity[i] < 1. ? fmax(off_rate,5.) : off_rate;
    if (capture_uniform(capture_key(seed,*tick,i,-1)) < -expm1(-rate*interval)) {
        partner[i] = -1;
        partner[j] = -1;
        atomicAdd(counts+1, 1ULL);
    }
}

ENTRY void refresh_capture_groups(int n, Index* sites, const Index* ligands,
                                  const Index* partner, const Index* offsets,
                                  const Index* adjacent) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i >= n || sites[2*i] < 0) return;
    Index allowed = 3;
    for (Index q = offsets[i]; q < offsets[i+1]; ++q) {
        Index atom = partner[adjacent[q]];
        if (atom >= 0)
            allowed &= sites[2*i] == ligands[2*atom] ? 0 : ligands[2*atom+1];
    }
    sites[2*i+1] = allowed;
}

ENTRY void propose_capture(const double* pos, int n, const Index* sites,
                           const Index* ligands, const double* activity, const Index* partner,
                           unsigned long long* claims, int* selected, const unsigned long long* tick,
                           unsigned long long seed, double radius, double interval, double on_rate,
                           const int* heads, const int* next, double cell, int nx, int ny) {
    int i = blockIdx.x*blockDim.x+threadIdx.x;
    if (i >= n || sites[2*i] < 0 || partner[i] >= 0) return;
    double p = -expm1(-activity[i]*on_rate*interval);
    double x = pos[2*i], y = pos[2*i+1];
    int left = cell_axis(x-radius,cell,nx), right = cell_axis(x+radius,cell,nx);
    int bottom = cell_axis(y-radius,cell,ny), top = cell_axis(y+radius,cell,ny);
    int chosen = -1;
    unsigned long long best = ~0ULL;
    for (int row = bottom; row <= top; ++row) {
        for (int col = left; col <= right; ++col) {
            for (int j = heads[row*nx+col]; j >= 0; j = next[j]) {
                if (sites[2*i] != ligands[2*j] || partner[j] >= 0 ||
                    !(sites[2*i+1] & ligands[2*j+1])) continue;
                Vec d = between(pos,i,j);
                if (dot(d,d) >= radius*radius) continue;
                auto key = capture_key(seed,*tick,i,j);
                auto priority = capture_hash(key+0x9e3779b97f4a7c15ULL);
                if (capture_uniform(key) < p &&
                    (chosen < 0 || priority < best || (priority == best && j < chosen))) {
                    chosen = j;
                    best = priority;
                }
            }
        }
    }
    // Each site proposes once. A ligand can commit only the winning site.
    if (chosen >= 0) {
        selected[i] = chosen;
        atomicMin(claims+chosen, (best & 0xffffffff00000000ULL) | unsigned(i));
    }
}

ENTRY void commit_capture(int n, const unsigned long long* claims, const int* selected,
                          const Index* ligands, const Index* offsets, const Index* adjacent,
                          Index* partner,
                          unsigned long long* tick, unsigned long long* counts) {
    int j = blockIdx.x*blockDim.x+threadIdx.x;
    if (j == 0) ++(*tick);
    if (j >= n || claims[j] == ~0ULL) return;
    int i = int(claims[j] & 0xffffffffULL);
    // Validate against the immutable reservation table. Adjacent claims with
    // incompatible material or symbols cannot both commit, even on distinct ligands.
    for (Index q = offsets[i]; q < offsets[i+1]; ++q) {
        Index other = adjacent[q];
        int atom = selected[other];
        if (atom < 0 || claims[atom] >= claims[j] ||
            (claims[atom] & 0xffffffffULL) != static_cast<unsigned long long>(other))
            continue;
        if (ligands[2*j] == ligands[2*atom] || ligands[2*j+1] != ligands[2*atom+1])
            return;
    }
    partner[i] = j;
    partner[j] = i;
    atomicAdd(counts, 1ULL);
}
"""
