"""EG1 coupled transfer, closure and thermal checks under frozen local laws."""
from pathlib import Path
from statistics import median
from experiments.review_boundary_transfer import collect as previous
from simulator.campaign_io import read,write


def decide(rows):
    if len(rows)!=3 or {r['seed'] for r in rows}!={0,1,2}:raise ValueError('Require all3 EG1 seeds')
    conditions=dict(invariants=all(r['invariant_failures']==0 for r in rows),
        late_closure=all(r['valid_fraction_late']>=.8 for r in rows),
        late_temperature=all(r['late_temperature']<=.12 for r in rows),
        insertion_two_seeds=sum(r['inserted_born_inside']>0 for r in rows)>=2,
        energy_gate_observed=all(r['exchange_gate_stats']['proposals']==r['exchange_gate_stats']['accepted']+r['exchange_gate_stats']['rejected'] for r in rows))
    for key in ('G_new','F_new','L_new'):
        conditions[key+'_preserved']=median(r[key] for r in rows)>0 and median(r[key] for r in rows)>=.5*median(r['reference'][key] for r in rows)
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Selected energy-gate transfer check, not global detailed balance, fed/loss maintenance '
            'or independent robustness. Three CW1 active references reused. Report then stop.')


def collect(folder,require_complete=True):
    folder=Path(folder);refs=read(folder/'plan.json')['reference_cases']
    def annotate(rows):
        from scripts.campaign import status
        s=status(folder)
        for r in rows:
            st=next(t for t in s['tasks'] if t['label']==r['label']);m=read(folder/st['result'])['metrics']
            r['reference']=next(q for q in refs if q['seed']==r['seed']);r['exchange_gate_stats']=m['exchange_gate_stats']
        return decide(rows)
    report=previous(folder,require_complete,decision_fn=annotate,expected_tasks=3)
    if len(report['rows'])<3:
        from scripts.campaign import status
        for r in report['rows']:
            st=next(t for t in status(folder)['tasks'] if t['label']==r['label'])
            r['reference']=next(q for q in refs if q['seed']==r['seed']);r['exchange_gate_stats']=read(folder/st['result'])['metrics']['exchange_gate_stats']
    report['scope']='Three EG1 cases at fixed CW1 rates/noise/width. Local exchange-energy gate; no feed/loss/homeostasis or new noL/nosynthesis controls.'
    write(folder/'energy_exchange_review.json',report);return report
