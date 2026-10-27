"""Post-hoc P/R material and polymer census. Never imported by dynamics."""
import numpy as np
from simulator.observations import components


def census(config,state,positions):
    """Analyze saved chemical state without loading or advancing a Simulation."""
    coupled=config['model']=='coupled_bath'
    cfg=config['chemistry']['genetics'] if coupled else config['chemistry']
    g=state['genetics'] if coupled else state
    n=len(cfg['sequence'])+cfg['free_units']+cfg['function_units']
    offset=(2*config['chemistry']['membrane']['units'] if config['chemistry']['include_membrane'] else 0) if coupled else 0
    positions=np.asarray(positions)[offset:]
    assert len(positions)==2*n
    assembly=g['assembly'];rungs=np.asarray(assembly['rungs'],dtype=int)
    bits=np.asarray(assembly['bits'],dtype=int)
    # R elementary symbols are supplied by the recipe, including prepared groups.
    initial_bits=[int(x) for x in cfg['sequence']]+[int(cfg['alphabet'][i%len(cfg['alphabet'])]) for i in range(cfg['free_units'])]+[int(cfg['alphabet'][i%len(cfg['alphabet'])]) for i in range(cfg['function_units'])]
    starts={0:len(cfg['sequence']),1:len(cfg['sequence'])+cfg['free_units']}
    for group in cfg['initial_assemblies']:
        s=starts[group['family']];initial_bits[s:s+len(group['sequence'])]=[int(x) for x in group['sequence']]
        starts[group['family']]+=len(group['sequence'])
    atom_bits=np.asarray(initial_bits,dtype=int)
    families=np.array([cfg['seed_family']]*len(cfg['sequence'])+[0]*cfg['free_units']+[1]*cfg['function_units'])
    active=rungs[:,1]>=0;attached=rungs[active,1]
    assert np.array_equal(rungs[:,0],np.arange(n))
    assert len(set(attached.tolist()))==len(attached) and np.all((attached>=n)&(attached<2*n))
    assert np.array_equal(bits[active],atom_bits[attached-n])
    free_R=sorted(set(range(n,2*n))-set(attached.tolist()))
    pools=dict(free_P_G=int(np.count_nonzero(~active&(families==0))),free_P_F=int(np.count_nonzero(~active&(families==1))),
               free_R0=sum(atom_bits[r-n]==0 for r in free_R),free_R1=sum(atom_bits[r-n]==1 for r in free_R),
               free_R2=sum(atom_bits[r-n]==2 for r in free_R),active_dimers=int(active.sum()))
    pools={k:int(v) for k,v in pools.items()}
    pools['beads_accounted']=sum(v for k,v in pools.items() if k.startswith('free_'))+2*pools['active_dimers']
    assert pools['beads_accounted']==2*n
    edges={tuple(p) for p in g['edges']};pairing=np.asarray(g['pairing'])
    assert all(active[i] and active[j] and families[i]==families[j] for i,j in edges)
    degree=np.zeros(n,dtype=int)
    for i,j in edges:degree[i]+=1;degree[j]+=1
    monomers=active&(degree==0)
    buckets=dict(monomer_G=0,monomer_F=0,target_G_units=0,target_F_units=0,other_G_units=0,other_F_units=0)
    target_counts=dict(G=0,F=0);fragments=[]
    for comp,order,cycle in components(n,edges):
        if not all(active[q] for q in comp):
            assert len(comp)==1;continue
        family='F' if families[order[0]] else 'G'
        if len(comp)==1:buckets['monomer_'+family]+=1;continue
        text=''.join(str(int(bits[q])) for q in order)
        match=not cycle and text in (cfg['sequence'],cfg['sequence'][::-1])
        buckets[('target_' if match else 'other_')+family+'_units']+=len(comp)
        if match:target_counts[family]+=1
        elif family=='F':fragments.append(dict(units=sorted(comp),sequence=text,unpaired=all(pairing[q]<0 for q in comp),cycle=bool(cycle)))
    assert sum(buckets.values())==pools['active_dimers']
    gene_R=rungs[:len(cfg['sequence']),1]
    assert np.all(gene_R>=n)
    def distances(mask):
        ids=rungs[np.flatnonzero(mask),1]
        if not len(ids):return dict(count=0,median_distance=None,within2=0,within5=0)
        d=np.linalg.norm(positions[ids,None]-positions[gene_R][None,:],axis=2).min(axis=1)
        return dict(count=len(ids),median_distance=float(np.median(d)),within2=int(np.count_nonzero(d<2.)),within5=int(np.count_nonzero(d<5.)))
    prepared=[];start=len(cfg['sequence'])+cfg['free_units']
    for group in cfg['initial_assemblies']:
        if group['family']!=1:continue
        ids=list(range(start,start+len(group['sequence'])));start+=len(ids)
        if group['backbone']:prepared+=ids
    tool_gap=None
    if prepared:
        tool_gap=float(np.linalg.norm(positions[rungs[prepared,1]].mean(axis=0)-positions[gene_R].mean(axis=0)))
    return dict(pools=pools,partition_active_units=buckets,target_like_components=target_counts,
        unpaired_non_target_F_units=sum(len(f['units']) for f in fragments if f['unpaired']),F_non_target_components=fragments,
        free_monomer_access={f:distances(monomers&(families==i)) for f,i in [('G',0),('F',1)]},
        prepared_tool_gene_distance=tool_gap,
        scope='Final global census only. Target-like is structural, not proven activity. Distances to initial gene are analytic labels, never forces. Unpaired F fragments cannot recapture by current family-degree rule, but may still catalyze.')
