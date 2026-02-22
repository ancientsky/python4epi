# CLAUDE.md

This file provides guidance for AI assistants working with the **Epi With Python** repository.

## Project Overview

An educational Jupyter Book site teaching infectious disease epidemiology with Python, from fundamentals through ML/DL. Content is written primarily in Traditional Chinese (繁體中文) with English technical terms. The project emphasizes beginner-friendly, copy-paste runnable code.

## Repository Layout

```
book/                          # Jupyter Book source
  _config.yml                  # Book configuration (language: zh, execute: force)
  _toc.yml                     # Active table of contents (swapped for student/instructor)
  _toc_student.yml             # Student TOC (no solutions)
  _toc_instructor.yml          # Instructor TOC (includes solutions)
  intro.md                     # Landing page
  chapters/                    # 15 markdown chapter files (00–14)
  chapters/notebooks/          # Embedded lesson notebooks (executed during build)
  chapters/exercises/          # Exercise/solution notebook pairs
notebooks/                     # Standalone runnable lesson notebooks
  exercises/                   # Exercise notebooks (mirrors book/chapters/exercises/)
  run_sitrep.py                # Example SitRep script
src/epi_learning/              # Reusable Python helper package
  __init__.py                  # Exports: attack_rate, case_fatality_rate, risk_ratio,
                               #   standardize_line_list, summarize_by_group
  metrics.py                   # Epi metrics (attack_rate, case_fatality_rate, risk_ratio)
  cleaning.py                  # Line-list data cleaning (standardize_line_list)
  tabulate.py                  # Group summary tabulation (summarize_by_group)
  viz.py                       # Visualization helpers (plot_epi_curve)
data/synthetic/                # Teaching datasets
  line_list.csv                # Sample case line-list
  admin_areas.geojson          # Administrative boundaries for spatial lessons
  location_population.csv      # Population data by location
tests/                         # pytest test suite
  test_metrics.py              # Unit tests for epi metrics
  test_cleaning.py             # Unit tests for data cleaning
  test_tabulate.py             # Unit tests for summarization
  test_notebook_smoke.py       # Smoke tests validating notebook JSON structure
.github/workflows/
  ci.yml                       # PR/push: pytest + jupyter-book build
  pages.yml                    # Deploy to GitHub Pages on push to main
```

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
- Lesson notebooks: `NN_topic_name.ipynb` (e.g., `06_spatial_choropleth.ipynb`)
- Exercise pairs: `NN_topic_exercise.ipynb` / `NN_topic_solution.ipynb`
- Python modules: lowercase with underscores

### Content language
- Prose and explanations: Traditional Chinese (繁體中文)
- Technical terms, variable names, code: English

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
