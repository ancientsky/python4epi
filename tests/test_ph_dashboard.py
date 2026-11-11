"""Tests for the Bantay Santa Luz dashboard generator (``scripts/build_ph_dashboard.py``)."""

from __future__ import annotations

import importlib.util
import json
import math
import re
from html.parser import HTMLParser
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_ph_dashboard.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("build_ph_dashboard", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dash = _load_module()


@pytest.fixture(scope="module")
def data():
    return dash.load_data()


@pytest.fixture(scope="module")
def pages(tmp_path_factory) -> dict[str, str]:
    out = {}
    for lang in dash.LANGS:
        page = dash.build_dashboard(lang, tmp_path_factory.mktemp(lang) / "dashboard")
        assert page.name == "index.html"
        out[lang] = page.read_text(encoding="utf-8")
    return out


class _Cells(HTMLParser):
    """Collect the <td> texts of every table of people counts (``table.counts``)."""

    def __init__(self) -> None:
        super().__init__()
        self.cells: list[str] = []
        self.tables = 0
        self._in_counts = False
        self._in_td = False
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._in_counts = "counts" in (dict(attrs).get("class") or "").split()
            self.tables += self._in_counts
        if tag == "td" and self._in_counts:
            self._in_td, self._buf = True, ""

    def handle_endtag(self, tag):
        if tag == "td" and self._in_td:
            self.cells.append(self._buf.strip())
            self._in_td = False

    def handle_data(self, data):
        if self._in_td:
            self._buf += data


def _payload(page: str) -> dict:
    match = re.search(r'<script type="application/json" id="dash-data">(.*?)</script>', page,
                      re.DOTALL)
    assert match
    return json.loads(match.group(1))


# ----------------------------------------------------------------------------- pages


def test_pages_are_self_contained(pages):
    for lang, page in pages.items():
        assert page.startswith("<!DOCTYPE html>")
        assert '<a href="../">' in page  # back to the edition's home page
        # No external resource: every src/href of a script, stylesheet or image is local.
        for tag in re.findall(r"<(?:script|link|img|iframe|source|video|audio)\b[^>]*>", page):
            for url in re.findall(r'(?:src|href)="([^"]*)"', tag):
                assert url.startswith("data:") or "http" not in url, tag
        assert "<script src" not in page and 'rel="stylesheet"' not in page
        for url in re.findall(r"url\(([^)]*)\)", page):
            assert url.strip("'\"").startswith(("data:", "#")), url
        assert "@import" not in page
        # Every link is relative (the post-build link check resolves them).
        for href in re.findall(r'href="([^"]*)"', page):
            assert not href.startswith(("http", "//", "/")), href
        assert f'lang="{ {"en": "en", "zh": "zh-Hant", "fil": "fil"}[lang] }"' in page


def test_size_is_sane(pages):
    for page in pages.values():
        assert len(page.encode("utf-8")) < 1_500_000


def test_output_is_deterministic(tmp_path, pages):
    again = dash.build_dashboard("en", tmp_path / "again").read_text(encoding="utf-8")
    assert again == pages["en"]


def test_invalid_language_rejected(tmp_path):
    with pytest.raises(ValueError, match="lang"):
        dash.build_dashboard("es", tmp_path)


def test_link_back_to_chapter_and_languages(pages):
    assert 'href="../chapters/dashboard/"' in pages["en"]
    assert 'href="../zh/dashboard/"' in pages["en"]
    assert 'href="../../fil/dashboard/"' in pages["zh"]
    assert 'href="../../dashboard/"' in pages["fil"]


def test_as_of_stamp(pages):
    assert "As of 30 Sept 2026" in pages["en"]
    assert "2026 年 9 月 30 日" in pages["zh"]
    assert "30 Setyembre 2026" in pages["fil"]


# ----------------------------------------------------------------------------- numbers


def test_kpis_match_readme(data):
    k = dash.compute_kpis(data)
    assert k["cases"] == {"leptospirosis": 230, "dengue": 388, "total": 618}
    assert k["deaths"] == {"leptospirosis": 20, "dengue": 1, "total": 21}
    assert math.isclose(k["cfr_pct"]["leptospirosis"], 8.7)
    assert math.isclose(k["cfr_pct"]["dengue"], 0.3)
    assert k["hospitalised"]["leptospirosis"] == 143 and k["hospitalised"]["dengue"] == 206
    assert k["weeks_above"] == 8 and k["first_above"] == "2026-W32"
    assert k["median_age"] == {"leptospirosis": 32, "dengue": 18}
    assert k["last_lepto_onset"].isoformat() == "2026-08-23"
    assert k["lab_median_days"]["leptospirosis"] == 18


def test_kpis_shown_on_page(pages):
    for page in pages.values():
        for shown in ("618", "21", "8.7%", "0.3%", "349"):
            assert f">{shown}</p>" in page


def test_threshold_matches_readme(data):
    thr = dash.epidemic_threshold(data["weekly"])
    assert math.isclose(round(thr[32], 1), 17.5)


def test_case_control_matches_readme(data):
    rows = {r["key"]: r for r in dash.case_control_ors(data)}
    assert (rows["waded"]["or"], rows["waded"]["lo"], rows["waded"]["hi"]) == (5.57, 3.41, 9.10)
    assert rows["waded_adj"]["or"] == 4.28
    assert rows["boots"]["or"] == 0.35 and rows["doxy"]["or"] == 0.43
    assert rows["rats"]["kind"] == "null" and rows["doxy"]["kind"] == "protective"


def test_717_matches_readme(data):
    t = dash.timeliness_717(data)
    assert [g["met"] for g in t["targets"]] == [26, 31, 27]
    assert t["all"]["met"] == 15


def test_band_rates_match_readme(data):
    rates = dash.band_rates(data)
    assert rates["leptospirosis"]["riverside"] == 19.7
    assert rates["dengue"]["coastal"] == 29.6


# ----------------------------------------------------------------------------- privacy


def test_suppress_small_cells_primary_and_secondary():
    t = pd.DataFrame({"M": [12, 3, 20], "F": [9, 0, 2]})
    out = dash.suppress_small_cells(t)
    assert out["M"].tolist() == ["x", "<5", 20]
    assert out["F"].tolist() == ["x", 0, "<5"]
    primary_only = dash.suppress_small_cells(t, secondary_axis=None)
    assert primary_only["M"].tolist() == [12, "<5", 20]
    # Two small cells in a column already protect each other: no secondary needed.
    two = dash.suppress_small_cells(pd.DataFrame({"A": [1, 4, 30]}))
    assert two["A"].tolist() == ["<5", "<5", 30]


def test_suppression_rejects_bad_input():
    with pytest.raises(ValueError):
        dash.suppression_status(pd.DataFrame({"A": [-1, 3]}))
    with pytest.raises(ValueError):
        dash.suppression_status(pd.DataFrame({"A": [1]}), threshold=0)


def test_no_small_values_in_public_tables(pages):
    for page in pages.values():
        parser = _Cells()
        parser.feed(page)
        assert parser.tables == 4 and parser.cells
        bad = [c for c in parser.cells if re.fullmatch(r"[1-4]", c)]
        assert not bad, bad
        assert "&lt;5" in page


def test_no_small_values_in_embedded_data(pages):
    def cells(payload):
        for w in payload["curve"]["weeks"]:
            yield from (w["leptospirosis"], w["dengue"])
        for w in payload["thr"]["weeks"]:
            yield w["cell"]
        for f in payload["map"]["features"]:
            yield from (f["leptospirosis"]["cell"], f["dengue"]["cell"])
        for d in ("leptospirosis", "dengue"):
            for s in ("M", "F"):
                yield from payload["pyramid"][d][s]

    for page in pages.values():
        payload = _payload(page)
        seen = list(cells(payload))
        assert seen
        for value, status in seen:
            if status == 0:
                assert value == 0 or value >= dash.SMALL_CELL
            else:
                assert value is None
        # a suppressed cell never leaks a rate
        for f in payload["map"]["features"]:
            for d in ("leptospirosis", "dengue"):
                if f[d]["cell"][1]:
                    assert f[d]["rate"] is None


def test_no_case_level_data_in_page(pages):
    for page in pages.values():
        assert "SLC-" not in page and "CC-0" not in page
        assert "date_onset" not in page and "Patient" not in page


def test_secondary_suppression_used_in_pyramid(pages):
    payload = _payload(pages["en"])
    statuses = [c[1] for s in ("M", "F") for c in payload["pyramid"]["dengue"][s]]
    assert 2 in statuses  # one sex column held a single small cell


# ----------------------------------------------------------------------------- forecast


def test_forecast_absent_says_so(data, tmp_path, pages):
    assert dash.load_forecast(data, tmp_path) is None
    if _payload(pages["en"])["forecast"] is None:
        assert "Forecast not available" in pages["en"]


def test_forecast_used_only_when_fingerprint_matches(data, tmp_path):
    from epi_learning.tsfm import QUANTILE_LEVELS, input_fingerprint

    y = data["weekly"]["cases"].to_numpy(dtype=float)
    horizon = 4
    quantiles = [[[10.0 + k + q for q in range(len(QUANTILE_LEVELS))] for k in range(horizon)]]
    entry = {"fingerprint": input_fingerprint([y], horizon), "horizon": horizon,
             "shape": [1, horizon], "forecast": [[14.0, 15.0, 16.0, 17.0]],
             "quantiles": quantiles}
    cache = {"schema": 1, "licence": "test", "producer": {}, "entries": {"next": entry}}
    (tmp_path / "ph_test.json").write_text(json.dumps(cache), encoding="utf-8")
    fc = dash.load_forecast(data, tmp_path)
    assert fc is not None
    assert [w["wk"] for w in fc["weeks"]] == ["W40", "W41", "W42", "W43"]
    assert fc["weeks"][0]["med"] == 14.0 and fc["weeks"][0]["lo"] == 10.0
    # a different input (e.g. a backtest) is never shown as a forecast
    entry["fingerprint"] = input_fingerprint([y[:-5]], horizon)
    (tmp_path / "ph_test.json").write_text(json.dumps(cache), encoding="utf-8")
    assert dash.load_forecast(data, tmp_path) is None
