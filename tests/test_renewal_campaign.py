import copy,unittest
import numpy as np
from simulator.engine import Simulation
from experiments.prepare_renewal_campaign import scenario,plan
from experiments.tool_product_flux import inventory
from experiments.review_renewal import renewal,decide


class RenewalTests(unittest.TestCase):
    def test_only_initial_bonds_change_and_tools_counted(self):
        sims=[Simulation(scenario(0,v,.1)) for v in ('active','split','nogene')];a,b,c=sims
        for sim in sims:
            np.testing.assert_array_equal(sim.chemistry.pos,a.chemistry.pos)
            self.assertEqual(sim.rng.bit_generator.state,a.rng.bit_generator.state)
            self.assertEqual(inventory(sim.config),inventory(a.config))
        self.assertEqual(a.chemistry.edges-b.chemistry.edges,{(39,40)})
        self.assertEqual(c.chemistry.edges,{(39,40)})
        self.assertEqual(len(plan()['tasks']),9)
        from simulator.runner import make_observer
        obs=make_observer(a.config,False);a.listeners.append(obs);a.prepare()
        self.assertEqual(obs.summary()['translated_detached_ever'],0)
        self.assertEqual(obs.summary()['constructed_detached_F'],0)

    def test_new_active_tool_needs_every_unit_constructed_and_prior_birth(self):
        e=dict(time=5.,chain_kind='expressed',chain=[10,11])
        m=dict(constructed_detached_F=1,assembly_state=dict(events=[dict(support=10,time=1.),dict(support=11,time=2.)],catalytic_events=[e]))
        self.assertEqual(renewal(m)['active_wholly_constructed_F'],1)
        for change in ('prepared','missing','late'):
            bad=copy.deepcopy(m)
            if change=='prepared':bad['assembly_state']['catalytic_events'][0]['chain_kind']='prepared'
            if change=='missing':bad['assembly_state']['events'].pop()
            if change=='late':bad['assembly_state']['events'][0]['time']=5.
            self.assertEqual(renewal(bad)['active_wholly_constructed_F'],0)

    def test_gate_requires_real_new_tool_activity_and_nogene_control(self):
        rows=[dict(label=f'MIN1R_{v}_s{s}',seed=s,F_new=int(v!='nogene'),renewal=dict(
            wholly_constructed_detached_F=int(v!='nogene'),active_wholly_constructed_F=int(v!='nogene')))
            for v in ('active','split','nogene') for s in range(3)]
        self.assertTrue(decide(rows)['screen_passed'])
        rows[-1]['F_new']=1;self.assertFalse(decide(rows)['screen_passed'])
        with self.assertRaises(ValueError):decide(rows[:-1])


if __name__=='__main__':unittest.main()
