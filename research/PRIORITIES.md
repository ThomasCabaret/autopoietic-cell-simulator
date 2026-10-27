# Priorités — lot14,27 octobre2026

GKA : diagnostiquer la reconnaissance et la ligation à froid avant tout réglage.
Six témoins J0 natif/froid rejoués à400, instrumentation sans rétroaction,
comparaison exacte aux originaux. Plan BATCH_14_PLAN.md : distinguer occasions
rares, occupations, géométrie et attente réactive ; suivi froid3200 de toutes les
graines seulement si le diagnostic le justifie. Aucun nouveau helper chimique.

## Priorités du lot13, historique

G1 achevé et analysé : insertion1/2/2, fermeture0,840/0,841/0,759 ; critère
conjoint2/3, aucune dominance sur B. Voir BATCH_12_RESULTS.md. **Arrêter les
réglages isolés de membrane** et tester J0 : vrais P/R libres/liés, température
commune, contacts et produits incorporés, témoins natif/froid et sans frontière.
Le plan BATCH_13_PLAN.md fixe quatre conditions × trois graines à400.

Ensuite décider si le verrou est thermique, dilution/concentration, transport ou
construction. La fabrication de L par F et une seconde fonction sous lois fixes
restent les prochains tests d'expressivité ; J0 ne les implémente pas. Longueur,
multigène et remplacement durable ouverts. Lire DESIGN_PRINCIPLES.md avant
toute nouvelle loi : pas de nouveau garde par défaut ni de loi par fonction.

Mise à jour du bilan technique : J0 terminé12/12 à400, premiers F natifs3/3
contre0/3 à froid ; bain commun sans F ni incorporation. Voir NUMERICS_AND_RENEWAL.
Avant retouche ou prolongation : analyser les contacts/occupations et l'éligibilité
du génétique à froid pour distinguer temps d'attente et pièges. Programmer ensuite
la convergence en dt des mécanismes retenus ; elle n'est pas encore démontrée.

## Priorités avant analyse du lot12, historique

Trace M1G terminée et garde géométrique rejeté. Comparer maintenant G1, condition
symétrique sur deux occupations de ports, sur0/1/2 à1500 aux témoins M1R conservés.
Pilote court sans activité, occasions admissibles non nulles : aucun succès à
déclarer. Conserver activité d'insertion **et** confinement ; zéro insertion
est une régression même si les défauts disparaissent. Une seule variante figée,
puis décision de mécanisme, avant intégration matérielle G/F.

## Priorités après lot11, historique

M1R achevé6/6 et références B exactes. Les ruptures spontanées des témoins sont
brèves ; B0 présente un défaut prolongé entre une substitution et son inversion.
Voir [résultats](BATCH_11_RESULTS.md).

**Prochain test M1G :** tracer les participants/ports d'une substitution réussie
et d'une défectueuse, puis restreindre un motif strictement local seulement si
la trace le justifie. Garder fixation des lois, réversibilité, fonctions utiles,
mesures d'exposition et critères conjoints. L'intégration matérielle G/F reste
ensuite ; pas d'insertase gratuite ni de balayage de constantes sans diagnostic.

## Priorités après lot10, historique

Campagne K1 achevée6/6, [résultats](BATCH_10_RESULTS.md). Insertion B observée3/3
à1500 ; fermeture/rétention conjointes incomplètes. B simple perd2–4/24 sondes et
n'insère que1/3. Conserver la barrière de lien comme référence, sans prétendre
qu'elle suffit au maintien global.

1. **Robustesse membrane :** même horizon sans échange pour isoler ses effets,
   mesurer ouvertures/périodes inconnues, puis accès et refermeture. Demander
   insertion et confinement conjoints ; ne pas multiplier les helpers.
2. **Intégration matérielle :** transférer membrane et vrais précurseurs G/F vers
   des lois communes, tester cohabitation, états libre/lié et effets parasites,
   puis copie/expression confinées. Construction L et diversité I0/T9 ouvertes.

Pas de prochaine campagne lancée pendant ce débriefing. Optimisation CPU si le
coût d'intégration le justifie ; aucun besoin démontré de portage GPU immédiat.

## Priorités avant analyse du lot10, historique

Le [lot9](BATCH_09.md) réduit le risque de grande frontière : rétention sélective
sur sondes3/3 à150 sans barrière de lien, fuite1/24 à450 sur un suivi ; deux
insertions par échange local sur une seule graine. Membrane et G/F restent séparés.

**Prochain lot technique K1 :** campagne figée, état consultable, arrêt/reprise
et analyse cinétique des rencontres, éligibilité, premières transitions et essais
censurés. Puis M1B sur horizons comparables et transfert sans barrière de lien.
Profiler avant optimisation CPU, sans modifier les lois ; GPU après preuve de coût.
I0/alphabet commun et T9/multigène suivent. L'ancien plan est conservé ci-dessous
comme contexte du lot8, et non comme état des preuves du lot9.

## Plan avant le lot9

Le [lot8](BATCH_08.md) franchit C3B pour une fonction : F exprimé→composant
incorporé3/3, copie G entièrement issue de ses produits2/3, renouvellement de
F complets1/3. Conserver cette référence commune ; le passage à XYZ/isomères
est une option de conception, pas une obligation imposée par l'utilisateur.

**Prochain lot : M1/I2–I4**, pour réduire le risque aval de grande frontière,
échange/insertion depuis l'intérieur et fuites. Un départ membranaire construit
est permis. Ensuite comparer les alphabets réutilisables et I0, puis T9/I1.
Ne pas multiplier des variantes de capture après ce transfert fonctionnel.

Le [graphe intégré](CELL_ARCHITECTURE.md) et les [contrats](CELL_INTERACTIONS.md)
encadrent désormais les choix. Cible conditionnelle :3 gènes/3 outils,16 espèces
cibles, budget nominal2 406 billes. Ce ne sont pas des capacités moléculaires
validées. V8 préfère des anneaux trop petits pour ce contenu ; l'insertion dans
un anneau saturé et la perméabilité selon l'état lié/libre sont à démontrer.

Suivre la méthode [exploration, unification, simplification et santé](../.agents/skills/local-chemistry-research/SKILL.md).
Le [lot 6](BATCH_06.md) construit de vrais dimères puis les incorpore dans G/F.
Copie seule et expression seule passent3/3, coexistence courte2/3 ; aucun outil
n'a encore produit ces dimères. La référence active E3C du lot5 reste conservée.

1. **P0 — I0/choix d'alphabet et diversité utile.** Le transfert C3B est obtenu
   pour un assembleur polyvalent de vrais P/R. Comparer la réutilisation des
   quatre précurseurs à la variante XYZ et ses états de produit distincts,
   en comptant les ports, outils et gènes nécessaires pour fabriquer L aussi.
   Tester plusieurs fonctions transférables et les interactions étrangères,
   sans imposer artificiellement des monomères isomasses. Ne pas additionner
   des réussites de modèles distincts ni simplement renommer XY.
   Le même alphabet doit permettre plusieurs outils ; commencer les contrôles
   d'espèces étrangères avant d'élargir leurs fonctions. EN/EA/EL sont des rôles
   visés par la forme des chaînes, jamais des types ni une table de séquences.
   Le noyau P_G/P_F/R0/R1 ne constitue pas encore une chimie commune avec L ;
   déclarer cet écart matériel et tester la fabrication/compatibilité membranaire.
2. **P0 — T9/E3, longueur et fragments.** Au prochain test génétique, diagnostiquer
   les stocks piégés et comparer finition/recyclage local des fragments à la
   croissance de chaînes complètes. Contrôles sans renouvellement et stabilité
   des gènes/outils ; aucun critère dynamique de longueur cible. L'association
   prolongée seule échoue. Garder le couplage court comme référence, sans prétendre
   que 001 résout la capacité d'information riche.
3. **P0 — M1/I2–I4, frontière dimensionnée, insertion et flux.** Tester une grande
   frontière préparée à faible courbure avant l'intégration : nominal rayon34,4,
   environ219 L, contre rayon préféré1,53 pour V8curved. Mesurer échange local,
   arrivée de L depuis dedans, refermeture et fuite. Rétention et passage sous interactions
   locales dépendant de l'état de liaison, puis compatibilité avec le noyau commun. Les
   indices intérieur/extérieur restent analytiques. Ne pas exiger la formation
   spontanée de toute la cellule, dont l'initialisation construite est autorisée.
   Ne pas résoudre le blocage par un outil d'insertion gratuit : compter gI/EI
   et leur reconstruction si une insertase devient nécessaire.
4. **P1 — utilité et diversité.** Obtenir un flux de composant utile, comparé
   avec/sans outil, puis plusieurs productions par assemblages différents sous
   les mêmes lois. Les opérations XY et le comptage de co-capture ne prouvent
   pas ce bénéfice. Prévoir remplacement sous pertes et matière/fuel déclarés.
5. **P2 — minimalité et robustesse.** Étendre les graines seulement quand elles
   répondent à une question ; ablater les aides et mesurer le coût réactif avant
   une grande campagne. Ne pas ajouter une règle spécifique par fonction.

## Références à préserver ou à marquer comme régression

- C3B1 G001+six monomères F préparés, aucune chaîne F : F libérés1/3/1,
  composants par F certifiés34/40/24, incorporés3/13/7 ; G complets1/2/0 et
  F complets0/2/0 entièrement issus des produits certifiés. t1200, trois graines.
- Outil préparé C3B1 :22/24/23 dimères et G3/3/5. Sans capture ou sans taux
  accéléré, aucun produit dans la graine0. Délier l'outil initial n'est pas un
  contrôle sans enzyme permanent : la graine2 réexprime un F et se réactive.

- C3A P/R libres : G001 seuls3/5/2, F001 seuls4/4/4 libérés ; mêmes lois.
  Mixte G2/0/2 et F1/1/1, deux graines avec coexistence simultanée. Sans
  assemblage ou sans ligation : aucune chaîne nouvelle ; sans gène : aucune.
- C3A001011 G seuls48, graine0 : une copie. Deux bains mixtes longs n'ont aucun
  G/F complet ; expression longue pas encore retrouvée dans cette variante.
  Les paramètres/initialisations diffèrent du bain alimentaire préparé : pas
  d'attribution causale à la seule constructibilité.

- E3C 001, 24 G + 24 F + X/Y, t=800, graines 0/1/2 : G 3/2/2, F 3/2/3,
  coexistence détachée 3/3, maximum d'opérations par outil 2/3/2.
- C2D expression→opération, F seuls, graine 0 : deux F, trois opérations par
  outil. E3C retrouve exactement toutes ses métriques et tableaux.
- G seuls 001011, 48 G à t=800, graine 0 : une copie sous coopération ; point
  perdu avec deux faces. Ne pas cacher cette régression par un changement de graine.
- Sans gène, coopération et deux faces : aucune chaîne fabriquée ni opération
  certifiée ; conserver les produits spontanés comme tels.
- 001011 dans le bain mixte : aucune coexistence démontrée, même si la coopération
  exprime un F par essai. Ne pas agréger cette réussite et une copie d'un autre run.

L'[évaluation de santé](PROJECT_HEALTH.md) fixe l'horizon E3, C3, M0. E3 et C3A
sont partiellement franchis ; M1 est le prochain point de décision aval, sans
prétendre C3 entièrement clos ni la membrane compatible avec cette boucle.
Si les interventions cessent de réduire les risques, revoir le candidat et le
budget plutôt que multiplier les démonstrateurs. Données locales, commits locaux,
aucun push. Les échecs et trois erreurs d'étiquette restent dans les recettes.

## État après livraison technique K1

Contrôleur/mesures livrés et testés ; utiliser le plan B/Bsimple sur horizons égaux,
puis analyser les occasions de réaction, la fermeture, la persistance et la fuite.
La livraison technique n'autorise pas à déclarer M1B robuste. Les décisions I0/T9
et le transfert vers une chimie commune restent les suites scientifiques.

## Mise en œuvre du prochain test M1R

Le lot11 prépare B et sans échange au même horizon1500, avec diagnostic des
ouvertures et contrôle source-exact. Analyser ces six résultats avant tout
réglage chimique. Ensuite intégration de vrais précurseurs/composants G/F sous
lois communes ; si le diagnostic reste indécidable, mesurer directement les
fuites des périodes inconnues, plutôt que déclarer leur rétention.
