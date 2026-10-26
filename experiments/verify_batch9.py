"""Exact old-chemistry regressions and source-only reconstruction for lot 9."""
import argparse,json,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.runner import run
from scripts.reconstruct_experiment import reconstruct


def compare(original,new):
    a=json.loads((original/'result.json').read_text(encoding='utf-8'))
    b=json.loads((new/'result.json').read_text(encoding='utf-8'))
    assert a['metrics']==b['metrics'] and b['completed'] and not b['error']
    with np.load(original/'trajectory.npz') as x,np.load(new/'trajectory.npz') as y:
        assert set(x.files)==set(y.files)
        for key in x.files:np.testing.assert_array_equal(x[key],y[key])
        keys=list(x.files)
    return dict(original=original.relative_to(ROOT).as_posix(),new=new.relative_to(ROOT).as_posix(),
        all_metrics_equal=True,all_arrays_equal=True,arrays=keys)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('case',choices=['membrane','copy','reconstruct'])
    a=p.parse_args();out=ROOT/'outputs/batch9/verification';out.mkdir(parents=True,exist_ok=True)
    if a.case=='reconstruct':
        original=next((ROOT/'research/engine_runs').glob('M1noBondBarrier_s0*'))
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        new=reconstruct(original,out/('reconstructed_'+stamp))
    else:
        pattern='V8curved_s0*' if a.case=='membrane' else 'C3Bexpress_s1*'
        original=next((ROOT/'research/engine_runs').glob(pattern))
        cfg=json.loads((original/'scenario.json').read_text(encoding='utf-8'))
        _,new=run(cfg,out)
    result=compare(original,new)
    (out/(new.name+'_comparison.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))
