# Lot14 GKA — diagnostic de la cinétique génétique froide

27 octobre2026. Lot d'intégration par diagnostic d'un blocage aval. Pas de
nouvelle loi ni nouveau helper. J0 à400 exprime un F natif3/3, froid0/3 et
bain commun0/3 ; les trajectoires froides ont néanmoins des appariements.
Les fonctions menacées sont expression et construction dans le bain commun.

Hypothèses : H1 rares rencontres admissibles à faible diffusion ; H2 sites
occupés trop longtemps ou fragments qui empêchent une finition ; H3 géométrie
de ligation rarement admissible ; H4 nombreuses occasions mais réaction absente.
Les comptes finaux ne les départagent pas. Un diagnostic doit séparer ces cas
avant ajout de mécanisme. Si le génétique échoue déjà en petite boîte froide,
ne pas accuser la membrane ni ajuster son docking.

## Phase A, comparaisons sans modification chimique

Ajouter un observateur pré-réaction au hook génétique, avec ses propres voisins
spatiaux et zéro appel PRNG. Mesurer rencontres de reconnaisseurs, exclusions
de capture, occupations G–F/G–G, motifs de ligation à quatre dimères et raisons
de rejet, captures de précurseurs et occasions catalytiques. Expositions
approximatives au début du tick ; l'ordre réel peut casser/créer des occasions
à l'intérieur du tick, donc ce ne sont pas des risques exacts. Mesurer aussi
les changements nets de paires et leurs épisodes aux ticks, pas une durée de
liaison exacte si une rupture/reformation survient dans le même tick.

Rejouer les six témoins natif/froid de J0, graines0/1/2, même horizon400, sources
figées. Comparer toutes les métriques primaires, positions finales, PRNG et état
chimique aux six originaux. Le coût ajouté est uniquement logiciel/mesure.
Le caractère non intrusif doit être vérifié avant campagne, ainsi que reprise
exacte et géométries positives/négatives. Les nouvelles mesures ne sont pas une
réévaluation rétroactive de la cinétique dans les anciens fichiers.

## Phase B conditionnelle

Si la rareté des occasions ou la diffusion reste plausible, prolonger **les trois
graines froides**, mêmes lois à3200 (8×400, face au ratio de diffusion0,6/0,08=7,5).
Cette échelle n'est pas une équivalence thermique : forces/bruit et cycle200/15
ne se redimensionnent pas ensemble. Garder le bilan censuré à400 et rapporter
séparément le suivi3200, sans sélectionner une graine favorable. Si le diagnostic
établit un piège structurel distinct, le documenter avant choix d'une variante.

Horizon de décision : phase A puis une seule prolongation ou un seul changement
conceptuel motivé. Ne pas faire une bibliothèque de réglages thermiques. Les
changements numériques dt/2/dt4 restent une obligation avant robustesse générale,
mais ne pas mélanger leur effet à la question H1–H4 dans cette comparaison.

Critère de progrès : diagnostic réfutable ou transfert matériel, pas nombre de
simulations. Conserver membrane, alphabet et références historiques. Aucun gène,
espèce, alimentation ni budget ajouté ; G/F et L chimiquement disjoints dans J0.

Décision après phase A : ne pas lancer ce suivi3200 maintenant. Voir
BATCH_14_RESULTS.md : tester un outil initial construit et son contrôle délié,
sous lois inchangées, répond plus directement à la cible cellulaire autorisée.
Le cycle200/15 est corrigé ici d'après la recette figée ; l'ancien texte60/10
était une erreur documentaire, sans effet sur les calculs.
