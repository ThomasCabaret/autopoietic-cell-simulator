"""CH1 final-geometry/selected-recovery screen, keep no-event runs censored."""
import math
from pathlib import Path
from simulator.campaign_io import write
from experiments.review_competitive_panel import collect as previous


def decide(rows):
    assembly=[r for r in rows if r['variant']=='assembly'];integration=[r for r in rows if r['variant']=='integrated']
    if len(rows)!=4 or {r['seed'] for r in assembly}!={0,1,2} or len(integration)!=1 or integration[0]['seed']!=1:raise ValueError('Require four selected CH1 cases')
    minimum=.25*math.pi*8.325**2
    witnesses=sum(any(c['units']>=26 and c['area']>=minimum for c in r['simple_contours']) for r in assembly)
    row=integration[0]
    conditions=dict(ports=all(r['final_ports_valid'] for r in rows),
        integrated_invariants=row['invariant_failures']==0,temperature=all(r['late_temperature']<=.12 for r in rows),
        macroscopic_final_contour_two_seeds=witnesses>=2,selected_integrated_closure=row['valid_fraction_late']>=.8,
        selected_integrated_production=all(row[k]>0 for k in ('G_new','F_new','L_new')))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Selected1800 horizon, final simple geometry only. No first-passage, continuous retention, general robustness, homeostasis or independence from CC1. No final witness does not exclude earlier transient closure; no closure rate inferred.')


def collect(folder,require_complete=True):
    report=previous(folder,require_complete,expected_tasks=4,decision_fn=decide)
    report['scope']='CH1 three isolated cases and selected integrated seed1, longer horizon with fixed laws/initial material.'
    write(Path(folder)/'competitive_horizon_review.json',report);return report
