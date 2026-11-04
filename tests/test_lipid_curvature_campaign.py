import copy,unittest
from simulator.engine import Simulation
from experiments.prepare_lipid_curvature import plan,scenario,REFERENCE,VARIANTS
from experiments.review_lipid_curvature import decide
import numpy as np


class CurvatureCampaignTests(unittest.TestCase):
    def test_budget_controls_and_unchanged_kinetics(self):
        p=plan(REFERENCE);self.assertEqual(len(p['tasks']),18)
        self.assertFalse(any(t['scenario']['name'].startswith('L3_reference') for t in p['tasks']))
        a=Simulation(scenario(0,'combined'));b=Simulation(scenario(0,'split'));c=Simulation(scenario(0,'no_boost'))
        for other in (b,c):
            np.testing.assert_array_equal(a.chemistry.pos,other.chemistry.pos)
            self.assertEqual(a.rng.bit_generator.state,other.rng.bit_generator.state)
        ref=scenario(0,'reference')
        self.assertEqual(a.config['mechanics'],ref['mechanics']);self.assertEqual(a.config['engine'],ref['engine'])
        for k in ('food_binding_rate','food_unbinding_rate','rung_catalytic_rate','temperature'):
            self.assertEqual(a.config['chemistry'][k],ref['chemistry'][k])

    def test_thermal_criterion_is_identical_to_L2(self):
        rows=[dict(label=f'L3_{v}_s{s}',seed=s,lipids=8 if v=='combined' else 0,
            max_products_per_site_pair=3,final_lateral_contacts=2,catalyzed=8 if v=='combined' else 0,
            mean_T_late=.08,p95_T_after5=.20) for v in VARIANTS for s in range(3)]
        self.assertTrue(decide(rows)['screen_passed']);self.assertFalse(decide(rows)['run_transfer'])
        bad=copy.deepcopy(rows);next(r for r in bad if r['label']=='L3_combined_s0')['p95_T_after5']=.241
        self.assertFalse(decide(bad)['screen_passed'])
        with self.assertRaises(ValueError):decide(rows[:-1])


if __name__=='__main__':unittest.main()
