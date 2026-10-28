# Lot18 — N1 analysé, exploration programmable et diagnostic T9

28 octobre2026. N1 était2/6 au début du lot,6/6 sans erreur lors de la validation.
BATCH_17_RESULTS.md donne les cohortes entières. Fabrication/incorporation
conservées au pas fin, aucune alerte médiane prospective ; G encore très rare
et une membrane fine fortement dégradée. Aucun résultat de convergence garanti.

Le suivi borné N1→analyse→N2 éventuel est implémenté avec sources figées,
contrôle des prédécesseurs, rapport/hash de décision, limite6 essais/2 travailleurs,
absence de doublon, pause/reprise et arrêt pour interprétation. Il réutilise les
campagnes existantes et ne choisit pas de lois pendant une trajectoire. La
transition N2 est calculable ; la conclusion scientifique ne l'est pas à partir
de trois médianes seules. Le plan a été choisi après deux résultats moyens,
avec les alertes N1 déjà annoncées ; pas une validation indépendante aveugle.

Le moteur expose reaction_every avec défaut5 exact. Seuls engine.py/config.py
changent, pas la chimie. N2 préconfiguré sépare les deux cadences si l'alerte
fine le demande. En absence d'alerte, sa préparation ne doit pas être présentée
comme six nouveaux essais réalisés. Zéro nouvelle primitive chimique ou outil.

## Diagnostic T9 : deux gardes et un risque de séquestration

`python experiments/diagnose_fragment_capture.py` reconstruit six contrôles
de contacts idéaux : F monomères, fragment01 et outil complet001, avec/sans
monomer_only_capture. Géométrie préparée, tirage conditionné à acceptation,
un seul appel à la règle réelle, aucun pas mécanique. C'est un contrôle logique,
pas une expérience de cinétique, d'assemblage ou de renouvellement. Les états,
sources et résultats sont conservés dans
`outputs/diagnostics/T9_gates_20261028T171634136779Z`.

Les trois sites monomères sont recrutables ; seuls le monomère isolé3 du cas
fragment est recruté ; aucun site du F complet ne l'est. Même résultat avec
le garde monomère désactivé : le garde G/F impose indépendamment degré(F)=0.
Une simple ablation de monomer_only_capture ne résout donc pas T9 pour F.

À l'inverse, autoriser les extrémités F liées expose aussi les extrémités des
outils complets : même degré local1 pour fragment et extrémité d'un outil.
On ne peut pas les distinguer en lisant le rôle global « incomplet ». Il faudra
tester une recapture locale et son effet sur les outils, sans garde par longueur
cible ou séquence entière. Piste : ports terminaux et cohérence des appariements
des voisins directement liés ; coûts et séquestration à comparer avant bain.
Cette piste est conçue, pas implémentée ou validée dans ce lot.

Prochain jalon T9 : motif de finition et contrôles négatifs sur outils complets,
puis transfert sous chimie commune. Automatiser les comparaisons de variantes,
graines et critères fixés à l'avance, avec arrêt si le succès en fragment détruit
l'activité des outils. Pas de nouveau balayage d'inventaires ou de rates sans
ce diagnostic. Maintien, L fabriqué, génome long et bibliothèque restent ouverts.

Validation :99 tests logiciels et7 historiques passent. Six états initiaux N2
appariés vérifiés, ancien moteur reproduit exactement, reprise entre ticks
indépendants exacte, suivi bloqué sur cohorte incomplète, pas de double lancement,
arrêt après critère sans alerte. Pilote N2 every20,t2 :2 produits catalysés,
zéro incorporation/G/F/contact L, contrôle technique seulement.
