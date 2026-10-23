# Premier dépôt Git

Depuis PowerShell, pour un dépôt GitHub vide à l'adresse indiquée :

```powershell
cd C:\CodeProjects\autopoietic_cell_simulation
git init -b main
git add .
git status --short
git diff --cached --stat
git commit -m "Initial commit: simulator, research notes and reproduction recipes"
git remote add origin https://github.com/ThomasCabaret/autopoietic-cell-simulator.git
git push -u origin main
```

Ces commandes sont fournies à exécuter : la préparation ne crée ni commit ni push.
L'authentification GitHub utilise le gestionnaire d'identifiants de Git installé
sur la machine. Si Git demande une identité d'auteur, renseigner les valeurs voulues
avec `git config user.name` et `git config user.email` dans ce dépôt, puis reprendre
le commit.

Le dépôt contient le code, les lois, les notes de recherche, les configurations,
les graines et les recettes de reconstruction. Les données restent sur le disque
local : trajectoires, checkpoints, résultats bruts et images de runs sont exclus,
ainsi que `outputs/`, `deliverables/`, environnements, caches et réglages locaux.
La méthode `.agents/skills/` et les sources historiques utiles restent incluses.
Voir [research/REPRODUCTION.md](research/REPRODUCTION.md).

Les commandes supposent que le dépôt distant existe et ne contient pas déjà
d'historique. S'il contient déjà des commits, inspecter cet historique avant
d'intégrer les fichiers ; ne pas remplacer un historique existant par un push forcé.

## Vérification de la préparation

Un dépôt temporaire dans `outputs/` a servi à simuler `git add` avec les conversions
Windows activées, sans créer de `.git` à la racine du projet :

- 419 fichiers suivis, environ **2,9 Mio** au total ; aucune donnée brute de run.
- 57 recettes, leurs paramètres et leurs sources exactes sont versionnés.
- 356 fichiers protégés du moteur et des archives comparés aux blobs Git.
- Reconstruction depuis les seules entrées de trois formats d'essais (ancien moteur,
  moteur partagé et audit abstrait) : mêmes métriques et tableaux enregistrés.
- Les données locales existantes sont conservées ; `git diff --cached --check`
  passe et le dépôt principal n'est pas encore initialisé.

Ces contrôles portent sur le dépôt local à préparer ; l'état du distant et
l'authentification du futur push n'ont pas été interrogés.
