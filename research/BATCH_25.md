# Lot25 — MD2, contacts liés et libres géométriquement cohérents

Suite autorisée après MD1. [Plan figé](BATCH_25_PLAN.md). Un seul nouveau
potentiel de contact, Langevin conservé, aucun nouvel outil fonctionnel.

## Changement de représentation locale

`bound_port_geometry=true` remplace, pour chaque contact explicite H/T, les
deux ressorts latéraux et quatre angles faibles par la continuation harmonique
du potentiel de ports libres au voisinage de q=0. Le même écart de deux ports
sur quatre billes est utilisé dans les deux états. Rungs internes inchangés.
Le coefficient dérive de dock_energy/dock_width² avec le facteur de coupure
existant ; aucune nouvelle raideur indépendante n'est ajustée.

La dérivée exacte inclut la rotation des ports avec leurs billes. Aucun contour,
taille ou rôle d'agrégat n'entre dans cette force. Coût : un choix explicite
de potentiel lié, zéro espèce/état/port/gène/outil/particule supplémentaire.
Moins de termes mécaniques de contact, pas une force superposée aux anciens
ressorts. L'option absente conserve les anciens scénarios résolus et leur loi.

La dissociation aléatoire, l'échange, les seuils de capture et les températures
sont conservés dans les essais de transfert. Les transitions chimiques peuvent
encore échanger de l'énergie hors q=0 ; pas de thermochimie équilibrée revendiquée.
Le seuil d'échange reste plus large que celui de capture : compatibilité et
échauffement doivent être lus, pas présumés par le seul raccordement mécanique.

## Vérifications et porte locale

Contrôles numériques : gradient de l'énergie, force résultante, couple,
raccordement des potentiels libres/liés, suppression des anciens termes,
absence de changement de schéma historique et reprise exacte du bain couplé.
Suite complète141 tests réussis, puis test supplémentaire de reprise exacte
réussi (142 tests logiciels distincts couverts) ;7 tests historiques réussis.
Le préfixe brownien P10 à50 garde exactement positions, état chimique et PRNG.
Les12 presets GUI conservent leurs signatures physiques, empreintes du moteur
actualisées et catalogue vérifié ; ils ne prétendent pas déjà utiliser MD2.

Six essais locaux : trois graines, ancien/nouveau contact initialement aligné,
T0,08,Langevin, puis coupure externe du seul lien à10 (heure fixée, pas issue
d'un score). La dissociation aléatoire est désactivée seulement dans ce banc
pour isoler la géométrie ; elle reste active en production/transfert.

| Graines0/1/2 | Ancien potentiel | Nouveau potentiel |
| --- | --- | --- |
| Fraction liée et capturable sur6–10 | 85,25 /100 /100% | 100 /100 /100% |
| Délai observé de recapture après coupure | 0,01 /0,03 /0,01 | 0,01 /0,03 /0,01 |

La porte préannoncée passe : toutes les nouvelles graines>=90%, liées avant
la coupure, et au moins2/3 recapturées avant12. Aucun échec des anciennes
références n'était exigé. Deux anciennes graines passent aussi parfaitement :
ce test démontre la compatibilité locale, pas une réparation statistiquement
établie de toutes les ouvertures rares de la grande membrane.

Le script applique lui-même la porte, prépare/exporte la recette et lance
le contrôleur existant seulement en cas de succès. Une garde ajoutée empêche
de relancer cette préparation pendant une campagne encore active. La source
exacte du premier passage, antérieure à cette garde, est conservée avec son
hash ; les nouvelles lois mécaniques sont déjà figées dans la cohorte.

## Transfert en cours,15 essais

Campagne `outputs/coherent_contacts_campaigns/campaign_20261030T115427443420Z`,
recette `research/campaign_recipes/MD2_20261030T115427443420Z`. Deux travailleurs,
checkpoints30s, aucune trajectoire globale dense. Le plan inclut :

- trois V8 nouvelles depuis molécules isolées et deux témoins V8 anciens ;
- trois paires ancien/nouveau de grande membrane avec sondes et molécules L
  libres internes, pour insertion et sélectivité des passages ;
- trois bains J3 nouveaux et un contrôle mécanique fin sur graine0.

Les références LT2 V8 ancienne graine0 et J3 ancien trois graines sont
réutilisées explicitement, sans nouvelles répétitions. Même potentiel dans
toutes les fonctions du candidat ; les géométries/températures V8/J3 restent
distinctes. Tailles : paire locale4 billes, V8 72, membranes avec sondes534,
bain intégré2118. Aucune dépendance causale ajoutée au budget cellulaire.

Les cinq essais V8 sont terminés, soit la comparaison à trois graines en
réutilisant explicitement le témoin LT2 graine0 :

| V8, graines0/1/2 à1000 | Ancien potentiel lié | Nouveau potentiel lié |
| --- | --- | --- |
| Fraction régulière avec≥1 contour | 94,5 /88,9 /86,6% | 97,5 /98,1 /94,0% |
| Première fermeture observée | 41 /41 /49 | 20 /10 /59 |
| Température moyenne dernier quart | 0,094 /0,110 /0,108 | 0,081 /0,080 /0,076 |

L'assemblage démarre bien depuis36 dimères isolés. À l'état final,100% des
contacts liés nouveaux sont géométriquement capturables, contre82,4/77,1%
pour les anciens témoins1/2 nouvellement calculés. Il s'agit d'une mesure
finale, pas d'une fraction de temps. La première fermeture régresse dans une
graine, les tailles/nombres finaux des vésicules diffèrent : ne pas prétendre
une domination de chaque indicateur. Le moindre échauffement tardif est un
résultat du candidat dans V8, pas une correction globale démontrée du thermostat.

Ce premier transfert sur trois graines est positif pour la continuité observée
et la cohérence des ports, sans preuve de grande membrane stable, insertion
ou maintien. Les six tests à sondes et quatre bains J3 restent à lire.

Suivi : `coherent_contacts_status.bat`, pause/reprise par
`stop_coherent_contacts.bat` et `resume_coherent_contacts.bat`. Le rapport
`demo_motion_analysis.json/md` est généré par sa source figée, progressivement
sur demande et automatiquement en fin de cohorte. Les états non classables
restent inconnus ; les statistiques finales des ports viennent des checkpoints,
sans rétroaction dans les forces ou les réactions. Aucun nouveau balayage après
le rapport final et aucune adoption automatique.

## Provenance, maturité et prochain choix

Porte locale : `outputs/coherent_contact_gate/gate_20261030T115427390878Z`,
avec rapport, chemins des six essais et source. Chaque essai conserve scénario,
moteur, positions initiales manuellement préparées, protocole de coupure, mesures
et driver. Recettes compactes et sources byte-à-byte : BATCH_25_RECIPES.json
et `research/abstract_runs/MD2_local_gate_20261030T115427390878Z`.
Les trajectoires/protocoles complets et rapports bruts restent locaux ignorés.

Maturité : motif local cohérent implémenté et premiers assemblages transférés,
pas encore correction intégrée validée. Le point de décision reste le transfert
insertion/rétention/grand bain, particulièrement les graines précédemment
dégradées. Si le nouveau contact rigidifie ou bloque croissance/échange, conserver
la régression et revoir le motif. Pas de réglage propre à chaque fonction.
Après lecture de la cohorte, décision mécanique puis reprise de T9 si le
transfert tient. Maintien, synthèse de L, diversité fonctionnelle et homéostasie
restent ouverts ; aucune nouvelle protéine sans proposition et accord utilisateur.
