# Lot16 : J2 analysé, densité construite et frontière ouverte future

27 octobre2026. Les12 témoins J2 sont terminés sans erreur, sources, événements,
durées et bilan P/R vérifiés. Bilan BATCH_15_RESULTS.md. Le compact aide les
incorporations, sans nouveau G/F complet : aucune solution cellulaire acquise.

Décision : J3 conserve les lois et teste trois inventaires construits dans
la vésicule centrée. Avec L588/1302/2118 billes, sans L102/816/1632. Neuf paires
initiales vérifiées P/R et PRNG identiques, plus les trois ablations K16 sans
boost. Même séquence001 copiée, pas une bibliothèque de fonctions supplémentaires.
Les matrices et réactions ne changent pas, le témoin sans boost est séparé.

Une correction d'observateur était nécessaire : chaque G complet préparé est
un parent de génération0. Auparavant seul le premier était certifié ; les
autres auraient sous-attribué la provenance des copies et outils exprimés.
Les nouvelles chaînes restent distinctes du stock construit. Fragments, F et
séquences incorrectes ne sont pas certifiés. Le cas à gène unique est exactement
conforme à l'observateur J2 archivé ; pas d'effet sur les forces ou le PRNG.

Le census ajoute les monomères disponibles au plus proche de tous les templates
initiaux, en gardant les anciennes distances au premier pour traçabilité. Le
rapporteur compare la fermeture aussi sur grille régulière0,5, afin que plus de
ligations ne surpondère pas leurs instants d'observation. Anciennes métriques
conservées. Ces changements sont analytiques, pas une nouvelle régulation.

Pilote sélectionné K16,bain,graine0,t2 :2118 billes, stable,3 dimères catalysés,
zéro incorporation/G/F nouveau et aucun contact P/R–L observé. Ce n'est qu'un
test technique ; recette source seule BATCH_16_PILOTS.json. Les résultats longs
doivent mesurer vrais contacts, flux incorporé et reconstruction, avec censure.

OPEN_BOUNDARY.md consigne la demande utilisateur : source réglable au bord
extérieur, sortie absorbante, gradients et concentration locale mesurée. Le
nombre de particules peut varier ; le moteur actuel préalloué doit évoluer
techniquement pour cela. Pas de source implémentée ni de concentration imposée
au voisinage cellulaire dans J3. Apports futurs ne corrigeront pas silencieusement
les déficits internes. Homéostasie et synthèse de L toujours non démontrées.

Plan long21 tâches à1200, deux travailleurs et checkpoints60s. Plusieurs heures
de calcul possibles. Horizon : cette campagne, puis choix de mécanisme si le
budget proche de la cible ne suffit pas. Pas d'engagement de durée biologique.

Validation avant gel :91 tests logiciels et7 historiques passent. Les neuf
paires avec/sans L et trois ablations ont été vérifiées. Comparaison de hashes
aux sources J2 : seul simulator/observations.py change, pour la filiation ;
tous les modules physiques et réactifs restent byte-identiques.

## Lancement figé

Campagne `campaign_20261027T192723206222Z`, code3d2cb79,21 tâches à1200,
deux travailleurs et checkpoints60s. Recette source seule conservée dans
campaign_recipes/J3_20261027T192723206222Z. Aucun résultat long encore interprété.
Suivi campaign_status.bat, arrêt/reprise et analyze_campaign.bat habituels ;
le census détaillé se lance par experiments/analyze_constructed_tool.py.
