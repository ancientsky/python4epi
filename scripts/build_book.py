"""Build the Epi With Python site with Jupyter Book 2 (MyST).

This is the one entry point for every edition, used locally, by CI and by the
Pages deploy::

    uv run python scripts/build_book.py --lang zh --edition student
    uv run python scripts/build_book.py --lang zh --edition instructor
    uv run python scripts/build_book.py --lang en --edition student
    uv run python scripts/build_book.py --lang en --edition instructor
    uv run python scripts/build_book.py --series ph --lang en    # also zh, fil
    uv run python scripts/build_book.py --series ph --all        # the three PH
    uv run python scripts/build_book.py --all --site-dir _site   # all seven

Each edition is a MyST project (``myst.yml``). The main book (series
``main``) has four; the Philippines special edition (series ``ph``, see
``book_ph/PRODUCTION.md``) has three, one per language, and no instructor
edition:

=========================  =========================  =================
Edition                    Project directory          Deploy path
=========================  =========================  =================
中文 學生版                ``book/``                  ``/``
中文 教師版                ``book/_instructor/``      ``/instructor/``
English student            ``book_en/``               ``/en/``
English instructor         ``book_en/_instructor/``   ``/en/instructor/``
PH English                 ``book_ph/en/``            ``/ph/``
PH 中文                    ``book_ph/zh/``            ``/ph/zh/``
PH Filipino                ``book_ph/fil/``           ``/ph/fil/``
=========================  =========================  =================

A build does three things Jupyter Book 2 cannot be configured to do itself:

1. **Kernel pre-execution setup.** JB1's ``nb_execution_pre_code`` has no MyST
   equivalent, so an IPython startup file that calls
   :func:`epi_learning.book_setup.configure_book_kernel` is written to
   ``<project>/_build/ipython`` and ``IPYTHONDIR`` points the kernels at it.
   The notebooks themselves are not changed (they must stay Colab-ready).
2. **Strict execution.** ``jupyter book build --html --execute --strict``: a
   notebook cell that raises (or any other build error) fails the build.
3. **Post-build step** (:func:`postprocess`) on the static HTML: ``<html lang>``,
   absolute Open Graph / Twitter tags, ``hreflang`` alternates, the
   language-switcher and YouTube scripts, the "Open in Colab" page map,
   ``book/_instructor/`` → ``book/`` in GitHub source links, and redirect
   stubs so JB1 URLs (``chapters/01_fundamentals.html``) keep working. It then
   fails the build if a student edition contains solution files or if any
   same-site link on a built page does not resolve to a file (with ``--all``,
   links between editions, including absolute links to the production site,
   are checked on the assembled site too).

Philippines editions differ in the post-build step only: ``hreflang``
alternates and the language switch span their three languages; pages load
``book/_static/epi-site.js`` (for ``window.epiWhenHydrated`` only),
``book_ph/_static/ph-site.js`` (three-way language switch, link back to the
full book, "Open in Colab") and the optional ``ph-games.css`` /
``ph-games.js`` instead of ``youtube-lite.js``; there are no JB1 redirect
stubs; and :func:`build_ph_dashboard.build_dashboard` writes the standalone
chapter-9 dashboard to ``<edition>/dashboard/index.html``.
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urljoin

REPO_ROOT = Path(__file__).resolve().parent.parent

#: Production URL of the zh student edition (the deploy root).
SITE_URL = "https://ancientsky.github.io/python4epi"
#: Path the deploy root is served under; ``BASE_URL`` for MyST is derived from it.
DEFAULT_BASE_PATH = "/python4epi"
GITHUB_REPO = "ancientsky/python4epi"
GITHUB_BRANCH = "main"

LANGS: tuple[str, ...] = ("zh", "en")
EDITIONS: tuple[str, ...] = ("student", "instructor")

#: Files copied from ``book/_static`` into every edition's ``_static/``.
STATIC_FILES: tuple[str, ...] = ("epi-site.js", "youtube-lite.js", "og-image.png")
#: Scripts injected (in this order) into every page.
PAGE_SCRIPTS: tuple[str, ...] = ("epi-site.js", "youtube-lite.js")

#: Per-language copy and locale data used by the post-build step.
LANG_META: dict[str, dict[str, str]] = {
    "zh": {
        "tree": "book",
        "html_lang": "zh-Hant",
        "hreflang": "zh-Hant",
        "og_locale": "zh_TW",
        "description": "一場退伍軍人症疫調，18 章 Python 課程，從接獲通報到結案報告。",
        "switch_title": "Switch to English",
        "colab_label": "Open in Colab",
    },
    "en": {
        "tree": "book_en",
        "html_lang": "en",
        "hreflang": "en",
        "og_locale": "en_US",
        "description": (
            "One Legionnaires' disease outbreak, 18 Python chapters, "
            "from first notification to the final report."
        ),
        "switch_title": "切換為繁體中文",
        "colab_label": "Open in Colab",
    },
}

#: The two book series: the main book and the Philippines special edition.
SERIES: tuple[str, ...] = ("main", "ph")
#: Languages of the Philippines edition; English is its source of truth.
PH_LANGS: tuple[str, ...] = ("en", "zh", "fil")
#: Languages and editions each series is published in.
SERIES_LANGS: dict[str, tuple[str, ...]] = {"main": LANGS, "ph": PH_LANGS}
SERIES_EDITIONS: dict[str, tuple[str, ...]] = {"main": EDITIONS, "ph": ("student",)}
#: Language the ``hreflang="x-default"`` alternate points at, per series.
X_DEFAULT: dict[str, str] = {"main": "zh", "ph": "en"}
SITE_NAMES: dict[str, str] = {"main": "Epi With Python", "ph": "Bantay Python · Epi With Python"}

#: Shared static files of the Philippines edition (``book_ph/_static``).
PH_STATIC_DIR = Path("book_ph") / "_static"
#: The MyST ``site.options.style`` of the PH projects (owned by the design work;
#: MyST only logs an error and builds unstyled while it is missing).
PH_STYLE = "ph.css"
#: Files copied into every PH edition's ``_static/``: name -> required. Optional
#: files that are missing are skipped with a warning and not linked from pages.
PH_STATIC_FILES: dict[str, bool] = {
    "ph-site.js": True,
    "ph-games.css": False,
    "ph-games.js": False,
}
#: Stylesheets linked from every PH page (after the theme and ``ph.css``).
PH_PAGE_STYLES: tuple[str, ...] = ("ph-games.css",)
#: Scripts injected (in this order) into every PH page. ``epi-site.js`` comes
#: from ``book/_static`` and only provides ``window.epiWhenHydrated`` here (its
#: book-specific part needs ``EPI_SITE.alternate``, which PH pages do not set).
PH_PAGE_SCRIPTS: tuple[str, ...] = ("epi-site.js", "ph-site.js", "ph-games.js")
#: Standalone pages generated into each PH edition (directory -> generator).
PH_DASHBOARD_DIR = "dashboard"
DASHBOARD_SCRIPT = Path(__file__).resolve().parent / "build_ph_dashboard.py"

#: Per-language copy and locale data of the Philippines edition.
PH_LANG_META: dict[str, dict[str, str]] = {
    "en": {
        "tree": "book_ph/en",
        "prefix": "ph/",
        "html_lang": "en",
        "hreflang": "en",
        "og_locale": "en_PH",
        "description": (
            "Python for Philippine disease surveillance staff, from zero to a "
            "shareable outbreak dashboard, with an AI co-pilot and privacy first."
        ),
        "label": "EN",
        "switch_title": "Read this page in English",
        "colab_label": "Open in Colab",
        "book_prefix": "en/",
        "book_title": "Epi With Python — the full book",
    },
    "zh": {
        "tree": "book_ph/zh",
        "prefix": "ph/zh/",
        "html_lang": "zh-Hant",
        "hreflang": "zh-Hant",
        "og_locale": "zh_TW",
        "description": "給菲律賓疾病監測人員的 Python 入門：從零開始，與 AI 一起寫程式，隱私優先，做出可分享的疫情儀表板。",
        "label": "中文",
        "switch_title": "以繁體中文閱讀本頁",
        "colab_label": "Open in Colab",
        "book_prefix": "",
        "book_title": "Epi With Python 完整版",
    },
    "fil": {
        "tree": "book_ph/fil",
        "prefix": "ph/fil/",
        "html_lang": "fil",
        "hreflang": "fil",
        # Facebook's Open Graph locale for Filipino is tl_PH.
        "og_locale": "tl_PH",
        "description": (
            "Python para sa mga kawani ng disease surveillance sa Pilipinas: mula sa "
            "simula hanggang sa outbreak dashboard, kasama ang AI, privacy muna."
        ),
        "label": "Filipino",
        "switch_title": "Basahin ang pahinang ito sa Filipino",
        "colab_label": "Buksan sa Colab",
        "book_prefix": "en/",
        "book_title": "Epi With Python — ang buong aklat",
    },
}

#: Marks a page as already post-processed, so the step is idempotent.
POSTBUILD_MARKER = "<!-- epi-postbuild -->"

KERNEL_STARTUP = '''\
"""Written by scripts/build_book.py: book-build kernel setup (see epi_learning.book_setup)."""
from epi_learning.book_setup import configure_book_kernel as _epi_configure

_epi_configure()
del _epi_configure
'''


@dataclass(frozen=True)
class Edition:
    """One of the seven published editions.

    Parameters
    ----------
    lang:
        ``"zh"`` or ``"en"`` (main book); ``"en"``, ``"zh"`` or ``"fil"`` (PH).
    edition:
        ``"student"`` or ``"instructor"``; the PH series has ``"student"`` only.
    series:
        ``"main"`` (the default) or ``"ph"`` (Philippines special edition).
    """

    lang: str
    edition: str = "student"
    series: str = "main"

    def __post_init__(self) -> None:
        if self.series not in SERIES:
            raise ValueError(f"series must be one of {SERIES}, got {self.series!r}")
        langs = SERIES_LANGS[self.series]
        if self.lang not in langs:
            raise ValueError(f"lang must be one of {langs}, got {self.lang!r}")
        editions = SERIES_EDITIONS[self.series]
        if self.edition not in editions:
            raise ValueError(
                f"edition must be one of {editions} for series {self.series!r}, "
                f"got {self.edition!r}"
            )

    @property
    def is_ph(self) -> bool:
        """Whether this is a Philippines-edition project."""
        return self.series == "ph"

    @property
    def meta(self) -> dict[str, str]:
        """Per-language copy and locale data (:data:`LANG_META` / :data:`PH_LANG_META`)."""
        return PH_LANG_META[self.lang] if self.is_ph else LANG_META[self.lang]

    @property
    def tree(self) -> str:
        """Source tree holding the content (``book``, ``book_en``, ``book_ph/en``…)."""
        return self.meta["tree"]

    @property
    def project_dir(self) -> Path:
        """Directory holding this edition's ``myst.yml``."""
        base = REPO_ROOT / self.tree
        return base / "_instructor" if self.edition == "instructor" else base

    @property
    def prefix(self) -> str:
        """Deploy path below the site root: ``""``, ``"en/"``, ``"ph/zh/"``…"""
        if self.is_ph:
            return self.meta["prefix"]
        parts = [] if self.lang == "zh" else ["en"]
        if self.edition == "instructor":
            parts.append("instructor")
        return "".join(f"{p}/" for p in parts)

    @property
    def html_dir(self) -> Path:
        """Static HTML output of ``jupyter book build --html``."""
        return self.project_dir / "_build" / "html"

    @property
    def site_dir(self) -> Path:
        """MyST site data: ``config.json`` and per-page ``content/<slug>.json``."""
        return self.project_dir / "_build" / "site"

    def counterpart(self) -> Edition:
        """The same edition in the other language (main book only)."""
        if self.is_ph:
            raise ValueError("PH editions have two other languages; use alternates()")
        other = "en" if self.lang == "zh" else "zh"
        return Edition(other, self.edition)

    def alternates(self) -> tuple[Edition, ...]:
        """The same edition in each other language of its series."""
        return tuple(
            Edition(lang, self.edition, self.series)
            for lang in SERIES_LANGS[self.series]
            if lang != self.lang
        )

    def label(self) -> str:
        """Human-readable name, e.g. ``"zh student"`` or ``"ph fil"``."""
        return f"ph {self.lang}" if self.is_ph else f"{self.lang} {self.edition}"


MAIN_EDITIONS: tuple[Edition, ...] = tuple(Edition(lang, ed) for lang in LANGS for ed in EDITIONS)
PH_EDITIONS: tuple[Edition, ...] = tuple(Edition(lang, "student", "ph") for lang in PH_LANGS)
ALL_EDITIONS: tuple[Edition, ...] = MAIN_EDITIONS + PH_EDITIONS
SERIES_EDITION_LIST: dict[str, tuple[Edition, ...]] = {"main": MAIN_EDITIONS, "ph": PH_EDITIONS}


@dataclass(frozen=True)
class Page:
    """A built page, as described by MyST's ``_build/site/content/<slug>.json``.

    Parameters
    ----------
    slug:
        MyST page slug, e.g. ``"chapters.notebooks.stats-basics"`` or ``"index"``.
    kind:
        ``"Notebook"`` or ``"Article"``.
    location:
        Source path relative to the project, e.g. ``"/chapters/03_stats.md"``.
    description:
        Page description from frontmatter (``""`` when absent).
    """

    slug: str
    kind: str
    location: str
    description: str = ""

    @property
    def url_path(self) -> str:
        """Page path below the edition root (``""`` for home, else ends in ``/``)."""
        return url_path(self.slug)

    @property
    def is_notebook(self) -> bool:
        """Whether the page was built from a ``.ipynb`` file."""
        return self.kind == "Notebook" or self.location.endswith(".ipynb")


def url_path(slug: str) -> str:
    """Map a MyST slug to its URL path with ``site.options.folders: true``.

    Parameters
    ----------
    slug:
        Dotted MyST slug.

    Returns
    -------
    str
        ``""`` for the home page (``index``), otherwise the slash-separated
        path with a trailing ``/``.
    """
    if not slug:
        raise ValueError("slug must be a non-empty string")
    if slug == "index":
        return ""
    return slug.replace(".", "/") + "/"


def legacy_path(location: str) -> str:
    """Return the Jupyter Book 1 URL path for a source file.

    Parameters
    ----------
    location:
        Source path relative to the project, e.g. ``"/chapters/03_stats.md"``.

    Returns
    -------
    str
        The old Sphinx page path, e.g. ``"chapters/03_stats.html"``.
    """
    rel = location.lstrip("/")
    stem, dot, ext = rel.rpartition(".")
    if not dot or ext not in {"md", "ipynb"}:
        raise ValueError(f"expected a .md or .ipynb location, got {location!r}")
    return f"{stem}.html"


def colab_url(tree: str, location: str) -> str:
    """Return the Google Colab URL for a notebook on GitHub ``main``.

    Parameters
    ----------
    tree:
        Source tree (``"book"`` or ``"book_en"``); instructor editions share it.
    location:
        Notebook path relative to the project.

    Returns
    -------
    str
        ``https://colab.research.google.com/github/<repo>/blob/<branch>/<path>``.
    """
    if not location.endswith(".ipynb"):
        raise ValueError(f"not a notebook: {location!r}")
    return (
        f"https://colab.research.google.com/github/{GITHUB_REPO}/blob/{GITHUB_BRANCH}/"
        f"{tree}/{location.lstrip('/')}"
    )


def base_url(base_path: str, edition: Edition) -> str:
    """Return the ``BASE_URL`` MyST needs for *edition* (no trailing slash).

    Parameters
    ----------
    base_path:
        Path the deploy root is served under (``"/python4epi"``, or ``""``).
    edition:
        The edition being built.

    Returns
    -------
    str
        E.g. ``"/python4epi/en/instructor"``; ``""`` when served at ``/``.
    """
    if base_path and not base_path.startswith("/"):
        raise ValueError(f"base_path must start with '/', got {base_path!r}")
    return f"{base_path.rstrip('/')}/{edition.prefix}".rstrip("/")


def page_slugs(site_config: dict) -> list[str]:
    """Slugs of the pages in the current build, from ``_build/site/config.json``.

    MyST never deletes stale ``content/*.json`` files, so the site config (the
    project's index page plus its TOC pages) is the authority on what exists.

    Parameters
    ----------
    site_config:
        The parsed ``config.json``.

    Returns
    -------
    list[str]
        Page slugs, home page first.
    """
    projects = site_config.get("projects") or []
    if len(projects) != 1:
        raise ValueError(f"expected exactly one MyST project, found {len(projects)}")
    project = projects[0]
    slugs = [project["index"]]
    slugs += [p["slug"] for p in project.get("pages", []) if p.get("slug")]
    return slugs


def load_pages(site_dir: Path) -> list[Page]:
    """Read the pages MyST built, from ``_build/site``.

    Parameters
    ----------
    site_dir:
        The edition's ``_build/site`` directory (``config.json`` + ``content/``).

    Returns
    -------
    list[Page]
        One entry per page in the current build, home page first.
    """
    config_file = site_dir / "config.json"
    if not config_file.is_file():
        raise FileNotFoundError(f"no MyST site config at {config_file}; did the build run?")
    pages = []
    for slug in page_slugs(json.loads(config_file.read_text(encoding="utf-8"))):
        data = json.loads((site_dir / "content" / f"{slug}.json").read_text(encoding="utf-8"))
        frontmatter = data.get("frontmatter") or {}
        pages.append(
            Page(
                slug=slug,
                kind=data.get("kind", ""),
                location=data["location"],
                description=frontmatter.get("description", "") or "",
            )
        )
    return pages


def set_html_lang(page_html: str, lang_tag: str) -> str:
    """Replace the theme's hard-coded ``<html lang="en">`` with *lang_tag*."""
    new, count = re.subn(r'<html lang="[^"]*"', f'<html lang="{lang_tag}"', page_html, count=1)
    if count != 1:
        raise ValueError("page has no <html lang=...> attribute")
    return new


def fix_source_links(text: str, edition: Edition) -> str:
    """Point GitHub source/edit links of instructor pages at the real files.

    Instructor projects reach the shared content through symlinks in
    ``<tree>/_instructor/``; GitHub does not serve files through a directory
    symlink, so ``.../blob/main/book/_instructor/chapters/x.md`` would 404.
    """
    if edition.edition != "instructor":
        return text
    for verb in ("blob", "edit"):
        text = text.replace(
            f"github.com/{GITHUB_REPO}/{verb}/{GITHUB_BRANCH}/{edition.tree}/_instructor/",
            f"github.com/{GITHUB_REPO}/{verb}/{GITHUB_BRANCH}/{edition.tree}/",
        )
    return text


_META_RX = r'<meta {attr}="{name}" content="([^"]*)"(\s*/?>)'


def _meta_content(page_html: str, attr: str, name: str) -> str | None:
    """Return the ``content`` of ``<meta attr="name">``, or ``None``."""
    match = re.search(_META_RX.format(attr=attr, name=re.escape(name)), page_html)
    return html.unescape(match.group(1)) if match else None


def upsert_meta(page_html: str, attr: str, name: str, content: str) -> tuple[str, bool]:
    """Set the ``content`` of an existing ``<meta>`` in place.

    Tags the theme rendered are edited, never removed or moved: React hydrates
    ``<head>`` and fails (error #418) when one of its elements is missing.

    Parameters
    ----------
    page_html:
        The page HTML.
    attr, name:
        Identify the tag, e.g. ``"property"``, ``"og:image"``.
    content:
        The new (unescaped) value.

    Returns
    -------
    tuple[str, bool]
        The HTML and whether the tag existed (if not, the caller must add it).
    """
    rx = re.compile(_META_RX.format(attr=attr, name=re.escape(name)))
    new, count = rx.subn(
        lambda m: f'<meta {attr}="{name}" content="{html.escape(content)}"{m.group(2)}',
        page_html,
        count=1,
    )
    return new, bool(count)


def absolute_url(edition: Edition, path: str = "") -> str:
    """Production URL of *path* inside *edition*."""
    return f"{SITE_URL}/{edition.prefix}{path}"


def page_meta(page: Page, edition: Edition, title: str) -> list[tuple[str, str, str]]:
    """The SEO / social ``<meta>`` tags every page should carry.

    Parameters
    ----------
    page, edition:
        The page and its edition.
    title:
        The page title (MyST's ``og:title``).

    Returns
    -------
    list[tuple[str, str, str]]
        ``(attribute, name, content)`` triples, e.g. ``("property", "og:url", ...)``.
    """
    meta = edition.meta
    description = page.description or meta["description"]
    page_url = absolute_url(edition, page.url_path)
    # MyST points og:image at the page's first figure (often an SVG, which
    # social sites reject) with a site-relative URL; use the absolute card image.
    image = absolute_url(edition, "_static/og-image.png")
    return [
        ("name", "description", description),
        ("property", "og:site_name", SITE_NAMES[edition.series]),
        ("property", "og:type", "website"),
        ("property", "og:url", page_url),
        ("property", "og:description", description),
        ("property", "og:locale", meta["og_locale"]),
        *(
            ("property", "og:locale:alternate", other.meta["og_locale"])
            for other in edition.alternates()
        ),
        ("name", "image", image),
        ("property", "og:image", image),
        ("property", "og:image:type", "image/png"),
        ("property", "og:image:width", "1200"),
        ("property", "og:image:height", "630"),
        ("property", "og:image:alt", title),
        ("name", "twitter:card", "summary_large_image"),
        ("name", "twitter:title", title),
        ("name", "twitter:description", description),
        ("name", "twitter:image", image),
    ]


def site_config(edition: Edition, *, base_path: str, colab: dict[str, str]) -> dict[str, object]:
    """The ``window.EPI_SITE`` object the page scripts read.

    The theme is a single-page app, so the object written into the first page
    loaded stays in use after client-side navigation: it holds nothing that
    is specific to one page.

    Parameters
    ----------
    edition:
        The page's edition.
    base_path:
        Path the deploy root is served under.
    colab:
        Map of page path -> Colab URL for this edition.

    Returns
    -------
    dict
        Main book: ``lang``, ``edition``, ``htmlLang``, ``root``, ``alternate``,
        ``colab``, ``colabLabel`` (see ``book/_static/epi-site.js``). PH: the
        same without ``alternate``, plus ``series``, ``languages``, ``book`` and
        ``standalone`` (see ``book_ph/_static/ph-site.js``).
    """
    meta = edition.meta
    base = base_path.rstrip("/")
    config: dict[str, object] = {
        "lang": edition.lang,
        "edition": edition.edition,
        "htmlLang": meta["html_lang"],
        "root": f"{base}/{edition.prefix}",
        "colab": colab,
        "colabLabel": meta["colab_label"],
    }
    if not edition.is_ph:
        other = edition.counterpart()
        config["alternate"] = {
            "root": f"{base}/{other.prefix}",
            "hreflang": other.meta["hreflang"],
            "title": meta["switch_title"],
        }
        return config
    config["series"] = edition.series
    config["languages"] = [
        {
            "lang": lang.lang,
            "root": f"{base}/{lang.prefix}",
            "hreflang": lang.meta["hreflang"],
            "label": lang.meta["label"],
            "title": lang.meta["switch_title"],
        }
        for lang in SERIES_EDITION_LIST["ph"]
    ]
    config["book"] = {"root": f"{base}/{meta['book_prefix']}", "title": meta["book_title"]}
    config["standalone"] = [f"{PH_DASHBOARD_DIR}/"]
    return config


def head_links_and_scripts(
    page: Page,
    edition: Edition,
    *,
    base_path: str,
    colab: dict[str, str],
    has_counterpart: bool = False,
    alternate_langs: tuple[str, ...] | None = None,
    static_files: tuple[str, ...] | None = None,
) -> str:
    """Build the canonical/``hreflang`` links and the page scripts.

    Parameters
    ----------
    page, edition:
        The page and its edition.
    base_path:
        Path the deploy root is served under, for script URLs.
    colab:
        Map of page path -> Colab URL for this edition.
    has_counterpart:
        Main book: whether the other language has the same page (controls
        ``hreflang``). Ignored when *alternate_langs* is given.
    alternate_langs:
        Other languages of the series that have the same page.
    static_files:
        PH only: the optional ``_static`` files present in the build; styles
        and scripts not listed are not linked (default: all of them).

    Returns
    -------
    str
        HTML to insert before ``</head>``.
    """
    if alternate_langs is None:
        alternate_langs = tuple(o.lang for o in edition.alternates()) if has_counterpart else ()
    esc = html.escape
    page_url = absolute_url(edition, page.url_path)
    tags = [f'<link rel="canonical" href="{esc(page_url)}"/>']
    alternates = {edition.lang: page_url}
    for other in edition.alternates():
        if other.lang in alternate_langs:
            alternates[other.lang] = absolute_url(other, page.url_path)
    for lang in SERIES_EDITION_LIST[edition.series]:
        if lang.edition == edition.edition and lang.lang in alternates:
            tags.append(
                f'<link rel="alternate" hreflang="{lang.meta["hreflang"]}" '
                f'href="{esc(alternates[lang.lang])}"/>'
            )
    x_default = alternates.get(X_DEFAULT[edition.series], page_url)
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{esc(x_default)}"/>')

    root = f"{base_path.rstrip('/')}/{edition.prefix}"
    config = site_config(edition, base_path=base_path, colab=colab)
    config_json = json.dumps(config, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    if edition.is_ph:
        present = set(PH_STATIC_FILES if static_files is None else static_files)
        present.add("epi-site.js")  # copied from book/_static, always there
        for style in PH_PAGE_STYLES:
            if style in present:
                tags.append(f'<link rel="stylesheet" href="{esc(root)}_static/{style}"/>')
        scripts = tuple(s for s in PH_PAGE_SCRIPTS if s in present)
    else:
        scripts = PAGE_SCRIPTS
    tags.append(f"<script>window.EPI_SITE={config_json};</script>")
    for script in scripts:
        tags.append(f'<script src="{esc(root)}_static/{script}" defer></script>')
    return "".join(tags)


def process_page_html(page_html: str, page: Page, edition: Edition, **kwargs: object) -> str:
    """Apply every post-build change to one page's HTML.

    Parameters
    ----------
    page_html:
        The HTML MyST wrote.
    page, edition:
        The page and its edition.
    **kwargs:
        ``base_path``, ``colab`` and ``has_counterpart`` / ``alternate_langs``
        (and, for PH, ``static_files``), passed to :func:`head_links_and_scripts`.

    Returns
    -------
    str
        The updated HTML (unchanged if it was already processed).
    """
    if POSTBUILD_MARKER in page_html:
        return page_html
    title = _meta_content(page_html, "property", "og:title") or SITE_NAMES[edition.series]
    page_html = set_html_lang(page_html, edition.meta["html_lang"])
    page_html = fix_source_links(page_html, edition)
    added = []
    seen: set[tuple[str, str]] = set()
    for attr, name, content in page_meta(page, edition, title):
        # A repeated tag (og:locale:alternate on PH pages) is added, not upserted.
        existed = False
        if (attr, name) not in seen:
            page_html, existed = upsert_meta(page_html, attr, name, content)
        seen.add((attr, name))
        if not existed:
            added.append(f'<meta {attr}="{name}" content="{html.escape(content)}"/>')
    head_end = page_html.find("</head>")
    if head_end < 0:
        raise ValueError(f"{page.slug}: page has no </head>")
    block = POSTBUILD_MARKER + "".join(added) + head_links_and_scripts(page, edition, **kwargs)  # type: ignore[arg-type]
    return page_html[:head_end] + block + page_html[head_end:]


def redirect_stub(target: str, canonical: str, lang_tag: str) -> str:
    """HTML that sends a JB1 URL to its new location (keeping the #fragment).

    Parameters
    ----------
    target:
        Site-relative URL of the new page (e.g. ``/python4epi/chapters/stats/``).
    canonical:
        Absolute production URL of the new page.
    lang_tag:
        Value for ``<html lang>``.

    Returns
    -------
    str
        A small standalone HTML document.
    """
    t = html.escape(target)
    return (
        f'<!DOCTYPE html><html lang="{lang_tag}"><head><meta charset="utf-8"/>'
        f"<title>Redirecting…</title>"
        f'<link rel="canonical" href="{html.escape(canonical)}"/>'
        '<meta name="robots" content="noindex"/>'
        f'<meta http-equiv="refresh" content="0; url={t}"/>'
        f"<script>location.replace({json.dumps(target)} + location.hash);</script>"
        f'</head><body><p><a href="{t}">{t}</a></p></body></html>\n'
    )


def find_solution_files(html_dir: Path, pages: list[Page]) -> list[str]:
    """List solution pages or files present in a built edition.

    A student edition must not ship solutions. Pages come from the TOC, but
    MyST also copies any *linked* local file into ``_public/`` for download,
    so a stray ``[...](solutions/x_solution.ipynb)`` link would leak one.

    Parameters
    ----------
    html_dir:
        The edition's ``_build/html``.
    pages:
        The pages of the build.

    Returns
    -------
    list[str]
        Offending page locations and file paths (relative to *html_dir*).
    """
    found = [p.location for p in pages if "solution" in p.location.rsplit("/", 1)[-1]]
    found += sorted(
        str(path.relative_to(html_dir))
        for path in html_dir.rglob("*")
        if path.is_file() and path.suffix in {".ipynb", ".md"} and "solution" in path.name
    )
    return found


_HREF_RX = re.compile(r'\shref="([^"]*)"')
_SCHEME_RX = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_SCRIPT_RX = re.compile(r"<script\b[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE)


def resolve_static(site_dir: Path, rel: str) -> Path | None:
    """Find the file a static host (GitHub Pages) serves for a URL path.

    Parameters
    ----------
    site_dir:
        Directory served at the URL root the path is relative to.
    rel:
        URL path below that root, without query or fragment (``""`` = root).

    Returns
    -------
    Path or None
        The file served, or ``None`` for a 404. ``a/`` and ``a`` both serve
        ``a/index.html``; ``a`` may also be a plain file.
    """
    rel = unquote(rel)
    candidate = site_dir / rel
    if rel and not rel.endswith("/") and candidate.is_file():
        return candidate
    index = candidate / "index.html"
    return index if index.is_file() else None


def page_url_for(html_file: Path, site_dir: Path, url_root: str) -> str:
    """URL path a built HTML file is served at (``x/index.html`` -> ``x/``)."""
    rel = html_file.relative_to(site_dir).as_posix()
    if rel == "index.html":
        return url_root
    if rel.endswith("/index.html"):
        return url_root + rel[: -len("index.html")]
    return url_root + rel


def broken_links(
    site_dir: Path,
    url_root: str,
    skip_prefixes: tuple[str, ...] = (),
    site_url: str | None = None,
) -> dict[str, list[str]]:
    """Same-site ``href``s in built pages that do not resolve to a file.

    Parameters
    ----------
    site_dir:
        Built output served at *url_root* (an edition's ``_build/html``, or an
        assembled site).
    url_root:
        URL path *site_dir* is served at, with a trailing ``/``
        (e.g. ``/python4epi/en/``).
    skip_prefixes:
        URL roots of other editions: links into them are not checked here
        (:func:`assemble_site` checks them on the assembled site).
    site_url:
        Absolute production URL that *url_root* is deployed at (no trailing
        ``/``). When given, absolute links into it (canonical/``hreflang``
        links, the navbar fallbacks, links to other editions) are checked too;
        only meaningful on the fully assembled site.

    Returns
    -------
    dict[str, list[str]]
        Broken ``href`` -> pages (relative paths) that contain it.
    """
    if not url_root.endswith("/"):
        raise ValueError(f"url_root must end with '/', got {url_root!r}")
    absolute = f"{site_url.rstrip('/')}/" if site_url else None
    broken: dict[str, list[str]] = {}
    for html_file in sorted(site_dir.rglob("*.html")):
        page_url = page_url_for(html_file, site_dir, url_root)
        text = html_file.read_text(encoding="utf-8", errors="replace")
        # Inline scripts (e.g. plotly.js in a notebook output) are not markup.
        text = _SCRIPT_RX.sub("", text)
        for raw in set(_HREF_RX.findall(text)):
            href = html.unescape(raw).strip()
            link = href
            if absolute and (link == absolute[:-1] or link.startswith(absolute)):
                link = url_root + link[len(absolute) :]
            if not link or link.startswith(("#", "//")) or _SCHEME_RX.match(link):
                continue  # in-page anchor or another site
            target = urljoin(page_url, link).split("#", 1)[0].split("?", 1)[0]
            if target.startswith(url_root):
                # Another edition nested below this one (e.g. /en/instructor/)?
                nested = [p for p in skip_prefixes if len(p) > len(url_root)]
                if any(target.startswith(p) for p in nested):
                    continue
                if resolve_static(site_dir, target[len(url_root) :]):
                    continue
            elif any(target.startswith(prefix) for prefix in skip_prefixes):
                continue
            broken.setdefault(href, []).append(html_file.relative_to(site_dir).as_posix())
    return broken


def check_links(
    site_dir: Path,
    url_root: str,
    label: str,
    skip_prefixes: tuple[str, ...] = (),
    site_url: str | None = None,
) -> None:
    """Raise :class:`SystemExit` if any same-site link in *site_dir* is broken.

    Parameters are those of :func:`broken_links`; *label* names the build.
    """
    broken = broken_links(site_dir, url_root, skip_prefixes, site_url)
    if broken:
        lines = [f"  {href}  (in {len(pages)} pages, e.g. {pages[0]})"
                 for href, pages in sorted(broken.items())[:20]]
        raise SystemExit(
            f"{label}: {len(broken)} broken internal link target(s):\n" + "\n".join(lines)
        )


def postprocess(edition: Edition, base_path: str = DEFAULT_BASE_PATH) -> dict[str, int]:
    """Run the post-build step on an edition's ``_build/html``.

    Parameters
    ----------
    edition:
        The edition whose build output to process.
    base_path:
        Path the deploy root is served under (must match the build's ``BASE_URL``).

    Returns
    -------
    dict[str, int]
        Counts of ``pages``, ``notebooks`` (Colab links) and ``redirects``
        written (plus, for PH editions, ``standalone`` generated pages).
    """
    html_dir = edition.html_dir
    if not (html_dir / "index.html").is_file():
        raise FileNotFoundError(f"{html_dir} has no index.html; did the build run?")
    pages = load_pages(edition.site_dir)
    if edition.edition == "student":
        leaked = find_solution_files(html_dir, pages)
        if leaked:
            raise SystemExit(
                f"{edition.label()}: student edition contains solution material: {leaked[:5]}"
            )

    static_dst = html_dir / "_static"
    static_dst.mkdir(exist_ok=True)
    static_files = copy_static(edition, static_dst)

    colab = {p.url_path: colab_url(edition.tree, p.location) for p in pages if p.is_notebook}
    lang_tag = edition.meta["html_lang"]
    edition_root = f"{base_path.rstrip('/')}/{edition.prefix}"

    for page in pages:
        page_file = html_dir / page.url_path / "index.html"
        page_html = page_file.read_text(encoding="utf-8")
        location = page.location.lstrip("/")
        alternate_langs = tuple(
            other.lang
            for other in edition.alternates()
            if (REPO_ROOT / other.tree / location).is_file()
        )
        page_file.write_text(
            process_page_html(
                page_html,
                page,
                edition,
                base_path=base_path,
                alternate_langs=alternate_langs,
                colab=colab,
                static_files=static_files,
            ),
            encoding="utf-8",
        )
    # The app fetches these JSON files on client-side navigation.
    if edition.edition == "instructor":
        for data_file in html_dir.glob("*.json"):
            text = data_file.read_text(encoding="utf-8")
            fixed = fix_source_links(text, edition)
            if fixed != text:
                data_file.write_text(fixed, encoding="utf-8")

    stats = {"pages": len(pages), "notebooks": len(colab)}
    # The PH edition never had Jupyter Book 1 URLs to keep alive.
    redirects = 0
    for page in pages if not edition.is_ph else ():
        stub = html_dir / legacy_path(page.location)
        if stub.exists():
            continue
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text(
            redirect_stub(
                edition_root + page.url_path, absolute_url(edition, page.url_path), lang_tag
            ),
            encoding="utf-8",
        )
        redirects += 1
    stats["redirects"] = redirects

    if edition.is_ph:
        build_dashboard = load_dashboard_builder()
        written = build_dashboard(edition.lang, html_dir / PH_DASHBOARD_DIR)
        if not Path(written).is_file():
            raise SystemExit(f"{edition.label()}: dashboard builder wrote no file at {written}")
        stats["standalone"] = 1

    other_roots = tuple(
        f"{base_path.rstrip('/')}/{other.prefix}" for other in ALL_EDITIONS if other != edition
    )
    check_links(html_dir, edition_root, edition.label(), other_roots)
    return stats


def copy_static(edition: Edition, static_dst: Path) -> tuple[str, ...]:
    """Copy the files MyST does not copy into an edition's ``_static/``.

    Main-book editions get :data:`STATIC_FILES` from ``book/_static``. PH
    editions get ``epi-site.js`` from ``book/_static``, ``og-image.png`` (the
    first of ``book_ph/_static/og-image_<lang>.png``,
    ``book_ph/_static/og-image.png`` and ``book/_static/og-image.png``) and
    :data:`PH_STATIC_FILES` from ``book_ph/_static``; a missing optional file
    is reported and skipped, a missing required one fails the build.

    Parameters
    ----------
    edition:
        The edition being post-processed.
    static_dst:
        Its ``_build/html/_static`` directory.

    Returns
    -------
    tuple[str, ...]
        Names of the files copied.
    """
    book_static = REPO_ROOT / "book" / "_static"
    if not edition.is_ph:
        for name in STATIC_FILES:
            shutil.copy2(book_static / name, static_dst / name)
        return STATIC_FILES
    ph_static = REPO_ROOT / PH_STATIC_DIR
    copied = []
    og_candidates = (
        ph_static / f"og-image_{edition.lang}.png",
        ph_static / "og-image.png",
        book_static / "og-image.png",
    )
    sources = {
        "epi-site.js": book_static / "epi-site.js",
        "og-image.png": next((p for p in og_candidates if p.is_file()), og_candidates[-1]),
    }
    sources.update({name: ph_static / name for name in PH_STATIC_FILES})
    for name, src in sources.items():
        if not src.is_file():
            if PH_STATIC_FILES.get(name, True):
                raise SystemExit(f"{edition.label()}: required static file {src} is missing")
            print(f"⚠ {edition.label()}: optional {src.relative_to(REPO_ROOT)} is missing; "
                  "pages will not link it", flush=True)
            continue
        shutil.copy2(src, static_dst / name)
        copied.append(name)
    if not (ph_static / PH_STYLE).is_file():
        print(f"⚠ {edition.label()}: {PH_STATIC_DIR / PH_STYLE} is missing; "
              "the site is built without the PH theme", flush=True)
    return tuple(copied)


def load_dashboard_builder() -> Callable[[str, Path], Path]:
    """Import ``build_dashboard`` from ``scripts/build_ph_dashboard.py``.

    Returns
    -------
    Callable[[str, Path], Path]
        ``build_dashboard(lang, out_dir) -> Path`` of the written ``index.html``.
    """
    spec = importlib.util.spec_from_file_location("build_ph_dashboard", DASHBOARD_SCRIPT)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {DASHBOARD_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_dashboard


def write_kernel_startup(edition: Edition) -> Path:
    """Write the IPython startup file and return the ``IPYTHONDIR`` to use."""
    ipython_dir = edition.project_dir / "_build" / "ipython"
    startup = ipython_dir / "profile_default" / "startup" / "00-epi-book-setup.py"
    startup.parent.mkdir(parents=True, exist_ok=True)
    startup.write_text(KERNEL_STARTUP, encoding="utf-8")
    return ipython_dir


def count_warnings(log: str) -> int:
    """Number of MyST warning lines (``⚠️``) in a build log."""
    return sum(1 for line in log.splitlines() if line.lstrip().startswith("⚠️"))


def run_myst(edition: Edition, base_path: str, *, execute: bool = True) -> tuple[int, str]:
    """Run ``jupyter book build --html --strict`` for one edition.

    Parameters
    ----------
    edition:
        The edition to build.
    base_path:
        Path the deploy root is served under.
    execute:
        Execute notebooks (``--execute``). Only skip this for a quick preview.

    Returns
    -------
    tuple[int, str]
        The process exit code and its combined output.
    """
    env = dict(os.environ)
    env["IPYTHONDIR"] = str(write_kernel_startup(edition))
    url = base_url(base_path, edition)
    if url:
        env["BASE_URL"] = url
    else:
        env.pop("BASE_URL", None)
    cmd = [sys.executable, "-m", "jupyter_book", "build", "--html", "--strict"]
    if execute:
        cmd.append("--execute")
    print(f"$ (cd {edition.project_dir.relative_to(REPO_ROOT)} && BASE_URL={url!r} "
          f"{' '.join(cmd[2:])})", flush=True)
    proc = subprocess.Popen(
        cmd,
        cwd=edition.project_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.stdout is not None
    lines = []
    for line in proc.stdout:
        lines.append(line)
        print(line, end="", flush=True)
    return proc.wait(), "".join(lines)


def build_edition(edition: Edition, base_path: str, *, execute: bool = True) -> dict[str, int]:
    """Build and post-process one edition; raise :class:`SystemExit` on failure.

    MyST never removes files from an earlier build, so ``_build/site`` and
    ``_build/html`` are cleared first (the execution cache and the downloaded
    theme in ``_build/execute`` and ``_build/templates`` are kept).
    """
    start = time.monotonic()
    for stale in ("site", "html"):
        shutil.rmtree(edition.project_dir / "_build" / stale, ignore_errors=True)
    code, log = run_myst(edition, base_path, execute=execute)
    log_file = edition.project_dir / "_build" / "build.log"
    log_file.write_text(log, encoding="utf-8")
    if code != 0:
        raise SystemExit(
            f"{edition.label()}: jupyter book build failed (exit {code}); see {log_file}"
        )
    stats = postprocess(edition, base_path)
    stats["warnings"] = count_warnings(log)
    stats["seconds"] = round(time.monotonic() - start)
    print(f"✔ {edition.label()}: {stats}", flush=True)
    return stats


def assemble_site(
    editions: list[Edition], site_dir: Path, base_path: str = DEFAULT_BASE_PATH
) -> None:
    """Copy each edition's HTML to its deploy path under *site_dir*.

    Parameters
    ----------
    editions:
        Editions to include; each must have been built.
    site_dir:
        Output directory, replaced if it exists. Its root is the zh student
        edition when that edition is included.
    base_path:
        Path the site root is served under; when all seven editions are
        included, every same-site link on the assembled site is checked,
        absolute links to the production site (:data:`SITE_URL`) included.
    """
    protected = {REPO_ROOT, REPO_ROOT / "book", REPO_ROOT / "book_en", REPO_ROOT / "book_ph"}
    protected |= {e.project_dir for e in ALL_EDITIONS}
    if site_dir.resolve() in protected:
        raise ValueError(f"refusing to replace {site_dir}")
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True)
    # Root first, so nested editions are copied into it rather than over it.
    for edition in sorted(editions, key=lambda e: len(e.prefix)):
        dest = site_dir / edition.prefix
        shutil.copytree(edition.html_dir, dest, dirs_exist_ok=True)
    for edition in editions:
        index = site_dir / edition.prefix / "index.html"
        if POSTBUILD_MARKER not in index.read_text(encoding="utf-8"):
            raise SystemExit(f"{index} was not post-processed")
    # Links between editions (e.g. the home page's "instructor edition" button)
    # can only be checked once they sit side by side.
    if set(editions) == set(ALL_EDITIONS):
        check_links(site_dir, f"{base_path.rstrip('/')}/", "assembled site", site_url=SITE_URL)
    print(f"✔ site assembled in {site_dir}", flush=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    ``--lang`` + ``--edition`` select one main-book edition (unchanged);
    ``--series ph --lang en|zh|fil`` one PH edition; ``--all`` every edition,
    or with ``--series`` every edition of that series.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--series", choices=SERIES, help="book series (default: main)")
    parser.add_argument(
        "--lang", choices=sorted(set(LANGS) | set(PH_LANGS)), help="language to build"
    )
    parser.add_argument("--edition", choices=EDITIONS, help="edition to build (main book)")
    parser.add_argument(
        "--all", action="store_true", help="build all seven editions (or all of --series)"
    )
    parser.add_argument(
        "--base-path",
        default=DEFAULT_BASE_PATH,
        help=f"path the site root is served under (default {DEFAULT_BASE_PATH}; '' for /)",
    )
    parser.add_argument("--site-dir", type=Path, help="assemble the built editions here")
    parser.add_argument(
        "--no-execute", action="store_true", help="skip notebook execution (preview only)"
    )
    parser.add_argument(
        "--postprocess-only", action="store_true", help="rerun the post-build step only"
    )
    args = parser.parse_args(argv)
    if args.all == bool(args.lang or args.edition):
        parser.error("give either --all, or --lang (with --edition for the main book)")
    if args.all:
        return args
    if (args.series or "main") == "main":
        if not (args.lang and args.edition):
            parser.error("--lang and --edition go together")
        if args.lang not in LANGS:
            parser.error(f"the main book is built in {LANGS}, not {args.lang!r}")
    else:
        if not args.lang or args.lang not in PH_LANGS:
            parser.error(f"--series ph needs --lang, one of {PH_LANGS}")
        if args.edition not in (None, "student"):
            parser.error("the PH edition has no instructor edition")
    return args


def selected_editions(args: argparse.Namespace) -> list[Edition]:
    """The editions the parsed command line asks for, in build order."""
    if args.all:
        return list(SERIES_EDITION_LIST[args.series] if args.series else ALL_EDITIONS)
    series = args.series or "main"
    return [Edition(args.lang, args.edition or "student", series)]


def main(argv: list[str] | None = None) -> None:
    """Command-line entry point."""
    args = parse_args(argv)
    editions = selected_editions(args)
    for edition in editions:
        if args.postprocess_only:
            print(f"✔ {edition.label()}: {postprocess(edition, args.base_path)}")
        else:
            build_edition(edition, args.base_path, execute=not args.no_execute)
    if args.site_dir:
        assemble_site(editions, args.site_dir, args.base_path)


if __name__ == "__main__":
    main()
