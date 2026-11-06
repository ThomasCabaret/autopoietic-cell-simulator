import unittest
import numpy as np
from experiments.audit_bound_curvature import pair_pose,local_profile,bare_modes
from simulator.docking import bound_port_force


class BoundCurvatureTests(unittest.TestCase):
    def test_open_backbone_has_only_three_rigid_modes_and_stable_soft_modes(self):
        a=bare_modes(12);b=bare_modes(12,step=5e-6)
        self.assertLess(a['force_at_reference'],1e-10)
        self.assertEqual(a['rigid_zero_modes'],3)
        self.assertAlmostEqual(a['softest_eigenvalue'],b['softest_eigenvalue'],places=7)
        self.assertGreater(bare_modes(34)['slowest_amplitude_envelope_time'],a['slowest_amplitude_envelope_time'])

    def test_reduced_profile_matches_engine_for_rotations_and_lengths(self):
        for r in (.5,.65,.8):
            for short in (.9,.92,1.):
                for angle in np.linspace(-2.8,2.8,17):
                    pos=pair_pose(angle,r,short=short)
                    value=bound_port_force(pos,np.array([[0,1,1,0]]),1.,short,4.,.6)[1]
                    expected=local_profile(angle,axial=r,short=short)[0]
                    self.assertAlmostEqual(value,expected,places=12)

    def test_minimum_curvature_and_translation_are_consistent(self):
        _,preferred,kappa=local_profile(0.);step=1e-4
        center=local_profile(preferred)[0]
        measured=(local_profile(preferred+step)[0]-2*center+local_profile(preferred-step)[0])/step**2
        self.assertAlmostEqual(measured,kappa,places=6)
        p=pair_pose(preferred);f,value=bound_port_force(p,np.array([[0,1,1,0]]),1.,.92,4.,.6)
        self.assertLess(np.linalg.norm(f),1e-12)
        shifted=p.copy();shifted[[1,3]]+=[.1,-.2]
        self.assertGreater(bound_port_force(shifted,np.array([[0,1,1,0]]),1.,.92,4.,.6)[1],value)
