"""Passive, source-checked comparison of live-demo motion variants; no chemistry changes."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
if __package__:
    from .campaign import validate,status
else:
    from campaign import validate,status


def regular(history,interval):
    # Event-triggered observations must not overweight a more reactive variant.
    return list({round(r['time']/interval):r for r in history
        if abs(r['time']/interval-round(r['time']/interval))<1e-6}.values())


def passage(history,key,horizon):
    hit=next((r['time'] for r in history if r.get(key,0)>0),None)
    return dict(event=hit is not None,time=hit if hit is not None else horizon)


def metrics_summary(metrics,cfg):
    interval=cfg['engine']['dt']*cfg['engine']['sample_every']
    g=metrics.get('genetics',metrics);result={}
    if 'detached_copy_sets_ever' in g:
        keys=('detached_copy_sets_ever','translated_detached_ever','assembled_dimers','catalyzed_dimers',
              'catalyzed_incorporated','expressed_catalyzed_dimers','expressed_catalyzed_incorporated')
        result.update({k:g.get(k) for k in keys})
        h=g.get('history',[])
        result['first_G']=passage(h,'detached_ever',cfg['duration'])
        result['first_F']=passage(h,'translated_detached_ever',cfg['duration'])
    if cfg['model']=='membrane':
        h=regular(metrics['history'],interval)
        result.update(closed_sets_ever=metrics['closed_sets_ever'],final_closed=metrics['final_closed'],
            regular_closed_fraction=sum(bool(r['closed']) for r in h)/len(h) if h else None,
            first_closed=passage([dict(time=r['time'],hit=bool(r['closed'])) for r in h],'hit',cfg['duration']))
    m=metrics.get('membrane')
    if m:
        h=regular(m['history'],interval)
        result.update(regular_parent_closed_fraction=sum(r['parent_closed'] for r in h)/len(h) if h else None,
            regular_envelope_valid_fraction=sum(r['envelope_valid'] for r in h)/len(h) if h else None,
            final_parent_closed=m['final_parent_closed'],inserted_into_closed_parent_ever=m['inserted_into_closed_parent_ever'],
            persistent_inserted_10=m['persistent_inserted_10'],final_inside_counts=metrics.get('final_inside_counts'),
            sampled_crossings=metrics.get('sampled_crossings'))
    return result


def analyze(folder):
    folder=Path(folder).resolve();manifest=validate(folder);snap=status(folder);rows=[]
    expected={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    plan=json.loads((folder/'plan.json').read_text(encoding='utf-8'))
    for task,state,raw in zip(manifest['tasks'],snap['tasks'],plan['tasks']):
        cfg=task['scenario'];row=dict(task=task['id'],name=task['label'],preset=raw['preset'],
            comparison=raw['comparison'],phase=state['phase'],time=state.get('simulated_time',0.),
            motion=cfg.get('mechanics',{}).get('motion','brownian'),dt=cfg['engine']['dt'],seed=cfg['seed'])
        if state['phase']=='complete':
            evidence=json.loads((folder/state['result']).read_text(encoding='utf-8'))
            if evidence['scenario']!=cfg or evidence['source_sha256']!=expected or not evidence['completed'] or evidence['error']:
                raise AssertionError('Evidence provenance/completion mismatch')
            row.update(metrics=metrics_summary(evidence['metrics'],cfg),elapsed_seconds=evidence['elapsed_seconds'],
                result_sha256=hashlib.sha256((folder/state['result']).read_bytes()).hexdigest())
        if state.get('motion_audit'):
            a=json.loads((folder/state['motion_audit']).read_text(encoding='utf-8'));h=a['history']
            row['thermal_range']=[min(r['kinetic_temperature'] for r in h),max(r['kinetic_temperature'] for r in h)] if h else None
            row['thermal_last']=h[-1]['kinetic_temperature'] if h else None
            late=[r['kinetic_temperature'] for r in h if r['time']>=.75*row['time']]
            row['thermal_last_quarter_mean']=sum(late)/len(late) if late else None
            row['target_temperature']=a['target_temperature']
            row['max_step_displacement']=max((r['max_step_displacement'] for r in h),default=None)
        rows.append(row)
    report=dict(rows=rows,counts=snap['counts'],complete_cohort=all(r['phase']=='complete' for r in rows),
        analysis_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        manifest_sha256=hashlib.sha256((folder/'manifest.json').read_bytes()).hexdigest(),
        scope='Paired historical demo initial states; microseeds illustrative, fine controls selected. Regular-grid membrane samples, censored first passages. Whole-worker elapsed includes compilation/IO and contention, not matched pure-engine speed. G/F counts exclude prepared chains. Prepared J3 membrane; no validated viability or extra enzyme.')
    (folder/'demo_motion_analysis.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    lines=['# LT2 — comparaison des démos','',f"Cohorte complète : {report['complete_cohort']}",'',
        '| Scène | Mouvement | Pas | État | G/F libérés | Catalysés / réutilisés | Membrane |',
        '| --- | --- | --- | --- | --- | --- | --- |']
    for r in rows:
        m=r.get('metrics',{});boundary=m.get('regular_parent_closed_fraction',m.get('regular_closed_fraction','—'))
        lines.append(f"| {r['preset']} | {r['motion']} | {r['dt']:g} | {r['phase']} t={r['time']:g} | {m.get('detached_copy_sets_ever','—')}/{m.get('translated_detached_ever','—')} | {m.get('catalyzed_dimers','—')}/{m.get('catalyzed_incorporated','—')} | {boundary} |")
    lines+=['',report['scope'],'','Aucun classement définitif sur une cohorte incomplète. Les contrôles fins ne certifient pas la convergence.']
    (folder/'demo_motion_analysis.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines));return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path);a=p.parse_args();analyze(a.folder)
