"""MX1 frozen shared-site competition and downstream material-transfer test."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_capture_transfer import scenario as genetic_scenario
from simulator.mixed_synthesis import SHARED
from simulator.config import resolve

VARIANTS=('mixed','uncaptured','noHT','nogene')
REFERENCE=ROOT/'research/campaign_recipes/CT1_20261104T174449362677Z'


def scenario(seed,variant,duration=1200.):
    if variant not in VARIANTS:raise ValueError(variant)
    cfg=genetic_scenario(seed,'nogene' if variant=='nogene' else 'matched',duration)
    g=cfg['chemistry'];cfg.update(model='mixed_synthesis',name=f'MX1_{variant}_s{seed}',branch='MX1')
    cfg['chemistry']=dict(genetics={k:v for k,v in g.items() if k not in SHARED},
        **{k:g[k] for k in SHARED},food_units=0 if variant=='noHT' else 24,
        lipid_capture=variant!='uncaptured',formation_gate='metropolis',tool_lipid_contact=0.)
    return resolve(cfg)


def plan():
    return dict(name='MX1 one shared capture pool P/R/H/T and functional product transfer',workers=2,
        checkpoint_seconds=30.,kinetic_window=25.,record_trajectory=False,
        tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in VARIANTS],
        comparison_policy='BATCH_41_PLAN:12 trials,t1200,198 beads (150 without H/T). '
            'One saturable F-site pool, same capture law/rates for P/R/H/T. '
            'Uncaptured H/T is an explicit capture ablation, background chemistry retained. '
            'Matched coordinates/RNG before Langevin for mixed/uncaptured/nogene; noHT velocities differ. '
            'No membrane, feed, loss, new tool or native-pose preparation. '
            'P/R helper unchanged, H/T uses local energy gate as L3. No automatic second phase or promotion.')
