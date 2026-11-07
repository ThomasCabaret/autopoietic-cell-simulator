"""Validate CUDA mixed-force snapshots against their CPU reference kernels."""
import json
from pathlib import Path

import numpy as np

from simulator.engine import Simulation
from simulator.mixed_boundary import segment_forces
from simulator.resident_motion import mixed_field_snapshot
from simulator.spatial import Neighborhood


ROOT = Path(__file__).resolve().parents[1]


def cp1_config():
    path = ROOT/'research/campaign_recipes/CH1_20261106T073608844143Z/manifest.json'
    tasks = json.loads(path.read_text(encoding='utf-8'))['tasks']
    return next(row['scenario'] for row in tasks if row['label'] == 'CH1_integrated_s1')


def compare(c):
    neighbors = Neighborhood('tree')
    expected = np.stack((c.capture.forces(c, neighbors), segment_forces(c, neighbors)))
    actual = mixed_field_snapshot(c)
    np.testing.assert_allclose(actual, expected, atol=1e-11, rtol=1e-12)
    return dict(max_force=np.abs(expected).max(axis=(1, 2)).tolist(),
                max_error=np.abs(actual-expected).max(axis=(1, 2)).tolist())


def main():
    sim = Simulation(cp1_config())
    sim.prepare()
    print(json.dumps(dict(step=0, **compare(sim.chemistry))))
    for steps in (250, 1000, 2500):
        sim.advance(steps)
        print(json.dumps(dict(step=sim.step_index, **compare(sim.chemistry))))


if __name__ == '__main__':
    main()
