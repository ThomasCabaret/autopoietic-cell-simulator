"""RF1 actual01 gene/co-recruiter, current genetic laws and existing RV1 helpers."""
import copy
from pathlib import Path
from simulator.config import resolve
from simulator.campaign_io import read
from simulator.mixed_synthesis import genetics_config
ROOT=Path(__file__).resolve().parents[1]
REFERENCE=ROOT/'research/campaign_recipes/CH1_20261106T073608844143Z'
RATES=dict(backbone_g=.00005,backbone_f=.001,rung_g=.001,rung_f=.01,protection=.05)


def scenario(seed,variant):
    old=next(q['scenario'] for q in read(REFERENCE/'manifest.json')['tasks'] if q['label']=='CH1_integrated_s1')
    g=genetics_config(old['chemistry']);g['box']=[12.,9.]
    rates=copy.deepcopy(RATES)
    if variant=='zero':rates.update({k:0. for k in ('backbone_g','backbone_f','rung_g','rung_f')})
    elif variant not in ('occupied','paired_edge'):raise ValueError(variant)
    rates['protection_scope']='paired_edge' if variant=='paired_edge' else 'occupied';g['bond_turnover']=rates
    return resolve(dict(schema_version=1,model='copy',name=f'RF1_{variant}_s{seed}',branch='RF1',seed=seed,duration=1200.,
        chemistry=g,mechanics=copy.deepcopy(old['mechanics']),engine=copy.deepcopy(old['engine'])))


def plan():
    return dict(name='RF1 actual01 functional recycling, existing protection alternatives',workers=1,
        checkpoint_seconds=30.,kinetic_window=50.,record_trajectory=False,
        tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in ('zero','occupied','paired_edge')],
        comparison_policy='BATCH_53_PLAN RF1: same01 current genetic laws/initial stock in12x9, no L/HT. '
            'Three seeds x zero/occupied/paired_edge at fixed RV1 rates,1200. Current-state census and actual late catalysis; '
            'functional motifs separate from exact target. One worker/two-hour cap, report then stop; no tuning, transfer or homeostasis claim.')
