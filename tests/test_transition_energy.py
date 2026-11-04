import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.spatial import Neighborhood
from simulator.runner import make_observer
from simulator import checkpoint
from simulator.transition_energy import formation_energy,thermal_factor
from experiments.diagnose_lipid_heat import energy


def config(gate='metropolis',contact=0.):
    return dict(schema_version=1,model='lipid_synthesis',seed=5,duration=.2,
        chemistry=dict(food_units=4,tool_count=1,formation_gate=gate,tool_lipid_contact=contact),
        engine=dict(dt=.002,sample_every=10),mechanics=dict(motion='langevin'))


def local_pose(c,captured=2):
    c.pos[:4]=[[2.,2.],[3.,2.],[2.,2.45],[3.,2.45]]
    c.pos[4:]=[9.,8.];c.pos[4]=[2.5,2.55];c.pos[10]=[2.5,1.9]
    c.pos[5]=[1.5,2.55];c.pos[8]=[1.5,1.9]
    c.lipids.bind(5,8);c.capture.refresh(c);c._mechanics()
    for s,atom in list(enumerate((4,10)))[:captured]:
        c.capture.site_bound[s]=atom;c.capture.atom_bound[atom]=s


class TransitionEnergyTests(unittest.TestCase):
    def test_local_delta_equals_exact_full_potential_difference_without_mutation(self):
        for contact in (0.,.55):
            for captured in (0,1,2):
                sim=Simulation(config(contact=contact));c=sim.chemistry;local_pose(c,captured)
                old=energy(c);saved=copy.deepcopy(c.export());pos=c.pos.copy();rng=copy.deepcopy(sim.rng.bit_generator.state)
                delta=formation_energy(c,4,10,Neighborhood('brute',0.))
                self.assertEqual(c.export(),saved);np.testing.assert_array_equal(c.pos,pos);self.assertEqual(sim.rng.bit_generator.state,rng)
                c.lipids.bind(4,10);c.capture.categories[[4,10]]=-1;c.capture.release(4);c.capture.release(10)
                after=energy(c)
                for k in old:self.assertAlmostEqual(delta[k],after[k]-old[k],places=10)
                self.assertLess(delta['ports'],0.)

    def test_distant_spectators_do_not_enter_the_local_gate(self):
        c=Simulation(config()).chemistry;local_pose(c)
        a=formation_energy(c,4,10,Neighborhood('tree',0.))
        c.pos[[6,7,9,11]]=[30.,20.]
        self.assertEqual(a,formation_energy(c,4,10,Neighborhood('brute',0.)))

    def test_gate_blocks_large_positive_jump_without_repositioning(self):
        for gate in ('none','metropolis'):
            c=Simulation(config(gate,.55)).chemistry;local_pose(c)
            c.pos[4]=[2.3,2.45];c.pos[10]=[2.5,2.45]
            c.config['rung_catalytic_rate']=1e9;before=c.pos.copy()
            c.form_lipids(0.,.01,Neighborhood('brute',0.))
            self.assertEqual(len(c.births),int(gate=='none'));np.testing.assert_array_equal(c.pos,before)
            if gate=='metropolis':self.assertGreater(c.transition_stats['catalytic']['proposals'],0)
        self.assertEqual(thermal_factor(-3.,0.),1.)
        self.assertEqual(thermal_factor(3.,0.),0.)
        self.assertAlmostEqual(thermal_factor(.08,.08),np.exp(-1))

    def test_gate_checkpoint_tree_brute_and_observer_are_exact(self):
        cfg=config();a=Simulation(cfg);b=Simulation(cfg);other=copy.deepcopy(cfg);other['engine']['spatial']='brute';d=Simulation(other)
        obs=make_observer(a.config,False);a.listeners.append(obs)
        a.advance(40);b.advance(40);d.advance(40)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos);np.testing.assert_array_equal(a.chemistry.pos,d.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'gate.npz';checkpoint.save(p,a,obs);c,otherobs=checkpoint.load(p,make_observer)
            a.advance(60);c.advance(60)
            np.testing.assert_array_equal(a.chemistry.pos,c.chemistry.pos);np.testing.assert_array_equal(a.motion.velocities,c.motion.velocities)
            self.assertEqual(a.chemistry.export(),c.chemistry.export());self.assertEqual(obs.summary(),otherobs.summary())


if __name__=='__main__':unittest.main()
