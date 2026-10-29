"""Compare sampled mixing goals against measured compute clocks, with censoring."""
import argparse
import hashlib
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
if __package__:
    from .campaign import validate,status
else:
    from campaign import validate,status
from simulator.campaign_io import read,write


def clock_bounds(performance,time):
    history=performance['history']
    warm=next((r['compute_seconds'] for r in history if r['time']>=2.5-1e-8),0.)
    high=next((i for i,r in enumerate(history) if r['time']>=time-1e-8),len(history)-1)
    low=max(0,high-1)
    return dict(including_warmup_low=history[low]['compute_seconds'],
        including_warmup_high=history[high]['compute_seconds'],
        steady_low=max(0.,history[low]['compute_seconds']-warm),
        steady_high=max(0.,history[high]['compute_seconds']-warm),
        warmup_seconds=warm,goal_in_warmup=time<=2.5)


def analyze(folder):
    folder=Path(folder).resolve();manifest=validate(folder);snapshot=status(folder);rows=[]
    expected={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    for task,state in zip(manifest['tasks'],snapshot['tasks']):
        cfg=task['scenario'];c=cfg['chemistry']
        row=dict(task=task['id'],name=task['label'],seed=cfg['seed'],phase=state['phase'],
            motion=c['motion'],damping=c['damping'],dt=cfg['engine']['dt'],temperature=c['temperature'])
        if state.get('mixing') and (folder/state['mixing']).exists():
            m=read(folder/state['mixing']);h=m['history'];row.update(metrics=m,sampled_until=h[-1]['time'])
            if state.get('performance'):
                perf=read(folder/state['performance']);goals={}
                for name,p in m['first_passages'].items():
                    goals[name]=dict(p,clock=clock_bounds(perf,p['time']))
                row['goals']=goals;row['compute_seconds']=perf['compute_seconds']
                row['performance_path']=state['performance']
            kinetic=[r['motion']['kinetic_temperature'] for r in h if 'motion' in r and r['time']>=20.]
            row['temperature_range_after20']=[min(kinetic),max(kinetic)] if kinetic else None
            row['temperature_screen_ok']=not kinetic or min(kinetic)>=.5*c['temperature'] and max(kinetic)<=2*c['temperature']
            if 'motion' in h[-1]:
                d=h[-1]['motion'];row['force_evaluations_per_step']=d['force_evaluations']/max(1,d['steps'])
                row['thermostat_pair_visits_per_step']=d['thermostat_pair_visits']/max(1,d['steps'])
                row['max_step_displacement']=d['max_step_displacement']
                row['max_sampled_bond_extension']=max(r['motion']['max_bond_extension'] for r in h)
        if state['phase']=='complete':
            evidence=read(folder/state['result'])
            if evidence['scenario']!=cfg or evidence['source_sha256']!=expected or not evidence['completed']:
                raise AssertionError('Motion result differs from frozen scenario or source')
            row.update(source_verified=True,elapsed_seconds=evidence['elapsed_seconds'])
        rows.append(row)
    report=dict(counts=snapshot['counts'],controller_active=snapshot['controller_active'],rows=rows,
        complete_cohort=all(r['phase']=='complete' for r in rows),
        analysis_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        limitations='Different fixed horizons; no-event goals censored, never omitted. Compute clocks include diagnostics but exclude checkpoint I/O; full elapsed includes startup/I/O. Warmup first2.5 simulated units also reported separately. Two workers and other jobs can affect wall time. No chemical reaction throughput validated.')
    write(folder/'motion_analysis.json',report)
    lines=['# MIX2 — rendement de mélange par temps réel', '',
        'Temps des premiers seuils échantillonnés ; bornes calculées depuis les segments de250 pas.',
        'Absence de seuil = censurée, pas échec définitif. Horizon12000 pour témoins lents,1600 pour variantes rapides.', '',
        '| Variante | Graine | État | Temps observé | Voisins : secondes réelles après échauffement | Occupation : secondes réelles après échauffement | Mélange conjoint tenu | T après20 |',
        '| --- | ---: | --- | ---: | --- | --- | --- | --- |']
    for row in rows:
        def cell(name):
            if name not in row.get('goals',{}):return '—'
            g=row['goals'][name];clock=g['clock']
            if not g['event']:return f">={clock['steady_high']:.3g} (censuré)"
            return f"{clock['steady_low']:.3g}–{clock['steady_high']:.3g}"
        lines.append(f"| {row['name']} | {row['seed']} | {row['phase']} | {row.get('sampled_until',0):g} | {cell('neighbor_replacement')} | {cell('occupation')} | {cell('joint_mixing')} | {row.get('temperature_range_after20')} |")
    lines+=['', 'Détail des contacts,50% des partenaires, MI, stabilité et coût des paires : motion_analysis.json.',
        'La référence MIX1 continue séparément ; les nouveaux témoins partent tous de la même géométrie sans compression initiale.',
        'Un gain de déplacement ne vaut pas gain de réaction. Aucun modèle de cellule modifié.']
    (folder/'motion_analysis.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if any('performance_path' in r for r in rows):draw(folder,rows)
    print('\n'.join(lines),flush=True);return report


def draw(folder,rows):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,axes=plt.subplots(2,2,figsize=(12,8),constrained_layout=True)
    for row in rows:
        if 'performance_path' not in row or row['seed']!=0 or row['dt']!=.005 or row['temperature']!=.08:continue
        h=row['metrics']['history'];p=read(folder/row['performance_path'])['history']
        times=np.array([v['time'] for v in p]);seconds=np.array([v['compute_seconds'] for v in p])
        warm=seconds[np.searchsorted(times,2.5)] if times[-1]>=2.5 else 0.
        x=np.interp([v['time'] for v in h],times,seconds)-warm;keep=x>0
        label=f"{row['motion']} g={row['damping']:g}"
        for ax,y in zip(axes.flat,([v['right_fraction'] for v in h],
            [v['neighbor_retention_excess'] for v in h],
            [v['contacts']['0.3']['mean_distinct_partners'] for v in h],
            [v['corrected_normalized_mi'] for v in h])):
            ax.plot(x[keep],np.asarray(y)[keep],label=label)
    for ax,title in zip(axes.flat,('Occupation droite','Mémoire des voisins, excès','Partenaires uniques, rayon0,3','Mémoire des positions, MI corrigée')):
        ax.set_title(title);ax.set_xlabel('Secondes réelles de calcul après échauffement');ax.set_xscale('log');ax.grid(alpha=.2)
        if ax.get_legend_handles_labels()[0]:ax.legend(fontsize=8)
    axes[0,0].axhline(.5,color='k',ls='--',lw=.7);axes[0,1].axhline(.1,color='k',ls='--',lw=.7)
    axes[1,0].axhline(99.5,color='k',ls='--',lw=.7);axes[1,1].axhline(.1,color='k',ls='--',lw=.7)
    fig.suptitle('MIX2 : coût réel, diagnostics inclus — graine0, cohorte à vérifier')
    fig.savefig(folder/'motion_analysis.png',dpi=140);plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',nargs='?',type=Path);a=p.parse_args()
    folder=a.folder or Path((ROOT/'outputs/motion_campaigns/latest.txt').read_text(encoding='utf-8').strip())
    analyze(folder)
