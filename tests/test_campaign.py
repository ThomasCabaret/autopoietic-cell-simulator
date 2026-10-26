import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from scripts.campaign import prepare,validate,status,run,analyze,survival,export_recipe,restore_recipe
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.kinetics import KineticProbe
from simulator.campaign_worker import execute
from simulator.campaign_io import read,write,lock,busy


def scenario():
    return dict(schema_version=1,model='membrane_bath',name='kinetic_test',seed=2,duration=3.,
        engine=dict(sample_every=100),chemistry=dict(units=44,ring_units=40,ring_radius=6.3,box=[26.,26.],
            retained_probes=8,permeable_probes=8,contact_exchange_rate=1e6))


class CampaignTests(unittest.TestCase):
    def prepare(self,d):
        plan=Path(d)/'plan.json';write(plan,dict(workers=1,checkpoint_seconds=.05,tasks=[dict(scenario=scenario())]))
        return prepare(plan,Path(d)/'campaigns')

    def test_probe_detects_eligible_geometry_without_affecting_rng_or_dynamics(self):
        a=Simulation(scenario());b=Simulation(scenario())
        for c in (a.chemistry,b.chemistry):
            n=c.n;c.pos[40]=c.pos[0]+.7*(c.pos[1]-c.pos[0])+[-.30,0.]
            c.pos[n+40]=c.pos[40]+c.pos[n]-c.pos[0]
        probe=KineticProbe(a.config);self.assertGreater(probe.scan(a.chemistry)['exchange_faces'],0)
        probe.attach(a.chemistry);a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertEqual(a.chemistry.export(),b.chemistry.export())

    def test_stop_resume_is_exact_including_diagnostic_exposure(self):
        with tempfile.TemporaryDirectory() as d:
            folder=self.prepare(d);original=Simulation.advance
            def advance(sim,steps=1):
                result=original(sim,steps)
                if sim.step_index>=500:(folder/'STOP').write_text('stop')
                return result
            with patch.object(Simulation,'advance',advance):execute(folder,'task0000')
            state=read(folder/'tasks/task0000/state.json');self.assertEqual(state['status'],'paused')
            self.assertGreater(state['step'],0);(folder/'STOP').unlink();execute(folder,'task0000')
            state=read(folder/'tasks/task0000/state.json');self.assertEqual(state['status'],'complete')
            ref=Simulation(scenario());obs=make_observer(ref.config,False);ref.listeners.append(obs)
            probe=KineticProbe(ref.config,window=25.);probe.attach(ref.chemistry);ref.advance(ref.target_step)
            with np.load(folder/state['checkpoint']) as data:np.testing.assert_array_equal(data['positions'],ref.chemistry.pos)
            self.assertEqual(read(folder/state['result'])['metrics'],json.loads(json.dumps(obs.summary())))
            self.assertEqual(read(folder/state['kinetics']),json.loads(json.dumps(probe.summary(ref.time,obs.summary()))))
            self.assertEqual(analyze(folder)['completed'],1)
            self.assertEqual(status(folder)['counts']['complete'],1)

    def test_os_lock_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as d:
            folder=self.prepare(d);self.assertFalse(busy(folder/'worker.lock'))
            with lock(folder/'worker.lock'):self.assertTrue(busy(folder/'worker.lock'))
            validate(folder)
            p=folder/'runtime/simulator/engine.py';p.write_bytes(p.read_bytes()+b'\n# changed\n')
            with self.assertRaises(ValueError):validate(folder)

    def test_source_only_recipe_restores_without_states_or_results(self):
        with tempfile.TemporaryDirectory() as d:
            folder=self.prepare(d);(folder/'STOP').write_text('stop')
            write(folder/'tasks/task0000/state.json',dict(status='failed',error='old result'))
            recipe=export_recipe(folder,Path(d)/'recipe');restored=restore_recipe(recipe,Path(d)/'restored')
            self.assertEqual(validate(restored),validate(folder))
            self.assertFalse((restored/'STOP').exists());self.assertFalse((restored/'tasks').exists())

    def test_censoring_and_saturation_are_not_successes(self):
        curve=survival([dict(time=1.,event=True),dict(time=2.,event=False)])
        self.assertEqual(curve[0]['survival'],.5);self.assertEqual(curve[-1]['survival'],.5)
        s=Simulation(scenario());probe=KineticProbe(s.config)
        metrics=dict(history=[]);r=probe.summary(3.,metrics)
        self.assertFalse(r['first_passages']['closed_insertion']['event'])
        self.assertEqual(r['first_passages']['closed_insertion']['time'],3.)

    def test_running_record_without_live_lock_is_interrupted(self):
        with tempfile.TemporaryDirectory() as d:
            folder=self.prepare(d);dest=folder/'tasks/task0000'
            write(dest/'state.json',dict(status='running',updated=0))
            self.assertEqual(status(folder)['tasks'][0]['phase'],'interrupted')
            with lock(dest/'worker.lock'):
                self.assertEqual(status(folder)['tasks'][0]['phase'],'running')

    def test_frozen_subprocess_run_and_completed_task_is_not_restarted(self):
        with tempfile.TemporaryDirectory() as d:
            folder=self.prepare(d);self.assertEqual(run(folder),0)
            state=read(folder/'tasks/task0000/state.json');self.assertEqual(state['status'],'complete')
            before=(folder/'tasks/task0000/state.json').read_bytes();self.assertEqual(run(folder),0)
            self.assertEqual((folder/'tasks/task0000/state.json').read_bytes(),before)


if __name__=='__main__':unittest.main()
