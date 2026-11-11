"""Tests for epi_learning.tsfm (cache path, fingerprints, metrics) without the real model."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from epi_learning import tsfm

REPO_CACHE = Path("data/tsfm_cache/ch11_timesfm.json")


class FakeOutput:
    def __init__(self, forecast: np.ndarray, quantiles: np.ndarray) -> None:
        self.forecast = forecast
        self.quantiles = quantiles


class FakeModel:
    """Mimics TimesFM3Evaluator.predict_batch: forecast = last value, quantiles = ±k."""

    def __init__(self) -> None:
        self.calls: list[dict] = []

    def predict_batch(self, contexts, horizon, **kwargs):
        self.calls.append({"n": len(contexts), "horizon": horizon, **kwargs})
        for ctx in contexts:
            last = float(np.asarray(ctx)[-1])
            fc = np.full(horizon, last)
            q = fc[:, None] + np.linspace(-4, 4, 9)[None, :]
            yield FakeOutput(fc, q)


def test_resolve_mode(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(tsfm.MODE_ENV, "cache")
    assert tsfm.resolve_mode() == "cache"
    assert tsfm.resolve_mode("record") == "record"
    monkeypatch.setenv(tsfm.MODE_ENV, "auto")
    assert tsfm.resolve_mode() == ("model" if tsfm.timesfm_available() else "cache")
    with pytest.raises(ValueError, match="EPI_TSFM_MODE"):
        tsfm.resolve_mode("sometimes")


def test_cache_path_appends_json(tmp_path: Path):
    assert tsfm.cache_path("abc", tmp_path) == tmp_path / "abc.json"
    assert tsfm.cache_path("abc.json", tmp_path) == tmp_path / "abc.json"
    with pytest.raises(ValueError):
        tsfm.cache_path("")


def test_load_model_cache_mode_returns_none(capsys: pytest.CaptureFixture[str], tmp_path: Path):
    assert tsfm.load_model(tmp_path / "x.json", mode="cache") is None
    assert "CACHE" in capsys.readouterr().out


def test_fingerprint_is_stable_and_sensitive():
    y = np.arange(20, dtype=float)
    base = tsfm.input_fingerprint([y], 7)
    assert base == tsfm.input_fingerprint([y + 1e-7], 7)  # rounding absorbs last-bit noise
    assert base != tsfm.input_fingerprint([y], 8)
    assert base != tsfm.input_fingerprint([y + 0.1], 7)
    assert base != tsfm.input_fingerprint([y], 7, past_only_covariates=[y[None, :]])


def test_record_then_replay_roundtrip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(tsfm, "_producer_info", lambda model: {"date": "2026-01-01"})
    cache = tmp_path / "c.json"
    contexts = tsfm.rolling_origin_contexts(np.arange(30, dtype=float), [10, 20])
    recorded = tsfm.forecast_batch(
        FakeModel(), contexts, 3, cache_key="k", cache_file=cache, mode="record", verbose=False
    )
    assert recorded.source == "model"
    assert recorded.forecast.shape == (2, 3)
    assert recorded.quantiles.shape == (2, 3, 9)

    replayed = tsfm.forecast_batch(
        None, contexts, 3, cache_key="k", cache_file=cache, verbose=False
    )
    assert replayed.source == "cache"
    np.testing.assert_allclose(replayed.forecast, [[9, 9, 9], [19, 19, 19]])
    assert math.isclose(replayed.quantile(0.9)[0, 0], 13.0)
    payload = json.loads(cache.read_text(encoding="utf-8"))
    assert "Non-Commercial" in payload["licence"]


def test_model_mode_does_not_write(tmp_path: Path):
    cache = tmp_path / "c.json"
    model = FakeModel()
    tsfm.forecast_batch(
        model, [np.ones(5)], 2, cache_key="k", cache_file=cache, mode="model", verbose=False
    )
    assert not cache.exists()
    assert model.calls[0]["return_quantiles"] is True


def test_replay_errors_on_missing_or_changed_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(tsfm, "_producer_info", lambda model: {})
    cache = tmp_path / "c.json"
    tsfm.forecast_batch(
        FakeModel(), [np.ones(5)], 2, cache_key="k", cache_file=cache, mode="record", verbose=False
    )
    with pytest.raises(KeyError, match="make_timesfm_cache"):
        tsfm.forecast_batch(None, [np.ones(5)], 2, cache_key="other", cache_file=cache)
    with pytest.raises(ValueError, match="different inputs"):
        tsfm.forecast_batch(None, [np.ones(6)], 2, cache_key="k", cache_file=cache)


def test_covariates_are_validated_and_passed(tmp_path: Path):
    model = FakeModel()
    y = np.arange(10, dtype=float)
    with pytest.raises(ValueError, match="context \\+ horizon"):
        tsfm.forecast_batch(
            model,
            [y],
            3,
            cache_key="k",
            cache_file=tmp_path / "c.json",
            past_future_covariates=[y[None, :]],
            mode="model",
        )
    with pytest.raises(ValueError, match="one entry per context"):
        tsfm.forecast_batch(
            model,
            [y],
            3,
            cache_key="k",
            cache_file=tmp_path / "c.json",
            past_only_covariates=[y, y],
            mode="model",
        )
    tsfm.forecast_batch(
        model,
        [y],
        3,
        cache_key="k",
        cache_file=tmp_path / "c.json",
        past_future_covariates=[np.arange(13.0)[None, :]],
        mode="model",
        verbose=False,
    )
    assert model.calls[-1]["past_future_covariates"][0].shape == (1, 13)


def test_input_validation(tmp_path: Path):
    with pytest.raises(ValueError, match="horizon"):
        tsfm.forecast_batch(None, [np.ones(3)], 0, cache_key="k", cache_file=tmp_path / "c")
    with pytest.raises(ValueError, match="at least one"):
        tsfm.forecast_batch(None, [], 3, cache_key="k", cache_file=tmp_path / "c")
    with pytest.raises(ValueError, match="origin"):
        tsfm.rolling_origin_contexts(np.ones(5), [6])


def test_rolling_origin_contexts_max_context():
    ctx = tsfm.rolling_origin_contexts(np.arange(10.0), [4, 8], max_context=3)
    assert [c.tolist() for c in ctx] == [[1, 2, 3], [5, 6, 7]]


def test_metrics():
    actual = np.array([1.0, 5.0, 10.0])
    assert math.isclose(tsfm.coverage(actual, actual - 1, actual + 1), 1.0)
    assert math.isclose(tsfm.coverage(actual, actual + 1, actual + 2), 0.0)
    perfect = np.repeat(actual[:, None], 9, axis=1)
    assert math.isclose(tsfm.mean_weighted_quantile_loss(actual, perfect), 0.0)
    assert tsfm.mean_weighted_quantile_loss(actual, perfect + 1) > 0
    with pytest.raises(ValueError):
        tsfm.coverage(actual, actual[:2], actual)


def test_committed_cache_is_small_and_attributed():
    assert REPO_CACHE.is_file(), "run scripts/make_timesfm_cache.py to create the cache"
    assert REPO_CACHE.stat().st_size < 500_000
    payload = tsfm.read_cache(REPO_CACHE)
    assert payload["producer"]["checkpoint"] == tsfm.CHECKPOINT
    assert payload["producer"]["date"]
    assert "Non-Commercial" in payload["licence"]
    for key, entry in payload["entries"].items():
        assert len(entry["fingerprint"]) == 64, key
