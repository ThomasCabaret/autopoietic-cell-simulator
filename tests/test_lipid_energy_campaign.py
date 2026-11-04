import copy,tempfile,time,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from simulator.engine import Simulation
from simulator.campaign_io import write,read
from experiments.prepare_lipid_energy import scenario,plan,VARIANTS,REFERENCE
from experiments.review_lipid_energy import decide
from scripts.expression_followup import step


class LipidEnergyCampaignTests(unittest.TestCase):
    def test_twenty_new_cases_and_matched_initial_controls(self):
        p=plan(REFERENCE);self.assertEqual(len(p['tasks']),20)
        self.assertNotIn('L2_reference_s0',[t['scenario']['name'] for t in p['tasks']])
        sims={v:Simulation(scenario(0,v)) for v in VARIANTS}
        a=sims['combined']
        for v,b in sims.items():
            if v!='no_tool':
                np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
                self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertEqual(len(sims['no_tool'].chemistry.pos),48)
        self.assertEqual(a.config['mechanics'],sims['reference'].config['mechanics'])
        self.assertEqual(a.config['engine'],sims['reference'].config['engine'])

    def test_gate_requires_usefulness_and_thermal_bounds_not_merely_more_products(self):
        rows=[dict(label=f'L2_{v}_s{s}',seed=s,lipids=8 if v=='combined' else 1,
            catalyzed=0 if v in ('split','no_tool') else 1,max_products_per_site_pair=2,
            final_lateral_contacts=2,mean_T_late=.08,p95_T_after5=.12) for v in VARIANTS for s in range(3)]
        self.assertTrue(decide(rows)['screen_passed']);self.assertFalse(decide(rows)['run_transfer'])
        bad=copy.deepcopy(rows);next(r for r in bad if r['label']=='L2_combined_s1')['mean_T_late']=.2
        self.assertFalse(decide(bad)['screen_passed'])
        bad=copy.deepcopy(rows);next(r for r in bad if r['label']=='L2_split_s0')['catalyzed']=1
        self.assertFalse(decide(bad)['screen_passed'])
        with self.assertRaises(ValueError):decide(rows[:-1])

    def test_one_hour_budget_pauses_instead_of_launching(self):
        with tempfile.TemporaryDirectory() as d:
            job=Path(d);folder=job/'A';folder.mkdir()
            write(job/'state.json',dict(phase='running_0',stage=0,first_launch=time.time()-3601))
            cfg=dict(campaigns=[str(folder)],max_wall_seconds=3600)
            with patch('scripts.expression_followup.validate_job',return_value=cfg),\
                patch('scripts.expression_followup.subprocess.Popen') as launch:
                self.assertEqual(step(job),'needs_attention');launch.assert_not_called()
                self.assertIn('3600s',read(job/'state.json')['reason'])
                self.assertTrue((folder/'STOP').exists())


if __name__=='__main__':unittest.main()
