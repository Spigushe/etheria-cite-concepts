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

- Structure de livre de jeu en sept parties : Ouverture, I. La cité
  (introduction, histoire, cartographie, personnages, quartiers),
  II. Jouer (règles, création de personnage, sécurité de table),
  III. Mener, IV. Campagne (trames et concepts par quartier),
  V. Scénarios, Annexes (glossaire, lexique, auteurs, cartes).
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

Le workflow `.github/workflows/checks.yml` lance ces vérifications à chaque
push sur `main`, sur chaque pull request et avant chaque déploiement. Je
peux aussi les lancer à la main avant de commiter :

```bash
uv run ruff check scripts/ --fix
uv run ruff format scripts/
uv run ty check
uv run python -m mkdocs build --strict -f mkdocs.dev.yml
npx --yes --package cspell --package @cspell/dict-fr-fr -- cspell --config cspell.json --no-progress
npx --yes markdownlint-cli2@0.24.1
```

- `ruff` : lint et style Python sur `scripts/`.
- `ty` : typage Python sur `scripts/`.
- `mkdocs build --strict` : le site compile sans avertissement (liens
  internes et nav inclus). En local je passe par `mkdocs.dev.yml` (voir
  plus haut) ; le CI, lui, build avec `mkdocs.yml` (export PDF inclus).
- `cspell` : orthographe française sur tous les fichiers Markdown, avec
  le dictionnaire `cspell.json`, complété au fil du temps avec les noms
  propres et le vocabulaire spécifiques au projet.
- `markdownlint` : structure des fichiers Markdown (titres, listes,
  tableaux, espaces en fin de ligne). Les règles sont dans
  `.markdownlint.json`, les fichiers contrôlés dans
  `.markdownlint-cli2.jsonc` ; l'extension VS Code recommandée lit les
  deux et signale les mêmes erreurs dans l'éditeur. Ajouter `--fix` à
  la commande corrige ce qui peut l'être automatiquement. Une liste
  imbriquée s'indente de quatre espaces, sans quoi MkDocs l'affiche à
  plat.

## Publication sur GitHub Pages

C'est déjà configuré : `site_url` dans `mkdocs.yml` pointe vers
`https://spigushe.github.io/etheria-cite-concepts/`, et **Settings → Pages**
est réglé sur la source **GitHub Actions**. Je n'ai rien à refaire à chaque
nouvelle machine — il suffit de pousser un tag (`git tag vX.Y.Z && git push
origin vX.Y.Z`) et le workflow `.github/workflows/deploy.yml` reconstruit et
republie le site.

## Ajouter une page

1. Je crée un fichier `.md` dans le sous-dossier concerné (`docs/cite/`,
   `docs/cite/quartiers/`, `docs/jouer/`, `docs/mener/`,
   `docs/campagne/`, `docs/annexes/auteurs/`, etc.).
2. J'ajoute une entrée dans la section `nav:` de `mkdocs.yml` pour qu'elle
   apparaisse dans le menu.
3. Je vérifie l'orthographe avec `cspell` : les nouveaux noms propres du
   monde d'Éthéria vont dans le tableau `words` de `cspell.json`.
4. Je vérifie la structure avec `markdownlint` (voir
   [Vérifications](#vérifications)).

## Ajouter un nouveau type de callout

1. Je l'écris directement dans un fichier `.md` : `> [!MONTYPE] Titre`.
   Aucune déclaration préalable n'est nécessaire, le rendu fonctionne
   par défaut (style neutre gris).
2. Pour lui donner une couleur/icône dédiée, j'ajoute un bloc dans
   `docs/assets/stylesheets/callouts.css` en suivant les exemples existants.

## Cartes imprimables

Chaque `{{ cartes: <quartier> / <famille> }}` dans
`docs/annexes/cartes.md` est remplacé au build par le carrousel
(recto) et le tableau (titre/détails) correspondants, lus depuis
`docs/annexes/decks-cartes.json`. Les images et le PDF à imprimer ne sont
pas stockés dans le dépôt : ils sont régénérés à chaque build par
`scripts/cards.py`. Pour changer une carte, il suffit de modifier le JSON ;
`cartes.md` n'a jamais besoin d'être touché pour ça.

## Fiches des prétirés

Les prétirés sont décrits dans `docs/annexes/pretires.json`, rangés par
« jeu » (un scénario ou une campagne). Au build, `scripts/fiches.py` remplit
une fiche de personnage A4 par prétiré (`assets/fiches/<jeu>/<slug>.pdf`,
plus `assets/fiches/<jeu>.pdf` qui les réunit), sans rien stocker dans le
dépôt. Deux balises s'utilisent dans n'importe quelle page :

- `{{ pretires: <jeu> }}` : la description de chaque prétiré du jeu.
- `{{ fiches_pdf: <jeu> }}` : la liste des liens vers les fiches.

Pour un nouveau prétiré, j'ajoute une entrée dans la liste `pretires` du jeu.
Pour un nouveau scénario, j'ajoute une clé au JSON, sur le modèle de
`le-huitieme-fragment` :

```json
"mon-scenario": {
  "titre": "Mon scénario",
  "pied": "Mon scénario, texte du pied de fiche",
  "pretires": [
    {
      "slug": "prenom-nom",
      "nom": "Prénom Nom",
      "role": "son rôle en deux mots",
      "origine": "d'où il vient",
      "discipline": "logique",
      "aspects": { "concept": "…", "faille": "…", "serment": "…", "lien": "…" },
      "approches": { "Rigoureux": 3, "Habile": 2, "Éclatant": 2, "Ferme": 1, "Vif": 1, "Retors": 0 },
      "stunts": [{ "nom": "Nom du stunt", "effet": "+2 en … pour …" }],
      "reputation": { "Rationaliste": 1, "Solidaire": 1 }
    }
  ]
}
```

`reputation` donne, par pôle, le nombre de crans depuis le centre (1 à 3).
`aspects` accepte aussi `libre`, laissé en blanc sur la fiche s'il est absent.
Le build s'arrête avec un message clair si un champ manque, si une Approche
est inconnue ou si un texte trop long fait déborder la fiche.

## Structure du repo

```text
docs/
├── index.md                    # ouverture : le jeu en bref, comment lire le livre
├── presentation.md             # ton, thèmes, ce que les joueurs incarnent
├── changelog.md                # 1 ligne : {{ changelog }}, ne pas éditer
├── cite/                       # I. La cité : introduction, Société des
│   │                           # Explorateurs, histoire, cartographie,
│   │                           # personnages
│   └── quartiers/                # les sept quartiers (ambiance, PNJ,
│                                 # dilemmes, menaces, mythes, connexions)
├── jouer/                      # II. Jouer : règles de base (Fate
│                               # Accelerated), fiche d'Aventurier,
│                               # réputation, évolution, prétirés, exemple
│                               # de partie, sécurité de table
├── mener/                      # III. Mener : mise en scène, dilemmes,
│                               # conséquences, Gardiens, oppositions,
│                               # cartes à table, secrets
├── campagne/                   # IV. Campagne : lancer une campagne, une
│   │                           # page de trames par quartier, quêtes
│   │                           # transversales, transitions
│   └── concepts/                 # une fiche concept par quartier
├── scenarios/                  # V. Scénarios : vue d'ensemble + sept
│                               # scénarios en une séance
├── annexes/                    # glossaire, lexique philosophique, cartes à
│   │                           # imprimer, données (decks-cartes.json,
│   │                           # pretires.json)
│   └── auteurs/                  # une fiche par philosophe/auteur
└── assets/
    ├── blasons/ et icons/        # 7 PNG numérotés 1..7
    ├── fiches/                   # fiche d'Aventurier, cartes de sécurité
    ├── scenarios/                # kits PDF des scénarios
    ├── fonts/                    # polices auto-hébergées (woff2)
    ├── javascripts/carrousel.js
    └── stylesheets/              # callouts.css + extra.css
scripts/
├── obsidian_callouts.py        # extension Markdown : syntaxe > [!TYPE]
├── changelog.py                # hook MkDocs : injecte {{ changelog }}
├── cards.py                    # hook MkDocs : génère les cartes (PNG + PDF)
└── fiches.py                   # hook MkDocs : remplit les fiches PDF des prétirés
templates/                      # gabarits de l'export PDF
mkdocs.yml                      # configuration du site (utilisée par le CI)
mkdocs.dev.yml                  # config de dev local (hérite de mkdocs.yml,
                                 # sans le plugin to-pdf)
pyproject.toml                  # dépendances Python (gérées par uv)
uv.lock                         # versions figées des dépendances
cspell.json                     # config orthographe (dictionnaire fr-fr)
.markdownlint.json              # règles markdownlint
.markdownlint-cli2.jsonc        # fichiers contrôlés par markdownlint
.github/workflows/deploy.yml    # build + déploiement automatique
CHANGELOG.md                    # historique des versions du wiki
```
