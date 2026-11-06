import unittest
from experiments.prepare_competitive_panel import scenario
from experiments.review_competitive_panel import decide
from simulator.engine import Simulation
from simulator.lipid_synthesis import DEFAULTS


class CompetitivePanelTests(unittest.TestCase):
    def test_isolated_control_shares_L_laws_but_no_prepared_lateral_chain_or_tools(self):
        a,b=scenario(0,'integrated'),scenario(0,'assembly');sa,sb=Simulation(a),Simulation(b)
        self.assertEqual((len(sa.chemistry.pos),len(sb.chemistry.pos)),(302,104))
        self.assertEqual(len(sb.chemistry.lipids.rungs),52);self.assertEqual(sb.chemistry.lipids.links,[])
        self.assertEqual(sb.chemistry.n,0);self.assertEqual(sb.chemistry.births,[])
        for key in DEFAULTS:
            if key not in ('initial_lipids','food_units','tool_count','tool_linked','tool_pose'):
                self.assertEqual(a['chemistry'].get(key,DEFAULTS[key]),b['chemistry'][key],key)

    def test_association_gate_does_not_claim_vesicle_or_late_insertion(self):
        rows=[dict(variant=v,seed=s,final_ports_valid=True,invariant_failures=0 if v=='integrated' else None,
            late_temperature=.08,valid_fraction_late=.9 if v=='integrated' else None,largest_component=4,lateral_contacts=3)
            for v in ('integrated','assembly') for s in range(3)]
        result=decide(rows);self.assertTrue(result['screen_passed']);self.assertFalse(result['run_transfer'])
        rows[-1]['largest_component']=1;self.assertFalse(decide(rows)['screen_passed'])
