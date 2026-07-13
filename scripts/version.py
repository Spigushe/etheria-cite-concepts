"""
Hook MkDocs : remplace `{{ version }}` par le numéro de version courante
et `{{ changelog }}` par le contenu de CHANGELOG.md dans les pages du
wiki.

La version est lue depuis la première entrée `## [x.y.z]` de
CHANGELOG.md, pour rester synchronisée avec lui sans rien coder en dur
dans les pages (voir docs/index.md). Le changelog complet est injecté
tel quel dans docs/changelog.md (voir mkdocs.yml), qui sert d'annexe
au site comme au PDF exporté.
"""

import re
from pathlib import Path

_VERSION_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)
_CHANGELOG = Path(__file__).resolve().parent.parent / "CHANGELOG.md"
_CHANGELOG_TEXT = _CHANGELOG.read_text(encoding="utf-8")


def _read_version() -> str:
    match = _VERSION_RE.search(_CHANGELOG_TEXT)
    return match.group(1) if match else "0.0.0"


_VERSION = _read_version()


def on_page_markdown(markdown, page, config, files):
    markdown = markdown.replace("{{ version }}", _VERSION)
    markdown = markdown.replace("{{ changelog }}", _CHANGELOG_TEXT)
    return markdown
