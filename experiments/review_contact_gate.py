"""CF1 simultaneous closure/insertion/thermal/throughput screen per dt."""
from pathlib import Path
from statistics import median
from experiments.review_boundary_transfer import collect as previous
from scripts.campaign import status
from simulator.campaign_io import read,write


def decide(rows):
    if len(rows)!=6:raise ValueError('Require six CF1 trials')
    conditions={}
    for scale in ('coarse','fine'):
        group=[r for r in rows if r['scale']==scale]
        if len(group)!=3 or {r['seed'] for r in group}!={0,1,2}:raise ValueError('Require three seeds per physical step')
        tests=dict(invariants=all(r['invariant_failures']==0 for r in group),
            closure=all(r['valid_fraction_late']>=.8 for r in group),temperature=all(r['late_temperature']<=.12 for r in group),
            insertion=sum(r['inserted_born_inside']>0 for r in group)>=2,
            accounting=all(s['proposals']==s['accepted']+s['rejected'] for r in group for s in r['contact_update_stats'].values()))
        for key in ('G_new','F_new','L_new'):tests[key]=median(r[key] for r in group)>0 and median(r[key] for r in group)>=.5*median(r['reference'][key] for r in group)
        conditions.update({scale+'_'+k:v for k,v in tests.items()})
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Fixed six-case intervention at both dt, reused historical references. No general numerical convergence, de novo vesicle assembly, fed renewal or homeostasis proof. Report then stop.')


def collect(folder,require_complete=True):
    folder=Path(folder);refs=read(folder/'plan.json')['reference_cases']
    def decorate(rows):
        states=status(folder)['tasks']
        for row in rows:
            row['scale']=row['label'].split('_')[1]
            row['reference']=next(q for q in refs if q['scale']==row['scale'] and q['seed']==row['seed'])
            s=next(s for s in states if s['label']==row['label']);m=read(folder/s['result'])['metrics']
            row['contact_update_stats']=m['contact_update_stats'];row['exchange_gate_stats']=m['exchange_gate_stats']
    def annotate(rows):
        decorate(rows);return decide(rows)
    report=previous(folder,require_complete,decision_fn=annotate,expected_tasks=6)
    if len(report['rows'])<6:decorate(report['rows'])
    report['scope']='CF1 fixed chemistry, coarse/fine mechanics. Same finite stocks/constructed frontier, no turnover or feed.'
    write(folder/'contact_gate_review.json',report);return report
