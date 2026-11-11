# Audit A — Ch00–04 (+intro), zh `book/` and en `book_en/`, as of 2026-11-11

Pinned (uv.lock): pandas 2.3.3, numpy 2.4.2, matplotlib 3.10.8, seaborn 0.13.2, scipy 1.17.0, statsmodels 0.14.6, plotly 6.5.2; .python-version 3.14; requires-python >=3.12; pyproject has `pandas>=2.2.0` (no upper bound).
PyPI latest pandas today: 3.1.1 (curl https://pypi.org/pypi/pandas/json). A learner who follows ch00's `uv add pandas` (00_guide.md:326, 376) gets pandas 3.x, not 2.3.3.

Verification done:
- Executed every notebook, exercise and solution of ch01-04 (zh, 3 dirs, 16 files) with PYTHONWARNINGS=default against the locked env: 0 errors, 0 deprecation warnings. Re-ran all with `--with pandas==3.1.1`: 0 errors, 0 warnings. So no code in the notebooks is broken; findings below are prose/teaching-snippet issues.
- No named AI tools/models/prices, no Colab UI click-steps, no "free tier" quotas in scope (only "Colab: free cloud Jupyter / free GPU" generic, 00_guide.md:759, still true).
- Install instructions are uv + Python 3.14, consistent with .python-version. Python 3.15.0 final was released 2026-10-09 (https://discuss.python.org/t/python-3-15-0-final-is-here/109415, python.org/downloads/release/python-3150), so 00_guide.md:245 "3.15 才剛推出（2026 年 10 月）" is accurate.
- 退伍軍人症 = 第三類法定傳染病 (1-week report) is correct (CDC Taiwan 法定及新興傳染病個案報告單, 第三類 list incl. 退伍軍人病).
- Story dates (2026-01-12..28) do not clash with the present.

## Findings

### 1. [medium] Chained `inplace=True` fillna shown as the "good comment" example
- zh: book/chapters/00_guide.md:578
- Text: `df["age"].fillna(df["age"].median(), inplace=True)`
- Why: works silently in pandas 2.3.3, but in pandas 3 (Copy-on-Write always on) it is a no-op. Proof, pandas 3.1.1: `df['age'].fillna(1, inplace=True)` -> `ChainedAssignmentError: ... Such inplace method never works to update the original DataFrame or Series`. pandas 3.1.1 is what a fresh `uv add pandas` installs. The book teaches a pattern that silently fails for new installs.
- Fix (zh): `df["age"] = df["age"].fillna(df["age"].median())`
- en: same issue, book_en/chapters/00_guide.md:578 (fix: same code line; comment text is already translated).

### 2. [medium] "text columns are `object`" and "`datetime64[ns]`" are pandas-2 only
- zh: book/chapters/02_data_wrangling.md:133 (`` `object` 文字 ``), :136 (「`object` 型別通常代表『文字』」), :159 (「讀入時都是**文字（object）**」); notebook book/chapters/notebooks/02_data_wrangling_for_beginners.ipynb cell 3 (comment "object=文字") and cell 5 ("應該都變成 datetime64[ns]，不再是 object", "CSV 讀進來的日期是「文字」(object)").
- Why: in pandas 3 string columns have dtype `str` (confirmed: `pd.read_csv(...)['wing'].dtype` -> `str` on 3.1.1) and `to_datetime` of strings yields `datetime64[us]`, so `df.info()` / `.dtypes` output will not match the text. Correct for locked 2.3.3, wrong for anyone on current pandas.
- Fix (zh): ":136 💡 `object`（pandas 3 起顯示為 `str`）型別代表「文字」——日期欄位讀進來也是文字，需要手動轉換成 `datetime`。"; :133 "`object`／`str` 文字"; notebook comment "應該都變成 datetime64（pandas 2 顯示 [ns]，pandas 3 為 [us]），不再是文字". Alternatively cap `pandas<3` in pyproject and say so in ch00 (then this finding drops to low).
- en: same issue, book_en/chapters/02_data_wrangling.md:133, :136, :159; notebook book_en/chapters/notebooks/02_data_wrangling_for_beginners.ipynb cells 3 and 5 ("object=text", "no longer object", "datetime64[ns]").

### 3. [low] "this book's venv has pandas 2.2" vs lock 2.3.3
- zh: book/chapters/00_guide.md:271 `└── pandas 2.2、matplotlib 3.10 ...` (labelled 專案 C（本教材）)
- Why: uv.lock pins pandas 2.3.3. Projects A/B lines (269-270) are hypothetical and fine.
- Fix: `└── pandas 2.3、matplotlib 3.10 ...`
- en: same, book_en/chapters/00_guide.md:271.

### 4. [low] Example installs/pins Python versions the project does not support
- zh: book/chapters/01b_python_toolbox.md:444 `uv python install 3.11`, :447 `uv python pin 3.12`
- Why: requires-python >=3.12 and book standard is 3.14 (ch00:233, 323); 3.11 is below the project's floor and is the only place a different install version is taught, so a reader copying it breaks `uv sync`.
- Fix: `uv python install 3.14` / `uv python pin 3.14`.
- en: same, book_en/chapters/01b_python_toolbox.md:444, 447.

### 5. [low] COVID-19 used as the example of a pathogen needing contact lists / "infectious period 2–14 days"
- zh: book/chapters/04_outbreak_workflow.md:1346-1347 "若病原為 COVID-19 / 流感 / 諾羅病毒… 向前追溯期 = 可傳染期（例：COVID-19 感染後 2–14 天）"
- Why: 2-14 days is the old incubation/quarantine window, not an infectious period; Taiwan ended COVID-19 close-contact tracing/quarantine in 2023 (COVID is now a 第四類 disease, routine case management). I could not fetch an official page (cdc.gov.tw / www.cdc.gov blocked) so treat as "could not verify wording"; the conceptual error (incubation vs infectious period) stands regardless.
- Fix: "若病原為麻疹／結核病／諾羅病毒（有人傳人）：向前追溯期 = 可傳染期（例：諾羅病毒自症狀開始至症狀緩解後 48–72 小時）" — or just drop the COVID example.
- en: same, book_en/chapters/04_outbreak_workflow.md:1320-1321.

### 6. [low / could not verify] CDC links in the epi-curve admonition
- zh: book/chapters/02_data_wrangling.md:709 `https://www.cdc.gov/wcms/4.0/cdc-wp/data-presentation/epi-chart.html` and `https://www.cdc.gov/field-epi-manual/php/chapters/describing-epi-data.html`; also :29 `https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf`, :1279 colorbrewer2.org, 00_guide.md:201/215 astral.sh install scripts, :132 docs.astral.sh/uv
- Why: all those hosts are blocked by the sandbox (curl 000 / WebFetch ENOTFOUND) -> could not verify. The `/wcms/4.0/cdc-wp/` path looks like an internal CMS staging path, not a stable public URL, so it is the likeliest to be dead; recommend a manual click-test. github.com/ancientsky/python4epi returns 200; ancientsky.github.io not reachable from sandbox.
- Fix: if dead, use the Field Epi Manual chapter only, or CDC "Principles of Epidemiology" epi-curve lesson.
- en: same link, book_en/chapters/02_data_wrangling.md:709.

## Not findings (checked, fine)
- `uv add`, `uv sync`, `uv python install 3.14` instructions; launchd/cron/schtasks steps (ch00 :814-905, ch04 :1484-1604) still valid.
- Plotly 6 / matplotlib 3.10 / seaborn 0.13 / scipy 1.17 / numpy 2.4 code in ch02-04 notebooks ran with no warnings (`observed=True` already passed to groupby, no `applymap`, `freq="D"` only).
- Colab setup cell `!pip install -q -e .` is mandated by CLAUDE.md for Colab; fine.
- Legionella facts (incubation 2-10 d, serogroup 1 >80%, CFR 5-10% community / up to 25-30% institutional, no person-to-person spread) match current CDC/WHO summaries.
