# Ethéria, Cité des Concepts

C'est mon wiki de campagne perso. Je l'écris en Markdown avec
[MkDocs](https://www.mkdocs.org/) + le thème
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), et il se
publie automatiquement sur GitHub Pages à chaque push sur `main`.

Ce README me sert d'aide-mémoire pour remonter le projet sur une nouvelle
machine.

## Fonctionnalités

- Structure prête à l'emploi : pitch, cosmologie, géographie,
  factions/PNJ, mécaniques, intrigues actives.
- Callouts personnalisés façon Obsidian : `> [!VILLE]`, `> [!PNJ]`,
  `> [!FACTION]`, `> [!REGLE]`, `> [!NOUVELLES]`, `> [!DANGER]`,
  `> [!SECRET]`, `> [!INTRIGUE]`, `> [!TRESOR]` — voir `docs/index.md`
  pour la liste et `docs/stylesheets/callouts.css` pour en ajouter.
- Déploiement automatique via GitHub Actions à chaque push sur `main`.

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

## Publication sur GitHub Pages

C'est déjà configuré : `site_url` dans `mkdocs.yml` pointe vers
`https://spigushe.github.io/etheria-cite-concepts/`, et **Settings → Pages**
est réglé sur la source **GitHub Actions**. Je n'ai rien à refaire à chaque
nouvelle machine — il suffit de pousser sur `main` et le workflow
`.github/workflows/deploy.yml` reconstruit et republie le site.

## Ajouter une page

1. Je crée un fichier `.md` dans le sous-dossier concerné (`docs/geographie/`,
   `docs/factions-pnj/`, etc.).
2. J'ajoute une entrée dans la section `nav:` de `mkdocs.yml` pour qu'elle
   apparaisse dans le menu.

## Ajouter un nouveau type de callout

1. Je l'écris directement dans un fichier `.md` : `> [!MONTYPE] Titre`.
   Aucune déclaration préalable n'est nécessaire, le rendu fonctionne
   par défaut (style neutre gris).
2. Pour lui donner une couleur/icône dédiée, j'ajoute un bloc dans
   `docs/stylesheets/callouts.css` en suivant les exemples existants.

## Structure du repo

```text
docs/
├── index.md                 # accueil
├── pitch/                   # ton, thèmes, ce qui rend l'univers unique
├── cosmologie/               # grande histoire, timeline
├── geographie/               # lieux, régions, cartes
├── factions-pnj/             # factions et PNJ
├── mecaniques/                # règles spécifiques à l'univers
├── intrigues/                 # suivi des fils en cours (change souvent)
└── stylesheets/callouts.css  # styles des callouts personnalisés
scripts/
└── obsidian_callouts.py      # extension Markdown : syntaxe > [!TYPE]
mkdocs.yml                    # configuration du site
requirements.txt
.github/workflows/deploy.yml  # build + déploiement automatique
```
