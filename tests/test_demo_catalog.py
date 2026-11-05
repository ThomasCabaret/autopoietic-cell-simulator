import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from visualizer.demos import DemoCatalog,dynamics_hash,ROOT
from visualizer.observations import live_observations
from simulator.engine import Simulation
from simulator.runner import make_observer


class DemoCatalogTests(unittest.TestCase):
    def test_all_presets_match_research_inputs_and_declared_initial_material(self):
        from experiments.prepare_demo_catalog import verify
        rows=verify();self.assertEqual(len(rows),39)
        catalog=DemoCatalog();self.assertEqual(catalog.data['recommended'],'current_energy_s0')
        _,_,cfg=catalog.get('integrated_s2');sim=Simulation(cfg);g=sim.chemistry.genetics
        prepared_g=1+sum(q['family']==0 and q['backbone'] and len(q['units'])==3 for q in g.initial_groups)
        prepared_f=sum(q['family']==1 and q['backbone'] and len(q['units'])==3 for q in g.initial_groups)
        self.assertEqual((prepared_g,prepared_f),(16,16))
        self.assertEqual((sim.chemistry.membrane.n,sim.chemistry.membrane.config['ring_units']),(243,219))
        _,_,cfg=catalog.get('material_cycle');g=Simulation(cfg).chemistry
        self.assertFalse(any(q['backbone'] for q in g.initial_groups))
        self.assertEqual(sum(len(q['units']) for q in g.initial_groups),6)

    def test_catalog_resolves_scenarios_independently_of_working_directory(self):
        with tempfile.TemporaryDirectory() as d:
            old=Path.cwd()
            try:
                os.chdir(d);variant,info,cfg=DemoCatalog().get('free_membrane')
                self.assertEqual(cfg['chemistry']['initial'],'dispersed_units')
                self.assertEqual(variant['beads'],72)
            finally:os.chdir(old)

    def test_changed_dynamics_are_rejected_instead_of_silently_relabeling_a_demo(self):
        catalog=DemoCatalog();variant,info,cfg=catalog.get('integrated_s2')
        data=copy.deepcopy(catalog.data)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);path=root/variant['config'];path.parent.mkdir(parents=True)
            cfg['chemistry']['temperature']*=2;path.write_text(json.dumps(cfg),encoding='utf-8')
            c=root/'catalog.json';c.write_text(json.dumps(data),encoding='utf-8')
            with patch('visualizer.demos.ROOT',root),patch('visualizer.demos.simulator_hashes',return_value=data['simulator_sha256']),self.assertRaisesRegex(ValueError,'changé'):
                DemoCatalog(c).get('integrated_s2')

    def test_changed_engine_code_requires_review_before_reusing_demo_labels(self):
        with patch('visualizer.demos.simulator_hashes',return_value={}),self.assertRaisesRegex(ValueError,'moteur a changé'):
            DemoCatalog().get('integrated_s2')

    def test_live_counts_match_primary_observer_and_exclude_prepared_tools(self):
        _,_,cfg=DemoCatalog().get('integrated_s0');cfg['duration']=2.
        sim=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs)
        sim.advance(sim.target_step);before=copy.deepcopy(obs.summary())
        pos=sim.chemistry.pos.copy();rng=copy.deepcopy(sim.rng.bit_generator.state)
        view=live_observations(obs);rows=dict(view['rows']);gen=before['genetics']
        self.assertEqual(rows['Nouveaux G libérés'],gen['detached_copy_sets_ever'])
        self.assertEqual(rows['Nouveaux F libérés'],gen['translated_detached_ever'])
        self.assertEqual(rows['Dont catalysés'],gen['catalyzed_dimers'])
        self.assertEqual(rows['Catalysés puis réutilisés'],gen['catalyzed_incorporated'])
        self.assertEqual(rows['Nouveaux F libérés'],0)
        self.assertEqual(before,obs.summary());np.testing.assert_array_equal(pos,sim.chemistry.pos)
        self.assertEqual(rng,sim.rng.bit_generator.state)

    def test_current_probe_readout_is_passive_and_preserves_unknown_states(self):
        _,_,cfg=DemoCatalog().get('current_probes_s2');cfg['duration']=.25
        sim=Simulation(cfg);other=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs)
        sim.advance(sim.target_step);other.advance(other.target_step)
        before=copy.deepcopy(obs.summary());rng=copy.deepcopy(sim.rng.bit_generator.state)
        rows=dict(live_observations(obs)['rows'])
        self.assertIn('Sondes retenues dedans',rows);self.assertIn('Sondes perméables entrées',rows)
        self.assertEqual(before,obs.summary());self.assertEqual(rng,sim.rng.bit_generator.state)
        np.testing.assert_array_equal(sim.chemistry.pos,other.chemistry.pos)
        self.assertEqual(sim.rng.bit_generator.state,other.rng.bit_generator.state)
        obs.history[-1]['envelope_valid']=False
        self.assertEqual(dict(live_observations(obs)['rows'])['Sondes retenues dedans'],'non classable')

    def test_food_derived_readout_requires_full_material_and_later_activity(self):
        from types import SimpleNamespace
        state=dict(detached=set(),translated_detached={(10,11),(12,13)},history=[dict(time=6.)],
            assembly_state=dict(events=[dict(support=q,time=2.) for q in (10,11,12)]),
            assembly_catalytic_events=[dict(support=20,catalyzed=True,chain_kind='expressed',chain=[10,11],time=5.),
                dict(support=21,catalyzed=True,chain_kind='expressed',chain=[12,13],time=5.),
                dict(support=22,catalyzed=True,chain_kind='expressed',chain=[10,12],time=1.)],
            assembly_incorporated=set())
        obs=SimpleNamespace(**state);before=copy.deepcopy(obs.__dict__)
        rows=dict(live_observations(obs)['rows'])
        self.assertEqual(rows['F entièrement refaits depuis nourriture'],1)
        self.assertEqual(rows['Dont actifs après libération'],1)
        self.assertEqual(obs.__dict__,before)

    def test_mixed_scene_has_real_species_and_passive_lipid_counters(self):
        from visualizer.scene import species
        _,_,cfg=DemoCatalog().get('current_mixed_s0');cfg['duration']=.05
        sim=Simulation(cfg);plain=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs)
        sim.advance(sim.target_step);plain.advance(plain.target_step)
        codes,labels,palette=species(sim.chemistry)
        self.assertEqual(len(codes),198);self.assertTrue((codes>=0).all());self.assertTrue((codes<len(labels)).all())
        self.assertIn('Support G',labels);self.assertIn('Support F',labels)
        self.assertTrue(all(labels[q].startswith('H ') for q in codes[150:174]))
        self.assertTrue(all(labels[q].startswith('T ') for q in codes[174:198]))
        before=copy.deepcopy(obs.summary());view=dict(live_observations(obs)['rows'])
        self.assertEqual(view['Lipides fabriqués depuis H/T'],before['lipids_formed'])
        self.assertEqual(view['Dont par F entièrement refaits'],before['lipids_from_whole_food_F'])
        self.assertEqual(before,obs.summary());np.testing.assert_array_equal(sim.chemistry.pos,plain.chemistry.pos)
        self.assertEqual(sim.rng.bit_generator.state,plain.rng.bit_generator.state)

    def test_energy_demo_readout_does_not_change_the_simulation_or_confuse_proposals_with_acceptances(self):
        _,info,cfg=DemoCatalog().get('current_energy_s0');cfg['duration']=.05
        sim=Simulation(cfg);plain=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs)
        sim.advance(sim.target_step);plain.advance(plain.target_step)
        before=copy.deepcopy(obs.summary());rows=dict(live_observations(obs)['rows'])
        self.assertEqual(rows['Échanges proposés (filtre local)'],before['exchange_gate_stats']['proposals'])
        self.assertEqual(rows['Échanges acceptés'],before['exchange_gate_stats']['accepted'])
        self.assertIn('maintien',info['limits']);self.assertEqual(before,obs.summary())
        np.testing.assert_array_equal(sim.chemistry.pos,plain.chemistry.pos)
        self.assertEqual(sim.rng.bit_generator.state,plain.rng.bit_generator.state)
