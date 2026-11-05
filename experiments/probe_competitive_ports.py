"""CP1 selected static contact comparison on the two paused CF1 snapshots."""
import json,sys,shutil
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from statistics import median
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write
from scripts.campaign import digest,validate
from simulator import checkpoint
from simulator.spatial import Neighborhood
from simulator.docking import port_geometry,free_faces,bound_port_force
from simulator.exchange_energy import port_delta
from simulator.mixed_boundary import segment_energy_delta
from simulator.transition_energy import thermal_factor
from experiments.competitive_port_potential import competitive_force,competitive_terms


def main():
    job=Path(read(ROOT/'research/BATCH_49_CF1_RECIPES.json')['job']);folder=Path(read(job/'job.json')['campaigns'][0]);manifest=validate(folder)
    if read(job/'state.json')['phase']!='paused':raise ValueError('Pause and checkpoint before static analysis')
    out=ROOT/'outputs/diagnostics'/('CP1_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    rows=[];inputs=[]
    for task in manifest['tasks'][:2]:
        state=read(folder/'tasks'/task['id']/'state.json');path=folder/state['checkpoint'];sim,_=checkpoint.load(path);c=sim.chemistry
        heads,ids,links=c.lipids.layout();pos=c.pos[ids];n=len(heads);cfg=c.config;free=free_faces(n,links)
        pairs=Neighborhood('brute',0.).pairs(pos[:n],1+4*cfg['dock_width'],'CP1');head,tail,_,_=port_geometry(pos,n,1.,cfg['short_length'])
        partners=np.full((n,2),-1,dtype=np.int64)
        for i,j,a,b in links:partners[i,a]=j;partners[j,b]=i
        candidates=[]
        for i,j in pairs:
            if any({int(i),int(j)}==set(edge[:2]) for edge in links):continue
            for a in range(2):
                b=1-a
                if free[i,a] and free[j,b]:
                    q=float(np.sum((head[j,b]-head[i,a])**2)+np.sum((tail[j,b]-tail[i,a])**2))
                    if q<cfg['dock_capture']**2:candidates.append((q,int(i),int(j),a,b))
        energy=competitive_force(pos,pairs,free,1.,cfg['short_length'],cfg['dock_energy'],cfg['dock_width'],partners)[1]
        load=competitive_terms(pos,pairs,free,1.,cfg['short_length'],cfg['dock_energy'],cfg['dock_width'],partners)[2]
        selected=[]
        for q,i,j,a,b in sorted(candidates)[:12]:
            edge=(i,j,a,b);new_partners=partners.copy();new_partners[i,a]=j;new_partners[j,b]=i
            newfree=free_faces(n,links+[edge])
            new=competitive_force(pos,pairs,newfree,1.,cfg['short_length'],cfg['dock_energy'],cfg['dock_width'],new_partners)[1]
            bound=bound_port_force(pos,np.asarray([edge]),1.,cfg['short_length'],cfg['dock_energy'],cfg['dock_width'])[1]
            barrier=segment_energy_delta(c,None,(heads[i],heads[j]),Neighborhood('brute',0.))
            olddelta=port_delta(pos,links,None,edge,cfg,Neighborhood('brute',0.))+barrier
            newdelta=new-energy+bound+barrier
            selected.append(dict(heads=[heads[i],heads[j]],faces=[a,b],mismatch=q,
                additive_delta=olddelta,competitive_delta=newdelta,
                additive_factor=thermal_factor(olddelta,cfg['temperature']),competitive_factor=thermal_factor(newdelta,cfg['temperature'])))
        rows.append(dict(label=task['label'],time=sim.time,L=n,links=len(links),eligible_contacts=len(candidates),
            max_competitive_face_load=float(load.max()),selected=selected))
        inputs.append(dict(task=task['id'],checkpoint_sha256=digest(path),step=sim.step_index,time=sim.time))
    report=dict(rows=rows,inputs=inputs,manifest_sha256=digest(folder/'manifest.json'),
        scope='Top12 geometric contacts per paused snapshot, same contacts for both static models. '
            'Competitive law not installed in simulator, no movement, rates or success declared.')
    write(out/'report.json',report)
    recipe=ROOT/'research/diagnostic_recipes'/out.name;recipe.mkdir(parents=True)
    for name in ('probe_competitive_ports.py','competitive_port_potential.py'):shutil.copyfile(ROOT/'experiments'/name,recipe/name)
    write(recipe/'recipe.json',dict(campaign=str(folder),inputs=inputs,manifest_sha256=digest(folder/'manifest.json'),selection='12 smallest eligible mismatch per first2 paused cases'))
    summary=[]
    for row in rows:
        summary.append({**{k:row[k] for k in ('label','time','L','links','eligible_contacts','max_competitive_face_load')},
            'selected_count':len(row['selected']),
            'median_additive_delta':median(q['additive_delta'] for q in row['selected']),
            'median_competitive_delta':median(q['competitive_delta'] for q in row['selected']),
            'competitive_nonpositive':sum(q['competitive_delta']<=0 for q in row['selected'])})
    write(ROOT/'research/BATCH_49_CP1.json',dict(output=str(out),recipe=recipe.relative_to(ROOT).as_posix(),
        report_sha256=digest(out/'report.json'),summary=summary,scope=report['scope']))
    for row in rows:
        print(row['label'],row['eligible_contacts'],row['max_competitive_face_load'],
            [(round(q['additive_delta'],4),round(q['competitive_delta'],4)) for q in row['selected'][:4]])
    return out


if __name__=='__main__':main()
