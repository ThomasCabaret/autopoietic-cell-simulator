import copy,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from simulator.competitive_ports import competitive_force,saturated_force,local_free_delta,partners,birth_port_delta
from simulator.docking import free_faces,bound_port_force
from simulator.exchange_energy import port_delta
from simulator.spatial import Neighborhood
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator import checkpoint
from simulator.config import resolve
from simulator.transition_energy import formation_energy
from experiments.prepare_contact_gate import scenario
from experiments.competitive_port_potential import competitive_force as prototype
from tests.test_exchange_energy import context,full_energy
from simulator.mixed_boundary import segment_energy_delta


def free_energy(pos,links,width=.6):
    n=len(pos)//2;pairs=Neighborhood('brute',0.).pairs(pos[:n],1+4*width)
    return competitive_force(pos,pairs,free_faces(n,links),1.,.92,4.,width,partners(n,links))[1]


class CompetitiveIntegrationTests(unittest.TestCase):
    def test_saturated_ports_match_binary_and_gradient_in_a_crowded_motif(self):
        heads=np.array([[0.,0.],[1.,.03],[1.05,.15],[.1,.7]])
        pos=np.vstack((heads,heads+[.03,-.65]))
        args=(np.array([[0,1]],dtype=np.int64),free_faces(4,[]),1.,.92,4.,.6)
        a,e=competitive_force(pos,*args);b,f=saturated_force(pos,*args)
        np.testing.assert_allclose(a,b,atol=1e-14);self.assertAlmostEqual(e,f,places=14)
        pairs=Neighborhood('brute',0.).pairs(heads,3.4)
        args=(pairs,free_faces(4,[]),1.,.92,4.,.6)
        force,_=saturated_force(pos,*args)
        for i,j in np.ndindex(pos.shape):
            upper=pos.copy();lower=pos.copy()
            upper[i,j]+=1e-6;lower[i,j]-=1e-6
            gradient=(saturated_force(upper,*args)[1]-saturated_force(lower,*args)[1])/2e-6
            self.assertAlmostEqual(force[i,j],-gradient,places=7)

    def test_saturated_birth_and_exchange_match_full_energy(self):
        c=context();c.config.update(free_port_potential='saturated')
        heads,ids,links=c.lipids.layout()
        removed,formed=(0,1,1,0),(0,2,1,0)
        before=c.lipids.forces(c.pos,c.config,Neighborhood('brute',0.))[1]
        delta=port_delta(c.pos[ids],links,removed,formed,c.config,Neighborhood('brute',0.))
        c.lipids.links=[(heads[0],heads[2],1,0)]
        after=c.lipids.forces(c.pos,c.config,Neighborhood('brute',0.))[1]
        self.assertAlmostEqual(delta,after-before,places=12)
        delta=birth_port_delta(c,0,3,Neighborhood('brute',0.))
        c.lipids.bind(0,3)
        self.assertAlmostEqual(delta,c.lipids.forces(c.pos,c.config,Neighborhood('brute',0.))[1]-after,places=12)

    def test_engine_kernel_matches_preserved_static_prototype(self):
        heads=np.array([[0.,0.],[1.,.03],[1.05,.15],[.1,.7]]);pos=np.vstack((heads,heads+[.03,-.65]))
        pairs=Neighborhood('brute',0.).pairs(heads,3.4);args=(pos,pairs,free_faces(4,[]),1.,.92,4.,.6)
        a,e=competitive_force(*args);b,f=prototype(*args)
        np.testing.assert_array_equal(a,b);self.assertEqual(e,f)

    def test_add_remove_exchange_delta_includes_neighbor_partitions_and_barrier(self):
        c=context();c.config.update(free_port_potential='competitive',dock_width=.6,short_length=.92)
        heads,ids,links=c.lipids.layout();pos=c.pos[ids];old=(6,7,1,0)
        for removed,formed in [(old,None),(None,(6,8,0,1)),(old,(6,8,1,0))]:
            before=full_energy(c);packed_old=None if removed is None else (0,1,1,0);packed_new=None if formed is None else (0,2,*formed[2:])
            delta=port_delta(pos,links,packed_old,packed_new,c.config,Neighborhood('brute',0.))
            delta+=segment_energy_delta(c,None if removed is None else removed[:2],None if formed is None else formed[:2],Neighborhood('brute',0.))
            after=[q for q in c.lipids.links if q!=removed]+([] if formed is None else [formed]);saved=c.lipids.links;c.lipids.links=after
            self.assertAlmostEqual(delta,full_energy(c)-before,places=9);c.lipids.links=saved

    def test_third_ring_matches_global_oracle_and_far_bath_has_no_effect(self):
        heads=np.column_stack((np.arange(7)*1.8,np.zeros(7)));pos=np.vstack((heads,heads+[0.,-.65]));n=len(heads)
        pairs=Neighborhood('brute',0.).pairs(heads,3.4);old=[];new=[(0,1,1,0)]
        delta=local_free_delta(pos,pairs,free_faces(n,old),free_faces(n,new),partners(n,old),partners(n,new),np.array([0,1]),1.,.92,4.,.6)
        self.assertAlmostEqual(delta,free_energy(pos,new)-free_energy(pos,old),places=11)
        far=np.array([[1000.,0.],[1001.,0.]]);h=np.vstack((heads,far));p=np.vstack((h,h+[0.,-.65]));m=len(h)
        q=Neighborhood('brute',0.).pairs(h,3.4)
        other=local_free_delta(p,q,free_faces(m,old),free_faces(m,new),partners(m,old),partners(m,new),np.array([0,1]),1.,.92,4.,.6)
        self.assertEqual(delta,other)

    def test_birth_reweights_existing_pairs_not_only_new_port_wells(self):
        cfg=scenario(0,'coarse');cfg['chemistry']['free_port_potential']='competitive';sim=Simulation(cfg);c=sim.chemistry
        heads,ids,links=c.lipids.layout();h,t=c.prefix,c.prefix+c.config['food_units']
        c.pos[h]=c.pos[heads[0]]+[.8,.1];c.pos[t]=c.pos[h]+[0.,-.65]
        before=c.lipids.forces(c.pos,c.config,Neighborhood('brute',0.))[1]
        delta=birth_port_delta(c,h,t,Neighborhood('brute',0.))
        self.assertAlmostEqual(formation_energy(c,h,t,Neighborhood('brute',0.))['ports'],delta,places=12)
        c.lipids.bind(h,t)
        after=c.lipids.forces(c.pos,c.config,Neighborhood('brute',0.))[1]
        self.assertAlmostEqual(delta,after-before,places=9)

    def test_new_world_checkpoint_and_observer_are_passive(self):
        cfg=scenario(2,'fine');cfg['duration']=.1;cfg['chemistry']['free_port_potential']='competitive'
        a,b=Simulation(cfg),Simulation(cfg);obs=make_observer(a.config,False);a.listeners.append(obs)
        a.advance(50);b.advance(50);np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'new.npz';checkpoint.save(p,a,obs);new,new_obs=checkpoint.load(p,make_observer)
            a.advance(50);new.advance(50);np.testing.assert_array_equal(a.chemistry.pos,new.chemistry.pos)
            self.assertEqual(a.chemistry.export(),new.chemistry.export());self.assertEqual(obs.summary(),new_obs.summary())

    def test_prepared_dimers_have_no_lateral_links_or_birth_certificates(self):
        cfg=resolve(dict(schema_version=1,model='lipid_synthesis',chemistry=dict(tool_count=0,food_units=2,
            initial_lipids=[dict(head=[2.,2.],tail=[2.,1.35]),dict(head=[4.,4.],tail=[4.,3.35])],free_port_potential='competitive')))
        c=Simulation(cfg).chemistry;self.assertEqual(len(c.lipids.rungs),2);self.assertEqual(c.lipids.links,[]);self.assertEqual(c.births,[])
        self.assertTrue((c.capture.categories>=0).sum()==0)
        cfg['chemistry']['initial_lipids'][0]['tail']=[2.,2.]
        with self.assertRaisesRegex(ValueError,'nonzero'):resolve(cfg)
        cfg['chemistry']['food_units']='bad'
        with self.assertRaises(ValueError):resolve(cfg)
