# GKA : mesurer avant de modifier le bain commun

27 octobre2026. [Plan](BATCH_14_PLAN.md). Le diagnostic historique J0 montre des
appariements à froid mais peu de ligations : maxima de sites appariés4/2/4 en
petite boîte froide, contre6/6/6 au chaud. Ce constat n'identifie pas la cause.

`simulator/genetic_audit.py` ajoute une mesure pré-réaction au hook génétique,
y compris dans le bain couplé. Voisinage privé, aucun PRNG, aucune modification
des forces, seuils, réactions ou séquences. Expositions intégrées par maintien
du dernier compte jusqu'au tick suivant, avec fenêtres25. Reconnaissance,
exclusions séquentielles, occupations, double appariement de motifs, ligation
géométriquement admissible, capture P/R et support catalytique sont distingués.
Les épisodes portent sur les paires nettes aux ticks ; une rupture/reformation
dans le même tick reste invisible. Aucun taux exact n'en est déduit.

Le worker sauvegarde l'état du diagnostic avec l'observateur et exporte
`genetic_audit.json`. Les tableaux de campagne l'affichent sans modifier les
anciens tableaux. Le mode est optionnel et figé dans le manifeste ; aucune
adaptation de loi à ces informations n'est permise.

Les tests ciblés vérifient reconnaissance positive, phase externe, orientation,
ligation et rejet géométrique, catalyse dépendant du vrai lien, absence de
rétroaction dans les deux hooks, reprise exacte et pause/reprise du worker.
La suite complète79 tests et les7 historiques passent avant gel ; les erreurs de fichiers temporaires
du premier passage sandbox sont des erreurs de permission, pas des régressions
chimiques. Relance hors sandbox réussie, mêmes tests et code.

Phase A : six rejeux source figés de J0 natif/froid400, trois graines chacun.
`experiments/analyze_batch14.py` vérifiera census/durées puis toutes les métriques,
positions, PRNG et état chimique contre les six témoins originaux. Le générateur
de plans lit leurs scénarios dans la recette versionnée, sans dépendre des données
brutes. Si celles-ci manquent, la comparaison exacte est marquée non vérifiée.

Coût : zéro élément, port, paramètre physique, outil ou gène supplémentaire.
Le coût logiciel et temporel de mesure ne doit pas être confondu avec une
capacité chimique nouvelle. Le génétique isolé reste102 billes, J0588 et le
budget cellulaire conditionnel2406. Une prolongation éventuelle de toutes les
graines froides à3200 répondra à une hypothèse, sans remplacer les censures400.

Maturité : aucune nouvelle fonction revendiquée. Le prochain gain attendu est
un diagnostic qui tranche une incompatibilité, puis le retour vers une fonction
transférée dans le bain commun. Production L et diversité sous lois fixes ouvertes.

## Clôture GKA et phase suivante

Six rejeux achevés et exacts jusque positions/PRNG/chimie ; résultats dans
BATCH_14_RESULTS.md. Sources physiques existantes toutes byte-identiques à J0,
seul le worker ajoute la mesure. Recette GKA_20261027T122747493430Z préservée.
Le cycle documentaire60/10 était erroné : recettes et calculs200/15, notes corrigées.

Suite J1, BATCH_14_BOOTSTRAP.md : outil construit et témoin géométrique délié,
aucune loi nouvelle. Le pilote200 produit3 dimères contre0, incorporation0/0.
Les douze essais1200 restent nécessaires pour tester le transfert et la membrane.
