# Lot 19 — P10 lancé, distribution des chaînes à dix symboles

29 octobre 2026. [Protocole](BATCH_19_PLAN.md). Hypothèse : une fidélité
d'appariement parfaite peut coexister avec une population dominée par les
fragments, sans amplification utile. Les séquences et longueurs sont désormais
recensées sans filtrer les produits non cibles.

## Pilotes terminés, pas un résultat d'amplification

Deux essais graine0 à50, copie et expression seules,820 billes. Sources figées
dans `campaign_recipes/P10pilot_20261029T115659494627Z` ; preuves locales dans
`outputs/population_pilots/campaign_20261029T115659494627Z`.

| Mesure à50 | Copie G seule | Expression F seule |
| --- | ---: | ---: |
| Temps réel, initialisation JIT comprise | 9,782s | 9,860s |
| Débit moyen | 1022 pas/s | 1014 pas/s |
| Monomères libres /400 | 391 | 389 |
| Nouveaux polymères, tous incomplets | 2 | 2 |
| Longueurs et séquences canoniques | 4:`0010`,5:`10101` | 4:`0010`,7:`0110101` |
| Copie exacte nouvelle observée | 0 | 0 |

La séquence initiale reste entière et séparée. Ces absences sont censurées à50,
avant la première phase de libération185–200. Aucun plateau, taux de mutation
ou impossibilité de longueur10 n'en est déduit. Les symboles sont strictement
appariés par les lois ; les liaisons de squelette ne se rompent pas.

Environ43–45% des supports touchent le cœur d'un autre composant à cette date :
ce n'est pas une preuve d'engorgement. Deux témoins de dilution sont ajoutés
prospectivement avant la campagne, en plus du stock/volume doublé prévu.

## Campagne longue en arrière-plan

Recette : `campaign_recipes/P10_20261029T120049792477Z`.
Données : `outputs/campaigns/campaign_20261029T120049792477Z`.
Plan : `../campaigns/polymer_population.json`, dix tâches, deux travailleurs,
horizon3200 pour toutes les tâches. Le début de la trajectoire principale0
retrouve exactement les six recensements du pilote jusqu'à50 malgré son horizon
plus long ; les pilotes ne sont pas additionnés à la cohorte.

- `population_status.bat` : progression et dernier recensement sauvegardé.
- `stop_campaign.bat` : pause propre avec checkpoint, puis attendre les travailleurs.
- `resume_campaign.bat` : reprise explicite après pause/redémarrage.
- `python scripts/population_report.py` : rapport progressif dans le dossier
  courant ; génération automatique également à la fin de la campagne.

Rapports : `population_analysis.md/json` ; chaque essai conserve `population.json`,
les audits, résultats et checkpoints. Sources, configurations et recettes seules
sont versionnées. Ordinateur actif nécessaire ; pas de notification ni relance
au démarrage présumée. L'estimation initiale de l'ordre d'une heure reste
provisoire, particulièrement pour les témoins deux fois plus grands.

## Vérifications et limites

Observateur passif : bilan de matière exhaustif, projection des longueurs depuis
les séquences, distinction du matériel initial et des nouveaux produits,
identité des positions/état chimique/PRNG avec et sans audit et reprise exacte.
Le contrôleur de campagne existant est réutilisé ; aucune nouvelle horloge de
simulation. Les empreintes du catalogue GUI sont révisées explicitement pour
l'instrumentation optionnelle ; les six scénarios gardent leur signature physique.

Ne pas assimiler une chaîne F de dix symboles à une enzyme conçue et validée.
Les deux modes sont des bains distincts de T7, sans membrane ni synthèse P/R ;
une réussite ne se transfère pas automatiquement au candidat froid intégré.
Le bilan scientifique final et la décision T9 restent à faire sur la cohorte.

## Lecture intermédiaire au jalon800 — cohorte incomplète

Les deux premières graines G ont dépassé800 au moment de la préparation du
commit. Les instantanés de cette date, tous deux après quatre cycles, donnent :

| Graine | G exacts nouveaux | Fragments courts nouveaux | Monomères encore libres |
| --- | ---: | ---: | ---: |
| 0 | 1 | 27 | 308/400 |
| 1 | 1 | 24 | 324/400 |

Les nouveaux exacts sont entièrement détachés à cet instant. Les fragments
observés sont des sous-séquences de la cible, aucune chaîne plus longue ou
séquence différente à longueur10 sur ces deux instantanés. Le brin préparé
reste distinct. Cela établit une population non réduite aux exacts alors que
77–81% des monomères sont encore libres ; pas une distribution finale ou une
preuve de saturation à une copie. Les données ultérieures restent conservées,
y compris si la réserve finit par être immobilisée. L'amplification éventuelle
des fragments par templating est une explication à examiner, pas une causalité
quantifiée par ce tableau.

Validation :115 tests logiciels et7 contrôles historiques passent. Le premier
lancement de la suite complète a été bloqué sur les dossiers temporaires du
bac à sable Windows ; la suite complète relancée avec les droits nécessaires
passe. Les16 tests ciblés population/campagnes/catalogue passent également.
Les six signatures physiques de démos sont conservées et vérifiées.
