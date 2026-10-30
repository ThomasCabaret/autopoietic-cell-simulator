# Démos représentatives accessibles dans la GUI

## État actuel — MD2,21 choix vérifiés

Relancer **`visualizer.bat`**, puis **Démos → État actuel · bain intégré**.
Ce raccourci ouvre **Cellule construite · état actuel, graine2**, en pause à t=0,
avec Langevin et les contacts liés/libres cohérents. Cliquer **Jouer**, laisser
la vitesse **Maximum**, zoomer à la molette et glisser pour déplacer la vue.
**F** revient à la vue globale ; **Explorer** propose filtres, sélection et suivi.

| Scène actuelle | Billes | Ce qu'on peut examiner |
| --- | ---: | --- |
| Cellule construite · état actuel | 2118 | Membrane, outils et gènes préparés, fabrication et usage de composants ; copie G rare, F non renouvelé |
| Membranes · molécules libres | 72 | Assemblage depuis36 dimères isolés, sans chaîne préassemblée ; scène plus rapide |
| Membrane · insertion et passages | 534 | Grande membrane préparée,24 L internes libres et48 sondes ; insertions locales et passages observés |

Chaque scène propose les trois graines2/0/1, exactement celles de la campagne
MD2. La graine2 recommandée du grand bain a une copie G observée et une bonne
tenue membranaire ; c'est un choix illustratif, pas une fréquence de succès.
La graine1 du contrôle à sondes garde son échec durable après224. Les ouvertures,
défauts et valeurs non classables restent visibles.

Le grand bain peut demander des dizaines de minutes pour atteindre1200 unités
simulées. Il est recalculé en direct, pas rejoué depuis un film ou un checkpoint
avantageux. Pour un premier regard rapide, choisir les molécules libres.
Les fiches indiquent matériel préparé, conditions, résultats mesurés et limites.

Les neuf nouveaux préréglages ont des signatures exactement égales au manifeste
MD2. Les12 choix antérieurs sont accessibles sous **Références et sous-systèmes**,
sans modification de leur dynamique. Ne pas additionner les réussites des
sous-systèmes chauds, des petites V8 et du bain intégré en une cellule viable.

La membrane, les16 G001 et16 F001 sont construits au départ dans le grand bain.
Ils ne comptent pas comme nouveaux produits. Ni synthèse de L depuis la
nourriture, flux continu, homéostasie ou maintien autonome n'est démontré.
Les compteurs des sondes sont passifs ; « non classable » reste inconnu,
et zéro sortie observée ne garantit pas l'étanchéité pendant ces périodes.

Validation :143 tests logiciels et7 historiques,21 actions Qt natives,
pause/lecture/recommencement exact. Les images actuelles coïncident exactement
avec les positions float32 du moteur sans interface au même pas. Aucune
information de caméra, contour ou résultat ne pilote les lois. Sources et
bilans : [MD2](../research/BATCH_25_RESULTS.md), [lot26](../research/BATCH_26.md).

## Historique — catalogue GUI2/LT2 et références conservées

Catalogue du 30 octobre 2026. Lancer `visualizer.bat`, puis **Démos → Bain intégré
actuel → Graine 2 · Langevin · candidat** pour examiner le nouveau mouvement.
Le choix **Graine 2 · transfert observé · Brownien · référence** conserve la
référence historique. Le bouton **Démos** de
la barre d'outils ouvre le même catalogue. Aucun chemin JSON à chercher.

Chaque choix recalcule la simulation depuis son état initial, en pause. Cliquer
**Jouer**, puis ajuster la vitesse, zoomer à la molette ou glisser pour
déplacer la vue. Le rythme initial des démos est **Maximum**, sans modification
du pas numérique ; ralentir ensuite pour examiner les liaisons. **F** revient
à la vue globale. L'onglet **Explorer** contient filtres, sélection et suivi ;
l'onglet **Démo** explique l'essai, ses limites et ses mesures en direct.

## Quatre démos, douze préréglages comparables

Chacune des six scènes a maintenant deux versions : **Brownien · référence**
et **Langevin · candidat**, y compris les trois graines du bain intégré.
Même matériel, positions initiales, lois chimiques, température, horizon et pas ;
Langevin ajoute des vitesses et une inertie avec masse1/frottement0,1.
Les trajectoires et tirages aléatoires divergent ensuite. Le défaut historique
reste brownien ; aucune réussite historique n'est attribuée au candidat.

La fiche **Enjeu de la comparaison** précise la fonction à préserver : copies
libérées, F exprimé réellement actif, composants utilisés, membrane et transport.
Les conditions et la référence interne s'adaptent à la variante.
Voir [protocole](../research/BATCH_23_PLAN.md) et [bilan](../research/BATCH_23.md).
Les résultats ne servent jamais à ajuster les lois pendant la simulation.

LT2 est désormais achevé16/16. Les microdémos se transfèrent, mais le grand
bain Langevin perd fortement sa continuité membranaire dans deux graines sur
trois. Ces échecs restent visibles, sans remplacement par une graine favorable.
Voir [résultats complets](../research/BATCH_23_RESULTS.md). Langevin reste la
base de recherche ; le diagnostic membranaire MD1 précède la reprise de T9.

| Démo | Billes | Rôle et départ | Limite essentielle |
|---|---:|---|---|
| Bain intégré actuel, J3 |2118|Grande membrane,16 G001 et16 F001 déjà construits, monomères et précurseurs ; même bain|Intégration partielle, pas une cellule viable ni un renouvellement complet|
| Copie, expression et fabrication, C3B1 |102|Un G001 et six monomères F, autres P/R libres ; les F complets doivent être exprimés|Sous-système chaud sans membrane, pas interchangeable avec le bain intégré|
| Copie binaire seule, T7 |108|Chaîne001011 et48 dimères libres déjà fabriqués|Copie seule, sans fabrication des dimères ni expression|
| Petites membranes depuis molécules libres, V8 |72|36 dimères isolés, aucune liaison latérale préassemblée|Petits contours distincts de la grande membrane, pas de rétention démontrée|

Le premier est la vue la plus intégrée effectivement étudiée. Trois graines
0/1/2 sont proposées ; la 2 apparaît en premier car un F nouvellement exprimé
y a produit des composants ensuite incorporés. Ce choix est illustratif :
il ne mesure pas une probabilité de succès. La 1 produit G et F nouveaux mais
sans activité observée de ce F à 1200 ; la 0 ne produit pas de nouveau F sur
cet horizon. Les résultats ne doivent pas être réunis en une réussite unique.
Référence : research/BATCH_16_RESULTS.md.

La grande membrane est **préparée** : 219 molécules en anneau et 24 libres.
Les 24 libres peuvent s'insérer ; elles ne sont pas synthétisées par les outils.
Le contenu est placé au centre puis évolue sans paroi interne ni recentrage.
Le stock de nourriture est fini, sans flux extérieur continu. Les défauts,
la dispersion et le faible renouvellement restent visibles. La durée 1200 est
en unités simulées ; le temps à l'écran dépend du débit réel, pas d'un film
précalculé. Le cycle d'association/libération est une aide externe 200/15.

Les trois sous-systèmes servent à voir plus facilement les mécanismes que le
grand bain rend rares ou difficiles à lire. C3B1 et T7 utilisent 0,6 de température,
le bain intégré 0,08 ; V8 a une autre géométrie membranaire. **Leurs réussites ne
s'additionnent pas en une preuve d'une chimie commune complète.** Les fiches
de la GUI déclarent ces différences et le matériel préparé.

## Mesures et traçabilité

La fiche montre les nouveaux G/F libérés hors chaînes préparées, les composants
construits/catalysés/réutilisés et l'état de frontière ou les contours observés,
selon le modèle. Ces compteurs viennent des observateurs de recherche existants,
avec leur temps de mesure ; ils ne pilotent jamais les réactions. Ce ne sont
pas encore des courbes cinétiques. « Frontière non classable » reste un état
inconnu, pas une fermeture supposée.

`demonstrators/catalog.json` décrit les fiches, graines, sources et signatures.
Les `demonstrators/configs/demo_*.json` sont des scénarios résolus dérivés des
entrées archivées, sans nouvelles règles ou liens forcés. Les champs de dynamique
modèle/graine/horizon/moteur/chimie sont comparés aux sources pour les références.
Les variantes gardent chimie et moteur identiques et ajoutent explicitement
`mechanics` dans leur signature ; les positions initiales sont vérifiées égales.
Le chargement
refuse une signature modifiée au lieu de garder silencieusement la même étiquette.
Chaque session écrit son scénario, ses sources moteur et un `demo.json` local.
Les sources historiques restent intactes ; aucune trajectoire ou checkpoint
n'est embarqué dans le catalogue.

Pour reconstruire ou contrôler les entrées :

```powershell
python experiments/prepare_demo_catalog.py build
python experiments/prepare_demo_catalog.py verify
```

Le contrôle vérifie notamment 16 G/F complets préparés pour J3, aucun F complet
préparé pour C3B1 et aucune liaison latérale initiale pour V8. Les validations
GUI ouvrent les douze choix via leurs actions Qt, vérifient la pause initiale,
font jouer les deux mouvements du bain intégré et retrouvent exactement leur état initial au
recommencement. Elles ne constituent pas une nouvelle campagne complète à 1200.
Les réussites de long horizon citées proviennent des expériences référencées.

Vidéo, relecture avancée et courbes sont reportées pour spécification ultérieure.
Elles ne conditionnent pas l'utilisation actuelle de ces démos.

Validation du lot23 :136 tests logiciels et7 historiques réussis, plus le test
Qt/OpenGL natif des douze entrées et du démarrage/pause/recommencement de J3
avec les deux mouvements. Les comparaisons de long horizon sont une campagne
scientifique séparée ; la validation de menu ne les remplace pas.

Le catalogue conserve aussi les empreintes du code moteur utilisé pour cette
sélection. Si ce code change, les démos demandent une révision du catalogue
avant leur lancement ; une ancienne étiquette ne masque pas de nouvelles lois.
