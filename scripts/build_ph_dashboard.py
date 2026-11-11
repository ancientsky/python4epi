"""Generate the Bantay Santa Luz outbreak dashboard (Philippines edition, chapter 9).

The dashboard is ONE self-contained ``index.html``: the CSS, the JavaScript
that draws the charts (hand-written inline SVG, no chart library) and the
aggregated data are all inside the file, so it makes no network request and
can be e-mailed, put on a USB stick or opened offline.

How it is built (each step is a small pure function the chapter-9 notebook
can import and explain)::

    data     = load_data()                    # read data/synthetic/ph/
    kpis     = compute_kpis(data)             # headline numbers (README)
    payload  = build_payload(data, lang)      # aggregate + suppress small cells
    page     = render_html(payload)           # one HTML string
    build_dashboard(lang, out_dir)            # all of the above, written to disk

Privacy rules implemented here (chapter 2 and the chapter-9 publish check):

* only aggregates leave this module — no case IDs, names, addresses or
  exact dates of individual cases;
* whole-city totals for the whole period (the KPI tiles) are shown in full;
  every smaller cell (a week, a barangay, an age-sex group) with a count of
  1-4 is replaced by ``"<5"`` *before* it is written into the page, and its
  rate is withheld (:func:`suppress_small_cells`);
* where a table's column totals are published, a second cell is withheld
  (``"x"``) whenever a column would otherwise hide only one small cell, so the
  small cell cannot be worked out by subtraction.

The book build (:mod:`build_book`) calls :func:`build_dashboard` once per PH
language with ``out_dir = <edition _build/html>/dashboard``; the page is
served at ``<edition root>/dashboard/`` and chapters link to it with the
root-relative MyST link ``[Open the dashboard](/dashboard/)``. Its own links
are relative (``../`` = the edition's home page), so the post-build link check
can verify them.

The TimesFM forecast fan is drawn only when chapter 7 has committed a cached
forecast (``data/tsfm_cache/ph*.json``, written by
:mod:`epi_learning.tsfm`) whose input fingerprint matches the weekly dengue
series *ending at the last week* — i.e. a genuine forecast of the weeks after
the data freeze (a single full-series context, or the
``scripts/make_timesfm_cache.py --csv`` layout: rolling origins plus the end
of the series; univariate, no covariates). Otherwise the panel says
"forecast not available"; nothing is ever invented.

Run it on its own for a quick look::

    uv run python scripts/build_ph_dashboard.py --lang en --out-dir /tmp/dash
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

#: Languages of the Philippines edition (same order as ``build_book.PH_LANGS``).
LANGS: tuple[str, ...] = ("en", "zh", "fil")

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "synthetic" / "ph"
CACHE_DIR = REPO_ROOT / "data" / "tsfm_cache"

#: Data freeze: the line list holds every case reported by this date.
AS_OF = dt.date(2026, 9, 30)
#: Typhoon Amihan makes landfall.
TYPHOON = dt.date(2026, 7, 18)
#: Counts of 1 .. SMALL_CELL - 1 are suppressed in every cell below city level.
SMALL_CELL = 5
#: Years whose same-week counts define the epidemic threshold (data README).
THRESHOLD_YEARS: tuple[int, ...] = (2022, 2023, 2024, 2025)
#: First ISO week of 2026 drawn in the threshold panel.
THRESHOLD_FROM_WEEK = 22
#: First ISO week of 2026 drawn in the epidemic curve (Amihan is in W29).
CURVE_FROM_WEEK = 28
DISEASES: tuple[str, ...] = ("leptospirosis", "dengue")
AGE_GROUPS: tuple[str, ...] = ("0-4", "5-14", "15-24", "25-44", "45-64", "65+")
BANDS: tuple[str, ...] = ("riverside", "coastal", "upland")

_HTML_LANG = {"en": "en", "zh": "zh-Hant", "fil": "fil"}
_LANG_NAMES = {"en": "EN", "zh": "中文", "fil": "Filipino"}
#: Relative path from each language's dashboard to every other language's.
_LANG_LINKS = {
    "en": {"en": "./", "zh": "../zh/dashboard/", "fil": "../fil/dashboard/"},
    "zh": {"en": "../../dashboard/", "zh": "./", "fil": "../../fil/dashboard/"},
    "fil": {"en": "../../dashboard/", "zh": "../../zh/dashboard/", "fil": "./"},
}

# =============================================================================
# 1. Data
# =============================================================================


def load_data(data_dir: Path = DATA_DIR) -> dict[str, Any]:
    """Read the synthetic Santa Luz files the dashboard needs.

    Parameters
    ----------
    data_dir : Path
        Folder with the files documented in ``data/synthetic/ph/README.md``.

    Returns
    -------
    dict
        ``linelist``, ``barangays``, ``weekly``, ``signals``, ``case_control``
        (pandas DataFrames) and ``geojson`` (the parsed FeatureCollection).
    """
    data_dir = Path(data_dir)
    if not (data_dir / "santa_luz_linelist.csv").is_file():
        raise ValueError(f"no santa_luz_linelist.csv in {data_dir}")
    dates = ["date_onset", "date_consult", "date_report", "date_lab_confirmed"]
    signal_dates = ["date_emergence", "date_detection", "date_notification",
                    "date_response_complete"]
    return {
        "linelist": pd.read_csv(data_dir / "santa_luz_linelist.csv", parse_dates=dates),
        "barangays": pd.read_csv(data_dir / "santa_luz_barangays.csv"),
        "weekly": pd.read_csv(data_dir / "santa_luz_dengue_weekly.csv",
                              parse_dates=["week_start"]),
        "signals": pd.read_csv(data_dir / "signals_717.csv", parse_dates=signal_dates),
        "case_control": pd.read_csv(data_dir / "lepto_case_control.csv"),
        "geojson": json.loads((data_dir / "santa_luz_barangays.geojson").read_text("utf-8")),
    }


# =============================================================================
# 2. Numbers
# =============================================================================


def epidemic_threshold(weekly: pd.DataFrame, years: tuple[int, ...] = THRESHOLD_YEARS
                       ) -> pd.Series:
    """Epidemic threshold per ISO week: mean + 2 SD of weeks w-1, w, w+1 in *years*.

    Same rule as ``epidemic_threshold()`` in ``generate_santa_luz.py``.

    Parameters
    ----------
    weekly : pandas.DataFrame
        Weekly file with ``iso_year``, ``iso_week`` and ``cases``.
    years : tuple of int
        Baseline years (non-epidemic, non-COVID).

    Returns
    -------
    pandas.Series
        Threshold indexed by ISO week 1-53 (week 1 wraps to week 52).
    """
    base = weekly[weekly["iso_year"].isin(years)]
    if base.empty:
        raise ValueError(f"no baseline weeks for years {years}")
    out = {}
    for wk in range(1, 54):
        window = {(wk - 2) % 52 + 1, wk, wk % 52 + 1} if wk <= 52 else {52, 53, 1}
        values = base.loc[base["iso_week"].isin(window), "cases"]
        out[wk] = values.mean() + 2 * values.std(ddof=1)
    return pd.Series(out, name="threshold")


def _pct(part: float, whole: float, decimals: int = 1) -> float:
    if whole == 0:
        raise ValueError("percentage of an empty denominator")
    return round(float(100 * part / whole), decimals)


def compute_kpis(data: dict[str, Any]) -> dict[str, Any]:
    """Headline numbers for the KPI tiles and the action panel.

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.

    Returns
    -------
    dict
        Counts by disease (``cases``, ``deaths``, ``hospitalised``), ``cfr_pct``,
        the dengue threshold weeks (``weeks_above``, ``first_above``) and a few
        details used in the text (median ages, severity, last onset, lab delay).
    """
    ll = data["linelist"]
    by = ll.groupby("disease")
    cases = by.size().reindex(DISEASES).astype(int)
    deaths = by["outcome"].apply(lambda s: int((s == "died").sum())).reindex(DISEASES)
    hosp = by["hospitalised"].sum().reindex(DISEASES).astype(int)

    weekly = data["weekly"]
    thr = epidemic_threshold(weekly)
    year = weekly[weekly["iso_year"] == AS_OF.isocalendar().year].copy()
    year["threshold"] = year["iso_week"].map(thr)
    above = year[year["cases"] > year["threshold"]]

    lep = ll[ll["disease"] == "leptospirosis"]
    den = ll[ll["disease"] == "dengue"]
    confirmed = ll[ll["case_class"] == "confirmed"]
    lab_days = (confirmed["date_lab_confirmed"] - confirmed["date_consult"]).dt.days
    lab_median = lab_days.groupby(confirmed["disease"]).median()
    last_lep = lep["date_onset"].max().date()
    severity = den["dengue_severity"].value_counts()
    return {
        "cases": {**{d: int(cases[d]) for d in DISEASES}, "total": int(cases.sum())},
        "deaths": {**{d: int(deaths[d]) for d in DISEASES}, "total": int(deaths.sum())},
        "cfr_pct": {d: _pct(deaths[d], cases[d]) for d in DISEASES},
        "hospitalised": {**{d: int(hosp[d]) for d in DISEASES}, "total": int(hosp.sum())},
        "hospitalised_pct": _pct(hosp.sum(), cases.sum(), 0),
        "weeks_above": len(above),
        "first_above": str(above["morbidity_week"].iloc[0]) if len(above) else None,
        "first_above_start": above["week_start"].iloc[0].date() if len(above) else None,
        "last_week": str(year["morbidity_week"].iloc[-1]),
        "male_pct": {d: _pct((ll.loc[ll["disease"] == d, "sex"] == "M").sum(), cases[d], 0)
                     for d in DISEASES},
        "median_age": {d: int(ll.loc[ll["disease"] == d, "age"].median()) for d in DISEASES},
        "dengue_warning": int(severity.get("warning_signs", 0)),
        "dengue_severe": int(severity.get("severe", 0)),
        "last_lepto_onset": last_lep,
        "days_since_lepto": (AS_OF - last_lep).days,
        "lab_median_days": {d: int(lab_median[d]) for d in DISEASES},
        "unknown_age": int(ll["age"].isna().sum()),
    }


# =============================================================================
# 3. Privacy: small-cell suppression
# =============================================================================


def suppression_status(counts: pd.DataFrame, threshold: int = SMALL_CELL,
                       secondary_axis: int | None = 0) -> pd.DataFrame:
    """Decide which cells of a count table may be published.

    Parameters
    ----------
    counts : pandas.DataFrame
        Non-negative whole-number counts.
    threshold : int
        Counts from 1 to ``threshold - 1`` are *primary* suppressed. Zero is
        published (it describes no one).
    secondary_axis : int or None
        ``0``: column totals are public, so in any column that hides exactly
        one cell, also hide the smallest other non-zero cell (*secondary*
        suppression), repeating until stable. ``1``: the same along rows.
        ``None``: no secondary suppression.

    Returns
    -------
    pandas.DataFrame
        Same shape, values ``"ok"``, ``"primary"`` or ``"secondary"``.
    """
    if threshold < 1:
        raise ValueError(f"threshold must be >= 1, got {threshold}")
    if secondary_axis not in (0, 1, None):
        raise ValueError(f"secondary_axis must be 0, 1 or None, got {secondary_axis!r}")
    values = counts.astype(float)
    if (values < 0).any().any() or values.isna().any().any():
        raise ValueError("counts must be non-negative and complete")
    status = pd.DataFrame("ok", index=counts.index, columns=counts.columns, dtype=object)
    status = status.mask((values > 0) & (values < threshold), "primary")
    if secondary_axis is None:
        return status
    changed = True
    while changed:
        changed = False
        frame_s, frame_v = (status, values) if secondary_axis == 0 else (status.T, values.T)
        for line in frame_s.columns:
            hidden = frame_s[line] != "ok"
            if hidden.sum() != 1:
                continue
            others = frame_v.loc[~hidden & (frame_v[line] > 0), line]
            if others.empty:
                continue
            pick = others.sort_values(kind="stable").index[0]
            if secondary_axis == 0:
                status.loc[pick, line] = "secondary"
            else:
                status.loc[line, pick] = "secondary"
            changed = True
    return status


def suppress_small_cells(counts: pd.DataFrame, threshold: int = SMALL_CELL,
                         secondary_axis: int | None = 0) -> pd.DataFrame:
    """Return the publishable version of a count table.

    Parameters
    ----------
    counts : pandas.DataFrame
        Whole-number counts (e.g. cases by barangay and disease).
    threshold : int
        Counts of 1 .. ``threshold - 1`` become ``"<5"`` (for the default 5).
    secondary_axis : int or None
        See :func:`suppression_status`; secondary cells become ``"x"``.

    Returns
    -------
    pandas.DataFrame
        Object table: published counts as ``int``, withheld cells as strings.

    Examples
    --------
    >>> t = pd.DataFrame({"M": [12, 3, 20], "F": [9, 0, 2]})
    >>> suppress_small_cells(t).to_dict("list")
    {'M': ['x', '<5', 20], 'F': ['x', 0, '<5']}
    """
    status = suppression_status(counts, threshold, secondary_axis)
    out = counts.astype(int).astype(object)
    out = out.mask(status == "primary", f"<{threshold}")
    return out.mask(status == "secondary", "x")


def _cell(value: float, status: str) -> list[Any]:
    """Encode one published cell for the page: ``[value or None, 0|1|2]``."""
    code = {"ok": 0, "primary": 1, "secondary": 2}[status]
    return [int(value) if code == 0 else None, code]


# =============================================================================
# 4. Aggregates for each panel (already suppressed)
# =============================================================================


def _iso_week_label(year: int, week: int) -> str:
    return f"{year}-W{week:02d}"


def epi_curve(data: dict[str, Any]) -> dict[str, Any]:
    """Weekly cases by onset and disease (2026, ISO weeks), small cells suppressed.

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.

    Returns
    -------
    dict
        ``weeks``: list of ``{"wk", "start", "leptospirosis", "dengue"}`` with
        each disease encoded as ``[value or None, status]``.
    """
    ll = data["linelist"].dropna(subset=["date_onset"])
    iso = ll["date_onset"].dt.isocalendar()
    year = AS_OF.isocalendar().year
    last = data["weekly"].query("iso_year == @year")["iso_week"].max()
    weeks = list(range(CURVE_FROM_WEEK, int(last) + 1))
    counts = (pd.crosstab(iso["week"].astype(int), ll["disease"])
              .reindex(index=weeks, columns=list(DISEASES), fill_value=0))
    status = suppression_status(counts, secondary_axis=None)
    rows = []
    for wk in weeks:
        start = dt.date.fromisocalendar(year, wk, 1)
        rows.append({"wk": f"W{wk:02d}", "start": start.isoformat(),
                     **{d: _cell(counts.loc[wk, d], status.loc[wk, d]) for d in DISEASES}})
    peaks = {d: counts[d].idxmax() for d in DISEASES}
    return {"weeks": rows,
            "peak": {d: {"wk": f"W{peaks[d]:02d}", "n": int(counts.loc[peaks[d], d])}
                     for d in DISEASES}}


def threshold_series(data: dict[str, Any]) -> dict[str, Any]:
    """2026 weekly dengue cases against the epidemic threshold (suppressed).

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.

    Returns
    -------
    dict
        ``weeks`` (``wk``, ``start``, ``cell``, ``thr``, ``above``) and the
        thresholds of the 12 weeks after the last one (``future_thr``).
    """
    weekly = data["weekly"]
    thr = epidemic_threshold(weekly)
    year = AS_OF.isocalendar().year
    sub = weekly[(weekly["iso_year"] == year) & (weekly["iso_week"] >= THRESHOLD_FROM_WEEK)]
    status = suppression_status(sub[["cases"]].reset_index(drop=True), secondary_axis=None)
    rows = []
    for i, r in enumerate(sub.itertuples(index=False)):
        rows.append({"wk": f"W{r.iso_week:02d}", "start": r.week_start.date().isoformat(),
                     "cell": _cell(r.cases, status.loc[i, "cases"]),
                     "thr": round(float(thr[r.iso_week]), 1),
                     "above": bool(r.cases > thr[r.iso_week])})
    last = int(sub["iso_week"].iloc[-1])
    future = []
    start = dt.date.fromisocalendar(year, last, 1)
    for k in range(1, 13):
        day = start + dt.timedelta(weeks=k)
        iso = day.isocalendar()
        future.append({"wk": f"W{iso.week:02d}", "start": day.isoformat(),
                       "thr": round(float(thr[iso.week]), 1)})
    return {"weeks": rows, "future_thr": future}


def barangay_table(data: dict[str, Any]) -> pd.DataFrame:
    """Cases and attack rates per 10,000 by barangay and disease, suppressed.

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.

    Returns
    -------
    pandas.DataFrame
        One row per barangay (``barangay_id`` order): ``barangay``, ``band``,
        ``population`` and, per disease, ``<disease>_cell`` (``[value, status]``)
        and ``<disease>_rate`` (``None`` when withheld).
    """
    brgy = data["barangays"].set_index("barangay_id")
    counts = (pd.crosstab(data["linelist"]["barangay_id"], data["linelist"]["disease"])
              .reindex(index=brgy.index, columns=list(DISEASES), fill_value=0))
    status = suppression_status(counts, secondary_axis=0)
    out = brgy[["barangay", "band", "population"]].copy()
    for d in DISEASES:
        out[f"{d}_cell"] = [_cell(counts.loc[i, d], status.loc[i, d]) for i in brgy.index]
        out[f"{d}_rate"] = pd.Series(
            [round(10_000 * counts.loc[i, d] / brgy.loc[i, "population"], 1)
             if status.loc[i, d] == "ok" else None for i in brgy.index],
            index=brgy.index, dtype=object)
    return out


def band_rates(data: dict[str, Any]) -> dict[str, dict[str, float]]:
    """Attack rate per 10,000 by band and disease (README table).

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.

    Returns
    -------
    dict
        ``{disease: {band: rate}}``.
    """
    pop = data["barangays"].groupby("band")["population"].sum()
    cases = data["linelist"].groupby(["disease", "band"]).size()
    return {d: {b: round(10_000 * int(cases.get((d, b), 0)) / pop[b], 1) for b in BANDS}
            for d in DISEASES}


def age_sex_table(data: dict[str, Any], disease: str) -> pd.DataFrame:
    """Cases by age group (rows) and sex (columns) for one disease, suppressed.

    Sex totals are quoted in the text, so secondary suppression runs down each
    sex column.

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.
    disease : str
        ``"leptospirosis"`` or ``"dengue"``.

    Returns
    -------
    pandas.DataFrame
        Index = age groups, columns ``M`` and ``F``, cells ``[value, status]``.
    """
    if disease not in DISEASES:
        raise ValueError(f"disease must be one of {DISEASES}, got {disease!r}")
    ll = data["linelist"][data["linelist"]["disease"] == disease]
    counts = (pd.crosstab(ll["age_group"], ll["sex"])
              .reindex(index=list(AGE_GROUPS), columns=["M", "F"], fill_value=0))
    status = suppression_status(counts, secondary_axis=0)
    return pd.DataFrame({s: [_cell(counts.loc[a, s], status.loc[a, s]) for a in AGE_GROUPS]
                         for s in ("M", "F")}, index=list(AGE_GROUPS))


def _woolf(a: float, b: float, c: float, d: float) -> tuple[float, float, float]:
    """Odds ratio with a Woolf (log) 95% CI from a 2x2 table."""
    if min(a, b, c, d) <= 0:
        raise ValueError("Woolf CI needs four non-zero cells")
    odds = (a * d) / (b * c)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    return odds, math.exp(math.log(odds) - 1.96 * se), math.exp(math.log(odds) + 1.96 * se)


def _two_by_two(frame: pd.DataFrame, exposed: pd.Series) -> tuple[int, int, int, int]:
    case = frame["case"] == 1
    return (int((exposed & case).sum()), int((exposed & ~case).sum()),
            int((~exposed & case).sum()), int((~exposed & ~case).sum()))


def _mantel_haenszel(frame: pd.DataFrame, exposure: str, stratum: str
                     ) -> tuple[float, float, float]:
    """Mantel-Haenszel OR with the Robins-Breslow-Greenland 95% CI."""
    r_sum = s_sum = pr = ps_qr = qs = 0.0
    for _, part in frame.groupby(stratum):
        a, b, c, d = _two_by_two(part, part[exposure] == 1)
        n = a + b + c + d
        r, s = a * d / n, b * c / n
        p, q = (a + d) / n, (b + c) / n
        r_sum += r
        s_sum += s
        pr += p * r
        ps_qr += p * s + q * r
        qs += q * s
    odds = r_sum / s_sum
    var = pr / (2 * r_sum**2) + ps_qr / (2 * r_sum * s_sum) + qs / (2 * s_sum**2)
    se = math.sqrt(var)
    return odds, math.exp(math.log(odds) - 1.96 * se), math.exp(math.log(odds) + 1.96 * se)


def case_control_ors(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Crude odds ratios (Woolf 95% CI) of the leptospirosis case-control study.

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.

    Returns
    -------
    list of dict
        ``key``, ``or``, ``lo``, ``hi`` and ``kind`` (``risk``, ``protective``,
        ``null`` or ``adjusted``), in display order.
    """
    cc = data["case_control"]
    waders = cc[cc["waded_floodwater"] == 1]
    rows: list[tuple[str, tuple[float, float, float], str | None]] = [
        ("waded", _woolf(*_two_by_two(cc, cc["waded_floodwater"] == 1)), None),
        ("waded_adj", _mantel_haenszel(cc, "waded_floodwater", "cleanup_work"), "adjusted"),
        ("noboots", _woolf(*_two_by_two(
            cc, (cc["waded_floodwater"] == 1) & (cc["wore_boots"] == 0))), None),
        ("boots", _woolf(*_two_by_two(waders, waders["wore_boots"] == 1)), None),
        ("doxy", _woolf(*_two_by_two(cc, cc["doxy_prophylaxis"] == 1)), None),
        ("wound", _woolf(*_two_by_two(cc, cc["skin_wound"] == 1)), None),
        ("cleanup", _woolf(*_two_by_two(cc, cc["cleanup_work"] == 1)), None),
        ("male", _woolf(*_two_by_two(cc, cc["sex"] == "M")), None),
        ("rats", _woolf(*_two_by_two(cc, cc["rats_near_home"] == 1)), None),
    ]
    out = []
    for key, (odds, lo, hi), kind in rows:
        if kind is None:
            kind = "risk" if lo > 1 else "protective" if hi < 1 else "null"
        out.append({"key": key, "or": round(odds, 2), "lo": round(lo, 2), "hi": round(hi, 2),
                    "kind": kind})
    return out


def timeliness_717(data: dict[str, Any]) -> dict[str, Any]:
    """7-1-7 performance of the 40 public-health events and their bottlenecks.

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.

    Returns
    -------
    dict
        ``targets`` (detect / notify / respond: ``met``, ``pct``, ``median``),
        ``all`` (met all three), ``n``, period and the four most frequent
        ``bottlenecks`` (``text``, ``n`` events).
    """
    s = data["signals"]
    delays = {
        "detect": ((s["date_detection"] - s["date_emergence"]).dt.days, 7),
        "notify": ((s["date_notification"] - s["date_detection"]).dt.days, 1),
        "respond": ((s["date_response_complete"] - s["date_notification"]).dt.days, 7),
    }
    met = {k: v <= limit for k, (v, limit) in delays.items()}
    n = len(s)
    all_met = met["detect"] & met["notify"] & met["respond"]
    causes = s.loc[s["bottleneck"] != "none", "bottleneck"].str.split("; ").explode()
    counted = causes.value_counts()
    ranked = sorted(counted.items(), key=lambda kv: (-kv[1], kv[0].casefold()))[:4]
    return {
        "n": n,
        "from": s["date_emergence"].min().date(),
        "to": s["date_emergence"].max().date(),
        "targets": [{"key": k, "met": int(met[k].sum()), "pct": _pct(met[k].sum(), n, 0),
                     "median": int(delays[k][0].median())} for k in delays],
        "all": {"met": int(all_met.sum()), "pct": _pct(all_met.sum(), n, 0)},
        "bottlenecks": [{"text": t, "n": int(c)} for t, c in ranked],
    }


def _forecast_layouts(y: np.ndarray, n: int, horizon: int
                      ) -> list[tuple[list[np.ndarray], int]]:
    """Batches of contexts a "forecast from the end of the series" request may have used.

    Returns ``(contexts, row)`` pairs; ``row`` is the context ending at the end of
    the data (or one week earlier). Layouts: a single context; ``[y, y[:-1]]`` (the
    chapter-7 notebook's ``forecast_now``); the ``make_timesfm_cache.py --csv``
    layout (rolling origins, then the end of the series).
    """
    layouts: list[tuple[list[np.ndarray], int]] = []
    for drop in (0, 1):
        series = y[: len(y) - drop]
        last = len(series)
        if n == 1:
            layouts.append(([series], 0))
        if n == 2 and drop == 0:
            layouts.append(([y, y[:-1]], 0))
        back = n - 1
        origins = list(range(max(1, last - horizon - back + 1), last - horizon + 1)) + [last]
        if n > 1 and len(origins) == n:
            layouts.append(([series[:o] for o in origins], n - 1))
    return layouts


def load_forecast(data: dict[str, Any], cache_dir: Path = CACHE_DIR) -> dict[str, Any] | None:
    """Find a cached TimesFM forecast of the weeks after the data freeze.

    Only an entry whose input fingerprint (:func:`epi_learning.tsfm.input_fingerprint`)
    matches the weekly dengue series ending at its last week (or at the week
    before, if chapter 7 dropped the incomplete week) is used.

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.
    cache_dir : Path
        Folder of the committed caches (``ph*.json`` files are searched).

    Returns
    -------
    dict or None
        ``start`` (first forecast week), ``weeks`` (``wk``, ``start``, ``med``,
        ``lo``, ``hi`` = 10%, 50%, 90% quantiles), ``source``; ``None`` when no
        matching forecast exists.
    """
    try:
        from epi_learning.tsfm import input_fingerprint
    except ImportError:
        return None
    weekly = data["weekly"]
    y_full = weekly["cases"].to_numpy(dtype=float)
    for path in sorted(Path(cache_dir).glob("ph*.json")):
        try:
            entries = json.loads(path.read_text(encoding="utf-8")).get("entries", {})
        except (OSError, ValueError):
            continue
        for key in sorted(entries):
            entry = entries[key]
            shape = entry.get("shape") or []
            horizon = int(entry.get("horizon", 0))
            if len(shape) != 2 or horizon < 1:
                continue
            for contexts, row in _forecast_layouts(y_full, shape[0], horizon):
                if input_fingerprint(contexts, horizon) != entry.get("fingerprint"):
                    continue
                last = len(contexts[row])
                quant = np.asarray(entry["quantiles"], dtype=float)[row]
                median = np.asarray(entry["forecast"], dtype=float)[row]
                start = weekly["week_start"].iloc[last - 1].date()
                weeks = []
                for k in range(horizon):
                    day = start + dt.timedelta(weeks=k + 1)
                    weeks.append({"wk": f"W{day.isocalendar().week:02d}",
                                  "start": day.isoformat(),
                                  "med": round(max(0.0, float(median[k])), 1),
                                  "lo": round(max(0.0, float(quant[k, 0])), 1),
                                  "hi": round(max(0.0, float(quant[k, -1])), 1)})
                return {"weeks": weeks, "start": weeks[0]["wk"],
                        "dropped_last": last < len(y_full), "source": f"{path.name}:{key}"}
    return None


def project_geojson(geojson: dict[str, Any], width: float = 1000.0) -> dict[str, Any]:
    """Project barangay polygons to SVG coordinates (equirectangular, north up).

    Parameters
    ----------
    geojson : dict
        FeatureCollection of ``Polygon`` features in lon/lat.
    width : float
        Width of the SVG coordinate frame.

    Returns
    -------
    dict
        ``vb`` = ``[width, height]`` and ``features`` (``id``, ``d`` path,
        ``cx``, ``cy`` label point).
    """
    rings = [f["geometry"]["coordinates"][0] for f in geojson["features"]]
    lons = [p[0] for ring in rings for p in ring]
    lats = [p[1] for ring in rings for p in ring]
    k = math.cos(math.radians((min(lats) + max(lats)) / 2))
    scale = width / ((max(lons) - min(lons)) * k)
    height = (max(lats) - min(lats)) * scale

    def xy(p: list[float]) -> tuple[float, float]:
        return (round((p[0] - min(lons)) * k * scale, 1), round((max(lats) - p[1]) * scale, 1))

    features = []
    for f, ring in zip(geojson["features"], rings, strict=True):
        pts = [xy(p) for p in ring]
        d = "M" + "L".join(f"{x:g} {y:g}" for x, y in pts[:-1]) + "Z"
        cx = round(sum(x for x, _ in pts[:-1]) / (len(pts) - 1), 1)
        cy = round(sum(y for _, y in pts[:-1]) / (len(pts) - 1), 1)
        features.append({"id": f["properties"]["barangay_id"], "d": d, "cx": cx, "cy": cy})
    return {"vb": [width, round(height, 1)], "features": features}


def class_breaks(values: list[float], k: int = 5, decimals: int = 1) -> list[float]:
    """Quantile class breaks (``k - 1`` upper limits) for a choropleth.

    Parameters
    ----------
    values : list of float
        Published, non-zero values (withheld cells are left out).
    k : int
        Number of colour classes.
    decimals : int
        Rounding of the breaks.

    Returns
    -------
    list of float
        Strictly increasing upper limits of classes 1 .. k-1.
    """
    if k < 2:
        raise ValueError("k must be >= 2")
    vals = sorted(v for v in values if v is not None and v > 0)
    if not vals:
        return []
    raw = np.quantile(vals, [i / k for i in range(1, k)])
    breaks: list[float] = []
    for b in raw:
        b = round(float(b), decimals)
        if not breaks or b > breaks[-1]:
            breaks.append(b)
    return breaks


def _class_of(value: float | None, breaks: list[float]) -> int | str:
    if value is None:
        return "s"
    if value == 0:
        return 0
    for i, b in enumerate(breaks):
        if value <= b:
            return i + 1
    return len(breaks) + 1


# =============================================================================
# 5. Words (all UI strings in the three languages)
# =============================================================================

_MONTHS = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"],
    "fil": ["Ene", "Peb", "Mar", "Abr", "May", "Hun", "Hul", "Ago", "Set", "Okt", "Nob", "Dis"],
}
_MONTHS_LONG_FIL = ["Enero", "Pebrero", "Marso", "Abril", "Mayo", "Hunyo", "Hulyo", "Agosto",
                    "Setyembre", "Oktubre", "Nobyembre", "Disyembre"]


def format_date(day: dt.date, lang: str, year: bool = False) -> str:
    """Format a date for the page language (``18 Jul``, ``7 月 18 日``, ``18 Hul``).

    Parameters
    ----------
    day : datetime.date
        The date.
    lang : str
        ``"en"``, ``"zh"`` or ``"fil"``.
    year : bool
        Add the year (Filipino then uses the full month name).

    Returns
    -------
    str
    """
    if lang == "zh":
        return (f"{day.year} 年 " if year else "") + f"{day.month} 月 {day.day} 日"
    if lang == "fil" and year:
        return f"{day.day} {_MONTHS_LONG_FIL[day.month - 1]} {day.year}"
    if lang not in _MONTHS:
        raise ValueError(f"lang must be one of {LANGS}, got {lang!r}")
    return f"{day.day} {_MONTHS[lang][day.month - 1]}" + (f" {day.year}" if year else "")


def format_number(value: float, decimals: int = 0) -> str:
    """``1234.5`` -> ``"1,234.5"`` (the same in all three languages)."""
    return f"{value:,.{decimals}f}"


STRINGS: dict[str, dict[str, Any]] = {
    "en": {
        "page_title": "Bantay Santa Luz · outbreak dashboard",
        "kicker": "Bantay Santa Luz",
        "title": "Outbreak command centre",
        "subtitle": "Leptospirosis and dengue after Typhoon Amihan · Santa Luz City "
                    "Epidemiology and Surveillance Unit (CESU)",
        "as_of": "As of {date}",
        "as_of_note": "data freeze: every case reported by this date",
        "fiction": "Fictional city · synthetic teaching data",
        "skip": "Skip to the dashboard",
        "lang_label": "Language",
        "dark": "Dark",
        "theme_label": "Dark theme",
        "print": "Print",
        "to_chapter": "How it was built",
        "home": "Book home",
        "alert": "Dengue has been above the epidemic threshold for {n} weeks in a row, "
                 "since {week} (week of {date}).",
        "kpi_cases": "Cases", "kpi_cases_sub": "{lep} leptospirosis · {den} dengue",
        "kpi_deaths": "Deaths", "kpi_deaths_sub": "{lep} leptospirosis · {den} dengue",
        "kpi_cfr_lep": "CFR · leptospirosis", "kpi_cfr_den": "CFR · dengue",
        "kpi_cfr_sub": "{deaths} of {cases} cases died",
        "kpi_weeks": "Weeks above threshold", "kpi_weeks_sub": "dengue, {first} to {last}",
        "kpi_hosp": "Hospitalised", "kpi_hosp_sub": "{pct}% of all cases",
        "leptospirosis": "Leptospirosis", "dengue": "Dengue", "both": "Both",
        "show": "Show",
        "curve_title": "Epidemic curve",
        "curve_sub": "Cases by week of symptom onset, 2026 (ISO weeks, Monday to Sunday)",
        "curve_take": "Leptospirosis peaked in {lep_wk} ({lep_n} cases), the second week after "
                      "the flood. Dengue rose later and peaked in {den_wk} ({den_n}).",
        "typhoon": "Typhoon Amihan, {date}",
        "incomplete": "incomplete",
        "map_title": "Where: attack rate by barangay",
        "map_sub_rate": "Cases per 10,000 residents", "map_sub_count": "Number of cases",
        "rate": "Rate", "count": "Count", "measure": "Measure", "disease": "Disease",
        "map_take": "Leptospirosis hit the riverside barangays ({lep_river} per 10,000); "
                    "dengue hit the coast ({den_coast} per 10,000).",
        "map_hint": "Hover, tap or Tab to a barangay.",
        "map_fiction": "Invented map: Santa Luz is not a real place.",
        "thr_title": "Dengue against the epidemic threshold",
        "thr_sub": "Weekly cases, {first} to {last} 2026. Threshold = mean + 2 SD of the same "
                   "weeks in 2022–2025.",
        "thr_take": "Above the threshold since {first}. Last complete week, {wk}: {n} cases "
                    "against a threshold of {thr}.",
        "threshold": "Epidemic threshold",
        "above": "above the threshold",
        "fc_label": "TimesFM forecast (median, 80% range)",
        "fc_none": "Forecast not available in this build. Chapter 7 makes one.",
        "fc_note": "Forecast for the {n} weeks from {start}: TimesFM 3.0, replayed from a cached "
                   "run (non-commercial licence). It cannot see a new typhoon coming.",
        "pyr_title": "Who: age and sex", "pyr_sub": "Cases by age group and sex",
        "male": "Male", "female": "Female",
        "pyr_take": "Leptospirosis: mostly working-age men ({lep_m}% male, median age "
                    "{lep_age}). Dengue: children and young people (median age {den_age}).",
        "t717_title": "7-1-7 timeliness",
        "t717_sub": "{n} public-health events, {start} to {end}",
        "detect": "Detect ≤ 7 days", "notify": "Notify ≤ 1 day", "respond": "Respond ≤ 7 days",
        "all3": "All three met",
        "median_d": "median {n} d", "met_of": "{met} of {n} events",
        "bottlenecks": "Most common bottlenecks", "events": "{n} events",
        "forest_title": "What drove leptospirosis",
        "forest_sub": "Case-control study, {cases} cases and {controls} matched controls. Odds "
                      "ratio with 95% CI, log scale.",
        "forest_take": "Wading in floodwater: OR {or_w} ({or_adj} after adjusting for clean-up "
                       "work). Boots and doxycycline were protective.",
        "protective": "lower odds", "risk": "higher odds",
        "ex_waded": "Waded in floodwater",
        "ex_waded_adj": "Waded, adjusted for clean-up (M–H)",
        "ex_noboots": "Waded without boots",
        "ex_boots": "Wore boots (waders only)",
        "ex_doxy": "Doxycycline prophylaxis",
        "ex_wound": "Wound on legs or feet",
        "ex_cleanup": "Did clean-up work",
        "ex_male": "Male sex",
        "ex_rats": "Rats near home",
        "actions_title": "What to do this week",
        "actions_sub": "For the Local Health Board, {date}",
        "p_urgent": "Urgent", "p_week": "This week", "p_fix": "Fix the system",
        "a1_t": "Keep the dengue response going",
        "a1_b": "Highest dengue attack rates: {top}. Start 4S search-and-destroy with the BHWs "
                "in these barangays.",
        "a2_t": "Get hospitals ready for severe dengue",
        "a2_b": "So far {ws} cases with warning signs and {sev} with severe dengue. Check fluids "
                "and beds; teach families the warning signs.",
        "a3_t": "Read the last week with care",
        "a3_b": "{wk} is incomplete because of reporting delay. Judge the trend on complete "
                "weeks ({prev}: {prev_n}, {last}: {last_n}).",
        "a4_t": "Close the leptospirosis cluster",
        "a4_b": "No new onset since {date}: {days} days, longer than the longest leptospirosis "
                "incubation period (2–30 days, WHO). Write the close-out report; keep boots and doxycycline ready for the "
                "next flood.",
        "a5_t": "Fix the top 7-1-7 bottleneck",
        "a5_b": "Only {pct}% of events met all three targets. Most common bottleneck: {b}.",
        "a6_t": "Speed up leptospirosis lab results",
        "a6_b": "Median {days} days from consultation to confirmation at the reference lab.",
        "numbers": "Show the numbers",
        "week": "Week", "week_start": "Week starting", "cases": "Cases", "per10k": "per 10,000",
        "brgy": "Barangay", "band": "Band", "population": "Population",
        "riverside": "Riverside", "coastal": "Coastal", "upland": "Upland",
        "age_group": "Age group", "exposure": "Exposure", "or": "OR", "ci": "95% CI",
        "target": "Target", "met": "Met", "missed": "Missed", "median": "Median delay",
        "days_n": "{n} d",
        "unknown_age": "{n} cases with unknown age are not shown.",
        "unknown_onset": "Cases with no onset date are not shown.",
        "lt5_long": "1–4 cases: shown as <5, rate withheld",
        "x_long": "x = withheld so a small cell cannot be worked out from the totals",
        "zero": "no cases",
        "withheld": "withheld",
        "tip_rank": "rank {n} of 24",
        "notes_title": "Data notes and privacy",
        "notes": [
            ("<b>Synthetic data.</b> Santa Luz City, Typhoon Amihan, every barangay, person and "
            "number on this page are invented for the <i>Bantay Python</i> course. No real "
            "patient is described."),
            ("<b>Aggregates only.</b> No names, addresses, phone numbers, case IDs or exact "
            "dates of individual cases are on this page or inside its code."),
            ("<b>Small cells suppressed.</b> Whole-city totals for the whole period (the tiles "
            "at the top) are shown in full, as in routine bulletins. In every smaller cell (a "
            "week, a barangay, an age–sex group) a count of 1 to 4 is shown as “&lt;5” and its "
            "rate is withheld; “x” marks a cell withheld so that a small cell cannot be worked "
            "out from the totals."),
            ("<b>Definitions.</b> Cases are counted by week of symptom onset. Attack rate = "
            "cases ÷ barangay population × 10,000. Case fatality rate (CFR) = deaths ÷ cases. "
            "Epidemic threshold = mean + 2 standard deviations of the same week and its two "
            "neighbours in 2022–2025. 7-1-7 = detect within 7 days of emergence, notify within "
            "1 day, complete the early response within 7 days."),
            ("<b>Reporting delay.</b> The line list holds cases reported to the CESU by the data "
            "freeze, so the most recent week is incomplete."),
        ],
        "footer": "Built with Python in chapter 9 of <i>Bantay Python — Epi With Python, "
                  "Philippines Edition</i>.",
        "noscript": "The charts need JavaScript. Every number is also in the “Show the "
                    "numbers” tables.",
        "or_ci": "OR {or} (95% CI {lo}–{hi})",
        "week_of": "week of {date}",
        "bottleneck_text": {},
    },
    "zh": {
        "page_title": "Bantay Santa Luz · 疫情儀表板",
        "kicker": "Bantay Santa Luz",
        "title": "疫情指揮中心",
        "subtitle": "颱風 Amihan 過後的鉤端螺旋體病與登革熱 · Santa Luz 市流行病學與監測單位（CESU）",
        "as_of": "資料截至 {date}",
        "as_of_note": "資料凍結：收錄此日前通報的所有病例",
        "fiction": "虛構城市 · 教學用合成資料",
        "skip": "跳到儀表板",
        "lang_label": "語言",
        "dark": "深色",
        "theme_label": "深色主題",
        "print": "列印",
        "to_chapter": "製作方法",
        "home": "回到課本",
        "alert": "登革熱已連續 {n} 週高於流行閾值，自 {week}（{date} 當週）起。",
        "kpi_cases": "病例數", "kpi_cases_sub": "鉤端螺旋體病 {lep} · 登革熱 {den}",
        "kpi_deaths": "死亡數", "kpi_deaths_sub": "鉤端螺旋體病 {lep} · 登革熱 {den}",
        "kpi_cfr_lep": "致死率 · 鉤端螺旋體病", "kpi_cfr_den": "致死率 · 登革熱",
        "kpi_cfr_sub": "{cases} 例中 {deaths} 例死亡",
        "kpi_weeks": "高於閾值的週數", "kpi_weeks_sub": "登革熱，{first} 至 {last}",
        "kpi_hosp": "住院", "kpi_hosp_sub": "占全部病例 {pct}%",
        "leptospirosis": "鉤端螺旋體病", "dengue": "登革熱", "both": "兩者",
        "show": "顯示",
        "curve_title": "流行曲線",
        "curve_sub": "依發病週的病例數，2026 年（ISO 週，週一至週日）",
        "curve_take": "鉤端螺旋體病在 {lep_wk} 達到高峰（{lep_n} 例），即淹水後第二週；登革熱較晚上升，"
                      "於 {den_wk} 達到高峰（{den_n} 例）。",
        "typhoon": "颱風 Amihan，{date}",
        "incomplete": "資料未齊",
        "map_title": "地點：各 barangay 的侵襲率",
        "map_sub_rate": "每 10,000 名居民病例數", "map_sub_count": "病例數",
        "rate": "侵襲率", "count": "病例數", "measure": "指標", "disease": "疾病",
        "map_take": "鉤端螺旋體病集中在沿河各 barangay（每 10,000 人 {lep_river}）；登革熱集中在沿海（每 10,000 人 {den_coast}）。",
        "map_hint": "滑過、點選或按 Tab 選擇一個 barangay。",
        "map_fiction": "虛構地圖：Santa Luz 並非真實地點。",
        "thr_title": "登革熱與流行閾值",
        "thr_sub": "每週病例數，2026 年 {first} 至 {last}。閾值 = 2022–2025 年同期各週的平均值 + 2 個標準差。",
        "thr_take": "自 {first} 起高於閾值。最後一個完整週 {wk}：{n} 例，閾值 {thr}。",
        "threshold": "流行閾值",
        "above": "高於閾值",
        "fc_label": "TimesFM 預測（中位數、80% 區間）",
        "fc_none": "本次建置沒有預測資料，第 07 章會產生預測。",
        "fc_note": "自 {start} 起 {n} 週的預測：TimesFM 3.0，重播先前執行的快取結果（非商業授權）。模型看不見即將到來的新颱風。",
        "pyr_title": "人：年齡與性別", "pyr_sub": "依年齡組與性別的病例數",
        "male": "男", "female": "女",
        "pyr_take": "鉤端螺旋體病：以工作年齡男性為主（男性 {lep_m}%，年齡中位數 {lep_age} 歲）。"
                    "登革熱：以兒童與年輕人為主（年齡中位數 {den_age} 歲）。",
        "t717_title": "7-1-7 時效",
        "t717_sub": "{n} 起公共衛生事件，{start} 至 {end}",
        "detect": "偵測 ≤ 7 天", "notify": "通報 ≤ 1 天", "respond": "應變 ≤ 7 天",
        "all3": "三項皆達成",
        "median_d": "中位數 {n} 天", "met_of": "{n} 起中 {met} 起",
        "bottlenecks": "最常見的瓶頸", "events": "{n} 起",
        "forest_title": "鉤端螺旋體病的危險因子",
        "forest_sub": "病例對照研究：{cases} 名病例、{controls} 名配對對照。勝算比與 95% 信賴區間（對數尺度）。",
        "forest_take": "涉入洪水：勝算比 {or_w}（校正清理工作的干擾後為 {or_adj}）。穿雨鞋與預防性服用"
                       "doxycycline 具保護作用。",
        "protective": "勝算較低", "risk": "勝算較高",
        "ex_waded": "涉入洪水",
        "ex_waded_adj": "涉入洪水，校正清理工作（M–H）",
        "ex_noboots": "涉水未穿雨鞋",
        "ex_boots": "穿雨鞋（僅涉水者）",
        "ex_doxy": "預防性服用 doxycycline",
        "ex_wound": "腿或腳有傷口",
        "ex_cleanup": "參與災後清理",
        "ex_male": "男性",
        "ex_rats": "住家附近有老鼠",
        "actions_title": "本週該做的事",
        "actions_sub": "提交地方衛生委員會，{date}",
        "p_urgent": "緊急", "p_week": "本週", "p_fix": "改善系統",
        "a1_t": "持續登革熱防治應變",
        "a1_b": "登革熱侵襲率最高的 barangay：{top}。請與村里衛生員（BHW）在這些 barangay 優先執行 4S 孳生源清除。",
        "a2_t": "讓醫院準備好收治重症登革熱",
        "a2_b": "目前有警示徵象者 {ws} 例、重症 {sev} 例。確認輸液與病床；教導家屬認識警示徵象。",
        "a3_t": "謹慎解讀最後一週",
        "a3_b": "{wk} 因通報延遲而資料未齊。請以完整週判斷趨勢（{prev}：{prev_n}，{last}：{last_n}）。",
        "a4_t": "結束鉤端螺旋體病群聚",
        "a4_b": "自 {date} 起沒有新的發病：已 {days} 天，超過鉤端螺旋體病最長的潛伏期（2–30 天，WHO）。撰寫結案報告；為下一次淹水備妥雨鞋與 doxycycline。",
        "a5_t": "改善 7-1-7 最大的瓶頸",
        "a5_b": "只有 {pct}% 的事件三項目標皆達成。最常見的瓶頸：{b}。",
        "a6_t": "加快鉤端螺旋體病的檢驗結果",
        "a6_b": "從就醫到參考實驗室確診的中位數為 {days} 天。",
        "numbers": "顯示數字",
        "week": "週", "week_start": "週起始日", "cases": "病例數", "per10k": "每 10,000 人",
        "brgy": "barangay", "band": "區帶", "population": "人口",
        "riverside": "沿河", "coastal": "沿海", "upland": "山區",
        "age_group": "年齡組", "exposure": "暴露", "or": "勝算比", "ci": "95% 信賴區間",
        "target": "目標", "met": "達成", "missed": "未達成", "median": "延遲中位數",
        "days_n": "{n} 天",
        "unknown_age": "另有 {n} 名年齡不詳的病例未列入。",
        "unknown_onset": "發病日不詳的病例未列入。",
        "lt5_long": "1–4 例：顯示為 <5，不列侵襲率",
        "x_long": "x = 為避免由總數推算出小格而遮蔽",
        "zero": "無病例",
        "withheld": "不公開",
        "tip_rank": "24 個 barangay 中排名第 {n}",
        "notes_title": "資料說明與隱私",
        "notes": [
            ("<b>合成資料。</b>Santa Luz 市、颱風 Amihan，以及本頁的每一個 barangay、每一個人與每一個數字，"
            "都是為 <i>Bantay Python</i> 課程虛構的，不描述任何真實病人。"),
            "<b>只呈現彙總資料。</b>本頁與其程式碼中沒有姓名、地址、電話、病例編號，也沒有個別病例的確切日期。",
            ("<b>小格遮蔽。</b>全市全期間的總數（上方的數字方塊）如例行疫情報告一樣完整呈現。"
            "其他較小的格子（某一週、某一個 barangay、某一年齡性別組）若為 1 至 4 例，顯示為「&lt;5」且不列侵襲率；"
            "「x」表示為避免由總數推算出小格而一併遮蔽的格子。"),
            ("<b>定義。</b>病例依發病週計算。侵襲率 = 病例數 ÷ 該 barangay（描籠涯，菲律賓最基層的行政區，類似台灣的村里）人口 × 10,000。致死率 = 死亡數 ÷ 病例數。"
            "流行閾值 = 2022–2025 年同一週及其前後兩週的平均值 + 2 個標準差。"
            "7-1-7 = 事件出現後 7 天內偵測、偵測後 1 天內通報、通報後 7 天內完成早期應變。"),
            "<b>通報延遲。</b>造冊（line list）只收錄資料凍結日前通報至 CESU 的病例，因此最近一週的資料尚未齊全。",
        ],
        "footer": "以 Python 製作於 <i>Bantay Python — Epi With Python 菲律賓特別版</i>第 09 章。",
        "noscript": "圖表需要 JavaScript。所有數字也都列在「顯示數字」的表格中。",
        "or_ci": "勝算比 {or}（95% 信賴區間 {lo}–{hi}）",
        "week_of": "{date} 當週",
        "bottleneck_text": {
            "Cases seen at a private clinic that is not yet a PIDSR disease reporting unit":
                "病例在尚未成為 PIDSR 通報單位的私人診所就診",
            "competing priorities": "其他業務排擠",
            "One DSO for 24 barangays": "一位疾病監測專員（DSO）負責 24 個 barangay",
            "BHW noticed the cluster but had no load to text the CESU":
                "BHW 發現群聚，但手機沒有儲值，無法傳簡訊給 CESU",
            "PESU learned of it days later": "PESU 數天後才得知",
            "Notified by personal chat message, not logged": "以私人聊天訊息通報，未登錄",
        },
    },
    "fil": {
        "page_title": "Bantay Santa Luz · dashboard ng outbreak",
        "kicker": "Bantay Santa Luz",
        "title": "Command centre ng outbreak",
        "subtitle": "Leptospirosis at dengue pagkatapos ng Bagyong Amihan · Santa Luz City "
                    "Epidemiology and Surveillance Unit (CESU)",
        "as_of": "Datos hanggang {date}",
        "as_of_note": "data freeze: lahat ng kasong naiulat hanggang sa petsang ito",
        "fiction": "Kathang-isip na lungsod · synthetic na datos para sa pagsasanay",
        "skip": "Lumaktaw sa dashboard",
        "lang_label": "Wika",
        "dark": "Madilim",
        "theme_label": "Madilim na tema",
        "print": "I-print",
        "to_chapter": "Paano ito ginawa",
        "home": "Bumalik sa aklat",
        "alert": "Lampas sa epidemic threshold ang dengue nang {n} sunod-sunod na linggo, mula "
                 "{week} (linggo ng {date}).",
        "kpi_cases": "Kaso", "kpi_cases_sub": "{lep} leptospirosis · {den} dengue",
        "kpi_deaths": "Namatay", "kpi_deaths_sub": "{lep} leptospirosis · {den} dengue",
        "kpi_cfr_lep": "CFR · leptospirosis", "kpi_cfr_den": "CFR · dengue",
        "kpi_cfr_sub": "{deaths} sa {cases} kaso ang namatay",
        "kpi_weeks": "Linggong lampas sa threshold",
        "kpi_weeks_sub": "dengue, {first} hanggang {last}",
        "kpi_hosp": "Na-ospital", "kpi_hosp_sub": "{pct}% ng lahat ng kaso",
        "leptospirosis": "Leptospirosis", "dengue": "Dengue", "both": "Pareho",
        "show": "Ipakita",
        "curve_title": "Epidemic curve",
        "curve_sub": "Mga kaso ayon sa linggo ng pagsisimula ng sintomas, 2026 (ISO week, "
                     "Lunes hanggang Linggo)",
        "curve_take": "Umabot sa rurok ang leptospirosis noong {lep_wk} ({lep_n} kaso), ang "
                      "ikalawang linggo matapos ang baha. Mas huling tumaas ang dengue at "
                      "umabot sa rurok noong {den_wk} ({den_n}).",
        "typhoon": "Bagyong Amihan, {date}",
        "incomplete": "kulang pa",
        "map_title": "Saan: attack rate bawat barangay",
        "map_sub_rate": "Kaso bawat 10,000 residente", "map_sub_count": "Bilang ng kaso",
        "rate": "Rate", "count": "Bilang", "measure": "Sukatan", "disease": "Sakit",
        "map_take": "Tinamaan ng leptospirosis ang mga barangay sa tabing-ilog ({lep_river} "
                    "bawat 10,000); ang dengue, ang baybayin ({den_coast} bawat 10,000).",
        "map_hint": "I-hover, i-tap o mag-Tab sa isang barangay.",
        "map_fiction": "Kathang-isip na mapa: hindi totoong lugar ang Santa Luz.",
        "thr_title": "Dengue laban sa epidemic threshold",
        "thr_sub": "Lingguhang kaso, {first} hanggang {last} 2026. Threshold = mean + 2 SD ng "
                   "parehong mga linggo noong 2022–2025.",
        "thr_take": "Lampas sa threshold mula {first}. Huling kumpletong linggo, {wk}: {n} kaso "
                    "laban sa threshold na {thr}.",
        "threshold": "Epidemic threshold",
        "above": "lampas sa threshold",
        "fc_label": "TimesFM forecast (median, 80% range)",
        "fc_none": "Walang forecast sa build na ito. Gumagawa nito ang kabanata 7.",
        "fc_note": "Forecast para sa {n} linggo mula {start}: TimesFM 3.0, mula sa naka-cache na "
                   "run (non-commercial na lisensya). Hindi nito nakikita ang paparating na "
                   "bagong bagyo.",
        "pyr_title": "Sino: edad at kasarian", "pyr_sub": "Mga kaso ayon sa age group at kasarian",
        "male": "Lalaki", "female": "Babae",
        "pyr_take": "Leptospirosis: karamihan ay lalaking nasa edad ng paghahanapbuhay "
                    "({lep_m}% lalaki, median na edad {lep_age}). Dengue: mga bata at kabataan "
                    "(median na edad {den_age}).",
        "t717_title": "7-1-7 timeliness",
        "t717_sub": "{n} public-health event, {start} hanggang {end}",
        "detect": "Detect ≤ 7 araw", "notify": "Notify ≤ 1 araw", "respond": "Respond ≤ 7 araw",
        "all3": "Pasado sa tatlo",
        "median_d": "median {n} araw", "met_of": "{met} sa {n} event",
        "bottlenecks": "Pinakamadalas na bottleneck", "events": "{n} event",
        "forest_title": "Ano ang nagpataas ng leptospirosis",
        "forest_sub": "Case-control study, {cases} kaso at {controls} matched control. Odds "
                      "ratio na may 95% CI, log scale.",
        "forest_take": "Paglusong sa baha: OR {or_w} ({or_adj} matapos i-adjust sa clean-up "
                       "work). Protektado ang may bota at ang uminom ng doxycycline.",
        "protective": "mas mababang odds", "risk": "mas mataas na odds",
        "ex_waded": "Lumusong sa baha",
        "ex_waded_adj": "Lumusong, adjusted sa clean-up (M–H)",
        "ex_noboots": "Lumusong nang walang bota",
        "ex_boots": "Nakabota (mga lumusong lang)",
        "ex_doxy": "Doxycycline prophylaxis",
        "ex_wound": "May sugat sa binti o paa",
        "ex_cleanup": "Sumama sa clean-up",
        "ex_male": "Lalaki",
        "ex_rats": "May daga malapit sa bahay",
        "actions_title": "Gagawin ngayong linggo",
        "actions_sub": "Para sa Local Health Board, {date}",
        "p_urgent": "Agaran", "p_week": "Ngayong linggo", "p_fix": "Ayusin ang sistema",
        "a1_t": "Ituloy ang dengue response",
        "a1_b": "Pinakamataas ang dengue attack rate sa {top}. Simulan ang 4S search-and-destroy "
                "kasama ang mga BHW sa mga barangay na ito.",
        "a2_t": "Ihanda ang mga ospital sa severe dengue",
        "a2_b": "Sa ngayon, {ws} kaso ang may warning signs at {sev} ang severe dengue. Suriin "
                "ang IV fluids at kama; ituro sa pamilya ang mga warning sign.",
        "a3_t": "Mag-ingat sa pagbasa ng huling linggo",
        "a3_b": "Kulang pa ang {wk} dahil sa reporting delay. Tingnan ang trend sa mga "
                "kumpletong linggo ({prev}: {prev_n}, {last}: {last_n}).",
        "a4_t": "Isara ang leptospirosis cluster",
        "a4_b": "Walang bagong kaso mula {date}: {days} araw na, lampas sa pinakamahabang incubation period "
                "ng leptospirosis (2–30 araw, WHO). Isulat ang close-out report; ihanda ang bota at doxycycline "
                "para sa susunod na baha.",
        "a5_t": "Ayusin ang pinakamalaking 7-1-7 bottleneck",
        "a5_b": "{pct}% lang ng mga event ang pumasa sa tatlong target. Pinakamadalas na "
                "bottleneck: {b}.",
        "a6_t": "Pabilisin ang lab result ng leptospirosis",
        "a6_b": "Median na {days} araw mula konsulta hanggang kumpirmasyon sa reference lab.",
        "numbers": "Ipakita ang mga numero",
        "week": "Linggo", "week_start": "Simula ng linggo", "cases": "Kaso",
        "per10k": "bawat 10,000",
        "brgy": "Barangay", "band": "Lugar", "population": "Populasyon",
        "riverside": "Tabing-ilog", "coastal": "Baybayin", "upland": "Kabundukan",
        "age_group": "Age group", "exposure": "Exposure", "or": "OR", "ci": "95% CI",
        "target": "Target", "met": "Pasado", "missed": "Hindi pasado",
        "median": "Median na delay", "days_n": "{n} araw",
        "unknown_age": "Hindi kasama ang {n} kasong walang edad.",
        "unknown_onset": "Hindi kasama ang mga kasong walang petsa ng onset.",
        "lt5_long": "1–4 kaso: ipinapakitang <5, walang rate",
        "x_long": "x = itinago para hindi makuwenta ang maliit na cell mula sa kabuuan",
        "zero": "walang kaso",
        "withheld": "itinago",
        "tip_rank": "ika-{n} sa 24",
        "notes_title": "Mga tala sa datos at privacy",
        "notes": [
            ("<b>Synthetic na datos.</b> Kathang-isip ang Santa Luz City, ang Bagyong Amihan, at "
            "bawat barangay, tao at numero sa pahinang ito, para sa kursong <i>Bantay "
            "Python</i>. Walang totoong pasyenteng inilalarawan."),
            ("<b>Aggregate lang.</b> Walang pangalan, address, numero ng telepono, case ID o "
            "eksaktong petsa ng isang kaso sa pahinang ito o sa code nito."),
            ("<b>Itinatago ang maliliit na cell.</b> Buo ang kabuuan ng buong lungsod para sa "
            "buong panahon (ang mga tile sa itaas), gaya ng sa karaniwang bulletin. Sa bawat "
            "mas maliit na cell (isang linggo, isang barangay, isang age–sex group), ang bilang "
            "na 1 hanggang 4 ay ipinapakitang “&lt;5” at walang rate; ang “x” ay cell na "
            "itinago para hindi makuwenta ang maliit na cell mula sa kabuuan."),
            ("<b>Mga depinisyon.</b> Binibilang ang kaso ayon sa linggo ng onset. Attack rate = "
            "kaso ÷ populasyon ng barangay × 10,000. Case fatality rate (CFR) = namatay ÷ kaso. "
            "Epidemic threshold = mean + 2 standard deviation ng parehong linggo at ng dalawang "
            "katabi nito noong 2022–2025. 7-1-7 = ma-detect sa loob ng 7 araw, ma-notify sa "
            "loob ng 1 araw, matapos ang early response sa loob ng 7 araw."),
            ("<b>Reporting delay.</b> Ang line list ay may mga kasong naiulat sa CESU hanggang sa "
            "data freeze, kaya kulang pa ang pinakahuling linggo."),
        ],
        "footer": "Ginawa gamit ang Python sa kabanata 9 ng <i>Bantay Python — Epi With Python, "
                  "Philippines Edition</i>.",
        "noscript": "Kailangan ng JavaScript ang mga chart. Nasa mga talaang “Ipakita ang mga "
                    "numero” ang lahat ng numero.",
        "or_ci": "OR {or} (95% CI {lo}–{hi})",
        "week_of": "linggo ng {date}",
        "bottleneck_text": {
            "Cases seen at a private clinic that is not yet a PIDSR disease reporting unit":
                "Nagpatingin ang mga kaso sa pribadong klinikang hindi pa disease reporting "
                "unit ng PIDSR",
            "competing priorities": "Maraming sabay-sabay na trabaho",
            "One DSO for 24 barangays": "Iisang DSO para sa 24 na barangay",
            "BHW noticed the cluster but had no load to text the CESU":
                "Napansin ng BHW ang cluster pero walang load para i-text ang CESU",
            "PESU learned of it days later": "Ilang araw bago nalaman ng PESU",
            "Notified by personal chat message, not logged":
                "Na-notify sa personal na chat, hindi naitala",
        },
    },
}


def _t(lang: str, key: str, **params: Any) -> str:
    """Look up a UI string and fill in its ``{placeholders}``."""
    text = STRINGS[lang][key]
    return text.format(**params) if params else text


def _bottleneck(lang: str, text: str) -> str:
    return STRINGS[lang]["bottleneck_text"].get(text, text)


# =============================================================================
# 6. Payload: everything the page shows, already aggregated and suppressed
# =============================================================================


def action_items(data: dict[str, Any], kpis: dict[str, Any], lang: str) -> list[dict[str, str]]:
    """The "what to do this week" list, written from the numbers.

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.
    kpis : dict
        Output of :func:`compute_kpis`.
    lang : str
        Page language.

    Returns
    -------
    list of dict
        ``priority`` (``urgent`` | ``week`` | ``fix``), ``title``, ``body``.
    """
    brgy = barangay_table(data)
    top = (brgy.dropna(subset=["dengue_rate"]).sort_values("dengue_rate", ascending=False)
           .head(3))
    top_text = ", ".join(f"{r.barangay} ({format_number(r.dengue_rate, 1)})"
                         for r in top.itertuples())
    thr = threshold_series(data)["weeks"]
    last, prev, prev2 = thr[-1], thr[-2], thr[-3]
    t717 = timeliness_717(data)
    items = [
        ("urgent", "a1", {"top": top_text}),
        ("urgent", "a2", {"ws": kpis["dengue_warning"], "sev": kpis["dengue_severe"]}),
        ("week", "a3", {"wk": last["wk"], "prev": prev2["wk"], "prev_n": prev2["cell"][0],
                        "last": prev["wk"], "last_n": prev["cell"][0]}),
        ("week", "a4", {"date": format_date(kpis["last_lepto_onset"], lang),
                        "days": kpis["days_since_lepto"]}),
        ("fix", "a5", {"pct": format_number(t717["all"]["pct"]),
                       "b": "“" + _bottleneck(lang, t717["bottlenecks"][0]["text"]) + "”"}),
        ("fix", "a6", {"days": kpis["lab_median_days"]["leptospirosis"]}),
    ]
    return [{"priority": p, "title": _t(lang, f"{key}_t"), "body": _t(lang, f"{key}_b", **kw)}
            for p, key, kw in items]


def build_payload(data: dict[str, Any], lang: str, cache_dir: Path = CACHE_DIR
                  ) -> dict[str, Any]:
    """Assemble every number and string the page needs (aggregated, suppressed).

    Parameters
    ----------
    data : dict
        Output of :func:`load_data`.
    lang : str
        ``"en"``, ``"zh"`` or ``"fil"``.
    cache_dir : Path
        Where to look for a cached TimesFM forecast.

    Returns
    -------
    dict
        JSON-serialisable; embedded in the page as ``<script type="application/json">``.
    """
    if lang not in LANGS:
        raise ValueError(f"lang must be one of {LANGS}, got {lang!r}")
    kpis = compute_kpis(data)
    curve = epi_curve(data)
    thr = threshold_series(data)
    brgy = barangay_table(data)
    shapes = project_geojson(data["geojson"])
    names = brgy["barangay"].to_dict()
    features = []
    for f in shapes["features"]:
        row = brgy.loc[f["id"]]
        features.append({**f, "name": names[f["id"]], "band": row["band"],
                         "pop": int(row["population"]),
                         **{d: {"cell": row[f"{d}_cell"], "rate": row[f"{d}_rate"]}
                            for d in DISEASES}})
    breaks: dict[str, dict[str, list[float]]] = {}
    for d in DISEASES:
        rates = [x[d]["rate"] for x in features]
        counts = [x[d]["cell"][0] for x in features]
        breaks[d] = {"rate": class_breaks(rates), "count": class_breaks(counts, decimals=0)}
        published = [x for x in features if x[d]["rate"] is not None]
        by_rate = sorted(published, key=lambda x: (-x[d]["rate"], x["id"]))
        by_count = sorted(published, key=lambda x: (-x[d]["cell"][0], x["id"]))
        rank_rate = {x["id"]: i + 1 for i, x in enumerate(by_rate)}
        rank_count = {x["id"]: i + 1 for i, x in enumerate(by_count)}
        for x in features:
            x[d]["cls_rate"] = _class_of(x[d]["rate"], breaks[d]["rate"])
            x[d]["cls_count"] = _class_of(x[d]["cell"][0], breaks[d]["count"])
            x[d]["rank_rate"] = rank_rate.get(x["id"])
            x[d]["rank_count"] = rank_count.get(x["id"])
    pyramid = {d: {s: age_sex_table(data, d)[s].tolist() for s in ("M", "F")}
               for d in DISEASES}
    forecast = load_forecast(data, cache_dir)
    t717 = timeliness_717(data)
    t = STRINGS[lang]
    js_keys = ["leptospirosis", "dengue", "both", "typhoon", "incomplete", "threshold", "above",
               "fc_label", "male", "female", "zero", "withheld", "per10k", "cases",
               "population", "tip_rank", "or_ci", "week_of", "protective", "risk",
               "lt5_long", "x_long", "map_sub_rate", "map_sub_count", "riverside", "coastal",
               "upland", "rate", "count", "median_d", "met_of", "curve_title", "thr_title",
               "pyr_title", "forest_title"]
    strings = {k: t[k] for k in js_keys}
    strings["typhoon"] = _t(lang, "typhoon", date=format_date(TYPHOON, lang))
    strings.update({f"ex_{r['key']}": t[f"ex_{r['key']}"] for r in case_control_ors(data)})
    return {
        "lang": lang,
        "as_of": AS_OF.isoformat(),
        "typhoon": TYPHOON.isoformat(),
        "months": _MONTHS.get(lang, _MONTHS["en"]),
        "kpis": _jsonable(kpis),
        "curve": curve,
        "thr": thr,
        "forecast": forecast,
        "map": {"vb": shapes["vb"], "features": features, "breaks": breaks},
        "bands": band_rates(data),
        "pyramid": {"groups": list(AGE_GROUPS), **pyramid},
        "forest": case_control_ors(data),
        "cc_n": {"cases": int((data["case_control"]["case"] == 1).sum()),
                 "controls": int((data["case_control"]["case"] == 0).sum())},
        "t717": _jsonable({**t717, "bottlenecks": [
            {**b, "label": _bottleneck(lang, b["text"])} for b in t717["bottlenecks"]]}),
        "actions": action_items(data, kpis, lang),
        "t": strings,
    }


def _jsonable(value: Any) -> Any:
    """Turn dates and NumPy scalars into JSON-friendly values (recursively)."""
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, np.generic):
        return value.item()
    return value


# =============================================================================
# 7. HTML
# =============================================================================


def _esc(text: Any) -> str:
    return html.escape(str(text), quote=True)


def _show_cell(cell: list[Any]) -> str:
    """Text of one published cell: the count, ``<5`` or ``x``."""
    value, code = cell
    return format_number(value) if code == 0 else ("<5" if code == 1 else "x")


def _table(headers: list[str], rows: list[list[str]], caption: str, cls: str = "") -> str:
    head = "".join(f'<th scope="col">{_esc(h)}</th>' for h in headers)
    body = "".join("<tr>" + "".join(
        (f'<th scope="row">{_esc(c)}</th>' if i == 0 else f"<td>{_esc(c)}</td>")
        for i, c in enumerate(r)) + "</tr>" for r in rows)
    return (f'<table class="num-table {cls}"><caption>{_esc(caption)}</caption>'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")


def _details(lang: str, inner: str, note: str = "") -> str:
    extra = f'<p class="tnote">{note}</p>' if note else ""
    return (f'<details class="numbers"><summary>{_esc(_t(lang, "numbers"))}</summary>'
            f'<div class="tscroll">{inner}</div>{extra}</details>')


def _seg(lang: str, key: str, label: str, options: list[tuple[str, str]], current: str) -> str:
    buttons = "".join(
        f'<button type="button" data-k="{key}" data-v="{v}" '
        f'aria-pressed="{"true" if v == current else "false"}">{_esc(text)}</button>'
        for v, text in options)
    return f'<div class="seg" role="group" aria-label="{_esc(label)}">{buttons}</div>'


def _panel(pid: str, title: str, sub: str, body: str, take: str = "", controls: str = "",
           extra_cls: str = "", sub_id: str = "") -> str:
    sub_attr = f' id="{sub_id}"' if sub_id else ""
    take_html = f'<p class="take">{take}</p>' if take else ""
    return (f'<section class="panel {extra_cls}" id="{pid}" aria-labelledby="{pid}-h">'
            f'<header class="ph"><div><h2 id="{pid}-h">{_esc(title)}</h2>'
            f'<p class="sub"{sub_attr}>{_esc(sub)}</p></div>{controls}</header>'
            f"{take_html}{body}</section>")


def _kpi(label: str, value: float, sub: str, tone: str, decimals: int = 0,
         suffix: str = "") -> str:
    shown = format_number(value, decimals) + suffix
    return (f'<div class="kpi kpi-{tone}"><p class="kpi-label">{_esc(label)}</p>'
            f'<p class="kpi-val" data-n="{value}" data-dec="{decimals}" '
            f'data-suffix="{_esc(suffix)}">{shown}</p>'
            f'<p class="kpi-sub">{_esc(sub)}</p></div>')


def _sun_svg(cls: str) -> str:
    rays = []
    for i in range(8):
        a = math.radians(i * 45)
        tip = (round(48 * math.sin(a), 2), round(-48 * math.cos(a), 2))
        left = (round(14 * math.sin(a - 0.32), 2), round(-14 * math.cos(a - 0.32), 2))
        right = (round(14 * math.sin(a + 0.32), 2), round(-14 * math.cos(a + 0.32), 2))
        rays.append(f"M{left[0]} {left[1]}L{tip[0]} {tip[1]}L{right[0]} {right[1]}Z")
    return (f'<svg class="{cls}" viewBox="-50 -50 100 100" aria-hidden="true" focusable="false">'
            f'<path d="{"".join(rays)}"/><circle r="17"/></svg>')


def _gauge_svg(pct: float, tone: str) -> str:
    """Static 270-degree ring gauge (drawn in Python so it prints without JS)."""
    r, length = 40.0, 2 * math.pi * 40.0 * 0.75
    filled = round(length * pct / 100, 2)
    return (f'<svg class="gauge g-{tone}" viewBox="0 0 100 100" aria-hidden="true" '
            f'focusable="false"><g transform="rotate(135 50 50)">'
            f'<circle class="g-track" cx="50" cy="50" r="{r:g}" '
            f'stroke-dasharray="{length:.2f} 999"/>'
            f'<circle class="g-fill" cx="50" cy="50" r="{r:g}" '
            f'stroke-dasharray="{filled} 999" style="--len:{length:.2f}"/></g>'
            f'<text x="50" y="56" class="g-val">{pct:g}%</text></svg>')


def _tone(pct: float) -> str:
    return "good" if pct >= 80 else "mid" if pct >= 60 else "bad"


def render_html(payload: dict[str, Any]) -> str:
    """Render the complete, self-contained dashboard page.

    Parameters
    ----------
    payload : dict
        Output of :func:`build_payload`.

    Returns
    -------
    str
        The HTML document (inline CSS, JS and data; no external resources).
    """
    lang = payload["lang"]
    t = STRINGS[lang]
    k = payload["kpis"]
    as_of = dt.date.fromisoformat(payload["as_of"])
    lep, den = "leptospirosis", "dengue"
    first_above = k["first_above"].split("-")[1]
    last_week = k["last_week"].split("-")[1]

    def lang_link(code: str) -> str:
        current = ' class="lang is-current" aria-current="page"' if code == lang else ' class="lang"'
        return (f'<a{current} href="{_LANG_LINKS[lang][code]}" hreflang="{_HTML_LANG[code]}" '
                f'lang="{_HTML_LANG[code]}">{_LANG_NAMES[code]}</a>')

    langs = "".join(lang_link(code) for code in LANGS)
    header = (
        f'<a class="skip" href="#main">{_esc(t["skip"])}</a>'
        '<div class="flagbar" aria-hidden="true"></div>'
        '<header class="top"><div class="sign">'
        f'{_sun_svg("sun")}'
        f'<div class="sign-text"><p class="kicker">{_esc(t["kicker"])}</p>'
        f'<h1>{_esc(t["title"])}</h1><p class="subtitle">{_esc(t["subtitle"])}</p></div>'
        '<div class="sign-side">'
        f'<p class="asof"><span class="dot" aria-hidden="true"></span>'
        f'<span><b>{_esc(_t(lang, "as_of", date=format_date(as_of, lang, year=True)))}</b>'
        f'<small>{_esc(t["as_of_note"])}</small></span></p>'
        f'<p class="fiction">{_esc(t["fiction"])}</p></div></div>'
        '<nav class="tools" aria-label="Bantay Santa Luz">'
        f'<div class="langs" role="group" aria-label="{_esc(t["lang_label"])}">{langs}</div>'
        f'<button type="button" class="tool" id="theme" aria-pressed="false" '
        f'aria-label="{_esc(t["theme_label"])}"><span aria-hidden="true" class="ico-moon"></span>'
        f'{_esc(t["dark"])}</button>'
        f'<button type="button" class="tool" id="print">{_esc(t["print"])}</button>'
        f'<a class="tool" href="../chapters/dashboard/">{_esc(t["to_chapter"])}</a>'
        f'<a class="tool" href="../">{_esc(t["home"])}</a>'
        "</nav></header>"
        '<div class="bunting" aria-hidden="true"></div>'
    )

    alert = ""
    if k["weeks_above"]:
        alert = ('<p class="alert" role="status"><span class="pulse" aria-hidden="true"></span>'
                 + _esc(_t(lang, "alert", n=k["weeks_above"], week=first_above,
                           date=format_date(dt.date.fromisoformat(k["first_above_start"]),
                                            lang)))
                 + "</p>")

    kpis = "".join([
        _kpi(t["kpi_cases"], k["cases"]["total"],
             _t(lang, "kpi_cases_sub", lep=k["cases"][lep], den=k["cases"][den]), "blue"),
        _kpi(t["kpi_deaths"], k["deaths"]["total"],
             _t(lang, "kpi_deaths_sub", lep=k["deaths"][lep], den=k["deaths"][den]), "ink"),
        _kpi(t["kpi_cfr_lep"], k["cfr_pct"][lep],
             _t(lang, "kpi_cfr_sub", deaths=k["deaths"][lep], cases=k["cases"][lep]),
             "lep", 1, "%"),
        _kpi(t["kpi_cfr_den"], k["cfr_pct"][den],
             _t(lang, "kpi_cfr_sub", deaths=k["deaths"][den], cases=k["cases"][den]),
             "den", 1, "%"),
        _kpi(t["kpi_weeks"], k["weeks_above"],
             _t(lang, "kpi_weeks_sub", first=first_above, last=last_week), "red"),
        _kpi(t["kpi_hosp"], k["hospitalised"]["total"],
             _t(lang, "kpi_hosp_sub", pct=format_number(k["hospitalised_pct"])), "sun"),
    ])

    # --- epidemic curve
    curve = payload["curve"]
    curve_rows = [[w["wk"], format_date(dt.date.fromisoformat(w["start"]), lang),
                   _show_cell(w[lep]), _show_cell(w[den])] for w in curve["weeks"]]
    curve_panel = _panel(
        "p-curve", t["curve_title"], t["curve_sub"],
        '<div class="legend" id="curve-legend"></div>'
        '<div class="chart" id="c-curve" role="img"></div>'
        + _details(lang, _table([t["week"], t["week_start"], t[lep], t[den]], curve_rows,
                                t["curve_title"], "counts"),
                   _esc(t["unknown_onset"]) + " " + _esc(t["lt5_long"])),
        take=_esc(_t(lang, "curve_take", lep_wk=curve["peak"][lep]["wk"],
                     lep_n=curve["peak"][lep]["n"], den_wk=curve["peak"][den]["wk"],
                     den_n=curve["peak"][den]["n"])),
        controls=_seg(lang, "curve", t["disease"],
                      [("both", t["both"]), (lep, t[lep]), (den, t[den])], "both"),
        extra_cls="span-8")

    # --- actions
    actions = "".join(
        f'<li class="act act-{a["priority"]}"><span class="chip">'
        f'{_esc(t["p_" + a["priority"]])}</span><h3>{_esc(a["title"])}</h3>'
        f'<p>{_esc(a["body"])}</p></li>' for a in payload["actions"])
    actions_panel = _panel("p-actions", t["actions_title"],
                           _t(lang, "actions_sub", date=format_date(as_of, lang, year=True)),
                           f'<ol class="actions">{actions}</ol>', extra_cls="span-4 actions-panel")

    # --- map
    bands = payload["bands"]
    feats = sorted(payload["map"]["features"], key=lambda f: f["id"])
    brgy_rows = [[f["name"], t[f["band"]], format_number(f["pop"]),
                  _show_cell(f[lep]["cell"]),
                  "–" if f[lep]["rate"] is None else format_number(f[lep]["rate"], 1),
                  _show_cell(f[den]["cell"]),
                  "–" if f[den]["rate"] is None else format_number(f[den]["rate"], 1)]
                 for f in feats]
    brgy_table = _table([t["brgy"], t["band"], t["population"], f"{t[lep]}: {t['cases']}",
                         f"{t[lep]}: {t['per10k']}", f"{t[den]}: {t['cases']}",
                         f"{t[den]}: {t['per10k']}"], brgy_rows, t["map_title"],
                        "counts")
    map_panel = _panel(
        "p-map", t["map_title"], t["map_sub_rate"],
        '<div class="map-wrap"><div class="chart" id="c-map" role="img"></div>'
        '<div class="map-side"><div class="legend vertical" id="map-legend"></div>'
        f'<p class="map-info" id="map-info" aria-live="polite">{_esc(t["map_hint"])}</p>'
        f'<p class="fine">{_esc(t["map_fiction"])}</p></div></div>'
        + _details(lang, brgy_table, _esc(t["lt5_long"]) + ". " + _esc(t["x_long"]) + "."),
        take=_esc(_t(lang, "map_take", lep_river=format_number(bands[lep]["riverside"], 1),
                     den_coast=format_number(bands[den]["coastal"], 1))),
        controls='<div class="ctrls">'
        + _seg(lang, "mapd", t["disease"], [(lep, t[lep]), (den, t[den])], lep)
        + _seg(lang, "mapm", t["measure"], [("rate", t["rate"]), ("count", t["count"])],
               "rate") + "</div>",
        extra_cls="span-6", sub_id="map-sub")

    # --- threshold
    thr = payload["thr"]["weeks"]
    complete = [w for w in thr[:-1]]
    fc = payload["forecast"]
    if fc:
        fc_text = _esc(_t(lang, "fc_note", n=len(fc["weeks"]), start=fc["start"]))
    else:
        fc_text = _esc(t["fc_none"])
    thr_rows = [[w["wk"], format_date(dt.date.fromisoformat(w["start"]), lang),
                 _show_cell(w["cell"]), format_number(w["thr"], 1),
                 "✓" if w["above"] else ""] for w in thr]
    thr_panel = _panel(
        "p-thr", t["thr_title"],
        _t(lang, "thr_sub", first=thr[0]["wk"], last=thr[-1]["wk"]),
        '<div class="legend" id="thr-legend"></div>'
        '<div class="chart" id="c-thr" role="img"></div>'
        f'<p class="fc-note{" none" if not fc else ""}">{fc_text}</p>'
        + _details(lang, _table([t["week"], t["week_start"], t["cases"], t["threshold"],
                                 t["above"]], thr_rows, t["thr_title"], "counts"),
                   _esc(t["lt5_long"]) + "."),
        take=_esc(_t(lang, "thr_take", first=first_above, wk=complete[-1]["wk"],
                     n=complete[-1]["cell"][0], thr=format_number(complete[-1]["thr"], 1))),
        extra_cls="span-6")

    # --- pyramid
    pyr = payload["pyramid"]
    pyr_rows = [[g, _show_cell(pyr[lep]["M"][i]), _show_cell(pyr[lep]["F"][i]),
                 _show_cell(pyr[den]["M"][i]), _show_cell(pyr[den]["F"][i])]
                for i, g in enumerate(pyr["groups"])]
    pyr_panel = _panel(
        "p-pyr", t["pyr_title"], t["pyr_sub"],
        '<div class="legend" id="pyr-legend"></div>'
        '<div class="chart" id="c-pyr" role="img"></div>'
        + _details(lang, _table([t["age_group"], f"{t[lep]}: {t['male']}",
                                 f"{t[lep]}: {t['female']}", f"{t[den]}: {t['male']}",
                                 f"{t[den]}: {t['female']}"], pyr_rows, t["pyr_title"],
                                "counts"),
                   _esc(_t(lang, "unknown_age", n=k["unknown_age"])) + " "
                   + _esc(t["lt5_long"]) + ". " + _esc(t["x_long"]) + "."),
        take=_esc(_t(lang, "pyr_take", lep_m=format_number(k["male_pct"][lep]),
                     lep_age=k["median_age"][lep], den_age=k["median_age"][den])),
        controls=_seg(lang, "pyr", t["disease"], [(lep, t[lep]), (den, t[den])], lep),
        extra_cls="span-4")

    # --- 7-1-7
    t717 = payload["t717"]
    gauges = "".join(
        f'<div class="g-item">{_gauge_svg(g["pct"], _tone(g["pct"]))}'
        f'<p class="g-cap"><b>{_esc(t[g["key"]])}</b>'
        f'<span>{_esc(_t(lang, "met_of", met=g["met"], n=t717["n"]))} · '
        f'{_esc(_t(lang, "median_d", n=g["median"]))}</span></p></div>'
        for g in t717["targets"])
    gauges += (f'<div class="g-item g-all">{_gauge_svg(t717["all"]["pct"], "bad")}'
               f'<p class="g-cap"><b>{_esc(t["all3"])}</b>'
               f'<span>{_esc(_t(lang, "met_of", met=t717["all"]["met"], n=t717["n"]))}'
               "</span></p></div>")
    top_n = max(b["n"] for b in t717["bottlenecks"])
    bottlenecks = "".join(
        f'<li><span class="b-text">{_esc(b["label"])}</span>'
        f'<span class="b-bar" style="--w:{round(100 * b["n"] / top_n)}%"></span>'
        f'<span class="b-n">{_esc(_t(lang, "events", n=b["n"]))}</span></li>'
        for b in t717["bottlenecks"])
    t717_rows = [[t[g["key"]], str(g["met"]), str(t717["n"] - g["met"]),
                  _t(lang, "days_n", n=g["median"])]
                 for g in t717["targets"]]
    t717_panel = _panel(
        "p-717", t["t717_title"],
        _t(lang, "t717_sub", n=t717["n"],
           start=format_date(dt.date.fromisoformat(t717["from"]), lang, year=True),
           end=format_date(dt.date.fromisoformat(t717["to"]), lang, year=True)),
        f'<div class="gauges">{gauges}</div>'
        f'<h3 class="mini">{_esc(t["bottlenecks"])}</h3><ol class="bottlenecks">{bottlenecks}</ol>'
        + _details(lang, _table([t["target"], t["met"], t["missed"], t["median"]], t717_rows,
                                t["t717_title"])),
        extra_cls="span-4")

    # --- forest
    forest = payload["forest"]
    by_key = {r["key"]: r for r in forest}
    forest_rows = [[t[f"ex_{r['key']}"], f"{r['or']:.2f}", f"{r['lo']:.2f}–{r['hi']:.2f}"]
                   for r in forest]
    forest_panel = _panel(
        "p-forest", t["forest_title"],
        _t(lang, "forest_sub", cases=payload["cc_n"]["cases"],
           controls=payload["cc_n"]["controls"]),
        '<div class="chart" id="c-forest" role="img"></div>'
        + _details(lang, _table([t["exposure"], t["or"], t["ci"]], forest_rows,
                                t["forest_title"])),
        take=_esc(_t(lang, "forest_take", or_w=f"{by_key['waded']['or']:.2f}",
                     or_adj=f"{by_key['waded_adj']['or']:.2f}")),
        extra_cls="span-4")

    notes = "".join(f"<li>{n}</li>" for n in t["notes"])
    if fc:
        notes += f"<li>{fc_text}</li>"
    footer = (f'<footer class="notes" id="notes"><h2>{_esc(t["notes_title"])}</h2>'
              f'<ul>{notes}</ul><p class="foot">{t["footer"]} '
              f'<a href="../chapters/dashboard/">{_esc(t["to_chapter"])}</a> · '
              f'<a href="../">{_esc(t["home"])}</a></p></footer>')

    data_json = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                           default=str).replace("</", "<\\/")
    main = (f'<main id="main" tabindex="-1">{alert}<div class="kpis">{kpis}</div>'
            f'<div class="grid">{curve_panel}{actions_panel}{map_panel}{thr_panel}'
            f"{pyr_panel}{t717_panel}{forest_panel}</div></main>")
    return (
        "<!DOCTYPE html>\n"
        f'<html lang="{_HTML_LANG[lang]}">\n<head>\n<meta charset="utf-8"/>\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
        '<meta name="color-scheme" content="light dark"/>\n'
        f'<meta name="description" content="{_esc(t["subtitle"])}"/>\n'
        f"<title>{_esc(t['page_title'])}</title>\n"
        f'<link rel="icon" href="data:image/svg+xml,{_FAVICON}"/>\n'
        f"<style>{_CSS}{_print_css()}</style>\n</head>\n<body>\n"
        f'<noscript><p class="noscript">{_esc(t["noscript"])}</p></noscript>\n'
        f"{header}\n{main}\n{footer}\n"
        '<div id="tip" class="tip" role="tooltip" hidden></div>\n'
        f'<script type="application/json" id="dash-data">{data_json}</script>\n'
        f"<script>{_JS}</script>\n</body>\n</html>\n"
    )


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
    page_html = render_html(build_payload(load_data(), lang))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    page = out_dir / "index.html"
    page.write_text(page_html, encoding="utf-8")
    return page


# =============================================================================
# 8. Inline assets (CSS, JavaScript) — no external resources
# =============================================================================

_FAVICON = (
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-50 -50 100 100'%3E"
    "%3Crect x='-50' y='-50' width='100' height='100' rx='22' fill='%230038A8'/%3E"
    "%3Ccircle r='18' fill='%23FCD116'/%3E%3Cpath d='M0-44L6-22H-6ZM0 44L6 22H-6ZM-44 0L-22 6V-6Z"
    "M44 0L22 6V-6Z' fill='%23FCD116'/%3E%3C/svg%3E"
)

_BUNTING = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 30'%3E"
    "%3Cpath d='M0 3 Q60 13 120 3' fill='none' stroke='%231C1B29' stroke-width='1.2'/%3E"
    "%3Cpath d='M3 4.6 L21 4.6 L12 22 Z' fill='%230038A8'/%3E"
    "%3Cpath d='M27 7.4 L45 7.4 L36 25 Z' fill='%23CE1126'/%3E"
    "%3Cpath d='M51 8.4 L69 8.4 L60 26 Z' fill='%23FCD116'/%3E"
    "%3Cpath d='M75 7.4 L93 7.4 L84 25 Z' fill='%23FFFCF4' stroke='%231C1B29' "
    "stroke-width='.6' stroke-opacity='.4'/%3E"
    "%3Cpath d='M99 4.6 L117 4.6 L108 22 Z' fill='%232F7D32'/%3E%3C/svg%3E\")"
)

_CSS = r"""
:root{
  --flag-blue:#0038a8;--flag-red:#ce1126;--sun:#fcd116;--sun-deep:#e0a800;--mango:#ff9f1c;
  --ink:#1c1b29;--night:#13183a;--cream:#fffcf4;--chrome-1:#f4f6f8;--chrome-2:#aeb7c0;--chrome-3:#6e7882;
  --bg:#fffbf2;--bg-alt:#fff4de;--surface:#ffffff;--surface-alt:#fff8ea;
  --text:#1c1b29;--muted:#4d4a5e;--border:#eadcc0;--border-strong:#cdb98f;
  --blue:#0038a8;--red:#b30e22;--leaf:#276b2a;--mango-text:#9a4600;--teal:#006d77;--indigo:#4b3fb0;
  --soft-red:#fdecee;--soft-sun:#fff6cc;--soft-blue:#e8efff;--soft-leaf:#e9f5e4;--soft-indigo:#eeebff;
  --lep:#0038a8;--den:#d9480f;--den-above:#b30e22;--thr:#ce1126;--fc:#4b3fb0;--male:#00737d;--female:#7b3fb0;
  --grid:#eadcc0;--axis:#4d4a5e;--hatch-bg:#f3ece0;
  --lep-1:#e3ecfd;--lep-2:#b3cbf4;--lep-3:#7a9fe4;--lep-4:#3a68cc;--lep-5:#0b2f86;
  --den-1:#ffefe0;--den-2:#ffcf9e;--den-3:#ffa25a;--den-4:#ea6a1c;--den-5:#a8360a;
  --zero:#f6f1e7;--map-line:#fffbf2;
  --shadow:0 1px 2px rgba(28,27,41,.06),0 8px 24px rgba(28,27,41,.07);
  --radius:16px;--ease:cubic-bezier(.34,1.4,.64,1);
  --font:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","PingFang TC","Microsoft JhengHei","Noto Sans TC","Noto Sans CJK TC","WenQuanYi Zen Hei",sans-serif;
  --display:"Bungee","Arial Black","Archivo Black","Noto Sans TC","PingFang TC","Microsoft JhengHei","WenQuanYi Zen Hei",Impact,system-ui,sans-serif;
  color-scheme:light;
}
:root[data-theme="dark"]{
  --bg:#11152a;--bg-alt:#161b33;--surface:#1b2140;--surface-alt:#222949;
  --text:#f4efe2;--muted:#c8c2b2;--border:#313a62;--border-strong:#4a5384;
  --blue:#9bbaff;--red:#ff8f9b;--leaf:#8ed88a;--mango-text:#ffb861;--teal:#5fd8cc;--indigo:#bcb3ff;
  --soft-red:#3a1c2a;--soft-sun:#36321c;--soft-blue:#1c2a55;--soft-leaf:#1b3326;--soft-indigo:#2a2752;
  --lep:#8fb0ff;--den:#ff9a52;--den-above:#ff6b7a;--thr:#ff6b7a;--fc:#bcb3ff;--male:#5fd8cc;--female:#d4a5ff;
  --grid:#313a62;--axis:#c8c2b2;--hatch-bg:#262c4d;
  --lep-1:#22305e;--lep-2:#2f4c94;--lep-3:#4673d6;--lep-4:#7fa2f2;--lep-5:#c3d5ff;
  --den-1:#3b2a22;--den-2:#704020;--den-3:#b8581c;--den-4:#f08a3c;--den-5:#ffc58f;
  --zero:#1f2545;--map-line:#11152a;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 28px rgba(0,0,0,.35);
  color-scheme:dark;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#11152a;--bg-alt:#161b33;--surface:#1b2140;--surface-alt:#222949;
    --text:#f4efe2;--muted:#c8c2b2;--border:#313a62;--border-strong:#4a5384;
    --blue:#9bbaff;--red:#ff8f9b;--leaf:#8ed88a;--mango-text:#ffb861;--teal:#5fd8cc;--indigo:#bcb3ff;
    --soft-red:#3a1c2a;--soft-sun:#36321c;--soft-blue:#1c2a55;--soft-leaf:#1b3326;--soft-indigo:#2a2752;
    --lep:#8fb0ff;--den:#ff9a52;--den-above:#ff6b7a;--thr:#ff6b7a;--fc:#bcb3ff;--male:#5fd8cc;--female:#d4a5ff;
    --grid:#313a62;--axis:#c8c2b2;--hatch-bg:#262c4d;
    --lep-1:#22305e;--lep-2:#2f4c94;--lep-3:#4673d6;--lep-4:#7fa2f2;--lep-5:#c3d5ff;
    --den-1:#3b2a22;--den-2:#704020;--den-3:#b8581c;--den-4:#f08a3c;--den-5:#ffc58f;
    --zero:#1f2545;--map-line:#11152a;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 28px rgba(0,0,0,.35);
    color-scheme:dark;
  }
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 var(--font);
  background-image:radial-gradient(circle at 100% 0,color-mix(in srgb,var(--sun) 14%,transparent),transparent 34rem)}
a{color:var(--blue)}
a:hover{color:var(--red)}
:focus-visible{outline:3px solid var(--sun-deep);outline-offset:2px;border-radius:6px}
.skip{position:absolute;left:12px;top:-60px;background:var(--sun);color:var(--ink);padding:8px 14px;border-radius:10px;z-index:20;font-weight:700}
.skip:focus{top:10px}
.noscript{margin:0;padding:10px 16px;background:var(--soft-sun);text-align:center}
.flagbar{height:6px;background:linear-gradient(90deg,var(--flag-blue) 0 50%,var(--flag-red) 50% 100%)}
/* ---------- header: jeepney signboard ---------- */
.top{max-width:1480px;margin:0 auto;padding:16px 20px 6px}
.sign{position:relative;display:flex;align-items:center;gap:18px;padding:16px 22px;border-radius:20px;
  background:linear-gradient(180deg,#0a46c2,var(--flag-blue) 60%,#002a80);color:var(--cream);
  border:4px solid var(--chrome-2);
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.35),inset 0 -6px 0 rgba(0,0,0,.18),0 6px 0 rgba(28,27,41,.22),var(--shadow);
  overflow:hidden}
.sign::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(115deg,transparent 0 40px,rgba(255,255,255,.035) 40px 80px)}
.sign::after{content:"";position:absolute;left:0;right:0;bottom:0;height:7px;
  background:linear-gradient(90deg,var(--flag-red) 0 33%,var(--sun) 33% 66%,var(--cream) 66%)}
.sun{width:74px;height:74px;flex:none;fill:var(--sun);filter:drop-shadow(0 2px 0 rgba(0,0,0,.25));animation:spin 90s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.sign-text{flex:1;min-width:0;position:relative}
.kicker{margin:0;display:inline-block;font:900 12px/1 var(--display);letter-spacing:.14em;text-transform:uppercase;
  background:var(--sun);color:var(--ink);padding:5px 10px 4px;border-radius:999px}
.top h1{margin:6px 0 2px;font:900 clamp(24px,3.4vw,42px)/1.05 var(--display);letter-spacing:.01em;color:var(--sun);
  text-shadow:0 3px 0 #001a55,3px 3px 0 #001a55}
.subtitle{margin:0;color:#dfe7ff;font-size:14px;max-width:62ch}
.sign-side{position:relative;display:flex;flex-direction:column;align-items:flex-end;gap:8px;text-align:right}
.asof{margin:0;display:flex;gap:10px;align-items:center;background:var(--cream);color:var(--ink);padding:8px 14px;border-radius:12px;
  box-shadow:0 3px 0 rgba(0,0,0,.25)}
.asof b{display:block;font-size:15px}
.asof small{display:block;font-size:11.5px;color:#4d4a5e}
.dot{width:10px;height:10px;border-radius:50%;background:#2f7d32;box-shadow:0 0 0 3px rgba(47,125,50,.25);flex:none}
.fiction{margin:0;font-size:12px;color:var(--sun);font-weight:700;letter-spacing:.02em}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:flex-end;margin-top:10px}
.langs{display:inline-flex;border:2px solid var(--border-strong);border-radius:999px;overflow:hidden;background:var(--surface)}
.langs a{padding:5px 12px;text-decoration:none;color:var(--text);font-weight:700;font-size:13px}
.langs a+a{border-left:1px solid var(--border)}
.langs a.is-current{background:var(--flag-blue);color:#fff}
.tool{font:inherit;font-size:13px;font-weight:700;display:inline-flex;align-items:center;gap:6px;padding:6px 13px;border-radius:999px;
  border:2px solid var(--border-strong);background:var(--surface);color:var(--text);text-decoration:none;cursor:pointer;
  transition:transform .15s var(--ease),box-shadow .15s}
.tool:hover{transform:translateY(-1px);box-shadow:0 3px 0 var(--border-strong);color:var(--text)}
.tool[aria-pressed="true"]{background:var(--night);color:var(--sun);border-color:var(--night)}
.ico-moon{width:12px;height:12px;border-radius:50%;box-shadow:inset -4px -2px 0 0 currentColor}
.bunting{height:30px;margin:4px 0 0;background:__BUNTING__ repeat-x 0 0/120px 30px;opacity:.95;
  animation:sway 6s ease-in-out infinite alternate;transform-origin:top}
@keyframes sway{from{transform:skewX(-1.5deg)}to{transform:skewX(1.5deg)}}
/* ---------- layout ---------- */
main{max-width:1480px;margin:0 auto;padding:8px 20px 24px;outline:none}
.alert{display:flex;gap:12px;align-items:center;margin:4px 0 14px;padding:11px 16px;border-radius:14px;font-weight:700;
  background:var(--soft-red);color:var(--red);border:2px solid color-mix(in srgb,var(--flag-red) 45%,transparent)}
.pulse{width:12px;height:12px;border-radius:50%;background:var(--flag-red);flex:none;position:relative}
.pulse::after{content:"";position:absolute;inset:-6px;border-radius:50%;border:2px solid var(--flag-red);animation:ping 1.8s ease-out infinite}
@keyframes ping{from{transform:scale(.5);opacity:1}to{transform:scale(1.6);opacity:0}}
.kpis{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px;margin-bottom:16px}
.kpi{position:relative;background:var(--surface);border:2px solid var(--border);border-radius:var(--radius);padding:12px 14px 11px;
  box-shadow:var(--shadow);overflow:hidden}
.kpi::before{content:"";position:absolute;left:0;top:0;right:0;height:6px;background:var(--tone)}
.kpi-blue{--tone:var(--flag-blue);--tone-t:var(--blue)}.kpi-ink{--tone:var(--ink);--tone-t:var(--text)}
.kpi-lep{--tone:var(--lep);--tone-t:var(--lep)}.kpi-den{--tone:var(--den);--tone-t:var(--den)}
.kpi-red{--tone:var(--flag-red);--tone-t:var(--red)}.kpi-sun{--tone:var(--sun);--tone-t:var(--mango-text)}
.kpi-label{margin:2px 0 0;font-size:12.5px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.kpi-val{margin:2px 0 0;font:900 clamp(28px,2.8vw,40px)/1.05 var(--display);color:var(--tone-t);font-variant-numeric:tabular-nums}
.kpi-sub{margin:4px 0 0;font-size:12.5px;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:16px}
.span-8{grid-column:span 8}.span-6{grid-column:span 6}.span-4{grid-column:span 4}
.panel{min-width:0;background:var(--surface);border:2px solid var(--border);border-radius:var(--radius);padding:14px 16px 12px;box-shadow:var(--shadow);position:relative}
.panel>.ph{display:flex;gap:12px;justify-content:space-between;align-items:flex-start;flex-wrap:wrap}
.panel h2{margin:0;font:900 17px/1.2 var(--display);letter-spacing:.01em;color:var(--text)}
.panel h2::before{content:"";display:inline-block;width:14px;height:14px;margin-right:8px;vertical-align:-1px;border-radius:50%;
  background:radial-gradient(circle,var(--sun) 0 38%,transparent 40%),conic-gradient(from 22.5deg,var(--sun-deep) 0 12.5%,transparent 0 25%,var(--sun-deep) 0 37.5%,transparent 0 50%,var(--sun-deep) 0 62.5%,transparent 0 75%,var(--sun-deep) 0 87.5%,transparent 0)}
.sub{margin:2px 0 0;font-size:12.5px;color:var(--muted)}
.take{margin:8px 0 6px;font-size:14px;padding-left:10px;border-left:4px solid var(--sun)}
.ctrls{display:flex;gap:8px;flex-wrap:wrap}
.seg{display:inline-flex;background:var(--surface-alt);border:2px solid var(--border);border-radius:999px;padding:2px}
.seg button{font:inherit;font-size:12.5px;font-weight:700;border:0;background:transparent;color:var(--muted);padding:5px 11px;border-radius:999px;cursor:pointer;min-height:30px}
.seg button[aria-pressed="true"]{background:var(--flag-blue);color:#fff;box-shadow:0 2px 0 rgba(0,0,0,.2)}
.seg button:hover:not([aria-pressed="true"]){color:var(--text);background:var(--soft-blue)}
.chart{width:100%;min-height:120px;position:relative}
.chart svg{display:block;width:100%;height:auto;overflow:visible}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12px;color:var(--muted);margin:4px 0 2px;min-height:18px}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{width:14px;height:12px;border-radius:3px;display:inline-block;flex:none}
.legend i.line{height:0;border-top:3px dashed var(--thr);border-radius:0;width:20px}
.legend i.band{background:color-mix(in srgb,var(--fc) 28%,transparent);border-top:2px solid var(--fc)}
.legend.vertical{flex-direction:column;gap:4px}
.sw-hatch{background:repeating-linear-gradient(135deg,var(--hatch-bg) 0 3px,var(--muted) 3px 4.5px)}
/* svg marks */
.ax text,.lbl{fill:var(--axis);font-size:11.5px}
.ax line,.gridl{stroke:var(--grid);stroke-width:1}
.ax .base{stroke:var(--axis);stroke-width:1.2}
.lbl.strong{fill:var(--text);font-weight:700}
.bar.lep{fill:var(--lep)}.bar.den{fill:var(--den)}.bar.den.above{fill:var(--den-above)}
.bar.inc{opacity:.55}
.hatch-line{stroke:var(--muted);stroke-width:1.5}.hatch-bg{fill:var(--hatch-bg)}
.stub{stroke:var(--muted);stroke-width:1;stroke-dasharray:2 2}
.mark{cursor:pointer;outline:none}
.mark:focus-visible{stroke:var(--sun-deep);stroke-width:3}
.mark:hover{filter:brightness(1.12)}
.typhoon line{stroke:var(--indigo);stroke-width:2;stroke-dasharray:5 4}
.typhoon text{fill:var(--indigo);font-weight:800;font-size:12px}
.typhoon path{fill:none;stroke:var(--indigo);stroke-width:2.2;stroke-linecap:round}
.incband{fill:var(--muted);opacity:.08}
.thr-line{fill:none;stroke:var(--thr);stroke-width:2.4;stroke-dasharray:6 4}
.fc-band{fill:var(--fc);opacity:.22}
.fc-line{fill:none;stroke:var(--fc);stroke-width:2.4}
.fc-dot{fill:var(--surface);stroke:var(--fc);stroke-width:2}
.fc-zone{fill:var(--fc);opacity:.06}
.fc-note{margin:6px 0 0;font-size:12px;color:var(--indigo)}
.fc-note.none{color:var(--muted);font-style:italic;padding:6px 10px;border:1.5px dashed var(--border-strong);border-radius:10px;display:inline-block}
.brgy{stroke:var(--map-line);stroke-width:1.4;vector-effect:non-scaling-stroke;cursor:pointer;transition:filter .2s}
.brgy.sel,.brgy:focus-visible{stroke:var(--sun-deep);stroke-width:3.5;outline:none}
.brgy:hover{filter:brightness(1.08) saturate(1.1)}
.c0{fill:var(--zero)}
.lep .c1{fill:var(--lep-1)}.lep .c2{fill:var(--lep-2)}.lep .c3{fill:var(--lep-3)}.lep .c4{fill:var(--lep-4)}.lep .c5{fill:var(--lep-5)}
.den .c1{fill:var(--den-1)}.den .c2{fill:var(--den-2)}.den .c3{fill:var(--den-3)}.den .c4{fill:var(--den-4)}.den .c5{fill:var(--den-5)}
.rank circle{fill:var(--sun);stroke:var(--ink);stroke-width:1.5;vector-effect:non-scaling-stroke}
.rank text{fill:var(--ink);font-weight:900;text-anchor:middle;dominant-baseline:central;pointer-events:none}
.band-lbl{fill:var(--text);opacity:.55;font-weight:800;letter-spacing:.12em;text-transform:uppercase;pointer-events:none}
.map-wrap{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:14px;align-items:start}
.map-info{margin:10px 0 0;font-size:13px;min-height:4.6em;padding:8px 10px;background:var(--surface-alt);border-radius:10px;border:1.5px solid var(--border)}
.map-info>b:first-child{display:block;font-size:14px}
.map-info .muted{display:block;color:var(--muted);font-size:12px}
.fine{margin:6px 0 0;font-size:11px;color:var(--muted)}
.male{fill:var(--male)}.female{fill:var(--female)}
.legend i.male{background:var(--male)}.legend i.female{background:var(--female)}
.legend i.lep{background:var(--lep)}.legend i.den{background:var(--den)}.legend i.den-above{background:var(--den-above)}
.f-ci{stroke:var(--axis);stroke-width:2.2}
.f-pt{stroke:var(--surface);stroke-width:1.5}
.f-risk{fill:var(--red)}.f-protective{fill:var(--leaf)}.f-null{fill:var(--muted)}.f-adjusted{fill:var(--indigo)}
.f-one{stroke:var(--text);stroke-width:1.2;stroke-dasharray:3 3}
.f-row:nth-child(odd) .f-bg{fill:var(--surface-alt)}
.f-bg{fill:transparent}
/* gauges */
.gauges{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:8px}
.g-item{text-align:center;min-width:0}
.gauge{width:100%;max-width:104px;height:auto;display:block;margin:0 auto}
.gauge circle{fill:none;stroke-width:11;stroke-linecap:round}
.g-track{stroke:var(--surface-alt);stroke:color-mix(in srgb,var(--muted) 18%,transparent)}
.g-good .g-fill{stroke:var(--leaf)}.g-mid .g-fill{stroke:var(--mango)}.g-bad .g-fill{stroke:var(--flag-red)}
.g-val{font:900 19px var(--display);fill:var(--text);text-anchor:middle}
.g-cap{margin:0;font-size:11.5px;line-height:1.3;color:var(--muted)}
.g-cap b{display:block;color:var(--text);font-size:12px}
.g-cap span{display:block}
.g-all .g-val{fill:var(--red)}
.mini{margin:12px 0 6px;font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
.bottlenecks{list-style:none;margin:0;padding:0;display:grid;gap:7px}
.bottlenecks li{display:grid;grid-template-columns:1fr auto;gap:2px 10px;font-size:12.5px;line-height:1.3}
.b-bar{grid-column:1/-1;height:7px;border-radius:99px;background:linear-gradient(90deg,var(--flag-red),var(--mango));width:var(--w);order:3}
.b-n{color:var(--muted);font-weight:700;white-space:nowrap}
/* actions */
.actions-panel{background:linear-gradient(180deg,var(--surface),var(--surface-alt));grid-row:span 1}
.actions{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:10px;counter-reset:a}
.act{position:relative;padding:9px 12px 10px 44px;border-radius:12px;background:var(--surface);border:1.5px solid var(--border);counter-increment:a}
.act::before{content:counter(a);position:absolute;left:10px;top:10px;width:24px;height:24px;border-radius:50%;display:grid;place-items:center;
  font:900 13px var(--display);background:var(--c);color:var(--on)}
.act-urgent{--c:var(--flag-red);--on:#fff;border-left:5px solid var(--flag-red)}
.act-week{--c:var(--sun);--on:var(--ink);border-left:5px solid var(--sun-deep)}
.act-fix{--c:var(--flag-blue);--on:#fff;border-left:5px solid var(--flag-blue)}
.act h3{margin:0;font-size:14px;line-height:1.3}
.act p{margin:3px 0 0;font-size:13px;color:var(--muted)}
.chip{float:right;margin:0 0 4px 8px;font-size:10.5px;font-weight:800;text-transform:uppercase;letter-spacing:.06em;padding:2px 8px;border-radius:99px;
  background:color-mix(in srgb,var(--c) 18%,transparent);color:var(--text)}
/* tables */
details.numbers{margin-top:8px;border-top:1.5px dashed var(--border);padding-top:6px}
details.numbers summary{cursor:pointer;font-size:12.5px;font-weight:700;color:var(--blue);width:max-content;max-width:100%}
.tscroll{overflow-x:auto;margin-top:6px}
.num-table{border-collapse:collapse;width:100%;font-size:12.5px;font-variant-numeric:tabular-nums}
.num-table caption{text-align:left;font-weight:700;padding:2px 0 6px;color:var(--muted)}
.num-table th,.num-table td{padding:4px 8px;border-bottom:1px solid var(--border);text-align:right;white-space:nowrap}
.num-table th[scope=row],.num-table thead th:first-child{text-align:left}
.num-table thead th{background:var(--flag-blue);color:#fff;font-weight:700;border-bottom:3px solid var(--sun)}
.num-table tbody tr:nth-child(even){background:var(--surface-alt)}
.tnote{margin:6px 0 0;font-size:11.5px;color:var(--muted)}
/* tooltip */
.tip{position:fixed;z-index:50;max-width:260px;padding:8px 11px;border-radius:10px;background:var(--night);color:var(--cream);
  font-size:12.5px;line-height:1.4;box-shadow:0 10px 30px rgba(0,0,0,.3);pointer-events:none;border:1.5px solid rgba(252,209,22,.6)}
.tip b{color:var(--sun)}
.tip .muted{color:#c8c2b2}
/* footer */
.notes{max-width:1480px;margin:0 auto 28px;padding:16px 20px}
.notes>h2{font:900 16px var(--display);margin:0 0 8px}
.notes ul{margin:0;padding-left:18px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 28px;font-size:12.5px;color:var(--muted)}
.notes li b{color:var(--text)}
.foot{font-size:12.5px;color:var(--muted);margin:12px 0 0;padding-top:10px;border-top:3px solid;border-image:linear-gradient(90deg,var(--flag-blue),var(--flag-red),var(--sun)) 1}
/* motion */
.kpi,.panel,.alert{animation:rise .7s var(--ease) both;animation-delay:calc(var(--i,0) * 70ms)}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.grow .gm{animation:grow .8s var(--ease) both;transform-box:fill-box;transform-origin:50% 100%}
.grow .gmx{animation:growx .8s var(--ease) both;transform-box:fill-box}
@keyframes grow{from{transform:scaleY(0)}}
@keyframes growx{from{transform:scaleX(0)}}
.grow .gfade{animation:fade .9s ease both}
@keyframes fade{from{opacity:0}}
.g-fill{animation:gauge 1.4s var(--ease) both .3s}
@keyframes gauge{from{stroke-dasharray:0 999}}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
}
/* responsive */
@media (max-width:1180px){
  .kpis{grid-template-columns:repeat(3,minmax(0,1fr))}
  .span-8,.span-4.actions-panel{grid-column:span 12}
  .span-6{grid-column:span 12}
  .span-4{grid-column:span 6}
  #p-forest{grid-column:span 12}
}
@media (max-width:760px){
  .top{padding:10px 12px 4px}
  .sign{flex-wrap:wrap;padding:14px 14px 18px;gap:10px 12px}
  .sun{width:46px;height:46px}
  .sign-side{align-items:flex-start;text-align:left;width:100%}
  .subtitle{font-size:13px}
  .tools{justify-content:flex-start}
  main{padding:6px 12px 20px}
  .notes{padding:12px}
  .kpis{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  .kpi{padding:10px 12px}
  .kpi-val{font-size:28px}
  .grid{gap:12px}
  .span-4,#p-forest{grid-column:span 12}
  .panel{padding:12px 12px 10px}
  .map-wrap{grid-template-columns:1fr}
  .legend.vertical{flex-direction:row;flex-wrap:wrap}
  .map-info{min-height:0}
  .notes ul{grid-template-columns:1fr}
  .gauges{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
  .gauge{max-width:96px}
}
@media (max-width:400px){
  .langs a{padding:5px 9px}
  .tool{padding:6px 10px}
}
"""
_CSS = _CSS.replace("__BUNTING__", _BUNTING)

#: Print layout (one A4 / Letter landscape page). ``{P}`` is replaced by the
#: selector prefix: ``html `` inside ``@media print`` and ``html.printing ``
#: for the live preview the page switches to on ``beforeprint``.
_PRINT_RULES = r"""
{P}body{background:#fff;color:#1c1b29;font-size:9px}
{P}.skip,{P}.tools,{P}.bunting,{P}details.numbers,{P}.ph .seg,{P}.ph .ctrls,{P}.map-info,{P}.tip,{P}.noscript{display:none!important}
{P}.flagbar{height:3px}
{P}.top{padding:0 0 3px;max-width:none}
{P}.sign{padding:3px 12px 6px;border-width:2px;border-radius:10px;box-shadow:none;gap:10px}
{P}.sign::after{height:3px}
{P}.sun{width:30px;height:30px;animation:none}
{P}.top h1{font-size:19px;margin:2px 0 0;text-shadow:0 2px 0 #001a55}
{P}.kicker{font-size:8px;padding:2px 6px}
{P}.subtitle{display:none}
{P}.asof{padding:3px 8px;box-shadow:none}
{P}.asof b{font-size:10px}{P}.asof small{font-size:7.5px}
{P}.fiction{font-size:8px}
{P}main{padding:0;max-width:none}
{P}.alert{margin:3px 0 4px;padding:3px 10px;font-size:9.5px;border-width:1px}
{P}.kpis{grid-template-columns:repeat(6,minmax(0,1fr));gap:5px;margin-bottom:5px}
{P}.kpi{padding:3px 8px 3px;box-shadow:none;border-width:1px;border-radius:8px}
{P}.kpi::before{height:3px}
{P}.kpi-label{font-size:7px;margin:0}{P}.kpi-val{font-size:15px;margin:0}{P}.kpi-sub{font-size:7px;margin:0}
{P}.grid{grid-template-columns:repeat(6,minmax(0,1fr));gap:4px}
{P}.panel{padding:4px 7px 3px;box-shadow:none;border-width:1px;border-radius:8px;break-inside:avoid;animation:none}
{P}.grid>.panel,{P}.grid>#p-forest{grid-column:span 2}{P}#p-actions{grid-column:1/-1;order:9}
{P}#p-curve{order:1}{P}#p-thr{order:2}{P}#p-map{order:3}{P}#p-pyr{order:4}{P}#p-forest{order:5}{P}#p-717{order:6}
{P}.map-wrap{grid-template-columns:1fr}{P}.legend.vertical{flex-direction:row;flex-wrap:wrap}
{P}.panel h2{font-size:10px}{P}.panel h2::before{width:8px;height:8px;margin-right:4px}
{P}.sub{font-size:7.5px;margin:0}
{P}.take{font-size:8.5px;margin:2px 0;padding-left:5px;border-left-width:2px}
{P}.legend{font-size:7.5px;margin:1px 0;min-height:0;gap:2px 8px}
{P}.legend i{width:9px;height:8px}
{P}.fine{display:none}
{P}.fc-note{font-size:7.5px;margin:1px 0 0;padding:1px 4px}
{P}.actions{gap:3px;margin-top:3px;grid-template-columns:repeat(6,minmax(0,1fr))}
{P}.panel .sub{display:none}{P}.legend.vertical{gap:1px 6px}
{P}#c-map svg{width:auto;max-width:100%;height:100px;margin:0 auto}
{P}.act{padding:3px 6px 3px 24px;border-radius:6px}
{P}.act::before{width:14px;height:14px;font-size:8px;left:5px;top:4px}
{P}.act h3{font-size:7.5px}{P}.act p{font-size:7px;line-height:1.3;margin:0}
{P}.chip{display:none}
{P}.gauges{gap:3px;margin-top:2px}
{P}.gauge{max-width:52px}
{P}.g-cap{font-size:7px}{P}.g-cap b{font-size:7.5px}
{P}.mini{font-size:7.5px;margin:3px 0 2px}
{P}.bottlenecks{gap:2px}
{P}.bottlenecks li{font-size:7.5px;gap:1px 6px}
{P}.b-bar{height:3px}
{P}.notes{padding:2px 0 0;margin:0;max-width:none;break-inside:avoid}
{P}.notes>h2{font-size:9px;margin:0 0 2px}
{P}.notes ul{grid-template-columns:repeat(auto-fit,minmax(0,1fr));grid-auto-flow:column;font-size:6px;line-height:1.22;gap:1px 10px;padding-left:10px}
{P}.fc-note:not(.none){display:none}
{P}.foot{font-size:7px;margin:2px 0 0;padding-top:2px}
{P}.kpi,{P}.panel,{P}.alert{animation:none}
"""


def _print_css() -> str:
    """CSS for printing: the print rules for ``@media print`` and for ``html.printing``."""
    in_print = _PRINT_RULES.replace("{P}", "html ")
    preview = _PRINT_RULES.replace("{P}", "html.printing ")
    return ("@page{size:A4 landscape;margin:5mm}"
            "@media print{html{-webkit-print-color-adjust:exact;print-color-adjust:exact}"
            + in_print + "}" + "html.printing body{width:1060px}" + preview)


_JS = r"""
(function () {
  "use strict";
  var D = JSON.parse(document.getElementById("dash-data").textContent);
  var T = D.t;
  var NS = "http://www.w3.org/2000/svg";
  var RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var DIS = ["leptospirosis", "dengue"];
  var SHORT = { leptospirosis: "lep", dengue: "den" };
  var state = { curve: "both", mapd: "leptospirosis", mapm: "rate", pyr: "leptospirosis" };
  var drawn = {};
  var uid = 0;
  var root = document.documentElement;
  function printing() {
    return root.classList.contains("printing") || (window.matchMedia && window.matchMedia("print").matches);
  }

  // ---------------------------------------------------------------- helpers
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function num(n, d) {
    d = d || 0;
    var s = Number(n).toFixed(d), parts = s.split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
  }
  function fill(tpl, o) {
    return tpl.replace(/\{(\w+)\}/g, function (_, k) { return o[k] !== undefined ? o[k] : ""; });
  }
  function S(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) if (attrs[k] !== null && attrs[k] !== undefined) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function T_(parent, x, y, s, cls, anchor, size) {
    var e = S("text", { x: x, y: y, "class": cls || "lbl", "text-anchor": anchor || "start" }, parent);
    if (size) e.style.fontSize = size + "px";
    e.textContent = s;
    return e;
  }
  function day(iso) { var p = iso.split("-"); return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])); }
  function fdate(iso) {
    var d = day(iso);
    if (D.lang === "zh") return (d.getUTCMonth() + 1) + " 月 " + d.getUTCDate() + " 日";
    return d.getUTCDate() + " " + D.months[d.getUTCMonth()];
  }
  function cellText(c) { return c[1] === 0 ? num(c[0]) : (c[1] === 1 ? "<5" : "x"); }
  function cellDraw(c) { return c[1] === 0 ? c[0] : 2.5; }
  function niceStep(max, ticks) {
    var raw = max / Math.max(1, ticks), mag = Math.pow(10, Math.floor(Math.log10(raw))), n = raw / mag;
    return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10) * mag;
  }
  function svgFor(host, w, h, label) {
    host.innerHTML = "";
    var s = S("svg", { viewBox: "0 0 " + w + " " + h, width: w, height: h, role: "presentation", focusable: "false" }, host);
    if (label) host.setAttribute("aria-label", label);
    if (!RM && !drawn[host.id]) s.setAttribute("class", "grow");
    drawn[host.id] = true;
    return s;
  }
  function hatch(svg) {
    var id = "h" + (++uid);
    var defs = S("defs", null, svg);
    var p = S("pattern", { id: id, width: 6, height: 6, patternUnits: "userSpaceOnUse", patternTransform: "rotate(45)" }, defs);
    S("rect", { width: 6, height: 6, "class": "hatch-bg" }, p);
    S("line", { x1: 0, y1: 0, x2: 0, y2: 6, "class": "hatch-line" }, p);
    return "url(#" + id + ")";
  }
  function yAxis(svg, m, w, h, max, ticks) {
    var step = niceStep(max, ticks), top = Math.ceil(max / step) * step;
    var g = S("g", { "class": "ax" }, svg);
    for (var v = 0; v <= top + 1e-9; v += step) {
      var y = m.t + (h - m.t - m.b) * (1 - v / top);
      S("line", { x1: m.l, x2: w - m.r, y1: y, y2: y, "class": v === 0 ? "base" : "" }, g);
      T_(g, m.l - 6, y + 4, num(v, step < 1 ? 1 : 0), "", "end");
    }
    return top;
  }

  // ---------------------------------------------------------------- tooltip
  var tip = document.getElementById("tip");
  var pinned = null;
  function place(x, y) {
    var r = tip.getBoundingClientRect(), vw = window.innerWidth, vh = window.innerHeight;
    var left = Math.min(Math.max(8, x + 14), vw - r.width - 8), top = y + 16;
    if (top + r.height > vh - 8) top = y - r.height - 14;
    tip.style.left = left + "px";
    tip.style.top = Math.max(8, top) + "px";
  }
  function showTip(html, x, y) { tip.innerHTML = html; tip.hidden = false; place(x, y); }
  function hideTip() { tip.hidden = true; pinned = null; }
  function bind(node, html, onSelect) {
    node.setAttribute("tabindex", "0");
    node.setAttribute("class", (node.getAttribute("class") || "") + " mark");
    node.setAttribute("aria-label", html().replace(/<br>/g, ". ").replace(/<[^>]+>/g, ""));
    node.addEventListener("pointermove", function (e) { if (e.pointerType === "mouse") showTip(html(), e.clientX, e.clientY); });
    node.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse" && pinned !== node) hideTip(); });
    node.addEventListener("focus", function () {
      var r = node.getBoundingClientRect(); showTip(html(), r.left + r.width / 2, r.top + r.height / 2);
      if (onSelect) onSelect();
    });
    node.addEventListener("blur", hideTip);
    node.addEventListener("click", function (e) {
      showTip(html(), e.clientX, e.clientY); pinned = node;
      if (onSelect) onSelect();
      e.stopPropagation();
    });
  }
  document.addEventListener("click", function () { if (pinned) hideTip(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") hideTip(); });
  window.addEventListener("scroll", function () { if (!tip.hidden) hideTip(); }, { passive: true });

  // ---------------------------------------------------------------- epidemic curve
  function legend(id, items) {
    var el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = items.map(function (it) {
      return "<span><i class=\"" + it[0] + "\"></i>" + esc(it[1]) + "</span>";
    }).join("");
  }
  function drawCurve() {
    var host = document.getElementById("c-curve"), W = host.clientWidth;
    if (!W) return;
    var weeks = D.curve.weeks, n = weeks.length;
    var show = state.curve === "both" ? DIS : [state.curve];
    var H = printing() ? Math.round(W * 0.31) : Math.round(Math.max(230, Math.min(440, W * 0.56)));
    var m = { l: 40, r: 10, t: 34, b: W < 520 || printing() ? 24 : 40 };
    legend("curve-legend", show.map(function (d) { return ["bar " + SHORT[d], T[d]]; })
      .map(function (x) { return [x[0].replace("bar ", ""), x[1]]; })
      .concat([["sw-hatch", T.lt5_long]]));
    var svg = svgFor(host, W, H, T.curve_title);
    var url = hatch(svg);
    var max = 1;
    weeks.forEach(function (w) {
      var t = 0; show.forEach(function (d) { t += cellDraw(w[d]); }); max = Math.max(max, t);
    });
    var top = yAxis(svg, m, W, H, max * 1.08, 5);
    var pw = W - m.l - m.r, bw = pw / n, ph = H - m.t - m.b;
    function y(v) { return m.t + ph * (1 - v / top); }
    // incomplete last week
    var last = n - 1;
    S("rect", { x: m.l + bw * last, y: m.t, width: bw, height: ph, "class": "incband" }, svg);
    T_(svg, m.l + bw * last + bw / 2, m.t - 4, T.incomplete, "lbl", "middle", 10.5);
    // bars
    var g = S("g", null, svg);
    weeks.forEach(function (w, i) {
      var base = 0, x = m.l + bw * i + bw * 0.12, bwi = bw * 0.76;
      show.forEach(function (d) {
        var c = w[d], v = cellDraw(c);
        if (c[1] === 0 && c[0] === 0) return;
        var r = S("rect", { x: x, y: y(base + v), width: bwi, height: Math.max(1, y(base) - y(base + v)), rx: 2,
          "class": c[1] === 0 ? "bar gm " + SHORT[d] + (i === last ? " inc" : "") : "gm stub",
          fill: c[1] === 0 ? null : url }, g);
        r.style.animationDelay = (i * 45) + "ms";
        bind(r, function () {
          return "<b>" + esc(w.wk) + "</b> · " + esc(fill(T.week_of, { date: fdate(w.start) })) + "<br>" +
            show.map(function (dd) { return esc(T[dd]) + ": <b>" + esc(cellText(w[dd])) + "</b>"; }).join("<br>") +
            (i === last ? "<br><span class=\"muted\">" + esc(T.incomplete) + "</span>" : "");
        });
        base += v;
      });
      var tot = 0, ok = true;
      show.forEach(function (d) { if (w[d][1] !== 0) ok = false; tot += cellDraw(w[d]); });
      if (ok && tot > 0 && bw > 26) T_(svg, x + bwi / 2, y(base) - 4, num(tot), "lbl strong gfade", "middle", 10.5);
    });
    // x labels
    var ax = S("g", { "class": "ax" }, svg);
    var every = bw < 34 ? 2 : 1;
    weeks.forEach(function (w, i) {
      if (i % every) return;
      var cx = m.l + bw * i + bw / 2;
      T_(ax, cx, H - m.b + 15, w.wk, "", "middle");
      if (W >= 520 && !printing()) T_(ax, cx, H - m.b + 29, fdate(w.start), "", "middle", 10);
    });
    // typhoon marker
    var t0 = day(weeks[0].start), ty = day(D.typhoon);
    var frac = (ty - t0) / (7 * 864e5);
    if (frac >= 0 && frac <= n) {
      var tx = m.l + bw * frac, tg = S("g", { "class": "typhoon gfade" }, svg);
      S("line", { x1: tx, x2: tx, y1: m.t - 18, y2: H - m.b }, tg);
      var r0 = 6, sx = tx, sy = m.t - 24;
      S("path", { d: "M" + (sx - r0) + " " + sy + "a" + r0 + " " + r0 + " 0 1 1 " + r0 + " " + r0 + "M" + (sx + r0) + " " + sy + "a" + r0 + " " + r0 + " 0 1 1 " + (-r0) + " " + (-r0) }, tg);
      var right = tx + 200 < W;
      T_(tg, right ? tx + 11 : tx - 11, m.t - 20, T.typhoon, "", right ? "start" : "end");
    }
  }

  // ---------------------------------------------------------------- threshold
  function drawThr() {
    var host = document.getElementById("c-thr"), W = host.clientWidth;
    if (!W) return;
    var weeks = D.thr.weeks, fc = D.forecast;
    var fweeks = fc ? fc.weeks : [];
    var slots = weeks.length + fweeks.length;
    var H = printing() ? Math.round(W * 0.31) : Math.round(Math.max(230, Math.min(310, W * 0.5)));
    var m = { l: 38, r: 10, t: 16, b: 32 };
    var items = [["den", T.dengue], ["den-above", T.above], ["line", T.threshold]];
    if (fc) items.push(["band", T.fc_label]);
    items.push(["sw-hatch", T.lt5_long]);
    legend("thr-legend", items);
    var svg = svgFor(host, W, H, T.thr_title);
    var url = hatch(svg);
    var max = 1;
    weeks.forEach(function (w) { max = Math.max(max, cellDraw(w.cell), w.thr); });
    fweeks.forEach(function (w) { max = Math.max(max, w.hi); });
    var top = yAxis(svg, m, W, H, max * 1.06, 5);
    var pw = W - m.l - m.r, bw = pw / slots, ph = H - m.t - m.b;
    function y(v) { return m.t + ph * (1 - v / top); }
    function cx(i) { return m.l + bw * i + bw / 2; }
    var last = weeks.length - 1;
    if (fc) {
      S("rect", { x: m.l + bw * weeks.length, y: m.t, width: bw * fweeks.length, height: ph, "class": "fc-zone" }, svg);
    }
    var g = S("g", null, svg);
    weeks.forEach(function (w, i) {
      var c = w.cell, v = cellDraw(c);
      if (c[1] === 0 && c[0] === 0) return;
      var r = S("rect", { x: m.l + bw * i + bw * 0.14, y: y(v), width: bw * 0.72, height: Math.max(1, y(0) - y(v)), rx: 2,
        "class": c[1] === 0 ? "bar gm den" + (w.above ? " above" : "") + (i === last ? " inc" : "") : "gm stub",
        fill: c[1] === 0 ? null : url }, g);
      r.style.animationDelay = (i * 30) + "ms";
      bind(r, function () {
        return "<b>" + esc(w.wk) + "</b> · " + esc(fill(T.week_of, { date: fdate(w.start) })) + "<br>" +
          esc(T.cases) + ": <b>" + esc(cellText(c)) + "</b><br>" + esc(T.threshold) + ": " + num(w.thr, 1) +
          (w.above ? "<br><b>" + esc(T.above) + "</b>" : "") +
          (i === last ? "<br><span class=\"muted\">" + esc(T.incomplete) + "</span>" : "");
      });
    });
    // threshold step line over data + forecast weeks
    var thr = weeks.map(function (w) { return w.thr; });
    var extra = fc ? fweeks.length : 0;
    for (var k = 0; k < extra; k++) thr.push(D.thr.future_thr[k].thr);
    var d = "";
    thr.forEach(function (v, i) {
      var x0 = m.l + bw * i, x1 = x0 + bw;
      d += (i ? "L" : "M") + x0.toFixed(1) + " " + y(v).toFixed(1) + "L" + x1.toFixed(1) + " " + y(v).toFixed(1);
    });
    S("path", { d: d, "class": "thr-line gfade" }, svg);
    if (fc) {
      var start = weeks.length - 1, pts = [[cx(start), y(cellDraw(weeks[start].cell))]];
      var up = "", lo = "";
      fweeks.forEach(function (f, i) {
        var x = cx(weeks.length + i);
        up += (i ? "L" : "M") + x.toFixed(1) + " " + y(f.hi).toFixed(1);
        lo = "L" + x.toFixed(1) + " " + y(f.lo).toFixed(1) + lo;
        pts.push([x, y(f.med)]);
      });
      S("path", { d: up + lo + "Z", "class": "fc-band gfade" }, svg);
      S("path", { d: "M" + pts.map(function (p) { return p[0].toFixed(1) + " " + p[1].toFixed(1); }).join("L"), "class": "fc-line gfade" }, svg);
      fweeks.forEach(function (f, i) {
        var dot = S("circle", { cx: cx(weeks.length + i), cy: y(f.med), r: 4.5, "class": "fc-dot gfade" }, svg);
        bind(dot, function () {
          return "<b>" + esc(f.wk) + "</b> · " + esc(T.fc_label) + "<br>" + num(f.med, 0) + " (" + num(f.lo, 0) + "–" + num(f.hi, 0) + ")";
        });
      });
    }
    var ax = S("g", { "class": "ax" }, svg);
    var every = Math.ceil(30 / bw);
    for (var i = 0; i < slots; i++) {
      if ((slots - 1 - i) % every) continue;
      var lab = i < weeks.length ? weeks[i].wk : fweeks[i - weeks.length].wk;
      T_(ax, cx(i), H - m.b + 15, lab, "", "middle");
    }
    T_(svg, m.l + 4, y(Math.max(thr[0], thr[1] || 0)) - 7, T.threshold, "lbl gfade", "start", 10.5).style.fill = "var(--thr)";
  }

  // ---------------------------------------------------------------- map
  function drawMap() {
    var host = document.getElementById("c-map"), W = host.clientWidth;
    if (!W) return;
    var M = D.map, vbw = M.vb[0], vbh = M.vb[1];
    var dis = state.mapd, metric = state.mapm, s = SHORT[dis];
    var H = Math.round(W * vbh / vbw);
    host.innerHTML = "";
    var svg = S("svg", { viewBox: "0 0 " + vbw + " " + vbh, width: W, height: H, focusable: "false" }, host);
    host.setAttribute("aria-label", document.getElementById("p-map-h").textContent);
    if (!RM && !drawn["c-map"]) svg.setAttribute("class", "grow");
    drawn["c-map"] = true;
    var url = hatch(svg);
    var g = S("g", { "class": s }, svg);
    var info = document.getElementById("map-info");
    var sel = null;
    function describe(f) {
      var x = f[dis], c = x.cell;
      var rank = x["rank_" + metric];
      return "<b>" + esc(f.name) + "</b><span class=\"muted\">" + esc(T[f.band]) + " · " + esc(T.population) + " " + num(f.pop) + "</span><br>" +
        esc(T[dis]) + ": <b>" + esc(cellText(c)) + "</b> " + esc(T.cases) +
        (x.rate !== null ? " · <b>" + num(x.rate, 1) + "</b> " + esc(T.per10k) : (c[1] ? " · " + esc(T.withheld) : "")) +
        (rank ? "<br><span class=\"muted\">" + esc(fill(T.tip_rank, { n: rank })) + "</span>" : "");
    }
    M.features.forEach(function (f, i) {
      var cls = f[dis]["cls_" + metric];
      var p = S("path", { d: f.d, "class": "brgy gfade " + (cls === "s" ? "" : "c" + cls), fill: cls === "s" ? url : null }, g);
      p.style.animationDelay = (i * 25) + "ms";
      bind(p, function () { return describe(f); }, function () {
        if (sel) sel.classList.remove("sel");
        sel = p; p.classList.add("sel");
        info.innerHTML = describe(f).replace("<br>", "<br>");
      });
    });
    // band labels
    var bands = {};
    M.features.forEach(function (f) { (bands[f.band] = bands[f.band] || []).push(f); });
    var fs = 12 * vbw / W;
    Object.keys(bands).forEach(function (b) {
      var list = bands[b], x = 0, y = 0;
      list.forEach(function (f) { x += f.cx; y += f.cy; });
      if (W > 300) {
        var t = T_(svg, x / list.length, y / list.length, T[b], "band-lbl", "middle");
        t.style.fontSize = fs + "px";
      }
    });
    // rank badges (top 3 by the selected metric)
    var top = M.features.filter(function (f) { var r = f[dis]["rank_" + metric]; return r && r <= 3; });
    var rg = S("g", { "class": "rank gfade" }, svg);
    top.forEach(function (f) {
      var r = 10 * vbw / W;
      S("circle", { cx: f.cx, cy: f.cy, r: r }, rg);
      var t = T_(rg, f.cx, f.cy, String(f[dis]["rank_" + metric]), "", "middle");
      t.style.fontSize = (12 * vbw / W) + "px";
    });
    // legend
    var br = M.breaks[dis][metric], dec = metric === "rate" ? 1 : 0, items = [];
    var lo = 0;
    for (var i = 0; i <= br.length; i++) {
      var label = i === 0 ? "≤ " + num(br[0], dec) : (i === br.length ? "> " + num(br[i - 1], dec) : num(br[i - 1], dec) + "–" + num(br[i], dec));
      items.push("<span><i style=\"background:var(--" + s + "-" + (i + 1) + ")\"></i>" + esc(label) + "</span>");
    }
    items.push("<span><i style=\"background:var(--zero);border:1px solid var(--border)\"></i>" + esc(T.zero) + "</span>");
    items.push("<span><i class=\"sw-hatch\"></i>" + esc(T.lt5_long) + "</span>");
    document.getElementById("map-legend").innerHTML = items.join("");
    document.getElementById("map-sub").textContent = metric === "rate" ? T.map_sub_rate : T.map_sub_count;
  }

  // ---------------------------------------------------------------- pyramid
  function drawPyr() {
    var host = document.getElementById("c-pyr"), W = host.clientWidth;
    if (!W) return;
    var P = D.pyramid, dis = state.pyr, groups = P.groups, n = groups.length;
    var rowH = printing() ? 13 : W < 420 ? 30 : 32, m = { t: 22, b: 24 }, H = m.t + m.b + rowH * n;
    var mid = 44, side = (W - mid) / 2 - 30;
    legend("pyr-legend", [["male", T.male], ["female", T.female], ["sw-hatch", T.lt5_long]]);
    var svg = svgFor(host, W, H, T.pyr_title);
    var url = hatch(svg);
    var vals = [];
    ["M", "F"].forEach(function (s) { P[dis][s].forEach(function (c) { vals.push(cellDraw(c)); }); });
    var max = Math.max.apply(null, vals) || 1;
    var step = niceStep(max, 3), top = Math.ceil(max / step) * step;
    var cxl = 30 + side, cxr = cxl + mid;
    var ax = S("g", { "class": "ax" }, svg);
    for (var v = step; v <= top + 1e-9; v += step) {
      var dx = side * v / top;
      S("line", { x1: cxl - dx, x2: cxl - dx, y1: m.t, y2: H - m.b, "class": "gridl" }, ax);
      S("line", { x1: cxr + dx, x2: cxr + dx, y1: m.t, y2: H - m.b, "class": "gridl" }, ax);
      T_(ax, cxl - dx, H - m.b + 15, num(v), "", "middle", 10.5);
      T_(ax, cxr + dx, H - m.b + 15, num(v), "", "middle", 10.5);
    }
    T_(svg, cxl, 13, T.male, "lbl strong", "end");
    T_(svg, cxr, 13, T.female, "lbl strong", "start");
    for (var i = 0; i < n; i++) {
      var gi = n - 1 - i, yy = m.t + rowH * i, bh = rowH * 0.72, by = yy + (rowH - bh) / 2;
      T_(svg, (cxl + cxr) / 2, by + bh / 2 + 4, groups[gi], "lbl strong", "middle");
      ["M", "F"].forEach(function (s) {
        var c = P[dis][s][gi], v = cellDraw(c), len = side * v / top;
        if (c[1] === 0 && c[0] === 0) return;
        var x = s === "M" ? cxl - len : cxr;
        var r = S("rect", { x: x, y: by, width: Math.max(1, len), height: bh, rx: 3,
          "class": c[1] === 0 ? "gmx " + (s === "M" ? "male" : "female") : "gmx stub", fill: c[1] === 0 ? null : url }, svg);
        r.style.transformOrigin = s === "M" ? "100% 50%" : "0% 50%";
        r.style.animationDelay = (i * 50) + "ms";
        bind(r, function () {
          return "<b>" + esc(T[dis]) + "</b> · " + esc(groups[gi]) + " · " + esc(s === "M" ? T.male : T.female) + "<br>" + esc(T.cases) + ": <b>" + esc(cellText(c)) + "</b>" +
            (c[1] === 2 ? "<br><span class=\"muted\">" + esc(T.x_long) + "</span>" : "");
        });
        var lx = s === "M" ? x - 5 : x + len + 5;
        T_(svg, lx, by + bh / 2 + 4, cellText(c), "lbl gfade", s === "M" ? "end" : "start", 11);
      });
    }
  }

  // ---------------------------------------------------------------- forest
  function wrap(text, max) {
    if (text.length <= max) return [text];
    var words = text.indexOf(" ") >= 0 ? text.split(" ") : null, lines = [], cur = "";
    if (!words) { for (var i = 0; i < text.length; i += max) lines.push(text.slice(i, i + max)); return lines.slice(0, 2); }
    words.forEach(function (w) {
      if ((cur + " " + w).trim().length > max && cur) { lines.push(cur); cur = w; } else cur = (cur + " " + w).trim();
    });
    if (cur) lines.push(cur);
    if (lines.length > 2) lines = [lines[0], lines.slice(1).join(" ")];
    return lines;
  }
  function drawForest() {
    var host = document.getElementById("c-forest"), W = host.clientWidth;
    if (!W) return;
    var rows = D.forest, PR = printing(), narrow = W < 400 && !PR, cjk = D.lang === "zh";
    var fsz = PR ? 8.5 : 11.5, lh = PR ? 9 : 13;
    var labW = PR ? W * 0.5 : Math.min(190, Math.max(118, W * 0.4)), valW = narrow ? 0 : (PR ? 70 : 92);
    var rowH = printing() ? 12.5 : narrow ? 36 : 30, m = { t: 6, b: PR ? 18 : 40 };
    var H = m.t + m.b + rowH * rows.length;
    var svg = svgFor(host, W, H, T.forest_title);
    var x0 = labW + 6, x1 = W - valW - 10, lmin = Math.log(0.1), lmax = Math.log(10);
    function X(v) { return x0 + (x1 - x0) * (Math.log(v) - lmin) / (lmax - lmin); }
    var ax = S("g", { "class": "ax" }, svg);
    (PR ? [0.1, 0.5, 1, 5, 10] : [0.1, 0.2, 0.5, 1, 2, 5, 10]).forEach(function (v) {
      S("line", { x1: X(v), x2: X(v), y1: m.t, y2: H - m.b, "class": "gridl" }, ax);
      T_(ax, X(v), H - m.b + 14, String(v), "", "middle", 10.5);
    });
    if (!PR) {
      T_(svg, X(1) - 6, H - 6, "← " + T.protective, "lbl", "end", 10.5);
      T_(svg, X(1) + 6, H - 6, T.risk + " →", "lbl", "start", 10.5);
    }
    var maxc = Math.floor(labW / (cjk ? fsz + 1 : fsz * 0.56));
    rows.forEach(function (r, i) {
      var y = m.t + rowH * i, cy = y + rowH / 2;
      var g = S("g", { "class": "f-row" }, svg);
      S("rect", { x: 0, y: y, width: W, height: rowH, "class": "f-bg" }, g);
      var lines = wrap(T["ex_" + r.key], maxc);
      lines.forEach(function (ln, j) {
        T_(g, 4, cy + 3 + (j - (lines.length - 1) / 2) * lh, ln, r.kind === "adjusted" ? "lbl strong" : "lbl", "start", fsz);
      });
      S("line", { x1: X(r.lo), x2: X(r.hi), y1: cy, y2: cy, "class": "f-ci gmx" }, g).style.transformOrigin = X(r.or) + "px 0";
      var pt;
      if (r.kind === "adjusted") {
        var s = 7;
        pt = S("path", { d: "M" + X(r.or) + " " + (cy - s) + "l" + s + " " + s + "l" + (-s) + " " + s + "l" + (-s) + " " + (-s) + "Z", "class": "f-pt f-adjusted gfade" }, g);
      } else {
        pt = S("rect", { x: X(r.or) - 5.5, y: cy - 5.5, width: 11, height: 11, rx: 2, "class": "f-pt f-" + r.kind + " gfade" }, g);
      }
      pt.style.animationDelay = (i * 60) + "ms";
      bind(pt, function () {
        return "<b>" + esc(T["ex_" + r.key]) + "</b><br>" + esc(fill(T.or_ci, { or: r.or.toFixed(2), lo: r.lo.toFixed(2), hi: r.hi.toFixed(2) }));
      });
      if (!narrow) T_(g, W - 4, cy + 3, r.or.toFixed(2) + " (" + r.lo.toFixed(2) + "–" + r.hi.toFixed(2) + ")", "lbl", "end", PR ? 8 : 11);
    });
    S("line", { x1: X(1), x2: X(1), y1: m.t, y2: H - m.b, "class": "f-one" }, svg);
  }

  // ---------------------------------------------------------------- KPIs count-up
  function countUp() {
    var els = document.querySelectorAll(".kpi-val");
    if (RM) return;
    var t0 = null, dur = 1300;
    var list = Array.prototype.map.call(els, function (el) {
      return { el: el, n: parseFloat(el.getAttribute("data-n")), d: +el.getAttribute("data-dec"), s: el.getAttribute("data-suffix") || "", final: el.textContent };
    });
    function frame(ts) {
      if (t0 === null) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      list.forEach(function (o) { o.el.textContent = p >= 1 ? o.final : num(o.n * e, o.d) + o.s; });
      if (p < 1) requestAnimationFrame(frame);
    }
    list.forEach(function (o) { o.el.textContent = num(0, o.d) + o.s; });
    requestAnimationFrame(frame);
  }

  // ---------------------------------------------------------------- wiring
  var charts = { "c-curve": drawCurve, "c-thr": drawThr, "c-map": drawMap, "c-pyr": drawPyr, "c-forest": drawForest };
  var widths = {};
  function drawAll(force) {
    Object.keys(charts).forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      var w = el.clientWidth;
      if (force || Math.abs((widths[id] || 0) - w) > 2) { widths[id] = w; charts[id](); }
    });
  }
  var redrawFor = { curve: ["c-curve"], mapd: ["c-map"], mapm: ["c-map"], pyr: ["c-pyr"] };
  document.querySelectorAll(".seg button").forEach(function (b) {
    b.addEventListener("click", function () {
      var k = b.getAttribute("data-k");
      state[k] = b.getAttribute("data-v");
      b.parentNode.querySelectorAll("button").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      hideTip();
      redrawFor[k].forEach(function (id) { charts[id](); });
    });
  });
  // panel entrance stagger
  document.querySelectorAll(".kpi, .panel").forEach(function (el, i) { el.style.setProperty("--i", i); });
  // theme
  var themeBtn = document.getElementById("theme");
  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function syncTheme() { themeBtn.setAttribute("aria-pressed", isDark() ? "true" : "false"); }
  try { var saved = localStorage.getItem("bantay-theme"); if (saved) root.setAttribute("data-theme", saved); } catch (e) { }
  syncTheme();
  themeBtn.addEventListener("click", function () {
    var next = isDark() ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("bantay-theme", next); } catch (e) { }
    syncTheme();
  });
  // print: switch to the print layout first so charts are drawn at print width
  window.addEventListener("beforeprint", function () { root.classList.add("printing"); drawAll(true); });
  window.addEventListener("afterprint", function () { root.classList.remove("printing"); drawAll(true); });
  document.getElementById("print").addEventListener("click", function () { window.print(); });

  drawAll(true);
  countUp();
  if (window.ResizeObserver) {
    var pending = null;
    var ro = new ResizeObserver(function () {
      if (pending) cancelAnimationFrame(pending);
      pending = requestAnimationFrame(function () { drawAll(false); });
    });
    Object.keys(charts).forEach(function (id) { var el = document.getElementById(id); if (el) ro.observe(el); });
  } else {
    window.addEventListener("resize", function () { drawAll(false); });
  }
})();
"""


def main(argv: list[str] | None = None) -> None:
    """Command-line entry point: write one language's dashboard to a directory."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lang", choices=LANGS, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    print(build_dashboard(args.lang, args.out_dir))


if __name__ == "__main__":
    main()
