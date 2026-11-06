"""Read frozen OB1 results; a transport construction screen, not cell evidence."""
import argparse
import json
from pathlib import Path
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write


def collect(folder):
    folder=Path(folder);manifest=validate(folder);snap=status(folder)
    if snap['controller_active'] or snap['counts']['complete']!=6:raise ValueError('Require six complete inactive OB1 trials')
    rows=[];hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    for task,state in zip(manifest['tasks'],snap['tasks']):
        path=folder/state['result'];r=read(path);m=r['metrics'];cfg=r['scenario']
        if r['error'] or not r['completed'] or cfg!=task['scenario'] or r['source_sha256']!=hashes:
            raise ValueError('OB1 provenance mismatch')
        late=[q for q in m['history'] if q['time']>=40.];final=m['final']
        rows.append(dict(label=task['label'],seed=cfg['seed'],dt=cfg['engine']['dt'],counts=final['counts'],
            injected=final['injected'],exported=final['exported'],max_balance_error=m['max_balance_error'],
            max_population=m['max_population'],source_digest=m['source_digest'],max_injection_lag=m['max_injection_lag'],
            mean_late_population=sum(sum(q['counts']) for q in late)/len(late),
            central_half_reached=any(sum(q['inside_central_half'])>0 for q in m['history']),
            elapsed_seconds=r['elapsed_seconds'],simulated_per_second=cfg['duration']/r['elapsed_seconds'],
            result_sha256=digest(path)))
    conditions=dict(exact_balance=all(r['max_balance_error']==0 for r in rows),
        real_exchange=all(sum(r['injected'])>0 and sum(r['exported'])>0 for r in rows),
        central_transport=all(r['central_half_reached'] for r in rows),
        application_lag=all(r['max_injection_lag']<=.02+1e-9 for r in rows),
        matched_source=all(len({r['source_digest'] for r in rows if r['seed']==s})==1 for s in range(3)))
    report=dict(rows=rows,counts=snap['counts'],conditions=conditions,screen_passed=all(conditions.values()),
        scope='Finite80 transport only. dt pairs share source but not thermal paths. Population differences are stochastic, '
            'not a convergence estimate. No membrane/G/F/L, chemistry, homeostasis or loss-helper transfer.')
    write(folder/'open_boundary_review.json',report)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);a=p.parse_args()
    print(json.dumps(collect(a.folder),indent=2))
