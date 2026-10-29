"""Transfer the selected Langevin candidate to frozen P10 reactions, without changing them."""
import argparse
import copy
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))


def scenario(mode='copy',seed=0,duration=3200.):
    manifest=json.loads((ROOT/'research/campaign_recipes/P10_20261029T120049792477Z/manifest.json').read_text())
    ref=next(t['scenario'] for t in manifest['tasks'] if t['label']==f'P10_{mode}_reserve1' and t['scenario']['seed']==seed)
    cfg=copy.deepcopy(ref)
    cfg.update(name=f'LT1_{mode}',branch='LT1',duration=duration,
        mechanics=dict(motion='langevin',mass=1.,damping=.1,dpd_cutoff=1.))
    return cfg


def plan(pilot=False):
    return dict(name='LT1 reactive Langevin pilot' if pilot else 'LT1 motion-to-copy transfer under unchanged P10 reactions',
        workers=2,checkpoint_seconds=30.,kinetic_window=50.,record_trajectory=False,
        population_audit=True,population_interval=10.,genetic_audit=True,
        comparison_policy='Selected Langevin gamma0.1 candidate from MIX2; not an independent model-selection validation. P10 reactions, physical temperature0.6, dt0.005, stocks, initial positions and external release cycle unchanged. Only motion/velocities differ. Brownian references P10 tasks0000-0005 explicitly reused; no initial-clearance packing substituted. G-only and F-only baths remain separate. No membrane, no extra enzyme or gene.',
        tasks=[dict(scenario=scenario(mode,seed,20. if pilot else 3200.)) for seed in (range(1) if pilot else range(3)) for mode in ('copy','expression')])


def verify_brownian():
    import numpy as np
    from simulator.engine import Simulation
    folder=ROOT/'outputs/population_pilots/campaign_20261029T115659494627Z'
    state=json.loads((folder/'tasks/task0000/state.json').read_text())
    with np.load(folder/state['checkpoint'],allow_pickle=False) as data:
        metadata=json.loads(str(data['metadata']));sim=Simulation(metadata['config']);sim.advance(metadata['step'])
        np.testing.assert_array_equal(sim.chemistry.pos,data['positions'])
    if sim.rng.bit_generator.state!=metadata['rng'] or json.loads(json.dumps(sim.chemistry.export()))!=metadata['chemistry']:
        raise AssertionError('The unchanged Brownian reference has drifted')
    print(json.dumps(dict(original_P10_prefix_identical=True,time=sim.time,beads=len(sim.chemistry.pos))))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--pilot',action='store_true');p.add_argument('--verify-brownian',action='store_true');p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.verify_brownian:verify_brownian()
    else:
        if a.output is None:p.error('--output required')
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(plan(a.pilot),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
