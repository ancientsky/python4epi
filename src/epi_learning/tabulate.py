"""Tabulation helpers inspired by epidemiology reporting workflows."""

from __future__ import annotations

import pandas as pd


def summarize_by_group(df: pd.DataFrame, group_col: str, outcome_col: str = "case_id") -> pd.DataFrame:
    """Produce a simple count and percentage summary by group."""
    if group_col not in df.columns:
        raise ValueError(f"Missing group column: {group_col}")
    if outcome_col not in df.columns:
        raise ValueError(f"Missing outcome column: {outcome_col}")

    summary = (
        df.groupby(group_col, dropna=False)[outcome_col]
        .count()
        .rename("n")
        .reset_index()
        .sort_values("n", ascending=False)
    )
    total = summary["n"].sum()
    summary["pct"] = (summary["n"] / total).round(4)
    return summary
