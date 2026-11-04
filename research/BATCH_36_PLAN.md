# Lot36 — L1 : fabriquer un vrai H–T et lui donner les ports MD2

4 novembre2026. Travail indépendant de MIN1M : **exploration mécanistique et
levée d'un verrou logiciel**. La campagne MIN1M continue avec ses propres sources
figées. Son résultat n'est pas utilisé pour choisir les lois de ce prototype.

## Mécanisme et coût

Réutiliser l'assembleur F01 déjà construit. Les sites F0/F1 captent H/T libres
avec le même noyau, potentiels et taux du co-recrutement P/R. Deux sites voisins
liés et deux ligands proches forment un lien H–T saturé, libèrent les sites et
exposent les ports MD2. Pas de nouvelle protéine, gène, type matériel ou décision
sur contour/séquence. Motif de six billes maximum (deux F composites +H+T).

**Extension de lois distincte de MD2**, sans adoption par défaut : H/T deviennent
ligands donneur/accepteur ; leur occupation axiale active les ports et leur
contact lié. H–T ressort180/longueur0,65, force de ports MD2 réutilisée, cores
L/L0,4 et F/L liés0,55, F/H-T libres0. Les taux/rayons reprennent MD2 sans bonus
spécifique L : fond0,0001, catalyse20, rayon0,58 ; capture20/rayon0,25,
libération0,1, énergie2/largeur0,6, activation des sites liée au degré local.
Pas de budget énergétique thermodynamique calibré : même helper cinétique
explicite, plus activation des ports au lien. Aucun fuel ou déchet gratuit inventé.

Le pool contient seulement F préparés et H/T libres ; **P/R, gènes/expression,
frontière cellulaire et interactions croisées ne sont pas inclus**. L1 n'est
donc pas déjà un univers unifié. Le gène de l'outil existant reste requis à terme,
et sa reconstruction est testée séparément par MIN1R/MIN1M, pas par L1.

## Déverrouillage utile même si la catalyse échoue

Une table de vrais liens H–T remplace la supposition queue=n+tête. Vue compacte
pour les noyaux MD2, redistribution exacte des forces vers les IDs physiques.
Elle accepte naissance et partenaires arbitraires, conserve les contacts par ID
de tête, et réutilise association, dissociation et échange de ports sans lire
une composante biologique. Aucun atome déplacé ou renommé lors de la synthèse.
Le moteur/scheduler reste Simulation ; nouveau hook lipid_synthesis opt-in.

## Périmètre du lot et réfutation

Vérifier gradients, conservation de force, invariance par permutation des IDs,
équivalence avec les noyaux MD2, occupation/saturation, rupture/échange latéraux,
vrai partenaire arbitraire, libération et réutilisation sur contacts contrôlés,
reprise exacte, tree/brute et passivité de l'observation. Contacts préparés et
taux forcés des tests sont des **contrôles idéaux**, pas une émergence spontanée.

Faire un court pilote dispersé à paramètres annoncés, pour vérifier exécution
et mesurer si une campagne ultérieure est nécessaire. Pas de grille, pas de
nouvelle campagne longue tant que MIN1M occupe ses deux travailleurs. Aucune
hausse du palier de synthèse L sur la seule implémentation ou les tests idéaux.
Arrêt pour bilan après le prototype et les contrôles bornés.

Fonction aval menacée : vrai L utilisable par association/insertion. Une paire
H–T qui ne produit pas les mêmes forces MD2 invalide la voie. Après ce lot :
mesurer catalyse/libération en bain libre avec témoins no_tool/split/no_boost,
puis compétition P/R/H/T et transfert réel vers membrane préparée. Si H/T
empoisonne la pince commune, comparer alternatives avant retouche ; une nouvelle
machine sélective requerra toujours proposition et accord utilisateur.
