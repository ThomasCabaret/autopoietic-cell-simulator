"""Progressive mechanics-only mixing report and compact scientific figures."""
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


def analyze(folder,plots=True):
    folder=Path(folder).resolve();manifest=validate(folder);snapshot=status(folder);rows=[]
    expected={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    for task,state in zip(manifest['tasks'],snapshot['tasks']):
        row=dict(task=task['id'],name=task['label'],seed=task['scenario']['seed'],phase=state['phase'],
            scenario=task['scenario'],latest=state.get('mixing_latest'))
        if state.get('mixing') and (folder/state['mixing']).exists():row['metrics']=read(folder/state['mixing'])
        if state['phase']=='complete':
            result=read(folder/state['result'])
            if result['source_sha256']!=expected or result['scenario']!=task['scenario'] or not result['completed']:
                raise AssertionError('Mixing result differs from the frozen source/scenario')
            row.update(metrics=result['metrics'],elapsed_seconds=result['elapsed_seconds'],source_verified=True)
        rows.append(row)
    report=dict(counts=snapshot['counts'],controller_active=snapshot['controller_active'],rows=rows,
        complete_cohort=all(r['phase']=='complete' for r in rows),
        analysis_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    # Same seed/physical case: only observation cadence differs in the fine control.
    fine=next((r for r in rows if r['name'].endswith('_fine') and 'metrics' in r),None)
    standard=next((r for r in rows if r['name']=='MIX1_T0.6_cores_b2' and r['seed']==0 and 'metrics' in r),None)
    if fine and standard:
        a=fine['metrics']['history'][-1]
        b=next((h for h in standard['metrics']['history'] if h['time']==a['time']),None)
        if b:
            report['contact_cadence_comparison']=dict(time=a['time'],
                D_fine=a['short_lag_bulk_D'],D_standard=b['short_lag_bulk_D'],
                fine=a['contacts'],standard=b['contacts'],
                spatial_msd_equal=a['mean_square_displacement']==b['mean_square_displacement'],
                scope='Same physical seed/path, not an independent replicate. Episode counts depend on sampling and Brownian recrossings.')
    write(folder/'mixing_analysis.json',report)
    lines=['# MIX1 — dispersion, mémoire et rencontres', '',
        'Aucune réaction chimique. Boîte à parois souples du moteur, molécules fixes, pas de flux ou vitesse inertielle.',
        'Les contacts géométriques ne sont pas des réactions éligibles. Les premiers seuils sont descriptifs et les absences censurées.', '',
        '| Cas | Graine | État | Temps | Fraction à droite | Mémoire des 5 voisins, excès | Partenaires distincts, rayon0,3 | D court / idéal |',
        '| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |']
    for row in rows:
        metrics=row.get('metrics');h=metrics['history'][-1] if metrics else row['latest']
        if h:
            pred=.25*row['scenario']['chemistry']['temperature']/row['scenario']['chemistry']['beads_per_molecule']
            D=h['short_lag_bulk_D']
            measured=f'{D:.4g}' if D is not None else '—'
            lines.append(f"| {row['name']} | {row['seed']} | {row['phase']} | {h['time']:g} | {h['right_fraction']:.3f} | {h['neighbor_retention_excess']:.3f} | {h['contacts']['0.3']['mean_distinct_partners']:.2f} | {measured} / {pred:.4g} |")
        else:lines.append(f"| {row['name']} | {row['seed']} | {row['phase']} | — | — | — | — | — |")
    lines+=['', 'Séries, MI corrigée par permutations, grille spatiale, clusters et temps de contact : mixing_analysis.json.',
        'Courbes : mixing_analysis.png. D court est une mesure locale, pas une preuve de diffusion libre à longue portée.',
        'Une convection uniforme peut transporter sans mélanger : renouvellement des voisins et répartition spatiale sont distincts.']
    (folder/'mixing_analysis.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if plots and any('metrics' in r for r in rows):draw(folder,rows)
    print('\n'.join(lines),flush=True);return report


def draw(folder,rows):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,axes=plt.subplots(2,3,figsize=(15,8),constrained_layout=True)
    for row in rows:
        if 'metrics' not in row:continue
        c=row['scenario']['chemistry']
        if c['beads_per_molecule']!=2 or not c['steric'] or row['name'].endswith('_fine'):continue
        h=row['metrics']['history'];t=np.array([r['time'] for r in h]);ax=axes[0 if c['temperature']==.08 else 1]
        label=f"seed {row['seed']}"
        ax[0].plot(t,[r['right_fraction'] for r in h],label=label)
        ax[1].plot(t,[r['neighbor_retention_excess'] for r in h],label=label)
        ax[1].plot(t,[r['corrected_normalized_mi'] for r in h],ls=':',alpha=.7)
        ax[2].plot(t,[r['contacts']['0.3']['mean_distinct_partners'] for r in h],label=label)
    for i,T in enumerate((.08,.6)):
        axes[i,0].axhline(.5,color='k',ls='--',lw=.8)
        axes[i,0].set_title(f'T={T}: occupation de la moitié droite')
        axes[i,1].set_title('Mémoire: voisins (trait), position (pointillé)')
        axes[i,2].set_title('Partenaires distincts, rayon 0,3')
        for ax in axes[i]:
            ax.set_xlabel('Temps simulé');ax.grid(alpha=.2)
            if ax.get_legend_handles_labels()[0]:ax.legend(fontsize=8)
    fig.suptitle('200 dimères, mécanique seule — observations finies, sans preuve de réaction')
    fig.savefig(folder/'mixing_analysis.png',dpi=140);plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',nargs='?',type=Path)
    p.add_argument('--no-plots',action='store_true');a=p.parse_args()
    folder=a.folder or Path((ROOT/'outputs/mixing_campaigns/latest.txt').read_text(encoding='utf-8').strip())
    analyze(folder,not a.no_plots)
