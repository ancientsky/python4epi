"""Generate every synthetic dataset of the Philippines edition (Santa Luz City).

**All Santa Luz data are synthetic.** Santa Luz City, the Province of Kalinaw,
Typhoon Amihan, the Marilag River, every person, name, phone number, address and
count produced here are invented for teaching.  The only real-world file is
``ph_regions_stats.csv``, which is *exported* (never estimated) from the research
compiled for the book (``book_ph/research/ph_surveillance_research_2026-11-09.json``).

Story (see ``book_ph/PRODUCTION.md`` §3): Typhoon Amihan makes landfall on
Saturday 18 July 2026; the Marilag River floods the riverside barangays for
three days (18–20 July) and clean-up runs into early August.  A leptospirosis
outbreak (common source, continuing exposure) follows in late July, then a
propagated dengue surge from early August.  The data freeze is Wednesday
30 September 2026, the day the City Mayor asks for the dashboard.

Files written to ``data/synthetic/ph/`` (schema and headline numbers in
``README.md``):

- ``santa_luz_barangays.csv`` / ``santa_luz_barangays.geojson``
- ``santa_luz_linelist_raw.csv`` (messy, fake PII) and ``santa_luz_linelist.csv``
- ``lepto_case_control.csv``
- ``santa_luz_dengue_weekly.csv``
- ``signals_717.csv``
- ``ph_regions_stats.csv`` (real, sourced)

How it works
------------
1. A synthetic population of all ~186,000 residents is simulated (age, sex,
   barangay) together with their flood exposures (wading, boots, wounds,
   clean-up work, doxycycline prophylaxis).  Leptospirosis is drawn from a
   logistic model whose odds ratios are the *true design values* of the
   case-control study.
2. Weekly dengue counts 2019-W01 … 2026-W40 are drawn from a negative-binomial
   model driven by rainfall lagged 5–9 weeks, plus a post-typhoon surge.  The
   2026 dengue cases are drawn person by person from the population.
3. The true line list is then (a) cleaned into ``santa_luz_linelist.csv`` and
   (b) messed up into ``santa_luz_linelist_raw.csv`` with a hidden mapping, so a
   correct cleaning of the raw file reproduces the clean file exactly.

The script is deterministic: one ``numpy.random.Generator`` seeded with
:data:`SEED`, no wall-clock dependence.  Run it with::

    uv run python data/synthetic/ph/generate_santa_luz.py
"""

from __future__ import annotations

import json
import math
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths and reproducibility
# ---------------------------------------------------------------------------
SEED = 20260755  # chosen from a scan of 20260718–20260757 (see README, "Seed")
OUT_DIR = Path(__file__).resolve().parent
REPO_ROOT = OUT_DIR.parents[2]
RESEARCH_JSON = REPO_ROOT / "book_ph" / "research" / "ph_surveillance_research_2026-11-09.json"

# ---------------------------------------------------------------------------
# Story calendar
# ---------------------------------------------------------------------------
LANDFALL = date(2026, 7, 18)  # Sat: Typhoon Amihan makes landfall
FLOOD_DAYS = 3  # 18–20 July: waist-deep water in riverside barangays
LINELIST_START = date(2026, 7, 20)  # Mon, ISO 2026-W30: enhanced surveillance starts
FREEZE = date(2026, 9, 30)  # Wed: data freeze (Mayor asks for "one screen")
EXCEL_EPOCH = date(1899, 12, 30)

# ---------------------------------------------------------------------------
# Barangays: (name, band, flood depth in metres during Amihan)
# Grid rows (south → north): coastal, riverside (Marilag valley floor), upland.
# ---------------------------------------------------------------------------
BARANGAYS: list[tuple[str, str, float]] = [
    ("Ilog", "riverside", 1.3),
    ("Tabing-Ilog", "riverside", 1.4),
    ("Pampang", "riverside", 1.1),
    ("Poblacion", "riverside", 0.8),
    ("Santo Niño", "riverside", 1.0),
    ("San Isidro", "riverside", 0.9),
    ("Bagong Silang", "riverside", 1.2),
    ("Sapa", "riverside", 0.7),
    ("San Pedro", "coastal", 0.3),
    ("Baybay", "coastal", 0.5),
    ("Dalampasigan", "coastal", 0.4),
    ("Pantalan", "coastal", 0.6),
    ("Talaba", "coastal", 0.3),
    ("Buhangin", "coastal", 0.2),
    ("Laot", "coastal", 0.4),
    ("Wawa", "coastal", 0.6),
    ("Bukid", "upland", 0.1),
    ("Burol", "upland", 0.0),
    ("Mataas na Lupa", "upland", 0.0),
    ("Kawayanan", "upland", 0.1),
    ("San Roque", "upland", 0.0),
    ("Maligaya", "upland", 0.1),
    ("Bagong Pag-asa", "upland", 0.0),
    ("Talahib", "upland", 0.1),
]
BANDS = ("riverside", "coastal", "upland")
CITY_POPULATION = 186_000
POP_RANGE = {"riverside": (9_500, 14_000), "coastal": (6_000, 9_000), "upland": (3_000, 5_500)}
HOUSEHOLD_SIZE = {"riverside": 4.3, "coastal": 4.8, "upland": 4.5}

# Made-up coordinate frame: a lon/lat box in the open Philippine Sea, ~600 km
# east of Luzon, where there is no land.  It cannot be mistaken for a real place.
FRAME_LON0 = 130.10
FRAME_LAT0 = 14.80
CELL_W_DEG = 0.025
ROW_H_DEG = (0.026, 0.024, 0.040)  # coastal, riverside, upland
N_COLS = 8

# ---------------------------------------------------------------------------
# Leptospirosis design (true conditional odds ratios of the logistic model)
# ---------------------------------------------------------------------------
TRUE_OR: dict[str, float] = {
    "waded_without_boots": 6.0,
    "waded_with_boots": 1.8,
    "skin_wound": 2.0,
    "doxy_prophylaxis": 0.30,
    "cleanup_work": 1.6,
    "male": 1.3,
    "rats_near_home": 1.0,
    "flood_depth_per_m": 5.0,
}
LEPTO_TARGET_CASES = 235.0  # expected notified leptospirosis cases (intercept is calibrated)
INCUBATION_MEDIAN = 9.5  # days; log-normal, sd(log) 0.45 → mode ≈ 7.8 d, clipped to 2–30
INCUBATION_SDLOG = 0.45

# ---------------------------------------------------------------------------
# Dengue design
# ---------------------------------------------------------------------------
WEEKLY_FIRST = (2019, 1)
WEEKLY_LAST = (2026, 39)  # last week written to the weekly file
SIM_LAST = (2026, 40)  # simulated one more week for the line list (onsets 28–30 Sep)
RAIN_LAG_WEIGHTS = {5: 0.1, 6: 0.2, 7: 0.4, 8: 0.2, 9: 0.1}
DENGUE_BASE = 2.5
DENGUE_RAIN_COEF = 0.11
NB_DISPERSION = 20.0
YEAR_MULT = {2019: 1.7, 2020: 1.0, 2021: 0.5, 2022: 1.1, 2023: 0.9, 2024: 1.0, 2025: 0.95,
             2026: 0.75}
COVID_START = (2020, 12)  # from 2020-W12 (lockdowns) the 2020 multiplier is COVID_MULT
COVID_MULT = 0.45
SURGE_TOTAL = 330.0  # extra expected dengue cases after Amihan (gamma kernel)
SURGE_SHAPE, SURGE_SCALE = 5.0, 1.5  # weeks after landfall week; mode at 6 weeks
AMIHAN_RAIN_MM = 390.0
THRESHOLD_YEARS = (2022, 2023, 2024, 2025)  # non-epidemic, post-COVID baseline years

AGE_GROUPS = [(0, 4, "0-4"), (5, 14, "5-14"), (15, 24, "15-24"), (25, 44, "25-44"),
              (45, 64, "45-64"), (65, 200, "65+")]

# Population pyramid weights for 5-year groups 0-4 … 80+ (synthetic, young city)
PYRAMID = np.array([10.5, 10.3, 10.0, 9.6, 9.0, 8.4, 7.6, 6.8, 6.0, 5.2, 4.4, 3.6, 2.8, 2.0,
                    1.4, 0.9, 0.8])


# ===========================================================================
# Small helpers
# ===========================================================================
def iso_weeks(first: tuple[int, int], last: tuple[int, int]) -> list[tuple[int, int]]:
    """List ISO (year, week) pairs from *first* to *last* inclusive.

    Parameters
    ----------
    first, last : tuple of int
        ISO year and week of the first and last week.

    Returns
    -------
    list of tuple of int
        Consecutive ISO weeks.
    """
    start = date.fromisocalendar(first[0], first[1], 1)
    stop = date.fromisocalendar(last[0], last[1], 1)
    if stop < start:
        raise ValueError("last week precedes first week")
    out = []
    day = start
    while day <= stop:
        iso = day.isocalendar()
        out.append((iso.year, iso.week))
        day += timedelta(days=7)
    return out


def age_group(age: float | None) -> str | None:
    """Return the age-group label used in every Santa Luz file.

    Parameters
    ----------
    age : int or None
        Age in completed years; ``None``/NaN gives ``None``.

    Returns
    -------
    str or None
        One of ``0-4``, ``5-14``, ``15-24``, ``25-44``, ``45-64``, ``65+``.
    """
    if age is None or (isinstance(age, float) and math.isnan(age)):
        return None
    for lo, hi, label in AGE_GROUPS:
        if lo <= age <= hi:
            return label
    raise ValueError(f"age out of range: {age}")


def nb_draw(rng: np.random.Generator, mean: np.ndarray | float, k: float = NB_DISPERSION) -> Any:
    """Draw negative-binomial counts with the given mean and dispersion *k*.

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    mean : array-like
        Expected counts (> 0).
    k : float
        Dispersion; variance = mean + mean**2 / k.

    Returns
    -------
    numpy.ndarray or int
        Counts.
    """
    mean = np.asarray(mean, dtype=float)
    return rng.negative_binomial(k, k / (k + mean))


def _int_col(values: Any) -> pd.Series:
    """Return a nullable integer Series (blank in CSV when missing)."""
    return pd.Series(values, dtype="Int64")


def _write_csv(df: pd.DataFrame, path: Path, header_line: str | None = None) -> None:
    """Write *df* as UTF-8 CSV with Unix newlines (byte-stable across platforms)."""
    with path.open("w", encoding="utf-8", newline="") as fh:
        if header_line is not None:
            fh.write(header_line + "\n")
        df.to_csv(fh, index=False, lineterminator="\n")


# ===========================================================================
# 1. Barangays and geometry
# ===========================================================================
def _lattice(rng: np.random.Generator) -> np.ndarray:
    """Jittered (N_COLS+1) x 4 lattice of polygon corners in lon/lat."""
    ys = FRAME_LAT0 + np.concatenate([[0.0], np.cumsum(ROW_H_DEG)])
    pts = np.zeros((N_COLS + 1, 4, 2))
    for c in range(N_COLS + 1):
        for r in range(4):
            dx = 0.0 if c in (0, N_COLS) else rng.uniform(-0.22, 0.22) * CELL_W_DEG
            h = ROW_H_DEG[min(r, 2)]
            dy = rng.uniform(-0.18, 0.18) * h if 0 < c < N_COLS or 0 < r < 3 else 0.0
            pts[c, r] = (FRAME_LON0 + c * CELL_W_DEG + dx, ys[r] + dy)
    return pts


def _edge_midpoint(rng: np.random.Generator, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Midpoint of segment a–b pushed sideways a little (organic boundaries)."""
    mid = (a + b) / 2
    d = b - a
    normal = np.array([-d[1], d[0]])
    return mid + normal * rng.uniform(-0.12, 0.12)


def build_barangay_polygons(rng: np.random.Generator) -> list[list[list[float]]]:
    """Build 24 non-overlapping polygons (8 columns x 3 bands) sharing edges.

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.

    Returns
    -------
    list
        One closed exterior ring (counter-clockwise, ``[lon, lat]`` pairs) per
        barangay, in the order of :data:`BARANGAYS`.
    """
    pts = _lattice(rng)
    mids: dict[tuple[tuple[int, int], tuple[int, int]], np.ndarray] = {}

    def mid(p: tuple[int, int], q: tuple[int, int]) -> np.ndarray:
        key = (min(p, q), max(p, q))
        if key not in mids:
            mids[key] = _edge_midpoint(rng, pts[key[0]], pts[key[1]])
        return mids[key]

    band_row = {"coastal": 0, "riverside": 1, "upland": 2}
    col_in_band = {b: 0 for b in BANDS}
    rings = []
    for _, band, _ in BARANGAYS:
        r = band_row[band]
        c = col_in_band[band]
        col_in_band[band] += 1
        corners = [(c, r), (c + 1, r), (c + 1, r + 1), (c, r + 1)]
        ring = []
        for i, p in enumerate(corners):
            q = corners[(i + 1) % 4]
            ring.append(pts[p])
            ring.append(mid(p, q))
        ring.append(ring[0])
        rings.append([[round(float(x), 5), round(float(y), 5)] for x, y in ring])
    return rings


def _ring_area_km2(ring: list[list[float]]) -> float:
    """Planar (shoelace) area of a lon/lat ring in km², equirectangular at the frame."""
    kx = 111.32 * math.cos(math.radians(FRAME_LAT0 + 0.045))
    ky = 110.57
    xs = [p[0] * kx for p in ring]
    ys = [p[1] * ky for p in ring]
    s = sum(xs[i] * ys[i + 1] - xs[i + 1] * ys[i] for i in range(len(ring) - 1))
    return abs(s) / 2


def _ring_centroid(ring: list[list[float]]) -> tuple[float, float]:
    """Area-weighted centroid of a simple polygon ring (lon, lat)."""
    a = cx = cy = 0.0
    for i in range(len(ring) - 1):
        x0, y0 = ring[i]
        x1, y1 = ring[i + 1]
        cross = x0 * y1 - x1 * y0
        a += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    a /= 2
    return cx / (6 * a), cy / (6 * a)


def _scale_to_total(raw: np.ndarray, total: int) -> np.ndarray:
    """Scale positive numbers to integers summing to *total* (largest remainder)."""
    exact = raw / raw.sum() * total
    base = np.floor(exact).astype(int)
    order = np.argsort(-(exact - base), kind="stable")
    base[order[: total - base.sum()]] += 1
    return base


def build_barangays(rng: np.random.Generator) -> tuple[pd.DataFrame, list[list[list[float]]]]:
    """Create the barangay table and polygons.

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.

    Returns
    -------
    (pandas.DataFrame, list)
        Barangay attributes and the polygon rings (same order).
    """
    rings = build_barangay_polygons(rng)
    raw_pop = np.array([rng.uniform(*POP_RANGE[band]) for _, band, _ in BARANGAYS])
    pop = _scale_to_total(raw_pop, CITY_POPULATION)
    rows = []
    for i, ((name, band, depth), ring) in enumerate(zip(BARANGAYS, rings, strict=True)):
        lon, lat = _ring_centroid(ring)
        area = _ring_area_km2(ring)
        rows.append({
            "barangay_id": f"SL{i + 1:02d}",
            "barangay": name,
            "band": band,
            "population": int(pop[i]),
            "households": round(pop[i] / HOUSEHOLD_SIZE[band]),
            "area_km2": round(area, 2),
            "density_per_km2": round(pop[i] / area),
            "centroid_lon": round(lon, 5),
            "centroid_lat": round(lat, 5),
            "flood_depth_m": depth,
        })
    return pd.DataFrame(rows), rings


def barangay_geojson(brgy: pd.DataFrame, rings: list[list[list[float]]]) -> str:
    """Serialise the barangays as a GeoJSON FeatureCollection (one feature per line).

    Parameters
    ----------
    brgy : pandas.DataFrame
        Barangay table.
    rings : list
        Polygon rings in the same order.

    Returns
    -------
    str
        GeoJSON text (RFC 7946, WGS 84 lon/lat).
    """
    feats = []
    for row, ring in zip(brgy.to_dict("records"), rings, strict=True):
        props = {k: row[k] for k in ("barangay_id", "barangay", "band", "population",
                                     "flood_depth_m")}
        feats.append(json.dumps({"type": "Feature", "properties": props,
                                 "geometry": {"type": "Polygon", "coordinates": [ring]}},
                                ensure_ascii=False))
    head = ('{"type": "FeatureCollection", "name": "santa_luz_barangays", '
            '"note": "SYNTHETIC: fictional Santa Luz City; coordinates are a made-up '
            'frame in the open Philippine Sea, not a real place",\n"features": [\n')
    return head + ",\n".join(feats) + "\n]}\n"


# ===========================================================================
# 2. Synthetic population with flood exposures and leptospirosis
# ===========================================================================
def simulate_population(rng: np.random.Generator, brgy: pd.DataFrame) -> pd.DataFrame:
    """Simulate every resident with flood exposures and leptospirosis risk.

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    brgy : pandas.DataFrame
        Barangay table from :func:`build_barangays`.

    Returns
    -------
    pandas.DataFrame
        One row per resident: ``brgy_idx``, ``age``, ``male``, exposures and
        ``lepto`` (drawn from the logistic model with :data:`TRUE_OR`).
    """
    brgy_idx = np.repeat(np.arange(len(brgy)), brgy["population"].to_numpy())
    n = len(brgy_idx)
    group = rng.choice(len(PYRAMID), size=n, p=PYRAMID / PYRAMID.sum())
    age = group * 5 + rng.integers(0, 5, size=n)
    age = np.where(group == len(PYRAMID) - 1, 80 + rng.integers(0, 15, size=n), age)
    male = rng.random(n) < 0.5

    band = brgy["band"].to_numpy()[brgy_idx]
    depth = brgy["flood_depth_m"].to_numpy()[brgy_idx]
    depth_f = np.clip(depth / 1.2, 0, 1)
    band_cleanup = np.select([band == "riverside", band == "coastal"], [1.0, 0.5], 0.15)

    adult = (age >= 15) & (age <= 64)
    p_cleanup = np.where(adult, np.where(male, 0.45, 0.12), np.where(age >= 65, 0.04, 0.0))
    cleanup = rng.random(n) < p_cleanup * band_cleanup

    p_wade = np.select(
        [cleanup, adult, (age >= 5) & (age <= 14), age >= 65],
        [np.minimum(0.90, 0.35 + 0.45 * depth_f), np.where(male, 0.45, 0.10) * depth_f,
         0.10 * depth_f, 0.15 * depth_f],
        0.02 * depth_f,
    )
    waded = rng.random(n) < p_wade
    boots = waded & (rng.random(n) < np.where(cleanup, 0.40, 0.20))
    wound = rng.random(n) < np.where(cleanup, 0.35, 0.18)
    p_doxy = np.select([band == "riverside", band == "coastal"], [0.12, 0.05], 0.01)
    p_doxy = np.where(cleanup, 0.30, p_doxy)
    doxy = (age >= 8) & (rng.random(n) < p_doxy)
    rats = rng.random(n) < np.select([band == "riverside", band == "coastal"], [0.45, 0.35], 0.55)

    lin = (math.log(TRUE_OR["waded_without_boots"]) * (waded & ~boots)
           + math.log(TRUE_OR["waded_with_boots"]) * boots
           + math.log(TRUE_OR["skin_wound"]) * wound
           + math.log(TRUE_OR["doxy_prophylaxis"]) * doxy
           + math.log(TRUE_OR["cleanup_work"]) * cleanup
           + math.log(TRUE_OR["male"]) * male
           + math.log(TRUE_OR["rats_near_home"]) * rats
           + math.log(TRUE_OR["flood_depth_per_m"]) * depth)
    alpha = _calibrate_intercept(lin, LEPTO_TARGET_CASES)
    p = 1 / (1 + np.exp(-(alpha + lin)))
    lepto = rng.random(n) < p
    return pd.DataFrame({
        "brgy_idx": brgy_idx, "age": age, "male": male, "cleanup": cleanup, "waded": waded,
        "boots": boots, "wound": wound, "doxy": doxy, "rats": rats, "lepto": lepto,
    })


def _calibrate_intercept(lin: np.ndarray, target: float) -> float:
    """Bisection for the logistic intercept giving *target* expected cases."""
    lo, hi = -20.0, 0.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if (1 / (1 + np.exp(-(mid + lin)))).sum() > target:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# ===========================================================================
# 3. Case records (truth)
# ===========================================================================
def _lepto_exposure_offset(rng: np.random.Generator, cleanup: bool, waded: bool) -> int:
    """Days after landfall of the infecting exposure (flood 0–2, clean-up 3–15)."""
    if cleanup and rng.random() < 0.7:
        days = np.arange(3, 16)
        w = np.exp(-(days - 3) / 4.0)
        return int(rng.choice(days, p=w / w.sum()))
    if waded or cleanup:
        return int(rng.integers(0, FLOOD_DAYS))
    return int(rng.integers(0, 12))


def lepto_cases(rng: np.random.Generator, pop: pd.DataFrame) -> pd.DataFrame:
    """Turn diseased residents into leptospirosis case records (truth).

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    pop : pandas.DataFrame
        Population from :func:`simulate_population`.

    Returns
    -------
    pandas.DataFrame
        Truth rows with dates, severity, laboratory and outcome fields.
    """
    rows = []
    for pid, r in pop[pop["lepto"]].iterrows():
        expo = LANDFALL + timedelta(days=_lepto_exposure_offset(rng, r.cleanup, r.waded))
        inc = int(np.clip(round(rng.lognormal(math.log(INCUBATION_MEDIAN), INCUBATION_SDLOG)),
                          2, 30))
        onset = expo + timedelta(days=inc)
        older = r.age >= 50
        hosp = rng.random() < (0.75 if older else 0.62)
        p_die = (0.20 if older else 0.10) if hosp else 0.01
        died = rng.random() < p_die
        consult = onset + timedelta(days=1 + int(rng.poisson(2.0)) + int(died))
        backlog = date(2026, 7, 27) <= consult <= date(2026, 8, 3)
        report = consult + timedelta(days=int(rng.poisson(1.0)) + (int(rng.poisson(2.0))
                                                                     if backlog else 0))
        rdt_pos = rng.random() < 0.75 * 0.60
        lab_tested = rng.random() < (0.70 if hosp else 0.30)
        lab_pos = lab_tested and rng.random() < 0.80
        lab_date = consult + timedelta(days=int(rng.integers(10, 26))) if lab_pos else None
        rows.append({
            "pid": pid, "disease": "leptospirosis", "date_onset": onset,
            "date_consult": consult, "date_report": report, "rdt_pos": rdt_pos,
            "lab_date": lab_date, "hospitalised": int(hosp), "died": int(died),
            "dengue_severity": None, "waded_floodwater": int(r.waded),
            "cleanup_work": int(r.cleanup),
        })
    return pd.DataFrame(rows)


def dengue_weights(pop: pd.DataFrame, brgy: pd.DataFrame) -> np.ndarray:
    """Per-resident relative dengue risk (band x age); lepto cases excluded.

    Parameters
    ----------
    pop, brgy : pandas.DataFrame
        Population and barangay tables.

    Returns
    -------
    numpy.ndarray
        Sampling probabilities summing to 1.
    """
    band = brgy["band"].to_numpy()[pop["brgy_idx"].to_numpy()]
    w_band = np.select([band == "riverside", band == "coastal"], [1.0, 1.35], 0.22)
    age = pop["age"].to_numpy()
    w_age = np.select([age <= 4, age <= 14, age <= 24, age <= 44, age <= 64],
                      [0.6, 1.7, 1.5, 0.8, 0.5], 0.4)
    w = w_band * w_age * (~pop["lepto"].to_numpy())
    return w / w.sum()


def dengue_cases(rng: np.random.Generator, pop: pd.DataFrame, brgy: pd.DataFrame,
                 counts_by_week: dict[tuple[int, int], int]) -> pd.DataFrame:
    """Draw dengue cases person by person for the line-list weeks (truth).

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    pop, brgy : pandas.DataFrame
        Population and barangay tables.
    counts_by_week : dict
        Number of cases by ISO (year, week) of onset (2026-W40: 28–30 Sep only).

    Returns
    -------
    pandas.DataFrame
        Truth rows (before truncation by the data freeze).
    """
    total = sum(counts_by_week.values())
    pids = rng.choice(len(pop), size=total, replace=False, p=dengue_weights(pop, brgy))
    rows = []
    i = 0
    for (yr, wk), n in counts_by_week.items():
        max_day = 3 if (yr, wk) == SIM_LAST else 7
        for _ in range(n):
            pid = int(pids[i])
            i += 1
            onset = date.fromisocalendar(yr, wk, 1) + timedelta(days=int(rng.integers(0, max_day)))
            age = int(pop.at[pid, "age"])
            p_ws = 0.40 if age < 15 else 0.32
            u = rng.random()
            sev = "severe" if u < 0.04 else ("warning_signs" if u < 0.04 + p_ws else "no_warning")
            hosp = rng.random() < {"severe": 1.0, "warning_signs": 0.9, "no_warning": 0.25}[sev]
            died = sev == "severe" and rng.random() < 0.12
            consult = onset + timedelta(days=1 + int(rng.poisson(1.8)))
            report = consult + timedelta(days=int(rng.poisson(1.0)))
            confirmed = rng.random() < 0.12
            lab_date = consult + timedelta(days=int(rng.integers(4, 13))) if confirmed else None
            rows.append({
                "pid": pid, "disease": "dengue", "date_onset": onset, "date_consult": consult,
                "date_report": report, "rdt_pos": bool(rng.random() < 0.5), "lab_date": lab_date,
                "hospitalised": int(hosp), "died": int(died), "dengue_severity": sev,
                "waded_floodwater": None, "cleanup_work": None,
            })
    return pd.DataFrame(rows)


def classify(rdt_pos: bool, lab_date: date | None) -> tuple[str, date | None]:
    """Case classification at the data freeze and the confirmation date if any.

    Parameters
    ----------
    rdt_pos : bool
        Positive rapid test (lepto RDT; dengue NS1/CBC criteria).
    lab_date : date or None
        Date the reference/sentinel laboratory result came back positive.

    Returns
    -------
    (str, date or None)
        ``confirmed`` if the result was back by :data:`FREEZE`, else
        ``probable`` (positive rapid test) or ``suspect``.
    """
    if lab_date is not None and lab_date <= FREEZE:
        return "confirmed", lab_date
    return ("probable" if rdt_pos else "suspect"), None


def assemble_truth(rng: np.random.Generator, pop: pd.DataFrame, brgy: pd.DataFrame,
                   lepto: pd.DataFrame, dengue: pd.DataFrame) -> pd.DataFrame:
    """Combine case records, apply the line-list window and give case IDs.

    Rows are kept when onset ≥ 20 Jul and report ≤ 30 Sep 2026.  They are put
    in the order the CESU encoded them (by report date, random within a day)
    and numbered ``SLC-0001`` … in that order.

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    pop, brgy : pandas.DataFrame
        Population and barangay tables.
    lepto, dengue : pandas.DataFrame
        Case records from :func:`lepto_cases` / :func:`dengue_cases`.

    Returns
    -------
    pandas.DataFrame
        The true line list (one row per notified case).
    """
    df = pd.concat([lepto, dengue], ignore_index=True)
    df = df[(df["date_onset"] >= LINELIST_START) & (df["date_report"] <= FREEZE)].copy()
    cls = [classify(r, d) for r, d in zip(df["rdt_pos"], df["lab_date"], strict=True)]
    df["case_class"] = [c for c, _ in cls]
    df["date_lab_confirmed"] = [d for _, d in cls]
    df["age"] = pop.loc[df["pid"], "age"].to_numpy()
    df["sex"] = np.where(pop.loc[df["pid"], "male"].to_numpy(), "M", "F")
    bi = pop.loc[df["pid"], "brgy_idx"].to_numpy()
    for col in ("barangay_id", "barangay", "band"):
        df[col] = brgy[col].to_numpy()[bi]
    df["outcome"] = np.where(df["died"] == 1, "died", "alive")
    df["_tie"] = rng.random(len(df))
    df = df.sort_values(["date_report", "_tie"]).reset_index(drop=True)
    df["case_id"] = [f"SLC-{i + 1:04d}" for i in range(len(df))]
    # infants: true age in months (shown in the raw file as "8 mos")
    df["age_months"] = [int(rng.integers(1, 12)) if a == 0 else None for a in df["age"]]
    return df.drop(columns=["_tie", "rdt_pos", "lab_date"])


# ===========================================================================
# 4. Weekly dengue series and rainfall
# ===========================================================================
def rainfall_series(rng: np.random.Generator, weeks: list[tuple[int, int]]) -> np.ndarray:
    """Weekly rainfall (mm): habagat season Jun–Oct, storm spikes, Amihan in 2026-W29.

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    weeks : list of tuple
        ISO (year, week) pairs.

    Returns
    -------
    numpy.ndarray
        Rainfall per week, rounded to 0.1 mm.
    """
    wk = np.array([w for _, w in weeks], dtype=float)
    clim = 12 + 110 * np.exp(-(((wk - 31) / 7.5) ** 2)) + 35 * np.exp(-(((wk - 45) / 4) ** 2))
    rain = clim * rng.gamma(3.0, 1 / 3.0, size=len(weeks))
    years = sorted({y for y, _ in weeks})
    for yr in years:
        idx = [i for i, (y, w) in enumerate(weeks) if y == yr and 30 <= w <= 46]
        if yr == 2026:
            continue
        for i in rng.choice(idx, size=2, replace=False):
            rain[i] += rng.uniform(80, 180)
    rain[weeks.index((2026, 29))] += AMIHAN_RAIN_MM
    return np.round(rain, 1)


def dengue_expected(weeks: list[tuple[int, int]], rain: np.ndarray) -> np.ndarray:
    """Expected weekly dengue cases: lagged-rainfall model x year multiplier + surge.

    Parameters
    ----------
    weeks : list of tuple
        ISO (year, week) pairs.
    rain : numpy.ndarray
        Weekly rainfall from :func:`rainfall_series`.

    Returns
    -------
    numpy.ndarray
        Expected cases per week (negative-binomial mean).
    """
    wk = np.array([w for _, w in weeks], dtype=float)
    clim = 12 + 110 * np.exp(-(((wk - 31) / 7.5) ** 2)) + 35 * np.exp(-(((wk - 45) / 4) ** 2))
    r_eff = np.zeros(len(weeks))
    for lag, wgt in RAIN_LAG_WEIGHTS.items():
        lagged = np.concatenate([clim[:lag], rain[:-lag]])  # climatology before 2019
        r_eff += wgt * lagged
    mult = np.array([
        COVID_MULT if (y == 2020 and w >= COVID_START[1]) else YEAR_MULT[y] for y, w in weeks
    ])
    lam = mult * (DENGUE_BASE + DENGUE_RAIN_COEF * r_eff)
    t0 = weeks.index((2026, 29))
    d = np.arange(len(weeks)) - t0
    dpos = np.clip(d, 0, None).astype(float)
    kernel = np.where(d > 0, dpos ** (SURGE_SHAPE - 1) * np.exp(-dpos / SURGE_SCALE), 0.0)
    norm = math.gamma(SURGE_SHAPE) * SURGE_SCALE ** SURGE_SHAPE
    return lam + SURGE_TOTAL * kernel / norm


def epidemic_threshold(weekly: pd.DataFrame) -> pd.Series:
    """Epidemic threshold: mean + 2 SD (ddof=1) of a 3-week window in baseline years.

    For ISO week *w* the baseline values are weeks *w*-1, *w* and *w*+1 of each
    year in :data:`THRESHOLD_YEARS` (12 values; week 53 of 2020 never enters
    because 2020 is not a baseline year).

    Parameters
    ----------
    weekly : pandas.DataFrame
        Weekly file with ``iso_year``, ``iso_week``, ``cases``.

    Returns
    -------
    pandas.Series
        Threshold indexed by ISO week number 1–53 (week 1 wraps to week 52).
    """
    base = weekly[weekly["iso_year"].isin(THRESHOLD_YEARS)]
    out = {}
    for wk in range(1, 54):
        window = {(wk - 2) % 52 + 1, wk, wk % 52 + 1} if wk <= 52 else {52, 53, 1}
        vals = base.loc[base["iso_week"].isin(window), "cases"]
        out[wk] = vals.mean() + 2 * vals.std(ddof=1)
    return pd.Series(out, name="threshold")


# ===========================================================================
# 5. Raw (messy) line list
# ===========================================================================
FIRST_M = ["Juan", "Jose", "Mark", "John Paul", "Jerome", "Rodel", "Arnel", "Romeo", "Eduardo",
           "Rogelio", "Danilo", "Christian", "Kevin", "Jayson", "Ronald", "Ramil", "Noel", "Efren",
           "Reynaldo", "Jericho", "Carlo", "Paolo", "Miguel", "Angelo", "Joshua", "Nathaniel",
           "Ariel", "Benjie", "Dennis", "Edgar", "Rolando", "Wilfredo", "Ernesto", "Lito",
           "Marvin", "Ryan", "Raffy", "Jomar", "Alvin", "Rommel"]
FIRST_F = ["Maria", "Ana", "Liza", "Rowena", "Marites", "Jocelyn", "Grace", "Rosalie", "Cristina",
           "Lorna", "Analyn", "Mary Joy", "Kristine", "Angelica", "Jasmine", "Princess", "Rhea",
           "Charmaine", "Leah", "Shiela", "Gemma", "Teresita", "Corazon", "Erlinda", "Nenita",
           "Divina", "Marilou", "Joy", "April", "Jennifer", "Lovely", "Mylene", "Rachelle",
           "Aileen", "Janine", "Clarissa"]
SURNAMES = ["Santos", "Reyes", "Cruz", "Garcia", "Mendoza", "Torres", "Flores", "Gonzales",
            "Lopez", "Castillo", "Aquino", "Navarro", "Salazar", "Mercado", "Domingo", "Gutierrez",
            "Pascual", "Soriano", "Manalo", "Fernandez", "Ocampo", "Rivera", "Morales", "Valdez",
            "Aguilar", "Panganiban", "Dizon", "Tolentino", "Sarmiento", "Macaraeg", "Magbanua",
            "Dimaculangan", "Pangilinan", "Cabrera", "Esguerra", "Agustin", "Bernardo", "Lim",
            "Tan", "Ramirez", "Del Rosario", "De Leon", "Dela Paz", "Evangelista", "Alcantara",
            "Buenaventura", "Galang", "Lagman", "Quiambao", "Sison", "Yap", "Manalastas"]
STREETS = ["Rizal", "Mabini", "Bonifacio", "Luna", "Burgos", "Del Pilar", "Sampaguita",
           "Ilang-Ilang", "Kamagong", "Narra", "Molave", "Acacia", "Mangga", "Bayabas"]
REPORTING_UNITS = {
    "hospital": ["Santa Luz City District Hospital", "Kalinaw Provincial Hospital"],
    "clinic": ["Santa Luz City Health Office", "Marilag Medical Clinic",
               "St. Agatha Family Clinic"],
}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
BRGY_TYPOS = {"Poblacion": "Pobalcion", "Dalampasigan": "Dalampasig", "Kawayanan": "Kawayan"}
DATE_STYLES = ["mdy", "mdy_nopad", "iso", "dmy_abbr", "long", "long_comma", "excel"]
DATE_STYLE_P = [0.42, 0.13, 0.13, 0.12, 0.08, 0.08, 0.04]
RAW_HEADER_LINE = ("# SYNTHETIC TRAINING DATA - every name, phone number and address in this "
                   "file is invented. Not real patients. Read with skiprows=1.")
RAW_COLUMNS = ["Date Reported", "Reporting Unit", "Patient Name", "Sex", "Age", "Contact No.",
               "Address", "Barangay", "Disease", "Date of Onset", "Date Consulted",
               "Classification", "Date Lab Confirmed", "Admitted", "Outcome",
               "Waded in Floodwater", "Did Cleanup Work", "Dengue Severity", "Remarks"]


def fmt_date(d: date | None, style: str) -> str:
    """Format a date in one of the raw-file styles (``""`` for missing).

    Parameters
    ----------
    d : date or None
        Date to format.
    style : str
        One of :data:`DATE_STYLES`.

    Returns
    -------
    str
        e.g. ``07/24/2026``, ``7/24/2026``, ``2026-07-24``, ``24-Jul-26``,
        ``July 24 2026``, ``July 24, 2026`` or the Excel serial ``46227``.
    """
    if d is None:
        return ""
    if style == "mdy":
        return d.strftime("%m/%d/%Y")
    if style == "mdy_nopad":
        return f"{d.month}/{d.day}/{d.year}"
    if style == "iso":
        return d.isoformat()
    if style == "dmy_abbr":
        return f"{d.day:02d}-{MONTHS[d.month - 1][:3]}-{d.year % 100:02d}"
    if style == "long":
        return f"{MONTHS[d.month - 1]} {d.day} {d.year}"
    if style == "long_comma":
        return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"
    if style == "excel":
        return str((d - EXCEL_EPOCH).days)
    raise ValueError(f"unknown date style: {style}")


def _pick(rng: np.random.Generator, options: list[str], p: list[float] | None = None) -> str:
    """Choose one string (helper keeping rng calls explicit)."""
    return str(options[int(rng.choice(len(options), p=p))])


def _name_pool(rng: np.random.Generator, sexes: list[str]) -> list[str]:
    """Unique invented full names ``First M. Last`` (unique after normalisation)."""
    names: list[str] = []
    seen: set[str] = set()
    for sex in sexes:
        while True:
            first = _pick(rng, FIRST_M if sex == "M" else FIRST_F)
            name = f"{first} {chr(65 + int(rng.integers(0, 26)))}. {_pick(rng, SURNAMES)}"
            key = normalise_name(name)
            if key not in seen:
                seen.add(key)
                names.append(name)
                break
    return names


def normalise_name(name: str) -> str:
    """Normalise a name for duplicate detection: upper case, no dots, single spaces.

    Parameters
    ----------
    name : str
        Name as typed.

    Returns
    -------
    str
        e.g. ``"juan  p. santos "`` → ``"JUAN P SANTOS"``.
    """
    return " ".join(name.replace(".", " ").upper().split())


def _phone(rng: np.random.Generator) -> str:
    """Fake mobile number in the fictional +63 900 555 xxxx block, mixed formats."""
    if rng.random() < 0.08:
        return _pick(rng, ["", "wala", "none"])
    tail = f"{int(rng.integers(0, 10000)):04d}"
    return _pick(rng, [f"+63 900 555 {tail}", f"0900-555-{tail}", f"0900555{tail}",
                       f"0900 555 {tail}"], [0.35, 0.3, 0.2, 0.15])


def _address(rng: np.random.Generator) -> str:
    """Invented street address (no '#', so read_csv(comment='#') stays safe)."""
    street = _pick(rng, STREETS)
    if rng.random() < 0.25:
        return f"Blk {int(rng.integers(1, 30))} Lot {int(rng.integers(1, 40))}, {street} St."
    return f"{int(rng.integers(1, 400))} {street} St., Purok {int(rng.integers(1, 8))}"


def _barangay_variant(rng: np.random.Generator, name: str, typo: bool) -> str:
    """Spelling variant of a barangay name as it appears on paper forms."""
    if typo:
        return BRGY_TYPOS[name]
    plain = name.replace("ñ", "n") if rng.random() < 0.5 else name
    if name.startswith("Santo ") and rng.random() < 0.6:
        plain = plain.replace("Santo ", _pick(rng, ["Sto. ", "Sto "]))
    if "-" in plain and rng.random() < 0.4:
        plain = plain.replace("-", " ")
    style = _pick(rng, ["plain", "brgy", "upper", "bgy", "lower", "barangay"],
                  [0.45, 0.17, 0.12, 0.10, 0.08, 0.08])
    return {
        "plain": plain, "brgy": f"Brgy. {plain}", "upper": plain.upper(), "bgy": f"Bgy {plain} ",
        "lower": plain.lower(), "barangay": f"Barangay {plain}",
    }[style]


def _sex_variant(rng: np.random.Generator, sex: str) -> str:
    """Sex as coded by different encoders (M/F/Male/babae…)."""
    if sex == "M":
        return _pick(rng, ["M", "Male", "male", "m", "lalaki"], [0.55, 0.2, 0.1, 0.08, 0.07])
    return _pick(rng, ["F", "Female", "female", "f", "babae"], [0.55, 0.2, 0.1, 0.08, 0.07])


def _age_variant(rng: np.random.Generator, age: int, months: int | None) -> str:
    """Age as typed: ``34``, ``34 y/o``, ``34 yrs``, ``34yo``; infants ``8 mos``."""
    if age == 0:
        m = int(months or 1)
        return _pick(rng, [f"{m} mos", f"{m} months", f"{m}mos"])
    return _pick(rng, [str(age), f"{age} y/o", f"{age} yrs", f"{age}yo"], [0.68, 0.14, 0.1, 0.08])


def _yes_no(rng: np.random.Generator, value: int | None, missing: bool) -> str:
    """Yes/no answer as typed (``Y``, ``No``, ``oo``, ``hindi``…); blank if missing."""
    if missing or value is None:
        return ""
    if value:
        return _pick(rng, ["Y", "Yes", "yes", "oo", "Oo"], [0.45, 0.25, 0.1, 0.1, 0.1])
    return _pick(rng, ["N", "No", "no", "hindi", "Hindi"], [0.45, 0.25, 0.1, 0.1, 0.1])


def _remark(rng: np.random.Generator, r: dict[str, Any], names: list[str]) -> str:
    """Taglish free-text remark consistent with the case (sometimes with PII)."""
    if rng.random() < 0.42:
        return ""
    if r["disease"] == "leptospirosis":
        opts = ["masakit ang binti (calf pain), mataas ang lagnat", "red eyes + fever 3 days",
                "nasa evacuation center pa", "for MAT, specimen sent", "positive sa RDT daw",
                "jaundice na, referred to district hosp", "may sugat sa paa"]
        if r["waded_floodwater"] == 1:
            opts += ["lumusong sa baha, walang bota", "lumusong sa baha para kunin ang aso"]
        if r["cleanup_work"] == 1:
            opts += ["nag-linis ng kanal after baha", "volunteer sa clean-up ng barangay"]
    else:
        opts = ["low platelet sa CBC", "nagsusuka, abdominal pain", "rashes + fever",
                "may kapitbahay din na nag-dengue", "NS1 done", "for CBC follow-up bukas",
                "estudyante, Grade 5"]
    opts += [f"anak/kapatid ni {_pick(rng, names).split()[0]} (kapitbahay)",
             "contact no. ng asawa ang nakalagay", "f/up c/o BHW"]
    return _pick(rng, opts)


def choose_corruptions(rng: np.random.Generator, truth: pd.DataFrame) -> dict[str, set[int]]:
    """Pick which rows get missing values, impossible values, typos and duplicates.

    Returns a dict of row-index sets: ``dup_exact``, ``dup_near``, ``age_missing``,
    ``age_150``, ``onset_typo``, ``consult_missing``, ``expo_missing``,
    ``brgy_typo``.  Impossible values and typos never fall on duplicated rows.

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    truth : pandas.DataFrame
        True line list.

    Returns
    -------
    dict
        Flag name → set of truth row indices.
    """
    n = len(truth)
    order = rng.permutation(n)
    taken: set[int] = set()

    def take(k: int, cond: Any = None) -> set[int]:
        out: set[int] = set()
        for i in order:
            i = int(i)
            if len(out) == k:
                break
            if i in taken or (cond is not None and not cond(i)):
                continue
            out.add(i)
        taken.update(out)
        return out

    n_dup = round(0.03 * n)
    dup_exact = take(n_dup // 3)
    dup_near = take(n_dup - n_dup // 3)
    lepto = truth["disease"].to_numpy() == "leptospirosis"
    consult = truth["date_consult"].to_numpy()
    onset = truth["date_onset"].to_numpy()
    return {
        "dup_exact": dup_exact,
        "dup_near": dup_near,
        "age_150": take(1, lambda i: truth.at[i, "age"] == 50),
        "onset_typo": take(2, lambda i: lepto[i] and _shift_month(onset[i]) > consult[i]),
        "age_missing": take(6),
        "consult_missing": take(12),
        "expo_missing": take(14, lambda i: lepto[i]),
        "brgy_typo": take(5, lambda i: truth.at[i, "barangay"] in BRGY_TYPOS),
    }


def _shift_month(d: date) -> date:
    """Same day one month later (slip of the pen on a paper form; day capped at 28)."""
    m = d.month % 12 + 1
    y = d.year + (d.month == 12)
    return date(y, m, min(d.day, 28))


def make_raw(rng: np.random.Generator, truth: pd.DataFrame,
             flags: dict[str, set[int]]) -> pd.DataFrame:
    """Render the truth as the messy export Jun sends (see README cleaning rules).

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    truth : pandas.DataFrame
        From :func:`assemble_truth`.
    flags : dict
        From :func:`choose_corruptions`.

    Returns
    -------
    pandas.DataFrame
        All-string raw table, duplicates inserted after their originals.
    """
    names = _name_pool(rng, list(truth["sex"]))
    rows: list[dict[str, str]] = []
    for i, r in enumerate(truth.to_dict("records")):
        rows.append(_raw_row(rng, r, i, flags, names))
    out = list(rows)
    # Insert duplicates after their originals (processed from the end so indices hold)
    for i in sorted(flags["dup_exact"] | flags["dup_near"], reverse=True):
        dup = dict(rows[i])
        if i in flags["dup_near"]:
            dup = _near_duplicate(rng, truth.iloc[i].to_dict(), dup, names[i])
        pos = out.index(rows[i]) + 1 + int(rng.integers(0, 25))
        out.insert(min(pos, len(out)), dup)
    return pd.DataFrame(out, columns=RAW_COLUMNS)


def _raw_row(rng: np.random.Generator, r: dict[str, Any], i: int,
             flags: dict[str, set[int]], names: list[str]) -> dict[str, str]:
    """One raw row for truth record *r* (index *i*)."""
    style = _pick(rng, DATE_STYLES, DATE_STYLE_P)
    unit = _pick(rng, REPORTING_UNITS["hospital" if r["hospitalised"] else "clinic"])
    if not r["hospitalised"] and rng.random() < 0.3:
        unit = f"{r['barangay']} Barangay Health Station"
    onset = _shift_month(r["date_onset"]) if i in flags["onset_typo"] else r["date_onset"]
    lepto = r["disease"] == "leptospirosis"
    if i in flags["age_150"]:
        age = "150"
    elif i in flags["age_missing"]:
        age = ""
    else:
        age = _age_variant(rng, int(r["age"]), r["age_months"])
    na_text = _pick(rng, ["", "N/A"], [0.8, 0.2])
    expo_missing = i in flags["expo_missing"]
    return {
        "Date Reported": fmt_date(r["date_report"], style),
        "Reporting Unit": unit,
        "Patient Name": names[i],
        "Sex": _sex_variant(rng, r["sex"]),
        "Age": age,
        "Contact No.": _phone(rng),
        "Address": _address(rng),
        "Barangay": _barangay_variant(rng, r["barangay"], i in flags["brgy_typo"]),
        "Disease": _pick(rng, ["Leptospirosis", "Lepto", "LEPTO", "leptospirosis"]
                         if lepto else ["Dengue", "DENGUE", "Dengue Fever", "DF", "dengue"]),
        "Date of Onset": fmt_date(onset, style),
        "Date Consulted": "" if i in flags["consult_missing"] else fmt_date(r["date_consult"],
                                                                             style),
        "Classification": _pick(rng, {
            "suspect": ["Suspect", "SUSPECT", "Suspected", "sus"],
            "probable": ["Probable", "PROBABLE", "prob."],
            "confirmed": ["Confirmed", "CONFIRMED", "Conf", "lab confirmed"],
        }[r["case_class"]]),
        "Date Lab Confirmed": fmt_date(r["date_lab_confirmed"], style),
        "Admitted": _yes_no(rng, r["hospitalised"], False),
        "Outcome": _pick(rng, ["Alive", "alive", "A", "buhay"] if r["outcome"] == "alive"
                         else ["Died", "D", "Namatay", "Expired"]),
        "Waded in Floodwater": _yes_no(rng, r["waded_floodwater"], expo_missing) if lepto
        else na_text,
        "Did Cleanup Work": _yes_no(rng, r["cleanup_work"], expo_missing) if lepto else na_text,
        "Dengue Severity": "" if lepto else _pick(rng, {
            "no_warning": ["Without warning signs", "w/o warning signs", "no WS"],
            "warning_signs": ["With warning signs", "w/ warning signs", "WS+"],
            "severe": ["Severe dengue", "SEVERE", "SD"],
        }[r["dengue_severity"]]),
        "Remarks": _remark(rng, r, names),
    }


def _near_duplicate(rng: np.random.Generator, r: dict[str, Any], row: dict[str, str],
                    name: str) -> dict[str, str]:
    """Second notification of the same patient from another unit / encoder."""
    dup = dict(row)
    style = _pick(rng, DATE_STYLES[:6])
    variant = _pick(rng, ["upper", "spaces", "nodot"])
    dup["Patient Name"] = {"upper": name.upper(), "spaces": "  ".join(name.split()) + " ",
                           "nodot": name.replace(".", "")}[variant]
    later = r["date_report"] + timedelta(days=int(rng.integers(0, 4)))
    dup["Date Reported"] = fmt_date(later, style)
    dup["Date of Onset"] = fmt_date(r["date_onset"], style)
    dup["Date Consulted"] = fmt_date(r["date_consult"], style)
    dup["Date Lab Confirmed"] = fmt_date(r["date_lab_confirmed"], style)
    dup["Barangay"] = _barangay_variant(rng, r["barangay"], False)
    dup["Sex"] = _sex_variant(rng, r["sex"])
    dup["Reporting Unit"] = "Santa Luz City Health Office"
    dup["Remarks"] = _pick(rng, ["double entry? also reported by hospital", "re-encoded",
                                 "same pt, ni-report ulit ng CHO"])
    return dup


# ===========================================================================
# 6. Clean line list
# ===========================================================================
CLEAN_COLUMNS = ["case_id", "disease", "case_class", "date_onset", "date_consult",
                 "date_report", "date_lab_confirmed", "age", "age_group", "sex", "barangay_id",
                 "barangay", "band", "hospitalised", "outcome", "dengue_severity",
                 "waded_floodwater", "cleanup_work"]


def _iso(d: date | None) -> str | None:
    """ISO string of a date or ``None``."""
    return None if d is None else d.isoformat()


def make_clean(truth: pd.DataFrame, flags: dict[str, set[int]]) -> pd.DataFrame:
    """The de-identified line list a correct cleaning of the raw file yields.

    Impossible/missing raw values become missing: age 150 → NA (age > 110),
    onset after consult → onset NA, blanks stay NA.

    Parameters
    ----------
    truth : pandas.DataFrame
        True line list.
    flags : dict
        From :func:`choose_corruptions`.

    Returns
    -------
    pandas.DataFrame
        Columns :data:`CLEAN_COLUMNS`.
    """
    df = truth.copy()
    idx = df.index
    bad_age = idx.isin(sorted(flags["age_150"] | flags["age_missing"]))
    age = df["age"].astype("Int64").mask(bad_age)
    out = pd.DataFrame({
        "case_id": df["case_id"],
        "disease": df["disease"],
        "case_class": df["case_class"],
        "date_onset": [None if i in flags["onset_typo"] else _iso(d)
                       for i, d in zip(idx, df["date_onset"], strict=True)],
        "date_consult": [None if i in flags["consult_missing"] else _iso(d)
                         for i, d in zip(idx, df["date_consult"], strict=True)],
        "date_report": [_iso(d) for d in df["date_report"]],
        "date_lab_confirmed": [_iso(d) for d in df["date_lab_confirmed"]],
        "age": age,
        "age_group": [age_group(None if pd.isna(a) else int(a)) for a in age],
        "sex": df["sex"],
        "barangay_id": df["barangay_id"],
        "barangay": df["barangay"],
        "band": df["band"],
        "hospitalised": _int_col(df["hospitalised"]),
        "outcome": df["outcome"],
        "dengue_severity": df["dengue_severity"],
        "waded_floodwater": _int_col([None if i in flags["expo_missing"] else v
                                      for i, v in zip(idx, df["waded_floodwater"], strict=True)]),
        "cleanup_work": _int_col([None if i in flags["expo_missing"] else v
                                  for i, v in zip(idx, df["cleanup_work"], strict=True)]),
    })
    return out[CLEAN_COLUMNS]


# ===========================================================================
# 7. Case-control study
# ===========================================================================
def make_case_control(rng: np.random.Generator, pop: pd.DataFrame, brgy: pd.DataFrame,
                      truth: pd.DataFrame) -> pd.DataFrame:
    """Barangay-matched 1:2 case-control study of leptospirosis.

    Cases: probable/confirmed leptospirosis in riverside residents aged ≥ 15.
    Controls: two residents aged ≥ 15 without leptospirosis from the case's
    barangay, sampled at random from the synthetic population.

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    pop, brgy : pandas.DataFrame
        Population and barangay tables.
    truth : pandas.DataFrame
        True line list.

    Returns
    -------
    pandas.DataFrame
        One row per participant, cases first in each matched set.
    """
    cases = truth[(truth["disease"] == "leptospirosis") & (truth["band"] == "riverside")
                  & (truth["case_class"] != "suspect") & (truth["age"] >= 15)]
    eligible = pop[(~pop["lepto"]) & (pop["age"] >= 15)]
    pool = {b: list(g.index) for b, g in eligible.groupby("brgy_idx")}
    used: set[int] = set()
    rows = []
    for s, r in enumerate(cases.to_dict("records"), start=1):
        b = int(pop.at[r["pid"], "brgy_idx"])
        rows.append(_cc_row(pop, brgy, r["pid"], s, "case", r["case_id"]))
        picked = 0
        while picked < 2:
            pid = int(rng.choice(pool[b]))
            if pid in used:
                continue
            used.add(pid)
            rows.append(_cc_row(pop, brgy, pid, s, "control", None))
            picked += 1
    df = pd.DataFrame(rows)
    df.insert(0, "study_id", [f"CC-{i + 1:03d}" for i in range(len(df))])
    for col in ("case", "age", "waded_floodwater", "wore_boots", "skin_wound",
                "doxy_prophylaxis", "cleanup_work", "rats_near_home"):
        df[col] = df[col].astype("Int64")
    return df


def _cc_row(pop: pd.DataFrame, brgy: pd.DataFrame, pid: int, matched_set: int, status: str,
            case_id: str | None) -> dict[str, Any]:
    """One participant row of the case-control file."""
    p = pop.loc[pid]
    b = brgy.iloc[int(p.brgy_idx)]
    return {
        "matched_set": matched_set, "status": status, "case": int(status == "case"),
        "case_id": case_id, "barangay_id": b.barangay_id, "barangay": b.barangay,
        "age": int(p.age), "sex": "M" if p.male else "F",
        "waded_floodwater": int(p.waded), "wore_boots": int(p.boots) if p.waded else None,
        "skin_wound": int(p.wound), "doxy_prophylaxis": int(p.doxy),
        "cleanup_work": int(p.cleanup), "rats_near_home": int(p.rats),
    }


# ===========================================================================
# 8. 7-1-7 signals
# ===========================================================================
SIGNAL_DISEASES = [
    ("dengue", 7), ("acute watery diarrhoea", 5), ("measles", 4), ("leptospirosis", 3),
    ("typhoid fever", 3), ("food poisoning", 4), ("influenza-like illness", 3),
    ("hand, foot and mouth disease", 3), ("pertussis", 2), ("rabies (human)", 2),
    ("diphtheria", 1), ("hepatitis A", 1), ("cholera", 1), ("chikungunya", 1),
    ("meningococcal disease", 1),
]
BOTTLENECKS = {
    "detection": [
        "Cases seen at a private clinic that is not yet a PIDSR disease reporting unit",
        "BHW noticed the cluster but had no load to text the CESU",
        "Clinicians treated it as 'trangkaso' (flu); case definition not applied",
        "Weekly batch encoding: forms sat in a folder for a week before EDCS entry",
        "Patients self-medicated from the botika before consulting",
        "Upland barangay: nearest health station two hours away by habal-habal",
        "No local test; diagnosis waited for the referral hospital",
    ],
    "notification": [
        "Detected on a Friday; DSO on leave and no back-up over the weekend",
        "Waited for the City Health Officer's signature on the CIF before notifying",
        "EDCS down and no internet at the City Health Office",
        "Hospital and CESU each assumed the other had notified the PESU",
        "Notified by personal chat message, not logged; PESU learned of it days later",
    ],
    "response": [
        "Specimens waited 9 days for a courier to the reference laboratory",
        "No vehicle available for the response team",
        "Outbreak-response vaccines requested from the province arrived late",
        "Response funds needed Sangguniang Panlungsod approval",
        "Road closed by a landslide; field team delayed",
        "Contact tracing on paper; list incomplete for a week",
        "One DSO for 24 barangays; competing priorities",
    ],
}
P_FAIL = {"detection": 0.40, "notification": 0.30, "response": 0.45}


def _signal_delays(rng: np.random.Generator) -> tuple[dict[str, int], list[str]]:
    """Draw detection/notification/response delays; return delays and failed stages."""
    fail = [s for s in ("detection", "notification", "response") if rng.random() < P_FAIL[s]]
    d = {
        "detection": int(rng.integers(8, 29)) if "detection" in fail else int(rng.integers(1, 8)),
        "notification": int(rng.integers(2, 9)) if "notification" in fail
        else int(rng.integers(0, 2)),
        "response": int(rng.integers(8, 22)) if "response" in fail else int(rng.integers(2, 8)),
    }
    return d, fail


def make_signals(rng: np.random.Generator, brgy: pd.DataFrame, truth: pd.DataFrame,
                 crossing_week: tuple[int, int]) -> pd.DataFrame:
    """About 40 public-health events in Santa Luz (Jan 2025 – Sep 2026) for 7-1-7.

    The last two events are the story's: the post-Amihan leptospirosis cluster
    and the dengue surge (detected the Monday after the threshold-crossing week).

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    brgy, truth : pandas.DataFrame
        Barangay table and true line list.
    crossing_week : tuple of int
        ISO week in which dengue first exceeded the threshold.

    Returns
    -------
    pandas.DataFrame
        One row per event, sorted by emergence date.
    """
    names = [d for d, _ in SIGNAL_DISEASES]
    w = np.array([k for _, k in SIGNAL_DISEASES], dtype=float)
    start = date(2025, 1, 6)
    span = (date(2026, 6, 30) - start).days
    rows = []
    for _ in range(38):
        delays, fail = _signal_delays(rng)
        emerg = start + timedelta(days=int(rng.integers(0, span)))
        rows.append(_signal_row(rng, _pick(rng, names, list(w / w.sum())),
                                _pick(rng, list(brgy["barangay"])), emerg, delays, fail))
    lep = truth[(truth["disease"] == "leptospirosis") & (truth["barangay"] == "Ilog")]
    first = min(lep["date_onset"])
    rows.append({
        "disease": "leptospirosis", "barangay": "Ilog", "date_emergence": first,
        "date_detection": date(2026, 7, 27), "date_notification": date(2026, 7, 29),
        "date_response_complete": date(2026, 8, 3),
        "bottleneck": "Paper notification forms piled up at the CESU during the typhoon "
                      "response; PESU notified two days after Aling Nena's text",
    })
    cross_monday = date.fromisocalendar(*crossing_week, 1)
    detect = cross_monday + timedelta(days=7)
    rows.append({
        "disease": "dengue", "barangay": "Baybay", "date_emergence": cross_monday,
        "date_detection": detect, "date_notification": detect + timedelta(days=1),
        "date_response_complete": detect + timedelta(days=11),
        "bottleneck": "4S clean-up and larval survey needed volunteers still busy with "
                      "typhoon relief; misting supplies requested from the province",
    })
    df = pd.DataFrame(rows).sort_values("date_emergence", kind="stable").reset_index(drop=True)
    df.insert(0, "event_id", [f"EV-{i + 1:03d}" for i in range(len(df))])
    for c in ("date_emergence", "date_detection", "date_notification", "date_response_complete"):
        df[c] = df[c].map(date.isoformat)
    return df


def _signal_row(rng: np.random.Generator, disease: str, barangay: str, emerg: date,
                delays: dict[str, int], fail: list[str]) -> dict[str, Any]:
    """One event row from its delays; bottleneck text names each failed stage."""
    det = emerg + timedelta(days=delays["detection"])
    note = det + timedelta(days=delays["notification"])
    resp = note + timedelta(days=delays["response"])
    text = "; ".join(_pick(rng, BOTTLENECKS[s]) for s in fail) if fail else "none"
    return {"disease": disease, "barangay": barangay, "date_emergence": emerg,
            "date_detection": det, "date_notification": note, "date_response_complete": resp,
            "bottleneck": text}


# ===========================================================================
# 9. Real regional statistics (export only, never estimated)
# ===========================================================================
REGION_FIELDS = [
    ("population_2020", "population2020"),
    ("population_2024", "population2024"),
    ("land_area_km2", "landAreaKm2"),
    ("density_2024_per_km2", "density2024"),
    ("urbanization_2020_pct", "urbanization2020Pct"),
    ("poverty_incidence_2021_pct", "povertyIncidencePop2021Pct"),
    ("poverty_incidence_2023_pct", "povertyIncidencePop2023Pct"),
    ("grdp_2024_php_million", "grdp2024CurrentPHPmillion"),
    ("grdp_per_capita_2024_php", "grdpPerCapita2024PHP"),
    ("functional_literacy_2024_pct", "functionalLiteracy2024Pct"),
    ("household_internet_2024_pct", "householdInternet2024Pct"),
    ("hospital_beds_2019", "hospitalBeds2019"),
    ("hospital_beds_per_10k_2019", "hospitalBedsPer10k2019"),
]
INT_REGION_FIELDS = {"population_2020", "population_2024", "grdp_2024_php_million",
                     "grdp_per_capita_2024_php", "hospital_beds_2019"}


def resolve_source_url(research: dict[str, Any], src: str | None) -> tuple[str | None, str | None]:
    """Resolve a region field's ``src`` code to (kind, url) via ``alias``/``sources``.

    Parameters
    ----------
    research : dict
        The parsed research JSON.
    src : str or None
        Code such as ``"S4"`` (cited), ``"D"`` (derived by the researcher).

    Returns
    -------
    (str or None, str or None)
        ``("cited", url)``, ``("derived", None)`` or ``(None, None)``.
    """
    if src is None:
        return None, None
    key = research["alias"].get(f"R-{src}")
    if key is None:
        raise ValueError(f"unknown region source code {src!r}")
    source = next(s for s in research["sources"] if s["k"] == key)
    kind = "derived" if source.get("q") == "derived" else "cited"
    if source.get("q") in ("estimate", "qualitative"):
        raise ValueError(f"region field uses non-factual source {src!r}")
    return kind, source.get("u")


def make_regions(research: dict[str, Any]) -> pd.DataFrame:
    """Export the 18-region statistics with year and source for every value.

    Parameters
    ----------
    research : dict
        The parsed research JSON (``regions.regs``).

    Returns
    -------
    pandas.DataFrame
        One row per region; ``adm1_psgc`` joins ``ph_regions.topo.json``.
    """
    rows = []
    for reg in research["regions"]["regs"]:
        row: dict[str, Any] = {
            "region_id": reg["id"], "adm1_psgc": int(reg["psgc"]), "psgc": reg["psgc"],
            "region_short": reg["short"], "region_name": reg["nameEN"],
            "region_name_zh": reg.get("zh"), "island_group": reg["islandGroup"],
        }
        for col, key in REGION_FIELDS:
            field = reg[key]
            value = field.get("value")
            kind, url = resolve_source_url(research, field.get("src")) if value is not None \
                else (None, None)
            row[col] = value
            row[f"{col}_year"] = field.get("year") if value is not None else None
            row[f"{col}_source"] = kind
            row[f"{col}_source_url"] = url
        rows.append(row)
    df = pd.DataFrame(rows).sort_values("adm1_psgc").reset_index(drop=True)
    for col, _ in REGION_FIELDS:
        df[f"{col}_year"] = df[f"{col}_year"].astype("Int64")
        if col in INT_REGION_FIELDS:
            df[col] = df[col].astype("Int64")
        else:
            df[col] = df[col].astype("Float64")
    return df


# ===========================================================================
# 10. Orchestration
# ===========================================================================
STREAMS = ("geo", "population", "lepto", "rain", "dengue_counts", "dengue_people", "truth",
           "history", "raw", "case_control", "signals")


def streams(seed: int = SEED) -> dict[str, np.random.Generator]:
    """Independent random streams per component, all derived from *seed*.

    Separate streams keep, e.g., the raw-file mess stable when the dengue model
    is retuned.  New streams must be appended to :data:`STREAMS`.

    Parameters
    ----------
    seed : int
        Master seed.

    Returns
    -------
    dict
        ``{stream name: numpy.random.Generator}``.
    """
    children = np.random.SeedSequence(seed).spawn(len(STREAMS))
    return {name: np.random.default_rng(ss) for name, ss in zip(STREAMS, children, strict=True)}


def build_weekly(rng: np.random.Generator, truth_dengue_counts: dict[tuple[int, int], int],
                 weeks: list[tuple[int, int]], lam: np.ndarray, rain: np.ndarray) -> pd.DataFrame:
    """Weekly file: NB draws before 2026-W30, line-list onset counts from W30 on.

    Parameters
    ----------
    rng : numpy.random.Generator
        Random generator.
    truth_dengue_counts : dict
        Line-list dengue cases by ISO (year, week) of onset.
    weeks : list of tuple
        Simulated ISO weeks.
    lam, rain : numpy.ndarray
        Expected cases and rainfall per week.

    Returns
    -------
    pandas.DataFrame
        Weeks 2019-W01 … 2026-W39.
    """
    cases = nb_draw(rng, lam)
    rows = []
    for i, (y, w) in enumerate(weeks):
        if (y, w) > WEEKLY_LAST:
            break
        n = truth_dengue_counts.get((y, w), 0) if (y, w) >= (2026, 30) else int(cases[i])
        rows.append({"iso_year": y, "iso_week": w, "morbidity_week": f"{y}-W{w:02d}",
                     "week_start": date.fromisocalendar(y, w, 1).isoformat(), "cases": n,
                     "rainfall_mm": float(rain[i])})
    return pd.DataFrame(rows)


def generate(out_dir: Path = OUT_DIR, research_path: Path = RESEARCH_JSON,
             seed: int = SEED, check: bool = True) -> dict[str, Any]:
    """Generate and write every Santa Luz file into *out_dir*.

    Parameters
    ----------
    out_dir : pathlib.Path
        Destination folder (the TopoJSON is not touched).
    research_path : pathlib.Path
        Research JSON used for ``ph_regions_stats.csv``.

    Returns
    -------
    dict
        Key internal values (threshold-crossing week, intercepts…) for reporting.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = streams(seed)
    brgy, rings = build_barangays(rng["geo"])
    pop = simulate_population(rng["population"], brgy)
    lepto = lepto_cases(rng["lepto"], pop)

    weeks = iso_weeks(WEEKLY_FIRST, SIM_LAST)
    rain = rainfall_series(rng["rain"], weeks)
    lam = dengue_expected(weeks, rain)
    ll_weeks = [wk for wk in weeks if wk >= (2026, 30)]
    counts = {}
    for wk in ll_weeks:
        mean = lam[weeks.index(wk)] * (3 / 7 if wk == SIM_LAST else 1.0)
        counts[wk] = int(nb_draw(rng["dengue_counts"], mean))
    dengue = dengue_cases(rng["dengue_people"], pop, brgy, counts)

    truth = assemble_truth(rng["truth"], pop, brgy, lepto, dengue)
    den = truth[truth["disease"] == "dengue"]
    by_week = pd.Series([tuple(d.isocalendar()[:2]) for d in den["date_onset"]]).value_counts()
    weekly = build_weekly(rng["history"], by_week.to_dict(), weeks, lam, rain)
    thr = epidemic_threshold(weekly)
    w26 = weekly[weekly["iso_year"] == 2026]
    above = w26[w26["cases"].to_numpy() > thr.loc[w26["iso_week"]].to_numpy()]
    crossing = (2026, int(above["iso_week"].iloc[0]))
    if crossing[1] < 31 and check:
        raise ValueError(f"dengue threshold crossed too early ({crossing}); retune the design")

    flags = choose_corruptions(rng["raw"], truth)
    raw = make_raw(rng["raw"], truth, flags)
    clean = make_clean(truth, flags)
    cc = make_case_control(rng["case_control"], pop, brgy, truth)
    signals = make_signals(rng["signals"], brgy, truth, crossing)
    research = json.loads(research_path.read_text(encoding="utf-8"))
    regions = make_regions(research)

    _write_csv(brgy, out_dir / "santa_luz_barangays.csv")
    (out_dir / "santa_luz_barangays.geojson").write_text(barangay_geojson(brgy, rings),
                                                         encoding="utf-8", newline="")
    _write_csv(raw, out_dir / "santa_luz_linelist_raw.csv", RAW_HEADER_LINE)
    _write_csv(clean, out_dir / "santa_luz_linelist.csv")
    _write_csv(cc, out_dir / "lepto_case_control.csv")
    _write_csv(weekly, out_dir / "santa_luz_dengue_weekly.csv")
    _write_csv(signals, out_dir / "signals_717.csv")
    _write_csv(regions, out_dir / "ph_regions_stats.csv")
    return {"crossing_week": crossing, "n_raw": len(raw), "n_clean": len(clean),
            "n_case_control": len(cc), "first_above_weeks": list(above["iso_week"]),
            "expected_2026_w30_w40": [round(float(lam[weeks.index(wk)]), 1) for wk in ll_weeks],
            "drawn_2026_w30_w40": list(counts.values())}


def main() -> None:
    """Regenerate the files and print a short summary."""
    info = generate()
    clean = pd.read_csv(OUT_DIR / "santa_luz_linelist.csv")
    print(f"raw rows: {info['n_raw']}  clean rows: {info['n_clean']}")
    print(clean.groupby("disease").agg(n=("case_id", "size"),
                                       deaths=("outcome", lambda s: (s == "died").sum())))
    print(f"dengue threshold first crossed: {info['crossing_week']} "
          f"(weeks above: {info['first_above_weeks']})")
    print(f"case-control participants: {info['n_case_control']}")


if __name__ == "__main__":
    main()
