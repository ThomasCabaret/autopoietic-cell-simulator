# Méthode : dé-risquer la cible avant d'optimiser ses pièces

31 octobre2026, demande utilisateur. Source de suivi :
[cell_checklist.json](cell_checklist.json), [vue fine](CELL_CHECKLIST.md),
[tableau compact](CELL_CHECKLIST_COMPACT.md). Ce registre complète le graphe
chimique CELL_ARCHITECTURE et les tests I0–I9 ; il ne les remplace pas.

## Décider du prochain lot

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

Les mesures globales de concentration, nombre de gènes/protéines, activité,
longueur ou stocks ne peuvent jamais devenir des commandes du simulateur.
Le registre et ses paliers sont de l'observation/planification seulement.
