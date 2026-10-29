"""Bounded comparison of physical mixing yield per second of computation."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_mixing_campaign import scenario as base


def scenario(kind='brownian',damping=4.,seed=0,dt=.005,T=.08,duration=None):
    cfg=base(T,seed,duration=duration if duration is not None else
        (12000. if kind=='brownian' or (kind=='langevin' and damping==4.) else 1600.))
    cfg.update(name=f'MIX2_{kind}_g{damping:g}_dt{dt:g}_T{T:g}',branch='MIX2')
    cfg['engine'].update(dt=dt,sample_every=round(.05/dt))
    cfg['chemistry'].update(motion=kind,damping=damping,mass=1.,dpd_cutoff=1.,
        initial_clearance=True,record_interval=2.5)
    return cfg


def plan(pilot=False):
    if pilot:
        tasks=[scenario(kind,g,duration=100.) for kind,g in
            (('brownian',4.),('langevin',4.),('langevin',.1),('dpd',.5),('dpd',2.))]
        tasks += [scenario(kind,g,dt=.01,duration=100.) for kind,g in (('langevin',.1),('dpd',.5))]
    else:
        tasks=[scenario(kind,g,seed) for seed in range(3) for kind,g in
            (('brownian',4.),('langevin',.1),('dpd',.5))]
        tasks += [scenario('langevin',4.)]+[scenario('dpd',2.,seed) for seed in range(3)]
        tasks += [scenario(kind,g,dt=.01) for kind,g in (('langevin',.1),('dpd',.5))]
        tasks += [scenario(kind,g,T=.6,duration=1600.) for kind,g in (('brownian',4.),('langevin',.1),('dpd',.5))]
    return dict(name='MIX2 motion comparison pilot' if pilot else 'MIX2 mixing per real compute second',
        workers=2,checkpoint_seconds=30.,kinetic_window=50.,record_trajectory=False,motion_report=True,
        comparison_policy='Frozen local mechanics variants; not chemistry integration. Same collision-free initial positions for each seed; same Maxwell initial velocities between inertial cases. Original MIX1 retained, matched Brownian baselines rerun. Cold baseline/matched-drag control12000, fast branches1600; no-event times censored, unequal horizons explicit. Contacts0.05 and statistics2.5 for all. Wall-clock brackets from actual250-step chunks including observers; also exclude first2.5 simulated time as declared warmup. Two workers; machine contention remains a limitation.',
        tasks=[dict(scenario=s) for s in tasks])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--pilot',action='store_true');p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(plan(a.pilot),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
