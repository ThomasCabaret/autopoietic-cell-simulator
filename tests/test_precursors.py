import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from experiments.run_batch8 import scenario
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.runner import run,replay
from simulator.spatial import Neighborhood
from simulator.precursors import precursor_force
from simulator import checkpoint


def fixture(link=True):
    cfg=scenario('C3Bprepared',0,1.,dict(free_units=2,rung_formation_rate=0.,
        rung_catalytic_rate=1e9,food_unbinding_rate=0.,food_binding_rate=0.))
    c=Simulation(cfg).chemistry;n=c.n
    c.pos[3]=[1.,1.];c.pos[n+4]=[1.,1.45]
    c.pos[4]=[6.,1.];c.pos[n+3]=[6.,5.]
    cat=c.assembly.catalyst
    cat.site_bound[6]=3;cat.atom_bound[3]=6
    cat.site_bound[7]=n+4;cat.atom_bound[n+4]=7
    if not link:c.edges.remove((6,7))
    return c


class PrecursorTests(unittest.TestCase):
    def test_local_catalytic_edge_then_product_release_and_real_identity(self):
        c=fixture();n=c.n;c.assembly.react(c,1.,.005,Neighborhood())
        self.assertEqual(len(c.assembly.events),1)
        e=c.assembly.events[0];self.assertTrue(e['catalyzed'])
        self.assertEqual(e['catalytic_support'],[6,7])
        self.assertEqual(c.rungs[3,1],n+4)
        self.assertEqual(c.bits[3],c.assembly.atom_bits[4])
        self.assertEqual(c.assembly.catalyst.site_bound[6],-1)
        self.assertEqual(c.assembly.catalyst.site_bound[7],-1)
        other=fixture(False);other.assembly.react(other,1.,.005,Neighborhood())
        self.assertEqual(other.assembly.events,[])

    def test_prepared_tool_is_not_reported_as_expressed_or_constructed(self):
        sim=Simulation(scenario('C3Bprepared',0,1.));obs=make_observer(sim.config)
        sim.listeners.append(obs);sim.prepare()
        self.assertEqual(obs.summary()['translated_chains_ever'],0)
        self.assertEqual(obs.summary()['constructed_detached_F'],0)
        self.assertIn('prepared',obs.assembly_prior_tools.values())
        self.assertEqual(len(sim.chemistry.bonds()['scaffold']),6)
        with self.assertRaises(ValueError):scenario('C3Bprepared',0,1.,dict(function_units=2))

    def test_no_retroactive_attribution_to_a_newly_observed_tool(self):
        c=fixture();obs=make_observer(Simulation(scenario('C3Bprepared',0,1.,dict(free_units=2))).config)
        c.assembly.react(c,1.,.005,Neighborhood());c.observe(obs,1.,[])
        self.assertEqual(obs.summary()['catalyzed_dimers'],1)
        self.assertEqual(obs.summary()['max_turnovers_per_prepared_tool'],0)
        self.assertIsNone(obs.assembly_catalytic_events[0]['chain_kind'])

    def test_genetic_occupancy_excludes_precursor_capture(self):
        c=Simulation(scenario('C3Bprepared',0,1.,dict(free_units=2,food_binding_rate=1e9))).chemistry
        c.pairing[6]=0;c.pairing[0]=6
        c.pos[3]=c.pos[c.rungs[6,1]]
        c.assembly.catalyst.react(c,.005,Neighborhood())
        self.assertEqual(c.assembly.catalyst.site_bound[6],-1)

    def test_capture_gradient_and_momentum(self):
        c=Simulation(scenario('C3Bprepared',0,1.,dict(free_units=4))).chemistry
        cat=c.assembly.catalyst;pairs=Neighborhood().pairs(c.pos,1.8)
        def evaluate(p):return precursor_force(p,pairs,cat.owners,cat.categories,c.bits,c.pairing,
            cat.site_bound,cat.atom_bound,cat.activity,2.,.6)
        f,_=evaluate(c.pos);numeric=np.zeros_like(f);h=1e-6
        for i in range(len(c.pos)):
            for a in range(2):
                plus=c.pos.copy();minus=c.pos.copy();plus[i,a]+=h;minus[i,a]-=h
                numeric[i,a]=-(evaluate(plus)[1]-evaluate(minus)[1])/(2*h)
        np.testing.assert_allclose(f,numeric,atol=1e-8)
        np.testing.assert_allclose(f.sum(axis=0),0.,atol=1e-12)
        self.assertAlmostEqual(float(np.sum(c.pos[:,0]*f[:,1]-c.pos[:,1]*f[:,0])),0.,places=10)

    def test_tree_brute_checkpoint_and_observation(self):
        raw=scenario('C3Bprepared',1,15.)
        a=Simulation(raw);oa=make_observer(a.config);a.listeners.append(oa);a.advance(1351)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'checkpoint.npz';checkpoint.save(path,a,oa)
            resumed,oc=checkpoint.load(path,make_observer)
            a.advance(a.target_step);resumed.advance(resumed.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,resumed.chemistry.pos)
            self.assertEqual(a.chemistry.export(),resumed.chemistry.export())
            self.assertEqual(oa.summary(),oc.summary())
        other=copy.deepcopy(raw);other['engine']['spatial']='brute'
        b=Simulation(other);ob=make_observer(b.config);b.listeners.append(ob);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(oa.summary(),ob.summary())
        c=a.chemistry;cat=c.assembly.catalyst
        self.assertFalse(np.any((cat.site_bound>=0)&(c.pairing>=0)))
        self.assertEqual(len(oa.times),len(oa.precursor_binding_frames))

    def test_replay_of_material_observer_with_numeric_id_keys(self):
        from experiments.run_batch6 import scenario as assembly_scenario
        with tempfile.TemporaryDirectory() as d:
            result,path=run(assembly_scenario('C3copy',1,80.),d)
            ids=result['metrics']['assembly_incorporation_times']
            self.assertNotEqual([str(k) for k in sorted(ids)],sorted(str(k) for k in ids))
            replay(path)


if __name__=='__main__':unittest.main()
