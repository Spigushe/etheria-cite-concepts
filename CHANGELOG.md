# Changelog

Toutes les évolutions notables de ce wiki sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

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
