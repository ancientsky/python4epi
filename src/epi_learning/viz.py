"""Visualization helpers for trend and demographic views."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def configure_chinese_font() -> None:
    """Configure matplotlib to display CJK (Traditional Chinese) characters.

    Explicitly scans system font directories to discover and register CJK
    font files, then sets ``font.sans-serif`` accordingly.  Also disables
    the minus-sign substitution that can cause display issues with CJK fonts.

    This function is called automatically when this module is imported.
    It can also be called explicitly to re-apply settings after an
    ``rcParams`` reset.

    Notes
    -----
    Matplotlib's ``addfont()`` only registers face 0 of ``.ttc`` (TrueType
    Collection) files.  For Noto Sans CJK collections, face 0 is typically
    the JP variant, so "Noto Sans CJK TC" is never registered.  This
    function works around the limitation by discovering which CJK font
    family names were *actually* registered and placing them first in the
    ``font.sans-serif`` priority list.
    """
    import pathlib

    import matplotlib.font_manager as fm

    # Explicitly discover and register CJK font files instead of relying
    # on the font cache, which may be stale after installing new fonts.
    for font_dir in map(pathlib.Path, ["/usr/share/fonts", "/usr/local/share/fonts"]):
        if font_dir.exists():
            for fp in sorted(font_dir.rglob("*")):
                if fp.suffix.lower() in {".ttf", ".ttc", ".otf"} and (
                    "CJK" in fp.name or "WenQuanYi" in fp.name or "wqy" in fp.name
                ):
                    try:
                        fm.fontManager.addfont(str(fp))
                    except Exception:  # noqa: BLE001
                        pass

    # Discover which CJK font names were actually registered.
    # addfont() only registers face 0 of .ttc collections, so the actual
    # family name may differ from our preferred list (e.g. "Noto Sans CJK JP"
    # instead of "Noto Sans CJK TC").  Any Noto Sans CJK variant covers the
    # full CJK Unified Ideographs range, so any variant works for display.
    _cjk_keywords = {"cjk", "wenquanyi", "wqy"}
    discovered: list[str] = []
    for entry in fm.fontManager.ttflist:
        if any(kw in entry.name.lower() for kw in _cjk_keywords):
            if entry.name not in discovered:
                discovered.append(entry.name)

    # Preferred candidates — may or may not be installed.
    preferred = [
        "Noto Sans CJK TC",
        "Noto Sans CJK SC",
        "Noto Sans CJK JP",
        "Noto Sans CJK KR",
        "Noto Sans CJK HK",
        "Noto Sans TC",
        "Microsoft JhengHei",
        "WenQuanYi Zen Hei",
        "SimHei",
        "Arial Unicode MS",
        "Heiti TC",
    ]

    # Build final list: actually-available CJK fonts first, then preferred,
    # then whatever the user already had configured.
    candidates = list(discovered)
    for name in preferred:
        if name not in candidates:
            candidates.append(name)

    current = plt.rcParams.get("font.sans-serif", [])
    plt.rcParams["font.sans-serif"] = candidates + [
        f for f in current if f not in candidates
    ]
    plt.rcParams["axes.unicode_minus"] = False


# Auto-configure on import so that any notebook or script that does
# ``from epi_learning.viz import plot_epi_curve`` gets CJK support.
configure_chinese_font()


def plot_epi_curve(df: pd.DataFrame, date_col: str = "date_onset"):
    """Return a matplotlib Axes object for epidemic curve."""
    if date_col not in df.columns:
        raise ValueError(f"Missing date column: {date_col}")

    plot_df = df.copy()
    plot_df[date_col] = pd.to_datetime(plot_df[date_col], errors="coerce")
    counts = plot_df.dropna(subset=[date_col]).groupby(date_col).size()

    fig, ax = plt.subplots(figsize=(10, 4))
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Epidemic Curve")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cases")
    fig.tight_layout()
    return ax
