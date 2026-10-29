"""Source-checked synthesis of P10/MIX1/MIX2 and its LT1 chemical transfer."""
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
import statistics
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status
from scripts.population_report import summarize
from experiments.audit_polymer_lineage import audit

FOLDERS=dict(P10=ROOT/'outputs/campaigns/campaign_20261029T120049792477Z',
    MIX1=ROOT/'outputs/mixing_campaigns/campaign_20261029T123103222882Z',
    MIX2=ROOT/'outputs/motion_campaigns/campaign_20261029T132411069082Z',
    LT1=ROOT/'outputs/transfer_campaigns/campaign_20261029T172315655927Z')


def review():
    reports={};inputs={}
    for name,folder in FOLDERS.items():
        manifest=validate(folder);state=status(folder)
        if state['controller_active'] or state['counts']['complete']!=len(manifest['tasks']):
            raise ValueError('Full completed cohort required: '+name)
        expected={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
        for task,s in zip(manifest['tasks'],state['tasks']):
            path=folder/s['result'];result=json.loads(path.read_text())
            if result['scenario']!=task['scenario'] or result['source_sha256']!=expected or not result['completed'] or result['error']:
                raise AssertionError('Scenario, result or code mismatch')
            inputs[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
        file={'P10':'population_analysis.json','MIX1':'mixing_analysis.json','MIX2':'motion_analysis.json','LT1':'population_analysis.json'}[name]
        report=json.loads((folder/file).read_text())
        report_source='population_report.py' if name in ('P10','LT1') else 'mixing_report.py' if name=='MIX1' else 'motion_report.py'
        if report['analysis_sha256']!=manifest['source_sha256'][report_source]:
            raise AssertionError('Expected frozen full-cohort analysis source')
        if not report['complete_cohort']:raise AssertionError('Incomplete cached report')
        reports[name]=report
    lineage={name:audit(FOLDERS[name]) for name in ('P10','LT1')}
    populations=[]
    datasets=[(study,task,row) for study in ('P10','LT1') for task,row in zip(validate(FOLDERS[study])['tasks'],reports[study]['rows'])]
    for study,task,row in datasets:
        raw=json.loads((FOLDERS[study]/status(FOLDERS[study])['tasks'][int(task['id'][4:])]['population']).read_text())
        rebuilt=summarize(raw,task['scenario'])
        if rebuilt!=row['population']:raise AssertionError('Population report cannot be independently rebuilt')
        target=raw['target'];bad=[]
        for frame in raw['state']['snapshots']:
            for t in frame['types']:
                seq=t['sequence']
                if t['topology']!='open' or t['length']>len(target) or (seq not in target and seq[::-1] not in target):
                    bad.append(dict(time=frame['time'],type=t))
        f=rebuilt['instantaneous_final'];l=next(x for x in lineage[study]['rows'] if x['task']==task['id'])
        populations.append(dict(study=study,case=row['case'],seed=row['seed'],new_exact=f['exact_new'],
            new_polymer_count=f['polymer_chains_new'],fragment_count=f['polymer_chains_new']-f['exact_new'],
            exact_fraction_of_new_polymer_units=f['exact_fraction_of_polymer_units'],
            monomers=sum(f['free_monomers_by_symbol'].values()),histogram=rebuilt['final_length_distribution'],
            off_target_observations=len(bad),original_backbone_always_present=rebuilt['original_backbone_always_present'],
            first_reserve_below_half=rebuilt['first_reserve_below_half'],lineage=l,
            at800=next(r for r in rebuilt['series'] if r['time']==800),series=rebuilt['series']))
    groups=[]
    for kind,gamma in (('brownian',4.),('langevin',.1),('dpd',.5),('dpd',2.)):
        rows=[r for r in reports['MIX2']['rows'] if r['temperature']==.08 and r['dt']==.005 and r['motion']==kind and r['damping']==gamma]
        if len(rows)!=3:raise AssertionError('Expected three-seed cold group')
        goals={}
        for goal in ('occupation','neighbor_replacement','positional_memory','half_partners','joint_mixing'):
            events=[r['goals'][goal] for r in rows];all_hit=all(v['event'] for v in events)
            clocks=[v['clock']['steady_high'] for v in events]
            goals[goal]=dict(events=sum(v['event'] for v in events),censored=sum(not v['event'] for v in events),
                median_seconds=statistics.median(clocks) if all_hit else None,
                min_seconds=min(clocks) if all_hit else None,max_seconds=max(clocks) if all_hit else None,
                clock_endpoints=clocks)
        groups.append(dict(motion=kind,damping=gamma,goals=goals,
            thermal_ok=all(r['temperature_screen_ok'] for r in rows)))
    report=dict(populations=populations,motion_groups=groups,inputs=inputs,
        cohorts={name:len(r['rows']) for name,r in reports.items()},
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        limitations='Three seeds only; machine contention, unequal inert-gas horizons and selected warm/dt controls explicit. Population failure is fragment competition, not a measured point-mutation rate. LT1 uses the selected thermostat in two separate genetic/expression baths, no membrane or functional enzyme validation.')
    out=ROOT/'outputs/reviews'/('completed_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    (out/'review.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (out/'driver.py').write_bytes(Path(__file__).read_bytes());draw(out,report,reports)
    print(json.dumps(dict(folder=str(out),cohorts=report['cohorts'],off_target_observations=sum(r['off_target_observations'] for r in populations),motion_groups=groups)))
    return out


def draw(out,report,reports):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,axes=plt.subplots(2,2,figsize=(13,8),constrained_layout=True)
    for p in report['populations']:
        if p['case']!='P10_copy_reserve1':continue
        s=p['series'];label=f"seed {p['seed']}"
        axes[0,0].plot([r['time'] for r in s],[r['exact_fraction_of_polymer_units'] if r['exact_fraction_of_polymer_units'] is not None else np.nan for r in s],label=label)
        axes[0,1].plot([r['time'] for r in s],[sum(r['free_monomers_by_symbol'].values()) for r in s],label=label)
    axes[0,0].set(title='P10 : fraction des unités polymérisées en copies exactes',xlabel='Temps simulé',ylim=(0,1))
    axes[0,1].set(title='P10 : monomères libres (départ400)',xlabel='Temps simulé')
    goals=('neighbor_replacement','occupation','positional_memory');names=('Voisins','Occupation','Mémoire')
    for i,g in enumerate(report['motion_groups']):
        x=np.arange(3)+(i-1.5)*.18
        y=np.array([g['goals'][k]['median_seconds'] for k in goals])
        low=y-np.array([g['goals'][k]['min_seconds'] for k in goals]);high=np.array([g['goals'][k]['max_seconds'] for k in goals])-y
        axes[1,0].bar(x,y,width=.18,yerr=[low,high],capsize=2,label=f"{g['motion']} g={g['damping']}")
    axes[1,0].set_xticks(np.arange(3),names);axes[1,0].set_yscale('log')
    axes[1,0].set(title='MIX2 froid : médiane3 graines et étendue',ylabel='Secondes réelles de calcul')
    warm=[r for r in reports['MIX2']['rows'] if r['temperature']==.6]
    axes[1,1].bar([r['motion'] for r in warm],[r['goals']['joint_mixing']['clock']['steady_high'] for r in warm])
    axes[1,1].set(title='MIX2 chaud : mélange conjoint, une graine',ylabel='Secondes réelles de calcul')
    for ax in axes.flat:
        ax.grid(axis='y',alpha=.2)
        if ax.get_legend_handles_labels()[0]:ax.legend(fontsize=8)
    fig.suptitle('44 essais principaux achevés : progrès mécanique et verrou de copie distincts')
    fig.savefig(out/'review.png',dpi=140);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),constrained_layout=True)
    for ax,mode,title in zip(axes,('copy','expression'),('Copies G complètes nouvelles','Chaînes F complètes nouvelles')):
        for offset,study,label,color in ((-.18,'P10','Brownien','#3583b9'),(.18,'LT1','Langevin0,1','#df8d30')):
            case=f'P10_{mode}_reserve1' if study=='P10' else f'LT1_{mode}'
            values=[next(p['new_exact'] for p in report['populations'] if p['case']==case and p['seed']==seed) for seed in range(3)]
            ax.bar(np.arange(3)+offset,values,width=.36,label=label,color=color)
        ax.set(title=title,xlabel='Graine',ylabel='Nombre à t=3200');ax.set_xticks([0,1,2]);ax.legend();ax.grid(axis='y',alpha=.2)
    fig.suptitle('Même stock, mêmes réactions : transfert mécanique sans nouvelle protéine')
    fig.savefig(out/'chemical_transfer.png',dpi=150);plt.close(fig)


if __name__=='__main__':review()
