"""MX2 one local capture change with matched longer horizons and controls."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_mixed_synthesis import scenario as previous
from simulator.config import resolve

VARIANTS=('cooperative','reference','nogene','noHT')
REFERENCE=ROOT/'research/campaign_recipes/MX1_20261104T192816403023Z'


def scenario(seed,variant,duration=2400.):
    if variant not in VARIANTS:raise ValueError(variant)
    cfg=previous(seed,variant if variant in ('nogene','noHT') else 'mixed',duration)
    cfg['chemistry']['capture_cooperativity']=variant!='reference'
    cfg.update(name=f'MX2_{variant}_s{seed}',branch='MX2');return resolve(cfg)


def plan():
    return dict(name='MX2 local capture cooperativity and selected horizon calibration',workers=2,
        checkpoint_seconds=30.,kinetic_window=25.,record_trajectory=False,
        tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in VARIANTS],
        comparison_policy='BATCH_42_PLAN:12 fixed trials,2400 units,198/150 beads. '
            'Same initial stocks/coordinates/velocities/RNG for reference/cooperative/nogene. '
            'Reference is a selected MX1 fixed-law longer horizon, not independent validation. '
            'One local neighboring-site compatibility condition, fixed rates and thermostat; '
            'no new protein, additional feed, second phase, tuning, retry or automatic adoption.')
