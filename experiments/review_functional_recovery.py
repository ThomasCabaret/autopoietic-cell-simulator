"""FR1 separates reconstructed F01, subsequent catalysis and encounter exposure."""
from simulator.checkpoint import load
from simulator.campaign_io import read,write
from experiments.independent_assay_results import completed


def decide(rows):
    groups={v:[r for r in rows if r['variant']==v] for v in ('fast','slow')}
    if len(rows)!=6 or any(len(g)!=3 or {r['seed'] for r in g}!={0,1,2} for g in groups.values()):raise ValueError('Require FR1 six cases')
    screens={}
    for v,g in groups.items():
        conditions=dict(invariants=all(r['atoms']==150 and r['invariant_failures']==0 for r in g),
            temperature=all(r['late_temperature']<=.12 for r in g),
            exact_G01_survival=all(r['G01_current']>=1 for r in g),
            recovered_then_active_two_seeds=sum(r['first_exact_F01']['event'] and r['catalysis_after_exact_F01']>0 for r in g)>=2)
        screens[v]=dict(screen_passed=all(conditions.values()),conditions=conditions)
    return dict(recovery_screens=screens,run_transfer=False,
        scope='Recovery after constructed loss of last F backbone with prepared monomers. Not whole-tool atom renewal, robust persistence, fed homeostasis or mixed CP1 transfer. No automatic winner.')


def collect(folder,require_complete=True):
    folder,manifest,snap,entries=completed(folder,6,require_complete);rows=[]
    for task,state,r,row in entries:
        m=r['metrics'];hist=m['history'];horizon=task['scenario']['duration']
        if hist[0]['target_chains']['F']!=0:raise ValueError('Expected no initial F chain')
        first=next((q['time'] for q in hist if q['target_chains']['F']>0),None)
        sim,obs=load(folder/state['checkpoint']);c=sim.chemistry
        events=c.turnover.events
        cat=sum(e['kind']=='rung_form' and e.get('catalyzed',False) and first is not None and e['time']>=first for e in events)
        genetic=read(folder/state['genetic_audit'])
        row.update(atoms=m['final']['atoms'],invariant_failures=m['invariant_failures'],G01_current=m['final']['target_chains']['G'],
            F01_current=m['final']['target_chains']['F'],first_exact_F01=dict(time=horizon if first is None else first,event=first is not None),
            catalysis_after_exact_F01=cat,free_P_final=m['final']['free_P'],free_R_final=m['final']['free_R'],
            genetic_exposure={key:genetic['exposure'].get(key,0.) for key in ('recognition_eligible_GF','ligation_eligible_F','assembly_catalytic_eligible')},
            scope='First exact target is sampled; later catalysis uses actual journal times. Missing recovery right-censored at horizon.')
        rows.append(row)
    report=dict(rows=rows,counts=snap['counts'],controller_active=snap['controller_active'],decision=decide(rows) if len(rows)==6 else None)
    write(folder/'functional_recovery_review.json',report);return report
