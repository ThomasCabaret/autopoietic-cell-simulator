# Lot10 technique — campagnes figées et premières mesures cinétiques

26 octobre2026. [Plan](BATCH_10_PLAN.md), [utilisation Windows](../campaigns/README.md).
Cette livraison améliore la méthode de calcul ; aucune nouvelle capacité chimique
ni accélération×10 n'est revendiquée. La campagne longue sera analysée au retour.

## Livré et vérifié

- Manifeste de scénarios résolus, sources copiées et empreintes vérifiées ;
  contrôleur et travailleurs exécutés depuis cette copie figée.
- Deux tâches simultanées maximum dans le plan fourni ; suivi du temps simulé,
  débit récent, ETA révisable, heartbeat, erreurs et verrou de processus actif.
- Arrêt demandé, checkpoint atomique périodique, reprise des inachevés et absence
  de relance des tâches terminées. Les anciens dossiers d'essai restent présents.
- Export source seule et restauration en sortie neuve ; recettes versionnables,
  trajectoires/checkpoints/résultats locaux et ignorés par Git.
- Diagnostic membrane avant chaque tick réactif : rencontres anciennes/nouvelles,
  géométries de capture/échange admissibles, temps-face par fenêtre, échanges
  effectués, premiers contacts et première insertion fermée.
- Passages sans événement censurés à droite ; courbes Kaplan–Meier par candidat,
  protocole et horizon identiques. Une graine dupliquée n'ajoute pas un réplicat.

58 tests logiciels et7 historiques passent. Nouveaux contrôles : géométrie
d'échange effectivement éligible, trajectoires/PRNG/export chimique identiques
avec diagnostic, arrêt à une étape intermédiaire puis reprise exactement égale
en positions/métriques/expositions, calcul dans un sous-processus figé, refus
d'une source altérée, restauration sans données, tâche terminée non redémarrée,
distinction statut ancien/processus vivant et censure connue. Le moteur physique
et les règles de réaction restent ceux du lot9 ; aucun ordonnanceur chimique ajouté.

## Limites et suite

Les temps-face sont des observations pré-réaction, pas une intégrale exacte du
risque : conflits séquentiels, échanges dans le sens nouvelle→ancienne et
rupture/reformation dans un même tick ne sont pas tous dénombrés. Trois graines
ne donnent pas une statistique robuste. Les autres hooks restent exécutables,
mais leurs occasions chimiques sont marquées non mesurées. Pas d'arrêt précoce
des graines lentes, d'ajustement de taux ni de verdict automatique d'impossibilité.

Plan long : B et B sans barrière de lien,0/1/2,t1500. Il teste à la fois le
temps d'attente et le transfert de la simplification du lot9 ; il ne contient
ni vrais G/F ni L fabriqués. Rapporter fraction classable, ouverture/fuite et
persistance, pas seulement le nombre d'échanges. Prochaine décision chimique
après ce lot, puis I0/T9. CPU/GPU après profil stabilisé ; le diagnostic a lui-même
un coût, dont il faudra mesurer la part avant optimisation.

Le calcul peut continuer après la réponse, ordinateur actif. Pas de service
au démarrage, notification ou poursuite pendant veille/extinction. Après arrêt
brutal, reprendre au checkpoint et inspecter les erreurs. Les lanceurs et leurs
limites sont décrits dans campaigns/README.md.
