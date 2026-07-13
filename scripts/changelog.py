"""
Hook MkDocs : remplace `{{ changelog }}` par le contenu de CHANGELOG.md
dans les pages du wiki.

Injecté tel quel dans docs/changelog.md (voir mkdocs.yml), qui sert
d'annexe au site comme au PDF exporté.
"""

from pathlib import Path

_CHANGELOG = Path(__file__).resolve().parent.parent / "CHANGELOG.md"
_CHANGELOG_TEXT = _CHANGELOG.read_text(encoding="utf-8")


def on_page_markdown(markdown, page, config, files):
    return markdown.replace("{{ changelog }}", _CHANGELOG_TEXT)
