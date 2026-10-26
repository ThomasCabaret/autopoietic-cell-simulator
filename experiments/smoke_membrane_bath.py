"""Offscreen rendering and worker/headless identity for sparse membrane records."""
import os
os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_AUDIODRIVER']='dummy'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
import sys,time,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pygame
from simulator.config import load
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.viewer import Controller,Canvas,replay_view


if __name__=='__main__':
    out=ROOT/'outputs/batch9/viewer';out.mkdir(parents=True,exist_ok=True)
    cfg=load(ROOT/'demonstrators/configs/large_membrane.json');cfg['duration']=2.;cfg['expected']={}
    ref=Simulation(cfg);obs=make_observer(ref.config);ref.listeners.append(obs);ref.advance(ref.target_step)
    worker=Controller(cfg,out);deadline=time.monotonic()+60.;state=None
    while time.monotonic()<deadline:
        while not worker.frames.empty():state=worker.frames.get_nowait()
        if state is not None and state['done']:break
        time.sleep(.02)
    worker.send('stop');worker.thread.join(10)
    assert not worker.thread.is_alive() and state and state['done'] and not state.get('error')
    np.testing.assert_array_equal(state['positions'],ref.chemistry.pos)
    result=json.loads((Path(state['path'])/'result.json').read_text(encoding='utf-8'))
    assert result['metrics']==json.loads(json.dumps(obs.summary()))
    assert len(state['colors'])==len(state['positions'])
    pygame.init();surface=pygame.Surface((1200,900));Canvas(surface).draw(state)
    pygame.image.save(surface,str(out/'live.png'));pygame.quit()
    folder=next((ROOT/'research/engine_runs').glob('M1exchange_s2*'))
    replay_view(folder,out/'replay.png')
    print('Sparse replay, rendering, worker/headless positions and all metrics: passed')
