"""Freeze input recipes and make selected paper figures; bulk data stays local."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.reconstruct_experiment import export_recipe

MANIFEST=ROOT/'research/BATCH_04_RECIPES.json'


def load_rows():
    if MANIFEST.exists(): refs=json.loads(MANIFEST.read_text(encoding='utf-8'))['recipes']
    else:
        refs=[]
        for p in sorted((ROOT/'research/engine_runs').glob('C2*/result.json')):
            r=json.loads(p.read_text(encoding='utf-8'))
            if r['scenario'].get('branch')!='C2':continue
            export_recipe(p.parent);refs.append((p.parent/'recipe.json').relative_to(ROOT).as_posix())
        MANIFEST.write_text(json.dumps(dict(batch=4,recipes=refs,policy='Inputs and sources only; raw data stays local'),indent=2),encoding='utf-8')
    rows=[];verified=0
    for ref in refs:
        folder=(ROOT/ref).parent;r=json.loads((folder/'result.json').read_text(encoding='utf-8'))
        recipe=json.loads((folder/'recipe.json').read_text(encoding='utf-8'))
        for name,digest in recipe['source_sha256'].items():
            assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest
            verified+=1
        rows.append(dict(recipe=ref,name=r['scenario']['name'],seed=r['scenario']['seed'],
                         duration=r['scenario']['duration'],error=r['error'],completed=r['completed'],
                         metrics={k:v for k,v in r['metrics'].items() if k not in ('history','events','food_events',
                         'functional_chain_shapes_final','complete_sets','detached_sets','translated_sets','certified_generations')},
                         food_events=r['metrics'].get('food_events',[])))
    out=ROOT/'outputs/batch4';out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    print(json.dumps(dict(runs=len(rows),errors=sum(bool(r['error']) for r in rows),verified_hashes=verified)))
    return rows


def main():
    rows=load_rows()
    fig,axes=plt.subplots(1,2,figsize=(12,4.4))
    labels=['F 001 prepare','F 010 prepare','F separes','Sans capture']
    for ax,key,title in zip(axes,['food_products','food_chain_supported_ligations'],
                            ['Produits XY totaux a t=200','Ligations soutenues par la chaine']):
        for x,name in enumerate(['C2preparedC','C2shuffledC','C2looseC','C2bareC']):
            selected=sorted((r for r in rows if r['name']==name),key=lambda r:r['seed'])
            vals=[r['metrics'][key] for r in selected]
            ax.scatter(x+np.linspace(-.1,.1,len(vals)),vals,s=55,color=['#148e9c','#df7947','#536e82'][0])
            ax.plot([x-.2,x+.2],[np.mean(vals)]*2,color='#24364b')
        ax.set_xticks(range(4),labels,rotation=12);ax.set_title(title);ax.set_ylim(-.5,8.7)
        ax.grid(axis='y',alpha=.2)
    fig.suptitle('C2C : operation repetee des vrais F composites, sans angle supplementaire')
    fig.text(.5,.01,'3 graines ; meme bain et memes affinites elementaires hors ablation. Aucune preuve de repliement specifique.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.05,1,.92]);fig.savefig(ROOT/'research/BATCH_04_CONTROLS.png',dpi=160);plt.close(fig)

    fig,axes=plt.subplots(1,3,figsize=(14,4.5),sharey=True)
    for seed,ax in enumerate(axes):
        for candidate,color in [('C','#b58a62'),('D','#148e9c')]:
            row=next(r for r in rows if r['name']=='C2express'+candidate and r['seed']==seed)
            events=[e for e in row['food_events'] if e['expressed_certified']]
            times=[e['time'] for e in events]
            ax.step([0]+times+[800],[0]+list(range(1,len(times)+1))+[len(times)],where='post',
                    color=color,label='Activation locale' if candidate=='D' else 'Sans activation')
        ax.set_title(f'Graine {seed}');ax.set_xlabel('Temps simule');ax.set_xlim(0,800);ax.set_ylim(-.1,4.5)
        ax.grid(alpha=.2)
    axes[0].set_ylabel('Ligations sur une chaine F exacte issue de G');axes[0].legend(fontsize=9)
    fig.suptitle('G vers F puis operation repetee dans le meme bain, sous lois fixes')
    fig.text(.5,.01,'D : 3 / 3 / 4 ligations sur la meme chaine par essai. Precurseurs actives et liberation locale du produit fournis.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.05,1,.92]);fig.savefig(ROOT/'research/BATCH_04_COUPLING.png',dpi=160);plt.close(fig)

    # Show a translated tool and the actual support identities at its first two turnovers.
    row=next(r for r in rows if r['name']=='C2expressD' and r['seed']==0)
    folder=(ROOT/row['recipe']).parent;result=json.loads((folder/'result.json').read_text(encoding='utf-8'))
    events=[e for e in row['food_events'] if e['expressed_certified']][:2]
    seq=result['scenario']['chemistry']['sequence'];n=len(seq)+result['scenario']['chemistry']['function_units']
    fig,axes=plt.subplots(1,2,figsize=(9,4.5))
    with np.load(folder/'trajectory.npz') as data:
        for ax,event in zip(axes,events):
            index=int(np.argmin(abs(data['times']-event['time'])))
            p=data['positions'][index];chain=event['chain']
            for a,b in np.argwhere(np.triu(data['edges'][index],1)):
                if a in chain and b in chain:ax.plot(*p[[a,b]].T,color='#536e82',lw=2)
            for i in chain:
                ax.plot(*p[[i,n+i]].T,color='#bac6cf');ax.scatter(*p[i],color='#9a4aa0',s=65)
                bit=int(seq[i]) if i<len(seq) else (i-len(seq))%2
                ax.scatter(*p[n+i],color='#148e9c' if bit==0 else '#df7947',s=55)
                ax.annotate(str(i),p[i]+[.03,.05],fontsize=9)
            ids=[2*n+f for f in event['formed']]
            ax.plot(*p[ids].T,color='#24364b',lw=2)
            for idx,f in zip(ids,event['formed']):ax.scatter(*p[idx],color='#148e9c' if f%2==0 else '#df7947',marker='s',s=55)
            view=p[chain+[n+i for i in chain]+ids];lo=view.min(axis=0)-.5;hi=view.max(axis=0)+.5
            ax.set_xlim(lo[0],hi[0]);ax.set_ylim(lo[1],hi[1]);ax.set_aspect('equal')
            ax.set_title(f"t={event['time']:.3f} ; supports {event['support']}");ax.grid(alpha=.15)
    fig.suptitle('La meme chaine exprimee [5, 10, 25] soutient des produits distincts')
    fig.text(.5,.01,'Instantanes echantillonnes proches des evenements ; les supports proviennent du journal reactionnel exact.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.05,1,.92]);fig.savefig(ROOT/'research/BATCH_04_TOOL.png',dpi=160);plt.close(fig)


if __name__=='__main__':main()
