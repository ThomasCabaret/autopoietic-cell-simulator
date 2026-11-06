"""Compare old closed-bath paths exactly after adding the population hook."""
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime,timezone
import numpy as np

ROOT=Path(__file__).resolve().parents[1]


def run():
    frozen=ROOT/'research/campaign_recipes/FR1_20261106T135511017624Z'
    ch=ROOT/'research/campaign_recipes/CH1_20261106T073608844143Z/manifest.json'
    cases=[json.loads((frozen/'manifest.json').read_text())['tasks'][0]['scenario']]
    tasks=json.loads(ch.read_text())['tasks']
    cases.append(next(t['scenario'] for t in tasks if t['scenario']['model']=='lipid_synthesis'))
    cases.append(next(t['scenario'] for t in tasks if t['scenario']['model']=='mixed_synthesis'))
    out=ROOT/'outputs/diagnostics'/('OB1_reference_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    out.mkdir(parents=True)
    code=('import json,sys;from simulator.engine import Simulation;from simulator.checkpoint import save;'
          's=Simulation(json.load(open(sys.argv[1],encoding="utf-8")));s.advance(round(5/s.dt));save(sys.argv[2],s)')
    rows=[]
    for i,cfg in enumerate(cases):
        path=out/f'case{i}.json';path.write_text(json.dumps(cfg),encoding='utf-8')
        for label,cwd in (('old',frozen/'runtime'),('current',ROOT)):
            subprocess.run([sys.executable,'-c',code,str(path),str(out/f'{label}{i}.npz')],cwd=cwd,check=True)
        with np.load(out/f'old{i}.npz',allow_pickle=False) as old,np.load(out/f'current{i}.npz',allow_pickle=False) as new:
            for key in ('positions','springs','angles'):np.testing.assert_array_equal(old[key],new[key])
            a,b=(json.loads(str(z['metadata'])) for z in (old,new))
            a.pop('source_sha256');b.pop('source_sha256')
            if a!=b:raise ValueError('Closed-bath state/RNG changed')
        rows.append(dict(name=cfg['name'],model=cfg['model'],time=5.,physical_state_rng_exact=True))
    report=dict(rows=rows,scope='Selected closed-bath five-unit prefixes, not renewed long-run chemical validation.')
    (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (out/'driver.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(dict(folder=str(out),**report)))


if __name__=='__main__':run()
