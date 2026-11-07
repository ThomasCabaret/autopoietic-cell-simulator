import tempfile
import unittest
from pathlib import Path

import numpy as np

from experiments.benchmark_resident_motion import scenario
from simulator import checkpoint
from simulator.engine import Simulation


class ResidentSelectionTests(unittest.TestCase):
    def test_reject_unsupported_motion_and_reactive_models(self):
        config = scenario(14, 100, 'cuda-resident')
        config['chemistry']['motion'] = 'dpd'
        with self.assertRaisesRegex(ValueError, 'only Langevin mixing'):
            Simulation(config)
        config.update(model='copy', chemistry={})
        with self.assertRaisesRegex(ValueError, 'only Langevin mixing'):
            Simulation(config)


class ResidentMotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import cupy as cp
        except ImportError as exc:
            raise unittest.SkipTest('CuPy unavailable') from exc
        try:
            available = cp.cuda.runtime.getDeviceCount()
        except cp.cuda.runtime.CUDARuntimeError as exc:
            raise unittest.SkipTest('CUDA unavailable') from exc
        if not available:
            raise unittest.SkipTest('No CUDA device')

    def test_cpu_agreement_and_exact_gpu_resume_at_uneven_boundary(self):
        for steric in (False, True):
            with self.subTest(steric=steric):
                simulations = []
                for backend in ('numba', 'cuda-resident'):
                    config = scenario(302, 200, backend)
                    config['chemistry']['steric'] = steric
                    sim = Simulation(config)
                    # Soft wall and a steric contact across a cell boundary.
                    sim.chemistry.pos[:2] = [[-.1, .69], [.05, .71]]
                    simulations.append(sim)
                cpu, gpu = simulations
                ticks = []
                gpu.listeners.append(lambda time, pos, diagnostics: ticks.append(time))
                cpu.advance(200)
                gpu.advance(63)
                with tempfile.TemporaryDirectory() as folder:
                    path = Path(folder)/'mixing.npz'
                    checkpoint.save(path, gpu)
                    resumed, _ = checkpoint.load(path)
                gpu.advance(137)
                resumed.advance(137)
                np.testing.assert_allclose(cpu.chemistry.pos, gpu.chemistry.pos, rtol=0, atol=1e-12)
                np.testing.assert_allclose(cpu.motion.velocities, gpu.motion.velocities,
                                           rtol=0, atol=1e-12)
                np.testing.assert_array_equal(gpu.chemistry.pos, resumed.chemistry.pos)
                self.assertEqual(gpu.motion.export(), resumed.motion.export())
                self.assertEqual(cpu.rng.bit_generator.state, gpu.rng.bit_generator.state)
                self.assertEqual(gpu.rng.bit_generator.state, resumed.rng.bit_generator.state)
                self.assertEqual(ticks, [step*.002 for step in range(0, 201, 25)])

    def test_unstable_block_keeps_last_host_checkpoint(self):
        sim = Simulation(scenario(14, 50, 'cuda-resident'))
        sim.motion.velocities[:] = [1000., 0.]
        initial = sim.chemistry.pos.copy()
        rng_state = sim.rng.bit_generator.state
        with self.assertRaisesRegex(FloatingPointError, 'unstable'):
            sim.advance(25)
        self.assertEqual(sim.step_index, 0)
        self.assertEqual(sim.motion.force_evaluations, 0)
        self.assertEqual(sim.rng.bit_generator.state, rng_state)
        np.testing.assert_array_equal(sim.chemistry.pos, initial)
