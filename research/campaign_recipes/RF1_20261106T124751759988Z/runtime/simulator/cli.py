"""The same scenario and engine power live rendering and headless experiments."""
import argparse
from pathlib import Path
import time
from .config import load
from .runner import run,replay


def main():
    p=argparse.ArgumentParser(description='Local chemistry simulator: one engine, optional viewer')
    p.add_argument('--config',type=Path)
    p.add_argument('--gui',action='store_true')
    p.add_argument('--seed',type=int)
    p.add_argument('--duration',type=float)
    p.add_argument('--spatial',choices=['tree','brute'])
    p.add_argument('--output',type=Path,default=Path('outputs'))
    p.add_argument('--no-trajectory',action='store_true')
    p.add_argument('--resume',type=Path)
    p.add_argument('--replay',type=Path)
    p.add_argument('--replay-view',type=Path)
    p.add_argument('--screenshot',type=Path,help=argparse.SUPPRESS)
    args=p.parse_args()
    if args.replay:
        replay(args.replay)
        return
    if args.replay_view:
        from .viewer import replay_view
        replay_view(args.replay_view,args.screenshot)
        return
    if not args.config and not args.resume:
        p.error('provide --config or --resume')
    config=load(args.config) if args.config else None
    if args.resume and any(v is not None for v in (args.seed,args.duration,args.spatial)):
        p.error('resume preserves its complete configuration; overrides are not accepted')
    if config:
        if args.seed is not None: config['seed']=args.seed
        if args.duration is not None: config['duration']=args.duration
        if args.spatial is not None: config['engine']['spatial']=args.spatial
    if args.gui:
        from .viewer import live_view
        live_view(config,args.output,not args.no_trajectory,args.resume)
    else:
        last=[0.]
        def progress(sim):
            if time.monotonic()-last[0]>5:
                print(f't={sim.time:.2f}/{sim.config["duration"]} ({sim.step_index}/{sim.target_step})',flush=True)
                last[0]=time.monotonic()
        evidence,_=run(config,args.output,not args.no_trajectory,args.resume,progress)
        if evidence['error'] or not all(evidence['expected_checks'].values()):
            raise SystemExit(1)
