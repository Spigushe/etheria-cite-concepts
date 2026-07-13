# -*- coding: utf-8 -*-
"""
Hook MkDocs : génère les cartes de chaque quartier au moment du build
(mkdocs build ou mkdocs serve), sans rien committer dans le dépôt.

Produit, par quartier :
- assets/cartes/<slug>.pdf : jeu complet recto-verso, prêt à imprimer
  (63x88 mm, traits de coupe, pages recto puis verso correspondantes).
- assets/cartes/<slug>/<famille>-<NN>.png : recto de chaque carte,
  utilisé par les carrousels des pages du wiki (voir docs/mj/annexes/
  ressources-mj.md).

Le recto ne porte que le blason et le type de carte (pas de titre ni
de texte), par choix : la carte reste "aveugle" tant qu'elle n'est
pas retournée. Les cartes d'une même famille, dans un même quartier,
ont donc un recto strictement identique.
"""

import io
import json
import re
from pathlib import Path
from typing import TypedDict

import pypdfium2 as pdfium  # type: ignore[import-untyped]
from mkdocs.structure.files import File
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

CARD_W = 63 * mm
CARD_H = 88 * mm
COLS = 3
ROWS = 3
PAGE_W, PAGE_H = A4

MARGIN_X = (PAGE_W - COLS * CARD_W) / 2
MARGIN_Y = (PAGE_H - ROWS * CARD_H) / 2

ASSETS_DIR = Path(__file__).resolve().parent.parent / "docs" / "assets"

# Couleurs reprises de docs/assets/stylesheets/callouts.css.
COLORS = {
    "evenement": (0xC6 / 255, 0x28 / 255, 0x28 / 255),  # rouge (danger)
    "idee": (0x15 / 255, 0x65 / 255, 0xC0 / 255),  # bleu (pnj)
    "pacte": (0x26 / 255, 0x32 / 255, 0x38 / 255),  # noir (secret)
    "lieu": (0x2E / 255, 0x7D / 255, 0x32 / 255),  # vert (ville)
}
FAMILY_LABELS = {
    "evenement": "ÉVÉNEMENT",
    "idee": "IDÉE",
    "pacte": "PACTE",
    "lieu": "LIEU",
}

CardTuple = tuple[str, str, str]


class Deck(TypedDict):
    quartier: str
    blason: Path
    cards: list[CardTuple]


# Les cartes de chaque quartier sont maintenues à part, dans un JSON
# lisible et modifiable sans toucher au code (voir docs/mj/annexes/
# decks-cartes.json). Ce module se contente de le charger et de le
# valider : ajouter, retirer ou reformuler une carte ne nécessite
# jamais de modifier ce fichier.
DECKS_JSON_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs"
    / "mj"
    / "annexes"
    / "decks-cartes.json"
)


def _load_decks() -> dict[str, Deck]:
    try:
        raw = json.loads(DECKS_JSON_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"Fichier de cartes introuvable : {DECKS_JSON_PATH}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"JSON invalide dans {DECKS_JSON_PATH} : {exc}") from exc

    decks: dict[str, Deck] = {}
    for slug, data in raw.items():
        for champ in ("quartier", "blason", "cartes"):
            if champ not in data:
                raise RuntimeError(
                    f"{DECKS_JSON_PATH} : le quartier « {slug} » n'a pas "
                    f"de champ « {champ} »."
                )

        blason_path = ASSETS_DIR / "blasons" / data["blason"]
        if not blason_path.is_file():
            raise RuntimeError(
                f"{DECKS_JSON_PATH} : le blason « {data['blason']} » du "
                f"quartier « {slug} » est introuvable dans "
                f"{ASSETS_DIR / 'blasons'}."
            )

        cards: list[CardTuple] = []
        for n, carte in enumerate(data["cartes"], start=1):
            for champ in ("famille", "titre", "texte"):
                if champ not in carte:
                    raise RuntimeError(
                        f"{DECKS_JSON_PATH} : carte n°{n} du quartier "
                        f"« {slug} » n'a pas de champ « {champ} »."
                    )
            famille = carte["famille"]
            if famille not in COLORS:
                attendues = ", ".join(sorted(COLORS))
                raise RuntimeError(
                    f"{DECKS_JSON_PATH} : carte « {carte['titre']}\u00a0» "
                    f"(quartier « {slug} ») a une famille inconnue "
                    f"« {famille} ». Valeurs attendues : {attendues}."
                )
            cards.append((famille, carte["titre"], carte["texte"]))

        decks[slug] = {
            "quartier": data["quartier"],
            "blason": blason_path,
            "cards": cards,
        }

    return decks


DECKS: dict[str, Deck] = _load_decks()


def _wrap_text(text, font_name, font_size, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if stringWidth(trial, font_name, font_size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _draw_cut_marks(c, x, y):
    c.setStrokeColorRGB(0.6, 0.6, 0.6)
    c.setLineWidth(0.3)
    c.rect(x, y, CARD_W, CARD_H)


def _draw_front(c, x, y, family, blason, cut_marks=True):
    color = COLORS[family]

    c.setFillColorRGB(1, 1, 1)
    c.rect(x, y, CARD_W, CARD_H, fill=1, stroke=0)

    c.setFillColorRGB(*color)
    c.rect(x, y + CARD_H - 6 * mm, CARD_W, 6 * mm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + CARD_W / 2, y + CARD_H - 4.2 * mm, FAMILY_LABELS[family])

    c.setFillColorRGB(*color)
    c.rect(x, y, CARD_W, 10 * mm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + CARD_W / 2, y + 4.2 * mm, FAMILY_LABELS[family])

    img_size = 48 * mm
    zone_top = CARD_H - 6 * mm
    zone_bottom = 10 * mm
    img_y = y + zone_bottom + (zone_top - zone_bottom - img_size) / 2
    c.drawImage(
        blason,
        x + (CARD_W - img_size) / 2,
        img_y,
        width=img_size,
        height=img_size,
        mask="auto",
    )

    if cut_marks:
        _draw_cut_marks(c, x, y)


def _draw_back(c, x, y, family, title, text, quartier, cut_marks=True):
    color = COLORS[family]
    pad = 4 * mm

    c.setFillColorRGB(1, 1, 1)
    c.rect(x, y, CARD_W, CARD_H, fill=1, stroke=0)

    c.setFillColorRGB(*color)
    c.rect(x, y + CARD_H - 8 * mm, CARD_W, 8 * mm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(
        x + CARD_W / 2, y + CARD_H - 5.2 * mm, f"{FAMILY_LABELS[family]} — {quartier}"
    )

    c.setFillColorRGB(*color)
    c.rect(x, y, CARD_W, 6 * mm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + CARD_W / 2, y + 2.2 * mm, FAMILY_LABELS[family])

    title_lines = _wrap_text(title, "Helvetica-Bold", 9.5, CARD_W - 2 * pad)
    body_lines = _wrap_text(text, "Helvetica", 8.5, CARD_W - 2 * pad)

    title_line_h = 11
    body_line_h = 10.5
    gap = 6
    content_h = len(title_lines) * title_line_h + gap + len(body_lines) * body_line_h

    zone_top = CARD_H - 11 * mm
    zone_bottom = 8 * mm
    zone_h = zone_top - zone_bottom
    ty = zone_bottom + (zone_h + content_h) / 2

    c.setFillColorRGB(*color)
    c.setFont("Helvetica-Bold", 9.5)
    for line in title_lines:
        c.drawCentredString(x + CARD_W / 2, y + ty, line)
        ty -= title_line_h

    ty -= gap

    c.setFillColorRGB(0.15, 0.15, 0.15)
    c.setFont("Helvetica", 8.5)
    for line in body_lines:
        c.drawCentredString(x + CARD_W / 2, y + ty, line)
        ty -= body_line_h

    if cut_marks:
        _draw_cut_marks(c, x, y)


def _cell_origin(index, mirrored):
    row = index // COLS
    col = index % COLS
    if mirrored:
        col = COLS - 1 - col
    x = MARGIN_X + col * CARD_W
    y = PAGE_H - MARGIN_Y - (row + 1) * CARD_H
    return x, y


# Ordre canonique des quartiers (celui de monde/quartiers/index.md,
# repris dans ressources-mj.md) : utilisé pour le PDF combiné, pour
# que son sommaire ne dépende pas de l'ordre d'insertion dans le JSON.
QUARTIER_ORDER = [
    "labyrinthe-des-identites",
    "concorde-du-pacte",
    "balance-d-orion",
    "gouffre-d-absyr",
    "rails-de-la-decision",
    "jardins-de-l-equite",
    "citadelle-de-l-arete",
]


def _ordered_slugs():
    connus = list(DECKS)
    manquants = [s for s in connus if s not in QUARTIER_ORDER]
    if manquants:
        raise RuntimeError(
            "QUARTIER_ORDER (scripts/cards.py) ne connaît pas le(s) "
            f"quartier(s) suivant(s), présents dans decks-cartes.json : "
            f"{', '.join(manquants)}. Ajoutez-les à QUARTIER_ORDER."
        )
    return [s for s in QUARTIER_ORDER if s in connus]


def _write_deck_pages(c, deck):
    """Dessine les pages recto puis verso d'un deck sur un canvas déjà
    ouvert, sans le sauvegarder (pour pouvoir enchaîner plusieurs
    decks sur un même document, voir render_all_decks_pdf)."""
    blason = ImageReader(str(deck["blason"]))

    per_page = COLS * ROWS
    cards = deck["cards"]
    pages = [cards[i : i + per_page] for i in range(0, len(cards), per_page)]

    for page_cards in pages:
        for i, (family, _title, _text) in enumerate(page_cards):
            x, y = _cell_origin(i, mirrored=False)
            _draw_front(c, x, y, family, blason)
        c.showPage()

        for i, (family, title, text) in enumerate(page_cards):
            x, y = _cell_origin(i, mirrored=True)
            _draw_back(c, x, y, family, title, text, deck["quartier"])
        c.showPage()


def render_deck_pdf(deck):
    """Jeu complet recto-verso d'un seul quartier (grille A4), en bytes."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    _write_deck_pages(c, deck)
    c.save()
    return buf.getvalue()


def render_all_decks_pdf():
    """Jeu complet recto-verso de tous les quartiers, à la suite les
    uns des autres dans l'ordre canonique, en un seul PDF."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    for slug in _ordered_slugs():
        _write_deck_pages(c, DECKS[slug])
    c.save()
    return buf.getvalue()


def render_card_back_png(deck, family, title, text, dpi=150):
    """Verso d'une carte (titre et texte, sans traits de coupe), rendu en PNG.

    150 DPI suffit largement pour un affichage web (carrousel) ; le
    PDF imprimable, lui, reste vectoriel et n'est pas concerné par
    cette résolution.
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(CARD_W, CARD_H))
    _draw_back(c, 0, 0, family, title, text, deck["quartier"], cut_marks=False)
    c.showPage()
    c.save()
    buf.seek(0)

    pdf = pdfium.PdfDocument(buf.read())
    page = pdf[0]
    bitmap = page.render(scale=dpi / 72)
    image = bitmap.to_pil()
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True)
    return out.getvalue()


def on_files(files, config):
    all_bytes = render_all_decks_pdf()
    all_uri = "assets/cartes/toutes-les-cartes.pdf"
    files.append(File.generated(config, all_uri, content=all_bytes))

    for slug, deck in DECKS.items():
        pdf_bytes = render_deck_pdf(deck)
        files.append(
            File.generated(config, f"assets/cartes/{slug}.pdf", content=pdf_bytes)
        )

        counters = {}
        for family, title, text in deck["cards"]:
            counters[family] = counters.get(family, 0) + 1
            n = counters[family]

            thumb_bytes = render_card_back_png(deck, family, title, text)
            thumb_uri = f"assets/cartes/{slug}/{family}-{n:02d}.png"
            files.append(File.generated(config, thumb_uri, content=thumb_bytes))

            zoom_bytes = render_card_back_png(deck, family, title, text, dpi=300)
            zoom_uri = f"assets/cartes/{slug}/{family}-{n:02d}@2x.png"
            files.append(File.generated(config, zoom_uri, content=zoom_bytes))

    return files


# ============================================================
# Balise Markdown : {{ cartes: <slug-quartier> / <famille> }}
#
# Remplacée, page par page, par le carrousel (recto) et le tableau
# (titre/détails) de la famille demandée, générés depuis DECKS. Garde
# les fichiers .md sobres : un quartier n'a plus qu'une ligne par
# famille de cartes, jamais de HTML ni de tableau à recopier à la
# main depuis decks-cartes.json.
# ============================================================

_CARTES_MARKER_RE = re.compile(r"\{\{\s*cartes:\s*([a-z0-9-]+)\s*/\s*([a-z]+)\s*\}\}")

# {{ cartes_pdf: <slug> }} et {{ cartes_pdf_global }} : liens de
# téléchargement des PDF imprimables. Deux particularités :
#
# 1. Générés en URL absolue (via site_url) plutôt qu'en lien relatif,
#    parce que mkdocs-to-pdf tente de résoudre tout lien relatif qui
#    ne pointe pas vers une page ou une image comme une ancre interne
#    au document fusionné, et échoue sur les liens vers de vrais
#    fichiers à télécharger (voir
#    mkdocs_to_pdf.preprocessor.links.transform.transform_href, qui
#    ne laisse passer que les URL absolues ou les .png).
#
# 2. Générés en HTML brut avec la classe masque-en-pdf (voir
#    extra.css, règle @media print), pour ne pas apparaître dans
#    documentation.pdf : un lien de téléchargement n'a aucun sens à
#    l'intérieur d'un PDF déjà imprimé. WeasyPrint (utilisé par
#    mkdocs-to-pdf) rend avec le média CSS "print" par défaut, donc
#    @media print masque ces liens à l'export sans les cacher sur le
#    site web (média "screen"/"all").
_CARTES_PDF_MARKER_RE = re.compile(r"\{\{\s*cartes_pdf:\s*([a-z0-9-]+)\s*\}\}")
_CARTES_PDF_GLOBAL_MARKER = "{{ cartes_pdf_global }}"


def _escape_cell(text):
    return text.replace("|", "\\|")


def _absolute_url(config, path):
    base = config["site_url"] or "/"
    if not base.endswith("/"):
        base += "/"
    return base + path


def _render_family_section(slug, family):
    cards = [c for c in DECKS[slug]["cards"] if c[0] == family]
    quartier = DECKS[slug]["quartier"]
    mot_famille = FAMILY_LABELS[family].lower()

    lines = [
        '<div class="carte-carrousel" markdown="1">',
        '<button class="carte-carrousel__prec" aria-label="Précédent">‹</button>',
        '<div class="carte-carrousel__piste" markdown="1">',
    ]
    for i in range(1, len(cards) + 1):
        lines.append(
            f"![Recto : carte {mot_famille} du {quartier}]"
            f"(../../assets/cartes/{slug}/{family}-{i:02d}.png)"
        )
    lines += [
        "</div>",
        '<button class="carte-carrousel__suivant" aria-label="Suivant">›</button>',
        "</div>",
        "",
        "| Titre | Détails |",
        "| - | - |",
    ]
    for _family, titre, texte in cards:
        lines.append(f"| {_escape_cell(titre)} | {_escape_cell(texte)} |")

    return "\n".join(lines)


def on_page_markdown(markdown, page, config, files):
    def _replace_famille(match):
        slug, family = match.group(1), match.group(2)
        if slug not in DECKS:
            connus = ", ".join(sorted(DECKS))
            raise RuntimeError(
                f"{page.file.src_uri} : quartier inconnu « {slug} » dans "
                f"{{{{ cartes: {slug} / {family} }}}} (quartiers connus : "
                f"{connus})."
            )
        if family not in COLORS:
            connues = ", ".join(sorted(COLORS))
            raise RuntimeError(
                f"{page.file.src_uri} : famille inconnue « {family} » dans "
                f"{{{{ cartes: {slug} / {family} }}}} (familles connues : "
                f"{connues})."
            )
        return _render_family_section(slug, family)

    def _replace_pdf(match):
        slug = match.group(1)
        if slug not in DECKS:
            connus = ", ".join(sorted(DECKS))
            raise RuntimeError(
                f"{page.file.src_uri} : quartier inconnu « {slug} » dans "
                f"{{{{ cartes_pdf: {slug} }}}} (quartiers connus : {connus})."
            )
        url = _absolute_url(config, f"assets/cartes/{slug}.pdf")
        texte = "Télécharger le jeu complet en PDF, prêt à imprimer recto-verso"
        return f'<p class="masque-en-pdf"><a href="{url}">{texte}</a></p>'

    markdown = _CARTES_MARKER_RE.sub(_replace_famille, markdown)
    markdown = _CARTES_PDF_MARKER_RE.sub(_replace_pdf, markdown)

    if _CARTES_PDF_GLOBAL_MARKER in markdown:
        url = _absolute_url(config, "assets/cartes/toutes-les-cartes.pdf")
        texte = (
            "Télécharger les sept jeux de cartes en un seul PDF, prêt à "
            "imprimer recto-verso"
        )
        markdown = markdown.replace(
            _CARTES_PDF_GLOBAL_MARKER,
            f'<p class="masque-en-pdf"><a href="{url}">{texte}</a></p>',
        )

    return markdown
