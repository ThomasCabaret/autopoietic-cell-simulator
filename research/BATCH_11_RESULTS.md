# Contrôles longs M1R — résultats

27 octobre2026. Six essais à1500 achevés sans erreur. Le postprocesseur vérifie
le census, les durées et les sources ; les trois B retrouvent toutes métriques,
positions finales, PRNG et état chimique de K1. Recette exacte dans
`campaign_recipes/M1R_20261026T165544113247Z/`, données locales conservées.

| Échange | Graine | Fraction fermée | Fraction classable | Inconnus | Dimères incorporés | Sorties observées /24 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Désactivé | 0 | 0,851 | 0,984 | 1,57% | 0 | 0 |
| Désactivé | 1 | 0,850 | 0,988 | 1,23% | 0 | 0 |
| Désactivé | 2 | 0,844 | 0,988 | 1,17% | 0 | 0 |
| B, taux0,2 | 0 | 0,590 | 0,718 | 28,22% | 1 | 0 |
| B, taux0,2 | 1 | 0,805 | 0,978 | 2,17% | 2 | 0 |
| B, taux0,2 | 2 | 0,826 | 0,978 | 2,23% | 5 | 0 |

Sans échange, les épisodes non classables sont brefs : plus longue séquence
échantillonnée de cause inconnue≤0,5. Pendant ces périodes inconnues, les extrémités ont un autre bout
à proximité (maximum des plus proches distances1,06–1,12). Cela n'établit pas
une étanchéité, mais ne ressemble pas à un grand trou durable. Les ouvertures
classables et les ruptures thermiques ordinaires restent fréquentes.

Dans B0,752 échantillons sont à grand écart terminal,93 fragmentés et2 croisés.
L'épisode de grand écart le plus long dure17,5 entre première et dernière image,
contre0 dans les trois témoins pour cette cause. Les extrémités les plus isolées
peuvent être à3,83 de leur voisin le plus proche. B1/B2 restent bien plus proches
des témoins. L'échange paraît donc exposer à une voie rare de défaut prolongé ;
la comparaison de trois graines ne donne pas un taux général d'échec. Les flux
de sondes pendant les périodes inconnues restent non mesurés : le zéro de sortie
observée de B0 ne devient pas une preuve de rétention.

Le journal B0 associe la phase dégradée au remplacement208–209 par209–232 à787,56,
finalement inversé à1236,11. Plusieurs autres échanges ont lieu entre-temps.
Entre ces deux événements, les897 images ont au moins une extrémité distante
de plus de1,35 de tout autre bout ;824 sont non classables. Avant cette phase
et après, aucune image de B0 ne dépasse ce seuil géométrique. C'est un indice
de défaut prolongé plus précis qu'un simple petit fragment transitoire.
Une proximité temporelle n'identifie pas à elle seule la cause locale ; la suite
sélectionne ce cas pour un traçage des seuls participants, sans changer les lois.

## Décision

Le risque a été localisé : le candidat tient sans échange sur ces trois essais,
mais la voie d'insertion peut produire un état qui se referme mal. Ne pas réviser
les seuils ni ajouter de pression globale. Prochain : géométrie et occupation
des faces lors d'un échange réussi et d'un échange défectueux, puis un garde
strictement local seulement si ces traces en montrent la justification.

Aucun nouveau type ou helper physique dans ce lot. Maturité : frontière préparée
avec sélection de sondes et insertion isolée obtenues, maintien conjoint encore
fragile, aucune intégration G/F. Une nouvelle intervention de conception reste
justifiée par ce diagnostic nouveau ; éviter un simple balayage de constantes.
