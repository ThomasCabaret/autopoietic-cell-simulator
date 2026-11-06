"""Passive final-checkpoint endpoint geometry; no claim about prior encounters."""
import hashlib,json,sys,shutil
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import numpy as np
from simulator.checkpoint import load
from simulator.docking import port_geometry,free_faces
from simulator.observations import components
from simulator.campaign_io import read,write


def geometry(pos,links,config):
    n=len(pos)//2;heads,tails,_,_=port_geometry(pos,n,1.,config['short_length'])
    free=free_faces(n,links);parts=list(components(n,{(a,b) for a,b,_,_ in links}));rows=[]
    for comp,order,cycle in parts:
        if cycle:continue
        ends=[(i,a) for i in comp for a in range(2) if free[i,a]]
        candidates=[]
        for i,a in ends:
            for j,b in ends:
                if i>=j or a==b:continue
                q=float(np.sum((heads[j,b]-heads[i,a])**2)+np.sum((tails[j,b]-tails[i,a])**2))
                candidates.append(dict(units=[i,j],faces=[a,b],port_mismatch=q**.5,
                    eligible_geometry=q<config['dock_capture']**2,
                    head_distance=float(np.linalg.norm(pos[j]-pos[i]))))
        rows.append(dict(size=len(comp),free_faces=len(ends),closure_candidates=candidates))
    return sorted(rows,key=lambda x:-x['size'])


def main():
    descriptor=ROOT/'research/BATCH_50_CH1_RECIPES.json';job=Path(read(descriptor)['job']);cfg=read(job/'job.json')
    folder=Path(cfg['campaigns'][0]);manifest=read(folder/'manifest.json');rows=[]
    for task in manifest['tasks']:
        if '_assembly_' not in task['label']:continue
        state=read(folder/'tasks'/task['id']/'state.json')
        if state['status']!='complete':raise ValueError('Require final completed checkpoints')
        checkpoint=folder/state['checkpoint'];sim,_=load(checkpoint);c=sim.chemistry;_,ids,links=c.lipids.layout()
        rows.append(dict(label=task['label'],checkpoint_sha256=hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
            dock_capture=c.config['dock_capture'],short_length=c.config['short_length'],
            chains=geometry(c.pos[ids],links,c.config)))
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');out=ROOT/'outputs/diagnostics'/('CE1_'+stamp)
    recipe=ROOT/'research/diagnostic_recipes'/('CE1_'+stamp);out.mkdir(parents=True);recipe.mkdir(parents=True)
    for src in [Path(__file__)]+list((ROOT/'simulator').glob('*.py')):
        dest=recipe/src.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
    result=dict(rows=rows,scope='Selected final geometry only, no encounter history, rate or absence of earlier transient closure inferred.')
    write(out/'report.json',result)
    provenance=dict(job_sha256=hashlib.sha256((job/'job.json').read_bytes()).hexdigest(),
        sources={p.relative_to(recipe).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in recipe.rglob('*.py')},
        result_sha256=hashlib.sha256((out/'report.json').read_bytes()).hexdigest())
    write(recipe/'recipe.json',provenance)
    write(ROOT/'research/BATCH_50_CE1.json',dict(output=str(out),recipe=recipe.relative_to(ROOT).as_posix(),summary=result,**provenance))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
