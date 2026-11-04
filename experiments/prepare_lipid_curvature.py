"""L3 fixed pose/curvature comparison with three reused L2 references."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_lipid_energy import scenario as previous
from simulator.config import resolve

VARIANTS=('reference','pose','curvature','combined','split','no_boost','no_tool')
REFERENCE=ROOT/'research/campaign_recipes/L2_20261104T122737643199Z'


def scenario(seed,variant):
    if variant not in VARIANTS:raise ValueError(variant)
    cfg=previous(seed,'combined' if variant in ('reference','pose','curvature','combined') else variant)
    g=cfg['chemistry'];g['capture_curvature']='legacy' if variant in ('reference','pose') else 'matched'
    g['tool_pose']='straight' if variant in ('reference','curvature') else 'native'
    cfg.update(name=f'L3_{variant}_s{seed}',branch='L3');return resolve(cfg)


def plan(reference_folder):
    from scripts.campaign import validate,digest
    validate(reference_folder)
    return dict(name='L3 capture curvature and constructed native pose',workers=1,checkpoint_seconds=30.,record_trajectory=False,
        tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in VARIANTS if v!='reference'],
        reused_reference=dict(campaign=str(reference_folder),manifest_sha256=digest(reference_folder/'manifest.json')),
        comparison_policy='BATCH_38_PLAN:18 new cases plus reused L2_combined x3, t100, one worker,1h wall budget. '
            'Fixed rates/thermostat and local derived capture stiffness; prepared native pose is initialization only. '
            'No new protein, retries, rate search, follow-up or automatic promotion.')
