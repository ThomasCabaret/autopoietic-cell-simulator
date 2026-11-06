import copy,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from simulator.engine import Simulation
from simulator.campaign_io import read,write
from simulator.campaign_worker import execute
from scripts.campaign import prepare
from experiments.prepare_competitive_relaxation import scenario,plan,REFERENCE
from experiments.review_competitive_relaxation import decide
from simulator.lipid_geometry_audit import LipidGeometryAudit


class CompetitiveRelaxationTests(unittest.TestCase):
    def test_only_horizon_names_and_observation_change(self):
        for seed in range(3):
            expected=copy.deepcopy(next(q['scenario'] for q in read(REFERENCE/'manifest.json')['tasks'] if q['label']==f'CH1_assembly_s{seed}'))
            actual=scenario(seed);expected.update(name=actual['name'],branch='CR1',duration=8000.)
            self.assertEqual(actual,expected)
        p=plan();self.assertEqual(len(p['tasks']),3);self.assertFalse(p['record_trajectory'])

    def test_gate_requires_persistence_final_geometry_and_complete_observation(self):
        rows=[dict(seed=s,final_ports_valid=True,geometry_dropped=0,late_temperature=.08,
            macro_fraction_late=.6,simple_contours=[dict(units=30,area=80.)]) for s in range(3)]
        self.assertTrue(decide(rows)['screen_passed'])
        rows[0]['macro_fraction_late']=.1;rows[1]['simple_contours']=[]
        self.assertFalse(decide(rows)['screen_passed'])
        rows[0]['macro_fraction_late']=.6;rows[0]['geometry_dropped']=1
        self.assertFalse(decide(rows)['screen_passed'])

    def test_worker_writes_and_resumes_the_passive_geometry_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);cfg=scenario(0);cfg['duration']=1.
            options=dict(interval=.1,max_samples=20)
            write(root/'plan.json',dict(workers=1,checkpoint_seconds=.05,record_trajectory=False,
                lipid_geometry_audit=options,tasks=[dict(scenario=cfg)]))
            folder=prepare(root/'plan.json',root/'campaigns');original=Simulation.advance
            def interrupted(sim,steps=1):
                result=original(sim,steps)
                if sim.step_index>=250:(folder/'STOP').write_text('pause')
                return result
            with patch.object(Simulation,'advance',interrupted):execute(folder,'task0000')
            state=read(folder/'tasks/task0000/state.json');self.assertEqual(state['status'],'paused')
            self.assertIn('lipid_geometry',state);(folder/'STOP').unlink();execute(folder,'task0000')
            state=read(folder/'tasks/task0000/state.json');self.assertEqual(state['status'],'complete')
            ref=Simulation(cfg);obs=LipidGeometryAudit(cfg,options);ref.listeners.append(obs);ref.advance(ref.target_step)
            with np.load(folder/state['checkpoint']) as data:np.testing.assert_array_equal(data['positions'],ref.chemistry.pos)
            self.assertEqual(read(folder/state['lipid_geometry']),obs.summary(ref.time))
