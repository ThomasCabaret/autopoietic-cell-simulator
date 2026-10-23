# Modèles dynamiques candidats

Les billes sont mobiles individuellement. Les assemblages ne sont plus des
objets rigides imposés. Le noyau mécanique commun additionne ressorts locaux,
potentiels d'angle sur trois billes, répulsions à courte portée et bruit brownien.
Le pas d'intégration est explicite, sans écrêtage des déplacements ; un grand
déplacement déclenche une erreur enregistrée. Quatre tests indépendants vérifient
les gradients des forces et le rejet de contours croisés par l'analyse.

Les deux cibles sont pour l'instant **deux modèles réactionnels candidats**, avec
des réglages et espèces différents. Leur coexistence sous un alphabet et une
table d'interactions uniques n'est pas démontrée.

## Copie : sous-unités composites et fermeture locale de quadrilatères

Chaque sous-unité préparée contient deux billes liées : un support B capable de
liaisons de squelette et un site Q de reconnaissance. Q possède deux variantes
pour l'information binaire. B et Q ont des fonctions primitives séparées.

Les Q peuvent se superposer ; les B se repoussent. Deux Q de même variante
peuvent s'apparier, un partenaire maximum par site. Leurs supports s'orientent
alors en sens opposés par un potentiel portant sur les quatre billes des deux
sous-unités. Les liaisons B-Q restent locales et déformables.

La primitive de ligation est intentionnellement favorable : une liaison B-B
existante, deux appariements de leurs Q voisins, et la géométrie adéquate peuvent
favoriser la liaison parallèle manquante entre les deux autres B. Ce motif lit
huit billes au maximum. Les ports sont saturables et opposés. Il ne lit aucune
séquence complète et n'attribue aucun rôle parent/copie. Une liaison nouvellement
formée devient immédiatement éligible comme support de ce même motif.

Il s'agit donc d'une **opportunité de ligation templée explicitement définie au
niveau local**. L'assemblage spatial, la séquence copiée, la complétion et la
libération résultent ensuite de la dynamique. Nous ne prétendons pas avoir fait
émerger cette opportunité chimique depuis un simple potentiel isotrope.

Helpers explorés :

- L'occupation du squelette B voisin active Q : les monomères libres se
  séquestrent moins entre eux. Cette dépendance ne regarde qu'un voisin lié.
- Cycle externe fixe d'association/libération. Dans T4 : période 200, dont les
  15 dernières unités favorisent la déliaison et bloquent l'appariement. Les
  produits incomplets subissent exactement le même cycle que les copies complètes.
- Rigidité de squelette et concentration augmentées, chacune déclarée dans les
  paramètres. Le premier essai T2 avait produit surtout des dimères parasites.
- Coiffes : un troisième symbole structurel, distinct des deux symboles
  d'information, donne un support à un seul port. La règle de valence est locale.
  Cette branche cherche à limiter l'allongement parasite des extrémités.

Les polymères sont non orientés : la métrique reconnaît la séquence à inversion
près. La ligation exacte n'introduit pas encore de substitutions ; mesurer une
fidélité sous erreurs et mutations reste à faire. Une copie complète correspond
à un nouveau composant linéaire de la séquence initiale, entièrement constitué
de sous-unités initialement libres. Une copie libérée n'a plus aucun appariement
actif au moment de l'observation. Une ligation soutenue par une copie complète
ne prouve pas une seconde génération complète.

## Membrane : courbure d'un ruban composite à deux rangées

Chaque sous-unité est une paire H-T liée, préparée initialement. Les liaisons
latérales H-H préfèrent une longueur de 1 ; les T-T une longueur de 0.75. La
distance H-T préfère 0.65. Ces valeurs s'appliquent aux types élémentaires de
liaisons, sans identité de molécule ou de vésicule.

Les ressorts et angles locaux font courber un ruban de ces sous-unités, car les
deux rangées ne peuvent satisfaire simultanément leurs longueurs préférées en
restant droites. Pour un polygone régulier sans contrainte angulaire, la relation
géométrique est `l_H - l_T = 2*d*sin(theta/2)` ; le minimum du modèle complet est
aussi influencé par les potentiels d'angle et les fluctuations.

Des ports libres proches, correctement orientés et de même type peuvent former
une liaison. Le moteur ne sait pas si ces ports appartiennent aux extrémités
d'un même ruban : il ne calcule ni composantes connexes, ni aire, ni fermeture.
L'analyse seule reconnaît une boucle des deux rangées avec mêmes voisinages,
sans intersection propre des polygones et d'aire supérieure à 1.

La branche coopérative V5 ajoute un motif local de quatre billes : si les deux
contacts H-H et T-T sont simultanément possibles, leur liaison peut se former
ensemble. Il ne regarde que les deux liens H-T et leurs ports. Ce helper cherche
à éviter les associations décalées entre rangées. Il doit être comparé aux essais
où les contacts latéraux se forment indépendamment.

V4 part d'un ruban **déjà polymérisé et droit**. V2/V4fragments partent de petits
fragments séparés, de centres et orientations tirés au hasard, dans un espace
ouvert. V5 place des fragments dispersés dans une boîte finie et utilise le motif
coopératif ; V5free part de sous-unités séparées. Le confinement est une propriété
de l'environnement, pas une attraction vers une structure biologique.

V6 garde cette configuration et remplace l'attraction isotrope des ports libres
par des sites virtuels orientés. La position de chaque port est définie par sa
bille et son voisin directement lié H-T. Un potentiel gaussien de portée finie
entre ports applique ses forces et couples à ces deux billes réelles, via le
gradient de la géométrie du port. Les sites ne sont ni des molécules ajoutées ni
des recruteurs globaux. Le gradient force/couple a son test indépendant.

Dans V6, une graine sur les deux essayées assemble cinq fragments de trois
sous-unités en une boucle de 15 ; la sixième pièce reste séparée. La graine
différente et l'essai partant de sous-unités entièrement libres ne ferment pas
dans la fenêtre testée. Cette branche démontre une possibilité, sans établir
un assemblage robuste.

Une boucle formée n'est pas encore une vésicule fonctionnelle démontrée : la
rétention d'un contenu, la perméabilité sélective, le renouvellement de matière,
la rupture/réparation et la croissance ne sont pas encore vérifiés. Les liaisons
latérales de ce premier prototype ne se rompent pas spontanément.

## Traces et reproduction

Chaque dossier de `research/runs/` contient sa configuration, ses sources exactes,
leurs SHA-256, ses métriques et sa trajectoire NPZ. Les nouvelles exécutions
contiennent aussi `replay.py` pour relancer les sources archivées sans modifier
les preuves enregistrées. La configuration omet parfois les valeurs par défaut ;
celles-ci sont conservées dans les sources archivées. Les versions de NumPy sont
enregistrées. Les horloges et graines sont distinctes du cycle physique simulé.

`experiments/replay_local_run.py` vérifie les SHA-256 et rejoue également les
anciens dossiers, puis compare toutes leurs métriques. Ce rejeu a reproduit
exactement l'ancien essai court T2. Les trajectoires récentes de copie conservent
les appariements et les types de reconnaissance en plus des positions et liens.

Les incidents de placement initial et les erreurs de rendu sont distingués des
échecs chimiques. Les anciens essais restent conservés après modification du code.

## Lot 2 : familles G/F, préférences natives et provenance

Les deux billes d'une sous-unité restent localisées. La famille est une propriété
chimique de la bille support : G ou F. Les reconnaisseurs portent le symbole 0/1.
Un appariement de même symbole est possible entre G-G ou G-F, jamais F-F ; dans
G-F, G doit être localement polymérisé et F libre à la capture. Une arête G peut
fournir le motif de ligation parallèle ; une arête F ne le fournit pas. Les deux
candidats à la nouvelle liaison doivent avoir la même famille chimique. Le moteur
n'examine toujours aucune séquence ni identité de gène complet.

T7 ajoute un critère de capture symétrique : exactement un des deux supports a
déjà un voisin de squelette. Les appariements existants ne sont pas supprimés
lorsque le monomère entrant est ligaturé. E0 applique cette opportunité aux pools
F. E2 ajoute une coopération bornée : les partenaires des voisins directement
liés au support G peuvent interdire la capture d'un entrant de l'autre famille.
Ce helper est déclaré ; il n'est pas une interaction purement deux à deux.

E1 donne aux angles locaux F un cosinus préféré de +0,3 pour le symbole 0 et
−0,3 pour 1. La valeur est masquée à zéro lorsque le reconnaisseur de cette
sous-unité est apparié, puis redevient native après déliaison. Une seule table
locale s'applique à toutes les séquences. Les géométries observées ne sont pas
des fonctions catalytiques : aucun substrat ni réaction supplémentaire n'est
introduit dans ces essais de forme.

L'observateur distingue copies G et produits F. Il certifie une génération
seulement si chaque arête du descendant provient du même parent complet, déjà
observé et toujours intact au moment des événements. Les supports fournis au
départ ont le rang zéro. Les produits d'origines mélangées peuvent être complets
sans être certifiés. Cet historique n'est jamais accessible à la dynamique.
Les anciens essais sans cette métrique sont « non mesurés », pas zéro.

La traduction G→F est directe symbole à symbole. Les familles servent à des
compatibilités de liaisons et d'appariement ; elles ne désignent pas des enzymes
ou des fonctions moléculaires entières. Les sous-unités G/F et celles de membrane
sont encore toutes fournies préparées. Le réseau C0 de CELL_ARCHITECTURE.md est
un audit abstrait séparé et n'ajoute aucune réaction macro à ce moteur.
