"""BI1 prospective contour/true-product transfer gate and calibration."""
from pathlib import Path
from experiments.mixed_calibration import row as stock_row,weighted
from experiments.review_renewal import renewal
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write


def decide(rows):
    if len(rows)!=9:raise ValueError('Require all9 BI1 trials')
    groups={}
    for variant in ('active','noexchange','nosynthesis'):
        group=[r for r in rows if r['label'].startswith(f'BI1_{variant}_s')]
        if len(group)!=3 or {r['seed'] for r in group}!={0,1,2}:raise ValueError('Require unique seeds per BI1 condition')
        groups[variant]=group
    active=groups['active'];negative=groups['nosynthesis']
    conditions=dict(atom_ports_valid=all(r['invariant_failures']==0 for r in rows),
        active_late_contour=all(r['valid_fraction_late']>=.8 for r in active),
        actual_inside_product_in_contour_two_seeds=sum(r['inserted_born_inside']>0 for r in active)>=2,
        nosynthesis_negative=all(r['L_new']==0 and r['inserted_born_inside']==0 for r in negative))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Finite local-packet insertion screen, not sustained confinement, fed maintenance, '
            'membrane replacement under loss or independent robustness. Stop for interpretation.')


def collect(folder,require_complete=True,decision_fn=decide,expected_tasks=9):
    folder=Path(folder);manifest=validate(folder);snapshot=status(folder)
    if require_complete and (snapshot['controller_active'] or snapshot['counts']['complete']!=expected_tasks):raise ValueError('Require complete inactive boundary cohort')
    rows=[];hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    for task,state in zip(manifest['tasks'],snapshot['tasks']):
        if state['phase']!='complete':continue
        path=folder/state['result'];result=read(path)
        if result['error'] or not result['completed'] or result['scenario']!=task['scenario'] or result['source_sha256']!=hashes:
            raise ValueError('BI1 result provenance mismatch')
        m=result['metrics'];g=m['genetics'];duration=task['scenario']['duration']
        b=m.get('boundary',dict(history=[],ever_inserted=[],ever_inserted_born_inside=[],residence={},birth_inside={},sampled_crossings={}))
        history=b['history']
        stock=stock_row(folder,task,state,manifest);kinetics=read(folder/state['kinetics'])
        motion=read(folder/state['motion_audit'])['history'];late=[r['kinetic_temperature'] for r in motion if r['time']>=.75*duration]
        inserted=set(b['ever_inserted_born_inside']);food=[]
        for e in m['births']:
            if e['head'] not in inserted or e['chain_kind']!='expressed' or not e['chain']:continue
            if all(any(q['support']==s and q['time']<e['time'] for q in g['assembly_state']['events']) for s in e['chain']):food.append(e['head'])
        rows.append(dict(label=task['label'],seed=task['scenario']['seed'],G_new=g['detached_copy_sets_ever'],
            F_new=g['translated_detached_ever'],renewal=renewal(g),L_new=m['lipids_formed'],
            lipids_from_whole_food_F=m['lipids_from_whole_food_F'],
            valid_fraction=weighted(history,'valid',0.,duration),valid_fraction_late=weighted(history,'valid',.75*duration,duration),
            inserted=len(b['ever_inserted']),inserted_born_inside=len(inserted),inserted_from_whole_food_F=len(food),
            sampled_residence=b['residence'],birth_inside=b['birth_inside'],sampled_crossings=b['sampled_crossings'],
            final=history[-1] if history else None,invariant_failures=m['atom_port_invariant_failures'],
            calibration=stock,kinetics=kinetics,late_temperature=sum(late)/len(late),
            elapsed_seconds=result['elapsed_seconds'],result_sha256=digest(path)))
    report=dict(counts=snapshot['counts'],controller_active=snapshot['controller_active'],rows=rows,
        decision=decision_fn(rows) if len(rows)==expected_tasks else None,manifest_sha256=digest(folder/'manifest.json'),
        scope='Actual births and same-law L contacts. Closed simple contours are passive witnesses. '
            'Pre-reaction exposure is sampled, not integrated hazard. Original/new IDs never enter laws. '
            'Finite near-frontier packet, global dilution, no feed or losses. Nosynthesis disables shared PR/HT rates.')
    write(folder/'boundary_transfer_review.json',report);return report
