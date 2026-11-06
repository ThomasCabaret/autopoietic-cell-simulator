import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.campaign_io import write
from simulator.campaign_worker import execute
from simulator.runner import make_observer
from simulator import checkpoint
from scripts.campaign import prepare
from experiments.prepare_selective_transport import scenario as transport,preflight
from experiments.prepare_functional_recycling import scenario as recycling,RATES
from experiments.review_selective_transport import decide as transport_gate,collect as transport_collect
from experiments.review_functional_recycling import decide as recycling_gate,collect as recycling_collect


class IndependentAssayTests(unittest.TestCase):
    def test_transport_cohorts_and_single_ablation_are_frozen(self):
        self.assertEqual(len(preflight()),3)
        a,b=transport(0,'barrier'),transport(0,'transparent')
        a.update(name=b['name']);a['chemistry']['bound_barrier_radius']=0.;self.assertEqual(a,b)
        sim=Simulation(b);g=sim.chemistry.host;bound=g.rungs[g.rungs[:,1]>=0].copy()
        sim.advance(250);self.assertEqual(len(sim.chemistry.pos),200);self.assertFalse(g.assembly.events)
        np.testing.assert_array_equal(g.rungs[g.rungs[:,1]>=0],bound)

    def test_recycling01_stock_and_zero_loss_are_correct(self):
        cfg=recycling(0,'zero');b=copy.deepcopy(cfg);b['chemistry'].pop('bond_turnover')
        a,plain=Simulation(cfg),Simulation(b);a.advance(100);plain.advance(100)
        np.testing.assert_array_equal(a.chemistry.pos,plain.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,plain.rng.bit_generator.state)
        self.assertEqual(a.chemistry.n,75);self.assertEqual(cfg['chemistry']['sequence'],'01')
        occupied=recycling(0,'occupied');paired=recycling(0,'paired_edge')
        occupied.update(name=paired['name']);occupied['chemistry']['bond_turnover']['protection_scope']='paired_edge'
        self.assertEqual(occupied,paired)
        self.assertEqual(paired['chemistry']['bond_turnover']['rung_f'],RATES['rung_f'])

    def test_transport_unknown_cannot_count_as_retention_or_motion(self):
        rows=[dict(seed=s,variant=v,invariant_failures=0,atoms=200,cohorts_stable=True,late_temperature=.08,
            valid_fraction_late=.95,bound_outside=.05 if v=='barrier' else .4,free_outside=.4) for s in range(3) for v in ('barrier','transparent')]
        self.assertTrue(transport_gate(rows)['screen_passed'])
        rows[0]['bound_outside']=None;self.assertFalse(transport_gate(rows)['screen_passed'])
        rows[0]['bound_outside']=.05;rows[0]['free_outside']=0.;self.assertFalse(transport_gate(rows)['screen_passed'])

    def test_recycling_gate_distinguishes_exact_tool_and_actual_function(self):
        rows=[dict(seed=s,variant=v,atoms=150,invariant_failures=0,late_temperature=.08,G01_current=2,
            F01_current=0,unpaired_F01_edges=1,late_catalysis=10,polymer_reassemblies=1,recycled_incorporations=1)
            for s in range(3) for v in ('zero','occupied','paired_edge')]
        result=recycling_gate(rows)
        self.assertTrue(all(q['screen_passed'] for q in result['protection_screens'].values()))
        for row in rows:
            if row['variant']=='paired_edge':row['late_catalysis']=0
        result=recycling_gate(rows);self.assertFalse(result['protection_screens']['paired_edge']['screen_passed'])
        self.assertTrue(result['protection_screens']['occupied']['screen_passed'])

    def test_real_workers_generate_reviewer_inputs_without_recalculating(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for name,cfg,review in [('transport',transport(1,'barrier'),transport_collect),('recycle',recycling(1,'paired_edge'),recycling_collect)]:
                cfg['duration']=1.;plan=root/(name+'.json');write(plan,dict(workers=1,checkpoint_seconds=.05,record_trajectory=False,tasks=[dict(scenario=cfg)]))
                folder=prepare(plan,root/name);execute(folder,'task0000');report=review(folder,False)
                self.assertEqual(report['counts']['complete'],1);self.assertIsNone(report['decision'])
                row=report['rows'][0];self.assertEqual(row['seed'],1)
                if name=='transport':self.assertTrue(row['cohorts_stable']);self.assertEqual(row['atoms'],200)
                else:self.assertEqual(row['atoms'],150);self.assertIn('unpaired_F01_edges',row)
