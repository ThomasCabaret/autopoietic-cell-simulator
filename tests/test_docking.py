import unittest
import numpy as np
from simulator.docking import docking_force
from simulator.config import resolve
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator import checkpoint
from pathlib import Path
import tempfile
import copy


class DockingTests(unittest.TestCase):
    def test_four_bead_force_gradient_and_momentum(self):
        pos=np.array([[0.,0.],[1.,-.12],[.07,-.65],[.84,-.75]])
        pairs=np.array([[0,1]],dtype=np.int64); free=np.ones((2,2),dtype=np.bool_)
        force,_=docking_force(pos,pairs,free,1.,.75,3.,.3)
        numeric=np.zeros_like(pos); h=1e-6
        for i in range(4):
            for a in range(2):
                plus,minus=pos.copy(),pos.copy(); plus[i,a]+=h; minus[i,a]-=h
                ep=docking_force(plus,pairs,free,1.,.75,3.,.3)[1]
                em=docking_force(minus,pairs,free,1.,.75,3.,.3)[1]
                numeric[i,a]=-(ep-em)/(2*h)
        np.testing.assert_allclose(force,numeric,atol=1e-7)
        np.testing.assert_allclose(force.sum(axis=0),0,atol=1e-12)
        self.assertAlmostEqual(float(np.sum(pos[:,0]*force[:,1]-pos[:,1]*force[:,0])),0.,places=11)

    def test_isolated_molecules_have_no_lateral_bonds(self):
        c=resolve(dict(schema_version=1,model='membrane',duration=1.,
                       chemistry=dict(units=24,initial='dispersed_units',face_docking=True,box=[10,10])))
        sim=Simulation(c)
        self.assertEqual(sim.chemistry.edges,[set(),set()])
        self.assertEqual(len(sim.chemistry.rungs),24)

    def test_saturated_faces_do_not_attract(self):
        pos=np.array([[0.,0.],[1.,-.12],[.07,-.65],[.84,-.75]])
        force,energy=docking_force(pos,np.array([[0,1]],dtype=np.int64),np.zeros((2,2),dtype=np.bool_),1.,.75,3.,.3)
        np.testing.assert_array_equal(force,0.)
        self.assertEqual(energy,0.)

    def test_face_contacts_tree_brute_and_checkpoint(self):
        config=resolve(dict(schema_version=1,model='membrane',duration=8.,seed=3,
            chemistry=dict(units=12,initial='dispersed_units',face_docking=True,
                           box=[8,8],dock_energy=4.,dock_width=.4,temperature=.08)))
        other=copy.deepcopy(config); other['engine']['spatial']='brute'
        a,b=Simulation(config),Simulation(other)
        a.advance(777)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'state.npz'; checkpoint.save(path,a)
            resumed,_=checkpoint.load(path)
            a.advance(a.target_step); resumed.advance(resumed.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,resumed.chemistry.pos)
            self.assertEqual(a.chemistry.export(),resumed.chemistry.export())
            self.assertEqual(a.rng.bit_generator.state,resumed.rng.bit_generator.state)
        b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.chemistry.export(),b.chemistry.export())


if __name__=='__main__': unittest.main()
