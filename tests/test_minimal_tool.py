import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from experiments.prepare_minimal_tool_campaign import prepared,expression,plans
from experiments.tool_product_flux import routes,inventory
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.spatial import Neighborhood
from scripts.minimal_tool_followup import decide,expression_decision
from tests.test_precursors import fixture


def report_row(phase,variant,seed):
    z={p:0 for p in ('G0','G1','F0','F1','G2','F2')}
    table={o:dict(z) for o in ('prepared','expressed','unattributed','background')}
    flux=dict(formed=copy.deepcopy(table),incorporated=copy.deepcopy(table),max_operations=dict(prepared=10,expressed=10))
    if phase=='A' and variant in ('short','long'):
        flux['formed']['prepared'].update(G0=10,F0=10)
    if phase=='B' and variant!='nogene':
        flux['formed']['expressed'].update(G0=10,F0=10);flux['incorporated']['expressed'].update(G0=1,F0=1)
    return dict(label=f'MIN1_{phase}_{variant}_s{seed}',seed=seed,F=0 if variant=='nogene' else 1,
        expressed_products=0 if variant=='nogene' else 20,expressed_used=0 if variant=='nogene' else 2,flux=flux)


class MinimalToolTests(unittest.TestCase):
    def test_A_material_equal_and_only_initial_assembly_changes(self):
        configs=[prepared(0,v,1.) for v in ('long','short','split','no_boost')]
        self.assertTrue(all(inventory(c)==inventory(configs[0]) for c in configs))
        self.assertEqual(inventory(configs[0])['beads'],150)
        laws=[]
        for c in configs[:3]:
            g=copy.deepcopy(c['chemistry']);g.pop('initial_assemblies');laws.append(g)
        self.assertEqual(laws,[laws[0]]*3)
        a,b=Simulation(configs[1]),Simulation(configs[3])
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        for c in configs:
            sim=Simulation(c);self.assertTrue(all(sim.chemistry.families[a]==1 for a,b in sim.chemistry.edges))

    def test_expression_and_nogene_same_atoms_positions_rng_and_no_F_edges(self):
        a,b=(Simulation(expression(1,v,1.)) for v in ('short','nogene'))
        self.assertEqual(inventory(a.config),inventory(b.config))
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertTrue(a.chemistry.edges);self.assertFalse(b.chemistry.edges)
        for sim in (a,b):self.assertTrue(all(sim.chemistry.families[q]==0 for e in sim.chemistry.edges for q in e))
        self.assertEqual(len(Simulation(expression(0,'long',1.)).chemistry.pos),150)
        self.assertEqual([len(p['tasks']) for p in plans()],[12,9])

    def test_short_local_motif_supports_same_real_atom_reaction(self):
        cfg=prepared(0,'short',1.);sim=Simulation(cfg);c=sim.chemistry;n=c.n
        obs=make_observer(sim.config,False);c.observe(obs,0.,[])
        # Ideal contact control, no kinetic inference: first prepared F01.
        a,b=next((a,b) for a,b in sorted(c.edges) if c.bits[a]==0 and c.bits[b]==1)
        p=4;r=n+5;cat=c.assembly.catalyst
        c.pos[p]=[1.,1.];c.pos[r]=[1.,1.45]
        cat.site_bound[a]=p;cat.atom_bound[p]=a;cat.site_bound[b]=r;cat.atom_bound[r]=b
        c.config.update(food_binding_rate=0.,food_unbinding_rate=0.,rung_catalytic_rate=1e9)
        c.assembly.react(c,1.,.002,Neighborhood());c.observe(obs,1.,[])
        data=routes(dict(scenario=sim.config,metrics=obs.summary()))
        self.assertGreater(sum(data['formed']['prepared'].values()),0)
        item=next(e for e in data['products'] if e['support']==p)
        self.assertEqual(item['recognizer'],r);self.assertEqual(item['origin'],'prepared')
        broken=copy.deepcopy(obs.summary());broken['assembly_state']['catalytic_events'].append(
            copy.deepcopy(broken['assembly_state']['catalytic_events'][0]))
        with self.assertRaises(ValueError):routes(dict(scenario=sim.config,metrics=broken))

    def test_bad_symbols_and_reverse_chronology_rejected(self):
        c=fixture();cfg=c.config
        raw=dict(schema_version=1,model='copy',chemistry=cfg,duration=1.)
        sim=Simulation(raw);obs=make_observer(sim.config,False);c.observe(obs,0.,[])
        c.assembly.react(c,1.,.005,Neighborhood());c.observe(obs,1.,[])
        result=dict(scenario=sim.config,metrics=obs.summary());self.assertTrue(routes(result)['products'])
        bad=copy.deepcopy(result);bad['metrics']['assembly_incorporation_times'][3]=.5
        with self.assertRaises(ValueError):routes(bad)
        bad=copy.deepcopy(result);bad['metrics']['assembly_state']['catalytic_events'][0]['symbol']=2
        with self.assertRaises(ValueError):routes(bad)
        bad=copy.deepcopy(result);bad['scenario']['chemistry']['bond_turnover']={}
        with self.assertRaises(ValueError):routes(bad)

    def test_prospective_gates_need_both_material_families_and_controls(self):
        rows=[report_row('A',v,s) for s in range(3) for v in ('long','short','split','no_boost')]
        self.assertTrue(decide(rows)['run_transfer'])
        bad=copy.deepcopy(rows);bad[1]['flux']['formed']['prepared']['F0']=0
        self.assertFalse(decide(bad)['run_transfer'])
        bad=copy.deepcopy(rows)
        for r in bad:
            if 'split' in r['label']:r['flux']['formed']['prepared']['G0']=100
        self.assertFalse(decide(bad)['run_transfer'])
        with self.assertRaises(ValueError):decide(rows[:-1])
        rows=[report_row('B',v,s) for s in range(3) for v in ('short','long','nogene')]
        self.assertTrue(expression_decision(rows)['screen_passed'])
        rows[2]['F']=1;self.assertFalse(expression_decision(rows)['screen_passed'])


if __name__=='__main__':unittest.main()
