# Changelog

Ce wiki évolue au fil de l'écriture, et ce journal garde une trace de
ce qui change à chaque étape : ce qui s'ajoute, ce qui se corrige, ce
qui se réécrit.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et les numéros de version suivent la logique du
[Semantic Versioning](https://semver.org/lang/fr/).

## [0.10.0] - 2026-07-14

### Ajouté

- Page « Changelog » (`docs/changelog.md`) en toute dernière entrée de
  la nav (`mkdocs.yml`) : ce fichier y est injecté tel quel via un
  marqueur `{{ changelog }}` (`scripts/version.py`), pour rester
  consultable comme annexe à la fois sur le site et en tout dernier
  élément du PDF combiné généré par `mkdocs-to-pdf`.
- Page de dos (`back_cover: true`, `mkdocs.yml`) pour l'export PDF :
  logo affiché en grand format sur fond blanc, sans pied de page, via
  un template personnalisé (`docs/assets/templates/back_cover.html.j2`)
  et une feuille de style dédiée
  (`docs/assets/templates/styles.scss`, référencée par `cspell.json`),
  rangés aux côtés des autres assets plutôt qu'à la racine du projet
  (`custom_template_path` dans la config du plugin `to-pdf`).

### Modifié

- Fiches des dix-neuf sources (`docs/resources-philo/sources/`) : paragraphe
  ajouté à chacune, reliant le philosophe à un PNJ, un lieu ou un dispositif
  précis de son quartier (l'auto-icône de Bentham, le veilleur Camüs pour
  Camus, l'Aiguilleur Argos pour Kant, la Grille de la Balance pour Rawls,
  entre autres), en écho aux paragraphes symétriques ajoutés côté fiches de
  concepts.
- Fiches des sept concepts philosophiques (`docs/resources-philo/concepts/`) :
  paragraphe ajouté après la présentation du dilemme, reliant explicitement
  chaque PNJ du quartier au philosophe ou à la source qu'il incarne sans le
  nommer (Singer et Mill dans la Balance d'Orion, Aristote, Confucius et
  MacIntyre dans la Citadelle de l'Arêtê, Hobbes/Locke/Rousseau dans la
  Concorde du Pacte, Camus, Nietzsche et Sartre dans le Gouffre d'Absyr, Sen
  et Rawls dans les Jardins de l'Équité, Ricœur et Parfit dans le Labyrinthe
  des Identités, Kant, Foot et Thomson dans les Rails de la Décision).
- Portraits de PNJ des sept fiches de quartier (`docs/monde/quartiers/`)
  étoffés : d'un résumé d'une phrase à un paragraphe par personnage,
  avec anecdotes, lieux précis et tics de comportement.
- `docs/monde/histoire.md` et `docs/monde/personnages.md` réécrits en
  prose continue : les listes à puces et citations isolées laissent
  place à des paragraphes liés entre eux, avec davantage de renvois
  croisés entre cycles, figures, factions et quartiers.

## [0.9.0] - 2026-07-13

### Ajouté

- Cartes imprimables (`docs/mj/annexes/ressources-mj.md`) : quatre
  familles par quartier (événement, idée, pacte, lieu), générées au
  build par un nouveau hook MkDocs (`scripts/cards.py`) à partir de
  `docs/mj/annexes/decks-cartes.json` — recto en PNG pour les
  carrousels de la page, jeu complet en PDF recto-verso prêt à
  imprimer (traits de coupe, 63×88 mm). Rien de généré n'est stocké
  dans le dépôt.
- Carrousel JS (`docs/assets/javascripts/carrousel.js`) et styles
  associés (`docs/assets/stylesheets/extra.css`) pour parcourir les
  rectos de cartes directement dans la page.
- PDF combiné `toutes-les-cartes.pdf` (les sept jeux de quartier à la
  suite, dans l'ordre canonique de la page Quartiers), généré par
  `scripts/cards.py` et publié comme asset de Release aux côtés du
  PDF de documentation (`.github/workflows/deploy.yml`).
- Nouvelles dépendances `pypdfium2` et `reportlab` (génération des
  PNG/PDF), stubs `types-PyYAML`, `types-pytz`, `types-reportlab`
  pour `ty`.

### Modifié

- `docs/mj/annexes/ressources-mj.md` : la section « Cartes
  imprimables » sort du statut WIP, les exemples codés en dur sont
  remplacés par les decks générés ; la page réapparaît dans la nav
  (`mkdocs.yml`, section Espace MJ).
- `cspell.json` : `ignorePaths` généralisé à `*.css`, `*.py`, `*.yml`
  et `requirements.txt` (plutôt que lister les fichiers un par un).
- Logo d'Éthéria (`docs/assets/logo.png`) ajouté en en-tête du README
  et de la page d'accueil du wiki, et utilisé comme `logo`/`favicon`
  du thème Material (`mkdocs.yml`).
- Liens de téléchargement des PDF de cartes remplacés par des
  marqueurs `{{ cartes_pdf: <quartier> }}` / `{{ cartes_pdf_global }}`
  (`scripts/cards.py`) : générés en URL absolue pour rester
  compatibles avec la résolution de liens de `mkdocs-to-pdf`, et
  masqués dans `documentation.pdf` via une règle `@media print`
  (`extra.css`, classe `masque-en-pdf`) puisqu'un lien de
  téléchargement n'a pas de sens dans un PDF déjà imprimé.

## [0.8.0] - 2026-07-13

### Ajouté

- Export PDF de la documentation (plugin `mkdocs-to-pdf`), généré au
  build et publié sur la Release GitHub associée au tag, aux côtés
  d'une archive `.zip` du site complet.
- Nouvelle identité visuelle « parchemin » : trois palettes (épuré,
  parchemin, mystère) pilotées par le toggle de thème Material,
  polices Cormorant Garamond (titres), EB Garamond (corps) et Roboto
  Mono (code), nouvelle feuille `docs/assets/stylesheets/extra.css`.

### Modifié

- Workflow de déploiement (`.github/workflows/deploy.yml`) : mise à
  jour des actions (`checkout@v6`, `upload-pages-artifact@v4`), ajout
  de `configure-pages`, permission `contents: write` pour créer/
  compléter la Release et y attacher le PDF et l'archive du site.
- Exclusion de `.venv`, `.mypy_cache` et `.ruff_cache` des vues
  fichiers/recherche de VS Code.
- Callouts (`docs/assets/stylesheets/callouts.css`) adaptés aux trois
  nouvelles palettes : fond dérivé de `--callout-color` via
  `color-mix`, bordures anguleuses, texte forcé sur
  `--md-default-fg-color` pour rester lisible dans chaque style.
- Page d'accueil (`docs/index.md`) réécrite : ton plus direct pour
  l'intro et les deux portes d'entrée (Pitch / Le monde), mention des
  outils de sécurité de table dans l'encart Espace MJ.

### Corrigé

- `mkdocs serve`/`build` en local plantait sous Windows : le plugin
  `to-pdf` est importé dès le chargement de la config (même désactivé
  par `enabled_if_env`), et son dépendant WeasyPrint requiert des
  bibliothèques natives GTK (`gobject`, `pango`...) absentes par
  défaut sur Windows. Nouvelle config `mkdocs.dev.yml` (hérite de
  `mkdocs.yml` sans `to-pdf`) à utiliser en local via
  `python -m mkdocs serve -f mkdocs.dev.yml` ; `mkdocs.yml` reste
  utilisé tel quel par le CI. README mis à jour en conséquence.
- Export PDF en échec (403) : l'appel à Google Fonts dans
  `extra.css` (`@import`) était bloqué quand WeasyPrint le
  rejouait pendant le rendu du PDF. Polices Cormorant Garamond, EB
  Garamond et Roboto Mono auto-hébergées en `.woff2` dans
  `docs/assets/fonts/` (licence SIL OFL 1.1) et déclarées via
  `@font-face` dans `extra.css` ; `theme.font: false` dans
  `mkdocs.yml` pour désactiver le chargement automatique par
  Material — plus aucun appel réseau externe au build.

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
