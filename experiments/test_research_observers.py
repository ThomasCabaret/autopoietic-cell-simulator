"""Check that scientific observations do not overstate ancestry or translation."""
import unittest
import numpy as np
from run_local_research import CopyObserver


class Provenance(unittest.TestCase):
    def setup_state(self):
        o = CopyObserver({"sequence": "010"})
        bits = np.tile([0, 1, 0], 4)
        p = np.zeros((24, 2))
        p[:, 0] = np.arange(24)
        pairing = np.full(12, -1)
        edges = {(0, 1), (1, 2)}
        o(0, p, edges, pairing, bits, [])
        edges |= {(3, 4), (4, 5)}
        o(1, p, edges, pairing, bits,
          [{"source": (0, 1), "formed": (3, 4)}, {"source": (1, 2), "formed": (4, 5)}])
        return o, p, pairing, bits, edges

    def test_one_descendant_ligation_is_not_generation_two(self):
        o, p, paired, bits, edges = self.setup_state()
        edges.add((6, 7))
        o(2, p, edges, paired, bits, [{"source": (3, 4), "formed": (6, 7)}])
        self.assertEqual(o.summary()["certified_max_generation"], 1)
        self.assertEqual(o.summary()["certified_detached_generation2"], 0)
        edges.add((7, 8))
        o(3, p, edges, paired, bits, [{"source": (4, 5), "formed": (7, 8)}])
        self.assertEqual(o.summary()["certified_max_generation"], 2)
        self.assertEqual(o.summary()["certified_detached_generation2"], 1)

    def test_mixed_parent_material_is_not_certified_as_one_generation(self):
        o, p, paired, bits, edges = self.setup_state()
        edges |= {(6, 7), (7, 8)}
        o(2, p, edges, paired, bits,
          [{"source": (3, 4), "formed": (6, 7)}, {"source": (1, 2), "formed": (7, 8)}])
        self.assertEqual(o.summary()["complete_copy_sets_ever"], 2)
        self.assertEqual(o.summary()["certified_max_generation"], 1)

    def test_translation_is_not_counted_as_genetic_copy(self):
        o = CopyObserver({"sequence": "010"})
        bits = np.array([0, 1, 0, 0, 1, 0])
        p = np.zeros((12, 2))
        edges = {(0, 1), (1, 2), (3, 4), (4, 5)}
        o(1, p, edges, np.full(6, -1), bits,
          [{"source": (0, 1), "formed": (3, 4)}, {"source": (1, 2), "formed": (4, 5)}],
          np.array([0, 0, 0, 1, 1, 1]))
        self.assertEqual(o.summary()["complete_copy_sets_ever"], 0)
        self.assertEqual(o.summary()["translated_detached_ever"], 1)


if __name__ == "__main__":
    unittest.main()
