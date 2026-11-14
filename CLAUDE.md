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
- **Node.js 24+** is required by Jupyter Book 2 (the MyST engine) to build the site.

## Essential Commands

All commands use `uv run` to execute within the managed virtual environment.

```bash
# Build the book (Jupyter Book 2) — always through the entry point, never bare
# `jupyter book build`: it installs the kernel pre-execution setup, builds with
# --execute --strict, and runs the post-build step
uv run python scripts/build_book.py --lang zh --edition student      # 中文 學生版
uv run python scripts/build_book.py --lang zh --edition instructor   # 中文 教師版 (solutions)
uv run python scripts/build_book.py --lang en --edition student      # English student
uv run python scripts/build_book.py --lang en --edition instructor   # English instructor
uv run python scripts/build_book.py --all --site-dir _site           # all four, as deployed

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
- The site is built with **Jupyter Book 2** (MyST). Each edition is a MyST project: `book/myst.yml` (zh student: all site config + TOC), `book/_instructor/myst.yml` (`extends: ../myst.yml`, replaces only `project.toc` to add Ch17 solutions), and the same pair under `book_en/`. MyST resolves files relative to the directory holding `myst.yml`, so each `_instructor/` holds symlinks (`chapters`, `intro.md`, `_static`, `_site`) back to the shared content — URLs are identical across editions
- `scripts/build_book.py` is the single build entry point (local, `ci.yml`, `pages.yml`). It runs `jupyter book build --html --execute --strict` per edition: every notebook is executed (cached in `<project>/_build/execute` between local builds), and a cell that raises — or any other ⛔ build error — fails the build. MyST has no per-notebook timeout setting, so notebooks must stay fast
- **Pre-execution setup** (JB1's `nb_execution_pre_code`) lives in `src/epi_learning/book_setup.py` (`configure_book_kernel()`): chdir to the repo root so `data/synthetic/...` resolves, CJK fonts, `ggplot` style at 150 dpi, Plotly `notebook` renderer. The build script writes an IPython startup file that calls it and points the kernels' `IPYTHONDIR` at it; notebooks are never modified for the build
- **Post-build step** (`postprocess()` in `scripts/build_book.py`, covered by `tests/test_build_book.py`) does what MyST cannot be configured to do: sets `<html lang>`, absolute OG/Twitter tags + `hreflang` alternates, injects `book/_static/epi-site.js` (language switcher + "Open in Colab") and `youtube-lite.js`, fixes instructor GitHub source links (`book/_instructor/` → `book/`), writes redirect stubs for the old JB1 URLs (`chapters/01_fundamentals.html` → `chapters/fundamentals/`), and refuses to finish if a student edition contains solution files
- URLs follow MyST's scheme with `folders: true`: leading numbers are dropped and `_` becomes `-` (`chapters/notebooks/03_stats_basics.ipynb` → `/chapters/notebooks/stats-basics/`). Link to other pages by file path (`[](05_stratified.md)`), never by a hand-written URL
- **Post-build link check**: the post-build step fails the build if any same-site `href` on a built page does not resolve to a file in that edition's output (and, with `--all`, across the assembled site). Never weaken it to get green; fix the link (or the theme pin)
- **Build-time messages**: `error_rules` in both `myst.yml` files silences `identifier-is-unique` (one warning per notebook cell id reused across notebooks). That rule also covers duplicate labels *within* one file, so give new labels unique names. zh projects set `numbering.figure.enabled: false`: MyST hard-codes an English "Figure N:" caption prefix that `numbering.figure.template` does not change, so zh captions carry no number (no zh page cross-references a figure by number; if one ever needs to, this has to be revisited)
- Content syntax is MyST (not Sphinx): no `{raw} html` (use a plain HTML block; only `class`/`id`/`style`/`href` survive), no sphinx-design options (`:gutter:`, `:text-align:`, `{button-ref}`) — use `{card}`, `{grid}`, the `{button}` role and `{div}` + `:class:` styled in `book/_static/site.css`
- Never link a solution notebook by relative path from a chapter: MyST copies linked local files into the build, which would ship it in the student edition. Link to the instructor edition URL instead
- The `uv.lock` file is committed to ensure reproducible dependency resolution
- Every notebook has a Colab setup cell at the top that detects `google.colab` and auto-clones the repo, puts `/content/python4epi/src` on `sys.path` (an editable install only becomes importable after a runtime restart, so without it `from epi_learning import ...` fails on the first run) + installs deps; this cell is a no-op when running locally
- When creating new notebooks, always include the standard Colab setup cell after the title markdown cell
- All chapters share a single dataset (`legionella_outbreak.csv`) for narrative continuity; standalone copies of all notebooks are kept in sync under `notebooks/`

## Bilingual Editions (繁中 / English)

The main book is built in two languages, deployed to four URLs by `.github/workflows/pages.yml` (which also deploys the three Philippines-edition URLs, see below):

| Edition | Source | Deploy path |
|---------|--------|-------------|
| 中文 學生版 | `book/myst.yml` | `/` |
| 中文 教師版 | `book/_instructor/myst.yml` | `/instructor/` |
| English student | `book_en/myst.yml` | `/en/` |
| English instructor | `book_en/_instructor/myst.yml` | `/en/instructor/` |

- **`book_en/` mirrors `book/` exactly** (same relative file structure) so the language switcher only has to toggle the `/en/` path prefix. It **shares** `_static` and `chapters/images` with `book/` via symlinks — do not duplicate CSS/JS/images; edit them once under `book/`. Only `book_en/_site/` (the navbar/footer parts) is language-specific.
- **`book_en/` content is English**: chapter prose, notebook markdown cells, code comments, and user-facing display strings (`print`, plot labels, DataFrame display labels) are translated; Python code, identifiers, dataset column names, and the Colab setup cell stay identical to `book/`. The `book/` (zh) tree is the source of truth for structure — when adding/renaming a chapter, mirror it in `book_en/` and in the TOCs of all four `myst.yml` files.
- **Language switcher**: `_site/navbar_end.md` (the theme's `navbar_end` part) renders a plain `a.epi-lang-switch` link to the other tree's home page (the no-JS fallback). `book/_static/epi-site.js` retargets it to the same page in the other language and the same edition (student↔student, instructor↔instructor), checks the target with a HEAD request on click and falls back to the other tree's home if it 404s. It re-applies after client-side navigation and only touches the DOM after React has hydrated the page (earlier changes cause React error #418 and a full client re-render): `window.epiWhenHydrated()` waits for React's first commit via `__REACT_DEVTOOLS_GLOBAL_HOOK__`; `youtube-lite.js` uses it too, so `epi-site.js` must be injected first. The same script adds the "Open in Colab" link on notebook pages from a page→notebook map the build writes.
- **Per-build language flag**: the language is a property of the edition in `scripts/build_book.py` (`Edition.lang`, copy and locales in `LANG_META`), not of `myst.yml` — the MyST theme hard-codes `<html lang="en">` and has no language option. The post-build step writes `lang="zh-Hant"`/`"en"`, the OG/Twitter locale + copy and the `hreflang` alternates per page, and passes the language to `epi-site.js` via `window.EPI_SITE`.
- The five-act narrative is encoded as title-only `project.toc` entries with `children` in every `myst.yml` (titles translated per language).

### Theme pin

The site theme is pinned to one commit of `myst-templates/book-theme` in **both** `book/myst.yml` and `book_en/myst.yml` (instructor editions inherit it):

```yaml
site:
  template: https://github.com/myst-templates/book-theme/archive/<40-char sha>.zip
```

The plain name `book-theme` would download the theme repo's `main` at build time, so any theme release could change the DOM that `book/_static/site.css` and `epi-site.js` target. The current pin is v1.4.1 (`23f2df5…`), the line whose layout and `template.yml` match the myst 1.11 engine bundled with jupyter-book 2.1.x; v2.0.0 doubled `BASE_URL` in breadcrumb links and its `template.yml` does not validate against myst 1.11. To bump it:

1. Pick a release commit from https://github.com/myst-templates/book-theme/commits/main (a `🚀 vX.Y.Z` commit) that targets the bundled myst version; replace the sha in both `myst.yml` files (`tests/test_book_toc.py` checks they match and are full shas).
2. Build all four editions (`scripts/build_book.py --all --site-dir _site`): the post-build link check must pass and the log must have no new warnings.
3. Check in a browser, light/dark, desktop and 390px phone: header (language switch, logo), page header (Colab link), home cards, code blocks, admonitions, tables, video cards, and that pages load without React errors in the console. Adjust `site.css` / `epi-site.js` selectors (`.myst-navbar-end`, `.myst-fm-block-header`, `.myst-card`, `.myst-code`, `--myst-color-*`) if the DOM changed.

MyST caches a URL template under `<project>/_build/templates/site/<sha256 of the URL>/`; delete `_build/templates` to force a fresh download.

## Philippines Edition (`book_ph/`)

A condensed sister book (*Bantay Python*) for Philippine surveillance staff; content,
story, TOC and design rules live in **`book_ph/PRODUCTION.md`** (read it first). Build
infrastructure:

| Edition | Source | Deploy path | `<html lang>` |
|---------|--------|-------------|---------------|
| PH English (source of truth) | `book_ph/en/myst.yml` | `/ph/` | `en` |
| PH 中文 | `book_ph/zh/myst.yml` | `/ph/zh/` | `zh-Hant` |
| PH Filipino | `book_ph/fil/myst.yml` | `/ph/fil/` | `fil` |

```bash
uv run python scripts/build_book.py --series ph --lang en     # or zh, fil
uv run python scripts/build_book.py --series ph --all         # the three (what ci.yml runs)
uv run python scripts/build_book.py --all --site-dir _site    # all seven, as deployed
```

- **Structure.** Each project has `myst.yml`, `intro.md`, `chapters/NN_stem.md`,
  `chapters/notebooks/NN_stem.ipynb`, `_site/navbar_end.md` + `_site/footer.md`. The three
  trees mirror each other file-for-file and their TOCs match (`tests/test_book_toc.py`); act
  groups are title-only TOC parents. No instructor edition, no JB1 redirect stubs. Same theme
  pin and `error_rules` as `book/`; zh and fil set `numbering.figure.enabled: false`.
- **Shared assets, once.** `book_ph/_static/` (CSS, JS, logos) and `book_ph/images/`
  (illustrations) are reached through symlinks `book_ph/<lang>/_static -> ../_static` and
  `book_ph/<lang>/chapters/images -> ../../images`; in a chapter write `![alt](images/x.svg)`.
- **Styles and scripts.** MyST `style: _static/ph.css`. The post-build step links
  `_static/ph-games.css` and injects, in order: `window.EPI_SITE={...}`, `epi-site.js` (copied
  from `book/_static`; on PH pages it only provides `window.epiWhenHydrated`), `ph-site.js`
  (three-way language switch `a.ph-lang.ph-lang-<code>` to the same page with a HEAD-check
  fallback to that language's home, `a.ph-book-link` back to the full book — `/` for zh, `/en/`
  otherwise — "Open in Colab" on notebook pages, full page loads for standalone pages), then
  `ph-games.js`. No `youtube-lite.js`. **Contract for `ph-games.js`:** `window.epiWhenHydrated(cb)`
  exists and `window.EPI_SITE.lang` is `"en" | "zh" | "fil"`. `ph-games.css`/`ph-games.js`
  are optional (skipped with a ⚠ warning while missing); `ph-site.js` is required; a missing
  `ph.css` only makes MyST log ⛔ and build unstyled.
- **Social cards.** `og-image.png` is the first of `book_ph/_static/og-image_<lang>.png`,
  `book_ph/_static/og-image.png`, `book/_static/og-image.png` (PNG only).
- **Chapter-9 dashboard.** `scripts/build_ph_dashboard.py` exposes
  `build_dashboard(lang: str, out_dir: Path) -> Path`; the post-build step calls it for each
  PH language with `out_dir=<edition>/_build/html/dashboard`, so it is served at
  `<edition root>/dashboard/` and the link check sees it. Link it from a chapter with a
  **root-relative** MyST link — `[Open the dashboard](/dashboard/)` — which MyST prefixes with
  the edition's `BASE_URL` (`/python4epi/ph/fil/dashboard/`); relative `../` paths do not
  survive MyST. `ph-site.js` turns clicks on it into a full page load (the theme's router
  cannot open a non-MyST page).
- **Links between books.** The main book links the PH edition from `intro.md` (absolute
  production URLs, like the instructor-edition button). With `--all`, the assembled-site link
  check also resolves absolute `https://ancientsky.github.io/python4epi/...` links
  (canonical/`hreflang`, navbar fallbacks, cross-edition buttons) against the assembled site.

## Time-series foundation model notebooks (TimesFM)

- `11_dl_timesfm.ipynb` (main book) and `book_ph/*/chapters/notebooks/07_forecast_timesfm.ipynb` show the real `timesfm3` calls, but the book build never downloads the ~1.3 GB weights: `src/epi_learning/tsfm.py` replays forecasts recorded from a real run in `data/tsfm_cache/*.json` (the build forces cache mode). Colab readers run the real model.
- `timesfm` is an optional dependency group (`uv sync --group timesfm`), not a default dependency. After changing a notebook's forecasting inputs (series, horizon, context, covariates), regenerate its cache with `scripts/make_timesfm_cache.py` (needs the group and access to huggingface.co) and commit the JSON; a stale cache makes the notebook fail rather than replay the wrong numbers.
- TimesFM 3.0 **weights** are under a non-commercial, non-production licence (code is Apache-2.0; 2.5 weights are Apache-2.0). Keep the licence box in any chapter that uses them, and re-check versions/licences before editing the landscape table in chapter 11.

## Tutorial Video & SVG Diagram Production

Visual style, colour palette, SVG conventions, the Manim + TTS + FFMPEG pipeline, YAML
script format, and Manim API compatibility notes (v0.20+) now live in the `video-production`
skill (`.claude/skills/video-production/SKILL.md`) — it loads automatically when you work
on videos or diagrams.

## CJK Font & Visualization Known Issues

### matplotlib `.ttc` face 0 trap
- `fontManager.addfont()` only registers **face 0** of `.ttc` (TrueType Collection) files
- For `NotoSansCJK-Regular.ttc`, face 0 = "Noto Sans CJK JP" (not TC)
- **Fix:** include ALL Noto Sans CJK variants (JP, SC, TC, KR, HK) in `font.sans-serif` candidate list
- The centralized font config lives in `src/epi_learning/viz.py` (`configure_chinese_font()`) and is applied to every notebook kernel of the book build by `src/epi_learning/book_setup.py`; it dynamically discovers registered CJK font names
- Inline font config in notebooks/chapters uses a static candidate list with all variants
- When modifying the font candidate list across notebooks, beware of two source formats:
  - **Array-style**: `"source": ["line1\n", "line2\n"]` — each line is a separate JSON array element
  - **Single-string**: `"source": "line1\nline2\n"` — entire cell is one JSON string with `\n` newlines
  - A `json.dump` rewrite changes formatting; prefer targeted `str.replace` within the parsed JSON to minimize diff noise

### Plotly blank charts in Jupyter Book
- Plotly's default renderer (`plotly_mimetype`) doesn't produce output in headless Jupyter Book builds
- **Fix:** set `pio.renderers.default = "notebook"` (self-contained HTML output that MyST displays) — configured globally for the build in `src/epi_learning/book_setup.py`

### CI font setup
- `.github/workflows/ci.yml` installs `fonts-noto-cjk` and clears `~/.cache/matplotlib`
- Font installation MUST happen before `uv sync` and before any matplotlib import to ensure the font cache is built correctly
