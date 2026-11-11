"""Tests for the synthetic Santa Luz datasets of the Philippines edition.

Covers ``data/synthetic/ph/``: byte-for-byte regeneration, schemas, the fixed
headline numbers quoted in the book (see ``data/synthetic/ph/README.md``), the
reference raw → clean line-list cleaning (chapter 03 must reproduce it),
geometry validity and the join of the real regional statistics to the TopoJSON.
"""

from __future__ import annotations

import importlib.util
import json
import math
import re
import unicodedata
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import LinearRing, shape
from shapely.ops import unary_union

REPO = Path(__file__).resolve().parents[1]
PH = REPO / "data" / "synthetic" / "ph"
GENERATED = [
    "santa_luz_barangays.csv",
    "santa_luz_barangays.geojson",
    "santa_luz_linelist_raw.csv",
    "santa_luz_linelist.csv",
    "lepto_case_control.csv",
    "santa_luz_dengue_weekly.csv",
    "signals_717.csv",
    "ph_regions_stats.csv",
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
def _load_generator() -> ModuleType:
    """Import ``generate_santa_luz.py`` (it lives outside any package)."""
    spec = importlib.util.spec_from_file_location("generate_santa_luz",
                                                  PH / "generate_santa_luz.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def gen() -> ModuleType:
    return _load_generator()


@pytest.fixture(scope="module")
def regenerated(gen: ModuleType, tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("santa_luz")
    gen.generate(out)
    return out


@pytest.fixture(scope="module")
def brgy() -> pd.DataFrame:
    return pd.read_csv(PH / "santa_luz_barangays.csv")


@pytest.fixture(scope="module")
def clean() -> pd.DataFrame:
    return pd.read_csv(PH / "santa_luz_linelist.csv", parse_dates=[
        "date_onset", "date_consult", "date_report", "date_lab_confirmed"])


@pytest.fixture(scope="module")
def cc() -> pd.DataFrame:
    return pd.read_csv(PH / "lepto_case_control.csv")


@pytest.fixture(scope="module")
def weekly() -> pd.DataFrame:
    return pd.read_csv(PH / "santa_luz_dengue_weekly.csv")


@pytest.fixture(scope="module")
def signals() -> pd.DataFrame:
    return pd.read_csv(PH / "signals_717.csv", parse_dates=[
        "date_emergence", "date_detection", "date_notification", "date_response_complete"])


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("name", GENERATED)
def test_regeneration_is_byte_identical(regenerated: Path, name: str) -> None:
    assert (regenerated / name).read_bytes() == (PH / name).read_bytes(), name


def test_total_size_is_small() -> None:
    total = sum((PH / n).stat().st_size for n in GENERATED)
    assert total < 1_000_000


def test_raw_file_announces_synthetic_data() -> None:
    first = (PH / "santa_luz_linelist_raw.csv").read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("# SYNTHETIC TRAINING DATA")


# ---------------------------------------------------------------------------
# Barangays and geometry
# ---------------------------------------------------------------------------
def test_barangays_schema(brgy: pd.DataFrame) -> None:
    assert list(brgy.columns) == ["barangay_id", "barangay", "band", "population", "households",
                                  "area_km2", "density_per_km2", "centroid_lon", "centroid_lat",
                                  "flood_depth_m"]
    assert len(brgy) == 24 and brgy["barangay_id"].is_unique and brgy["barangay"].is_unique
    assert brgy["band"].value_counts().to_dict() == {"riverside": 8, "coastal": 8, "upland": 8}
    assert brgy["population"].sum() == 186_000
    by_band = brgy.groupby("band")["population"].sum().to_dict()
    assert by_band == {"coastal": 58_852, "riverside": 96_064, "upland": 31_084}
    depth = brgy.groupby("band")["flood_depth_m"].min()
    assert depth["riverside"] > brgy.loc[brgy["band"] != "riverside", "flood_depth_m"].max()


def test_geojson_valid_non_overlapping_and_offshore(brgy: pd.DataFrame) -> None:
    gdf = gpd.read_file(PH / "santa_luz_barangays.geojson")
    assert len(gdf) == 24
    assert gdf.crs is not None and gdf.crs.to_epsg() == 4326
    assert gdf.geometry.is_valid.all()
    assert (gdf.geom_type == "Polygon").all()
    polys = list(gdf.geometry)
    union = unary_union(polys)
    assert math.isclose(union.area, sum(p.area for p in polys), rel_tol=1e-9)
    assert union.geom_type == "Polygon"  # one contiguous city, no holes
    assert len(union.interiors) == 0
    minx, miny, maxx, maxy = gdf.total_bounds
    assert 130.0 < minx and maxx < 130.4 and 14.7 < miny and maxy < 14.95  # open sea
    raw = json.loads((PH / "santa_luz_barangays.geojson").read_text(encoding="utf-8"))
    for feat in raw["features"]:
        assert LinearRing(feat["geometry"]["coordinates"][0]).is_ccw  # RFC 7946 exterior
    merged = gdf.merge(brgy, on="barangay_id", suffixes=("", "_csv"))
    assert len(merged) == 24 and (merged["barangay"] == merged["barangay_csv"]).all()
    for _, row in merged.iterrows():
        assert shape(row.geometry.__geo_interface__).contains(
            gpd.points_from_xy([row.centroid_lon], [row.centroid_lat])[0])


# ---------------------------------------------------------------------------
# Reference cleaning: raw → clean (chapter 03 teaches exactly these rules)
# ---------------------------------------------------------------------------
MONTH_ABBR = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
BARANGAY_TYPOS = {"pobalcion": "poblacion", "dalampasig": "dalampasigan", "kawayan": "kawayanan"}
YES = {"y", "yes", "oo"}
NO = {"n", "no", "hindi"}


def parse_raw_date(text: str) -> date | None:
    """Parse one raw date string (rule D1–D6 in the README)."""
    s = text.strip()
    if s == "":
        return None
    if re.fullmatch(r"\d{5}", s):  # D6 Excel serial
        return date(1899, 12, 30) + timedelta(days=int(s))
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)  # D1/D2 month/day/year
    if m:
        return date(int(m[3]), int(m[1]), int(m[2]))
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)  # D3 ISO
    if m:
        return date(int(m[1]), int(m[2]), int(m[3]))
    m = re.fullmatch(r"(\d{1,2})-([A-Za-z]{3})-(\d{2})", s)  # D4 24-Jul-26
    if m:
        return date(2000 + int(m[3]), MONTH_ABBR[m[2].lower()], int(m[1]))
    m = re.fullmatch(r"([A-Za-z]+) (\d{1,2}),? (\d{4})", s)  # D5 July 24 2026 / July 24, 2026
    if m:
        return date(int(m[3]), MONTH_ABBR[m[1][:3].lower()], int(m[2]))
    raise ValueError(f"unparseable date: {text!r}")


def normalise_barangay(text: str) -> str:
    """Barangay key: rule B1–B5 in the README."""
    s = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower().strip()
    s = re.sub(r"^(barangay|brgy\.?|bgy\.?)\s+", "", s)
    s = re.sub(r"^sto\.?\s+", "santo ", s)
    s = " ".join(s.replace("-", " ").replace(".", " ").split())
    return BARANGAY_TYPOS.get(s, s)


def parse_age(text: str) -> int | None:
    """Age in completed years (rule A1–A3)."""
    s = text.strip().lower()
    if s == "":
        return None
    n = int(re.match(r"\d+", s)[0])  # type: ignore[index]
    years = n // 12 if "mo" in s else n
    return None if years > 110 else years


def parse_yes_no(text: str) -> int | None:
    s = text.strip().lower()
    if s in YES:
        return 1
    if s in NO:
        return 0
    if s in ("", "n/a"):
        return None
    raise ValueError(f"unexpected yes/no value {text!r}")


def map_value(text: str, rules: list[tuple[str, str]]) -> str:
    """First rule whose regex matches the lower-cased text wins."""
    s = text.strip().lower()
    for pattern, value in rules:
        if re.search(pattern, s):
            return value
    raise ValueError(f"unmapped value {text!r}")


SEX_RULES = [(r"^(m|male|lalaki)$", "M"), (r"^(f|female|babae)$", "F")]
DISEASE_RULES = [(r"^lep", "leptospirosis"), (r"^(deng|df$)", "dengue")]
CLASS_RULES = [(r"conf", "confirmed"), (r"^prob", "probable"), (r"^sus", "suspect")]
OUTCOME_RULES = [(r"^(alive|a|buhay)$", "alive"), (r"^(died|d|namatay|expired)$", "died")]
SEVERITY_RULES = [(r"severe|^sd$", "severe"), (r"without|w/o|^no ws$", "no_warning"),
                  (r"with|w/|^ws\+$", "warning_signs")]


def age_group(age: int | None) -> str | None:
    if age is None:
        return None
    for hi, label in [(4, "0-4"), (14, "5-14"), (24, "15-24"), (44, "25-44"), (64, "45-64")]:
        if age <= hi:
            return label
    return "65+"


def reference_clean(raw_path: Path, brgy: pd.DataFrame) -> pd.DataFrame:
    """Reference implementation of the README cleaning rules (C1–C8)."""
    raw = pd.read_csv(raw_path, skiprows=1, dtype=str, keep_default_na=False)  # C1
    lookup = {normalise_barangay(n): (i, n, b)
              for i, n, b in brgy[["barangay_id", "barangay", "band"]].itertuples(index=False)}
    rows = []
    for r in raw.to_dict("records"):  # C2 standardise every field
        disease = map_value(r["Disease"], DISEASE_RULES)
        bid, bname, band = lookup[normalise_barangay(r["Barangay"])]
        age = parse_age(r["Age"])
        rows.append({
            "_key": " ".join(r["Patient Name"].replace(".", " ").upper().split()),
            "disease": disease,
            "case_class": map_value(r["Classification"], CLASS_RULES),
            "date_onset": parse_raw_date(r["Date of Onset"]),
            "date_consult": parse_raw_date(r["Date Consulted"]),
            "date_report": parse_raw_date(r["Date Reported"]),
            "date_lab_confirmed": parse_raw_date(r["Date Lab Confirmed"]),
            "age": age, "age_group": age_group(age),
            "sex": map_value(r["Sex"], SEX_RULES),
            "barangay_id": bid, "barangay": bname, "band": band,
            "hospitalised": parse_yes_no(r["Admitted"]),
            "outcome": map_value(r["Outcome"], OUTCOME_RULES),
            "dengue_severity": map_value(r["Dengue Severity"], SEVERITY_RULES)
            if disease == "dengue" else None,
            "waded_floodwater": parse_yes_no(r["Waded in Floodwater"]),
            "cleanup_work": parse_yes_no(r["Did Cleanup Work"]),
        })
    df = pd.DataFrame(rows)
    df = df.drop_duplicates(["_key", "disease", "date_onset"], keep="first")  # C3
    later = df["date_consult"].where(df["date_consult"].notna(), df["date_report"])
    bad = [o is not None and o > c for o, c in zip(df["date_onset"], later, strict=True)]
    df.loc[bad, "date_onset"] = None  # C4 onset after consultation → missing
    df = df.reset_index(drop=True)
    df.insert(0, "case_id", [f"SLC-{i + 1:04d}" for i in range(len(df))])  # C5
    for col in ("date_onset", "date_consult", "date_report", "date_lab_confirmed"):
        df[col] = [None if d is None or pd.isna(d) else d.isoformat() for d in df[col]]
    for col in ("age", "hospitalised", "waded_floodwater", "cleanup_work"):
        df[col] = df[col].astype("Int64")
    return df.drop(columns="_key")  # C6 drop direct identifiers (never carried over)


def test_reference_cleaning_reproduces_clean_file(brgy: pd.DataFrame) -> None:
    ours = reference_clean(PH / "santa_luz_linelist_raw.csv", brgy)
    text = ours.to_csv(index=False, lineterminator="\n")
    assert text == (PH / "santa_luz_linelist.csv").read_text(encoding="utf-8")


def test_raw_file_has_the_promised_mess() -> None:
    raw = pd.read_csv(PH / "santa_luz_linelist_raw.csv", skiprows=1, dtype=str,
                      keep_default_na=False)
    assert len(raw) == 637
    assert raw.duplicated().sum() == 6  # exact copies
    assert raw["Age"].eq("150").sum() == 1
    assert raw["Age"].str.contains("mo").sum() == 13
    assert raw["Date of Onset"].str.fullmatch(r"\d{5}").sum() > 0  # Excel serials
    assert raw["Date of Onset"].str.contains("-[A-Z][a-z]{2}-").sum() > 0
    assert raw["Barangay"].str.endswith(" ").sum() > 0
    assert {"babae", "lalaki", "Male", "F"} <= set(raw["Sex"])
    assert raw["Contact No."].str.contains("555").mean() > 0.85
    assert not raw.apply(lambda c: c.str.contains("#")).any().any()  # comment="#" is safe


# ---------------------------------------------------------------------------
# Clean line list: schema and headline numbers
# ---------------------------------------------------------------------------
def test_clean_schema(clean: pd.DataFrame) -> None:
    assert list(clean.columns) == [
        "case_id", "disease", "case_class", "date_onset", "date_consult", "date_report",
        "date_lab_confirmed", "age", "age_group", "sex", "barangay_id", "barangay", "band",
        "hospitalised", "outcome", "dengue_severity", "waded_floodwater", "cleanup_work"]
    assert clean["case_id"].is_unique
    assert set(clean["disease"]) == {"leptospirosis", "dengue"}
    assert set(clean["case_class"]) == {"suspect", "probable", "confirmed"}
    assert set(clean["sex"]) == {"M", "F"}
    assert set(clean["outcome"]) == {"alive", "died"}
    assert clean["date_report"].min() >= pd.Timestamp("2026-07-20")
    assert clean["date_report"].max() <= pd.Timestamp("2026-09-30")
    assert clean["date_onset"].min() >= pd.Timestamp("2026-07-20")
    ok = clean.dropna(subset=["date_onset", "date_consult"])
    assert (ok["date_onset"] <= ok["date_consult"]).all()
    assert (clean["date_consult"].dropna() <= clean.loc[clean["date_consult"].notna(),
                                                        "date_report"]).all()
    conf = clean["case_class"] == "confirmed"
    assert clean.loc[conf, "date_lab_confirmed"].notna().all()
    assert clean.loc[~conf, "date_lab_confirmed"].isna().all()
    den = clean["disease"] == "dengue"
    assert clean.loc[den, "waded_floodwater"].isna().all()
    assert clean.loc[~den, "dengue_severity"].isna().all()
    assert set(clean.loc[den, "dengue_severity"]) == {"no_warning", "warning_signs", "severe"}


def test_headline_counts(clean: pd.DataFrame) -> None:
    assert len(clean) == 618
    counts = clean["disease"].value_counts().to_dict()
    assert counts == {"dengue": 388, "leptospirosis": 230}
    deaths = clean[clean["outcome"] == "died"]["disease"].value_counts().to_dict()
    assert deaths == {"leptospirosis": 20, "dengue": 1}
    lep = clean[clean["disease"] == "leptospirosis"]
    assert math.isclose(20 / 230, 0.0870, abs_tol=5e-5)
    assert lep["case_class"].value_counts().to_dict() == {
        "confirmed": 119, "suspect": 59, "probable": 52}
    assert lep["hospitalised"].sum() == 143
    assert lep["sex"].value_counts().to_dict() == {"M": 155, "F": 75}
    assert lep["band"].value_counts().to_dict() == {"riverside": 189, "coastal": 33, "upland": 8}
    den = clean[clean["disease"] == "dengue"]
    assert den["band"].value_counts().to_dict() == {"riverside": 195, "coastal": 174, "upland": 19}
    assert den["dengue_severity"].value_counts().to_dict() == {
        "no_warning": 241, "warning_signs": 132, "severe": 15}


def test_attack_rates_differ_by_band(clean: pd.DataFrame, brgy: pd.DataFrame) -> None:
    pop = brgy.groupby("band")["population"].sum()
    for disease, expected in {
        "leptospirosis": {"riverside": 19.7, "coastal": 5.6, "upland": 2.6},
        "dengue": {"riverside": 20.3, "coastal": 29.6, "upland": 6.1},
    }.items():
        n = clean[clean["disease"] == disease]["band"].value_counts()
        ar = (n / pop * 10_000).round(1).to_dict()
        assert ar == expected, disease


def test_lepto_epicurve_is_common_source(clean: pd.DataFrame) -> None:
    lep = clean[clean["disease"] == "leptospirosis"].dropna(subset=["date_onset"])
    assert lep["date_onset"].min() >= pd.Timestamp("2026-07-20")
    assert lep["date_onset"].max() <= pd.Timestamp("2026-08-31")
    peak = lep["date_onset"].dt.isocalendar().week.value_counts().idxmax()
    assert peak == 31  # 27 Jul – 2 Aug
    adults = lep["age"].between(15, 64).mean()
    assert adults > 0.75


def test_dengue_skews_young(clean: pd.DataFrame) -> None:
    den = clean[clean["disease"] == "dengue"]
    assert den["age"].between(5, 24).mean() > 0.5


# ---------------------------------------------------------------------------
# Case-control study
# ---------------------------------------------------------------------------
def _odds_ratio(df: pd.DataFrame, exposure: str) -> float:
    t = pd.crosstab(df[exposure], df["case"])
    return t.loc[1, 1] * t.loc[0, 0] / (t.loc[1, 0] * t.loc[0, 1])


def _mantel_haenszel(df: pd.DataFrame, exposure: str, stratum: str) -> float:
    num = den = 0.0
    for _, s in df.groupby(stratum):
        n = len(s)
        e, c = s[exposure] == 1, s["case"] == 1
        num += (e & c).sum() * (~e & ~c).sum() / n
        den += (e & ~c).sum() * (~e & c).sum() / n
    return num / den


def test_case_control_design(cc: pd.DataFrame, clean: pd.DataFrame) -> None:
    assert list(cc.columns) == ["study_id", "matched_set", "status", "case", "case_id",
                                "barangay_id", "barangay", "age", "sex", "waded_floodwater",
                                "wore_boots", "skin_wound", "doxy_prophylaxis", "cleanup_work",
                                "rats_near_home"]
    assert len(cc) == 360 and cc["case"].sum() == 120
    assert (cc.groupby("matched_set")["case"].agg(["sum", "size"]) == [1, 3]).all().all()
    assert (cc.groupby("matched_set")["barangay_id"].nunique() == 1).all()
    assert cc["age"].min() >= 15
    assert cc.loc[cc["waded_floodwater"] == 0, "wore_boots"].isna().all()
    cases = cc[cc["case"] == 1].merge(clean, on="case_id", suffixes=("", "_ll"))
    assert len(cases) == 120
    assert (cases["band"] == "riverside").all()
    assert set(cases["case_class"]) == {"probable", "confirmed"}
    known = cases.dropna(subset=["waded_floodwater_ll"])
    assert (known["waded_floodwater"] == known["waded_floodwater_ll"]).all()


def test_case_control_headline_ors(cc: pd.DataFrame) -> None:
    assert round(_odds_ratio(cc, "waded_floodwater"), 2) == 5.57
    assert round(_mantel_haenszel(cc, "waded_floodwater", "cleanup_work"), 2) == 4.28
    waders = cc[cc["waded_floodwater"] == 1]
    assert round(_odds_ratio(waders, "wore_boots"), 2) == 0.35
    assert round(_odds_ratio(cc, "doxy_prophylaxis"), 2) == 0.43
    assert round(_odds_ratio(cc, "skin_wound"), 2) == 3.03
    assert round(_odds_ratio(cc, "cleanup_work"), 2) == 3.20
    assert round(_odds_ratio(cc, "rats_near_home"), 2) == 1.03


def test_true_design_values(gen: ModuleType) -> None:
    assert gen.TRUE_OR["waded_without_boots"] == 6.0
    assert gen.TRUE_OR["doxy_prophylaxis"] == 0.30
    assert math.isclose(gen.TRUE_OR["waded_with_boots"] / gen.TRUE_OR["waded_without_boots"],
                        0.30)


# ---------------------------------------------------------------------------
# Weekly dengue series
# ---------------------------------------------------------------------------
def test_weekly_schema_and_span(weekly: pd.DataFrame) -> None:
    assert list(weekly.columns) == ["iso_year", "iso_week", "morbidity_week", "week_start",
                                    "cases", "rainfall_mm"]
    assert weekly["morbidity_week"].iloc[0] == "2019-W01"
    assert weekly["morbidity_week"].iloc[-1] == "2026-W39"
    assert len(weekly) == 404 and weekly["morbidity_week"].is_unique
    starts = pd.to_datetime(weekly["week_start"])
    assert (starts.dt.dayofweek == 0).all() and (starts.diff().dropna().dt.days == 7).all()
    iso = starts.dt.isocalendar()
    assert (iso["year"].to_numpy() == weekly["iso_year"].to_numpy()).all()
    assert (iso["week"].to_numpy() == weekly["iso_week"].to_numpy()).all()
    assert "2020-W53" in set(weekly["morbidity_week"])


def test_weekly_matches_line_list(weekly: pd.DataFrame, clean: pd.DataFrame) -> None:
    den = clean[clean["disease"] == "dengue"]
    wk = den["date_onset"].dt.isocalendar()
    by_week = wk[wk["year"] == 2026].groupby("week").size()
    w26 = weekly[(weekly["iso_year"] == 2026) & (weekly["iso_week"] >= 30)]
    assert w26["cases"].tolist() == by_week.loc[30:39].tolist()
    assert by_week.get(40, 0) == len(den) - w26["cases"].sum()  # onsets 28–30 Sep (W40)


def test_weekly_threshold_crossing(gen: ModuleType, weekly: pd.DataFrame) -> None:
    thr = gen.epidemic_threshold(weekly)
    w26 = weekly[weekly["iso_year"] == 2026].set_index("iso_week")["cases"]
    above = [w for w, n in w26.items() if n > thr[w]]
    assert above[0] == 32
    assert above == list(range(32, 40))
    assert round(float(thr[32]), 1) == 17.5 and w26[32] == 33


def test_weekly_seasonality_covid_and_rain_lead(weekly: pd.DataFrame) -> None:
    totals = weekly.groupby("iso_year")["cases"].sum()
    assert totals[2019] == totals[:2025].max()  # 2019-style epidemic year
    assert totals[2020] < 0.6 * totals[2022] and totals[2021] < 0.6 * totals[2022]
    month = pd.to_datetime(weekly["week_start"]).dt.month
    assert weekly[month.between(7, 10)]["cases"].mean() > 2 * weekly[month <= 4]["cases"].mean()
    corr = {lag: weekly["rainfall_mm"].shift(lag).corr(weekly["cases"]) for lag in range(13)}
    assert 6 <= max(corr, key=corr.get) <= 8
    assert weekly.loc[weekly["rainfall_mm"].idxmax(), "morbidity_week"] == "2026-W29"


# ---------------------------------------------------------------------------
# 7-1-7 signals
# ---------------------------------------------------------------------------
def test_signals_717(signals: pd.DataFrame, brgy: pd.DataFrame) -> None:
    assert list(signals.columns) == ["event_id", "disease", "barangay", "date_emergence",
                                     "date_detection", "date_notification",
                                     "date_response_complete", "bottleneck"]
    assert len(signals) == 40 and signals["event_id"].is_unique
    assert set(signals["barangay"]) <= set(brgy["barangay"])
    det = (signals["date_detection"] - signals["date_emergence"]).dt.days
    note = (signals["date_notification"] - signals["date_detection"]).dt.days
    resp = (signals["date_response_complete"] - signals["date_notification"]).dt.days
    assert (det >= 0).all() and (note >= 0).all() and (resp >= 0).all()
    assert ((det <= 7).sum(), (note <= 1).sum(), (resp <= 7).sum()) == (26, 31, 27)
    assert ((det <= 7) & (note <= 1) & (resp <= 7)).sum() == 15
    all_met = (det <= 7) & (note <= 1) & (resp <= 7)
    assert (signals.loc[all_met, "bottleneck"] == "none").all()
    assert (signals.loc[~all_met, "bottleneck"] != "none").all()
    assert signals["date_response_complete"].max() <= pd.Timestamp("2026-09-30")
    story = signals.iloc[-2:]  # the post-Amihan events emerge last
    assert list(story["disease"]) == ["leptospirosis", "dengue"]
    assert list(story["barangay"]) == ["Ilog", "Baybay"]


# ---------------------------------------------------------------------------
# Real regional statistics
# ---------------------------------------------------------------------------
def test_regions_join_topojson_and_sources() -> None:
    reg = pd.read_csv(PH / "ph_regions_stats.csv", dtype={"region_id": str, "psgc": str})
    topo = json.loads((PH / "ph_regions.topo.json").read_text(encoding="utf-8"))
    codes = {g["properties"]["adm1_psgc"] for g in topo["objects"]["PH_Adm1_Regions"]["geometries"]}
    assert len(reg) == 18 and reg["adm1_psgc"].is_unique
    assert set(reg["adm1_psgc"]) == codes
    assert (reg["psgc"].str.len() == 10).all()
    research = json.loads((REPO / "book_ph" / "research" /
                           "ph_surveillance_research_2026-11-09.json").read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in research["regions"]["regs"]}
    ncr = reg.set_index("region_short").loc["NCR"]
    assert ncr["population_2024"] == by_id["13"]["population2024"]["value"] == 14_001_751
    value_cols = [c for c in reg.columns if c + "_source_url" in reg.columns]
    assert len(value_cols) == 13
    for col in value_cols:
        has = reg[col].notna()
        assert reg.loc[has, f"{col}_year"].notna().all(), col
        assert set(reg.loc[has, f"{col}_source"]) <= {"cited", "derived"}, col
        cited = has & (reg[f"{col}_source"] == "cited")
        urls = reg.loc[cited, f"{col}_source_url"].astype(str)
        assert urls.str.startswith("https://").all(), col
        assert reg.loc[~has, [f"{col}_year", f"{col}_source", f"{col}_source_url"]] \
            .isna().all().all(), col
    assert reg["urbanization_2020_pct"].isna().all()  # research has no regional values
    assert reg["population_2020"].isna().sum() == 2  # XII and BARMM not re-aggregated
