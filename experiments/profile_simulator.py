"""Short instrumented profiles, without observers; not a whole-campaign benchmark."""
import argparse,cProfile,json,pstats,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.engine import Simulation
from simulator.checkpoint import source_hashes
from experiments.run_batch9 import scenario as membrane
from experiments.run_batch8 import scenario as copying


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--steps',type=int,default=5000)
    a=p.parse_args()
    if not 0<a.steps<=5000:p.error('steps must be between1 and5000 for these short scenarios')
    out=ROOT/'outputs/performance'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out.mkdir(parents=True,exist_ok=False)
    cases=[('membrane534',membrane('M1A',0,12.)),('copy102',copying('C3Bexpress',1,30.))]
    for name,cfg in cases:
        sim=Simulation(cfg);sim.advance(10)
        profile=cProfile.Profile();profile.enable();sim.advance(a.steps);profile.disable()
        profile.dump_stats(str(out/(name+'.prof')))
        with (out/(name+'.txt')).open('w',encoding='utf-8') as stream:
            pstats.Stats(profile,stream=stream).strip_dirs().sort_stats('cumulative').print_stats(30)
        record=dict(scenario=cfg,source_sha256=source_hashes(),profile_steps=a.steps,warmup_steps=10,
            observer=False,warning='Instrumented short initial segment; JIT may still occur; not steady-state throughput or GPU speedup')
        (out/(name+'.json')).write_text(json.dumps(record,indent=2),encoding='utf-8')
        pstats.Stats(profile).strip_dirs().sort_stats('cumulative').print_stats(12)
    print(str(out))
