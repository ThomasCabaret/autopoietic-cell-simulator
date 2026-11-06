"""CBEN1 warmed force/delta microcost on preserved crowded CF1 snapshots."""
import json,time,hashlib,shutil,sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.spatial import Neighborhood
from simulator.docking import docking_force,free_faces
from simulator.competitive_ports import competitive_force,partners
from simulator.exchange_energy import port_delta
from simulator.campaign_io import read,write


def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def timing(fn,number):
    fn();times=[]
    for _ in range(3):
        start=time.perf_counter()
        for _ in range(number):fn()
        times.append((time.perf_counter()-start)/number)
    return float(np.median(times))


def benchmark():
    source=read(ROOT/'research/BATCH_49_CP1.json');old=read(Path(source['output'])/'report.json')
    if digest(Path(source['output'])/'report.json')!=source['report_sha256']:raise ValueError('CP1 evidence changed')
    job=Path(read(ROOT/'research/BATCH_49_CF1_RECIPES.json')['job']);folder=Path(read(job/'job.json')['campaigns'][0])
    if read(job/'state.json')['phase']!='paused':raise ValueError('CF1 must stay paused during the snapshot benchmark')
    manifest=read(folder/'manifest.json');rows=[]
    for item,input_hash in zip(old['rows'],old['inputs']):
        task=next(t for t in manifest['tasks'] if t['label']==item['label']);state=read(folder/'tasks'/task['id']/'state.json');path=folder/state['checkpoint']
        if digest(path)!=input_hash['checkpoint_sha256']:raise ValueError('Paused snapshot changed')
        with np.load(path,allow_pickle=False) as z:meta=json.loads(str(z['metadata']));positions=z['positions'].copy()
        lipids=meta['chemistry']['lipids'];rungs=dict(lipids['rungs']);heads=sorted(rungs);lookup={h:i for i,h in enumerate(heads)}
        pos=positions[heads+[rungs[h] for h in heads]];links=[(lookup[a],lookup[b],x,y) for a,b,x,y in lipids['links']]
        cfg=dict(meta['config']['chemistry']);n=len(heads);free=free_faces(n,links);bound=partners(n,links)
        pairs=Neighborhood('tree',.25).pairs(pos[:n],1+4*cfg['dock_width']);args=(pos,pairs,free,1.,cfg['short_length'],cfg['dock_energy'],cfg['dock_width'],bound)
        oldforce=timing(lambda:docking_force(*args),100);newforce=timing(lambda:competitive_force(*args),100)
        selected=item['selected'][:12];costs=[]
        for selected_contact in selected:
            a,b=selected_contact['heads'];x,y=selected_contact['faces'];edge=(lookup[a],lookup[b],x,y);near=Neighborhood('tree',.25)
            cfg['free_port_potential']='additive';oldcfg=cfg.copy()
            cfg['free_port_potential']='competitive';newcfg=cfg.copy()
            a=timing(lambda:port_delta(pos,links,None,edge,oldcfg,near),10)
            b=timing(lambda:port_delta(pos,links,None,edge,newcfg,near),10);costs.append((a,b))
        olddelta=float(np.median([x[0] for x in costs]));newdelta=float(np.median([x[1] for x in costs]))
        rows.append(dict(label=item['label'],L=n,pairs=len(pairs),force_seconds_additive=oldforce,force_seconds_competitive=newforce,
            force_ratio=newforce/oldforce,delta_seconds_additive=olddelta,delta_seconds_competitive=newdelta,delta_ratio=newdelta/olddelta,
            checkpoint_sha256=digest(path)))
    report=dict(rows=rows,screen_passed=all(r['force_ratio']<=5 and r['delta_ratio']<=5 for r in rows),
        scope='Warmed selected snapshot microcost, median3 repeats. Force100 calls, delta10 per selected contact. No full runtime/mixing or machine-independent speed guarantee.')
    out=ROOT/'outputs/diagnostics'/('CBEN1_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    write(out/'report.json',report)
    recipe=ROOT/'research/diagnostic_recipes'/out.name;recipe.mkdir(parents=True);shutil.copyfile(Path(__file__),recipe/Path(__file__).name)
    write(recipe/'recipe.json',dict(CP1_descriptor='research/BATCH_49_CP1.json',inputs=old['inputs'],source_sha256=digest(Path(__file__))))
    write(ROOT/'research/BATCH_50_COST.json',dict(output=str(out),recipe=recipe.relative_to(ROOT).as_posix(),report_sha256=digest(out/'report.json'),summary=report))
    return report


if __name__=='__main__':print(json.dumps(benchmark(),indent=2))
