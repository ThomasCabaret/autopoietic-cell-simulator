# Lot11 — diagnostic des ouvertures et contrôle sans échange

26 octobre2026. [Plan figé](BATCH_11_PLAN.md), configuration
`campaigns/membrane_robustness.json`. Livraison de mesures et préparation d'une
nouvelle campagne ; aucune loi chimique ni capacité intégrée nouvelle.

## Préparation vérifiée

Un observateur séparé identifie fragmentation, grand écart terminal, aire faible,
croisement et ouverture classable. Il rapporte les épisodes, extrémités et leur
proximité sans créer un contour ni classer les sondes dans les périodes inconnues.
Les anciens critères et métriques restent inchangés. Le checkpoint conserve les
compteurs et épisodes ; le suivi peut afficher l'état analytique courant.

63 tests logiciels et7 historiques passent, plus vérification ciblée du rapport
lisible. Nouveaux tests : deux arcs aux extrémités proches restent inconnus,
grand arc non refermé artificiellement, distinction durées/épisodes échantillonnés,
absence de rétroaction et reprise exacte avec audit. Aucun type, port, paramètre
physique ou aide chimique ajouté ; coût d'analyse seulement.

## Pilote source-exact

`outputs/batch11/pilots/campaign_20261026T164551801107Z/` retrouve exactement les
positions, PRNG, état chimique et toutes métriques du B0 à150 du lot9
(`M1exchange_s0_20261025T225915563115Z`). Les sources de référence sont vérifiées
avant comparaison.301 observations, dont260 fermées,38 ouvertes classables,
2 à grand écart terminal et1 fragmentée.35 transitions fermées→non fermées sont
observées alors qu'aucun échange n'a encore eu lieu. Des ouvertures préexistent
donc aux premiers échanges dans ce pilote ; cela n'explique pas à lui seul la
dégradation tardive de B0. Le census et les temps d'état sont recoupés par le
postprocesseur, sans nouvelle simulation.

Il manque toujours les contrôles longs. Le nouvel audit ne mesure pas les
transitions sous0,5 unité ; une suite d'images fermées ne prouve pas une fermeture
continue. Des bouts proches ne prouvent pas l'étanchéité. Les périodes inconnues
restent explicitement inconnues ; aucun gain de rétention n'est créé par l'analyse.

## Campagne et décision attendue

Six tâches à1500 : B et absence d'échange, trois graines chacune, deux travailleurs,
checkpoints60s, sans trajectoire dense. Les B sont rejoués pour obtenir des mesures
absentes des anciennes sorties, avec comparaison automatique aux résultats K1
lorsque leurs données locales sont disponibles. Les lois restent celles de B ;
la valeur0 est l'ablation déclarée du taux d'échange0,2.

Le postprocesseur `experiments/analyze_batch11.py` vérifie le census avec les
historiques, les sources, les durées et les références locales B. Ses nouvelles
sorties d'analyse conservent aussi son code et son hash. Recettes versionnables,
données et checkpoints locaux. Aucun remplacement des anciennes archives.

À l'issue : isoler robustesse spontanée et effet de l'échange, puis décider entre
travail sur les contacts, chemin local de refermeture ou mesure directe des fuites
pendant les périodes inconnues. Pas d'insertase ajoutée avant ce diagnostic.
L'intégration matérielle G/F reste l'étape suivante ; membrane, vrais aliments et
déchets non réunis. Budget de ce bain534 billes, cible C0B2406 toujours conditionnelle.
La maturité chimique reste celle du lot10 tant que les six nouveaux essais ne
sont pas analysés. Aucun nouveau blocage de principe ni délai fiable annoncé.

## Lancement effectif

`campaign_20261026T165544113247Z`, sources du commit0850065, six essais à1500,
deux travailleurs. Démarrage vérifié sans erreur : deux tâches actives, quatre
en attente, progression effective et contrôleur vivant. Les résultats restent
à analyser ; la mise en route ne constitue pas un résultat chimique.

[Recette de campagne](campaign_recipes/M1R_20261026T165544113247Z/manifest.json),
[recette du pilote](campaign_recipes/M1Rpilot_20261026T164551801107Z/manifest.json).
Sorties locales sous outputs/campaigns/campaign_20261026T165544113247Z/.
Les lanceurs status/stop/resume/analyze restent ceux documentés dans campaigns/.
