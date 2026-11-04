import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.spatial import Neighborhood
from simulator import checkpoint
from simulator.transition_energy import formation_energy
from experiments.prepare_lipid_energy import scenario
from experiments.diagnose_capture_heat import elastic
from experiments.diagnose_lipid_heat import energy
from tests.test_transition_energy import local_pose,config


class CaptureCurvatureTests(unittest.TestCase):
    def test_native_initialization_removes_F_elastic_energy_and_matches_split(self):
        cfg=scenario(0,'combined');a=Simulation(cfg)
        cfg['chemistry']['tool_pose']='native';b=Simulation(cfg)
        cfg['chemistry']['tool_linked']=False;d=Simulation(cfg)
        np.testing.assert_array_equal(b.chemistry.pos,d.chemistry.pos)
        self.assertEqual(b.rng.bit_generator.state,d.rng.bit_generator.state)
        n=a.chemistry.n;prefix=a.chemistry.prefix
        np.testing.assert_array_equal(a.chemistry.pos[:n],b.chemistry.pos[:n])
        np.testing.assert_array_equal(a.chemistry.pos[prefix:],b.chemistry.pos[prefix:])
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        a.prepare();b.prepare()
        self.assertAlmostEqual(elastic(a.chemistry)['angles'],51.2)
        self.assertLess(elastic(b.chemistry)['angles'],1e-20)
        self.assertLess(elastic(b.chemistry)['springs'],1e-20)

    def test_matching_uses_existing_curvature_and_exact_local_energy(self):
        cfg=config();cfg['chemistry']['capture_curvature']='matched';sim=Simulation(cfg);c=sim.chemistry
        self.assertAlmostEqual(c.capture.stiffness,2./.6**2);local_pose(c)
        self.assertTrue(all(s[2]==c.capture.stiffness for s in c.capture.springs(c)))
        before=energy(c);delta=formation_energy(c,4,10,Neighborhood('brute'))
        c.lipids.bind(4,10);c.capture.categories[[4,10]]=-1;c.capture.release(4);c.capture.release(10)
        after=energy(c)
        for k in before:self.assertAlmostEqual(delta[k],after[k]-before[k],places=10)

    def test_both_options_resume_exactly_with_derived_stiffness(self):
        cfg=scenario(1,'combined');cfg['duration']=.2;cfg['chemistry'].update(capture_curvature='matched',tool_pose='native')
        a=Simulation(cfg);obs=make_observer(a.config,False);a.listeners.append(obs);a.advance(40)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'curvature.npz';checkpoint.save(p,a,obs);b,newobs=checkpoint.load(p,make_observer)
            a.advance(60);b.advance(60)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos);np.testing.assert_array_equal(a.motion.velocities,b.motion.velocities)
            self.assertEqual(a.chemistry.capture.stiffness,b.chemistry.capture.stiffness)
            self.assertEqual(a.chemistry.export(),b.chemistry.export());self.assertEqual(obs.summary(),newobs.summary())


if __name__=='__main__':unittest.main()
