import copy
from pathlib import Path
import tempfile
import unittest
import numpy as np
from experiments.prepare_reactive_motion import scenario
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.motion import MotionAudit
from simulator import checkpoint
from visualizer.demos import dynamics_hash


class ReactiveMotionTests(unittest.TestCase):
    def cfg(self):
        cfg=scenario(duration=2.)
        cfg['chemistry'].update(sequence='001',free_units=12,box=[10.,7.])
        return cfg

    def test_unreported_reaction_changes_invalidate_the_force_cache(self):
        sim=Simulation(self.cfg());sim.advance(4)
        self.assertIsNotNone(sim.motion.force)
        original=sim.chemistry.react
        def changed(time,dt,neighbors):
            original(time,dt,neighbors)
            sim.chemistry.springs[0,2]*=1.1
            return []
        sim.chemistry.react=changed;sim.advance(1)
        self.assertIsNone(sim.motion.force)

    def test_cached_and_always_refreshed_forces_produce_identical_dynamics(self):
        a=Simulation(self.cfg());b=Simulation(self.cfg())
        a.advance(a.target_step)
        for _ in range(b.target_step):
            b.motion.force=None;b.advance(1)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        np.testing.assert_array_equal(a.motion.velocities,b.motion.velocities)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)

    def test_reactive_resume_and_passive_thermal_audit(self):
        a=Simulation(self.cfg());b=Simulation(self.cfg());obs=make_observer(a.config,False)
        a.listeners.extend([obs,MotionAudit(a)]);a.advance(150);b.advance(150)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'s.npz';checkpoint.save(p,a,obs);c,other=checkpoint.load(p,make_observer)
        a.advance(1000);b.advance(1000);c.advance(1000)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        np.testing.assert_array_equal(a.chemistry.pos,c.chemistry.pos)
        np.testing.assert_array_equal(a.motion.velocities,c.motion.velocities)
        self.assertEqual(a.rng.bit_generator.state,c.rng.bit_generator.state)
        self.assertEqual(obs.summary(),other.summary())

    def test_motion_is_part_of_the_scenario_signature_and_positions_are_matched(self):
        cfg=self.cfg();brown=copy.deepcopy(cfg);del brown['mechanics']
        self.assertNotEqual(dynamics_hash(cfg),dynamics_hash(brown))
        np.testing.assert_array_equal(Simulation(cfg).chemistry.pos,Simulation(brown).chemistry.pos)
        self.assertEqual(Simulation(cfg).config['chemistry'],Simulation(brown).config['chemistry'])


if __name__=='__main__':unittest.main()
