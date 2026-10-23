"""Exercise the real viewer and worker with SDL's offscreen video driver."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
from pathlib import Path
import sys
import threading
import time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import pygame
from simulator.config import load
from simulator.engine import Simulation
from simulator.runner import make_observer,compact
from simulator.viewer import Canvas,Controller,live_view,replay_view

out=ROOT/'outputs/viewer_smoke'
out.mkdir(parents=True,exist_ok=True)
config=load(ROOT/'demonstrators/configs/membrane.json')
config['duration']=2.
config['expected']={}
reference=Simulation(config)
reference.advance(reference.target_step)
controller=Controller(config,out,record=False)
deadline=time.monotonic()+15
state=None
while time.monotonic()<deadline:
    while not controller.frames.empty(): state=controller.frames.get_nowait()
    if state is not None and state['done']: break
    time.sleep(.02)
controller.send('stop'); controller.thread.join(10)
assert not controller.thread.is_alive() and state is not None and state['done']
assert not state.get('error'),state.get('error')
np.testing.assert_array_equal(state['positions'],reference.chemistry.pos)
pygame.init()
surface=pygame.Surface((1200,900))
canvas=Canvas(surface)
canvas.draw(state)
assert len(canvas.buttons)==7
pygame.image.save(surface,str(out/'live_interface.png'))
pygame.quit()
# Pump the actual event loop and close it without opening a native window.
timer=threading.Timer(1.5,lambda:pygame.event.post(pygame.event.Event(pygame.QUIT)))
timer.start()
live_view(config,out,record=False)
timer.join()
replay_view(ROOT/'research/runs/V6_s1_20261023T115206264055Z',out/'fragments_replay.png')
print('Offscreen UI, replay and worker/headless trajectory equivalence: passed')
