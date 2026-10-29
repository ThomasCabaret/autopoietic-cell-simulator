# Lot 20 — MIX1, dispersion et mélange sans chimie

29 octobre 2026, demande utilisateur pendant P10. Un mouvement visuel local
peut masquer un temps de mélange très long. Séparer le remplissage de l'espace,
la perte de mémoire spatiale des identités et le renouvellement des contacts.
Suivre la méthode de recherche et les contrats DESIGN_PRINCIPLES.md,
LOCALITY_AUDIT.md et KINETICS_AND_PERFORMANCE.md. Lot de diagnostic mécanique,
sans modification du candidat chimique, de son bruit ou de son intégrateur.

## Modèle mesuré

Utiliser `Simulation.advance` et les noyaux existants :
`dx=mu*F*dt+sqrt(2*mu*T*dt)*N(0,1)`, mu=0,25 par bille. Aucune vitesse
inertielle, convection ou conservation de quantité de mouvement. Les parois
existantes sont des **forces souples hors de la boîte**, pas un rebond exact.
Ne pas les appeler un tore ou des murs mathématiquement réfléchissants exacts.

Hook diagnostique `mixing` : 200 molécules fixes, dimères de deux billes avec
le ressort 180/longueur0,45 et la matrice de répulsion de G/F. Initialement leurs
centres occupent uniformément la moitié gauche de 24×18, séparation minimale0,6.
Aucune affinité, reconnaissance, réaction, liaison temporaire ou conversion.
Les liens internes sont préparés et ne changent jamais. Ce modèle ne prétend
pas reproduire le transport d'une protéine pliée ou les pièges d'appariement.

Le coût chimique ajouté est nul. Le hook n'est pas un nouvel univers candidat :
il isole une mécanique existante ; les contrôles retirant la répulsion sont
des variantes déclarées, pas une optimisation silencieuse de la cellule.

## Campagne bornée, un travailleur

Avant les longs calculs, pilotes froid/chaud de20 temps simulés, graine0.
Ensuite dix essais fixés :

1. Dimères avec répulsion, T=0,08, graines0/1/2, horizon12000.
2. Dimères avec répulsion, T=0,6, graines0/1/2, horizon1600.
3. Témoins sans répulsion, graine0, mêmes horizons froid/chaud.
4. Billes seules sans répulsion, T=0,08, graine0, horizon6000.
5. Témoin de cadence : dimères chauds avec répulsion, graine0, horizon400,
   observation des contacts0,025 au lieu de0,05. Même trajectoire physique,
   pas une nouvelle répétition indépendante ; comparaison au préfixe400.

dt=0,005, même intégrateur, observations brutes de contacts tous les0,05,
instantanés de statistiques tous les10, checkpoints30 secondes réelles.
Le témoin fin change uniquement la cadence de mesure. Une grille4×2 et les
rayons0,3/0,7/1,5 sont fixés avant les campagnes. Pas d'adaptation aux succès.
Sources/horizons/configurations figés ; pas de flux ni forçage de dispersion.

Concurrence bornée à un travailleur MIX1 pendant les deux travailleurs P10.
Dossier et pointeur séparés sous `outputs/mixing_campaigns` : les commandes
P10 ne doivent pas être détournées par ce diagnostic. Aucun essai P10 relancé
ou modifié. Le contrôleur des campagnes existantes assure lancement et reprise.

## Mesures

- Occupation de la moitié droite, histogramme spatial, variation totale à
  l'uniforme et premier mode cosinus de la concentration selon X.
- Déplacement quadratique moyen du centre et D apparent sur courts incréments
  loin des murs ; ne pas extrapoler ce D court en diffusion collective libre.
- Conservation des cinq voisins initiaux, avec référence de hasard5/(N-1).
- Information mutuelle entre les cases initiales et courantes, corrigée par
  32 permutations des identités. Générateur d'analyse indépendant, jamais le
  PRNG dynamique. Référence d'occupation obtenue par2048 tirages multinomiaux
  de200 points dans8 cases, sans force ni réinjection.
- Clusters géométriques par distance1,5 : nombre, plus grand et degré moyen.
  Ce sont des proximités spatiales, pas des agrégats chimiques liés.
- Aux trois rayons, partenaires uniques par molécule, fraction sans rencontre,
  contacts instantanés, temps-paire, épisodes échantillonnés et leur durée.
  Les sites mesurés sont les reconnaisseurs pour les dimères, les billes pour
  les monomères. Aucun test de symbole, orientation ou réaction n'est inclus.
- Quantifier la fraction de centres sortant légèrement des parois souples.

Les recroisements browniens rendent le nombre d'épisodes dépendant de la cadence.
Le témoin fin doit surtout vérifier partenaires uniques et temps de contact ;
ne pas traiter des épisodes corrélés comme des rencontres moléculaires nouvelles
ou des événements réactionnels indépendants. Durées quantifiées, événements
sous la cadence éventuellement manqués, épisodes actifs censurés à la fin.

Seuils descriptifs préfixés : occupation droite0,4–0,6 avec écart spatial sous
le95e percentile de bruit d'échantillonnage uniforme ; excès de voisins initiaux
<=0,1 ; MI corrigée normalisée<=0,1. Rapporter premiers passages échantillonnés,
pas une preuve d'équilibre durable. Garder les courbes et les absences censurées.

## Référence analytique et décisions

Sans interactions/murs, le centre d'un assemblage de b billes de même mobilité
a D=mu*T/b : les forces internes se compensent et les bruits indépendants
s'additionnent puis sont divisés par b. Pour un dimère froid D=0,01, chaud0,075.
Dans une boîte idéalement réfléchissante, le premier mode décroît comme
exp(-pi²*D*t/Lx²) : tau≈5836 froid,778 chaud pour Lx=24. Cette approximation
ne remplace pas les mesures sous répulsion et parois souples. La loi en taille
concerne ce thermostat implicite sans hydrodynamique, pas les molécules réelles.

Le risque aval est le coût de transport dans une cellule de largeur bien plus
grande et pour des polymères plus longs. Une lenteur de l'ordre de L²/D peut
exister même sans cage ; inversement des rencontres locales utiles peuvent
précéder l'homogénéité globale. Après ce lot, distinguer moteur lent, diffusion
physiquement lente, blocage de foule et éventuelle séquestration chimique absente
de ce modèle. Aucune correction automatique de T, mu ou ajout d'inertie/courant.
Concevoir une variante de mouvement seulement après cette interprétation.
