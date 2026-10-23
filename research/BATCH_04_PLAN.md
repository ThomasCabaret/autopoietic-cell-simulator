# Lot 4 — intégration de la fonction dans les F composites

Objectif d'intégration, 23 octobre 2026, avant essais. Branche C2, parent C1,
reliée à E1. Le moteur reste Simulation et le hook reste `copy` : les unités
F ont exactement leurs deux billes support/reconnaissance et peuvent être
fabriquées par les réactions G→F existantes, sans conversion après synthèse.

## Candidat et modification

Transférer capture X/Y, ligation de bain uniforme et libération par occupation
du produit depuis C1 aux reconnaisseurs F. Leur occupation par un substrat
doit exclure simultanément l'appariement G ; cette concurrence est une
interférence à mesurer, pas à contourner par un changement global de mode.
X/Y restent deux types primitifs de ressources activées ; leur produit est
irréversible. Pas de bilan énergétique complet ni de monomère utile revendiqué.

Le repliement natif de F est décrit par un angle local entre deux liens du
squelette, dépendant du symbole central. L'alignement de traduction est conservé
quand les unités sont appariées. Les paramètres sont identiques pour toutes
les séquences ; aucun test de chaîne complète dans la dynamique.

Coût à suivre : deux espèces de substrats, un état d'occupation du reconnaisseur,
une paire de paramètres géométriques natifs et leur force, capture saturable,
perte d'affinité locale du produit. Les trois billes simples du prototype C1
ne sont plus une famille fonctionnelle distincte. Les helpers historiques de
copie, le cycle externe et les sous-unités préparées restent déclarés.

## Séquence de tests et critères

1. Vérifier conservation des billes, exclusion des occupations, réactions dans
   le bain sans chaîne, géométrie locale, égalité arbre/exhaustif et reprise.
2. Chaîne F composite préparée 001 ; contrôle 010 de même composition, trois
   unités F non reliées, absence de capture. Mesurer les ligations soutenues
   par deux sites de la même chaîne, produits distincts et rendement total.
3. Si l'opération répétée fonctionne, tenter G→F puis usage dans le même bain,
   sans outil préparé ni changement de loi. Certifier a posteriori que la chaîne
   exacte est issue de ligations soutenues par G et que plusieurs produits
   successifs sont soutenus par cette même chaîne libérée.
4. Référence copie G et traduction des séquences historiques sous les nouvelles
   règles, en distinguant un ancien rejeu d'une nouvelle compatibilité. Conserver
   régressions, non-testés et changements de paramètres entre candidats.

Le candidat est figé pendant chaque comparaison. Les recettes identifient les
paramètres et sources ; une correction ouvre un nouveau candidat explicite.
Plusieurs graines pour une réussite revendiquée ; les criblages et variantes
intermédiaires restent traçables. Le contrôle sans gène doit distinguer ligation
spontanée et activité d'une chaîne effectivement exprimée.

La membrane reste extérieure à ce candidat matériel : son intégration n'est
pas revendiquée. E3 (copie et expression simultanées) reste une autre priorité,
non résolue par ce seul transfert. Les données restent locales, seules les
recettes/sources et les synthèses entrent dans Git. Commits locaux, aucun push.
