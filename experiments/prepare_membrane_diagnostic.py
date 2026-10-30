"""Five predeclared early failure controls, retaining the chosen Langevin dynamics."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))


def plan():
    src=ROOT/'research/campaign_recipes/LT2_20261030T065759494210Z/manifest.json'
    reference=next(t['scenario'] for t in json.loads(src.read_text())['tasks'] if t['label']=='LT2_integrated_s0_langevin')
    tasks=[]
    for variant in ('base','brownian','no_random_off','no_exchange','fine'):
        cfg=copy.deepcopy(reference);cfg.update(name='MD1_'+variant,branch='MD1',duration=80.)
        if variant=='brownian':del cfg['mechanics']
        elif variant=='no_random_off':cfg['chemistry']['membrane']['bond_off_rate']=0.
        elif variant=='no_exchange':cfg['chemistry']['membrane']['contact_exchange_rate']=0.
        elif variant=='fine':
            cfg['engine']['dt']/=2;cfg['engine']['reaction_every']*=2;cfg['engine']['sample_every']*=2
        tasks.append(dict(scenario=cfg,preset=variant,comparison='fine' if variant=='fine' else 'base'))
    return dict(name='MD1 early membrane failure diagnostic',workers=2,checkpoint_seconds=30.,
        kinetic_window=10.,record_trajectory=False,demo_motion_report=True,
        comparison_policy='Five selected seed0 controls to80; no extra protein. Off-rate and exchange ablations are separate chemistry diagnostics, not adopted candidates. Fine mechanics preserves reaction/observer intervals. Unknown boundaries do not establish retention. No automatic parameter search.',tasks=tasks)


if __name__=='__main__':
    p=ROOT/'campaigns/membrane_diagnostic.json';p.write_text(json.dumps(plan(),indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(p)
