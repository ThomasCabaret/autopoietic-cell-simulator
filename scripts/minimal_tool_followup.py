"""MIN1 bounded preparation -> expression chain using existing campaign control."""
import argparse,json,shutil,sys,time
from pathlib import Path
from datetime import datetime,timezone
from statistics import median
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import expression_followup as controller
from scripts.campaign import prepare as prepare_campaign,export_recipe,validate,status as campaign_status
from simulator.campaign_io import read,write
from experiments.tool_product_flux import routes,inventory
digest=controller.digest


def collect(folder,complete=True):
    folder=Path(folder);manifest=validate(folder);snap=campaign_status(folder)
    if complete and (snap['controller_active'] or snap['counts']['complete']!=len(manifest['tasks'])):
        raise ValueError('Require complete inactive cohort')
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')};rows=[]
    for task,state in zip(manifest['tasks'],snap['tasks']):
        if state['phase']!='complete':continue
        path=folder/state['result'];r=read(path)
        if r['scenario']!=task['scenario'] or r['source_sha256']!=hashes or not r['completed'] or r['error']:
            raise ValueError('Result provenance/completion mismatch')
        g=r['metrics'].get('genetics',r['metrics']);flux=routes(r)
        rows.append(dict(label=task['label'],seed=task['scenario']['seed'],G=g['detached_copy_sets_ever'],F=g['translated_detached_ever'],
            expressed_products=g['expressed_catalyzed_dimers'],expressed_used=g['expressed_catalyzed_incorporated'],
            flux={k:v for k,v in flux.items() if k!='products'},inventory=inventory(task['scenario']),
            result_sha256=digest(path),elapsed_seconds=r['elapsed_seconds']))
    return dict(rows=rows,manifest_sha256=digest(folder/'manifest.json'),counts=snap['counts'],
        scope='Closed stocks, absent events censored at declared horizon; prepared A and gene-expression B distinct. '
              'Products incorporated into any backbone, not necessarily a full new tool. No new chemical laws or L synthesis.')


def grouped(rows,phase,variants):
    if len(rows)!=3*len(variants):raise ValueError('Incomplete cohort')
    out={}
    for v in variants:
        group=[r for r in rows if r['label'].startswith(f'MIN1_{phase}_{v}_s')]
        if len(group)!=3 or {r['seed'] for r in group}!={0,1,2}:raise ValueError('Need three distinct seeds per variant')
        out[v]=group
    return out


def count(row,origin='prepared',family=None,used=False):
    table=row['flux']['incorporated' if used else 'formed'][origin]
    return sum(v for key,v in table.items() if family is None or key.startswith(family))


def decide(rows):
    groups=grouped(rows,'A',('long','short','split','no_boost'));s=groups['short']
    med=lambda v:median(count(r) for r in groups[v])
    conditions=dict(long_nonzero=med('long')>0,short_at_least_half=med('short')>=.5*med('long'),
        short_over_controls=med('short')>=5*max(1,med('split'),med('no_boost')),
        both_products_each_seed=all(count(r,family='G')>0 and count(r,family='F')>0 for r in s),
        repeat_operation_each_seed=all(r['flux']['max_operations']['prepared']>=2 for r in s))
    return dict(run_transfer=all(conditions.values()),conditions=conditions,
        interpretation='Size simplification screen only; not function diversity or integrated viability.')


def expression_decision(rows):
    groups=grouped(rows,'B',('short','long','nogene'));s=groups['short']
    conditions=dict(expression_to_use_two_seeds=sum(r['F']>0 and r['expressed_used']>0 for r in s)>=2,
        both_families_expressed_used_two_seeds=sum(count(r,'expressed','G',True)>0 and count(r,'expressed','F',True)>0 for r in s)>=2,
        no_gene_control_negative=all(r['F']==0 and r['expressed_products']==0 and
            sum(count(r,origin) for origin in ('prepared','expressed','unattributed'))==0 for r in groups['nogene']))
    return dict(conditions=conditions,screen_passed=all(conditions.values()),
        next='Stop for interpretation; no third phase or demo promotion. Long-gene capacity, L and regulation remain open.')


def prepare():
    from experiments.prepare_minimal_tool_campaign import plans,MD2
    parent=ROOT/'outputs/minimal_tool_followups';parent.mkdir(parents=True,exist_ok=True);latest=parent/'latest.txt'
    if latest.exists():
        s=controller.status(Path(latest.read_text().strip()))
        if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):
            raise RuntimeError('Existing MIN1 work active')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');job=parent/('followup_'+stamp);job.mkdir()
    folders=[];recipes=[]
    for phase,plan in zip(('A','B'),plans()):
        path=job/f'plan_{phase}.json';write(path,plan);folder=prepare_campaign(path,job/phase);folders.append(str(folder))
        recipe=ROOT/f'research/campaign_recipes/MIN1{phase}_{stamp}';export_recipe(folder,recipe)
        recipes.append(recipe.relative_to(ROOT).as_posix())
    runtime=job/'runtime';hashes={}
    sources=list((ROOT/'simulator').glob('*.py'))+[ROOT/'scripts/campaign.py',ROOT/'scripts/expression_followup.py',
        ROOT/'experiments/tool_product_flux.py',Path(__file__)]
    for src in sources:
        name=src.relative_to(ROOT).as_posix();dest=runtime/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dest);hashes[name]=digest(dest)
    cfg=dict(version=1,campaigns=folders,source_sha256=hashes,manifests={p:digest(Path(p)/'manifest.json') for p in folders},
        baseline_recipe=str(MD2.parent),baseline_manifest_sha256=digest(MD2),max_tasks=21,workers=2,max_wall_seconds=86400,
        gate='MIN1_v1_BATCH_32_PLAN',after='Stop after B or rejected A; no new chemistry/tuning')
    write(job/'job.json',cfg);(job/'job.sha256').write_text(digest(job/'job.json'))
    write(job/'state.json',dict(phase='ready_A',stage=0,updated=time.time()));latest.write_text(str(job.resolve()))
    write(ROOT/'research/BATCH_32_RECIPES.json',dict(job=str(job.resolve()),recipes=recipes,
        job_sha256=digest(job/'job.json'),supervisor_source_sha256=hashes,gate=cfg['gate'],
        note='Sources/configurations only; raw results and checkpoints local. B is selected, not independent validation.'))
    return job


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run','resume','status','stop','review'])
    p.add_argument('--job',type=Path);a=p.parse_args()
    if a.action=='prepare':print(prepare());return
    job=a.job or Path((ROOT/'outputs/minimal_tool_followups/latest.txt').read_text().strip())
    if a.action=='run':controller.run(job,collect,decide)
    elif a.action=='stop':
        cfg=controller.validate_job(job);(job/'STOP').write_text('pause')
        for f in cfg['campaigns']:(Path(f)/'STOP').write_text('pause')
    elif a.action=='review':
        cfg=controller.validate_job(job);reports=[collect(Path(f),False) for f in cfg['campaigns']]
        if len(reports[1]['rows'])==9:reports[1]['decision']=expression_decision(reports[1]['rows'])
        report=dict(state=read(job/'state.json'),cohorts=reports);write(job/'review.json',report)
        print(json.dumps(report,indent=2))
    elif a.action=='status':
        s=controller.status(job)
        print(json.dumps(dict(job=s['job'],active=s['active'],state=s['state'],campaigns=[dict(name=c['name'],counts=c['counts'],
            controller_active=c['controller_active'],running=[dict(label=t['label'],time=t.get('simulated_time'))
                for t in c['tasks'] if t['phase']=='running']) for c in s['campaigns']]),indent=2))
    else:
        s=controller.status(job)
        if s['active'] or any(c['controller_active'] or any(t['worker_active'] for t in c['tasks']) for c in s['campaigns']):
            raise RuntimeError('Wait for all workers/controllers to stop')
        state=s['state']
        if state['phase']=='needs_interpretation':raise RuntimeError('Finished/gate refused; no work to resume')
        cfg=controller.validate_job(job)
        for folder in [job]+[Path(f) for f in cfg['campaigns']]:
            if (folder/'STOP').exists():(folder/'STOP').unlink()
        state.update(phase='ready_resume',explicit_resume=True);state.pop('launched',None)
        write(job/'state.json',state);controller.run(job,collect,decide)


if __name__=='__main__':main()
