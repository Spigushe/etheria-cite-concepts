"""
Hook MkDocs : remplit la fiche de personnage de chaque prétiré au
moment du build (mkdocs build ou mkdocs serve), sans rien committer
dans le dépôt.

Les prétirés sont décrits dans docs/mj/annexes/pretires.json, rangés
par « jeu » (un scénario ou une campagne). Ajouter un prétiré, ou un
nouveau jeu de prétirés, ne demande que de compléter ce JSON : ce
module se contente de le charger, de le valider et de dessiner.

Produit, par jeu :
- assets/fiches/<jeu>/<slug>.pdf : la fiche A4 d'un prétiré.
- assets/fiches/<jeu>.pdf : toutes les fiches du jeu, une par page.

Deux balises Markdown :
- {{ pretires: <jeu> }} : la description de chaque prétiré du jeu
  (une section par personnage, avec le lien vers sa fiche).
- {{ fiches_pdf: <jeu> }} : la liste des liens vers les fiches.

La mise en page reprend docs/mj/annexes/fiche-personnage.md. Les
cotes sont en pixels CSS (96 par pouce), comme sur une maquette web :
une page A4 fait 794 x 1123.
"""

import io
import json
import re
from pathlib import Path

from fontTools.ttLib import TTFont as FichierPolice
from mkdocs.structure.files import File
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_POLICES = RACINE / "docs" / "assets" / "fonts"
PRETIRES_JSON_PATH = RACINE / "docs" / "mj" / "annexes" / "pretires.json"

PAGE_L, PAGE_H = 794, 1123
ECHELLE = A4[0] / PAGE_L
GAUCHE, DROITE = 52, 742
LARGEUR = DROITE - GAUCHE
BAS = 1055  # limite basse du contenu, au-dessus du pied de page

# Couleurs de la palette « épuré » (docs/assets/stylesheets/extra.css).
ENCRE = (0x1C / 255, 0x1A / 255, 0x16 / 255)
GRIS = (0x5A / 255, 0x54 / 255, 0x42 / 255)
ACCENT = (0x7A / 255, 0x5C / 255, 0x22 / 255)
FILET = (0xD9 / 255, 0xD0 / 255, 0xB8 / 255)
PAPIER = (0xFD / 255, 0xFB / 255, 0xF6 / 255)

TITRE, TEXTE, ITALIQUE, GRAS = "Fiche-Titre", "Fiche-Texte", "Fiche-Ital", "Fiche-Gras"
POLICES = {
    TITRE: "cormorant-garamond-700-normal.woff2",
    TEXTE: "eb-garamond-400-normal.woff2",
    ITALIQUE: "eb-garamond-400-italic.woff2",
    GRAS: "eb-garamond-700-normal.woff2",
}

# Ordre et libellés de docs/mj/annexes/fiche-personnage.md.
APPROCHES = [
    ("Rigoureux", "Analyse froide, logique serrée, patience"),
    ("Habile", "Ruse argumentative, sens de la repartie"),
    ("Éclatant", "Rhétorique flamboyante, gestes qui marquent"),
    ("Ferme", "Ténacité, pression morale, refus de céder"),
    ("Vif", "Repartie immédiate, réaction sous urgence"),
    ("Retors", "Sous-entendu, piège rhétorique, manipulation"),
]
AXES = [
    ("Idéaliste", "Pragmatique"),
    ("Cohérent", "Inconstant"),
    ("Solidaire", "Individualiste"),
    ("Révisionniste", "Conservateur"),
    ("Rationaliste", "Intuitif"),
]
ASPECTS = [
    ("concept", "Concept central"),
    ("faille", "Faille"),
    ("serment", "Serment"),
    ("lien", "Lien"),
]
CONSEQUENCES = [
    ("Doute passager", 2),
    ("Conviction ébranlée", 4),
    ("Crise existentielle", 6),
]
CRANS = {1: "un cran", 2: "deux crans", 3: "trois crans"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


# ============================================================
# Chargement et validation de pretires.json
# ============================================================


def _erreur(message):
    return RuntimeError(f"{PRETIRES_JSON_PATH} : {message}")


def _valider_pretire(jeu, p):
    champs = ("slug", "nom", "role", "origine", "discipline", "aspects")
    for champ in (*champs, "approches", "stunts", "reputation"):
        if champ not in p:
            nom = p.get("nom", p.get("slug", "?"))
            raise _erreur(
                f"le prétiré « {nom} » du jeu « {jeu} » n'a pas de champ « {champ} »."
            )
    nom = p["nom"]
    if not SLUG_RE.match(p["slug"]):
        raise _erreur(
            f"slug invalide « {p['slug']} » pour « {nom} » : minuscules, "
            "chiffres et tirets seulement."
        )
    for cle, libelle in ASPECTS:
        if not p["aspects"].get(cle):
            raise _erreur(f"« {nom} » n'a pas d'aspect « {cle} » ({libelle}).")

    attendues = [a for a, _ in APPROCHES]
    if sorted(p["approches"]) != sorted(attendues):
        raise _erreur(
            f"les Approches de « {nom} » doivent être exactement : "
            f"{', '.join(attendues)}."
        )
    for approche, score in p["approches"].items():
        if not isinstance(score, int) or not 0 <= score <= 4:
            raise _erreur(
                f"« {nom} » : l'Approche {approche} doit valoir de 0 à 4 "
                f"(trouvé : {score!r})."
            )

    if not 1 <= len(p["stunts"]) <= 3:
        raise _erreur(f"« {nom} » doit avoir de 1 à 3 stunts.")
    for stunt in p["stunts"]:
        if not stunt.get("nom") or not stunt.get("effet"):
            raise _erreur(f"« {nom} » : chaque stunt a un « nom » et un « effet ».")

    poles = {pole: axe for axe in AXES for pole in axe}
    axes_vus = set()
    for pole, crans in p["reputation"].items():
        if pole not in poles:
            raise _erreur(
                f"« {nom} » : pôle de réputation inconnu « {pole} ». Pôles "
                f"connus : {', '.join(poles)}."
            )
        if crans not in CRANS:
            raise _erreur(
                f"« {nom} » : la réputation « {pole} » se compte en crans, "
                f"de 1 à 3 (trouvé : {crans!r})."
            )
        if poles[pole] in axes_vus:
            raise _erreur(
                f"« {nom} » : deux pôles du même axe ({' / '.join(poles[pole])})."
            )
        axes_vus.add(poles[pole])


def _charger_jeux():
    try:
        brut = json.loads(PRETIRES_JSON_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"Fichier de prétirés introuvable : {PRETIRES_JSON_PATH}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"JSON invalide dans {PRETIRES_JSON_PATH} : {exc}") from exc

    for jeu, data in brut.items():
        if not SLUG_RE.match(jeu):
            raise _erreur(
                f"nom de jeu invalide « {jeu} » : minuscules, chiffres et "
                "tirets seulement."
            )
        for champ in ("titre", "pied", "pretires"):
            if champ not in data:
                raise _erreur(f"le jeu « {jeu} » n'a pas de champ « {champ} ».")
        slugs = set()
        for p in data["pretires"]:
            _valider_pretire(jeu, p)
            if p["slug"] in slugs:
                raise _erreur(f"slug « {p['slug']} » en double dans « {jeu} ».")
            slugs.add(p["slug"])
    return brut


JEUX = _charger_jeux()


# ============================================================
# Dessin d'une fiche
# ============================================================


def _enregistrer_polices():
    """reportlab ne lit pas le woff2 : les polices du site sont
    décompressées en mémoire, sans fichier supplémentaire à committer."""
    for nom, fichier in POLICES.items():
        if nom in pdfmetrics.getRegisteredFontNames():
            continue
        police = FichierPolice(DOSSIER_POLICES / fichier)
        police.flavor = None
        tampon = io.BytesIO()
        police.save(tampon)
        tampon.seek(0)
        pdfmetrics.registerFont(TTFont(nom, tampon))


def _maj(texte):
    return texte[:1].upper() + texte[1:]


def _lignes(texte, police, taille, largeur, retrait=0.0):
    """Découpe texte en lignes ; la première est plus courte de retrait."""
    lignes, courante = [], ""
    for mot in texte.split():
        essai = f"{courante} {mot}".strip()
        place = largeur - (0 if lignes else retrait)
        if stringWidth(essai, police, taille) <= place or not courante:
            courante = essai
        else:
            lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes


class _Fiche:
    """Outils de dessin en pixels, l'origine en haut à gauche."""

    def __init__(self, c):
        self.c = c

    def texte(self, x, y, s, police=TEXTE, taille=16, couleur=ENCRE, ancre="g"):
        """Écrit s, ligne de base à y. ancre : g(auche), c(entre), d(roite)."""
        c = self.c
        c.setFont(police, taille)
        c.setFillColorRGB(*couleur)
        if ancre == "d":
            c.drawRightString(x, -y, s)
        elif ancre == "c":
            c.drawCentredString(x, -y, s)
        else:
            c.drawString(x, -y, s)

    def capitales(self, x, y, s, taille, couleur, ancre="g"):
        """Petit intitulé en capitales espacées."""
        s = s.upper()
        espace = taille * 0.12
        if ancre == "d":
            x -= stringWidth(s, TITRE, taille) + espace * (len(s) - 1)
        self.c.setFont(TITRE, taille)
        self.c.setFillColorRGB(*couleur)
        self.c.drawString(x, -y, s, charSpace=espace)

    def paragraphe(self, x, y, s, largeur, police=TEXTE, taille=16, **options):
        """Écrit s sur plusieurs lignes ; renvoie la ligne de base suivante."""
        interligne = options.pop("interligne", taille * 1.3)
        for ligne in _lignes(s, police, taille, largeur):
            self.texte(x, y, ligne, police, taille, **options)
            y += interligne
        return y

    def trait(self, x1, x2, y, couleur=ENCRE, epaisseur=1.0):
        self.c.setStrokeColorRGB(*couleur)
        self.c.setLineWidth(epaisseur)
        self.c.setDash()
        self.c.line(x1, -y, x2, -y)

    def case(self, x, y, largeur=26, hauteur=26, chiffre=None):
        """Case à cocher, coin haut gauche en (x, y)."""
        self.c.setStrokeColorRGB(*ENCRE)
        self.c.setLineWidth(1.5)
        self.c.setDash()
        self.c.roundRect(x, -y - hauteur, largeur, hauteur, 3, stroke=1, fill=0)
        if chiffre is not None:
            self.texte(x + largeur / 2, y + 17.5, str(chiffre), TEXTE, 13, GRIS, "c")

    def titre(self, x, y, s, largeur):
        """Intitulé de section ; renvoie le haut du contenu qui suit."""
        self.capitales(x, y + 13, s, 15, ACCENT)
        self.trait(x, x + largeur, y + 22)
        return y + 28


def _dessiner_aspects(f, p, y):
    y = f.titre(GAUCHE, y, "Aspects", LARGEUR)
    lignes = [(lib, p["aspects"][cle]) for cle, lib in ASPECTS]
    lignes.append(("Aspect libre", p["aspects"].get("libre", "")))
    for libelle, valeur in lignes:
        f.capitales(GAUCHE, y + 22, libelle, 12, GRIS)
        if valeur:
            y = f.paragraphe(GAUCHE + 150, y + 22, valeur, 540, ITALIQUE, 17) - 10
        else:
            f.trait(GAUCHE + 150, DROITE, y + 26)
            y += 34
        f.trait(GAUCHE, DROITE, y, FILET)
    if not p["aspects"].get("libre"):
        f.texte(
            DROITE,
            y + 16,
            "À remplir en jeu : qu'est-ce qui a fait entrer ton personnage à Éthéria ?",
            ITALIQUE,
            12.5,
            GRIS,
            "d",
        )
        y += 20
    return y


def _dessiner_approches(f, p, x, y, largeur):
    y = f.titre(x, y, "Approches", largeur)
    for nom, description in APPROCHES:
        f.case(x, y + 5, 38, 34)
        f.texte(x + 19, y + 29, f"+{p['approches'][nom]}", TITRE, 20, ENCRE, "c")
        f.texte(x + 48, y + 20, nom, GRAS, 16)
        f.texte(x + 48, y + 36, description, TEXTE, 12.5, GRIS)
        y += 45
        f.trait(x, x + largeur, y, FILET)
    return y


def _dessiner_stunts_et_stress(f, p, x, y, largeur):
    y = f.titre(x, y, "Stunts", largeur)
    for n in range(3):
        f.texte(x, y + 20, f"{n + 1}.", GRAS, 16)
        if n < len(p["stunts"]):
            stunt = p["stunts"][n]
            nom = f"{stunt['nom']} :"
            f.texte(x + 24, y + 20, nom, GRAS, 16)
            # L'effet commence sur la ligne du nom, à sa suite.
            retrait = stringWidth(nom + " ", GRAS, 16)
            lignes = _lignes(stunt["effet"], TEXTE, 16, largeur - 24, retrait)
            for i, ligne in enumerate(lignes):
                decalage = retrait if i == 0 else 0
                f.texte(x + 24 + decalage, y + 20, ligne)
                y += 21
            y += 9
        else:
            f.trait(x + 24, x + largeur, y + 24)
            y += 36

    y = f.titre(x, y + 12, "Stress", largeur)
    for piste in ("Résolution", "Conviction"):
        f.texte(x, y + 24, piste, GRAS, 17)
        for i in range(3):
            f.case(x + largeur - 26 - (2 - i) * 34, y + 5, chiffre=i + 1)
        y += 36
    note = (
        "Résolution : physique, pratique. Conviction : mentale, "
        "philosophique. Une case absorbe autant de crans que son chiffre. "
        "Le stress s'efface en fin de scène."
    )
    return f.paragraphe(x, y + 14, note, largeur, ITALIQUE, 12.5, couleur=GRIS) - 8


def _dessiner_consequences(f, x, y, largeur):
    y = f.titre(x, y, "Conséquences", largeur)
    for nom, crans in CONSEQUENCES:
        f.case(x, y + 5)
        f.texte(x + 36, y + 23, nom, GRAS, 16)
        suite = x + 36 + stringWidth(nom + " ", GRAS, 16)
        f.texte(suite, y + 23, f"({crans} crans)", TEXTE, 13, GRIS)
        f.trait(x, x + largeur, y + 52)
        y += 57
    return y


def _dessiner_reputation(f, p, x, y, largeur):
    y = f.titre(x, y, "Réputation philosophique", largeur)
    centre = x + largeur / 2
    debut = centre - (7 * 15 + 6 * 8) / 2
    c = f.c
    for gauche, droite in AXES:
        position = 3 - p["reputation"].get(gauche, 0) + p["reputation"].get(droite, 0)
        f.texte(debut - 10, y + 21, gauche, TEXTE, 15, ENCRE, "d")
        f.texte(debut + 153 + 10, y + 21, droite, TEXTE, 15)
        for i in range(7):
            c.setStrokeColorRGB(*ENCRE)
            c.setFillColorRGB(*ENCRE)
            c.setLineWidth(1.5)
            c.setDash(2, 2) if i == 3 and i != position else c.setDash()
            cx = debut + 7.5 + i * 23
            c.circle(cx, -(y + 16), 6.75, stroke=1, fill=int(i == position))
        y += 32
    c.setDash()
    f.texte(
        centre,
        y + 14,
        "En fin de séance, un axe peut se déplacer d'un cran, justifié par un acte.",
        ITALIQUE,
        12.5,
        GRIS,
        "c",
    )
    return y + 20


def _dessiner_fiche(c, pied, p):
    c.saveState()
    c.translate(0, A4[1])
    c.scale(ECHELLE, ECHELLE)
    c.setFillColorRGB(*PAPIER)
    c.rect(0, -PAGE_H, PAGE_L, PAGE_H, stroke=0, fill=1)
    f = _Fiche(c)

    # En-tête : nom à gauche, points de Destin à droite.
    f.capitales(GAUCHE, 55, "Éthéria · Aventurier philosophe · Prétiré", 13, ACCENT)
    f.texte(GAUCHE, 104, p["nom"], TITRE, 50)
    f.texte(GAUCHE, 137, _maj(p["role"]), ITALIQUE, 20, GRIS)
    f.capitales(DROITE, 86, "Points de Destin", 12, GRIS, "d")
    for i in range(3):
        f.case(DROITE - 26 - i * 34, 96)
    f.texte(DROITE, 141, "3 en début de séance", ITALIQUE, 12.5, GRIS, "d")
    f.trait(GAUCHE, DROITE, 158, epaisseur=2)

    f.capitales(GAUCHE, 191, "Origine", 12, GRIS)
    f.capitales(GAUCHE + 468, 191, "Discipline", 12, GRIS)
    f.texte(GAUCHE + 468, 214, _maj(p["discipline"]), TEXTE, 17)
    y = f.paragraphe(GAUCHE, 214, _maj(p["origine"]), 440, TEXTE, 17)

    y = _dessiner_aspects(f, p, y + 2)

    y += 20
    colonne = (LARGEUR - 32) / 2
    bas_gauche = _dessiner_approches(f, p, GAUCHE, y, colonne)
    bas_droite = _dessiner_stunts_et_stress(f, p, GAUCHE + colonne + 32, y, colonne)

    y = max(bas_gauche, bas_droite) + 20
    etroite = (LARGEUR - 32) * 5 / 12
    bas_gauche = _dessiner_consequences(f, GAUCHE, y, etroite)
    bas_droite = _dessiner_reputation(
        f, p, GAUCHE + etroite + 32, y, LARGEUR - 32 - etroite
    )

    if max(bas_gauche, bas_droite) > BAS:
        raise _erreur(
            f"la fiche de « {p['nom']} » déborde de la page : raccourcis ses "
            "aspects ou ses stunts."
        )

    f.trait(GAUCHE, DROITE, 1066, FILET)
    f.texte(
        PAGE_L / 2, 1083, f"{pied} · Règles : Fate Accelerated", TEXTE, 12, GRIS, "c"
    )
    c.restoreState()
    c.showPage()


def render_fiches_pdf(jeu, pretires=None):
    """PDF des fiches d'un jeu : toutes, ou seulement celles données."""
    _enregistrer_polices()
    data = JEUX[jeu]
    tampon = io.BytesIO()
    c = canvas.Canvas(tampon, pagesize=A4)
    c.setTitle(f"Prétirés : {data['titre']}")
    for p in pretires or data["pretires"]:
        _dessiner_fiche(c, data["pied"], p)
    c.save()
    return tampon.getvalue()


def on_files(files, config):
    for jeu, data in JEUX.items():
        files.append(
            File.generated(
                config, f"assets/fiches/{jeu}.pdf", content=render_fiches_pdf(jeu)
            )
        )
        for p in data["pretires"]:
            files.append(
                File.generated(
                    config,
                    f"assets/fiches/{jeu}/{p['slug']}.pdf",
                    content=render_fiches_pdf(jeu, [p]),
                )
            )
    return files


# ============================================================
# Balises Markdown : {{ pretires: <jeu> }} et {{ fiches_pdf: <jeu> }}
#
# Les liens sont absolus (via site_url) et masqués à l'export PDF du
# site, pour les mêmes raisons que ceux des cartes : voir le
# commentaire au-dessus de _CARTES_PDF_MARKER_RE dans scripts/cards.py.
# ============================================================

_PRETIRES_MARKER_RE = re.compile(r"\{\{\s*pretires:\s*([a-z0-9-]+)\s*\}\}")
_FICHES_PDF_MARKER_RE = re.compile(r"\{\{\s*fiches_pdf:\s*([a-z0-9-]+)\s*\}\}")


def _url(config, chemin):
    base = config["site_url"] or "/"
    if not base.endswith("/"):
        base += "/"
    return base + chemin


def _section_pretire(config, jeu, p):
    url = _url(config, f"assets/fiches/{jeu}/{p['slug']}.pdf")
    approches = sorted(p["approches"].items(), key=lambda a: -a[1])
    reputation = ", ".join(
        f"{CRANS[crans]} vers {pole}" for pole, crans in p["reputation"].items()
    )
    lignes = [
        f"## {p['nom']}, {p['role']}",
        "",
        f'<p class="masque-en-pdf"><a href="{url}">Fiche à imprimer (PDF)</a></p>',
        "",
        f"- Origine : {p['origine']}. Discipline : {p['discipline']}.",
    ]
    lignes += [f"- {lib} : *{p['aspects'][cle]}*" for cle, lib in ASPECTS]
    if p["aspects"].get("libre"):
        lignes.append(f"- Aspect libre : *{p['aspects']['libre']}*")
    lignes.append(
        "- Approches : " + ", ".join(f"{nom} +{score}" for nom, score in approches)
    )
    lignes += [f"- Stunt, {s['nom']} : {s['effet']}" for s in p["stunts"]]
    lignes.append(f"- Réputation de départ : {_maj(reputation)}.")
    return "\n".join(lignes)


def _liens_fiches(config, jeu):
    data = JEUX[jeu]
    items = "\n".join(
        f'<li><a href="{_url(config, f"assets/fiches/{jeu}/{p['slug']}.pdf")}">'
        f"{p['nom']}</a></li>"
        for p in data["pretires"]
    )
    toutes = _url(config, f"assets/fiches/{jeu}.pdf")
    return (
        '<div class="masque-en-pdf">\n'
        "<p>Fiches des prétirés, une page A4 chacune, prêtes à imprimer "
        f'(<a href="{toutes}">toutes les fiches en un seul PDF</a>) :</p>\n'
        f"<ul>\n{items}\n</ul>\n</div>"
    )


def on_page_markdown(markdown, page, config, files):
    def _jeu(match, balise):
        jeu = match.group(1)
        if jeu not in JEUX:
            connus = ", ".join(sorted(JEUX))
            raise RuntimeError(
                f"{page.file.src_uri} : jeu de prétirés inconnu « {jeu} » dans "
                f"{{{{ {balise}: {jeu} }}}} (jeux connus : {connus})."
            )
        return jeu

    def _remplacer_pretires(match):
        jeu = _jeu(match, "pretires")
        return "\n\n".join(
            _section_pretire(config, jeu, p) for p in JEUX[jeu]["pretires"]
        )

    def _remplacer_fiches(match):
        return _liens_fiches(config, _jeu(match, "fiches_pdf"))

    markdown = _PRETIRES_MARKER_RE.sub(_remplacer_pretires, markdown)
    return _FICHES_PDF_MARKER_RE.sub(_remplacer_fiches, markdown)
