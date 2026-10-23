"""Compatibility research launcher using the shared simulator and source archive."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from simulator.observations import CopyObserver,VesicleObserver,components,simple_polygon,area
from simulator.plots import plot_run
from simulator.config import legacy
from simulator.runner import run as run_scenario


def run(case,seed,duration=None,overrides=None):
    cases=json.loads((ROOT/'research/cases.json').read_text(encoding='utf-8'))
    config={**cases[case],**(overrides or {}),'case':case,'seed':seed}
    if duration is not None: config['duration']=duration
    return run_scenario(legacy(config),parent=ROOT/'research/runs')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('case')
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--duration',type=float)
    parser.add_argument('--overrides',type=Path)
    args=parser.parse_args()
    evidence,_=run(args.case,args.seed,args.duration,
        json.loads(args.overrides.read_text(encoding='utf-8')) if args.overrides else None)
    if evidence['error']: raise SystemExit(1)
