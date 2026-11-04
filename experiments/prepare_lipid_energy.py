"""L2 fixed two-factor mechanism comparison plus prospective negative controls."""
import copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve
from simulator.campaign_io import read


VARIANTS=('reference','gate','compatible','combined','split','no_boost','no_tool')
REFERENCE=ROOT/'research/campaign_recipes/L1P_20261104T115550305191Z'


def scenario(seed,variant):
    if variant not in VARIANTS:raise ValueError(variant)
    cfg=copy.deepcopy(read(REFERENCE/'manifest.json')['tasks'][0]['scenario']);g=cfg['chemistry']
    g['formation_gate']='none' if variant in ('reference','compatible') else 'metropolis'
    g['tool_lipid_contact']=.55 if variant in ('reference','gate') else 0.
    if variant=='split':g['tool_linked']=False
    if variant=='no_boost':g['rung_catalytic_rate']=g['rung_formation_rate']
    if variant=='no_tool':g['tool_count']=0
    cfg.update(seed=seed,name=f'L2_{variant}_s{seed}',branch='L2');return resolve(cfg)


def plan(reference_folder):
    from scripts.campaign import digest,validate
    m=validate(reference_folder)
    return dict(name='L2 local energy and capture-compatible contacts',workers=1,checkpoint_seconds=30.,
        record_trajectory=False,tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in VARIANTS if (s,v)!=(0,'reference')],
        reused_reference=dict(campaign=str(reference_folder),manifest_sha256=digest(reference_folder/'manifest.json')),
        comparison_policy='BATCH_37_PLAN:20 new tasks plus exactly reused original L1 seed0,3 seeds x7 conditions, '
            't100,one worker,1h wall budget. No automatic follow-up, retries or promotion. '
            'Two-factor comparison and combined split/no_boost/no_tool; latter has different atom count and RNG.')
