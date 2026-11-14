"""Smoke tests for notebook JSON integrity and cross-tree parity.

These validate structure only (valid JSON, nbformat 4, non-empty cells) — they
do not execute notebooks. Full execution is exercised by the Jupyter Book build
in CI. Coverage spans every notebook tree we ship:

* ``notebooks/`` — standalone lesson + exercise/solution copies (Colab/local)
* ``book/chapters/{notebooks,exercises,solutions}`` — the zh site
* ``book_en/chapters/{notebooks,exercises,solutions}`` — the English site
* ``book_ph/{en,zh,fil}/chapters/notebooks`` — the Philippines edition
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
    Path("book_ph/en/chapters/notebooks"),
    Path("book_ph/zh/chapters/notebooks"),
    Path("book_ph/fil/chapters/notebooks"),
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


def test_ph_notebooks_mirrored_across_languages():
    """The three Philippines-edition trees ship the same notebooks, each
    starting with a title cell and the standard Colab setup cell."""
    names = {
        lang: sorted(p.name for p in Path(f"book_ph/{lang}/chapters/notebooks").glob("*.ipynb"))
        for lang in ("en", "zh", "fil")
    }
    assert names["en"], "no PH notebooks found"
    assert names["zh"] == names["en"] == names["fil"]
    for lang, lang_names in names.items():
        for name in lang_names:
            cells = json.loads(
                Path(f"book_ph/{lang}/chapters/notebooks/{name}").read_text(encoding="utf-8")
            )["cells"]
            assert cells[0]["cell_type"] == "markdown", f"{lang}/{name}: no title cell"
            setup = "".join(cells[1]["source"])
            assert "google.colab" in setup and "python4epi" in setup, f"{lang}/{name}"


def test_colab_setup_cell_makes_epi_learning_importable() -> None:
    """Every tracked notebook's Colab setup cell puts ``src`` on ``sys.path``.

    ``pip install -e .`` only becomes importable after a runtime restart, so the
    cell must add the path itself before any ``from epi_learning import ...``.
    """
    roots = ["notebooks", "book/chapters", "book_en/chapters", "book_ph"]
    paths = sorted(p for root in roots for p in Path(root).rglob("*.ipynb") if "_build" not in p.parts)
    assert paths, "no notebooks found"
    for path in paths:
        cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
        setup = next(
            ("".join(c["source"]) for c in cells if "google.colab" in "".join(c["source"])), ""
        )
        chdir = setup.find("os.chdir('/content/python4epi')")
        add_path = setup.find("sys.path.insert(0, '/content/python4epi/src')")
        assert 0 <= chdir < add_path, str(path)
