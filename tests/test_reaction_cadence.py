import importlib.util
import tempfile
import unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.config import resolve
from simulator.runner import make_observer
from simulator import checkpoint
from experiments.prepare_numerical_campaign import scenario


class ReactionCadenceTests(unittest.TestCase):
    def test_default_is_exact_archived_engine_in_actual_coupled_bath(self):
        p=Path('research/campaign_recipes/N1_20261028T073131539788Z/runtime/simulator/engine.py')
        spec=importlib.util.spec_from_file_location('simulator._n1_engine',p)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        raw=scenario(1,0,duration=2.)
        a=Simulation(raw);b=module.Simulation(raw)
        a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.chemistry.export(),b.chemistry.export())
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)

    def test_independent_reaction_clock_preserves_integrator_step(self):
        raw=dict(schema_version=1,model='copy',duration=.04,
            engine=dict(dt=.001,reaction_every=20),chemistry=dict(sequence='001',free_units=0))
        sim=Simulation(raw);calls=[];original=sim.chemistry.react
        def record(time,dt,neighbors):
            calls.append((time,5*dt));return original(time,dt,neighbors)
        sim.chemistry.react=record;sim.advance(sim.target_step)
        np.testing.assert_allclose(calls,[(0.,.02),(.02,.02),(.04,.02)])
        self.assertEqual(sim.step_index,40)
        self.assertEqual(sim.dt,.001)

    def test_checkpoint_between_reaction_ticks_keeps_both_clocks(self):
        raw=dict(schema_version=1,model='copy',duration=2.,
            engine=dict(dt=.001,reaction_every=20),chemistry=dict(sequence='001',free_units=4))
        a=Simulation(raw);obs=make_observer(a.config,False);a.listeners.append(obs);a.advance(777)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'checkpoint.npz';checkpoint.save(path,a,obs)
            b,other=checkpoint.load(path,make_observer)
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.chemistry.export(),b.chemistry.export())
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
            self.assertEqual(obs.summary(),other.summary())

    def test_reject_ambiguous_or_invalid_reaction_clock(self):
        for value in (True,0,-1,1.5,'5'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                resolve(dict(schema_version=1,model='copy',engine=dict(reaction_every=value)))
