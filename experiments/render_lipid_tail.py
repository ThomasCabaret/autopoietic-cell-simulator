"""Selected unchanged-law thermal tails, with the productive transient visible."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.lipid_curvature_followup import latest
from scripts.campaign import validate,status
from simulator.campaign_io import read
from experiments.lipid_thermal_tail import collect


def main():
    job=latest(True);folder=Path(read(job/'job.json')['campaigns'][0]);report=collect(folder);m=validate(folder);s=status(folder)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4),constrained_layout=True)
    for t,st,color in zip(m['tasks'],s['tasks'],('#168f99','#b27840','#7b62a3')):
        g=read(folder/st['result'])['metrics'];h=read(folder/st['motion_audit'])['history'];seed=t['scenario']['seed']
        axes[0].step([x['time'] for x in g['history']],[x['lipids'] for x in g['history']],where='post',c=color,label=f'Graine{seed}')
        bins=[]
        for start in range(0,400,25):
            v=[x['kinetic_temperature'] for x in h if start<=x['time']<start+25]
            bins.append(sum(v)/len(v))
        axes[1].plot([12.5+25*i for i in range(16)],bins,c=color,marker='o',ms=3,label=f'Graine{seed}')
    axes[0].set(title='Production réelle : stocks finis',xlabel='Temps simulé',ylabel='H–T fabriqués',ylim=(0,25))
    axes[1].axhspan(.04,.12,color='#5ea978',alpha=.12);axes[1].axhline(.08,color='#3f7859',ls='--',lw=1)
    axes[1].set(title='Température moyenne par tranches25',xlabel='Temps simulé',ylabel='Température cinétique')
    for ax in axes:ax.axvline(100,color='#777',ls=':',lw=1);ax.grid(alpha=.15)
    axes[0].legend();fig.suptitle('L4 sélectionné · trois préfixes exacts · refroidissement après la phase productive')
    fig.savefig(ROOT/'research/BATCH_39_RESULTS.png',dpi=150);plt.close(fig)


if __name__=='__main__':main()
