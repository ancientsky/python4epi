# Repository Guidelines

## Project Structure & Module Organization
- `book/`: Jupyter Book source (chapters, TOC, config). Main learning content lives in `book/chapters/`.
- `notebooks/`: runnable lesson notebooks; `notebooks/exercises/` stores exercise/solution pairs.
- `src/epi_learning/`: reusable Python helpers (`cleaning.py`, `metrics.py`, `tabulate.py`, `viz.py`).
- `data/synthetic/`: teaching datasets (e.g., `line_list.csv`, `admin_areas.geojson`).
- `tests/`: unit and smoke tests.
- `.github/workflows/`: CI and Pages deployment pipelines.

## Build, Test, and Development Commands
- `uv sync`: install and lock dependencies into local `.venv`.
- `uv run pytest`: run unit + notebook JSON smoke tests.
- `uv run jupyter lab`: start local notebook environment.
- `uv run python notebooks/run_sitrep.py`: run the SitRep example end-to-end.
- `uv run jupyter-book build book/`: build the site (requires Node.js 20+).
- Instructor build: `cp book/_toc_instructor.yml book/_toc.yml && uv run jupyter-book build book/`.

## Coding Style & Naming Conventions
- Python: 4-space indentation, clear variable names, and small focused functions.
- Follow existing module style in `src/epi_learning/`.
- File naming:
- lessons: `NN_topic_name.ipynb` (e.g., `06_spatial_choropleth.ipynb`)
- exercises: `NN_topic_exercise.ipynb` and `NN_topic_solution.ipynb`
- Keep markdown educational and copy-paste runnable; prefer Traditional Chinese explanations with English technical terms.

## Testing Guidelines
- Framework: `pytest`.
- Test files: `tests/test_*.py`; keep tests deterministic and fast.
- Update smoke tests when adding notebooks under `notebooks/`.
- Minimum bar for PRs: `uv run pytest` must pass.

## Commit & Pull Request Guidelines
- This workspace currently has no visible Git history; use Conventional Commits going forward:
- `feat: add choropleth lesson notebook`
- `fix: correct epi week conversion in chapter 02`
- PRs should include:
- scope summary (chapters/modules changed)
- validation output (`uv run pytest`, `jupyter-book build` if applicable)
- screenshots for major visualization/UI changes

## Security & Configuration Tips
- Do not commit real patient data; use synthetic or properly anonymized datasets only.
- Keep secrets out of notebooks and markdown.
- For map lessons, verify ID matching between data and GeoJSON before publishing.
