"""Visualization helpers for trend and demographic views."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


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
