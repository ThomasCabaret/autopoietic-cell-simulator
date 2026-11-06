"""CH1 selected horizon extension, no changed local laws or initial material."""
import copy,math
from pathlib import Path
from simulator.config import resolve
from simulator.campaign_io import read
from scripts.campaign import digest
ROOT=Path(__file__).resolve().parents[1]
REFERENCE=ROOT/'research/campaign_recipes/CC1_20261106T071431955883Z'


def scenario(seed,variant):
    cfg=copy.deepcopy(next(t['scenario'] for t in read(REFERENCE/'manifest.json')['tasks'] if t['label']==f'CC1_{variant}_s{seed}'))
    cfg.update(name=f'CH1_{variant}_s{seed}',branch='CH1',duration=1800.);return resolve(cfg)


def plan():
    job=Path(read(ROOT/'research/BATCH_50_CC1_RECIPES.json')['job']);s=read(job/'state.json');p=Path(s['report_0'])
    if s['phase']!='needs_interpretation' or digest(p)!=s['report_0_sha256']:raise ValueError('Require completed unchanged CC1')
    return dict(name='CH1 selected same-law assembly/closure horizon',workers=2,checkpoint_seconds=30.,
        kinetic_window=50.,record_trajectory=False,
        tasks=[dict(scenario=scenario(seed,'assembly')) for seed in range(3)]+[dict(scenario=scenario(1,'integrated'))],
        selected_reference_report=str(p),selected_reference_sha256=digest(p),minimum_contour_area=.25*math.pi*8.325**2,
        comparison_policy='BATCH_50_HORIZON_PLAN selected followup: identical laws and initial states,1800 instead of300. '
            'Three isolated cases, only failed integrated seed1. Final geometric witness, not first passage or permanence. Four trials/2h, report then stop, no tuning/retry.')
