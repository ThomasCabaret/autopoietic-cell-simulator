import json
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
        with self.assertRaisesRegex(ValueError, 'requires Langevin mixing'):
            Simulation(config)
        config.update(model='copy', chemistry={})
        with self.assertRaisesRegex(ValueError, 'requires Langevin mixing'):
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

    def test_reactive_copy_tracks_topology_and_resumes_exactly(self):
        from simulator.config import load

        root = Path(__file__).resolve().parents[1]
        cfg = load(root/'demonstrators/configs/demo_binary_copy_langevin.json')
        cpu = Simulation(cfg)
        cfg['engine']['force_backend'] = 'cuda-resident'
        gpu = Simulation(cfg)
        start_edges = gpu.chemistry.edges.copy()
        cpu.advance(1000)
        gpu.advance(507)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'copy.npz'
            checkpoint.save(path, gpu)
            resumed, _ = checkpoint.load(path)
        gpu.advance(493)
        resumed.advance(493)
        self.assertNotEqual(start_edges, gpu.chemistry.edges)
        self.assertTrue(np.any(gpu.chemistry.pairing >= 0))
        self.assertEqual(cpu.chemistry.export(), gpu.chemistry.export())
        self.assertEqual(cpu.rng.bit_generator.state, gpu.rng.bit_generator.state)
        self.assertEqual(cpu.motion.force_evaluations, gpu.motion.force_evaluations)
        np.testing.assert_allclose(cpu.chemistry.pos, gpu.chemistry.pos, rtol=0, atol=1e-10)
        np.testing.assert_allclose(cpu.motion.velocities, gpu.motion.velocities, rtol=0, atol=1e-10)
        np.testing.assert_array_equal(gpu.chemistry.pos, resumed.chemistry.pos)
        self.assertEqual(gpu.motion.export(), resumed.motion.export())
        self.assertEqual(gpu.chemistry.export(), resumed.chemistry.export())
        self.assertEqual(gpu.rng.bit_generator.state, resumed.rng.bit_generator.state)

    def test_catalytic_copy_refreshes_capture_on_binding(self):
        root = Path(__file__).resolve().parents[1]
        path = root/'research/campaign_recipes/FR1_20261106T135511017624Z/manifest.json'
        cfg = json.loads(path.read_text(encoding='utf-8'))['tasks'][0]['scenario']
        cfg['chemistry'].update(food_binding_rate=1e6, rung_formation_rate=0.,
                                rung_catalytic_rate=0.)
        simulations = []
        for backend in ('numba', 'cuda-resident'):
            cfg['engine']['force_backend'] = backend
            sim = Simulation(cfg)
            c = sim.chemistry
            cap = c.assembly.catalyst
            owners = np.flatnonzero(cap.owners >= 0)
            owner = owners[np.argmax(cap.activity[cap.owners[owners]])]
            site = cap.owners[owner]
            ligand = np.flatnonzero(cap.categories == c.bits[site])[0]
            c.pos[ligand] = c.pos[owner] + [.15, 0.]
            simulations.append((sim, site, ligand))
        for sim, site, ligand in simulations:
            # Run mechanics with the free field before the next real reaction.
            sim.prepared = True
            sim.advance(5)
            self.assertEqual(sim.chemistry.assembly.catalyst.site_bound[site], ligand)
            sim.advance(22)
        cpu, gpu = (row[0] for row in simulations)
        self.assertEqual(cpu.chemistry.export(), gpu.chemistry.export())
        self.assertEqual(cpu.rng.bit_generator.state, gpu.rng.bit_generator.state)
        np.testing.assert_allclose(cpu.chemistry.pos, gpu.chemistry.pos, rtol=0, atol=1e-11)
        np.testing.assert_allclose(cpu.motion.velocities, gpu.motion.velocities, rtol=0, atol=1e-11)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'capture.npz'
            checkpoint.save(path, gpu)
            resumed, _ = checkpoint.load(path)
        gpu.advance(23)
        resumed.advance(23)
        np.testing.assert_array_equal(gpu.chemistry.pos, resumed.chemistry.pos)
        self.assertEqual(gpu.motion.export(), resumed.motion.export())
        self.assertEqual(gpu.chemistry.export(), resumed.chemistry.export())

    def test_mixed_fields_find_probes_along_a_stretched_segment(self):
        from experiments.verify_resident_fields import compare, cp1_config

        sim = Simulation(cp1_config())
        sim.prepare()
        c = sim.chemistry
        a, b, _, _ = c.lipids.links[0]
        probe = c.host.rungs[c.host.rungs[:, 1] >= 0][0, 0]
        c.pos[[a, b, probe]] = [[2., 2.], [14., 2.], [8., 2.25]]
        result = compare(c)
        self.assertGreater(result['max_force'][0], 0.)
        self.assertGreater(result['max_force'][1], 0.)

    def test_lipid_ports_keep_real_competition_and_bound_forces(self):
        from experiments.verify_resident_fields import cp1_config
        from simulator.resident_motion import mixed_field_snapshot
        from simulator.spatial import Neighborhood

        c = Simulation(cp1_config()).chemistry
        a, b, d, e = sorted(c.lipids.rungs)[:4]
        heads = [a, b, d, e]
        c.lipids.rungs = {i: c.lipids.rungs[i] for i in heads}
        c.lipids.links = [(a, e, 1, 0)]
        c.pos[heads] = [[6., 6.], [7., 6.15], [7.1, 5.85], [5.2, 5.9]]
        c.pos[list(c.lipids.rungs.values())] = c.pos[heads]+[0., .65]
        fields = []
        for potential in ('additive', 'competitive'):
            c.config['free_port_potential'] = potential
            expected = c.lipids.forces(c.pos, c.config, Neighborhood('brute'))[0]
            actual = mixed_field_snapshot(c)[2]
            np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=1e-12)
            np.testing.assert_allclose(actual.sum(axis=0), 0., atol=1e-12)
            fields.append(expected)
        self.assertGreater(np.max(np.abs(fields[0]-fields[1])), .1)

    def test_mixed_simulation_tracks_new_lipid_and_resumes(self):
        from experiments.verify_resident_fields import cp1_config

        cfg = cp1_config()
        cfg['chemistry'].update(rung_formation_rate=1e6, formation_gate='none')
        simulations = []
        for backend in ('numba', 'cuda-resident'):
            cfg['engine']['force_backend'] = backend
            sim = Simulation(cfg)
            c = sim.chemistry
            ids = [np.flatnonzero(c.ligand_types == kind)[0] for kind in (0, 1)]
            c.pos[ids] = [[17., 17.], [17.4, 17.]]
            sim.prepared = True
            sim.advance(27)
            self.assertEqual(c.lipids.rungs[ids[0]], ids[1])
            simulations.append(sim)
        cpu, gpu = simulations
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'mixed.npz'
            checkpoint.save(path, gpu)
            resumed, _ = checkpoint.load(path)
        for sim in (cpu, gpu, resumed):
            sim.advance(73)
        self.assertEqual(cpu.chemistry.bonds(), gpu.chemistry.bonds())
        self.assertEqual(cpu.rng.bit_generator.state, gpu.rng.bit_generator.state)
        np.testing.assert_allclose(cpu.chemistry.pos, gpu.chemistry.pos, atol=1e-11, rtol=0)
        np.testing.assert_array_equal(gpu.chemistry.pos, resumed.chemistry.pos)
        self.assertEqual(gpu.motion.export(), resumed.motion.export())
        self.assertEqual(gpu.chemistry.export(), resumed.chemistry.export())

    def test_open_resident_bath_remaps_births_and_losses(self):
        from tests.test_open_bath import scenario as open_scenario

        for radius in (0., .25):
            with self.subTest(core_radius=radius):
                config = open_scenario()
                config['chemistry'].update(initial_counts=[0, 0], core_radius=radius)
                cpu = Simulation(config)
                config['engine']['force_backend'] = 'cuda-resident'
                gpu = Simulation(config)
                gpu.advance(1)
                self.assertEqual(gpu.chemistry.pos.shape, (0, 2))
                with tempfile.TemporaryDirectory() as folder:
                    path = Path(folder)/'empty.npz'
                    checkpoint.save(path, gpu)
                    resumed, _ = checkpoint.load(path)
                self.assertEqual(resumed.motion.velocities.shape, (0, 2))
                for sim in (cpu, gpu, resumed):
                    sim.advance(sim.target_step)
                self.assertGreater(gpu.chemistry.injected.sum(), 0)
                self.assertGreater(gpu.chemistry.exported.sum(), 0)
                self.assertEqual(gpu.chemistry.census(gpu.time)['balance_error'], [0, 0])
                self.assertEqual(cpu.chemistry.export(), gpu.chemistry.export())
                self.assertEqual(cpu.rng.bit_generator.state, gpu.rng.bit_generator.state)
                self.assertEqual(cpu.motion.force_evaluations, gpu.motion.force_evaluations)
                np.testing.assert_allclose(cpu.chemistry.pos, gpu.chemistry.pos, atol=1e-11, rtol=0)
                np.testing.assert_array_equal(gpu.chemistry.pos, resumed.chemistry.pos)
                self.assertEqual(gpu.chemistry.export(), resumed.chemistry.export())
                self.assertEqual(gpu.motion.export(), resumed.motion.export())

    def test_device_capture_resolves_one_ligand_between_two_sites(self):
        from experiments.probe_cuda_capture_ticks import capture_scenario, capture_sim, occupancy

        config = capture_scenario(150)
        config['chemistry'].update(food_activation=False, food_binding_rate=1e6,
                                   food_unbinding_rate=0., temperature=0.)
        sims = []
        for steps in ((50,), (25, 25)):
            sim = capture_sim(config, True)
            c = sim.chemistry
            cap = c.assembly.catalyst
            owners = np.flatnonzero(cap.owners >= 0)
            bit = c.bits[cap.owners[owners[0]]]
            sites = owners[c.bits[cap.owners[owners]] == bit][:2]
            ligand = np.flatnonzero(cap.categories == bit)[0]
            cap.categories[:] = -1
            cap.categories[ligand] = bit
            for site, target in zip(sites, ([1., 1.], [1.35, 1.])):
                translation = target-c.pos[site]
                c.pos[c.rungs[cap.owners[site]]] += translation
            c.pos[ligand] = [1.175, 1.]
            for count in steps:
                sim.advance(count)
            self.assertEqual(occupancy(sim, True), 1)
            self.assertIn(sim.motion.partner.get()[ligand], sites)
            np.testing.assert_array_equal(sim.motion.counts.get(), [1, 0])
            np.testing.assert_array_equal(sim.motion.tick.get(), [10])
            sims.append(sim)
        np.testing.assert_array_equal(sims[0].motion.partner.get(), sims[1].motion.partner.get())
        np.testing.assert_array_equal(sims[0].chemistry.pos, sims[1].chemistry.pos)
