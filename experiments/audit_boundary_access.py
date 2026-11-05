"""Read BI1 evidence and a bounded static three-L docking control; no trajectory."""
import json,sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import digest
from scripts.expression_followup import status
from simulator.campaign_io import read,write
from simulator.docking import docking_force,free_faces,port_geometry


def local_control(config):
    # One actual contact i--j, with k translated normally near j's occupied pose.
    # This is a constructed static geometry, not spontaneous insertion.
    links=[(0,1,1,0)];free=free_faces(3,links);rows=[]
    for d in (2.,1.,.6,.5,.4):
        heads=np.array([[0.,0.],[1.,0.],[1.,d]])
        pos=np.vstack((heads,heads+[0.,-.65]))
        head,tail,_,_=port_geometry(pos,3,1.,config['short_length'])
        q=float(np.sum((head[2,0]-head[0,1])**2)+np.sum((tail[2,0]-tail[0,1])**2))
        pairs=np.array([[0,2],[1,2]],dtype=np.int64)
        f,e=docking_force(pos,pairs,free,1.,config['short_length'],config['dock_energy'],config['dock_width'])
        rows.append(dict(normal_separation=d,occupied_port_q=q,exchange_geometric_capture=q<config['contact_exchange_capture']**2,
            free_port_energy=float(e),incoming_attractive_force=float(np.linalg.norm(f[[2,5]])),
            axial_core_overlap=max(.4-d,0.)))
    return rows


def main():
    job=Path(read(ROOT/'research/BATCH_43_RECIPES.json')['job']);snap=status(job)
    if snap['active'] or snap['campaigns'][0]['counts']['complete']!=9:raise ValueError('Require complete inactive BI1')
    p=Path(snap['state']['report_0'])
    if digest(p)!=snap['state']['report_0_sha256']:raise ValueError('BI1 report changed')
    report=read(p);active=[r for r in report['rows'] if '_active_' in r['label']]
    folder=Path(read(job/'job.json')['campaigns'][0]);cfg=read(folder/'manifest.json')['tasks'][0]['scenario']['chemistry']
    rows=[]
    for r in active:
        k=r['kinetics']['opportunity_totals'];exposure=k['gated_exchange_face_time']*cfg['contact_exchange_rate']
        rows.append(dict(label=r['label'],L=r['L_new'],G=r['G_new'],F=r['F_new'],
            unassembled=r['calibration']['windows'][-1]['unassembled'],encounter_pair_time=k['encounter_pair_time'],
            exchange_face_time=k['gated_exchange_face_time'],sampled_rate_weighted_exposure=exposure,
            last_PR=r['calibration']['last_PR'],last_L=r['calibration']['last_L']))
    out=ROOT/'outputs/diagnostics'/('BI1_access_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir(parents=True)
    result=dict(predecessor_report_sha256=digest(p),active=rows,three_lipid_control=local_control(cfg),
        summed_sampled_rate_weighted_exposure=sum(r['sampled_rate_weighted_exposure'] for r in rows),
        scope='Pre-reaction face time only, not full competing/sequential hazard or Poisson probability. '
            'Static constructed three-L geometry does not prove dynamics. Occupied ports have no attractive docking field. '
            'No source edits, fitting, simulation, RNG or observer feedback.')
    write(out/'report.json',result);(out.parent/'latest_boundary_access.txt').write_text(str(out.resolve()))
    print(json.dumps(result,indent=2));print(out)


if __name__=='__main__':main()
