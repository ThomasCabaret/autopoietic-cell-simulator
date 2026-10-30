"""Bounded T9E small-bath comparison -> selected common-bath transfer, no tuning loop."""
import argparse,hashlib,json,shutil,subprocess,sys,time
from pathlib import Path
from statistics import median
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import prepare as prepare_campaign,export_recipe,validate,status as campaign_status
from simulator.campaign_io import read,write,lock,busy


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def collect(folder):
    folder=Path(folder);manifest=validate(folder);snap=campaign_status(folder)
    if snap['controller_active'] or snap['counts']['complete']!=len(manifest['tasks']):
        raise ValueError('Require complete, inactive cohort')
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')};rows=[]
    for task,state in zip(manifest['tasks'],snap['tasks']):
        path=folder/state['result'];r=read(path)
        if r['scenario']!=task['scenario'] or r['source_sha256']!=hashes or not r['completed'] or r['error']:
            raise ValueError('Result provenance/completion mismatch')
        g=r['metrics'].get('genetics',r['metrics']);audit=read(folder/state['genetic_audit'])
        exp=audit['exposure'];sites=exp['prepared_F_sites']
        rows.append(dict(label=task['label'],seed=task['scenario']['seed'],
            G=g['detached_copy_sets_ever'],F=g['translated_detached_ever'],
            F_complete=g['translated_chains_ever'],incorporated=g['catalyzed_incorporated'],
            expressed_incorporated=g['expressed_catalyzed_incorporated'],
            prepared_paired_fraction=exp['prepared_F_paired_sites']/sites if sites else None,
            genetic_audit={k:v for k,v in audit.items() if k!='state'},
            result_sha256=digest(path),membrane=r['metrics'].get('membrane',{}).get('parent_closed_fraction')))
    return dict(rows=rows,manifest_sha256=digest(folder/'manifest.json'),
        scope='Finite cohorts; no-event outcomes right-censored at each declared horizon. Pre-tick site exposure is approximate. '
              'Counts exclude initial prepared chains. Follow-up selected by this gate, not independent validation.')


def decide(rows):
    def group(prep,variant):
        found=[r for r in rows if r['label'].startswith(f'T9E_{prep}_{variant}_s')]
        if len(found)!=3 or {r['seed'] for r in found}!={0,1,2}:raise ValueError('Require three distinct seeds per preparation/variant')
        return found
    if len(rows)!=12:raise ValueError('Expected12 stage-A trials')
    old,new=group('expression','old'),group('expression','end')
    tool_old,tool_new=group('tool','old'),group('tool','end')
    conditions=dict(F_in_at_least_two_seeds=sum(r['F']>0 for r in new)>=2,
        F_median_strictly_improved=median(r['F'] for r in new)>median(r['F'] for r in old),
        G_median_preserved=median(r['G'] for r in new)>=median(r['G'] for r in old),
        tool_reference_nonzero=median(r['incorporated'] for r in tool_old)>0,
        tool_incorporation_at_least_half=median(r['incorporated'] for r in tool_new)>=.5*median(r['incorporated'] for r in tool_old),
        prepared_tool_pairing_below_half=all(r['prepared_paired_fraction'] is not None and
                                           r['prepared_paired_fraction']<=.5 for r in tool_new))
    return dict(run_transfer=all(conditions.values()),conditions=conditions,
        interpretation='Prospective screening alarm/selection, not proof of useful sustained renewal or robust chemistry.')


def prepare():
    from experiments.prepare_expression_campaign import plans,MD2
    parent=ROOT/'outputs/expression_followups';parent.mkdir(parents=True,exist_ok=True)
    latest=parent/'latest.txt'
    if latest.exists():
        previous=Path(latest.read_text().strip());snap=status(previous)
        if snap['active'] or any(s['controller_active'] or s['counts']['running'] for s in snap['campaigns']):
            raise RuntimeError('T9E work is still active')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');job=parent/('followup_'+stamp);job.mkdir()
    folders=[]
    for phase,plan in zip(('A','B'),plans()):
        path=job/f'plan_{phase}.json';write(path,plan)
        folder=prepare_campaign(path,job/phase);folders.append(str(folder))
        export_recipe(folder,ROOT/f'research/campaign_recipes/T9E{phase}_{stamp}')
    runtime=job/'runtime';hashes={}
    for src in list((ROOT/'simulator').glob('*.py'))+[ROOT/'scripts/campaign.py',Path(__file__)]:
        name=src.relative_to(ROOT).as_posix();dest=runtime/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dest);hashes[name]=digest(dest)
    cfg=dict(version=1,campaigns=folders,source_sha256=hashes,
        manifests={p:digest(Path(p)/'manifest.json') for p in folders},baseline_recipe=str(MD2.parent),
        baseline_manifest_sha256=digest(MD2),max_tasks=16,workers=2,max_wall_seconds=86400,gate='T9E_v1_BATCH_27_PLAN',
        after='Stop for interpretation, no automatic new chemistry/retries')
    write(job/'job.json',cfg);(job/'job.sha256').write_text(digest(job/'job.json'))
    write(job/'state.json',dict(phase='ready_A',stage=0,updated=time.time()))
    latest.write_text(str(job.resolve()));return job


def validate_job(job):
    if digest(job/'job.json')!=(job/'job.sha256').read_text().strip():raise ValueError('Job changed')
    cfg=read(job/'job.json')
    for name,sha in cfg['source_sha256'].items():
        if digest(job/'runtime'/name)!=sha:raise ValueError('Job source changed')
    for p,sha in cfg['manifests'].items():
        validate(Path(p))
        if digest(Path(p)/'manifest.json')!=sha:raise ValueError('Campaign changed')
    baseline=Path(cfg['baseline_recipe']);validate(baseline)
    if digest(baseline/'manifest.json')!=cfg['baseline_manifest_sha256']:raise ValueError('Baseline changed')
    return cfg


def step(job):
    cfg=validate_job(job);state=read(job/'state.json');stage=state['stage'];folder=Path(cfg['campaigns'][stage])
    def finish(phase,**values):
        state.update(phase=phase,updated=time.time(),**values);write(job/'state.json',state);return phase
    if state['phase'] in ('needs_attention','needs_interpretation'):return state['phase']
    if (job/'STOP').exists():return finish('paused')
    if state.get('first_launch') and time.time()-state['first_launch']>=cfg.get('max_wall_seconds',86400):
        (job/'STOP').write_text('wall budget reached')
        for path in cfg['campaigns']:(Path(path)/'STOP').write_text('wall budget reached')
        return finish('needs_attention',reason='24-hour wall budget reached; checkpoint pause requested, no further tests')
    if stage==1:
        evidence=Path(state['report_0'])
        if digest(evidence)!=state['report_0_sha256'] or not decide(read(evidence)['rows'])['run_transfer']:
            raise ValueError('Selected transfer gate evidence changed')
    snap=campaign_status(folder)
    if snap['counts']['failed'] or (any(snap['counts'][k] for k in ('paused','interrupted')) and not state.get('explicit_resume')):
        (folder/'STOP').write_text('inspection required')
        return finish('needs_attention',reason='Inspect errors/pauses/interruptions; no automatic retry')
    if snap['controller_active'] or any(t['worker_active'] for t in snap['tasks']):return finish(f'running_{stage}')
    if snap['counts']['complete']==len(snap['tasks']):
        report=collect(folder)
        if stage==0:report['decision']=decide(report['rows'])
        dest=job/f'report_{stage}.json';write(dest,report)
        state[f'report_{stage}']=str(dest);state[f'report_{stage}_sha256']=digest(dest)
        if stage==1 or not report['decision']['run_transfer']:
            return finish('needs_interpretation',reason='Budget completed or gate refused; no further tuning')
        state.update(stage=1);state.pop('launched',None)
        return finish('ready_B')
    if state.get('launched'):
        if time.time()-state['launched']<60:return finish('launching')
        return finish('needs_attention',reason='Controller absent; no duplicate/retry')
    with (job/f'controller_{stage}.out.log').open('ab') as out,(job/f'controller_{stage}.err.log').open('ab') as err:
        p=subprocess.Popen([sys.executable,str(folder/'runtime/campaign.py'),'run',str(folder)],cwd=folder,
            stdout=out,stderr=err,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    state.pop('explicit_resume',None)
    state.setdefault('first_launch',time.time())
    return finish('launching',launched=time.time(),controller_pid=p.pid)


def run(job):
    with lock(job/'followup.lock'):
        while True:
            try:phase=step(job)
            except Exception:
                import traceback
                state=read(job/'state.json');state.update(phase='needs_attention',error=traceback.format_exc(),updated=time.time())
                write(job/'state.json',state);raise
            if phase in ('needs_attention','needs_interpretation','paused'):return
            time.sleep(15)


def status(job):
    cfg=validate_job(job)
    return dict(job=str(job),active=busy(job/'followup.lock'),state=read(job/'state.json'),
        campaigns=[campaign_status(Path(p)) for p in cfg['campaigns']])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run','resume','status','stop'])
    p.add_argument('--job',type=Path);a=p.parse_args()
    if a.action=='prepare':print(prepare())
    else:
        job=a.job or Path((ROOT/'outputs/expression_followups/latest.txt').read_text().strip())
        if a.action=='run':run(job)
        elif a.action=='resume':
            s=status(job)
            if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):
                raise RuntimeError('Wait for all controllers/workers to stop before explicit resume')
            state=s['state']
            if state['phase']=='needs_interpretation':raise RuntimeError('Finished/gate refused; no work to resume')
            cfg=validate_job(job)
            for pth in [job]+[Path(p) for p in cfg['campaigns']]:
                if (pth/'STOP').exists():(pth/'STOP').unlink()
            state.update(phase='ready_resume',explicit_resume=True);state.pop('launched',None)
            write(job/'state.json',state);run(job)
        elif a.action=='status':
            s=status(job)
            print(json.dumps(dict(job=s['job'],active=s['active'],state=s['state'],
                campaigns=[dict(name=c['name'],counts=c['counts'],controller_active=c['controller_active'],
                    running=[dict(label=t['label'],time=t.get('simulated_time'),target=1200.) for t in c['tasks'] if t['phase']=='running']) for c in s['campaigns']]),indent=2))
        else:
            cfg=validate_job(job);(job/'STOP').write_text('pause')
            for folder in cfg['campaigns']:(Path(folder)/'STOP').write_text('pause')
