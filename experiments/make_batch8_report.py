"""Independent material/graph checks and curated C3B1 synthesis."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.reconstruct_experiment import export_recipe
from simulator.observations import components
MANIFEST=ROOT/'research/BATCH_08_RECIPES.json'


def audit(folder,r):
    c=r['scenario']['chemistry'];m=r['metrics'];state=m.get('assembly_state')
    if state is None:return {}
    events=state['events'];made={e['support']:e for e in events};assert len(made)==len(events)
    initial=len(c['sequence']);prepared=set(range(initial));excluded=set(range(initial))
    cursor=[initial,initial+c['free_units']];edge_birth={tuple((i,i+1)):0. for i in range(initial-1) if c['template']}
    for g in c.get('initial_assemblies',[]):
        f=g['family'];units=tuple(range(cursor[f],cursor[f]+len(g['sequence'])));cursor[f]+=len(units)
        prepared.update(units)
        if g.get('backbone',True) and len(units)>1:
            excluded.update(units);edge_birth.update({p:0. for p in zip(units[:-1],units[1:])})
    if c['assembled_stock']:prepared=set(range(len(state['rungs'])))
    for event in m['events']:edge_birth[tuple(sorted(event['formed']))]=event['time']
    cat={e['support'] for e in events if e.get('catalyzed',False)}
    expressed={e['support'] for e in state.get('catalytic_events',[]) if e['chain_kind']=='expressed'}
    incorporation={}
    for event in m['events']:
        for s in event['formed']:
            if s in made:
                assert made[s]['time']<=event['time'];incorporation.setdefault(s,event['time'])
    assert len(incorporation)==m['incorporated_constructed']
    detached=[set(),set()];first_F=None;first_G=None
    with np.load(folder/'trajectory.npz') as data:
        times=data['times'];rungs=data['rungs'];bits=data['unit_bits'];families=data['families']
        matrices=data['edges'];pairs=data['pairing'];atom=data['atom_bits'];n=len(atom)
        assert data['positions'].shape[1:]==(2*n,2)
        assert set(np.flatnonzero(rungs[0,:,1]>=0))==prepared
        assert not set(made)&prepared
        assert len({e['recognizer'] for e in events})==len(events)
        for e in events:
            assert e['symbol']==int(atom[e['recognizer']-n])
            if e.get('catalyzed',False):
                a,b=e['catalytic_support'];assert families[a]==families[b]==1
                assert bits[-1,a]==0 and bits[-1,b]==1
                assert edge_birth[tuple(sorted((a,b)))]<e['time']
        for k,t in enumerate(times):
            active=rungs[k,:,1]>=0;rr=rungs[k,active,1]
            assert len(set(rr))==len(rr) and np.all((rr>=n)&(rr<2*n))
            np.testing.assert_array_equal(bits[k,active],atom[rr-n]);assert np.all(bits[k,~active]==-1)
            if k:
                old=rungs[k-1,:,1]>=0;np.testing.assert_array_equal(rungs[k,old],rungs[k-1,old])
            for comp,order,cycle in components(n,{tuple(e) for e in np.argwhere(np.triu(matrices[k],1))}):
                if not order or cycle or comp&excluded or any(pairs[k,i]>=0 for i in comp):continue
                if ''.join(str(int(bits[k,i])) for i in order) not in (c['sequence'],c['sequence'][::-1]):continue
                f=int(families[order[0]]);assert all(families[i]==f for i in comp)
                detached[f].add(tuple(sorted(comp)))
                if f==1 and first_F is None:first_F=float(t)
                if f==0 and first_G is None:first_G=float(t)
        bound=data['precursor_binding'] if 'precursor_binding' in data else None
        mean_bound=float(np.mean(np.count_nonzero(bound>=0,axis=1))) if bound is not None else None
        final_bound=int(np.count_nonzero(bound[-1]>=0)) if bound is not None else None
    assert len(detached[0])==m['detached_copy_sets_ever']
    assert len(detached[1])==m['translated_detached_ever']
    if 'catalyzed_dimers' in m:
        assert len(cat)==m['catalyzed_dimers']
        assert len(set(incorporation)&expressed)==m['expressed_catalyzed_incorporated']
    return dict(material_frames=len(times),first_F_sample=first_F,first_G_sample=first_G,
        first_expressed_reaction=min((e['time'] for e in state.get('catalytic_events',[]) if e['chain_kind']=='expressed'),default=None),
        first_expressed_incorporation=min((t for s,t in incorporation.items() if s in expressed),default=None),
        G_all_expressed_components=sum(set(k)<=expressed for k in detached[0]),
        F_all_expressed_components=sum(set(k)<=expressed for k in detached[1]),
        mean_captured_atoms_sampled=mean_bound,final_captured_atoms=final_bound,
        incorporated_by_family={str(f):sum(s in incorporation and int(families[s])==f for s in expressed) for f in (0,1)})


def main():
    if MANIFEST.exists():refs=json.loads(MANIFEST.read_text(encoding='utf-8'))['recipes']
    else:
        refs=[]
        for p in sorted((ROOT/'research/engine_runs').glob('C3B*/scenario.json')):
            r=json.loads((p.parent/'result.json').read_text(encoding='utf-8'));assert r['completed'] and not r['error']
            export_recipe(p.parent);refs.append((p.parent/'recipe.json').relative_to(ROOT).as_posix())
        MANIFEST.write_text(json.dumps(dict(batch=8,recipes=refs,policy='Inputs and exact sources only'),indent=2),encoding='utf-8')
    rows=[];hashes=0
    for ref in refs:
        folder=(ROOT/ref).parent;r=json.loads((folder/'result.json').read_text(encoding='utf-8'))
        recipe=json.loads((folder/'recipe.json').read_text(encoding='utf-8'))
        for name,digest in recipe['source_sha256'].items():
            assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest;hashes+=1
        row=dict(recipe=ref,name=r['scenario']['name'],seed=r['scenario']['seed'],duration=r['scenario']['duration'],
            completed=r['completed'],error=r['error'],metrics={k:v for k,v in r['metrics'].items() if isinstance(v,(str,int,float))})
        row.update(audit(folder,r));rows.append(row)
    out=ROOT/'outputs/batch8';out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    fig,axes=plt.subplots(1,3,figsize=(13,4.3));names=['C3Bprepared','C3Bunlinked','C3Bnone']
    labels=['Outil prepare','Outil initial delie','Sans outil initial']
    for ax,key,title in zip(axes,['assembled_dimers','catalyzed_incorporated','detached_copy_sets_ever'],
        ['Dimeres construits','Produits catalyses incorpores','Copies G exactes liberees']):
        for x,name in enumerate(names):
            selected=sorted([r for r in rows if r['name']==name and r['duration']==800.],key=lambda r:r['seed']);assert len(selected)==3
            ax.scatter(x+np.linspace(-.12,.12,3),[r['metrics'][key] for r in selected],s=60,color='#148e9c')
        ax.set_xticks(range(3),labels,rotation=12);ax.set_title(title,fontsize=11);ax.grid(axis='y',alpha=.2);ax.set_ylim(bottom=-.4)
    fig.suptitle('C3B1 : catalyse sur les vraies billes, puis incorporation, trois graines')
    fig.text(.5,.01,"L'outil initialement delie se reconstitue par expression sur une graine ; ce controle n'est pas un interdit permanent.",ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.07,1,.93]);fig.savefig(ROOT/'research/BATCH_08_TRANSFER.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.6));series=[('translated_detached_ever','F exprimes'),('expressed_catalyzed_dimers','Dimeres par F exprimes'),('expressed_catalyzed_incorporated','Produits incorpores'),('detached_G_with_expressed_catalyzed_component','Copies G avec produit')]
    selected=sorted([r for r in rows if r['name']=='C3Bexpress'],key=lambda r:r['seed']);assert len(selected)==3
    x=np.arange(4)
    for shift,r,color in zip([-.2,0,.2],selected,['#148e9c','#df7947','#8d75bb']):
        ax.bar(x+shift,[r['metrics'][key] for key,label in series],width=.19,label='Graine '+str(r['seed']),color=color)
    ax.set_xticks(x,[label for key,label in series]);ax.set_ylabel('Comptes de nature differente');ax.legend();ax.grid(axis='y',alpha=.2)
    ax.set_title('Aucune chaine F initiale : expression → fabrication → utilisation')
    fig.text(.5,.015,'6 monomeres F prepares amorcent le systeme. Lois fixes, 001, t=1200 ; pas de maintien sous pertes ni de membrane.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(ROOT/'research/BATCH_08_EXPRESSION.png',dpi=160);plt.close(fig)
    print(json.dumps(dict(runs=len(rows),source_hashes_verified=hashes,material_frames=sum(r.get('material_frames',0) for r in rows),all_completed=all(r['completed'] and not r['error'] for r in rows))))


if __name__=='__main__':main()
