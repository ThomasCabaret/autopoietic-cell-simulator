import copy
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np

from simulator.config import legacy,resolve
from simulator.engine import Simulation
from simulator.runner import make_observer,run,replay
from simulator.spatial import Neighborhood
from simulator.physics import force_kernel,orientation_kernel
from simulator.reference import mechanical_forces,opposite_force,port_attraction
from simulator import checkpoint

ROOT=Path(__file__).resolve().parents[1]
CASES=json.loads((ROOT/'research/cases.json').read_text(encoding='utf-8'))


def scenario(case='T7',duration=10.):
    return legacy({**CASES[case],'case':case,'seed':0,'duration':duration})


def attach(sim):
    obs=make_observer(sim.config)
    sim.listeners.append(obs)
    return obs


class SpatialTests(unittest.TestCase):
    def test_tree_matches_brute_and_skin_never_misses_contacts(self):
        rng=np.random.default_rng(42)
        p=np.concatenate((rng.uniform(-5,5,(200,2)),np.array([[0,0],[0,0],[-1.,0.],[1.,0.]])))
        tree,brute=Neighborhood('tree',.4),Neighborhood('brute',0)
        for _ in range(20):
            np.testing.assert_array_equal(tree.pairs(p,.7),brute.pairs(p,.7))
            p+=rng.normal(0,.02,p.shape)
        p[0]+=20.
        np.testing.assert_array_equal(tree.pairs(p,.7),brute.pairs(p,.7))

    def test_finite_sparse_force_equals_dense_reference(self):
        rng=np.random.default_rng(3)
        p=rng.uniform(-1,1,(20,2))
        kinds=np.arange(20,dtype=np.int64)%2
        contact=np.array([[.7,.28],[.28,0.]])
        core=contact[kinds[:,None],kinds[None,:]].copy()
        np.fill_diagonal(core,0)
        springs=np.array([[0,19,12.,.8],[3,7,15.,.7]])
        angles=np.array([[0,3,7,2.,-.2]])
        pairs=Neighborhood().pairs(p,.7)
        actual=force_kernel(p,pairs,kinds,contact,springs,angles)
        np.testing.assert_allclose(actual,mechanical_forces(p,springs,angles,core),atol=1e-12)
        np.testing.assert_allclose(actual.sum(axis=0),0.,atol=1e-12)

    def test_stretched_bond_is_not_lost_outside_contact_cutoff(self):
        p=np.array([[0.,0.],[20.,0.]])
        pairs=Neighborhood().pairs(p,.7)
        force=force_kernel(p,pairs,np.zeros(2,dtype=np.int64),np.array([[.7]]),
                           np.array([[0.,1.,2.,1.]]),np.empty((0,5)))
        np.testing.assert_array_equal(force,np.array([[38.,0.],[-38.,0.]]))

    def test_compiled_orientation_and_sparse_virtual_ports(self):
        p=np.array([[0.,0.],[1.15,.08],[.04,-.65],[1.1,-.58]])
        rungs=np.array([[0,2],[1,3]])
        pairs=np.array([[0,1]],dtype=np.int64)
        np.testing.assert_allclose(orientation_kernel(p,rungs,pairs),opposite_force(p,rungs,pairs.tolist()),atol=1e-12)
        expected=port_attraction(p,rungs,set(),0,1.)
        actual=port_attraction(p,rungs,set(),0,1.,neighbors=Neighborhood())
        np.testing.assert_allclose(actual,expected,atol=1e-12)


class EngineTests(unittest.TestCase):
    def test_tree_brute_same_positions_reactions_rng_and_observations(self):
        for case in ('T7','E0','V6'):
            with self.subTest(case=case):
                a=scenario(case,4.)
                b=copy.deepcopy(a); b['engine']['spatial']='brute'
                first,second=Simulation(a),Simulation(b)
                oa,ob=attach(first),attach(second)
                first.advance(first.target_step); second.advance(second.target_step)
                np.testing.assert_array_equal(first.chemistry.pos,second.chemistry.pos)
                self.assertEqual(first.chemistry.export(),second.chemistry.export())
                self.assertEqual(first.rng.bit_generator.state,second.rng.bit_generator.state)
                self.assertEqual(oa.summary(),ob.summary())

    def test_checkpoint_exact_continuation_between_chemical_updates(self):
        for case in ('T7','E0','V6'):
            with self.subTest(case=case),tempfile.TemporaryDirectory() as directory:
                sim=Simulation(scenario(case,8.))
                obs=attach(sim)
                sim.advance(777)
                path=Path(directory)/'checkpoint.npz'
                checkpoint.save(path,sim,obs)
                resumed,other=checkpoint.load(path,make_observer)
                sim.advance(sim.target_step-sim.step_index)
                resumed.advance(resumed.target_step-resumed.step_index)
                np.testing.assert_array_equal(sim.chemistry.pos,resumed.chemistry.pos)
                self.assertEqual(sim.rng.bit_generator.state,resumed.rng.bit_generator.state)
                self.assertEqual(sim.chemistry.export(),resumed.chemistry.export())
                self.assertEqual(obs.summary(),other.summary())

    def test_snapshots_and_chunk_size_cannot_change_dynamics(self):
        first,second=Simulation(scenario(duration=2.)),Simulation(scenario(duration=2.))
        while not first.done:
            first.advance(1)
            snapshot=first.snapshot()
            snapshot['positions'][:]=12345
            snapshot['bonds']['backbone'].clear()
        second.advance(second.target_step)
        np.testing.assert_array_equal(first.chemistry.pos,second.chemistry.pos)
        self.assertEqual(first.rng.bit_generator.state,second.rng.bit_generator.state)

    def test_headless_provenance_and_full_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence,path=run(scenario(duration=1.),parent=directory,record=False)
            self.assertTrue(evidence['completed'])
            self.assertFalse((path/'trajectory.npz').exists())
            self.assertTrue((path/'simulator/engine.py').exists())
            replay(path)

    def test_config_rejects_mistakes(self):
        for change in ({'duration':-.1},{'duration':.003},{'schema_version':2}, {'seed':-1}):
            c=scenario(); c.update(change)
            with self.assertRaises(ValueError): resolve(c)
        c=scenario(); c['chemistry']['typo']=12
        with self.assertRaises(ValueError): resolve(c)


if __name__=='__main__': unittest.main()
