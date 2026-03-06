# CLAUDE.md

This file provides guidance for AI assistants working with the **Epi With Python** repository.

## Project Overview

An educational Jupyter Book site teaching infectious disease epidemiology with Python, from fundamentals through ML/DL. All 18 chapters share a single unifying story: **a Legionella outbreak investigation at a nursing home** (280 residents, 121 infected, 19 deaths). Content is written primarily in Traditional Chinese (繁體中文) with English technical terms. The project emphasizes beginner-friendly, copy-paste runnable code.

## Repository Layout

```
book/                          # Jupyter Book source
  _config.yml                  # Book configuration (language: zh, execute: force)
  _toc.yml                     # Active table of contents (swapped for student/instructor)
  _toc_student.yml             # Student TOC (no solutions)
  _toc_instructor.yml          # Instructor TOC (includes solutions)
  intro.md                     # Landing page
  chapters/                    # 18 markdown chapter files (00–17)
  chapters/notebooks/          # Embedded lesson notebooks (executed during build)
  chapters/exercises/          # Exercise notebooks (14 chapters)
  chapters/solutions/          # Solution notebooks (14 chapters, instructor only)
notebooks/                     # Standalone runnable lesson notebooks
  exercises/                   # Exercise + solution notebooks (mirrors book/chapters/)
  run_sitrep.py                # Example SitRep script
src/epi_learning/              # Reusable Python helper package
  __init__.py                  # Exports: attack_rate, case_fatality_rate, risk_ratio,
                               #   standardize_line_list, summarize_by_group
  metrics.py                   # Epi metrics (attack_rate, case_fatality_rate, risk_ratio)
  cleaning.py                  # Line-list data cleaning (standardize_line_list)
  tabulate.py                  # Group summary tabulation (summarize_by_group)
  viz.py                       # Visualization helpers (plot_epi_curve)
data/synthetic/                # Teaching datasets
  legionella_outbreak.csv      # Primary dataset: 280 residents × 32 columns
  line_list.csv                # Legacy sample line-list (used by choropleth demo)
  admin_areas.geojson          # Administrative boundaries for choropleth lessons
  location_population.csv      # Population data by location (choropleth demo)
tests/                         # pytest test suite
  test_metrics.py              # Unit tests for epi metrics
  test_cleaning.py             # Unit tests for data cleaning
  test_tabulate.py             # Unit tests for summarization
  test_notebook_smoke.py       # Smoke tests validating notebook JSON structure
.github/workflows/
  ci.yml                       # PR/push: pytest + jupyter-book build
  pages.yml                    # Deploy to GitHub Pages on push to main
```

## Chapter Structure (18 chapters)

```
【第一幕：接獲通報】
  Ch00  導讀與工具
  Ch01  Python 基礎
  Ch02  資料處理與視覺化

【第二幕：描述性分析】
  Ch03  描述性統計與 2×2 表
  Ch04  群聚調查工作流

【第三幕：深入分析】
  Ch05  分層分析與交絡因子 [新增]
  Ch06  邏輯斯迴歸 [新增]
  Ch07  時間序列與預測
  Ch08  空間流病

【第四幕：進階建模】
  Ch09  存活分析 [新增]
  Ch10  機器學習
  Ch11  深度學習
  Ch12  因果推論

【第五幕：收尾與實戰】
  Ch13  可重現研究
  Ch14  實戰案例
  Ch15  附錄
  Ch16  作業區（14 組練習）
  Ch17  解答區（14 組解答，講師版）
```

## Primary Dataset

**`data/synthetic/legionella_outbreak.csv`** — 280 rows × 32 columns

A synthetic dataset simulating a Legionella outbreak at a nursing home (松柏護理之家).

Key columns:
- Demographics: `case_id`, `age`, `sex`, `floor`, `wing`, `room`
- Comorbidities: `comorbidity_chf`, `comorbidity_dm`, `comorbidity_cancer`, `comorbidity_copd`, `immunosuppressed`
- Exposures: `shower_use`, `hydrotherapy_use`, `smoking_history`, `functional_status`
- Clinical: `clinical_severity` (not_ill/asymptomatic/mild/moderate/severe), `outcome` (survived/dead)
- Dates: `symptom_onset_date`, `hospitalization_date`, `death_date`, `notification_date`
- Classification: `lab_confirmed`, `case_classification`, `hospitalized`, `icu_admission`

Key facts: 121 infected (43.2%), 19 deaths (CFR 15.7%), onset range 2026-01-12 to 2026-01-28.

## Tech Stack

- **Python 3.12** (pinned in `.python-version` and `pyproject.toml`)
- **uv** as the sole package manager (no pip, conda, or poetry); notebooks also run on **Google Colab**
- **Node.js 20+** required by Jupyter Book for building the site
- **Jupyter Book** for static site generation from markdown and notebooks
- **pytest** for testing, **ruff** for linting, **mypy** for type checking

## Essential Commands

All commands use `uv run` to execute within the managed virtual environment.

```bash
# Setup
uv sync                              # Install/lock all dependencies into .venv

# Tests (minimum bar for PRs)
uv run pytest                        # Run unit + smoke tests
uv run pytest -v                     # Verbose output
uv run pytest --cov                  # With coverage report

# Linting and type checking
uv run ruff check .                  # Lint check
uv run ruff format --check .         # Format check
uv run mypy src/                     # Type check the package

# Notebooks
uv run jupyter lab                   # Start interactive notebook server

# Build the book
cp book/_toc_student.yml book/_toc.yml
uv run jupyter-book build book/      # Student edition

cp book/_toc_instructor.yml book/_toc.yml
uv run jupyter-book build book/      # Instructor edition (includes solutions)

# Run example script
uv run python notebooks/run_sitrep.py
```

## CI Pipeline

The CI workflow (`.github/workflows/ci.yml`) runs on every PR and push to `main`:
1. Installs uv, Node.js 20, Python 3.12
2. Runs `uv sync --all-groups`
3. Runs `uv run pytest`
4. Builds the Jupyter Book

A separate Pages workflow deploys the built book to GitHub Pages on push to `main`.

## Coding Conventions

### Python style
- 4-space indentation, line length 100 characters (ruff)
- Target version: Python 3.12
- Use `from __future__ import annotations` at the top of all source files
- Full type annotations on function signatures
- Small, focused functions with clear variable names
- Explicit input validation with descriptive `ValueError` messages

### Docstrings
- NumPy-style docstrings with `Parameters` and `Returns` sections
- Module-level docstrings on all files

### Imports
- `from __future__ import annotations` first
- Standard library, then third-party, then local/relative imports
- No star imports

### File naming
- Lesson notebooks: `NN_topic_name.ipynb` (e.g., `08_spatial_rates.ipynb`)
- Exercise pairs: `NN_topic_exercise.ipynb` / `NN_topic_solution.ipynb`
- Python modules: lowercase with underscores

### Content language
- Prose and explanations: Traditional Chinese (繁體中文)
- Technical terms, variable names, code: English

### Epidemiological terminology (台灣繁體中文譯名)

All Chinese epidemiological terms must follow **Taiwan (ROC) standard usage**. Key terms:

| English | 台灣譯名（使用這個） | ❌ 避免使用 |
|---------|----------------------|-------------|
| Attack rate | 侵襲率 | 攻擊率 |
| Case fatality rate (CFR) | 致死率 | 病死率 |
| Risk ratio (RR) | 風險比 | 危險比 |
| Odds ratio (OR) | 勝算比 | 比值比 |
| Confidence interval (CI) | 信賴區間 | 置信區間 |
| Incidence rate | 發生率 | 發病率（可用於非正式語境） |
| Prevalence | 盛行率 | 流行率、患病率 |
| Epidemic curve | 流行曲線 | — |
| Outbreak / cluster | 群聚 | 聚集性疫情 |
| Surveillance | 監測 | 監控 |
| Case notification | 通報 | 報告（用於疫情通報語境時） |
| Epidemiological investigation | 疫調（口語）/ 流行病學調查 | 流調 |
| Basic reproduction number | 基本再生數 | 基本傳染數 |
| Sensitivity (test) | 敏感度 | 靈敏度 |
| Specificity | 特異度 | 特異性 |
| Chi-square test | 卡方檢定 | 卡方检验 |
| Exposure | 暴露 | — |
| Confounding | 交絡 | 混淆 |
| Stratified analysis | 分層分析 | — |
| Hazard ratio (HR) | 風險比 | 危險比 |
| Kaplan-Meier | Kaplan-Meier 估計式 | — |

**Note:** Python variable names and function names remain in English (e.g., `attack_rate`, `case_fatality_rate`)—only Chinese prose uses the translated terms above.

## Testing Guidelines

- Test files: `tests/test_*.py`
- Keep tests deterministic and fast
- Use `math.isclose()` for floating-point assertions
- Use `pytest.raises` for expected exceptions
- When adding notebooks under `notebooks/`, update smoke tests accordingly
- All tests must pass before merging: `uv run pytest`

## Commit Conventions

Use Conventional Commits:
- `feat: add choropleth lesson notebook`
- `fix: correct epi week conversion in chapter 02`
- `docs: update README quick start section`
- `test: add edge case tests for risk_ratio`

PR descriptions should include scope summary, validation output, and screenshots for visualization changes.

## Security Rules

- Never commit real patient data; use only synthetic or properly anonymized datasets
- Keep secrets out of notebooks and markdown
- For map lessons, verify ID matching between data and GeoJSON before publishing

## Key Architecture Decisions

- The `epi_learning` package under `src/` is installed in editable mode via `uv sync` and imported as `from epi_learning import ...` in both notebooks and tests
- The book uses `execute_notebooks: force` — all embedded notebooks are re-executed during every build, so they must remain runnable and fast (300s timeout per notebook)
- Two TOC variants exist for student vs. instructor editions; `_toc.yml` is the active file that gets overwritten before builds
- The `uv.lock` file is committed to ensure reproducible dependency resolution
- Every notebook has a Colab setup cell at the top that detects `google.colab` and auto-clones the repo + installs deps; this cell is a no-op when running locally
- When creating new notebooks, always include the standard Colab setup cell after the title markdown cell
- All chapters share a single dataset (`legionella_outbreak.csv`) for narrative continuity; standalone copies of all notebooks are kept in sync under `notebooks/`

## CJK Font & Visualization Known Issues

### matplotlib `.ttc` face 0 trap
- `fontManager.addfont()` only registers **face 0** of `.ttc` (TrueType Collection) files
- For `NotoSansCJK-Regular.ttc`, face 0 = "Noto Sans CJK JP" (not TC)
- **Fix:** include ALL Noto Sans CJK variants (JP, SC, TC, KR, HK) in `font.sans-serif` candidate list
- The centralized font config lives in `src/epi_learning/viz.py` (`configure_chinese_font()`) and `book/_config.yml` (`nb_execution_pre_code`); both dynamically discover registered CJK font names
- Inline font config in notebooks/chapters uses a static candidate list with all variants
- When modifying the font candidate list across notebooks, beware of two source formats:
  - **Array-style**: `"source": ["line1\n", "line2\n"]` — each line is a separate JSON array element
  - **Single-string**: `"source": "line1\nline2\n"` — entire cell is one JSON string with `\n` newlines
  - A `json.dump` rewrite changes formatting; prefer targeted `str.replace` within the parsed JSON to minimize diff noise

### Plotly blank charts in Jupyter Book
- Plotly's default renderer (`plotly_mimetype`) doesn't produce output in headless Jupyter Book builds
- **Fix:** set `pio.renderers.default = "notebook"` — this is configured globally in `book/_config.yml` `nb_execution_pre_code`

### CI font setup
- `.github/workflows/ci.yml` installs `fonts-noto-cjk` and clears `~/.cache/matplotlib`
- Font installation MUST happen before `uv sync` and before any matplotlib import to ensure the font cache is built correctly
