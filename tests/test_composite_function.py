import copy
from pathlib import Path
import tempfile
import unittest
import numpy as np
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator.spatial import Neighborhood
from simulator.observations import CopyObserver
from simulator import checkpoint


def config():
    return dict(schema_version=1,model='copy',seed=4,duration=5.,engine=dict(dt=.005),
        chemistry=dict(sequence='001',seed_family=1,free_units=0,food_pairs=2,
            functional_bend_cosines={'0':.6,'1':-.5}))


class CompositeFunctionTests(unittest.TestCase):
    def test_food_ligation_release_and_site_exclusion(self):
        c=Simulation(config()).chemistry; n=c.n
        c.config.update(food_reaction_rate=10000.,food_unbinding_rate=0.)
        c.pos[2*n:2*n+2]=[[2.,2.],[2.1,2.]]
        c.food.site_bound[0]=0;c.food.site_bound[2]=1
        c.food.food_bound[:2]=[0,2]
        events=c.react(0.,.005,Neighborhood())
        self.assertEqual(c.food.products,{(0,1)})
        self.assertEqual(events[0]['support'],(0,2))
        np.testing.assert_array_equal(c.food.site_bound,-1)
        self.assertEqual(len(c.pos),2*n+4)
        # A recognition site occupied by food cannot also recruit a G unit.
        c=Simulation(dict(schema_version=1,model='copy',duration=1.,chemistry=dict(
            sequence='00',free_units=0,function_units=1,food_pairs=1))).chemistry
        c.pos[c.n+2]=c.pos[c.n]; c.pos[2]=c.pos[c.n+2]+[0,.45]
        c.food.site_bound[2]=0;c.food.food_bound[0]=2
        c.config['food_unbinding_rate']=0.
        for _ in range(100): c.react(0.,.005,Neighborhood())
        self.assertEqual(c.pairing[2],-1)

    def test_food_force_gradient(self):
        c=Simulation(config()).chemistry
        c.pos[:3]=[[1,1],[4,4],[6,1]]
        c.pos[3:6]=[[1.1,1.4],[4.1,4.4],[6.1,1.4]]
        c.pos[6:]=[[1.2,1.5],[4.2,4.5],[6.2,1.5],[7.5,4.5]]
        def energy(p):
            total=0.
            for i in range(c.n):
                for f in range(c.food.count):
                    if c.bits[i]!=f%2: continue
                    d=p[2*c.n+f]-p[c.n+i];r2=d@d;w=c.config['food_ligand_width']
                    if r2<(3*w)**2: total-=c.config['food_ligand_energy']*np.exp(-r2/(2*w*w))
            return total
        numeric=np.zeros_like(c.pos); h=1e-6
        for i in range(len(c.pos)):
            for axis in range(2):
                plus=c.pos.copy();minus=c.pos.copy();plus[i,axis]+=h;minus[i,axis]-=h
                numeric[i,axis]=-(energy(plus)-energy(minus))/(2*h)
        np.testing.assert_allclose(c.food.forces(c,Neighborhood()),numeric,atol=1e-8)

    def test_tree_brute_checkpoint_and_observer(self):
        first=config();first['chemistry'].update(food_activation=True,function_units=2)
        a=Simulation(first);oa=make_observer(a.config);a.listeners.append(oa)
        raw=copy.deepcopy(first);raw['engine']['spatial']='brute'
        b=Simulation(raw);ob=make_observer(b.config);b.listeners.append(ob)
        a.advance(333)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state.npz';checkpoint.save(p,a,oa)
            resumed,oc=checkpoint.load(p,make_observer)
            a.advance(a.target_step);resumed.advance(resumed.target_step)
            np.testing.assert_array_equal(a.chemistry.pos,resumed.chemistry.pos)
            self.assertEqual(a.chemistry.export(),resumed.chemistry.export())
            self.assertEqual(oa.summary(),oc.summary())
        b.advance(b.target_step)
        np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
        self.assertEqual(oa.summary(),ob.summary())

    def test_observer_requires_full_translation_provenance(self):
        cfg=dict(sequence='001',template=True,seed_family=0)
        obs=CopyObserver(cfg); bits=np.array([0,0,1,0,0,1]);families=np.array([0,0,0,1,1,1])
        pairing=np.full(6,-1); pos=np.zeros((16,2));edges={(0,1),(1,2),(3,4),(4,5)}
        food=dict(products=[(0,1)],site_bound=[-1]*6,food_bound=[-1]*4)
        ev=dict(kind='food',formed=(0,1),support=(3,5))
        obs(0.,pos,edges,pairing,bits,[ev],families,food)
        self.assertEqual(obs.summary()['food_expressed_tool_ligations'],0)
        # Exact shape alone does not certify expression. Each new edge needs G support.
        obs=CopyObserver(cfg)
        obs(0.,pos,{(0,1),(1,2)},pairing,bits,[],families,food)
        obs(.1,pos,edges,pairing,bits,[dict(source=(0,1),formed=(3,4)),dict(source=(1,2),formed=(4,5))],families,food)
        obs(.2,pos,edges,pairing,bits,[ev],families,food)
        self.assertEqual(obs.summary()['food_expressed_tool_ligations'],1)
        self.assertEqual(obs.summary()['food_max_turnovers_per_expressed_tool'],1)


if __name__=='__main__':unittest.main()
