"""Curated CT1 comparison from the validated local report; no raw data bundled."""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read
from scripts.campaign import digest


def main():
    job=Path(read(ROOT/'research/BATCH_40_RECIPES.json')['job']);state=read(job/'state.json')
    report=Path(state['report_0'])
    if digest(report)!=state['report_0_sha256']:raise ValueError('CT1 report changed')
    rows=read(report)['rows'];fig,axes=plt.subplots(1,4,figsize=(13,4.1))
    panels=[('F_new','F nouveaux libérés'),('wholly_constructed_detached_F','F entièrement alimentaires'),
        ('active_wholly_constructed_F','Dont actifs sur P/R'),('operations_by_wholly_constructed_F','Opérations de ces F')]
    x=np.arange(3)
    for ax,(key,title) in zip(axes,panels):
        for v,shift,color,label in (('legacy',-.18,'#637a94','Capture35'),('matched',.18,'#149b97','Capture E/largeur²')):
            group=[next(r for r in rows if r['label']==f'CT1_{v}_s{s}') for s in range(3)]
            values=[r[key] if key=='F_new' else r['renewal'][key] for r in group]
            bars=ax.bar(x+shift,values,.34,color=color,label=label);ax.bar_label(bars,padding=2,fontsize=9)
        ax.set_title(title,fontsize=10);ax.set_xticks(x,['Graine0','Graine1','Graine2']);ax.set_ylim(0,16)
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
    fig.legend(*axes[0].get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.5,.89),ncol=2,frameon=False,fontsize=9)
    fig.suptitle('CT1 · reconstruction conservée, activité variable · 9 essais terminés',fontsize=13)
    fig.text(.5,.015,'Témoins sans gène : aucun nouveau F (3/3). Stocks finis, aucun H/T dans ces bains. Ce résultat ne prouve pas la coexistence.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.07,1,.81]);dest=ROOT/'research/BATCH_41_CT1.png';fig.savefig(dest,dpi=150);plt.close(fig)
    print(dest)


if __name__=='__main__':main()
