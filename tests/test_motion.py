import copy
from pathlib import Path
import tempfile
import unittest
import numpy as np
from experiments.prepare_mixing_campaign import scenario
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator import checkpoint
from simulator.motion import pair_ou
from scripts.motion_report import clock_bounds,analyze
from scripts.campaign import prepare,run
from simulator.campaign_io import read,write


class MotionTests(unittest.TestCase):
    def cfg(self,kind):
        c=scenario(duration=3.)
        c['chemistry'].update(molecules=20,box=[12.,10.],record_interval=.1,
            motion=kind,damping=.1 if kind=='langevin' else 2.,initial_clearance=True)
        return c

    def test_reciprocal_pair_thermostat_and_exact_relative_ou(self):
        pos=np.array([[0.,0.],[.5,0.]])
        vel=np.array([[1.,.3],[-1.,.2]])
        before=vel.sum(axis=0).copy()
        pair_ou(pos,vel,np.array([[0,1]],dtype=np.int64),np.zeros(1),.1,1.,2.,0.,1.)
        np.testing.assert_allclose(vel.sum(axis=0),before,atol=1e-15)
        self.assertAlmostEqual(vel[0,0]-vel[1,0],2*np.exp(-.1))
        velocities=np.repeat(np.array([[.7,.2]]),2,axis=0)
        pair_ou(pos,velocities,np.array([[0,1]],dtype=np.int64),np.zeros(1),.1,1.,20.,0.,1.)
        np.testing.assert_array_equal(velocities,np.repeat(np.array([[.7,.2]]),2,axis=0))

    def test_resume_is_exact_for_velocity_rng_force_cache_and_observer(self):
        for kind in ('langevin','dpd'):
            with self.subTest(kind=kind):
                a=Simulation(self.cfg(kind));obs=make_observer(a.config,False);a.listeners.append(obs);a.advance(150)
                with tempfile.TemporaryDirectory() as d:
                    path=Path(d)/'s.npz';checkpoint.save(path,a,obs);b,other=checkpoint.load(path,make_observer)
                a.advance(1000);b.advance(1000)
                np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
                np.testing.assert_array_equal(a.motion.velocities,b.motion.velocities)
                self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
                self.assertEqual(obs.summary(),other.summary())

    def test_passive_observer_and_matched_initial_positions(self):
        positions=[];velocities=[]
        for kind in ('brownian','langevin','dpd'):
            cfg=self.cfg(kind);a=Simulation(cfg);b=Simulation(cfg);positions.append(a.chemistry.pos.copy())
            if a.motion is not None:velocities.append(a.motion.velocities.copy())
            obs=make_observer(a.config,False);a.listeners.append(obs)
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        for p in positions[1:]:np.testing.assert_array_equal(p,positions[0])
        np.testing.assert_array_equal(velocities[0],velocities[1])

    def test_ballistic_free_flight_and_no_temperature_blowup(self):
        cfg=self.cfg('langevin');cfg['chemistry'].update(beads_per_molecule=1,steric=False,temperature=0.,damping=0.)
        sim=Simulation(cfg);sim.motion.velocities[:]=[.2,0.];old=sim.chemistry.pos.copy()
        sim.advance(sim.target_step)
        np.testing.assert_allclose(sim.chemistry.pos,old+[.6,0.],atol=1e-12)
        for kind in ('langevin','dpd'):
            a=Simulation(self.cfg(kind));a.advance(a.target_step)
            temperature=a.motion.diagnostics(a.chemistry)['kinetic_temperature']
            self.assertTrue(0.02<temperature<.16)

    def test_clocks_are_bracketed_with_explicit_warmup(self):
        performance=dict(history=[dict(time=t,compute_seconds=s) for t,s in ((0.,0.),(1.25,2.),(2.5,3.),(3.75,4.))])
        c=clock_bounds(performance,3.)
        self.assertEqual((c['steady_low'],c['steady_high']),(0.,1.))
        self.assertFalse(c['goal_in_warmup'])

    def test_frozen_motion_campaign_records_compute_cost_and_censoring(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'plan.json'
            write(p,dict(workers=1,motion_report=True,tasks=[dict(scenario=self.cfg('langevin'))]))
            folder=prepare(p,Path(d)/'runs');self.assertEqual(run(folder),0)
            report=analyze(folder)
            self.assertTrue(report['complete_cohort'])
            row=report['rows'][0];self.assertTrue(row['source_verified'])
            self.assertGreater(row['compute_seconds'],0.)
            self.assertFalse(row['goals']['half_partners']['event'])


if __name__=='__main__':unittest.main()
