"""N2: split mechanical refinement from reaction cadence, conditional on N1."""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_numerical_campaign import scenario as base
from simulator.engine import Simulation


def scenario(every,seed,duration=1200.):
    if every not in (10,20):raise ValueError(every)
    cfg=base(4,seed,duration)
    cfg.update(name=f'N2_every{every}',branch='N2')
    cfg['engine']['reaction_every']=every
    return cfg


def plan():
    return dict(name='N2 fixed fine mechanics, coarser reaction intervals conditional on N1 drift',
        workers=2,checkpoint_seconds=60,kinetic_window=25,record_trajectory=False,genetic_audit=True,
        comparison_policy='All six tasks dt0.0005, observation0.5, reaction_every10/20 '
            '(interval0.005/0.01),seeds0/1/2 to1200. Same J3 chemical laws and initial state. '
            'Compare N1 finest every5, plus J3 and N1 medium at matched reaction intervals. '
            'Run only if prospective N1 median alert to factor4, not selected successful seeds.',
        tasks=[dict(scenario=scenario(e,s)) for e in (10,20) for s in range(3)])


def verify():
    rows=[]
    for seed in range(3):
        a=Simulation(base(4,seed,2.))
        for every in (10,20):
            b=Simulation(scenario(every,seed,2.))
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            assert a.chemistry.export()==b.chemistry.export()
            assert a.rng.bit_generator.state==b.rng.bit_generator.state
            assert a.config['chemistry']==b.config['chemistry']
            rows.append(dict(seed=seed,reaction_every=every,dt=b.dt,interval=b.dt*every,matched=True))
    return rows


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['plan','verify']);a=p.parse_args()
    if a.action=='plan':
        (ROOT/'campaigns/cadence_controls.json').write_text(json.dumps(plan(),indent=2)+'\n',encoding='utf-8')
    else:print(json.dumps(verify()))
