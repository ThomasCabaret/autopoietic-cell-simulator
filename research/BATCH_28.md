# Lot28 — atlas généré de la cellule visée

Livraison demandée : [SVG vectoriel](../docs/metabolism/metabolism.svg),
[page autonome](../docs/metabolism/index.html), [guide](../docs/metabolism/README.md).
Lanceur Windows `metabolism.bat`. Le source Python contrôle toutes les positions,
courbes, formes et textes ; aucun dessin bitmap manuel ou génération d'image IA.

## Contenu et provenance

Trois espèces gN/gA/gL sur brins distincts, leurs outils EN/EA/EL, intrants
partagés, synthèse N/A/L, copies, expression, insertion intérieure, apports
au bord externe, sortie de W et frontière. Chaque matrice/catalyseur est conservé ;
les intrants se combinent par ET. Les12 réactions formelles de C0B sont identifiées
dans le SVG et incluses en métadonnées avec empreintes des sources.

Les rôles, équations et budget viennent de minimal_cell_spec.json et du même
audit matériel/causal que l'ancienne planche. Les annotations d'état sont dans
metabolism_map.json, le look dans le générateur, la navigation dans le gabarit
HTML. Génération déterministe et autonome sans dépendance web. SVG/HTML versionnés,
aperçu raster et captures locales exclus de Git. Les figures historiques restent.

Clarification :3 gènes,24 bases chacun uniquement dans le budget nominal,72 bases
par ensemble,144 pour deux copies/gène. Séquences fonctionnelles inconnues.
Un symbole→un monomère F envisagé, pas des codons biologiques ; appariement
transitoire, pas duplex permanent exigé. Un brin/gène simplifie le découpage
sans résoudre initiation/finition/libération. La démo reste001×16, pas ces trois
fonctions. Aucun outil supplémentaire ou nouveau type ajouté.

La planche signale les dettes : X/Y/Z/E/W sont une abstraction comptable, pas les
types P/R+L actuels ; homéostasie, flux et recyclage non réalisés ; aucun déchet
polymère supposé disparaître ou traverser magiquement. La conformation dessinée
d'EN/EA/EL est illustrative, pas une protéine fonctionnelle découverte. Une
fermeture de graphe ne prouve pas la viabilité, ni l'orthogonalité des réactions.

## Vérifications et limites

Neuf tests (carte + audit de cellule) réussis : conservation et dépendances,
présence de chaque réaction/gène/outil, absence de séquences inventées,
déterminisme et propagation des annotations. Syntaxe JavaScript vérifiée avec
node --check. SVG rendu par Qt avec polices chargées explicitement, aperçu
inspecté sous outputs/metabolism/map.png. Les textes restent vectoriels.

Le navigateur intégré refuse les URL file://. Aucun contournement tenté ;
les clics, panoramique et impression n'ont pas été validés dans ce navigateur.
Le SVG statique a été inspecté et peut être ouvert directement. L'ouverture
du SVG dans le panneau Codex est demandée, statut retourné queued.

## État des recherches conservé

Lecture de statut T9E : cohorte corrigée12/12 complète, zéro erreur, porte refusée ;
F libérés dans les trois contrôles expression0/0/0 pour ancien et T9E. Quatre
transferts non lancés. Aucune campagne nouvelle, aucun calcul actif de ce suivi.
Ne pas prétendre que cette lecture explique déjà le verrou : prochain lot
scientifique pour interpréter accès/éligibilité/ligation, pas réglage automatique.

Arbre, journal, priorités, santé/maturité actualisés. Niveau de maturité inchangé :
couplage MD2 partiel, renouvellement F et fermeture constructive ouverts. La
carte rend le cahier des charges inspectable, sans remplacer sa réalisation.
