import copy,math,unittest
from experiments.audit_cell_design import load,network,audit,assess,sizing


class CellDesignTests(unittest.TestCase):
    def test_baseline_requires_regeneration_and_all_ten_failures_detected(self):
        result=assess(load())
        self.assertTrue(result['audit']['conditionally_regenerable'])
        self.assertEqual(result['target_species_count'],16)
        self.assertEqual(len(result['negative_controls']),10)
        self.assertTrue(all(not x['conditionally_regenerable'] for x in result['negative_controls'].values()))
        self.assertIn('EA',result['negative_controls']['missing_expression_EA']['not_regenerated'])
        self.assertIn('L_surface',result['negative_controls']['missing_insertion']['not_regenerated'])

    def test_equal_mass_wrong_monomer_family_is_not_accepted(self):
        spec=load();model=network(spec)
        reaction=next(r for r in model['reactions'] if r['id']=='express_EN')
        reaction['inputs']['N0']=reaction['inputs'].pop('A0')
        result=audit(spec,model)
        self.assertIn('wrong_monomer_family:express_EN',result['errors'])
        self.assertFalse(any(e.startswith('mass:') for e in result['errors']))

    def test_inventories_and_surface_are_counted_separately(self):
        result=assess(load());b=result['budgets'][1]
        self.assertEqual(b['gene_chains'],6);self.assertEqual(b['tool_chains'],12)
        self.assertEqual(b['interior_beads'],1712)
        self.assertEqual(b['total_beads'],b['interior_beads']+2*b['membrane_molecules']+b['outside_beads'])
        self.assertEqual(b['free_compound_molecules'],312)
        self.assertGreater(b['needed_inner_pitch'],.98)
        self.assertFalse(b['current_curvature_fits'])

    def test_existing_curvature_matches_polygon_and_is_too_small(self):
        spec=load();b=sizing(spec,spec['sizing']['cases'][1]);n=b['current_preferred_units']
        angle=math.pi/n;h=spec['sizing']['lipid_thickness']
        self.assertAlmostEqual(2*h*math.sin(angle),1.-.65)
        self.assertTrue(11.<n<12.)
        self.assertGreater(b['membrane_radius'],20*b['current_preferred_radius'])

    def test_adding_insertase_adds_both_gene_and_protein_cost(self):
        spec=load();case=spec['sizing']['cases'][1]
        a=sizing(spec,case);b=sizing(spec,case,1)
        self.assertEqual(b['gene_chains']-a['gene_chains'],2)
        self.assertEqual(b['tool_chains']-a['tool_chains'],4)
        self.assertEqual(b['interior_beads']-a['interior_beads'],2*24*(2+4))
        self.assertGreater(b['membrane_molecules'],a['membrane_molecules'])

    def test_budget_replacement_conserves_atoms_and_energy_carrier(self):
        spec=load();result=assess(spec);flux=result['replacement'];m=network(spec)['masses']
        left=[sum(n*m[s][k] for s,n in flux['food'].items()) for k in range(4)]
        right=[sum(n*m[s][k] for s,n in flux['new_material'].items())+flux['waste']*m['W'][k] for k in range(4)]
        self.assertEqual(left,right)
        self.assertEqual(flux['food']['E'],flux['waste'])


if __name__=='__main__':unittest.main()
