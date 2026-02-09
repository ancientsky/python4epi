"""Data cleaning utilities for line list datasets."""

from __future__ import annotations

from typing import Iterable

import pandas as pd

REQUIRED_COLUMNS = (
    "case_id",
    "date_onset",
    "date_report",
    "location",
    "age",
    "sex",
    "outcome",
)


def standardize_line_list(df: pd.DataFrame, required: Iterable[str] = REQUIRED_COLUMNS) -> pd.DataFrame:
    """Return a cleaned line list with standardized column names and dates.

    Parameters
    ----------
    df:
        Raw line list data.
    required:
        Required columns for teaching contracts.
    """
    out = df.copy()
    out.columns = [c.strip().lower() for c in out.columns]

    missing = [c for c in required if c not in out.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out["date_onset"] = pd.to_datetime(out["date_onset"], errors="coerce")
    out["date_report"] = pd.to_datetime(out["date_report"], errors="coerce")
    out["sex"] = out["sex"].astype(str).str.upper().replace({"MALE": "M", "FEMALE": "F"})
    out["location"] = out["location"].astype(str).str.strip()
    out["outcome"] = out["outcome"].astype(str).str.lower().str.strip()
    return out
