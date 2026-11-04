import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.config import resolve
from simulator import checkpoint
from experiments.prepare_capture_transfer import scenario,plan
from experiments.prepare_lipid_curvature import scenario as lipid_scenario
from experiments.review_capture_transfer import decide


class CaptureTransferTests(unittest.TestCase):
    def test_initial_material_velocity_rng_match_and_only_curvature_changes(self):
        for seed in range(3):
            a,b,c=[Simulation(scenario(seed,v,.1)) for v in ('legacy','matched','nogene')]
            for other in (b,c):
                np.testing.assert_array_equal(a.chemistry.pos,other.chemistry.pos)
                np.testing.assert_array_equal(a.motion.velocities,other.motion.velocities)
                self.assertEqual(a.rng.bit_generator.state,other.rng.bit_generator.state)
            g=copy.deepcopy(b.config['chemistry']);g.pop('capture_curvature')
            self.assertEqual(a.config['chemistry'],g)
            self.assertEqual(a.chemistry.assembly.catalyst.stiffness,35.)
            self.assertEqual(b.chemistry.assembly.catalyst.stiffness,Simulation(lipid_scenario(seed,'combined')).chemistry.capture.stiffness)
        self.assertEqual(len(plan()['tasks']),9)

    def test_legacy_optional_flag_keeps_dynamics_exact_and_matched_resume(self):
        cfg=scenario(0,'legacy',.4);a=Simulation(cfg)
        cfg['chemistry']['capture_curvature']='legacy';b=Simulation(cfg)
        a.advance(100);b.advance(100)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.chemistry.export(),b.chemistry.export())
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        sim=Simulation(scenario(1,'matched',.4));sim.advance(100)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'capture.npz';checkpoint.save(p,sim);other,_=checkpoint.load(p)
            sim.advance(100);other.advance(100)
            np.testing.assert_array_equal(sim.chemistry.pos,other.chemistry.pos)
            np.testing.assert_array_equal(sim.motion.velocities,other.motion.velocities)
            self.assertEqual(sim.chemistry.export(),other.chemistry.export())
        cfg['chemistry']['capture_curvature']='magic'
        with self.assertRaises(ValueError):resolve(cfg)

    def test_screen_stops_and_rejects_missing_controls_or_activity(self):
        rows=[dict(label=f'CT1_{v}_s{s}',seed=s,G_new=0 if v=='nogene' else 8,F_new=0 if v=='nogene' else 10,
            renewal=dict(active_wholly_constructed_F=0 if v=='nogene' else 2),elapsed_seconds=10.)
            for s in range(3) for v in ('legacy','matched','nogene')]
        self.assertTrue(decide(rows)['screen_passed']);self.assertFalse(decide(rows)['run_transfer'])
        bad=copy.deepcopy(rows);bad[2]['F_new']=1;self.assertFalse(decide(bad)['screen_passed'])
        for r in rows:
            if '_matched_' in r['label']:r['renewal']['active_wholly_constructed_F']=0
        self.assertFalse(decide(rows)['screen_passed'])
        with self.assertRaises(ValueError):decide(rows[:-1])


if __name__=='__main__':unittest.main()
