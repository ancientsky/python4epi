"""Build the Epi With Python site with Jupyter Book 2 (MyST).

This is the one entry point for every edition, used locally, by CI and by the
Pages deploy::

    uv run python scripts/build_book.py --lang zh --edition student
    uv run python scripts/build_book.py --lang zh --edition instructor
    uv run python scripts/build_book.py --lang en --edition student
    uv run python scripts/build_book.py --lang en --edition instructor
    uv run python scripts/build_book.py --all --site-dir _site   # all four

Each edition is a MyST project (``myst.yml``):

======================  =========================  =================
Edition                 Project directory          Deploy path
======================  =========================  =================
中文 學生版             ``book/``                  ``/``
中文 教師版             ``book/_instructor/``      ``/instructor/``
English student         ``book_en/``               ``/en/``
English instructor      ``book_en/_instructor/``   ``/en/instructor/``
======================  =========================  =================

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
   links between editions are checked on the assembled site too).
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
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
    """One of the four published editions.

    Parameters
    ----------
    lang:
        ``"zh"`` or ``"en"``.
    edition:
        ``"student"`` or ``"instructor"``.
    """

    lang: str
    edition: str

    def __post_init__(self) -> None:
        if self.lang not in LANGS:
            raise ValueError(f"lang must be one of {LANGS}, got {self.lang!r}")
        if self.edition not in EDITIONS:
            raise ValueError(f"edition must be one of {EDITIONS}, got {self.edition!r}")

    @property
    def tree(self) -> str:
        """Source tree holding the content (``book`` or ``book_en``)."""
        return LANG_META[self.lang]["tree"]

    @property
    def project_dir(self) -> Path:
        """Directory holding this edition's ``myst.yml``."""
        base = REPO_ROOT / self.tree
        return base / "_instructor" if self.edition == "instructor" else base

    @property
    def prefix(self) -> str:
        """Deploy path below the site root: ``""``, ``"en/"``, ``"en/instructor/"``…"""
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
        """The same edition in the other language."""
        other = "en" if self.lang == "zh" else "zh"
        return Edition(other, self.edition)

    def label(self) -> str:
        """Human-readable name, e.g. ``"zh student"``."""
        return f"{self.lang} {self.edition}"


ALL_EDITIONS: tuple[Edition, ...] = tuple(Edition(lang, ed) for lang in LANGS for ed in EDITIONS)


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
    meta = LANG_META[edition.lang]
    description = page.description or meta["description"]
    page_url = absolute_url(edition, page.url_path)
    # MyST points og:image at the page's first figure (often an SVG, which
    # social sites reject) with a site-relative URL; use the absolute card image.
    image = absolute_url(edition, "_static/og-image.png")
    return [
        ("name", "description", description),
        ("property", "og:site_name", "Epi With Python"),
        ("property", "og:type", "website"),
        ("property", "og:url", page_url),
        ("property", "og:description", description),
        ("property", "og:locale", meta["og_locale"]),
        ("property", "og:locale:alternate", LANG_META[edition.counterpart().lang]["og_locale"]),
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


def head_links_and_scripts(
    page: Page,
    edition: Edition,
    *,
    base_path: str,
    has_counterpart: bool,
    colab: dict[str, str],
) -> str:
    """Build the canonical/``hreflang`` links and the page scripts.

    Parameters
    ----------
    page, edition:
        The page and its edition.
    base_path:
        Path the deploy root is served under, for script URLs.
    has_counterpart:
        Whether the other language has the same page (controls ``hreflang``).
    colab:
        Map of page path -> Colab URL for this edition.

    Returns
    -------
    str
        HTML to insert before ``</head>``.
    """
    meta = LANG_META[edition.lang]
    other = edition.counterpart()
    esc = html.escape
    page_url = absolute_url(edition, page.url_path)
    tags = [f'<link rel="canonical" href="{esc(page_url)}"/>']
    alternates = {edition.lang: page_url}
    if has_counterpart:
        alternates[other.lang] = absolute_url(other, page.url_path)
    for lang in LANGS:
        if lang in alternates:
            tags.append(
                f'<link rel="alternate" hreflang="{LANG_META[lang]["hreflang"]}" '
                f'href="{esc(alternates[lang])}"/>'
            )
    tags.append(
        f'<link rel="alternate" hreflang="x-default" '
        f'href="{esc(alternates.get("zh", page_url))}"/>'
    )

    root = f"{base_path.rstrip('/')}/{edition.prefix}"
    config = {
        "lang": edition.lang,
        "edition": edition.edition,
        "htmlLang": meta["html_lang"],
        "root": root,
        "alternate": {
            "root": f"{base_path.rstrip('/')}/{other.prefix}",
            "hreflang": LANG_META[other.lang]["hreflang"],
            "title": meta["switch_title"],
        },
        "colab": colab,
        "colabLabel": meta["colab_label"],
    }
    config_json = json.dumps(config, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    tags.append(f"<script>window.EPI_SITE={config_json};</script>")
    for script in PAGE_SCRIPTS:
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
        ``base_path``, ``has_counterpart`` and ``colab``, passed to
        :func:`head_links_and_scripts`.

    Returns
    -------
    str
        The updated HTML (unchanged if it was already processed).
    """
    if POSTBUILD_MARKER in page_html:
        return page_html
    title = _meta_content(page_html, "property", "og:title") or "Epi With Python"
    page_html = set_html_lang(page_html, LANG_META[edition.lang]["html_lang"])
    page_html = fix_source_links(page_html, edition)
    added = []
    for attr, name, content in page_meta(page, edition, title):
        page_html, existed = upsert_meta(page_html, attr, name, content)
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
    site_dir: Path, url_root: str, skip_prefixes: tuple[str, ...] = ()
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

    Returns
    -------
    dict[str, list[str]]
        Broken ``href`` -> pages (relative paths) that contain it.
    """
    if not url_root.endswith("/"):
        raise ValueError(f"url_root must end with '/', got {url_root!r}")
    broken: dict[str, list[str]] = {}
    for html_file in sorted(site_dir.rglob("*.html")):
        page_url = page_url_for(html_file, site_dir, url_root)
        text = html_file.read_text(encoding="utf-8", errors="replace")
        # Inline scripts (e.g. plotly.js in a notebook output) are not markup.
        text = _SCRIPT_RX.sub("", text)
        for raw in set(_HREF_RX.findall(text)):
            href = html.unescape(raw).strip()
            if not href or href.startswith(("#", "//")) or _SCHEME_RX.match(href):
                continue  # in-page anchor or another site
            target = urljoin(page_url, href).split("#", 1)[0].split("?", 1)[0]
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
    site_dir: Path, url_root: str, label: str, skip_prefixes: tuple[str, ...] = ()
) -> None:
    """Raise :class:`SystemExit` if any same-site link in *site_dir* is broken."""
    broken = broken_links(site_dir, url_root, skip_prefixes)
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
        Counts of ``pages``, ``notebooks`` (Colab links) and ``redirects`` written.
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

    static_src = REPO_ROOT / "book" / "_static"
    static_dst = html_dir / "_static"
    static_dst.mkdir(exist_ok=True)
    for name in STATIC_FILES:
        shutil.copy2(static_src / name, static_dst / name)

    colab = {p.url_path: colab_url(edition.tree, p.location) for p in pages if p.is_notebook}
    other_tree = REPO_ROOT / edition.counterpart().tree
    lang_tag = LANG_META[edition.lang]["html_lang"]
    edition_root = f"{base_path.rstrip('/')}/{edition.prefix}"

    for page in pages:
        page_file = html_dir / page.url_path / "index.html"
        page_html = page_file.read_text(encoding="utf-8")
        page_file.write_text(
            process_page_html(
                page_html,
                page,
                edition,
                base_path=base_path,
                has_counterpart=(other_tree / page.location.lstrip("/")).is_file(),
                colab=colab,
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

    redirects = 0
    for page in pages:
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

    other_roots = tuple(
        f"{base_path.rstrip('/')}/{other.prefix}" for other in ALL_EDITIONS if other != edition
    )
    check_links(html_dir, edition_root, edition.label(), other_roots)
    return {"pages": len(pages), "notebooks": len(colab), "redirects": redirects}


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
        Path the site root is served under; when all four editions are
        included, every same-site link on the assembled site is checked.
    """
    if site_dir.resolve() in {REPO_ROOT, REPO_ROOT / "book", REPO_ROOT / "book_en"}:
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
    if len(editions) == len(ALL_EDITIONS):
        check_links(site_dir, f"{base_path.rstrip('/')}/", "assembled site")
    print(f"✔ site assembled in {site_dir}", flush=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lang", choices=LANGS, help="language to build")
    parser.add_argument("--edition", choices=EDITIONS, help="edition to build")
    parser.add_argument("--all", action="store_true", help="build all four editions")
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
        parser.error("give either --all, or both --lang and --edition")
    if not args.all and not (args.lang and args.edition):
        parser.error("--lang and --edition go together")
    return args


def main(argv: list[str] | None = None) -> None:
    """Command-line entry point."""
    args = parse_args(argv)
    editions = list(ALL_EDITIONS) if args.all else [Edition(args.lang, args.edition)]
    for edition in editions:
        if args.postprocess_only:
            print(f"✔ {edition.label()}: {postprocess(edition, args.base_path)}")
        else:
            build_edition(edition, args.base_path, execute=not args.no_execute)
    if args.site_dir:
        assemble_site(editions, args.site_dir, args.base_path)


if __name__ == "__main__":
    main()
