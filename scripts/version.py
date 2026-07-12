"""
Hook MkDocs : remplace `{{ version }}` par le numéro de version courant
dans les pages du wiki.

La version est lue depuis la première entrée `## [x.y.z]` de
CHANGELOG.md, pour rester synchronisée avec lui sans rien coder en dur
dans les pages (voir docs/index.md).
"""

import re
from pathlib import Path

_VERSION_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)
_CHANGELOG = Path(__file__).resolve().parent.parent / "CHANGELOG.md"


def _read_version() -> str:
    text = _CHANGELOG.read_text(encoding="utf-8")
    match = _VERSION_RE.search(text)
    return match.group(1) if match else "0.0.0"


_VERSION = _read_version()


def on_page_markdown(markdown, page, config, files):
    return markdown.replace("{{ version }}", _VERSION)
