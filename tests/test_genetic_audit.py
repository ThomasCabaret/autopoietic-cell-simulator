import copy,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.genetic_audit import GeneticAudit
from simulator import checkpoint
from experiments.run_batch13 import scenario


def geometry():
    cfg=dict(schema_version=1,model='copy',duration=1.,chemistry=dict(sequence='001',free_units=0,function_units=3,
        initial_assemblies=[dict(family=1,sequence=b,backbone=False) for b in '001']))
    c=Simulation(cfg).chemistry
    c.pos[:3]=np.column_stack((np.arange(3),np.zeros(3)))
    c.pos[3:6]=c.pos[:3]+[0.,.9]
    c.pos[6:9]=c.pos[:3]+[0.,.45];c.pos[9:12]=c.pos[3:6]-[0.,.45]
    return c


class GeneticAuditTests(unittest.TestCase):
    def test_recognition_stages_and_external_phase_are_nonvacuous(self):
        c=geometry();a=GeneticAudit();s=a.scan(c,0.)
        self.assertEqual(s['recognition_eligible_GF'],3)
        s=a.scan(c,55.);self.assertEqual(s['recognition_eligible_GF'],0)
        self.assertEqual(s['recognition_blocked_external_release_phase'],3)
        c.pos[9:12]=c.pos[3:6]+[0.,.45]
        self.assertEqual(a.scan(c,0.)['recognition_eligible_GF'],0)

    def test_ligation_eligibility_and_geometric_rejection(self):
        c=geometry();c.pairing[:]=[3,4,5,0,1,2];a=GeneticAudit()
        s=a.scan(c,0.);self.assertEqual(s['ligation_double_paired'],2);self.assertEqual(s['ligation_eligible_F'],2)
        c.pos[4]+=[.7,0.];c.pos[10]+=[.7,0.]
        s=a.scan(c,0.);self.assertEqual(s['ligation_eligible_F'],0)
        self.assertEqual(s['ligation_blocked_distance'],2)

    def test_precursor_eligibility_is_the_existing_catalytic_motif(self):
        from tests.test_precursors import fixture
        c=fixture();a=GeneticAudit();self.assertEqual(a.scan(c,0.)['assembly_catalytic_eligible'],1)
        c.edges.remove((6,7));self.assertEqual(a.scan(c,0.)['assembly_catalytic_eligible'],0)

    def test_observer_does_not_change_any_dynamics_in_either_hook(self):
        for case in ('native','bath'):
            raw=scenario(case,1,2.);a=Simulation(raw);b=Simulation(raw)
            p=GeneticAudit();p.attach(a.chemistry)
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.chemistry.export(),b.chemistry.export())
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
            self.assertAlmostEqual(p.summary(a.time)['observed_time'],a.time)

    def test_resume_preserves_audit_and_counts(self):
        raw=scenario('cold',2,4.);a=Simulation(raw);obs=make_observer(a.config,False);a.listeners.append(obs)
        p=GeneticAudit(window=.25);p.attach(a.chemistry);a.advance(777)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'state.npz';obs.campaign_genetic_state=p.state;checkpoint.save(path,a,obs)
            b,other=checkpoint.load(path,make_observer)
            q=GeneticAudit(other.campaign_genetic_state,window=.25);q.attach(b.chemistry)
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
            self.assertEqual(p.summary(a.time),q.summary(b.time))
            self.assertEqual(obs.summary(),other.summary())

    def test_worker_stop_resume_keeps_diagnostics(self):
        from scripts.campaign import prepare,analyze
        from simulator.campaign_io import read,write
        from simulator.campaign_worker import execute
        with tempfile.TemporaryDirectory() as d:
            plan=Path(d)/'plan.json';raw=scenario('cold',0,1.)
            write(plan,dict(genetic_audit=True,tasks=[dict(scenario=raw)]))
            folder=prepare(plan,Path(d)/'runs');advance=Simulation.advance
            def stop(sim,steps):
                value=advance(sim,steps)
                (folder/'STOP').write_text('pause');return value
            with patch.object(Simulation,'advance',stop):execute(folder,'task0000')
            self.assertEqual(read(folder/'tasks/task0000/state.json')['status'],'paused')
            (folder/'STOP').unlink();execute(folder,'task0000')
            row=analyze(folder)['rows'][0]
            direct=Simulation(raw);p=GeneticAudit();p.attach(direct.chemistry);direct.advance(direct.target_step)
            self.assertEqual(row['genetic_audit']['exposure'],p.summary(direct.time)['exposure'])
            self.assertAlmostEqual(row['genetic_audit']['observed_time'],1.)
