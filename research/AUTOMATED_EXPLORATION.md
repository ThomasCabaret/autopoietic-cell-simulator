# Exploration programmable et décisions de conception

28 octobre2026, demande utilisateur. L'exploration peut être un arbre de
backtracking ; une conversation ne doit pas remplacer une boucle dont le test
et les décisions sont déjà calculables. Utiliser le moteur et les campagnes
existants, pas un second ordonnanceur de simulation ni une plateforme générale.

Avant un lot, distinguer :

- **Programmable** : grille bornée de variantes, répétitions, critères techniques,
  calcul des métriques, seuils annoncés, lancement des contrôles suivants,
  arrêt d'une branche et conservation de son motif de rejet. Les programmer
  ensemble si cela évite une ou plusieurs interventions manuelles prévisibles.
- **À interpréter** : origine probable d'un piège, pertinence d'une représentation,
  nouvelle loi ou primitive, flexibilité aval, compromis entre fonctions et
  révision d'un critère scientifique. L'automate rend alors un rapport et s'arrête.

Un seuil peut choisir un prochain **test**, pas établir à lui seul sa conclusion
scientifique. Toute sélection dépendant des résultats est déclarée : conserver
les essais non retenus, ne pas convertir une branche sélectionnée en validation
indépendante et ne pas additionner des succès de chimies différentes.

Chaque chaîne fixe avant exécution ses scénarios/sources, nœuds et conditions de
transition, graines/horizons, budget maximal, témoins réutilisés, critères d'arrêt
et sorties à interpréter. Les réglages adaptatifs créent des candidats tracés,
jamais une modification silencieuse d'une cohorte en cours. Le contrôleur de
recherche agit **entre essais**, pas sur les particules selon un observateur.
Cette adaptation expérimentale externe n'est pas une régulation cellulaire.

Préserver un statut atomique, un journal des décisions avec hashes des rapports,
les checkpoints et sources figées. Pas de relance automatique d'un essai en
erreur ni de duplication après interruption ; exiger inspection/reprise explicite.
Ne pas lancer le suivi pendant que ses prédécesseurs utilisent encore les
travailleurs. Une pause doit empêcher les branches suivantes ; une reprise
conserve les tâches achevées et les échecs. Le budget borne aussi le coût réel
de calcul ; un arbre extensible sans horizon de décision est à éviter.

Première application : `scripts/numerical_followup.py`, chaîne spécifique N1 →
analyse → éventuellement N2. Six nouveaux essais maximum, deux travailleurs.
Le critère d'alerte N1 était déjà déclaré ; le suivi N2 est annoncé après lecture
de deux essais sur six, avant la cohorte fine et ses décisions. À la fin,
interpréter T9 ou les cadences ; aucune nouvelle chimie inventée automatiquement.
