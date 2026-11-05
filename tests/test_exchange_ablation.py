import copy,unittest
import numpy as np
from experiments.prepare_exchange_ablation import scenario,REFERENCE
from experiments.review_exchange_ablation import decide
from simulator.campaign_io import read
from simulator.engine import Simulation


class ExchangeAblationTests(unittest.TestCase):
    def test_only_exchange_changes_and_initial_mechanics_rng_match(self):
        old=next(t['scenario'] for t in read(REFERENCE/'manifest.json')['tasks'] if t['label']=='CB1_active_s0')
        new=scenario(0);a,b=Simulation(old),Simulation(new)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        np.testing.assert_array_equal(a.motion.velocities,b.motion.velocities)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        expected=copy.deepcopy(a.config);expected.update(name=new['name'],branch='CX1');expected['chemistry']['contact_exchange_rate']=0.
        self.assertEqual(expected,b.config)

    def test_gate_requires_stability_and_preserved_positive_production(self):
        rows=[dict(seed=s,invariant_failures=0,valid_fraction_late=.95,G_new=4,F_new=4,L_new=20,
            reference=dict(G_new=4,F_new=4,L_new=23)) for s in range(3)]
        self.assertTrue(decide(rows)['screen_passed']);rows[0]['valid_fraction_late']=0.
        self.assertFalse(decide(rows)['screen_passed'])

    def test_wider_port_variant_changes_only_width_and_requires_insertions(self):
        old=next(t['scenario'] for t in read(REFERENCE/'manifest.json')['tasks'] if t['label']=='CB1_active_s0')
        new=scenario(0,True);expected=copy.deepcopy(old);expected.update(name=new['name'],branch='CW1');expected['chemistry']['dock_width']=.6
        self.assertEqual(expected,new)
        rows=[dict(label=f'CW1_wide_s{s}',seed=s,invariant_failures=0,valid_fraction_late=.95,G_new=4,F_new=4,L_new=20,inserted_born_inside=0,
            reference=dict(G_new=4,F_new=4,L_new=23)) for s in range(3)]
        self.assertFalse(decide(rows)['screen_passed']);rows[0]['inserted_born_inside']=rows[1]['inserted_born_inside']=1
        self.assertTrue(decide(rows)['screen_passed'])


if __name__=='__main__':unittest.main()
