# Lot15 — bilan J1, stocks et contrôles de domaine J2

27 octobre2026. Lot d'intégration/diagnostic, pas nouvelle fonction. Au début
de la reprise,6 tâches J1 terminées et2 actives ; les12 se sont achevées pendant
le traitement. Aucun essai interrompu ni loi modifiée pendant la campagne.

J1 : résultats complets dans BATCH_14_BOOTSTRAP_RESULTS.md. Le nouveau census
post-hoc `experiments/inventory_audit.py` distingue matière libre, monomères,
polymères et formes structurellement compatibles avec la cible. Le rapporteur
vérifie hashes, durée, événements, vrais partenaires P–R et conservation des
102 billes avant interprétation. Analyse complète locale :
`outputs/campaigns/campaign_20261027T144451586423Z/inventory_analysis_20261027T161249026008Z`.
Son code et ses dépendances sont copiés et hashés avec les résultats locaux.

Le bain produit des dimères mais ne les incorpore pas ; le stock final contient
des monomères isolés plus éloignés du gène. Aucun fragment F délié non cible dans
les bains. Ce diagnostic privilégie un contrôle spatial avant T9 ou une hausse
de taux. Une photo finale ne prouve pas le mécanisme ni la stationnarité.

J2 ajoute seulement un réglage de boîte **globale** sans L pour des témoins
open/compact. Les lois de réaction et forces sont héritées inchangées. Le mode
par défaut reproduit exactement le hook J1 archivé sur positions/PRNG/chimie.
Tous les6 couples initiaux sont vérifiés : mêmes P/R et PRNG, translation seule
entre grand et petit monde ; concordance aussi avec le paquet membranaire J1.
Les murs compacts ne font jamais partie d'une cellule simulée.

86 tests logiciels et7 historiques passent. Le census est testé contre double
comptage d'un R, fragments appariés/déliés et confusion préparé/renouvelé. Les
tests d'environnement contrôlent le mode par défaut et refusent un override
compact avec membrane. Aucune homéostasie revendiquée ; HOMEOSTASIS.md rend
l'obligation explicite et est référencé par le contrat lu à chaque reprise.

Plan J2 :12 tâches à1200, mêmes lois/température/cycle200/15, stocks et trois
graines, deux travailleurs et checkpoints. Horizon de décision : cette cohorte,
puis densité/organisation ou diagnostic de L. Aucune nouvelle synthétase,
aucun changement du budget cellulaire conditionnel. Le maintien, la diversité
et la synthèse de L par F restent ouverts ; pas de délai biologique estimable.

## Lancement J2

Campagne `campaign_20261027T162612551317Z`, codeb0e104a,12 témoins à1200,
deux travailleurs, audit génétique et checkpoints60s. Recette source seule :
campaign_recipes/J2_20261027T162612551317Z. Résultats encore en cours, pas
de conclusion sur le contraste de domaine. Suivi campaign_status.bat et analyse
analyze_campaign.bat ; le census s'applique aussi à cette cohorte.

## Clôture

J2 terminé12/12 sans erreur. Vérification complète et résultats BATCH_15_RESULTS.md.
Le compact facilite les incorporations, mais aucun G/F nouveau complet ; le
grand domaine échoue fréquemment aussi sans L. J3 teste l'inventaire construit
près du budget cellulaire, avant toute nouvelle loi ou source de particules.
