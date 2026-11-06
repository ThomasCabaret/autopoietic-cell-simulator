import unittest
from unittest.mock import Mock,patch
from scripts import campaign
from scripts.recover_followup_monitor import retry_read


class ReadRetryTests(unittest.TestCase):
    def test_transient_read_preserves_result_and_retries_only_io(self):
        for mode in ('campaign','recovery'):
            reader=Mock(side_effect=[PermissionError('sharing'),PermissionError('sharing'),{'time':42}])
            with patch.object(campaign.os,'name','nt'),patch.object(campaign.time,'sleep') as sleep:
                if mode=='campaign':
                    with patch.object(campaign,'read_record',reader):result=campaign.read('state')
                else:result=retry_read(reader,'state')
                self.assertEqual(result,{'time':42});self.assertEqual(reader.call_count,3);self.assertEqual(sleep.call_count,2)

    def test_permanent_and_non_io_failure_are_not_hidden(self):
        with patch.object(campaign.os,'name','nt'),patch.object(campaign.time,'sleep'):
            reader=Mock(side_effect=PermissionError('persistent'))
            with self.assertRaises(PermissionError):retry_read(reader,'state')
            self.assertEqual(reader.call_count,7)
            reader=Mock(side_effect=ValueError('bad JSON'))
            with self.assertRaises(ValueError):retry_read(reader,'state')
            self.assertEqual(reader.call_count,1)
