# Changelog

Ce wiki évolue au fil de l'écriture, et ce journal garde une trace de
ce qui change à chaque étape : ce qui s'ajoute, ce qui se corrige, ce
qui se réécrit.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et les numéros de version suivent la logique du
[Semantic Versioning](https://semver.org/lang/fr/).

Chaque tag Git associé à une version porte aussi un nom, à la manière
d'une sortie de jeu : un PNJ pour une évolution mineure (`v0.10.0-eudemos`),
un événement historique d'Éthéria pour une évolution majeure. Un
correctif reprend le nom de la version qu'il corrige (`v0.11.1-silys`
pour un correctif de `v0.11.0-silys`).

## [Non publié]

### Modifié

- Le wiki prend la structure d'un livre de jeu en sept parties,
  dans la nav comme dans les dossiers : Ouverture, I. La cité
  (`cite/`), II. Jouer (`jouer/`), III. Mener (`mener/`),
  IV. Campagne (`campagne/`), V. Scénarios (`scenarios/`) et Annexes
  (`annexes/`). Toutes les adresses de pages changent.
- Les règles communes à la table sortent de l'ancien Espace MJ :
  règles de base, fiche d'Aventurier, réputation, évolution, prétirés
  et sécurité de table forment la partie II.
- « Système de jeu » est scindé en six pages : règles de base,
  réputation et évolution (partie II), dilemmes, conséquences et
  jugement des Gardiens (partie III). Chaque règle n'est plus écrite
  qu'à un endroit : le guide de la fiche renvoie aux règles au lieu
  de les répéter, et son tableau « Ce qui change, et quand » rejoint
  la page Évolution.
- Les valeurs d'un PNJ sont fixes : seuls les joueurs lancent les
  dés. La règle est écrite dans les règles de base et dans « Bâtir une
  opposition ». Les règles de base gagnent une section « Se défendre »
  qui détaille l'action : jet du joueur contre la valeur fixe de
  l'attaquant, choix de l'Approche, résultats, cas de deux
  Aventuriers.
- Les thèmes philosophiques des quartiers sont publics. Les encadrés
  qui les réservaient au MJ disparaissent de la vue d'ensemble des
  quartiers et de la cartographie.
- Les « éléments de jeu » de chaque quartier quittent la vue
  d'ensemble des quartiers pour ouvrir la page de trames du quartier,
  et la fiche concept de chaque quartier rejoint la partie Campagne.
- « Ressources pour jouer » est scindé : ce que fait chaque famille de
  cartes en partie III, les planches à imprimer en annexe.
- L'accueil présente le jeu, le matériel nécessaire et l'ordre de
  lecture.
- Les données `decks-cartes.json` et `pretires.json` passent dans
  `docs/annexes/`.
- Le livre PDF (`etheria-jdr.pdf`) suit l'ordre des sept parties et
  laisse le changelog sur le site (`exclude_pages`). Le lien de
  l'accueil vers le changelog passe en URL absolue pour ne pas casser
  l'export.
- Relecture après le redécoupage : une attaque inflige l'écart entre
  le jet et la défense (valeur fixe) ; la présentation renvoie à la
  règle de réputation au lieu de la recopier ; Silys renvoie à
  l'histoire, comme Élégéia ; la puce « Concept sous-jacent » des
  quartiers ne renvoie plus qu'à la fiche concept ; nouvelle
  description du site.

### Ajouté

- Quatre pages : « Bâtir une opposition » (`mener/oppositions.md`),
  « Lancer une campagne » (`campagne/lancer-une-campagne.md`, avec deux
  feuilles de suivi provisoires), « Exemple de partie »
  (`jouer/exemple-de-partie.md`) et « Glossaire »
  (`annexes/glossaire.md`).
- « Écrire un scénario » (`mener/ecrire-un-scenario.md`) : le gabarit
  commun aux sept scénarios, pour développer une trame en scènes.
- « Aide-mémoire » (`annexes/aide-memoire.md`) : les règles en
  tableaux, avec renvoi vers chaque page de règles.
- « Crédits » (`annexes/credits.md`) : licence Fate et mention de
  droits ; les noms des auteurs restent à compléter.
- Dans « Le jugement des Gardiens », une section « Jouer un Gardien »
  réunit les aspects des sept Gardiens, relevés dans les scénarios.
- « La Société des Explorateurs » (`cite/societe-des-explorateurs.md`),
  « Secrets de la cité » (`mener/secrets.md`), une vue d'ensemble des
  scénarios avec leurs kits (`scenarios/index.md`) et le lexique
  philosophique en page propre (`annexes/lexique.md`).

### Supprimé

- Les pages d'accueil « Ressources Philo » et « Concepts par
  quartier », remplacées par la vue d'ensemble de la campagne et les
  annexes.
- Dans l'histoire de la cité, le secret du huitième quartier (déplacé
  en partie III) et le renvoi au système de jeu.

## [0.12.0] - 2026-11-15 — Éléon Rive

### Ajouté

- Kits prêts à jouer, un PDF A4 par scénario
  (`docs/assets/scenarios/etheria-kit-<scénario>.pdf`) : livret du
  meneur, page pour les joueurs, fiches des prétirés, cartes citées
  et cartes de sécurité. Lien de téléchargement dans chaque scénario,
  cités en exemple dans la vue d'ensemble des quartiers et dans les
  Ressources pour jouer.
- Cartes de sécurité de table (Carte X, Passer, Ralentir, Hors
  personnage, Silence, carte libre, dos commun) : planches A4 recto
  verso, trois exemplaires de chaque carte
  (`docs/assets/fiches/cartes-securite.pdf`), et carrousel dans la
  section Sécurité de table de l'Accueil MJ.
- Second scénario d'initiation, « Le Dernier Jour du Régent », à la
  Concorde du Pacte (`mj/scenarios/le-dernier-jour-du-regent.md`) :
  il développe la trame « Le Pacte d'Unité » en scènes jouables et
  introduit les Serments, un premier conflit et la concession.
- Un scénario en une séance pour chacun des cinq autres quartiers,
  développant à chaque fois la première trame de la campagne avec
  les lieux, personnages, menaces et cartes existants : « Le Prix du
  Bonheur » (Balance d'Orion), « Le Festin du Néant » (Gouffre
  d'Absyr), « La Manette » (Rails de la Décision), « Le Voile
  d'Ignorance » (Jardins de l'Équité) et « Le Jardin des Épreuves »
  (Citadelle de l'Arété).
- Second jeu de cinq prétirés (clé `second-jeu` de `pretires.json`) :
  Mahaut Verdier, Anselme Corbin, Lazare Quint, Clémence Rouvray et
  Ombeline Tessier, chacun lié à une figure d'un de ces cinq
  quartiers, avec leurs fiches PDF.
- Lien de téléchargement des cartes de sécurité dans la liste « À
  préparer » des sept scénarios, en URL absolue pour ne pas casser
  l'export PDF.

### Modifié

- Fiche de personnage (`mj/annexes/fiche-personnage.md`) réécrite en
  guide de remplissage de la Fiche d'Aventurier imprimable : elle
  suit le recto puis le verso zone par zone (quoi écrire, où, avec
  des exemples tirés des prétirés) et se termine par un tableau de ce
  qui change sur la fiche et à quel moment. Le gabarit en texte, qui
  doublait le PDF, disparaît. Une section « Serment et Lien »
  explique comment écrire ces deux aspects et comment ils se jouent.
- Page des prétirés organisée en deux jeux ; les scénarios indiquent
  le jeu conseillé et les accroches valables pour l'autre.
- Workflow `checks.yml` : le build strict tourne avec la config de
  production et l'export PDF, comme au déploiement, pour que les
  erreurs de `mkdocs-to-pdf` sortent avant le tag.
- Règle `MD007` de `.markdownlint.json` passée à quatre espaces,
  l'indentation qu'attend MkDocs pour une liste imbriquée.
- Workflow `checks.yml` : contrôle `markdownlint` de tous les fichiers
  Markdown (`markdownlint-cli2`, version figée), donc aussi avant
  chaque déploiement. Les fichiers contrôlés sont listés dans
  `.markdownlint-cli2.jsonc`, la commande est documentée dans le
  README.

### Corrigé

- Accueil MJ (`mj/index.md`) : la liste des scénarios prêts à jouer
  s'affichait à plat, au même niveau que les autres entrées de « Pour
  préparer une séance ». Sous-liste indentée de quatre espaces pour
  qu'elle soit bien imbriquée.

### Retiré

- Planche de six Cartes X (`docs/assets/fiches/carte-x.pdf`),
  remplacée par les planches de cartes de sécurité, qui contiennent
  la Carte X. Les liens de l'Accueil MJ et des scénarios pointent
  désormais vers `cartes-securite.pdf`.

## [0.11.1] - 2026-11-14 — Silys, correctif 1

### Corrigé

- Déploiement en échec à l'export PDF : le lien relatif vers
  `assets/fiches/fiche-aventurier.pdf` dans la fiche de personnage
  était pris par `mkdocs-to-pdf` pour une ancre interne introuvable.
  Lien passé en URL absolue, comme ceux des cartes et des prétirés.

## [0.11.0] - 2026-11-14 — Silys [CASSÉE]

> Déploiement cassé (export PDF en échec, lien relatif vers
> `fiche-aventurier.pdf`) : voir le correctif 0.11.1 ci-dessus.

### Ajouté

- Zoom au clic sur les images marquées `.zoomable` (visionneuse des
  carrousels de cartes réutilisée), appliqué aux aperçus de la fiche
  d'Aventurier.
- Fiche d'Aventurier imprimable (PDF A4 recto verso, aperçus PNG)
  dans `docs/assets/fiches/`, liée depuis la fiche de personnage.
- Cinquième prétiré, Sidoine Farge, et fiches PDF imprimables des
  prétirés (une page A4 chacune), liées depuis `mj/annexes/pretires.md`
  et le scénario « Le Huitième Fragment ». Le hook `scripts/fiches.py`
  les remplit au build depuis `docs/mj/annexes/pretires.json`, par jeu
  de prétirés (un scénario ou une campagne) ; la page des prétirés est
  générée depuis le même fichier.
- Scénario d'initiation « Le Huitième Fragment »
  (`mj/scenarios/le-huitieme-fragment.md`), dans une nouvelle section
  « Scénarios prêts à jouer » : la trame « Les Éclats du
  Navire Originel » découpée en scènes, avec oppositions chiffrées,
  pour une séance au Labyrinthe des Identités. Non testé en partie.
- Workflow `checks.yml` : ruff, ty, cspell et build strict à chaque
  push sur `main`, sur les pull requests, et en préalable au déploiement.
- Document de navigation du dépôt `CLAUDE.md` ajouté, incluant la structure du projet, la stack technique et les points d’entrée pour les contributions.
- Règles de base de Fate Accelerated dans `mj/systeme.md` (dés,
  difficultés, issues, actions, points de Destin, stress), avec la
  mention de licence d'Evil Hat.
- Échelle de réputation (trois crans de chaque côté du centre),
  jugement des Gardiens par axe, évolution des personnages par
  jalons, journal des altérations outillé.
- Création de personnage, valeurs des cases de stress et des
  conséquences dans la fiche de personnage.
- Page `mj/annexes/pretires.md` : quatre Aventuriers prêts à jouer.
- Effet de chaque famille de cartes dans `mj/annexes/ressources-mj.md`.
- Section « La Société des Explorateurs » dans `monde/presentation.md`.
- Type de dilemme et thèmes sensibles sur les 39 trames d'aventure.
- Fiche `resources-philo/sources/kierkegaard.md`.
- Secret de campagne sur le huitième quartier dans `monde/histoire.md`.
- Élégéia, Silys et les Non-Signataires dans les personnages et la
  fiche de la Concorde ; regards entre quartiers complétés dans les
  sept fiches de quartier.

### Modifié

- Gestion des dépendances Python confiée à uv : `pyproject.toml`
  (outils de typage et lint dans un groupe `dev`, Python fixé à
  3.13 via `requires-python`) et `uv.lock` remplacent `requirements.txt`. Le CI installe via
  `uv sync --locked`.
- `cspell.json` : liste des fichiers vérifiés (`**/*.md`) déclarée dans
  la config (la commande du README n'affichait que l'aide), code en
  ligne et blocs de code ignorés, dictionnaire complété et trié.
- « Aventures prêtes à jouer » remplacé par « trames d'aventure ».
- Thésée devient Théséis dans les aventures du Labyrinthe (« Le
  Jugement de Théséis »), avec une note MJ.
- « La Manette d'Orion » devient « La Manette » ; Eudaimon devient
  l'Algorithme d'Orion ; l'Érudit-Régent et le contrat fondateur
  accordés à la fiche de la Concorde ; titres de la Citadelle
  accordés à la Salle de l'Exemplarité.
- Typologie des dilemmes de `ressources-mj.md` remplacée par un lien
  vers `systeme.md`.
- Assets `5-dilemne-tramway.png` renommés `5-dilemme-tramway.png`.
- README et commentaires de `mkdocs.yml` remis à jour ; graphie
  « Éthéria » dans `site_name` et le titre du README.

### Corrigé

- Coquille `l'Arêtê` dans le CHANGELOG.
- Quartier de l'Abîme et son maître retirés de `monde/histoire.md`.
- Foot : le cas de 1967 est celui du conducteur, comparé au juge ; le
  témoin à l'aiguillage et le pont viennent de Thomson (1976 et 1985).
- Doublons et lieux flous : le Collecteur de Restes devient le
  Préleveur de Surplus ; le Tramway Immatériel devient la légende du
  Tramway Fantôme ; les « villes » des trames deviennent des secteurs
  nommés (secteur des Justes, Secteur d'Essai, Enclos des Mérites,
  Faubourg des Rêves Inversés) ; Miroir Flatteur distingué du Miroir
  d'Éleusis ; « épreuve de justice » au Jardin des Épreuves ; Lac des
  Réfractions et Confrérie du Vide ajoutés aux fiches de quartier.
- Œuvres de référence de Sartre et Singer dans l'index des sources ;
  Locke ajouté au Labyrinthe ; Zok n'est plus présenté comme
  l'aboutissement de Singer.
- Citations sourcées (Locke, Hobbes, Hutcheson, Bentham), citation d'Aristote
  passée en paraphrase.
- Notes « Non documentée ailleurs » retirées des transitions ; note de
  travail retirée de `mj/index.md` ; libellés périmés de l'accueil ;
  « Le Manuscrit Délié », « Bambou Fendu », « Arété ».

## [0.10.3] - 2026-07-14 — Eudémos, hotfix 3

### Corrigé

- Build en échec (`mkdocs build --strict`) : la page d'accueil
  (`docs/index.md`) pointait encore vers `monde/pitch.md`, supprimé
  lors du renommage de la page Pitch en Présentation (0.10.2). Lien
  corrigé vers `monde/presentation.md`.

## [0.10.2] - 2026-07-14 — Eudémos, correctif 2 [CASSÉE]

> Build cassé (`mkdocs build --strict` en échec, lien mort vers
> `monde/pitch.md`) : voir le hotfix 0.10.3 ci-dessus.

### Modifié

- Page « Pitch » (`docs/monde/pitch.md`) renommée en « Présentation »
  (`docs/monde/presentation.md`), titre changé en « Présentation de
  l'univers-campagne ». Dans la nav (`mkdocs.yml`), l'onglet
  « Présentation » pointe directement dessus au lieu d'un sous-menu ;
  la page Système, qui s'y trouvait à côté du Pitch, rejoint
  l'Espace MJ (`mj/systeme.md`).
- Logo de la page de dos (`templates/styles.scss`) : largeur portée
  à `170mm` (au lieu de `120mm`), toujours dans le max `80%`.

## [0.10.1] - 2026-07-14 — Eudémos, correctif 1

### Ajouté

- Règle de nommage des tags de version (voir en tête de ce fichier) :
  un nom de PNJ pour une évolution mineure, un événement historique
  d'Éthéria pour une évolution majeure, `-fix-<description>` pour un
  correctif.

### Modifié

- PDF de documentation attaché à la Release GitHub renommé
  `etheria-jdr-<tag>.pdf` (au lieu de `documentation-<tag>.pdf`),
  dans `.github/workflows/deploy.yml`. Le fichier généré au build
  suit désormais le même nom (`output_path: pdf/etheria-jdr.pdf`,
  `mkdocs.yml`), pour que la copie dans le workflow n'ait plus besoin
  de renommer un fichier `documentation.pdf`.
- Templates PDF personnalisés (`back_cover.html.j2`, `styles.scss`)
  replacés dans `templates/` à la racine du projet plutôt que
  `docs/assets/templates/` ; `custom_template_path` retiré de la
  config du plugin `to-pdf` (`mkdocs.yml`), qui retrouve son
  emplacement par défaut.
- Logo de la page de dos (`templates/styles.scss`) : largeur fixée à
  `120mm` (max `80%`) plutôt qu'en pourcentage plein cadre — réglage
  encore en cours pour corriger son rendu dans le PDF exporté.

### Retiré

- Affichage de la version sur la page d'accueil (`docs/index.md`),
  devenu redondant avec la page Changelog en annexe. Le hook qui le
  générait (`scripts/version.py`) disparaît avec lui ; l'injection de
  `{{ changelog }}` qu'il portait aussi est reprise par un nouveau
  hook dédié, `scripts/changelog.py`.

## [0.10.0] - 2026-07-14 — Eudémos

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
  MacIntyre dans la Citadelle de l'Arété, Hobbes/Locke/Rousseau dans la
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
