"""Verify the frozen G1 cohort and summarize joint criteria without retuning."""
import argparse,hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,read,write


def analyze(folder):
    folder=Path(folder).resolve();manifest=validate(folder);rows=[]
    expected={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    snapshot=status(folder)
    for task in snapshot['tasks']:
        if task['phase']!='complete':continue
        result=read(folder/task['result']);m=result['metrics'];a=read(folder/task['boundary_audit'])
        k=read(folder/task['kinetics']);history=m['history']
        assert result['completed'] and not result['error'] and result['source_sha256']==expected
        assert a['samples']==len(history)==sum(a['sample_counts'].values())
        assert a['sample_counts']['closed']==sum(h['parent_closed'] for h in history)
        assert sum(a['unknown_reason_samples'].values())==sum(not h['envelope_valid'] for h in history)
        assert abs(sum(a['state_time'].values())-result['scenario']['duration'])<1e-8
        assert len(m['exchange_events'])==k['opportunity_totals']['exchanges']
        rows.append(dict(seed=result['scenario']['seed'],closed=m['parent_closed_fraction'],
            valid=m['envelope_valid_fraction'],inserted=m['inserted_into_closed_parent_ever'],
            persistent=m['persistent_inserted_10'],escape=m['retained_escape_fraction'],
            joint_screen=bool(m['parent_closed_fraction']>=.8 and m['retained_escape_fraction']<=.05 and m['persistent_inserted_10']>0),
            counts_and_sources_verified=True))
    out=folder/('post_analysis_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir()
    source=Path(__file__).read_bytes();(out/'analyze_batch12.py').write_bytes(source)
    report=dict(complete=snapshot['counts']['complete'],total=len(manifest['tasks']),rows=rows,
        source_sha256=hashlib.sha256(source).hexdigest(),
        conclusion='Insertion retained; joint screen 2/3 is not robust closure or proven retention during unknown periods.')
    write(out/'verification.json',report);print(json.dumps(dict(report=str(out),**report),ensure_ascii=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path);a=p.parse_args();analyze(a.folder)
