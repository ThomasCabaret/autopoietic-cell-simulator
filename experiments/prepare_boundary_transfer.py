"""BI1 true H/T synthesis and insertion into a constructed common-law ring."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_cooperative_synthesis import scenario as previous
from simulator.config import resolve

VARIANTS=('active','noexchange','nosynthesis')


def scenario(seed,variant,duration=1200.):
    if variant not in VARIANTS:raise ValueError(variant)
    cfg=previous(seed,'cooperative',duration);c=cfg['chemistry']
    c.update(box=[90.,90.],initial_boundary=dict(units=219,radius=34.5,
        packet_box=[12.,9.],packet_offset=[27.5,0.]),bound_barrier_radius=.55,bound_barrier_stiffness=80.)
    if variant=='noexchange':c['contact_exchange_rate']=0.
    if variant=='nosynthesis':c['rung_formation_rate']=c['rung_catalytic_rate']=0.
    # Rates are shared with P/R, so this control suppresses BOTH syntheses.
    # It is an attribution negative, not an isolated causal effect on H/T.
    cfg.update(name=f'BI1_{variant}_s{seed}',branch='BI1');return resolve(cfg)


def plan():
    return dict(name='BI1 synthesized lipids and constructed common-law frontier',workers=2,
        checkpoint_seconds=30.,kinetic_window=25.,record_trajectory=False,
        tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in VARIANTS],
        comparison_policy='BATCH_43_PLAN:9 trials at1200,636 beads, finite local precursor packet '
            'near a constructed219-L frontier. Same initial coordinates/velocities/RNG. '
            'Local segment barrier uses only actual P/R bonds. Birth-triggered passive samples. '
            'Nosynthesis turns off shared PR and HT rates, not an isolated HT intervention. '
            'No feed/loss/new tool, automatic tuning, retry or GUI adoption.')
