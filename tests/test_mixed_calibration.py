import unittest
from experiments.mixed_calibration import stock_at,weighted
from experiments.review_cooperative_synthesis import decide
from experiments.prepare_cooperative_synthesis import plan


class MixedCalibrationTests(unittest.TestCase):
    def test_typed_stocks_reconstruct_actual_partners_at_requested_times(self):
        cfg=dict(chemistry=dict(food_units=1,genetics=dict(sequence='01',seed_family=0,free_units=1,function_units=1)))
        assembly=dict(rungs=[[0,4],[1,5],[2,7],[3,-1]],initial_supports=[0,1],atom_bits=[0,1,0,1],
            events=[dict(time=2.,support=2,recognizer=7,symbol=1)])
        lipid=[dict(time=3.,head=8,tail=9)]
        self.assertEqual(stock_at(cfg,assembly,lipid,1.),dict(P_G=1,P_F=1,R0=1,R1=1,H=1,T=1))
        self.assertEqual(stock_at(cfg,assembly,lipid,2.),dict(P_G=0,P_F=1,R0=1,R1=0,H=1,T=1))
        self.assertEqual(stock_at(cfg,assembly,lipid,3.)['H'],0)
        cfg['chemistry']['initial_boundary']=dict(units=219)
        self.assertEqual(stock_at(cfg,assembly,lipid,1.),dict(P_G=1,P_F=1,R0=1,R1=1,H=1,T=1))
        history=[dict(time=0.,x=0.),dict(time=9.,x=1.),dict(time=10.,x=1.)]
        self.assertAlmostEqual(weighted(history,'x',0.,10.),.1)
        self.assertAlmostEqual(weighted(history,'x',5.,10.),.2)

    def test_mx2_gate_requires_matched_horizon_improvement_and_zero_crossed_time(self):
        rows=[dict(label=f'MX2_{v}_s{s}',seed=s,G_new=2 if v=='reference' else (0 if v=='nogene' else 8),
            F_new=0 if v=='nogene' else 10,renewal=dict(active_wholly_constructed_F=1),
            catalyzed_lipids=0 if v=='noHT' else 8,new_lipids_later_contacted=4,
            lipids_from_whole_food_F=0 if v=='nogene' else 3,lipids_from_expressed_F=0 if v=='nogene' else 3,
            sampled_wrong_double_edge_time=0.,atom_port_invariant_failures=0)
            for s in range(3) for v in ('cooperative','reference','nogene','noHT')]
        self.assertTrue(decide(rows)['screen_passed']);self.assertFalse(decide(rows)['run_transfer'])
        rows[0]['sampled_wrong_double_edge_time']=.01;self.assertFalse(decide(rows)['screen_passed'])
        self.assertEqual(len(plan()['tasks']),12)


if __name__=='__main__':unittest.main()
