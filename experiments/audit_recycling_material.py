"""Passive topology replay of RV1 event journals, not a physical re-simulation.

Question: is polymer material actually released, or are repeated monomer
assembly/loss events inflating apparent recycling? Only final local occupancy
is inspected; no integrated protection hazard is inferred from that snapshot.
"""
import json,sys
from pathlib import Path
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.initial import groups
from simulator.observations import components
from simulator.campaign_io import read,write
from scripts.recycling_followup import controller,digest
from scripts.campaign import status,validate


def audit(metadata):
    cfg=metadata['config'];g=cfg['chemistry'].get('genetics',cfg['chemistry'])
    state=metadata['chemistry'].get('genetics',metadata['chemistry']);gs=groups(g)
    length=len(g['sequence']);n=length+g['free_units']+g['function_units']
    fam=[g['seed_family']]*length+[0]*g['free_units']+[1]*g['function_units']
    edges={tuple(e) for e in zip(range(length-1),range(1,length))} if g['template'] else set()
    for group in gs:
        if group['backbone']:edges.update(zip(group['units'][:-1],group['units'][1:]))
    active=set(range(n if g['assembled_stock'] else length))|{q for group in gs for q in group['units']}
    rungs={s:n+s for s in active};poly={q for edge in edges for q in edge}
    counts=Counter();released_supports=set();poly_atoms=poly|{rungs[s] for s in poly}
    released_atoms=set();origins={};used_lives=set();births=Counter();incorporations=Counter()
    for e in state['turnover_events']:
        kind=e['kind']
        if kind=='backbone_break':
            edges.remove((e['a'],e['b']));counts['backbone_break_'+('G' if fam[e['a']]==0 else 'F')]+=1
        elif kind=='rung_break':
            s=e['support'];assert rungs.pop(s)==e['recognizer']
            released_atoms.update({s,e['recognizer']}&poly_atoms)
            origins.pop(s,None);used_lives.discard(s)
            if s in poly:counts['polymer_support_release_events']+=1;released_supports.add(s)
            else:counts['never_polymerized_support_release_events']+=1
        elif kind=='rung_form':
            s=e['support'];assert s not in rungs;rungs[s]=e['recognizer']
            p=s in released_atoms;r=e['recognizer'] in released_atoms
            category='both' if p and r else 'P_only' if p else 'R_only' if r else 'neither'
            births[category]+=1;origins[s]=category;used_lives.discard(s)
            released_atoms.discard(s);released_atoms.discard(e['recognizer'])
        elif kind=='backbone_form':
            edge=(e['a'],e['b']);assert edge not in edges
            for q in edge:
                assert rungs[q]==e['recognizers'][str(q)]
                poly_atoms.update((q,rungs[q]))
                if q in origins and q not in used_lives:
                    incorporations[origins[q]]+=1;used_lives.add(q)
            edges.add(edge);poly.update(edge)
        else:raise ValueError(kind)
    assert edges=={tuple(e) for e in state['edges']}
    assert rungs=={i:int(r) for i,r in enumerate(np.array(state['assembly']['rungs'])[:,1]) if r>=0}
    fragments=Counter();occupied=Counter();capture=state['assembly'].get('capture',{})
    sites=capture.get('site_bound',[-1]*n)
    for comp,order,cycle in components(n,edges):
        if not all(q in rungs for q in comp):continue
        family='G' if fam[order[0]]==0 else 'F';key=family+str(len(comp))
        fragments[key]+=1
        occupied[key]+=sum(int(sites[q]>=0) for q in comp)
    return dict(journal_topology_exact=True,**dict(counts),
        unique_polymer_supports_released=len(released_supports),
        reassemblies_by_released_polymer_atom=dict(births),incorporations_by_released_polymer_atom=dict(incorporations),
        final_components=dict(fragments),final_ligand_occupied_sites_by_component=dict(occupied),
        limitation='Topology replay only. Component labels are passive. Final occupation is not an integrated hazard or causal proof.')


def main():
    job=Path((ROOT/'outputs/recycling_followups/latest.txt').read_text().strip())
    cfg=controller.validate_job(job);rows=[]
    folder=Path(cfg['campaigns'][0]);manifest=validate(folder);snap=status(folder)
    for task,st in zip(manifest['tasks'],snap['tasks']):
        if st['phase']!='complete':continue
        result=folder/st['result'];checkpoint=result.parent/'checkpoint.npz'
        with np.load(checkpoint,allow_pickle=False) as data:meta=json.loads(str(data['metadata']))
        if meta['config']!=task['scenario'] or meta['source_sha256']!={
            k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}:
            raise ValueError('Checkpoint source/config mismatch')
        detail=audit(meta);metrics=read(result)['metrics'];metrics=metrics.get('genetics',metrics)
        assert detail['reassemblies_by_released_polymer_atom'].get('both',0)==metrics['polymer_reassemblies']
        assert detail['incorporations_by_released_polymer_atom'].get('both',0)==metrics['recycled_incorporations']
        rows.append(dict(label=task['label'],checkpoint_sha256=digest(checkpoint),**detail))
    report=dict(question=__doc__,rows=rows,partial=snap['counts']['complete']!=len(manifest['tasks']))
    write(job/'material_audit.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
