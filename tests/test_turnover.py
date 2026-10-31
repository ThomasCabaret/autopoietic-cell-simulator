import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from experiments.prepare_recycling_campaign import small,rates,transfer
from simulator.config import resolve
from simulator.engine import Simulation
from simulator.runner import make_observer,run,replay
from simulator.spatial import Neighborhood
from simulator import checkpoint
from simulator.observations import CopyObserver


class Certain:
    def random(self):return 0.


class TurnoverTests(unittest.TestCase):
    def test_validation(self):
        for bad in (True,{},dict(rates('full'),rung_g=-1),dict(rates('full'),protection=2),dict(rates('full'),rung_f=float('nan'))):
            cfg=small(0,'zero',1.);cfg['chemistry']['bond_turnover']=bad
            with self.assertRaises(ValueError):resolve(cfg)
        cfg=small(0,'zero',1.);cfg['chemistry']['constructible']=False
        with self.assertRaises(ValueError):resolve(cfg)
        with self.assertRaises(ValueError):CopyObserver(small(0,'zero',1.)['chemistry'])

    def test_zero_rates_preserve_positions_rng_and_chemical_state(self):
        cfg=small(0,'zero',2.);old=copy.deepcopy(cfg);del old['chemistry']['bond_turnover']
        a,b=Simulation(cfg),Simulation(old)
        for sim in (a,b):sim.advance(sim.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        state=a.chemistry.export();state.pop('turnover_events')
        self.assertEqual(state,b.chemistry.export())

    def test_local_protection_and_real_atom_release(self):
        c=Simulation(small(0,'full',1.)).chemistry
        c.rng=Certain();c.turnover.settings=dict(backbone_g=1.,backbone_f=1.,rung_g=1.,rung_f=1.,protection=0.)
        c.pairing[0]=3;c.pairing[3]=0
        cat=c.assembly.catalyst;cat.site_bound[39]=20;cat.atom_bound[20]=39
        pos=c.pos.copy();symbols=c.assembly.atom_bits.copy();n=c.n
        c.turnover.react(c,1.,.002)
        self.assertIn((0,1),c.edges);self.assertIn((3,4),c.edges);self.assertIn((39,40),c.edges)
        self.assertNotIn((1,2),c.edges)
        self.assertEqual(c.rungs[2,1],-1);self.assertEqual(c.bits[2],-1)
        self.assertEqual(c.rungs[39,1],n+39)
        np.testing.assert_array_equal(pos,c.pos);np.testing.assert_array_equal(symbols,c.assembly.atom_bits)

    def test_polymer_to_real_precursors_reassembly_and_reincorporation(self):
        c=Simulation(small(0,'full',1.)).chemistry;obs=make_observer(small(0,'full',1.),False)
        c.observe(obs,0.,[])
        c.rng=Certain();c.turnover.settings=dict(backbone_g=1.,backbone_f=1.,rung_g=1.,rung_f=1.,protection=1.)
        c.turnover.react(c,1.,.002)
        self.assertFalse(c.edges)
        # Controlled local encounter, no dynamics claim: exchange real R partners.
        for s in range(c.n):c.pos[s]=[10.*s,0.];c.pos[c.n+s]=[10.*s,5.]
        s,r=0,c.n+1;c.pos[r]=c.pos[s]+[0.,.45]
        c.config['rung_formation_rate']=1e9
        c.rng=np.random.default_rng(4);start=len(c.assembly.events)
        c.assembly.react(c,2.,.002,Neighborhood());c.turnover.formed(c,2.,start,[])
        self.assertEqual(c.rungs[s,1],r);self.assertEqual(c.bits[s],c.assembly.atom_bits[1])
        # Observer receives journals after multiple transitions between samples.
        c.observe(obs,2.,[])
        self.assertEqual(obs.summary()['polymer_reassemblies'],1)
        # A real templated ligation, existing local laws and geometry.
        for q,r0 in ((1,c.n),(2,c.n+2),(3,c.n+3)):
            c.rungs[q,1]=r0;c.bits[q]=c.assembly.atom_bits[r0-c.n]
        c.pos[[0,1,2,3]]=[[1,1],[2,1],[1,1.9],[2,1.9]]
        c.pos[c.rungs[[0,1,2,3],1]]=c.pos[[0,1,2,3]]+[[0,.45],[0,.45],[0,-.45],[0,-.45]]
        c.edges={(2,3)};c.pairing[:]=-1;c.pairing[[0,1,2,3]]=[2,3,0,1]
        c.turnover.settings=rates('zero');c.config['release']='never';c.config['ligation_rate']=1e9
        c.react(3.,.002,Neighborhood());c.observe(obs,3.,[])
        self.assertIn((0,1),c.edges)
        self.assertEqual(obs.summary()['recycled_incorporations'],1)
        self.assertEqual(obs.summary()['invariant_failures'],0)

    def test_observer_passive_checkpoint_tree_brute_and_replay(self):
        cfg=small(1,'protected',4.);cfg['chemistry']['bond_turnover'].update(backbone_f=1.,rung_f=1.)
        a=Simulation(cfg);obs=make_observer(a.config,False);a.listeners.append(obs);a.advance(431)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'checkpoint.npz';checkpoint.save(path,a,obs)
            b,ob=checkpoint.load(path,make_observer)
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.chemistry.export(),b.chemistry.export());self.assertEqual(obs.summary(),ob.summary())
            cfg['engine']['spatial']='brute';c=Simulation(cfg);c.advance(c.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,c.chemistry.pos)
            cfg['duration']=.1;result,p=run(cfg,d,record=True);replay(p)
            self.assertTrue((p/'trajectory.npz').is_file())
        self.assertEqual(obs.summary()['invariant_failures'],0)

    def test_nested_factory_and_bound_profile(self):
        cfg=transfer(0);cfg['duration']=.01
        sim=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs);sim.prepare()
        c=sim.chemistry;g=c.genetics;s=0;r=int(g.rungs[s,1])
        self.assertTrue(c.bound_atoms()[s]);self.assertEqual(c.kinds[c.offset+s],3)
        g.edges={e for e in g.edges if s not in e};g.pairing[s]=-1
        g.turnover.settings=dict(rates('zero'),rung_g=1e9);g.turnover.react(g,1.,.002);c._mechanics()
        self.assertFalse(c.bound_atoms()[s]);self.assertFalse(c.bound_atoms()[r])
        self.assertEqual(c.kinds[c.offset+s],1);self.assertEqual(c.kinds[c.offset+r],2)
        self.assertEqual(obs.summary()['genetics']['observer'],'reversible_current_census_v1')


if __name__=='__main__':unittest.main()
