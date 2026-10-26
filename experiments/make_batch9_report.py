"""Frozen recipes, independent sparse graph census and curated membrane figure."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.reconstruct_experiment import export_recipe
MANIFEST=ROOT/'research/BATCH_09_RECIPES.json'


def cycles(n,links):
    adjacent=[set() for _ in range(n)]
    for i,j,a,b in links:adjacent[i].add(int(j));adjacent[j].add(int(i))
    seen=set();result=[]
    for start in range(n):
        if start in seen:continue
        comp={start};todo=[start]
        while todo:
            for j in adjacent[todo.pop()]:
                if j not in comp:comp.add(j);todo.append(j)
        seen.update(comp)
        if len(comp)<3 or any(len(adjacent[i])!=2 for i in comp):continue
        order=[start];prev=-1;cur=start
        while True:
            nxt=min(adjacent[cur]-{prev})
            if nxt==start:break
            order.append(nxt);prev,cur=cur,nxt
        assert set(order)==comp;result.append(order)
    return result


def audit(folder,r):
    cfg=r['scenario']['chemistry'];n=cfg['units'];m=cfg['ring_units'];original=set(range(m))
    metrics=r['metrics'];inserted=set();closed=[];spans={};previous=set();current_spans={}
    with np.load(folder/'trajectory.npz') as data:
        p=data['positions'];times=data['times'];links=data['membrane_face_links']
        assert p.shape==(len(times),2*n+cfg['retained_probes']+cfg['permeable_probes'],2)
        assert data['edges'].size==0 and links.shape==(len(times),n,4)
        initial=metrics['initial_area']
        for k,t in enumerate(times):
            graph=links[k];graph=graph[graph[:,0]>=0]
            assert np.all(graph[:,0]<graph[:,1]) and np.all(graph[:,:2]<n)
            occupied=[(int(i),int(a)) for i,j,a,b in graph]+[(int(j),int(b)) for i,j,a,b in graph]
            assert len(occupied)==len(set(occupied)) and len({(i,j) for i,j,a,b in graph})==len(graph)
            candidates=[]
            for order in cycles(n,graph):
                xy=p[k,order];area=abs(np.dot(xy[:,0],np.roll(xy[:,1],-1))-np.dot(xy[:,1],np.roll(xy[:,0],-1)))/2
                if len(set(order)&original)>=.8*m and area>=.5*initial:candidates.append((area,order))
            # Simple-contour filtering is independently cross-checked by the
            # saved observer flag; crossed cycles are not added as insertions.
            sample=metrics['history'][k];current=set()
            if sample['parent_closed']:
                assert candidates
                current=set(max(candidates)[1])-original
                assert current==set(sample['inserted_now']);inserted.update(current)
            closed.append(bool(sample['parent_closed']))
            dt=float(t-times[k-1]) if k else 0.
            for i in current:
                current_spans[i]=current_spans.get(i,0.)+dt if i in previous else 0.
                spans[i]=max(spans.get(i,0.),current_spans[i])
            previous=current
        assert inserted==set(metrics['inserted_ids'])
        assert sum(v>=10 for v in spans.values())==metrics['persistent_inserted_10']
        assert np.mean(closed)==metrics['parent_closed_fraction']
        memory=dict(sparse_contact_bytes=links.nbytes,dense_two_row_uint8_bytes=len(times)*2*n*n)
        first_new_contact=next((float(times[k]) for k in range(len(times)) if np.any((links[k,:,0]>=0)&(links[k,:,1]>=m)&(links[k,:,0]<m))),None)
    return dict(frames=len(times),faces_saturated_at_most_once=True,independent_insertion_ids=sorted(inserted),
        first_new_old_contact_sample=first_new_contact,**memory)


def main():
    if MANIFEST.exists():refs=json.loads(MANIFEST.read_text())['recipes']
    else:
        refs=[]
        for p in sorted((ROOT/'research/engine_runs').glob('M1*/scenario.json')):
            r=json.loads((p.parent/'result.json').read_text(encoding='utf-8'))
            assert r['completed'] and not r['error'];export_recipe(p.parent)
            refs.append((p.parent/'recipe.json').relative_to(ROOT).as_posix())
        MANIFEST.write_text(json.dumps(dict(batch=9,recipes=refs,policy='Only inputs and exact sources; raw evidence stays local'),indent=2),encoding='utf-8')
    rows=[];hashes=0
    for ref in refs:
        folder=(ROOT/ref).parent;r=json.loads((folder/'result.json').read_text(encoding='utf-8'))
        recipe=json.loads((folder/'recipe.json').read_text(encoding='utf-8'))
        for name,digest in recipe['source_sha256'].items():
            assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest;hashes+=1
        row=dict(recipe=ref,name=r['scenario']['name'],seed=r['scenario']['seed'],duration=r['scenario']['duration'],
            metrics={k:v for k,v in r['metrics'].items() if k not in ('history','exchange_events')},**audit(folder,r))
        rows.append(row)
    def select(name,duration=150.):return sorted([r for r in rows if r['name']==name and r['duration']==duration],key=lambda r:r['seed'])
    # Matched initial positions, including all probes, establish a real control.
    for a,b in zip(select('M1A'),select('M1transparent')):
        with np.load((ROOT/a['recipe']).parent/'trajectory.npz') as x,np.load((ROOT/b['recipe']).parent/'trajectory.npz') as y:
            np.testing.assert_array_equal(x['positions'][0],y['positions'][0])
    out=ROOT/'outputs/batch9';out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    fig,axes=plt.subplots(1,3,figsize=(13,4.3))
    for ax,key,title in zip(axes,['parent_closed_fraction','retained_escape_fraction','permeable_entry_fraction'],
        ['Grand contour ferme (fraction)','Sondes internes sorties (fraction)','Sondes transparentes entrees (fraction)']):
        for j,name in enumerate(['M1A','M1noBondBarrier','M1transparent']):
            values=[r['metrics'][key] for r in select(name)];assert len(values)==3
            ax.scatter(j+np.linspace(-.1,.1,3),values,s=55,color=['#148e9c','#8d75bb','#df7947'][j])
        ax.set_xticks(range(3),['Avec barriere\nde lien','Contacts de\nbilles seuls','Tout\ntransparent']);ax.set_title(title,fontsize=10)
        ax.set_ylim(-.03,1.03);ax.grid(axis='y',alpha=.2)
    fig.suptitle('219 dimeres prepares + 24 libres : selectivite locale, t=150, trois graines')
    fig.text(.5,.015,'Sondes inertes ; etats non classables rapportes dans le bilan. Aucune insertion durable validee.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.07,1,.94]);fig.savefig(ROOT/'research/BATCH_09_MEMBRANE.png',dpi=160);plt.close(fig)
    print(json.dumps(dict(runs=len(rows),source_hashes_verified=hashes,material_frames=sum(r['frames'] for r in rows),
        positive_insertions=[dict(name=r['name'],seed=r['seed'],duration=r['duration'],ids=r['independent_insertion_ids']) for r in rows if r['independent_insertion_ids']])))


if __name__=='__main__':main()
