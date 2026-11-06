"""Render/check a curated semantic rule ledger; never modify or run chemistry.

Source hashes detect stale audits. Semantic grouping remains an explicit human
review; a source if-count or repeated numeric literal count is not a chemistry.
"""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'research/CHEMISTRY_COMPLEXITY.json';VIEW=ROOT/'research/CHEMISTRY_COMPLEXITY.md'


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def value(config,path):
    for part in path.split('.'):config=config[part]
    return config


def load():
    data=json.loads(SOURCE.read_text(encoding='utf-8'));ref=data['reference'];path=ROOT/ref['manifest']
    if digest(path)!=ref['sha256']:raise ValueError('Reference scenario changed')
    config=next(q['scenario'] for q in json.loads(path.read_text())['tasks'] if q['label']==ref['label'])
    for name,sha in data['source_sha256'].items():
        if digest(ROOT/name)!=sha:raise ValueError('Review stale semantic audit after source change: '+name)
    ids={q['id'] for q in data['predicates']}
    for group in ('elementary','composites','bonds','ports','forces','reactions','predicates','configured','fixed','external','inactive'):
        entries=data[group]
        if len({q['id'] for q in entries})!=len(entries):raise ValueError('Duplicate ID in '+group)
        for row in entries:
            if any(not (ROOT/p).is_file() for p in row['source'].split(';')):raise ValueError('Missing source')
    for row in data['reactions']:
        if set(row['predicates'])-ids:raise ValueError('Unknown semantic predicate')
    for row in data['configured']:row['value']=value(config,row['path'])
    for row in data['external']:
        if row['path']:row['value']=value(config,row['path'])
    return data,config


def render(data,config):
    n=lambda group:len(data[group]);special=sum(q['category']=='functional' for q in data['predicates'])
    lines=['# Complexité de la chimie — inventaire sémantique v1','',
        'Revue '+data['reviewed']+' · candidat CP1 intégré (CH1), lois physiques inchangées par CR1.',
        '', '**Diagnostic : alphabet petit, spécialisation déjà substantielle.** La localité est mieux',
        'établie que la simplicité universelle ou la richesse fonctionnelle. Les chiffres suivants',
        'sont une convention de description vérifiable, pas une entropie de Shannon, un nombre de',
        'degrés de liberté indépendants ou une preuve de minimalité.',
        '', '| Élément compté | Bain intégré CP1 | Isolé CR1 |', '|---|---:|---:|']
    for group,label in [('elementary','Types élémentaires résolus'),('composites','Dimères chimiques possibles'),
                        ('bonds','Familles de liaison/contact structurel'),('ports','Rôles de ports'),
                        ('forces','Formules de force/potentiel intrinsèques'),('reactions','Schémas de transition dirigés')]:
        lines.append(f'| {label} | {n(group)} | {sum(q["scope"]=="both" for q in data[group])} |')
    lines+=['',f'**{n("predicates")} conditions sémantiques nommées** :4 d’occupation/valence,4 structurelles et{special}',
        'orientées vers une fonction. Elles sont partagées entre les schémas, pas additionnées une',
        'fois par appel ou par combinaison de symboles. Leur découpage est explicite ci-dessous.',
        '',f'**{n("configured")} entrées numériques configurées actives +{n("fixed")} contrôles numériques fixes recensés**,',
        f'plus{n("external")} contrôles d’environnement (période, fenêtre de relâchement, raideur des parois).',
        'Deux entrées peuvent avoir la même valeur ; cela ne fait pas deux paramètres indépendants.',
        'Les zéros d’interaction sont comptés dans la matrice de compatibilité, les epsilon numériques',
        'et identifiants/index ne sont pas des paramètres chimiques. Les constantes dérivées ne sont',
        'pas recomptées : raideur de capture, offset/raideur des ports, dénominateurs compétitifs.',
        'Le registre des28 contrôles fixes est une première revue sémantique, pas une extraction',
        'exhaustive de tous les littéraux Python.',
        '', '## Ce que ces chiffres rendent visible','',
        '- Les six types sont PG, PF, R0, R1, H et T. On peut factoriser P/R/H/T avec',
        '  un attribut G/F sur P et un symbole0/1 sur R ; les six combinaisons chimiques',
        '  autorisées restent bien distinctes. G0/G1/F0/F1/L sont cinq dimères, pas cinq',
        '  nouveaux atomes. Une chaîne, un gène et une vésicule ne sont pas de nouveaux types.',
        '- Les six liaisons se ramènent à quatre connectivités si l’on identifie les deux',
        '  axes PR/HT et les deux captures R–R/R–ligand. Leurs longueurs et conditions',
        '  restent différentes : le décompte détaillé6 évite de cacher ces profils.',
        '- Le moteur utilise4 classes de collision, différentes des6 types chimiques : P, R,',
        '  H/T libres et H/T liés. Sur10 canaux non ordonnés,5 sont répulsifs et5 transparents.',
        '  Trois distances positives seulement (.28,.4,.7), plus le cas transparent0.',
        '  Un changement libre/lié est une véritable règle contextuelle.',
        '- Huit formules intrinsèques couvrent plusieurs profils : le même ressort sert',
        '  cinq rôles paramétrés (PR, HT, squelette, appariement, capture). L’angle a deux',
        '  profils actifs, G à0 et F à.8. Les symboles F0/F1 ont actuellement la même',
        '  préférence angulaire : bibliothèque de replis programmables non démontrée.',
        '- La capture est mutualisée entre P/R et H/T, mais le code impose encore leur',
        '  compatibilité et l’identité des sites F0/F1. Ce n’est pas une chimie indifférenciée.',
        '- L’isolé CR1 a tous ses H/T déjà liés. Sans rupture axiale, la synthèse HT n’y',
        '  est pas accessible : seulement formation, rupture et échange de contacts latéraux.',
        '  Ses petits nombres ne décrivent donc pas le coût de la cellule intégrée.',
        '- Les pertes/recyclages, régulations et outils distincts nécessaires au maintien',
        '  ne sont pas tous intégrés. Le coût du système final n’est pas encore borné par cet inventaire.',
        '', '## Principales dettes de spécialisation','',
        'Les rôles G et F sont attribués aux supports primitifs : seuls G peuvent fournir',
        'la matrice, F–F ne s’apparient pas. F0 recrute les catégories P/H et F1 les',
        'catégories R/T. Un motif local de deux sites voisins déclenche la catalyse ;',
        'il n’y a pas de primitive représentant une protéine entière, mais cette grammaire',
        'est choisie pour les fonctions recherchées. La coopération qui exclut les mélanges',
        'P/R–H/T, les échanges terminaux et la barrière visant les PR assemblés sont aussi',
        'des choix spécifiques. Le filtre énergétique traite HT/L différemment des PR.',
        'Enfin, la libération périodique est un helper externe, pas une autonomie émergente.',
        '', '## Comment comparer les prochaines variantes','',
        'Comparer le vecteur (atomes résolus, composites, profils de liaisons, ports, formules,',
        'transitions, prédicats fonctionnels, contrôles numériques, forcing) sous cette même',
        'convention. Donner les IDs ajoutés/retirés et leur réutilisation démontrée. Un nouveau',
        'seuil par réaction ou une nouvelle affinité spécialisée augmente le coût même si le',
        'nombre de particules reste fixe. Un passage gaussien→compétitif change une formule,',
        'sans ajouter d’atome, mais augmente sa portée/coût : ces deux axes restent séparés.',
        'Ne pas fusionner des lignes après coup pour faire baisser artificiellement le score.',
        'Une nouvelle famille de fonctions obtenue par assemblage sous lois fixes constitue',
        'la contrepartie recherchée ; compter les démos ou les lignes de code ne la remplace pas.',
        '', '## Détail des primitives, transitions et conditions','']
    for group,title in [('elementary','Types élémentaires'),('composites','Dimères'),('bonds','Liaisons/contact'),('ports','Ports'),('forces','Formules intrinsèques'),('reactions','Transitions dirigées'),('predicates','Conditions partagées')]:
        lines+=['### '+title,'','| ID | Définition | Détail | Source |','|---|---|---|---|']
        for row in data[group]:
            detail=row.get('category','')
            if 'predicates' in row:detail=', '.join(row['predicates']) or 'Horloge externe / état local'
            if 'capacity' in row:detail='capacité '+str(row['capacity'])+' sur le porteur concerné'
            sources=', '.join(f'[{Path(p).name}](../{p})' for p in row['source'].split(';'))
            lines.append(f'| {row["id"]} | {row["label"]} | {detail} | {sources} |')
        lines.append('')
    lines+=['### Registres d’état dérivés','', '| Registre | Valeurs |','|---|---|']
    for row in data['state_registers']:lines.append('| '+row['label']+' | '+', '.join(row['states'])+' |')
    lines+=['', 'Ces états concernent des porteurs différents ; leur produit cartésien ne décrit pas',
        'un nombre d’espèces indépendant. Activité et repli dépendent d’occupations existantes,',
        'pas de deux nouvelles molécules ou de labels de fonction entière.','']
    for group,title in [('configured','Contrôles numériques configurés'),('fixed','Contrôles numériques fixes recensés'),('external','Contrôles externes')]:
        lines+=['### '+title,'', '| ID | Quantité | Valeur | Source |','|---|---|---:|---|']
        for row in data[group]:
            sources=', '.join(f'[{Path(p).name}](../{p})' for p in row['source'].split(';'))
            lines.append(f'| {row["id"]} | {row["label"]} | {row["value"]} | {sources} |')
        lines.append('')
    lines+=['## Exclusions et limites','']+[f'- {row["label"]}.' for row in data['inactive']]
    lines+=['', 'Le bain de Langevin, les parois et l’horloge externe sont explicitement distincts',
        'des8 potentiels intrinsèques. Initialisations, observations, critères de réussite,',
        'pas/caches/JIT, gardes de stabilité numérique et variantes historiques sont exclus',
        'du compte chimique. Les coefficients des parois et de l’horloge restent déclarés.',
        '', 'Source structurée : [CHEMISTRY_COMPLEXITY.json](CHEMISTRY_COMPLEXITY.json).',
        'Génération/vérification : `python experiments/chemical_complexity.py build` / `check`.',
        'Les hashes invalident la fiche quand une source auditée change ; une revue sémantique',
        'doit alors déterminer ce qui a réellement changé. Aucun test de ce registre ne pilote la simulation.','']
    return '\n'.join(lines)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['build','check']);a=p.parse_args()
    data,config=load();view=render(data,config)
    if a.action=='build':VIEW.write_text(view,encoding='utf-8')
    elif not VIEW.exists() or VIEW.read_text(encoding='utf-8')!=view:raise SystemExit('Regenerate stale complexity view')
    print(json.dumps({k:len(data[k]) for k in ('elementary','composites','bonds','ports','forces','reactions','predicates','configured','fixed','external')}))
