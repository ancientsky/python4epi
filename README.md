# Epi With Python

A Traditional Chinese-first learning website for infectious disease epidemiology with Python, from fundamentals to ML/DL.

## The Story

全書 18 章共享一個真實感的故事線：**松柏護理之家退伍軍人症群聚調查**。

> 週五下午四點，你接到衛生局的電話：某護理之家有多名住民出現肺炎症狀。
> 你帶著筆電趕到現場，開始進行流行病學調查⋯⋯

280 位住民、121 人感染、19 人死亡——你將用 Python 一步步揭開真相。

## What This Project Covers

| 幕 | 章節 | 主題 |
|----|------|------|
| 第一幕：接獲通報 | Ch00–02 | 導讀、Python 基礎、資料處理與視覺化 |
| 第二幕：描述性分析 | Ch03–04 | 2×2 表、卡方檢定、SitRep 工作流 |
| 第三幕：深入分析 | Ch05–08 | 分層分析、邏輯斯迴歸、時間序列、空間流病 |
| 第四幕：進階建模 | Ch09–12 | 存活分析、機器學習、深度學習、因果推論 |
| 第五幕：收尾與實戰 | Ch13–14 | 可重現研究、完整疫調報告 |
| 附錄 | Ch15–17 | 術語表、作業區（14 組）、解答區 |

## Core Principles

- Beginner-friendly science communication (繁體中文科普)
- Copy-paste runnable code and notebooks
- End-to-end `uv` workflow, with Google Colab support
- One unified dataset across all chapters for narrative continuity

## Terminology / 術語慣例

本教材的流行病學中文術語依照**台灣（ROC）常用譯名**。例如：attack rate 譯為「侵襲率」（非「攻擊率」）、confidence interval 譯為「信賴區間」（非「置信區間」）。完整對照表請見 `CLAUDE.md` 及 Ch15 附錄。

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

## CJK Font Troubleshooting (matplotlib 中文顯示)

matplotlib 圖表如果出現方框 □□□ 或 `Glyph missing from font(s) DejaVu Sans` 警告，表示系統缺少 CJK 字型或字型未被正確註冊。

**Linux (Ubuntu / CI):**

```bash
sudo apt-get install -y fonts-noto-cjk
rm -rf ~/.cache/matplotlib    # 清除字型快取
```

> **注意：** Noto Sans CJK 以 `.ttc` 集合檔安裝，matplotlib 的 `addfont()` 只會註冊 face 0（通常是 JP 變體）。因此 `font.sans-serif` 候選清單中須包含 `"Noto Sans CJK JP"` 等多個變體——它們的 CJK 字集相同，都能顯示繁體中文。

**所有平台通用設定（在 `import matplotlib.pyplot as plt` 之後）：**

```python
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
```

詳細排錯步驟見書中 Ch15 附錄 E。

## Plotly in Jupyter Book

Plotly 圖表在 `jupyter-book build` 時顯示空白？設定渲染器：

```python
import plotly.io as pio
pio.renderers.default = "notebook"
```

本教材已在 `book/_config.yml` 的 `nb_execution_pre_code` 中全域設定。

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

- `book/`: Jupyter Book source (`_config.yml`, TOCs, 18 chapter markdown files, embedded notebooks)
- `notebooks/`: standalone runnable lesson notebooks
- `notebooks/exercises/`: exercise/solution notebook pairs (14 chapters)
- `src/epi_learning/`: reusable helper package (`cleaning`, `metrics`, `tabulate`, `viz`)
- `data/synthetic/`: teaching datasets — primary: `legionella_outbreak.csv` (280 × 32)
- `tests/`: unit tests and notebook JSON smoke tests
- `.github/workflows/`: CI and GitHub Pages workflows

## Dataset

**`data/synthetic/legionella_outbreak.csv`** — 280 位住民 × 32 欄

模擬松柏護理之家退伍軍人症群聚事件的合成資料集。涵蓋人口學、共病、暴露史、臨床嚴重度、結果等完整疫調欄位。詳細欄位說明見 Ch15 附錄。

## Key Learning Assets

- Lesson notebooks: `notebooks/01_*.ipynb` through `notebooks/14_*.ipynb`
- Exercise notebooks: `notebooks/exercises/NN_*_exercise.ipynb` (14 chapters)
- Visualization toolkit: `notebooks/02_visualization_epi_charts.ipynb`
- Spatial analysis: `notebooks/08_spatial_rates.ipynb`
- Complete outbreak report: `notebooks/14_case_study_legionella.ipynb`
- SitRep script example: `notebooks/run_sitrep.py`

## Recommended Reading Order

1. `book/chapters/00_guide.md` — 導讀與環境設定
2. `book/chapters/01_fundamentals.md` — Python 基礎
3. `book/chapters/02_data_wrangling.md` — 資料處理與視覺化
4. Follow the story from Ch03 onwards!
