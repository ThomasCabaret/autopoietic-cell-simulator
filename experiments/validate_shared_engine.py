"""A pinned technical migration campaign; it does not assert new chemical maturity."""
import json
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from simulator.config import legacy
from simulator.engine import Simulation
from simulator.runner import make_observer,compact

case=sys.argv[1]
seed=int(sys.argv[2]) if len(sys.argv)>2 else 0
cases=json.loads((ROOT/'research/cases.json').read_text(encoding='utf-8'))
duration=float(sys.argv[3]) if len(sys.argv)>3 else (300. if case=='V4' else 600.)
config=legacy({**cases[case],'case':case,'seed':seed,'duration':duration})
sim=Simulation(config)
obs=make_observer(sim.config,record=False)
sim.listeners.append(obs)
start=time.perf_counter()
while not sim.done: sim.advance(1000)
print(json.dumps({'case':case,'seed':seed,'elapsed':time.perf_counter()-start,
                  'config':sim.config,'metrics':compact(obs.summary())},ensure_ascii=False),flush=True)
