# TimesFM 3.0 hands-on: report

Date: 2026-11-11. All numbers below are printed by code that actually ran.

## Files changed / added

New
- `src/epi_learning/tsfm.py`: helper (model path / cache path / record path)
- `scripts/make_timesfm_cache.py`: regenerates caches (notebook mode or CSV mode)
- `data/tsfm_cache/ch11_timesfm.json`: 208 KB, 15 cached requests from a real TimesFM 3.0 CPU run
- `tests/test_tsfm.py`: 13 tests, using a fake model; no network or weights needed
- `book/chapters/notebooks/11_dl_timesfm.ipynb` (zh), `book_en/chapters/notebooks/11_dl_timesfm.ipynb` (en), `notebooks/11_dl_timesfm.ipynb` (standalone; identical to zh, like the other lessons)

Modified
- `pyproject.toml`: new optional dependency group `timesfm = ["timesfm[torch]>=3.0.2", "huggingface-hub>=0.28,<2"]`; `uv.lock` updated
- `src/epi_learning/book_setup.py`: `configure_book_kernel()` now sets `os.environ.setdefault("EPI_TSFM_MODE", "cache")`, so the build always replays the cache, even where the group is installed. `tests/test_book_setup.py` asserts this.
- `book/chapters/11_deep_learning.md` and `book_en/...`:
  - learning goals, the Part A/B framing, decision-tree step 4 plus the figure alt text, the DL-fit table row
  - Part A is now 3 steps (Step 3 = TimesFM notebook)
  - Part B header and intro
  - model-zoo alt text
  - TSFM section fully rewritten (label `sec-tsfm`): 2026 landscape table, benchmark caveat, 3.0 API, multivariate/covariates, honest scorecard, when not to trust it, hardware, licence box
  - lines ~712 and ~723, plus two new "common misuse" rows
  - audit F9: DGL and pycox tool lines
- `book/chapters/07_time_series.md` and `book_en/...`:
  - Prophet reframed as the "classic" option, now in maintenance mode (method-map text, Step 11 intro)
  - new "延伸 / Going further: TSFM" subsection after Step 11 with the measured numbers on the Ch07 ILI series and a licence caveat
  - new bullet in the Step 12 decision list
- SVGs: `dl_decision_tree.svg`, `dl_decision_tree_en.svg` (box 4 reframed), `dl_model_zoo.svg`, `dl_model_zoo_en.svg` (TSFM "use when" line). Text edits only; XML validated.
- TOC: `book/myst.yml`, `book/_instructor/myst.yml`, `book_en/myst.yml`, `book_en/_instructor/myst.yml` (after `11_dl_sequence.ipynb`)
- `README.md`: notebook counts 21 → 22, `tsfm` in the helper list, new section "TimesFM 預測快取（選用）"
- Not touched: `scripts/build_book.py`, the workflows, CLAUDE.md, `book_ph/`, `data/synthetic/ph/`, `videos/`. `tests/test_book_toc.py` needed no change: its zh/en and instructor-parity checks pass with the new entry.

## Verified facts (primary sources)

- **README** (https://raw.githubusercontent.com/google-research/timesfm/master/README.md, fetched 2026-11-11, identical to the scratch copy):
  - TimesFM 3.0 released August 2026; API `from timesfm3 import TimesFM3Evaluator, ModelConfig`
  - native multivariate plus past-only and past-and-future covariates
  - claims #1 on fev-bench and TIME, and #1 among foundation models on GIFT-Eval
  - September 2026 note: 3.0 commercial and production use via BigQuery ML
  - "TimesFM in Google 1P products": BigQuery ML, Sheets, Vertex
  - licence notice: code Apache-2.0; weights ≤2.5 Apache-2.0; 3.0 weights under `timesfm-non-commercial-license-v1.0`, no commercial or production use
- **PyPI**: `timesfm` 3.0.2 (uploaded 2026-09-09), requires Python ≥3.10, deps numpy, huggingface_hub, safetensors, plus torch for the `[torch]` extra.
- **Installed package (3.0.2), inspected**:
  - `ModelConfig` defaults: `per_core_batch_size=4`, `device=None` (auto: cuda if available, else cpu; `"cpu"` works)
  - `TimesFM3Evaluator.predict_batch` defaults: `return_quantiles=True`, `use_symmetric_averaging=True`, `make_positive=True`; output `.forecast` (h,) and `.quantiles` (h, 9), deciles 0.1–0.9
  - max context 15,360; covariates `past_only_covariates` (n, T) and `past_future_covariates` (n, T+h)
  - the TimesFM 2.5 class in the same package is `timesfm.TimesFM_2p5_200M_torch`
- **HF model card / config** (https://huggingface.co/google/timesfm-3.0-pytorch):
  - not gated; revision `43046b85ec22d584a13f8098c2ed39c889e129c2`; `model.safetensors` 1,322,898,824 bytes
  - 20 layers, model dim 1280, 16 heads, patch 32 in / 64 out
  - pretraining: GiftEvalPretrain (minus fev-bench overlap), Wikipedia pageviews, Google Trends, synthetic data
  - I counted 330,710,976 parameters myself
- **LICENSE** (https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE), read in full:
  - "Non-Commercial Purpose" = testing, evaluation or research not tied to commercial gain, production deployment or revenue
  - explicitly excluded: "(b) in direct or indirect interactions with end users or production systems"
  - no distribution of the model or derivatives
  - Outputs are not Derivatives, but the restriction on commercial or production use extends to Outputs
  - The chapter states what a health agency may do (internal backtests, research, teaching) and may not do (routine surveillance or early warning, public releases or routine decisions, paid services, distillation, redistribution).
- **TimesFM 2.5 / 2.0 weights**: Apache-2.0 (HF API: `google/timesfm-2.5-200m-pytorch` cardData license apache-2.0, created 2025-09-02).
- **Landscape table** (HF API and repo READMEs):
  - Chronos-2: Apache-2.0, released 2025-10-20, 120M parameters; README claims best among pretrained models on fev-bench and GIFT-Eval (https://github.com/amazon-science/chronos-forecasting)
  - Moirai 2.0 R-small: CC-BY-NC-4.0, 2025-08 (uni2ts README, HF)
  - TimeGPT-2.1: Nixtla commercial API with key (Nixtla README)
  - GIFT-Eval (Salesforce) and fev-bench (AutoGluon `fev`) confirmed from their READMEs
  - Leaderboard positions are attributed as developer claims; I did not verify them independently.
  - Not included: TiRex, Toto, Sundial (exist, but I did not cross-check their claims).
- **Prophet**: the official README says "2026 Update: Prophet is in maintenance mode as of v1.4.0. Only bug fixes, dependency bumps…" (https://raw.githubusercontent.com/facebook/prophet/main/README.md). PyPI latest is 1.5.0 (2026-10-05); the repo locks 1.3.0.
- **F9 (PyPI JSON, 2026-11-11)**: dgl 2.2.1 (2024-05-13); pycox 0.3.0 (2024-09-04); torchtuples 0.2.2 (2021-08-31); torch-geometric 2.8.1 (2026-10-12).
- Not reachable here: research.google (the blog post). Claims rely on the README, the model card, the code and the licence only.

## Measured hardware and timings

Sandbox: 4-core CPU, no GPU, 15 GB RAM; timesfm 3.0.2, torch 2.10.0+cu128 (CPU), Python 3.14.

- Download: 1.3 GB, about 12 s here (Xet/CDN). I had to add `us.aws.cdn.hf.co` to this personal environment's allowed hosts (approved); `huggingface.co` alone is not enough.
- Load from disk: 4.5–5.1 s. Peak RSS about 3.1 GB (`ru_maxrss` 3073–3091 MB).
- Inference (uncontended, symmetric averaging on):

| Batch | Context length | Horizon | Time |
|---|---|---|---|
| 1 | 300 | 7 | 0.17 s |
| 8 | 300 | 7 | 0.46 s |
| 60 | 300 | 7 | 2.8 s |
| 60 rolling-origin contexts | ~300 | 7 | 3.8 s |

  - With a covariate: 6.8 s (past-only) and 8.5 s (past-future)
- The recorded cache run happened under heavy CPU contention from other agents' builds (load average 12–18), so its stored `seconds` are 100–250 s. The replay message no longer prints them.
- Book build: `11_dl_timesfm.ipynb` in cache mode took 63 s (en) and 150 s (zh) under the same contention. The SARIMA refits (14) and imports dominate; the cache replay itself is instant.

## Backtest numbers (from the notebook, identical in zh and en)

**Ch11 dengue × temperature series**: same DGP and seed as `11_dl_sequence.ipynb`; test target days 300–359; 7 days ahead; 60 rolling origins.

| Model | MAE | RMSE | MAPE % |
|---|---|---|---|
| Persistence (recomputed, matches Ch11) | 2.879 | 3.586 | 27.20 |
| TimesFM 3.0 zero-shot, whole history | 2.384 | 2.995 | 22.60 |
| LSTM (quoted from `11_dl_sequence.ipynb`, re-executed today) | 2.149 | 2.727 | 21.45 |
| 1D-CNN (same source) | 2.197 | 2.639 | 20.42 |

- TimesFM, whole history: 80% PI coverage 85%, WQL 1.883.
- Context length chosen on validation (targets 260–299):

| Context | Validation MAE |
|---|---|
| 28 | 2.364 |
| 56 | 2.022 |
| 112 | 4.499 |
| all | 2.145 |

  With 56 days, test MAE is **2.015**, which beats the LSTM.
- Covariate temperature: past-only MAE 2.395 (coverage 87%); past-and-future with a perfect forecast 2.463 (88%). **No gain.**
- First look, 60-day horizon from day 300: MAE 3.44, 80% PI coverage 95%.

**Ch07 ILI 90-day series** (identical to `synth_cases`), last 7 days:

| Model | MAE |
|---|---|
| TimesFM | 0.897 |
| Seasonal naive | 0.714 |
| ARIMA (Ch07) | 1.872 |
| SARIMA (Ch07) | 0.770 |
| Prophet (Ch07) | 0.774 |

Rolling origin, 14 origins × 7 days:

| Model | MAE |
|---|---|
| TimesFM | 0.948 (coverage 94%, too wide) |
| SARIMA refit at each origin | 0.804 |
| Seasonal naive | 1.265 |

**Legionella daily onsets** `[5,4,7,5,6,8,17,12,22,8,6,5,2,7,1,4,2]`:
- Origin day 5: forecast about 5.6/day vs actual 8, 17, 12, 22, 8; the 80% PI covers 20%.
- Origin day 9: forecast 15→12 vs actual 8, 6, 5, 2, 7.

**Reporting delay** (origin 330; last 7 days at 95→20% completeness): 7-day total 66.0 vs 103.5 with complete data (truth 89.6), so **26% too low**.

## Helper API (for the Philippines forecasting chapter)

```python
from epi_learning import tsfm
CACHE = tsfm.cache_path("ph_dengue")                 # data/tsfm_cache/ph_dengue.json
model = tsfm.load_model(CACHE)                       # TimesFM3Evaluator, or None (cache path); prints which
# or, to show the official calls in the notebook as 11_dl_timesfm does:
#   if tsfm.resolve_mode() == "cache": model = None
#   else: from timesfm3 import TimesFM3Evaluator, ModelConfig; model = TimesFM3Evaluator(ModelConfig(...))
y = df["cases"].to_numpy(float)                      # weekly series
origins = range(len(y) - 26 - 4 + 1, len(y) - 4 + 1) # last 26 origins, 4 weeks ahead
res = tsfm.forecast_batch(model, tsfm.rolling_origin_contexts(y, origins), 4,
                          cache_key="weekly_backtest", cache_file=CACHE,
                          past_only_covariates=None,       # list of (n_cov, T) per context
                          past_future_covariates=None)     # list of (n_cov, T+4) per context
res.forecast           # (n_series, 4)
res.quantile(0.1)      # (n_series, 4); also res.quantiles (n, 4, 9)
res.source             # "model" or "cache"
tsfm.coverage(actual, res.quantile(0.1), res.quantile(0.9))
tsfm.mean_weighted_quantile_loss(actual, res.quantiles)   # CRPS approximation
```

Modes: env `EPI_TSFM_MODE` = `auto` (default: model if `timesfm3` imports) | `model` | `cache` | `record`. The book build forces `cache` via `book_setup`.

Each cache entry stores a SHA-256 fingerprint of the inputs (rounded to 4 decimals), the horizon and the shape. On replay:
- a missing key raises `KeyError`
- changed inputs raise `ValueError`

Both messages name the regeneration command, so a strict build fails loudly instead of showing stale forecasts.

**To add a new cached series:**
1. Write the notebook with `tsfm.forecast_batch(...)` calls (unique `cache_key` per call within the file).
2. Run `uv run --group timesfm python scripts/make_timesfm_cache.py book_ph/<lang>/chapters/notebooks/<nb>.ipynb`. This runs the notebook's code cells in-process with `EPI_TSFM_MODE=record` and writes every call into its cache file.
3. Commit the JSON.

The en/zh/fil copies replay the same file as long as their data code is identical.

**Without a notebook:**

```bash
uv run --group timesfm python scripts/make_timesfm_cache.py \
    --csv data/synthetic/ph/santa_luz_dengue_weekly.csv --column <col> \
    --horizon 4 --origins 26 --cache-file ph_dengue --cache-key weekly_backtest
```

This uses origins `len-h-origins+1 … len-h` plus the end of the series. The notebook must build the same list with `rolling_origin_contexts(y, origins)` to replay it. Tested end to end with a temporary CSV.

Requirements: the first run downloads 1.3 GB, and the sandbox needs `huggingface.co` plus the CDN host `us.aws.cdn.hf.co`.

## uv / dependencies

- `uv lock`: adds timesfm 3.0.2, safetensors 0.8.0, huggingface-hub 1.33.0 and hf-xet 1.8.0 to the `timesfm` group only.
- I capped `huggingface-hub<2` in the group: hub 2.x pulls `httpx2`, which bumped `idna` 3.11→3.20 for the **default** install.
- With the cap, the `uv export --frozen` default + dev package set is identical to HEAD (176 packages), so the default `uv sync` is unchanged.
- `click` 8.3.1→8.5.1 changes only for the `video` group (manim).
- TimesFM verified working with hub 1.33.0 (load + forecast).

## Verification

- `uv run pytest`: all pass. Before the build: 403 tests plus mine; tsfm, book_setup, smoke, svg and toc re-run after the last edits.
- `uv run ruff check`: clean on every file I touched. The repo-wide check reports 8 pre-existing findings in files I did not touch (`generate_og_image.py`, `cleaning.py`, `viz.py`, `test_notebook_smoke.py` PH block). Ruff's rule set was widened by someone during this session.
- Notebooks executed in cache mode (zh + en) with nbclient: both pass. The en notebook replays the zh-recorded fingerprints.
- `uv run pytest`: 495 passed.
- Builds (strict, sequential, nothing else running):
  - `build_book.py --lang zh --edition student`: ✔ 55 pages, 36 notebooks, **0 warnings**, 349 s; post-build link check passed
  - `--lang en --edition student`: ✔ 55 pages, 36 notebooks, **0 warnings**, 385 s
  - `11_dl_timesfm.ipynb` takes 3.2–3.4 min inside the build, because MyST runs all notebooks concurrently on 4 cores. Run alone in cache mode it takes about 4 s total (SARIMA refits 3.0 s; every replay under 0.1 s).
- **Sandbox build blockers I hit (not repo problems)**:
  1. Someone wiped `book/_build` and `book_en/_build`, including the theme cache, and the session's GitHub proxy returns 403 for `github.com/.../archive/<sha>.zip` ("GitHub access to this repository is not enabled"). Git reads of public repos do work, so I git-fetched `myst-templates/book-theme` at the pinned sha `23f2df5…` and extracted it into `book{,_en}/_build/templates/site/3a97af73…/` (sha256 of the template URL). That is the same content as the zip. Other projects' caches (instructor, PH) are still empty; populate them the same way, or allow archive downloads.
  2. `jupyter_server` refuses to start as root ("Use --allow-root"), so every executed notebook fails with "Could not load Jupyter session manager". I built with `JUPYTER_CONFIG_DIR=<scratchpad>/jupyter_cfg` holding `{"ServerApp": {"allow_root": true}}`. I changed no global or repo config; CI runs as non-root and is unaffected.

## Unfinished / for the director

- The cached `seconds` are contention-inflated, but they are no longer displayed. Re-record on an idle machine if you want clean metadata: `uv run --group timesfm python scripts/make_timesfm_cache.py book/chapters/notebooks/11_dl_timesfm.ipynb`. The forecasts would be identical.
- CLAUDE.md is not updated (another agent owns it). A one-line note may be worth adding there: "TimesFM notebooks replay `data/tsfm_cache/` (`EPI_TSFM_MODE`, `scripts/make_timesfm_cache.py`)".
- Licence judgment call: committing TimesFM 3.0 Outputs to a public, non-commercial teaching repo. The licence restricts Outputs only for commercial or production purposes, and Outputs are not Derivatives. The cache file carries a licence note. Worth a legal sanity check if the book is ever used commercially.
- `07_time_series_baseline.ipynb`, the Ch07 exercise Q9 and the method-map SVGs still present Prophet without the maintenance note. I kept the Ch07 changes to the markdown, as instructed.
