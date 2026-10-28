# N1 achevé — raffinement temporel, 28 octobre2026

Six nouveaux essais terminés sans erreur à1200, avec réutilisation déclarée
de trois J3. Sources/scénarios, temps, provenance des P/R, bilans et checkpoints
contrôlés par `experiments/analyze_numerical_campaign.py` ; rapport local :
`outputs/campaigns/campaign_20261028T073131539788Z/numerical_analysis_20261028T162258944076Z`.
Tous les modules des archives N1 et J3 sont byte-identiques. Les modifications
ultérieures de cadence du lot18 ne changent pas leurs calculs ou recettes.

| dt / réaction | Catalysés0/1/2 | Incorporés0/1/2 | G nouveaux | F nouveaux |
|---|---|---|---|---|
|0,002 /0,01, J3 réutilisé|331/401/313|18/18/26|1/1/0|0/1/1|
|0,001 /0,005|277/335/345|9/16/22|1/0/2|0/2/0|
|0,0005 /0,0025|335/337/312|11/12/24|0/0/0|1/1/1|

La médiane de catalyse par outil initial vaut20,6875/20,9375/20,9375 ;
incorporation par gène1,125/1/0,75. Entre résolutions successives, aucune
variation ne franchit30%. La baisse **cumulée** d'incorporation est toutefois
33,3% entre extrêmes ; elle ne prouve ni biais systématique ni stabilité.
Médianes de fermeture0,7863/0,7993/0,8255, enveloppe0,9779/0,9771/0,9838 :
aucune alerte médiane préannoncée. Le déclenchement N2 automatique n'a donc pas
lieu. Ne pas modifier son seuil après résultats pour lancer la branche souhaitée.

Au pas le plus fin, F complet3/3 mais aucun G nouveau3/3. F exprimés :3/2/0
opérations, dont1/0/0 produits utilisés. Le transfert utile reste donc possible
au pas fin. Trois graines ne certifient pas la convergence de ces événements
rares et les trajectoires de même graine ne sont pas des chemins browniens communs.

La graine fine1 a une frontière dégradée : fermeture0,426, enveloppe0,703,
contre0,825/0,827 et0,984/0,984 pour fines0/2. L'alerte de médiane ne la voit
pas ; les lignes par graine la conservent et l'analyse humaine la relève. Une
robustesse de frontière n'est pas démontrée. Cet événement peut dépendre des
trajectoires et du schéma, sans attribution causale sur une seule réalisation.

Décision : pas de forte dérive médiane signalée, pas de certificat numérique.
Le contrôle N2 reste disponible mais non lancé ; aucune nouvelle grille par
défaut. Examiner T9 par ses règles et contrôles de fragments/outils complets,
en conservant le risque de frontière et les limites numériques au bilan.
