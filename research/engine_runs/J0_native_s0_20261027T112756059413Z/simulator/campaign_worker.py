"""One frozen campaign task, using Simulation.advance and the shared observer."""
import argparse,hashlib,os,time,traceback
from pathlib import Path
from .engine import Simulation
from .runner import create_output,save_result,make_observer
from . import checkpoint
from .campaign_io import read,write,lock
from .kinetics import KineticProbe
from .boundary_audit import BoundaryAudit


def execute(folder,task_id):
    folder=Path(folder).resolve();manifest=read(folder/'manifest.json')
    if hashlib.sha256((folder/'manifest.json').read_bytes()).hexdigest()!=(folder/'manifest.sha256').read_text().strip():
        raise ValueError('Frozen manifest changed')
    for name,digest in manifest['source_sha256'].items():
        if hashlib.sha256((folder/'runtime'/name).read_bytes()).hexdigest()!=digest:raise ValueError('Frozen source changed: '+name)
    task=next(t for t in manifest['tasks'] if t['id']==task_id)
    dest=folder/'tasks'/task_id;dest.mkdir(parents=True,exist_ok=True)
    with lock(dest/'worker.lock'):
        prior=read(dest/'state.json',{});sim=obs=path=None;start=time.monotonic()
        state=dict(task=task_id,status='running',pid=os.getpid(),updated=time.time(),checkpoint=prior.get('checkpoint'))
        write(dest/'state.json',state)
        try:
            if state['checkpoint']:
                sim,obs=checkpoint.load(folder/state['checkpoint'],make_observer)
            else:
                sim=Simulation(task['scenario']);obs=make_observer(sim.config,manifest['record_trajectory']);sim.listeners.append(obs)
            probe=KineticProbe(sim.config,getattr(obs,'campaign_kinetics_state',None),manifest['kinetic_window'])
            probe.attach(sim.chemistry)
            audit=None
            if manifest.get('boundary_audit',False):
                audit=BoundaryAudit(sim.config,obs,getattr(obs,'campaign_boundary_state',None))
                sim.listeners.append(audit)
            path=create_output(sim.config,dest/'attempts');last_save=last_report=time.monotonic();last_step=sim.step_index
            def save():
                obs.campaign_kinetics_state=probe.state
                if audit is not None:obs.campaign_boundary_state=audit.state
                checkpoint.save(path/'periodic.npz',sim,obs)
                state['checkpoint']=(path/'periodic.npz').relative_to(folder).as_posix()
            while not sim.done:
                if (folder/'STOP').exists():
                    save();state.update(status='paused',step=sim.step_index,simulated_time=sim.time,updated=time.time())
                    write(dest/'state.json',state);return 0
                sim.advance(250);now=time.monotonic()
                if now-last_save>=manifest['checkpoint_seconds']:save();last_save=now
                if now-last_report>=1.:
                    rate=(sim.step_index-last_step)/(now-last_report);last_report=now;last_step=sim.step_index
                    state.update(updated=time.time(),step=sim.step_index,target_step=sim.target_step,
                        simulated_time=sim.time,steps_per_second=rate,eta_seconds=(sim.target_step-sim.step_index)/rate if rate else None)
                    state['kinetic_exposure']={k:sum(w[k] for w in probe.state['windows'].values())
                        for k in ('encounter_pair_time','capture_face_time','exchange_face_time','exchanges')}
                    if probe.terminal:
                        state['kinetic_exposure']['gated_exchange_face_time']=sum(w.get('gated_exchange_face_time',0.) for w in probe.state['windows'].values())
                    if audit is not None:state['boundary_state']=audit.state['last_kind']
                    write(dest/'state.json',state)
            obs.campaign_kinetics_state=probe.state
            if audit is not None:obs.campaign_boundary_state=audit.state
            evidence=save_result(path,sim,obs,time.monotonic()-start)
            save();write(path/'kinetics.json',probe.summary(sim.time,evidence['metrics']))
            if audit is not None:
                write(path/'boundary_audit.json',audit.summary())
                state['boundary_audit']=(path/'boundary_audit.json').relative_to(folder).as_posix()
            state.update(status='complete',updated=time.time(),step=sim.step_index,target_step=sim.target_step,
                simulated_time=sim.time,result=(path/'result.json').relative_to(folder).as_posix(),
                kinetics=(path/'kinetics.json').relative_to(folder).as_posix(),expected_checks=evidence['expected_checks'])
            write(dest/'state.json',state);return 0
        except Exception:
            state.update(status='failed',updated=time.time(),error=traceback.format_exc())
            if sim is not None and obs is not None and path is not None:
                try:save()
                except Exception:state['checkpoint_error']=traceback.format_exc()
            write(dest/'state.json',state);raise


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('task_id');a=p.parse_args()
    raise SystemExit(execute(a.folder,a.task_id))
