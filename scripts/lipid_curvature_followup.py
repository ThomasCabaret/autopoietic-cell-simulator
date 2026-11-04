"""L3 one-cohort driver, reusing the source-frozen simulation/controller."""
import argparse,json,shutil,sys,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import expression_followup as controller
from scripts.campaign import prepare as prepare_campaign,export_recipe
from simulator.campaign_io import read,write
from experiments.review_lipid_curvature import collect,decide


def latest(tail=False):return Path((ROOT/('outputs/lipid_thermal_tail_followups/latest.txt' if tail else 'outputs/lipid_curvature_followups/latest.txt')).read_text().strip())


def prepare(tail=False):
    from experiments.prepare_lipid_curvature import plan,REFERENCE
    from experiments.verify_lipid_curvature_reference import main as verify
    if tail:
        from experiments.lipid_thermal_tail import plan,REFERENCE
    parent=ROOT/('outputs/lipid_thermal_tail_followups' if tail else 'outputs/lipid_curvature_followups');parent.mkdir(parents=True,exist_ok=True)
    if (parent/'latest.txt').exists():
        s=controller.status(latest(tail))
        if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):raise RuntimeError('L3 already active')
    refjob=Path(read(ROOT/('research/BATCH_38_RECIPES.json' if tail else 'research/BATCH_37_RECIPES.json'))['job']);ref=Path(read(refjob/'job.json')['campaigns'][0])
    prior=controller.status(refjob)
    if prior['active'] or prior['campaigns'][0]['controller_active'] or prior['campaigns'][0]['counts']['complete']!=(18 if tail else 20):
        raise RuntimeError('Require completed inactive L2 cohort before L3')
    verification=verify();stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    job=parent/('followup_'+stamp);job.mkdir();p=ROOT/('campaigns/lipid_thermal_tail.json' if tail else 'campaigns/lipid_curvature.json');write(p,plan(ref))
    folder=prepare_campaign(p,job/'A');recipe=ROOT/f'research/campaign_recipes/{"L4" if tail else "L3"}_{stamp}';export_recipe(folder,recipe)
    sources=list((ROOT/'simulator').glob('*.py'))+[ROOT/q for q in ('scripts/campaign.py','scripts/expression_followup.py',
        'scripts/lipid_curvature_followup.py','experiments/prepare_lipid_curvature.py','experiments/review_lipid_curvature.py',
        'experiments/prepare_lipid_energy.py','experiments/review_lipid_energy.py','experiments/lipid_thermal_tail.py')];hashes={}
    for src in sources:
        name=src.relative_to(ROOT).as_posix();dest=job/'runtime'/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dest);hashes[name]=controller.digest(dest)
    cfg=dict(version=1,campaigns=[str(folder)],source_sha256=hashes,manifests={str(folder):controller.digest(folder/'manifest.json')},
        baseline_recipe=str(REFERENCE),baseline_manifest_sha256=controller.digest(REFERENCE/'manifest.json'),
        max_tasks=3 if tail else 18,workers=1,max_wall_seconds=3600,gate='L4_BATCH_39_PLAN' if tail else 'L3_BATCH_38_PLAN',after='Interpret, no second phase or retry')
    write(job/'job.json',cfg);(job/'job.sha256').write_text(controller.digest(job/'job.json'))
    write(job/'state.json',dict(phase='ready_A',stage=0,updated=time.time()));(parent/'latest.txt').write_text(str(job.resolve()))
    write(ROOT/('research/BATCH_39_RECIPES.json' if tail else 'research/BATCH_38_RECIPES.json'),dict(job=str(job.resolve()),recipes=[recipe.relative_to(ROOT).as_posix()],
        job_sha256=controller.digest(job/'job.json'),supervisor_source_sha256=hashes,reused_recipe=REFERENCE.relative_to(ROOT).as_posix(),reference_verification=str(verification)))
    return job


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','run','resume','status','stop','review']);p.add_argument('--job',type=Path);p.add_argument('--tail',action='store_true');a=p.parse_args()
    gather,decision=collect,decide
    if a.tail:
        from experiments.lipid_thermal_tail import collect as gather,decide as decision
    if a.action=='prepare':print(prepare(a.tail));return
    job=a.job or latest(a.tail)
    if a.action=='run':controller.run(job,gather,decision)
    elif a.action=='review':print(json.dumps(gather(Path(read(job/'job.json')['campaigns'][0]),False),indent=2))
    elif a.action=='status':
        s=controller.status(job);print(json.dumps(dict(active=s['active'],state=s['state'],campaigns=[dict(counts=c['counts'],controller_active=c['controller_active'],
            running=[dict(label=t['label'],time=t.get('simulated_time'),eta_seconds=t.get('eta_seconds')) for t in c['tasks'] if t['phase']=='running']) for c in s['campaigns']]),indent=2))
    elif a.action=='stop':
        cfg=controller.validate_job(job);(job/'STOP').write_text('pause requested')
        for f in cfg['campaigns']:(Path(f)/'STOP').write_text('pause requested')
    else:
        s=controller.status(job)
        if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):raise RuntimeError('Wait for all workers/controllers')
        if s['state']['phase']=='needs_interpretation':raise RuntimeError('Completed; no work to resume')
        if any(c['counts']['failed'] for c in s['campaigns']):raise RuntimeError('Inspect failures; no retry')
        cfg=controller.validate_job(job)
        for f in [job]+[Path(f) for f in cfg['campaigns']]:
            if (f/'STOP').exists():(f/'STOP').unlink()
        state=s['state'];state.update(phase='ready_resume',explicit_resume=True);state.pop('launched',None);write(job/'state.json',state)
        controller.run(job,gather,decision)


if __name__=='__main__':main()
