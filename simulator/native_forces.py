"""Shared local mechanical expressions for the optional C++ and CUDA backends.

The C++ source lives here so existing source snapshots also freeze the native
kernel. Each lane owns one output particle and visits terms in reference order.
The caller still owns topology, neighbors, integration and reactions.
"""
import ctypes
from functools import lru_cache
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import numpy as np
from numba import njit


SOURCE = r"""
#ifdef __CUDACC__
#define LOCAL __device__ __forceinline__
#define ENTRY extern "C" __global__
#else
#include <math.h>
#define LOCAL static inline
#ifdef _WIN32
#define ENTRY extern "C" __declspec(dllexport)
#else
#define ENTRY extern "C"
#endif
#endif

using Index = long long;

struct Vec {
    double x, y;
};

LOCAL Vec between(const double* pos, Index i, Index j) {
    return {pos[2*j] - pos[2*i], pos[2*j+1] - pos[2*i+1]};
}

LOCAL double dot(Vec a, Vec b) {
    return a.x*b.x + a.y*b.y;
}

LOCAL double at_least(double value, double lower) {
    return value < lower ? lower : value;
}

LOCAL Vec angle_force(const double* pos, const double* angle, int role) {
    Index i = Index(angle[0]), j = Index(angle[1]), k = Index(angle[2]);
    Vec u = between(pos, j, i), v = between(pos, j, k);
    double lu = at_least(sqrt(dot(u, u)), 1e-8);
    double lv = at_least(sqrt(dot(v, v)), 1e-8);
    u = {u.x/lu, u.y/lu};
    v = {v.x/lv, v.y/lv};
    double cosine = dot(u, v);
    double scale = angle[3] * (cosine - angle[4]);
    Vec g = {scale/lu*(v.x-cosine*u.x), scale/lu*(v.y-cosine*u.y)};
    Vec h = {scale/lv*(u.x-cosine*v.x), scale/lv*(u.y-cosine*v.y)};
    if (role == 0) return {-g.x, -g.y};
    if (role == 2) return {-h.x, -h.y};
    return {g.x+h.x, g.y+h.y};
}

LOCAL Vec particle_force(
    Index i, const double* pos, const Index* offsets, const Index* refs,
    const Index* pairs, const Index* kinds, const double* contact,
    const double* springs, const double* angles,
    Index pair_count, Index spring_count, Index kind_count, double core_k
) {
    Vec force = {0.0, 0.0};
    for (Index q = offsets[i]; q < offsets[i+1]; ++q) {
        Index term = refs[q]/3;
        int role = int(refs[q]%3);
        Vec contribution;
        if (term < pair_count) {
            Index a = pairs[2*term], b = pairs[2*term+1];
            Vec d = between(pos, a, b);
            double r = sqrt(dot(d, d));
            double overlap = at_least(contact[kinds[a]*kind_count+kinds[b]]-r, 0.0);
            double scale = core_k*overlap / at_least(r, 1e-8);
            double sign = role == 0 ? -1.0 : 1.0;
            contribution = {sign*(scale*d.x), sign*(scale*d.y)};
        } else if (term < pair_count+spring_count) {
            const double* spring = springs+4*(term-pair_count);
            Vec d = between(pos, Index(spring[0]), Index(spring[1]));
            double r = sqrt(dot(d, d));
            double scale = spring[2]*(r-spring[3]) / at_least(r, 1e-8);
            double sign = role == 0 ? 1.0 : -1.0;
            contribution = {sign*(scale*d.x), sign*(scale*d.y)};
        } else {
            contribution = angle_force(pos, angles+5*(term-pair_count-spring_count), role);
        }
        force.x += contribution.x;
        force.y += contribution.y;
    }
    return force;
}

ENTRY void local_forces(
    const double* pos, const Index* offsets, const Index* refs,
    const Index* pairs, const Index* kinds, const double* contact,
    const double* springs, const double* angles,
    Index pair_count, Index spring_count, Index kind_count, double core_k,
    Index count, Index batch, double* output
) {
#ifdef __CUDACC__
    Index lane = Index(blockIdx.x)*blockDim.x+threadIdx.x;
    if (lane >= count*batch) return;
    {
#else
    for (Index lane = 0; lane < count*batch; ++lane) {
#endif
        Index i = lane%count;
        Vec value = particle_force(i, pos+2*(lane-i), offsets, refs, pairs,
                                   kinds, contact, springs, angles, pair_count,
                                   spring_count, kind_count, core_k);
        output[2*lane] = value.x;
        output[2*lane+1] = value.y;
    }
}
"""


@njit(cache=True)
def _incident_terms(count, pairs, springs, angles):
    """Pack incident term IDs by particle, retaining pair/spring/angle order."""
    split = len(pairs)+len(springs)
    indices = np.full((split+len(angles), 3), -1, dtype=np.int64)
    indices[:len(pairs), :2] = pairs
    indices[len(pairs):split, :2] = springs[:, :2]
    indices[split:] = angles[:, :3]
    offsets = np.zeros(count+1, dtype=np.int64)
    for term in indices:
        for i in term:
            if i >= 0:
                offsets[i+1] += 1
    offsets = np.cumsum(offsets)
    refs = np.empty(offsets[-1], dtype=np.int64)
    cursor = offsets[:-1].copy()
    for number, term in enumerate(indices):
        for role, i in enumerate(term):
            if i >= 0:
                refs[cursor[i]] = 3*number+role
                cursor[i] += 1
    return offsets, refs


def pack_terms(count, pairs, kinds, contact, springs, angles):
    pairs = np.ascontiguousarray(pairs, dtype=np.int64).reshape(-1, 2)
    kinds = np.ascontiguousarray(kinds, dtype=np.int64)
    contact = np.ascontiguousarray(contact, dtype=np.float64)
    springs = np.ascontiguousarray(springs, dtype=np.float64).reshape(-1, 4)
    angles = np.ascontiguousarray(angles, dtype=np.float64).reshape(-1, 5)
    # These are internal engine arrays. Check index ranges before native access.
    if kinds.shape != (count,) or contact.ndim != 2 or contact.shape[0] != contact.shape[1]:
        raise ValueError('Invalid force topology')
    if kinds.size and (kinds.min() < 0 or kinds.max() >= len(contact)):
        raise ValueError('Invalid contact kind')
    for indices in (pairs, springs[:, :2], angles[:, :3]):
        if indices.size and not np.all((indices >= 0) & (indices < count)):
            raise ValueError('Invalid force term index')
    offsets, refs = _incident_terms(count, pairs, springs, angles)
    return offsets, refs, pairs, kinds, contact, springs, angles


@lru_cache(maxsize=1)
def _cpp_kernel():
    compiler = shutil.which(os.environ.get('AUTOPOIETIC_CXX', 'g++'))
    if compiler is None:
        raise RuntimeError('C++ forces require g++ or AUTOPOIETIC_CXX')
    flags = ['-O3', '-shared', '-std=c++11', '-ffp-contract=off']
    if os.name != 'nt':
        flags.append('-fPIC')
    version = subprocess.check_output([compiler, '--version'])
    fingerprint = hashlib.sha256(SOURCE.encode()+version+repr(flags).encode()).hexdigest()[:20]
    cache = Path(tempfile.gettempdir())/'autopoietic_native_forces'
    cache.mkdir(parents=True, exist_ok=True)
    library = cache/(fingerprint+('.dll' if os.name == 'nt' else '.so'))
    if not library.exists():
        with tempfile.TemporaryDirectory(dir=cache) as folder:
            target = Path(folder)/library.name
            result = subprocess.run([compiler, *flags, '-x', 'c++', '-', '-o', str(target)],
                                    input=SOURCE, text=True, capture_output=True)
            if result.returncode:
                raise RuntimeError('C++ force compilation failed\n'+result.stderr)
            try:
                os.replace(target, library)
            except PermissionError:
                if not library.exists():
                    raise
    fn = ctypes.CDLL(str(library)).local_forces
    fn.argtypes = ([ctypes.c_void_p]*8 + [ctypes.c_longlong]*3 +
                   [ctypes.c_double, ctypes.c_longlong, ctypes.c_longlong, ctypes.c_void_p])
    fn.restype = None
    return fn


@lru_cache(maxsize=1)
def _cuda_kernel():
    try:
        import cupy
    except ImportError as exc:
        raise RuntimeError('CUDA forces require CuPy and a CUDA runtime') from exc
    fn = cupy.RawKernel(SOURCE, 'local_forces', options=('--std=c++11', '--fmad=false'))
    fn.compile()
    return cupy, fn


def _sizes(terms):
    return len(terms[2]), len(terms[5]), len(terms[4])


def cuda_forces_device(positions, terms, output, core_k=80.):
    """Evaluate a device-resident batch sharing the same interaction topology."""
    _, fn = _cuda_kernel()
    batch, count, _ = positions.shape
    if batch*count:
        integers = tuple(np.int64(x) for x in (*_sizes(terms), count, batch))
        fn(((batch*count+127)//128,), (128,),
           (positions, *terms, *integers[:3], np.float64(core_k), *integers[3:], output))


def cpp_forces(pos, pairs, kinds, contact, springs, angles, core_k=80.):
    pos = np.ascontiguousarray(pos, dtype=np.float64).reshape(-1, 2)
    terms = pack_terms(len(pos), pairs, kinds, contact, springs, angles)
    output = np.empty_like(pos)
    fn = _cpp_kernel()
    fn(*(x.ctypes.data for x in (pos, *terms)), *_sizes(terms), core_k,
       len(pos), 1, output.ctypes.data)
    return output


def cuda_forces(pos, pairs, kinds, contact, springs, angles, core_k=80.):
    cupy, _ = _cuda_kernel()
    pos = np.ascontiguousarray(pos, dtype=np.float64).reshape(-1, 2)
    terms = pack_terms(len(pos), pairs, kinds, contact, springs, angles)
    positions = cupy.asarray(pos[None, ...])
    output = cupy.empty_like(positions)
    cuda_forces_device(positions, tuple(cupy.asarray(x) for x in terms), output, core_k)
    return output.get()[0]


def select_force_kernel(name):
    if name == 'cpp':
        _cpp_kernel()
        return cpp_forces
    if name == 'cuda':
        _cuda_kernel()
        return cuda_forces
    raise ValueError('Unknown native force backend '+str(name))
