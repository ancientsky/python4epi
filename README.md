# Epi With Python

A Traditional Chinese-first learning website for infectious disease epidemiology with Python, from fundamentals to ML/DL.

## What This Project Covers

- Epidemiology fundamentals and core metrics
- Data cleaning, visualization, and epidemic curves
- Outbreak workflow and situation reporting
- Time-series, spatial analysis, and choropleth maps
- Machine learning and deep learning (PyTorch)
- Causal inference and reproducible research

## Core Principles

- Beginner-friendly science communication
- Copy-paste runnable code and notebooks
- End-to-end `uv` workflow, with Google Colab support

## Terminology / 術語慣例

本教材的流行病學中文術語依照**台灣（ROC）常用譯名**。例如：attack rate 譯為「侵襲率」（非「攻擊率」）、confidence interval 譯為「信賴區間」（非「置信區間」）。完整對照表請見 `CLAUDE.md`。

## Prerequisites

- Python `3.12`
- Node.js `20+` (required by Jupyter Book)

## Quick Start

```bash
uv python pin 3.12
uv sync
uv run jupyter lab
```

## Windows Quick Start (PowerShell)

```powershell
winget install Python.Python.3.12
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv python pin 3.12
uv sync
uv run jupyter lab
```

## Google Colab

不需要安裝任何東西，直接在 Colab 上開啟 notebook 即可。每個 notebook 頂部都有一個 setup cell，會自動偵測 Colab 環境並安裝所需套件：

```python
# Google Colab setup -- 若在本機執行可跳過此 cell
import sys
import os
if 'google.colab' in sys.modules:
    !git clone https://github.com/ancientsky/python4epi.git /content/python4epi 2>/dev/null || true
    os.chdir('/content/python4epi')
    !pip install -q -e .
```

## Windows Troubleshooting

- `uv : The term 'uv' is not recognized`
- Close and reopen PowerShell, then run `uv --version`.
- If still failing, confirm `%USERPROFILE%\\.local\\bin` is in `PATH`.

- `running scripts is disabled on this system`
- Run PowerShell as current user and execute:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

- VS Code cannot find notebook kernel
- In project root, run `uv sync`, then choose `.venv` Python interpreter in VS Code.

Recommended first lessons:
1. `book/chapters/00_guide.md`
2. `book/chapters/01_fundamentals.md`
3. `book/chapters/02_data_wrangling.md`

## Build the Site

Student edition (default TOC):

```bash
cp book/_toc_student.yml book/_toc.yml
uv run jupyter-book build book/
```

Instructor edition (includes solution chapter):

```bash
cp book/_toc_instructor.yml book/_toc.yml
uv run jupyter-book build book/
```

## Run Checks

```bash
uv run pytest
```

## Repository Layout

- `book/`: Jupyter Book source (`_config.yml`, TOCs, chapter markdown, embedded notebooks)
- `notebooks/`: runnable lesson notebooks
- `notebooks/exercises/`: exercise/solution notebook pairs
- `src/epi_learning/`: reusable helper package (`cleaning`, `metrics`, `tabulate`, `viz`)
- `data/synthetic/`: teaching datasets (CSV + GeoJSON)
- `tests/`: unit tests and notebook JSON smoke tests
- `.github/workflows/`: CI and GitHub Pages workflows

## Key Learning Assets

- Visualization toolkit notebook: `notebooks/02_visualization_epi_charts.ipynb`
- Spatial choropleth notebook: `notebooks/06_spatial_choropleth.ipynb`
- SitRep script example: `notebooks/run_sitrep.py`
