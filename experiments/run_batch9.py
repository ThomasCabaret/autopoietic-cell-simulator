"""Large prepared membrane, spontaneous local exchange and diagnostic probes."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve
from simulator.runner import run
from scripts.reconstruct_experiment import export_recipe

CASES={
    'M1A':{},'M1transparent':dict(barrier_radius=0.),
    'M1oldCurve':dict(short_length=.65),'M1flat':dict(short_length=1.),
    'M1noOff':dict(bond_off_rate=0.),'M1noAttract':dict(dock_energy=0.),
    'M1noFree':dict(units=219),'M1outside':dict(free_lipid_start='outside_annulus'),
    'M1bulk':dict(free_lipid_start='inside_bulk')
}
CASES.update(M1exchange=dict(contact_exchange_rate=.2),
    M1exchangeOutside=dict(contact_exchange_rate=.2,free_lipid_start='outside_annulus'),
    M1exchangeTransparent=dict(contact_exchange_rate=.2,barrier_radius=0.),
    M1noBondBarrier=dict(barrier_stiffness=0.),M1slowHeal=dict(dock_rate=1.))


def scenario(case,seed=0,duration=150.,overrides=None):
    if case not in CASES:raise ValueError('Unknown membrane batch9 case')
    return resolve(dict(schema_version=1,model='membrane_bath',name=case,branch='M1A',seed=seed,
        duration=duration,engine=dict(dt=.002,sample_every=250),chemistry={**CASES[case],**(overrides or {})}))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('case',choices=CASES)
    p.add_argument('--seed',type=int,default=0);p.add_argument('--duration',type=float,default=150.)
    p.add_argument('--overrides',type=Path)
    a=p.parse_args();change=json.loads(a.overrides.read_text()) if a.overrides else None
    r,path=run(scenario(a.case,a.seed,a.duration,change),ROOT/'research/engine_runs');export_recipe(path)
    if r['error']:raise SystemExit(1)
