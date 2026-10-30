"""Predeclared local gate: aligned thermal pair then one externally timed bond cut."""
from datetime import datetime,timezone
import argparse,hashlib,json,shutil,subprocess,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.engine import Simulation
from simulator.docking import port_geometry
from simulator.runner import create_output
from scripts.campaign import prepare,export_recipe,status
from experiments.prepare_coherent_contacts import plan


def local(seed,new):
    cfg=dict(schema_version=1,model='membrane',name=f'MD2_local_{new}',branch='MD2',seed=seed,duration=12.,
        engine=dict(dt=.002,sample_every=5),mechanics=dict(motion='langevin',mass=1.,damping=.1),
        chemistry=dict(units=2,initial='straight',face_docking=True,short_length=.98,box=[8.,8.],
            temperature=.08,bond_off_rate=0.,dock_energy=4.,dock_width=.3))
    if new:cfg['chemistry']['bound_port_geometry']=True
    sim=Simulation(cfg);c=sim.chemistry
    theta=np.arctan((1.-.98)/(2*.65));h=np.array([[3.,4.],[3.+np.cos(theta),4.]])
    v=np.array([[np.sin(theta),-np.cos(theta)],[-np.sin(theta),-np.cos(theta)]])
    c.pos=np.concatenate((h,h+.65*v));c.face_links=[(0,1,1,0)];c.edges=[{(0,1)},{(0,1)}];c._face_mechanics()
    out=create_output(sim.config,ROOT/'outputs/coherent_contact_gate');samples=[];cut=False;rebound=None;bound_at_cut=False
    started=time.perf_counter()
    while not sim.done:
        if not cut and sim.time>=10.-1e-9:
            bound_at_cut=bool(c.face_links)
            c.face_links=[];c.edges=[set(),set()];c._face_mechanics();sim.motion.force=None
            cut=True
        sim.advance(5)
        head,tail,_,_=port_geometry(c.pos,2,1.,.98)
        q=float(np.sum((head[1,0]-head[0,1])**2)+np.sum((tail[1,0]-tail[0,1])**2))
        samples.append(dict(time=sim.time,q=q,bound=bool(c.face_links)))
        if cut and c.face_links and rebound is None:rebound=sim.time
    late=[r for r in samples if 6.<=r['time']<10.]
    compatible=sum(r['bound'] and r['q']<c.config['dock_capture']**2 for r in late)/len(late)
    row=dict(seed=seed,new=new,compatible_fraction=compatible,bound_before_cut=bound_at_cut,
        recapture_event=rebound is not None,recapture_time=rebound if rebound is not None else 12.,folder=str(out))
    # Constructor inputs alone do not describe this prepared pair: preserve the exact initial coordinates and imposed-cut protocol.
    (out/'local_protocol.json').write_text(json.dumps(dict(scenario=sim.config,initial_positions=np.concatenate((h,h+.65*v)).tolist(),
        initial_face_links=[[0,1,1,0]],forced_cut_time=10.,samples=samples,result=row),indent=2)+'\n',encoding='utf-8')
    (out/'driver.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(row),flush=True);return row


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prepare-campaign',action='store_true');a=p.parse_args()
    latest=ROOT/'outputs/coherent_contacts_campaigns/latest.txt'
    if a.prepare_campaign and latest.exists():
        old=status(Path(latest.read_text().strip()))
        if old['controller_active'] or any(t['worker_active'] for t in old['tasks']):
            raise RuntimeError('A coherent-contact campaign is already active; inspect it before a new launch')
    rows=[local(seed,new) for seed in range(3) for new in (False,True)]
    new=[r for r in rows if r['new']]
    passed=all(r['compatible_fraction']>=.9 and r['bound_before_cut'] for r in new) and sum(r['recapture_event'] for r in new)>=2
    out=ROOT/'outputs/coherent_contact_gate'/('gate_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir()
    report=dict(passed=passed,rows=rows,criteria='All3 new >=90% bound and capture-compatible during6-10, all bound before fixed external cut10, >=2/3 recaptured by12; no instability.',
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='Prepared local pair diagnostic; no population or membrane proof. Cut imposed at fixed time, never from an observed score. No new production reaction.')
    if passed and a.prepare_campaign:
        recipe=ROOT/'campaigns/coherent_contacts.json';recipe.write_text(json.dumps(plan(),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        folder=prepare(recipe,ROOT/'outputs/coherent_contacts_campaigns')
        export_recipe(folder,ROOT/'research/campaign_recipes'/('MD2_'+folder.name.removeprefix('campaign_')))
        report['campaign']=str(folder)
        # The existing frozen controller owns execution, checkpoints, status and final analysis.
        stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
        with (folder/f'controller_{stamp}.stdout.log').open('wb') as stdout,(folder/f'controller_{stamp}.stderr.log').open('wb') as stderr:
            proc=subprocess.Popen([sys.executable,str(folder/'runtime/campaign.py'),'run',str(folder)],cwd=folder,stdout=stdout,stderr=stderr,
                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        report['controller_pid']=proc.pid
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');(out/'driver.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(dict(gate=str(out),**report)),flush=True)


if __name__=='__main__':main()
