"""Tests for scripts/build_book.py (the Jupyter Book 2 build entry point).

Only the deterministic parts are tested here (URL mapping, post-build HTML
rewriting, redirect stubs, site assembly); running MyST itself is exercised
by the book build in CI.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "build_book", Path(__file__).resolve().parent.parent / "scripts" / "build_book.py"
)
assert _SPEC and _SPEC.loader
bb = importlib.util.module_from_spec(_SPEC)
sys.modules["build_book"] = bb
_SPEC.loader.exec_module(bb)

NOTEBOOK_PAGE = bb.Page(
    "chapters.notebooks.stats-basics", "Notebook", "/chapters/notebooks/03_stats_basics.ipynb"
)
ZH_STUDENT = bb.Edition("zh", "student")
ZH_INSTRUCTOR = bb.Edition("zh", "instructor")
EN_STUDENT = bb.Edition("en", "student")
EN_INSTRUCTOR = bb.Edition("en", "instructor")

PAGE_HTML = (
    '<!DOCTYPE html><html lang="en" class=""><head><meta charSet="utf-8"/>'
    "<title>03 Stats - Epi With Python</title>"
    '<meta property="og:title" content="03 Stats &amp; more - Epi With Python"/>'
    '<meta name="image" content="/_public/fig.svg"/>'
    '<meta property="og:image" content="/_public/fig.svg"/>'
    "</head><body>"
    '<a href="https://github.com/ancientsky/python4epi/blob/main/book/_instructor/chapters/x.md">src</a>'
    "</body></html>"
)


# --- Edition -----------------------------------------------------------------


def test_edition_paths_and_prefixes():
    assert ZH_STUDENT.project_dir == bb.REPO_ROOT / "book"
    assert ZH_INSTRUCTOR.project_dir == bb.REPO_ROOT / "book" / "_instructor"
    assert EN_INSTRUCTOR.project_dir == bb.REPO_ROOT / "book_en" / "_instructor"
    assert [e.prefix for e in bb.ALL_EDITIONS] == ["", "instructor/", "en/", "en/instructor/"]
    assert ZH_INSTRUCTOR.counterpart() == EN_INSTRUCTOR
    assert EN_STUDENT.counterpart() == ZH_STUDENT


def test_edition_rejects_unknown_values():
    with pytest.raises(ValueError, match="lang"):
        bb.Edition("fr", "student")
    with pytest.raises(ValueError, match="edition"):
        bb.Edition("zh", "teacher")


def test_every_edition_has_a_myst_config():
    for edition in bb.ALL_EDITIONS:
        assert (edition.project_dir / "myst.yml").is_file(), edition.label()


def test_instructor_projects_reach_shared_content():
    for edition in (ZH_INSTRUCTOR, EN_INSTRUCTOR):
        for name in ("chapters", "intro.md", "_static", "_site"):
            assert (edition.project_dir / name).exists(), f"{edition.label()}: {name}"


def test_base_url():
    assert bb.base_url("/python4epi", ZH_STUDENT) == "/python4epi"
    assert bb.base_url("/python4epi", EN_INSTRUCTOR) == "/python4epi/en/instructor"
    assert bb.base_url("", ZH_STUDENT) == ""
    assert bb.base_url("", EN_STUDENT) == "/en"
    with pytest.raises(ValueError, match="start with"):
        bb.base_url("python4epi", ZH_STUDENT)


# --- URL mapping ---------------------------------------------------------------


def test_url_path():
    assert bb.url_path("index") == ""
    assert bb.url_path("chapters.fundamentals") == "chapters/fundamentals/"
    assert bb.url_path("chapters.notebooks.stats-basics") == "chapters/notebooks/stats-basics/"
    with pytest.raises(ValueError):
        bb.url_path("")


def test_legacy_path():
    assert bb.legacy_path("/intro.md") == "intro.html"
    assert bb.legacy_path("/chapters/01_fundamentals.md") == "chapters/01_fundamentals.html"
    assert (
        bb.legacy_path("/chapters/notebooks/03_stats_basics.ipynb")
        == "chapters/notebooks/03_stats_basics.html"
    )
    with pytest.raises(ValueError):
        bb.legacy_path("/chapters/data.csv")


def test_colab_url():
    assert bb.colab_url("book_en", "/chapters/notebooks/03_stats_basics.ipynb") == (
        "https://colab.research.google.com/github/ancientsky/python4epi/blob/main/"
        "book_en/chapters/notebooks/03_stats_basics.ipynb"
    )
    with pytest.raises(ValueError, match="not a notebook"):
        bb.colab_url("book", "/chapters/03_stats.md")


def test_page_slugs_reads_index_and_toc_pages():
    config = {
        "projects": [
            {
                "index": "index",
                "pages": [
                    {"title": "Act I", "level": 1},
                    {"slug": "chapters.guide", "level": 2},
                ],
            }
        ]
    }
    assert bb.page_slugs(config) == ["index", "chapters.guide"]
    with pytest.raises(ValueError, match="exactly one"):
        bb.page_slugs({"projects": []})


# --- HTML rewriting ------------------------------------------------------------


def test_set_html_lang():
    new = bb.set_html_lang('<html lang="en" class="">', "zh-Hant")
    assert new == '<html lang="zh-Hant" class="">'
    with pytest.raises(ValueError):
        bb.set_html_lang("<html>", "en")


def test_fix_source_links_only_for_instructor():
    link = "https://github.com/ancientsky/python4epi/edit/main/book_en/_instructor/chapters/a.md"
    assert bb.fix_source_links(link, EN_INSTRUCTOR).endswith("/edit/main/book_en/chapters/a.md")
    assert bb.fix_source_links(link, EN_STUDENT) == link


def test_upsert_meta_edits_in_place():
    html, existed = bb.upsert_meta(PAGE_HTML, "property", "og:image", "https://x/a.png")
    assert existed
    assert '<meta property="og:image" content="https://x/a.png"/>' in html
    assert html.count("og:image") == 1
    unchanged, existed = bb.upsert_meta(PAGE_HTML, "property", "og:url", "https://x/")
    assert not existed
    assert unchanged == PAGE_HTML


def _process(edition: bb.Edition, has_counterpart: bool = True) -> str:
    return bb.process_page_html(
        PAGE_HTML,
        NOTEBOOK_PAGE,
        edition,
        base_path="/python4epi",
        has_counterpart=has_counterpart,
        colab={"chapters/notebooks/stats-basics/": "https://colab.example/nb"},
    )


def test_process_page_html_head_tags():
    html = _process(ZH_INSTRUCTOR)
    url = "https://ancientsky.github.io/python4epi/instructor/chapters/notebooks/stats-basics/"
    assert html.startswith('<!DOCTYPE html><html lang="zh-Hant"')
    assert f'<meta property="og:url" content="{url}"/>' in html
    assert f'<link rel="canonical" href="{url}"/>' in html
    image = "https://ancientsky.github.io/python4epi/instructor/_static/og-image.png"
    assert f'<meta property="og:image" content="{image}"/>' in html
    assert f'<meta name="image" content="{image}"/>' in html
    assert '<meta name="twitter:card" content="summary_large_image"/>' in html
    # The title is reused (and stays escaped) for Twitter.
    assert 'name="twitter:title" content="03 Stats &amp; more - Epi With Python"' in html
    assert '<meta property="og:locale" content="zh_TW"/>' in html
    assert f'hreflang="zh-Hant" href="{url}"' in html
    en_url = "https://ancientsky.github.io/python4epi/en/instructor/chapters/notebooks/stats-basics/"
    assert f'hreflang="en" href="{en_url}"' in html
    assert f'hreflang="x-default" href="{url}"' in html
    # Instructor source links point at the real file, not the symlink.
    assert "/blob/main/book/chapters/x.md" in html
    assert '<script src="/python4epi/instructor/_static/epi-site.js" defer></script>' in html


def test_process_page_html_config_script():
    html = _process(EN_STUDENT)
    start = html.index("window.EPI_SITE=") + len("window.EPI_SITE=")
    config = json.loads(html[start : html.index(";</script>", start)])
    assert config["root"] == "/python4epi/en/"
    assert config["alternate"]["root"] == "/python4epi/"
    assert config["alternate"]["hreflang"] == "zh-Hant"
    assert config["htmlLang"] == "en"
    assert config["colab"] == {"chapters/notebooks/stats-basics/": "https://colab.example/nb"}


def test_process_page_html_without_counterpart_has_no_other_hreflang():
    html = _process(EN_STUDENT, has_counterpart=False)
    assert 'hreflang="zh-Hant"' not in html
    assert 'hreflang="x-default" href="https://ancientsky.github.io/python4epi/en/' in html


def test_process_page_html_is_idempotent():
    once = _process(ZH_STUDENT)
    twice = bb.process_page_html(
        once, NOTEBOOK_PAGE, ZH_STUDENT, base_path="/python4epi", has_counterpart=True, colab={}
    )
    assert twice == once


def test_redirect_stub():
    stub = bb.redirect_stub("/python4epi/chapters/stats/", "https://h/chapters/stats/", "zh-Hant")
    assert '<meta http-equiv="refresh" content="0; url=/python4epi/chapters/stats/"/>' in stub
    assert 'location.replace("/python4epi/chapters/stats/" + location.hash)' in stub
    assert '<link rel="canonical" href="https://h/chapters/stats/"/>' in stub


def test_count_warnings():
    log = "⚠️  a\nok\n  ⚠️  b\n⛔️ c\n"
    assert bb.count_warnings(log) == 2


# --- postprocess on a fake build ------------------------------------------------


def _fake_build(project: Path, pages: dict[str, tuple[str, str]]) -> None:
    """Write a minimal MyST ``_build`` tree: slug -> (kind, location)."""
    site = project / "_build" / "site"
    (site / "content").mkdir(parents=True)
    config = {
        "projects": [
            {"index": "index", "pages": [{"slug": s, "level": 1} for s in pages if s != "index"]}
        ]
    }
    (site / "config.json").write_text(json.dumps(config), encoding="utf-8")
    for slug, (kind, location) in pages.items():
        data = {"slug": slug, "kind": kind, "location": location, "frontmatter": {}}
        (site / "content" / f"{slug}.json").write_text(json.dumps(data), encoding="utf-8")
        page_file = project / "_build" / "html" / bb.url_path(slug) / "index.html"
        page_file.parent.mkdir(parents=True, exist_ok=True)
        page_file.write_text(PAGE_HTML, encoding="utf-8")


def _patch_repo(monkeypatch: pytest.MonkeyPatch, root: Path) -> None:
    monkeypatch.setattr(bb, "REPO_ROOT", root)
    static = root / "book" / "_static"
    static.mkdir(parents=True, exist_ok=True)
    for name in bb.STATIC_FILES:
        (static / name).write_text(name, encoding="utf-8")


PAGES = {
    "index": ("Article", "/intro.md"),
    "chapters.stats": ("Article", "/chapters/03_stats.md"),
    "chapters.notebooks.stats-basics": ("Notebook", "/chapters/notebooks/03_stats_basics.ipynb"),
}


def test_postprocess_end_to_end(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _patch_repo(monkeypatch, tmp_path)
    (tmp_path / "book_en" / "chapters").mkdir(parents=True)
    (tmp_path / "book_en" / "chapters" / "03_stats.md").write_text("x", encoding="utf-8")
    _fake_build(tmp_path / "book", PAGES)

    stats = bb.postprocess(ZH_STUDENT, "/python4epi")
    assert stats == {"pages": 3, "notebooks": 1, "redirects": 3}

    html_dir = tmp_path / "book" / "_build" / "html"
    assert (html_dir / "_static" / "epi-site.js").is_file()
    chapter = (html_dir / "chapters" / "stats" / "index.html").read_text(encoding="utf-8")
    assert 'hreflang="en"' in chapter  # book_en has the file
    notebook = (html_dir / "chapters/notebooks/stats-basics/index.html").read_text(encoding="utf-8")
    assert 'hreflang="en"' not in notebook  # book_en lacks it
    assert "book/chapters/notebooks/03_stats_basics.ipynb" in notebook  # Colab map
    stub = (html_dir / "chapters/notebooks/03_stats_basics.html").read_text(encoding="utf-8")
    assert "url=/python4epi/chapters/notebooks/stats-basics/" in stub
    assert "url=/python4epi/" in (html_dir / "intro.html").read_text(encoding="utf-8")

    # Re-running changes nothing and writes no new redirects.
    assert bb.postprocess(ZH_STUDENT, "/python4epi")["redirects"] == 0
    assert (html_dir / "chapters" / "stats" / "index.html").read_text(encoding="utf-8") == chapter


def test_postprocess_rejects_solutions_in_student_edition(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    _patch_repo(monkeypatch, tmp_path)
    _fake_build(tmp_path / "book", PAGES)
    leaked = tmp_path / "book" / "_build" / "html" / "_public" / "03_stats_solution-abc.ipynb"
    leaked.parent.mkdir(parents=True)
    leaked.write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit, match="solution"):
        bb.postprocess(ZH_STUDENT, "/python4epi")


def test_find_solution_files_flags_solution_pages(tmp_path: Path):
    location = "/chapters/solutions/03_stats_solution.ipynb"
    pages = [bb.Page("chapters.solutions.stats-solution", "Notebook", location)]
    assert bb.find_solution_files(tmp_path, pages) == [location]
    assert bb.find_solution_files(tmp_path, [bb.Page("index", "Article", "/intro.md")]) == []


def test_assemble_site(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _patch_repo(monkeypatch, tmp_path)
    for edition in bb.ALL_EDITIONS:
        html = edition.html_dir
        html.mkdir(parents=True)
        (html / "index.html").write_text(
            f"{bb.POSTBUILD_MARKER}{edition.label()}", encoding="utf-8"
        )
    site = tmp_path / "site"
    bb.assemble_site(list(bb.ALL_EDITIONS), site)
    assert "zh student" in (site / "index.html").read_text(encoding="utf-8")
    assert "zh instructor" in (site / "instructor" / "index.html").read_text(encoding="utf-8")
    assert "en student" in (site / "en" / "index.html").read_text(encoding="utf-8")
    assert "en instructor" in (site / "en/instructor/index.html").read_text(encoding="utf-8")


def test_assemble_site_refuses_repo_dirs():
    with pytest.raises(ValueError, match="refusing"):
        bb.assemble_site([], bb.REPO_ROOT)


def test_parse_args():
    args = bb.parse_args(["--lang", "en", "--edition", "instructor"])
    assert (args.lang, args.edition, args.all) == ("en", "instructor", False)
    assert bb.parse_args(["--all"]).all
    for bad in ([], ["--lang", "zh"], ["--all", "--lang", "zh"]):
        with pytest.raises(SystemExit):
            bb.parse_args(bad)


# --- internal link check ---------------------------------------------------------


def _site(tmp_path: Path, pages: dict[str, str]) -> Path:
    for rel, body in pages.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"<html><head></head><body>{body}</body></html>", encoding="utf-8")
    return tmp_path


def test_resolve_static(tmp_path: Path):
    site = _site(tmp_path, {"index.html": "", "a/index.html": "", "f.html": ""})
    assert bb.resolve_static(site, "") == site / "index.html"
    assert bb.resolve_static(site, "a/") == site / "a" / "index.html"
    assert bb.resolve_static(site, "a") == site / "a" / "index.html"
    assert bb.resolve_static(site, "f.html") == site / "f.html"
    assert bb.resolve_static(site, "missing/") is None


def test_broken_links_finds_the_doubled_base_path(tmp_path: Path):
    # The shape of the book-theme 2.0.0 breadcrumb bug: base path doubled.
    site = _site(
        tmp_path,
        {
            "index.html": '<a href="/python4epi/chapters/x">ok</a>',
            "chapters/x/index.html": (
                '<a href="/python4epi/python4epi/chapters">crumb</a>'
                '<a href="/python4epi/">home</a>'
                '<a href="../y/">relative, missing</a>'
                '<a href="#top">anchor</a>'
                '<a href="https://github.com/x">external</a>'
                '<a href="mailto:a@b.c">mail</a>'
                "<script>var s='<a href=\"/nowhere\">';</script>"
            ),
        },
    )
    broken = bb.broken_links(site, "/python4epi/")
    assert broken == {
        "/python4epi/python4epi/chapters": ["chapters/x/index.html"],
        "../y/": ["chapters/x/index.html"],
    }


def test_broken_links_skips_other_editions_only(tmp_path: Path):
    site = _site(
        tmp_path,
        {
            "index.html": (
                '<a href="/python4epi/en/instructor/a/">nested edition</a>'
                '<a href="/python4epi/instructor/b/">sibling edition</a>'
                '<a href="/python4epi/en/missing/">own edition, missing</a>'
                '<a href="/elsewhere/">outside the site</a>'
            )
        },
    )
    others = ("/python4epi/", "/python4epi/instructor/", "/python4epi/en/instructor/")
    broken = bb.broken_links(site, "/python4epi/en/", others)
    assert set(broken) == {"/python4epi/en/missing/", "/elsewhere/"}
    with pytest.raises(ValueError, match="end with"):
        bb.broken_links(site, "/python4epi")


def test_check_links_fails_the_build(tmp_path: Path):
    site = _site(tmp_path, {"index.html": '<a href="/python4epi/gone/">x</a>'})
    with pytest.raises(SystemExit, match="1 broken internal link"):
        bb.check_links(site, "/python4epi/", "zh student")
    ok_site = _site(tmp_path / "ok", {"index.html": "<a href='#'>x</a>"})
    bb.check_links(ok_site, "/python4epi/", "ok")


def test_postprocess_rejects_broken_internal_links(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    _patch_repo(monkeypatch, tmp_path)
    _fake_build(tmp_path / "book", PAGES)
    page = tmp_path / "book" / "_build" / "html" / "chapters" / "stats" / "index.html"
    page.write_text(PAGE_HTML.replace("</body>", '<a href="/python4epi/nope/">x</a></body>'))
    with pytest.raises(SystemExit, match="broken internal link"):
        bb.postprocess(ZH_STUDENT, "/python4epi")
