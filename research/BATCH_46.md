# Lot46 — isoler l'instabilité, filtrer son coût local, rejeter un faux régulateur

5 novembre2026. Intégration du candidat compact et examen d'un risque conceptuel
indépendant. Aucun nouvel outil, gène, alphabet, port ou scheduler. Voir le
[plan figé](BATCH_46_PLAN.md), les [résumés vérifiables](BATCH_46_RESULTS.json)
et les recettes avec leurs empreintes. Les données complètes restent locales.

## Résultats clos, sans changer les portes

| Série | Résultat | Conclusion permise |
| --- | --- | --- |
| CX1,3/3 à2400 | Fermeture tardive.9575/.9600/.95938 ; G4/9/11,F7/12/11,L22/22/23 ; zéro insertion | La synthèse n'ouvre pas à elle seule ces frontières ; enlever l'échange préserve production et stabilité, mais ne renouvelle pas la membrane |
| CW1,3/3 à2400 | Insertions0/5/14 ; fermeture.2267/.95473/.92667 ; T tardive.37638/.08560/.08509 | Deux transferts, mais porte de fermeture refusée. La variante ne peut pas être promue |
| PI1,15/15 à400 | Produits F01 préparés4/16 : occupation G nulle dans toutes les graines ; certains témoins F déliés se fixent | Aucune rétroaction directe par fixation des produits dans ces lois ; pas un test d'homéostasie |

CW1 graine0 a262 échanges contre10/2 dans les autres, première température>.2
à1938.5. Il ne faut ni ralentir Langevin, ni cacher la graine, ni poursuivre une
grille de largeurs. CL1 avait montré une hausse locale de potentiel+6.0243 au
premier échange de CB1. Ces éléments motivent un changement de transition, sans
prétendre démontrer que toute chaleur de CW1 provient de ce seul mécanisme.

PI1 devait isoler une condition nécessaire d'un frein possible : occupation G par
F déjà fabriqué. Les cas linked/split ont mêmes billes, positions, vitesses et
RNG initiaux ; les doses ne sont pas appariées en hasard. Production/ligation
désactivées dans tous les cas, pas de L/HT ; une autre configuration que le bain
productif, sous ablations communes. L'audit passif compte une approximation
pré-réaction à un tick de retard, pas un hazard exact. **L'interdit était pourtant
statique** : monomer_only_capture et absence de gf_end_capture excluent F de degré
de squelette>0. Tous les produits F01 ont ce degré ; allonger le calcul ne pouvait
pas les rendre admissibles. Cette vérification aurait dû précéder les15 essais.
Le précontrôle courant construit des contacts orientés et appelle le véritable
GeneticAudit : produits exclus, monomères admissibles. Il bloque une répétition
de PI1 ; les recettes antérieures restent intactes. CAMPAIGN_CALIBRATION exige
désormais cette vérification lorsque réalisable.

## Construction EG1 — filtre énergétique d'un échange, pas une insertase

Une proposition géométrique/cinétique garde ses taux et coupures. Son coût
deltaU est calculé à positions fixes : continuation du contact formé moins
retiré, potentiels libres modifiés des trois L et voisins à portée, différence
de barrière P/R des deux segments. Acceptation1 si deltaU<=0, sinon
exp(-deltaU/T), avec la température existante. Forces, largeur.6, bruit Langevin,
pas de temps et états initiaux CW1 inchangés. Pas de téléportation ou d'assemblage
identifié globalement. Zéro lecture d'origine, contour ou objectif biologique.

Coût : un gate et un calcul de potentiel local supplémentaires, aucun paramètre
numérique, port, état, gène ou type supplémentaire. Les statistiques de
propositions/refus/acceptations sont passives et checkpointées. Réutilisation
dans d'autres échanges espérée, pas démontrée ; calcul du voisinage à mesurer
sur les vrais essais. Pas de detailed balance globale : ruptures spontanées,
aides de synthèse et travail du cycle externe ne sont pas tous équilibrés ainsi.
Le callback de barrière est obligatoire si celle-ci existe, pour éviter un bilan
silencieusement incomplet. L'option est désactivée par défaut, pas promue partout.

Contrôles microscopiques : delta local égal au changement de potentiel complet
avec voisins extérieurs et barrière P/R ; signe inverse en échange inverse ;
à T0 une hausse est refusée et la baisse acceptée sans mouvement forcé ;
observateur retiré sans effet et reprise de checkpoint exacte.

Pilote100 en graine0 : invariants0, fermeture temporelle.945, T75–100=.08592,
3 L nouveaux en67.25s. Zéro proposition d'échange : ce pilote vérifie l'état
initial/la stabilité courte, pas la nouvelle fonction. La cohorte EG1 comprend
3 graines à2400,2 travailleurs, budget3h, checkpoints30s, rapport puis arrêt.
Portes préannoncées : fermeture tardive>=.8 et T<=.12 dans chaque graine,
insertion sur au moins2 graines, médianes G/F/L positives et>=moitié de CW1,
invariants0 et comptabilité du gate. Aucun résultat ou adoption anticipés.

Suivi : `energy_exchange_status.bat`, arrêt/reprise par les scripts associés.
Les études utilisent le contrôleur existant, des sources figées et un routage
autoritaire par le type déclaré dans le job. Pas de réglage/retry/phase cachée.

## Conséquences conceptuelles et maturité

Le scénario « produit F se refixe à G et freine l'expression » n'est pas disponible
dans le candidat. Ne pas activer une option pour l'obtenir sans examiner pièges et
parasites. Une alternative sans outil est production limitée par substrats/sites,
pertes locales et recyclage/export. Elle donne un bilan qualitatif possible,
mais pas encore protection ou maintien de chaque espèce. Ces deux maillons restent
des gaps H-03/H-04 ; voir MACROMOLECULE_HOMEOSTASIS. RV1 reste une variante de
pertes séparée, pas une preuve de compatibilité avec le bain courant.

Aucun palier biologique n'augmente. M-04 reste25 sous-cas, H-03/H-04 restent0,
maintien intégré0. Les étapes locales d'insertion existent ; leur robustesse
et la fermeture énergétique restent à démontrer. Pas de cellule non naïve prête.
Prochain jalon discriminant : EG1 complet. S'il bloque l'insertion ou conserve
l'instabilité, analyser les propositions/énergies et reconsidérer le mécanisme
avant une autre constante. En parallèle, dessiner protection/pertes/export
avec les vrais états chimiques, sans présumer une rétroaction inexistante.

## Validation et visualisation

L'ajout du défaut explicite contact_exchange_gate=none requiert une normalisation
des comparaisons de configurations historiques ; premier passage245 tests : un
échec de cette comparaison, corrigé sans modifier la recette ou la dynamique.
Le passage final réussit **246 tests** ; le contrôle natif valide les **33 démos**,
chargement en pause, lecture/recommencement et identité avec le moteur. Journaux
locaux `outputs/batch46_tests_final.log` et `outputs/batch46_gui.log`.
Sept préfixes archivés MIN1R/MIN1M/MD2/L3/MX1/BI1/MX2 gardent états,
vitesses, chimie et RNG exacts à5 unités, gate désactivé. Cela vérifie la
compatibilité historique, pas l'adoption du gate dans ces sept chimies.

La GUI conserve CB1 « Intégration compacte · défauts connus » et33 choix.
Le nouveau candidat non évalué n'y remplace pas la référence ; les démos restent
sous Langevin. Les sources du lot sont intégrées au générateur de distribution.
