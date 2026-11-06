import copy,unittest
from simulator.campaign_io import read
from simulator.config import resolve
from experiments.prepare_competitive_horizon import scenario,REFERENCE
from experiments.review_competitive_horizon import decide


class CompetitiveHorizonTests(unittest.TestCase):
    def test_only_duration_and_record_names_change_in_selected_followup(self):
        for seed,variant in [(0,'assembly'),(1,'integrated')]:
            old=next(t['scenario'] for t in read(REFERENCE/'manifest.json')['tasks'] if t['label']==f'CC1_{variant}_s{seed}')
            expected=resolve(copy.deepcopy(old));new=scenario(seed,variant);expected.update(name=new['name'],branch='CH1',duration=1800.)
            self.assertEqual(new,expected)

    def test_small_cycle_or_selected_only_success_cannot_certify_the_panel(self):
        rows=[dict(variant='assembly',seed=s,final_ports_valid=True,late_temperature=.08,simple_contours=[dict(units=30,area=80.)]) for s in range(3)]
        rows.append(dict(variant='integrated',seed=1,final_ports_valid=True,invariant_failures=0,late_temperature=.08,
            valid_fraction_late=.9,G_new=3,F_new=4,L_new=10))
        self.assertTrue(decide(rows)['screen_passed'])
        for r in rows[:3]:r['simple_contours']=[dict(units=10,area=80.)]
        self.assertFalse(decide(rows)['screen_passed'])
