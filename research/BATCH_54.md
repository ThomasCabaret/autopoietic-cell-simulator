# Lot54 — refus interprétés et récupération fonctionnelle ciblée

6 novembre2026. [Plan](BATCH_54_PLAN.md), [audit FA1](BATCH_54_FA1.json),
[preuve compacte](BATCH_54_RESULTS.json), [campagne FR1](BATCH_54_FR1_RECIPES.json).

## Deux campagnes achevées ; leurs portes ne sont pas assouplies

PT1 termine6/6 sans erreur technique. Température, validité majoritaire et
témoins transparents passent. Les deux contours finaux classables avec barrière
retiennent tous les atomes assemblés tandis que58–60% des libres sont dehors ;
les témoins ont39–78% des assemblés dehors. Mais graine1/barrière finit **ouverte** :
51 liens/52 L, extrémités distantes de.639, grande aire203.46 et chaîne simple.
Dernier contour valide à299.5, ouverture observée à300. Refus maintenu :
inconnu n'est ni fuite mesurée ni bonne étanchéité. Les zéro traversées assemblées
échantillonnées n'excluent pas un passage dans une période non classable.

RF1 termine9/9 sans erreur technique ; les deux protections refusent le crible.

| Variante | G01 finaux | F01 finaux | Catalyse900–1200 | Réassemblages stricts | Réincorporations strictes |
|---|---|---|---|---|---|
| zero | 13/13/11 | 13/11/12 | 0/0/0 | 0/0/0 | 0/0/0 |
| occupied | 10/5/15 | 4/0/8 | 42/0/39 | 0/0/2 | 0/0/0 |
| paired_edge | 12/5/15 | 1/0/8 | 37/0/38 | 0/0/0 | 0/0/0 |

Bilans atomiques valides. Températures tardives de graine2 avec pertes.1224/.1254
dépassent le seuil.12 ; pas de refroidissement ou de changement de seuil.
Le témoin zero est presque épuisé, donc son inactivité tardive ne démontre pas
une perte d'outils et empêche la comparaison d'activité prévue. Les graines1
avec pertes gardent64 P/64 R libres mais perdent tous leurs motifs F01 :
ici la pénurie de substrat n'explique pas l'inactivité. Les gènes G01 survivent.
L'absence de réincorporation stricte ne mesure pas toutes les formes possibles
de réemploi d'un fragment composite ; le critère exige les deux atomes libérés
puis réassemblés et incorporés. Aucun maintien ou recyclage complet acquis.

## FA1 : la dynamique des liaisons explique le choix de l'étape suivante

Analyse des journaux complets et checkpoints existants, sans nouveau calcul
dynamique. Chaque reconstruction retrouve exactement rungs, symboles et liens
de squelette finaux. Les appariements intermédiaires ne sont pas journalisés
complètement : les motifs ici sont structuraux, pas une mesure de disponibilité.

Dans les deux variantes graine1, l'unique lien F39–F40 casse à96.99 ; il reste
alors5 F0 et6 F1 actifs, ainsi que les gènes. Aucun motif ne revient avant1200.
Neuf monomères F avaient même été synthétisés avant cette perte : le problème
n'est pas l'absence totale de fabrication F. Dans paired_edge/graine0, perte
du dernier motif à289.66 puis retour à316.89 : récupération observée en27.23.
Cette trajectoire montre une possibilité sous les lois actuelles, pas sa robustesse.

Une hypothèse précise devient testable : les monomères F libres sont trop
éphémères relativement à leur capture/traduction. Leur demi-vie idéale non
protégée vaut69 pour le taux.01, face au cycle externe200. Cela ne remplace
pas les expositions réelles ni ne démontre la cause ; FR1 garde l'hypothèse falsifiable.
Pas de raison de lancer un nouveau balayage membranaire ou une cellule sous
pertes avant d'éclaircir cette fragilité du réseau.

## Construction et lancement de FR1

Scénario JSON, prévol, analyse et commandes de statut/arrêt/reprise dans le
gestionnaire existant ; aucun nouvel ordonnanceur ou fichier du moteur modifié.
150 atomes, G01 et stocks identiques à RF1 ; F01 fourni avec son lien absent.
Il n'y a aucun F polymère au départ. C'est un état de récupération construit,
**pas une reprise exacte du checkpoint à96.99**. L'absence de l'outil est une
perturbation sévère, plus exigeante que le départ équipé autorisé pour la cellule.

Trois graines × pertes P/R libres F `fast=.01` / `slow=.001`, durée600,
deux travailleurs/1h. Aucun outil supplémentaire ; une seule valeur change,
utilisant un taux déjà existant. La variante est séparée de CP1 ; helpers de
perte RV1, énergie non fermée, coût inchangé en règles/types/paramètres.
Les monomères plus stables pourraient aussi s'accumuler : stocks rapportés.

La porte, fixée avant lancement, demande reconstruction d'un F01 puis
catalyse effective dans au moins2/3 graines, conservation de G01 et seuil
thermique partout. L'audit génétique distingue rencontres GF, double appariement,
ligation et accès catalytique. Première reconstruction absente censurée à600.
Pas de porte de permanence tardive dans un stock qui peut s'épuiser, pas de
requalification rétrospective de RF1. Rapport puis arrêt, sans vainqueur ou
transfert automatique. **Statut : `functional_recovery_status.bat`.**

Neuf tests ciblés passent, dont vrai worker et audit, censure et portes non
vacuelles, préservation des atomes et ablation unique. Microbenchmark20 : audit
3.64→4.78s (×1.31), positions/vitesses/PRNG/état chimique exactement identiques ;
mesure sélectionnée, pas garantie de débit. **299 tests** de la suite complète
passent ; registre et inventaire CA1 vérifiés. Le refus initial des tests par
permissions du dossier temporaire Windows est conservé ; relance autorisée réussie.

## Maturité et décision

Progrès : deux refus transformés en diagnostics distincts et une hypothèse
locale ciblée ; récupération ponctuelle réellement observée dans RF1. Aucun
palier biologique relevé. Transport encore borné/incomplet, recyclage utile et
robustesse thermique refusés ; maintien0. CP1 fermeture CR1 reste acquise en
sous-bain, M-01=50 ; M-04=75 seulement EG1 historique limité. Les démos physiques
et leur bruit restent inchangés ; FA1/FR1 ne sont pas de nouvelles démos intégrées.

Prochain jalon : interpréter FR1 selon exposition/ligation/fonction. Si favorable,
exiger ensuite remplacement matériel entier actif et thermique avant transfert
des pertes dans CP1. Si monomères présents sans capture, changer le diagnostic
de conception plutôt que poursuivre une descente de taux. Diversité des outils,
information, régulation et flux/export restent conceptuellement ouverts.
