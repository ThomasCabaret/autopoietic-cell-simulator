import copy,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from simulator.turnover import paired_edge,BondTurnover
from simulator.engine import Simulation
from simulator.config import resolve
from simulator.runner import make_observer
from simulator import checkpoint
from simulator.campaign_io import read
from experiments.prepare_pair_protection import scenario,REFERENCE
from experiments.review_pair_protection import decide


class PairProtectionTests(unittest.TestCase):
    def test_protection_requires_reciprocal_pairing_and_a_neighbor_bond_not_food_capture(self):
        c=SimpleNamespace(pairing=np.array([2,3,0,1]),edges={(0,1),(2,3)})
        self.assertTrue(paired_edge(c,0,1));c.edges.remove((2,3));self.assertFalse(paired_edge(c,0,1))
        c.edges.add((2,3));c.pairing[3]=-1;self.assertFalse(paired_edge(c,0,1))
        c.pairing[:]=-1;self.assertFalse(paired_edge(c,0,1))

    def test_only_predicate_changes_and_reversible_observation_and_resume_are_passive(self):
        old=next(t['scenario'] for t in read(REFERENCE/'manifest.json')['tasks'] if t['label']=='RV1_protected_s0')
        cfg=scenario(0);expected=resolve(copy.deepcopy(old));expected.update(name=cfg['name'],branch='RP1')
        expected['chemistry']['bond_turnover']['protection_scope']='paired_edge';self.assertEqual(cfg,expected)
        cfg['duration']=.1;a,b=Simulation(cfg),Simulation(cfg);obs=make_observer(a.config,False);a.listeners.append(obs)
        a.advance(25);b.advance(25);np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'state.npz';checkpoint.save(p,a,obs);new,new_obs=checkpoint.load(p,make_observer)
            a.advance(25);new.advance(25);np.testing.assert_array_equal(a.chemistry.pos,new.chemistry.pos)
            self.assertEqual(a.chemistry.export(),new.chemistry.export());self.assertEqual(obs.summary(),new_obs.summary())

    def test_actual_loss_keeps_paired_edges_but_food_capture_alone_does_not_protect_them(self):
        cfg=scenario(0);cfg['chemistry']['bond_turnover'].update(backbone_g=1e9,backbone_f=1e9,rung_g=0.,rung_f=0.,protection=0.)
        c=Simulation(cfg).chemistry;c.edges={(0,1),(2,3)};c.pairing[:]=-1;c.pairing[:4]=[2,3,0,1]
        c.assembly.catalyst=None;c.turnover.react(c,0.,.002);self.assertEqual(len(c.edges),2)
        c.pairing[:]=-1;c.assembly.catalyst=SimpleNamespace(site_bound=np.zeros(c.n,dtype=int),refresh=lambda _:None)
        c.turnover.react(c,.01,.002);self.assertEqual(c.edges,set())

    def test_useful_material_gate_cannot_pass_with_futile_cycles_or_extinct_genes(self):
        rows=[dict(seed=s,invariant_failures=0,atoms=150,G_current=2,F_current=1,polymer_reassemblies=3,recycled_incorporations=1) for s in range(3)]
        self.assertTrue(decide(rows)['screen_passed']);rows[0]['G_current']=0;self.assertFalse(decide(rows)['screen_passed'])
        rows[0]['G_current']=2
        for r in rows:r['recycled_incorporations']=0
        self.assertFalse(decide(rows)['screen_passed'])
