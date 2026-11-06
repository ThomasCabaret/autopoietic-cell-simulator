"""PT1 transport alarms, constructed contour only; unknown is never retention."""
from simulator.campaign_io import write
from simulator.checkpoint import load
from simulator.runner import make_observer
from experiments.independent_assay_results import completed
from experiments.mixed_calibration import weighted


def decide(rows):
    groups={v:[r for r in rows if r['variant']==v] for v in ('barrier','transparent')}
    if len(rows)!=6 or any(len(q)!=3 or {r['seed'] for r in q}!={0,1,2} for q in groups.values()):raise ValueError('Require PT1 six cases')
    def known(r,k):return r[k] is not None
    conditions=dict(invariants=all(r['invariant_failures']==0 and r['atoms']==200 and r['cohorts_stable'] for r in rows),
        temperature=all(r['late_temperature']<=.12 for r in rows),closure=all(r['valid_fraction_late']>=.8 for r in rows),
        final_classifiable=all(known(r,'bound_outside') and known(r,'free_outside') for r in rows),
        free_transport=all(known(r,'free_outside') and r['free_outside']>=.2 for r in rows),
        transparent_control=sum(known(r,'bound_outside') and r['bound_outside']>=.2 for r in groups['transparent'])>=2,
        selective_retention=all(known(r,'bound_outside') and r['bound_outside']<=.1 for r in groups['barrier']))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Constructed, chemistry-disabled sub-bath. Final atom fractions and sampled crossings, not continuous sealing, self-assembly, open feed or viability.')


def collect(folder,require_complete=True):
    folder,manifest,snap,entries=completed(folder,6,require_complete);rows=[]
    for task,state,r,row in entries:
        sim,obs=load(folder/state['checkpoint'],make_observer);c=sim.chemistry;g=c.host;s=obs.boundary_state
        cohort=set(g.assembly.initial_supports);bound=cohort|{g.n+i for i in cohort};free=set(range(c.prefix))-bound
        stable=(not g.edges and not g.assembly.events and not c.births and
            all(int(g.rungs[i,1])==(g.n+i if i in cohort else -1) for i in range(g.n)))
        inside=s['last_inside'];valid=s['history'][-1]['valid']
        outside=lambda ids:sum(not inside[i] for i in ids)/len(ids) if valid and len(inside)==c.prefix else None
        row.update(atoms=len(c.pos),cohorts_stable=bool(stable),invariant_failures=r['metrics']['atom_port_invariant_failures'],
            bound_outside=outside(bound),free_outside=outside(free),final_contour_valid=valid,
            valid_fraction_late=weighted(s['history'],'valid',.5*task['scenario']['duration'],task['scenario']['duration']),sampled_crossings=s['crossings'])
        rows.append(row)
    report=dict(rows=rows,counts=snap['counts'],controller_active=snap['controller_active'],decision=decide(rows) if len(rows)==6 else None)
    write(folder/'selective_transport_review.json',report);return report
