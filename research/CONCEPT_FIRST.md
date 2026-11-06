# Méthode : dé-risquer la cible avant d'optimiser ses pièces

31 octobre2026, demande utilisateur. Source de suivi :
[cell_checklist.json](cell_checklist.json), [vue fine](CELL_CHECKLIST.md),
[tableau compact](CELL_CHECKLIST_COMPACT.md). Ce registre complète le graphe
chimique CELL_ARCHITECTURE et les tests I0–I9 ; il ne les remplace pas.

## Décider du prochain lot

Reprise lot55 après [revue Astra](ASTRA_REVIEW.md) : consulter d'abord
[CURRENT_STATUS](../CURRENT_STATUS.md), puis les points nécessaires du registre.
Les bilans de lots restent historiques ; une recommandation d'audit n'est ni
une loi adoptée ni une nouvelle obligation de campagne.

Avant une exploration coûteuse, vérifier les contraintes de symétrie, valence
et matière : des précurseurs indiscernables pour une règle ne deviennent pas
sélectivement reconnaissables par un balayage de séquences. Identifier ce que
le prédicat peut réellement distinguer. Un contre-exemple analytique peut
éliminer une branche ; annoncer son domaine, sans généraliser à tout le réseau.

Relier chaque critère au besoin fonctionnel. Conserver les portes prospectives
mais distinguer refus fonctionnel, proxy inadéquat et exposition insuffisante.
Cycle de liaisons, barrière répulsive et rétention mesurée ne sont pas identiques ;
réemploi d'un monomère et recyclage jusqu'aux précurseurs ne sont pas identiques.
Un calcul sur géométrie figée ne prouve pas le confinement dynamique.

Le maintien équipé/redondant et le redémarrage depuis zéro outil ont des
critères distincts. Ne pas ajouter ce dernier à la cible construite ; ne pas
utiliser la redondance pour masquer l'absence de remplacement. L'expressivité
par plusieurs assemblages reste un jalon séparé à dé-risquer tôt, sans supposer
trois enzymes nécessaires au plus petit réseau ni considérer `01` comme une
preuve de bibliothèque programmable. Une construction indépendante nécessaire,
comme la source/absorption, peut avancer pendant ce choix conceptuel.

Avant un lot, parcourir le registre entier et ses dépendances. Donner priorité
à un sous-but nécessaire dont le mécanisme n'est pas même qualitativement fermé,
surtout s'il pourrait invalider l'architecture. Un réglage quantitatif devient
prioritaire si sa mesure peut départager ces mécanismes ou s'il bloque le
transfert d'une fonction déjà établie. Aucun devoir de laisser toutes les
preuves isolées attendre la conception totale : un petit contre-exemple peut
être le moyen le moins coûteux de lever une incertitude conceptuelle.

Pour chaque point critique, il faut décrire ou reconnaître l'absence de :

- chaîne d'événements locale, intrants et produits réellement utilisables ;
- conditions de libération/retour, énergie, pertes et déchets ;
- dépendances pour produire puis renouveler tous les outils, y compris ceux
  de régulation/recyclage, sans les injecter silencieusement ;
- interaction indésirable qui pourrait casser la fonction ou sa coexistence ;
- test court qui distinguerait cette piste de son contre-exemple.

Une famille de mécanismes n'est pas une solution particulière trouvée. « Faire
un inhibiteur », « ajouter une protéase », « limiter le stock » ne ferme pas
un point sans préciser sa réalisation et ses conséquences. Dire clairement
**trou conceptuel**, **esquisse incomplète**, ou **draft décrit**, sans présenter
ces drafts comme des fonctionnalités validées. Déclarer les nouveaux coûts
d'alphabet, ports, taux, aides, énergie, gènes et renouvellement avant adoption.

Séparer identité de séquence et capacité fonctionnelle dans les critères : la
perte d'une chaîne F cible ne démontre pas l'extinction de tous ses motifs actifs.
Un fragment peut conserver une fonction locale. Inversement, la présence d'un
motif ou des cycles catalysés ne prouve ni information intacte ni flux utile.
Définir avant campagne quel inventaire/activité répond au sous-but ; conserver
les portes initiales après refus et documenter un éventuel proxy inadéquat.
FS1/lot49 illustre cette distinction sans requalifier RP1 en réussite.

## Deux axes de suivi

**Concept** :

- `none` : pas de draft local défendable ; manque à traiter en premier.
- `gap` : famille plausible mais maillon essentiel encore indéterminé.
- `draft` : mécanisme qualitatif et test falsifiant décrits ; paramètres et
  réalisation peuvent rester à trouver. Cela ne constitue pas une preuve.

**Preuve**, avec une échelle ordinale affichée en pourcentages :

| Palier | Affichage | Signification |
| --- | ---: | --- |
| `none` | 0% | Pas de résultat dynamique pertinent pour ce sous-but |
| `subcase` | 25% | Un sous-cas ou un prototype partiel étayé, portée déclarée |
| `separate` | 50% | Comportement étudié séparément sous les lois du candidat annoncé |
| `coupled` | 75% | Couplage utile observé dans un bain commun sur un domaine limité |
| `target` | 100% | Critère propre au point satisfait sur le domaine annoncé, avec preuves |

Ce ne sont **ni** des fractions d'effort accompli, **ni** des probabilités de
réussite, **ni** une mesure continue précise. Un25% peut reposer sur une ancienne
chimie ; la portée et les limites sont obligatoires. Un75% n'établit pas maintien,
robustesse ou fonctionnement de tous les gènes. Le tableau de groupe affiche
min–max et les trous conceptuels ; aucune moyenne ne peut compenser une voie
indispensable absente. Pas de pourcentage global de cellule.

100% pour un outil logiciel ne signifie rien sur100% de viabilité. Les buts
biologiques demandent des horizons et perturbations annoncés, des stocks utiles
et flux de remplacement mesurés. Pas d'immortalité exigée, pas d'extinction
impossible promise. Une preuve au domaine fini ne garantit pas tous les futurs
assemblages. La déclaration de maintien intégré exige tous les points nécessaires,
pas seulement un chemin formellement fermé.

## Faire évoluer la checklist

Chaque entrée contient son objectif et critère d'aboutissement, draft/gap,
dépendances fonctionnelles et de renouvellement, preuve référencée, portée et
prochain test. Les dépendances de renouvellement **peuvent former des cycles** :
ne pas prétendre qu'un ordre topologique de tâches les résout. Elles désignent
les capacités requises à terme, pas forcément nécessaires à l'amorçage construit.

Ajouter un ID stable lorsqu'un problème mérite une décision/test indépendant.
Lors d'une scission, conserver l'ancien ID dans `retired`, avec raison et
remplaçants. Conserver échecs et références historiques ; changer un palier
requiert une preuve et une justification, y compris pour une régression. Réviser
la date et le numéro du registre ; garder la raison dans son historique. Les
changements de périmètre ne sont pas un progrès scientifique automatique.

```powershell
python experiments/cell_readiness.py status
python experiments/cell_readiness.py build
python experiments/cell_readiness.py check
```

Avant remise de main : actualiser les points affectés, ajouter les nouveaux
sous-buts, régénérer les deux vues et vérifier les liens. Donner le tableau
compact (ou ses lignes modifiées avec lien au tableau complet), les régressions,
le trou conceptuel prioritaire et le prochain jalon. Mettre aussi à jour arbre,
journal, priorités et santé ; garder les résultats volumineux locaux.

Inclure une colonne « Progrès du dernier lot » : `last_batch_progress` associe
les IDs affectés à un changement concret, une preuve ou un essai encore en cours.
Réinitialiser ces notes à chaque lot ; l'historique des révisions et les bilans
conservent les anciens deltas. Une implémentation, un contrôle idéal et une
campagne lancée doivent rester distingués d'un transfert dynamique obtenu.

Les mesures globales de concentration, nombre de gènes/protéines, activité,
longueur ou stocks ne peuvent jamais devenir des commandes du simulateur.
Le registre et ses paliers sont de l'observation/planification seulement.

## Amorçage et remplacement matériel

Un départ sans enzyme est un test d'amorçage, plus fort que le départ construit
autorisé. Son échec ne suffit pas à rejeter le maintien d'une cellule déjà
équipée. Réciproquement, la persistance d'un outil préparé ou l'expression depuis
des monomères fournis ne prouve pas sa reconstruction depuis la nourriture.
Compter un remplaçant entier dont tous les constituants composites sont
réellement nouveaux, puis une opération fonctionnelle après sa construction
et libération. Distinguer renouvellement ponctuel, sous pertes et maintien
intégré ; conserver témoins déliés et sans gène, même s'ils réussissent à amorcer.
