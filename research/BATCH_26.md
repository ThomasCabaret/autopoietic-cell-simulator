# Lot26 — démos actuelles vérifiées et priorités après MD2

[Plan](BATCH_26_PLAN.md), [bilan MD2 complet](BATCH_25_RESULTS.md). Les15 essais
sont terminés,0 erreur, aucun calcul encore actif. Pas de nouvelle loi chimique
ou de nouveau long calcul dans ce lot de consolidation.

## Lancement utilisateur

Relancer `visualizer.bat`, menu **Démos → État actuel · bain intégré**.
Cette action charge exactement MD2_bath_new_s2, en pause à t=0,2118 billes,
Langevin et contacts cohérents. Jouer en Maximum, zoomer et suivre dans Explorer.
Le grand bain peut prendre des dizaines de minutes jusqu'à1200 ; ce n'est pas
une animation précalculée. La graine2 est un choix illustratif déclaré (G
nouveau observé et bonne tenue), pas une preuve de fréquence de succès.

Trois scènes actuelles, chacune aux graines2/0/1 :

- **Cellule construite · état actuel** : bain MD2, anneau/gènes/outils construits,
  matière fabriquée et utilisée, copies G rares, aucun nouveau F à1200.
- **Membranes · molécules libres** :36 dimères sans liens latéraux, scène rapide
  pour vérifier que l'assemblage n'est pas un ruban préparé qui se replie.
- **Membrane · insertion et passages** : grande membrane et sondes préparées,
  insertion et passages locaux ; l'échec de la graine1 reste accessible.

Les12 anciennes entrées sont rangées sous **Références et sous-systèmes**,
avec leurs scénarios/signatures conservés.21 choix au total. Aucun état initial
ou paramètre retouché pour la présentation, sources exactes du manifeste MD2.

## Ce que le contrôle visuel établit

Signatures et matériels des neuf nouveaux presets comparés aux sources,
comme les12 anciens.21 actions Qt natives ouvertes, pause initiale vérifiée.
Lecture/pas/pause/recommencement exact sur les scènes actuelles. Les positions
copiées en float32 correspondent **exactement** au moteur sans interface au
même pas ; aucune force, réaction ou PRNG piloté par caméra, filtres ou mesure.

Les compteurs de sondes viennent de l'observateur existant. Une frontière
inconnue affiche « non classable », sans transformer un dernier inventaire
connu en mesure actuelle. Sorties/entrées indiquent ce qui a été observé,
pas un flux garanti ni l'étanchéité sur les périodes inconnues. Les structures
préparées restent exclues des nouveaux G/F.

143 tests logiciels et7 historiques réussis. Test de passivité ajouté pour
les compteurs des sondes, comparaison avec/sans observateur et PRNG identiques.
Test natif21 entrées, action recommandée, identité des images au moteur et
recommencement exact. Captures locales inspectées sous outputs/demo_qa.
Les vérifications GUI courtes ne remplacent pas les essais scientifiques1200.

## Bilan et suite

La mécanique membranaire progresse nettement ; le bain reste un prototype
construit à renouvellement incomplet. Aucun F nouveau complet à1200 et stock
global F non épuisé : T9 doit examiner accès, éligibilité, ligation et finition,
avec contrôle de séquestration des outils complets. L'insertion/réparation
garde un cas fragile à diagnostiquer, notamment autour de l'échange223,61.
Synthèse L, diversité de fonctions, flux extérieur et homéostasie restent ouverts.
Les verrous sont mieux identifiés, leur résolution conjointe n'est pas acquise.

Aucun outil/gène/type/port supplémentaire, même budget de particules et mêmes
lois que MD2. Ce lot rend le candidat inspectable avant de nouvelles décisions.
Arbre, santé, maturité et priorités actualisés ; code/recettes seuls versionnés,
données/figures locales, commit local sans push.
