# Lot13 — contrat explicite et banc de transport commun J0

27 octobre2026. Lot d'intégration. [Plan figé](BATCH_13_PLAN.md),
[contrat de conception](DESIGN_PRINCIPLES.md). Le bilan G1 est clos dans
[BATCH_12_RESULTS.md](BATCH_12_RESULTS.md). Les exigences ne sont pas nouvelles :
elles sont désormais explicites dans AGENTS.md et le skill pour les reprises.

## Mise en œuvre

`coupled_bath` compose les hooks existants dans un unique tableau de positions
et un unique `Simulation.advance`. Même bruit thermique0,08, mobilités par
particule0,4/0,25 et véritables réactions P–R/copie/expression. Les caches spatiaux
sont séparés par espèce de requête, pas les espaces physiques. Le paquet génétique
est placé près de la frontière ; sa boîte native ne reste pas une paroi cachée.

P/R libres traversent les interactions de L ; un lien réel P–R active le contact
répulsif0,55 et la barrière de segment existante. Les deux extrémités de L reçoivent
la réaction mécanique de cette force. Pas de force basée sur un contour, un gène
complet ou une origine alimentaire. Les observateurs conservent les vraies IDs,
la provenance et les incorporations ; ils ne convertissent aucun produit.

Coût : union de deux alphabets (six types élémentaires hérités), un contrat
croisé libre/lié à rayon0,55 et raideur80, aucun outil/gène supplémentaire.
Les classes mécaniques ne sont pas de nouveaux types biologiques. L'aide de
commutation peut changer l'énergie à la formation du lien ; le cycle génétique
externe et les précurseurs activés restent fournis. Aucune calibration énergétique.
Les réactions chimiques croisées sont absentes par contrat de types explicite.

## Vérification et pilotes sélectionnés

73 tests logiciels passent (72 en suite complète puis13 tests ciblés couvrant
le nouveau test de sorties matérielles), ainsi que7 historiques. Reprise exacte après une
formation P–R réelle, PRNG, observateur sans rétroaction, arbres/brut identiques,
matrices mécaniques et offsets, refus de températures séparées vérifiés.

Quatre pilotes graine0 : natif0,6 et froid0,08 jusqu'à60 ; bain et sans L jusqu'à20.
Tous finissent sans erreur, zéro dimère construit et zéro chaîne nouvelle ; le
bain20 n'a encore aucun contact avec la membrane. Ce n'est **ni** une preuve
d'inactivité ni une preuve de transport : horizons courts et accès non exposé.
Ne pas choisir une autre graine pour les faire réussir. Recettes/sources exactes
préservées ; données locales dans outputs/batch13/pilots.

## Suite et limites structurelles

Douze essais prévus : quatre conditions × trois graines, horizon400 fixé avant
résultats, deux travailleurs, checkpoints60s, pas de trajectoire dense. Témoins
thermiques puis bain sans/avec L ; tableaux automatiques des produits réellement
catalysés/incorporés et du transport. Les expositions de contact sont approximées
aux observations, pas une cinétique complète d'éligibilité catalytique.

J0 ne sait pas encore fabriquer H/T via un F : les réactions P/R et L restent
chimiquement disjointes, même si leurs forces se rencontrent. Ce verrou exige
une loi matérielle de fabrication, pas davantage de concentration. La géométrie
P–R0,45 diffère de H–T0,65 ; leur simple renommage ne serait pas un transfert.
Avant une bibliothèque, demander ensuite une seconde production par un autre
assemblage sous lois fixes, avec usage du produit et contrôles hors cible.

Budget du test :486 billes L +102 billes génétiques/précurseurs =588 ; sans L102.
Ce petit contenu ne remplace pas le budget cellulaire conditionnel C0B2406.
Aucune division, renouvellement durable, membrane synthétisée ni viabilité.
Maturité : banc commun vérifié, compatibilité chimique fonctionnelle encore à
mesurer. Santé : poursuite ciblée, effort global toujours non estimable.

## Lancement figé

Campagne `campaign_20261027T113835658766Z`, code55bcbf9, douze tâches à400,
deux travailleurs. [Recette source seule](campaign_recipes/J0_20261027T113835658766Z/manifest.json)
préservée. Les résultats sont en cours, pas encore un bilan de compatibilité.
Suivi `campaign_status.bat`, pause/reprise et analyse par les lanceurs existants.
Les paramètres ne seront pas modifiés d'après les premiers résultats.

Contrôle de fonctionnement en cours : checkpoint périodique du premier bain
(graine0) rechargé à143,5,588 billes dont102 P/R, vues partagées et288 observations.
Exposition observée approchée448 temps-atome libres,0 lié : premiers contacts
réels, pas encore une démonstration de rétention ou de transfert fonctionnel.
Ce point partiel n'est pas une sélection de succès et ne modifie aucun horizon.

## Statut au bilan technique suivant

Les12 essais sont maintenant terminés sans erreur à400 ; première lecture dans
[NUMERICS_AND_RENEWAL.md](NUMERICS_AND_RENEWAL.md). Contacts/passages libres
présents3/3 mais aucun F ou flux incorporé dans le bain commun à cette échéance.
Les témoins natifs produisent chacun un F, les témoins froids aucun. Ce constat
appelle un diagnostic d'accès/éligibilité/occupation, pas la déclaration d'une
impossibilité à froid. Audit détaillé du transfert et des périodes inconnues
encore à faire. Aucune nouvelle campagne lancée pendant ce bilan technique.
