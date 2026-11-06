"""PT1 independent constructed-frontier permeability assay, no active chemistry."""
import copy
from pathlib import Path
from simulator.config import resolve
from simulator.campaign_io import read
ROOT=Path(__file__).resolve().parents[1]
REFERENCE=ROOT/'research/campaign_recipes/CH1_20261106T073608844143Z'


def scenario(seed,variant):
    cfg=copy.deepcopy(next(q['scenario'] for q in read(REFERENCE/'manifest.json')['tasks'] if q['label']=='CH1_integrated_s1'))
    cfg.update(name=f'PT1_{variant}_s{seed}',branch='PT1',seed=seed,duration=300.)
    c=cfg['chemistry'];c.update(food_units=0,rung_formation_rate=0.,rung_catalytic_rate=0.)
    c['genetics'].update(sequence='01',free_units=46,function_units=0,template=False,ligation=False,
        initial_assemblies=[dict(family=0,sequence='0',backbone=False) for _ in range(16)])
    if variant=='transparent':c['bound_barrier_radius']=0.
    elif variant!='barrier':raise ValueError(variant)
    return resolve(cfg)


def preflight():
    import numpy as np
    from simulator.engine import Simulation
    from simulator.membrane_bath import in_polygon
    rows=[]
    for seed in range(3):
        a,b=Simulation(scenario(seed,'barrier')),Simulation(scenario(seed,'transparent'))
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        if a.rng.bit_generator.state!=b.rng.bit_generator.state:raise ValueError('Initial RNG differs')
        c=a.chemistry;g=c.host;bound=np.zeros(c.prefix,dtype=bool);bound[g.rungs[g.rungs[:,1]>=0].reshape(-1)]=True
        # Order the prepared contour geometrically for initialization-only QA.
        points=c.pos[c.initial_boundary_heads]
        if len(c.pos)!=200 or bound.sum()!=36 or (~bound).sum()!=60 or not in_polygon(c.pos[:c.prefix],points).all():raise ValueError('Invalid transport cohorts/start')
        if g.edges or c.config['rung_formation_rate'] or c.config['rung_catalytic_rate'] or len(g.families[g.families==1]):raise ValueError('Transport chemistry not isolated')
        rows.append(dict(seed=seed,atoms=len(c.pos),bound_atoms=int(bound.sum()),free_atoms=int((~bound).sum()),all_initially_inside=True,paired_initial_conditions=True))
    return rows


def plan():
    checks=preflight()
    return dict(name='PT1 independent selective retention with constructed CP1 boundary',workers=1,checkpoint_seconds=30.,
        kinetic_window=25.,record_trajectory=False,preflight=checks,
        tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in ('barrier','transparent')],
        comparison_policy='BATCH_53_PLAN PT1: prepared52L,18PR dimers+60 free atoms, same CP1 L laws; births/ligation off in both variants. '
            'Only barrier radius .55 vs0 changes; paired initialization, six300 trials, one worker/two-hour cap, report then stop. No self-assembly, sealing or maintenance proof.')
