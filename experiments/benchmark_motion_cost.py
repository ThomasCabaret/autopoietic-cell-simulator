"""Short serial cost measurements; not a proxy for a completed mixing goal."""
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
import sys
import time
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_motion_campaign import scenario
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.checkpoint import source_hashes


def main():
    out=ROOT/'outputs/performance'/('motion_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    out.mkdir(parents=True)
    rows=[]
    for kind,gamma in (('brownian',4.),('langevin',4.),('langevin',.1),('dpd',.5),('dpd',2.)):
        for observed in (False,True):
            cfg=scenario(kind,gamma,duration=1000.);sim=Simulation(cfg)
            if observed:sim.listeners.append(make_observer(sim.config,False))
            sim.advance(500)  # warm compilation and initial caches, never included
            blocks=[]
            for _ in range(3):
                begin=time.perf_counter();sim.advance(2000);blocks.append(time.perf_counter()-begin)
            row=dict(kind=kind,damping=gamma,observed=observed,scenario=sim.config,
                block_steps=2000,block_seconds=blocks,median_steps_per_second=2000/float(np.median(blocks)))
            if sim.motion is not None:row['motion']=sim.motion.diagnostics(sim.chemistry)
            rows.append(row)
    payload=dict(source_sha256=source_hashes(),driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        rows=rows,limitations='Serial blocks while other campaigns may be active. Different motion trajectories, early density state, three short blocks only. Not a whole-cell or chemical-reaction speedup.')
    (out/'benchmark.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    (out/'driver.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(dict(folder=str(out),rows=[{k:r[k] for k in ('kind','damping','observed','median_steps_per_second')} for r in rows])))


if __name__=='__main__':main()
