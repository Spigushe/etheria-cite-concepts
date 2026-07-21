<!-- cSpell:ignore-file -->
# MAP — `Spigushe/etheria-cite-concepts`

> Document de navigation rapide. État constaté au commit `3c7dab0` (tag v0.10.3 « Eudémos, hotfix 3 », 2026-07-14). Wiki MkDocs Material en français, publié sur GitHub Pages : <https://spigushe.github.io/etheria-cite-concepts/>

## En une phrase

Wiki de campagne JdR perso : **Ethéria, Cité des Concepts** — un univers où chaque quartier incarne un concept philosophique, avec un espace pédagogique (fiches concepts + auteurs) et un espace MJ (système FATE, campagne, cartes imprimables).

## Stack technique

| Élément | Détail |
| --- | --- |
| Générateur | MkDocs + Material (fr), 3 palettes (épuré / parchemin / nocturne), polices auto-hébergées (`font: false`) |
| Config prod | `mkdocs.yml` (référence CI, inclut plugin `to-pdf` → `pdf/etheria-jdr.pdf`) |
| Config dev | `mkdocs.dev.yml` (hérite de prod **sans** `to-pdf` — WeasyPrint/GTK absent sous Windows). Lancer avec `python -m mkdocs serve -f mkdocs.dev.yml` (le `python -m` est requis pour importer `scripts/obsidian_callouts.py`) |
| Hooks MkDocs | `scripts/changelog.py` (injecte `{{ changelog }}` depuis `CHANGELOG.md` dans `docs/changelog.md`) · `scripts/cards.py` (génère PNG recto + PDF recto-verso des cartes au build, rien de committé) |
| Extension MD locale | `scripts/obsidian_callouts.py` : syntaxe `> [!TYPE] Titre`. Types : VILLE, PNJ, FACTION, REGLE, NOUVELLES, DANGER, SECRET, INTRIGUE, TRESOR, **MJ** (hors-fiction meneur). CSS : `docs/assets/stylesheets/callouts.css` |
| CI/CD | `.github/workflows/deploy.yml` — déclenché sur push de **tag `v*`**, Python 3.13, `ENABLE_PDF_EXPORT=1`, déploie sur Pages |
| Qualité | `mkdocs build --strict`, cspell (`cspell.json`), markdownlint (`.markdownlint.json`) |
| Versioning | Keep a Changelog + SemVer. Tags nommés : PNJ pour mineure (`v0.10.0-eudemos`), événement historique d'Ethéria pour majeure, hotfix = `-N` incrémental |

## Arborescence commentée

```text
CHANGELOG.md                  ← source de vérité version (injecté dans le site)
mkdocs.yml / mkdocs.dev.yml   ← nav complète dans mkdocs.yml (clé `nav:`)
requirements.txt
scripts/                      ← hooks + extension markdown (voir tableau ci-dessus)
templates/                    ← back_cover.html.j2 + styles.scss (export PDF)
docs/
├── index.md                  ← accueil (liste des callouts, version dynamique)
├── changelog.md              ← 1 ligne : {{ changelog }}
├── monde/                    ← LORE joueur
│   ├── presentation.md       ← ton, thèmes, ce que les joueurs incarnent
│   ├── introduction.md       ← la cité, ce qu'on y vient chercher
│   ├── histoire.md           ← 5 ères (Premier Souffle → Avènement de l'Exploration)
│   ├── cartographie.md       ← Agora Latente + portails
│   ├── personnages.md        ← figures légendaires, courants, Gardiens des Concepts
│   └── quartiers/            ← index + 7 fiches (~125 lignes chacune, structure
│                                identique : Architecture / Habitants / Dilemmes /
│                                Sortir / Menaces / Ce qu'on raconte / Regard sur les autres)
├── resources-philo/          ← PÉDAGOGIE
│   ├── concepts/             ← index (+ lexique philosophique) + 7 fiches quartier
│   │                            (callout REGLE "Concept abordé", Philosophes associés,
│   │                            Ce que ça donne en jeu, Questions à poser à la table)
│   └── sources/              ← index + 22 fiches auteurs (~30 lignes :
│                                "Ce qu'il apporte à Ethéria" / "À retenir pour la table")
├── mj/                       ← ESPACE MENEUR
│   ├── index.md              ← mise en scène, impro, sécurité de table, prépa séance
│   ├── systeme.md            ← FATE : Réputation philosophique, dilemmes, conséquences
│   ├── campagne/             ← index + 7 fichiers quartier (~55 lignes, 5 aventures
│   │                            chacun) + quetes-transversales.md
│   │                            + transitions-entre-quartiers.md (473 lignes, le plus
│   │                            gros fichier : 3 scènes par paire de quartiers)
│   └── annexes/
│       ├── fiche-personnage.md   ← fiche FATE (Aspects, Approches, Stunts, Réputation)
│       ├── ressources-mj.md      ← carrousels de cartes par quartier + typologie dilemmes
│       └── decks-cartes.json     ← données des cartes, 1 clé par slug de quartier
│                                    (consommé par scripts/cards.py)
└── assets/
    ├── blasons/ et icons/    ← 7 PNG numérotés 1..7 (ordre canonique, cf. tableau)
    ├── fonts/                ← Cormorant Garamond, EB Garamond, Roboto Mono (woff2)
    ├── javascripts/carrousel.js
    └── stylesheets/          ← callouts.css + extra.css
```

## Les 7 quartiers — table de correspondance

Chaque quartier existe en **4 exemplaires** : lore (`monde/quartiers/`), fiche concept (`resources-philo/concepts/`), aventures (`mj/campagne/`), deck (`decks-cartes.json`). Même slug partout.

| N° asset | Quartier (slug) | Concept | Philosophes associés (vérifiés dans les fiches) |
| --- | --- | --- | --- |
| 1 | Labyrinthe des Identités `labyrinthe-des-identites` | Identité personnelle (bateau de Thésée) | Hobbes, Parfit, Plutarque, Ricœur |
| 2 | Concorde du Pacte `concorde-du-pacte` | Contrat social | Hobbes, Locke, Rousseau, Rawls |
| 3 | Balance d'Orion `balance-d-orion` | Utilitarisme | Bentham, Mill, Singer |
| 4 | Gouffre d'Absyr `gouffre-d-absyr` | Absurdité de l'existence | Camus, Nietzsche, Sartre |
| 5 | Rails de la Décision `rails-de-la-decision` | Dilemme du tramway | Foot, Thomson, Kant |
| 6 | Jardins de l'Équité `jardins-de-l-equite` | Théorie de la justice | Rawls, Nozick, Sen, Aristote |
| 7 | Citadelle de l'Arété `citadelle-de-l-arete` | Éthique de la vertu | Aristote, Confucius, MacIntyre, Thomas d'Aquin |

Auteurs restants dans `sources/` sans quartier attitré dans les fiches concepts : aucun — les 22 fiches couvrent les noms ci-dessus (Rawls et Aristote apparaissent dans 2 quartiers ; Hobbes aussi).

## Où aller selon la demande

| Demande | Fichier(s) à ouvrir en premier |
| --- | --- |
| Modifier la nav / ajouter une page | `mkdocs.yml` (clé `nav:`) |
| Écrire du lore d'un quartier | `docs/monde/quartiers/<slug>.md` (copier la structure d'une fiche existante) |
| Ajouter/modifier une aventure | `docs/mj/campagne/<slug>.md` ; liaisons inter-quartiers → `transitions-entre-quartiers.md` |
| Cartes à jouer | `docs/mj/annexes/decks-cartes.json` (données) + `scripts/cards.py` (génération) + `ressources-mj.md` (affichage carrousel) |
| Fiches philo | `docs/resources-philo/concepts/<slug>.md` ou `sources/<auteur>.md` |
| Règles du jeu | `docs/mj/systeme.md` + `docs/mj/annexes/fiche-personnage.md` (FATE) |
| Nouveau callout | `scripts/obsidian_callouts.py` + `docs/assets/stylesheets/callouts.css` + liste dans `docs/index.md` |
| Publier une version | mettre à jour `CHANGELOG.md` (section `[Non publié]` → version datée + nom), puis tag `v*` → CI fait le reste |
| Style/typo du site | `docs/assets/stylesheets/extra.css`, palettes dans `mkdocs.yml` |
| Export PDF | plugin `to-pdf` dans `mkdocs.yml`, gabarits dans `templates/` |

## Pièges connus (documentés dans le repo)

1. `mkdocs serve` seul échoue : utiliser `python -m mkdocs serve -f mkdocs.dev.yml` (PYTHONPATH + pas de WeasyPrint en local).
2. Le build CI est en `--strict` : tout lien interne cassé fait échouer le déploiement (cause du hotfix 0.10.3 : lien mort vers `monde/pitch.md` après renommage Pitch → Présentation en 0.10.2).
3. `docs/changelog.md` ne se modifie jamais à la main : c'est `CHANGELOG.md` racine qui fait foi.
4. Les cartes ne sont pas committées : elles sont régénérées à chaque build par le hook.
