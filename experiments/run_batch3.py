"""Pinned exploratory cases; raw data stays local, source-only recipes are retained."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from simulator.config import resolve
from simulator.runner import run
from scripts.reconstruct_experiment import export_recipe

CASES={
    'V8':dict(face_docking=True,initial='dispersed_units',units=24,short_length=.75,
              box=[10.,10.],temperature=.08,dock_energy=4.,dock_width=.3,
              bond_off_rate=.02,break_extension=.35),
    'V8irreversible':dict(bond_off_rate=0.,break_extension=10.),
    'V8equal':dict(short_length=1.),
    'V8weak':dict(dock_energy=1.),
    'V8broad':dict(dock_width=.5,dock_capture=.35),
    'V8cold':dict(temperature=.03),
    'V8dense':dict(units=36),
    'V8nolinks':dict(bonding=False),
    'V8curved':dict(units=36,short_length=.65),
    'V8warm':dict(units=36,temperature=.2),
    'V8equalDense':dict(units=36,short_length=1.),
    'V8curvedNoAttract':dict(units=36,short_length=.65,dock_energy=0.),
    'V8curvedNoThermal':dict(units=36,short_length=.65,bond_off_rate=0.),
    'C1':dict(sequence='001'),
    'C1open':dict(sequence='011'),
    'C1loose':dict(assembled=False),
    'C1bare':dict(ligand_energy=0.,binding_rate=0.),
    'C1scrambled':dict(sequence='010'),
}


def scenario(case,seed,duration,overrides=None):
    if case.startswith('C1'):
        return resolve(dict(schema_version=1,model='catalysis',name=case,branch='C1',
                            seed=seed,duration=duration,chemistry={**CASES[case],**(overrides or {})},
                            engine=dict(sample_every=250)))
    chemistry={**CASES['V8'],**CASES[case],**(overrides or {})}
    return resolve(dict(schema_version=1,model='membrane',name=case,branch='V8',
                        seed=seed,duration=duration,chemistry=chemistry,
                        engine=dict(sample_every=500)))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('case',choices=CASES)
    p.add_argument('--seed',type=int,default=0)
    p.add_argument('--duration',type=float,default=300.)
    p.add_argument('--overrides',type=Path)
    args=p.parse_args()
    overrides=json.loads(args.overrides.read_text(encoding='utf-8')) if args.overrides else None
    evidence,path=run(scenario(args.case,args.seed,args.duration,overrides),parent=ROOT/'research/engine_runs')
    export_recipe(path)
    if evidence['error']: raise SystemExit(1)
