# Lot35 — MIN1M : transfert du petit outil dans la membrane

4 novembre2026. **Intégration**, avant modification de lois. MIN1R a reconstruit
des F01 entiers puis actifs3/3, dans150 billes sans membrane. MIN1M teste si ce
couplage survit dans le même bain que L, aux concentrations et dimensions MD2.
La fabrication L et la régulation des polymères restent des drafts à risque ;
ce contre-test court réduit une incompatibilité aval avant de les implémenter.

## Candidat et comparaisons figés

Même alphabet P_G/P_F/R0/R1/H/T, mêmes ports, forces, taux et température MD2.
Langevin masse1/frottement0,1, T0,08, dt0,002, réaction0,01, observation0,5,
cycle externe200/15. Aucun nouvel outil, état, paramètre ou helper. La réaction
reste bornée à deux sites liés et leurs ligands, sans connaissance du gène,
du contour ou des origines mesurées. Le départ construit est autorisé.

12 essais : graines0/1/2 × active/noL/split/nogene, horizon1200 fixé. Active :
16 G01 et16 F01 préparés,64 F monomères0011, précurseurs libres ;432 supports G
et384 F comme MD2, soit1632 billes génétiques +486 L =2118. Anneau219 L et24
L libres internes, rayon34,5, boîte90×90, paquet32×24 centré. Pas de mur autour
du paquet. Les G préparés deviennent32 composites contre48 historiquement,
les F restent96. Les symboles et stocks exacts sont audités par le générateur.
Symboles G0/G1 =216/216 contre224/208 dans MD2, F0/F1 =192/192 inchangés.
La comparaison à MD2 n'isole donc pas uniquement la longueur de séquence.

Split délie les16 F01 ; nogene délie tous les G ; noL enlève les486 L en gardant
le paquet P/R et ses positions identiques. L est construit puis omis dans
noL pour conserver les tirages de placement. L'initialisation des vitesses
Langevin tire ensuite un tableau plus petit : vitesses et PRNG après préparation
diffèrent déjà pour noL. Aucune comparaison bit-exacte de sa trajectoire.
Split/nogene conservent exactement positions, symboles, atomes et
tirages de placement de active. Aucun témoin délié n'est un interdit permanent
d'amorçage. Les anciennes références MD2 et MIN1R sont réutilisées, pas relancées.

## Mesures, réfutation et budget

Compter tous les G/F nouveaux, F entiers dont chaque vrai composite naît depuis
P/R libre, puis activité après expression/libération et toutes ces naissances.
Exclure les16 F préparés. Pas de RV1 : l'analyse irréversible reste applicable.
Mesurer produits et incorporation par famille/origine, occasions génétiques,
temps de première activité (absence censurée1200), temps réel et fermeture
membranaire sur grille régulière0,5 plutôt que sur observations d'événements.
Rapporter insertions et passages observés, avec les limites des contours inconnus.

Crible prospectif : dans au moins2/3 active, F entièrement neuf actif ; dans au
moins2/3 active, fermeture parent≥70% du temps échantillonné ; ces deux propriétés
doivent coexister dans les mêmes≥2 graines. Nogene : aucun nouveau F ni F neuf
actif dans les trois graines. Split/noL sont diagnostics, sans seuil imposant
leur échec. Seuil70% = filtre de coexistence, pas critère d'étanchéité/viabilité.
Échec : interpréter capture, dilution, rétention ou membrane avant nouvelle grille.

Deux travailleurs,12 trajectoires maximum, checkpoints30s, plafond24h réel
du superviseur existant ; pause sauvegardée si dépassé. Sources/configurations
et collecteur figés avant départ. Analyse et décision automatiques à cohorte
complète ; **arrêt dans tous les cas**, aucune phase suivante, aucun retry.
Pas de loupe systématique : seulement si un résultat justifie une cible locale.

Le moteur et les métriques restent réutilisables en cas d'échec. Une réussite
établirait un couplage limité avec membrane ; l'enzyme initiale reste présente,
aucune perte, alimentation ouverte, synthèse L ou homéostasie n'est testée.
Les longues séquences et un répertoire de fonctions distinctes restent ouverts.
