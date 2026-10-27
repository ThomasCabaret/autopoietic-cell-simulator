import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.contact_exchange import exchange_faces
from simulator.membrane_bath import DEFAULTS
from simulator.spatial import Neighborhood
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.kinetics import KineticProbe
from simulator import checkpoint
from tests.test_membrane_bath import small


class TerminalExchangeTests(unittest.TestCase):
    def fixture(self,side=1.):
        h=np.array([[0.,0.],[1.,0.],[.7,side*.35],[2.,0.],[1.7,side*.35]])
        return np.concatenate((h,h+[0.,-.65]))

    def test_chain_splice_blocked_but_terminal_replacement_and_reverse_allowed(self):
        cfg=dict(DEFAULTS,contact_exchange_rate=1e9,terminal_exchange=True)
        for side in (-1.,1.):
            pos=self.fixture(side);before=pos.copy()
            blocked=[(0,1,1,0),(1,3,1,0),(2,4,1,0)]
            result,events=exchange_faces(pos,blocked,cfg,np.random.default_rng(0),Neighborhood(),.01)
            self.assertIn((0,1,1,0),result)
            self.assertNotIn((0,2,1,0),result)
            self.assertEqual(len(result),len(blocked))
            # A free other face on either partner permits exchange. It remains
            # permitted in reverse; no forced insertion, atom movement or seal.
            linked=[(0,1,1,0),(2,4,1,0)]
            result,events=exchange_faces(pos,linked,cfg,np.random.default_rng(0),Neighborhood(),.01)
            self.assertIn((0,2,1,0),result);self.assertEqual(len(result),len(linked))
            result,events=exchange_faces(pos,result,cfg,np.random.default_rng(0),Neighborhood(),.01)
            self.assertIn((0,1,1,0),result);self.assertEqual(len(result),len(linked))
            np.testing.assert_array_equal(pos,before)

    def test_disabled_option_is_exact_old_exchange_including_rng(self):
        root=Path(__file__).resolve().parents[1]
        folder=root/'research/campaign_recipes/M1R_20261026T165544113247Z'
        path=folder/'runtime/simulator/contact_exchange.py';manifest=json.loads((folder/'manifest.json').read_text())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),manifest['source_sha256']['simulator/contact_exchange.py'])
        spec=importlib.util.spec_from_file_location('simulator._exchange_reference',path)
        legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
        for seed in range(5):
            a=np.random.default_rng(seed);b=np.random.default_rng(seed)
            links=[(0,1,1,0),(1,3,1,0),(2,4,1,0)]
            cfg=dict(DEFAULTS,contact_exchange_rate=10.)
            x=exchange_faces(self.fixture(),links,cfg,a,Neighborhood(),.01)
            y=legacy.exchange_faces(self.fixture(),links,cfg,b,Neighborhood(),.01)
            self.assertEqual(x,y);self.assertEqual(a.bit_generator.state,b.bit_generator.state)

    def test_gated_exposure_excludes_blocked_geometry_without_feedback(self):
        raw=small();raw['chemistry']['terminal_exchange']=True
        fixture=Simulation(raw);c=fixture.chemistry;n=c.n
        c.pos[40]=c.pos[0]+.7*(c.pos[1]-c.pos[0])+[-.30,0.]
        c.pos[n+40]=c.pos[40]+c.pos[n]-c.pos[0]
        c.pos[41]=c.pos[40]+[0.,1.];c.pos[n+41]=c.pos[41]+c.pos[n]-c.pos[0]
        c.face_links.append((40,41,0,1))
        counts=KineticProbe(fixture.config).scan(c)
        self.assertGreater(counts['exchange_faces'],0)
        self.assertLess(counts['gated_exchange_faces'],counts['exchange_faces'])
        a=Simulation(raw);b=Simulation(raw);probe=KineticProbe(a.config);probe.attach(a.chemistry)
        oa=make_observer(a.config);ob=make_observer(b.config);a.listeners.append(oa);b.listeners.append(ob)
        a.advance(a.target_step);b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        self.assertEqual(oa.summary(),ob.summary())
        total=probe.summary(a.time,oa.summary())['opportunity_totals']
        self.assertLessEqual(total['gated_exchange_face_time'],total['exchange_face_time'])
        self.assertIn('gated_exchange_faces',probe.summary(a.time,oa.summary())['first_passages'])

    def test_active_guard_checkpoint_is_exact(self):
        raw=small();raw['chemistry'].update(terminal_exchange=True,contact_exchange_rate=1e6)
        a=Simulation(raw);c=a.chemistry;n=c.n
        c.pos[40]=c.pos[0]+.7*(c.pos[1]-c.pos[0])+[-.30,0.]
        c.pos[n+40]=c.pos[40]+c.pos[n]-c.pos[0]
        obs=make_observer(a.config);a.listeners.append(obs);a.advance(500)
        self.assertTrue(c.exchange_events)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state.npz';checkpoint.save(p,a,obs);b,other=checkpoint.load(p,make_observer)
            a.advance(a.target_step);b.advance(b.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
            self.assertEqual(a.chemistry.export(),b.chemistry.export());self.assertEqual(obs.summary(),other.summary())


if __name__=='__main__':unittest.main()
