"""Prepare, run, inspect, stop and analyze frozen local simulation campaigns."""
import argparse,hashlib,json,os,shutil,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve
from simulator.campaign_io import read,write,lock,busy


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare(plan_path,parent):
    plan=read(plan_path);parent=Path(parent);parent.mkdir(parents=True,exist_ok=True)
    workers=plan.get('workers',2);interval=plan.get('checkpoint_seconds',60.);window=plan.get('kinetic_window',25.)
    if not isinstance(workers,int) or not 1<=workers<=max(1,os.cpu_count() or 1):raise ValueError('Invalid worker count')
    if not all(isinstance(v,(int,float)) and 0<v<86400 for v in (interval,window)):raise ValueError('Invalid checkpoint/window interval')
    if not plan.get('tasks'):raise ValueError('Empty campaign')
    tasks=[]
    for i,raw in enumerate(plan['tasks']):
        cfg=resolve(raw['scenario']) if 'scenario' in raw else resolve(read(ROOT/raw['config']))
        tasks.append(dict(id=f'task{i:04d}',label=raw.get('label',cfg['name']),scenario=cfg))
    folder=parent/('campaign_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));folder.mkdir(exist_ok=False)
    runtime=folder/'runtime';runtime.mkdir();source=ROOT/'simulator'
    (runtime/'simulator').mkdir()
    for p in source.glob('*.py'):shutil.copyfile(p,runtime/'simulator'/p.name)
    shutil.copyfile(__file__,runtime/'campaign.py')
    hashes={p.relative_to(runtime).as_posix():digest(p) for p in runtime.rglob('*.py')}
    manifest=dict(version=1,name=plan.get('name','campaign'),created=time.time(),tasks=tasks,
        workers=workers,checkpoint_seconds=interval,kinetic_window=window,
        record_trajectory=bool(plan.get('record_trajectory',False)),source_sha256=hashes,
        comparison_policy=plan.get('comparison_policy','Separate candidates; no common chemistry inferred'),
        plan_sha256=digest(plan_path))
    git=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True)
    manifest['git_revision']=git.stdout.strip() if git.returncode==0 else None
    write(folder/'manifest.json',manifest)
    (folder/'manifest.sha256').write_text(digest(folder/'manifest.json'),encoding='ascii')
    shutil.copyfile(plan_path,folder/'plan.json')
    (parent/'latest.txt').write_text(str(folder.resolve()),encoding='utf-8')
    return folder.resolve()


def validate(folder):
    if digest(folder/'manifest.json')!=(folder/'manifest.sha256').read_text().strip():raise ValueError('Manifest changed')
    manifest=read(folder/'manifest.json')
    if digest(folder/'plan.json')!=manifest['plan_sha256']:raise ValueError('Frozen plan changed')
    for name,expected in manifest['source_sha256'].items():
        if digest(folder/'runtime'/name)!=expected:raise ValueError('Frozen source changed: '+name)
    return manifest


def export_recipe(folder,target):
    manifest=validate(folder);target=Path(target);target.mkdir(parents=True,exist_ok=False)
    for name in ('manifest.json','manifest.sha256','plan.json'):
        shutil.copyfile(folder/name,target/name)
    for name in manifest['source_sha256']:
        p=target/'runtime'/name;p.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(folder/'runtime'/name,p)
    validate(target);return target


def restore_recipe(recipe,parent):
    validate(recipe);parent=Path(parent);parent.mkdir(parents=True,exist_ok=True)
    folder=parent/('campaign_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    export_recipe(recipe,folder)
    (parent/'latest.txt').write_text(str(folder.resolve()),encoding='utf-8')
    return folder.resolve()


def status(folder):
    manifest=read(folder/'manifest.json');tasks=[]
    for task in manifest['tasks']:
        dest=folder/'tasks'/task['id'];state=read(dest/'state.json',dict(status='pending'))
        active=busy(dest/'worker.lock');phase=state['status']
        if phase=='running' and not active:phase='interrupted'
        if active and phase not in ('complete','failed','paused'):phase='running'
        tasks.append(dict(id=task['id'],label=task['label'],**state,phase=phase,worker_active=active,
            heartbeat_age_seconds=time.time()-state['updated'] if 'updated' in state else None))
    return dict(folder=str(folder),name=manifest['name'],controller_active=busy(folder/'controller.lock'),
        stop_requested=(folder/'STOP').exists(),counts={k:sum(t['phase']==k for t in tasks)
            for k in ('pending','running','complete','failed','paused','interrupted')},tasks=tasks)


def run(folder,retry_failed=False):
    manifest=validate(folder)
    with lock(folder/'controller.lock'):
        snapshot=status(folder)
        if any(t['worker_active'] for t in snapshot['tasks']):raise RuntimeError('Workers still active; inspect before restarting controller')
        if (folder/'STOP').exists():(folder/'STOP').unlink()
        todo=[]
        for task in snapshot['tasks']:
            if task['phase']=='complete':
                if not (folder/task['result']).exists():raise FileNotFoundError('Completed result missing: '+task['id'])
                continue
            if task['phase']=='failed' and not retry_failed:continue
            todo.append(task['id'])
        active={};failures=0
        while todo or active:
            stopping=(folder/'STOP').exists()
            while todo and len(active)<manifest['workers'] and not stopping:
                task_id=todo.pop(0);dest=folder/'tasks'/task_id;dest.mkdir(parents=True,exist_ok=True)
                log=(dest/'worker.log').open('ab')
                process=subprocess.Popen([sys.executable,'-m','simulator.campaign_worker',str(folder),task_id],
                    cwd=folder/'runtime',stdout=log,stderr=subprocess.STDOUT)
                active[task_id]=(process,log)
            for task_id,(process,log) in list(active.items()):
                code=process.poll()
                if code is None:continue
                log.close();del active[task_id]
                if code:
                    failures+=1;dest=folder/'tasks'/task_id;state=read(dest/'state.json',{})
                    if state.get('status')!='failed':state.update(status='failed',error=f'Worker exited {code}',updated=time.time());write(dest/'state.json',state)
            write(folder/'controller.json',dict(pid=os.getpid(),updated=time.time(),active=list(active),queued=len(todo),stopping=stopping))
            if stopping and not active:break
            time.sleep(.25)
        final=status(folder)
        return 1 if failures or final['counts']['failed'] else 0


def survival(passages):
    # Kaplan-Meier with right censoring; event times are recorded diagnostics,
    # not independent molecular samples. One sample per replicate/task.
    times=sorted({p['time'] for p in passages});probability=1.;rows=[]
    for t in times:
        risk=sum(p['time']>=t for p in passages);events=sum(p['time']==t and p['event'] for p in passages)
        censored=sum(p['time']==t and not p['event'] for p in passages)
        if risk:probability*=1-events/risk
        rows.append(dict(time=t,at_risk=risk,events=events,censored=censored,survival=probability))
    return rows


def analyze(folder):
    manifest=validate(folder);snapshot=status(folder);rows=[];groups={}
    for task,state in zip(manifest['tasks'],snapshot['tasks']):
        if state['phase']!='complete':continue
        kinetic=read(folder/state['kinetics']);result=read(folder/state['result']);cfg=task['scenario']
        # Freeze chemistry, model, engine, initial name/protocol and horizon.
        # Seed alone is excluded; unequal horizons remain separate by default.
        signature=json.dumps({k:v for k,v in cfg.items() if k not in ('seed','expected','description')},sort_keys=True)
        key=hashlib.sha256(signature.encode()).hexdigest()[:12]
        row=dict(task=task['id'],group=key,seed=cfg['seed'],name=cfg['name'],duration=cfg['duration'],
            metrics={k:result['metrics'].get(k) for k in ('parent_closed_fraction','envelope_valid_fraction','retained_escape_fraction','inserted_into_closed_parent_ever','persistent_inserted_10')},
            first_passages=kinetic['first_passages'],opportunities=kinetic['opportunity_totals'])
        rows.append(row);groups.setdefault(key,[]).append(row)
    estimates={}
    for key,group in groups.items():
        unique={r['seed']:r for r in group}
        estimates[key]={name:survival([r['first_passages'][name] for r in unique.values() if r['first_passages'][name]['measured']]) for name in group[0]['first_passages']}
    report=dict(campaign=str(folder),completed=len(rows),counts=snapshot['counts'],rows=rows,first_passage_survival=estimates,
        caveat='Right-censored finite runs, grouped by identical laws/protocol/horizon. Duplicate seeds and small groups do not establish independent statistics; no stationarity or exact hazard assumed.')
    write(folder/'analysis.json',report)
    lines=['# Analyse cinétique de campagne','',report['caveat'],'','| Tâche | Graine | Rencontre | Éligibilité échange | Insertion fermée |','| --- | ---: | --- | --- | --- |']
    for row in rows:
        def fmt(key):
            p=row['first_passages'][key]
            if not p['measured']:return 'non mesuré'
            return f"{p['time']:g}" if p['event'] else f"> {p['time']:g} (censuré)"
        lines.append(f"| {row['task']} | {row['seed']} | {fmt('encounter_pairs')} | {fmt('exchange_faces')} | {fmt('closed_insertion')} |")
    (folder/'analysis.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','restore','export','run','status','stop','analyze'])
    p.add_argument('path',type=Path);p.add_argument('--output',type=Path,default=ROOT/'outputs/campaigns')
    p.add_argument('--retry-failed',action='store_true');p.add_argument('--json',action='store_true');a=p.parse_args()
    if a.action=='prepare':print(prepare(a.path,a.output));return
    if a.action=='restore':print(restore_recipe(a.path,a.output));return
    folder=a.path.resolve()
    if a.action=='export':print(export_recipe(folder,a.output));return
    if a.action in ('run','analyze'):
        validate(folder);frozen=folder/'runtime/campaign.py'
        if Path(__file__).resolve()!=frozen:return subprocess.call([sys.executable,str(frozen),a.action,str(folder)]+(['--retry-failed'] if a.retry_failed else []))
        if a.action=='run':return run(folder,a.retry_failed)
    if a.action=='stop':(folder/'STOP').write_text('stop requested\n');print('Arrêt demandé ; sauvegarde puis pause.');return
    result=status(folder) if a.action=='status' else analyze(folder)
    if a.action=='status' and not a.json:
        print(str(folder));print(' | '.join(f'{k}: {v}' for k,v in result['counts'].items()))
        print('Controleur actif:',result['controller_active'],'| arret demande:',result['stop_requested'])
        for t in result['tasks']:
            progress=f"t={t.get('simulated_time',0):g}, {t.get('steps_per_second',0):.0f} pas/s"
            eta=t.get('eta_seconds');eta=f', reste ~{eta/60:.1f} min' if eta is not None and t['phase']=='running' else ''
            print(f"{t['id']}  {t['phase']:11}  {t['label']}  {progress}{eta}")
        return
    if a.action=='analyze':result={k:v for k,v in result.items() if k not in ('rows','first_passage_survival')}
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=='__main__':raise SystemExit(main() or 0)
