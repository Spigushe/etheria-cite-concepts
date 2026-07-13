# Changelog

Toutes les évolutions notables de ce wiki sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

## [Non publié]

### Ajouté

- Export PDF de la documentation (plugin `mkdocs-to-pdf`), généré au
  build et publié sur la Release GitHub associée au tag, aux côtés
  d'une archive `.zip` du site complet.
- Nouvelle identité visuelle « parchemin » : trois palettes (épuré,
  parchemin, mystère) pilotées par le toggle de thème Material,
  polices Cormorant Garamond (titres) et EB Garamond (corps),
  nouvelle feuille `docs/stylesheets/extra.css`.

### Modifié

- Workflow de déploiement (`.github/workflows/deploy.yml`) : mise à
  jour des actions (`checkout@v6`, `upload-pages-artifact@v4`), ajout
  de `configure-pages`, permission `contents: write` pour créer/
  compléter la Release et y attacher le PDF et l'archive du site.
- Exclusion de `.venv`, `.mypy_cache` et `.ruff_cache` des vues
  fichiers/recherche de VS Code.
- Callouts (`docs/stylesheets/callouts.css`) adaptés aux trois
  nouvelles palettes : fond dérivé de `--callout-color` via
  `color-mix`, bordures anguleuses, texte forcé sur
  `--md-default-fg-color` pour rester lisible dans chaque style.

### Corrigé

- `mkdocs serve`/`build` en local plantait sous Windows : le plugin
  `to-pdf` est importé dès le chargement de la config (même désactivé
  par `enabled_if_env`), et son dépendant WeasyPrint requiert des
  bibliothèques natives GTK (`gobject`, `pango`...) absentes par
  défaut sur Windows. Nouvelle config `mkdocs.dev.yml` (hérite de
  `mkdocs.yml` sans `to-pdf`) à utiliser en local via
  `python -m mkdocs serve -f mkdocs.dev.yml` ; `mkdocs.yml` reste
  utilisé tel quel par le CI. README mis à jour en conséquence.

## [0.7.0] - 2026-07-13

### Ajouté

- Bestiaire de menaces conceptuelles (trois par quartier, dont deux
  inédites), intégré directement dans chaque fiche de quartier en
  callouts `[!DANGER]` plutôt qu'en page séparée.
- Dictionnaire `cspell.json` complété avec l'ensemble des noms propres
  et du vocabulaire du projet (philosophes, factions, PNJ, jargon FATE).

### Modifié

- Fusion de la section « Le monde » et de « Quartiers » en une seule
  section « Univers d'Éthéria », `docs/quartiers/` déplacé sous
  `docs/monde/quartiers/`.
- Correction du dictionnaire `cspell.json` : le champ `import` était
  vide, empêchant le dictionnaire français `fr-fr` de charger
  réellement (des milliers de faux positifs sur des mots français
  ordinaires).
- Deux fautes corrigées (`precises` → `précises`, `reconcevoir` →
  `repenser`) trouvées en passant le wiki au crible de `cspell`.
- README entièrement réécrit pour refléter la structure réelle du
  projet (l'ancienne version décrivait encore `pitch/`, `cosmologie/`,
  `geographie/`, des dossiers qui n'existent plus).
- Le workflow de déploiement (`.github/workflows/deploy.yml`) se
  déclenche désormais sur un push de tag (`v*`) plutôt qu'à chaque
  push sur `main`.

## [0.6.0] - 2026-07-13

### Ajouté

- Affichage dynamique du numéro de version sur la page d'accueil, lu
  depuis ce changelog via un hook MkDocs (`scripts/version.py`).
- Fichier `cspell.json` à la racine du projet : langue `fr` et
  dictionnaire `fr-fr`, pour partager la config de vérification
  orthographique entre l'éditeur et un futur check en ligne de
  commande/CI.
- Page « Transitions entre quartiers » (`mj/campagne/transitions-entre-quartiers.md`) :
  trois événements courts par paire de quartiers, pensés pour
  s'insérer entre deux aventures au moment où le groupe franchit un
  seuil.
- Section « Sécurité de table » sur la page d'accueil de l'Espace MJ
  (`mj/index.md`) : présentation des thèmes sensibles, Carte-X et
  signaux de table plus légers, tour de table de fin de séance.

### Modifié

- Ajout de détails pour les aventures de la campagne (`mj/campagne/*`)
  et structure sous forme de tableaux (Accroche, Scènes clés, Bascule,
  Dénouements possibles, Portée) pour une lecture plus rapide en session.
- Déplacement de la configuration cSpell (`cSpell.language`,
  `cSpell.words`) de `.vscode/settings.json` vers `cspell.json`.
- Enrichissement des connexions entre quartiers (`quartiers/index.md`)
  avec des liens croisés supplémentaires (tensions, affinités,
  curiosités) au-delà des paires déjà décrites.
- Ajout d'une règle à tester sur la réputation philosophique comme
  actionnable (aspects libres, adversité à contre-courant) dans
  `mj/systeme.md`.

## [0.5.0] - 2026-07-12

### Ajouté

- Rédaction complète des sept fiches de quartier (ambiance, PNJ,
  dilemmes, mythes, connexions) et mise à jour de la cartographie du
  monde.
- Page « Ressources MJ » (aides de jeu, supports imprimables).
- Les sept aventures de campagne prêtes à jouer, une par quartier, et
  les quêtes transversales, ainsi que l'accueil de l'Espace MJ.

## [0.4.0] - 2026-07-12

### Ajouté

- Fiche de personnage de l'Aventurier Philosophe (FATE) et système de
  jeu : réputation philosophique sur cinq axes de tension, dilemmes.

### Modifié

- Réorganisation de l'arborescence (`systeme/` → `mj/systeme.md`,
  `pitch/` → `monde/pitch.md`, `annexes/` → `mj/annexes/`) et mise à
  jour des liens internes.
- Correction de la navigation de `mkdocs.yml` et ajout de `site/` au
  `.gitignore`.
- Retrait de la page « Accueil MJ » tant qu'elle n'était pas rédigée.

## [0.3.0] - 2026-07-12

### Ajouté

- Espace Pédagogie : concepts philosophiques par quartier et fiches
  des vingt-deux sources et auteurs (Aristote, Bentham, Camus,
  Confucius, Foot, Hobbes, Kant, Locke, MacIntyre, Mill, Nietzsche,
  Nozick, Parfit, Plutarque, Rawls, Ricœur, Rousseau, Sartre, Sen,
  Singer, Thomas d'Aquin, Thomson).
- Vue d'ensemble des sept quartiers d'Éthéria et navigation associée.
- Classe d'admonition `[!MJ]` pour les informations hors-fiction
  réservées au meneur.
- Blasons et icônes illustrant chaque concept philosophique par
  quartier.

## [0.2.0] - 2026-07-12

### Ajouté

- Le monde : introduction, histoire, cartographie, personnages
  emblématiques.
- Le pitch : ton, ambiance, thèmes centraux, spécificités de
  l'univers.

## [0.1.0] - 2026-07-12

### Ajouté

- Mise en place du template MkDocs + Material for MkDocs.
- Extension Markdown maison pour les callouts façon Obsidian
  (`> [!VILLE]`, `> [!PNJ]`, `> [!FACTION]`, `> [!REGLE]`,
  `> [!NOUVELLES]`, `> [!DANGER]`, `> [!SECRET]`, `> [!INTRIGUE]`,
  `> [!TRESOR]`).
- Déploiement automatique sur GitHub Pages via GitHub Actions
  (`.github/workflows/deploy.yml`).
- Structure de base des sections du wiki (`docs/`).
- README détaillant l'installation locale et la publication.
