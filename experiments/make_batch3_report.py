"""Freeze input references and make curated figures; raw summaries stay in outputs/."""
import json
from pathlib import Path
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from simulator.observations import components,simple_polygon,area
from scripts.reconstruct_experiment import export_recipe

MANIFEST=ROOT/'research/BATCH_03_RECIPES.json'


def contour_keys(pos,mat):
    n=len(pos)//2
    edges={tuple(p) for p in np.argwhere(np.triu(mat[0],1))}
    tail={tuple(p) for p in np.argwhere(np.triu(mat[1],1))}
    keys=[]
    for comp,order,cycle in components(n,edges):
        if not cycle: continue
        if not all(tuple(sorted((order[q],order[(q+1)%len(order)]))) in tail for q in range(len(order))): continue
        if simple_polygon(pos[order]) and simple_polygon(pos[n+np.array(order)]) and area(pos[order])>1:
            keys.append(tuple(sorted(comp)))
    return keys


def membrane_details(folder,result):
    starts={}; longest=0.; first=None; occupied=0; previous=None
    with np.load(folder/'trajectory.npz') as d:
        keys=[]
        for t,p,m in zip(d['times'],d['positions'],d['edges']):
            keys=contour_keys(p,m)
            if keys:
                occupied+=1
                if first is None: first=float(t)
            for key in list(starts):
                if key not in keys:
                    longest=max(longest,float(previous)-starts.pop(key))
            for key in keys: starts.setdefault(key,float(t))
            previous=t
        for key,start in starts.items(): longest=max(longest,float(previous)-start)
        final_fraction=sum(len(key) for key in keys)/result['config']['units']
        initial_edges=int(np.count_nonzero(d['edges'][0]))//2
    return dict(first_sampled_closure=first,longest_same_contour_sampled=longest,
                closed_snapshots=occupied,final_fraction_in_contours=final_fraction,
                first_recorded_lateral_edges=initial_edges,
                warning='Sampled at 1 simulated time unit; short openings between samples are not excluded')


def main():
    if MANIFEST.exists():
        refs=json.loads(MANIFEST.read_text(encoding='utf-8'))['recipes']
    else:
        refs=[]
        for p in sorted((ROOT/'research/engine_runs').glob('*/result.json')):
            r=json.loads(p.read_text(encoding='utf-8'))
            if r.get('scenario',{}).get('branch') not in ('V8','C1'): continue
            export_recipe(p.parent)
            refs.append((p.parent/'recipe.json').relative_to(ROOT).as_posix())
        MANIFEST.write_text(json.dumps({'batch':3,'recipes':refs,'policy':'Inputs and code only; generated data remains local'},indent=2),encoding='utf-8')
    rows=[]
    for ref in refs:
        folder=(ROOT/ref).parent
        r=json.loads((folder/'result.json').read_text(encoding='utf-8'))
        cfg=r['scenario']; m=r['metrics']
        row={'recipe':ref,'name':cfg['name'],'seed':cfg['seed'],'duration':cfg['duration'],
             'model':cfg['model'],'error':r['error'],'metrics':{k:v for k,v in m.items() if k not in ('history','events')}}
        if cfg['model']=='membrane': row.update(membrane_details(folder,r))
        else:
            row['co_bound_events_recounted']=sum(all(q>=0 for q in e['support']) for e in m['events'])
            row['paired_site_identities']=[e['support'] for e in m['events'] if all(q>=0 for q in e['support'])]
        rows.append(row)
    out=ROOT/'outputs/batch3'; out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    # Canonical demonstration, rerun with the current shared engine.
    demo=next(r for r in rows if r['name']=='Vesicules depuis des molecules isolees')
    folder=(ROOT/demo['recipe']).parent
    with np.load(folder/'trajectory.npz') as d:
        indices=[0,len(d['times'])//3,2*len(d['times'])//3,len(d['times'])-1]
        fig,axes=plt.subplots(1,4,figsize=(14,4),constrained_layout=True)
        for ax,q in zip(axes,indices):
            p=d['positions'][q]; n=len(p)//2
            for i in range(n): ax.plot(p[[i,n+i],0],p[[i,n+i],1],c='#bdc6cd',lw=.7)
            for row,color in ((0,'#148e9c'),(1,'#df7947')):
                for i,j in np.argwhere(np.triu(d['edges'][q,row],1)):
                    pair=np.array([i,j])+row*n
                    ax.plot(p[pair,0],p[pair,1],c=color,lw=1.5)
                ax.scatter(p[row*n:(row+1)*n,0],p[row*n:(row+1)*n,1],c=color,s=12)
            ax.set(xlim=(-.2,10.2),ylim=(-.2,10.2),title=f"t = {d['times'][q]:g}",aspect='equal')
        fig.suptitle('36 molecules libres a deux billes : aucun ruban prepare | graine 0\nContours fermes observes ; retention et permeabilite non testees')
        fig.savefig(ROOT/'research/BATCH_03_MEMBRANES.png',dpi=155);plt.close(fig)
    groups=['C1','C1scrambled','C1loose','C1bare']
    fig,axes=plt.subplots(1,2,figsize=(10,4.5),constrained_layout=True)
    labels=['001 liee','010 liee\nmeme composition','001 non liee','001 sans capture']
    for i,case in enumerate(groups):
        subset=sorted([r for r in rows if r['name']==case],key=lambda r:r['seed'])
        # Validation reruns use a different name, so the original three seeds stay unique.
        subset=subset[:3]
        for j,r in enumerate(subset):
            x=i+(j-1)*.14
            axes[0].scatter(x,r['metrics']['products'],s=45,c=['#148e9c','#df7947','#718594'][j])
            axes[1].scatter(x,r['co_bound_events_recounted'],s=45,c=['#148e9c','#df7947','#718594'][j])
    for ax in axes: ax.set(xticks=range(4),xticklabels=labels,ylim=(-.3,8.2))
    axes[0].set(title='Produits totaux a t=200',ylabel='Nombre de ligations')
    axes[1].set(title='Deux reactifs lies a des sites avant ligation')
    fig.suptitle('C1 : prototype distinct, chaine preparee de trois billes\nTrois graines ; gain net encore variable, chaine non issue de la traduction')
    fig.savefig(ROOT/'research/BATCH_03_LIGATION.png',dpi=155);plt.close(fig)
    print(json.dumps({'runs':len(rows),'errors':sum(bool(r['error']) for r in rows),
                      'summary':'outputs/batch3/summary.json','manifest':str(MANIFEST.relative_to(ROOT))}))


if __name__=='__main__':main()
