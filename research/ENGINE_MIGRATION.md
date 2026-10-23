# W0 — factorisation et démonstrateurs, 23 octobre 2026

Politique Git corrigée ensuite : seuls les codes, configurations et recettes
des essais sont versionnés. Les enregistrements mentionnés ici restent locaux
et se reconstruisent avec [REPRODUCTION.md](REPRODUCTION.md). Le ZIP ne contient
plus de données de simulation ; la relecture de fragments les recalcule si nécessaire.

Ce lot est un travail d'infrastructure demandé par l'utilisateur. Il ne remplace
pas le lot 2 de chimie ni ne démontre une nouvelle fermeture biologique.

## Décision et réalisation

Un ordonnanceur et des noyaux mécaniques CPU communs remplacent les deux boucles
des prototypes courants. Les hooks copie/expression et membrane gardent leurs
lois locales distinctes. Campagnes, fenêtre et anciens points d'entrée utilisent
le même moteur. Python/Numba a été choisi pour garder l'itération de recherche
rapide tout en compilant les calculs numériques ; le C++ historique reste une
référence d'architecture, pas une dépendance de construction.

Les contacts utilisent un arbre KD avec marge de voisinage et ordre déterministe,
comparé à une recherche exhaustive. Les ressorts et angles ne passent pas par le
filtre spatial. L'interface, les réactions et les observations sont découplées.
Des configurations JSON résolues et six lanceurs Windows sont fournis, dont quatre
scénarios calculés, une relecture identifiée et une campagne sans fenêtre.

L'architecture est détaillée dans `SIMULATOR_ARCHITECTURE.md`. Le paquet à extraire
se trouve dans `deliverables/`. Il contient les sources, les scripts, les
configurations et les enregistrements requis, sans environnement Python embarqué.

## Validation des comportements migrés

Quatre essais complets sont archivés dans `research/engine_runs/`, référencés
précisément par `ENGINE_VERIFICATION.json`. Tous passent leurs critères :

| Scénario, graine 0 | Durée simulée | Résultat actuel |
| --- | ---: | --- |
| Copie T7 | 800 | Une nouvelle chaîne G complète libérée |
| Membrane V4 | 300 | Une boucle fermée de 18 unités, aire finale 24,849 |
| Expression E0 | 600 | Une nouvelle chaîne F complète libérée |
| E0 sans gène polymérisé | 600 | Zéro ligation |

Ces essais confirment les démonstrateurs choisis. Ils ne sont pas des répétitions
indépendantes supplémentaires des anciennes statistiques. L'ordre numérique et
le parcours des contacts ont changé ; les trajectoires historiques sont conservées
avec leur code, sans promesse de les retrouver avec la révision actuelle.
La deuxième génération favorable du lot 2 **n'est pas retrouvée** dans cet essai
T7 migré. L'assemblage de fragments V6 est validé à courte durée techniquement,
mais sa réussite historique est seulement montrée en relecture dans ce lot.

## Vérifications et incidents conservés

- Neuf tests du nouveau moteur : contacts exacts malgré le cache, forces cohérentes,
  lien étiré conservé, orientation/ports, arbre/exhaustif, checkpoints intermédiaires,
  indépendance du découpage des pas et du rendu, provenance et rejeu, entrées invalides.
- Quatre tests mécaniques et trois tests des observateurs historiques continuent
  de passer par les nouveaux points d'entrée.
- L'interface est exercée avec le pilote vidéo SDL hors écran : dessin réel,
  boucle d'événements, fermeture, relecture, et même trajectoire entre travailleur
  graphique et headless. Les captures ont été inspectées. L'usage manuel d'une
  fenêtre native sur le bureau n'a pas été testé dans cette session.
- Le lanceur `.bat` commun est exécuté depuis un autre répertoire sous Windows,
  avec le contrôle sans gène raccourci. Il retrouve correctement racine et config.
- Le même contrôle passe depuis le paquet extrait dans un autre dossier, avec
  les sources et configurations du paquet. Les SHA-256 de tous les membres du ZIP
  sont vérifiés. Le rejeu complet du ruban membranaire depuis son moteur archivé
  reproduit toutes les métriques ; le headless n'importe aucune bibliothèque graphique.
- Les premiers tests ont détecté un nom de voisinage masqué par un tableau dans
  les ports et un masque vide de mauvais type ; corrigés avant les validations.
  L'accès au répertoire temporaire Windows a nécessité une exécution autorisée
  des tests hors du bac à sable. Ce ne sont pas des échecs chimiques.

Le benchmark compare les mêmes forces de répulsion, recherche et reconstruction
de l'arbre incluses. Sur 128 / 512 / 2 048 billes à densité fixée, le relevé final
donne environ 4,2× / 31× / 107× face à la matrice dense. Les mesures exactes
et le périmètre figurent dans `ENGINE_BENCHMARK.json`. Ce n'est pas une accélération
mesurée de toute la simulation : réactions, analyse et rendu sont hors benchmark.

## Maturité et prochaine recherche

**Logiciel : premier outil utilisable et vérifié pour les petits démonstrateurs.**
Les grandes populations avec chimie réactive, le GPU, la distribution sans Python
et la création/destruction générique de billes restent à construire si nécessaires.

**Chimie : toujours précoce.** Les objectifs C1 (chaîne catalytique réutilisable)
et E3 (copie et expression compatibles) restent prioritaires. Ce lot fournit
l'instrument commun pour ces expériences ; il n'établit pas leurs fonctions.
