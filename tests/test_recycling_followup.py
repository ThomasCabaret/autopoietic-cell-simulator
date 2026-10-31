import copy,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts.recycling_followup import decide
from scripts.expression_followup import step
from simulator.campaign_io import write,read


def rows():
    return [dict(label=f'RV1_{v}_s{s}',seed=s,invariant_failures=0,
        final=dict(invariants_valid=True,detached_targets=dict(G=1)),polymer_reassemblies=1,
        recycled_incorporations=1,catalyzed_formations=10)
        for v in ('zero','backbone','full','protected') for s in range(3)]


class RecyclingGateTests(unittest.TestCase):
    def test_gate_requires_material_path_survival_and_activity(self):
        self.assertTrue(decide(rows())['run_transfer'])
        for field,value in [('polymer_reassemblies',0),('recycled_incorporations',0),('catalyzed_formations',0)]:
            data=rows()
            for r in data[-3:]:r[field]=value
            self.assertFalse(decide(data)['run_transfer'])
        data=rows();data[-1]['final']['detached_targets']['G']=0
        self.assertFalse(decide(data)['run_transfer'])
        data=rows();data[0]['invariant_failures']=1
        self.assertFalse(decide(data)['run_transfer'])
        with self.assertRaises(ValueError):decide(rows()[:-1])

    def test_gate_dispatch_stops_or_advances_without_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            job=Path(tmp);cfg=dict(campaigns=[str(job/'A'),str(job/'B')])
            snap=dict(counts=dict(failed=0,paused=0,interrupted=0,complete=12),tasks=[{}]*12,controller_active=False)
            for r in snap['tasks']:r['worker_active']=False
            for passed in (False,True):
                write(job/'state.json',dict(phase='running_0',stage=0))
                with patch('scripts.expression_followup.validate_job',return_value=cfg),patch(
                    'scripts.expression_followup.campaign_status',return_value=snap),patch(
                    'scripts.expression_followup.subprocess.Popen') as spawn:
                    result=step(job,lambda _:dict(rows=rows()),lambda _:dict(run_transfer=passed))
                    self.assertEqual(result,'ready_B' if passed else 'needs_interpretation')
                    self.assertEqual(read(job/'state.json')['stage'],1 if passed else 0)
                    spawn.assert_not_called()


if __name__=='__main__':unittest.main()
