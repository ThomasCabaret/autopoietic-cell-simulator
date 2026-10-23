"""Compatibility entry points. All current execution uses simulator.engine.
Exact historical implementations remain inside immutable research run archives.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from simulator.reference import (add_force, mechanical_forces, normals, opposite_force,
    local_port_free, degree, integrate, port_sites, port_attraction)
from simulator.config import legacy
from simulator.engine import Simulation


def _run(config,seed,observer,mode):
    sim=Simulation(legacy({**config,'seed':seed,'mode':mode}))
    sim.listeners.append(observer)
    sim.advance(sim.target_step)


def copying(config,seed,observer):
    _run(config,seed,observer,'copy')


def vesicle(config,seed,observer):
    _run(config,seed,observer,'vesicle')
