import copy,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.coupled_bath import genetics_config
from experiments.prepare_expression_campaign import baseline
from experiments.prepare_membrane_renewal import scenario,plan,VARIANTS
from experiments.tool_product_flux import inventory
from experiments.review_membrane_renewal import decide


class MembraneRenewalTests(unittest.TestCase):
    def test_matched_controls_and_frozen_physics(self):
        for seed in range(3):
            sims={v:Simulation(scenario(seed,v,.02)) for v in VARIANTS};a=sims['active'];g=a.chemistry.genetics
            old=genetics_config(baseline(seed)['chemistry']);new=genetics_config(a.config['chemistry'])
            for k in ('sequence','free_units','initial_assemblies'):old.pop(k);new.pop(k)
            self.assertEqual(old,new)
            self.assertEqual(len(a.chemistry.pos),2118);self.assertEqual(g.n,816)
            self.assertEqual(len(sims['noL'].chemistry.pos),1632)
            self.assertEqual(sum(g.rungs[:,1]>=0),128)
            center=a.chemistry.box/2
            self.assertLess(np.linalg.norm(g.pos-center,axis=1).max(),33.5)
            for other in sims.values():
                np.testing.assert_array_equal(g.pos,other.chemistry.genetics.pos)
                if other is not sims['noL']:
                    self.assertEqual(a.rng.bit_generator.state,other.rng.bit_generator.state)
                self.assertEqual(inventory(a.config),inventory(other.config))
            self.assertEqual(len(g.edges-sims['split'].chemistry.genetics.edges),16)
            self.assertEqual(len(sims['nogene'].chemistry.genetics.edges),16)
            obs=make_observer(a.config,False);a.listeners.append(obs);a.prepare()
            self.assertEqual(obs.summary()['genetics']['constructed_detached_F'],0)
        self.assertEqual(len(plan()['tasks']),12)

    def test_same_seed_success_must_include_both_material_and_membrane(self):
        rows=[dict(label=f'MIN1M_{v}_s{s}',seed=s,F_new=int(v!='nogene'),
            renewal=dict(active_wholly_constructed_F=int(v!='nogene')),
            physical=dict(regular_parent_closed_fraction=.8)) for s in range(3) for v in VARIANTS]
        d=decide(rows);self.assertTrue(d['screen_passed']);self.assertFalse(d['run_transfer'])
        bad=copy.deepcopy(rows);bad[-1]['F_new']=1;self.assertFalse(decide(bad)['screen_passed'])
        # Two material hits and two closure hits, but only one joint hit.
        a=[r for r in rows if r['label'].startswith('MIN1M_active')]
        a[0]['physical']['regular_parent_closed_fraction']=.6;a[2]['renewal']['active_wholly_constructed_F']=0
        self.assertFalse(decide(rows)['screen_passed'])
        with self.assertRaises(ValueError):decide(rows[:-1])

    def test_single_cohort_stops_even_when_successful(self):
        from scripts.expression_followup import step
        from simulator.campaign_io import write,read
        rows=[dict(label=f'MIN1M_{v}_s{s}',seed=s,F_new=int(v!='nogene'),
            renewal=dict(active_wholly_constructed_F=int(v!='nogene')),
            physical=dict(regular_parent_closed_fraction=.8)) for s in range(3) for v in VARIANTS]
        with tempfile.TemporaryDirectory() as d:
            job=Path(d);write(job/'state.json',dict(phase='running_0',stage=0))
            cfg=dict(campaigns=[d],max_wall_seconds=86400)
            snap=dict(controller_active=False,counts=dict(complete=12,failed=0,paused=0,interrupted=0),
                tasks=[dict(worker_active=False)]*12)
            with patch('scripts.expression_followup.validate_job',return_value=cfg),\
                patch('scripts.expression_followup.campaign_status',return_value=snap),\
                patch('scripts.expression_followup.subprocess.Popen') as launch:
                self.assertEqual(step(job,lambda _:dict(rows=rows),decide),'needs_interpretation')
                self.assertEqual(read(job/'state.json')['stage'],0)
                self.assertTrue(read(job/'report_0.json')['decision']['screen_passed'])
                self.assertEqual(step(job,lambda _:self.fail('Reanalysis'),decide),'needs_interpretation')
                launch.assert_not_called()


if __name__=='__main__':unittest.main()
