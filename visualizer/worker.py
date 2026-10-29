"""Process boundary: the child owns Simulation, numerical clocks and RNG.

Commands affect execution pacing only. Scene/filter/camera/shader state never
crosses this boundary. Output queues and event buffers have explicit bounds.
"""
import multiprocessing as mp
from pathlib import Path
import queue
import time
import traceback
from .scene import EventTap,frame,species
from .observations import live_observations


def execute(config,commands,frames,parent):
    from simulator.engine import Simulation
    from simulator.runner import make_observer,create_output,save_result
    from simulator import checkpoint
    sim=obs=path=None;started=time.monotonic();saved=False;error=None
    try:
        sim=Simulation(config);obs=make_observer(sim.config,False);sim.listeners.append(obs)
        observed_time=[None]
        def observation_clock(time,*args):observed_time[0]=float(time)
        sim.listeners.append(observation_clock)
        path=create_output(sim.config,parent);tap=EventTap(sim.chemistry);catalog=species(sim.chemistry)
        paused=True;speed=.5;last_publish=-1.;last=time.monotonic();last_rate=last;last_step=0;rate=0.;credit=0.;dirty=True
        sim.advance(0)
        def publish(force=False):
            nonlocal last_publish,dirty
            now=time.monotonic()
            if not dirty:return
            if not force and now-last_publish<1/30:return
            if frames.full():return
            packet=dict(frame=frame(sim,catalog,tap.revision),events=list(tap.events),dropped=tap.dropped,
                paused=paused,speed=speed,rate=rate,path=str(path.resolve()),config=sim.config,
                observations=live_observations(obs,observed_time[0]))
            try:frames.put_nowait(packet)
            except queue.Full:return
            tap.events.clear();last_publish=now;dirty=False
        running=True
        while running:
            now=time.monotonic();elapsed=now-last;last=now;single=False;force=False
            while True:
                try:action,value=commands.get_nowait()
                except queue.Empty:break
                if action=='stop':running=False
                elif action=='pause':paused=bool(value);credit=0.;force=True
                elif action=='step':paused=True;single=True;credit=0.;force=True
                elif action=='speed':speed=float(value);credit=0.;force=True
                elif action=='checkpoint':checkpoint.save(path/'user_checkpoint.npz',sim,obs);force=True
            if not running:break
            if force:dirty=True
            if single and not sim.done:sim.advance(1);dirty=True
            elif not paused and not sim.done:
                if speed==0:steps=32
                else:
                    credit=min(64.,credit+elapsed*speed/sim.dt);steps=min(32,int(credit));credit-=steps
                if steps:sim.advance(steps);dirty=True
            if sim.done and not saved:
                save_result(path,sim,obs,time.monotonic()-started);saved=True
            if now-last_rate>=.5:
                rate=(sim.step_index-last_step)/(now-last_rate);last_step=sim.step_index;last_rate=now
            publish(force)
            if paused or sim.done:time.sleep(.005)
            elif speed:time.sleep(.001)
    except Exception:
        error=traceback.format_exc()
        try:frames.put(dict(error=error),timeout=2.)
        except queue.Full:pass
    finally:
        if sim is not None and path is not None and not saved:
            try:save_result(path,sim,obs,time.monotonic()-started,error)
            except Exception:pass


class ProcessSource:
    def __init__(self,config,parent='outputs/visualizer'):
        ctx=mp.get_context('spawn');self.commands=ctx.Queue();self.frames=ctx.Queue(maxsize=2)
        self.process=ctx.Process(target=execute,args=(config,self.commands,self.frames,str(Path(parent).resolve())),daemon=True)
        self.process.start()

    def command(self,action,value=None):self.commands.put((action,value))

    def poll(self):
        packets=[]
        while True:
            try:packets.append(self.frames.get_nowait())
            except queue.Empty:return packets

    def close(self):
        self.command('stop');deadline=time.monotonic()+10
        while self.process.is_alive() and time.monotonic()<deadline:
            self.poll();self.process.join(.02)
        clean=not self.process.is_alive()
        if not clean:self.process.terminate();self.process.join(2)
        self.commands.close();self.frames.close();return clean
