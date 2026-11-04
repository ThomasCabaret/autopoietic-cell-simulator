"""Check default MD2/MIN1R/MIN1M and L3 prefixes against preserved source recipes."""
import json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write


def main():
    cases=[('MIN1R_20261031T110654015735Z','MIN1R_active_s0'),
        ('MIN1M_20261104T113752867767Z','MIN1M_active_s0'),
        ('MD2_20261030T115427443420Z','MD2_bath_new_s2'),
        ('L3_20261104T164655147905Z','L3_combined_s0')]
    out=ROOT/'outputs/diagnostics'/('CT1_reference_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    code=('import json,sys;from simulator.engine import Simulation;from simulator.checkpoint import save;'
        'sim=Simulation(json.load(open(sys.argv[1],encoding="utf-8")));sim.advance(round(5./sim.dt));save(sys.argv[2],sim)')
    rows=[]
    for recipe_name,label in cases:
        recipe=ROOT/'research/campaign_recipes'/recipe_name
        cfg=next(t['scenario'] for t in read(recipe/'manifest.json')['tasks'] if t['label']==label)
        case=out/label;case.mkdir();write(case/'scenario.json',cfg)
        for name,cwd in (('old',recipe/'runtime'),('current',ROOT)):
            subprocess.run([sys.executable,'-c',code,str(case/'scenario.json'),str(case/f'{name}.npz')],cwd=cwd,check=True)
        with np.load(case/'old.npz',allow_pickle=False) as a,np.load(case/'current.npz',allow_pickle=False) as b:
            for k in ('positions','springs','angles'):np.testing.assert_array_equal(a[k],b[k])
            x,y=[json.loads(str(z['metadata'])) for z in (a,b)]
        for value in (x,y):value.pop('source_sha256')
        if x!=y:raise ValueError(f'Physical state/RNG/motion changed: {label}')
        rows.append(dict(label=label,time=5.,state_rng_motion_exact=True))
    write(out/'report.json',dict(rows=rows));print(out);return out


if __name__=='__main__':main()
