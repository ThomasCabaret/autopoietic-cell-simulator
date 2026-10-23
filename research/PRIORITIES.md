# Priorités — après le lot 3, 23 octobre 2026

Critère : une chimie commune pour membrane, copie, expression, fonctions des chaînes,
production des composants et remplacement des outils. Cellule préparée et énergie
externe déclarée autorisées. Les fonctions abstraites de C0 restent des obligations,
pas des réactions biologiques à coder comme primitives.

## Règle de conduite pour les prochains lots

La méthode [Exploration, unification et simplification](../.agents/skills/local-chemistry-research/SKILL.md)
s'applique aux priorités ci-dessous. C1 et E3 sont des tests de convergence :
transférer une fonction aux vrais F exprimables et faire coexister copie et
expression. Définir le candidat commun et ses expériences de référence avant
de le modifier ; suivre régressions et coût des helpers, puis tenter les
simplifications pertinentes. Toute nouvelle exploration séparée doit préciser
l'obstacle qu'elle résout et son test de transfert. Les réussites déjà obtenues
restent des preuves de leurs modèles respectifs, sans compatibilité commune
présumée. Cette précision méthodologique n'ajoute aucun résultat expérimental.

## Décisions du lot

À la demande de l'utilisateur, l'assemblage membranaire depuis des molécules
isolées devient prioritaire par rapport au simple repliement du ruban préparé.
V8 obtient des contours finaux sur trois graines au point retenu ; le démonstrateur
est remplacé. Les échecs et ablations sont conservés dans [BATCH_03.md](BATCH_03.md).
L'attraction et la rupture thermique ne sont pas nécessaires à toute fermeture.

En parallèle, C1 démontre préorganisation, ligation et libération répétées dans
un prototype distinct. Les contrôles montrent un effet sur la co-capture, mais
un gain total variable. Cette étape ne résout pas l'activité des F exprimés.
Le plan d'avant essais reste dans [BATCH_03_PLAN.md](BATCH_03_PLAN.md) et les
décisions antérieures sont conservées dans le journal et les bilans précédents.

1. **P0 — C1 : transférer l'opération aux F composites exprimables.** Réutiliser
   le véritable alphabet G/F et sa connectivité, plutôt qu'une troisième famille
   incompatible. D'abord chaîne composite préparée, puis exprimée depuis G.
   Garder réaction de bain identique, permutation de même composition, sites
   séparés et absence de capture. Mesurer produits, renouvellement et rendement ;
   refuser les gains dus à une règle de séquence entière ou à un comptage favorable.
2. **P0 — E3 : coexistence copie/expression.** Tester deux faces locales de
   recrutement, avec G et F complets libérés dans le même essai sur plusieurs
   graines. Aucun changement global de mode copie/traduction. E3 demeure non testée.
3. **P1 — M0 : frontière réellement fonctionnelle.** Mettre des solutés tests
   près des contours V8 et mesurer rétention et passage selon une table locale
   fixe. Distinguer fuites entre billes, rupture des liens et passage autorisé.
   Les étiquettes intérieur/extérieur appartiennent uniquement à l'analyse.
4. **P1 — nourriture→composants et outils.** Après transfert de C1, construire
   une sous-unité utilisable avec matière et carburant déclarés ; viser ensuite
   le remplacement d'un outil. Ne pas prendre le produit XY du prototype pour
   un monomère fonctionnel déjà fabriqué.
5. **P1 — T9 : fragments parasites et générations.** Comparer coiffes et
   renouvellement local sans critère dynamique de longueur cible ; mesurer
   plusieurs générations complètes, pas seulement davantage de ligations.
6. **P2 — V9/V7 : minimalité et robustesse.** V9 : élargir les graines et varier
   séparément attraction, courbure, densité et rupture ; suivre les ouvertures à
   meilleure résolution. V7 sur V6 reste ouverte ; le contrôle thermique de V8
   ne démontre pas la sortie de pièges sur V6.

Toutes les nouvelles dynamiques utilisent le moteur commun. Code, lois, recettes
et notes sont versionnés ; données complètes locales ignorées. Les sources des
anciennes recettes restent figées. Commits locaux autorisés ; aucun push.
