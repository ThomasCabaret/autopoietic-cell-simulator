import unittest
from pathlib import Path
import tempfile
from unittest.mock import patch
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer,create_output,save_result
from simulator.spatial import Neighborhood
from simulator import checkpoint
import copy


class CatalysisTests(unittest.TestCase):
    def test_uniform_ligation_and_local_release_conserve_material(self):
        sim=Simulation(dict(schema_version=1,model='catalysis',duration=1.,
            chemistry=dict(food_pairs=1,reaction_rate=10000.,unbinding_rate=0.)))
        c=sim.chemistry
        c.pos[:3]=np.array([[4.91,5.],[5.,4.2],[5.09,5.]])
        c.pos[3:]=c.pos[[0,2]]
        c.binding[:]=[3,-1,4,0,2]
        events=c.react(0.,sim.dt,Neighborhood())
        self.assertEqual(len(c.pos),5)
        self.assertEqual(c.products,{(3,4)})
        self.assertEqual(c.scaffold,{(0,1),(1,2)})
        np.testing.assert_array_equal(c.binding,-1)
        self.assertEqual(events[0]['support'],(0,2))
        # The same primitive ligation also operates without any bound catalyst.
        other=Simulation(dict(schema_version=1,model='catalysis',duration=1.,
            chemistry=dict(food_pairs=1,reaction_rate=10000.,binding_rate=0.)))
        other.chemistry.pos[3:]=c.pos[3:]
        events=other.chemistry.react(0.,sim.dt,Neighborhood())
        self.assertEqual(len(events),1)
        self.assertEqual(events[0]['support'],(-1,-1))

    def test_capture_force_gradient(self):
        sim=Simulation(dict(schema_version=1,model='catalysis',duration=1.,chemistry=dict(food_pairs=1)))
        c=sim.chemistry
        c.pos=np.array([[1.,1.],[4.,4.],[3.,1.],[1.4,1.2],[3.3,1.2]])
        def energy(p):
            total=0.; cfg=c.config
            for i in range(len(p)):
                for j in range(i+1,len(p)):
                    if c.family[i]==c.family[j] or c.bits[i]!=c.bits[j]: continue
                    r2=np.sum((p[j]-p[i])**2)
                    if r2<(3*cfg['ligand_width'])**2:
                        total-=cfg['ligand_energy']*np.exp(-r2/(2*cfg['ligand_width']**2))
            return total
        actual=c.extra_forces(Neighborhood())
        numeric=np.zeros_like(c.pos); h=1e-6
        for i in range(len(c.pos)):
            for axis in range(2):
                plus,minus=c.pos.copy(),c.pos.copy(); plus[i,axis]+=h;minus[i,axis]-=h
                numeric[i,axis]=-(energy(plus)-energy(minus))/(2*h)
        np.testing.assert_allclose(actual,numeric,atol=1e-8)

    def test_result_hashes_use_frozen_code_snapshot(self):
        config=dict(schema_version=1,model='catalysis',duration=.1,chemistry=dict(food_pairs=1))
        sim=Simulation(config); obs=make_observer(sim.config); sim.listeners.append(obs)
        with tempfile.TemporaryDirectory() as directory:
            path=create_output(sim.config,directory)
            sim.advance(sim.target_step)
            with patch('simulator.checkpoint.source_hashes',return_value={'edited.py':'0'*64}):
                result=save_result(path,sim,obs,0.)
            self.assertIn('simulator/engine.py',result['source_sha256'])
            self.assertNotIn('edited.py',result['source_sha256'])

    def test_catalysis_tree_brute_checkpoint_and_observer(self):
        config=dict(schema_version=1,model='catalysis',seed=2,duration=4.,chemistry=dict(food_pairs=4))
        first=Simulation(config); oa=make_observer(first.config); first.listeners.append(oa)
        other=copy.deepcopy(config); other['engine']={'spatial':'brute'}
        second=Simulation(other); ob=make_observer(second.config); second.listeners.append(ob)
        first.advance(777)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'state.npz'; checkpoint.save(path,first,oa)
            resumed,oc=checkpoint.load(path,make_observer)
            first.advance(first.target_step); resumed.advance(resumed.target_step)
            np.testing.assert_array_equal(first.chemistry.pos,resumed.chemistry.pos)
            self.assertEqual(oa.summary(),oc.summary())
        second.advance(second.target_step)
        np.testing.assert_array_equal(first.chemistry.pos,second.chemistry.pos)
        self.assertEqual(oa.summary(),ob.summary())


if __name__=='__main__': unittest.main()
