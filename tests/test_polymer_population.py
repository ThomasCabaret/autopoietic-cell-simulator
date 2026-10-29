import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from experiments.prepare_population_campaign import scenario
from scripts.campaign import prepare, run, validate
from simulator.campaign_io import read, write
from simulator.campaign_worker import execute
from simulator.engine import Simulation
from simulator.polymer_population import PopulationAudit, canonical
from simulator import checkpoint
from scripts.population_report import analyze, summarize


class PopulationTests(unittest.TestCase):
    def cfg(self):
        cfg = scenario(duration=1.)
        cfg['chemistry'].update(sequence='0011', free_units=20, box=[10., 7.])
        return cfg

    def test_passive_and_checkpointed_population_are_exact(self):
        a = Simulation(self.cfg()); b = Simulation(self.cfg())
        audit = PopulationAudit(a.config, interval=.1); a.listeners.append(audit)
        a.advance(100); b.advance(100)
        np.testing.assert_array_equal(a.chemistry.pos, b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state, b.rng.bit_generator.state)
        self.assertEqual(a.chemistry.export(), b.chemistry.export())
        state = copy.deepcopy(audit.state)
        with tempfile.TemporaryDirectory() as d:
            checkpoint.save(Path(d)/'s.npz', a)
            resumed, _ = checkpoint.load(Path(d)/'s.npz')
        restored = PopulationAudit(resumed.config, state, .1); resumed.listeners.append(restored)
        a.advance(1000); resumed.advance(1000)
        np.testing.assert_array_equal(a.chemistry.pos, resumed.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state, resumed.rng.bit_generator.state)
        self.assertEqual(audit.summary(), restored.summary())
        json.dumps(audit.summary())

    def test_all_sequences_lengths_cycles_and_initial_material_counted(self):
        cfg = Simulation(self.cfg()).config
        audit = PopulationAudit(cfg, interval=.1)
        # Original0011, exact reversed1100, short01, wrong0000, long00110, cycle010.
        texts = ['0011', '1100', '01', '0000', '00110', '010']
        bits = np.array([int(b) for t in texts for b in t]); n = len(bits)
        pos = np.column_stack([np.arange(2*n, dtype=float), np.zeros(2*n)])
        edges = set(); start = 0
        for i, text in enumerate(texts):
            edges.update((j, j+1) for j in range(start, start+len(text)-1))
            if i == len(texts)-1: edges.add((start, start+len(text)-1))
            start += len(text)
        audit(0., pos, edges, np.full(n, -1), bits, [], np.zeros(n, dtype=int))
        row = audit.state['snapshots'][0]
        self.assertEqual(row['accounted_units'], n)
        self.assertEqual(row['categories']['G']['exact_chains'], 2)
        self.assertEqual(row['categories']['G']['same_length_other_chains'], 1)
        self.assertEqual(row['categories']['G']['longer_chains'], 1)
        self.assertEqual(row['categories']['G']['cycle_chains'], 1)
        exact = next(r for r in row['types'] if r['sequence'] == '0011')
        self.assertEqual((exact['new_count'], exact['new_detached_count']), (1, 1))
        self.assertEqual(sum(r['count'] for r in row['types']), len(texts))
        self.assertTrue(row['original_still_separate'])
        self.assertEqual(canonical('100', True), '001')

    def test_frozen_worker_stop_resume_preserves_census(self):
        with tempfile.TemporaryDirectory() as d:
            plan = Path(d)/'plan.json'
            write(plan, dict(workers=1, population_audit=True, population_interval=.1,
                record_trajectory=False, tasks=[dict(scenario=self.cfg())]))
            folder = prepare(plan, Path(d)/'runs'); validate(folder)
            original = Simulation.advance
            def stopped(sim, steps=1):
                result = original(sim, min(steps, 100))
                (folder/'STOP').write_text('pause')
                return result
            with patch.object(Simulation, 'advance', stopped): execute(folder, 'task0000')
            state = read(folder/'tasks/task0000/state.json')
            self.assertEqual(state['status'], 'paused')
            first = read(folder/state['population'])['state']['snapshots']
            self.assertGreater(len(first), 0)
            (folder/'STOP').unlink()
            self.assertEqual(run(folder), 0)
            state = read(folder/'tasks/task0000/state.json')
            self.assertEqual(state['status'], 'complete')
            actual = read(folder/state['population'])
            reference = Simulation(self.cfg()); audit = PopulationAudit(reference.config, interval=.1)
            reference.listeners.append(audit); reference.advance(reference.target_step)
            self.assertEqual(actual, json.loads(json.dumps(audit.summary())))
            self.assertEqual(actual['state']['snapshots'][:len(first)], first)
            report=analyze(folder)
            self.assertTrue(report['complete_cohort'])
            self.assertTrue(report['rows'][0]['source_verified'])
            self.assertEqual(report['rows'][0]['population']['sampled_until'],1.)

    def test_reserve_flag_and_histogram_validation(self):
        sim=Simulation(self.cfg());audit=PopulationAudit(sim.config)
        sim.listeners.append(audit);sim.advance(0)
        population=audit.summary();row=copy.deepcopy(population['state']['snapshots'][0])
        row['time']=200.;row['free_monomers_by_symbol']['G']['0']=0
        population=copy.deepcopy(population);population['state']['snapshots'].append(row)
        report=summarize(population,sim.config)
        self.assertEqual(report['first_reserve_below_half'],200.)
        row['length_distribution']['G']['1']+=1
        with self.assertRaisesRegex(AssertionError,'disagree'):summarize(population,sim.config)


if __name__ == '__main__': unittest.main()
