import copy
from pathlib import Path
import tempfile
import unittest
import numpy as np
from simulator.engine import Simulation
from simulator.config import resolve
from simulator.runner import make_observer
from simulator import checkpoint


def scenario(seed=0,duration=4.,dt=.004):
    return dict(schema_version=1,model='open_bath',name='OB1',seed=seed,duration=duration,
        chemistry=dict(initial_counts=[3,2],influx_per_length=[.5,.5],max_samples=5),
        engine=dict(dt=dt,reaction_every=round(.02/dt),sample_every=round(.1/dt)))


class OpenBathTests(unittest.TestCase):
    def test_source_calendar_independent_of_motion_and_cadences(self):
        runs=[]
        for seed,dt,cadence in ((0,.004,5),(1,.002,10),(0,.002,5)):
            cfg=scenario(seed=seed,dt=dt);cfg['engine']['reaction_every']=cadence
            sim=Simulation(cfg);sim.advance(sim.target_step);runs.append(sim)
            c=sim.chemistry
            self.assertLessEqual(c.max_injection_lag,cadence*dt+1e-10)
            self.assertTrue(np.all(np.array(c.census(sim.time)['balance_error'])==0))
        for other in runs[1:]:
            np.testing.assert_array_equal(runs[0].chemistry.injected,other.chemistry.injected)
            self.assertEqual(runs[0].chemistry.source_digest,other.chemistry.source_digest)

    def test_population_map_preserves_survivor_velocities_ids_and_removes_walls(self):
        cfg=scenario(duration=.04);cfg['chemistry'].update(influx_per_length=[0.,0.],temperature=0.)
        sim=Simulation(cfg);c=sim.chemistry
        c.pos[:]=[[2.,2.],[3.,2.],[4.,2.],[5.,2.],[6.,2.]]
        sim.motion.velocities[:]=[[.1,0.],[.2,0.],[.3,0.],[.4,0.],[.5,0.]]
        sim.prepare();sim.advance(4)
        # Last mechanical step has no reflecting force; one external atom exits.
        c.pos[1]=[-.1,2.];sim.motion.force=None
        before=sim.motion.velocities[[0,2,3,4]].copy()
        sim.advance(1)
        np.testing.assert_array_equal(c.atom_ids,[0,2,3,4])
        np.testing.assert_allclose(sim.motion.velocities,before*np.exp(-.1*.004),atol=1e-15)
        self.assertEqual(c.exported.tolist(),[1,0])
        self.assertEqual(c.census(sim.time)['balance_error'],[0,0])
        self.assertFalse(sim.neighbors.cache)

    def test_empty_bath_birth_death_and_source_off(self):
        cfg=scenario();cfg['chemistry'].update(initial_counts=[0,0],influx_per_length=[0.,0.])
        sim=Simulation(cfg);sim.advance(sim.target_step)
        self.assertEqual(sim.chemistry.pos.shape,(0,2))
        self.assertIsNone(sim.motion.diagnostics(sim.chemistry)['kinetic_temperature'])
        self.assertEqual(sim.chemistry.census(sim.time)['counts'],[0,0])
        cfg['chemistry']['influx_per_length']=[.5,.5]
        sim=Simulation(cfg);sim.advance(sim.target_step)
        self.assertGreater(sim.chemistry.injected.sum(),0)
        self.assertGreater(sim.chemistry.exported.sum(),0)
        self.assertEqual(sim.chemistry.census(sim.time)['balance_error'],[0,0])
        self.assertEqual(len(set(sim.chemistry.atom_ids)),len(sim.chemistry.pos))
        self.assertGreaterEqual(sim.chemistry.next_id,len(sim.chemistry.pos))

    def test_resume_exact_and_observation_passive_and_bounded(self):
        a=Simulation(scenario());obs=make_observer(a.config,False);a.listeners.append(obs)
        a.advance(255)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'open.npz';checkpoint.save(path,a,obs);b,other=checkpoint.load(path,make_observer)
        a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        np.testing.assert_array_equal(a.motion.velocities,b.motion.velocities)
        self.assertEqual(a.chemistry.export(),b.chemistry.export())
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertEqual(obs.summary(),other.summary())
        c=Simulation(scenario());c.advance(c.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,c.chemistry.pos)
        self.assertEqual(a.chemistry.export(),c.chemistry.export())
        self.assertEqual(a.rng.bit_generator.state,c.rng.bit_generator.state)
        self.assertLessEqual(len(obs.history),5);self.assertLessEqual(len(obs.times),5)
        self.assertGreater(obs.observations,5)

    def test_capacity_fails_instead_of_regulating_and_validation(self):
        cfg=scenario();cfg['chemistry'].update(initial_counts=[0,0],influx_per_length=[100.,100.],max_particles=1)
        sim=Simulation(cfg)
        with self.assertRaisesRegex(RuntimeError,'capacity exhausted'):sim.advance(100)
        for settings in (dict(influx_per_length=[-1.,1.]),dict(influx_per_length=[1.]),dict(initial_counts=[True,0]),
                         dict(source_seed=-1),dict(max_samples=0),dict(injection_depth=4.),dict(motion='brownian')):
            cfg=scenario();cfg['chemistry'].update(settings)
            with self.subTest(settings=settings),self.assertRaises(ValueError):resolve(cfg)


if __name__=='__main__':unittest.main()
