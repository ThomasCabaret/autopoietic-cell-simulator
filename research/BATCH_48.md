# Lot48 — EN1 refusé, bilan ciblé et protection cohérente

5 novembre2026. [Plan](BATCH_48_PLAN.md), [preuves compactes](BATCH_48_RESULTS.json).
Deux fronts séparés, sans nouvelle protéine ou taux numérique.

## EN1 clos : la robustesse ne suit pas la réussite limitée EG1

| Graine | G / F / L nouveaux | L insérés nés dedans | Fermeture tardive | T tardive |
| --- | --- | --- | --- | --- |
| 0 | 7 /7 /23 | 0 | 94,54 % | .08996 |
| 1 | 6 /10 /22 | 0 | 94,66 % | .08780 |
| 2 | 8 /9 /23 | 2 | 58,98 % | .15167 |

Trois essais complets sans erreur/invariant, porte refusée. Production préservée,
mais insertion insuffisante et troisième graine chaude/ouverte. Pas de nouveau
choix de dt ou de relance de graines pour sauver le résultat. Les3 mêmes graines
ne représentent pas des bruits appariés entre discrétisations ; rien ne distingue
encore une variation stochastique d'un effet numérique systématique.

Les graines0/1 ont zéro face de capture nouveau/ancien éligible. Leurs4/2
propositions d'échange ont toutes deltaU>0 et sont refusées ; sommes des facteurs
thermiques.0370 et3,56e-7. Ce sont des occasions rares et défavorables dans cet
horizon, pas une simulation incapable d'exécuter une réaction. Le rapport garde
ces absences censurées, pas des taux asymptotiques nuls.

Graine2 : température moyenne par fenêtre100 reste proche.08–.096 jusqu'à2100,
puis.1505/.2813/.2211 sur les trois dernières fenêtres. Premier T>.2 après1000
à2173.5, avant le premier échange après2000 à2177.63. Aucun PR/H/T ne naît
pendant ce début de hausse : PR précédent2063.68, H/T suivant2373.53. Cela exclut
leur commutation simultanée comme déclencheur, pas une énergie stockée auparavant
ni les transitions de contacts ou autres cycles génétiques.

## EL1 : bilan de transitions de contact, passif et borné

Rejeu source figée EN1 s2 jusqu'à2200 ; seule fenêtre après2100 instrumentée.
Les changements update_faces (ruptures/formations) et exchange_faces sont
mesurés séparément à positions fixes : potentiel des ports et barrière P/R.
Un clone à2100 vérifiera état, vitesse, RNG et observateur à2200 ; préfixes
observés historiques recoupés. Potentiel observé égal aux noyaux réels sur un
microcas avec barrière, sans mutation ; tolérance numérique1e-12 pour les sommes.
Un pilote distinct0–2 sous la sonde figée exerce deux transitions de contacts :
clone et préfixe historique exacts,20 échantillons cinétiques. Cela teste la
sonde, pas la fenêtre chaude ; son rapport brut a hérité du texte de portée
du plan principal, intervalle effectif déclaré dans BATCH_48_EL1_MICRO.json.

Pas de coordonnées globales enregistrées : température cinétique par classes
de matière initiale toutes.1 unité, au plus2000 événements et seules positions
des billes affectées par le plus grand saut. Le marquage initial est observer-only.
Checkpoints/statut/pause exposés, budget2700s, rapport puis arrêt. Pas de feedback
des mesures, de nouveau thermostat ou de chimie ajoutée. Ce bilan partiel ne
garantit ni conservation énergétique globale ni causalité d'un facteur isolé.
Si le bilan n'explique pas la phase chaude, revenir aux forces/autres cycles.

## RP1 : protection par un motif apparié, séparée du bain EG1

Le nouveau prédicat de perte de squelette lit seulement une liaison (a,b),
les deux partenaires appariés x,y, la réciprocité de ces appariements et le
lien direct (x,y). Quatre composites/huit billes au maximum ; aucun test de
longueur, séquence entière, nom de gène, origine ou fonction. Une capture de
nourriture seule ne protège plus ce squelette dans cette variante. La perte
P–R garde exactement son garde local antérieur : degré nul et ports inoccupés.

Les quatre taux et le facteur.05 de RV1 protected sont inchangés. Coût : un
choix de prédicat local alternatif (`protection_scope=paired_edge`), pas de
nouveau nombre, type, port, gène ou outil. Défaut historique `occupied` conservé
sans nouveau tirage. Réutilisation pour les duplex espérée, pas démontrée ;
dette cinétique/thermique du turnover conservée. Une fonction biologique n'est
pas identifiée par une primitive. Les témoins capturés/non réciproques/non liés
rejettent la protection ; le vrai hook garde les liaisons appariées et détruit
celles dont seule la capture est occupée dans un contrôle de taux forcé.

Passivité et reprise exactes contrôlées. Rejeux5 unités RV1 full/protected
historiques sous code courant : positions, vitesses/état mécanique, chimie et
RNG exacts. Cela vérifie la compatibilité du défaut, pas la supériorité de RP1.
Campagne figée3 graines à1200,1 travailleur,1h/checkpoints30s ; porte annoncée
dans le plan, rapport puis arrêt. Census réversible et deux atomes réellement
recyclés, jamais lineage irréversible. Aucun transfert vers EG1 ; la configuration
mixte continue à refuser un turnover non validé. Les risques d'extinction des
outils actifs et de protection des fragments appariés restent explicitement ouverts.

## GUI, validation et maturité

Le menu **Intégration compacte · contrôle au pas fin** expose les trois EN1,
y compris la phase chaude de la graine2. EG1 reste la référence par défaut
avec avertissement EN1 dans sa fiche ; aucune variante refusée n'est promue.
39 choix et mêmes lois que leurs recettes. Les compteurs ne pilotent rien.

**256 tests complets passent,39 démos natives vérifiées** : chargement en pause,
lecture/recommencement et positions égales au moteur, y compris EN1 s2.
Les vérifications complètes/natives sont consignées dans les journaux locaux
`outputs/batch48_tests.log` et `outputs/batch48_gui.log`. Registre18 régénéré
à la clôture. Le premier contrôle de somme d'énergie exigeait exactement0 et
refusait un arrondi1,8e-15 ; tolérance1e-12 ensuite, aucune porte scientifique
modifiée. M-04 conserve75 pour le seul domaine EG1 déjà observé, avec refus
EN1 désormais explicite ; aucune robustesse revendiquée. Q-01/C-02 restent25,
W-02/W-03 restent25 et H-06 reste0. Pas de palier augmenté par RP1 ou EL1 en cours.
Le projet progresse par séparation des mécanismes ; maintien, information,
régulation/protection et diversité restent des verrous de recherche.

**Calculs lancés :** `pair_protection_status.bat` (RP1) et
`contact_heat_status.bat` (EL1), chacun avec arrêt/reprise associés.
L'état réel à la remise de main doit être relu ; aucune seconde phase automatique.
