import copy,unittest
import numpy as np
from simulator.engine import Simulation
from experiments.inventory_audit import census
from experiments.prepare_batch14_bootstrap import scenario


class InventoryAuditTests(unittest.TestCase):
    def test_partition_and_material_conservation_for_both_domains(self):
        for case in ('cold_prepared','bath_prepared'):
            sim=Simulation(scenario(case,0,.02));c=sim.chemistry;before=copy.deepcopy(c.export());rng=copy.deepcopy(sim.rng.bit_generator.state)
            inv=census(sim.config,c.export(),c.pos)
            self.assertEqual(inv['pools']['beads_accounted'],102)
            self.assertEqual(inv['pools']['active_dimers'],9)
            self.assertEqual(inv['target_like_components'],dict(G=1,F=1))
            self.assertEqual(sum(inv['partition_active_units'].values()),9)
            self.assertEqual(c.export(),before);self.assertEqual(sim.rng.bit_generator.state,rng)

    def test_partial_F_can_be_refractory_without_being_called_inert(self):
        sim=Simulation(scenario('cold_unlinked',0,.02));c=sim.chemistry
        c.edges.add((27,28));inv=census(sim.config,c.export(),c.pos)
        self.assertEqual(inv['unpaired_non_target_F_units'],2)
        self.assertEqual(inv['target_like_components']['F'],0)
        c.pairing[27]=0;c.pairing[0]=27
        self.assertEqual(census(sim.config,c.export(),c.pos)['unpaired_non_target_F_units'],0)

    def test_bound_R_is_not_counted_twice_and_symbol_uses_real_partner(self):
        sim=Simulation(scenario('cold_unlinked',0,.02));c=sim.chemistry
        c.rungs[3,1]=c.n+4;c.bits[3]=c.assembly.atom_bits[4]
        inv=census(sim.config,c.export(),c.pos)
        self.assertEqual(inv['pools']['active_dimers'],10)
        self.assertEqual(inv['pools']['beads_accounted'],102)
        c.rungs[4,1]=c.n+4;c.bits[4]=c.bits[3]
        with self.assertRaises(AssertionError):census(sim.config,c.export(),c.pos)

    def test_initial_tool_is_not_a_renewed_tool(self):
        sim=Simulation(scenario('cold_prepared',0,.02));c=sim.chemistry
        inv=census(sim.config,c.export(),c.pos)
        self.assertEqual(inv['target_like_components']['F'],1)
        self.assertEqual(c.assembly.events,[])
        self.assertIn('structural',inv['scope'])

    def test_membrane_comparison_does_not_overweight_gene_event_samples(self):
        from experiments.analyze_constructed_tool import membrane_grid_metrics
        regular=[dict(time=t,parent_closed=True,envelope_valid=True) for t in (0.,.5,1.)]
        extra=[dict(time=t,parent_closed=False,envelope_valid=False) for t in (.1,.2,.3,.4)]
        a=membrane_grid_metrics(regular,.5,1.)
        self.assertEqual(a,membrane_grid_metrics(sorted(regular+extra,key=lambda h:h['time']),.5,1.))
        self.assertEqual(a['regular_grid_closed_fraction'],1.)

    def test_scaled_census_uses_nearest_of_all_initial_templates(self):
        from experiments.prepare_density_campaign import scenario as scaled
        sim=Simulation(scaled(8,False,0,duration=.02));c=sim.chemistry;g=c.genetics
        positions=c.pos.copy();positions[g.rungs[3:6,1]]=[5.,5.]
        monomers=[q for group in g.initial_groups if group['family']==1 and not group['backbone'] for q in group['units']]
        positions[g.rungs[monomers,1]]=[5.1,5.1]
        inv=census(sim.config,c.export(),positions)
        self.assertEqual(inv['initial_template_count'],8)
        self.assertEqual(inv['pools']['beads_accounted'],816)
        self.assertLess(inv['available_monomer_nearest_template']['F']['median_distance'],1.)
        self.assertGreater(inv['free_monomer_access']['F']['median_distance'],10.)
