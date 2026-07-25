# CLAUDE.md

This file provides guidance for AI assistants working with the **Epi With Python** repository.

## Project Overview

An educational Jupyter Book site teaching infectious disease epidemiology with Python, from fundamentals through ML/DL. All 18 chapters share a single unifying story: **a Legionella outbreak investigation at a nursing home** (280 residents, 121 infected, 19 deaths). Content is written primarily in Traditional Chinese (繁體中文) with English technical terms. The project emphasizes beginner-friendly, copy-paste runnable code.

## Primary Dataset

**`data/synthetic/legionella_outbreak.csv`** — 280 rows × 32 columns

A synthetic dataset simulating a Legionella outbreak at a nursing home (松柏護理之家).

Key facts: 121 infected (43.2%), 19 deaths (CFR 15.7%), onset range 2026-01-12 to 2026-01-28.

## Tech Stack

See `pyproject.toml` / `.python-version` for versions and dependencies. Constraints
that the manifest does *not* state:

- **uv** is the sole package manager — never pip, conda, or poetry. Notebooks must also
  run on **Google Colab**.
- **Node.js 24+** is required by Jupyter Book to build the site.

## Essential Commands

All commands use `uv run` to execute within the managed virtual environment.

```bash
# Build the book — the TOC file is swapped before each edition build
cp book/_toc_student.yml book/_toc.yml
uv run jupyter-book build book/      # Student edition

cp book/_toc_instructor.yml book/_toc.yml
uv run jupyter-book build book/      # Instructor edition (includes solutions)

# Run example script
uv run python notebooks/run_sitrep.py
```

## Coding Conventions

### Python style
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
| Confounding | 干擾作用 | 交絡（統計學語境）、混淆 |
| Confounder / Confounding variable | 干擾因子 / 干擾因素 | 交絡因子、混淆變項 |
| Adjust for confounding | 校正干擾 / 調整干擾因子 | 控制交絡 |
| Stratified analysis | 分層分析 | — |
| Hazard ratio (HR) | 風險比（存活分析語境） | 危險比 |
| Kaplan-Meier | Kaplan-Meier 估計式 | — |
| Outbreak（超過預期的群聚） | 群突發 | — |
| Sporadic case | 散發病例 | — |
| Epidemic | 流行 | — |
| Pandemic | 大流行 | — |
| Incubation period | 潛伏期 | — |
| Latent period | 潛藏期 | 潛伏期（兩者不同，潛藏期 = 從暴露到具傳染性） |
| Infectious period | 可傳染期 | — |
| Serial interval / Generation interval | 世代間隔 / 發病世代間隔 | — |
| Reservoir | 傳染窩 | 宿主（宿主另有其義） |
| Chain of infection | 傳染鏈 | — |
| Susceptible host | 易感宿主 | — |
| Vector-borne transmission | 媒介傳播 | — |
| Vehicle-borne transmission | 媒介物傳播 | — |
| Traceback (epidemiological) | 向後回溯 | — |
| Trace-forward | 向前追溯 | — |
| Isolation | 隔離 | — |
| Quarantine | 檢疫 | — |
| Post-exposure prophylaxis (PEP) | 暴露後預防 | — |
| Infection control | 感染管制 | 感染控制 |
| Confirmed case | 確診病例 | — |
| Probable case | 可能病例 | — |
| Suspect case | 疑似病例 | — |
| Line list | 造冊 / line list | — |

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

## Bilingual Editions (繁中 / English)

The site is built in two languages, deployed to four URLs by `.github/workflows/pages.yml`:

| Edition | Source | Deploy path |
|---------|--------|-------------|
| 中文 學生版 | `book/` + `_toc_student.yml` | `/` |
| 中文 教師版 | `book/` + `_toc_instructor.yml` | `/instructor/` |
| English student | `book_en/` + `_toc_student.yml` | `/en/` |
| English instructor | `book_en/` + `_toc_instructor.yml` | `/en/instructor/` |

- **`book_en/` mirrors `book/` exactly** (same relative file structure) so the language switcher only has to toggle the `/en/` path prefix. It **shares** `_static`, `_templates`, and `chapters/images` with `book/` via symlinks — do not duplicate CSS/JS/templates/images; edit them once under `book/`.
- **`book_en/` content is English**: chapter prose, notebook markdown cells, code comments, and user-facing display strings (`print`, plot labels, DataFrame display labels) are translated; Python code, identifiers, dataset column names, and the Colab setup cell stay identical to `book/`. The `book/` (zh) tree is the source of truth for structure — when adding/renaming a chapter, mirror it in `book_en/` and both TOC sets.
- **Language switcher**: `book/_static/lang-switch.js` derives the deploy base from its own script URL and toggles `/en/`, mapping each page to its counterpart (falls back to the other tree's home page if the counterpart 404s). `book/_templates/lang-switch.html` renders the header button, registered via `html_theme_options.article_header_end` in both `_config.yml` files.
- **Per-build language flag**: each `_config.yml` sets `sphinx.config.html_context.epi_lang` (`zh` / `en`) and `sphinx.config.language` (`zh_Hant` / `en`). `book/_templates/layout.html` branches on `epi_lang` for OG/Twitter locale + copy and emits `hreflang` alternates. (jupyter-book does not reliably propagate the top-level `language:` key, hence setting it under `sphinx.config` too.)
- The five-act narrative is encoded as MyST `parts:` in every TOC (captions translated per language).

## Tutorial Video & SVG Diagram Production

Visual style, colour palette, SVG conventions, the Manim + TTS + FFMPEG pipeline, YAML
script format, and Manim v0.20.1 breaking changes now live in the `video-production`
skill (`.claude/skills/video-production/SKILL.md`) — it loads automatically when you work
on videos or diagrams.

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
