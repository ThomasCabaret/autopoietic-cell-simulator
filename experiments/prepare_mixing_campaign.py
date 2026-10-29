"""Frozen mechanics-only mixing experiments; no chemistry or altered integrator."""
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))


def scenario(temperature=.08,seed=0,steric=True,size=2,duration=None,fine=False):
    return dict(schema_version=1,model='mixing',branch='MIX1',seed=seed,
        name=f'MIX1_T{temperature:g}_'+('cores' if steric else 'ideal')+f'_b{size}'+('_fine' if fine else ''),
        duration=duration if duration is not None else (12000. if temperature==.08 else 1600.),
        engine=dict(dt=.005,spatial='tree',skin=.25,sample_every=5 if fine else 10,reaction_every=5),
        chemistry=dict(molecules=200,beads_per_molecule=size,steric=steric,
            temperature=temperature,box=[24.,18.],initial_half=True,
            record_interval=10.,contact_interval=.025 if fine else .05))


def plan(pilot=False):
    tasks=[scenario(T,seed,duration=20. if pilot else None) for T in (.08,.6) for seed in (range(1) if pilot else range(3))]
    if not pilot:
        tasks += [scenario(.08,steric=False),scenario(.6,steric=False),
            scenario(.08,steric=False,size=1,duration=6000.),scenario(.6,fine=True,duration=400.)]
    return dict(name='MIX1 mixing pilot' if pilot else 'MIX1 mechanics-only dispersion and neighbor turnover',
        workers=1,checkpoint_seconds=30.,kinetic_window=50.,record_trajectory=False,mixing_report=True,
        comparison_policy='One shared Brownian engine, 200 fixed molecules initially in left half. No chemistry/affinity/flow/inertia. Warm and cold baths separate. Steric ablations and ideal single-bead controls explicit. Warm fine-contact run is a selected measurement-cadence control, not another physical replicate. Fixed horizons; no result-dependent continuation.',
        tasks=[dict(scenario=s) for s in tasks])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--pilot',action='store_true')
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(plan(a.pilot),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
