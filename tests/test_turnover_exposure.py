import tempfile,unittest
from pathlib import Path
import numpy as np
from experiments.inspect_turnover_exposure import Exposure
from experiments.prepare_recycling_campaign import small
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator import checkpoint


def attach(sim,audit):
    original=sim.chemistry.turnover.react
    def observed(c,t,dt):
        before=audit.before(c);original(c,t,dt);audit.after(c,t,dt,before)
    sim.chemistry.turnover.react=observed


class TurnoverExposureTests(unittest.TestCase):
    def test_intra_call_backbone_breaks_are_counted_before_rung_eligibility(self):
        cfg=small(0,'full',.02)
        cfg['chemistry']['bond_turnover'].update(backbone_g=1e9,backbone_f=1e9,rung_g=1e9,rung_f=1e9)
        sim=Simulation(cfg);audit=Exposure(range(12));c=sim.chemistry
        before=audit.before(c);self.assertTrue(np.any(before['degree']>0))
        c.turnover.react(c,0.,.002);audit.after(c,0.,.002,before)
        totals=audit.summary()['totals'];self.assertGreater(sum(totals['rung_intensity'].values()),0.)
        self.assertFalse(any(k.endswith(':linked') for k in totals['rung_gate_time']))
        self.assertGreater(totals['events']['backbone_break'],0.)
        self.assertGreater(sum(v for k,v in totals['events'].items() if k.startswith('rung_break')),0.)

    def test_probe_is_passive_and_checkpoint_restarts_with_the_same_exposure(self):
        cfg=small(0,'protected',.1);a,b=Simulation(cfg),Simulation(cfg)
        obs=make_observer(a.config,False);obs.record_trajectory=False;a.listeners.append(obs)
        audit=Exposure(q for q in obs.polymer_atoms if q<a.chemistry.n);attach(a,audit)
        a.advance(25);b.advance(25)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.chemistry.export(),b.chemistry.export());self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'probe.npz';checkpoint.save(p,a,obs)
            # JSON checkpoint sidecar is a deep snapshot, never shared counters.
            import json
            resumed=Exposure.restore(json.loads(json.dumps(audit.export())))
            new,new_obs=checkpoint.load(p,make_observer);attach(new,resumed)
            a.advance(25);new.advance(25)
            np.testing.assert_array_equal(a.chemistry.pos,new.chemistry.pos)
            self.assertEqual(a.rng.bit_generator.state,new.rng.bit_generator.state)
            self.assertEqual(audit.summary(),resumed.summary());self.assertEqual(obs.summary(),new_obs.summary())
