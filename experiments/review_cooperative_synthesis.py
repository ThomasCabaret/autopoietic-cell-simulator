"""MX2 matched-horizon decision and post-hoc stocks; no state feedback."""
from pathlib import Path
from statistics import median
from experiments.review_mixed_synthesis import collect as collect_previous
from experiments.mixed_calibration import row as stock_row
from scripts.campaign import validate,status
from simulator.campaign_io import read,write


def decide(rows):
    if len(rows)!=12:raise ValueError('Require all12 MX2 trials')
    groups={}
    for v in ('cooperative','reference','nogene','noHT'):
        g=[r for r in rows if r['label'].startswith(f'MX2_{v}_s')]
        if len(g)!=3 or {r['seed'] for r in g}!={0,1,2}:raise ValueError('Require three unique seeds per condition')
        groups[v]=g
    a,b,g,n=[groups[k] for k in ('cooperative','reference','nogene','noHT')]
    conditions=dict(G_median_at_least_half_noHT=median(r['G_new'] for r in a)>=.5*median(r['G_new'] for r in n),
        F_median_at_least_half_noHT=median(r['F_new'] for r in a)>=.5*median(r['F_new'] for r in n),
        G_median_improved_over_reference=median(r['G_new'] for r in a)>median(r['G_new'] for r in b),
        simultaneous_transfer_two_seeds=sum(r['renewal']['active_wholly_constructed_F']>0 and
            r['catalyzed_lipids']>=4 and r['new_lipids_later_contacted']>0 for r in a)>=2,
        whole_food_F_to_L_two_seeds=sum(r['lipids_from_whole_food_F']>0 for r in a)>=2,
        nogene_negative=all(r['F_new']==0 and r['lipids_from_expressed_F']==0 for r in g),
        noHT_no_false_catalysis=all(r['catalyzed_lipids']==0 for r in n),
        no_wrong_double_time=all(r['sampled_wrong_double_edge_time']==0 for r in a),
        atom_ports_valid=all(r['atom_port_invariant_failures']==0 for r in rows))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Selected finite2400-unit followups, not independent robustness or maintenance. '
            'One new local law, no added feed. Original MX1 at1200 stays refused. Stop for interpretation.')


def collect(folder,require_complete=True):
    # The generic collector's physical rows are reused, but its MX1 decision
    # must never be applied to the new variant names or horizon.
    folder=Path(folder);m=validate(folder);s=status(folder)
    if require_complete and (s['controller_active'] or s['counts']['complete']!=12):raise ValueError('Require complete inactive MX2')
    report=collect_previous(folder,require_complete,decision_fn=decide)
    stocks=[stock_row(folder,t,st,m) for t,st in zip(m['tasks'],s['tasks']) if st['phase']=='complete']
    report['calibration']=[dict(label=r['label'],windows=r['windows'],last_PR=r['last_PR'],last_L=r['last_L'],
        time_weighted_occupancy=r['time_weighted_occupancy']) for r in stocks]
    # Selected longer references must reproduce the entire original observed
    # prefix, not merely a few favorable endpoint counts.
    reference=read(folder/'plan.json')['reused_MX1'];old_folder=Path(reference['campaign'])
    from scripts.campaign import digest
    old_m=validate(old_folder);old_s=status(old_folder)
    if digest(old_folder/'manifest.json')!=reference['manifest_sha256'] or old_s['counts']['complete']!=12:
        raise ValueError('MX1 reference changed or incomplete')
    prefixes=[]
    for t,st in zip(m['tasks'],s['tasks']):
        if '_reference_' not in t['label'] or st['phase']!='complete':continue
        old_label=f'MX1_mixed_s{t["scenario"]["seed"]}'
        index=next(i for i,q in enumerate(old_m['tasks']) if q['label']==old_label)
        old=read(old_folder/old_s['tasks'][index]['result']);new=read(folder/st['result'])
        for section,key in (('metrics','history'),('metrics','births'),('genetics','history'),('genetics','events')):
            a=old['metrics'] if section=='metrics' else old['metrics']['genetics']
            b=new['metrics'] if section=='metrics' else new['metrics']['genetics']
            if a[key]!=[e for e in b[key] if e['time']<=1200.+1e-9]:raise ValueError('Selected reference prefix changed: '+key)
        prefixes.append(dict(label=t['label'],original_label=old_label,observed_prefix_exact_through=1200.))
    report['reference_prefix_checks']=prefixes
    report['scope']='MX2 fixed-law reference and cooperative variants at matched2400 horizon; source-checked stocks and finite-window production, no asymptotic failure inference.'
    write(folder/'cooperative_synthesis_review.json',report);return report
