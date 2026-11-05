"""CX1 three predeclared no-exchange controls of completed CB1, no new law."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve
REFERENCE=ROOT/'research/campaign_recipes/CB1_20261105T092857284853Z'


def scenario(seed,wide=False):
    tasks=json.loads((REFERENCE/'manifest.json').read_text())['tasks']
    cfg=copy.deepcopy(next(t['scenario'] for t in tasks if t['label']==f'CB1_active_s{seed}'))
    if wide:cfg['chemistry']['dock_width']=.6
    else:cfg['chemistry']['contact_exchange_rate']=0.
    cfg.update(name=f'CW1_wide_s{seed}' if wide else f'CX1_noexchange_s{seed}',branch='CW1' if wide else 'CX1');return resolve(cfg)


def plan(baseline,wide=False):
    return dict(name='CW1 wider free-port basin and derived bonded curvature' if wide else 'CX1 same compact chemistry without associative exchange',workers=2,
        checkpoint_seconds=30.,kinetic_window=25.,record_trajectory=False,
        tasks=[dict(scenario=scenario(seed,wide)) for seed in range(3)],reference_cases=baseline,
        comparison_policy=('BATCH_45_PLAN CW1 selected followup: dock_width.6 instead of.3 only, '
            'same initial stocks/positions/velocities/RNG; bonded curvature derived from width, '
            'no rate/thermostat/helper change. Three active variants at2400, compare reused CB1 '
            'references. No new controls for all downstream functions or general adoption. '
            'Report then stop, no tuning/retry/second phase.') if wide else 'BATCH_45_PLAN: three new controls at2400. Same CB1 initial atoms, '
            'coordinates, velocities and RNG, only contact_exchange_rate zero. Subsequent RNG '
            'differs because the ablated rule consumes no draws. Reuse three completed CB1 '
            'active cases descriptively; no rerun, second phase, tuning, retry or adoption.')
