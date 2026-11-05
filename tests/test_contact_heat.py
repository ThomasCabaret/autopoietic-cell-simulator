import copy,unittest
import numpy as np
from experiments.inspect_contact_heat import potential,Ledger
from tests.test_exchange_energy import context,full_energy


class ContactHeatTests(unittest.TestCase):
    def test_ledger_matches_real_full_potential_and_never_mutates_the_chemistry(self):
        c=context();state=copy.deepcopy(c.lipids.export());pos=c.pos.copy();heads,ids,links=c.lipids.layout()
        self.assertAlmostEqual(sum(potential(c,c.pos[ids],links,heads)),full_energy(c),places=9)
        before=sum(potential(c,c.pos[ids],links,heads));after=[(0,2,1,0)]
        delta=sum(potential(c,c.pos[ids],after,heads))-before
        ledger=Ledger();ledger.change(c,2.,c.pos[ids],links,after,'exchange',delta)
        self.assertAlmostEqual(ledger.events[0]['delta_U'],delta,places=9)
        self.assertAlmostEqual(ledger.totals['exchange']['max_reported_delta_error'],0.,places=12)
        self.assertEqual(c.lipids.export(),state);np.testing.assert_array_equal(c.pos,pos)
        ledger.change(c,2.,c.pos[ids],links,links,'face_update');self.assertEqual(len(ledger.events),1)
