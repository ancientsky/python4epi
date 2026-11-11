"""Generate the standalone Bantay Santa Luz dashboard page (Philippines edition).

Chapter 09 of the Philippines edition ends with a self-contained HTML
dashboard. The book build (:mod:`build_book`) calls :func:`build_dashboard`
once per PH language after MyST has built that edition, with
``out_dir = <edition _build/html>/dashboard``; the page is therefore served at
``<edition root>/dashboard/`` (``/ph/dashboard/``, ``/ph/zh/dashboard/``,
``/ph/fil/dashboard/``) and the post-build link check accepts links to it.

Chapters link to it with a root-relative MyST link, which MyST prefixes with
the edition's ``BASE_URL``::

    [Open the dashboard](/dashboard/)

This module currently writes a small placeholder page; the chapter-09 author
replaces the body of :func:`build_dashboard` (keeping its signature). Contract:

* write ``out_dir / "index.html"`` (plus any assets it needs inside
  ``out_dir``) and return the path of ``index.html``;
* be deterministic and fast (it runs on every book build) and read only
  synthetic data under ``data/synthetic/ph/``;
* every same-site ``href`` it writes must resolve inside the built site (the
  post-build link check scans this page too); a relative ``../`` link goes
  back to the edition's home page.

It can also be run on its own for a quick look::

    uv run python scripts/build_ph_dashboard.py --lang en --out-dir /tmp/dash
"""

from __future__ import annotations

import argparse
import html
from pathlib import Path

#: Languages of the Philippines edition (same order as ``build_book.PH_LANGS``).
LANGS: tuple[str, ...] = ("en", "zh", "fil")

_HTML_LANG = {"en": "en", "zh": "zh-Hant", "fil": "fil"}

_COPY = {
    "en": {
        "title": "Bantay Santa Luz — outbreak dashboard",
        "lead": "The dashboard you build in chapter 9 will appear here.",
        "note": "Fictional city, synthetic data.",
        "back": "Back to the book",
    },
    "zh": {
        "title": "Bantay Santa Luz — 疫情儀表板",
        "lead": "你在第 9 章打造的儀表板將會放在這裡。",
        "note": "虛構的城市，合成的資料。",
        "back": "回到課本",
    },
    "fil": {
        "title": "Bantay Santa Luz — dashboard ng outbreak",
        "lead": "Dito lalabas ang dashboard na bubuuin mo sa kabanata 9.",
        "note": "Kathang-isip na lungsod, synthetic na datos.",
        "back": "Bumalik sa aklat",
    },
}


def build_dashboard(lang: str, out_dir: Path) -> Path:
    """Write the dashboard page for one language.

    Parameters
    ----------
    lang:
        ``"en"``, ``"zh"`` or ``"fil"``.
    out_dir:
        Directory the page is written to (created if needed); the build passes
        ``<edition _build/html>/dashboard``.

    Returns
    -------
    Path
        The written ``out_dir / "index.html"``.
    """
    if lang not in LANGS:
        raise ValueError(f"lang must be one of {LANGS}, got {lang!r}")
    copy = {key: html.escape(value) for key, value in _COPY[lang].items()}
    out_dir.mkdir(parents=True, exist_ok=True)
    page = out_dir / "index.html"
    page.write_text(
        "<!DOCTYPE html>\n"
        f'<html lang="{_HTML_LANG[lang]}">\n<head>\n<meta charset="utf-8"/>\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
        f"<title>{copy['title']}</title>\n"
        "<style>body{font-family:system-ui,sans-serif;max-width:40rem;margin:3rem auto;"
        "padding:0 1rem;line-height:1.5}h1{color:#0038A8}</style>\n"
        "</head>\n<body>\n"
        f"<h1>{copy['title']}</h1>\n<p>{copy['lead']}</p>\n<p><small>{copy['note']}</small></p>\n"
        f'<p><a href="../">{copy["back"]}</a></p>\n'
        "</body>\n</html>\n",
        encoding="utf-8",
    )
    return page


def main(argv: list[str] | None = None) -> None:
    """Command-line entry point: write one language's dashboard to a directory."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lang", choices=LANGS, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    print(build_dashboard(args.lang, args.out_dir))


if __name__ == "__main__":
    main()
