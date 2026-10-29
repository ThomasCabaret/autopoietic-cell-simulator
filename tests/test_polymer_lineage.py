import unittest
from experiments.prepare_population_campaign import scenario
from experiments.audit_polymer_lineage import reconstruct


class LineageTests(unittest.TestCase):
    def test_pre_tick_graph_and_fragment_template_are_reconstructed(self):
        cfg=scenario();cfg['chemistry'].update(sequence='01',free_units=4)
        # G01 initially; first form a new01, then that now-exact descendant templates.
        events=[dict(time=1.,source=[0,1],formed=[2,3]),dict(time=2.,source=[2,3],formed=[4,5])]
        r=reconstruct(cfg,events,[[0,1],[2,3],[4,5]],[0,1,0,1,0,1])
        self.assertEqual(r['by_template_kind'],dict(initial=1,exact_descendant=1))
        cfg['chemistry'].update(sequence='010',free_units=4)
        events=[dict(time=1.,source=[0,1],formed=[3,4]),dict(time=2.,source=[3,4],formed=[5,6])]
        r=reconstruct(cfg,events,[[0,1],[1,2],[3,4],[5,6]],[0,1,0,0,1,0,1])
        self.assertEqual(r['by_template_kind'],dict(initial=1,fragment=1))

    def test_same_tick_new_edges_cannot_become_sources(self):
        cfg=scenario();cfg['chemistry'].update(sequence='01',free_units=4)
        events=[dict(time=1.,source=[0,1],formed=[2,3]),dict(time=1.,source=[2,3],formed=[4,5])]
        with self.assertRaisesRegex(AssertionError,'pre-tick'):reconstruct(cfg,events,[],[0,1,0,1,0,1])


if __name__=='__main__':unittest.main()
