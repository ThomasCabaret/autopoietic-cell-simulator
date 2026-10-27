"""Audit genetic opportunity counts and exact J0 replay against local evidence."""
import argparse,hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,read,write


def analyze(folder,reference):
    folder=Path(folder).resolve();manifest=validate(folder);expected={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    refs={}
    if reference.exists():
        validate(reference)
        for state in status(reference)['tasks']:
            if state['phase']=='complete':
                r=read(reference/state['result']);refs[(r['scenario']['name'],r['scenario']['seed'])]=state
    rows=[]
    for state in status(folder)['tasks']:
        if state['phase']!='complete':continue
        r=read(folder/state['result']);a=read(folder/state['genetic_audit']);m=r['metrics'];duration=r['scenario']['duration']
        assert r['completed'] and r['error'] is None and r['source_sha256']==expected
        assert abs(a['observed_time']-duration)<1e-7
        assert a['ligations']==m['ligation_events'] and a['assembled']==m['assembled_dimers']
        assert a['catalytic_assembled']==m['catalyzed_dimers']
        exposure=a['exposure']
        recog=sum(v for k,v in exposure.items() if k.startswith('recognition_blocked_') or k.startswith('recognition_eligible_'))
        lig=sum(v for k,v in exposure.items() if k.startswith('ligation_blocked_') or k.startswith('ligation_eligible_'))
        assert abs(recog-exposure.get('recognition_near',0.))<1e-6
        assert abs(lig-exposure.get('ligation_double_paired',0.))<1e-6
        key=(r['scenario']['name'],r['scenario']['seed']);exact=None
        if key in refs and duration==400.:
            old=refs[key];saved=read(reference/old['result']);assert m==saved['metrics']
            with np.load(folder/state['checkpoint']) as x,np.load(reference/old['checkpoint']) as y:
                np.testing.assert_array_equal(x['positions'],y['positions'])
                mx=json.loads(str(x['metadata']));my=json.loads(str(y['metadata']))
                assert mx['rng']==my['rng'] and mx['chemistry']==my['chemistry']
            exact=True
        row=dict(task=state['id'],name=key[0],seed=key[1],duration=duration,exact_primary_replay=exact,
                 F=m['translated_detached_ever'],incorporated=m['incorporated_constructed'],audit={k:v for k,v in a.items() if k!='state'})
        rows.append(row)
    out=folder/('post_analysis_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir()
    source=Path(__file__).read_bytes();(out/'analyze_batch14.py').write_bytes(source)
    write(out/'verification.json',dict(source_sha256=hashlib.sha256(source).hexdigest(),rows=rows))
    for r in rows:
        e=r['audit']['exposure'];print(json.dumps(dict(name=r['name'],seed=r['seed'],F=r['F'],exact=r['exact_primary_replay'],
            recognition_near=e.get('recognition_near',0.),recognition_eligible_GF=e.get('recognition_eligible_GF',0.),
            paired_GF=e.get('paired_GF',0.),double_paired=e.get('ligation_double_paired',0.),
            ligation_eligible_F=e.get('ligation_eligible_F',0.),catalytic_eligible=e.get('assembly_catalytic_eligible',0.))))
    print(str(out))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path)
    p.add_argument('--reference',type=Path,default=ROOT/'outputs/campaigns/campaign_20261027T113835658766Z')
    a=p.parse_args();analyze(a.folder,a.reference)
