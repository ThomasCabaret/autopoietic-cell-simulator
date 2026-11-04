"""Curated endpoints and thermal trace of the one L1 pilot; no dynamics feedback."""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.review_lipid_pilot import review
from simulator.campaign_io import read
from simulator.engine import Simulation
from simulator.checkpoint import source_hashes
from scripts.campaign import status


def main():
    report=review();folder=Path(report['campaign']);s=status(folder);state=s['tasks'][0]
    result=read(folder/state['result']);cfg=result['scenario'];prefix=4*cfg['chemistry']['tool_count'];n=cfg['chemistry']['food_units']
    with np.load(folder/state['checkpoint'],allow_pickle=False) as data:
        pos=data['positions'].copy();meta=json.loads(str(data['metadata']))
    if meta['source_sha256']!=source_hashes():raise ValueError('Render initial state using exact archived sources')
    initial=Simulation(cfg).chemistry.pos;chem=meta['chemistry'];rungs=chem['lipids']['rungs'];mapping=dict(rungs)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(14,4.6),constrained_layout=True)
    def scene(ax,p,bonds,links,title):
        for h,t in bonds:ax.plot(p[[h,t],0],p[[h,t],1],color='#547d8d',lw=1.2,zorder=1)
        for i,j,_,_ in links:
            for a,b in ((i,j),(mapping[i],mapping[j])):ax.plot(p[[a,b],0],p[[a,b],1],color='#075d70',lw=2,zorder=1)
        k=prefix//2
        for i,j in chem['host']['edges']:ax.plot(p[[i,j],0],p[[i,j],1],color='#965297',lw=2.5,zorder=2)
        for i in range(k):ax.plot(p[[i,k+i],0],p[[i,k+i],1],color='#965297',lw=1,zorder=1)
        ax.scatter(p[:prefix,0],p[:prefix,1],c='#965297',s=20,label='F préparés')
        ax.scatter(p[prefix:prefix+n,0],p[prefix:prefix+n,1],c='#169d9c',s=20,label='H')
        ax.scatter(p[prefix+n:,0],p[prefix+n:,1],c='#d5963b',s=20,label='T')
        ax.set(xlim=(0,12),ylim=(0,9),aspect='equal',title=title);ax.grid(alpha=.15)
    scene(axes[0],initial,[],[],'Départ : quatre F01 et H/T libres')
    scene(axes[1],pos,rungs,chem['lipids']['links'],'À100 :22 H–T,16 contacts latéraux')
    axes[0].legend(loc='lower left',fontsize=8)
    thermal=read(folder/state['motion_audit'])['history'];history=result['metrics']['history'];ax=axes[2]
    ax.plot([h['time'] for h in thermal],[h['kinetic_temperature'] for h in thermal],color='#af5538',lw=1,label='T cinétique')
    ax.axhline(.08,color='#af5538',ls='--',lw=1,label='Consigne0,08');ax.set(xlabel='Temps simulé',ylabel='Température cinétique',title='Dette énergétique visible')
    second=ax.twinx();second.plot([h['time'] for h in history],[h['lipids'] for h in history],color='#128787',label='H–T fabriqués')
    second.set(ylabel='H–T fabriqués',ylim=(0,25));ax.legend(loc='upper right',fontsize=8);second.legend(loc='lower right',fontsize=8)
    fig.suptitle('L1 · prototype séparé, une graine · outil existant et partenaires réels',fontsize=13)
    fig.savefig(ROOT/'research/BATCH_36_LIPIDS.png',dpi=150);plt.close(fig)


if __name__=='__main__':main()
