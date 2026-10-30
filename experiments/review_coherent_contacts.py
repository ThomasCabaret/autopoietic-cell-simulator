"""Source-verified MD2 closure and comparison with reused Langevin references."""
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.review_langevin_transfer import verify_completed


def main():
    folder=ROOT/'outputs/coherent_contacts_campaigns/campaign_20261030T115427443420Z'
    reference=ROOT/'outputs/demo_motion_campaigns/campaign_20261030T065759494210Z'
    manifest,state,report=verify_completed(folder,15)
    _,_,old=verify_completed(reference,16)
    rows=report['rows']+[r for r in old['rows'] if r['motion']=='langevin' and r['comparison']=='base' and
        (r['preset'].startswith('integrated') or r['preset']=='free_membrane')]
    from collections import Counter
    from simulator import checkpoint
    from simulator.observations import components
    inventory=[]
    for task,s in zip(manifest['tasks'],state['tasks']):
        if task['scenario']['model']!='coupled_bath':continue
        sim,_=checkpoint.load(folder/s['checkpoint']);g=sim.chemistry.genetics
        active=set(int(i) for i in range(g.n) if g.rungs[i,1]>=0)
        prepared={frozenset(q['units']) for q in g.initial_groups if q['family']==1 and q['backbone']}
        lengths=Counter();new=Counter()
        for comp,order,cycle in components(g.n,g.edges):
            if not comp<=active or any(g.families[i]!=1 for i in comp):continue
            lengths[str(len(comp))]+=1
            if len(comp)>1 and frozenset(comp) not in prepared:new[str(len(comp))]+=1
        inventory.append(dict(name=task['label'],seed=task['scenario']['seed'],F_length_histogram=dict(lengths),
            new_F_polymers_by_length=dict(new),scope='Final active composite F graph only, excluding inactive precursor slots; prepared F sets classified passively. No simulation advanced.'))
    out=ROOT/'outputs/reviews'/('MD2_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    result=dict(rows=rows,verified_MD2=15,final_F_inventory=inventory,reused_reference_case_ids=[r['task'] for r in rows[len(report['rows']):]],
        manifest_sha256=hashlib.sha256((folder/'manifest.json').read_bytes()).hexdigest(),
        scope='Three-seed selected prototype comparisons; no viable-cell or quantitative convergence proof. Probe escapes are observed only in classifiable periods; zero observed escape is not a bound across unknown periods.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');(out/'driver.py').write_bytes(Path(__file__).read_bytes())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,axes=plt.subplots(2,2,figsize=(11,7),constrained_layout=True)
    plots=(('regular_parent_closed_fraction','J3 : fraction fermée, grille0,5'),
           ('catalyzed_incorporated','J3 : composants catalysés utilisés'),
           ('detached_copy_sets_ever','J3 : nouveaux G libérés'),
           ('translated_detached_ever','J3 : nouveaux F libérés'))
    for ax,(key,title) in zip(axes.flat,plots):
        for offset,kind,label in ((-.18,'old','Ancien contact / Langevin'),(.18,'new','Contact cohérent / Langevin')):
            chosen=[r for r in rows if r['comparison']=='base' and (r['preset'].startswith('integrated') if kind=='old' else r['preset']=='bath_new')]
            values=[next(r['metrics'][key] for r in chosen if r['seed']==seed) for seed in range(3)]
            ax.bar(np.arange(3)+offset,values,width=.36,label=label)
        ax.set(title=title,xlabel='Graine');ax.set_xticks([0,1,2]);ax.grid(axis='y',alpha=.2)
        if key.startswith('regular'):ax.set_ylim(0,1)
    axes[0,0].legend(fontsize=8);fig.suptitle('MD2 achevé : membrane améliorée, expression F encore bloquante')
    fig.savefig(out/'integrated_comparison.png',dpi=150);plt.close(fig)
    print(json.dumps(dict(output=str(out),verified=15,final_F_inventory=inventory)));return out


if __name__=='__main__':main()
