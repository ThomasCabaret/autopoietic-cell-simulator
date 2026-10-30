import copy
import tempfile
from pathlib import Path
import unittest
import numpy as np
from experiments.prepare_demo_catalog import origins,langevin_variant
from experiments.prepare_demo_motion import plan
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.motion import MotionAudit
from simulator import checkpoint
from scripts.demo_motion_report import regular,passage,metrics_summary


class DemoMotionTests(unittest.TestCase):
    def test_extended_hooks_are_passive_cache_safe_and_resume_exactly(self):
        configs={r[0]:r[3] for r in origins()}
        from simulator.coupled_bath import membrane_config
        configs['large_membrane']=dict(schema_version=1,model='membrane_bath',seed=2,
            chemistry=membrane_config(configs['integrated_s2']['chemistry']))
        for key in ('free_membrane','material_cycle','integrated_s2','large_membrane'):
            with self.subTest(key=key):
                cfg=langevin_variant(configs[key]);cfg['duration']=.05
                a=Simulation(cfg);b=Simulation(cfg);obs=make_observer(a.config,False)
                a.listeners.extend([obs,MotionAudit(a)])
                brown=copy.deepcopy(cfg);del brown['mechanics']
                np.testing.assert_array_equal(a.chemistry.pos,Simulation(brown).chemistry.pos)
                a.advance(10)
                for _ in range(10):b.motion.force=None;b.advance(1)
                np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
                self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
                with tempfile.TemporaryDirectory() as d:
                    p=Path(d)/'s.npz';checkpoint.save(p,a,obs);c,other=checkpoint.load(p,make_observer)
                a.advance(a.target_step);c.advance(c.target_step)
                np.testing.assert_array_equal(a.chemistry.pos,c.chemistry.pos)
                np.testing.assert_array_equal(a.motion.velocities,c.motion.velocities)
                self.assertEqual(a.rng.bit_generator.state,c.rng.bit_generator.state)
                self.assertEqual(obs.summary(),other.summary())

    def test_bounded_pairs_and_fine_controls_preserve_laws_and_cadences(self):
        tasks=plan()['tasks'];self.assertEqual(len(tasks),16);self.assertEqual(len(plan(True)['tasks']),2)
        for fine in (t for t in tasks if t['comparison']=='fine'):
            cfg=fine['scenario']
            base=next(t['scenario'] for t in tasks if t['preset']==fine['preset'] and
                t['comparison']=='base' and 'mechanics' in t['scenario'])
            self.assertEqual(cfg['chemistry'],base['chemistry'])
            self.assertEqual(cfg['mechanics'],base['mechanics'])
            for cadence in ('sample_every','reaction_every'):
                self.assertEqual(cfg['engine']['dt']*cfg['engine'][cadence],base['engine']['dt']*base['engine'][cadence])
        for t in tasks:
            if 'mechanics' not in t['scenario']:
                mate=next(q for q in tasks if q['preset']==t['preset'] and q['comparison']=='base' and 'mechanics' in q['scenario'])
                self.assertEqual(t['scenario']['chemistry'],mate['scenario']['chemistry'])
                self.assertEqual(t['scenario']['engine'],mate['scenario']['engine'])

    def test_event_sampling_does_not_bias_membrane_fraction_and_absence_is_censored(self):
        h=[dict(time=0.,closed=[]),dict(time=.1,closed=[1]),dict(time=1.,closed=[1]),dict(time=1.,closed=[1]),dict(time=2.,closed=[])]
        self.assertEqual(len(regular(h,1.)),3)
        m=dict(history=h,closed_sets_ever=1,final_closed=[])
        out=metrics_summary(m,dict(model='membrane',duration=2.,engine=dict(dt=.01,sample_every=100)))
        self.assertEqual(out['regular_closed_fraction'],1/3)
        self.assertEqual(passage([], 'hit', 20.),dict(event=False,time=20.))


if __name__=='__main__':unittest.main()
