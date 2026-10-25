"""Independent material/trajectory audit; only curated synthesis enters Git."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.reconstruct_experiment import export_recipe
from simulator.observations import components
MANIFEST=ROOT/'research/BATCH_06_RECIPES.json'


def audit(folder,result):
    m=result['metrics'];c=result['scenario']['chemistry'];state=m.get('assembly_state')
    if state is None:return {}
    made={e['support']:e for e in state['events']};atom_bits=np.array(state['atom_bits'])
    incorporation={}
    for event in m['events']:
        for s in event['formed']:
            if s in made:
                assert made[s]['time']<=event['time']
                incorporation.setdefault(s,event['time'])
    assert len(incorporation)==m['incorporated_constructed']
    joint_first=None;independent_g=set();independent_f=set()
    with np.load(folder/'trajectory.npz') as data:
        times=data['times'];rungs=data['rungs'];bits=data['unit_bits'];edges=data['edges']
        pairs=data['pairing'];families=data['families'];n=len(atom_bits);length=len(c['sequence'])
        assert data['positions'].shape[1:]==(2*n,2)
        assert len(rungs)==len(times)==len(bits)
        assert np.all(rungs[:,:,0]==np.arange(n))
        assert np.count_nonzero(rungs[0,:,1]>=0)==(n if c['assembled_stock'] else length)
        for k,t in enumerate(times):
            active=rungs[k,:,1]>=0;recognizers=rungs[k,active,1]
            assert len(set(recognizers))==len(recognizers)
            assert np.all((recognizers>=n)&(recognizers<2*n))
            np.testing.assert_array_equal(bits[k,active],atom_bits[recognizers-n])
            assert np.all(bits[k,~active]==-1)
            if k:
                old=rungs[k-1,:,1]>=0
                np.testing.assert_array_equal(rungs[k,old],rungs[k-1,old])
            detached=[False,False]
            for comp,order,cycle in components(n,{tuple(e) for e in np.argwhere(np.triu(edges[k],1))}):
                if cycle or not order or any(i<length for i in comp):continue
                if not all(i in made for i in comp):continue
                text=''.join(str(int(bits[k,i])) for i in order)
                if text not in (c['sequence'],c['sequence'][::-1]) or any(pairs[k,i]>=0 for i in comp):continue
                f=int(families[order[0]])
                assert all(families[i]==f for i in comp)
                (independent_g if f==0 else independent_f).add(tuple(sorted(comp)))
                detached[f]=True
            if all(detached) and joint_first is None:joint_first=float(t)
    # Irreversible backbone and periodic release make every certified detached
    # product persist until the next sampled frame in these runs.
    assert len(independent_g)==m['constructed_detached_G']
    assert len(independent_f)==m['constructed_detached_F']
    return dict(material_frames_checked=len(times),incorporation_witnesses=len(incorporation),
        cross_index_partners=sum(e['recognizer']!=n+e['support'] for e in made.values()),
        first_constructed_joint_sample=joint_first,
        final_composition={str(f):{str(b):int(np.count_nonzero((families[length:]==f)&(bits[-1,length:]==b)))
            for b in (0,1)} for f in (0,1)})


def main():
    if MANIFEST.exists():refs=json.loads(MANIFEST.read_text(encoding='utf-8'))['recipes']
    else:
        refs=[]
        for path in sorted((ROOT/'research/engine_runs').glob('C3*/scenario.json')):
            result=json.loads((path.parent/'result.json').read_text(encoding='utf-8'))
            assert result['completed'] and not result['error']
            export_recipe(path.parent);refs.append((path.parent/'recipe.json').relative_to(ROOT).as_posix())
        MANIFEST.write_text(json.dumps(dict(batch=6,recipes=refs,policy='Sources and inputs only'),indent=2),encoding='utf-8')
    rows=[];hashes=0
    for ref in refs:
        folder=(ROOT/ref).parent;r=json.loads((folder/'result.json').read_text(encoding='utf-8'))
        recipe=json.loads((folder/'recipe.json').read_text(encoding='utf-8'))
        for name,digest in recipe['source_sha256'].items():
            assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest;hashes+=1
        row=dict(recipe=ref,name=r['scenario']['name'],seed=r['scenario']['seed'],duration=r['scenario']['duration'],
                 sequence=r['scenario']['chemistry']['sequence'],error=r['error'],completed=r['completed'],
                 metrics={k:v for k,v in r['metrics'].items() if isinstance(v,(int,float,str))})
        row.update(audit(folder,r));rows.append(row)
    out=ROOT/'outputs/batch6';out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    names=['C3copy','C3expression','C3mixed'];labels=['G seuls','F seuls','Bain G + F']
    fig,axes=plt.subplots(1,3,figsize=(12,4.1))
    for ax,key,title in zip(axes,['assembled_dimers','constructed_detached_G','constructed_detached_F'],
                           ['Dimeres construits','Copies G construites et liberees','F construits et liberes']):
        for x,name in enumerate(names):
            vals=[r['metrics'][key] for r in sorted(rows,key=lambda r:r['seed']) if r['name']==name and r['duration']==800.]
            assert len(vals)==3
            ax.scatter(x+np.linspace(-.1,.1,3),vals,color='#148e9c',s=60)
        ax.set_xticks(range(3),labels);ax.set_title(title,fontsize=11);ax.set_ylim(bottom=-.3);ax.grid(axis='y',alpha=.2)
    fig.suptitle('001 : composants construits depuis P et R libres, puis incorpores')
    fig.text(.5,.015,'Trois graines par bain. Formation P-R spontanee et irreversible ; pas encore de fabrication pilotee par les outils.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.07,1,.92]);fig.savefig(ROOT/'research/BATCH_06_CONSTRUCTION.png',dpi=160);plt.close(fig)
    print(json.dumps(dict(runs=len(rows),source_hashes_verified=hashes,
        material_frames=sum(r.get('material_frames_checked',0) for r in rows),
        all_completed=all(r['completed'] and not r['error'] for r in rows))))


if __name__=='__main__':main()
