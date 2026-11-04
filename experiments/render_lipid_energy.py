"""Curated complete L2 cohort, with frozen thresholds and reused case explicit."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.lipid_energy_followup import latest
from simulator.campaign_io import read
from experiments.review_lipid_energy import collect
from experiments.prepare_lipid_energy import VARIANTS


def plot(rows,variants=VARIANTS,names=('L1','Porte','Contacts','Combinés','Délié','Sans bonus','Sans outil'),
         path=ROOT/'research/BATCH_37_RESULTS.png',title='L2 achevé · production conservée, crible thermique refusé · L1 graine0 réutilisée',prefix='L2'):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,axes=plt.subplots(1,3,figsize=(13,4.5),constrained_layout=True)
    for ax,key,subplot_title in zip(axes,('lipids','mean_T_late','p95_T_after5'),
        ('Lipides produits à100','Température moyenne, dernier quart','95e percentile de T après5')):
        for seed,color in enumerate(('#168f99','#b27840','#7b62a3')):
            values=[next(x[key] for x in rows if x['label']==f'{prefix}_{v}_s{seed}') for v in variants]
            ax.scatter(np.arange(7)+(seed-1)*.17,values,c=color,s=30,label=f'Graine{seed}',zorder=3)
        ax.set_xticks(range(7),names,rotation=45,ha='right');ax.set_title(subplot_title);ax.grid(axis='y',alpha=.2)
        if key=='mean_T_late':ax.axhspan(.04,.12,color='#5ea978',alpha=.16)
        if key=='p95_T_after5':ax.axhline(.24,color='#ba5142',ls='--',lw=1)
    axes[0].legend(fontsize=8);fig.suptitle(title,fontsize=12)
    fig.savefig(path,dpi=150);plt.close(fig)


def main():
    job=latest();r=collect(Path(read(job/'job.json')['campaigns'][0]));plot(r['rows'])


if __name__=='__main__':main()
