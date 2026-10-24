"""Curated E3 synthesis; raw run summaries and trajectories stay local."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.reconstruct_experiment import export_recipe
from simulator.observations import components
MANIFEST=ROOT/'research/BATCH_05_RECIPES.json'
MISLABELLED={'E3dual6long','E3base6long'}


def sampled_joint(folder,cfg):
    first=None;peak=0
    target=cfg['chemistry']['sequence'];initial=len(target)
    with np.load(folder/'trajectory.npz') as d:
        bits=d['recognition_types'];families=d['families']
        times=d['times'];edges_frames=d['edges'];pairing_frames=d['pairing']
        back_frames=d['copy_pairing'] if 'copy_pairing' in d else None
        for index,t in enumerate(times):
            mat=edges_frames[index];pairs=pairing_frames[index]
            back=back_frames[index] if back_frames is not None else np.full(len(bits),-1)
            counts=[0,0]
            edges={tuple(e) for e in np.argwhere(np.triu(mat,1))}
            for comp,order,cycle in components(len(bits),edges):
                if cycle or not order or any(i<initial for i in comp):continue
                text=''.join(str(int(bits[i])) for i in order)
                if text not in (target,target[::-1]):continue
                if any(pairs[i]>=0 or back[i]>=0 for i in comp):continue
                family=int(families[order[0]])
                if all(families[i]==family for i in comp):counts[family]+=1
            if all(counts):
                if first is None:first=float(t)
                peak=max(peak,min(counts))
        final=components(len(bits),{tuple(e) for e in np.argwhere(np.triu(edges_frames[-1],1))})
        f_partial=sum(len(comp) for comp,order,cycle in final if len(comp)>1 and
                      all(families[i]==1 for i in comp) and
                      (cycle or ''.join(str(int(bits[i])) for i in order) not in (target,target[::-1])))
    return dict(first_joint_sample=first,peak_simultaneous_pairs=peak,final_F_units_in_incomplete_polymers=f_partial)


def main():
    if MANIFEST.exists():refs=json.loads(MANIFEST.read_text(encoding='utf-8'))['recipes']
    else:
        refs=[]
        for p in sorted((ROOT/'research/engine_runs').glob('E3*/scenario.json')):
            if not (p.parent/'result.json').exists():raise RuntimeError('Unfinished run: '+str(p.parent))
            export_recipe(p.parent);refs.append((p.parent/'recipe.json').relative_to(ROOT).as_posix())
        MANIFEST.write_text(json.dumps(dict(batch=5,recipes=refs,policy='Inputs and exact sources only; raw data stays local'),indent=2),encoding='utf-8')
    rows=[];hashes=0
    for ref in refs:
        folder=(ROOT/ref).parent;r=json.loads((folder/'result.json').read_text(encoding='utf-8'))
        cfg=r['scenario'];c=cfg['chemistry'];m=r['metrics']
        recipe=json.loads((folder/'recipe.json').read_text(encoding='utf-8'))
        for name,digest in recipe['source_sha256'].items():
            assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest
            hashes+=1
        row=dict(recipe=ref,name=cfg['name'],sequence=c['sequence'],seed=cfg['seed'],
                 duration=cfg['duration'],period=c['period'],dual_faces=c.get('dual_faces',False),
                 cooperative=c.get('product_cooperativity',False),completed=r['completed'],error=r['error'],
                 mislabelled=cfg['name'] in MISLABELLED,
                 metrics={k:v for k,v in m.items() if k not in ('history','events','food_events','complete_sets',
                 'detached_sets','translated_sets','certified_generations','functional_chain_shapes_final')})
        row.update(sampled_joint(folder,cfg));rows.append(row)
    out=ROOT/'outputs/batch5';out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    keys=['detached_copy_sets_ever','translated_detached_ever','food_max_turnovers_per_expressed_tool']
    titles=['Nouvelles copies G liberees','F exacts liberes','Operations max / F exprime']
    fig,axes=plt.subplots(1,3,figsize=(13,4.3))
    names=['E3base3','E3dual3','E3cooperative3'];labels=['Port unique','Deux faces','Cooperation existante']
    colors=['#8799a4','#df7947','#148e9c']
    for ax,key,title in zip(axes,keys,titles):
        for x,name in enumerate(names):
            selected=sorted([r for r in rows if r['name']==name],key=lambda r:r['seed'])
            assert len(selected)==3
            vals=[r['metrics'][key] for r in selected]
            ax.scatter(x+np.linspace(-.12,.12,3),vals,color=colors[x],s=65)
            ax.plot([x-.2,x+.2],[np.mean(vals)]*2,color='#24364b')
        ax.set_title(title);ax.set_xticks(range(3),labels,rotation=12)
        ax.set_ylim(-.3,5.7);ax.grid(axis='y',alpha=.2)
    fig.suptitle('001 : copie, traduction et operation dans le meme bain, trois graines')
    fig.text(.5,.01,'Cooperation : coexistence detachee 3/3 ; deux faces 3/3 ; port unique sans cooperation 1/3. Generalisation a six symboles non acquise.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.05,1,.92]);fig.savefig(ROOT/'research/BATCH_05_COEXISTENCE.png',dpi=160);plt.close(fig)
    print(json.dumps(dict(runs=len(rows),hashes_verified=hashes,scenario_mislabels=sum(r['mislabelled'] for r in rows),
                         simulation_errors=sum(bool(r['error']) for r in rows),all_completed=all(r['completed'] for r in rows))))


if __name__=='__main__':main()
