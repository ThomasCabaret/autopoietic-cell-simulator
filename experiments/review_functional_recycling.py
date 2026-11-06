"""RF1 exact01 information, potential local motifs and actual catalytic flux apart."""
from statistics import median
from simulator.campaign_io import write
from simulator.checkpoint import load
from experiments.independent_assay_results import completed


def decide(rows):
    groups={v:[r for r in rows if r['variant']==v] for v in ('zero','occupied','paired_edge')}
    if len(rows)!=9 or any(len(q)!=3 or {r['seed'] for r in q}!={0,1,2} for q in groups.values()):raise ValueError('Require RF1 nine cases')
    baseline=median(r['late_catalysis'] for r in groups['zero']);screens={}
    for variant in ('occupied','paired_edge'):
        g=groups[variant]
        conditions=dict(invariants=all(r['atoms']==150 and r['invariant_failures']==0 for r in rows),
            temperature=all(r['late_temperature']<=.12 for r in rows),
            exact_G01_survival=all(r['G01_current']>=1 for r in g),
            functional_motif_final=sum(r['unpaired_F01_edges']>=1 for r in g)>=2,
            actual_late_catalysis=sum(r['late_catalysis']>0 for r in g)>=2,
            useful_reassembly=sum(r['polymer_reassemblies']>0 for r in g)>=2,
            useful_reincorporation=sum(r['recycled_incorporations']>0 for r in g)>=2,
            active_baseline=baseline>0,late_flux_preserved=median(r['late_catalysis'] for r in g)>=.5*baseline)
        screens[variant]=dict(screen_passed=all(conditions.values()),conditions=conditions)
    return dict(protection_screens=screens,run_transfer=False,
        scope='Fixed existing loss helpers in current01 genetic sub-bath. Exact targets, final motifs and late catalysis are separate; no whole-tool lineage, mixed CP1 transfer or homeostasis.')


def collect(folder,require_complete=True):
    folder,manifest,snap,entries=completed(folder,9,require_complete);rows=[]
    for task,state,r,row in entries:
        m=r['metrics'];last=m['final'];late=[q for q in m['history'] if q['time']>=.75*task['scenario']['duration']]
        sim,_=load(folder/state['checkpoint']);c=sim.chemistry
        motifs=[(a,b) for a,b in c.edges if c.families[a]==c.families[b]==1 and c.rungs[a,1]>=0 and c.rungs[b,1]>=0 and c.bits[a]!=c.bits[b]]
        row.update(atoms=last['atoms'],invariant_failures=m['invariant_failures'],G01_current=last['target_chains']['G'],
            F01_current=last['target_chains']['F'],unpaired_F01_edges=sum(c.pairing[a]<0 and c.pairing[b]<0 for a,b in motifs),
            late_exact_F01_fraction=sum(q['target_chains']['F']>0 for q in late)/len(late),
            late_catalysis=late[-1]['catalyzed_formations']-late[0]['catalyzed_formations'],
            polymer_reassemblies=m['polymer_reassemblies'],recycled_incorporations=m['recycled_incorporations'],
            backbone_break=m['backbone_break'],rung_break=m['rung_break'],free_P_final=last['free_P'],free_R_final=last['free_R'])
        row['unpaired_F01_edges']=int(row['unpaired_F01_edges']);rows.append(row)
    report=dict(rows=rows,counts=snap['counts'],controller_active=snap['controller_active'],decision=decide(rows) if len(rows)==9 else None)
    write(folder/'functional_recycling_review.json',report);return report
