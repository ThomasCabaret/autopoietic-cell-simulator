import unittest
import numpy as np
from experiments.prepare_product_binding import scenario,preflight,plan
from experiments.review_product_binding import decide
from simulator.engine import Simulation


class ProductBindingTests(unittest.TestCase):
    def test_assay_has_only_prepared_material_and_matched_connectivity_controls(self):
        a,b=Simulation(scenario(0,'linked4')),Simulation(scenario(0,'split4'))
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos);np.testing.assert_array_equal(a.motion.velocities,b.motion.velocities)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertTrue((a.chemistry.rungs[:,1]>=0).all());self.assertFalse(a.chemistry.config['ligation'])
        self.assertEqual(a.chemistry.config['rung_formation_rate'],0.)
        self.assertEqual((len(a.chemistry.pos),len(a.chemistry.edges),len(b.chemistry.edges)),(20,5,1))

    def test_signal_gate_does_not_relabel_binding_as_homeostasis(self):
        rows=[dict(variant=v,seed=s,occupied_G_fraction=0. if v=='zero' else .3,new_backbone_links=0,new_composites=0)
            for s in range(3) for v in ('zero','linked4','split4','linked16','split16')]
        result=decide(rows);self.assertTrue(result['screen_passed']);self.assertFalse(result['run_transfer'])
        rows[0]['occupied_G_fraction']=.1;self.assertFalse(decide(rows)['screen_passed'])

    def test_actual_eligibility_preflight_blocks_repeating_an_unreachable_mechanism(self):
        result=preflight();self.assertEqual(result['linked16']['eligible_GF'],0)
        self.assertGreater(result['linked16']['geometric_product_contacts'],0)
        self.assertGreater(result['linked16']['blocked_family_degree'],0)
        self.assertGreater(result['split16']['eligible_GF'],0)
        with self.assertRaisesRegex(ValueError,'excluded'):plan()
