<!-- cSpell:ignore-file -->
# MAP — `Spigushe/etheria-cite-concepts`

> Document de navigation rapide. État constaté sur la branche `structure-livre` (refonte en livre de jeu, 2026-11-16), partie du tag v0.12.0 « Éléon Rive ». Wiki MkDocs Material en français, publié sur GitHub Pages : <https://spigushe.github.io/etheria-cite-concepts/>

## En une phrase

Wiki de campagne JdR perso : **Ethéria, Cité des Concepts** — un univers où chaque quartier incarne un concept philosophique. Depuis la refonte en livre de jeu, le wiki suit sept parties : Ouverture, I. La cité, II. Jouer, III. Mener, IV. Campagne, V. Scénarios, Annexes.

## Stack technique

| Élément | Détail |
| --- | --- |
| Générateur | MkDocs + Material (fr), 3 palettes (épuré / parchemin / nocturne), polices auto-hébergées (`font: false`) |
| Config prod | `mkdocs.yml` (référence CI, inclut plugin `to-pdf` → `pdf/etheria-jdr.pdf`) |
| Config dev | `mkdocs.dev.yml` (hérite de prod **sans** `to-pdf` — WeasyPrint/GTK absent sous Windows). Lancer avec `uv run python -m mkdocs serve -f mkdocs.dev.yml` (le `python -m` est requis pour importer `scripts/obsidian_callouts.py`) |
| Hooks MkDocs | `scripts/changelog.py` (injecte `{{ changelog }}` depuis `CHANGELOG.md` dans `docs/changelog.md`) · `scripts/cards.py` (génère PNG recto + PDF recto-verso des cartes au build, rien de committé) · `scripts/fiches.py` (remplit les fiches PDF A4 des prétirés au build depuis `pretires.json`, rien de committé ; balises `{{ pretires: <jeu> }}` et `{{ fiches_pdf: <jeu> }}`) |
| Extension MD locale | `scripts/obsidian_callouts.py` : syntaxe `> [!TYPE] Titre`. Types : VILLE, PNJ, FACTION, REGLE, NOUVELLES, DANGER, SECRET, INTRIGUE, TRESOR, **MJ** (hors-fiction meneur). CSS : `docs/assets/stylesheets/callouts.css` |
| Dépendances | **uv** : `pyproject.toml` (+ groupe `dev` : ruff, ty, stubs), `uv.lock`. Python 3.13 imposé par `requires-python = "==3.13.*"`. `uv sync` pour installer, `uv add` pour ajouter |
| CI/CD | `.github/workflows/checks.yml` (push `main`, PR, et appelé par deploy) : ruff, ty, cspell, markdownlint, build strict avec export PDF (même build qu'au déploiement). `.github/workflows/deploy.yml` — déclenché sur push de **tag `v*`**, après `checks`, `setup-uv` + `uv sync --locked --no-dev`, `ENABLE_PDF_EXPORT=1`, déploie sur Pages |
| Qualité | `mkdocs build --strict`, cspell (`cspell.json`), markdownlint (`npx --yes markdownlint-cli2@0.24.1` ; règles dans `.markdownlint.json`, fichiers contrôlés dans `.markdownlint-cli2.jsonc`) |
| Versioning | Keep a Changelog + SemVer. Tags nommés : PNJ pour mineure (`v0.10.0-eudemos`), événement historique d'Ethéria pour majeure, un correctif reprend le nom de la version qu'il corrige, sans suffixe (`v0.11.1-silys`) ; les tags antérieurs à la 0.11.1 portent encore un `-N` (`v0.10.3-eudemos-3`) |

## Arborescence commentée

```text
CHANGELOG.md                  ← source de vérité version (injecté dans le site)
mkdocs.yml / mkdocs.dev.yml   ← nav complète dans mkdocs.yml (clé `nav:`), en sept parties
pyproject.toml / uv.lock      ← dépendances (uv)
scripts/                      ← hooks + extension markdown (voir tableau ci-dessus)
templates/                    ← back_cover.html.j2 + styles.scss (export PDF)
docs/
├── index.md                  ← OUVERTURE : le jeu en bref, matériel, comment lire le livre
├── presentation.md           ← ton, thèmes (publics), ce que les joueurs incarnent
├── changelog.md              ← 1 ligne : {{ changelog }}
├── cite/                     ← I. LA CITÉ (lore, joueurs et MJ)
│   ├── introduction.md       ← la cité, ce qu'on y vient chercher
│   ├── societe-des-explorateurs.md
│   ├── histoire.md           ← 5 ères (Premier Souffle → Avènement de l'Exploration)
│   ├── cartographie.md       ← Agora Latente + portails
│   ├── personnages.md        ← figures légendaires, courants, Gardiens des Concepts
│   └── quartiers/            ← index (aperçu joueur) + 7 fiches (~125 lignes chacune :
│                                Architecture / Habitants / Dilemmes / Entrer ou Sortir /
│                                Menaces / Ce qu'on raconte / Regard sur les autres)
├── jouer/                    ← II. JOUER (toute la table)
│   ├── regles-de-base.md     ← Fate Accelerated : dés, actions, Destin, stress, licence
│   ├── creer-un-aventurier.md ← guide de remplissage de la fiche imprimable (création, recto, verso)
│   ├── reputation.md         ← cinq axes, échelle à 3 crans par côté
│   ├── evolution.md          ← jalons + tableau « ce qui change sur la fiche, et quand »
│   ├── pretires.md           ← intro + {{ pretires: <jeu> }} par jeu (rendu par scripts/fiches.py)
│   ├── exemple-de-partie.md  ← une scène commentée, dés compris
│   └── securite-de-table.md  ← Carte-X, signaux, cartes de sécurité
├── mener/                    ← III. MENER (MJ)
│   ├── index.md              ← mise en scène, improvisation
│   ├── dilemmes.md           ← les cinq formes de dilemmes
│   ├── consequences.md       ← traces dans la cité, journal des altérations
│   ├── gardiens.md           ← quel Gardien se méfie de quelle tendance
│   ├── oppositions.md        ← chiffrer un PNJ ou une menace (valeurs fixes, 4 profils)
│   ├── ecrire-un-scenario.md ← gabarit commun aux sept scénarios
│   ├── cartes.md             ← ce que fait chaque famille de cartes
│   └── secrets.md            ← le huitième quartier
├── campagne/                 ← IV. CAMPAGNE (MJ)
│   ├── index.md + lancer-une-campagne.md (premières séances, feuilles de suivi provisoires)
│   ├── <slug>.md             ← 7 fichiers quartier : éléments de jeu + 5 trames
│   ├── concepts/<slug>.md    ← 7 fiches concept (callout REGLE "Concept abordé", Philosophes
│   │                            associés, Ce que ça donne en jeu, Questions à poser à la table)
│   ├── quetes-transversales.md
│   └── transitions-entre-quartiers.md (473 lignes : 3 scènes par paire de quartiers)
├── scenarios/                ← V. SCÉNARIOS : index (tableau + kits) + 7 scénarios en scènes
│                                (le-huitieme-fragment.md et le-dernier-jour-du-regent.md
│                                sont les deux initiations)
├── annexes/
│   ├── aide-memoire.md       ← les règles en tableaux (renvoie aux pages de règles)
│   ├── glossaire.md          ← noms propres par quartier + termes de jeu
│   ├── credits.md            ← licence Fate, droits ; noms des auteurs à compléter
│   ├── lexique.md            ← lexique philosophique
│   ├── auteurs/              ← index + 23 fiches auteurs (~30 lignes :
│   │                            "Ce qu'il apporte à Ethéria" / "À retenir pour la table")
│   ├── cartes.md             ← carrousels de cartes par quartier
│   ├── decks-cartes.json     ← données des cartes, 1 clé par slug de quartier (scripts/cards.py)
│   └── pretires.json         ← données des prétirés, 1 clé par jeu (scripts/fiches.py)
└── assets/
    ├── blasons/ et icons/    ← 7 PNG numérotés 1..7 (ordre canonique, cf. tableau)
    ├── fonts/                ← Cormorant Garamond, EB Garamond, Roboto Mono (woff2)
    ├── scenarios/            ← kits prêts à jouer, 1 PDF committé par scénario
    │                            (etheria-kit-<slug du scénario>.pdf), liés en URL absolue
    │                            depuis les scénarios et scenarios/index.md
    ├── javascripts/carrousel.js
    └── stylesheets/          ← callouts.css + extra.css
```

## Les 7 quartiers — table de correspondance

Chaque quartier existe en **4 exemplaires** : lore (`cite/quartiers/`), fiche concept (`campagne/concepts/`), éléments de jeu et aventures (`campagne/`), deck (`annexes/decks-cartes.json`). Même slug partout.

| N° asset | Quartier (slug) | Concept | Philosophes associés (vérifiés dans les fiches) |
| --- | --- | --- | --- |
| 1 | Labyrinthe des Identités `labyrinthe-des-identites` | Identité personnelle (bateau de Thésée) | Hobbes, Locke, Parfit, Plutarque, Ricœur |
| 2 | Concorde du Pacte `concorde-du-pacte` | Contrat social | Hobbes, Locke, Rousseau, Rawls |
| 3 | Balance d'Orion `balance-d-orion` | Utilitarisme | Bentham, Mill, Singer |
| 4 | Gouffre d'Absyr `gouffre-d-absyr` | Absurdité de l'existence | Camus, Nietzsche, Sartre (+ Kierkegaard en contrepoint) |
| 5 | Rails de la Décision `rails-de-la-decision` | Dilemme du tramway | Foot, Thomson, Kant |
| 6 | Jardins de l'Équité `jardins-de-l-equite` | Théorie de la justice | Rawls, Nozick, Sen, Aristote |
| 7 | Citadelle de l'Arété `citadelle-de-l-arete` | Éthique de la vertu | Aristote, Confucius, MacIntyre, Thomas d'Aquin |

Auteurs restants dans `annexes/auteurs/` sans quartier attitré dans les fiches concepts : Kierkegaard (contrepoint au Gouffre, cité dans la nuance de la fiche concept). Rawls, Aristote, Hobbes et Locke apparaissent dans 2 quartiers.

## Où aller selon la demande

| Demande | Fichier(s) à ouvrir en premier |
| --- | --- |
| Modifier la nav / ajouter une page | `mkdocs.yml` (clé `nav:`) |
| Écrire du lore d'un quartier | `docs/cite/quartiers/<slug>.md` (copier la structure d'une fiche existante) |
| Ajouter/modifier une aventure | `docs/campagne/<slug>.md` ; liaisons inter-quartiers → `transitions-entre-quartiers.md` |
| Cartes à jouer | `docs/annexes/decks-cartes.json` (données) + `scripts/cards.py` (génération) + `docs/annexes/cartes.md` (affichage carrousel) + `docs/mener/cartes.md` (règles) |
| Prétirés (nouveau personnage ou nouveau jeu) | `docs/annexes/pretires.json` (données) ; `scripts/fiches.py` (mise en page) ; balises dans `docs/jouer/pretires.md` et les scénarios |
| Fiches philo | `docs/campagne/concepts/<slug>.md` ou `docs/annexes/auteurs/<auteur>.md` |
| Règles du jeu | `docs/jouer/` (règles de base, fiche, réputation, évolution) + `docs/mener/` (dilemmes, conséquences, Gardiens, oppositions) |
| Nouveau callout | `scripts/obsidian_callouts.py` + `docs/assets/stylesheets/callouts.css` + liste dans `docs/index.md` |
| Publier une version | mettre à jour `CHANGELOG.md` (section `[Non publié]` → version datée + nom), puis tag `v*` → CI fait le reste |
| Style/typo du site | `docs/assets/stylesheets/extra.css`, palettes dans `mkdocs.yml` |
| Export PDF | plugin `to-pdf` dans `mkdocs.yml`, gabarits dans `templates/` |

## Pièges connus (documentés dans le repo)

1. `mkdocs serve` seul échoue : utiliser `uv run python make.py dev` (PYTHONPATH + pas de WeasyPrint en local).
2. Le build CI est en `--strict` : tout lien interne cassé fait échouer le déploiement (cause du hotfix 0.10.3 : lien mort vers `monde/pitch.md` après renommage Pitch → Présentation en 0.10.2).
3. `docs/changelog.md` ne se modifie jamais à la main : c'est `CHANGELOG.md` racine qui fait foi.
4. Les cartes ne sont pas committées : elles sont régénérées à chaque build par le hook.
5. Un lien relatif vers un fichier à télécharger (PDF, etc.) passe le build strict local (sans PDF), mais fait échouer l'export PDF en CI (`checks.yml` et déploiement) : `mkdocs-to-pdf` le prend pour une ancre interne. Utiliser une URL absolue (`site_url`), comme le font `cards.py` et `fiches.py` (cause du correctif 0.11.1).
6. Une liste imbriquée s'indente de **quatre** espaces (règle `MD007`) : avec deux, Python-Markdown l'affiche à plat, au niveau de la liste parente.
7. `scripts/cards.py` écrit en dur le chemin relatif des images de cartes (`../assets/cartes/…`), valable pour une page à un seul niveau sous `docs/` (aujourd'hui `docs/annexes/cartes.md`). Si les balises `{{ cartes: … }}` changent de page ou de profondeur, adapter ce chemin, sinon le build strict échoue.
8. L'export PDF (`to-pdf`) suit l'ordre de la `nav` et exclut le changelog (`exclude_pages`). Toute page ajoutée à la `nav` entre dans le livre PDF.
9. Les sept kits PDF (`docs/assets/scenarios/`) sont committés, sans script de génération dans le dépôt. Leur aide-mémoire date d'avant la règle des valeurs fixes (« au jet d'un adversaire », « l'écart entre les deux jets ») : à corriger avant le prochain tag (décision de Martin).
