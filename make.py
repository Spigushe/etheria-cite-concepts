"""Tâches du dépôt, « style Makefile » : `uv run python make.py <tâche>`.

Windows n'a pas `make` : ce script le remplace, avec les mêmes commandes
en local et en CI. `python make.py` sans argument liste les tâches.
"""

import io
import os
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).parent

# En CI, l'environnement est déjà synchronisé (`uv sync --locked`).
UV_RUN = ["uv", "run"] + (["--no-sync"] if os.environ.get("CI") else [])
PY_SOURCES = ["scripts/", "make.py"]


def run(*cmd: str, env: dict[str, str] | None = None) -> None:
    """Lance une commande depuis la racine ; s'arrête à la première erreur."""
    exe = shutil.which(cmd[0]) or cmd[0]  # résout npx.cmd sous Windows
    print(f"$ {' '.join(cmd)}", flush=True)
    result = subprocess.run(
        [exe, *cmd[1:]], cwd=ROOT, env={**os.environ, **(env or {})}, check=False
    )
    if result.returncode:
        sys.exit(result.returncode)


def sync() -> None:
    """Installe les dépendances figées (uv.lock)."""
    run("uv", "sync", "--locked")


def dev() -> None:
    """Serveur de dev avec rechargement, sans export PDF."""
    run(*UV_RUN, "python", "-m", "mkdocs", "serve", "-f", "mkdocs.dev.yml")


def build() -> None:
    """Build strict local, sans export PDF (config dev)."""
    run(*UV_RUN, "python", "-m", "mkdocs", "build", "--strict", "-f", "mkdocs.dev.yml")


def build_pdf() -> None:
    """Build strict de prod avec export PDF (CI Linux ; WeasyPrint requis)."""
    run(
        *UV_RUN, "python", "-m", "mkdocs", "build", "--strict",
        env={"ENABLE_PDF_EXPORT": "1"},
    )  # fmt: skip


def lint() -> None:
    """Ruff : lint et contrôle du formatage."""
    run(*UV_RUN, "ruff", "check", *PY_SOURCES)
    run(*UV_RUN, "ruff", "format", "--check", *PY_SOURCES)


def fmt() -> None:
    """Applique le formatage ruff et les corrections automatiques."""
    run(*UV_RUN, "ruff", "check", "--fix", *PY_SOURCES)
    run(*UV_RUN, "ruff", "format", *PY_SOURCES)


def types() -> None:
    """Typage Python (ty)."""
    run(*UV_RUN, "ty", "check")


def spell() -> None:
    """Orthographe (cspell, dictionnaire français)."""
    run(
        "npx", "--yes", "--package", "cspell", "--package", "@cspell/dict-fr-fr",
        "--", "cspell", "--config", "cspell.json", "--no-progress",
    )  # fmt: skip


def mdlint() -> None:
    """Lint Markdown. Version figée : une nouvelle règle ne doit pas casser la CI."""
    run("npx", "--yes", "markdownlint-cli2@0.24.1")


def check() -> None:
    """Toutes les vérifications rapides (sans build)."""
    lint()
    types()
    spell()
    mdlint()


def ci() -> None:
    """Ce que fait la CI : vérifications puis build strict avec PDF."""
    check()
    build_pdf()


def clean() -> None:
    """Supprime le dossier `site/` généré."""
    shutil.rmtree(ROOT / "site", ignore_errors=True)
    print("site/ supprimé")


TASKS: dict[str, Callable[[], None]] = {
    "sync": sync,
    "dev": dev,
    "build": build,
    "build-pdf": build_pdf,
    "lint": lint,
    "fmt": fmt,
    "types": types,
    "spell": spell,
    "mdlint": mdlint,
    "check": check,
    "ci": ci,
    "clean": clean,
}


def main(args: list[str]) -> None:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    if not args or any(a not in TASKS for a in args):
        unknown = [a for a in args if a not in TASKS]
        if unknown:
            print(f"Tâche inconnue : {', '.join(unknown)}\n")
        print("Tâches disponibles :")
        for name, fn in TASKS.items():
            print(f"  {name:<10} {(fn.__doc__ or '').splitlines()[0]}")
        sys.exit(1 if unknown else 0)
    for name in args:
        TASKS[name]()


if __name__ == "__main__":
    main(sys.argv[1:])
