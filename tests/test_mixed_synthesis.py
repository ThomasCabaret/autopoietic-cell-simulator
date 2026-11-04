import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.config import resolve
from simulator.runner import make_observer
from simulator import checkpoint
from simulator.spatial import Neighborhood
from simulator.transition_energy import formation_energy
from experiments.diagnose_lipid_heat import energy
from experiments.prepare_mixed_synthesis import scenario
from experiments.prepare_capture_transfer import scenario as reference


def tool(c):
    return next(q['units'] for q in c.host.initial_groups if q['family']==1 and q['backbone'])


def capture(c,sites,atoms):
    c.capture.site_bound[:]=-1;c.capture.atom_bound[:]=-1
    for s,a in zip(sites,atoms):c.capture.site_bound[s]=a;c.capture.atom_bound[a]=s


class MixedSynthesisTests(unittest.TestCase):
    def test_noHT_matches_genetic_reference_and_initial_controls_match(self):
        for seed in range(3):
            a=Simulation(scenario(seed,'noHT',.2));b=Simulation(reference(seed,'matched',.2))
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            np.testing.assert_array_equal(a.motion.velocities,b.motion.velocities)
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
            self.assertEqual(a.chemistry.host.export(),b.chemistry.export())
            x,y,z=[Simulation(scenario(seed,v,.2)) for v in ('mixed','uncaptured','nogene')]
            for other in (y,z):
                np.testing.assert_array_equal(x.chemistry.pos,other.chemistry.pos)
                np.testing.assert_array_equal(x.motion.velocities,other.motion.velocities)
                self.assertEqual(x.rng.bit_generator.state,other.rng.bit_generator.state)

    def test_one_pool_releases_HT_then_same_sites_can_catalyze_PR(self):
        c=Simulation(scenario(0,'mixed',.2)).chemistry;g=c.host;sites=tool(c)
        h,t=c.prefix+2,c.prefix+24+5
        # Constructed local mechanism check at forced rate, not a kinetic result.
        c.pos[:]=[11.,8.];c.pos[h]=[3.,3.];c.pos[t]=[3.5,3.]
        c.config.update(formation_gate='none',rung_catalytic_rate=1e9,rung_formation_rate=0.)
        c.capture.refresh(c);capture(c,sites,(h,t));before=c.pos.copy()
        c.form_lipids(1.,.01,Neighborhood('brute',0.))
        self.assertEqual(c.lipids.rungs[h],t);np.testing.assert_array_equal(c.pos,before)
        self.assertTrue(all(c.capture.site_bound[s]<0 for s in sites))
        s=int(np.flatnonzero(g.rungs[:,1]<0)[0]);r=next(q for q in range(g.n,c.prefix) if q not in g.rungs[:,1])
        c.pos[:]=[11.,8.];c.pos[s]=[3.,3.];c.pos[r]=[3.4,3.]
        c.capture.refresh(c);capture(c,sites,(s,r));g.config.update(rung_catalytic_rate=1e9,rung_formation_rate=0.)
        # Isolate the already-captured formation step; no stochastic rebind/unbind.
        view=g.assembly.catalyst;original=view.react;view.react=lambda *args:None
        try:g.assembly.react(g,2.,.002,Neighborhood('brute',0.))
        finally:view.react=original
        self.assertEqual(g.rungs[s,1],r);self.assertTrue(g.assembly.events[-1]['catalyzed'])
        self.assertTrue(all(c.capture.site_bound[s]<0 for s in sites))
        self.assertTrue(np.all(c.capture.atom_bound[[h,t,s,r]]<0))
        self.assertEqual(len(c.pos),198)

    def test_wrong_material_pair_can_occupy_sites_but_never_forms_product(self):
        c=Simulation(scenario(0,'mixed',.2)).chemistry;g=c.host;sites=tool(c)
        p=int(np.flatnonzero(g.rungs[:,1]<0)[0]);t=c.prefix+24
        c.capture.refresh(c)
        self.assertEqual((c.capture.categories[p],c.capture.categories[t]),(0,1))
        c.pos[:]=[11.,8.];c.pos[p]=[3.,3.];c.pos[t]=[3.2,3.]
        c.pos[c.rungs[sites[0],1]]=c.pos[p];c.pos[c.rungs[sites[1],1]]=c.pos[t]
        c.config.update(food_binding_rate=1e9,food_unbinding_rate=0.,formation_gate='none',rung_catalytic_rate=1e9,rung_formation_rate=0.)
        c.capture.react(c,.002,Neighborhood('brute',0.))
        self.assertEqual([int(c.capture.site_bound[s]) for s in sites],[p,t])
        c.form_lipids(0.,.01,Neighborhood('brute',0.));self.assertEqual(c.births,[])
        self.assertEqual(c.lipids.rungs,{})
        c.capture.release(p);self.assertEqual(c.capture.atom_bound[p],-1)

    def test_H_T_local_delta_includes_competing_genetic_attractions(self):
        c=Simulation(scenario(0,'mixed',.2)).chemistry;sites=tool(c);h,t=c.prefix,c.prefix+24
        c.pos[:]=[10.,8.]
        for k,s in enumerate(sites):c.pos[s]=[3.+k,3.];c.pos[c.rungs[s,1]]=[3.+k,3.45]
        c.pos[h]=[3.3,3.45];c.pos[t]=[3.8,3.45];c.capture.refresh(c);capture(c,sites,(h,t));c._mechanics()
        before=energy(c);state=copy.deepcopy(c.export());rng=copy.deepcopy(c.rng.bit_generator.state)
        delta=formation_energy(c,h,t,Neighborhood('brute',0.))
        self.assertEqual(c.export(),state);self.assertEqual(c.rng.bit_generator.state,rng)
        c.lipids.bind(h,t);c.capture.categories[[h,t]]=-1;c.capture.release(h);c.capture.release(t)
        after=energy(c)
        for k in before:self.assertAlmostEqual(delta[k],after[k]-before[k],places=9)

    def test_capture_spring_once_checkpoint_and_observer_are_exact(self):
        cfg=scenario(1,'mixed',.4);a=Simulation(cfg);b=Simulation(cfg)
        other=copy.deepcopy(cfg);other['engine']['spatial']='brute';brute=Simulation(other)
        obs=make_observer(a.config,False);a.listeners.append(obs)
        a.advance(100);b.advance(100);brute.advance(100)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        np.testing.assert_array_equal(a.chemistry.pos,brute.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'mixed.npz';checkpoint.save(p,a,obs);d,newobs=checkpoint.load(p,make_observer)
            a.advance(100);d.advance(100)
            np.testing.assert_array_equal(a.chemistry.pos,d.chemistry.pos)
            np.testing.assert_array_equal(a.motion.velocities,d.motion.velocities)
            self.assertEqual(a.chemistry.export(),d.chemistry.export());self.assertEqual(obs.summary(),newobs.summary())
        c=a.chemistry;sites=tool(c);h=c.prefix
        c.capture.refresh(c);capture(c,sites[:1],(h,));c._mechanics()
        self.assertEqual(sum(int(i)==c.rungs[sites[0],1] and int(j)==h for i,j,_,_ in c.springs),1)
        self.assertEqual(c.host.assembly.catalyst.springs(c.host),[])

    def test_shared_constants_cannot_be_overridden_per_substrate(self):
        cfg=scenario(0,'mixed');cfg['chemistry']['genetics']['food_binding_rate']=1.
        with self.assertRaises(ValueError):resolve(cfg)

    def test_lipid_provenance_excludes_prepared_partial_and_late_material(self):
        from types import SimpleNamespace
        obs=make_observer(scenario(0,'mixed'),False)
        obs.births=[dict(time=5.,head=i,tail=i+10,catalyzed=True,sites=[10,11],chain=[10,11],chain_kind=kind)
            for i,kind in enumerate(('prepared','expressed'))]
        for material,expected in (([dict(support=10,time=2.)],0),
            ([dict(support=10,time=2.),dict(support=11,time=6.)],0),
            ([dict(support=10,time=2.),dict(support=11,time=3.)],1)):
            obs.genetic_observer=lambda:SimpleNamespace(summary=lambda:dict(assembly_state=dict(events=material)))
            result=obs.summary();self.assertEqual(result['lipids_from_whole_food_F'],expected)
            self.assertEqual(result['whole_food_F_active_on_lipids'],expected)


if __name__=='__main__':unittest.main()
