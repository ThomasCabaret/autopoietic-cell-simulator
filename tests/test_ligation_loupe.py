import copy,json,tempfile,unittest
from pathlib import Path
import numpy as np
from experiments.prepare_minimal_tool_campaign import expression
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.genetic_audit import GeneticAudit
from simulator.ligation_loupe import LigationLoupe,settings
from simulator import checkpoint
from scripts.campaign import prepare
from simulator.campaign_io import write


def constructed(duration=.4):
    sim=Simulation(expression(0,'short',duration));c=sim.chemistry
    a,b=39,41
    c.pos[[0,1,a,b]]=[[2.,2.],[3.,2.],[2.,2.9],[3.,2.9]]
    c.pos[c.rungs[[0,1,a,b],1]]=c.pos[[0,1,a,b]]+[[0,.45],[0,.45],[0,-.45],[0,-.45]]
    c.pairing[:]=-1;c.pairing[[0,1,a,b]]=[a,b,0,1]
    return sim


class LigationLoupeTests(unittest.TestCase):
    def test_exact_local_geometry_and_truncation_budget(self):
        c=constructed().chemistry;probe=LigationLoupe(dict(max_particles=8,max_records=4))
        g=probe.geometry(c,[0,1,39,41]);self.assertTrue(g['eligible']);self.assertAlmostEqual(g['distance'],1.)
        for i in range(100):probe.before(c,.02*i);probe.after(c,.02*i,[])
        state=probe.state;self.assertEqual(state['records'],4)
        self.assertEqual(len(state['captures']),1)
        self.assertEqual(state['captures'][0]['end_reason'],'record_budget')
        self.assertTrue(all(len(f['ids'])<=8 for f in state['captures'][0]['frames']))
        self.assertTrue(all(len(f['ids'])==len(f['positions']) for f in state['captures'][0]['frames']))
        self.assertLess(len(json.dumps(state)),15000)
        c.pos[41]=[5,2.9];self.assertEqual(probe.geometry(c,[0,1,39,41])['reason'],'distance')
        c.pairing[0]=-1;self.assertEqual(probe.geometry(c,[0,1,39,41])['reason'],'partners_changed')

    def test_passivity_checkpoint_and_events(self):
        a=constructed();oa=make_observer(a.config,False);a.listeners.append(oa)
        ga=GeneticAudit(loupe={});ga.attach(a.chemistry);a.advance(37)
        with tempfile.TemporaryDirectory() as tmp:
            oa.campaign_genetic_state=ga.state;path=Path(tmp)/'state.npz';checkpoint.save(path,a,oa)
            b,ob=checkpoint.load(path,make_observer);gb=GeneticAudit(ob.campaign_genetic_state,loupe={});gb.attach(b.chemistry)
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
            self.assertEqual(oa.summary(),ob.summary());self.assertEqual(ga.summary(a.time),gb.summary(b.time))
        plain=constructed();op=make_observer(plain.config,False);plain.listeners.append(op);plain.advance(plain.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,plain.chemistry.pos)
        np.testing.assert_array_equal(a.motion.velocities,plain.motion.velocities)
        self.assertEqual(a.chemistry.export(),plain.chemistry.export());self.assertEqual(a.rng.bit_generator.state,plain.rng.bit_generator.state)
        self.assertEqual(oa.summary(),op.summary());self.assertGreater(ga.loupe.state['records'],0)

    def test_no_motif_is_censored_and_legacy_summary_unchanged(self):
        sim=Simulation(expression(0,'nogene',.02));ga=GeneticAudit(loupe={});ga.attach(sim.chemistry);sim.advance(sim.target_step)
        self.assertEqual(ga.loupe.summary(sim.time)['captures'],[])
        self.assertNotIn('ligation_loupe',GeneticAudit().summary(0.))

    def test_settings_and_campaign_require_passive_genetic_audit(self):
        for cfg in (True,dict(max_particles=7),dict(max_captures=9),dict(max_records=100000),dict(radius=float('nan'))):
            with self.assertRaises(ValueError):settings(cfg)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'plan.json';write(path,dict(tasks=[dict(scenario=expression(0,'short',1.))],ligation_loupe={}))
            with self.assertRaises(ValueError):prepare(path,Path(tmp)/'jobs')


if __name__=='__main__':unittest.main()
