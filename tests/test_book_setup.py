"""Tests for epi_learning.book_setup (kernel setup used by the book build)."""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path

import matplotlib
import pytest

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from epi_learning import book_setup


def _make_repo(root: Path) -> Path:
    (root / "data" / "synthetic").mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    nested = root / "book" / "chapters" / "notebooks"
    nested.mkdir(parents=True)
    return nested


def test_find_repo_root_walks_up(tmp_path: Path):
    nested = _make_repo(tmp_path)
    assert book_setup.find_repo_root(nested) == tmp_path.resolve()


def test_find_repo_root_ignores_data_symlinks_without_pyproject(tmp_path: Path):
    nested = _make_repo(tmp_path)
    # book/data -> ../data exists in the repo; it must not stop the search.
    (tmp_path / "book" / "data").symlink_to(tmp_path / "data")
    assert book_setup.find_repo_root(nested) == tmp_path.resolve()


def test_find_repo_root_gives_up(tmp_path: Path):
    nested = _make_repo(tmp_path)
    assert book_setup.find_repo_root(nested, max_levels=1) is None
    with pytest.raises(ValueError, match="max_levels"):
        book_setup.find_repo_root(nested, max_levels=-1)


def test_the_real_repo_is_found():
    here = Path(__file__).resolve().parent
    assert (book_setup.find_repo_root(here) / "data" / "synthetic").is_dir()


def test_configure_book_kernel(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    nested = _make_repo(tmp_path)
    fake_pio = types.SimpleNamespace(renderers=types.SimpleNamespace(default="plotly_mimetype"))
    monkeypatch.setitem(sys.modules, "plotly.io", fake_pio)
    monkeypatch.chdir(nested)
    monkeypatch.delenv(book_setup.TSFM_MODE_ENV, raising=False)
    with plt.style.context("default"):
        root = book_setup.configure_book_kernel()
        # the build replays committed TimesFM forecasts instead of running the model
        assert os.environ[book_setup.TSFM_MODE_ENV] == "cache"
        assert root == tmp_path.resolve()
        assert Path(os.getcwd()).resolve() == tmp_path.resolve()
        assert plt.rcParams["figure.dpi"] == book_setup.FIGURE_DPI
        assert plt.rcParams["axes.unicode_minus"] is False
        # ggplot's signature grey axes background
        assert matplotlib.colors.to_hex(plt.rcParams["axes.facecolor"]) == "#e5e5e5"
        assert "Noto Sans CJK TC" in plt.rcParams["font.sans-serif"]
    assert fake_pio.renderers.default == book_setup.PLOTLY_RENDERER


def test_configure_book_kernel_outside_repo_keeps_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.chdir(tmp_path)
    with plt.style.context("default"):
        assert book_setup.configure_book_kernel() is None
    assert Path(os.getcwd()).resolve() == tmp_path.resolve()
