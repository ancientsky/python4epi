"""Drift guards for the four Jupyter Book 2 (MyST) tables of contents.

The TOC is written out in four files (book/ and book_en/, each with a student
``myst.yml`` and an instructor ``_instructor/myst.yml``, because MyST's
``extends`` replaces ``project.toc`` rather than appending to it). These tests
keep them consistent:

* each instructor TOC is its student TOC plus the Ch17 solutions entries, and
* the zh and en TOCs list the same files in the same structure, and
* the three Philippines-edition projects (``book_ph/{en,zh,fil}/myst.yml``)
  list the file stems of the production bible (``book_ph/PRODUCTION.md`` §4)
  in the same structure, with the same theme pin as the main book.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIGS = {
    ("zh", "student"): ROOT / "book" / "myst.yml",
    ("zh", "instructor"): ROOT / "book" / "_instructor" / "myst.yml",
    ("en", "student"): ROOT / "book_en" / "myst.yml",
    ("en", "instructor"): ROOT / "book_en" / "_instructor" / "myst.yml",
}
SOLUTIONS_CHAPTER = "chapters/17_solutions.md"
PH_LANGS = ("en", "zh", "fil")
PH_CONFIGS = {lang: ROOT / "book_ph" / lang / "myst.yml" for lang in PH_LANGS}
#: Chapter stems from book_ph/PRODUCTION.md §4 and whether each has a notebook.
PH_CHAPTERS = {
    "00_start_here": False,
    "01_python_with_ai": True,
    "02_privacy_first": True,
    "03_clean_linelist": True,
    "04_time_place_person": True,
    "05_find_the_source": True,
    "06_signals_and_thresholds": True,
    "07_forecast_timesfm": True,
    "08_maps": True,
    "09_dashboard": True,
    "10_wrap_up": False,
}


def _toc(lang: str, edition: str) -> list[dict[str, Any]]:
    config = yaml.safe_load(CONFIGS[(lang, edition)].read_text(encoding="utf-8"))
    return config["project"]["toc"]


def _files(entries: list[dict[str, Any]]) -> list[str]:
    out: list[str] = []
    for entry in entries:
        if "file" in entry:
            out.append(entry["file"])
        out += _files(entry.get("children", []))
    return out


def _structure(entries: list[dict[str, Any]]) -> list[Any]:
    """The TOC with titles stripped: only files, groups and nesting remain."""
    return [
        {
            "file": entry.get("file"),
            "group": "title" in entry and "file" not in entry,
            "children": _structure(entry.get("children", [])),
        }
        for entry in entries
    ]


def _without_solutions(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pruned = copy.deepcopy(entries)
    for entry in pruned:
        if "children" in entry:
            entry["children"] = [
                child
                for child in _without_solutions(entry["children"])
                if child.get("file") != SOLUTIONS_CHAPTER
            ]
    return [entry for entry in pruned if entry.get("file") != SOLUTIONS_CHAPTER]


@pytest.mark.parametrize("lang", ["zh", "en"])
def test_instructor_toc_is_student_toc_plus_solutions(lang: str):
    student = _toc(lang, "student")
    instructor = _toc(lang, "instructor")
    assert _without_solutions(instructor) == student

    extra = [f for f in _files(instructor) if f not in _files(student)]
    assert extra[0] == SOLUTIONS_CHAPTER
    assert extra[1:], "the solutions chapter lists no solution notebooks"
    assert all(f.startswith("chapters/solutions/") for f in extra[1:])
    assert not any("solution" in f for f in _files(student))


@pytest.mark.parametrize("edition", ["student", "instructor"])
def test_zh_and_en_tocs_match(edition: str):
    zh, en = _toc("zh", edition), _toc("en", edition)
    assert _structure(zh) == _structure(en)
    # Group titles exist in both languages and are translated, not copied.
    zh_titles = [e["title"] for e in zh if "title" in e]
    en_titles = [e["title"] for e in en if "title" in e]
    assert len(zh_titles) == len(en_titles) == 6
    assert not set(zh_titles) & set(en_titles)


@pytest.mark.parametrize("key", sorted(CONFIGS), ids=lambda k: "-".join(k))
def test_every_toc_file_exists(key: tuple[str, str]):
    project = CONFIGS[key].parent
    missing = [f for f in _files(_toc(*key)) if not (project / f).is_file()]
    assert not missing, f"{CONFIGS[key]}: {missing}"


def test_instructor_configs_extend_their_student_config():
    for lang in ("zh", "en"):
        config = yaml.safe_load(CONFIGS[(lang, "instructor")].read_text(encoding="utf-8"))
        assert config["extends"] == "../myst.yml"
        # Only the TOC may differ; everything else comes from the student file.
        assert set(config) == {"version", "extends", "project"}
        assert set(config["project"]) == {"toc"}


def _config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_theme_is_pinned_identically():
    templates = {
        lang: _config(CONFIGS[(lang, "student")])["site"]["template"] for lang in ("zh", "en")
    }
    templates |= {f"ph-{lang}": _config(path)["site"]["template"] for lang, path in PH_CONFIGS.items()}
    assert len(set(templates.values())) == 1, templates
    assert templates["zh"].startswith("https://github.com/myst-templates/book-theme/archive/")
    sha = templates["zh"].rsplit("/", 1)[-1].removesuffix(".zip")
    assert len(sha) == 40 and all(c in "0123456789abcdef" for c in sha), sha


# --- Philippines edition -----------------------------------------------------------


def _ph_toc(lang: str) -> list[dict[str, Any]]:
    return _config(PH_CONFIGS[lang])["project"]["toc"]


def test_ph_toc_follows_the_production_bible():
    expected = ["intro.md"]
    for stem, has_notebook in PH_CHAPTERS.items():
        expected.append(f"chapters/{stem}.md")
        if has_notebook:
            expected.append(f"chapters/notebooks/{stem}.ipynb")
    assert _files(_ph_toc("en")) == expected
    toc = _ph_toc("en")
    assert toc[0] == {"file": "intro.md"}
    acts = toc[1:]
    assert len(acts) == 4
    assert all("title" in act and "file" not in act for act in acts)  # title-only parents


@pytest.mark.parametrize("lang", ["zh", "fil"])
def test_ph_tocs_match_english(lang: str):
    en, other = _ph_toc("en"), _ph_toc(lang)
    assert _structure(other) == _structure(en)
    en_titles = [e["title"] for e in en if "title" in e]
    titles = [e["title"] for e in other if "title" in e]
    assert len(titles) == len(en_titles)
    assert not set(titles) & set(en_titles), "act titles must be translated"


@pytest.mark.parametrize("lang", PH_LANGS)
def test_ph_toc_files_exist(lang: str):
    project = PH_CONFIGS[lang].parent
    missing = [f for f in _files(_ph_toc(lang)) if not (project / f).is_file()]
    assert not missing, f"{PH_CONFIGS[lang]}: {missing}"


@pytest.mark.parametrize("lang", PH_LANGS)
def test_ph_config_matches_main_book_settings(lang: str):
    config = _config(PH_CONFIGS[lang])
    main = _config(CONFIGS[("zh", "student")])
    assert config["project"]["error_rules"] == main["project"]["error_rules"]
    options = config["site"]["options"]
    assert options["style"] == "_static/ph.css"
    assert options["folders"] is True
    assert set(config["site"]["parts"]) == {"navbar_end", "footer"}
    # zh and fil turn off MyST's English "Figure N:" caption prefix, like book/.
    numbering = config["project"].get("numbering", {}).get("figure", {})
    assert numbering.get("enabled", True) is (lang == "en")
    assert config["project"]["title"] != ""
