import copy,unittest
import numpy as np
from simulator.engine import Simulation
from simulator.lipid_geometry_audit import LipidGeometryAudit,settings
from experiments.prepare_competitive_panel import scenario


class LipidGeometryAuditTests(unittest.TestCase):
    def test_sampling_is_passive_and_state_can_resume(self):
        cfg=scenario(0,'assembly');cfg['duration']=.3
        a,b=Simulation(cfg),Simulation(cfg);opts=dict(interval=.05,max_samples=20)
        audit=LipidGeometryAudit(cfg,opts);a.listeners.append(audit)
        a.advance(50);b.advance(50)
        saved=copy.deepcopy(audit.state);a.listeners.remove(audit)
        resumed=LipidGeometryAudit(cfg,opts,saved);a.listeners.append(resumed)
        a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertEqual(a.chemistry.export(),b.chemistry.export())
        self.assertFalse(resumed.summary(a.time)['first_sampled_macro']['event'])
        self.assertIsNone(resumed.state['first_capture'])

    def test_cycle_is_observed_and_capture_is_bounded_once(self):
        cfg=scenario(0,'assembly');sim=Simulation(cfg);c=sim.chemistry;heads,ids,_=c.lipids.layout();n=len(heads)
        a=np.arange(n)*2*np.pi/n;center=np.array([11.,11.]);u=np.column_stack((np.cos(a),np.sin(a)))
        c.pos[heads]=center+8.325*u;c.pos[[c.lipids.rungs[h] for h in heads]]=center+(8.325-.65)*u
        c.lipids.links=[(min(heads[i],heads[(i+1)%n]),max(heads[i],heads[(i+1)%n]),1 if heads[i]<heads[(i+1)%n] else 0,0 if heads[i]<heads[(i+1)%n] else 1) for i in range(n)]
        obs=LipidGeometryAudit(cfg,dict(max_samples=2));obs(0.,c,[]);capture=copy.deepcopy(obs.state['first_capture'])
        obs(5.,c,[]);obs(10.,c,[])
        self.assertTrue(obs.summary(10.)['first_sampled_macro']['event']);self.assertEqual(obs.state['first_macro_sample'],0.)
        self.assertEqual(len(capture['positions']),104);self.assertEqual(obs.state['first_capture'],capture)
        self.assertEqual(len(obs.state['history']),2);self.assertEqual(obs.state['dropped'],1)

    def test_invalid_settings_are_rejected(self):
        for opts in (dict(interval=0),dict(min_units=2),dict(max_samples=10001),dict(min_area=float('nan')),dict(unknown=True)):
            with self.assertRaises(ValueError):settings(opts)
