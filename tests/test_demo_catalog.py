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
        rows=verify();self.assertEqual(len(rows),6)
        catalog=DemoCatalog();self.assertEqual(catalog.data['recommended'],'integrated_s2')
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
