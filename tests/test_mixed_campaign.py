import copy,unittest
from experiments.prepare_mixed_synthesis import plan
from experiments.review_mixed_synthesis import decide


class MixedCampaignTests(unittest.TestCase):
    def test_all_twelve_and_whole_tool_transfer_needed_before_any_decision(self):
        rows=[dict(label=f'MX1_{v}_s{s}',seed=s,G_new=0 if v=='nogene' else 9,F_new=0 if v=='nogene' else 10,
            renewal=dict(active_wholly_constructed_F=0 if v=='nogene' else 2),catalyzed_lipids=8 if v in ('mixed','nogene') else 0,
            max_products_per_site_pair=4 if v=='mixed' else 0,new_lipids_later_contacted=4,
            lipids_from_whole_food_F=2 if v=='mixed' else 0,lipids_from_expressed_F=2 if v=='mixed' else 0,
            atom_port_invariant_failures=0) for s in range(3) for v in ('mixed','uncaptured','noHT','nogene')]
        self.assertTrue(decide(rows)['screen_passed']);self.assertFalse(decide(rows)['run_transfer'])
        bad=copy.deepcopy(rows)
        for r in bad:
            if '_mixed_' in r['label']:r['lipids_from_whole_food_F']=0
        self.assertFalse(decide(bad)['screen_passed'])
        bad=copy.deepcopy(rows);bad[1]['catalyzed_lipids']=1;self.assertFalse(decide(bad)['screen_passed'])
        bad=copy.deepcopy(rows);bad[0]['atom_port_invariant_failures']=1;self.assertFalse(decide(bad)['screen_passed'])
        with self.assertRaises(ValueError):decide(rows[:-1])
        self.assertEqual(len(plan()['tasks']),12)


if __name__=='__main__':unittest.main()
