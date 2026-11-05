"""CB1 analytically scaled short-tool compartment, no new chemical helper."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_boundary_transfer import scenario as previous
from simulator.config import resolve
VARIANTS=('active','noL','nosynthesis')


def scenario(seed,variant,duration=2400.):
    if variant not in VARIANTS:raise ValueError(variant)
    cfg=previous(seed,'nosynthesis' if variant=='nosynthesis' else 'active',duration);c=cfg['chemistry']
    c.update(box=[22.,22.],short_length=.92,initial_boundary=dict(units=0 if variant=='noL' else 52,
        radius=8.,packet_box=[12.,9.],packet_offset=[0.,0.]))
    cfg.update(name=f'CB1_{variant}_s{seed}',branch='CB1');return resolve(cfg)


def plan():
    return dict(name='CB1 compact common-law material transfer',workers=2,checkpoint_seconds=30.,
        kinetic_window=25.,record_trajectory=False,tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in VARIANTS],
        comparison_policy='BATCH_44_PLAN:9 tasks at2400.52 prepared L, radius8,22x22 world, '
            'original12x9 centered packet.302 atoms,198 noL. short_length.92 analytically chosen '
            'from curvature, changed from BI1.98; other laws/rates/thermostat fixed. '
            'NoL same initial packet coordinates but smaller velocity array and different post-motion RNG. '
            'Nosynthesis disables shared PR/HT rates. No new tool/feed/loss/retry/tuning/promotion.')
