"""Measure full shared-engine steps on synthetic cell-sized chemical workloads.

Prepared repeated sequences exercise existing laws; they are NOT three working
synthases, a viable cell or a renewal experiment. No chemistry parameter is
tuned for speed. Raw timing reports and frozen sources remain under outputs.
"""
import argparse,hashlib,json,platform,shutil,sys,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.checkpoint import source_hashes
from experiments.run_batch13 import scenario as previous

SIZES={'small':(1020,126,12,20.,12,3,6),
       'nominal':(2406,219,24,34.5,24,6,12),
       'larger':(6292,458,48,72.5,48,9,24)}


def scenario(case,steps):
    cfg=previous('bath',0,.002*steps)
    cfg['name']='workload_'+case;cfg['branch']='PERF_cell_synthetic'
    if case=='current':return cfg
    total,ring,free,radius,length,genes,tools=SIZES[case]
    lipid=ring+free;units=(total-2*lipid)//2
    assert 2*(lipid+units)==total
    seq=('001011'*((length+5)//6))[:length]
    g=cfg['chemistry']['genetics']
    # Include prepared long chains and free precursors. The larger square
    # keeps initialization feasible; some content lies outside the ring.
    # This is a CPU workload, not a packed-cell geometric success.
    size=1.8*radius
    g.update(sequence=seq,free_units=(units-length)//3,
        function_units=units-length-(units-length)//3,box=[size,size],
        initial_assemblies=[dict(family=0,sequence=seq,backbone=True) for _ in range(genes-1)]+
                           [dict(family=1,sequence=seq,backbone=True) for _ in range(tools)])
    cfg['chemistry']['membrane'].update(units=lipid,ring_units=ring,ring_radius=radius,
                                      box=[2*(radius+10)]*2)
    cfg['chemistry']['packet_offset']=[0.,0.]
    return cfg


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cases',nargs='+',choices=['current',*SIZES],default=['current',*SIZES])
    p.add_argument('--warmup',type=int,default=50);p.add_argument('--steps',type=int,default=250)
    p.add_argument('--blocks',type=int,default=3);a=p.parse_args()
    if min(a.warmup,a.steps,a.blocks)<1:p.error('positive counts required')
    out=ROOT/'outputs/performance'/('cell_workload_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    out.mkdir(parents=True);hashes=source_hashes()
    for name,digest in hashes.items():
        target=out/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
    shutil.copyfile(__file__,out/'benchmark_cell_workload.py')
    report=dict(scope='Full chemistry/forces/integration/observation on synthetic initial workloads; no renderer, disk checkpoints, sustained dynamics, optimal feeding or measured cell renewal. Short warm timings, not a scaling theorem.',
        python=sys.version,platform=platform.platform(),source_sha256=hashes,
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        settings=vars(a),rows=[])
    for case in a.cases:
        cfg=scenario(case,a.warmup+a.steps*a.blocks)
        start=time.perf_counter();sim=Simulation(cfg);init=time.perf_counter()-start
        obs=make_observer(sim.config,False);sim.listeners.append(obs)
        start=time.perf_counter();sim.advance(a.warmup);warm=time.perf_counter()-start
        blocks=[]
        for _ in range(a.blocks):
            start=time.perf_counter();sim.advance(a.steps);blocks.append(time.perf_counter()-start)
        median=float(np.median(blocks));rate=a.steps/median
        row=dict(case=case,particles=len(sim.chemistry.pos),scenario=sim.config,
                 initialization_seconds=init,warmup_seconds=warm,block_seconds=blocks,
                 median_steps_per_wall_second=rate,simulated_units_per_wall_second=rate*sim.dt,
                 wall_minutes_per_1000_simulated=1000/(rate*sim.dt)/60)
        report['rows'].append(row)
        (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
        print(json.dumps({k:v for k,v in row.items() if k!='scenario'}),flush=True)
    print(str(out),flush=True)


if __name__=='__main__':main()
