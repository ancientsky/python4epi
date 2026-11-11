# Repository Guidelines

## Project Structure & Module Organization
- `book/`: Jupyter Book 2 (MyST) source — `myst.yml` (student edition config + TOC), `_instructor/myst.yml` (instructor TOC). Main learning content lives in `book/chapters/`. `book_en/` is the English mirror.
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
- `uv run python scripts/build_book.py --lang zh --edition student`: build the site (requires Node.js 24+); `--edition instructor` adds solutions, `--lang en` builds the English tree, `--all --site-dir _site` builds and assembles all four editions.

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
- validation output (`uv run pytest`, `scripts/build_book.py` if applicable)
- screenshots for major visualization/UI changes

## Security & Configuration Tips
- Do not commit real patient data; use synthetic or properly anonymized datasets only.
- Keep secrets out of notebooks and markdown.
- For map lessons, verify ID matching between data and GeoJSON before publishing.
