"""Independent finite-difference checks of force/energy consistency."""
import unittest

import numpy as np

from local_dynamics import mechanical_forces, opposite_force, normals, port_attraction, port_sites
from run_local_research import simple_polygon, area


def finite_force(energy, pos):
    result = np.zeros_like(pos)
    h = 1e-6
    for i in range(len(pos)):
        for axis in (0, 1):
            plus, minus = pos.copy(), pos.copy()
            plus[i, axis] += h
            minus[i, axis] -= h
            result[i, axis] = -(energy(plus) - energy(minus)) / (2 * h)
    return result


class LocalMechanics(unittest.TestCase):
    def test_spring_angle_and_soft_core_gradient(self):
        pos = np.array([[0., 0.], [.8, .1], [.25, .95]])
        core = np.full((3, 3), 1.)
        np.fill_diagonal(core, 0)
        springs = [(0, 1, 12., .65)]
        angles = [(0, 1, 2, 3., -.2)]

        def energy(p):
            r = np.linalg.norm(p[:, None] - p[None, :], axis=-1)
            repulsion = 20 * np.sum(np.triu(np.maximum(core - r, 0) ** 2, 1))
            bond = 6 * (np.linalg.norm(p[1] - p[0]) - .65) ** 2
            u, v = p[0] - p[1], p[2] - p[1]
            c = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
            return repulsion + bond + 1.5 * (c + .2) ** 2

        actual = mechanical_forces(pos, springs, angles, core, core_k=40)
        np.testing.assert_allclose(actual, finite_force(energy, pos), atol=1e-7)
        np.testing.assert_allclose(actual.sum(axis=0), 0, atol=1e-12)

    def test_antiparallel_pair_gradient(self):
        pos = np.array([[0., 0.], [.8, .9], [.2, .5], [.6, .4]])
        rungs = np.array([[0, 2], [1, 3]])

        def energy(p):
            n = normals(p, rungs)
            return 8 * (1 + np.dot(n[0], n[1]))

        actual = opposite_force(pos, rungs, [(0, 1)])
        np.testing.assert_allclose(actual, finite_force(energy, pos), atol=1e-7)
        np.testing.assert_allclose(actual.sum(axis=0), 0, atol=1e-12)

    def test_polygon_observer_rejects_crossing(self):
        square = np.array([[0., 0.], [2., 0.], [2., 2.], [0., 2.]])
        self.assertTrue(simple_polygon(square))
        self.assertAlmostEqual(area(square), 4.)
        self.assertFalse(simple_polygon(square[[0, 2, 1, 3]]))

    def test_virtual_port_force_and_torque_gradient(self):
        pos = np.array([[0., 0.], [1.15, .08], [.04, -.65], [1.1, -.58]])
        rungs = np.array([[0, 2], [1, 3]])

        def energy(p):
            sites, anchors, *_ = port_sites(p, rungs, set(), 0, 1.)
            total = 0.
            for i in range(len(sites)):
                for j in range(i + 1, len(sites)):
                    r2 = np.sum((sites[j] - sites[i]) ** 2)
                    if anchors[i] != anchors[j] and r2 < .75 ** 2:
                        total -= .6 * np.exp(-r2 / .25 ** 2)
            return total

        actual = port_attraction(pos, rungs, set(), 0, 1.)
        np.testing.assert_allclose(actual, finite_force(energy, pos), atol=1e-7)
        np.testing.assert_allclose(actual.sum(axis=0), 0, atol=1e-12)


if __name__ == "__main__":
    unittest.main()
