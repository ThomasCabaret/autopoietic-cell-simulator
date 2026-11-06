"""CR1 sampled persistence screen, never a continuous first-passage claim."""
import math
from pathlib import Path
from simulator.campaign_io import read,write
from experiments.review_competitive_panel import collect as base
from experiments.mixed_calibration import weighted


def decide(rows):
    if len(rows)!=3 or {r['seed'] for r in rows}!={0,1,2}:raise ValueError('Require three CR1 seeds')
    minimum=.25*math.pi*8.325**2
    persistent=sum(r['macro_fraction_late']>=.5 and any(q['units']>=26 and q['area']>=minimum for q in r['simple_contours']) for r in rows)
    conditions=dict(final_ports=all(r['final_ports_valid'] for r in rows),
        complete_observation=all(r['geometry_dropped']==0 for r in rows),
        temperature=all(r['late_temperature']<=.12 for r in rows),persistent_final_macro_two_seeds=persistent>=2)
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Three same-seed selected horizons8000, sampled macro occupancy6000–8000. Not independent validation, continuous retention, reaction hazard or maintenance. Report then stop.')


def collect(folder,require_complete=True):
    folder=Path(folder);report=base(folder,require_complete,expected_tasks=3,decision_fn=lambda rows:None)
    from scripts.campaign import status
    states=status(folder)['tasks']
    manifest=read(folder/'manifest.json')
    for row in report['rows']:
        task=next(q for q in manifest['tasks'] if q['label']==row['label']);state=next(q for q in states if q['id']==task['id'])
        audit=read(folder/state['lipid_geometry']);history=audit['history']
        row.update(macro_fraction_late=weighted(history,'macro',6000.,8000.),geometry_dropped=audit['dropped'],
            first_sampled_macro=audit['first_sampled_macro'],sampled_self_capture_peak=max(q['self_capture_faces'] for q in history),
            sampled_macro_frames=sum(q['macro'] for q in history),geometry_scope=audit['scope'])
    report['decision']=decide(report['rows']) if len(report['rows'])==3 else None
    write(folder/'competitive_relaxation_review.json',report);return report
