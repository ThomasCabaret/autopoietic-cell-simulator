"""N2 factor separation, retaining raw cohort comparisons without causal overclaim."""
import argparse
import hashlib
import json
import statistics
import sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate
from simulator.campaign_io import read,write
from experiments.analyze_constructed_tool import analyze
from experiments.analyze_numerical_campaign import compare as compare_n1,BASELINE


def compare(folder,n1,baseline=BASELINE):
    folder,n1,baseline=map(lambda p:Path(p).resolve(),(folder,n1,baseline))
    old,new=validate(n1),validate(folder)
    if {k for k in old['source_sha256'] if k.startswith('simulator/')}!={k for k in new['source_sha256'] if k.startswith('simulator/')}:
        raise ValueError('N2 may not add or remove simulator modules')
    changed={k for k in old['source_sha256'] if k.startswith('simulator/')
        and old['source_sha256'][k]!=new['source_sha256'].get(k)}
    if changed!={'simulator/config.py','simulator/engine.py'}:
        raise ValueError('N2 requires the reviewed cadence-only engine/config revision')
    refs={t['scenario']['seed']:t['scenario'] for t in old['tasks'] if t['label']=='N1_dt4'}
    seen=set()
    for task in new['tasks']:
        cfg=task['scenario'];every=int(cfg['name'].removeprefix('N2_every'))
        if every not in (10,20) or (every,cfg['seed']) in seen:raise ValueError('Unexpected N2 task')
        seen.add((every,cfg['seed']));ref=refs[cfg['seed']]
        engine=dict(ref['engine'],reaction_every=every)
        if cfg['chemistry']!=ref['chemistry'] or cfg['engine']!=engine or cfg['duration']!=ref['duration']:
            raise ValueError('N2 laws, numerics or horizon changed')
    if seen!={(e,s) for e in (10,20) for s in range(3)}:raise ValueError('Incomplete N2 design')
    joint=read(compare_n1(n1,baseline)/'report.json')
    if not joint['triage']['complete_cohorts']:raise ValueError('N1 must finish before interpreting N2')
    report=read(analyze(folder)/'report.json')
    levels={f'joint_dt{f}':rows for f,rows in joint['levels'].items()}
    levels.update({f'fine_every{e}':[r for r in report['rows'] if r['case']==f'N2_every{e}'] for e in (10,20)})
    medians={key:dict(catalyzed=statistics.median(r['catalyzed'] for r in rows),
        incorporated=statistics.median(r['catalyzed_incorporated'] for r in rows),
        closed=statistics.median(r['membrane']['regular_grid_closed_fraction'] for r in rows),
        envelope=statistics.median(r['membrane']['regular_grid_envelope_fraction'] for r in rows))
        for key,rows in levels.items() if len(rows)==3}
    out=folder/('cadence_analysis_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir()
    hashes={}
    for name in ('experiments/analyze_cadence_campaign.py','experiments/analyze_numerical_campaign.py',
                 'experiments/analyze_constructed_tool.py','experiments/inventory_audit.py'):
        src=ROOT/name;dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(src.read_bytes())
        hashes[name]=hashlib.sha256(src.read_bytes()).hexdigest()
    result=dict(campaign=str(folder),n1=str(n1),baseline=str(baseline),levels=levels,medians=medians,
        complete_cohort=report['complete_cohort'],analysis_source_sha256=hashes,
        source_changes=sorted(changed),
        comparisons=dict(mechanical_fixed_reaction=[['joint_dt1','fine_every20'],['joint_dt2','fine_every10']],
            reaction_fixed_mechanical=['fine_every20','fine_every10','joint_dt4']),
        caveat='Descriptive three-seed comparisons, not convergence or proof of cause. '
            'No successful seed selection, new chemistry or automatic mechanistic conclusion.')
    write(out/'report.json',result);print(json.dumps(medians));print(out);return out


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path)
    p.add_argument('--n1',required=True,type=Path);p.add_argument('--baseline',type=Path,default=BASELINE)
    a=p.parse_args();compare(a.folder,a.n1,a.baseline)
