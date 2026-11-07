"""Validate CUDA mixed-force snapshots and the short CH1 reactive trajectory."""
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
    expected = np.stack((c.capture.forces(c, neighbors), segment_forces(c, neighbors),
                         c.lipids.forces(c.pos, c.config, neighbors)[0]))
    actual = mixed_field_snapshot(c)
    np.testing.assert_allclose(actual, expected, atol=1e-11, rtol=1e-12)
    return dict(max_force=np.abs(expected).max(axis=(1, 2)).tolist(),
                max_error=np.abs(actual-expected).max(axis=(1, 2)).tolist())


def main():
    config = cp1_config()
    cpu = Simulation(config)
    config['engine']['force_backend'] = 'cuda-resident'
    gpu = Simulation(config)
    for steps in (0, 250, 1000, 2500):
        cpu.advance(steps)
        gpu.advance(steps)
        checks = dict(step=cpu.step_index, **compare(cpu.chemistry))
        for key, a, b in (
            ('position', cpu.chemistry.pos, gpu.chemistry.pos),
            ('velocity', cpu.motion.velocities, gpu.motion.velocities),
        ):
            np.testing.assert_allclose(a, b, atol=1e-10, rtol=0)
            checks[key+'_error'] = float(np.abs(a-b).max())
        assert cpu.chemistry.bonds() == gpu.chemistry.bonds()
        assert cpu.rng.bit_generator.state == gpu.rng.bit_generator.state
        print(json.dumps(checks))


if __name__ == '__main__':
    main()
