"""MIN1R: existing constructed F01 versus exact split/nogene controls."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_minimal_tool_campaign import expression
from simulator.config import resolve
from simulator.campaign_io import read,write
from scripts.campaign import prepare as prepare_campaign,export_recipe,status


def scenario(seed,variant,duration=1200.):
    if variant not in ('active','split','nogene'):raise ValueError(variant)
    cfg=expression(seed,'short',duration);g=cfg['chemistry'];gene=variant!='nogene'
    g.update(template=gene,initial_assemblies=[dict(family=0,sequence='01',backbone=gene) for _ in range(3)]+
        [dict(family=1,sequence='01',backbone=variant!='split')]+
        [dict(family=1,sequence=b,backbone=False) for b in '0011'])
    cfg.update(name=f'MIN1R_{variant}_s{seed}',branch='MIN1R');return resolve(cfg)


def plan():
    return dict(name='MIN1R actual food-derived renewal from a constructed start',workers=2,checkpoint_seconds=30.,
        kinetic_window=25.,record_trajectory=False,tasks=[dict(scenario=scenario(s,v)) for s in range(3) for v in ('active','split','nogene')],
        comparison_policy='BATCH_34_PLAN: same MD2 laws, matched atoms/symbols/positions/RNG; only initial F/G bonds differ. '
            'Wholly food-derived active new tool required, prepared tool excluded. Finite stock, no homeostasis or third phase.')


def prepare():
    from experiments.review_minimal_diagnostic import review
    _,report=review()
    if report['controller_active'] or report['counts']['complete']!=2 or any(not r['physical_replay_exact'] for r in report['rows']):
        raise RuntimeError('Require both validated diagnostic replays complete')
    parent=ROOT/'outputs/renewal_campaigns';latest=parent/'latest.txt'
    if latest.exists():
        s=status(Path(latest.read_text().strip()))
        if s['controller_active'] or any(t['worker_active'] for t in s['tasks']):raise RuntimeError('Renewal work already active')
    p=ROOT/'campaigns/minimal_renewal.json';write(p,plan());folder=prepare_campaign(p,parent)
    recipe=ROOT/'research/campaign_recipes'/('MIN1R_'+folder.name.removeprefix('campaign_'));export_recipe(folder,recipe)
    write(ROOT/'research/BATCH_34_RECIPES.json',dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix(),
        plan='research/BATCH_34_PLAN.md',note='Configurations and frozen code only; raw results local, no automatic follow-up.'))
    print(folder);return folder


if __name__=='__main__':prepare()
