"""PI1 passive binding evidence, explicitly not a homeostasis score."""
from pathlib import Path
from statistics import median
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write


def decide(rows):
    if len(rows)!=15:raise ValueError('Require all15 PI1 cases')
    groups={v:[r for r in rows if r['variant']==v] for v in ('zero','linked4','split4','linked16','split16')}
    if any(len(g)!=3 or {r['seed'] for r in g}!={0,1,2} for g in groups.values()):raise ValueError('PI1 seeds/cases incomplete')
    conditions=dict(no_false_binding=all(r['occupied_G_fraction']==0 for r in groups['zero']),
        birth_disabled=all(r['new_backbone_links']==0 and r['new_composites']==0 for r in rows),
        linked_products_occupy_gene=median(r['occupied_G_fraction'] for r in groups['linked16'])>=.1)
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Existing binding opportunity only. No measured inhibition of production, '
            'homeostasis, useful losses, selective protection, feed or polymer regulation.')


def collect(folder,require_complete=True):
    folder=Path(folder);m=validate(folder);s=status(folder)
    if require_complete and (s['controller_active'] or s['counts']['complete']!=15):raise ValueError('Require inactive complete PI1')
    hashes={k:v for k,v in m['source_sha256'].items() if k.startswith('simulator/')};rows=[]
    for task,state in zip(m['tasks'],s['tasks']):
        if state['phase']!='complete':continue
        p=folder/state['result'];r=read(p);a=read(folder/state['genetic_audit'])
        if not r['completed'] or r['error'] or r['scenario']!=task['scenario'] or r['source_sha256']!=hashes:raise ValueError('PI1 provenance mismatch')
        windows=[w for w in a['state']['windows'].values() if 200<=w['start']<400]
        time=sum(w['observed_time'] for w in windows)
        ex={key:sum(w['exposure'].get(key,0.) for w in windows) for key in ('paired_GF','active_G','active_F','recognition_eligible_GF')}
        rows.append(dict(label=task['label'],seed=task['scenario']['seed'],variant=task['label'].split('_')[1],
            observed_late_time=time,occupied_G_fraction=ex['paired_GF']/ex['active_G'],
            F_site_paired_fraction=ex['paired_GF']/ex['active_F'] if ex['active_F'] else None,
            exposure=ex,new_backbone_links=a['ligations'],new_composites=a['assembled'],
            completed_net_pair_span=a['max_completed_net_pair_span'],censored_pairs=a['right_censored_pairs'],
            elapsed_seconds=r['elapsed_seconds'],result_sha256=digest(p)))
    report=dict(counts=s['counts'],controller_active=s['controller_active'],rows=rows,
        decision=decide(rows) if len(rows)==15 else None,manifest_sha256=digest(folder/'manifest.json'),
        scope='Pre-reaction counts left-held, one-tick lag and approximate dwell, not exact hazard. '
            'Late cycle200-400. Prepared products, no formation or loss, separate binding assay.')
    write(folder/'product_binding_review.json',report);return report
