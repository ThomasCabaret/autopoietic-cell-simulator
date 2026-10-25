# Lot7 — graphe causal, interactions et taille de cellule

25 octobre2026. Lot de conception/audit demandé par l'utilisateur, **sans nouvelle
preuve dynamique moléculaire**. Livrables : [architecture](CELL_ARCHITECTURE.md),
[matrice d'interaction](CELL_INTERACTIONS.md), [spécification](minimal_cell_spec.json),
[tests à réaliser](INTEGRATION_TESTS.json).

Le schéma initial C0 existait mais ne détaillait pas les contacts, l'insertion,
les stocks ni la taille compatible avec la courbure. Il est conservé comme
historique. Nouveau candidat minimal :3 gènes fragmentés et3 synthétases N/A/L,
énergie activée fournie de l'extérieur ; copie et traduction directes restent
des opérations primitives proposées. Un rôle d'activation interne n'est donc
pas obligatoire ici. Insertase ou activation interne impliquent chacune un gène
et un outil supplémentaires, avec leur renouvellement.

L'audit AND/stœchiométrique passe pour ce cahier des charges conditionnel et
détecte10 contre-exemples. Six tests logiciels vérifient notamment la mauvaise
famille de monomère malgré même masse, la perte d'une expression, l'insertion,
la géométrie et le coût d'un rôle supplémentaire. Reconstruction depuis les
sources et la configuration archivées : toutes les valeurs identiques.

**16 espèces cibles**, quatre sortes matérielles primitives mais plusieurs états
de liaison/polarité/énergie. Complexes, fragments et séquences parasites ajoutent
des possibilités :16 n'est pas le nombre total de molécules que la chimie permet.
Budgets de travail :**1 020 / 2 406 / 6 292 billes**, avec126/219/458 lipides
dans la frontière. Les longueurs12/24/48 et stocks sont des hypothèses explicites,
non des protéines déjà conçues. Une insertase porte le nominal à18 espèces et
2 726 billes ; activation plus insertase :20 espèces et3 044 billes.

Le calcul révèle une incompatibilité géométrique à tester : V8curved préfère
environ11,5 unités et un rayon1,53, contre34,4 pour le budget nominal. Augmenter
le nombre d'unités ne corrige pas cette préférence. Une frontière préparée,
faiblement courbée et capable d'échange doit être testée avant intégration.
N/A de même composition, perméabilité selon l'état lié/libre et incorporation
dans un anneau saturé deviennent des obligations explicites, avec tests de
réactions parasites et d'encombrement sous lois figées.

## Décisions et suite

Conserver la cible à3 rôles comme plan minimal, sans prétendre la chimie actuelle
capable de la réaliser. C3B et I0 doivent tester un vrai flux de composant utile
et la sélectivité entre produits. En parallèle de priorités, I2/I3/I4 décrivent
le prochain risque membranaire : grande frontière, insertion intérieure, fuite.
T9/I1 portent le risque génétique multigène. Pas de nouvelle exploration isolée
sans lien à ce réseau et à un produit utilisable par la suite.

Maturité : cahier des charges global mieux contraint ; progrès moléculaires
inchangés depuis le lot6. Santé conditionnelle : pas de contradiction de principe
identifiée, mais les courbures et la sélectivité actuelles ne suffisent pas.
Les décisions I0–I4 doivent éviter une longue accumulation d'ajustements.

Reproduction :

```powershell
python experiments/audit_cell_design.py
python experiments/render_cell_design.py
python -m unittest discover -s tests -p test_cell_design.py -v
python scripts/reconstruct_experiment.py research/abstract_runs/C0B_20261025T075945112877Z
```

La recette archive le code exact et le hash de configuration. Les sorties
complètes restent locales ; seuls configuration, sources, recette et synthèse
sont versionnés. Aucun fichier d'une ancienne expérience n'est modifié.
