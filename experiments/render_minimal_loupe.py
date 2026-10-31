"""Curated pre/near/post-ligation plate from validated passive local captures."""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.review_minimal_diagnostic import review
from simulator.campaign_io import read
from scripts.campaign import validate,status


def render():
    folder,report=review()
    if report['controller_active'] or report['counts']['complete']!=2:raise ValueError('Require both diagnostic replays complete')
    assert all(r['physical_replay_exact'] for r in report['rows'])
    st=status(folder);target=next(t for t in st['tasks'] if t['label']=='MIN1D_short_s0')
    audit=read(folder/target['genetic_audit']);capture=audit['state']['loupe']['captures'][0]
    formed=next(e['time'] for e in capture['outcomes'] if e['kind']=='formed')
    frames=capture['frames'];chosen=[frames[0],min(frames,key=lambda f:abs(f['time']-formed+.02)),
        next(f for f in frames if f['time']>formed+1e-9)]
    i,j,a,b=capture['target'];supports=[i,j,a,b]
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(11,4.4));core_cloud=[]
    for frame in chosen:
        pos=dict(zip(frame['ids'],frame['positions']));core_cloud.extend(pos[q] for q in supports)
    cloud=np.array(core_cloud);lo=cloud.min(axis=0)-.8;hi=cloud.max(axis=0)+.8
    for ax,frame in zip(axes,chosen):
        pos={k:np.array(v) for k,v in zip(frame['ids'],frame['positions'])};core=set(supports)
        for x,y in frame['bonds']['scaffold']:
            if x in supports:core.add(y)
        context=[q for q in frame['ids'] if q not in core]
        if context:ax.scatter(*np.array([pos[q] for q in context]).T,c='#a6abb5',s=18,alpha=.35)
        styles=dict(scaffold=('#71818b',2),backbone=('#34414c',3),pairing=('#d8a32a',1.5))
        for kind,pairs in frame['bonds'].items():
            color,width=styles.get(kind,('#999999',1))
            for x,y in pairs:
                if x in core and y in core:ax.plot(*np.array([pos[x],pos[y]]).T,c=color,lw=width,zorder=1)
        for q in supports:
            color='#167d9a' if q in (i,j) else '#91549b';p=pos[q]
            ax.scatter(*p,c=color,s=95,zorder=3);ax.annotate(('G' if q in (i,j) else 'F')+str(q),p,xytext=(5,5),textcoords='offset points',fontsize=9)
        for q in core-set(supports):ax.scatter(*pos[q],c='#e69b3e',s=42,zorder=3)
        g=frame['geometry'];ax.set_title(f"t={frame['time']:.2f} · {g['reason']}\nd={g['distance']:.3f} · obliquité max={max(g['skew']):.3f}",fontsize=10)
        ax.set_xlim(lo[0],hi[0]);ax.set_ylim(lo[1],hi[1]);ax.set_aspect('equal');ax.grid(alpha=.13)
    fig.suptitle('MIN1D · double capture tardive puis ligation réelle à t916,40',fontsize=12)
    fig.text(.5,.02,'G bleu · F violet · reconnaisseurs orange · liaisons réelles seulement · contexte tronqué, forces extérieures non représentées',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.05,1,.94));path=ROOT/'research/BATCH_33_LOUPE.png';fig.savefig(path,dpi=150);plt.close(fig)
    print(path);return path


if __name__=='__main__':render()
