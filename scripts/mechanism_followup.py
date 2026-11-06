"""Source-frozen adapters for bounded mechanism assays; shared controller only."""
import argparse,importlib,json,shutil,sys,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import expression_followup as controller
from scripts.campaign import prepare as prepare_campaign,export_recipe
from simulator.campaign_io import read,write
STUDIES=dict(inhibition=dict(tag='PI1',prepare='prepare_product_binding',review='review_product_binding',tasks=15,budget=3600),
    energy=dict(tag='EG1',prepare='prepare_energy_exchange',review='review_energy_exchange',tasks=3,budget=10800),
    timestep=dict(tag='EN1',prepare='prepare_exchange_refinement',review='review_exchange_refinement',tasks=3,budget=10800,batch=47,
        predecessor='research/BATCH_46_EG1_RECIPES.json'),
    protection=dict(tag='RP1',prepare='prepare_pair_protection',review='review_pair_protection',tasks=3,budget=3600,batch=48,
        predecessor='research/BATCH_31_RECIPES.json',predecessor_tasks=12,workers=1),
    contacts=dict(tag='CF1',prepare='prepare_contact_gate',review='review_contact_gate',tasks=6,budget=10800,batch=49,
        predecessor='research/BATCH_47_EN1_RECIPES.json'),
    competitive=dict(tag='CC1',prepare='prepare_competitive_panel',review='review_competitive_panel',tasks=6,budget=3600,batch=50,
        predecessor='research/BATCH_47_EN1_RECIPES.json'),
    competitive_horizon=dict(tag='CH1',prepare='prepare_competitive_horizon',review='review_competitive_horizon',tasks=4,budget=7200,batch=50,
        predecessor='research/BATCH_50_CC1_RECIPES.json',predecessor_tasks=6),
    competitive_relaxation=dict(tag='CR1',prepare='prepare_competitive_relaxation',review='review_competitive_relaxation',tasks=3,budget=10800,batch=51,
        predecessor='research/BATCH_50_CH1_RECIPES.json',predecessor_tasks=4),
    selective_transport=dict(tag='PT1',prepare='prepare_selective_transport',review='review_selective_transport',tasks=6,budget=7200,batch=53,workers=1,
        predecessor='research/BATCH_50_CH1_RECIPES.json',predecessor_tasks=4),
    functional_recycling=dict(tag='RF1',prepare='prepare_functional_recycling',review='review_functional_recycling',tasks=9,budget=7200,batch=53,workers=1,
        predecessor='research/BATCH_48_RP1_RECIPES.json',predecessor_tasks=3))


def latest(study):return Path((ROOT/f'outputs/{study}_mechanism_followups/latest.txt').read_text().strip())


def prepare(study):
    info=STUDIES[study];module=importlib.import_module('experiments.'+info['prepare'])
    previous=Path(read(ROOT/info.get('predecessor','research/BATCH_45_WIDE_RECIPES.json'))['job']);s=controller.status(previous)
    if s['active'] or s['state']['phase']!='needs_interpretation' or s['campaigns'][0]['counts']['complete']!=info.get('predecessor_tasks',3):raise ValueError('Require complete analyzed predecessor')
    evidence=Path(s['state']['report_0'])
    if controller.digest(evidence)!=s['state']['report_0_sha256']:raise ValueError('Predecessor evidence changed')
    if study=='energy':
        from scripts.campaign import validate
        from experiments.mixed_calibration import weighted
        pilot=Path(read(ROOT/'research/BATCH_46_EG1_PILOT.json')['campaign']);pm=validate(pilot)
        ps=read(pilot/'tasks/task0000/state.json');pr=read(pilot/ps['result'])
        motion=read(pilot/ps['motion_audit'])['history'];late=[q['kinetic_temperature'] for q in motion if q['time']>=75.]
        if ps['status']!='complete' or pr['error'] or pr['scenario']!=pm['tasks'][0]['scenario'] or pr['metrics']['atom_port_invariant_failures'] or weighted(pr['metrics']['boundary']['history'],'valid',0.,100.)<.8 or sum(late)/len(late)>.12:
            raise ValueError('EG1 pilot refused; inspect before followup')
    parent=ROOT/f'outputs/{study}_mechanism_followups';parent.mkdir(parents=True,exist_ok=True)
    if (parent/'latest.txt').exists():
        old=controller.status(latest(study))
        if old['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in old['campaigns']):raise ValueError('Study already active')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');job=parent/('followup_'+stamp);job.mkdir()
    plan=module.plan();p=ROOT/f'campaigns/{study}_mechanism.json';write(p,plan);folder=prepare_campaign(p,job/'A')
    recipe=ROOT/f'research/campaign_recipes/{info["tag"]}_{stamp}';export_recipe(folder,recipe)
    sources=list((ROOT/'simulator').glob('*.py'))+[ROOT/p for p in ('scripts/campaign.py','scripts/expression_followup.py','scripts/mechanism_followup.py',f'experiments/{info["prepare"]}.py',f'experiments/{info["review"]}.py')]
    if study in ('energy','timestep','contacts','competitive'):sources += [ROOT/p for p in ('experiments/review_boundary_transfer.py','experiments/mixed_calibration.py','experiments/review_renewal.py','experiments/tool_product_flux.py')]
    if study=='competitive':sources += [ROOT/'experiments/prepare_contact_gate.py',ROOT/'experiments/benchmark_competitive_ports.py']
    if study in ('competitive_horizon','competitive_relaxation'):sources += [ROOT/'experiments/review_competitive_panel.py',ROOT/'experiments/mixed_calibration.py']
    if study in ('selective_transport','functional_recycling'):sources += [ROOT/'experiments/independent_assay_results.py']
    if study=='selective_transport':sources += [ROOT/'experiments/mixed_calibration.py']
    if study=='timestep':sources += [ROOT/'experiments/review_energy_exchange.py']
    hashes={}
    for src in sources:
        name=src.relative_to(ROOT).as_posix();dest=job/'runtime'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest);hashes[name]=controller.digest(dest)
    cfg=dict(version=1,study=study,campaigns=[str(folder)],source_sha256=hashes,manifests={str(folder):controller.digest(folder/'manifest.json')},
        baseline_recipe=str(module.REFERENCE),baseline_manifest_sha256=controller.digest(module.REFERENCE/'manifest.json'),
        max_tasks=info['tasks'],workers=info.get('workers',2),max_wall_seconds=info['budget'],gate=info['tag']+f'_BATCH_{info.get("batch",46)}_PLAN',
        predecessor_report=str(evidence),predecessor_report_sha256=controller.digest(evidence),after='Report and stop; no tuning/retry/second phase')
    write(job/'job.json',cfg);(job/'job.sha256').write_text(controller.digest(job/'job.json'));write(job/'state.json',dict(phase='ready_A',stage=0,updated=time.time()))
    (parent/'latest.txt').write_text(str(job.resolve()));write(ROOT/f'research/BATCH_{info.get("batch",46)}_{info["tag"]}_RECIPES.json',dict(job=str(job),recipes=[recipe.relative_to(ROOT).as_posix()],job_sha256=controller.digest(job/'job.json'),supervisor_source_sha256=hashes))
    return job


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','run','resume','status','stop','review']);p.add_argument('--study',choices=STUDIES,default='inhibition');p.add_argument('--job',type=Path);a=p.parse_args()
    if a.action=='prepare':print(prepare(a.study));return
    job=a.job or latest(a.study);cfg=controller.validate_job(job);study=cfg['study'];info=STUDIES[study]
    analysis=importlib.import_module('experiments.'+info['review'])
    if cfg['gate']!=info['tag']+f'_BATCH_{info.get("batch",46)}_PLAN':raise ValueError('Study/job gate mismatch')
    if a.action=='run':controller.run(job,analysis.collect,analysis.decide)
    elif a.action=='review':print(json.dumps(analysis.collect(Path(cfg['campaigns'][0]),False),indent=2))
    elif a.action=='status':
        s=controller.status(job);print(json.dumps(dict(active=s['active'],state=s['state'],campaigns=[dict(counts=c['counts'],controller_active=c['controller_active'],running=[dict(label=t['label'],time=t.get('simulated_time'),eta_seconds=t.get('eta_seconds')) for t in c['tasks'] if t['phase']=='running']) for c in s['campaigns']]),indent=2))
    elif a.action=='stop':
        for f in [job]+[Path(f) for f in cfg['campaigns']]:(f/'STOP').write_text('pause requested')
    else:
        s=controller.status(job)
        if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):raise ValueError('Wait for workers')
        if s['state']['phase']=='needs_interpretation':raise ValueError('Already finished')
        if any(c['counts']['failed'] for c in s['campaigns']):raise ValueError('Inspect failures; no retry')
        for f in [job]+[Path(f) for f in cfg['campaigns']]:
            if (f/'STOP').exists():(f/'STOP').unlink()
        state=s['state'];state.update(phase='ready_resume',explicit_resume=True);state.pop('launched',None);write(job/'state.json',state);controller.run(job,analysis.collect,analysis.decide)


if __name__=='__main__':main()
