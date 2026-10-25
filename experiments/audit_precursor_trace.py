"""Read-only local tracing on exact archived laws; never feeds analysis to physics."""
import argparse,hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]


def main(folder,output=None):
    folder=folder.resolve();saved=json.loads((folder/'result.json').read_text(encoding='utf-8'))
    out=output.resolve() if output else ROOT/'outputs/batch8_trace'/(folder.name+'_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    if out.exists():raise FileExistsError('Choose a new trace output directory: '+str(out))
    for name,digest in saved['source_sha256'].items():
        assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest
    sys.path.insert(0,str(folder))
    from simulator.engine import Simulation
    from simulator.runner import make_observer
    sim=Simulation(saved['scenario']);obs=make_observer(sim.config);sim.listeners.append(obs)
    c=sim.chemistry;assembly=c.assembly;cat=assembly.catalyst
    original_react=assembly.react;original_release=cat.release
    released=[];verified=[]

    def release(atom):
        s=int(cat.atom_bound[atom])
        released.append(dict(atom=int(atom),site=s,time=sim.time,
            reciprocal=bool(s>=0 and cat.site_bound[s]==atom),
            genetic_pair=int(c.pairing[s]) if s>=0 else None))
        return original_release(atom)

    def react(chem,time,dt,neighbors):
        released.clear();before=chem.rungs.copy();used=set(before[before[:,1]>=0,1].tolist())
        old=len(assembly.events);result=original_react(chem,time,dt,neighbors)
        for event in assembly.events[old:]:
            p,r=event['support'],event['recognizer']
            assert before[p,1]==-1 and r not in used
            assert chem.rungs[p,1]==r and chem.bits[p]==assembly.atom_bits[r-chem.n]
            distance=float(np.linalg.norm(chem.pos[p]-chem.pos[r]))
            assert distance<chem.config['rung_capture_radius']
            if event['catalyzed']:
                a,b=event['catalytic_support']
                assert tuple(sorted((a,b))) in chem.edges
                assert chem.families[a]==chem.families[b]==1
                assert chem.bits[a]==0 and chem.bits[b]==1
                for atom,site in ((p,a),(r,b)):
                    matches=[e for e in released if e['atom']==atom and e['site']==site]
                    assert matches and matches[-1]['reciprocal'] and matches[-1]['genetic_pair']==-1
                assert cat.atom_bound[p]==cat.atom_bound[r]==-1
            verified.append(dict(event,distance=distance))
            used.add(r);before[p,1]=r
        return result

    cat.release=release;assembly.react=react
    while not sim.done:sim.advance(1000)
    assert json.loads(json.dumps(obs.summary()))==saved['metrics']
    with np.load(folder/'trajectory.npz') as data:
        np.testing.assert_array_equal(np.array(obs.frames),data['positions'])
        np.testing.assert_array_equal(np.array(obs.rungs_frames),data['rungs'])
    out.mkdir(parents=True,exist_ok=False)
    result=dict(recipe=(folder/'recipe.json').as_posix(),verified_reactions=verified,
        tracer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        all_metrics_and_positions_exact=True)
    (out/'audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(dict(run=folder.name,local_reactions_verified=len(verified),
        catalytic=sum(e['catalyzed'] for e in verified),all_metrics_and_positions_exact=True)))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args();main(args.folder,args.output)
