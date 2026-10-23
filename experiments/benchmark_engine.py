"""Compare the same soft-core forces, including spatial lookup, after JIT warmup."""
import json
from pathlib import Path
import platform
import sys
import time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from simulator.physics import force_kernel
from simulator.reference import mechanical_forces
from simulator.spatial import Neighborhood
from simulator.checkpoint import source_hashes


def median_time(fun,repeats=5):
    times=[]
    for _ in range(repeats):
        start=time.perf_counter(); fun(); times.append(time.perf_counter()-start)
    return float(np.median(times))


def main():
    rows=[]
    rng=np.random.default_rng(234)
    for count in (128,512,2048):
        pos=rng.uniform(0,np.sqrt(count/4),(count,2))
        core=np.full((count,count),.7); np.fill_diagonal(core,0)
        kinds=np.zeros(count,dtype=np.int64); contact=np.array([[.7]])
        springs=np.empty((0,4)); angles=np.empty((0,5))
        tree=Neighborhood('tree',.25)
        brute=Neighborhood('brute',.25)
        def fast(): return force_kernel(pos,tree.pairs(pos,.7),kinds,contact,springs,angles)
        def exhaustive(): return force_kernel(pos,brute.pairs(pos,.7),kinds,contact,springs,angles)
        expected=mechanical_forces(pos,springs,angles,core)
        np.testing.assert_allclose(fast(),expected,atol=1e-11)
        np.testing.assert_allclose(exhaustive(),expected,atol=1e-11)
        # Invalidate each cache to measure rebuilds as well as the cheap cached path.
        def rebuilt():
            tree.cache.clear()
            return fast()
        dense=median_time(lambda:mechanical_forces(pos,springs,angles,core))
        cached=median_time(fast)
        rebuilding=median_time(rebuilt)
        rows.append({'particles':count,'density':4,'dense_reference_seconds':dense,
                     'tree_cached_seconds':cached,'tree_rebuilt_seconds':rebuilding,
                     'speedup_rebuilt_vs_dense':dense/rebuilding,'forces_equal_tolerance':1e-11})
    result={'scope':'Soft-core force + spatial search only; no chemistry, observer, rendering or GPU. Stationary configurations, medians of five calls after JIT warmup.',
            'python':platform.python_version(),'platform':platform.platform(),'source_sha256':source_hashes(),'measurements':rows}
    (ROOT/'research/ENGINE_BENCHMARK.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(rows,indent=2))


if __name__=='__main__': main()
