"""Freeze two selected MIN1 replays, reference hashes and bounded observation."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.minimal_tool_followup import controller,digest
from scripts.campaign import prepare as prepare_campaign,export_recipe,status,validate
from simulator.campaign_io import read,write


def prepare():
    index=read(ROOT/'research/BATCH_32_RECIPES.json');job=Path(index['job']);cfg=controller.validate_job(job)
    baseline=Path(cfg['campaigns'][1]);manifest=validate(baseline);snap=status(baseline)
    if snap['controller_active'] or snap['counts']['complete']!=9:raise ValueError('MIN1 B must be complete')
    parent=ROOT/'outputs/minimal_diagnostic_campaigns';latest=parent/'latest.txt'
    if latest.exists():
        s=status(Path(latest.read_text().strip()))
        if s['controller_active'] or any(t['worker_active'] for t in s['tasks']):raise RuntimeError('Diagnostic already active')
    tasks=[];references={}
    for seed in (0,1):
        original=next(t for t in manifest['tasks'] if t['label']==f'MIN1_B_short_s{seed}')
        state=next(t for t in snap['tasks'] if t['id']==original['id'])
        result=baseline/state['result'];cp=result.parent/'checkpoint.npz';label=f'MIN1D_short_s{seed}'
        tasks.append(dict(label=label,scenario=original['scenario']))
        references[label]=dict(result=str(result),result_sha256=digest(result),checkpoint=str(cp),checkpoint_sha256=digest(cp))
    plan=dict(name='MIN1D selected exact replay with bounded molecular loupe',workers=2,checkpoint_seconds=30.,kinetic_window=25.,
        record_trajectory=False,genetic_audit=True,ligation_loupe={},tasks=tasks,references=references,
        comparison_policy='Two selected diagnostic replays, not independent replication; BATCH_33_PLAN. '
            'No altered laws, horizon or initial conditions. Stop after diagnosis, no third candidate.')
    path=ROOT/'campaigns/minimal_diagnostic.json';write(path,plan);folder=prepare_campaign(path,parent)
    recipe=ROOT/'research/campaign_recipes'/('MIN1D_'+folder.name.removeprefix('campaign_'));export_recipe(folder,recipe)
    write(ROOT/'research/BATCH_33_RECIPES.json',dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix(),
        reference_recipe=index['recipes'][1],reference_result_hashes={k:v['result_sha256'] for k,v in references.items()},
        plan='research/BATCH_33_PLAN.md',note='Only code, configs and hashes tracked; captures/checkpoints/results local.'))
    print(folder);return folder


if __name__=='__main__':prepare()
