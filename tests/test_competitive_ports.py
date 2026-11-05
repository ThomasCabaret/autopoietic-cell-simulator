import unittest
import numpy as np
from experiments.competitive_port_potential import competitive_force,competitive_terms
from simulator.docking import docking_force,free_faces
from simulator.spatial import Neighborhood


class CompetitivePortTests(unittest.TestCase):
    def test_isolated_binary_potential_and_force_are_preserved(self):
        p=np.array([[0.,0.],[1.,.05],[0.,-.65],[.98,-.59]])
        pairs=np.array([[0,1]]);free=np.ones((2,2),dtype=bool)
        a,e=competitive_force(p,pairs,free,1.,.92,4.,.6);b,f=docking_force(p,pairs,free,1.,.92,4.,.6)
        np.testing.assert_allclose(a,b,rtol=1e-12,atol=1e-12);self.assertAlmostEqual(e,f,places=12)

    def test_crowded_force_is_gradient_of_energy_and_port_capacity_is_bounded(self):
        heads=np.array([[0.,0.],[1.,.03],[1.05,.15],[.1,.7]]);p=np.vstack((heads,heads+np.array([.03,-.65])))
        pairs=Neighborhood('brute',0.).pairs(p[:4],3.4,'CP1');free=free_faces(4,[])
        force,energy=competitive_force(p,pairs,free,1.,.92,4.,.6)
        _,_,load,_=competitive_terms(p,pairs,free,1.,.92,4.,.6)
        self.assertTrue(np.all(load<=1+1e-12));self.assertTrue(np.any(load>.5))
        for i in range(len(p)):
            for axis in range(2):
                a=p.copy();b=p.copy();a[i,axis]+=1e-6;b[i,axis]-=1e-6
                ea=competitive_force(a,pairs,free,1.,.92,4.,.6)[1];eb=competitive_force(b,pairs,free,1.,.92,4.,.6)[1]
                self.assertAlmostEqual(force[i,axis],-(ea-eb)/2e-6,places=6)
        np.testing.assert_allclose(force.sum(axis=0),0.,atol=1e-12)

    def test_port_occupancy_and_bound_partner_exclusions_still_apply(self):
        p=np.array([[0.,0.],[1.,0.],[0.,-.65],[1.,-.65]]);pairs=np.array([[0,1]])
        partners=np.array([[1,-1],[0,-1]])
        force,e=competitive_force(p,pairs,np.ones((2,2),dtype=bool),1.,.92,4.,.6,partners)
        self.assertEqual(e,0.);np.testing.assert_array_equal(force,np.zeros_like(p))
