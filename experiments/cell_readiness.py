"""Validate and render the evolving cell requirements register, never simulate it."""
import argparse,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'research/cell_checklist.json'
STAGES={'none':(0,'non observé'),'subcase':(25,'sous-cas étayé'),
    'separate':(50,'test séparé'),'coupled':(75,'couplage partiel'),'target':(100,'critère satisfait')}
CONCEPTS={'none':'sans draft','gap':'esquisse à fermer','draft':'draft décrit'}
OUTPUTS=('CELL_CHECKLIST_COMPACT.md','CELL_CHECKLIST.md')


def validate(data,check_paths=True):
    if data.get('schema_version')!=1 or type(data.get('revision')) is not int or data['revision']<1:
        raise ValueError('Unknown schema or invalid revision')
    groups={g['id']:g for g in data['groups']};items={r['id']:r for r in data['items']}
    if len(groups)!=len(data['groups']) or len(items)!=len(data['items']):raise ValueError('Duplicate ID')
    retired={r['id']:r for r in data['retired']}
    if len(retired)!=len(data['retired']) or set(retired)&set(items):raise ValueError('Retired/active ID collision')
    for key,r in retired.items():
        if not r.get('reason') or not r.get('replaced_by') or set(r['replaced_by'])-set(items):
            raise ValueError('Retirement needs reason and active replacements: '+key)
    for key,r in items.items():
        if not re.fullmatch(r'[A-Z]+-\d{2}',key) or r['group'] not in groups:raise ValueError('Invalid ID/group: '+key)
        if r['concept'] not in CONCEPTS or r['proof'] not in STAGES:raise ValueError('Unknown stage: '+key)
        if 'percent' in r:raise ValueError('Percentages derive from proof stages, not manual estimates')
        for field in ('label','done_when','scope','next_test'):
            if not isinstance(r.get(field),str) or not r[field].strip():raise ValueError('Missing '+field+': '+key)
        if r['concept']!='none' and not r['mechanism'].strip():raise ValueError('Mechanism missing: '+key)
        if r['concept'] in ('none','gap') and not r['concept_gap'].strip():raise ValueError('Concept gap missing: '+key)
        deps=r['needs']+r['renewal_needs']
        if key in deps or set(deps)-set(items):raise ValueError('Dangling, retired or self dependency: '+key)
        if STAGES[r['proof']][0]>0 and not r['references']:raise ValueError('Evidence required: '+key)
        if r['proof']=='target' and r['concept']!='draft':raise ValueError('Target claim with conceptual gap: '+key)
        if check_paths:
            for ref in r['references']:
                p=(ROOT/ref.split('#')[0]).resolve()
                if not p.is_relative_to(ROOT) or not p.is_file():raise ValueError('Missing/local reference: '+ref)
    if set(groups)-{r['group'] for r in items.values()}:raise ValueError('Empty group')
    for focus in data.get('decision_focus',[]):
        if not focus.get('reason') or set(focus['items'])-set(items):raise ValueError('Invalid decision focus')
    for key,note in data.get('last_batch_progress',{}).items():
        if key not in items or not isinstance(note,str) or not note.strip():
            raise ValueError('Invalid last-batch progress: '+key)
    if not data['history'] or data['history'][-1]['revision']!=data['revision']:
        raise ValueError('Revision requires a history entry')
    # Cycles are expected in biological renewal; deliberately no DAG test.
    if 'C-04' in items and items['C-04']['proof']=='target':
        missing=[k for k,r in items.items() if r['essential'] and r['proof']!='target']
        if missing:raise ValueError('Integrated claim with open essential requirements: '+','.join(missing))
    return data


def validate_integration_links(data,cases):
    ids={r['id'] for r in data['items']};seen=set()
    for case in cases['tests']:
        linked=case.get('checklist_ids',[])
        if set(linked)-ids:raise ValueError('Unknown/retired checklist link: '+case['id'])
        seen.update(linked)
    return sorted(ids-seen)


def load():
    data=validate(json.loads(SOURCE.read_text(encoding='utf-8')))
    data['_integration_unmapped']=validate_integration_links(data,json.loads((ROOT/'research/INTEGRATION_TESTS.json').read_text(encoding='utf-8')))
    return data


def group_rows(data):
    rows=[]
    for g in data['groups']:
        members=[r for r in data['items'] if r['group']==g['id']]
        scores=[STAGES[r['proof']][0] for r in members]
        gaps=[r['id'] for r in members if r['concept']!='draft']
        status=('sans draft' if any(r['concept']=='none' for r in members) else 'à fermer') if gaps else 'drafts décrits'
        rows.append(dict(id=g['id'],label=g['label'],low=min(scores),high=max(scores),
            points=len(members),gaps=gaps,concept=status,progress=' ; '.join(
                r['id']+' : '+data.get('last_batch_progress',{})[r['id']] for r in members
                if r['id'] in data.get('last_batch_progress',{})) or '—'))
    return rows


def compact(data):
    lines=['# Checklist compacte — cellule construite maintenue','',
        f"Révision {data['revision']} · revue {data['reviewed']} · {len(data['items'])} sous-buts · {data['candidate']}",'',
        '**Pourcentages = paliers de preuve**, pas effort accompli ni probabilité de réussite. '
        'Les plages indiquent min–max des sous-buts ; aucune moyenne globale.',
        '0% non observé ·25% sous-cas ·50% séparé ·75% couplage partiel ·100% critère satisfait sur son domaine.',
        'Concept : « à fermer » signale au moins un maillon essentiel manquant ; un draft décrit reste hypothétique.','',
        '| Domaine | Points | Concept | Preuve min–max | Trous conceptuels | Progrès du dernier lot |',
        '| --- | ---: | --- | ---: | --- | --- |']
    for r in group_rows(data):
        score=f"{r['low']}%" if r['low']==r['high'] else f"{r['low']}–{r['high']}%"
        gaps=', '.join(r['gaps']) or '—'
        lines.append(f"| {r['label']} | {r['points']} | {r['concept']} | {score} | {gaps} | {r['progress']} |")
    lines+=['','**Trous conceptuels prioritaires au présent bilan :**','']
    for focus in data.get('decision_focus',[]):lines.append('- '+', '.join(focus['items'])+' : '+focus['reason'])
    lines+=['','Voir [draft des outils](FUNCTIONAL_MECHANISMS.md) et [homéostasie des polymères](MACROMOLECULE_HOMEOSTASIS.md).',
        '', '[Détails, critères, dépendances, preuves et prochain test](CELL_CHECKLIST.md) · '
        '[Méthode et évolution](CONCEPT_FIRST.md).', '',
        'Un75% peut être un couplage limité avec outil préparé ; aucun maintien durable implicite. '
        'Le100% logiciel concerne les références actuelles et ne valide aucune fonction biologique.',
        'Cible hors périmètre : '+', '.join(data['out_of_scope'])+'.',
        '', 'Généré par `python experiments/cell_readiness.py build` depuis `cell_checklist.json`.']
    if data.get('_integration_unmapped'):
        lines+=['','**Points pas encore reliés à un cas de test d’intégration :** '+', '.join(data['_integration_unmapped'])+'.']
    return '\n'.join(lines)+'\n'


def fine(data):
    lines=['# Checklist détaillée — critères et dépendances','',
        f"Revue {data['reviewed']} · révision{data['revision']}. Source : [cell_checklist.json](cell_checklist.json).",
        '[Tableau compact](CELL_CHECKLIST_COMPACT.md) · [Échelle et méthode](CONCEPT_FIRST.md).','',
        'Les dépendances ci-dessous sont les capacités requises à terme, pas un ordre '
        'acyclique de codage. Les cycles de renouvellement sont intentionnels. '
        'Une condition initiale construite peut amorcer un sous-cas sans fermer ces cycles.','']
    def links(ids):return ', '.join(f'[{i}](#{i})' for i in ids) or '—'
    for group in data['groups']:
        lines+=['## '+group['label'],'']
        for r in data['items']:
            if r['group']!=group['id']:continue
            percent,label=STAGES[r['proof']]
            lines += [f'<a id="{r["id"]}"></a>',f"### {r['id']} — {r['label']}",'',
                f"**Concept : {CONCEPTS[r['concept']]} · Preuve : {percent}% ({label}).**",
                '', '**Aboutissement :** '+r['done_when'],
                '', '**Draft local :** '+(r['mechanism'] or 'Pas de mécanisme local défendable décrit.'),
                '', '**Manque / limite :** '+r['concept_gap'],
                '', '**Dépend de :** '+links(r['needs'])+' · **Pour renouveler :** '+links(r['renewal_needs']),
                '', '**Portée des preuves :** '+r['scope'],
                '', '**Références :** '+(', '.join(f'[{p}](../{p})' for p in r['references']) or 'Aucune preuve dynamique.'),
                '', '**Prochain test / décision :** '+r['next_test'],'']
            if r['id'] in data.get('last_batch_progress',{}):
                lines+=['**Progrès du dernier lot :** '+data['last_batch_progress'][r['id']],'']
    lines+=['## Évolution conservée','']
    for h in data['history']:lines.append(f"- Révision{h['revision']} ({h['date']}) : {h['reason']}")
    for r in data['retired']:lines.append(f"- Retiré {r['id']} : {r['reason']} → "+', '.join(r['replaced_by']))
    return '\n'.join(lines)+'\n'


def views(data):return dict(zip(OUTPUTS,(compact(data),fine(data))))


if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['status','build','check']);a=p.parse_args()
    data=load();rendered=views(data)
    if a.action=='status':print(rendered[OUTPUTS[0]])
    elif a.action=='build':
        for name,text in rendered.items():(ROOT/'research'/name).write_text(text,encoding='utf-8')
        print(f"{len(data['items'])} points, {len(data['groups'])} domaines, deux vues générées ; aucun score global.")
    else:
        stale=[name for name,text in rendered.items() if not (ROOT/'research'/name).is_file() or
            (ROOT/'research'/name).read_text(encoding='utf-8')!=text]
        if stale:raise SystemExit('Regenerate changed views: '+', '.join(stale))
        print('Registre, dépendances, références et vues cohérents.')
