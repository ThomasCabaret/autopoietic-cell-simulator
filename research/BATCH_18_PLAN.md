# Lot18 — N1 en cours, exploration conditionnelle N1→N2

28 octobre2026. Lot technique au service de l'intégration : séparer la mécanique
de la cadence réaction si N1 dérive, avant retouche des fragments T9. Aucune
nouvelle loi chimique ; le contrôle de recherche reste extérieur aux trajectoires.
Lire AUTOMATED_EXPLORATION.md pour la séparation programmation/interprétation.

## État connu au choix du suivi

N1 : deux achevés, deux actifs, deux en attente, aucune erreur. Les deux achevés
àdt0,001 donnent277/335 actes,9/16 produits incorporés et G1/0,F0/2. Un F
exprimé effectue4 actes en graine1, sans produit utilisé observé. Ce sont des
résultats partiels, pas une cohorte valide pour la médiane prévue. N1 conserve
sources, horizons et seuils ; aucun arrêt ou ajustement de ses tâches.

## Petit arbre automatique borné

1. Attendre N1 achevé et ses travailleurs/contrôleur libérés. Une erreur, pause
   ou interruption demande attention ; aucun traitement d'une cohorte partielle.
2. Vérifier les sources/résultats, analyser et archiver le rapport N1. Reprendre
   les alertes de BATCH_17_PLAN.md : médiane catalyse/incorporation >30%, fermeture
   >0,10, enveloppe >0,05 entre niveaux successifs. Conserver toutes les graines.
3. Si au moins une alerte porte sur facteur2→facteur4, lancer **N2 entier**.
   Sinon s'arrêter pour interprétation et choix T9. Une alerte grossier→moyen
   seule ne déclenche pas N2. L'absence d'alerte ne certifie pas la convergence.
4. N2 terminé : analyser le tableau croisé et s'arrêter pour interprétation.
   Pas d'autre branche, nouveau seuil, nouvelle chimie ou répétition automatique.

Budget conditionnel : six tâches au plus, deux travailleurs, horizon1200,
checkpoints60s, mêmes graines0/1/2 ; simulations déjà terminées non rejouées.
Le suivi et ses sources sont figés avant lancement. Son état inclut la décision,
le chemin/hash du rapport et les tâches en attente/actives. Pas de source/sink,
de changement de concentration ou de cycle externe ajouté.

## Contrôle N2 et contrat numérique

Même bain2118 billes, chimie/état initial J3, dt0,0005, observation0,5.
Trois graines avec réaction tous10 pas (intervalle0,005), puis trois avec tous20
pas (0,01). Réutiliser N1 fin à5 pas (0,0025), N1 moyen dt0,001 à5 pas (0,005)
et J3 grossier dt0,002 à5 pas (0,01). Comparaisons :

| Effet examiné | Conditions |
|---|---|
| Mécanique à réaction0,01 fixe | J3 grossier / N2 fin20 |
| Mécanique à réaction0,005 fixe | N1 moyen / N2 fin10 |
| Réaction à dt0,0005 fixe | N2 fin20 / N2 fin10 / N1 fin5 |

Le moteur ajoute `engine.reaction_every`, entier positif, défaut5 exact à
l'ancien ordonnanceur. Les hooks existants interprètent leur second argument
comme un cinquième de l'intervalle de réaction ; un adaptateur leur fournit
intervalle/5, sans changer leur API ni leurs lois. Les forces/bruit utilisent
toujours le vrai dt mécanique. Le cas par défaut transmet directement dt pour
préserver l'arrondi et le PRNG. Aucune source ancienne ni campagne N1 modifiée.

Coût : zéro élément/port/état/gène/outil/taux chimique, une cadence numérique
indépendante. Sources changées uniquement config.py/engine.py, avec tests de
défaut exact, deux horloges et reprise entre ticks. L'analyse déclare cette
différence de sources ; elle ne prétend pas les archives byte-identiques.

L'analyse N2 compare stocks, G/F, produits utilisés, provenance, contacts et
fractions de membrane régulières, pas seulement production brute. Trois graines
restent insuffisantes pour certifier la convergence des chaînes rares. Si la
cadence domine, revoir la résolution des rencontres ; si la mécanique domine,
revoir intégration/contacts. Une dérive faible n'établit ni homéostasie ni gènes
longs. Après ces deux contrôles numériques, pas de grille supplémentaire par
défaut : décision mécanistique ou T9, avec héritage explicite des régressions.
