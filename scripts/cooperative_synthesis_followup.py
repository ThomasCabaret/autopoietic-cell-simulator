"""MX2 bounded adapter, reusing the source-frozen simulation/campaign controller."""
import argparse,json,shutil,sys,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import expression_followup as controller
from scripts.campaign import prepare as prepare_campaign,export_recipe
from simulator.campaign_io import read,write
from experiments.review_cooperative_synthesis import collect,decide


def latest():return Path((ROOT/'outputs/cooperative_synthesis_followups/latest.txt').read_text().strip())


def prepare():
    from experiments.prepare_cooperative_synthesis import plan,REFERENCE
    previous=Path(read(ROOT/'research/BATCH_41_RECIPES.json')['job']);s=controller.status(previous)
    if s['active'] or s['campaigns'][0]['controller_active'] or s['campaigns'][0]['counts']['complete']!=12:
        raise RuntimeError('Require complete inactive MX1 before MX2')
    evidence=Path(s['state']['report_0'])
    if controller.digest(evidence)!=s['state']['report_0_sha256']:raise RuntimeError('MX1 gate evidence changed')
    old_folder=Path(read(previous/'job.json')['campaigns'][0])
    parent=ROOT/'outputs/cooperative_synthesis_followups';parent.mkdir(parents=True,exist_ok=True)
    if (parent/'latest.txt').exists():
        s=controller.status(latest())
        if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):raise RuntimeError('MX2 already active')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');job=parent/('followup_'+stamp);job.mkdir()
    p=ROOT/'campaigns/cooperative_synthesis.json';prepared=plan()
    prepared['reused_MX1']=dict(campaign=str(old_folder),manifest_sha256=controller.digest(old_folder/'manifest.json'))
    write(p,prepared);folder=prepare_campaign(p,job/'A')
    recipe=ROOT/f'research/campaign_recipes/MX2_{stamp}';export_recipe(folder,recipe)
    sources=list((ROOT/'simulator').glob('*.py'))+[ROOT/q for q in ('scripts/campaign.py','scripts/expression_followup.py',
        'scripts/cooperative_synthesis_followup.py','experiments/review_cooperative_synthesis.py',
        'experiments/review_mixed_synthesis.py','experiments/mixed_calibration.py','experiments/review_renewal.py',
        'experiments/tool_product_flux.py')];hashes={}
    for src in sources:
        name=src.relative_to(ROOT).as_posix();dest=job/'runtime'/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dest);hashes[name]=controller.digest(dest)
    cfg=dict(version=1,campaigns=[str(folder)],source_sha256=hashes,manifests={str(folder):controller.digest(folder/'manifest.json')},
        baseline_recipe=str(REFERENCE),baseline_manifest_sha256=controller.digest(REFERENCE/'manifest.json'),
        max_tasks=12,workers=2,max_wall_seconds=14400,gate='MX2_BATCH_42_PLAN',after='Interpret, no second phase/retry/promotion',
        predecessor_report=str(evidence),predecessor_report_sha256=controller.digest(evidence))
    write(job/'job.json',cfg);(job/'job.sha256').write_text(controller.digest(job/'job.json'))
    write(job/'state.json',dict(phase='ready_A',stage=0,updated=time.time()));(parent/'latest.txt').write_text(str(job.resolve()))
    write(ROOT/'research/BATCH_42_RECIPES.json',dict(job=str(job.resolve()),recipes=[recipe.relative_to(ROOT).as_posix()],
        job_sha256=controller.digest(job/'job.json'),supervisor_source_sha256=hashes,baseline_recipe=REFERENCE.relative_to(ROOT).as_posix(),
        predecessor_report_sha256=cfg['predecessor_report_sha256']))
    return job


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','run','resume','status','stop','review']);p.add_argument('--job',type=Path);a=p.parse_args()
    if a.action=='prepare':print(prepare());return
    job=a.job or latest()
    if a.action=='run':controller.run(job,collect,decide)
    elif a.action=='review':print(json.dumps(collect(Path(read(job/'job.json')['campaigns'][0]),False),indent=2))
    elif a.action=='status':
        s=controller.status(job);print(json.dumps(dict(active=s['active'],state=s['state'],campaigns=[dict(counts=c['counts'],controller_active=c['controller_active'],
            running=[dict(label=t['label'],time=t.get('simulated_time'),eta_seconds=t.get('eta_seconds')) for t in c['tasks'] if t['phase']=='running']) for c in s['campaigns']]),indent=2))
    elif a.action=='stop':
        cfg=controller.validate_job(job);(job/'STOP').write_text('pause requested')
        for f in cfg['campaigns']:(Path(f)/'STOP').write_text('pause requested')
    else:
        s=controller.status(job)
        if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):raise RuntimeError('Wait for controllers/workers')
        if s['state']['phase']=='needs_interpretation':raise RuntimeError('Completed; no work to resume')
        if any(c['counts']['failed'] for c in s['campaigns']):raise RuntimeError('Inspect failures; no retry')
        cfg=controller.validate_job(job)
        for f in [job]+[Path(f) for f in cfg['campaigns']]:
            if (f/'STOP').exists():(f/'STOP').unlink()
        state=s['state'];state.update(phase='ready_resume',explicit_resume=True);state.pop('launched',None);write(job/'state.json',state)
        controller.run(job,collect,decide)


if __name__=='__main__':main()
