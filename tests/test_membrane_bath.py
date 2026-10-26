import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.spatial import Neighborhood
from simulator.physics import force_kernel
from simulator.membrane_bath import barrier_force
from simulator.membrane_bath import MembraneBathObserver
from simulator import checkpoint
from simulator.contact_exchange import exchange_faces
from simulator.membrane_bath import DEFAULTS


def small():
    return dict(schema_version=1,model='membrane_bath',duration=3.,seed=2,engine=dict(sample_every=100),
        chemistry=dict(units=44,ring_units=40,ring_radius=6.3,box=[26.,26.],retained_probes=8,permeable_probes=8))


class MembraneBathTests(unittest.TestCase):
    def test_exchange_is_local_one_for_one_on_either_side_of_open_fragment(self):
        cfg=dict(DEFAULTS,contact_exchange_rate=1e9)
        for side in (-1.,1.):
            h=np.array([[0.,0.],[1.,0.],[.7,side*.35]])
            pos=np.concatenate((h,h+[0.,-.65]));before=pos.copy()
            links,events=exchange_faces(pos,[(0,1,1,0)],cfg,np.random.default_rng(0),Neighborhood(),.01)
            self.assertEqual(links,[(0,2,1,0)]);self.assertEqual(len(events),1)
            self.assertEqual(events[0]['removed'],[0,1,1,0])
            np.testing.assert_array_equal(pos,before)
        rng=np.random.default_rng(2);state=copy.deepcopy(rng.bit_generator.state)
        links,events=exchange_faces(pos,[(0,1,1,0)],DEFAULTS,rng,Neighborhood(),.01)
        self.assertEqual(links,[(0,1,1,0)]);self.assertEqual(events,[])
        self.assertEqual(state,rng.bit_generator.state)

    def test_active_exchange_checkpoint_preserves_events_and_rng(self):
        raw=small();raw['chemistry']['contact_exchange_rate']=1e6
        a=Simulation(raw);c=a.chemistry;n=c.n
        # Geometry only: a free dimer approaching an occupied face.
        c.pos[40]=c.pos[0]+.7*(c.pos[1]-c.pos[0])+[-.30,0.]
        c.pos[n+40]=c.pos[40]+c.pos[n]-c.pos[0]
        obs=make_observer(a.config);a.listeners.append(obs);a.advance(500)
        self.assertTrue(c.exchange_events)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'exchange.npz';checkpoint.save(path,a,obs)
            b,other=checkpoint.load(path,make_observer)
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.chemistry.export(),b.chemistry.export())
            self.assertEqual(obs.summary(),other.summary())
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)

    def test_fragmented_open_arc_is_unknown_not_a_false_escape(self):
        sim=Simulation(small());c=sim.chemistry
        edges=[set(x) for x in c.edges]
        for row in edges:row.remove((0,1));row.remove((8,9))
        obs=make_observer(sim.config);obs(0.,c.pos,edges,[])
        self.assertEqual(obs.summary()['envelope_valid_fraction'],0.)
        self.assertIsNone(obs.summary()['retained_escape_fraction'])

    def test_three_atom_barrier_gradient_momentum_and_both_sides(self):
        p=np.array([[0.,0.],[1.,0.],[.4,.2],[-.2,.1],[.4,-.2]])
        edges=np.array([[0,1]],dtype=np.int64);probes=np.array([2,3,4],dtype=np.int64)
        pairs=np.array([[0,0],[0,1],[0,2]],dtype=np.int64)
        f,_=barrier_force(p,edges,probes,pairs,.55,80.);numeric=np.zeros_like(f);h=1e-6
        for i in range(len(p)):
            for a in range(2):
                plus=p.copy();minus=p.copy();plus[i,a]+=h;minus[i,a]-=h
                numeric[i,a]=-(barrier_force(plus,edges,probes,pairs,.55,80.)[1]-barrier_force(minus,edges,probes,pairs,.55,80.)[1])/(2*h)
        np.testing.assert_allclose(f,numeric,atol=1e-7)
        np.testing.assert_allclose(f.sum(axis=0),0.,atol=1e-12)
        self.assertAlmostEqual(float(np.sum(p[:,0]*f[:,1]-p[:,1]*f[:,0])),0.,places=10)
        self.assertGreater(f[2,1],0.);self.assertLess(f[4,1],0.)
        z,_=barrier_force(p,edges,probes,pairs,0.,80.);np.testing.assert_array_equal(z,0.)

    def test_initial_labels_radius_and_observer_do_not_control_dynamics(self):
        raw=small();a=Simulation(raw);b=Simulation(raw)
        obs=make_observer(a.config);a.listeners.append(obs)
        b.chemistry.config['ring_radius']=12345.;b.chemistry.config['ring_units']=3
        b.chemistry.config['free_lipid_start']='outside_annulus'
        a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.chemistry.export(),b.chemistry.export())
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertEqual(obs.edges_frames,[])
        self.assertEqual(len(obs.face_link_frames),len(obs.frames))

    def test_sparse_state_tree_brute_and_checkpoint(self):
        raw=small();a=Simulation(raw);oa=make_observer(a.config);a.listeners.append(oa);a.advance(777)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'state.npz';checkpoint.save(path,a,oa)
            resumed,oc=checkpoint.load(path,make_observer)
            a.advance(a.target_step);resumed.advance(resumed.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,resumed.chemistry.pos)
            self.assertEqual(a.chemistry.export(),resumed.chemistry.export())
            self.assertEqual(oa.summary(),oc.summary())
        other=copy.deepcopy(raw);other['engine']['spatial']='brute'
        b=Simulation(other);ob=make_observer(b.config);b.listeners.append(ob);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(oa.summary(),ob.summary())

    def test_forces_are_equivariant_under_arbitrary_lipid_relabeling(self):
        c=Simulation(small()).chemistry;c.react(0.,.002,Neighborhood())
        def force():
            neighbors=Neighborhood();pairs=neighbors.pairs(c.pos,float(c.contact.max()),'core')
            return force_kernel(c.pos,pairs,c.kinds,c.contact,c.springs,c.angles)+c.extra_forces(neighbors)
        original=force();n=c.n
        permutation=np.random.default_rng(4).permutation(n);inverse=np.argsort(permutation)
        order=np.concatenate((permutation,n+permutation,np.arange(2*n,len(c.pos))))
        c.pos=c.pos[order].copy()
        c.face_links=[(int(inverse[i]),int(inverse[j]),a,b) if inverse[i]<inverse[j] else
                      (int(inverse[j]),int(inverse[i]),b,a) for i,j,a,b in c.face_links]
        c.face_links.sort();contacts={(i,j) for i,j,a,b in c.face_links};c.edges=[contacts.copy(),contacts.copy()];c._face_mechanics()
        np.testing.assert_allclose(force(),original[order],atol=1e-10)


if __name__=='__main__':unittest.main()
