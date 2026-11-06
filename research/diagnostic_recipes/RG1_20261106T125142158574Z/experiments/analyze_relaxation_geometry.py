"""Passive CR1 completed-case time summaries; partial cohorts never get a gate."""
import hashlib,json,shutil,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write
from scripts.campaign import validate,status,digest
from experiments.mixed_calibration import weighted


def episodes(history):
    """Sample-and-hold intervals, not continuous closure lifetimes."""
    result=[];start=None
    for row in history:
        if row['macro'] and start is None:start=row['time']
        if not row['macro'] and start is not None:
            result.append(dict(start=start,end=row['time'],ends_at_horizon=False));start=None
    if start is not None:result.append(dict(start=start,end=history[-1]['time'],ends_at_horizon=True))
    return result


def main():
    job=Path(read(ROOT/'research/BATCH_51_CR1_RECIPES.json')['job']);folder=Path(read(job/'job.json')['campaigns'][0])
    manifest=validate(folder);snap=status(folder);rows=[];histories=[];inputs={}
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    for task,state in zip(manifest['tasks'],snap['tasks']):
        if state['phase']!='complete':continue
        result=read(folder/state['result']);path=folder/state['lipid_geometry'];audit=read(path);h=audit['history']
        if result['scenario']!=task['scenario'] or result['source_sha256']!=hashes or result['error'] or not result['completed']:raise ValueError('CR1 provenance mismatch')
        if audit['dropped'] or h[0]['time']!=0 or h[-1]['time']!=8000.:raise ValueError('Require full observed horizon')
        spans=episodes(h)
        rows.append(dict(label=task['label'],first_sampled_macro=audit['first_sampled_macro'],sampled_episodes=len(spans),
            sampled_macro_fraction=weighted(h,'macro',0.,8000.),late_fraction=weighted(h,'macro',6000.,8000.),
            last_episode=spans[-1] if spans else None,largest_final=h[-1]['largest'],simple_contours_final=h[-1]['simple_cycles'],
            sampled_port_contact_frames=sum(q['self_capture_faces']>0 for q in h),
            result_sha256=digest(folder/state['result']),geometry_sha256=digest(path)))
        histories.append((task['label'],h));inputs[str(path)]=digest(path);inputs[str(folder/state['result'])]=digest(folder/state['result'])
    if not rows:raise ValueError('No complete cases')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');out=ROOT/'outputs/diagnostics'/('RG1_'+stamp);out.mkdir(parents=True)
    recipe=ROOT/'research/diagnostic_recipes'/('RG1_'+stamp);recipe.mkdir(parents=True)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(len(rows),2,figsize=(11,3*len(rows)),squeeze=False,layout='constrained')
    for (label,h),pair in zip(histories,axes):
        times=[q['time'] for q in h]
        pair[0].plot(times,[q['largest'] for q in h],color='#168b97');pair[0].set(title=label+' · largest assembly',ylabel='L units',ylim=(0,55),xlabel='Simulated time')
        pair[1].step(times,[int(q['macro']) for q in h],where='post',color='#c46145');pair[1].set(title='Sampled simple macro contour',ylabel='Witness',ylim=(-.1,1.1),xlabel='Simulated time')
        pair[1].axvspan(6000,8000,color='#168b97',alpha=.1)
    fig.suptitle('RG1 · completed cases only; sampled geometry, no continuous first passage')
    fig.savefig(out/'geometry.png',dpi=140);plt.close(fig)
    result=dict(rows=rows,cohort_counts=snap['counts'],cohort_complete=snap['counts']['complete']==3,
        scope='Completed-case descriptive analysis, selected same seeds. Partial cohort has no decision. Episodes are sampled intervals, not exact lifetimes or rates.')
    write(out/'report.json',result)
    sources=[Path(__file__),ROOT/'experiments/mixed_calibration.py',ROOT/'scripts/campaign.py']
    for src in sources:
        dest=recipe/src.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
    proof=dict(manifest_sha256=digest(folder/'manifest.json'),inputs=inputs,
        sources={p.relative_to(recipe).as_posix():digest(p) for p in recipe.rglob('*.py')},result_sha256=digest(out/'report.json'))
    write(recipe/'recipe.json',proof)
    prior=read(ROOT/'research/BATCH_52_GEOMETRY.json') if (ROOT/'research/BATCH_52_GEOMETRY.json').exists() else None
    write(ROOT/'research/BATCH_52_GEOMETRY.json',dict(output=str(out),recipe=recipe.relative_to(ROOT).as_posix(),summary=result,previous_attempt=prior,**proof))
    shutil.copyfile(out/'geometry.png',ROOT/'research/BATCH_52_GEOMETRY.png');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
