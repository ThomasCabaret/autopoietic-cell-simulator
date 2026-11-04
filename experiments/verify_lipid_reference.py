"""The unmodified L1 default remains exact against its frozen recipe prefix."""
import json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write


def main():
    recipe=ROOT/'research/campaign_recipes/L1P_20261104T115550305191Z'
    cfg=read(recipe/'manifest.json')['tasks'][0]['scenario']
    out=ROOT/'outputs/diagnostics'/('L2_reference_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    write(out/'scenario.json',cfg)
    code=('import json,sys; from simulator.engine import Simulation; from simulator.checkpoint import save; '
        'sim=Simulation(json.load(open(sys.argv[1],encoding="utf-8"))); sim.advance(round(5./sim.dt));save(sys.argv[2],sim)')
    for name,cwd in (('old',recipe/'runtime'),('current',ROOT)):
        subprocess.run([sys.executable,'-c',code,str(out/'scenario.json'),str(out/f'{name}.npz')],cwd=cwd,check=True)
    with np.load(out/'old.npz',allow_pickle=False) as a,np.load(out/'current.npz',allow_pickle=False) as b:
        for key in ('positions','springs','angles'):np.testing.assert_array_equal(a[key],b[key])
        x,y=[json.loads(str(z['metadata'])) for z in (a,b)]
    for v in (x,y):
        v.pop('source_sha256');v['config']['chemistry'].pop('formation_gate',None);v['config']['chemistry'].pop('tool_lipid_contact',None)
    if x!=y:raise ValueError('L1 reference state changed')
    write(out/'report.json',dict(time=5.,physical_state_rng_motion_and_chemistry_exact=True,
        limitation='Prefix only; permits reuse of original unchanged-law pilot, not proof of new L2 compatibility.'))
    print(out)
    return out


if __name__=='__main__':main()
