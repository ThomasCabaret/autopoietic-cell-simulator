import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.campaign_worker import execute
from simulator.campaign_io import write
from scripts.campaign import prepare
from experiments.prepare_functional_recovery import scenario
from experiments.review_functional_recovery import collect,decide
from experiments.audit_independent_failures import journal


class FunctionalRecoveryTests(unittest.TestCase):
    def test_postcleavage_pair_has_same_atoms_and_only_one_rate_differs(self):
        for seed in range(3):
            a,b=scenario(seed,'fast'),scenario(seed,'slow');x,y=Simulation(a),Simulation(b)
            np.testing.assert_array_equal(x.chemistry.pos,y.chemistry.pos)
            self.assertEqual(x.rng.bit_generator.state,y.rng.bit_generator.state)
            self.assertEqual(len(x.chemistry.pos),150)
            self.assertFalse(any(x.chemistry.families[i]==1 for i,j in x.chemistry.edges))
            self.assertEqual(len(x.chemistry.edges),4)
            a.update(name=b['name']);a['chemistry']['bond_turnover']['rung_f']=.001
            self.assertEqual(a,b)

    def test_real_short_worker_exposes_genetic_diagnostics_and_censoring(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cfg=scenario(0,'fast');cfg['duration']=1.
            p=root/'plan.json';write(p,dict(workers=1,record_trajectory=False,genetic_audit=True,tasks=[dict(scenario=cfg)]))
            folder=prepare(p,root/'campaign');execute(folder,'task0000');r=collect(folder,False)
            self.assertIsNone(r['decision']);self.assertEqual(r['counts']['complete'],1)
            self.assertEqual(r['rows'][0]['first_exact_F01'],dict(time=1.,event=False))
            self.assertIn('recognition_eligible_GF',r['rows'][0]['genetic_exposure'])

    def test_recovery_gate_requires_actual_activity_and_preserved_gene(self):
        rows=[dict(variant=v,seed=s,atoms=150,invariant_failures=0,late_temperature=.08,G01_current=1,
            first_exact_F01=dict(time=10.,event=True),catalysis_after_exact_F01=1) for s in range(3) for v in ('fast','slow')]
        self.assertTrue(decide(rows)['recovery_screens']['slow']['screen_passed'])
        for r in rows:
            if r['variant']=='slow':r['catalysis_after_exact_F01']=0
        self.assertFalse(decide(rows)['recovery_screens']['slow']['screen_passed'])
        self.assertTrue(decide(rows)['recovery_screens']['fast']['screen_passed'])
        rows[0]['G01_current']=0
        self.assertFalse(decide(rows)['recovery_screens']['fast']['screen_passed'])

    def test_journal_check_rejects_missing_bond_event(self):
        cfg=scenario(0,'fast');cfg['duration']=10.;a,b=Simulation(cfg),Simulation(cfg)
        edge=next(iter(a.chemistry.edges));b.chemistry.edges.remove(edge)
        with self.assertRaises(ValueError):journal(a.chemistry,[],b)
        result=journal(a.chemistry,[dict(kind='backbone_break',time=1.,a=edge[0],b=edge[1])],b)
        self.assertTrue(result['final_state_reconstructed'])
