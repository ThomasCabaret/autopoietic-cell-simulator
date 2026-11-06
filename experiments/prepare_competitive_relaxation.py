"""CR1 same-law isolated runs, horizon justified by bare-backbone modes."""
import copy,json,math
from pathlib import Path
from simulator.config import resolve
ROOT=Path(__file__).resolve().parents[1]
REFERENCE=ROOT/'research/campaign_recipes/CH1_20261106T073608844143Z'


def scenario(seed):
    manifest=json.loads((REFERENCE/'manifest.json').read_text())
    cfg=copy.deepcopy(next(q['scenario'] for q in manifest['tasks'] if q['label']==f'CH1_assembly_s{seed}'))
    cfg.update(name=f'CR1_assembly_s{seed}',branch='CR1',duration=8000.);return resolve(cfg)


def plan():
    from scripts.campaign import digest
    evidence=ROOT/'research/BATCH_51_BC1.json';bc=json.loads(evidence.read_text())
    summary=bc['summary']
    if summary['local_profile']['engine_energy_max_error']>1e-12 or len(summary.get('bare_modes',[]))!=4:raise ValueError('Require verified BC1 mode analysis')
    return dict(name='CR1 same-law isolated relaxation and sampled closure',workers=2,checkpoint_seconds=30.,kinetic_window=50.,
        record_trajectory=False,lipid_geometry_audit=dict(interval=5.,min_units=26,min_area=.25*math.pi*8.325**2,max_samples=2001),
        tasks=[dict(scenario=scenario(seed)) for seed in range(3)],
        mode_evidence_sha256=digest(evidence),comparison_policy='BATCH_51_RELAXATION_PLAN: fixed CP1/CH1 laws, isolated initial molecules unchanged; '
            'three selected seeds8000 justified by slow bare mode1890. Passive sampled geometry, one coordinate capture, no feedback. '
            'Three-hour budget then report/stop; no retry, automatic horizon increase or physical tuning.')
