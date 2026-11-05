"""CB1 fixed gates; shared BI1 evidence reader handles real products/controls."""
from statistics import median
from experiments.review_boundary_transfer import collect as previous


def decide(rows):
    if len(rows)!=9:raise ValueError('Require9 CB1 cases')
    groups={}
    for variant in ('active','noL','nosynthesis'):
        g=[r for r in rows if r['label'].startswith(f'CB1_{variant}_s')]
        if len(g)!=3 or {r['seed'] for r in g}!={0,1,2}:raise ValueError('Require unique CB1 seeds')
        groups[variant]=g
    a,n,z=[groups[k] for k in ('active','noL','nosynthesis')]
    conditions=dict(atom_ports_valid=all(r['invariant_failures']==0 for r in rows),
        active_late_contour=all(r['valid_fraction_late']>=.8 for r in a),
        actual_inside_product_in_contour_two_seeds=sum(r['inserted_born_inside']>0 for r in a)>=2,
        noL_G_reference_positive=median(r['G_new'] for r in n)>0,
        noL_F_reference_positive=median(r['F_new'] for r in n)>0,
        G_at_least_half_noL=median(r['G_new'] for r in a)>=.5*median(r['G_new'] for r in n),
        F_at_least_half_noL=median(r['F_new'] for r in a)>=.5*median(r['F_new'] for r in n),
        nosynthesis_negative=all(r['L_new']==0 and r['inserted_born_inside']==0 for r in z))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Selected compact geometry, finite stocks and external cycle. No fed maintenance or losses. '
            'Negative/noL controls are new at the same horizon. Stop regardless of result.')


def collect(folder,require_complete=True):
    return previous(folder,require_complete,decision_fn=decide)
