"""Freeze unchanged J0 genetic controls with a read-only opportunity audit."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))


def plan(long=False):
    reference=json.loads((ROOT/'research/campaign_recipes/J0_20261027T113835658766Z/manifest.json').read_text(encoding='utf-8'))
    tasks=[]
    for t in reference['tasks']:
        cfg=t['scenario']
        if cfg['name'] not in (('J0_cold',) if long else ('J0_native','J0_cold')):continue
        if long:cfg['duration']=3200.
        tasks.append(dict(label=cfg['name'],scenario=cfg))
    return dict(name='GKA cold follow-up all seeds to3200' if long else 'GKA source-exact J0 native/cold opportunity diagnosis',
        workers=2,checkpoint_seconds=60,kinetic_window=25,record_trajectory=False,genetic_audit=True,
        comparison_policy='Unchanged physical laws. Pre-reaction opportunities are approximate, no feedback. All cold seeds in any3200 follow-up; retain the censored400 results separately.',tasks=tasks)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--long',action='store_true');p.add_argument('--output',type=Path)
    a=p.parse_args();target=a.output or ROOT/('campaigns/genetic_cold_long.json' if a.long else 'campaigns/genetic_kinetics.json')
    target.write_text(json.dumps(plan(a.long),indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(target)
