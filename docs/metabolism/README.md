# Atlas du métabolisme visé

Ouvrir [index.html](index.html), ou double-cliquer sur **metabolism.bat** à la
racine : le lanceur régénère la page avant de l'ouvrir. La page est autonome,
sans réseau, police téléchargée, serveur, installation web ou télémétrie.

Vue complète, zoom/molette, déplacement par glisser, focus sur gN/gA/gL,
retour avec Échap. Le SVG reste du texte vectoriel, les textes sont sélectionnables.
« Imprimer / PDF » utilise l'impression du navigateur, une page A3 paysage.
La planche [metabolism.svg](metabolism.svg) s'ouvre aussi dans un éditeur vectoriel.

## Source et reconstruction

```powershell
python experiments/build_metabolism_map.py
# Facultatif : aperçu raster local, PySide6 déjà fourni avec la GUI
python experiments/build_metabolism_map.py --preview outputs/metabolism/map.png
```

- [Spécification canonique](../../research/minimal_cell_spec.json) : rôles,
  précurseurs, stœchiométrie, énergie de comptabilité, tailles et budgets.
- [Annotations](../../research/metabolism_map.json) : noms, couleurs, séquences
  non assignées, état des preuves et références. Réviser la date et ces notes
  quand la connaissance change ; elles ne sont pas une déduction de l'audit.
- [Générateur](../../experiments/build_metabolism_map.py) : positions, parcours
  des flèches, typographie et symboles. Aucun dessin bitmap manuel.
- [Gabarit HTML](viewer.html.in) : affichage, navigation et impression.

Les équations utilisent `audit_cell_design.network`, contrôlé avant génération.
Le SVG contient les réactions formelles et les empreintes des sources dans ses
métadonnées ; les12 réactions sont représentées par des éléments identifiés.
SVG/HTML sont des sorties documentaires déterministes versionnées. Aperçus et
captures restent locaux dans outputs. Après modification des sources, régénérer
et inspecter la page : une génération ne garantit pas une bonne mise en page.
Un nouveau rôle oblige à revoir explicitement les trois colonnes ; il n'est pas
omis silencieusement. Le programme ne modifie pas le simulateur ni ses démos.

Vérification initiale : SVG rendu avec Qt et inspecté, contrôles sémantiques et
syntaxe JavaScript vérifiés. La politique du navigateur intégré bloque le
protocole file:// ; navigation interactive et impression n'ont donc pas été
testées dans ce navigateur. Cette limite de QA ne modifie pas le SVG statique.

## Lecture scientifique

Trois gènes **gN, gA, gL**, chacun sur son propre brin, exprimeraient **EN, EA, EL**.
Ce sont des rôles d'assemblages à concevoir, pas trois types primitifs fonctionnels
ou trois séquences déjà identifiées. La traduction cible correspond à une base
binaire pour un monomère F ; ce n'est pas un code à triplets.

Les24 bases par brin viennent du budget nominal :72 bases pour un exemplaire
de chaque gène,144 avec deux copies par gène. Les scénarios12/48 sont des bornes
de dimensionnement alternatives. Ce ne sont pas24 paires de bases permanentes :
le modèle suit des chaînes simples et leurs appariements transitoires. Un brin
par gène simplifie le découpage sans garantir début, finition et libération.

Révision02 / lot29 : « taille inconnue » sur chacun des gènes et dans l'en-tête.
Les barres interrompues ne représentent pas un nombre de bases ; les24 unités
ne sont conservées que dans le scénario de comptabilité, y compris les
métadonnées `network` explicitement marquées comme budget nominal. La fonction
de l'assemblage devra déterminer sa longueur, éventuellement différente pour
chaque outil. Voir [le brouillon mécanistique](../../research/FUNCTIONAL_MECHANISMS.md).

Chaque flèche de copie/expression suppose **tous** ses intrants : gène matrice,
monomères adéquats et énergie ; matrice et catalyseur sont conservés. Les
intersections de traits sans point ne constituent pas une réaction. Les formes
illustratives des outils ne représentent pas une conformation fonctionnelle trouvée.

**C0B est une hypothèse d'architecture abstraite**, pas la chimie matérielle déjà
unifiée. X/Y/Z et E/W sont des symboles de comptabilité ; le moteur actuel
utilise P_G/P_F/R0/R1 et L, avec activation/cycle externes, sans porteur E/W
explicite. Les flux au bord et le recyclage n'y sont pas implémentés. Les gros
fragments ne sont pas supposés pouvoir traverser la membrane ni disparaître.
La cellule actuelle possède seulement le gène001, en16 copies initiales, pas
les trois synthétases distinctes. Le bandeau d'état évite de confondre la cible
avec la démo. Une fermeture causale conditionnelle ne prouve pas la viabilité.

Inspiration de lecture en réseaux : [Roche Biochemical Pathways](https://www.roche.com/about/roche-global-citizenship/science-education/biochemical-pathways).
Composition, code, iconographie et contenu de cette planche sont propres au projet.
