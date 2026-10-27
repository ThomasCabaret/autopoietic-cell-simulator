import importlib.util,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from experiments.prepare_compartment_controls import scenario,verify
from experiments.prepare_batch14_bootstrap import scenario as original


class CompartmentControlsTests(unittest.TestCase):
    def test_matched_packets_and_rng_all_six_pairs(self):
        self.assertEqual(len(verify()),6)

    def test_default_remains_identical_to_frozen_J1_dynamics(self):
        path=Path('research/campaign_recipes/J1_20261027T144451586423Z/runtime/simulator/coupled_bath.py')
        spec=importlib.util.spec_from_file_location('simulator._j1_reference',path)
        old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
        raw=original('bath_prepared',0,1.)
        a=Simulation(raw);b=Simulation(raw);b.rng=np.random.default_rng(b.config['seed'])
        b.chemistry=old.CoupledBathChemistry(b.config['chemistry'],b.rng)
        a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.chemistry.export(),b.chemistry.export())
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)

    def test_box_is_global_not_hidden_and_rejects_membrane_override(self):
        raw=scenario('compact',True,0,.02);a=Simulation(raw)
        self.assertEqual(a.chemistry.box.tolist(),[8.,6.])
        self.assertIs(a.chemistry.genetics.box,a.chemistry.box)
        self.assertEqual(a.chemistry.offset,0)
        raw['chemistry']['include_membrane']=True
        with self.assertRaises(ValueError):Simulation(raw)
