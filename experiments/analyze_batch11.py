"""Validate boundary census and compare unchanged B laws with prior local K1 data."""
import argparse,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,read,write


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path);a=p.parse_args()
    folder=a.folder.resolve();manifest=validate(folder)
    expected_sources={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    subprocess.run([sys.executable,str(ROOT/'scripts/campaign.py'),'analyze',str(folder)],check=True)
    report=read(folder/'analysis.json');rows=[]
    previous=ROOT/'outputs/campaigns/campaign_20261026T102204813246Z'
    old={}
    if previous.exists():
        validate(previous)
        for s in status(previous)['tasks']:
            if s['phase']=='complete':
                r=read(previous/s['result'])
                if r['scenario']['name']=='M1B_long':old[r['scenario']['seed']]=s
    for row in report['rows']:
        task=next(t for t in status(folder)['tasks'] if t['id']==row['task'])
        result=read(folder/task['result']);audit=read(folder/task['boundary_audit'])
        assert result['completed'] and not result['error']
        assert result['source_sha256']==expected_sources
        counts=audit['sample_counts'];history=result['metrics']['history']
        assert audit['samples']==sum(counts.values())==len(history)
        assert counts.get('closed',0)==sum(h['parent_closed'] for h in history)
        assert sum(audit['unknown_reason_samples'].values())==sum(not h['envelope_valid'] for h in history)
        assert abs(sum(audit['state_time'].values())-result['scenario']['duration'])<1e-8
        check=dict(task=task['id'],name=row['name'],seed=row['seed'],boundary_census_verified=True,
            legacy_reference='not applicable or prior raw data unavailable')
        if row['name']=='M1B_recheck' and row['seed'] in old:
            reference=old[row['seed']];saved=read(previous/reference['result'])
            assert saved['source_sha256']=={k:v for k,v in read(previous/'manifest.json')['source_sha256'].items() if k.startswith('simulator/')}
            assert saved['metrics']==result['metrics']
            with np.load(previous/reference['checkpoint']) as x,np.load(folder/task['checkpoint']) as y:
                np.testing.assert_array_equal(x['positions'],y['positions'])
                mx=json.loads(str(x['metadata']));my=json.loads(str(y['metadata']))
                assert mx['rng']==my['rng'] and mx['chemistry']==my['chemistry']
            check['legacy_reference']='all metrics, positions, RNG and chemistry identical to K1'
        rows.append(check)
    out=folder/('post_analysis_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir()
    source=Path(__file__).read_bytes();(out/'analyze_batch11.py').write_bytes(source)
    write(out/'verification.json',dict(source_sha256=hashlib.sha256(source).hexdigest(),
        complete=report['counts']['complete'],total=len(read(folder/'manifest.json')['tasks']),checks=rows))
    print(json.dumps(dict(verified=len(rows),report=str(out)),ensure_ascii=False))
