"""N1: refine time discretization of the frozen J3 populated bath, not its laws."""
import argparse
import copy
import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from simulator.engine import Simulation

BASELINE = ROOT/'research/campaign_recipes/J3_20261027T192723206222Z/manifest.json'


def scenario(factor, seed, duration=1200.):
    if factor not in (1, 2, 4):
        raise ValueError('N1 refinement must be 1, 2 or 4')
    manifest = json.loads(BASELINE.read_text(encoding='utf-8'))
    raw = copy.deepcopy(next(t['scenario'] for t in manifest['tasks']
        if t['label'] == 'J3_k16_bath' and t['scenario']['seed'] == seed))
    raw.update(name=f'N1_dt{factor}', branch='N1', duration=duration)
    raw['engine']['dt'] /= factor
    raw['engine']['sample_every'] *= factor
    return raw


def verify():
    rows = []
    for seed in range(3):
        baseline = Simulation(scenario(1, seed, duration=2.))
        for factor in (2, 4):
            sim = Simulation(scenario(factor, seed, duration=2.))
            assert sim.config['chemistry'] == baseline.config['chemistry']
            np.testing.assert_array_equal(sim.chemistry.pos, baseline.chemistry.pos)
            assert sim.chemistry.export() == baseline.chemistry.export()
            assert sim.rng.bit_generator.state == baseline.rng.bit_generator.state
            assert sim.dt*sim.config['engine']['sample_every'] == .5
            assert len(sim.chemistry.pos) == 2118
            rows.append(dict(seed=seed, factor=factor, same_laws_initial_state_rng=True,
                dt=sim.dt, reaction_interval=5*sim.dt, observation_interval=.5))
    return rows


def plan():
    return dict(name='N1 J3 common bath joint mechanical and reaction timestep refinement',
        workers=2, checkpoint_seconds=60, kinetic_window=25, record_trajectory=False,
        genetic_audit=True,
        comparison_policy='J3 k16 bath seeds0/1/2 at1200 reused as dt0.002 baseline. '
            'Six new tasks dt0.001/0.0005, reaction cadence remains5dt; observation0.5. '
            'Same resolved chemical parameters and constructed initial states/RNG. '
            'Shared seed labels are not coupled Brownian paths or extra independent samples. '
            'Joint temporal refinement, not isolation of integration versus reaction splitting.',
        tasks=[dict(scenario=scenario(factor, seed)) for factor in (2, 4) for seed in range(3)])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['plan', 'verify', 'pilot'])
    a = p.parse_args()
    if a.action == 'plan':
        (ROOT/'campaigns/numerical_refinement.json').write_text(
            json.dumps(plan(), indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    elif a.action == 'verify':
        print(json.dumps(verify()))
    else:
        from simulator.runner import run
        from scripts.reconstruct_experiment import export_recipe
        evidence, path = run(scenario(4, 0, duration=2.), ROOT/'research/engine_runs', record=False)
        export_recipe(path)
        print(path)
        if evidence['error']:
            raise SystemExit(1)
