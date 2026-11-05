"""CX1 finite comparison to frozen CB1 summaries; no feedback or tuning."""
from statistics import median
from pathlib import Path
from experiments.review_boundary_transfer import collect as previous
from simulator.campaign_io import read,write


def decide(rows):
    if len(rows)!=3 or {r['seed'] for r in rows}!={0,1,2}:raise ValueError('Require three unique CX1 controls')
    conditions=dict(invariants=all(r['invariant_failures']==0 for r in rows),
        late_closure=all(r['valid_fraction_late']>=.8 for r in rows))
    for field in ('G_new','F_new','L_new'):
        conditions[field+'_preserved']=median(r[field] for r in rows)>0 and median(r[field] for r in rows)>=.5*median(r['reference'][field] for r in rows)
    if all(r.get('label','').startswith('CW1_') for r in rows):conditions['insertion_two_seeds']=sum(r['inserted_born_inside']>0 for r in rows)>=2
    wide=all(r.get('label','').startswith('CW1_') for r in rows)
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope=('Selected wider-port variant; rates and noise unchanged; insertion required on two seeds. '
            if wide else 'Ablation of exchange, same compact setting; insertion not required to disappear. ')+
            'Three reused CB1 references, not independent robustness or maintenance. Stop for interpretation.')


def collect(folder,require_complete=True):
    folder=Path(folder);references=read(folder/'plan.json')['reference_cases']
    def with_reference(rows):
        for r in rows:r['reference']=next(q for q in references if q['seed']==r['seed'])
        return decide(rows)
    report=previous(folder,require_complete,decision_fn=with_reference,expected_tasks=3)
    for r in report['rows']:r['reference']=next(q for q in references if q['seed']==r['seed'])
    report['scope']='Three selected CX1/CW1 cases versus completed CB1 active references. Actual condition '
    report['scope']+='is encoded by each frozen scenario; no new noL or nosynthesis controls in this followup. '
    report['scope']+='Stocks, observed contacts and late closure do not establish fed/loss maintenance.'
    write(folder/'exchange_ablation_review.json',report);return report
