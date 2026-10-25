# Lot 6 — premier composant constructible, 25 octobre 2026

Lot d'intégration matérielle et de simplification de représentation, branche
C3A sous C3. Le lot 5 conserve copie/expression/opération sur001 mais assigne
tous les dimères au départ. Ce lot teste une première obligation nécessaire,
pas encore une usine pilotée par un outil exprimé.

## Hypothèse figée A

Les supports primitifs P_G/P_F et reconnaisseurs R0/R1 sont des billes
persistantes. Une liaison P–R saturée se forme au contact, sans partenaire
préassigné. Le symbole d'un dimère est celui du R réellement lié ; sa famille
vient du support. Les sites incomplets ne capturent ni ne polymérisent. Après
formation, exactement les mêmes règles de copie/expression et ressorts que
les dimères préparés s'appliquent. Un G001 préparé est autorisé.

Nouveau coût : un état de liaison P–R dynamique, rayon et taux de formation ;
aucun nouveau type par rapport aux attributs primitifs déjà présents. Le lien
est irréversible et les ressources sont activées : énergie et recyclage restent
hors preuve. Les précurseurs sont spécialisés (P_G/P_F,R0/R1), pas X/Y génériques.
Leur production par un F exprimé est la prochaine intégration, pas un acquis.

## Campagne et références

- A : G001 + supports/R libres, zéro dimère libre initial ; trois graines.
  Exiger dimères formés puis incorporés dans une copie G exacte détachée.
- Contrôles : sans formation P–R ; sans ligation de squelette ; sans gène.
  Le premier doit bloquer le composant, le second conserver les dimères mais
  empêcher les chaînes, le dernier empêcher la copie dirigée.
- Transfert sous les mêmes lois : remplacer les supports G libres par F,
  sans changer les taux ni la géométrie ; expression exacte détachée.
- Perturbation : bain mixte G/F, mêmes lois ; ne pas agréger les essais séparés
  en preuve de coexistence. Six symboles seulement si le verrou court converge.
- Régressions : candidat E3C préparé et G001011 seul sous code refactorisé,
  comparer métriques et tableaux exacts aux références du lot5.

Observations hors dynamique : IDs des deux billes de chaque lien formé,
instant de formation avant ligation, séquence complète et détachement. Vérifier
conservation des positions/IDs/types, saturation et absence de future paire
imposée. Répéter arbre/exhaustif et reprise. Sources/paramètres figés par run ;
nouveau dossier pour toute variante ; conserver échecs et preuves locales.

## Décision

Une copie issue de vrais dimères construits réduit le risque de représentation,
sans prouver C3 complet, flux utile, maintenance ou fermeture. Si la réaction
P–R construit des dimères mais la copie échoue, diagnostiquer composition et
géométrie avant d'ajouter des helpers. Réévaluer santé, arbre, priorités et
maturité à la clôture ; commit local, aucun push.
