# Éthéria, Cité des Concepts

<p align="center">
  <img src="docs/assets/logo.png" alt="Blason d'Éthéria" width="220">
</p>

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
  `docs/assets/stylesheets/callouts.css` pour en ajouter.
- Page Changelog générée depuis `CHANGELOG.md` par un hook MkDocs
  (`scripts/changelog.py`, qui remplace `{{ changelog }}`).
- Déploiement automatique via GitHub Actions à chaque push d'un tag
  (`v*`).

## Remettre le projet en route sur une nouvelle machine

```bash
git clone https://github.com/Spigushe/etheria-cite-concepts.git
cd etheria-cite-concepts

uv sync                        # installe Python 3.13 + dépendances dans .venv

uv run python -m mkdocs serve -f mkdocs.dev.yml
```

> Les dépendances sont gérées par [uv](https://docs.astral.sh/uv/) :
> `pyproject.toml` les déclare (outils de typage et lint dans le groupe
> `dev`), `uv.lock` fige les versions exactes. Ajouter un paquet :
> `uv add <paquet>` (ou `uv add --dev <paquet>`).

<!-- -->

> J'utilise bien `python -m mkdocs` (et non `mkdocs` seul) : ça ajoute la
> racine du repo au PYTHONPATH, ce qui est nécessaire pour que mon extension
> locale `scripts/obsidian_callouts.py` soit importable.

<!-- -->

> `-f mkdocs.dev.yml` charge la config de dev (hérite de `mkdocs.yml` sans le
> plugin `to-pdf`) : l'export PDF dépend de WeasyPrint, qui a besoin de
> bibliothèques natives GTK absentes par défaut sous Windows. Cet export
> n'est utile qu'au build de Release (CI Linux, tag `v*`), donc `mkdocs.yml`
> reste la config de référence utilisée par le CI, sans `-f`.

Le site est alors visible sur `http://127.0.0.1:8000`, avec rechargement
automatique à chaque modification d'un fichier `.md`.

## Vérifications

Pas d'automatisation à l'heure actuelle, je lance ces commandes à la main
avant de commiter :

```bash
uv run ruff check scripts/ --fix
uv run ruff format scripts/
uv run ty check
uv run python -m mkdocs build --strict -f mkdocs.dev.yml
npx --yes --package cspell --package @cspell/dict-fr-fr -- cspell --config cspell.json --no-progress
```

- `ruff` : lint et style Python sur `scripts/`.
- `ty` : typage Python sur `scripts/`.
- `mkdocs build --strict` : le site compile sans avertissement (liens
  internes et nav inclus). En local je passe par `mkdocs.dev.yml` (voir
  plus haut) ; le CI, lui, build avec `mkdocs.yml` (export PDF inclus).
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
   `docs/assets/stylesheets/callouts.css` en suivant les exemples existants.

## Cartes imprimables

Chaque `{{ cartes: <quartier> / <famille> }}` dans
`docs/mj/annexes/ressources-mj.md` est remplacé au build par le carrousel
(recto) et le tableau (titre/détails) correspondants, lus depuis
`docs/mj/annexes/decks-cartes.json`. Les images et le PDF à imprimer ne sont
pas stockés dans le dépôt : ils sont régénérés à chaque build par
`scripts/cards.py`. Pour changer une carte, il suffit de modifier le JSON ;
`ressources-mj.md` n'a jamais besoin d'être touché pour ça.

## Structure du repo

```text
docs/
├── index.md                    # accueil, liste des callouts
├── changelog.md                # 1 ligne : {{ changelog }}, ne pas éditer
├── monde/                      # univers d'Éthéria
│   ├── presentation.md           # ton, thèmes, ce que les joueurs incarnent
│   ├── introduction.md
│   ├── histoire.md
│   ├── cartographie.md
│   ├── personnages.md
│   └── quartiers/                # les sept quartiers (ambiance, PNJ,
│                                 # dilemmes, menaces, mythes, connexions)
├── resources-philo/            # espace pédagogique
│   ├── concepts/                 # une fiche concept par quartier
│   └── sources/                  # une fiche par philosophe/auteur
├── mj/                         # espace MJ
│   ├── index.md                  # conseils de mise en scène, sécurité de table
│   ├── systeme.md                # FATE (Fate Accelerated) : règles de base,
│   │                             # réputation, évolution, dilemmes
│   ├── annexes/                  # fiche de personnage, prétirés, cartes
│   │                             # (decks-cartes.json)
│   └── campagne/                 # trames d'aventure, une page par
│                                 # quartier, quêtes transversales,
│                                 # transitions entre quartiers
└── assets/
    ├── blasons/ et icons/        # 7 PNG numérotés 1..7
    ├── fonts/                    # polices auto-hébergées (woff2)
    ├── javascripts/carrousel.js
    └── stylesheets/              # callouts.css + extra.css
scripts/
├── obsidian_callouts.py        # extension Markdown : syntaxe > [!TYPE]
├── changelog.py                # hook MkDocs : injecte {{ changelog }}
└── cards.py                    # hook MkDocs : génère les cartes (PNG + PDF)
templates/                      # gabarits de l'export PDF
mkdocs.yml                      # configuration du site (utilisée par le CI)
mkdocs.dev.yml                  # config de dev local (hérite de mkdocs.yml,
                                 # sans le plugin to-pdf)
pyproject.toml                  # dépendances Python (gérées par uv)
uv.lock                         # versions figées des dépendances
cspell.json                     # config orthographe (dictionnaire fr-fr)
.github/workflows/deploy.yml    # build + déploiement automatique
CHANGELOG.md                    # historique des versions du wiki
```
