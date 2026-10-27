import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.spatial import Neighborhood
from simulator.physics import force_kernel
from simulator import checkpoint


def small():
    return dict(schema_version=1,model='coupled_bath',duration=2.,seed=2,
        engine=dict(sample_every=100),chemistry=dict(packet_offset=[0.,0.],
            membrane=dict(units=44,ring_units=40,ring_radius=6.3,box=[26.,26.],
                          contact_exchange_rate=.2,terminal_exchange=True),
            genetics=dict(sequence='001',box=[7.,5.],free_units=6,function_units=3,
                initial_assemblies=[dict(family=1,sequence='001',backbone=True)],
                constructible=True,rung_catalysis=True,rung_formation_rate=20.)))


class CoupledBathTests(unittest.TestCase):
    def test_one_bath_state_contact_and_action_reaction(self):
        sim=Simulation(small());c=sim.chemistry;g=c.genetics
        self.assertTrue(np.shares_memory(c.pos,g.pos))
        self.assertEqual(c.config['temperature'],g.config['temperature'])
        self.assertEqual(c.config['temperature'],c.membrane.config['temperature'])
        self.assertEqual(c.contact[0,c.kinds[c.offset+3]],0.)
        self.assertEqual(c.contact[0,c.kinds[c.offset]],.55)
        # The same real P/R atoms acquire permeability through their local bond.
        r=g.n+3;g.rungs[3,1]=r;c._mechanics()
        self.assertEqual(c.contact[0,c.kinds[c.offset+3]],.55)
        self.assertEqual(c.contact[0,c.kinds[c.offset+r]],.55)
        from simulator.membrane_bath import barrier_force
        p=np.array([[0.,0.],[1.,0.],[.5,.2]])
        f,_=barrier_force(p,np.array([[0,1]]),np.array([2]),np.array([[0,0]]),.55,80.)
        np.testing.assert_allclose(f.sum(axis=0),0.,atol=1e-12)

    def test_existing_mechanics_offsets_and_shared_core(self):
        sim=Simulation(small());sim.prepare();c=sim.chemistry;nb=Neighborhood()
        pairs=nb.pairs(c.pos,float(c.contact.max()),'whole')
        combined=force_kernel(c.pos,pairs,c.kinds,c.contact,c.springs,c.angles)
        g=c.genetics;m=c.membrane
        # The initial packet is far from L, so the joint mechanical force is
        # precisely the sum of the old forces (not two independent advances).
        expected=np.concatenate((force_kernel(m.pos,nb.pairs(m.pos,.4,'m'),m.kinds,m.contact,m.springs,m.angles),
            force_kernel(g.pos,nb.pairs(g.pos,.7,'g'),g.kinds,g.contact,g.springs,g.angles)))
        np.testing.assert_allclose(combined,expected,atol=1e-12)
        self.assertEqual(c.mobility.shape,(len(c.pos),1))

    def test_observer_is_read_only_and_resume_exact_after_real_assembly(self):
        raw=small();a=Simulation(raw);b=Simulation(raw)
        oa=make_observer(a.config,False);a.listeners.append(oa)
        a.advance(333);b.advance(333)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state.npz';checkpoint.save(p,a,oa)
            resumed,other=checkpoint.load(p,make_observer)
            a.advance(a.target_step);resumed.advance(resumed.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,resumed.chemistry.pos)
            self.assertEqual(a.chemistry.export(),resumed.chemistry.export())
            self.assertEqual(a.rng.bit_generator.state,resumed.rng.bit_generator.state)
            self.assertEqual(oa.summary(),other.summary())
        self.assertGreater(len(a.chemistry.genetics.assembly.events),0)

    def test_no_hidden_native_walls_tree_brute_and_no_membrane(self):
        raw=small();a=Simulation(raw);braw=copy.deepcopy(raw);braw['engine']['spatial']='brute'
        b=Simulation(braw);a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.chemistry.genetics.box.tolist(),[26.,26.])
        raw['chemistry']['include_membrane']=False;c=Simulation(raw);c.advance(20)
        self.assertEqual(c.chemistry.offset,0)
        self.assertEqual(len(c.chemistry.pos),len(c.chemistry.genetics.pos))

    def test_reject_two_temperatures_or_nonconstructible_material(self):
        for patch in (dict(genetics=dict(temperature=.6,constructible=True)),
                      dict(genetics=dict(constructible=False))):
            raw=small();raw['chemistry'].update(patch)
            with self.assertRaises(ValueError):Simulation(raw)

    def test_campaign_exports_real_material_metrics_not_membrane_placeholders(self):
        from scripts.campaign import prepare,analyze
        from simulator.campaign_io import write
        from simulator.campaign_worker import execute
        raw=small();raw['duration']=.02
        with tempfile.TemporaryDirectory() as d:
            plan=Path(d)/'plan.json';write(plan,dict(tasks=[dict(scenario=raw)]))
            folder=prepare(plan,Path(d)/'runs');execute(folder,'task0000')
            report=analyze(folder);row=report['rows'][0]
            self.assertEqual(row['genetics']['assembled_dimers'],0)
            self.assertIn('near_membrane_atom_time',row['transport'])
            self.assertIn('Produits génétiques matériels',(folder/'analysis.md').read_text(encoding='utf-8'))
