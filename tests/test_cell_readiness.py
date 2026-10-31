import copy,re,unittest
from experiments.cell_readiness import load,validate,validate_integration_links,group_rows,views,STAGES


class ReadinessTests(unittest.TestCase):
    def test_fine_view_each_requirement_once_in_its_own_group(self):
        d=load();text=views(d)['CELL_CHECKLIST.md']
        ids=re.findall(r'<a id="([^"]+)"></a>',text)
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(set(ids),{r['id'] for r in d['items']})
        for g in d['groups']:
            section=text.split('## '+g['label']+'\n',1)[1].split('\n## ',1)[0]
            self.assertEqual(set(re.findall(r'<a id="([^"]+)"></a>',section)),
                             {r['id'] for r in d['items'] if r['group']==g['id']})
    def test_unknown_integration_links_fail_and_unmapped_goals_remain_visible(self):
        d=load();case=dict(tests=[dict(id='case',checklist_ids=['Z-99'])])
        with self.assertRaises(ValueError):validate_integration_links(d,case)
        unmapped=validate_integration_links(d,dict(tests=[]))
        self.assertEqual(set(unmapped),{r['id'] for r in d['items']})
    def test_actual_register_includes_distinct_macro_controls_and_cycles(self):
        d=load();by_id={r['id']:r for r in d['items']}
        self.assertEqual(by_id['H-03']['group'],'large') # F populations
        self.assertEqual(by_id['H-04']['group'],'large') # each gene population
        self.assertIn('W-03',by_id['H-03']['needs']) # retained mass must have a destination
        self.assertIn('W-02',by_id['H-06']['needs'])
        self.assertIn('H-06',by_id['W-02']['needs']) # biological cycle must not be rejected as a DAG error

    def test_dangling_dependencies_references_and_manual_percentages_are_rejected(self):
        for mutation in ('dependency','reference','percent'):
            d=copy.deepcopy(load());r=d['items'][0]
            if mutation=='dependency':r['needs'].append('Z-99')
            if mutation=='reference':r['references'].append('research/does_not_exist.md')
            if mutation=='percent':r['percent']=97
            with self.assertRaises(ValueError):validate(d)

    def test_evidence_and_concept_gates_prevent_unsupported_completion(self):
        d=copy.deepcopy(load());d['items'][0]['references']=[]
        with self.assertRaises(ValueError):validate(d)
        d=copy.deepcopy(load());r=next(r for r in d['items'] if r['id']=='C-04')
        r.update(proof='target',concept='draft')
        with self.assertRaises(ValueError):validate(d)
        d=copy.deepcopy(load());d['items'][0]['proof']='target'
        with self.assertRaises(ValueError):validate(d)

    def test_ranges_are_not_averages_and_scale_is_fixed(self):
        self.assertEqual([x[0] for x in STAGES.values()],[0,25,50,75,100])
        d=load()
        for g in group_rows(d):
            scores=[STAGES[r['proof']][0] for r in d['items'] if r['group']==g['id']]
            self.assertEqual((g['low'],g['high']),(min(scores),max(scores)))
            self.assertEqual(g['points'],len(scores))

    def test_new_subgoals_and_traceable_splits_render_without_fixed_item_count(self):
        d=copy.deepcopy(load());old=next(r for r in d['items'] if r['id']=='O-01')
        new=copy.deepcopy(old);new.update(id='Z-01',label='Nouveau sous-but séparé')
        d['items'].remove(old);d['items'].append(new)
        for r in d['items']:
            for field in ('needs','renewal_needs'):r[field]=['Z-01' if i=='O-01' else i for i in r[field]]
        d['retired'].append(dict(id='O-01',reason='Scission explicitée',replaced_by=['Z-01']))
        validate(d)
        text='\n'.join(views(d).values())
        self.assertIn('Nouveau sous-but séparé',text);self.assertIn('Scission explicitée',text)
        d['retired'][0]['reason']=''
        with self.assertRaises(ValueError):validate(d)


if __name__=='__main__':unittest.main()
