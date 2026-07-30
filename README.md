# Epi With Python

A Traditional Chinese-first learning website for infectious disease epidemiology with Python, from fundamentals to ML/DL.

## The Story

全書 19 章共享一個真實感的故事線：**松柏護理之家退伍軍人症群聚調查**。

> 週五下午四點，你接到衛生局的電話：某護理之家有多名住民出現肺炎症狀。
> 你帶著筆電趕到現場，開始進行流行病學調查⋯⋯

280 位住民、121 人感染、19 人死亡——你將用 Python 一步步揭開真相。

## What This Project Covers

| 幕 | 章節 | 主題 |
|----|------|------|
| 第一幕：接獲通報 | Ch00–02（含 Ch01b） | 導讀、Python 基礎、開發者工具箱、資料處理與視覺化 |
| 第二幕：從描述到推論 | Ch03–04 | 2×2 表、卡方檢定、SitRep 工作流 |
| 第三幕：深入分析 | Ch05–08 | 分層分析、邏輯斯迴歸、時間序列、空間流病 |
| 第四幕：進階建模 | Ch09–12 | 存活分析、機器學習、深度學習、因果推論 |
| 第五幕：收尾與實戰 | Ch13–14 | 可重現研究、完整疫調報告 |
| 附錄與練習 | Ch15–17 | 術語表、作業區（15 組）、解答區 |

## Core Principles

- Beginner-friendly science communication (繁體中文科普)
- Copy-paste runnable code and notebooks
- End-to-end `uv` workflow, with Google Colab support
- One unified dataset across all chapters for narrative continuity

## Terminology / 術語慣例

本教材的流行病學中文術語依照**台灣（Taiwan）常用譯名**。例如：attack rate 譯為「侵襲率」（非「攻擊率」）、confidence interval 譯為「信賴區間」（非「置信區間」）。完整對照表請見 `CLAUDE.md` 及 Ch15 附錄。

## Prerequisites

- Python `3.13` (pinned in `.python-version`; the package itself accepts `>=3.12`)
- Node.js `24+` (required by Jupyter Book)

## Quick Start

```bash
uv python pin 3.13
uv sync
uv run jupyter lab
```

## Windows Quick Start (PowerShell)

```powershell
winget install Python.Python.3.13
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv python pin 3.13
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

The site ships in **two languages** — Traditional Chinese (`book/`) and English
(`book_en/`) — each with a student and an instructor edition. Every page has a
繁中 / EN language switcher in the top-right header (`book/_static/lang-switch.js`
toggles the `/en/` path prefix). GitHub Pages deploys four variants:

| Edition | URL |
|---------|-----|
| 中文 學生版 | `/python4epi/` |
| 中文 教師版 | `/python4epi/instructor/` |
| English student | `/python4epi/en/` |
| English instructor | `/python4epi/en/instructor/` |

Chinese student edition (default TOC):

```bash
cp book/_toc_student.yml book/_toc.yml
uv run jupyter-book build book/
```

Chinese instructor edition (includes solution chapter):

```bash
cp book/_toc_instructor.yml book/_toc.yml
uv run jupyter-book build book/
```

English editions (mirror the Chinese tree; `book_en/` shares `_static`,
`_templates`, chapter images, and `data` with `book/` via symlinks):

```bash
cp book_en/_toc_student.yml book_en/_toc.yml
uv run jupyter-book build book_en/            # English student

cp book_en/_toc_instructor.yml book_en/_toc.yml
uv run jupyter-book build book_en/            # English instructor (with solutions)
```

## Run Checks

```bash
uv run pytest                                            # unit + notebook smoke tests
uv run ruff check videos/ --select F821,E9               # undefined names in Manim scenes
uv run python videos/sync_video_embeds.py --validate     # youtube_ids.yaml is usable
uv run python videos/sync_video_embeds.py --check        # ...and chapters are in sync
```

CI runs the first three. `--check` is local-only: the embeds committed in the
chapters are a snapshot that the deploy re-renders, so it is expected to go stale.

## Tutorial Videos

Ch00–Ch14 共 **122 個概念**都有配套教學影片（Manim + edge-tts + ffmpeg），以輕鬆幽默的語調手把手教學。附錄章（Ch15–17）依設計沒有影片。

每個概念都有**中英雙語**兩支影片，共用同一組 Manim 動畫，只換旁白與畫面文字：

| 語言 | 腳本 | 配音 |
|------|------|------|
| 繁體中文 | `videos/scripts/<name>.yaml` | `zh-TW-HsiaoChenNeural` |
| English | `videos/scripts/<name>_en.yaml` | `en-US-AriaNeural` |

影片採用統一的視覺風格：暖白色背景 `#FAF8F3`、橘色強調 `#D97757`、藍色輔助 `#6A9BCC`、綠色成功 `#788C5D`。每支影片包含三個部分：

1. **主線教學** — 用退伍軍人症群聚資料解說核心概念
2. **額外防疫範例** — 同一概念應用到其他疫情（COVID-19、登革熱、腸病毒等）
3. **初學者盲點** — 3 個常見錯誤，用「錯誤 vs 正確」對照動畫呈現

```bash
uv sync --group video
sudo apt install ffmpeg fonts-noto-cjk          # Linux 系統相依

uv run python videos/build.py --all --lang zh   # 全部中文版
uv run python videos/build.py --chapter ch08 --lang en   # 單章英文版
```

也可以用 GitHub Actions 的 **Build Tutorial Videos** workflow 手動觸發，它會**每支影片各開一個平行 job**，避免大章節（Ch02 有 13 支）撞到單一 job 的時間上限。

### 把 YouTube 連結掛上網站

`videos/youtube_ids.yaml` 是全站影片連結的**唯一真相來源**。建置產出的檔名就是登錄表的 key，不需查對照：

| 產出檔案 | 登錄表 key | 欄位 |
|----------|-----------|------|
| `ch08_04_morans_i.mp4` | `ch08_04_morans_i` | `zh:` |
| `ch08_04_morans_i_en.mp4` | `ch08_04_morans_i` | `en:` |

**直接在 GitHub 網頁上編輯這個檔案就好**——commit 到 `main` 之後 *deploy-pages* 會在建置前自動把登錄表算成中英兩版的影片卡片，幾分鐘後網站就更新了，不需要任何人在本機跑東西，也不會有機器人 commit（`main` 的 ruleset 本來就擋機器人直接推送）。同時 *Check video links* 會在約 30 秒內驗證你貼的連結，打錯了馬上就知道。貼完整網址或純 ID 都可以；留空則該卡片不會出現在網站上（不會有死連結）。

由於卡片是在部署時才產生，repo 裡章節 markdown 內的卡片只是**快照**，會落後於登錄表——網站不受影響。要順便更新快照與 `videos/VIDEO_INDEX.md`，在本機執行 `uv run python videos/sync_video_embeds.py`。細節見 [`videos/README.md`](videos/README.md)。

## Visual Diagrams

章節中嵌入手繪 SVG 教學圖（`book/chapters/images/`），用統一色彩配置視覺化解說困難概念：

- 2×2 列聯表解剖圖、RR vs OR 直覺圖、CI log 轉換三步驟
- 卡方檢定觀察值 vs 期望值、森林圖閱讀指南
- Git 工作流程、分支概念、PR 協作流程、學習路線圖

## Repository Layout

- `book/`: Jupyter Book source, 繁中版 (`_config.yml`, TOCs, 19 chapter markdown files, embedded notebooks)
- `book_en/`: English mirror of `book/`; shares `_static`, `_templates`, chapter images and `data` via symlinks
- `book/chapters/images/`: hand-crafted SVG diagrams for visual explanations
- `book/_static/`: custom CSS/JS (youtube-lite embed, language switcher)
- `notebooks/`: standalone runnable lesson notebooks (21 files)
- `notebooks/exercises/`: exercise/solution notebook pairs (15 chapters)
- `src/epi_learning/`: reusable helper package (`cleaning`, `metrics`, `tabulate`, `viz`)
- `data/synthetic/`: teaching datasets — primary: `legionella_outbreak.csv` (280 × 32)
- `videos/`: tutorial video generation (Manim + edge-tts + ffmpeg) — `scripts/` narration YAML, `scenes/` Manim classes, `youtube_ids.yaml` link registry
- `tests/`: unit tests and notebook JSON smoke tests
- `.github/workflows/`: `ci.yml` (tests + build), `pages.yml` (renders video embeds, then deploys), `videos.yml` (render videos), `sync-video-links.yml` (validate the link registry)

## Dataset

**`data/synthetic/legionella_outbreak.csv`** — 280 位住民 × 32 欄

模擬松柏護理之家退伍軍人症群聚事件的合成資料集。涵蓋人口學、共病、暴露史、臨床嚴重度、結果等完整疫調欄位。詳細欄位說明見 Ch15 附錄。

## Key Learning Assets

- Lesson notebooks: `notebooks/01_*.ipynb` through `notebooks/14_*.ipynb` (21 notebooks)
- Exercise notebooks: `notebooks/exercises/NN_*_exercise.ipynb` (15 chapters, each with a matching solution)
- Visualization toolkit: `notebooks/02_visualization_epi_charts.ipynb`
- Spatial analysis: `notebooks/08_spatial_rates.ipynb`
- Complete outbreak report: `notebooks/14_case_study_legionella.ipynb`
- SitRep script example: `notebooks/run_sitrep.py`

## Recommended Reading Order

1. `book/chapters/00_guide.md` — 導讀與環境設定
2. `book/chapters/01_fundamentals.md` — Python 基礎
3. `book/chapters/02_data_wrangling.md` — 資料處理與視覺化
4. Follow the story from Ch03 onwards!
