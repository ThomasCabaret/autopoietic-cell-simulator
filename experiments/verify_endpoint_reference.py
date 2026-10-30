"""Exact archived/current MD2 prefixes with the optional T9E rule absent."""
import json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_expression_campaign import baseline,MD2


def run():
    out=ROOT/'outputs/diagnostics'/('T9E_reference_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    code=('import json,sys; from simulator.engine import Simulation; from simulator.checkpoint import save; '
          'sim=Simulation(json.load(open(sys.argv[1],encoding="utf-8"))); '
          'sim.advance(round(5./sim.dt)); save(sys.argv[2],sim)')
    rows=[]
    for seed in range(3):
        cfg=baseline(seed);path=out/f's{seed}.json';path.write_text(json.dumps(cfg),encoding='utf-8')
        for mode,cwd in (('old',MD2.parent/'runtime'),('current',ROOT)):
            subprocess.run([sys.executable,'-c',code,str(path),str(out/f'{mode}{seed}.npz')],cwd=cwd,check=True)
        with np.load(out/f'old{seed}.npz',allow_pickle=False) as a,np.load(out/f'current{seed}.npz',allow_pickle=False) as b:
            for key in ('positions','springs','angles'):np.testing.assert_array_equal(a[key],b[key])
            x,y=(json.loads(str(z['metadata'])) for z in (a,b))
            for v in (x,y):v.pop('source_sha256')
            assert x==y
        rows.append(dict(seed=seed,time=5.,positions_bonds_rng_motion_exact=True))
    report=dict(rows=rows,scope='Exact five-unit prefixes of all three current integrated MD2 demos; '
        'optional endpoint rule absent. Does not re-estimate long-run success or validate the new variant.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (out/'driver.py').write_bytes(Path(__file__).read_bytes());print(json.dumps(dict(folder=str(out),**report)))


if __name__=='__main__':run()
