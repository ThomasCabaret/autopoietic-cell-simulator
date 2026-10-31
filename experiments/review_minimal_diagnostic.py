"""Verify passive replay before interpreting bounded MIN1D captures."""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write
from scripts.campaign import validate,status,digest


def exact_checkpoint(reference,replay):
    with np.load(reference,allow_pickle=False) as a,np.load(replay,allow_pickle=False) as b:
        for k in ('positions','springs','angles'):np.testing.assert_array_equal(a[k],b[k])
        x,y=(json.loads(str(z['metadata'])) for z in (a,b))
    for k in ('config','step','prepared','rng','chemistry','motion'):
        if x.get(k)!=y.get(k):raise ValueError('Physical replay differs: '+k)
    return True


def review(folder=None):
    folder=Path(folder) if folder else Path((ROOT/'outputs/minimal_diagnostic_campaigns/latest.txt').read_text().strip())
    manifest=validate(folder);snap=status(folder);plan=read(folder/'plan.json');rows=[]
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    allowed={'simulator/campaign_worker.py','simulator/genetic_audit.py','simulator/ligation_loupe.py'}
    for task,st in zip(manifest['tasks'],snap['tasks']):
        if st['phase']!='complete':continue
        ref=plan['references'][task['label']]
        for key in ('result','checkpoint'):
            if digest(Path(ref[key]))!=ref[key+'_sha256']:raise ValueError('Reference changed')
        original=read(ref['result']);result=read(folder/st['result'])
        if result['scenario']!=original['scenario'] or result['scenario']!=task['scenario'] or result['source_sha256']!=hashes:
            raise ValueError('Source/config mismatch')
        for key in (set(hashes)|set(original['source_sha256']))-allowed:
            if hashes.get(key)!=original['source_sha256'].get(key):raise ValueError('Non-observer source changed: '+key)
        if not result['completed'] or result['error'] or result['metrics']!=original['metrics']:
            raise ValueError('Replay completion/primary metrics differ')
        exact_checkpoint(ref['checkpoint'],(folder/st['result']).parent/'checkpoint.npz')
        audit=read(folder/st['genetic_audit']);loupe=audit['ligation_loupe']
        exposure=audit['exposure'];typed=loupe['exposure']
        rows.append(dict(label=task['label'],physical_replay_exact=True,primary_metrics_exact=True,
            exposure={k:v for k,v in exposure.items() if k.startswith(('recognition_','ligation_','paired_GF','active_F'))},
            F_edge_exposure=typed,loupe={k:v for k,v in loupe.items() if k!='state'},
            result_sha256=digest(folder/st['result']),audit_sha256=digest(folder/st['genetic_audit'])))
    report=dict(counts=snap['counts'],controller_active=snap['controller_active'],rows=rows,
        scope='Two selected exact replays. Exposure is approximate pre-tick edge-time; captures miss within-tick transient motifs. '
              'Interpret only after physical and primary-metric equality; no success-rate inference.')
    write(folder/'diagnostic_review.json',report);print(json.dumps(report,indent=2));return folder,report


if __name__=='__main__':review()
