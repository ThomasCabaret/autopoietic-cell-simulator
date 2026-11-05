"""EN1: half mechanical step, identical physical chemistry/sample cadence."""
import copy
from pathlib import Path
from simulator.config import resolve
from simulator.campaign_io import read
ROOT=Path(__file__).resolve().parents[1]
REFERENCE=ROOT/'research/campaign_recipes/EG1_20261105T131525540618Z'


def scenario(seed):
    cfg=copy.deepcopy(next(t['scenario'] for t in read(REFERENCE/'manifest.json')['tasks'] if t['scenario']['seed']==seed))
    cfg.update(name=f'EN1_fine_s{seed}',branch='EN1')
    cfg['engine']['dt']/=2
    for key in ('reaction_every','sample_every'):cfg['engine'][key]*=2
    return resolve(cfg)


def plan():
    job=Path(read(ROOT/'research/BATCH_46_EG1_RECIPES.json')['job']);s=read(job/'state.json')
    from scripts.campaign import digest
    if s['phase']!='needs_interpretation' or digest(s['report_0'])!=s['report_0_sha256']:raise ValueError('Require unchanged complete EG1 report')
    report=read(s['report_0'])
    if not report['decision']['screen_passed']:raise ValueError('Require EG1 passed before refinement')
    keys=('seed','G_new','F_new','L_new','valid_fraction_late','late_temperature','inserted_born_inside')
    return dict(name='EN1 fixed EG1 chemistry, half mechanical step',workers=2,checkpoint_seconds=30.,
        kinetic_window=25.,record_trajectory=False,tasks=[dict(scenario=scenario(s)) for s in range(3)],
        reference_cases=[{k:r[k] for k in keys} for r in report['rows']],
        comparison_policy='BATCH_47_PLAN: dt halved, reaction/sample counts doubled; physical cadences fixed. '
            'Three selected sensitivity checks, not matched trajectories or numerical convergence proof. Report then stop, no tuning or retry.')
