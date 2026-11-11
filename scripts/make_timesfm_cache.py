"""Regenerate the committed TimesFM 3.0 forecast caches under ``data/tsfm_cache/``.

The book build replays cached forecasts (see ``src/epi_learning/tsfm.py``);
this script produces them with a real model run. It needs the optional
``timesfm`` dependency group and downloads the ~1.3 GB checkpoint once
(into the Hugging Face cache, ``~/.cache/huggingface``)::

    # 1) Re-record every epi_learning.tsfm.forecast_batch(...) call of a notebook
    uv run --group timesfm python scripts/make_timesfm_cache.py \\
        book/chapters/notebooks/11_dl_timesfm.ipynb

    # 2) Cache a rolling-origin backtest of one CSV column, no notebook needed
    uv run --group timesfm python scripts/make_timesfm_cache.py \\
        --csv data/synthetic/some_weekly.csv --column cases \\
        --horizon 4 --origins 20 --cache-file my_chapter --cache-key cases_backtest

Mode 1 runs the notebook's code cells in this process with
``EPI_TSFM_MODE=record``: each ``forecast_batch`` call runs the model and is
written into its cache file under its ``cache_key``. Mode 2 forecasts
``horizon`` steps from each of the last ``origins`` time points of the column
(the contexts are ``epi_learning.tsfm.rolling_origin_contexts(y, origins)``,
so a notebook that builds the same contexts replays the entry).

Licence: TimesFM 3.0 weights are under the TimesFM Non-Commercial License
v1.0 (non-commercial, non-production use only).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def record_notebook(notebook: Path) -> None:
    """Execute *notebook*'s code cells in-process with ``EPI_TSFM_MODE=record``.

    Parameters
    ----------
    notebook:
        Path to the ``.ipynb`` file.
    """
    if not notebook.is_file():
        raise ValueError(f"notebook not found: {notebook}")
    os.environ.setdefault("MPLBACKEND", "Agg")
    from IPython.core.interactiveshell import InteractiveShell

    cells = json.loads(notebook.read_text(encoding="utf-8"))["cells"]
    shell = InteractiveShell.instance()
    start = time.perf_counter()
    for index, cell in enumerate(cells):
        if cell["cell_type"] != "code":
            continue
        source = cell["source"]
        source = "".join(source) if isinstance(source, list) else source
        result = shell.run_cell(source, silent=False)
        if not result.success:
            raise RuntimeError(f"cell {index} ({cell.get('id')}) of {notebook} failed")
    print(f"recorded {notebook} in {time.perf_counter() - start:.1f}s")


def record_csv(
    csv_path: Path,
    column: str,
    horizon: int,
    origins: int,
    cache_file: str,
    cache_key: str,
) -> None:
    """Cache a rolling-origin backtest of one CSV column.

    Parameters
    ----------
    csv_path:
        CSV file with one row per time step, in time order.
    column:
        Numeric column to forecast.
    horizon:
        Steps ahead.
    origins:
        Number of forecast origins: the last ``origins`` time points that
        still leave ``horizon`` observed steps, plus the end of the series.
    cache_file, cache_key:
        Where to store the result (see ``epi_learning.tsfm.cache_path``).
    """
    import pandas as pd

    from epi_learning import tsfm

    if horizon < 1 or origins < 1:
        raise ValueError("horizon and origins must be >= 1")
    frame = pd.read_csv(csv_path)
    if column not in frame.columns:
        raise ValueError(f"column {column!r} not in {csv_path} ({list(frame.columns)})")
    y = frame[column].to_numpy(dtype=float)
    last = len(y)
    origin_list = list(range(max(1, last - horizon - origins + 1), last - horizon + 1)) + [last]
    contexts = tsfm.rolling_origin_contexts(y, origin_list)
    model = tsfm.load_model(mode="record")
    tsfm.forecast_batch(
        model,
        contexts,
        horizon,
        cache_key=cache_key,
        cache_file=tsfm.cache_path(cache_file),
        mode="record",
    )
    print(f"origins: {origin_list[0]}..{origin_list[-2]} and {last} (end of series)")


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("notebooks", nargs="*", type=Path, help="notebooks to re-record")
    parser.add_argument("--csv", type=Path, help="CSV file (mode 2)")
    parser.add_argument("--column", help="column of --csv to forecast")
    parser.add_argument("--horizon", type=int, default=4)
    parser.add_argument("--origins", type=int, default=12)
    parser.add_argument("--cache-file", help="cache file name under data/tsfm_cache/")
    parser.add_argument("--cache-key", help="entry name inside the cache file")
    args = parser.parse_args(argv)
    args.notebooks = [p.resolve() for p in args.notebooks]
    if args.csv is not None:
        args.csv = args.csv.resolve()

    os.chdir(REPO_ROOT)  # notebooks read data/... relative to the repo root
    sys.path.insert(0, str(REPO_ROOT / "src"))
    os.environ["EPI_TSFM_MODE"] = "record"

    from epi_learning import tsfm

    if not tsfm.timesfm_available():
        parser.error("timesfm is not installed: run with  uv run --group timesfm python ...")
    if args.csv is not None:
        if not (args.column and args.cache_file and args.cache_key):
            parser.error("--csv needs --column, --cache-file and --cache-key")
        record_csv(
            args.csv, args.column, args.horizon, args.origins, args.cache_file, args.cache_key
        )
    for notebook in args.notebooks:
        record_notebook(notebook)
    if args.csv is None and not args.notebooks:
        parser.error("give at least one notebook or --csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
