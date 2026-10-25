import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from experiments.run_batch6 import scenario
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.spatial import Neighborhood
from simulator import checkpoint


def attach(sim):
    obs=make_observer(sim.config);sim.listeners.append(obs);return obs


class AssemblyTests(unittest.TestCase):
    def test_actual_partner_defines_symbol_and_saturation(self):
        c=Simulation(scenario('C3copy',0,1.,dict(free_units=3,rung_formation_rate=1e8))).chemistry
        self.assertTrue(np.all(c.rungs[3:,1]==-1))
        self.assertTrue(np.all(c.bits[3:]==-1))
        before=c.pos.copy();n=c.n
        # Support3 and recognizer4 are different initial pool indices/bits.
        c.pos[3]=[1.,1.];c.pos[n+4]=[1.,1.45]
        c.pos[4]=[6.,1.];c.pos[5]=[6.,4.]
        c.pos[n+3]=[6.,5.];c.pos[n+5]=[2.,5.]
        c.assembly.react(c,0.,.005,Neighborhood())
        made=[e for e in c.assembly.events if e['recognizer']==n+4]
        self.assertEqual(len(made),1)
        s=made[0]['support'];self.assertEqual(s,3)
        self.assertEqual(c.bits[s],c.assembly.atom_bits[4])
        c.assembly.react(c,1.,.005,Neighborhood())
        used=c.rungs[c.rungs[:,1]>=0,1]
        self.assertEqual(len(used),len(set(used.tolist())))
        self.assertEqual(c.pos.shape,before.shape)

    def test_unassembled_sites_cannot_capture_or_polymerize(self):
        c=Simulation(scenario('C3noassembly',0,1.)).chemistry
        for k in range(100):c.react(k*.025,.005,Neighborhood())
        self.assertEqual(len(c.edges),2)
        self.assertTrue(np.all(c.pairing==-1))
        self.assertEqual(c.assembly.events,[])
        self.assertEqual(len(c.bonds()['scaffold']),3)

    def test_prepared_stock_is_exact_same_mechanics(self):
        raw=scenario('C3prepared',0,10.)
        a=Simulation(raw);oa=attach(a)
        other=copy.deepcopy(raw);other['chemistry']['constructible']=False
        b=Simulation(other);ob=attach(b)
        a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.chemistry.edges,b.chemistry.edges)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        for key,val in ob.summary().items():
            if key!='history':self.assertEqual(oa.summary()[key],val)

    def test_tree_brute_checkpoint_and_material(self):
        raw=scenario('C3copy',1,15.)
        a=Simulation(raw);oa=attach(a)
        a.advance(1351)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'state.npz';checkpoint.save(path,a,oa)
            resumed,oc=checkpoint.load(path,make_observer)
            a.advance(a.target_step);resumed.advance(resumed.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,resumed.chemistry.pos)
            self.assertEqual(a.chemistry.export(),resumed.chemistry.export())
            self.assertEqual(oa.summary(),oc.summary())
        other=copy.deepcopy(raw);other['engine']['spatial']='brute'
        b=Simulation(other);ob=attach(b);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(oa.summary(),ob.summary())
        c=a.chemistry;bound=c.rungs[:,1]>=0
        self.assertEqual(len(c.pos),2*c.n)
        np.testing.assert_array_equal(c.bits[bound],c.assembly.atom_bits[c.rungs[bound,1]-c.n])
        self.assertEqual(len(oa.frames),len(oa.rungs_frames))
        self.assertEqual(len(oa.frames),len(oa.unit_bits_frames))
        self.assertEqual(len(set(c.rungs[bound,1])),int(bound.sum()))

    def test_constructible_rejects_unported_helpers(self):
        for change in (dict(food_pairs=1),dict(dual_faces=True)):
            with self.assertRaises(ValueError):Simulation(scenario('C3copy',0,1.,change))


if __name__=='__main__':unittest.main()
