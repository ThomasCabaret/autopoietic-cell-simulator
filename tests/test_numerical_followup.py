import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch,MagicMock
from simulator.campaign_io import write,read
from scripts.numerical_followup import step,decision


def snapshot(phase='complete',active=False):
    counts={k:int(k==phase) for k in ('pending','running','complete','failed','paused','interrupted')}
    return dict(counts=counts,controller_active=active,tasks=[dict(worker_active=active)])


class FollowupTests(unittest.TestCase):
    def test_incomplete_or_only_coarse_alerts_cannot_trigger_N2(self):
        with self.assertRaises(ValueError):decision(dict(triage=dict(complete_cohorts=False,alerts=[dict(to_factor=4)])))
        self.assertFalse(decision(dict(triage=dict(complete_cohorts=True,alerts=[dict(to_factor=2)]))))
        self.assertTrue(decision(dict(triage=dict(complete_cohorts=True,alerts=[dict(to_factor=4)]))))

    def test_waiting_or_parent_failure_never_launches(self):
        with tempfile.TemporaryDirectory() as d:
            job=Path(d);cfg=dict(parent=d,child=d,baseline=d)
            with patch('scripts.numerical_followup.validate_job',return_value=cfg),patch('scripts.numerical_followup.compare_n1') as analyze,patch('scripts.numerical_followup.subprocess.Popen') as launch:
                with patch('scripts.numerical_followup.campaign_status',return_value=snapshot('running',True)):
                    self.assertEqual(step(job),'waiting_N1')
                with patch('scripts.numerical_followup.campaign_status',return_value=snapshot('failed')):
                    self.assertEqual(step(job),'needs_attention')
                analyze.assert_not_called();launch.assert_not_called()

    def test_favorable_gate_stops_for_interpretation(self):
        with tempfile.TemporaryDirectory() as d:
            job=Path(d);report=job/'analysis';report.mkdir()
            write(report/'report.json',dict(triage=dict(complete_cohorts=True,alerts=[])))
            cfg=dict(parent=d,child=d,baseline=d)
            with patch('scripts.numerical_followup.validate_job',return_value=cfg),patch('scripts.numerical_followup.compare_n1',return_value=report) as analyze,patch('scripts.numerical_followup.campaign_status',return_value=snapshot()),patch('scripts.numerical_followup.subprocess.Popen') as launch:
                self.assertEqual(step(job),'needs_interpretation')
                self.assertEqual(step(job),'needs_interpretation')
                self.assertEqual(analyze.call_count,1);launch.assert_not_called()

    def test_trigger_launches_once_and_never_oversubscribes_parent(self):
        with tempfile.TemporaryDirectory() as d:
            job=Path(d);report=job/'analysis';report.mkdir()
            write(report/'report.json',dict(triage=dict(complete_cohorts=True,alerts=[dict(to_factor=4)])))
            cfg=dict(parent=d,child=d,baseline=d)
            with patch('scripts.numerical_followup.validate_job',return_value=cfg),patch('scripts.numerical_followup.compare_n1',return_value=report),patch('scripts.numerical_followup.subprocess.Popen',return_value=MagicMock(pid=123)) as launch:
                with patch('scripts.numerical_followup.campaign_status',return_value=snapshot(active=True)):
                    self.assertEqual(step(job),'waiting_N1');launch.assert_not_called()
                with patch('scripts.numerical_followup.campaign_status',side_effect=[snapshot(),snapshot('pending'),snapshot(),snapshot('pending')]):
                    self.assertEqual(step(job),'launching_N2')
                    self.assertEqual(step(job),'launching_N2')
                self.assertEqual(launch.call_count,1)
                (job/'STOP').write_text('pause')
                self.assertEqual(step(job),'paused')
                self.assertTrue(read(job/'state.json')['run_N2'])
