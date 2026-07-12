# Ethéria, Cité des Concepts

C'est mon wiki de campagne perso. Je l'écris en Markdown avec
[MkDocs](https://www.mkdocs.org/) + le thème
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), et il se
publie automatiquement sur GitHub Pages à chaque push d'un tag (`v*`).

Ce README me sert d'aide-mémoire pour remonter le projet sur une nouvelle
machine.

## Fonctionnalités

- Structure prête à l'emploi : univers d'Éthéria (introduction, histoire,
  cartographie, personnages, quartiers), espace pédagogique (concepts
  philosophiques et sources), espace MJ (système de jeu, fiche de
  personnage, campagne).
- Callouts personnalisés façon Obsidian : `> [!VILLE]`, `> [!PNJ]`,
  `> [!FACTION]`, `> [!REGLE]`, `> [!NOUVELLES]`, `> [!DANGER]`,
  `> [!SECRET]`, `> [!INTRIGUE]`, `> [!TRESOR]`, `> [!MJ]` (informations
  hors-fiction réservées au meneur) — voir `docs/index.md` pour la liste et
  `docs/stylesheets/callouts.css` pour en ajouter.
- Numéro de version affiché dynamiquement sur la page d'accueil, lu depuis
  `CHANGELOG.md` par un hook MkDocs (`scripts/version.py`).
- Déploiement automatique via GitHub Actions à chaque push d'un tag
  (`v*`).

## Remettre le projet en route sur une nouvelle machine

```bash
git clone https://github.com/Spigushe/etheria-cite-concepts.git
cd etheria-cite-concepts

python3 -m venv .venv
source .venv/bin/activate      # sous Windows : .venv\Scripts\activate
pip install -r requirements.txt

python -m mkdocs serve
```

> J'utilise bien `python -m mkdocs` (et non `mkdocs` seul) : ça ajoute la
> racine du repo au PYTHONPATH, ce qui est nécessaire pour que mon extension
> locale `scripts/obsidian_callouts.py` soit importable.

Le site est alors visible sur `http://127.0.0.1:8000`, avec rechargement
automatique à chaque modification d'un fichier `.md`.

## Vérifications

Pas d'automatisation à l'heure actuelle, je lance ces commandes à la main
avant de commiter :

```bash
ruff check scripts/ --fix
ruff format scripts/
ty check
python -m mkdocs build --strict
npx --yes --package cspell --package @cspell/dict-fr-fr -- cspell --config cspell.json --no-progress
```

- `ruff` : lint et style Python sur `scripts/`.
- `ty` : typage Python sur `scripts/`.
- `mkdocs build --strict` : le site compile sans avertissement (liens
  internes et nav inclus).
- `cspell` : orthographe française sur tous les fichiers Markdown, avec
  le dictionnaire `cspell.json`, complété au fil du temps avec les noms
  propres et le vocabulaire spécifiques au projet.

## Publication sur GitHub Pages

C'est déjà configuré : `site_url` dans `mkdocs.yml` pointe vers
`https://spigushe.github.io/etheria-cite-concepts/`, et **Settings → Pages**
est réglé sur la source **GitHub Actions**. Je n'ai rien à refaire à chaque
nouvelle machine — il suffit de pousser un tag (`git tag vX.Y.Z && git push
origin vX.Y.Z`) et le workflow `.github/workflows/deploy.yml` reconstruit et
republie le site.

## Ajouter une page

1. Je crée un fichier `.md` dans le sous-dossier concerné (`docs/monde/`,
   `docs/monde/quartiers/`, `docs/resources-philo/concepts/`,
   `docs/resources-philo/sources/`, `docs/mj/campagne/`, etc.).
2. J'ajoute une entrée dans la section `nav:` de `mkdocs.yml` pour qu'elle
   apparaisse dans le menu.
3. Je vérifie l'orthographe avec `cspell` : les nouveaux noms propres du
   monde d'Éthéria vont dans le tableau `words` de `cspell.json`.

## Ajouter un nouveau type de callout

1. Je l'écris directement dans un fichier `.md` : `> [!MONTYPE] Titre`.
   Aucune déclaration préalable n'est nécessaire, le rendu fonctionne
   par défaut (style neutre gris).
2. Pour lui donner une couleur/icône dédiée, j'ajoute un bloc dans
   `docs/stylesheets/callouts.css` en suivant les exemples existants.

## Structure du repo

```text
docs/
├── index.md                    # accueil, numéro de version dynamique
├── monde/                      # univers d'Éthéria
│   ├── introduction.md
│   ├── histoire.md
│   ├── cartographie.md
│   ├── personnages.md
│   ├── pitch.md
│   └── quartiers/               # les sept quartiers (ambiance, PNJ,
│                                 # dilemmes, menaces, mythes, connexions)
├── resources-philo/            # espace pédagogique
│   ├── concepts/                 # une fiche concept par quartier
│   └── sources/                  # une fiche par philosophe/auteur
├── mj/                         # espace MJ
│   ├── index.md                  # conseils de mise en scène, sécurité de table
│   ├── systeme.md                # réputation philosophique, dilemmes
│   ├── annexes/                  # fiche de personnage FATE, aides de jeu
│   └── campagne/                 # aventures prêtes à jouer, une par
│                                 # quartier, quêtes transversales,
│                                 # transitions entre quartiers
└── stylesheets/callouts.css    # styles des callouts personnalisés
scripts/
├── obsidian_callouts.py        # extension Markdown : syntaxe > [!TYPE]
└── version.py                  # hook MkDocs : injecte {{ version }}
mkdocs.yml                      # configuration du site
requirements.txt
cspell.json                     # config orthographe (dictionnaire fr-fr)
.github/workflows/deploy.yml    # build + déploiement automatique
CHANGELOG.md                    # historique des versions du wiki
```
