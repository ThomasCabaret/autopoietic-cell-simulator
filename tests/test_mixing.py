import copy
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from experiments.prepare_mixing_campaign import scenario
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator import checkpoint
from simulator.mixing import information,geometric_clusters
from scripts.campaign import prepare,run
from simulator.campaign_io import read,write
from scripts.mixing_report import analyze


class MixingTests(unittest.TestCase):
    def cfg(self):
        s=scenario(duration=2.)
        s['chemistry'].update(molecules=20,record_interval=.1,box=[12.,10.])
        return s

    def test_no_chemistry_and_passive_observation(self):
        a=Simulation(self.cfg());b=Simulation(self.cfg())
        initial=copy.deepcopy(a.chemistry.bonds())
        obs=make_observer(a.config,False);a.listeners.append(obs)
        a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertEqual(a.chemistry.bonds(),initial)
        self.assertEqual(obs.summary()['isolated_center_D_prediction'],.01)
        for row in obs.state['history']:
            self.assertEqual(sum(row['spatial_grid_counts']),20)
            self.assertLessEqual(row['contacts']['0.3']['unique_pairs'],190)
        json.dumps(obs.summary())

    def test_resume_preserves_contacts_and_information(self):
        a=Simulation(self.cfg());obs=make_observer(a.config,False);a.listeners.append(obs);a.advance(150)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'checkpoint.npz';checkpoint.save(path,a,obs)
            b,resumed=checkpoint.load(path,make_observer)
        a.advance(1000);b.advance(1000)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(obs.summary(),resumed.summary())

    def test_information_and_geometric_clusters(self):
        a=np.repeat(np.arange(4),20)
        self.assertAlmostEqual(information(a,a),np.log(4))
        b=np.tile(np.arange(4),20)
        self.assertAlmostEqual(information(a,b),0.)
        self.assertEqual(geometric_clusters(np.array([[0.,0.],[.5,0.],[4.,0.]]),1.)['largest'],2)

    def test_steric_control_starts_identically_and_no_noise_has_no_free_drift(self):
        a=self.cfg();b=copy.deepcopy(a);b['chemistry']['steric']=False
        x=Simulation(a);y=Simulation(b)
        np.testing.assert_array_equal(x.chemistry.pos,y.chemistry.pos)
        self.assertEqual(x.rng.bit_generator.state,y.rng.bit_generator.state)
        b['chemistry'].update(beads_per_molecule=1,temperature=0.)
        z=Simulation(b);before=z.chemistry.pos.copy();z.advance(100)
        np.testing.assert_array_equal(before,z.chemistry.pos)

    def test_ideal_com_diffusion_scales_with_bead_count(self):
        estimates=[]
        for size in (1,2):
            cfg=scenario(steric=False,size=size,duration=2.)
            cfg['chemistry']['record_interval']=1.
            sim=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs)
            sim.advance(sim.target_step)
            measured=obs.state['history'][-1]['short_lag_bulk_D']
            expected=.25*.08/size
            self.assertLess(abs(measured/expected-1),.08)
            estimates.append(measured)
        self.assertLess(abs(estimates[0]/estimates[1]-2),.2)

    def test_frozen_campaign_report_and_mass(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'plan.json'
            write(p,dict(workers=1,mixing_report=True,record_trajectory=False,
                tasks=[dict(scenario=self.cfg())]))
            folder=prepare(p,Path(d)/'runs')
            self.assertEqual(run(folder),0)
            result=analyze(folder,plots=False)
            self.assertTrue(result['complete_cohort'])
            self.assertTrue(result['rows'][0]['source_verified'])
            self.assertEqual(result['rows'][0]['metrics']['bead_count'],40)


if __name__=='__main__':unittest.main()
