import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch,MagicMock
import numpy as np
from simulator.engine import Simulation
from simulator.genetic_audit import GeneticAudit
from simulator.spatial import Neighborhood
from simulator.campaign_io import read,write
from simulator import checkpoint
from simulator.runner import make_observer
from tests.test_genetic_audit import geometry
from experiments.diagnose_fragment_capture import CertainDraw
from experiments.prepare_expression_campaign import small,transfer,baseline,plans
from scripts.expression_followup import decide,step,digest


class EndpointTests(unittest.TestCase):
    def test_only_ends_rebind_and_audit_matches_actual_rule(self):
        for enabled in (False,True):
            for edges,expected in ((set(),[3,4,5]),({(4,5)},[3,4,5] if enabled else [3]),
                                   ({(3,4),(4,5)},[3,5] if enabled else [])):
                c=geometry();c.config.update(gf_end_capture=enabled,monomer_only_capture=True,
                    release='never',product_cooperativity=True,ligation=False)
                c.cycle='never';c.edges.update(edges);c.rng=CertainDraw()
                audit=GeneticAudit().scan(c,0.)
                self.assertEqual(audit['recognition_eligible_GF'],len(expected))
                c.react(0.,.002,Neighborhood())
                self.assertEqual([i for i in range(3,6) if c.pairing[i]>=0],expected)

    def test_saturation_orientation_and_symbol_still_block_end_contact(self):
        for condition in ('occupied','orientation','symbol','precursor'):
            cfg=small(0,'end','tool');c=Simulation(cfg).chemistry
            # Start from controlled six-unit geometry, constructible site occupancy included.
            a=geometry();c.pos[:3]=a.pos[:3];c.pos[27:30]=a.pos[3:6]
            c.pos[c.rungs[:3,1]]=a.pos[6:9];c.pos[c.rungs[27:30,1]]=a.pos[9:12]
            c.rng=CertainDraw();target=27
            if condition=='occupied':c.pairing[0]=target;c.pairing[target]=0
            if condition=='orientation':c.pos[target]=c.pos[0];c.pos[c.rungs[target,1]]=c.pos[0]+[0.,.45]
            if condition=='symbol':c.bits[target]=1
            if condition=='precursor':c.assembly.catalyst.site_bound[target]=50
            # Inspect pre-tick eligibility rather than catalysis consuming a synthetic ligand.
            scan=GeneticAudit().scan(c,0.)
            self.assertGreater(scan.get('recognition_blocked_'+condition,0),0)

    def test_baseline_and_candidate_preserve_initial_state_and_rng(self):
        for prep in ('expression','tool'):
            a,b=Simulation(small(0,'old',prep)),Simulation(small(0,'end',prep))
            self.assertEqual(len(a.chemistry.pos),102)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.chemistry.export(),b.chemistry.export())
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        a,b=baseline(0),transfer(0)
        b['chemistry']['genetics'].pop('gf_end_capture')
        for key in ('name','branch'):a.pop(key);b.pop(key)
        self.assertEqual(a,b)
        x,y=plans();self.assertEqual((len(x['tasks']),len(y['tasks'])),(12,4))

    def test_audit_passivity_with_langevin_and_prepared_tool(self):
        raw=small(0,'end','tool');raw['duration']=2.
        a,b=Simulation(raw),Simulation(raw);audit=GeneticAudit();audit.attach(a.chemistry)
        a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.chemistry.export(),b.chemistry.export())
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        result=audit.summary(a.time)
        self.assertAlmostEqual(result['exposure']['prepared_F_sites'],6.)
        json.dumps(result)

    def test_candidate_checkpoint_preserves_motion_and_audit(self):
        raw=small(0,'end','tool');raw['duration']=2.
        a=Simulation(raw);obs=make_observer(a.config,False);a.listeners.append(obs)
        p=GeneticAudit();p.attach(a.chemistry);a.advance(377)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'checkpoint.npz';obs.campaign_genetic_state=p.state;checkpoint.save(path,a,obs)
            b,other=checkpoint.load(path,make_observer);q=GeneticAudit(other.campaign_genetic_state);q.attach(b.chemistry)
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.chemistry.export(),b.chemistry.export())
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
            self.assertEqual(p.summary(a.time),q.summary(b.time))


def rows():
    return [dict(label=f'T9E_{prep}_{variant}_s{seed}',seed=seed,G=1,
        F=2 if variant=='end' else 1,incorporated=10,prepared_paired_fraction=.1)
        for prep in ('expression','tool') for seed in range(3) for variant in ('old','end')]


def snapshot(phase='complete',active=False):
    return dict(counts={k:int(k==phase) for k in ('pending','running','complete','failed','paused','interrupted')},
        controller_active=active,tasks=[dict(worker_active=active)])


class ExpressionFollowupTests(unittest.TestCase):
    def test_windows_transient_rename_preserves_atomic_record(self):
        from simulator import campaign_io
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'state.json';write(target,dict(previous=True))
            original=Path.replace;calls=[]
            def transient(path,destination):
                calls.append(1)
                self.assertEqual(read(target),dict(previous=True))
                if len(calls)<3:raise PermissionError('temporary Windows sharing conflict')
                return original(path,destination)
            with patch.object(Path,'replace',transient),patch.object(campaign_io.os,'name','nt'),patch.object(campaign_io.time,'sleep') as sleep:
                write(target,dict(next=True))
                self.assertEqual(sleep.call_count,2)
            self.assertEqual(read(target),dict(next=True))

    def test_windows_permanent_rename_failure_is_bounded(self):
        from simulator import campaign_io
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'state.json';write(target,dict(previous=True))
            with patch.object(Path,'replace',side_effect=PermissionError('persistent')) as replace,\
                 patch.object(campaign_io.os,'name','nt'),patch.object(campaign_io.time,'sleep') as sleep:
                with self.assertRaises(PermissionError):write(target,dict(next=True))
                self.assertEqual(replace.call_count,7);self.assertEqual(sleep.call_count,6)
            self.assertEqual(read(target),dict(previous=True))
    def test_gate_demands_both_improvement_and_tool_preservation(self):
        r=rows();self.assertTrue(decide(r)['run_transfer'])
        for change in ('F','G','incorporated','prepared_paired_fraction'):
            r=rows()
            for x in r:
                if change in ('F','G') and 'expression_end' in x['label']:x[change]=0
                if change=='incorporated' and 'tool_end' in x['label']:x[change]=0
                if change=='prepared_paired_fraction' and 'tool_end' in x['label']:x[change]=.51
            self.assertFalse(decide(r)['run_transfer'])
        with self.assertRaises(ValueError):decide(rows()[:-1])
        r=rows();r[0]['seed']=2
        with self.assertRaises(ValueError):decide(r)

    def test_transition_uses_complete_cohort_and_launches_once(self):
        with tempfile.TemporaryDirectory() as d:
            job=Path(d);write(job/'state.json',dict(phase='ready_A',stage=0))
            cfg=dict(campaigns=[d,d])
            with patch('scripts.expression_followup.validate_job',return_value=cfg),\
                 patch('scripts.expression_followup.collect',return_value=dict(rows=rows())) as collect,\
                 patch('scripts.expression_followup.subprocess.Popen',return_value=MagicMock(pid=123)) as launch:
                with patch('scripts.expression_followup.campaign_status',return_value=snapshot('running',True)):
                    self.assertEqual(step(job),'running_0');collect.assert_not_called();launch.assert_not_called()
                with patch('scripts.expression_followup.campaign_status',return_value=snapshot()):
                    self.assertEqual(step(job),'ready_B');self.assertEqual(read(job/'state.json')['stage'],1)
                with patch('scripts.expression_followup.campaign_status',return_value=snapshot('pending')):
                    self.assertEqual(step(job),'launching');self.assertEqual(step(job),'launching')
                self.assertEqual(launch.call_count,1)
                (job/'STOP').write_text('pause');self.assertEqual(step(job),'paused')

    def test_rejection_failure_and_completed_transfer_stop(self):
        for case in ('reject','failed','interrupted','complete_B'):
            with tempfile.TemporaryDirectory() as d:
                job=Path(d);state=dict(phase='ready_A',stage=int(case=='complete_B'))
                if case=='complete_B':
                    path=job/'report_0.json';write(path,dict(rows=rows()))
                    state.update(report_0=str(path),report_0_sha256=digest(path))
                write(job/'state.json',state)
                r=rows()
                for x in r:x['F']=0
                with patch('scripts.expression_followup.validate_job',return_value=dict(campaigns=[d,d])),\
                     patch('scripts.expression_followup.collect',return_value=dict(rows=r)),\
                     patch('scripts.expression_followup.campaign_status',return_value=snapshot(case if case in ('failed','interrupted') else 'complete')),\
                     patch('scripts.expression_followup.subprocess.Popen') as launch:
                    expected='needs_attention' if case in ('failed','interrupted') else 'needs_interpretation'
                    self.assertEqual(step(job),expected);self.assertEqual(step(job),expected);launch.assert_not_called()

    def test_selected_gate_evidence_is_verified_before_launch(self):
        with tempfile.TemporaryDirectory() as d:
            job=Path(d);path=job/'report_0.json';write(path,dict(rows=rows()))
            write(job/'state.json',dict(phase='ready_B',stage=1,report_0=str(path),report_0_sha256=digest(path)))
            write(path,dict(rows=[]))
            with patch('scripts.expression_followup.validate_job',return_value=dict(campaigns=[d,d])),\
                 patch('scripts.expression_followup.subprocess.Popen') as launch:
                with self.assertRaises(ValueError):step(job)
                launch.assert_not_called()


if __name__=='__main__':unittest.main()
