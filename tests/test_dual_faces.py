import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.dual_faces import reflected_force
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.spatial import Neighborhood
from simulator.observations import CopyObserver
from simulator import checkpoint


def config():
    return dict(schema_version=1,model='copy',duration=3.,seed=2,
        chemistry=dict(sequence='001',free_units=4,function_units=4,food_pairs=2,
                       dual_faces=True,food_activation=True,functional_cosines={'0':.8,'1':.8}))


class DualFaceTests(unittest.TestCase):
    def test_campaign_selects_actual_sequence_not_name_suffix(self):
        from experiments.run_batch5 import scenario
        self.assertEqual(scenario('E3dual6extended',0,1.)['chemistry']['sequence'],'001011')
        self.assertEqual(scenario('E3dual3Fonly',0,1.)['chemistry']['sequence'],'001')
        self.assertEqual(scenario('E3dual3Fonly',0,1.)['chemistry']['free_units'],0)
        self.assertTrue(scenario('E3cooperative3',0,1.)['chemistry']['product_cooperativity'])
        self.assertFalse(scenario('E3cooperative3',0,1.)['chemistry']['dual_faces'])
        with self.assertRaises(ValueError):scenario('unregistered_label',0,1.)

    def test_virtual_force_gradient_momentum_torque(self):
        p=np.array([[0.,0.],[.2,-.9],[.1,.45],[.13,-1.3]])
        pairs=np.array([[0,1]],dtype=np.int64);force,_=reflected_force(p,pairs,2)
        numeric=np.zeros_like(p);h=1e-6
        for i in range(4):
            for axis in range(2):
                plus=p.copy();minus=p.copy();plus[i,axis]+=h;minus[i,axis]-=h
                numeric[i,axis]=-(reflected_force(plus,pairs,2)[1]-reflected_force(minus,pairs,2)[1])/(2*h)
        np.testing.assert_allclose(force,numeric,atol=1e-8)
        np.testing.assert_allclose(force.sum(axis=0),0.,atol=1e-12)
        self.assertAlmostEqual(float(np.sum(p[:,0]*force[:,1]-p[:,1]*force[:,0])),0.,places=10)

    def test_both_faces_can_bind_same_G_without_global_switch(self):
        c=Simulation(dict(schema_version=1,model='copy',duration=1.,chemistry=dict(
            sequence='00',free_units=1,function_units=1,dual_faces=True,monomer_only_capture=True))).chemistry
        # Unit 0 belongs to prepared G, unit 2 is G, unit 3 is F.
        c.pos[:4]=[[3.,3.],[4.,3.],[3.,2.1],[3.,3.9]]
        c.pos[4:]=[[3.,3.45],[4.,3.45],[3.,1.65],[3.,3.45]]
        for _ in range(100):
            c.react(0.,.005,Neighborhood())
            if c.copy_pairing[0]==2 and c.pairing[0]==3:break
        self.assertEqual(c.copy_pairing[0],2);self.assertEqual(c.pairing[0],3)
        self.assertTrue(all(c.families[i]==0 and c.families[j]==0 for i,j in c.back_pairs))
        self.assertTrue(all(c.families[i]!=c.families[j] for i,j in enumerate(c.pairing) if j>i))

    def test_dual_tree_brute_and_checkpoint(self):
        a=Simulation(config());oa=make_observer(a.config);a.listeners.append(oa)
        other=copy.deepcopy(config());other['engine']={'spatial':'brute'}
        b=Simulation(other);ob=make_observer(b.config);b.listeners.append(ob)
        a.advance(333)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state.npz';checkpoint.save(p,a,oa)
            resumed,oc=checkpoint.load(p,make_observer)
            a.advance(a.target_step);resumed.advance(resumed.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,resumed.chemistry.pos)
            self.assertEqual(a.chemistry.export(),resumed.chemistry.export())
            self.assertEqual(oa.summary(),oc.summary())
        b.advance(b.target_step);np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(oa.summary(),ob.summary())

    def test_observer_detachment_checks_both_faces(self):
        obs=CopyObserver(dict(sequence='01',template=True,seed_family=0,dual_faces=True))
        bits=np.array([0,1,0,1,0,1]);fam=np.array([0,0,0,0,1,1]);p=np.zeros((12,2))
        edges={(0,1),(2,3),(4,5)};front=np.full(6,-1);back=np.array([2,3,0,1,-1,-1])
        obs(0.,p,edges,front,bits,[],fam,None,back)
        self.assertEqual(obs.summary()['detached_copy_sets_ever'],0)
        self.assertEqual(obs.summary()['joint_detached_ever'],0)
        back[:]=-1
        obs(1.,p,edges,front,bits,[],fam,None,back)
        self.assertEqual(obs.summary()['joint_detached_ever'],1)


if __name__=='__main__':unittest.main()
