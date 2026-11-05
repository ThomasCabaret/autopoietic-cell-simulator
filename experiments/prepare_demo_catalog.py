"""Build reproducible GUI presets from preserved research inputs, not result data."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve


def signature(cfg):
    resolved=resolve(cfg)
    payload={k:resolved[k] for k in ('model','seed','duration','engine','chemistry')}
    if 'mechanics' in resolved:payload['mechanics']=resolved['mechanics']
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def origins():
    manifest='research/campaign_recipes/J3_20261027T192723206222Z/manifest.json'
    data=json.loads((ROOT/manifest).read_text(encoding='utf-8'))
    items=[]
    for seed in (2,0,1):
        task=next(t for t in data['tasks'] if t['label']=='J3_k16_bath' and t['scenario']['seed']==seed)
        items.append((f'integrated_s{seed}','integrated',f'Graine {seed}'+(' · transfert observé' if seed==2 else ''),
            copy.deepcopy(task['scenario']),manifest,task['id'],2118))
    for key,origin,beads in (
        ('material_cycle','research/engine_runs/C3Bexpress_s1_20261025T094654876859Z/scenario.json',102),
        ('binary_copy','research/engine_runs/Copie_binaire_composite_s0_20261023T140139872073Z/scenario.json',108),
        ('free_membrane','research/engine_runs/Vesicules_depuis_des_molecules_isolees_s0_20261023T153753630959Z/scenario.json',72)):
        cfg=json.loads((ROOT/origin).read_text(encoding='utf-8'))
        items.append((key,key,f"Graine {cfg['seed']}",cfg,origin,None,beads))
    return items


def current_origins():
    source='research/campaign_recipes/MD2_20261030T115427443420Z/manifest.json'
    data=json.loads((ROOT/source).read_text(encoding='utf-8'));items=[]
    for group,prefix,label,beads in (
        ('current_cell','MD2_bath_new','Cellule construite',2118),
        ('current_free','MD2_free_new','Assemblage depuis molécules libres',72),
        ('current_probes','MD2_probes_new','Insertion et sondes',534)):
        for seed in (2,0,1):
            task=next(t for t in data['tasks'] if t['label']==f'{prefix}_s{seed}')
            items.append((f'{group}_s{seed}',group,f'Graine {seed}',copy.deepcopy(task['scenario']),source,task['id'],beads))
    return items


def current_descriptions():
    common=dict(conditions='Langevin, masse 1, frottement 0,1 ; température 0,08, dt 0,002 ; contacts liés/libres cohérents MD2. Paramètres identiques à la recette étudiée, sans réglage de la vue.',
        evidence='research/BATCH_25_RESULTS.md',archive=False)
    return [dict(common,id='current_cell',title='Cellule construite · état actuel',level='Candidat MD2 · bain le plus intégré',
        summary='Membrane, gènes, outils et précurseurs dans un même bain sous Langevin.',
        question='Voir la tenue de la membrane et les vrais transferts de matière ; les nouvelles chaînes fonctionnelles restent le prochain verrou.',
        prepared='219 molécules L en anneau et 24 libres internes ; 16 G001 et 16 F001 complets préparés, 48 monomères F et précurseurs P/R. Total : 2 118 billes.',
        observe='Des outils initialement construits fabriquent des composants réellement utilisés. Fermeture régulière observée : 85,5 / 72,8 / 86,9 % sur graines 0 / 1 / 2 ; nouveaux G libérés : 0 / 1 / 1 ; aucun nouveau F complet libéré à 1 200.',
        limits='Cellule initialement construite, pas cellule viable démontrée : outils non renouvelés, L non synthétisés, pas de flux de nourriture, d’homéostasie ou division. Ouvertures réelles laissées visibles. Départ à t=0, pas de film précalculé.',
        conditions=common['conditions']+' Cycle externe 200 / 15. Graine 2 recommandée pour illustrer une copie G et une bonne tenue ; choix illustratif, les trois graines restent accessibles.',
        look='Jouer en Maximum, vue globale puis zoom au centre. Sélectionner une bille et suivre ses partenaires dans Explorer. Le grand bain peut demander des dizaines de minutes pour 1 200 ; les copies G sont rares, aucune copie F à promettre.'),
      dict(common,id='current_free',title='Membranes · molécules libres',level='MD2 · sous-système séparé, trois graines',
        summary='Les contacts actuels assemblent 36 molécules isolées en petits contours.',
        question='Vérifier l’assemblage sans chaîne ou contour déjà préparé, avec la même forme de potentiel de ports.',
        prepared='36 dimères H/T construits et dispersés ; aucune liaison latérale initiale. Total : 72 billes.',
        observe='Premiers contours observés à 20 / 10 / 59 selon graine 0 / 1 / 2, puis associations et ruptures réelles. Les trois essais ferment des contours ; tailles et nombres finaux varient.',
        limits='Les dimères sont fournis. Petits contours à géométrie différente de la grande membrane ; pas de contenu cellulaire, de fabrication de L ou de rétention prouvée par cette scène.',
        look='C’est la scène rapide pour commencer. Jouer en Maximum, puis ralentir et zoomer sur une extrémité. Les contours sont reconnus par l’observateur, jamais refermés par un contrôleur.'),
      dict(common,id='current_probes',title='Membrane · insertion et passages',level='MD2 · contrôle séparé L et sondes',
        summary='Grande membrane préparée, molécules L libres internes et deux familles de sondes.',
        question='Observer l’insertion locale et les passages sélectifs, y compris les défauts qui persistent.',
        prepared='219 dimères L en anneau et 24 libres internes ; 24 sondes retenues initialement internes et 24 perméables initialement externes. Total : 534 billes, sans gène ou outil protéique.',
        observe='Insertions persistantes observées : 1 / 1 / 2 sur graines 0 / 1 / 2. La graine 1 se dégrade durablement après 224 ; elle est conservée. Les compteurs affichent les entrées/sorties effectivement observées.',
        limits='Frontière non classable = inconnu, pas étanchéité supposée. Zéro sortie observée ne garantit rien pendant ces périodes. Sondes de contrôle, pas synthèse de nourriture ni cellule intégrée.',
        look='Zoomer sur une molécule L libre près de la membrane et activer le suivi. Filtrer les sondes dans Explorer. La graine 2 montre deux insertions persistantes ; la graine 1 montre un échec important.')]


def renewal_origins():
    source='research/campaign_recipes/MIN1R_20261031T110654015735Z/manifest.json'
    data=json.loads((ROOT/source).read_text(encoding='utf-8'));items=[]
    for seed in range(3):
        task=next(t for t in data['tasks'] if t['label']==f'MIN1R_active_s{seed}')
        items.append((f'current_renewal_s{seed}','current_renewal',f'Graine {seed}',
            copy.deepcopy(task['scenario']),source,task['id'],150))
    return items


def renewal_description():
    return dict(id='current_renewal',title='Catalyseurs reconstruits · progrès récent',
        level='MD2 / MIN1R · boucle matérielle sans membrane',archive=False,
        summary='De la nourriture à un nouveau catalyseur entier, puis à son activité.',
        question='L’outil peut-il reconstruire des composants qui deviennent à leur tour un outil fonctionnel ?',
        prepared='4 G01 et un F01 construits, quatre F monomères et précurseurs P/R libres. 150 billes, boîte12×9 ; aucun composant membranaire.',
        observe='À1200 :10 F entièrement refaits depuis P/R dans chaque graine, dont5 /2 /1 actifs ensuite pour12 /9 /9 opérations. Première activité à392,68 /192,14 /395,92. Les compteurs distinguent nouveaux F, F entièrement refaits et activité ultérieure.',
        conditions='Lois MD2 inchangées, Langevin masse1/frottement0,1, température0,08, dt0,002 ; cycle externe200/15. Trois graines intégrales, sans sélection de la plus favorable.',
        limits='L’outil initial reste présent. Production de remplaçants fonctionnels, pas remplacement sous pertes ni maintien cellulaire. Stocks finis, pas membrane, synthèse L ou homéostasie. Gène très court, pas capacité informationnelle générale.',
        look='Jouer en Maximum pour atteindre le premier outil neuf actif, puis ralentir et suivre une chaîne. Les F initiaux sont exclus des trois compteurs de nouveauté. La simulation repart réellement de t0 ; aucun film précalculé.',
        evidence='research/BATCH_34.md')


def membrane_renewal_origins():
    source='research/campaign_recipes/MIN1M_20261104T113752867767Z/manifest.json'
    data=json.loads((ROOT/source).read_text(encoding='utf-8'));items=[]
    for seed in range(3):
        task=next(t for t in data['tasks'] if t['label']==f'MIN1M_active_s{seed}')
        items.append((f'current_membrane_renewal_s{seed}','current_membrane_renewal',f'Graine {seed}',
            copy.deepcopy(task['scenario']),source,task['id'],2118))
    return items


def membrane_renewal_description():
    return dict(id='current_membrane_renewal',title='Membrane et catalyseurs reconstruits · progrès actuel',
        level='MD2 / MIN1M · transfert dans le même bain',archive=False,
        summary='Membrane, copie courte, expression et catalyseurs entièrement refaits dans un même bain.',
        question='La reconstruction matérielle de F01 reste-t-elle fonctionnelle avec la membrane présente ?',
        prepared='219 L en anneau et24 L libres ;16 G01 et16 F01 préparés,64 F monomères et P/R libres. 2118 billes ; stocks totaux432 supports G et384 F.',
        observe='À1200, graines0/1/2 :7/6/2 F entièrement refaits depuis nourriture, dont6/4/2 actifs ensuite pour12/6/16 opérations. Première activité à776,02/606,11/607,46 ; membrane fermée sur85,7/85,6/85,3% des observations régulières. Les trois témoins sans gène ne produisent aucun nouveau F.',
        conditions='Lois MD2 inchangées ; Langevin masse1/frottement0,1, température0,08, dt0,002 ; cycle externe200/15. Trois graines disponibles. Graine0 ouverte par défaut par convention, sans sélection de résultat.',
        limits='Départ construit et outils initiaux toujours présents. Production de remplaçants fonctionnels, pas remplacement sous pertes ni maintien. L préparés, pas synthétisés ; stocks finis, pas flux extérieur, homéostasie ou information longue démontrés. Le prototype H/T séparé n’est pas inclus.',
        look='Jouer en Maximum ; le grand bain demande des dizaines de minutes pour1200. Examiner les compteurs F entièrement refaits et actifs, puis zoomer ou suivre une particule avec Explorer. Simulation réelle depuis t0, pas trajectoire précalculée.',
        evidence='research/BATCH_40.md')


def descriptions():
    result=[dict(id='integrated',title='Bain intégré actuel',level='Intégration partielle · priorité de lecture',
        summary='Membrane, gènes, outils et précurseurs dans un même bain.',
        prepared='219 molécules membranaires en anneau + 24 libres ; 16 G001 et 16 F001 déjà construits, 48 monomères F, précurseurs P/R libres. 2 118 billes au total.',
        observe='Voir la membrane et son contenu, zoomer sur une chaîne, suivre ses liaisons. Les outils fabriquent des composants ; leur incorporation et les nouvelles chaînes restent rares.',
        limits='La membrane est préparée et peut se dégrader. Ses molécules ne sont pas fabriquées. Stock de nourriture fini, sans apport continu, homéostasie ni cellule viable démontrés.',
        conditions='Température 0,08 ; cycle externe 200 / 15. Les trois graines sont celles de J3. La graine 2 est choisie pour montrer un outil exprimé produisant de la matière ensuite utilisée, pas pour établir une fréquence de réussite.',
        look='Commencer par la vue globale (F), puis zoomer au centre. Cliquer une bille et ouvrir l’onglet Explorer pour suivre son assemblage. À vitesse maximale, le calcul peut prendre plusieurs minutes ; aucune animation n’est précalculée.',
        evidence='research/BATCH_16_RESULTS.md'),
      dict(id='material_cycle',title='Copie, expression et fabrication',level='Sous-système séparé · bain chaud',
        summary='G → F exprimé → fabrication de composants → réutilisation.',
        prepared='Un G001 et six monomères F préparés ; les autres P et R sont libres. Aucun outil F complet n’est construit au départ. 102 billes.',
        observe='Les monomères s’organisent sur le gène. Après libération, un F exprimé peut catalyser l’assemblage de vrais P/R ; les produits peuvent entrer dans de nouvelles chaînes.',
        limits='Pas de membrane. Température différente du bain intégré : cette réussite séparée n’établit pas leur compatibilité complète. Ni alimentation continue ni renouvellement durable.',
        conditions='Température 0,6 ; cycle externe 200 / 15 ; graine 1 sélectionnée parmi les essais du lot 8 pour illustrer le transfert. Même scénario physique que l’essai archivé.',
        look='Laisser avancer au maximum, puis mettre en pause ou ralentir. Les compteurs distinguent les nouveaux produits des structures préparées ; les flashes montrent les changements de liens.',
        evidence='research/BATCH_08.md'),
      dict(id='binary_copy',title='Copie binaire seule · six symboles',level='Sous-système séparé · copie',
        summary='Un polymère 001011 recrute et relie des sous-unités composites.',
        prepared='Une chaîne de six dimères et 48 dimères monomères libres : 108 billes. Les dimères sont fournis, pas fabriqués dans cet essai.',
        observe='Suivre la chaîne initiale et ses partenaires. Les appariements positionnent les monomères ; de nouvelles liaisons forment des chaînes qui peuvent être libérées.',
        limits='Pas de traduction, de synthèse des dimères ou de membrane. La capacité à copier six symboles ici ne valide pas un génome long ou le circuit intégré.',
        conditions='Température 0,6 ; cycle externe 200 / 15 ; graine 0 du témoin T7 historique. La libération est aidée par le cycle fourni.',
        look='Passer en vitesse maximale jusqu’aux associations, puis ralentir et sélectionner la chaîne. Une copie complète exclut la chaîne initialement préparée.',
        evidence='research/ENGINE_MIGRATION.md'),
      dict(id='free_membrane',title='Petites membranes depuis molécules libres',level='Sous-système séparé · assemblage moléculaire',
        summary='36 molécules à deux billes, sans chaîne ou anneau préassemblé.',
        prepared='36 dimères H/T isolés et dispersés : 72 billes. Les liaisons internes des molécules existent déjà ; aucune liaison latérale initiale.',
        observe='Les molécules se rencontrent, forment des fragments et peuvent fermer de petits contours. Zoomer sur une extrémité pour voir association et rupture.',
        limits='Ces petites vésicules ne sont pas la grande membrane du bain intégré : géométrie et paramètres distincts. Pas de contenu cellulaire, de synthèse membranaire ou de rétention validés ici.',
        conditions='Température 0,08 ; graine 0 ; aucun ruban initial replié. Les lois restent celles de la référence V8 à petits contours.',
        look='Observer d’abord l’ensemble à vitesse maximale, puis ralentir lors de l’assemblage. Les contours fermés sont identifiés après coup, sans guider la dynamique.',
        evidence='research/BATCH_03.md')]
    questions=dict(
        integrated='Langevin améliore-t-il le transfert utile sans dégrader la membrane, la rétention et les outils ? La membrane de départ est préparée.',
        material_cycle='Le mouvement accéléré conserve-t-il G → F exprimé → composants fabriqués puis réellement réutilisés ?',
        binary_copy='Les rencontres supplémentaires produisent-elles des copies complètes libérées ou surtout des fragments concurrents ?',
        free_membrane='Les molécules isolées ferment-elles encore des contours avec inertie ? Aucune chaîne latérale ne doit être préparée.')
    for item in result:item['question']=questions[item['id']]
    return result


def langevin_variant(config):
    cfg=resolve(config)
    cfg['mechanics']=dict(motion='langevin',mass=1.,damping=.1,dpd_cutoff=1.)
    cfg['name']+=' · Langevin candidat';cfg['branch']='LT2'
    return resolve(cfg)


def mixed_origins():
    source='research/campaign_recipes/MX2_20261104T203221072374Z/manifest.json'
    data=json.loads((ROOT/source).read_text(encoding='utf-8'));items=[]
    for seed in range(3):
        task=next(t for t in data['tasks'] if t['label']==f'MX2_cooperative_s{seed}')
        items.append((f'current_mixed_s{seed}','current_mixed',f'Graine {seed}',copy.deepcopy(task['scenario']),source,task['id'],198))
    return items


def mixed_description():
    return dict(id='current_mixed',title='Chimie mixte · outils et lipides',archive=False,
        level='MX2 validé · couplage matériel sans membrane',
        summary='Un même pool de sites fabrique les composants génétiques/fonctionnels et les vrais lipides H/T.',
        question='Voir la concurrence des substrats, les F refaits depuis nourriture, leur activité et les L qui s’associent.',
        prepared='4 G01 et1 F01 construits,4 F monomères, précurseurs P/R,24 H et24 T.198 billes. Aucun lipide ni contour préparé.',
        observe='À2400, graines0/1/2 : nouveaux G12/13/14, F14/12/15 et L24/23/23. F entièrement alimentaires11/9/11 ; L fabriqués par ces F1/0/3. Contribution variable conservée, sans choix de la meilleure graine.',
        conditions='Recette coopérative MX2 exacte ; Langevin masse1/frottement0,1, T0,08, dt0,002 ; boîte12×9 et cycle externe200/15. Sources et états initiaux validés par cohorte12 essais.',
        limits='Aucune membrane cellulaire dans ce sous-système. Association de L ne signifie pas insertion ni maintien. Stocks presque épuisés à2400, outils initiaux présents, pas de pertes, flux ouvert ou homéostasie. Gène court01, pas génome riche démontré.',
        look='Jouer en Maximum puis ralentir. Filtrer H/T ou les supports G/F dans Explorer. Les flashes marquent les vraies liaisons et les compteurs distinguent production H/T et activité des F refaits. Départ t0, aucun résultat précalculé.',
        evidence='research/BATCH_43.md')


def compact_origins():
    source='research/campaign_recipes/CB1_20261105T092857284853Z/manifest.json'
    data=json.loads((ROOT/source).read_text(encoding='utf-8'));items=[]
    for seed in range(3):
        task=next(t for t in data['tasks'] if t['label']==f'CB1_active_s{seed}')
        title=f'Graine {seed} · '+('une insertion, tenue tardive' if seed==1 else 'ouverture persistante')
        items.append((f'current_compact_s{seed}','current_compact',title,copy.deepcopy(task['scenario']),source,task['id'],302))
    return items


def compact_description():
    return dict(id='current_compact',title='Intégration compacte · défauts connus',archive=False,
        level='CB1 · montage le plus intégré, maintien non démontré',
        summary='Même bain productif : gènes, outils, précurseurs, vrais lipides fabriqués et frontière construite.',
        question='Voir le transfert matériel jusqu’à la frontière, et pourquoi les échanges peuvent laisser une ouverture durable.',
        prepared='52 molécules L en anneau,4 G01 et1 F01 préparés,4 F monomères, précurseurs P/R et24 H/24 T.302 billes, boîte22×22. Pas de perte ou de flux ouvert.',
        observe='À2400, graines0/1/2 : nouveaux G3/10/4, F4/9/1,L24/23/23. Un L né dedans et produit par un F entièrement reconstruit est inséré en graine1. Fermeture tardive0 /94,17 /0 %. Les deux échecs persistent et restent visibles.',
        conditions='Recettes CB1 exactes ; Langevin masse1/frottement0,1,T0,08,dt0,002 ; short_length0,92 et cycle externe200/15. Graine0 par convention pour le raccourci, sans sélectionner la réussite.',
        limits='Porte de cohorte refusée : fermeture et insertion insuffisantes sur deux graines. Zéro traversée liée observée ne garantit pas étanchéité pendant les périodes non classables. Stocks finis, outils initiaux présents, aucun maintien sous pertes, recyclage, alimentation ouverte ou homéostasie.',
        look='Jouer en Maximum. Graine1 pour le transfert jusqu’à une insertion ; graines0/2 pour suivre la première ouverture. Explorer permet filtre H/T, suivi des molécules et inspection des flashes. Simulation depuis t0, pas une vidéo sélectionnée.',
        evidence='research/BATCH_45.md')


def energy_origins():
    source='research/campaign_recipes/EG1_20261105T131525540618Z/manifest.json'
    data=json.loads((ROOT/source).read_text(encoding='utf-8'));items=[]
    for seed in range(3):
        task=next(t for t in data['tasks'] if t['label']==f'EG1_energy_s{seed}')
        title=f'Graine {seed} · '+('sans insertion observée' if seed==1 else 'insertion et tenue tardive')
        items.append((f'current_energy_s{seed}','current_energy',title,copy.deepcopy(task['scenario']),source,task['id'],302))
    return items


def energy_description():
    return dict(id='current_energy',title='Intégration compacte · échanges stabilisés',archive=False,
        level='EG1 · résultat limité, sensibilité numérique non résolue',
        summary='Même bain G/F/H/T et frontière construite, avec acceptation énergétique locale des échanges.',
        question='Des lipides réellement fabriqués peuvent-ils rejoindre la frontière sans emballement thermique ni ouverture persistante ?',
        prepared='52 L en anneau,4 G01 et1 F01 préparés,4 F monomères, nourriture P/R et24 H/24 T.302 billes, boîte22×22. Stocks finis, aucun apport ou perte.',
        observe='À2400, graines0/1/2 : nouveaux G9/2/8,F7/9/9,L23/23/24 ; L nés dedans insérés1/0/2. Fermeture tardive94,48/94,67/94,50 %, T0,0849/0,0826/0,0889 pour consigne0,08. La graine1 reste sans insertion. Échanges acceptés6/1/10, refusés16/7/15.',
        conditions='Recettes EG1 exactes ; Langevin masse1/frottement0,1,T0,08,dt0,002 ; largeur des ports0,6, cycle externe200/15. Un échange lit seulement son changement de potentiel local, jamais un contour ou une identité biologique.',
        limits='Porte limitée EG1 passée3/3, mais EN1 au pas divisé par deux refuse : insertion0/0/2 et une graine chaude/ouverte. Voir le menu contrôle au pas fin. Pas maintien sous pertes, alimentation ou homéostasie. Outils initiaux présents ; aucune insertion de L issu de F entièrement alimentaire dans EG1. Fermeture échantillonnée intermittente, zéro traversée liée observée ne garantit pas étanchéité continue. Bilan énergétique global non démontré.',
        look='Jouer en Maximum ; première insertion observée vers1108 en graine0. Ralentir ensuite, filtrer H/T et suivre un L. Graine0 par convention ; conserver la graine1 sans insertion et comparer aux défauts CB1 dans le menu. La simulation repart de t0, sans film précalculé.',
        evidence='research/BATCH_48.md')


def refinement_origins():
    source='research/campaign_recipes/EN1_20261105T170333609605Z/manifest.json'
    data=json.loads((ROOT/source).read_text(encoding='utf-8'));items=[]
    for seed in range(3):
        task=next(t for t in data['tasks'] if t['scenario']['seed']==seed)
        title=f'Graine {seed} · '+('chauffage et ouverture tardive' if seed==2 else 'tenue sans insertion')
        items.append((f'current_fine_s{seed}','current_fine',title,copy.deepcopy(task['scenario']),source,task['id'],302))
    return items


def refinement_description():
    return dict(id='current_fine',title='Intégration compacte · contrôle au pas fin',archive=False,
        level='EN1 · critères refusés, fragilité à comprendre',
        summary='Même chimie EG1, pas mécanique divisé par deux ; les échecs restent visibles.',
        question='Le couplage utile survit-il au raffinement mécanique, sans ralentir le bruit ou les réactions ?',
        prepared='Même montage EG1 :302 billes,52 L en anneau, gènes/outils courts préparés et nourriture finie. Aucun apport/perte ou nouvelle enzyme.',
        observe='À2400, graines0/1/2 : G7/6/8,F7/10/9,L23/22/23 ; L nés dedans insérés0/0/2. Fermeture tardive94,54/94,66/58,98 %, T0,0900/0,0878/0,1517. La graine2 chauffe tard ; première T>0,2 après t1000 à2173,5, avant son premier échange tardif2177,63.',
        conditions='Recettes EN1 exactes : dt0,001, reaction_every10, sample_every500 ; cadences physiques inchangées. Langevin masse1/frottement0,1,T0,08, mêmes taux et potentiels EG1. Les trajectoires de même graine divergent après initialisation.',
        limits='Porte refusée : fermeture/température de la graine2 et insertion dans deux graines insuffisantes. Trois essais ne départagent pas aléa et biais numérique. Aucun maintien ou robustesse démontrés ; ne pas sélectionner un dt parce que son résultat est favorable.',
        look='Graine2 pour voir la phase chaude après2100 et l’ouverture persistante ; graines0/1 pour la tenue sans insertion. Simulation depuis t0, pas trace sélectionnée. Comparer à EG1 ; cadence de lecture réglable sans changer le dt logique.',
        evidence='research/BATCH_48.md')


def build():
    variants=[]
    for key,demo,title,cfg,origin,task,beads in current_origins()+renewal_origins()+membrane_renewal_origins()+mixed_origins()+compact_origins()+energy_origins()+refinement_origins():
        cfg=resolve(cfg);path=f'demonstrators/configs/demo_{key}.json'
        (ROOT/path).write_text(json.dumps(cfg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        variants.append(dict(id=key,demo=demo,title=title,seed=cfg['seed'],config=path,beads=beads,
            source=origin,source_task=task,source_sha256=hashlib.sha256((ROOT/origin).read_bytes()).hexdigest(),
            dynamics_sha256=signature(cfg),view_speed=0.,motion='langevin'))
    for key,demo,title,cfg,origin,task,beads in origins():
        for inertial in (False,True):
            resolved=langevin_variant(cfg) if inertial else resolve(cfg)
            variant_key=key+'_langevin' if inertial else key
            path=f'demonstrators/configs/demo_{variant_key}.json'
            (ROOT/path).write_text(json.dumps(resolved,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
            variant=dict(id=variant_key,demo=demo,title=(f"Graine {resolved['seed']} · Langevin · candidat" if inertial else title+' · Brownien · référence'),
                seed=resolved['seed'],config=path,beads=beads,source=origin,source_task=task,
                source_sha256=hashlib.sha256((ROOT/origin).read_bytes()).hexdigest(),
                dynamics_sha256=signature(resolved),view_speed=0.,comparison_reference=key,
                motion='langevin' if inertial else 'brownian')
            if inertial:
                variant['presentation']=dict(
                    conditions=f"Variante expérimentale : Langevin, masse 1, frottement 0,1 ; température {resolved['chemistry']['temperature']:g}, dt {resolved['engine']['dt']:g}. Même matériel initial et mêmes lois chimiques que la référence. Le cycle externe éventuel est conservé.",
                    observe='Comparer avec le choix Brownien de la même graine : déplacement, durée des contacts, chaînes libérées, activité et membrane. Le résultat de la référence historique ne garantit pas celui de ce candidat.',
                    evidence='research/BATCH_23.md')
            variants.append(variant)
    from visualizer.demos import simulator_hashes
    archived=descriptions()
    for info in archived:info['archive']=True
    catalog=dict(version=1,date='2026-11-05',recommended='current_energy_s0',simulator_sha256=simulator_hashes(),
        policy='Live simulations from preserved initial inputs. Selected illustrative seeds, not a robustness claim. No trajectories/checkpoints bundled.',
        demos=[energy_description(),refinement_description(),compact_description(),membrane_renewal_description(),mixed_description()]+current_descriptions()+[renewal_description()]+archived,variants=variants)
    (ROOT/'demonstrators/catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def verify():
    from visualizer.demos import DemoCatalog
    from simulator.engine import Simulation
    catalog=DemoCatalog();rows=[]
    for key,_,_,original,source,task,beads in origins():
        variant,info,cfg=catalog.get(key)
        assert signature(cfg)==signature(original)
        assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==variant['source_sha256']
        sim=Simulation(cfg)
        assert len(sim.chemistry.pos)==beads==variant['beads']
        if key.startswith('integrated'):
            assert sim.chemistry.offset==486 and sim.chemistry.genetics.n==816
        elif key=='free_membrane':assert all(not edges for edges in sim.chemistry.edges)
        rows.append(dict(id=key,beads=beads,source_dynamics_identical=True,temperature=cfg['chemistry']['temperature']))
        _,info,inertial=catalog.get(key+'_langevin');other=Simulation(inertial)
        assert inertial['chemistry']==cfg['chemistry'] and inertial['engine']==cfg['engine']
        assert signature(inertial)!=signature(original)
        import numpy as np
        np.testing.assert_array_equal(sim.chemistry.pos,other.chemistry.pos)
        assert other.motion is not None and info['question']
        rows.append(dict(id=key+'_langevin',beads=beads,initial_positions_identical=True,
            chemical_laws_identical=True,temperature=inertial['chemistry']['temperature']))
    for key,_,_,original,source,task,beads in current_origins():
        variant,info,cfg=catalog.get(key)
        assert signature(cfg)==signature(original)
        assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==variant['source_sha256']
        sim=Simulation(cfg);m=sim.chemistry.membrane if cfg['model']=='coupled_bath' else sim.chemistry
        assert len(sim.chemistry.pos)==beads and m.config['bound_port_geometry']
        assert sim.motion is not None and not info['archive']
        if key.startswith('current_free'):assert m.edges==[set(),set()]
        if key.startswith('current_probes'):assert m.config['retained_probes']==m.config['permeable_probes']==24
        rows.append(dict(id=key,beads=beads,source_dynamics_identical=True,current=True))
    for key,_,_,original,source,task,beads in renewal_origins():
        variant,info,cfg=catalog.get(key)
        assert signature(cfg)==signature(original)
        assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==variant['source_sha256']
        sim=Simulation(cfg)
        assert len(sim.chemistry.pos)==beads==150 and not info['archive'] and sim.motion is not None
        assert cfg['chemistry']['sequence']=='01'
        rows.append(dict(id=key,beads=beads,source_dynamics_identical=True,current=True))
    for key,_,_,original,source,task,beads in membrane_renewal_origins():
        variant,info,cfg=catalog.get(key)
        assert signature(cfg)==signature(original)
        assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==variant['source_sha256']
        sim=Simulation(cfg);g=sim.chemistry.genetics
        assert len(sim.chemistry.pos)==beads==2118 and g.n==816
        assert cfg['chemistry']['genetics']['sequence']=='01'
        assert sim.motion is not None and not info['archive']
        rows.append(dict(id=key,beads=beads,source_dynamics_identical=True,current=True))
    for key,_,_,original,source,task,beads in mixed_origins():
        variant,info,cfg=catalog.get(key)
        assert signature(cfg)==signature(original)
        assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==variant['source_sha256']
        sim=Simulation(cfg)
        assert len(sim.chemistry.pos)==beads==198 and sim.motion is not None
        assert cfg['chemistry']['capture_cooperativity'] and not sim.chemistry.lipids.rungs
        rows.append(dict(id=key,beads=beads,source_dynamics_identical=True,current=True))
    for key,_,_,original,source,task,beads in compact_origins()+energy_origins()+refinement_origins():
        variant,info,cfg=catalog.get(key)
        assert signature(cfg)==signature(original)
        assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==variant['source_sha256']
        sim=Simulation(cfg)
        assert len(sim.chemistry.pos)==beads==302 and len(sim.chemistry.lipids.rungs)==52
        assert cfg['chemistry']['short_length']==.92 and sim.motion is not None
        if key.startswith('current_energy'):assert cfg['chemistry']['contact_exchange_gate']=='metropolis'
        if key.startswith('current_fine'):assert cfg['engine']['dt']==.001 and cfg['engine']['reaction_every']==10
        rows.append(dict(id=key,beads=beads,source_dynamics_identical=True,current=True))
    return rows


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['build','verify']);a=p.parse_args()
    if a.action=='build':build()
    else:print(json.dumps(verify()))
