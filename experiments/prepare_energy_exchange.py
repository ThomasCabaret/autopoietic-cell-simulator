"""EG1 existing CW1 candidate plus a finite-neighborhood exchange energy gate."""
import copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve
from simulator.campaign_io import read
REFERENCE=ROOT/'research/campaign_recipes/CW1_20261105T115432485306Z'


def scenario(seed,duration=2400.):
    old=next(t['scenario'] for t in read(REFERENCE/'manifest.json')['tasks'] if t['scenario']['seed']==seed)
    cfg=copy.deepcopy(old);cfg['chemistry']['contact_exchange_gate']='metropolis'
    cfg.update(name=f'EG1_energy_s{seed}',branch='EG1',duration=duration);return resolve(cfg)


def plan():
    descriptor=read(ROOT/'research/BATCH_45_WIDE_RECIPES.json');job=Path(descriptor['job']);state=read(job/'state.json')
    report=read(state['report_0']);reference=[{k:r[k] for k in ('seed','G_new','F_new','L_new','result_sha256')} for r in report['rows']]
    return dict(name='EG1 energy-gated exchange at unchanged CW1 width and thermostat',workers=2,
        checkpoint_seconds=30.,kinetic_window=25.,record_trajectory=False,
        tasks=[dict(scenario=scenario(seed)) for seed in range(3)],reference_cases=reference,
        comparison_policy='BATCH_46_PLAN:3 selected2400-unit followups. CW1 stocks/width.6/rates/'
            'noise/dt fixed, one local Metropolis gate on total affected L-port and PR-segment '
            'potential. Same initial coordinates/velocities/RNG; extra acceptance draws alter '
            'later RNG. No new tool/type/port/rate, no automatic retry/tuning/adoption. '
            'P/R synthesis, spontaneous contact loss and external cycle still explicit helpers.')
