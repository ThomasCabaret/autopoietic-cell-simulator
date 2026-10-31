"""Bounded RV1 experiment chain; reuse campaign workers and two-stage controller."""
import argparse,json,shutil,sys,time
from pathlib import Path
from datetime import datetime,timezone
from statistics import median
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import expression_followup as controller
from scripts.campaign import prepare as prepare_campaign,export_recipe,validate,status as campaign_status
from simulator.campaign_io import read,write
digest=controller.digest


def collect(folder):
    folder=Path(folder);manifest=validate(folder);snap=campaign_status(folder)
    if snap['controller_active'] or snap['counts']['complete']!=len(manifest['tasks']):
        raise ValueError('Require complete inactive cohort')
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')};rows=[]
    for task,state in zip(manifest['tasks'],snap['tasks']):
        path=folder/state['result'];r=read(path)
        if r['scenario']!=task['scenario'] or r['source_sha256']!=hashes or not r['completed'] or r['error']:
            raise ValueError('Result provenance/completion mismatch')
        g=r['metrics'].get('genetics',r['metrics'])
        if g['observer']!='reversible_current_census_v1':raise ValueError('Wrong observer')
        rows.append(dict(label=task['label'],seed=task['scenario']['seed'],
            invariant_failures=g['invariant_failures'],final=g['final'],
            polymer_reassemblies=g['polymer_reassemblies'],recycled_incorporations=g['recycled_incorporations'],
            catalyzed_formations=g['catalyzed_formations'],backbone_break=g['backbone_break'],
            rung_break=g['rung_break'],result_sha256=digest(path),
            membrane_closed_fraction=r['metrics'].get('membrane',{}).get('parent_closed_fraction')))
    return dict(rows=rows,manifest_sha256=digest(folder/'manifest.json'),
        scope='Finite closed stock; prepared chains included in current census. Event counts, no lineage or new F certificate. '
              'Missing events right-censored at1200. Selected transfer is not independent validation or homeostasis.')


def decide(rows):
    if len(rows)!=12:raise ValueError('Expected12 phase-A trials')
    groups={}
    for v in ('zero','backbone','full','protected'):
        g=[r for r in rows if r['label'].startswith(f'RV1_{v}_s')]
        if len(g)!=3 or {r['seed'] for r in g}!={0,1,2}:raise ValueError('Need3 unique seeds per variant')
        groups[v]=g
    p=groups['protected'];z=groups['zero'];m=median(r['catalyzed_formations'] for r in z)
    conditions=dict(all_invariants_valid=all(r['invariant_failures']==0 and r['final']['invariants_valid'] for r in rows),
        polymer_reassembly_in_two=sum(r['polymer_reassemblies']>0 for r in p)>=2,
        reincorporation_in_two=sum(r['recycled_incorporations']>0 for r in p)>=2,
        target_G_survives_all=all(r['final']['detached_targets']['G']>=1 for r in p),
        baseline_catalysis_nonzero=m>0,
        catalysis_at_least_half=median(r['catalyzed_formations'] for r in p)>=.5*m)
    return dict(run_transfer=all(conditions.values()),conditions=conditions,
        interpretation='Screening only; stop after rejection or B, no tuning or adoption.')


def prepare():
    from experiments.prepare_recycling_campaign import plans,MD2
    parent=ROOT/'outputs/recycling_followups';parent.mkdir(parents=True,exist_ok=True)
    latest=parent/'latest.txt'
    if latest.exists():
        s=controller.status(Path(latest.read_text().strip()))
        if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):
            raise RuntimeError('Existing RV1 work active')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');job=parent/('followup_'+stamp);job.mkdir()
    folders=[];recipes=[]
    for phase,plan in zip(('A','B'),plans()):
        path=job/f'plan_{phase}.json';write(path,plan)
        folder=prepare_campaign(path,job/phase);folders.append(str(folder))
        recipe=ROOT/f'research/campaign_recipes/RV1{phase}_{stamp}';export_recipe(folder,recipe)
        recipes.append(recipe.relative_to(ROOT).as_posix())
    runtime=job/'runtime';hashes={}
    sources=list((ROOT/'simulator').glob('*.py'))+[ROOT/'scripts/campaign.py',ROOT/'scripts/expression_followup.py',Path(__file__)]
    for src in sources:
        name=src.relative_to(ROOT).as_posix();dest=runtime/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dest);hashes[name]=digest(dest)
    cfg=dict(version=1,campaigns=folders,source_sha256=hashes,manifests={p:digest(Path(p)/'manifest.json') for p in folders},
        baseline_recipe=str(MD2.parent),baseline_manifest_sha256=digest(MD2),max_tasks=16,workers=2,max_wall_seconds=86400,
        gate='RV1_v1_BATCH_31_PLAN',after='Stop for interpretation; no automatic tuning/retries')
    write(job/'job.json',cfg);(job/'job.sha256').write_text(digest(job/'job.json'))
    write(job/'state.json',dict(phase='ready_A',stage=0,updated=time.time()))
    latest.write_text(str(job.resolve()))
    write(ROOT/'research/BATCH_31_RECIPES.json',dict(job=str(job.resolve()),recipes=recipes,
        job_sha256=digest(job/'job.json'),supervisor_source_sha256=hashes,gate=cfg['gate'],
        note='Raw state/results stay local; reconstruct phase inputs from recipes. B selected only on prospective gate.'))
    return job


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run','resume','status','stop'])
    p.add_argument('--job',type=Path);a=p.parse_args()
    if a.action=='prepare':print(prepare());return
    job=a.job or Path((ROOT/'outputs/recycling_followups/latest.txt').read_text().strip())
    if a.action=='run':controller.run(job,collect,decide)
    elif a.action=='status':
        s=controller.status(job)
        print(json.dumps(dict(job=s['job'],active=s['active'],state=s['state'],campaigns=[
            dict(name=c['name'],counts=c['counts'],controller_active=c['controller_active'],running=[
                dict(label=t['label'],time=t.get('simulated_time'),target=1200.) for t in c['tasks'] if t['phase']=='running'])
            for c in s['campaigns']]),indent=2))
    elif a.action=='stop':
        cfg=controller.validate_job(job);(job/'STOP').write_text('pause')
        for f in cfg['campaigns']:(Path(f)/'STOP').write_text('pause')
    else:
        s=controller.status(job)
        if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):
            raise RuntimeError('Wait for all controllers/workers to stop')
        state=s['state']
        if state['phase']=='needs_interpretation':raise RuntimeError('Finished/gate refused; no work to resume')
        cfg=controller.validate_job(job)
        for folder in [job]+[Path(f) for f in cfg['campaigns']]:
            if (folder/'STOP').exists():(folder/'STOP').unlink()
        state.update(phase='ready_resume',explicit_resume=True);state.pop('launched',None)
        write(job/'state.json',state);controller.run(job,collect,decide)


if __name__=='__main__':main()
