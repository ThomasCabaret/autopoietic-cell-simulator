"""A bounded N1 -> analysis -> optional N2 follow-up, reusing campaign workers."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import prepare as prepare_campaign,validate,status as campaign_status
from simulator.campaign_io import read,write,lock,busy
from experiments.analyze_numerical_campaign import compare as compare_n1
from experiments.analyze_cadence_campaign import compare as compare_n2


def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def prepare(parent,plan,baseline,output):
    parent,plan,baseline,output=map(lambda p:Path(p).resolve(),(parent,plan,baseline,output))
    parent_manifest=validate(parent);validate(baseline)
    if len(parent_manifest['tasks'])!=6 or {t['label'] for t in parent_manifest['tasks']}!={'N1_dt2','N1_dt4'}:
        raise ValueError('This bounded follow-up requires the N1 six-task design')
    design=read(plan)
    if len(design['tasks'])!=6 or design.get('workers')!=2:raise ValueError('Fixed N2 budget: six tasks, two workers')
    job=output/('followup_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));job.mkdir(parents=True)
    # Separate latest pointer: preparing conditional work must not hide active N1.
    child=prepare_campaign(plan,job/'next_campaigns')
    runtime=job/'runtime';sources=list((ROOT/'simulator').glob('*.py'))
    sources += [ROOT/p for p in ('scripts/campaign.py','scripts/numerical_followup.py',
        'experiments/analyze_numerical_campaign.py','experiments/analyze_cadence_campaign.py',
        'experiments/analyze_constructed_tool.py','experiments/inventory_audit.py')]
    hashes={}
    for src in sources:
        name=src.relative_to(ROOT).as_posix();dest=runtime/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dest);hashes[name]=digest(dest)
    revision=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True)
    cfg=dict(version=1,parent=str(parent),baseline=str(baseline),child=str(child),
        source_sha256=hashes,git_revision=revision.stdout.strip(),
        manifest_sha256={str(p):digest(p/'manifest.json') for p in (parent,baseline,child)},
        gate='any_N1_prospective_median_alert_to_factor4_only_after_complete_cohorts',
        budget=dict(max_new_tasks=6,workers=2,poll_seconds=30),
        after='Stop for mechanistic interpretation; no automatic new chemistry or retries')
    write(job/'job.json',cfg);(job/'job.sha256').write_text(digest(job/'job.json'),encoding='ascii')
    write(job/'state.json',dict(phase='waiting_N1',updated=time.time()))
    (output/'latest.txt').write_text(str(job),encoding='utf-8');return job


def validate_job(job):
    job=Path(job)
    if digest(job/'job.json')!=(job/'job.sha256').read_text().strip():raise ValueError('Follow-up changed')
    cfg=read(job/'job.json')
    for name,expected in cfg['source_sha256'].items():
        if digest(job/'runtime'/name)!=expected:raise ValueError('Follow-up source changed: '+name)
    for path,expected in cfg['manifest_sha256'].items():
        p=Path(path);validate(p)
        if digest(p/'manifest.json')!=expected:raise ValueError('Campaign identity changed')
    return cfg


def decision(report):
    triage=report['triage']
    if not triage['complete_cohorts']:raise ValueError('Refuse decision from incomplete cohorts')
    return any(a['to_factor']==4 for a in triage['alerts'])


def step(job):
    job=Path(job);cfg=validate_job(job);state=read(job/'state.json',{})
    parent,child,baseline=map(Path,(cfg['parent'],cfg['child'],cfg['baseline']))
    def finish(phase,**values):
        state.update(phase=phase,updated=time.time(),**values);write(job/'state.json',state);return phase
    if (job/'STOP').exists():return finish('paused')
    if state.get('phase') in ('needs_interpretation','needs_attention'):return state['phase']
    snapshot=campaign_status(parent)
    if any(snapshot['counts'][k] for k in ('failed','paused','interrupted')):
        return finish('needs_attention',reason='N1 has errors, pauses or interrupted tasks; no automatic retry')
    if snapshot['counts']['complete']!=len(snapshot['tasks']) or snapshot['controller_active']:
        return finish('waiting_N1',parent_counts=snapshot['counts'])
    if 'run_N2' not in state:
        out=compare_n1(parent,baseline);report=read(out/'report.json')
        state.update(run_N2=decision(report),N1_report=str(out/'report.json'),N1_report_sha256=digest(out/'report.json'))
        finish('N1_analyzed')
    if digest(state['N1_report'])!=state['N1_report_sha256']:raise ValueError('Decision evidence changed')
    if state['run_N2']!=decision(read(state['N1_report'])):raise ValueError('Cached decision differs from its evidence')
    if not state['run_N2']:
        return finish('needs_interpretation',reason='No prospective finest-level median alert; review T9, no N2 launched')
    snapshot=campaign_status(child)
    if snapshot['counts']['failed'] or (any(snapshot['counts'][k] for k in ('paused','interrupted')) and not state.get('resume_child')):
        return finish('needs_attention',reason='N2 requires inspection or explicit campaign resume; no automatic retry')
    if snapshot['counts']['complete']==len(snapshot['tasks']) and not snapshot['controller_active']:
        out=compare_n2(child,parent,baseline)
        return finish('needs_interpretation',N2_report=str(out/'report.json'),reason='N2 finished; interpret cadence effects before choosing chemistry')
    if snapshot['controller_active'] or any(t['worker_active'] for t in snapshot['tasks']):
        return finish('running_N2',child_counts=snapshot['counts'])
    if state.get('launched'):
        if time.time()-state['launched']<60:return finish('launching_N2')
        return finish('needs_attention',reason='N2 controller absent after launch; no duplicate or automatic retry')
    stdout=(job/'child_controller.stdout.log').open('ab');stderr=(job/'child_controller.stderr.log').open('ab')
    try:
        process=subprocess.Popen([sys.executable,str(child/'runtime/campaign.py'),'run',str(child)],cwd=child,
            stdout=stdout,stderr=stderr,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    finally:stdout.close();stderr.close()
    state.pop('resume_child',None)
    return finish('launching_N2',launched=time.time(),child_controller_pid=process.pid)


def run(job):
    job=Path(job)
    with lock(job/'followup.lock'):
        while True:
            try:phase=step(job)
            except Exception:
                import traceback
                write(job/'state.json',dict(phase='needs_attention',updated=time.time(),error=traceback.format_exc()))
                raise
            if phase in ('paused','needs_attention','needs_interpretation'):return
            time.sleep(30)


def status(job):
    job=Path(job);cfg=validate_job(job)
    child=campaign_status(Path(cfg['child']))
    return dict(job=str(job),active=busy(job/'followup.lock'),state=read(job/'state.json'),
        parent=campaign_status(Path(cfg['parent']))['counts'],child=child['counts'],
        child_controller_active=child['controller_active'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run','status','stop','resume'])
    p.add_argument('--job',type=Path);p.add_argument('--parent',type=Path);p.add_argument('--baseline',type=Path)
    p.add_argument('--plan',type=Path,default=ROOT/'campaigns/cadence_controls.json')
    p.add_argument('--output',type=Path,default=ROOT/'outputs/followups');a=p.parse_args()
    if a.action=='prepare':print(prepare(a.parent,a.plan,a.baseline,a.output))
    elif a.action=='run':run(a.job)
    elif a.action=='status':print(json.dumps(status(a.job),indent=2))
    elif a.action=='resume':
        validate_job(a.job)
        if busy(a.job/'followup.lock'):raise RuntimeError('Follow-up is already active')
        if (a.job/'STOP').exists():(a.job/'STOP').unlink()
        state=read(a.job/'state.json',{});state.update(phase='waiting_N1',resume_child=True)
        state.pop('launched',None);write(a.job/'state.json',state);run(a.job)
    else:
        cfg=validate_job(a.job);(a.job/'STOP').write_text('pause',encoding='ascii')
        if read(a.job/'state.json',{}).get('launched'):
            (Path(cfg['child'])/'STOP').write_text('pause',encoding='ascii')
