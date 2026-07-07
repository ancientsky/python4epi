"""Smoke tests for notebook JSON integrity and cross-tree parity.

These validate structure only (valid JSON, nbformat 4, non-empty cells) — they
do not execute notebooks. Full execution is exercised by the Jupyter Book build
in CI. Coverage spans every notebook tree we ship:

* ``notebooks/`` — standalone lesson + exercise/solution copies (Colab/local)
* ``book/chapters/{notebooks,exercises,solutions}`` — the zh site
* ``book_en/chapters/{notebooks,exercises,solutions}`` — the English site
"""

import json
from pathlib import Path

import pytest

NOTEBOOK_ROOTS = [
    Path("notebooks"),
    Path("book/chapters/notebooks"),
    Path("book/chapters/exercises"),
    Path("book/chapters/solutions"),
    Path("book_en/chapters/notebooks"),
    Path("book_en/chapters/exercises"),
    Path("book_en/chapters/solutions"),
]


def _all_notebooks() -> list[Path]:
    paths: list[Path] = []
    for root in NOTEBOOK_ROOTS:
        if root.is_dir():
            paths.extend(sorted(root.rglob("*.ipynb")))
    return paths


def test_notebook_roots_exist():
    # At least the standalone and zh-site notebook trees must be present.
    assert Path("notebooks").is_dir()
    assert Path("book/chapters/notebooks").is_dir()


@pytest.mark.parametrize("nb_path", _all_notebooks(), ids=str)
def test_notebook_is_valid_json(nb_path: Path):
    payload = json.loads(nb_path.read_text(encoding="utf-8"))
    assert payload["nbformat"] == 4, f"{nb_path}: expected nbformat 4"
    assert payload["cells"], f"{nb_path}: has no cells"


def test_standalone_notebooks_found():
    assert _all_notebooks(), "No notebooks found in any tree"


def test_book_notebooks_mirrored_in_standalone():
    """Drift guard: every lesson notebook in the zh site has a same-named
    standalone copy under ``notebooks/`` (so a notebook added to the book is
    not silently missing from the Colab/local set). Content may differ; this
    only checks that the mirror exists.
    """
    book_nbs = {p.name for p in Path("book/chapters/notebooks").glob("*.ipynb")}
    standalone_nbs = {p.name for p in Path("notebooks").glob("*.ipynb")}
    missing = sorted(book_nbs - standalone_nbs)
    assert not missing, f"Book notebooks with no standalone copy in notebooks/: {missing}"
