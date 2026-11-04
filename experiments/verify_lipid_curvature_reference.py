"""Default L2 dynamics unchanged by optional pose/curvature implementation."""
import json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write


def main():
    recipe=ROOT/'research/campaign_recipes/L2_20261104T122737643199Z'
    cfg=next(t['scenario'] for t in read(recipe/'manifest.json')['tasks'] if t['label']=='L2_combined_s0')
    out=ROOT/'outputs/diagnostics'/('L3_reference_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    write(out/'scenario.json',cfg)
    code=('import json,sys; from simulator.engine import Simulation; from simulator.checkpoint import save; '
        'sim=Simulation(json.load(open(sys.argv[1],encoding="utf-8")));sim.advance(round(5./sim.dt));save(sys.argv[2],sim)')
    for name,cwd in (('old',recipe/'runtime'),('current',ROOT)):
        subprocess.run([sys.executable,'-c',code,str(out/'scenario.json'),str(out/f'{name}.npz')],cwd=cwd,check=True)
    with np.load(out/'old.npz',allow_pickle=False) as a,np.load(out/'current.npz',allow_pickle=False) as b:
        for k in ('positions','springs','angles'):np.testing.assert_array_equal(a[k],b[k])
        x,y=[json.loads(str(z['metadata'])) for z in (a,b)]
    for v in (x,y):
        v.pop('source_sha256');v['config']['chemistry'].pop('capture_curvature',None);v['config']['chemistry'].pop('tool_pose',None)
    if x!=y:raise ValueError('L2 default physical state changed')
    write(out/'report.json',dict(time=5.,physical_state_chemistry_rng_motion_exact=True))
    print(out);return out


if __name__=='__main__':main()
