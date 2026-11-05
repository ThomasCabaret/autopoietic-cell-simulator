import copy,unittest
import numpy as np
from experiments.prepare_compact_transfer import scenario,plan
from experiments.review_compact_transfer import decide
from experiments.audit_boundary_access import local_control
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.membrane_bath import in_polygon


class CompactTransferTests(unittest.TestCase):
    def test_geometry_is_analytically_close_and_all_initial_material_is_inside(self):
        a,b=Simulation(scenario(0,'active',.02)),Simulation(scenario(0,'noL',.02))
        c=a.chemistry;self.assertEqual(len(c.pos),302);self.assertEqual(len(b.chemistry.pos),198)
        np.testing.assert_array_equal(c.pos[:198],b.chemistry.pos)
        self.assertTrue(in_polygon(c.pos[:198],c.pos[c.initial_boundary_heads]).all())
        self.assertLess(abs(.92-(1-1.3*np.sin(np.pi/52))),.002)
        obs=make_observer(a.config,False);a.listeners.append(obs);a.advance(10)
        self.assertEqual(obs.invariant_failures,0);self.assertTrue(obs.summary()['boundary']['history'][0]['valid'])
        obs=make_observer(b.config,False);b.listeners.append(obs);b.advance(10)
        self.assertEqual(obs.invariant_failures,0);self.assertNotIn('boundary',obs.summary())
        self.assertEqual(len(plan()['tasks']),9)

    def test_static_access_diagnosis_and_gate_cannot_pass_on_zero_reference(self):
        cfg=scenario(0,'active')['chemistry'];r=local_control(cfg)
        self.assertTrue(r[-2]['exchange_geometric_capture']);self.assertEqual(r[-2]['incoming_attractive_force'],0.)
        rows=[dict(label=f'CB1_{v}_s{s}',seed=s,invariant_failures=0,valid_fraction_late=.9,
            inserted_born_inside=0 if v!='active' else 1,L_new=0 if v=='nosynthesis' else 3,
            G_new=0 if v=='nosynthesis' else 4,F_new=0 if v=='nosynthesis' else 4)
            for s in range(3) for v in ('active','noL','nosynthesis')]
        self.assertTrue(decide(rows)['screen_passed'])
        for r in rows:r['G_new']=0;r['F_new']=0
        self.assertFalse(decide(rows)['screen_passed'])


if __name__=='__main__':unittest.main()
