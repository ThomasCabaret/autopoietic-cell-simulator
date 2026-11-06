"""FR1: recover the existing F01 tool from constructed post-cleavage starts."""
from experiments.prepare_functional_recycling import scenario as original,REFERENCE
from simulator.config import resolve


def scenario(seed,variant):
    cfg=original(seed,'occupied');cfg.update(name=f'FR1_{variant}_s{seed}',branch='FR1',duration=600.)
    for group in cfg['chemistry']['initial_assemblies']:
        if group['family']==1:group['backbone']=False
    if variant=='slow':cfg['chemistry']['bond_turnover']['rung_f']=.001
    elif variant!='fast':raise ValueError(variant)
    return resolve(cfg)


def plan():
    return dict(name='FR1 existing co-recruiter recovery after constructed backbone cleavage',workers=2,
        checkpoint_seconds=30.,kinetic_window=25.,record_trajectory=False,genetic_audit=True,
        tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in ('fast','slow')],
        comparison_policy='BATCH_54_PLAN: no F backbone initially, G01 and150 atoms unchanged; only rung_f .01 versus .001 differs. '
            'Six600 trials,2 workers/1h, fixed recovery gate then report/stop. No whole-atom recycling, persistence, open feed or CP1 adoption claim.')
