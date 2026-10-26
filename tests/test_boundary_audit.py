import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.boundary_audit import BoundaryAudit
from simulator.kinetics import KineticProbe
from simulator.campaign_worker import execute
from simulator.campaign_io import read,write
from scripts.campaign import prepare,analyze
from tests.test_campaign import scenario


class BoundaryAuditTests(unittest.TestCase):
    def sample(self,sim,primary,audit,t,remove=()):
        edges=[set(row) for row in sim.chemistry.edges]
        for pair in remove:
            for row in edges:row.remove(pair)
        links=[e for e in sim.chemistry.face_links if (e[0],e[1]) not in remove]
        primary(t,sim.chemistry.pos,edges,links)
        audit(t,sim.chemistry.pos,edges,links)
        return audit.state['last_kind']

    def test_fragments_with_nearby_endpoints_are_not_falsely_sealed(self):
        sim=Simulation(scenario());obs=make_observer(sim.config,False);audit=BoundaryAudit(sim.config,obs)
        kind=self.sample(sim,obs,audit,0.,((0,1),(20,21)))
        self.assertEqual(kind,'fragmented_parent')
        item=audit.state['history'][-1]
        self.assertEqual(item['parent_components'],2)
        self.assertEqual(item['parent_endpoints'],4)
        self.assertLess(item['nearest_endpoint_max'],1.2)
        self.assertFalse(obs.history[-1]['envelope_valid'])
        self.assertIsNone(obs.summary()['retained_escape_fraction'])

    def test_large_open_arc_remains_unknown(self):
        sim=Simulation(scenario());obs=make_observer(sim.config,False);audit=BoundaryAudit(sim.config,obs)
        self.assertEqual(self.sample(sim,obs,audit,0.,((0,1),(8,9))),'long_endpoint_gap')
        self.assertEqual(audit.state['history'][-1]['largest_original_fraction'],.8)
        self.assertFalse(obs.history[-1]['envelope_valid'])

    def test_episode_lengths_and_state_times_are_different_sampled_measures(self):
        sim=Simulation(scenario());obs=make_observer(sim.config,False);audit=BoundaryAudit(sim.config,obs)
        for t,remove in [(0.,()),(.5,()),(1.,((0,1),)),(1.5,((0,1),)),(2.,())]:
            self.sample(sim,obs,audit,t,remove)
        result=audit.summary()
        self.assertEqual(result['state_time'],dict(closed=1.,open_classifiable=1.))
        self.assertEqual(result['longest_observed_span_by_state'],dict(closed=.5,open_classifiable=.5))
        self.assertEqual(result['closed_to_nonclosed_samples'],1)

    def test_audit_does_not_change_positions_rng_or_legacy_observations(self):
        a=Simulation(scenario());b=Simulation(scenario())
        oa=make_observer(a.config,False);ob=make_observer(b.config,False)
        audit=BoundaryAudit(a.config,oa);a.listeners.extend((oa,audit));b.listeners.append(ob)
        a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertEqual(a.chemistry.export(),b.chemistry.export())
        self.assertEqual(oa.summary(),ob.summary())
        self.assertEqual(audit.summary()['samples'],len(oa.times))

    def test_worker_resume_preserves_audit_and_old_metrics(self):
        with tempfile.TemporaryDirectory() as d:
            plan=Path(d)/'plan.json';write(plan,dict(workers=1,boundary_audit=True,
                checkpoint_seconds=.05,tasks=[dict(scenario=scenario())]))
            folder=prepare(plan,Path(d)/'campaigns');original=Simulation.advance
            def advance(sim,steps=1):
                result=original(sim,steps)
                if sim.step_index>=500:(folder/'STOP').write_text('stop')
                return result
            with patch.object(Simulation,'advance',advance):execute(folder,'task0000')
            state=read(folder/'tasks/task0000/state.json');self.assertEqual(state['status'],'paused')
            (folder/'STOP').unlink();execute(folder,'task0000');state=read(folder/'tasks/task0000/state.json')
            ref=Simulation(scenario());obs=make_observer(ref.config,False);ref.listeners.append(obs)
            probe=KineticProbe(ref.config);probe.attach(ref.chemistry)
            audit=BoundaryAudit(ref.config,obs);ref.listeners.append(audit);ref.advance(ref.target_step)
            self.assertEqual(read(folder/state['boundary_audit']),json.loads(json.dumps(audit.summary())))
            self.assertEqual(read(folder/state['result'])['metrics'],json.loads(json.dumps(obs.summary())))
            self.assertEqual(analyze(folder)['rows'][0]['boundary_audit']['samples'],len(obs.times))
            self.assertIn('Diagnostic des ouvertures',(folder/'analysis.md').read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
