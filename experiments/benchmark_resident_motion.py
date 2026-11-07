"""Compare complete warm advances on identical Langevin baths."""
import argparse
import json
import platform
from statistics import median
from time import perf_counter

import numpy as np

from simulator.engine import Simulation


def scenario(particles, steps, backend):
    scale = np.sqrt(particles/302)
    return dict(schema_version=1, model='mixing', seed=43, duration=steps*.002,
                chemistry=dict(motion='langevin', damping=.1, molecules=particles//2,
                               box=[24*scale, 18*scale]),
                engine=dict(sample_every=25, force_backend=backend))


def measure(particles, steps, repeats, backends):
    row = dict(particles=particles, timings={})
    reference = None
    for backend in backends:
        start = perf_counter()
        sim = Simulation(scenario(particles, 25+steps*repeats, backend))
        setup = perf_counter()-start
        samples = []
        sim.listeners.append(lambda time, pos, diagnostics: samples.append(time))
        start = perf_counter()
        sim.advance(25)
        first = perf_counter()-start
        if reference is None:
            reference = (sim.chemistry.pos.copy(), sim.motion.velocities.copy())
        elif backend == 'cuda-resident':
            row['first_block_max_error'] = {
                name: float(np.max(np.abs(candidate-expected)))
                for name, candidate, expected in zip(
                    ('position', 'velocity'),
                    (sim.chemistry.pos, sim.motion.velocities), reference)
            }
        durations = []
        for _ in range(repeats):
            start = perf_counter()
            sim.advance(steps)
            durations.append(perf_counter()-start)
        assert sim.done and len(samples) == 2+steps*repeats//25
        row['timings'][backend] = dict(
            setup_s=setup, first_25_steps_s=first, warm_repeats_s=durations,
            warm_median_s=median(durations), warm_steps_per_s=steps/median(durations))
    row['speedup'] = {
        backend: row['timings'][backend]['warm_median_s'] /
        row['timings']['cuda-resident']['warm_median_s']
        for backend in backends if backend != 'cuda-resident'
    }
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--particles', nargs='+', type=int, default=[302, 3000, 12000])
    parser.add_argument('--steps', type=int, default=500)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--cpp', action='store_true')
    args = parser.parse_args()
    if (args.steps <= 0 or args.steps % 25 or args.repeats <= 0 or
        any(count < 14 or count % 2 for count in args.particles)):
        parser.error('need positive repeats, steps in blocks of 25, and even particle counts >= 14')
    import cupy as cp

    properties = cp.cuda.runtime.getDeviceProperties(cp.cuda.Device().id)
    print(json.dumps(dict(gpu=properties['name'].decode(), cupy=cp.__version__,
                          os=platform.platform(), steps=args.steps, repeats=args.repeats,
                          dt=.002, sample_every=25, seed=43)), flush=True)
    backends = ['numba', 'cpp', 'cuda-resident'] if args.cpp else ['numba', 'cuda-resident']
    for particles in args.particles:
        print(json.dumps(measure(particles, args.steps, args.repeats, backends)), flush=True)


if __name__ == '__main__':
    main()
