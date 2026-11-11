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
PH_EN = bb.Edition("en", "student", "ph")
PH_ZH = bb.Edition("zh", "student", "ph")
PH_FIL = bb.Edition("fil", "student", "ph")

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
    assert [e.prefix for e in bb.MAIN_EDITIONS] == ["", "instructor/", "en/", "en/instructor/"]
    assert [e.prefix for e in bb.PH_EDITIONS] == ["ph/", "ph/zh/", "ph/fil/"]
    assert bb.ALL_EDITIONS == bb.MAIN_EDITIONS + bb.PH_EDITIONS
    assert ZH_INSTRUCTOR.counterpart() == EN_INSTRUCTOR
    assert EN_STUDENT.counterpart() == ZH_STUDENT


def test_edition_rejects_unknown_values():
    with pytest.raises(ValueError, match="lang"):
        bb.Edition("fr", "student")
    with pytest.raises(ValueError, match="edition"):
        bb.Edition("zh", "teacher")
    with pytest.raises(ValueError, match="lang"):
        bb.Edition("fil", "student")  # the main book has no Filipino edition
    with pytest.raises(ValueError, match="edition"):
        bb.Edition("en", "instructor", "ph")
    with pytest.raises(ValueError, match="series"):
        bb.Edition("en", "student", "jp")


def test_ph_edition_properties():
    assert PH_EN.project_dir == bb.REPO_ROOT / "book_ph" / "en"
    assert PH_FIL.tree == "book_ph/fil"
    assert PH_ZH.html_dir == bb.REPO_ROOT / "book_ph" / "zh" / "_build" / "html"
    assert PH_EN.is_ph and not ZH_STUDENT.is_ph
    assert PH_ZH.meta["html_lang"] == "zh-Hant"
    assert PH_FIL.meta["html_lang"] == "fil"
    assert [e.lang for e in PH_ZH.alternates()] == ["en", "fil"]
    assert ZH_INSTRUCTOR.alternates() == (EN_INSTRUCTOR,)
    assert PH_FIL.label() == "ph fil"
    assert bb.base_url("/python4epi", PH_ZH) == "/python4epi/ph/zh"
    assert bb.base_url("", PH_EN) == "/ph"
    with pytest.raises(ValueError, match="alternates"):
        PH_EN.counterpart()


def test_ph_projects_share_static_and_images():
    for edition in bb.PH_EDITIONS:
        project = edition.project_dir
        assert (project / "_static").resolve() == bb.REPO_ROOT / "book_ph" / "_static"
        assert (project / "chapters" / "images").resolve() == bb.REPO_ROOT / "book_ph" / "images"
        for part in ("navbar_end.md", "footer.md"):
            assert (project / "_site" / part).is_file(), f"{edition.label()}: {part}"
    assert (bb.REPO_ROOT / bb.PH_STATIC_DIR / "ph-site.js").is_file()
    assert bb.DASHBOARD_SCRIPT.is_file()


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


# --- Philippines edition ----------------------------------------------------------

PH_NOTEBOOK = bb.Page("chapters.notebooks.maps", "Notebook", "/chapters/notebooks/08_maps.ipynb")


def _ph_config(html: str) -> dict:
    start = html.index("window.EPI_SITE=") + len("window.EPI_SITE=")
    return json.loads(html[start : html.index(";</script>", start)])


def test_process_page_html_ph_head_and_config():
    html = bb.process_page_html(
        PAGE_HTML,
        PH_NOTEBOOK,
        PH_FIL,
        base_path="/python4epi",
        alternate_langs=("en", "zh"),
        colab={"chapters/notebooks/maps/": "https://colab.example/nb"},
        static_files=("ph-site.js", "ph-games.css", "ph-games.js"),
    )
    site = "https://ancientsky.github.io/python4epi"
    assert html.startswith('<!DOCTYPE html><html lang="fil"')
    assert f'<link rel="canonical" href="{site}/ph/fil/chapters/notebooks/maps/"/>' in html
    for tag, prefix in (("en", "ph/"), ("zh-Hant", "ph/zh/"), ("fil", "ph/fil/")):
        assert f'hreflang="{tag}" href="{site}/{prefix}chapters/notebooks/maps/"' in html
    assert f'hreflang="x-default" href="{site}/ph/chapters/notebooks/maps/"' in html
    # One og:locale:alternate per other language.
    assert html.count('property="og:locale:alternate"') == 2
    assert '<meta property="og:locale" content="tl_PH"/>' in html
    assert 'content="Bantay Python · Epi With Python"' in html
    # Styles, then the config, then the scripts in contract order; no YouTube.
    order = [
        '<link rel="stylesheet" href="/python4epi/ph/fil/_static/ph-games.css"/>',
        "window.EPI_SITE=",
        '<script src="/python4epi/ph/fil/_static/epi-site.js" defer>',
        '<script src="/python4epi/ph/fil/_static/ph-site.js" defer>',
        '<script src="/python4epi/ph/fil/_static/ph-games.js" defer>',
    ]
    positions = [html.index(snippet) for snippet in order]
    assert positions == sorted(positions)
    assert "youtube-lite.js" not in html

    config = _ph_config(html)
    assert config["lang"] == "fil" and config["series"] == "ph"
    assert config["root"] == "/python4epi/ph/fil/"
    assert "alternate" not in config  # keeps epi-site.js's book-only part inert
    assert [lang["root"] for lang in config["languages"]] == [
        "/python4epi/ph/",
        "/python4epi/ph/zh/",
        "/python4epi/ph/fil/",
    ]
    assert config["book"]["root"] == "/python4epi/en/"
    assert config["standalone"] == ["dashboard/"]
    assert config["colab"] == {"chapters/notebooks/maps/": "https://colab.example/nb"}


def test_ph_zh_links_back_to_the_zh_book_and_skips_missing_optional_files():
    html = bb.process_page_html(
        PAGE_HTML,
        PH_NOTEBOOK,
        PH_ZH,
        base_path="",
        alternate_langs=(),
        colab={},
        static_files=("ph-site.js",),
    )
    assert _ph_config(html)["book"]["root"] == "/"
    assert "ph-games" not in html
    assert '<script src="/ph/zh/_static/ph-site.js" defer>' in html
    assert 'hreflang="en"' not in html  # no alternate page
    assert 'hreflang="x-default" href="https://ancientsky.github.io/python4epi/ph/zh/' in html


def _patch_ph_static(root: Path, *names: str) -> None:
    static = root / "book_ph" / "_static"
    static.mkdir(parents=True, exist_ok=True)
    for name in names:
        (static / name).write_text(name, encoding="utf-8")


PH_PAGES = {
    "index": ("Article", "/intro.md"),
    "chapters.dashboard": ("Article", "/chapters/09_dashboard.md"),
    "chapters.notebooks.maps": ("Notebook", "/chapters/notebooks/08_maps.ipynb"),
}


def test_postprocess_ph_end_to_end(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    _patch_repo(monkeypatch, tmp_path)
    _patch_ph_static(tmp_path, "ph-site.js", "ph-games.js")  # no ph-games.css yet
    (tmp_path / "book_ph" / "zh" / "chapters").mkdir(parents=True)
    (tmp_path / "book_ph" / "zh" / "chapters" / "09_dashboard.md").write_text("x")
    _fake_build(tmp_path / "book_ph" / "en", PH_PAGES)
    chapter = tmp_path / "book_ph/en/_build/html/chapters/dashboard/index.html"
    # The documented way to link the dashboard: [text](/dashboard/), which MyST
    # renders with the edition's BASE_URL in front.
    chapter.write_text(
        PAGE_HTML.replace("</body>", '<a class="link" href="/python4epi/ph/dashboard/">d</a></body>')
    )
    calls = []
    real_builder = bb.load_dashboard_builder()

    def fake_dashboard(lang: str, out_dir: Path) -> Path:
        calls.append((lang, out_dir))
        return real_builder(lang, out_dir)

    monkeypatch.setattr(bb, "load_dashboard_builder", lambda: fake_dashboard)
    stats = bb.postprocess(PH_EN, "/python4epi")
    assert stats == {"pages": 3, "notebooks": 1, "redirects": 0, "standalone": 1}

    html_dir = tmp_path / "book_ph" / "en" / "_build" / "html"
    assert calls == [("en", html_dir / "dashboard")]
    assert (html_dir / "dashboard" / "index.html").is_file()
    assert sorted(p.name for p in (html_dir / "_static").iterdir()) == [
        "epi-site.js",
        "og-image.png",
        "ph-games.js",
        "ph-site.js",
    ]
    assert "ph-games.css is missing" in capsys.readouterr().out
    page = chapter.read_text(encoding="utf-8")
    assert '<html lang="en"' in page
    assert 'hreflang="zh-Hant"' in page and 'hreflang="fil"' not in page
    assert "ph-games.css" not in page and "_static/ph-games.js" in page
    notebook = (html_dir / "chapters/notebooks/maps/index.html").read_text(encoding="utf-8")
    assert "blob/main/book_ph/en/chapters/notebooks/08_maps.ipynb" in notebook
    assert not list(html_dir.glob("chapters/*.html"))  # no JB1 redirect stubs


def test_postprocess_ph_requires_ph_site_js(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _patch_repo(monkeypatch, tmp_path)
    _patch_ph_static(tmp_path)
    _fake_build(tmp_path / "book_ph" / "zh", PH_PAGES)
    with pytest.raises(SystemExit, match="ph-site.js"):
        bb.postprocess(PH_ZH, "/python4epi")


def test_ph_og_image_prefers_the_language_card(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _patch_repo(monkeypatch, tmp_path)
    _patch_ph_static(tmp_path, "ph-site.js", "og-image.png", "og-image_fil.png")
    dst = tmp_path / "out"
    dst.mkdir()
    bb.copy_static(PH_FIL, dst)
    assert (dst / "og-image.png").read_text() == "og-image_fil.png"
    bb.copy_static(PH_ZH, dst)
    assert (dst / "og-image.png").read_text() == "og-image.png"


def test_dashboard_builder_placeholder(tmp_path: Path):
    build = bb.load_dashboard_builder()
    for lang in bb.PH_LANGS:
        page = build(lang, tmp_path / lang / "dashboard")
        assert page == tmp_path / lang / "dashboard" / "index.html"
        text = page.read_text(encoding="utf-8")
        assert text.startswith("<!DOCTYPE html>")
        assert '<a href="../">' in text
    with pytest.raises(ValueError, match="lang"):
        build("es", tmp_path)


def test_parse_args_ph_series():
    assert bb.selected_editions(bb.parse_args(["--series", "ph", "--lang", "fil"])) == [PH_FIL]
    args = bb.parse_args(["--series", "ph", "--lang", "en", "--edition", "student"])
    assert bb.selected_editions(args) == [PH_EN]
    assert bb.selected_editions(bb.parse_args(["--lang", "zh", "--edition", "student"])) == [
        ZH_STUDENT
    ]
    assert bb.selected_editions(bb.parse_args(["--all"])) == list(bb.ALL_EDITIONS)
    assert bb.selected_editions(bb.parse_args(["--all", "--series", "ph"])) == list(
        bb.PH_EDITIONS
    )
    assert bb.selected_editions(bb.parse_args(["--all", "--series", "main"])) == list(
        bb.MAIN_EDITIONS
    )
    for bad in (
        ["--series", "ph"],
        ["--series", "ph", "--lang", "en", "--edition", "instructor"],
        ["--lang", "fil", "--edition", "student"],
        ["--series", "main", "--lang", "en"],
    ):
        with pytest.raises(SystemExit):
            bb.parse_args(bad)


def test_broken_links_checks_absolute_production_links(tmp_path: Path):
    site = _site(
        tmp_path,
        {
            "index.html": (
                '<a href="https://ancientsky.github.io/python4epi/ph/">ok</a>'
                '<a href="https://ancientsky.github.io/python4epi">ok, root</a>'
                '<link rel="canonical" href="https://ancientsky.github.io/python4epi/gone/"/>'
                '<a href="https://ancientsky.github.io/other/">another site</a>'
            ),
            "ph/index.html": "",
        },
    )
    assert bb.broken_links(site, "/python4epi/") == {}  # absolute links ignored by default
    broken = bb.broken_links(site, "/python4epi/", site_url=bb.SITE_URL)
    assert broken == {"https://ancientsky.github.io/python4epi/gone/": ["index.html"]}


def test_broken_links_ph_edition_skips_nested_and_main_editions(tmp_path: Path):
    site = _site(
        tmp_path,
        {
            "index.html": (
                '<a href="/python4epi/ph/zh/chapters/x/">nested PH language</a>'
                '<a href="/python4epi/en/">main book</a>'
                '<a href="/python4epi/ph/dashboard/">dashboard, missing</a>'
            )
        },
    )
    others = tuple(f"/python4epi/{e.prefix}" for e in bb.ALL_EDITIONS if e != PH_EN)
    assert set(bb.broken_links(site, "/python4epi/ph/", others)) == {"/python4epi/ph/dashboard/"}
    _site(tmp_path, {"dashboard/index.html": ""})
    assert bb.broken_links(site, "/python4epi/ph/", others) == {}
