"""CF1 fixed-law contact-cost comparison at both existing mechanical steps."""
import copy,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
from simulator.config import resolve
from simulator.campaign_io import read,write
ROOT=Path(__file__).resolve().parents[1]
REFERENCE=ROOT/'research/campaign_recipes/EG1_20261105T131525540618Z'
REFERENCES={'coarse':REFERENCE,'fine':ROOT/'research/campaign_recipes/EN1_20261105T170333609605Z'}


def scenario(seed,scale):
    cfg=copy.deepcopy(next(t['scenario'] for t in read(REFERENCES[scale]/'manifest.json')['tasks'] if t['scenario']['seed']==seed))
    cfg.update(name=f'CF1_{scale}_s{seed}',branch='CF1');cfg['chemistry']['contact_update_gate']='metropolis';return resolve(cfg)


def ensure_pilot():
    from scripts.campaign import prepare,export_recipe,validate,digest
    from experiments.mixed_calibration import weighted
    descriptor=ROOT/'research/BATCH_49_CF1_PILOT.json'
    if not descriptor.exists():
        cfg=scenario(2,'fine');cfg.update(duration=100.,name='CF1_pilot_s2')
        path=ROOT/'campaigns/contact_gate_pilot.json';write(path,dict(name='CF1 short physical precheck',workers=1,
            checkpoint_seconds=30.,kinetic_window=25.,record_trajectory=False,tasks=[dict(scenario=cfg)]))
        folder=prepare(path,ROOT/'outputs/contact_gate_pilots');stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        recipe=ROOT/'research/campaign_recipes'/('CF1P_'+stamp);export_recipe(folder,recipe)
        write(descriptor,dict(campaign=str(folder),recipe=recipe.relative_to(ROOT).as_posix()))
        with (folder/'pilot.out.log').open('w') as out,(folder/'pilot.err.log').open('w') as err:
            try:result=subprocess.run([sys.executable,str(folder/'runtime/campaign.py'),'run',str(folder)],cwd=folder,stdout=out,stderr=err,timeout=900)
            except subprocess.TimeoutExpired:
                (folder/'STOP').write_text('pilot budget reached; checkpoint pause requested',encoding='utf-8')
                raise ValueError('CF1 pilot timed out; inspect workers/checkpoint before any retry')
        if result.returncode:raise ValueError('CF1 pilot failed; inspect, no automatic retry')
    folder=Path(read(descriptor)['campaign']);manifest=validate(folder);s=read(folder/'tasks/task0000/state.json')
    if s['status']!='complete':raise ValueError('CF1 pilot incomplete; inspect before retry')
    result=read(folder/s['result']);metrics=result['metrics']
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    current={'simulator/'+p.name:digest(p) for p in (ROOT/'simulator').glob('*.py')}
    motion=read(folder/s['motion_audit'])['history'];temps=[q['kinetic_temperature'] for q in motion if q['time']>=75.]
    checks=dict(provenance=result['scenario']==manifest['tasks'][0]['scenario'] and result['source_sha256']==hashes and hashes==current,
        completed=result['completed'] and not result['error'],invariants=metrics['atom_port_invariant_failures']==0,
        closure=weighted(metrics['boundary']['history'],'valid',0.,100.)>=.8,temperature=sum(temps)/len(temps)<=.12,
        gate_exercised=sum(q['proposals'] for q in metrics['contact_update_stats'].values())>0)
    write(folder/'pilot_review.json',dict(checks=checks,passed=all(checks.values()),mean_late_temperature=sum(temps)/len(temps),
        closed_fraction=weighted(metrics['boundary']['history'],'valid',0.,100.),scope='Technical100-unit pilot, no late insertion/maintenance proof.'))
    if not all(checks.values()):raise ValueError('CF1 pilot gate refused; report then stop')


def plan():
    from scripts.campaign import digest
    refs=[];reports=[]
    for scale,file in [('coarse','research/BATCH_46_EG1_RECIPES.json'),('fine','research/BATCH_47_EN1_RECIPES.json')]:
        job=Path(read(ROOT/file)['job']);s=read(job/'state.json');p=Path(s['report_0'])
        if s['phase']!='needs_interpretation' or digest(p)!=s['report_0_sha256']:raise ValueError('Reference incomplete/changed')
        reports.append(dict(scale=scale,report=str(p),sha256=digest(p)))
        for row in read(p)['rows']:refs.append(dict(scale=scale,**{k:row[k] for k in ('seed','G_new','F_new','L_new')}))
    ensure_pilot()
    return dict(name='CF1 all L-contact transitions carry local energy cost',workers=2,checkpoint_seconds=30.,
        kinetic_window=25.,record_trajectory=False,tasks=[dict(scenario=scenario(seed,scale)) for scale in ('coarse','fine') for seed in range(3)],
        reference_cases=refs,reference_reports=reports,
        comparison_policy='BATCH_49_PLAN six fixed-law trials, both existing mechanical dt/cadences. '
            'Only contact_update_gate changes. Reuse EG1/EN1 references; no new ablation controls. Report then stop, no tuning/retry/promotion.')
