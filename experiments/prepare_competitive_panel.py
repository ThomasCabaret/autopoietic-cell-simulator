"""CC1 first dynamic panel: same L laws, integrated and isolated-molecule baths."""
import copy,math
from pathlib import Path
import numpy as np
from simulator.config import resolve
from simulator.campaign_io import read
from experiments.prepare_contact_gate import scenario as previous
ROOT=Path(__file__).resolve().parents[1]
REFERENCE=ROOT/'research/campaign_recipes/EG1_20261105T131525540618Z'


def scenario(seed,variant):
    cfg=previous(seed,'coarse');cfg['chemistry']['free_port_potential']='competitive'
    cfg.update(name=f'CC1_{variant}_s{seed}',branch='CC1',duration=300.)
    if variant=='assembly':
        from simulator.lipid_synthesis import DEFAULTS
        chem={k:copy.deepcopy(v) for k,v in cfg['chemistry'].items() if k in DEFAULTS}
        chem.update(tool_count=0,food_units=52,box=[22.,22.])
        rng=np.random.default_rng(seed+5000);centres=[];molecules=[]
        for _ in range(52):
            for attempt in range(100000):
                point=rng.uniform([1.2,1.2],[20.8,20.8])
                if all(np.linalg.norm(point-other)>=1.1 for other in centres):break
            else:raise ValueError('Cannot disperse52 isolated molecules')
            centres.append(point);angle=rng.uniform(0.,2*math.pi);axis=.325*np.array([math.cos(angle),math.sin(angle)])
            molecules.append(dict(head=(point-axis).tolist(),tail=(point+axis).tolist()))
        chem['initial_lipids']=molecules;cfg.update(model='lipid_synthesis',chemistry=chem)
    elif variant!='integrated':raise ValueError(variant)
    return resolve(cfg)


def plan():
    from experiments.benchmark_competitive_ports import benchmark
    result=benchmark()
    if not result['screen_passed']:raise ValueError('Competitive kernel cost gate refused; inspect before campaign')
    return dict(name='CC1 first competitive dynamics and isolated L assembly',workers=2,
        checkpoint_seconds=30.,kinetic_window=25.,record_trajectory=False,
        tasks=[dict(scenario=scenario(seed,variant)) for variant in ('integrated','assembly') for seed in range(3)],
        comparison_policy='BATCH_50_PLAN: one competitive law, short300-time panel. Integrated finite bath and reduced H/T-only bath with52 prepared isolated dimers. '
            'Same L kernel/constants; no prepared lateral chain/contour. First dynamics require interpretation after report, no auto long campaign, retry or promotion.')
