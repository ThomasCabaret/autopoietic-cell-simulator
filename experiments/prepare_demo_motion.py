"""Bounded paired transfer of Langevin to the existing live demos, with fixed-dt controls."""
import argparse
import copy
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_demo_catalog import origins,langevin_variant
from simulator.config import resolve


def task(key,cfg,motion='langevin',fine=False,duration=None):
    cfg=langevin_variant(cfg) if motion=='langevin' else resolve(cfg)
    if fine:
        cfg['engine']['dt']/=2
        cfg['engine']['reaction_every']*=2
        cfg['engine']['sample_every']*=2
    if duration is not None:cfg['duration']=duration
    cfg['name']=f'LT2_{key}_{motion}'+('_fine' if fine else '')
    cfg['branch']='LT2'
    return dict(scenario=cfg,preset=key,comparison='fine' if fine else 'base')


def plan(pilot=False):
    entries={row[0]:row[3] for row in origins()};tasks=[]
    if pilot:
        tasks=[task(key,entries[key],duration=5.) for key in ('free_membrane','integrated_s2')]
    else:
        micros=('binary_copy','material_cycle','free_membrane')
        for key in micros:
            tasks.extend(task(key,entries[key],m) for m in ('brownian','langevin'))
        tasks.extend(task(key,entries[key],fine=True) for key in micros)
        for key in ('integrated_s2','integrated_s0','integrated_s1'):
            tasks.extend(task(key,entries[key],m) for m in ('brownian','langevin'))
            if key=='integrated_s2':tasks.append(task(key,entries[key],fine=True))
    return dict(name='LT2 pilots' if pilot else 'LT2 paired demos and selected timestep controls',workers=2,
        checkpoint_seconds=30.,kinetic_window=50.,record_trajectory=False,demo_motion_report=True,
        comparison_policy='Same initial materials, geometry, chemical laws, temperature, duration and reaction interval within each pair. Only Langevin gamma0.1,m1 differs. Fine controls halve dt while preserving reaction and observation intervals. Existing illustrative seeds, no robustness claim from single-seed microdemos. No extra tool or gene; integrated membrane prepared, V8 molecules initially isolated.',tasks=tasks)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--pilot',action='store_true');p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(plan(a.pilot),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
