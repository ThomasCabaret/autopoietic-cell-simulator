"""Curated full-cohort MIN1R material/activity figure with explicit censoring."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.review_renewal import review


def render():
    report=review()
    if len(report['rows'])!=9 or report['controller_active']:raise ValueError('Require complete inactive cohort')
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    variants=('active','split','nogene');labels=('F01 construit','Même F01 délié','Sans gène')
    fig,axes=plt.subplots(1,2,figsize=(10,4.3));colors=('#167d9a','#d58328','#7763a8')
    for seed,color in enumerate(colors):
        rows=[next(r for r in report['rows'] if r['label']==f'MIN1R_{v}_s{seed}') for v in variants]
        x=np.arange(3)+(seed-1)*.12
        counts=[r['renewal']['active_wholly_constructed_F'] for r in rows]
        axes[0].scatter(x,counts,c=color,s=50,label=f'Graine {seed}',zorder=3)
        for xx,row in zip(x,rows):
            first=row['renewal']['first_operation_by_wholly_constructed_F']
            axes[1].scatter(xx,1200. if first is None else first,edgecolors=color,
                facecolors='none' if first is None else color,marker='^' if first is None else 'o',s=58,zorder=3)
    for ax in axes:
        ax.set_xticks(range(3),labels,rotation=10);ax.grid(axis='y',alpha=.2)
    axes[0].set_ylim(bottom=-.25);axes[0].set_ylabel('Nouveaux F entièrement neufs et actifs');axes[0].legend(frameon=False)
    axes[1].set_ylim(0,1320);axes[1].set_ylabel('Premier acte catalytique, temps simulé')
    axes[1].axhline(1200,color='#888888',lw=1,ls=':');axes[1].text(.02,.96,'△ absence observée : censurée à1200',transform=axes[1].transAxes,fontsize=9,va='top')
    fig.suptitle('MIN1R · nouveaux outils entièrement refaits depuis P/R · lois MD2 inchangées',fontsize=12)
    fig.text(.5,.015,'150 billes, stocks fermés ; F initial exclu, chaque composite du remplaçant vient de P/R libres. Pas de maintien intégré.',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.07,1,.94));path=ROOT/'research/BATCH_34_RENEWAL.png';fig.savefig(path,dpi=160);plt.close(fig)
    print(path);return path


if __name__=='__main__':render()
