"""Compare local saturation on frozen H/T proposals and short CR1 prefixes."""
import argparse
import json
from pathlib import Path
from statistics import median
from time import perf_counter

import numpy as np

from experiments.benchmark_cp1_scaling import scaled_cp1
from simulator.competitive_ports import birth_port_base, birth_port_delta
from simulator.engine import Simulation
from simulator.observations import components
from simulator.resident_motion import saturated_birth_snapshot
from simulator.spatial import Neighborhood


ROOT = Path(__file__).resolve().parents[1]


def timed(call):
    call()
    samples = []
    for _ in range(5):
        start = perf_counter()
        result = call()
        samples.append(perf_counter()-start)
    return result, median(samples)


def birth_screen():
    sim = Simulation(scaled_cp1(2118))
    sim.prepare()
    c = sim.chemistry
    # Expose free faces and guarantee trial births near real lipid neighbors.
    c.lipids.links = [link for i, link in enumerate(c.lipids.links) if i%4]
    h = np.flatnonzero((c.ligand_types == 0) & (c.capture.categories >= 0))
    t = np.flatnonzero((c.ligand_types == 1) & (c.capture.categories >= 0))
    for a, b, (i, j) in zip(h[:16], t[:16], c.lipids.rungs.items()):
        c.pos[a], c.pos[b] = c.pos[i]+[.75, .15], c.pos[j]+[.75, .15]
    neighbors = Neighborhood()
    pairs = c.lipid_candidates(neighbors)
    trials = pairs.copy()
    flip = c.ligand_types[trials[:, 0]] == 1
    trials[flip] = trials[flip, ::-1]
    if not len(trials):
        raise AssertionError('No proposals in the frozen comparison')

    def cpu_batch():
        base = birth_port_base(c, neighbors)
        return np.array([birth_port_delta(c, a, b, neighbors, base) for a, b in trials])

    competitive, original_s = timed(cpu_batch)
    c.config['free_port_potential'] = 'saturated'
    saturated, saturated_s = timed(cpu_batch)
    device, gpu_s = timed(lambda: saturated_birth_snapshot(c, trials))
    np.testing.assert_allclose(device, saturated, atol=1e-12, rtol=1e-12)
    assert np.count_nonzero(saturated) > 0
    return dict(proposals=len(trials), active=int(np.count_nonzero(saturated)),
                competitive_cpu_s=original_s, saturated_cpu_s=saturated_s, saturated_gpu_s=gpu_s,
                max_error=float(np.abs(device-saturated).max()),
                max_law_difference=float(np.abs(competitive-saturated).max()))


def assembly_screen(duration):
    path = ROOT/'research/campaign_recipes/CR1_20261106T105709120898Z/manifest.json'
    tasks = json.loads(path.read_text(encoding='utf-8'))['tasks']
    for task in tasks[:2]:
        for law in ('competitive', 'saturated'):
            cfg = task['scenario']
            cfg['duration'] = duration
            cfg['chemistry']['free_port_potential'] = law
            sim = Simulation(cfg)
            checkpoints = []
            for step in range(1, 5):
                end = round(sim.target_step*step/4)
                sim.advance(end-sim.step_index)
                heads, _, links = sim.chemistry.lipids.layout()
                groups = list(components(len(heads), {(a, b) for a, b, _, _ in links}))
                checkpoints.append(dict(time=sim.time, links=len(links),
                    largest=max(len(group) for group, _, _ in groups),
                    largest_cycle=max((len(group) for group, _, cycle in groups if cycle), default=0)))
            print(json.dumps(dict(law=law, seed=cfg['seed'], checkpoints=checkpoints)), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assembly-duration', type=float, default=20.)
    args = parser.parse_args()
    print(json.dumps(birth_screen()), flush=True)
    if args.assembly_duration:
        assembly_screen(args.assembly_duration)


if __name__ == '__main__':
    main()
