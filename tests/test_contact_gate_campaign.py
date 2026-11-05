import copy,unittest
import subprocess,tempfile
from pathlib import Path
from unittest.mock import patch
from experiments.prepare_contact_gate import scenario,REFERENCES
from experiments.review_contact_gate import decide
from simulator.campaign_io import read
from simulator.config import resolve


class ContactGateCampaignTests(unittest.TestCase):
    def test_pilot_timeout_requests_worker_pause_and_never_starts_the_cohort(self):
        import experiments.prepare_contact_gate as module
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);folder=root/'pilot';folder.mkdir()
            with patch.object(module,'ROOT',root),patch.object(module,'scenario',return_value={}),\
                    patch('scripts.campaign.prepare',return_value=folder),patch('scripts.campaign.export_recipe'),\
                    patch.object(module.subprocess,'run',side_effect=subprocess.TimeoutExpired('pilot',900)) as run:
                with self.assertRaisesRegex(ValueError,'timed out'):module.ensure_pilot()
                self.assertTrue((folder/'STOP').exists());self.assertEqual(run.call_count,1)

    def test_both_step_cases_only_add_the_declared_contact_option(self):
        for scale in ('coarse','fine'):
            old=resolve(next(t['scenario'] for t in read(REFERENCES[scale]/'manifest.json')['tasks'] if t['scenario']['seed']==0))
            new=scenario(0,scale);expected=copy.deepcopy(old);expected.update(name=new['name'],branch='CF1')
            expected['chemistry']['contact_update_gate']='metropolis';self.assertEqual(new,expected)

    def test_success_at_one_dt_cannot_hide_failure_at_the_other(self):
        rows=[dict(scale=scale,seed=s,invariant_failures=0,valid_fraction_late=.95,late_temperature=.08,
            inserted_born_inside=1,G_new=8,F_new=9,L_new=23,reference=dict(G_new=8,F_new=9,L_new=23),
            contact_update_stats={k:dict(proposals=3,accepted=2,rejected=1) for k in ('formation','breaking')})
            for scale in ('coarse','fine') for s in range(3)]
        self.assertTrue(decide(rows)['screen_passed']);rows[-1]['late_temperature']=.2
        self.assertFalse(decide(rows)['screen_passed']);rows[-1]['late_temperature']=.08
        for r in rows:
            if r['scale']=='fine':r['inserted_born_inside']=0
        self.assertFalse(decide(rows)['screen_passed'])
