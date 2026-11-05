import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from tests.test_exchange_energy import context,full_energy
from simulator.exchange_energy import port_delta
from simulator.mixed_boundary import segment_energy_delta
from simulator.docking import update_faces
from simulator.spatial import Neighborhood
from simulator.lipid_synthesis import DEFAULTS
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator import checkpoint
from experiments.prepare_exchange_refinement import scenario


def stats():
    return {k:dict(proposals=0,accepted=0,rejected=0,positive_delta=0,sum_factor=0.,sum_accepted_delta=0.,min_delta=None,max_delta=None) for k in ('formation','breaking')}


class ContactUpdateEnergyTests(unittest.TestCase):
    def test_single_addition_removal_matches_full_port_and_barrier_energy(self):
        c=context();p=c.pos.copy();heads,ids,links=c.lipids.layout();old=(6,7,1,0)
        initial=full_energy(c)
        delta=port_delta(c.pos[ids],links,(0,1,1,0),None,c.config,Neighborhood('brute',0.))
        delta+=segment_energy_delta(c,old[:2],None,Neighborhood('brute',0.))
        c.lipids.links=[];self.assertAlmostEqual(delta,full_energy(c)-initial,places=9)
        reverse=port_delta(c.pos[ids],[],None,(0,1,1,0),c.config,Neighborhood('brute',0.))
        reverse+=segment_energy_delta(c,None,old[:2],Neighborhood('brute',0.))
        self.assertAlmostEqual(delta,-reverse,places=9);np.testing.assert_array_equal(c.pos,p)

    def test_free_composites_can_bind_thermally_but_zero_T_rejects_uphill_formation(self):
        heads=np.array([[0.,0.],[1.,0.]]);pos=np.vstack((heads,heads+[0.,-.65]));before=pos.copy()
        cfg=dict(DEFAULTS,short_length=.92,dock_width=.6,contact_update_gate='metropolis',dock_rate=1e9,bond_off_rate=0.,temperature=0.)
        s=stats();links,broken=update_faces(pos,[],cfg,np.random.default_rng(3),Neighborhood('brute',0.),.01,stats=s)
        self.assertEqual(links,[]);self.assertGreater(s['formation']['rejected'],0)
        cfg['temperature']=.08;s=stats()
        links,broken=update_faces(pos,[],cfg,np.random.default_rng(3),Neighborhood('brute',0.),.01,stats=s)
        self.assertEqual(len(links),1);self.assertEqual(s['formation']['accepted'],1)
        cfg.update(temperature=0.,bond_off_rate=1e9,bonding=False);s=stats()
        links,broken=update_faces(pos,links,cfg,np.random.default_rng(3),Neighborhood('brute',0.),.01,stats=s)
        self.assertEqual((links,broken),([],1));self.assertLess(s['breaking']['sum_accepted_delta'],0.)
        np.testing.assert_array_equal(pos,before)

    def test_barrier_callback_is_required_and_its_creation_cost_is_used(self):
        heads=np.array([[0.,0.],[1.,0.]]);pos=np.vstack((heads,heads+[0.,-.65]))
        cfg=dict(DEFAULTS,contact_update_gate='metropolis',dock_rate=1e9,bound_barrier_radius=.55)
        with self.assertRaisesRegex(ValueError,'callback'):update_faces(pos,[],cfg,np.random.default_rng(1),Neighborhood('brute',0.),.01)
        seen=[]
        def cost(old,new):seen.append((old,new));return 1e6
        links,_=update_faces(pos,[],cfg,np.random.default_rng(1),Neighborhood('brute',0.),.01,cost)
        self.assertEqual(links,[]);self.assertTrue(seen);self.assertIsNone(seen[0][0])

    def test_gated_world_is_passive_and_contact_statistics_resume_exactly(self):
        cfg=scenario(2);cfg['duration']=2.;cfg['chemistry']['contact_update_gate']='metropolis'
        a,b=Simulation(cfg),Simulation(cfg);obs=make_observer(a.config,False);a.listeners.append(obs)
        a.advance(1000);b.advance(1000);np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertGreater(sum(q['proposals'] for q in a.chemistry.lipids.contact_stats.values()),0)
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'contacts.npz';checkpoint.save(p,a,obs);new,new_obs=checkpoint.load(p,make_observer)
            a.advance(1000);new.advance(1000);np.testing.assert_array_equal(a.chemistry.pos,new.chemistry.pos)
            self.assertEqual(a.chemistry.export(),new.chemistry.export());self.assertEqual(obs.summary(),new_obs.summary())
