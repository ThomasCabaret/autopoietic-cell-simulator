import copy,unittest
import numpy as np
from experiments.prepare_exchange_refinement import scenario,REFERENCE
from experiments.review_exchange_refinement import decide
from simulator.campaign_io import read
from simulator.engine import Simulation
from simulator.config import resolve


class ExchangeRefinementTests(unittest.TestCase):
    def test_only_discretization_changes_with_identical_initial_states_and_physical_cadences(self):
        old=read(REFERENCE/'manifest.json')['tasks'][0]['scenario'];new=scenario(old['seed'])
        expected=resolve(copy.deepcopy(old));expected.update(name=new['name'],branch='EN1')
        expected['engine']['dt']/=2
        for key in ('reaction_every','sample_every'):expected['engine'][key]*=2
        self.assertEqual(new,expected)
        for key in ('reaction_every','sample_every'):
            self.assertEqual(new['engine'][key]*new['engine']['dt'],old['engine'][key]*old['engine']['dt'])
        a,b=Simulation(old),Simulation(new)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        np.testing.assert_array_equal(a.motion.velocities,b.motion.velocities)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)

    def test_sensitivity_gate_keeps_thermal_and_insertion_failures_visible(self):
        rows=[dict(seed=s,invariant_failures=0,valid_fraction_late=.94,late_temperature=.08,
            inserted_born_inside=1 if s!=1 else 0,G_new=8,F_new=9,L_new=23,
            reference=dict(G_new=8,F_new=9,L_new=23),exchange_gate_stats=dict(proposals=2,accepted=1,rejected=1)) for s in range(3)]
        self.assertTrue(decide(rows)['screen_passed'])
        rows[0]['late_temperature']=.2;self.assertFalse(decide(rows)['screen_passed'])
        rows[0]['late_temperature']=.08;rows[0]['inserted_born_inside']=0
        self.assertFalse(decide(rows)['screen_passed'])
