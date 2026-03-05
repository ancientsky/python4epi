"""Visualization helpers for trend and demographic views."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def configure_chinese_font() -> None:
    """Configure matplotlib to display CJK (Traditional Chinese) characters.

    Searches for common CJK fonts available on the system and sets
    ``font.sans-serif`` accordingly.  Also disables the minus-sign
    substitution that can cause display issues with CJK fonts.

    This function is called automatically when this module is imported.
    It can also be called explicitly to re-apply settings after an
    ``rcParams`` reset.
    """
    import matplotlib.font_manager as fm

    # Rebuild font list to pick up newly installed fonts (e.g. in CI)
    fm._load_fontmanager(try_read_cache=False)

    candidates = [
        "Noto Sans CJK TC",
        "Noto Sans TC",
        "Microsoft JhengHei",
        "WenQuanYi Zen Hei",
        "SimHei",
        "Arial Unicode MS",
        "Heiti TC",
    ]
    current = plt.rcParams.get("font.sans-serif", [])
    # Prepend CJK candidates (preserving existing fallbacks)
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
