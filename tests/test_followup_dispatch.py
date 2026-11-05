import sys,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import boundary_transfer_followup as driver
from experiments import review_compact_transfer,review_boundary_transfer


class FollowupDispatchTests(unittest.TestCase):
    def test_job_gate_selects_correct_analyzer_even_when_shell_loses_mode(self):
        for gate,collect,decide in (('CB1_BATCH_44_PLAN',review_compact_transfer.collect,review_compact_transfer.decide),
                                   ('BI1_BATCH_43_PLAN',review_boundary_transfer.collect,review_boundary_transfer.decide)):
            with patch.object(sys,'argv',['driver','run','--job','example']),patch.object(driver.controller,'validate_job',return_value={'gate':gate}),patch.object(driver.controller,'run') as run:
                driver.main();run.assert_called_once_with(Path('example'),collect,decide)

    def test_conflicting_explicit_mode_is_rejected(self):
        with patch.object(sys,'argv',['driver','run','--job','example','--compact']),patch.object(driver.controller,'validate_job',return_value={'gate':'BI1_BATCH_43_PLAN'}),patch.object(driver.controller,'run') as run:
            with self.assertRaisesRegex(ValueError,'contradicts'):driver.main()
            run.assert_not_called()


if __name__=='__main__':unittest.main()
