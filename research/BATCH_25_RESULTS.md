# MD2 achevé — progrès membranaire, expression F non rétablie

15/15 essais terminés,0 erreur, aucun contrôleur actif. Les sources, scénarios,
hashes des résultats et du rapport figé sont vérifiés par
`experiments/review_coherent_contacts.py`. Les références LT2 sont réutilisées,
pas recalculées ou comptées comme nouvelles répétitions.

## J3 intégré, même Langevin, graines0/1/2 à1200

| Mesure | Ancien contact LT2 | Contact cohérent MD2 |
| --- | --- | --- |
| Fraction régulière fermée, grille0,5 | 2,6 /23,6 /74,2% | **85,5 /72,8 /86,9%** |
| Catalysés puis incorporés | 9 /7 /32 | 12 /15 /31 |
| Nouveaux G complets libérés | 0 /0 /1 | 0 /1 /1 |
| Nouveaux F complets libérés | 0 /1 /0 | **0 /0 /0** |
| Insertions L persistantes≥10 | 0 /0 /1 | 0 /1 /1 |

La fermeture est restaurée au-dessus du cas LT2 sur les trois graines, pas
parfaite. Les membranes finales0/2 sont fermées,1 ouverte. Tous les contacts
liés finaux sont géométriquement capturables ; moyenne q≈0,0052–0,0061.
Température cinétique tardive≈0,084–0,085 pour cible0,08, contre≈0,090–0,092
dans LT2. Pas de réduction du bruit, des taux ou de rescaling global.

Le contrôle fin sélectionné graine0 donne84,8% de fermeture contre85,5%,
18 composants incorporés contre12,0G/0F dans les deux cas, et2 insertions
persistantes contre0. Pas de convergence quantitative déduite d'une graine.

Les quatre essais MD2 intégrés, contrôle fin inclus, n'ont **aucun F nouveau
complet même encore apparié**, pas seulement aucune libération. Les outils F
préparés catalysent la matière ; leur propre renouvellement reste non démontré.
Les gains de membrane ne sont pas une preuve d'autopoïèse.

## Inventaire final F, mesure passive depuis les checkpoints

Sur les graines0/1/2 :16 chaînes F de longueur3 initialement préparées restent
présentes ;194/191/204 monomères F composites actifs et4/5/5 nouveaux fragments
F de longueur2. Contrôle fin0 :188 monomères,3 fragments,16 chaînes préparées.
Le recensement exclut les emplacements de précurseurs encore non assemblés.

Le stock **global** de monomères F ne s'est donc pas épuisé. Cela ne prouve
pas leur disponibilité locale sur les gènes. La priorité T9 doit distinguer
rencontres, captures autorisées, attente de ligation et impossibilité de
réutilisation des fragments, plutôt que supposer qu'un apport accru suffirait.
Le garde actuel G/F refuse la recapture d'un F déjà polymérisé ; son assouplissement
doit aussi être testé sur les outils complets pour éviter leur séquestration.

## Grandes membranes avec sondes, autre bain sans génétique

| Mesure, graines0/1/2 | Ancien contact | MD2 |
| --- | --- | --- |
| Fraction régulière fermée | 27,4 /5,7 /0,4% | 86,6 /15,7 /79,3% |
| Fraction de frontière classable | 41,4 /7,7 /1,0% | 99,2 /26,7 /97,2% |
| Insertions L persistantes≥10 | 2 /0 /0 | 1 /1 /2 |

Un défaut reste sévère sur graine1 : épisode non fermé de224 à1200. Un échange
accepté à223,61, écart de ports q≈0,590, précède cette ouverture. L'échange
autorise q<0,64 contre q<0,0625 pour la capture : cible concrète de prochaine
loupe, pas preuve que cet événement est la cause unique. Ce cas est conservé
dans la GUI, pas remplacé par un succès.

Les sorties de sondes retenues observées sous MD2 sont0/1/0 sur24 ; les entrées
de sondes perméables24/22/24 sur24. **Ce sont des observations pendant les
périodes classables**, sans garantie pendant les périodes inconnues. Aucun
zéro de fuite interprété comme étanchéité parfaite. Sondes et L libres sont
préparés, les L ne sont pas fabriqués par des outils dans cette scène.

## Petites membranes, résultat du lot25 confirmé

Depuis36 dimères isolés, fractions régulières avec un contour94,5/88,9/86,6%
anciennes contre97,5/98,1/94,0% MD2. Premières fermetures41/41/49 contre20/10/59 :
une métrique régresse dans une graine. Petits contours V8 et grande géométrie
J3 restent distincts, malgré la même forme de potentiel ; leurs réussites
ne s'additionnent pas en une preuve de chimie commune complète.

## Décision, santé et provenance

MD2 sous Langevin devient le candidat courant à examiner dans la GUI et la
base explicite des prochaines expériences. Les archives historiques gardent
leurs lois/signatures. Prochain verrou prioritaire : expression/finition F
et recapture locale sous contrôles d'interférence ; copie longue T9 reste liée.
La réparation/insertion membranaire demeure un verrou secondaire explicite,
avec un événement ciblable. Pas de nouvelle protéine sans proposition/accord.

Le progrès est net et des hypothèses réfutables existent ; la suffisance de
l'alphabet, la diversité fonctionnelle, la synthèse de L et le maintien avec
flux/homéostasie restent des problèmes de recherche. Pas de garantie qu'ils
se réduisent tous à des corrections techniques indépendantes, ni de délai
de cellule viable. Division toujours reportée.

Synthèse source-vérifiée et inventaire final :
`outputs/reviews/MD2_20261030T151902947518Z/summary.json`, driver et
`integrated_comparison.png`. Recette/data : BATCH_25.md/BATCH_25_RECIPES.json.
Les données brutes restent locales ; aucun nouvel essai long lancé pour cette lecture.
