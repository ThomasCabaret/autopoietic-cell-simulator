"""One bounded, passive first-incompatible-capture microscope under MX1 sources.

Question: do nominal unbindings actually free a trapped mixed F pair, or does
the same atom immediately rebind? Target first crossed material pair,20 units
of release events, <=500 local frames, fixed40-unit replay and plain control.
"""
import json,sys,copy
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
RECIPE=ROOT/'research/campaign_recipes/MX1_20261104T192816403023Z'
sys.path.insert(0,str(RECIPE/'runtime'))
from simulator.engine import Simulation
from simulator.checkpoint import source_hashes


def main():
    manifest=json.loads((RECIPE/'manifest.json').read_text(encoding='utf-8'))
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    if source_hashes()!=hashes:raise ValueError('Use exact MX1 recipe sources')
    cfg=next(t['scenario'] for t in manifest['tasks'] if t['label']=='MX1_mixed_s0')
    sim=Simulation(cfg);plain=Simulation(cfg);c=sim.chemistry;cap=c.capture
    target=None;events=[];frames=[];phase=None;now=0.;next_frame=0.
    original_release=cap.release;original_react=cap.react;released=[]
    def release(atom):
        site=int(cap.atom_bound[atom]);original_release(atom)
        if target and phase=='capture' and site in target['sites'] and now<=target['time']+20.:
            released.append(dict(time=now,site=site,atom=int(atom),kind='unbinding'))
    def react(world,dt,neighbors):
        nonlocal target,phase,next_frame
        released.clear();phase='capture';original_react(world,dt,neighbors);phase=None
        if target is None:
            for i,j in sorted(c.edges):
                a,b=int(cap.site_bound[i]),int(cap.site_bound[j])
                if a>=0 and b>=0 and ((a<c.prefix)!=(b<c.prefix)):
                    target=dict(time=now,sites=[i,j],atoms=[a,b],local_ids=sorted(set(map(int,c.rungs[[i,j]].ravel()))|{a,b}))
                    next_frame=now;break
        if target and now<=target['time']+20.:
            for e in released:
                e['same_atom_rebound_within_tick']=bool(cap.site_bound[e['site']]==e['atom'])
                events.append(e)
            if now>=next_frame-1e-8 and len(frames)<500:
                ids=target['local_ids'];frames.append(dict(time=now,bound=[int(cap.site_bound[s]) for s in target['sites']],
                    ids=ids,positions=c.pos[ids].tolist()))
                next_frame+=.05
    cap.release=release;cap.react=react
    # Time is only read by this microscope, never injected into the chemistry.
    original_world_react=c.react
    def observed(time,dt,neighbors):
        nonlocal now
        now=float(time);return original_world_react(time,dt,neighbors)
    c.react=observed
    sim.advance(round(40./sim.dt));plain.advance(round(40./plain.dt))
    np.testing.assert_array_equal(c.pos,plain.chemistry.pos)
    np.testing.assert_array_equal(sim.motion.velocities,plain.motion.velocities)
    if c.export()!=plain.chemistry.export() or sim.rng.bit_generator.state!=plain.rng.bit_generator.state:raise ValueError('Microscope changed chemistry/RNG')
    if target is None or target['time']+20.>40.:raise ValueError('Target absent or incomplete within frozen40-unit horizon')
    report=dict(target=target,events=events,frames=frames,unbindings=len(events),
        same_atom_immediate_rebindings=sum(e['same_atom_rebound_within_tick'] for e in events),
        source_sha256=hashes,physical_control_exact=True,control_horizon=40.,
        scope='One selected early crossed pair,20-unit window, <=6 fixed atom IDs and500 frames. '
            'Release events logged inside capture only, product releases excluded. Immediate rebinding is observed, '
            'not inferred from coarse unchanged occupancies. No population-frequency estimate or permanent trapping claim.')
    out=ROOT/'outputs/diagnostics'/('MX1_capture_loupe_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (ROOT/'outputs/diagnostics/latest_mixed_capture_loupe.txt').write_text(str(out.resolve()))
    print(json.dumps({k:v for k,v in report.items() if k not in ('events','frames','source_sha256')}));print(out)


if __name__=='__main__':main()
