# J1 — cellule construite, outil initial et vrai renouvellement à distinguer

27 octobre2026. Décision après les six diagnostics exacts GKA, voir
BATCH_14_RESULTS.md. Tester un départ déjà outillé est autorisé par l'objectif ;
l'expression depuis six monomères seuls est un test d'amorçage plus exigeant.
Les chaînes nouvelles et le renouvellement restent requis en aval.

Lois strictement J0, température0,08, cycle200/15, stocks et six dimères F
initiaux001011 inchangés. Un F001 lié plus trois monomères011, ou le même groupe
001 délié plus011. Positions initiales, PRNG, vrais rungs et symboles identiques
dans chacune des six paires de contrôles (trois graines × avec/sans membrane).
Seuls les deux liens F27–28 et F28–29 diffèrent. Vérification par
`python experiments/prepare_batch14_bootstrap.py verify` avant tout calcul.

L'outil préparé est exclu des F nouveaux par l'observateur historique. Aucun
nouveau type primitif, motif chimique, port, taux, outil/gène ou énergie non
déclarée ; les aides anciennes persistent. Il y a un outil initial, mais il
réutilise le gène001 existant, pas un outil gratuit à ajouter au graphe cible.
Le trimer préparé n'est jamais présenté comme auto-assemblé ou traduit.

Pilotes sélectionnés graine0, froid isolé200 : outil lié3 dimères catalysés,
maximum3 opérations par outil préparé ; contrôle délié0. Aucune incorporation,
aucun G/F nouveau, aucune opération attribuée à un F exprimé. Ces deux essais
ne démontrent ni efficacité3/3 ni compatibilité membranaire. Recettes dans
BATCH_14_PILOTS.json ; données locales dans outputs/batch14/pilots.

Campagne figée : quatre conditions froid/préparé, froid/délié, bain/préparé,
bain/délié, trois graines0/1/2, horizon1200, deux travailleurs, checkpoints60s,
audit génétique actif, sans trajectoire dense. Le plan a été généré avant les
résultats pilotes. Le suivi froid3200 sans outil n'est pas lancé.

Critères : opérations répétées puis produit réellement incorporé ; compter
séparément produits du premier outil et de F nouvellement exprimés, G/F nouveaux
et leur origine. Le délié peut s'outiller par expression : le conserver comme
témoin initial délié, ne pas le rebaptiser contrôle sans enzyme permanent.
Mesurer contacts, passages, inconnus et état de membrane dans le bain. Une
fabrication abondante sans incorporation reste un échec de transfert.

Horizon de décision : ces12 tâches. Si l'outil fonctionne isolé mais pas dans le
bain, diagnostiquer dilution/adsorption/transport avant une autre loi ; si les
fragments dominent, T9 est prioritaire. Ni synthèse de L par F, ni bibliothèque
de fonctions, ni renouvellement durable ou division ne sont démontrés par J1.
Budget102/588 billes et cible C0B inchangés. Coût de conception : une comparaison
de conditions initiales, pas12 nouvelles lois. La suite doit réduire un verrou,
pas accumuler des aides. Pas de prévision de délai biologique sous dix heures.

## Lancement

Campagne `campaign_20261027T144451586423Z`, code39fead3, douze tâches à1200,
deux travailleurs, audit et checkpoints actifs. Recette source seule dans
campaign_recipes/J1_20261027T144451586423Z ; résultats non encore analysés.
Les79 tests logiciels+7 historiques passent ; les13 tests campagne/couplage
repassent après ajout de la distinction préparé/exprimé dans le tableau.
Suivi campaign_status.bat, pause/reprise et analyze_campaign.bat habituels.

## Clôture

Les12 essais sont terminés, sources/événements/inventaires vérifiés. Voir
[résultats complets](BATCH_14_BOOTSTRAP_RESULTS.md). Froid préparé : produits
incorporés3/3 ; témoin délié1 : F exprimé actif et un produit incorporé. Dans
les6 bains membranaires : aucune incorporation, frontière encore fragile.
J2 sépare maintenant domaine et présence de L, sans nouvelle réaction.
