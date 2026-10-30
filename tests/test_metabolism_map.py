"""Semantic figure checks: prevent a polished chart from dropping dependencies."""
import copy,json,unittest
from xml.etree import ElementTree as ET
from experiments.build_metabolism_map import load_model,build_svg,build_html


class MetabolismMapTests(unittest.TestCase):
    def test_every_canonical_reaction_gene_and_tool_is_present(self):
        m=load_model();svg=build_svg(m);root=ET.fromstring(svg)
        ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual({x[9:] for x in ids if x.startswith('reaction-')},
            {r['id'] for r in m['network']['reactions']})
        for role in m['spec']['roles']:
            self.assertIn('species-'+role['gene'],ids);self.assertIn('species-'+role['tool'],ids)
        namespace={'s':'http://www.w3.org/2000/svg'}
        metadata=json.loads(root.find('s:metadata',namespace).text)
        self.assertEqual(metadata['network'],m['network'])
        for reaction in metadata['network']['reactions']:
            if reaction['kind']=='polymer':
                self.assertEqual(len(reaction['catalysts']),1)
                self.assertNotIn(reaction['catalysts'][0],reaction['inputs'])

    def test_no_functional_sequence_or_demonstrated_target_is_fabricated(self):
        m=load_model();svg=build_svg(m)
        self.assertEqual(m['annotations']['genome']['sequences'],dict(gN=None,gA=None,gL=None))
        self.assertEqual(m['nominal']['length'],24)
        self.assertEqual((m['current_sequence'],m['current_gene_copies']),('001',16))
        self.assertEqual(svg.count('Séquence à concevoir'),3)
        self.assertIn('CIBLE CONDITIONNELLE',svg)
        self.assertIn('mécanisme de recyclage à choisir',svg)

    def test_determinism_and_curated_evidence_reaches_the_document(self):
        m=load_model();svg=build_svg(m)
        self.assertEqual(svg,build_svg(load_model()))
        m=copy.deepcopy(m);m['annotations']['current']['notes'][0]='CHANGEMENT DE PREUVE'
        self.assertIn('CHANGEMENT DE PREUVE',build_svg(m))
        html=build_html(svg)
        self.assertIn(svg,html);self.assertNotIn('<!-- GENERATED_MAP -->',html)
        self.assertNotIn('<script src=',html);self.assertNotIn('<link href=',html)


if __name__=='__main__':unittest.main()
