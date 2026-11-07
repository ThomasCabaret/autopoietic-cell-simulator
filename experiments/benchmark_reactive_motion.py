"""Time short, matched reactive prefixes and locate the CPU costs of CP1."""
import argparse
import cProfile
import json
from pathlib import Path
import pstats
from statistics import median
from time import perf_counter

from simulator.engine import Simulation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario', type=Path)
    parser.add_argument('--backends', nargs='+', default=['numba'],
                        choices=['numba', 'cpp', 'cuda', 'cuda-resident'])
    parser.add_argument('--profile', action='store_true')
    args = parser.parse_args()
    config = json.loads(args.scenario.read_text(encoding='utf-8'))
    for backend in args.backends:
        config.setdefault('engine', {})['force_backend'] = backend
        sim = Simulation(config)
        steps = 1000
        warmup = 250
        if sim.target_step < warmup+3*steps:
            parser.error('scenario must allow at least 3250 steps')
        sim.advance(warmup)
        timings = []
        for _ in range(3):
            start = perf_counter()
            sim.advance(steps)
            timings.append(perf_counter()-start)
        print(json.dumps(dict(backend=backend, scenario=config['name'], particles=len(sim.chemistry.pos),
                              warmup_steps=warmup, steps=steps, timings_s=timings,
                              median_s=median(timings))), flush=True)
        if args.profile:
            # Profile a matched earlier state, separate from the timed runs.
            sim = Simulation(config)
            sim.advance(warmup)
            profile = cProfile.Profile()
            profile.runcall(sim.advance, steps)
            pstats.Stats(profile).strip_dirs().sort_stats('cumulative').print_stats(30)


if __name__ == '__main__':
    main()
