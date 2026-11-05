import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator import checkpoint
from simulator.spatial import Neighborhood
from simulator.mixed_boundary import BoundaryObserver,segment_forces
from simulator.kinetics import KineticProbe
from experiments.prepare_boundary_transfer import scenario
from experiments.prepare_cooperative_synthesis import scenario as previous


class BoundaryTransferTests(unittest.TestCase):
    def test_common_products_and_matched_initial_controls(self):
        sims=[Simulation(scenario(0,v,.05)) for v in ('active','noexchange','nosynthesis')]
        a=sims[0];c=a.chemistry
        for b in sims[1:]:
            np.testing.assert_array_equal(c.pos,b.chemistry.pos)
            np.testing.assert_array_equal(a.motion.velocities,b.motion.velocities)
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        old=Simulation(previous(0,'cooperative',.05));shift=np.array([66.5,40.5])
        np.testing.assert_allclose(c.pos[:198],old.chemistry.pos+shift,atol=1e-14)
        self.assertEqual((len(c.pos),len(c.colors()),len(c.lipids.rungs),len(c.lipids.links)),(636,636,219,219))
        self.assertEqual(len({q for p in c.lipids.rungs.items() for q in p}),438)
        self.assertTrue(all(c.capture.categories[q]<0 for p in c.lipids.rungs.items() for q in p))

    def test_segment_force_reads_actual_axial_state_and_is_reciprocal(self):
        c=Simulation(scenario(0,'active',.05)).chemistry
        a,b,_,_=c.lipids.links[0];mid=(c.pos[a]+c.pos[b])/2
        active=np.flatnonzero(c.host.rungs[:,1]>=0);s=int(active[0]);r=int(c.host.rungs[s,1])
        free=int(np.flatnonzero(c.host.rungs[:,1]<0)[0])
        c.pos[:c.prefix]=[45.,45.];c.pos[s]=mid+[.15,0.];c.pos[r]=mid+[.2,0.];c.pos[free]=mid+[.1,0.]
        f=segment_forces(c,Neighborhood('brute',0.))
        self.assertGreater(np.linalg.norm(f[s]),0.);np.testing.assert_allclose(f.sum(axis=0),0.,atol=1e-10)
        np.testing.assert_array_equal(f[free],0.)
        c.host.rungs[s,1]=-1
        f=segment_forces(c,Neighborhood('brute',0.));np.testing.assert_array_equal(f[[s,r,free]],0.)

    def test_observer_does_not_count_adsorption_or_internal_cycle(self):
        c=Simulation(scenario(0,'active',.05)).chemistry;o=BoundaryObserver();o.observe(0.,c)
        h,t=c.prefix,c.prefix+24;c.lipids.bind(h,t)
        c.births.append(dict(time=1.,head=h,tail=t,birth_midpoint=[72.,45.]))
        a,b,x,y=c.lipids.links[0]
        # Adsorption makes the original component a branched graph: no closed
        # frontier witness, even though a new head touches a prepared one.
        c.lipids.links.append((h,a,0,1));o.observe(1.,c)
        self.assertEqual(o.ever_inserted,set())
        self.assertIn(h,o.history[-1]['new_heads_touching_prepared'])
        c.lipids.links.pop();o.observe(2.,c)
        self.assertTrue(o.history[-1]['valid']);self.assertEqual(o.ever_inserted,set())

    def test_real_cycle_insertion_and_residence_without_bridging_invalid_gaps(self):
        c=Simulation(scenario(0,'active',.05)).chemistry;o=BoundaryObserver();o.observe(0.,c)
        h,t=c.prefix,c.prefix+24;a,b,x,y=c.lipids.links.pop(0)
        c.pos[h]=(c.pos[a]+c.pos[b])/2;c.pos[t]=(c.pos[c.lipids.rungs[a]]+c.pos[c.lipids.rungs[b]])/2
        c.lipids.bind(h,t);c.lipids.links.extend([(h,a,1,0),(h,b,0,1)])
        c.births.append(dict(time=1.,head=h,tail=t,birth_midpoint=((c.pos[h]+c.pos[t])/2).tolist()))
        o.observe(1.,c);o.observe(2.,c)
        self.assertEqual(o.ever_inserted,{h});self.assertEqual(o.ever_inserted_born_inside,{h})
        self.assertEqual(o.residence[h],1.)
        link=c.lipids.links.pop();o.observe(3.,c);c.lipids.links.append(link);o.observe(4.,c)
        self.assertEqual(o.residence[h],1.)

    def test_passive_observer_brute_spatial_and_exact_resume(self):
        cfg=scenario(1,'active',.04);a=Simulation(cfg);b=Simulation(cfg)
        other=copy.deepcopy(cfg);other['engine']['spatial']='brute';brute=Simulation(other)
        obs=make_observer(a.config,False);a.listeners.append(obs)
        a.advance(10);b.advance(10);brute.advance(10)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        np.testing.assert_array_equal(a.chemistry.pos,brute.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'boundary.npz';checkpoint.save(p,a,obs);d,new=checkpoint.load(p,make_observer)
            a.advance(10);d.advance(10)
            np.testing.assert_array_equal(a.chemistry.pos,d.chemistry.pos)
            np.testing.assert_array_equal(a.motion.velocities,d.motion.velocities)
            self.assertEqual(a.chemistry.export(),d.chemistry.export());self.assertEqual(obs.summary(),new.summary())

    def test_birth_triggered_observation_does_not_wait_for_regular_frame(self):
        cfg=scenario(0,'active',.04);cfg['engine']['sample_every']=100
        sim=Simulation(cfg);calls=[];sim.listeners.append(lambda time,c,events:calls.append(time))
        sim.prepare();original=sim.chemistry.react
        def react(time,dt,neighbors):
            events=original(time,dt,neighbors);sim.chemistry.observation_due=True;return events
        sim.chemistry.react=react;sim.advance(5)
        self.assertIn(5*sim.dt,calls)

    def test_pre_reaction_census_and_frozen_gate_do_not_confuse_near_with_inserted(self):
        cfg=scenario(0,'active',.04);c=Simulation(cfg).chemistry
        h,t=c.prefix,c.prefix+24;a,b,_,_=c.lipids.links[0]
        c.pos[h]=(c.pos[a]+c.pos[b])/2
        c.pos[t]=(c.pos[c.lipids.rungs[a]]+c.pos[c.lipids.rungs[b]])/2;c.lipids.bind(h,t)
        probe=KineticProbe(cfg);before=copy.deepcopy(c.export());rng=copy.deepcopy(c.rng.bit_generator.state)
        scan=probe.scan(c);self.assertGreater(scan['encounter_pairs'],0);self.assertIn(h,scan['units'])
        self.assertEqual(c.export(),before);self.assertEqual(c.rng.bit_generator.state,rng)
        from experiments.review_boundary_transfer import decide
        rows=[dict(label=f'BI1_{v}_s{s}',seed=s,invariant_failures=0,valid_fraction_late=.9,
            inserted_born_inside=0 if v=='nosynthesis' else 1,L_new=0 if v=='nosynthesis' else 3)
            for s in range(3) for v in ('active','noexchange','nosynthesis')]
        self.assertTrue(decide(rows)['screen_passed']);rows[0]['inserted_born_inside']=0;rows[3]['inserted_born_inside']=0
        self.assertFalse(decide(rows)['screen_passed'])


if __name__=='__main__':unittest.main()
