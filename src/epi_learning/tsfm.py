"""Run a time-series foundation model (TimesFM 3.0) or replay its cached forecasts.

The book build executes every notebook, must stay fast, and should not download
a 1.3 GB checkpoint on every CI run. This module lets a notebook show the
genuine ``timesfm3`` calls while the build replays forecasts that a real run
produced earlier:

* **model path** – ``timesfm3`` is installed (Colab, or ``uv sync --group
  timesfm``): :func:`load_model` returns a real ``TimesFM3Evaluator`` and
  :func:`forecast_batch` calls its ``predict_batch``.
* **cache path** – ``timesfm3`` is missing, or the book build forces it
  (``EPI_TSFM_MODE=cache``): :func:`load_model` returns ``None`` and
  :func:`forecast_batch` reads the committed JSON cache under
  ``data/tsfm_cache/``. Every cache entry stores a fingerprint of its inputs,
  so a notebook whose data changed fails loudly instead of showing stale
  forecasts.
* **record path** – ``EPI_TSFM_MODE=record`` (set by
  ``scripts/make_timesfm_cache.py``): runs the model and writes each result
  into the cache file.

Mode selection (environment variable ``EPI_TSFM_MODE``):

``auto`` (default)
    model if ``timesfm3`` can be imported, otherwise cache.
``model``
    always run the model (error if ``timesfm3`` is missing).
``cache``
    always replay the cache (what the book build uses).
``record``
    run the model and save every result into the cache.

Licence: the TimesFM *code* is Apache-2.0, but the TimesFM 3.0 *weights*
(``google/timesfm-3.0-pytorch``) are under the TimesFM Non-Commercial License
v1.0: research, teaching and evaluation only, no commercial or production use.
The cached forecasts are model Outputs produced under that licence for this
non-commercial teaching material.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

#: Hugging Face repo of the TimesFM 3.0 PyTorch checkpoint.
CHECKPOINT = "google/timesfm-3.0-pytorch"

#: The nine quantile levels TimesFM 3.0 returns (last axis of ``quantiles``).
QUANTILE_LEVELS: tuple[float, ...] = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)

#: Environment variable that selects the path (see the module docstring).
MODE_ENV = "EPI_TSFM_MODE"
MODES = ("auto", "model", "cache", "record")

#: Default directory of the committed caches (relative to the repository root).
CACHE_DIR = Path("data") / "tsfm_cache"

#: Short licence statement stored in every cache file.
LICENCE_NOTE = (
    "Forecasts produced by TimesFM 3.0 weights (google/timesfm-3.0-pytorch) under the "
    "TimesFM Non-Commercial License v1.0: non-commercial, non-production use only."
)

#: Decimals kept in the cache (forecasts) and in input fingerprints.
_CACHE_DECIMALS = 3
_FINGERPRINT_DECIMALS = 4
_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class TSFMForecast:
    """Forecasts for a batch of series.

    Attributes
    ----------
    forecast:
        Median (point) forecasts, shape ``(n_series, horizon)`` for univariate
        contexts or ``(n_series, n_targets, horizon)`` for multivariate ones.
    quantiles:
        Quantile forecasts with :data:`QUANTILE_LEVELS` on the last axis, shape
        ``forecast.shape + (9,)``.
    source:
        ``"model"`` when TimesFM ran in this session, ``"cache"`` when the
        forecasts were replayed from the committed cache.
    seconds:
        Wall-clock time of the model call (for the cache path: of the original
        recorded run).
    """

    forecast: np.ndarray
    quantiles: np.ndarray
    source: str
    seconds: float

    def quantile(self, level: float) -> np.ndarray:
        """Return the forecasts for one quantile level (e.g. ``0.1``).

        Parameters
        ----------
        level:
            One of :data:`QUANTILE_LEVELS`.

        Returns
        -------
        numpy.ndarray
            Array shaped like :attr:`forecast`.
        """
        for i, q in enumerate(QUANTILE_LEVELS):
            if abs(q - level) < 1e-9:
                return self.quantiles[..., i]
        raise ValueError(f"level must be one of {QUANTILE_LEVELS}, got {level}")


# --------------------------------------------------------------------------- mode


def timesfm_available() -> bool:
    """Return ``True`` when the ``timesfm3`` package (``pip install timesfm[torch]``) imports."""
    try:
        import timesfm3  # noqa: F401
    except ImportError:
        return False
    return True


def resolve_mode(mode: str | None = None) -> str:
    """Resolve the effective mode: ``"model"``, ``"cache"`` or ``"record"``.

    Parameters
    ----------
    mode:
        One of :data:`MODES`; defaults to the ``EPI_TSFM_MODE`` environment
        variable, or ``"auto"`` when that is unset.

    Returns
    -------
    str
        ``"model"``, ``"cache"`` or ``"record"`` (``"auto"`` is resolved).
    """
    chosen = (mode or os.environ.get(MODE_ENV) or "auto").strip().lower()
    if chosen not in MODES:
        raise ValueError(f"{MODE_ENV} must be one of {MODES}, got {chosen!r}")
    if chosen == "auto":
        return "model" if timesfm_available() else "cache"
    return chosen


def default_device() -> str:
    """Return ``"cuda"`` when a GPU is visible to PyTorch, else ``"cpu"``."""
    try:
        import torch
    except ImportError:
        return "cpu"
    return "cuda" if torch.cuda.is_available() else "cpu"


def cache_path(name: str, cache_dir: Path | str | None = None) -> Path:
    """Return the path of cache file *name* (``.json`` is appended if missing).

    Parameters
    ----------
    name:
        Cache file name, e.g. ``"ch11_timesfm"``.
    cache_dir:
        Directory; defaults to :data:`CACHE_DIR` (relative to the working
        directory, which the book build and the Colab cell set to the repo root).

    Returns
    -------
    Path
    """
    if not name:
        raise ValueError("cache name must be a non-empty string")
    file_name = name if name.endswith(".json") else f"{name}.json"
    return Path(cache_dir if cache_dir is not None else CACHE_DIR) / file_name


# ------------------------------------------------------------------ fingerprints


def _as_2d_float(values: Any, what: str) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    if arr.ndim not in (1, 2):
        raise ValueError(f"{what} must be 1-D or 2-D, got shape {arr.shape}")
    if arr.size == 0:
        raise ValueError(f"{what} must not be empty")
    return arr


def input_fingerprint(
    contexts: Sequence[Any],
    horizon: int,
    past_only_covariates: Sequence[Any | None] | None = None,
    past_future_covariates: Sequence[Any | None] | None = None,
) -> str:
    """Return a SHA-256 fingerprint of a forecasting request.

    Values are rounded to 4 decimals first, so the same synthetic series
    regenerated on another machine (last-bit floating point differences)
    still matches.

    Parameters
    ----------
    contexts, horizon, past_only_covariates, past_future_covariates:
        Exactly what is passed to :func:`forecast_batch`.

    Returns
    -------
    str
        64-character hex digest.
    """
    digest = hashlib.sha256()
    digest.update(f"h={int(horizon)};n={len(contexts)}".encode())
    groups: list[tuple[str, Sequence[Any | None] | None]] = [
        ("ctx", contexts),
        ("po", past_only_covariates),
        ("pf", past_future_covariates),
    ]
    for label, group in groups:
        if group is None:
            digest.update(f"|{label}:none".encode())
            continue
        for i, item in enumerate(group):
            if item is None:
                digest.update(f"|{label}{i}:none".encode())
                continue
            arr = np.round(_as_2d_float(item, f"{label}[{i}]"), _FINGERPRINT_DECIMALS)
            arr = arr + 0.0  # turn -0.0 into 0.0
            digest.update(f"|{label}{i}:{arr.shape}".encode())
            digest.update(np.ascontiguousarray(arr).tobytes())
    return digest.hexdigest()


# ----------------------------------------------------------------------- caching


def _empty_cache() -> dict[str, Any]:
    return {"schema": _SCHEMA_VERSION, "licence": LICENCE_NOTE, "producer": {}, "entries": {}}


def read_cache(path: Path | str) -> dict[str, Any]:
    """Read a cache file; return an empty cache structure when it does not exist.

    Parameters
    ----------
    path:
        Cache file path (see :func:`cache_path`).

    Returns
    -------
    dict
        ``{"schema", "licence", "producer", "entries"}``.
    """
    path = Path(path)
    if not path.is_file():
        return _empty_cache()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != _SCHEMA_VERSION:
        raise ValueError(f"{path}: unsupported cache schema {payload.get('schema')!r}")
    return payload


def _write_cache(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload["entries"] = dict(sorted(payload["entries"].items()))
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
    path.write_text(text + "\n", encoding="utf-8")


def _producer_info(model: Any) -> dict[str, Any]:
    info: dict[str, Any] = {"checkpoint": CHECKPOINT}
    try:
        from importlib.metadata import version

        info["timesfm_version"] = version("timesfm")
    except Exception:  # pragma: no cover - metadata missing
        info["timesfm_version"] = None
    try:
        import torch

        info["torch_version"] = torch.__version__
        info["torch_threads"] = torch.get_num_threads()
    except ImportError:  # pragma: no cover
        pass
    config = getattr(model, "config", None)
    if config is not None:
        info["checkpoint"] = getattr(config, "checkpoint_path", CHECKPOINT)
        info["device"] = str(getattr(model, "device", getattr(config, "device", None)))
    try:
        from huggingface_hub import HfApi

        info["revision"] = HfApi().model_info(info["checkpoint"]).sha
    except Exception:
        info["revision"] = None
    info["date"] = _dt.date.today().isoformat()
    return info


def describe_cache(path: Path | str) -> str:
    """Return a one-line description of who produced the cache file.

    Parameters
    ----------
    path:
        Cache file path.

    Returns
    -------
    str
    """
    payload = read_cache(path)
    producer = payload.get("producer") or {}
    if not payload["entries"]:
        return f"{path}: (empty – run scripts/make_timesfm_cache.py)"
    revision = (producer.get("revision") or "unknown")[:10]
    return (
        f"{path}: {len(payload['entries'])} cached requests, produced on "
        f"{producer.get('date', '?')} by {producer.get('checkpoint', CHECKPOINT)} "
        f"(HF revision {revision}, timesfm {producer.get('timesfm_version', '?')}, "
        f"device {producer.get('device', '?')})"
    )


# ------------------------------------------------------------------------- model


def load_model(
    cache_file: Path | str | None = None,
    *,
    mode: str | None = None,
    device: str | None = None,
    per_core_batch_size: int = 32,
    checkpoint: str = CHECKPOINT,
    verbose: bool = True,
) -> Any | None:
    """Load TimesFM 3.0, or return ``None`` when forecasts come from the cache.

    The model branch is exactly the official recipe::

        from timesfm3 import TimesFM3Evaluator, ModelConfig
        config = ModelConfig(checkpoint_path="google/timesfm-3.0-pytorch",
                             per_core_batch_size=32, device="cpu")
        model = TimesFM3Evaluator(config)

    Parameters
    ----------
    cache_file:
        Cache file that the cache path will read; only used for the message.
    mode:
        Overrides ``EPI_TSFM_MODE`` (see :func:`resolve_mode`).
    device:
        ``"cpu"`` or ``"cuda"``; defaults to :func:`default_device`.
    per_core_batch_size:
        How many series one forward pass handles.
    checkpoint:
        Hugging Face repo id or local directory of the weights.
    verbose:
        Print which path was taken.

    Returns
    -------
    TimesFM3Evaluator or None
    """
    if per_core_batch_size < 1:
        raise ValueError(f"per_core_batch_size must be >= 1, got {per_core_batch_size}")
    effective = resolve_mode(mode)
    if effective == "cache":
        if verbose:
            print("[tsfm] path = CACHE: timesfm3 is not used in this session;")
            print("       forecasts are replayed from a real TimesFM 3.0 run.")
            if cache_file is not None:
                print(f"       {describe_cache(cache_file)}")
        return None
    if not timesfm_available():
        raise ImportError(
            f"{MODE_ENV}={effective} needs the timesfm package: "
            "pip install 'timesfm[torch]>=3.0.2'  (or: uv sync --group timesfm)"
        )
    from timesfm3 import ModelConfig, TimesFM3Evaluator

    chosen_device = device or default_device()
    start = time.perf_counter()
    config = ModelConfig(
        checkpoint_path=checkpoint,
        per_core_batch_size=per_core_batch_size,
        device=chosen_device,
    )
    model = TimesFM3Evaluator(config)
    if verbose:
        n_params = sum(p.numel() for p in model.model.parameters())
        print(
            f"[tsfm] path = MODEL ({effective}): {checkpoint} on {chosen_device}, "
            f"{n_params / 1e6:.0f}M parameters, loaded in {time.perf_counter() - start:.1f}s"
        )
    return model


def _list_or_none(group: Sequence[Any | None] | None, n: int, what: str) -> list[Any] | None:
    if group is None:
        return None
    items = list(group)
    if len(items) != n:
        raise ValueError(f"{what} must have one entry per context ({n}), got {len(items)}")
    if all(item is None for item in items):
        return None
    return [None if item is None else np.asarray(item, dtype=np.float32) for item in items]


def forecast_batch(
    model: Any | None,
    contexts: Sequence[Any],
    horizon: int,
    *,
    cache_key: str,
    cache_file: Path | str,
    past_only_covariates: Sequence[Any | None] | None = None,
    past_future_covariates: Sequence[Any | None] | None = None,
    mode: str | None = None,
    verbose: bool = True,
) -> TSFMForecast:
    """Forecast a batch of series with TimesFM 3.0, or replay the cached result.

    Parameters
    ----------
    model:
        The object returned by :func:`load_model` (``None`` → cache path).
    contexts:
        One history per series: 1-D arrays (univariate) or ``(n_targets, T)``
        arrays (multivariate). Lengths may differ between series.
    horizon:
        Steps to forecast (>= 1).
    cache_key:
        Name of this request inside the cache file, e.g. ``"dengue_backtest"``.
    cache_file:
        Cache file path (see :func:`cache_path`).
    past_only_covariates:
        Optional, one ``(n_cov, T)`` array (or ``None``) per context: covariates
        known only up to the forecast origin.
    past_future_covariates:
        Optional, one ``(n_cov, T + horizon)`` array (or ``None``) per context:
        covariates also known over the forecast horizon (e.g. a weather forecast).
    mode:
        Overrides ``EPI_TSFM_MODE`` for this call.
    verbose:
        Print where the forecasts came from.

    Returns
    -------
    TSFMForecast
    """
    if horizon < 1:
        raise ValueError(f"horizon must be >= 1, got {horizon}")
    if not cache_key:
        raise ValueError("cache_key must be a non-empty string")
    contexts = list(contexts)
    if not contexts:
        raise ValueError("contexts must contain at least one series")
    po = _list_or_none(past_only_covariates, len(contexts), "past_only_covariates")
    pf = _list_or_none(past_future_covariates, len(contexts), "past_future_covariates")
    if pf is not None:
        for i, (ctx, cov) in enumerate(zip(contexts, pf)):
            if cov is not None and np.atleast_2d(cov).shape[-1] != np.shape(ctx)[-1] + horizon:
                raise ValueError(
                    f"past_future_covariates[{i}] must cover context + horizon "
                    f"({np.shape(ctx)[-1] + horizon} steps), got {np.atleast_2d(cov).shape[-1]}"
                )
    fingerprint = input_fingerprint(contexts, horizon, po, pf)
    path = Path(cache_file)

    if model is None:
        return _replay(path, cache_key, fingerprint, verbose)

    start = time.perf_counter()
    outputs = list(
        model.predict_batch(
            [np.asarray(c, dtype=np.float32) for c in contexts],
            horizon=horizon,
            past_only_covariates=po,
            past_future_covariates=pf,
            return_quantiles=True,
        )
    )
    seconds = time.perf_counter() - start
    forecast = np.stack([np.asarray(o.forecast, dtype=np.float64) for o in outputs])
    quantiles = np.stack([np.asarray(o.quantiles, dtype=np.float64) for o in outputs])
    if verbose:
        print(
            f"[tsfm] {cache_key}: TimesFM forecast {len(contexts)} series × {horizon} steps "
            f"in {seconds:.1f}s"
        )
    if resolve_mode(mode) == "record":
        _record(path, cache_key, fingerprint, horizon, forecast, quantiles, seconds, model)
        if verbose:
            print(f"[tsfm] {cache_key}: recorded into {path}")
    return TSFMForecast(forecast=forecast, quantiles=quantiles, source="model", seconds=seconds)


def _record(
    path: Path,
    key: str,
    fingerprint: str,
    horizon: int,
    forecast: np.ndarray,
    quantiles: np.ndarray,
    seconds: float,
    model: Any,
) -> None:
    payload = read_cache(path)
    payload["licence"] = LICENCE_NOTE
    payload["producer"] = _producer_info(model)
    payload["entries"][key] = {
        "fingerprint": fingerprint,
        "horizon": int(horizon),
        "shape": list(forecast.shape),
        "seconds": round(float(seconds), 2),
        "forecast": np.round(forecast, _CACHE_DECIMALS).tolist(),
        "quantiles": np.round(quantiles, _CACHE_DECIMALS).tolist(),
    }
    _write_cache(path, payload)


def _replay(path: Path, key: str, fingerprint: str, verbose: bool) -> TSFMForecast:
    payload = read_cache(path)
    entry = payload["entries"].get(key)
    hint = (
        "Regenerate it with a real run: "
        f"uv run --group timesfm python scripts/make_timesfm_cache.py <notebook> "
        f"(cache: {path})"
    )
    if entry is None:
        raise KeyError(f"No cached TimesFM forecast {key!r} in {path}. {hint}")
    if entry["fingerprint"] != fingerprint:
        raise ValueError(
            f"Cached TimesFM forecast {key!r} in {path} was made from different inputs "
            f"(the data or horizon changed since it was recorded). {hint}"
        )
    forecast = np.asarray(entry["forecast"], dtype=np.float64)
    quantiles = np.asarray(entry["quantiles"], dtype=np.float64)
    if verbose:
        date = (payload.get("producer") or {}).get("date", "?")
        print(
            f"[tsfm] {key}: replayed {forecast.shape[0]} cached forecasts "
            f"(real TimesFM 3.0 run of {date}, took {entry.get('seconds', '?')}s)"
        )
    return TSFMForecast(
        forecast=forecast,
        quantiles=quantiles,
        source="cache",
        seconds=float(entry.get("seconds", float("nan"))),
    )


# --------------------------------------------------------------------- utilities


def rolling_origin_contexts(
    series: Any, origins: Sequence[int], max_context: int | None = None
) -> list[np.ndarray]:
    """Return the history available at each forecast origin: ``series[:origin]``.

    Use it in both the notebook and the cache script so their inputs match.

    Parameters
    ----------
    series:
        1-D array of the target (or ``(n_targets, T)`` for multivariate).
    origins:
        Forecast origins: each context ends just before index ``origin``.
    max_context:
        Optionally keep only the last ``max_context`` points of each history.

    Returns
    -------
    list of numpy.ndarray
    """
    arr = np.asarray(series, dtype=np.float64)
    length = arr.shape[-1]
    contexts: list[np.ndarray] = []
    for origin in origins:
        if not 1 <= int(origin) <= length:
            raise ValueError(f"origin must be in [1, {length}], got {origin}")
        start = 0 if max_context is None else max(0, int(origin) - int(max_context))
        contexts.append(arr[..., start : int(origin)].copy())
    return contexts


def coverage(actual: Any, lower: Any, upper: Any) -> float:
    """Share of observations inside ``[lower, upper]`` (empirical interval coverage).

    Parameters
    ----------
    actual, lower, upper:
        Arrays of the same shape.

    Returns
    -------
    float
        Between 0 and 1.
    """
    a, lo, hi = (np.asarray(x, dtype=np.float64) for x in (actual, lower, upper))
    if not a.shape == lo.shape == hi.shape:
        raise ValueError(f"shapes differ: {a.shape}, {lo.shape}, {hi.shape}")
    if a.size == 0:
        raise ValueError("coverage needs at least one observation")
    return float(np.mean((a >= lo) & (a <= hi)))


def mean_weighted_quantile_loss(actual: Any, quantiles: Any) -> float:
    """Mean pinball (quantile) loss over :data:`QUANTILE_LEVELS`, a CRPS approximation.

    Parameters
    ----------
    actual:
        Observed values, shape ``S``.
    quantiles:
        Forecast quantiles, shape ``S + (9,)``.

    Returns
    -------
    float
        Lower is better; in the units of the series.
    """
    a = np.asarray(actual, dtype=np.float64)
    q = np.asarray(quantiles, dtype=np.float64)
    if q.shape != a.shape + (len(QUANTILE_LEVELS),):
        raise ValueError(f"quantiles must have shape {a.shape + (len(QUANTILE_LEVELS),)}")
    levels = np.asarray(QUANTILE_LEVELS)
    diff = a[..., None] - q
    loss = np.maximum(levels * diff, (levels - 1) * diff)
    return float(2 * loss.mean())
