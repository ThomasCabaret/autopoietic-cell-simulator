"""RP1 single protection-predicate change; historical RV1 material/rates fixed."""
import copy
from pathlib import Path
from simulator.config import resolve
from simulator.campaign_io import read
ROOT=Path(__file__).resolve().parents[1]
REFERENCE=ROOT/'research/campaign_recipes/RV1A_20261031T080348730984Z'


def scenario(seed):
    cfg=copy.deepcopy(next(t['scenario'] for t in read(REFERENCE/'manifest.json')['tasks'] if t['label']==f'RV1_protected_s{seed}'))
    cfg.update(name=f'RP1_pair_s{seed}',branch='RP1')
    cfg['chemistry']['bond_turnover']['protection_scope']='paired_edge';return resolve(cfg)


def plan():
    return dict(name='RP1 coherent paired-edge protection, fixed RV1 rates',workers=1,
        checkpoint_seconds=30.,kinetic_window=50.,record_trajectory=False,
        tasks=[dict(scenario=scenario(s)) for s in range(3)],
        comparison_policy='BATCH_48_PLAN: one local predicate variant, historical RV1 references reused descriptively. '
            'Current-state reversible census only, no lineage or gene-name protection. Three1200 trials, report then stop; no tuning/retry/transfer.')
