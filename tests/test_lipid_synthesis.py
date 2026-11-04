import copy,tempfile,unittest
from pathlib import Path
import numpy as np
from simulator.config import resolve
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.spatial import Neighborhood
from simulator.linked_lipids import LinkedLipids
from simulator.lipid_synthesis import DEFAULTS
from simulator.docking import docking_force,bound_port_force,free_faces,update_faces
from simulator.contact_exchange import exchange_faces
from simulator import checkpoint


def config(**changes):
    return resolve(dict(schema_version=1,model='lipid_synthesis',seed=4,duration=.12,
        engine=dict(dt=.002,sample_every=10),mechanics=dict(motion='langevin'),
        chemistry=dict(food_units=3,tool_count=1,**changes)))


class LipidTests(unittest.TestCase):
    def test_indexed_forces_equal_md2_gradients_and_arbitrary_labels(self):
        cfg=dict(DEFAULTS);pos=np.array([[0.,0.],[.98,.08],[.04,-.65],[1.02,-.61]])
        pairs=np.array([[0,1]],dtype=np.int64)
        for links in ([],[(0,1,0,1)]):
            pool=LinkedLipids();pool.bind(0,2);pool.bind(1,3);pool.links=list(links)
            f,e=pool.forces(pos,cfg,Neighborhood('brute',0.))
            partners=np.full((2,2),-1,dtype=np.int64)
            for i,j,a,b in links:partners[i,a]=j;partners[j,b]=i
            a,x=docking_force(pos,pairs,free_faces(2,links),1.,cfg['short_length'],4.,.3,partners)
            b,y=bound_port_force(pos,np.array(links,dtype=np.int64).reshape(-1,4),1.,cfg['short_length'],4.,.3)
            np.testing.assert_array_equal(f,a+b);self.assertEqual(e,x+y)
            np.testing.assert_allclose(f.sum(axis=0),0.,atol=1e-12)
            for i in range(4):
                for j in range(2):
                    p=pos.copy();p[i,j]+=1e-6;q=pos.copy();q[i,j]-=1e-6
                    derivative=(pool.forces(p,cfg,Neighborhood('brute',0.))[1]-pool.forces(q,cfg,Neighborhood('brute',0.))[1])/2e-6
                    self.assertAlmostEqual(f[i,j],-derivative,places=5)
            ids=np.array([5,1,0,6]);world=np.full((8,2),10.);world[ids]=pos
            other=LinkedLipids();other.bind(ids[0],ids[2]);other.bind(ids[1],ids[3])
            other.links=[(ids[j],ids[i],b,a) if ids[j]<ids[i] else (ids[i],ids[j],a,b) for i,j,a,b in links]
            g,v=other.forces(world,cfg,Neighborhood('brute',0.))
            np.testing.assert_allclose(g[ids],f,atol=1e-12);self.assertAlmostEqual(v,e)
            np.testing.assert_array_equal(g[[2,3,4,7]],0.)

    def test_face_reactions_and_restore_use_real_head_ids(self):
        pool=LinkedLipids();pool.bind(3,0);pool.bind(5,2);pool.bind(7,6)
        p=np.zeros((8,2));p[[3,5,7]]=[[0.,0.],[1.,0.],[2.,0.]];p[[0,2,6]]=p[[3,5,7]]-[0.,.65]
        pool.links=[(3,5,1,0)];cfg=dict(DEFAULTS);heads,ids,links=pool.layout()
        r=np.random.default_rng(6);t=np.random.default_rng(6)
        a,broken=update_faces(p[ids],links,cfg,r,Neighborhood('brute'),.01)
        a,events=exchange_faces(p[ids],a,cfg,r,Neighborhood('brute'),.01)
        pool.react(p,cfg,t,Neighborhood('brute'),.01)
        self.assertEqual(pool.links,[(heads[i],heads[j],a,b) for i,j,a,b in a])
        self.assertEqual(r.bit_generator.state,t.bit_generator.state)
        restored=LinkedLipids();restored.restore(pool.export());self.assertEqual(restored.export(),pool.export())
        with self.assertRaises(ValueError):pool.bind(1,0)

    def test_real_arbitrary_partners_release_sites_and_allow_reuse(self):
        sim=Simulation(config());c=sim.chemistry;before=c.pos.copy();n=c.prefix
        # Deliberately cross-indexed, prepared local contacts. Large test rate,
        # not a candidate kinetic observation. No pose change on formation.
        for h,t in ((n+2,n+3),(n,n+5)):
            c.pos[n:]=[10.,8.];c.pos[h]=[3.,3.];c.pos[t]=[3.4,3.]
            c.capture.refresh(c);c.capture.site_bound[:]=[h,t];c.capture.atom_bound[h]=0;c.capture.atom_bound[t]=1
            old=c.pos.copy();c.config['rung_catalytic_rate']=1e9
            c.form_lipids(1.,.01,Neighborhood('brute',0.));c._mechanics()
            self.assertEqual(c.lipids.rungs[h],t);self.assertEqual(c.capture.site_bound.tolist(),[-1,-1])
            self.assertTrue(np.all(c.capture.atom_bound[[h,t]]==-1));np.testing.assert_array_equal(c.pos,old)
        self.assertEqual(len(c.births),2);self.assertTrue(all(e['catalyzed'] for e in c.births))
        self.assertEqual(len(c.pos),len(before));self.assertEqual(len(set(c.lipids.rungs.values())),2)

    def test_disconnected_sites_cannot_supply_catalytic_bonus(self):
        for linked in (True,False):
            c=Simulation(config(tool_linked=linked,rung_formation_rate=0.,rung_catalytic_rate=1e9)).chemistry;n=c.prefix
            c.pos[n:]=[10.,8.];h,t=n,n+3;c.pos[h]=[3.,3.];c.pos[t]=[3.4,3.]
            c.capture.refresh(c);c.capture.site_bound[:]=[h,t];c.capture.atom_bound[h]=0;c.capture.atom_bound[t]=1
            c.form_lipids(0.,.01,Neighborhood('brute',0.));self.assertEqual(len(c.births),int(linked))

    def test_shared_engine_tree_brute_passivity_and_exact_restart(self):
        cfg=config();a=Simulation(cfg);b=Simulation(cfg);other=copy.deepcopy(cfg);other['engine']['spatial']='brute';d=Simulation(other)
        obs=make_observer(a.config,False);a.listeners.append(obs);a.advance(20);b.advance(20);d.advance(20)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos);np.testing.assert_array_equal(a.chemistry.pos,d.chemistry.pos)
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'checkpoint.npz';checkpoint.save(p,a,obs);c,newobs=checkpoint.load(p,make_observer)
            a.advance(40);c.advance(40)
            np.testing.assert_array_equal(a.chemistry.pos,c.chemistry.pos)
            np.testing.assert_array_equal(a.motion.velocities,c.motion.velocities)
            self.assertEqual(a.chemistry.export(),c.chemistry.export());self.assertEqual(obs.summary(),newobs.summary())

    def test_empty_tool_pool_and_invalid_configuration(self):
        cfg=config();cfg['chemistry']['tool_count']=0;sim=Simulation(cfg);sim.advance(10)
        self.assertEqual(sim.chemistry.n,0)
        for k,v in (('tool_count',-1),('food_units',True),('food_binding_radius',0.)):
            bad=config();bad['chemistry'][k]=v
            with self.assertRaises(ValueError):resolve(bad)


if __name__=='__main__':unittest.main()
