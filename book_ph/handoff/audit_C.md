# Audit C: outdated content in Ch10-17, notebooks 10-14, README / AGENTS / REWRITE_PLAN (as of 2026-11-11)

Method: read every in-scope file; executed all Ch10-14 notebooks, exercises and solutions (zh) cell by cell under the locked env (scikit-learn 1.8.0, xgboost 3.3.0, shap 0.54.1, torch 2.10.0, pandas 2.3.3, numpy 2.4.2, python-docx 1.2.0, python-pptx 1.0.2, fpdf2 2.9.0, statsmodels 0.14.6) with all Future/Deprecation/User warnings captured. Re-ran the non-torch ones in a scratch env with the newest releases (pandas 3.1.1, scikit-learn 1.9.1, numpy 2.5.4, statsmodels 0.15.0): zero errors and zero warnings, so pandas 3 and numpy 2.5 are NOT a code problem for these chapters. The only library deprecation found is F4 below. PyPI was reachable (version and date data below come from pypi.org JSON); ancientsky.github.io and the astral/google hosts were blocked, so the Pages links are "could not verify".

Line numbers: `.md` = text line; `.ipynb` = raw JSON line (use the cell text to locate). Unless stated, the en mirror has the same text at the same line number.

Counts: high 3, medium 9, low 6 (18 total).

---------------------------------------------------------------------------------

## HIGH

### F1. Appendix E-2 points readers to a config file and key that no longer exist (JB1 leftovers)
- File: `book/chapters/15_appendix.md:326` and `:336`
- Current text: "在 notebook 中（或透過 `_config.yml` 的 `nb_execution_pre_code`）設定：" and "本教材已在 `book/_config.yml` 的 `nb_execution_pre_code` 中全域設定 `pio.renderers.default = "notebook"`..."
- Why outdated: the book is Jupyter Book 2 / MyST. `ls book/_config.yml` fails; there is only `book/myst.yml`. The Plotly renderer is set in `src/epi_learning/book_setup.py` (`configure_book_kernel()`), injected as a kernel startup file by `scripts/build_book.py` (CLAUDE.md, README.md:109). MyST has no `nb_execution_pre_code`.
- Proposed zh (326): 「在 notebook 中，或在建置時用 kernel 啟動檔（startup file）統一設定：」
- Proposed zh (336): 「本教材已由 `scripts/build_book.py` 在每個執行 notebook 的 kernel 啟動時呼叫 `epi_learning.book_setup.configure_book_kernel()`，全域設定 `pio.renderers.default = "notebook"`，所有 notebook 不需再個別設定。如果你在自己的專案中遇到同樣問題，只要在 kernel 啟動時（或 notebook 第一格）加上面那兩行即可。」
- Severity: high (reference to a file that does not exist).
- en: same issue, `book_en/chapters/15_appendix.md:326` and `:336` ("`_config.yml`'s `nb_execution_pre_code`", "`book/_config.yml`'s `nb_execution_pre_code`"). Proposed en 336: "This book already sets `pio.renderers.default = "notebook"` globally: `scripts/build_book.py` calls `epi_learning.book_setup.configure_book_kernel()` when each notebook kernel starts, so no notebook needs to set it. In your own project, add those two lines at kernel startup (or in the first cell)."

### F2. python-pptx layout 5 is "Title Only", not a blank slide
- File: `book/chapters/14_case_studies.md:205`; also `book/chapters/notebooks/14_case_study_legionella.ipynb:766` (table) and `:790` (code comment "版面 5 = 空白版面")
- Current text: "`prs.slides.add_slide(prs.slide_layouts[5])` | 版面 5 = 空白投影片，自己用 textbox／picture／table 排版"
- Evidence (python-pptx 1.0.2 default template, `Presentation().slide_layouts`): 0 Title Slide, 1 Title and Content, 2 Section Header, 3 Two Content, 4 Comparison, **5 Title Only**, **6 Blank**. Layout 5 leaves an empty title placeholder on the slide ("Click to add title" in PowerPoint), which the code never fills.
- Proposed zh: 「版面 5 = 「僅標題」投影片（Title Only），自己再加 picture／table；要完全空白請用 `slide_layouts[6]`」; code comment: 「（版面 5 = 僅標題版面；記得填 `slide.shapes.title.text`，或改用 6 = 空白版面）」
- Severity: high (factually wrong, visible in the produced deck). Not strictly "dated", but checked against the pinned python-pptx.
- en: same, `book_en/chapters/14_case_studies.md:205` ("Layout 5 = a blank slide"), `book_en/chapters/notebooks/14_case_study_legionella.ipynb:766`, `:791` (comment "layout 5 = blank layout" is at the cell's comment line just above).

### F3. Appendix C tells readers to build the book with the bare JB1-style command
- File: `book/chapters/15_appendix.md:145`; also `:318`
- Current text: `uv run jupyter-book build book/ # 建置 Jupyter Book`; and "透過 `jupyter-book build` 產生的靜態 HTML"
- Why outdated/wrong: CLAUDE.md and README.md:139 say the site must be built through `scripts/build_book.py` ("never bare `jupyter book build`": it installs the kernel pre-execution setup (CJK font, Plotly renderer, chdir to repo root), runs `--execute --strict`, and does the post-build step). Bare `jupyter-book build book/` (it does run on JB 2.1.7) produces an un-executed site with wrong fonts and no language switcher/Colab links. REWRITE_PLAN.md:683 has the same stale command.
- Proposed zh (145): `uv run python scripts/build_book.py --lang zh --edition student  # 建置網站（需要 Node.js 24+）`; (318): 「透過 `scripts/build_book.py`（底層是 `jupyter book build`）產生的靜態 HTML」
- Severity: high for 145 (the documented command gives a broken site), low for 318.
- en: same, `book_en/chapters/15_appendix.md:145` and `:318`.

---------------------------------------------------------------------------------

## MEDIUM

### F4. `LogisticRegression(penalty=...)` is deprecated in scikit-learn 1.8 (and silenced in the notebook)
- File: `book/chapters/notebooks/10_ml_advanced.ipynb:178` (cell "zoo")
- Current text: `"LASSO": LogisticRegression(penalty="l1", solver="liblinear", C=0.5, class_weight="balanced", max_iter=2000),`
- Evidence (`uv run python -W error`): `FutureWarning: 'penalty' was deprecated in version 1.8 and will be removed in 1.10. ... Use l1_ratio=0 instead of penalty='l2', l1_ratio=1 instead of penalty='l1', and C=np.inf instead of penalty=None.` Executing the notebook cell also emits `UserWarning: Inconsistent values: penalty=l1 with l1_ratio=0.0` (cell 8 and the StackingClassifier cell 10, because the zoo is re-fitted). The warning is hidden by `warnings.filterwarnings("ignore")` in the import cell, and the notebook is built with `--strict`, so it does not fail yet, but it breaks when scikit-learn reaches 1.10 (1.9.1 is current on PyPI, 2026-09-10). Verified that `LogisticRegression(l1_ratio=1, solver="liblinear", C=0.5)` gives identical sparse coefficients without a warning.
- Proposed replacement: `"LASSO": LogisticRegression(l1_ratio=1, solver="liblinear", C=0.5, class_weight="balanced", max_iter=2000),`. Chapter text (10_machine_learning.md:293 "LASSO（L1 邏輯斯迴歸）") needs no change.
- Severity: medium.
- en: same, `book_en/chapters/notebooks/10_ml_advanced.ipynb:178`. No other `penalty=` use in Ch10-14 notebooks/exercises/solutions.

### F5. Time-series-foundation-model (TSFM) references outside the section being rewritten
(Skipping the section itself, `11_deep_learning.md` lines ~590-610, and the line-610 callout.) These pages sell TSFM zero-shot as *the* answer for "new pathogen, little data" and must stay consistent with the rewrite; they also contain nothing about LLMs / general foundation models, so after the rewrite the framing should be checked.
- `book/chapters/11_deep_learning.md:8`: "現代深度學習全景導覽：GNN（圖神經網路）、時空 Transformer / TFT、DeepSurv、時序基礎模型（TSFM）、PINN"
- `:20`: "圖神經網路、Transformer、時序基礎模型、物理知情神經網路"
- `:137` (figure alt text) "...新病原初期資料極少但外部有大量其他疫情資料就用TSFM零樣本或少樣本..."
- `:148`: "4. **新病原、初期資料極少，但外面已經有大量其他疫情的資料？** → 借用預訓練的 TSFM 做零樣本 / 少樣本預測，不用等自己的資料累積夠"
- `:159` (table row): "有相關的預訓練模型可遷移（TSFM 零樣本）"
- `:520` (figure alt text for dl_model_zoo): "...TSFM是讀遍全球案件的老手適..."
- `:712`: "（TSFM 零樣本預測的主場）"
- `:723`: "| 9 | TSFM 零樣本預測 + PINN / Mechanistic-AI ensemble |"
- Images that bake the term into the picture: `book/chapters/images/dl_decision_tree.svg`, `dl_model_zoo.svg` and the `_en` variants.
- Also note (for the rewriter): `timesfm` is now 3.0.2 (PyPI 2026-09-09), `chronos-forecasting` 2.3.2 (2026-09-08), `uni2ts` 2.0.0 (2025-11-04), `nixtla` 0.9.0, all need Python >=3.10; the snippet at :602-607 uses the v1 API (`timesfm.TimesFm(context_len=..., backend="cpu")`, `google/timesfm-1.0-200m`).
- Proposed text: replace "TSFM 零樣本" by whatever term/claim the rewrite settles on; if the section is hedged ("零樣本表現因病原與資料而異，需與 naive / ETS 基準比較"), echo that hedge at :148, :159 and :723.
- Severity: medium (consistency, depends on the rewrite).
- en: same lines, `book_en/chapters/11_deep_learning.md:8, 137, 148, 159, 520, 712, 723` (line 20 has the same sentence in en).
- No LLM / ChatGPT / Copilot / Claude / AI-coding-tool mention exists anywhere else in Ch10-17, the notebooks, README, AGENTS or REWRITE_PLAN (grep checked).

### F6. Ch13 "unpinned versions" example uses pandas 2.0 -> 2.2 as the cautionary tale
- File: `book/chapters/13_reproducibility.md:82`
- Current text: "`pandas` 從 2.0 升級到 2.2，某個函式對缺值或排序的預設處理悄悄改變"
- Why dated: pandas 3.0 was released 2026-01-21 (https://pandas.pydata.org/docs/whatsnew/v3.0.0.html) with exactly this kind of silent change: default `str` dtype, Copy-on-Write as the only mode. Today's reader who runs an unpinned `pip install pandas` gets 3.1.1 (2026-11-04). The lock here is still 2.3.3 (pyproject `pandas>=2.2.0`), which is a better teaching moment than the 2.0 -> 2.2 one.
- Proposed zh: 「`pandas` 從 2.x 升級到 3.0（預設字串型別改為 `str`、全面採用 Copy-on-Write），同一段程式碼對字串欄位與鏈式賦值的行為悄悄改變，同一份資料就算出不一樣的結果。」
- Severity: medium.
- en: same, `book_en/chapters/13_reproducibility.md:82` ("`pandas` upgrades from 2.0 to 2.2"). Proposed en: "`pandas` upgrades from 2.x to 3.0 (strings now default to the `str` dtype, Copy-on-Write everywhere), and the same code quietly behaves differently on string columns and chained assignment — same data, different numbers."

### F7. Appendix D troubleshooting row lists `SettingWithCopyWarning` as the typical error
- File: `book/chapters/15_appendix.md:163`
- Current text: "| `SettingWithCopyWarning` | 在 slice 上賦值 | 使用 `.copy()` 或 `.loc` |"
- Why outdated: with Copy-on-Write (the only mode in pandas 3.0, 2026-01-21) the warning no longer exists. Verified on pandas 3.1.1: `df[df.a>1]['b'] = 9` raises `ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment... Try using '.loc[row_indexer, col_indexer] = value'`, and the original frame is simply not modified. Under the locked pandas 2.3.3 the old warning still appears, so list both.
- Proposed zh: 「| `SettingWithCopyWarning`（pandas 2.x）／`ChainedAssignmentError`（pandas 3） | 在 slice 或鏈式索引（`df[cond]["col"] = ...`）上賦值，改不到原表 | 用 `df.loc[cond, "col"] = ...`，或先 `.copy()` |」
- Severity: medium.
- en: same, `book_en/chapters/15_appendix.md:163`.

### F8. Ch13 says `uv sync` guarantees the locked versions; it will silently re-lock a stale lockfile
- File: `book/chapters/13_reproducibility.md:62`, `:90`, `:106`, `:115`, `:242`, `:261`; also the Ch13 notebook intro and the appendix command list (`15_appendix.md:140`)
- Current text: "任何人執行 `uv sync`，裝出來的虛擬環境都跟你的一致" / "`uv sync` | 依照 `uv.lock` 裡鎖定的版本，...一模一樣"
- Why imprecise: plain `uv sync` updates `uv.lock` when `pyproject.toml` changed or the lock is stale. `uv sync --help` lists `--locked` ("Assert that the `uv.lock` will remain unchanged") and `--frozen` ("Sync without updating the `uv.lock` file"). The chapter's whole thesis is "lock = identical environment", so the verification step should use `--locked`.
- Proposed zh (106 and 242): `uv sync --locked`; add after the table at :115: 「`--locked` 會在 `uv.lock` 與 `pyproject.toml` 不一致時直接報錯，而不是默默重新解析版本；CI 與重現他人結果時建議一律加上。」
- Severity: medium (the guarantee claimed is stronger than the command gives).
- en: same, `book_en/chapters/13_reproducibility.md:62, 90, 106, 115, 242`.

### F9. GNN and survival "tools" in Part B are unmaintained or near-dormant
- File: `book/chapters/11_deep_learning.md:531` ("`torch-geometric`（PyG）、`DGL`") and `:578` ("`pycox`（DeepSurv、CoxTime、DeepHit）")
- Evidence (PyPI JSON, fetched 2026-11-11): `dgl` latest 2.2.1 released 2024-05-13 (no PyPI release for 2.5 years; NVIDIA RAPIDS also dropped cuGraph-DGL packages, https://docs.rapids.ai/notices/rsn0046/); `pycox` 0.3.0 released 2024-09-04 and its dependency `torchtuples` 0.2.2 released 2021-08-31; by contrast `torch-geometric` 2.8.1 (2026-10-12) and `pytorch-forecasting` 1.8.0 (2026-06-24) are active. Not run here (not installed), so "pycox imports cleanly on torch 2.10 / numpy 2" is unverified.
- Proposed zh (531): 「**工具**：`torch-geometric`（PyG，目前主流且持續更新；`DGL` 近兩年沒有新版）」; (578): 「**工具**：`pycox`（DeepSurv、CoxTime、DeepHit；最後一版為 2024 年，使用前先確認與你的 torch / numpy 版本相容）」
- Severity: medium (low if the rewrite already touches the zoo).
- en: same, `book_en/chapters/11_deep_learning.md:531` and `:578`.

### F10. REWRITE_PLAN.md is a finished plan whose instructions are now wrong
- File: `REWRITE_PLAN.md:618-619`, `:635`, `:683`, `:699-710`, and the status framing at `:1-60`
- Current text: "`book/_toc_student.yml`", "`book/_toc_instructor.yml`", "更新 `_toc_student.yml` 和 `_toc_instructor.yml`", "`uv run jupyter-book build book/` 成功建置", the Colab snippet with `try: import google.colab ... %cd /content/python4epi ... !pip install -e .`, "全書改寫規劃" as if work were pending ("現有章節盤點（15 章 + 13 notebook + 11 exercise/solution 對）", "新章節架構（18 章）", Phase 0-5 task tables).
- Why outdated: TOCs are now `project.toc` in `book/myst.yml`, `book/_instructor/myst.yml` and the `book_en` pair (`ls book/_toc*` fails); the book builds through `scripts/build_book.py`; the real Colab cell is `if 'google.colab' in sys.modules: !git clone ... 2>/dev/null || true; os.chdir(...); !pip install -q -e .`; the book has 19 chapter files (Ch00, 01, 01b, 02-17); all phases are done.
- Proposed fix: add a banner on line 1-2: 「> **歷史文件**：此規劃已於改寫完成後封存，僅供了解設計脈絡；現行結構與建置方式請見 `CLAUDE.md`、`README.md`。其中 `_toc_*.yml`、`jupyter-book build book/`、Colab setup cell 的寫法已過時。」 (or delete the file / move to `docs/archive/`).
- Severity: medium (a contributor or AI agent following it will touch non-existent files).
- en: n/a (root file).

### F11. Ch12 background case descriptions are shaky or contradicted by the official reports
- File: `book/chapters/12_causal.md:83` and `:143`
- Current text (83): "2019 年新北市曾發生一起校園團膳食物中毒事件，據調查與當日供應的滷雞腿有關...驗出產氣莢膜梭菌". (143): "2020 年新北市三峽區五寮里曾出現登革熱本土群聚，據調查與境外移入病例及周邊積水容器孳生病媒蚊有關".
- Evidence: the Sept 2019 New Taipei school-lunch Clostridium perfringens event is real, but Taiwan CDC's 疫情報導 papers name different implicated foods: one (2022) "滷雞腿", a later 2023 cohort report on the 11 Sept 2019 lunch names "宮保雞腿" (https://www.cdc.gov.tw/Uploads/7bb4fe1c-f9ed-4520-ac06-9d8c9cdf5484.pdf and https://www.cdc.gov.tw/Uploads/85ea9abf-40c5-4a28-8093-da70311bc599.pdf, found via search; I did not open them, so cite as "could not fully verify"). For Sanxia 2020: news/MOHW releases (e.g. https://newtalk.tw/news/view/2020-09-22/469016) describe a cluster around 五寮尖山 bamboo-shoot fields, started from a local case in Guishan, Taoyuan whose family worked there, with ~42 cases and control points at the fields; not an "imported case + water-container" story.
- Proposed zh (83): keep the lesson but hedge: 「報導指出...與當日供應的雞腿類菜色有關（不同報告指認的菜色名稱略有出入）」; (143): 「報導指出，2020 年 9 月新北市三峽區五寮里出現登革熱本土群聚，感染地研判與當地筍園有關，病媒蚊孳生源清除與管制人員進出同步展開。」 and adjust the DAG sketch (:146-150) so "境外移入" is not asserted as the source.
- Severity: medium-low (both blocks already say "非精確重現", but a reader can check and find a mismatch).
- en: same, `book_en/chapters/12_causal.md:83` and `:143`.

### F12. Ch14 "13 chapters" / "前 14 章" and run_sitrep.py claim a Legionella report that the script does not produce
- File: `book/chapters/13_reproducibility.md:107-109`, `:117`, `:244` (and `notebooks/run_sitrep.py`)
- Current text: Step 1 runs `uv run python notebooks/run_sitrep.py` and the table says it "讀取 line list、計算 CFR 與侵襲率、輸出各區統計表 — 這就是本章要的「最小可重跑報告」", right after the story "上次跑出來是 121 人感染、19 人死亡".
- Why stale: `notebooks/run_sitrep.py` still reads `data/synthetic/line_list.csv` (the old 10-row dataset, `attack_rate(total_cases, 5000)`) and prints "Cases by location", not the 280-row Legionella numbers (121 / 19) the chapter is built around. A reader who runs the three commands gets numbers that contradict the narrative. README.md:270 / AGENTS.md:15 also advertise it as "the SitRep example".
- Proposed fix: either update `run_sitrep.py` to read `legionella_outbreak.csv` and print the `summary` dict from Step 2, or change the table text to "(示範用的舊版 line list)". Doc-side zh replacement: 「這份腳本讀取示範用的 `line_list.csv`，示範「單一命令重跑」的結構；本章 Step 2 的 `summary` 才是 Legionella 事件的標準答案」.
- Severity: medium-low.
- en: same, `book_en/chapters/13_reproducibility.md:108, 117`.

---------------------------------------------------------------------------------

## LOW

### F13. Stale instructions in AGENTS.md
- `AGENTS.md:22`: "lessons: `NN_topic_name.ipynb` (e.g., `06_spatial_choropleth.ipynb`)": the spatial notebooks are numbered 08 (`08_spatial_choropleth.ipynb`; Ch06 is logistic regression). Proposed: `08_spatial_choropleth.ipynb`.
- `AGENTS.md:33`: "This workspace currently has no visible Git history; use Conventional Commits going forward": the repo has 121 commits (`git log --oneline | wc -l`). Proposed: "Use Conventional Commits:".
- `AGENTS.md:5`: "`notebooks/exercises/` stores exercise/solution pairs" is right, but line 7 "`data/synthetic/`: ... (e.g., `line_list.csv`, `admin_areas.geojson`)" lists only legacy files; the primary dataset `legionella_outbreak.csv` is not mentioned. Proposed: add `legionella_outbreak.csv` first.
- README.md / CLAUDE.md claims checked and found consistent (Python 3.14, Node 24+, 19 chapters, 21 lesson notebooks, `uv python pin 3.14`, `winget install Python.Python.3.14`, `astral.sh/uv/install.ps1`); no stale claim found there.
- Severity: low. en: n/a.

### F14. Colab setup cell in the four Ch14 notebooks uses `|| True` (capital T)
- File: `book/chapters/notebooks/14_case_study_legionella.ipynb:24`, `book/chapters/exercises/14_case_study_exercise.ipynb:24`, `book/chapters/solutions/14_case_study_solution.ipynb:24` and the standalone `notebooks/06_logistic_regression.ipynb:28`, `notebooks/14_case_study_legionella.ipynb:24`
- Current text: `!git clone https://github.com/ancientsky/python4epi.git /content/python4epi 2>/dev/null || True`
- Why wrong: in the shell `True` is not a command (`true` is). When the clone fails (e.g. the cell is re-run in the same Colab VM because the directory already exists) the user sees `True: command not found`. Every other notebook uses `|| true`. Not executed here (Colab-only), so this is by inspection.
- Proposed: `... 2>/dev/null || true`.
- Severity: low.
- en: same, `book_en/chapters/notebooks/14_case_study_legionella.ipynb:24`, `book_en/chapters/exercises/14_case_study_exercise.ipynb:24`, `book_en/chapters/solutions/14_case_study_solution.ipynb:24`.

### F15. Ch16 homework list omits the Ch01b exercise that exists
- File: `book/chapters/16_exercises.md:26-41`
- Current text: table rows 01, 02 ... 14 (14 rows). `book/chapters/exercises/01b_python_toolbox_exercise.ipynb` and `solutions/01b_python_toolbox_solution.ipynb` exist and README.md:23/:266 say "15 組", so the book page lists 14 and the README says 15. Same omission in `17_solutions.md:66-81` (14 rows).
- Proposed zh row (insert after 01): `| 01b | 開發者工具箱 | 終端機、Git、環境管理 | [作業](exercises/01b_python_toolbox_exercise.ipynb) |` and the matching solution link (instructor-edition URL, per CLAUDE.md rule not to link solution notebooks by relative path). I did not read the 01b notebook to confirm its topic line; adjust the description.
- Severity: low (not dated; stale vs repo contents).
- en: same, `book_en/chapters/16_exercises.md` and `17_solutions.md`.

### F16. Ch10 common-mistakes table contradicts the chapter's own prevalence
- File: `book/chapters/10_machine_learning.md:340`: "重症只佔 8% 時，「全猜沒病」就有 92% 準確率"; the chapter's Task B severe prevalence is 24% (76% accuracy, line 242) and the advanced notebook downsamples to ~8%. Not dated, but a reader will see two numbers. Proposed: 「重症只佔 8%（例如本章 Part B 下採樣後的情境）時...」.
- Severity: low. en: same, `book_en/chapters/10_machine_learning.md:340` (checked by grep pattern; wording identical).

### F17. Appendix claim about Google Colab fonts could not be verified
- File: `book/chapters/15_appendix.md:312`: "| Google Colab | 預裝 | Noto Sans CJK JP |". I could not check what the current Colab image ships (Colab is blocked in the sandbox). The Colab image changes with each runtime release (Python 3.12 in 2025-26); suggest adding a fallback line "若 `fc-list :lang=zh` 沒有輸出，先 `!apt-get install -y fonts-noto-cjk` 並重啟 runtime".
- Severity: low, "could not verify". en: same line 312.

### F18. Pages links in Ch16/17 and Ch10-14 solution links could not be verified
- `https://ancientsky.github.io/python4epi/` and `/instructor/chapters/solutions/*-solution/` URLs (16_exercises.md:16-19, 17_solutions.md:68-81, and the "解答版（講師）" lines in 10-14): host blocked by the sandbox proxy ("connect_rejected"), not evidence they are dead. `https://github.com/ancientsky/python4epi` returns HTTP 200. URL slugs follow the MyST "leading number dropped, `_` to `-`" rule in CLAUDE.md, so they look right. Severity: low (could not verify). en: n/a.

---------------------------------------------------------------------------------

## Checked, nothing to report

- Ch10 md and notebooks: OneHotEncoder(`drop="first"`, `handle_unknown="ignore"`), ColumnTransformer, cross_val_score, permutation_importance, `xgb.XGBClassifier(eval_metric=...)` in constructor (valid in xgboost 3.x), `shap.TreeExplainer`, `shap.summary_plot`, `shap.dependence_plot`, StackingClassifier, calibration_curve: no warnings under scikit-learn 1.8 / xgboost 3.3 / shap 0.54 (and none under scikit-learn 1.9.1, pandas 3.1.1 for the non-xgboost/shap cells).
- Ch11 PyTorch code (training loop, LSTM, 1D-CNN, `torch.manual_seed`, `state_dict` clone) ran clean on torch 2.10; baseline/sequence/exercise/solution notebooks produced no warnings.
- Ch12 notebook (statsmodels `smf.ols(..., cov_type="HC3")`, panel DiD), Ch13 notebook (stdlib + `np.random.default_rng`), Ch14 notebook (python-docx `Light Grid Accent 1`, BytesIO to pptx/docx) ran clean on locked and newest versions. The Taiwan Level-3 alert (May 2021) statement at 12_causal.md:250 is correct.
- Appendix terminology tables, Legionella facts (incubation 2-10 days, >70 C heat flush), foodborne table: no revised facts found. The appendix contains no course/book/website resource list, so there are no dead resource links to report.
- fpdf2 is used only in Ch04 (outside this scope); `fpdf2 2.9.0` is locked and the Ch04 note about `uni=True` matches the 2.5.1+ behaviour.
- README.md: all commands and version claims match `pyproject.toml`, `.python-version` and CLAUDE.md.
