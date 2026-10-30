import copy,unittest
import numpy as np
from simulator.engine import Simulation
from experiments.prepare_membrane_diagnostic import plan
from experiments.probe_membrane_failure import MembraneLoupe


class MembraneLoupeTests(unittest.TestCase):
    def test_bounded_loupe_does_not_change_positions_rng_or_links(self):
        cfg=copy.deepcopy(plan()['tasks'][0]['scenario']);cfg['duration']=.1
        cfg['chemistry']['membrane']['bond_off_rate']=20.
        a=Simulation(cfg);b=Simulation(cfg);a.advance(a.target_step)
        with MembraneLoupe(b,window=(0.,.1),before=.02,after=.03,max_units=6) as probe:
            while not b.done:b.advance(5);probe.tick()
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        np.testing.assert_array_equal(a.motion.velocities,b.motion.velocities)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertEqual(a.chemistry.membrane.face_links,b.chemistry.membrane.face_links)
        self.assertIsNotNone(probe.trigger);self.assertLessEqual(len(probe.ids),6)
        self.assertLessEqual(len(probe.events),64)
        self.assertLessEqual(max(r['time'] for r in probe.frames),probe.trigger+.03+1e-8)

    def test_five_diagnostic_variants_have_no_new_particle_inventory(self):
        tasks=plan()['tasks'];self.assertEqual(len(tasks),5)
        positions=Simulation(tasks[0]['scenario']).chemistry.pos
        for task in tasks[1:]:
            np.testing.assert_array_equal(Simulation(task['scenario']).chemistry.pos,positions)


if __name__=='__main__':unittest.main()
