import copy,hashlib,json,tempfile,time,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator import checkpoint
from visualizer.checkpoints import snapshot_checkpoint
from visualizer.worker import ProcessSource
from visualizer.local_runs import available


def prepared(path):
    cfg=dict(schema_version=1,model='copy',seed=2,duration=.08,
        chemistry=dict(sequence='001',free_units=3),engine=dict(dt=.005,sample_every=5))
    sim=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs);sim.advance(7)
    checkpoint.save(path,sim,obs);return sim,obs


class CheckpointViewerTests(unittest.TestCase):
    def test_import_preserves_original_and_refuses_incompatible_source_or_task(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=root/'original.npz';sim,_=prepared(path);original=path.read_bytes()
            imported=snapshot_checkpoint(path,root/'view',sim.config)
            self.assertEqual(Path(imported['snapshot']).read_bytes(),original);self.assertEqual(path.read_bytes(),original)
            self.assertEqual(imported['sha256'],hashlib.sha256(original).hexdigest());self.assertEqual(imported['step'],7)
            wrong=copy.deepcopy(sim.config);wrong['seed']=3
            with self.assertRaisesRegex(ValueError,'tâche'):snapshot_checkpoint(path,root/'view',wrong)
            with np.load(path) as data:arrays={k:data[k].copy() for k in data.files}
            meta=json.loads(str(arrays['metadata']));meta['source_sha256']['simulator/engine.py']='changed'
            arrays['metadata']=json.dumps(meta);np.savez(root/'old.npz',**arrays)
            with self.assertRaisesRegex(ValueError,'moteur différente'):snapshot_checkpoint(root/'old.npz',root/'view')

    def test_process_opens_paused_at_saved_step_and_continues_exactly(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=root/'original.npz';ref,obs=prepared(path);initial=ref.chemistry.pos.copy()
            imported=snapshot_checkpoint(path,root/'view');ref.advance(ref.target_step)
            # Campaign replaces original after import: viewer must keep frozen step7.
            checkpoint.save(path,ref,obs);original=path.read_bytes()
            source=ProcessSource(ref.config,root/'view',imported['snapshot'])
            def wait(predicate):
                end=time.monotonic()+45
                while time.monotonic()<end:
                    for packet in source.poll():
                        self.assertNotIn('error',packet,packet.get('error'))
                        if predicate(packet):return packet
                    time.sleep(.01)
                self.fail('Checkpoint viewer worker timeout')
            try:
                first=wait(lambda p:True);self.assertTrue(first['paused']);self.assertEqual(first['frame'].step,7)
                self.assertEqual(first['events'],[]);np.testing.assert_array_equal(first['frame'].positions,initial.astype('f4'))
                source.command('step');wait(lambda p:p['frame'].step==8)
                source.command('speed',0.);source.command('pause',False);last=wait(lambda p:p['frame'].done)
                saved,observed=checkpoint.load(Path(last['path'])/'checkpoint.npz',make_observer)
                np.testing.assert_array_equal(saved.chemistry.pos,ref.chemistry.pos)
                self.assertEqual(saved.chemistry.export(),ref.chemistry.export())
                self.assertEqual(saved.rng.bit_generator.state,ref.rng.bit_generator.state)
                self.assertEqual(observed.summary(),obs.summary());self.assertEqual(path.read_bytes(),original)
            finally:self.assertTrue(source.close())

    def test_local_catalog_uses_available_checkpoints_and_validates_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);self.assertEqual(available(root),[])
            parent=root/'outputs/competitive_relaxation_mechanism_followups';job=parent/'job';folder=job/'campaign';dest=folder/'tasks/task0000'
            dest.mkdir(parents=True);(parent/'latest.txt').write_text(str(job))
            (job/'job.json').write_text(json.dumps(dict(campaigns=[str(folder)])))
            manifest=folder/'manifest.json';manifest.write_text(json.dumps(dict(tasks=[dict(id='task0000',label='CR1_assembly_s0',scenario=dict(seed=0))])))
            (folder/'manifest.sha256').write_text(hashlib.sha256(manifest.read_bytes()).hexdigest())
            (folder/'saved.npz').write_bytes(b'available')
            (dest/'state.json').write_text(json.dumps(dict(status='complete',checkpoint='saved.npz',simulated_time=8000.)))
            rows=available(root);self.assertEqual(len(rows),1);self.assertEqual(rows[0]['status'],'complete')
            manifest.write_text('{}')
            with self.assertRaisesRegex(ValueError,'modifié'):available(root)
