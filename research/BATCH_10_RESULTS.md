# Débriefing de la campagne cinétique K1

26 octobre2026. Les six essais de la [recette figée](campaign_recipes/K1_20261026T102204813246Z/manifest.json)
atteignent1500 sans erreur, graines0/1/2 pour chaque candidat. Analyse par le
contrôleur archivé ; données complètes dans outputs/campaigns/campaign_20261026T102204813246Z/.
Aucune nouvelle simulation lancée pour ce débriefing.

| Candidat | Graine | Nouveaux dimères incorporés | Première insertion fermée | Fraction fermée | Fraction classable | Sondes sorties /24 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| B, barrière de lien | 0 | 1 | 293 | 0,590 | 0,718 | 0 |
| B, barrière de lien | 1 | 2 | 376 | 0,805 | 0,978 | 0 |
| B, barrière de lien | 2 | 5 | 77 | 0,826 | 0,978 | 0 |
| B simple, sans barrière de lien | 0 | 0 | >1500, censuré | 0,771 | 0,951 | 4 |
| B simple, sans barrière de lien | 1 | 1 | 890 | 0,842 | 0,990 | 3 |
| B simple, sans barrière de lien | 2 | 0 | >1500, censuré | 0,613 | 0,734 | 2 |

Tous les dimères incorporés de B atteignent une persistance fermée échantillonnée
≥10 : maxima18,5 pour graine0 ;14,5–18 pour1 ;15–20 pour2. Ces maxima n'impliquent
ni fermeture permanente ni absence d'ouvertures entre images. Il s'agit du nombre
d'IDs distincts incorporés au moins une fois, pas du nombre final de lipides gagnés.

## Conclusions permises

1. **La durée courte masquait un mécanisme lent.** B insère dans3/3 essais à1500,
   contre1/3 à150. Les premiers événements293 et376 expliquent ces deux échecs
   courts. Cela valide une possibilité locale reproductible sur ces trois graines,
   sans mesurer encore une probabilité de succès générale ou un flux soutenu.
2. **La membrane entière n'est pas fiabilisée.** Le seuil fermé≥0,8 passe seulement
   pour deux graines B. Le zéro de sortie observé de B0 est accompagné de28% de
   périodes non classables : ne pas l'interpréter comme rétention complète.
3. **La simplification ne se transfère pas.** Sans barrière de lien, les pertes
   observées sont2–4/24 (8,3–16,7%), au-dessus du criblage≤5%, et l'insertion ne
   se produit que dans1/3 essais. Les réussites courtes S ne justifient donc pas
   de supprimer cette aide du candidat B à longue durée.
4. **Les occasions admissibles sont rares.**21–24 des24 nouveaux dimères rencontrent
   des anciens dans chaque essai. Le temps-face admissible de capture n'est que
   1,90/2,27/6,71 dans B et0,15/0,61/0,21 dans B simple ; celui d'échange vaut
   37,08/39,60/31,97 contre18,23/21,50/16,46. Il y a9/12/11 échanges effectués
   dans B contre4/9/2. Ces expositions approximatives et les conflits locaux ne
   permettent pas un taux exact ni une attribution de toute la différence à la
   seule barrière. L'accès géométrique et la refermeture sont les pistes prioritaires.

L'effet causal de l'échange sur la fragilité n'est **pas isolé** : il manque des
contrôles sans échange à la même durée1500. Les passages censurés ne prouvent
pas l'impossibilité de B simple. Le premier contact est déjà présent àt0 pour
quelques molécules : livraison initiale près de la frontière, pas import depuis
un réservoir extérieur. Aucune chimie G/F ni fabrication de L n'est intégrée.

## Vérification et deux étapes proposées

Six résultats achevés sans erreur ;168 empreintes des sources et18006 observations
temporelles vérifiées. Sommes des fenêtres cinétiques et temps de première
insertion recoupés indépendamment avec les historiques. Les résultats, checkpoints
et analyses restent locaux ; la recette et ce bilan sont versionnés. Pas de
nouvelle batterie de tests logiciels nécessaire pour cette analyse sans changement
de code ou de lois.

**1 — Fermer le diagnostic de robustesse membranaire.** Conserver B comme référence,
comparer sans échange au même horizon et mesurer les ouvertures/périodes inconnues.
Séparer accès, échange et refermeture avant de modifier une règle. Demander
insertion, rétention et stabilité conjointes, sous les mêmes lois et plusieurs
graines ; ne pas ajouter d'insertase sur ce seul résultat.

**2 — Tester une première intégration matérielle avec G/F.** Portage explicite
vers un alphabet/jeu de lois commun, d'abord cohabitation et perméabilité des
vrais précurseurs libres et composants liés ; puis copie/expression dans la
frontière préparée, avec mêmes produits réellement utilisables. Mesurer également
liaisons parasites, séquestration et fuites. La production L et le renouvellement
de la frontière restent des dépendances à réaliser, pas à déduire de cette étape.

Santé : progrès réel et risque mieux localisé, aucun blocage de principe établi.
Le candidat reste conditionnel, avec aides locales déclarées et énergie non
calibrée ; aucun nombre fiable de lots restants. Le GPU n'est pas requis pour
conclure ce diagnostic ; optimisation CPU après mesure si le prochain bain coûte
trop. La maturité progresse pour l'insertion isolée, pas pour la cellule intégrée.
