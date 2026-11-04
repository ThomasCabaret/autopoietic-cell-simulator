"""MIN1M: transfer the existing short assembler to the MD2 compartment."""
import copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_expression_campaign import baseline
from simulator.config import resolve


VARIANTS=('active','noL','split','nogene')


def scenario(seed,variant,duration=1200.):
    if variant not in VARIANTS:raise ValueError(variant)
    cfg=baseline(seed);c=cfg['chemistry'];g=c['genetics'];gene=variant!='nogene'
    # Keep MD2's 432 G and384 F supports, but prepare short G/F assemblies.
    # The removed seed symbol becomes a free precursor slot, not a new atom.
    g.update(sequence='01',free_units=430,template=gene,
        initial_assemblies=[dict(family=0,sequence='01',backbone=gene) for _ in range(15)]+
        [q for _ in range(16) for q in ([dict(family=1,sequence='01',backbone=variant!='split')]+
            [dict(family=1,sequence=b,backbone=False) for b in '0011'])])
    c['include_membrane']=variant!='noL'
    cfg.update(name=f'MIN1M_{variant}_s{seed}',branch='MIN1M',duration=duration)
    return resolve(cfg)


def plan():
    return dict(name='MIN1M short-tool reconstruction in the shared MD2 membrane bath',workers=2,
        checkpoint_seconds=30.,kinetic_window=25.,record_trajectory=False,genetic_audit=True,
        tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in VARIANTS],
        comparison_policy='BATCH_35_PLAN: same MD2 local laws/parameters, short initial assemblies. '
            'Matched PR positions/types for all controls; matched RNG for active/split/nogene. '
            'noL removes L and initializes a smaller Langevin velocity array, so post-initialization RNG differs. '
            'Original MD2 results reused descriptively, not a pure sequence-length intervention. '
            'Twelve finite-stock trials, t1200, no losses, no L synthesis, no automatic second phase.')
