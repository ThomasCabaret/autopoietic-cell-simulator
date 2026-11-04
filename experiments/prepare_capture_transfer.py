"""CT1: transfer the H/T capture curvature to short genetic renewal."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_renewal_campaign import scenario as previous
from simulator.config import resolve

VARIANTS=('legacy','matched','nogene')
REFERENCE=ROOT/'research/campaign_recipes/MIN1R_20261031T110654015735Z'


def scenario(seed,variant,duration=1200.):
    if variant not in VARIANTS:raise ValueError(variant)
    cfg=previous(seed,'nogene' if variant=='nogene' else 'active',duration)
    if variant!='legacy':cfg['chemistry']['capture_curvature']='matched'
    cfg.update(name=f'CT1_{variant}_s{seed}',branch='CT1')
    return resolve(cfg)


def plan():
    return dict(name='CT1 common capture-law prerequisite for P/R/H/T',workers=2,
        checkpoint_seconds=30.,kinetic_window=25.,record_trajectory=False,genetic_audit=True,
        tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in VARIANTS],
        comparison_policy='BATCH_40_PLAN: nine trials to1200, same150 beads, initial coordinates, velocities, '
            'rates and thermostat. Capture k=35 versus E/width²; matched nogene removes only initial G edges. '
            'No native-pose initializer, lipid synthesis, new protein or automatic follow-up. '
            'Recompute legacy references under the same frozen sources; not a mixed-bath result.')
