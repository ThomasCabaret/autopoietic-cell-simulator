import copy,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from simulator.exchange_energy import port_delta
from simulator.contact_exchange import exchange_faces
from simulator.linked_lipids import LinkedLipids
from simulator.mixed_boundary import segment_energy_delta
from simulator.membrane_bath import barrier_force
from simulator.spatial import Neighborhood
from simulator.lipid_synthesis import DEFAULTS
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator import checkpoint
from experiments.prepare_exchange_ablation import scenario


def context():
    cfg=dict(DEFAULTS,bound_barrier_radius=.55,bound_barrier_stiffness=80.)
    heads=np.array([[0.,0.],[1.,0.],[1.,.5],[2.,.6]])
    probes=np.array([[.2,.15],[.7,.1],[1.3,.3],[.2,-.3],[.7,-.35],[1.3,-.15]])
    pos=np.vstack((probes,heads,heads+[0.,-.65]));lipids=LinkedLipids()
    for h in range(6,10):lipids.bind(h,h+4)
    lipids.links=[(6,7,1,0)]
    return SimpleNamespace(config=cfg,pos=pos,host=SimpleNamespace(rungs=np.array([[0,3],[1,4],[2,5]])),lipids=lipids)


def full_energy(c):
    port=c.lipids.forces(c.pos,c.config,Neighborhood('brute',0.))[1]
    edges=np.asarray([(a,b) for a,b,_,_ in c.lipids.links],dtype=np.int64)
    ids=c.host.rungs.reshape(-1);pairs=np.asarray([(a,b) for a in range(len(edges)) for b in range(len(ids))],dtype=np.int64).reshape(-1,2)
    return port+barrier_force(c.pos,edges,ids,pairs,.55,80.)[1]


class ExchangeEnergyTests(unittest.TestCase):
    def test_local_delta_matches_full_potential_including_outside_affinities_and_PR_barrier(self):
        c=context();old=(6,7,1,0);new=(6,8,1,0);heads,ids,links=c.lipids.layout()
        before=full_energy(c);state=copy.deepcopy(c.lipids.export());p=c.pos.copy()
        delta=port_delta(c.pos[ids],links,(0,1,1,0),(0,2,1,0),c.config,Neighborhood('brute',0.))
        barrier=segment_energy_delta(c,old[:2],new[:2],Neighborhood('brute',0.))
        self.assertNotEqual(barrier,0.);self.assertEqual(c.lipids.export(),state);np.testing.assert_array_equal(c.pos,p)
        c.lipids.links=[new];self.assertAlmostEqual(delta+barrier,full_energy(c)-before,places=9)
        reverse=port_delta(c.pos[ids],[(0,2,1,0)],(0,2,1,0),(0,1,1,0),c.config,Neighborhood('brute',0.))
        reverse+=segment_energy_delta(c,new[:2],old[:2],Neighborhood('brute',0.))
        self.assertAlmostEqual(reverse,-delta-barrier,places=9)

    def test_zero_temperature_rejects_uphill_and_accepts_reverse_without_moving_atoms(self):
        heads=np.array([[0.,0.],[1.,0.],[1.,.5]]);pos=np.vstack((heads,heads+[0.,-.65]));before=pos.copy()
        cfg=dict(DEFAULTS,contact_exchange_gate='metropolis',contact_exchange_rate=1e9,temperature=0.)
        stats=dict(proposals=0,accepted=0,rejected=0,positive_delta=0,sum_positive_delta=0.,sum_factor=0.,min_delta=None,max_delta=None)
        links,events=exchange_faces(pos,[(0,1,1,0)],cfg,np.random.default_rng(1),Neighborhood('brute',0.),.01,stats=stats)
        self.assertEqual(links,[(0,1,1,0)]);self.assertEqual(events,[]);self.assertGreater(stats['rejected'],0)
        links,events=exchange_faces(pos,[(0,2,1,0)],cfg,np.random.default_rng(1),Neighborhood('brute',0.),.01,stats=stats)
        self.assertIn((0,1,1,0),links);self.assertTrue(any(e['delta_U']<=0 for e in events));np.testing.assert_array_equal(pos,before)
        cfg['bound_barrier_radius']=.55
        with self.assertRaisesRegex(ValueError,'callback'):exchange_faces(pos,links,cfg,np.random.default_rng(1),Neighborhood('brute',0.),.01)

    def test_exchange_statistics_and_gated_world_resume_exactly_without_observer_feedback(self):
        cfg=scenario(0,True);cfg['duration']=.1;cfg['chemistry']['contact_exchange_gate']='metropolis'
        sim=Simulation(cfg);plain=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs)
        sim.advance(25);plain.advance(25)
        np.testing.assert_array_equal(sim.chemistry.pos,plain.chemistry.pos);self.assertEqual(sim.rng.bit_generator.state,plain.rng.bit_generator.state)
        self.assertIsNotNone(sim.chemistry.lipids.exchange_stats)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'gate.npz';checkpoint.save(path,sim,obs);new,other=checkpoint.load(path,make_observer)
            sim.advance(25);new.advance(25)
            np.testing.assert_array_equal(sim.chemistry.pos,new.chemistry.pos)
            self.assertEqual(sim.chemistry.export(),new.chemistry.export());self.assertEqual(obs.summary(),other.summary())
