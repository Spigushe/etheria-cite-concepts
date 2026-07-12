"""
Extension Python-Markdown : callouts façon Obsidian / GitHub.

Syntaxe supportée :

    > [!VILLE] Lyon-sur-Rhone
    > Une ville marchande au bord du fleuve.

    > [!NOUVELLES]
    > Le duc a disparu depuis trois jours.

Contrairement à l'extension officielle "github-callouts" (limitée à
NOTE/TIP/IMPORTANT/WARNING/CAUTION), celle-ci accepte n'importe quel
type en majuscules, y compris avec des espaces ou accents
(ex: [!NOUVELLES], [!PNJ], [!FACTION]).

Le type est converti en classe CSS (minuscules, espaces -> tirets,
accents supprimés) pour permettre un style personnalisé dans le CSS.
Le titre affiché reprend le texte tel quel (respecte les accents/majuscules).
"""

import re
import unicodedata
import xml.etree.ElementTree as etree

from markdown import Markdown, util
from markdown.blockprocessors import BlockQuoteProcessor
from markdown.extensions import Extension


def slugify_type(kind: str) -> str:
    """Convertit '!NOUVELLES RECENTES' -> 'nouvelles-recentes' pour le CSS."""
    normalized = unicodedata.normalize("NFKD", kind)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only).strip("-").lower()
    return slug or "note"


class _ObsidianCalloutsBlockProcessor(BlockQuoteProcessor):
    # > [!TYPE] Titre optionnel
    # Le TYPE peut contenir lettres (accentuées), chiffres, espaces et tirets.
    REGEX = re.compile(
        r"((?:^|\n) *(?:[^>].*)?(?:^|\n))"
        r" {0,3}> *\[!([A-ZÀ-Ý0-9][A-ZÀ-Ý0-9 \-]*)\]"
        r"(?: +([^\n]*))?"
        r" *\n"
        r"(?: *> *\n)*"
        r"() *(?:> *[^\s\n]|[^\s\n>])",
    )

    def test(self, parent, block):
        return (
            bool(self.REGEX.search(block))
            and not self.parser.state.isstate("blockquote")
            and not util.nearing_recursion_limit()
        )

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        block = blocks.pop(0)
        m = self.REGEX.search(block)
        assert m

        before = block[: m.end(1)]
        rest = block[m.end(4) :]
        block_body = "\n".join(self.clean(line) for line in rest.split("\n"))
        self.parser.parseBlocks(parent, [before])

        kind = m.group(2).strip()
        custom_title = m.group(3)
        css_class = slugify_type(kind)

        admon = etree.SubElement(parent, "div", {"class": "admonition " + css_class})
        title = etree.SubElement(admon, "p", {"class": "admonition-title"})
        title.text = custom_title.strip() if custom_title else kind.title()

        self.parser.state.set("blockquote")
        self.parser.parseChunk(admon, block_body)
        self.parser.state.reset()


class ObsidianCalloutsExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        parser = md.parser
        parser.blockprocessors.register(
            _ObsidianCalloutsBlockProcessor(parser),
            "obsidian-callouts",
            21.2,  # juste avant le blockquote standard
        )


def makeExtension(**kwargs):
    return ObsidianCalloutsExtension(**kwargs)
