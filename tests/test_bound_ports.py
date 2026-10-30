import copy,unittest
import numpy as np
from simulator.docking import bound_port_force,docking_force,port_geometry
from simulator.engine import Simulation
from simulator.config import resolve


class BoundPortTests(unittest.TestCase):
    def test_coupled_checkpoint_restores_new_bound_potential_exactly(self):
        from pathlib import Path
        import tempfile
        from simulator import checkpoint
        from simulator.runner import make_observer
        from experiments.prepare_coherent_contacts import plan
        cfg=next(t['scenario'] for t in plan()['tasks'] if t['scenario']['name']=='MD2_bath_new_s0')
        cfg['duration']=.25;sim=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs)
        sim.advance(25)
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]/'outputs/test_tmp') as d:
            path=Path(d)/'s.npz';checkpoint.save(path,sim,obs);other,other_obs=checkpoint.load(path,make_observer)
        sim.advance(sim.target_step);other.advance(other.target_step)
        np.testing.assert_array_equal(sim.chemistry.pos,other.chemistry.pos)
        np.testing.assert_array_equal(sim.motion.velocities,other.motion.velocities)
        self.assertEqual(sim.rng.bit_generator.state,other.rng.bit_generator.state)
        self.assertEqual(obs.summary(),other_obs.summary())

    def test_exact_gradient_momentum_and_torque(self):
        pos=np.array([[0.,0.],[1.,-.12],[.07,-.65],[.84,-.75]])
        links=np.array([[0,1,1,0]],dtype=np.int64)
        f,_=bound_port_force(pos,links,1.,.75,4.,.3);numeric=np.zeros_like(pos);h=1e-6
        for i in range(4):
            for axis in range(2):
                plus,minus=pos.copy(),pos.copy();plus[i,axis]+=h;minus[i,axis]-=h
                numeric[i,axis]=-(bound_port_force(plus,links,1.,.75,4.,.3)[1]-bound_port_force(minus,links,1.,.75,4.,.3)[1])/(2*h)
        np.testing.assert_allclose(f,numeric,atol=1e-7)
        np.testing.assert_allclose(f.sum(axis=0),0,atol=1e-12)
        self.assertAlmostEqual(float(np.sum(pos[:,0]*f[:,1]-pos[:,1]*f[:,0])),0.,places=11)

    def test_free_and_bound_potentials_match_near_ideal_contact(self):
        theta=np.arctan((1.-.98)/1.3);v=np.array([[np.sin(theta),-np.cos(theta)],[-np.sin(theta),-np.cos(theta)]])
        head=np.array([[0.,0.],[np.cos(theta),0.]]);pos=np.concatenate((head,head+.65*v))
        links=np.array([[0,1,1,0]],dtype=np.int64);pairs=links[:,:2];free=np.zeros((2,2),dtype=np.bool_);free[0,1]=free[1,0]=True
        fb,eb=bound_port_force(pos,links,1.,.98,4.,.3)
        ff,ef=docking_force(pos,pairs,free,1.,.98,4.,.3)
        self.assertAlmostEqual(eb,ef,places=12);np.testing.assert_allclose(fb,ff,atol=1e-12)
        pos[1,0]+=1e-4
        fb,eb=bound_port_force(pos,links,1.,.98,4.,.3);ff,ef=docking_force(pos,pairs,free,1.,.98,4.,.3)
        self.assertLess(abs(eb-ef),1e-10);np.testing.assert_allclose(fb,ff,atol=1e-8)

    def test_opt_in_replaces_old_terms_and_absence_preserves_configuration(self):
        cfg=dict(schema_version=1,model='membrane',duration=.1,chemistry=dict(units=2,initial='straight',face_docking=True))
        old=resolve(cfg);self.assertNotIn('bound_port_geometry',old['chemistry'])
        new=copy.deepcopy(cfg);new['chemistry']['bound_port_geometry']=True
        sim=Simulation(new);sim.advance(0)
        self.assertEqual(len(sim.chemistry.springs),2);self.assertEqual(len(sim.chemistry.angles),0)
        sim.chemistry.config['bound_port_geometry']=False;sim.chemistry._face_mechanics()
        self.assertEqual(len(sim.chemistry.springs),4);self.assertEqual(len(sim.chemistry.angles),4)
        new['chemistry']['face_docking']=False
        with self.assertRaises(ValueError):resolve(new)


if __name__=='__main__':unittest.main()
