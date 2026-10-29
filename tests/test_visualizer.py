import copy
import json
import tempfile
import time
import unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.config import load
from simulator.runner import make_observer
from simulator import checkpoint
from visualizer.camera import Camera
from visualizer.scene import Frame,EventTap,Selection,frame,style_arrays


class VisualizationContracts(unittest.TestCase):
    def test_pointer_anchored_zoom_and_pan_preserve_world_mapping(self):
        camera=Camera(np.array([7.,2.]),31.);size=(1700,900);point=np.array([323.,118.])
        world=camera.world(point,size);camera.zoom(4,point,size)
        np.testing.assert_allclose(camera.world(point,size),world)
        camera.pan([30.,-20.]);np.testing.assert_allclose(camera.screen(world,size),point+[30,-20])

    def test_reaction_observation_preserves_positions_rng_and_all_metrics(self):
        from experiments.prepare_density_campaign import scenario
        for raw in [scenario(1,True,0,duration=2.),load(Path('demonstrators/configs/large_membrane.json'))]:
            raw=copy.deepcopy(raw);raw['duration']=2.
            a,b=Simulation(raw),Simulation(raw)
            oa,ob=make_observer(a.config,False),make_observer(b.config,False)
            a.listeners.append(oa);b.listeners.append(ob);tap=EventTap(a.chemistry)
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.chemistry.export(),b.chemistry.export())
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
            self.assertEqual(oa.summary(),ob.summary())

    def test_transition_buffer_keeps_creation_and_break_between_display_frames(self):
        class Chemistry:
            def __init__(self):self.pos=np.array([[0.,0.],[1.,0.]]);self.links=[];self.calls=0
            def bonds(self):return dict(pairing=self.links)
            def react(self,time,dt,neighbors):
                self.calls+=1;self.links=[(0,1)] if self.calls%2 else [];return ['original']
        c=Chemistry();tap=EventTap(c)
        self.assertEqual(c.react(1.,.002,None),['original']);c.react(2.,.002,None)
        self.assertEqual([e.kind for e in tap.events],['bond_created','bond_broken'])
        self.assertEqual([e.time for e in tap.events],[1.,2.]);self.assertEqual(c.calls,2)
        c=Chemistry();tap=EventTap(c,capacity=1);c.react(1,0,None);c.react(2,0,None)
        self.assertEqual(tap.dropped,1);self.assertEqual(len(tap.events),1)

    def test_display_arrays_are_copies_and_filters_never_touch_chemistry(self):
        sim=Simulation(load(Path('demonstrators/configs/construction.json')));before=sim.chemistry.pos.copy()
        f=frame(sim);f.positions[:]=999
        np.testing.assert_array_equal(sim.chemistry.pos,before)
        f=frame(sim);selection=Selection();selection.anchor=0;selection.focus=True
        rgba,_,ids,_=style_arrays(f,np.zeros(len(f.labels)),selection)
        self.assertTrue(np.all(rgba[ids,3]==1));np.testing.assert_array_equal(sim.chemistry.pos,before)

    def test_structural_tracking_excludes_temporary_partner_and_survives_split(self):
        f=Frame(np.zeros((4,2)),np.zeros(4,dtype=int),('A',),np.ones((1,3)),
            dict(scaffold=np.array([[0,1],[2,3]]),pairing=np.array([[1,2]])),0.,0,False)
        s=Selection();s.anchor=0;np.testing.assert_array_equal(s.indices(f),[0,1])
        np.testing.assert_array_equal(s.linked_partners(f,s.indices(f)),[2])
        f.bonds['scaffold']=np.array([[2,3]]);f.revision=1
        np.testing.assert_array_equal(s.indices(f),[0]);self.assertEqual(s.anchor,0)

    def test_legacy_virtual_face_bonds_use_actual_reflected_anchor_geometry(self):
        raw=dict(schema_version=1,model='copy',chemistry=dict(sequence='00',free_units=1,dual_faces=True))
        sim=Simulation(raw);c=sim.chemistry;c.copy_pairing[0]=2;c.copy_pairing[2]=0
        c.back_pairs=np.array([[0,2]])
        f=frame(sim);pairs=f.bonds['pairing'];k=next(i for i,p in enumerate(pairs) if tuple(p)==(0,2))
        np.testing.assert_allclose(f.bond_positions['pairing'][k],2*c.pos[[0,2]]-c.pos[c.n+np.array([0,2])],rtol=1e-6)

    def test_real_process_pause_step_and_pacing_keep_exact_final_state(self):
        from visualizer.worker import ProcessSource
        raw=dict(schema_version=1,model='copy',seed=1,duration=.05,
            chemistry=dict(sequence='001',free_units=3),engine=dict(dt=.005))
        ref=Simulation(raw);ref.advance(ref.target_step)
        with tempfile.TemporaryDirectory() as d:
            source=ProcessSource(raw,d)
            def wait(predicate):
                deadline=time.monotonic()+45.;last=None
                while time.monotonic()<deadline:
                    for packet in source.poll():
                        self.assertNotIn('error',packet,packet.get('error'));last=packet
                        if predicate(packet):return packet
                    time.sleep(.01)
                self.fail(f'Worker timeout, last packet: {last}')
            try:
                first=wait(lambda p:p['frame'].step==0);self.assertTrue(first['paused'])
                source.command('step');single=wait(lambda p:p['frame'].step==1)
                self.assertTrue(single['paused']);source.command('speed',.2);source.command('pause',False)
                final=wait(lambda p:p['frame'].done)
                np.testing.assert_array_equal(final['frame'].positions,ref.chemistry.pos.astype('f4'))
                saved,_=checkpoint.load(Path(final['path'])/'checkpoint.npz',make_observer)
                np.testing.assert_array_equal(saved.chemistry.pos,ref.chemistry.pos)
                self.assertEqual(saved.rng.bit_generator.state,ref.rng.bit_generator.state)
            finally:self.assertTrue(source.close())
