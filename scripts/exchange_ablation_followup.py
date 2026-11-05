"""CX1 adapter to the existing frozen campaign controller; three tasks only."""
import argparse,json,shutil,sys,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import expression_followup as controller
from scripts.campaign import prepare as prepare_campaign,export_recipe,validate
from simulator.campaign_io import read,write
from experiments.review_exchange_ablation import collect,decide
WIDE=False


def latest():return Path((ROOT/('outputs/wide_ports_followups/latest.txt' if WIDE else 'outputs/exchange_ablation_followups/latest.txt')).read_text().strip())


def prepare():
    from experiments.prepare_exchange_ablation import plan,REFERENCE
    tag='CW1' if WIDE else 'CX1'
    previous=Path(read(ROOT/'research/BATCH_44_RECIPES.json')['job']);s=controller.status(previous)
    if s['active'] or s['state']['phase']!='needs_interpretation' or s['campaigns'][0]['counts']['complete']!=9:raise ValueError('Require analyzed inactive CB1')
    evidence=Path(s['state']['report_0'])
    if controller.digest(evidence)!=s['state']['report_0_sha256']:raise ValueError('CB1 report changed')
    baseline=[{k:r[k] for k in ('label','seed','G_new','F_new','L_new','valid_fraction_late','result_sha256')}
        for r in read(evidence)['rows'] if '_active_' in r['label']]
    if WIDE:
        from experiments.mixed_calibration import weighted
        pilot=Path(read(ROOT/'research/BATCH_45_WIDE_PILOT.json')['campaign'])
        pm=validate(pilot)
        ps=read(pilot/'tasks/task0000/state.json');pr=read(pilot/ps['result'])
        if pr['scenario']!=pm['tasks'][0]['scenario'] or pr['source_sha256']!={k:v for k,v in pm['source_sha256'].items() if k.startswith('simulator/')}:
            raise ValueError('Wider-port pilot provenance mismatch')
        if ps['status']!='complete' or pr['error'] or pr['metrics']['atom_port_invariant_failures'] or weighted(pr['metrics']['boundary']['history'],'valid',0.,100.)<.8:
            raise ValueError('Wider-port pilot refused; inspect before followups')
    parent=ROOT/('outputs/wide_ports_followups' if WIDE else 'outputs/exchange_ablation_followups');parent.mkdir(parents=True,exist_ok=True)
    if (parent/'latest.txt').exists():
        snap=controller.status(latest())
        if snap['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in snap['campaigns']):raise ValueError('CX1 already active')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');job=parent/('followup_'+stamp);job.mkdir()
    p=ROOT/('campaigns/wide_ports.json' if WIDE else 'campaigns/exchange_ablation.json');write(p,plan(baseline,WIDE));folder=prepare_campaign(p,job/'A')
    recipe=ROOT/f'research/campaign_recipes/{tag}_{stamp}';export_recipe(folder,recipe)
    names=('scripts/campaign.py','scripts/expression_followup.py','scripts/exchange_ablation_followup.py',
        'experiments/review_exchange_ablation.py','experiments/review_boundary_transfer.py',
        'experiments/mixed_calibration.py','experiments/review_renewal.py','experiments/tool_product_flux.py')
    hashes={}
    for src in list((ROOT/'simulator').glob('*.py'))+[ROOT/q for q in names]:
        name=src.relative_to(ROOT).as_posix();dest=job/'runtime'/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dest);hashes[name]=controller.digest(dest)
    cfg=dict(version=1,campaigns=[str(folder)],source_sha256=hashes,manifests={str(folder):controller.digest(folder/'manifest.json')},
        baseline_recipe=str(REFERENCE),baseline_manifest_sha256=controller.digest(REFERENCE/'manifest.json'),
        max_tasks=3,workers=2,max_wall_seconds=10800,gate=f'{tag}_BATCH_45_PLAN',after='Interpret, no second phase/retry',
        predecessor_report=str(evidence),predecessor_report_sha256=controller.digest(evidence))
    write(job/'job.json',cfg);(job/'job.sha256').write_text(controller.digest(job/'job.json'))
    write(job/'state.json',dict(phase='ready_A',stage=0,updated=time.time()));(parent/'latest.txt').write_text(str(job.resolve()))
    write(ROOT/('research/BATCH_45_WIDE_RECIPES.json' if WIDE else 'research/BATCH_45_RECIPES.json'),dict(job=str(job),recipes=[recipe.relative_to(ROOT).as_posix()],
        job_sha256=controller.digest(job/'job.json'),supervisor_source_sha256=hashes,predecessor_report_sha256=controller.digest(evidence)))
    return job


def main():
    global WIDE
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','run','resume','status','stop','review']);p.add_argument('--job',type=Path);p.add_argument('--wide',action='store_true');a=p.parse_args();WIDE=a.wide
    if a.action=='prepare':print(prepare());return
    job=a.job or latest()
    gate=controller.validate_job(job)['gate']
    if not gate.startswith(('CX1_','CW1_')):raise ValueError('Unsupported exchange comparison gate')
    if WIDE and not gate.startswith('CW1_'):raise ValueError('Wide option contradicts job')
    if a.action=='run':controller.run(job,collect,decide)
    elif a.action=='review':print(json.dumps(collect(Path(read(job/'job.json')['campaigns'][0]),False),indent=2))
    elif a.action=='status':
        s=controller.status(job);print(json.dumps(dict(active=s['active'],state=s['state'],campaigns=[dict(counts=c['counts'],controller_active=c['controller_active'],running=[dict(label=t['label'],time=t.get('simulated_time'),eta_seconds=t.get('eta_seconds')) for t in c['tasks'] if t['phase']=='running']) for c in s['campaigns']]),indent=2))
    elif a.action=='stop':
        cfg=controller.validate_job(job);(job/'STOP').write_text('pause requested')
        for f in cfg['campaigns']:(Path(f)/'STOP').write_text('pause requested')
    else:
        s=controller.status(job)
        if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):raise ValueError('Wait for workers')
        if s['state']['phase']=='needs_interpretation':raise ValueError('Already complete')
        if any(c['counts']['failed'] for c in s['campaigns']):raise ValueError('Inspect failures; no retry')
        cfg=controller.validate_job(job)
        for f in [job]+[Path(f) for f in cfg['campaigns']]:
            if (f/'STOP').exists():(f/'STOP').unlink()
        state=s['state'];state.update(phase='ready_resume',explicit_resume=True);state.pop('launched',None);write(job/'state.json',state)
        controller.run(job,collect,decide)


if __name__=='__main__':main()
