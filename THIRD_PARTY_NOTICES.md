# Référence historique conservée

`research/legacy_reference/source/` contient une sélection non modifiée des fichiers
du projet historique fourni comme référence. Sa licence d'origine est conservée
dans [research/legacy_reference/source/LICENSE](research/legacy_reference/source/LICENSE).
Elle porte la mention **Copyright (c) 2018 HackerPoet** et le texte de la licence MIT.

L'inventaire des fichiers et leurs empreintes se trouvent dans
`research/legacy_reference/manifest.json`. Cette sélection n'est pas une distribution
compilable complète de l'ancien projet ; ses limites sont décrites dans
`research/LEGACY_PROJECT_NOTES.md`.

Ce texte documente la référence et ne réattribue pas sa propriété. La licence de
cette référence n'est pas déclarée comme licence globale du nouveau simulateur.

# Dépendances graphiques optionnelles GUI1

`requirements-viewer.txt` référence PySide6 (Qt for Python) et ModernGL, installés
séparément et non copiés dans le dépôt. Les métadonnées des distributions testées
indiquent : PySide6 6.8.3, `LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only` ;
ModernGL 5.12.0, MIT. Les textes de licence de ces distributions restent fournis
par leurs paquets. Le présent dépôt distribue son client et ses shaders, pas
une copie des bibliothèques Qt ou des pilotes OpenGL.
