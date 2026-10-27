# Lot13 J0 — premier bain commun de transport matériel

27 octobre2026. Lot d'intégration, pas un nouveau réglage de docking.
G1 insère1/2/2 dimères à1500 mais ferme0,840/0,841/0,759 ; arrêter ici les
réglages de membrane isolée. Le défaut résiduel reste une limite, non une réussite.

## Question et contre-exemple précoce

Les vrais P/R libres de C3B1 peuvent-ils traverser une frontière dont les mêmes
atomes, liés en dimères G/F, ressentent une répulsion locale ? Leurs réactions
peuvent-elles continuer dans le même bain physique ? Le prochain processus
menacé est l'alimentation de la copie/expression, pas encore la fabrication de L.
La politique est décrite dans DESIGN_PRINCIPLES.md.

Composer les hooks CopyChemistry et MembraneBathChemistry dans **un seul**
Simulation.advance, un tableau de positions et un bain thermique. Aucun passage
de produit par conversion externe. Les deux alphabets restent distincts :
cohabitation matérielle ne démontre ni alphabet minimal ni synthèse de L par F.
Conserver les réactions historiques internes ; ajouter seulement les contacts
membrane–P/R et la barrière de segment existante sur les atomes localement liés.
Pas de réaction chimique croisée encore : ce contrat zéro-affinité est explicite.

## Candidat figé J0

- Température commune0,08. C3B1 utilisait0,6 : c'est une variante, pas un transfert
  acquis. Mobilités élémentaires conservées0,4 pour L et0,25 pour P/R.
- Configuration génétique C3Bexpress : G001 préparé, six monomères F préparés,
  précurseurs P/R réellement indépendants ; cycle60/10 et activation fournis.
- Frontière219 L préparés,24 L libres, lois G1 inchangées ; aucune sonde artificielle.
- Répulsion de billes membrane–P/R libres nulle ; rayon0,55 quand l'atome a un lien
  P–R. Barrière de segment à trois atomes de mêmes rayon/raideur0,55/80. Pas de
  test de composant entier, de longueur ni de position intérieure dans les lois.
- Cette commutation locale peut injecter de l'énergie à la formation du lien :
  aide physique déclarée, aucun équilibre thermodynamique revendiqué.
- Placer le paquet initial à7 unités de la frontière pour exposer les interactions.
  Le petit rectangle génétique d'origine sert uniquement à construire le paquet ;
  aucune paroi interne cachée après placement. Boîte globale90×90 pour tous.

## Contrôles et critères

Contrôle sans membrane : mêmes lois et même paquet, L absents initialement.
Contrôle thermique C3B1 ancien et basse température en boîte native pour séparer
la perte de confinement du changement de température. Pilotes techniques courts
avant campagne ; ne pas appeler leur absence de réaction un échec cinétique.

Campagne J0 : quatre conditions (natif, froid, sans L, avec L) sur graines0/1/2,
horizon400 fixé avant résultats, soit12 essais. Observer flux de dimères catalysés et incorporés, copie/expression,
contacts réels avec la frontière, passage par état local et adsorption. Un zéro
sans contact est censuré/informatif sur l'accès, pas une perméabilité démontrée.
Mesurer les états pendant les périodes de contour valide seulement et rapporter
l'inconnu ; ne pas transformer une étiquette dedans en force.

Critère : obtenir contacts effectivement exposés et produits matériels utilisables,
pas simplement deux modules exécutés. Les faibles comptes ou l'absence de
renouvellement à400 ne prouvent pas l'impossibilité. Si l'activité isolée à0,08
disparaît ou si la géométrie de confinement échoue, traiter ce verrou avant une
grande campagne. Aucune bibliothèque fonctionnelle, division ni viabilité promise.

À titre de calibration historique (autres dt/trajectoires, pas prévision), les
C3Bexpress1200 avaient leurs premiers F libérés à385,5/185,5/385,5 et premiers
actes catalysés à387,275/198,05/400,15. L'horizon400 est donc un **criblage précoce**,
pas un test de maintien ni un délai suffisant garanti. Rapporter les zéros
censurés et l'exposition ; geler séparément toute prolongation, sélectionnée ou
systématique, sans fusionner les horizons dans une estimation favorable.

Coût : table croisée contact libre/lié, deux constantes0,55/80 et réutilisation de la barrière, zéro type
élémentaire ajouté aux deux alphabets réunis, zéro outil/gène. Six types chimiques
hérités (H/T et P_G/P_F/R0/R1), classes mécaniques agrégées distinctes des espèces.
Si J0 échoue, moteur, sources/recettes et mécanismes séparés restent réutilisables ;
les mêmes réussites chimiques ne sont pas garanties. Réévaluer après ce lot,
sans empiler des tables par fonction.
