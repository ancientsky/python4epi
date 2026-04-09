"""Generate the Open Graph social card for Epi With Python.

Outputs ``book/_static/og-image.png`` at 1200×630 (the Facebook/Twitter/LinkedIn
recommended aspect for ``twitter:card = summary_large_image``).

Run once after visual tweaks and commit the resulting PNG so CI does not need
to regenerate it:

    uv run python scripts/generate_og_image.py

The visual language mirrors the repository brand palette used consistently by
the Manim videos (``videos/src/base_scene.py``) and the SVG diagrams under
``book/chapters/images/``.
"""

from __future__ import annotations

import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------------------
# Brand palette (keep in sync with CLAUDE.md "Visual Style")
# ---------------------------------------------------------------------------
BG_WARM = "#FAF8F3"
BG_CARD_ALT = "#F5F3EE"
ACCENT_ORANGE = "#D97757"
ACCENT_ORANGE_SOFT = "#F2B89E"
ACCENT_BLUE = "#6A9BCC"
ACCENT_GREEN = "#788C5D"
TEXT_PRIMARY = "#1A1A1A"
TEXT_SECONDARY = "#6B6B6B"
BORDER_LIGHT = "#E8E5DF"

# Output canvas: 1200 × 630 at dpi=100
WIDTH, HEIGHT, DPI = 1200, 630, 100


def _register_cjk_fonts() -> tuple[str, str]:
    """Discover installed CJK fonts and return (serif_name, sans_name).

    Mirrors the discovery logic in ``book/_config.yml`` ``nb_execution_pre_code``
    so this script works inside the same environment the book is built in.
    """
    font_dirs = [
        pathlib.Path("/usr/share/fonts"),
        pathlib.Path("/usr/local/share/fonts"),
        pathlib.Path.home() / ".fonts",
    ]
    for root in font_dirs:
        if not root.exists():
            continue
        for fp in sorted(root.rglob("*")):
            if fp.suffix.lower() not in {".ttf", ".ttc", ".otf"}:
                continue
            name = fp.name
            if "CJK" in name or "WenQuanYi" in name or "wqy" in name or "Noto" in name:
                try:
                    fm.fontManager.addfont(str(fp))
                except Exception:
                    pass

    serif_candidates = [
        "Noto Serif CJK TC", "Noto Serif CJK JP", "Noto Serif CJK SC",
        "Noto Serif TC", "Source Han Serif TC", "Songti TC",
    ]
    sans_candidates = [
        "Noto Sans CJK TC", "Noto Sans CJK JP", "Noto Sans CJK SC",
        "Noto Sans TC", "WenQuanYi Zen Hei", "PingFang TC",
    ]
    available = {f.name for f in fm.fontManager.ttflist}

    serif = next((n for n in serif_candidates if n in available), None)
    sans = next((n for n in sans_candidates if n in available), None)

    # Fall back to the first CJK-capable family we can find
    if serif is None:
        serif = next((n for n in available if "CJK" in n or "Noto" in n), "DejaVu Serif")
    if sans is None:
        sans = next((n for n in available if "CJK" in n or "Noto" in n), "DejaVu Sans")

    return serif, sans


def _draw_bacteria_glyph(ax: plt.Axes, cx: float, cy: float, scale: float,
                         alpha: float = 1.0) -> None:
    """Draw the rod-shaped bacterium glyph that matches favicon.svg / logo.svg.

    Because the axes use inverted Y (top-left origin) we draw in *data*
    coordinates directly, without combining Affine2D transforms — the latter
    interacts awkwardly with FancyBboxPatch's boxstyle geometry.
    """
    # Rod body: rounded rectangle centered on (cx, cy)
    body_w, body_h = 44 * scale, 14 * scale
    body = FancyBboxPatch(
        (cx - body_w / 2, cy - body_h / 2),
        body_w, body_h,
        boxstyle=f"round,pad=0,rounding_size={7 * scale}",
        facecolor=ACCENT_ORANGE, edgecolor="none", alpha=alpha, zorder=6,
    )
    ax.add_patch(body)

    # Inner highlight stripe
    hl_w, hl_h = 36 * scale, 3 * scale
    highlight = FancyBboxPatch(
        (cx - hl_w / 2, cy - body_h / 2 + 3 * scale),
        hl_w, hl_h,
        boxstyle=f"round,pad=0,rounding_size={1.5 * scale}",
        facecolor=ACCENT_ORANGE_SOFT, edgecolor="none",
        alpha=0.55 * alpha, zorder=7,
    )
    ax.add_patch(highlight)

    # Two accent dots: blue (left), green (right)
    ax.add_patch(patches.Circle(
        (cx - 11 * scale, cy + 1 * scale), 3 * scale,
        facecolor=ACCENT_BLUE, edgecolor="none", alpha=alpha, zorder=7,
    ))
    ax.add_patch(patches.Circle(
        (cx + 11 * scale, cy + 1 * scale), 2.2 * scale,
        facecolor=ACCENT_GREEN, edgecolor="none", alpha=alpha, zorder=7,
    ))


def generate(out_path: pathlib.Path) -> None:
    serif_name, sans_name = _register_cjk_fonts()
    print(f"Using serif = {serif_name!r}, sans = {sans_name!r}", file=sys.stderr)

    fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor=BG_WARM)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.invert_yaxis()  # put (0,0) at top-left for easier layout math
    ax.set_axis_off()

    # Warm background
    ax.add_patch(patches.Rectangle((0, 0), WIDTH, HEIGHT, facecolor=BG_WARM, zorder=0))

    # Subtle alternate-tone strip on the right
    ax.add_patch(patches.Rectangle(
        (WIDTH - 420, 0), 420, HEIGHT,
        facecolor=BG_CARD_ALT, edgecolor="none", alpha=0.6, zorder=1,
    ))

    # Accent bar on the left edge
    ax.add_patch(patches.Rectangle(
        (0, 0), 24, HEIGHT, facecolor=ACCENT_ORANGE, zorder=2,
    ))

    # Fine border line
    ax.add_patch(patches.Rectangle(
        (0, 0), WIDTH, HEIGHT,
        facecolor="none", edgecolor=BORDER_LIGHT, linewidth=3, zorder=3,
    ))

    # Small kicker label
    ax.text(
        78, 120, "EPIDEMIOLOGY × PYTHON",
        fontfamily=sans_name, fontsize=18, color=TEXT_SECONDARY,
        fontweight="bold", ha="left", va="center", zorder=5,
    )

    # Accent dot separator
    ax.add_patch(patches.Circle((78 + 340, 120), 4, facecolor=ACCENT_ORANGE, zorder=5))
    ax.text(
        78 + 360, 120, "18 CHAPTERS",
        fontfamily=sans_name, fontsize=18, color=TEXT_SECONDARY,
        fontweight="bold", ha="left", va="center", zorder=5,
    )

    # Main English title
    ax.text(
        78, 230, "Epi With Python",
        fontfamily=serif_name, fontsize=78, color=TEXT_PRIMARY,
        fontweight="bold", ha="left", va="center", zorder=5,
    )

    # Chinese subtitle
    ax.text(
        78, 320, "用 Python 學流行病學",
        fontfamily=serif_name, fontsize=54, color=TEXT_PRIMARY,
        fontweight="bold", ha="left", va="center", zorder=5,
    )

    # Tagline
    ax.text(
        78, 405, "從接獲通報到結案報告 — 一場退伍軍人症疫調",
        fontfamily=sans_name, fontsize=26, color=TEXT_SECONDARY,
        ha="left", va="center", zorder=5,
    )
    ax.text(
        78, 445, "18 章 Python 課程，從零基礎到 ML / DL",
        fontfamily=sans_name, fontsize=26, color=TEXT_SECONDARY,
        ha="left", va="center", zorder=5,
    )

    # Footer strip with site URL
    ax.add_patch(patches.Rectangle(
        (0, HEIGHT - 70), WIDTH, 70, facecolor=BG_CARD_ALT, zorder=4,
    ))
    ax.add_patch(patches.Rectangle(
        (0, HEIGHT - 73), WIDTH, 3, facecolor=BORDER_LIGHT, zorder=4,
    ))
    ax.text(
        78, HEIGHT - 35, "ancientsky.github.io/python4epi",
        fontfamily=sans_name, fontsize=22, color=TEXT_PRIMARY,
        fontweight="bold", ha="left", va="center", zorder=5,
    )
    ax.text(
        WIDTH - 78, HEIGHT - 35, "松柏護理之家 · 退伍軍人症群聚事件",
        fontfamily=sans_name, fontsize=20, color=TEXT_SECONDARY,
        ha="right", va="center", zorder=5,
    )

    # Bacteria glyph (big, on the right-hand alt-tone panel)
    _draw_bacteria_glyph(ax, cx=WIDTH - 210, cy=255, scale=5.0, alpha=1.0)
    # Smaller echo
    _draw_bacteria_glyph(ax, cx=WIDTH - 330, cy=400, scale=2.2, alpha=0.65)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=DPI, facecolor=BG_WARM, edgecolor="none")
    plt.close(fig)
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)", file=sys.stderr)


def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    out = repo_root / "book" / "_static" / "og-image.png"
    generate(out)


if __name__ == "__main__":
    main()
