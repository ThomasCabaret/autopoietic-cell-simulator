# Décisions pendant le lot 5

- Le port unique C2D échoue dans les bains mixtes (24 G + 24 F), graines 0/1,
  séquences 001 et 001011 : aucune chaîne exacte libérée de l'une ou l'autre
  famille à t=800/1200. Référence actuelle, distincte des échecs historiques.
- E3A, deux faces définies par les deux billes : 001, graines 0/1, t=800 donne
  4/5 copies G libérées et 3/4 F libérés ; deux produits nouveaux détachés observés
  ensemble. Les outils exprimés font 3/5 opérations au total, maximum 2/3 sur
  un même outil. Le critère court est positif ; tester la troisième graine.
- E3A 001011, graines 0/1, t=1200 : aucun G ni F exact libéré. Les fragments
  atteignent 5 et 3 symboles. La coexistence courte n'établit pas la capacité à
  porter une information plus longue. Les fragments F libérés ne sont plus
  recrutables comme entrants (monomères seuls) ; le stock peut être piégé.
- E3B conserve les mêmes lois et pools, mais porte l'association externe à 600
  au lieu de 200 (durée 1800). C'est une variante de protocole environnemental,
  pas une bascule copie/traduction. Comparer port unique et double face ; elle
  doit tester l'hypothèse de libération avant achèvement, sans la supposer vraie.
- Incident de scénario identifié avant analyse : la première règle de nommage
  reconnaissait seulement les noms finissant par « 6 ». Les trois premiers
  essais nommés E3dual6long (graines 0/1) et E3base6long (graine 0) ont donc
  en réalité la séquence 001 dans leurs scénarios résolus. Les conserver comme
  contrôles courts à période longue, jamais comme preuves sur six symboles.
  La sélection est désormais une table explicite, avec option --sequence et
  rejet des noms inconnus. Relancer les trois essais six symboles sous les noms
  E3dual6extended/E3base6extended. Les recettes complètes révèlent cette erreur ;
  aucun paramètre ni source des essais lancés n'est réécrit.
- Troisième graine courte : port unique réussit aussi (1 G, 2 F, deux opérations
  maximum par outil) ; les deux faces ne sont pas nécessaires à la possibilité
  de coexistence. Deux faces, trois graines : 4/5/3 G et 3/4/3 F libérés,
  coexistence détachée 3/3 et maximum 2/3/3 opérations par outil. Tester une
  simplification : port unique avec coopération locale déjà disponible (E2),
  plutôt que supposer indispensable la nouvelle géométrie à deux faces.
- Les vrais essais six symboles à période 600 donnent, avec deux faces, un G
  libéré en graine 0 et aucun en graine 1, aucun F exact dans les deux. Le port
  unique reste négatif, graine 0. Ce protocole ne résout pas la généralisation.
  G seul avec deux faces, 48 monomères, graine 0 : aucune copie exacte à t=800,
  contre une dans la référence historique. Vérifier ce contrôle sous code actuel
  avec port unique et conserver la régression du point de fonctionnement.
- E3C, port unique et coopération E2 réutilisée sous C2D, séquence 001,
  graines 0/1/2 : 3/2/2 G libérés et 3/2/3 F libérés, coexistence détachée
  dans les trois essais, maximum 2/3/2 opérations par F exprimé. Le nouvel
  état de double occupation n'est donc pas indispensable à ce résultat.
  Retenir provisoirement cette simplification, comparer la longueur 6 et
  vérifier le couplage F seul avant d'en faire la référence suivante.
