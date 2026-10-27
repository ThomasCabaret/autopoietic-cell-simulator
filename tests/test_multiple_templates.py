import unittest
import importlib.util
from pathlib import Path
import numpy as np
from simulator.observations import CopyObserver
from simulator.config import resolve
from simulator.engine import Simulation


class MultipleTemplateObserverTests(unittest.TestCase):
    def test_each_prepared_gene_can_certify_a_copy_and_expression(self):
        cfg=resolve(dict(schema_version=1,model='copy',chemistry=dict(sequence='001',free_units=6,function_units=3,
            initial_assemblies=[dict(family=0,sequence='001',backbone=True)])))['chemistry']
        o=CopyObserver(cfg);o.record_trajectory=False
        self.assertEqual(o.certified,{(0,1,2):0,(3,4,5):0})
        bits=np.tile([0,0,1],4);families=np.array([0]*9+[1]*3);pairing=np.full(12,-1)
        pos=np.zeros((24,2));pos[:,0]=np.arange(24)
        edges={(0,1),(1,2),(3,4),(4,5)};o(0.,pos,edges,pairing,bits,[],families)
        edges|={(6,7),(7,8)}
        events=[dict(source=(3,4),formed=(6,7)),dict(source=(4,5),formed=(7,8))]
        o(1.,pos,edges,pairing,bits,events,families)
        self.assertEqual(o.certified[(6,7,8)],1)
        edges|={(9,10),(10,11)}
        o(2.,pos,edges,pairing,bits,[dict(source=(3,4),formed=(9,10)),dict(source=(4,5),formed=(10,11))],families)
        self.assertEqual(o.edge_parent[(9,10)],(3,4,5))
        self.assertEqual(o.summary()['translated_detached_ever'],1)

    def test_partial_wrong_or_functional_groups_are_not_gene_parents(self):
        cfg=resolve(dict(schema_version=1,model='copy',chemistry=dict(sequence='001',free_units=8,function_units=3,
            initial_assemblies=[dict(family=0,sequence='01',backbone=True),dict(family=0,sequence='111',backbone=True),
                                dict(family=1,sequence='001',backbone=True)])))['chemistry']
        self.assertEqual(CopyObserver(cfg).certified,{(0,1,2):0})

    def test_single_template_metrics_stay_exact_to_frozen_observer(self):
        path=Path('research/campaign_recipes/J2_20261027T162612551317Z/runtime/simulator/observations.py')
        spec=importlib.util.spec_from_file_location('simulator._j2_observer',path)
        old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
        raw=dict(schema_version=1,model='copy',duration=2.,chemistry=dict(sequence='001',free_units=6,function_units=3,
            constructible=True,rung_catalysis=True,initial_assemblies=[dict(family=1,sequence='001',backbone=True)]))
        sim=Simulation(raw);new=CopyObserver(sim.config['chemistry']);prior=old.CopyObserver(sim.config['chemistry'])
        new.record_trajectory=prior.record_trajectory=False
        sim.listeners.extend([new,prior]);sim.advance(sim.target_step)
        self.assertEqual(new.summary(),prior.summary())
