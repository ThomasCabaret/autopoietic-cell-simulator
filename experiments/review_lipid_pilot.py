"""Passive L1 pilot audit: actual atoms, output bonds, references and heat debt."""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write


def review():
    folder=Path((ROOT/'outputs/lipid_pilots/latest.txt').read_text().strip());m=validate(folder);s=status(folder)
    if s['controller_active'] or s['counts']['complete']!=1:raise ValueError('Require complete inactive single pilot')
    task=m['tasks'][0];state=s['tasks'][0];path=folder/state['result'];r=read(path)
    hashes={k:v for k,v in m['source_sha256'].items() if k.startswith('simulator/')}
    if r['source_sha256']!=hashes or r['scenario']!=task['scenario'] or not r['completed'] or r['error']:
        raise ValueError('Pilot source/completion mismatch')
    cfg=r['scenario']['chemistry'];prefix=4*cfg['tool_count'];count=cfg['food_units']
    with np.load(folder/state['checkpoint'],allow_pickle=False) as data:
        meta=json.loads(str(data['metadata']));pos=data['positions'].copy()
    if meta['source_sha256']!=hashes or meta['config']!=task['scenario']:raise ValueError('Checkpoint mismatch')
    born=r['metrics']['births'];rungs=dict(meta['chemistry']['lipids']['rungs']);heads=set();tails=set()
    for e in born:
        h,t=e['head'],e['tail']
        if not prefix<=h<prefix+count or not prefix+count<=t<prefix+2*count or h in heads or t in tails or rungs[h]!=t:
            raise ValueError('Invalid or repeated H/T product identity')
        if e['catalyzed'] and (tuple(sorted(e['sites'])) not in {tuple(x) for x in meta['chemistry']['host']['edges']}):
            raise ValueError('Catalyst sites not locally linked')
        heads.add(h);tails.add(t)
    if len(rungs)!=len(born) or len(pos)!=prefix+2*count:raise ValueError('Material conservation failure')
    thermal=read(folder/state['motion_audit']);late=[h['kinetic_temperature'] for h in thermal['history'] if h['time']>=75.]
    bonds=list(rungs.items());last=r['metrics']['history'][-1]
    report=dict(campaign=str(folder),result_sha256=digest(path),manifest_sha256=digest(folder/'manifest.json'),
        scope='One dispersed seed at100,64 atoms; no negative cohort or rates inference. All H/T initially free, tool prepared.',
        lipids=r['metrics']['lipids_formed'],catalyzed=r['metrics']['catalyzed_lipids'],
        max_products_per_site_pair=r['metrics']['max_products_per_site_pair'],final_lateral_contacts=last['lateral_contacts'],
        first_lateral_contact_sample=next((h['time'] for h in r['metrics']['history'] if h['lateral_contacts']),None),
        products_with_nonprescribed_tail=sum(t!=h+count for h,t in bonds),atoms=len(pos),
        maximum_final_axial_error=max((abs(float(np.linalg.norm(pos[h]-pos[t]))-.65) for h,t in bonds),default=None),
        target_temperature=cfg['temperature'],final_kinetic_temperature=thermal['history'][-1]['kinetic_temperature'],
        mean_kinetic_temperature_last_quarter=sum(late)/len(late) if late else None,elapsed_seconds=r['elapsed_seconds'],
        limitation='New local ligand extension, same numeric constants but not a validated common P/R/L bath. '
            'Formation/capture/port switches supply uncalibrated energy; measured kinetic temperature must not be equated with thermostat target. '
            'No loss, expression, insertion into cell boundary, fuel budget or homeostasis demonstrated.')
    write(folder/'pilot_review.json',report);return report


if __name__=='__main__':print(json.dumps(review(),indent=2))
