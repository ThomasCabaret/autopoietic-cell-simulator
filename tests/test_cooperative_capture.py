import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.spatial import Neighborhood
from simulator.transition_energy import formation_energy
from simulator import checkpoint
from experiments.prepare_mixed_synthesis import scenario
from experiments.diagnose_lipid_heat import energy
from tests.test_mixed_synthesis import tool,capture


def config(seed=0,duration=.4):
    cfg=scenario(seed,'mixed',duration);cfg['chemistry']['capture_cooperativity']=True;return cfg


class CooperativeCaptureTests(unittest.TestCase):
    def test_first_ligand_broad_then_neighbor_compatible_and_release_reopens(self):
        c=Simulation(config()).chemistry;sites=tool(c);g=c.host
        p=int(np.flatnonzero(g.rungs[:,1]<0)[0]);r=next(q for q in range(g.n,c.prefix) if q not in g.rungs[:,1])
        h,t=c.prefix,c.prefix+24
        self.assertTrue(c.capture.binding_allowed(c,sites[0],p));self.assertTrue(c.capture.binding_allowed(c,sites[0],h))
        capture(c,sites[:1],(p,));c.capture.refresh(c)
        self.assertTrue(c.capture.binding_allowed(c,sites[1],r));self.assertFalse(c.capture.binding_allowed(c,sites[1],t))
        c.capture.release(p);c.capture.refresh(c)
        self.assertTrue(c.capture.binding_allowed(c,sites[1],t))
        capture(c,sites[:1],(h,));c.capture.refresh(c)
        self.assertTrue(c.capture.binding_allowed(c,sites[1],t));self.assertFalse(c.capture.binding_allowed(c,sites[1],r))

    def test_actual_capture_rejects_crossed_pair_without_erasing_its_atoms(self):
        c=Simulation(config()).chemistry;sites=tool(c);g=c.host
        p=int(np.flatnonzero(g.rungs[:,1]<0)[0]);t=c.prefix+24
        c.pos[:]=[11.,8.];c.pos[p]=[3.,3.];c.pos[t]=[3.2,3.]
        c.pos[c.rungs[sites[0],1]]=c.pos[p];c.pos[c.rungs[sites[1],1]]=c.pos[t]
        capture(c,sites[:1],(p,));c.capture.refresh(c);old=c.pos.copy()
        c.config.update(food_binding_rate=1e9,food_unbinding_rate=0.)
        c.capture.react(c,.002,Neighborhood('brute',0.))
        self.assertEqual(c.capture.site_bound[sites[0]],p);self.assertEqual(c.capture.site_bound[sites[1]],-1)
        self.assertEqual(c.capture.atom_bound[t],-1);np.testing.assert_array_equal(c.pos,old)

    def test_force_is_reciprocal_and_gradient_of_same_gated_attraction(self):
        c=Simulation(config()).chemistry;sites=tool(c);p=int(np.flatnonzero(c.host.rungs[:,1]<0)[0]);t=c.prefix+24
        c.pos[:]=[11.,8.];c.pos[c.rungs[sites[1],1]]=[3.,3.];c.pos[t]=[3.4,3.1]
        capture(c,sites[:1],(p,));c.capture.refresh(c)
        force=c.capture.forces(c,Neighborhood('brute',0.));np.testing.assert_allclose(force[t],0.)
        c.capture.release(p);c.capture.refresh(c);force=c.capture.forces(c,Neighborhood('brute',0.))
        self.assertGreater(np.linalg.norm(force[t]),0.);np.testing.assert_allclose(force.sum(axis=0),0.,atol=1e-12)
        for axis in range(2):
            x=c.pos[t,axis];c.pos[t,axis]=x+1e-6;a=energy(c)['free_capture_potential']
            c.pos[t,axis]=x-1e-6;b=energy(c)['free_capture_potential'];c.pos[t,axis]=x
            self.assertAlmostEqual(force[t,axis],-(a-b)/2e-6,places=6)

    def test_formation_delta_includes_affinity_change_at_next_bonded_site(self):
        c=Simulation(config()).chemistry;i,j=tool(c);k=j+1;h,t=c.prefix,c.prefix+24
        c.host.edges.add((j,k));c.pos[:]=[10.,8.]
        for q,x in ((i,2.),(j,3.),(k,4.)):
            c.pos[q]=[x,3.];c.pos[c.rungs[q,1]]=[x,3.45]
        c.pos[h]=[2.6,3.45];c.pos[t]=[3.1,3.45]
        p=int(np.flatnonzero(c.host.rungs[:,1]<0)[0]);c.pos[p]=[4.2,3.45]
        capture(c,[i,j],[h,t]);c.capture.refresh(c);c._mechanics()
        before=energy(c);state=copy.deepcopy(c.export());delta=formation_energy(c,h,t,Neighborhood('brute',0.))
        self.assertEqual(state,c.export());self.assertFalse(c.capture.binding_allowed(c,k,p))
        c.lipids.bind(h,t);c.capture.release(h);c.capture.release(t);c.capture.refresh(c)
        self.assertTrue(c.capture.binding_allowed(c,k,p));after=energy(c)
        for key in before:self.assertAlmostEqual(delta[key],after[key]-before[key],places=9)

    def test_tree_brute_passivity_and_resume_exact(self):
        cfg=config(seed=1);a=Simulation(cfg);b=Simulation(cfg);brute=copy.deepcopy(cfg);brute['engine']['spatial']='brute';d=Simulation(brute)
        obs=make_observer(a.config,False);a.listeners.append(obs)
        a.advance(100);b.advance(100);d.advance(100)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos);np.testing.assert_array_equal(a.chemistry.pos,d.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'coop.npz';checkpoint.save(p,a,obs);other,newobs=checkpoint.load(p,make_observer)
            a.advance(100);other.advance(100)
            np.testing.assert_array_equal(a.chemistry.pos,other.chemistry.pos)
            np.testing.assert_array_equal(a.motion.velocities,other.motion.velocities)
            self.assertEqual(a.chemistry.export(),other.chemistry.export());self.assertEqual(obs.summary(),newobs.summary())


if __name__=='__main__':unittest.main()
