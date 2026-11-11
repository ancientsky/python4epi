# Audit B — ch05-09 (as of 2026-11-11). Locked versions: pandas 2.3.3, numpy 2.4.2, scipy 1.17.0, statsmodels 0.14.6, prophet 1.3.0, geopandas 1.1.2, esda 2.10.0, libpysal 4.15.0, lifelines 0.30.1, plotly 6.5.2, matplotlib 3.10.8, scikit-learn 1.8.0.
Method: all code cells of ch05-09 notebooks/exercises/solutions executed with warnings=always under (a) the lock (uv run --frozen) and (b) a scratch venv with the latest PyPI (pandas 3.1.1, statsmodels 0.15.0, geopandas 1.2.0, scipy 1.18.1, numpy 2.5.4). Zero cell errors in either. Paths are zh; en mirror noted per item. External hosts (od.cdc.gov.tw, maps.nlsc.gov.tw) are proxy-blocked: "could not verify".

## HIGH

### 1. Firth logistic fallback points to a package that crashes with current scikit-learn
- book/chapters/06_logistic_regression.md:554 — "改用 **Firth's penalized likelihood**（`firthlogist` 套件）"
- Evidence: firthlogist's last release is 0.5.0 (2022-08-07, pypi.org/pypi/firthlogist/json). Installed next to scikit-learn 1.9.1 (lock has 1.8.0): `FirthLogisticRegression().fit(X,y)` -> `AttributeError: 'FirthLogisticRegression' object has no attribute '_validate_data'` (removed in sklearn 1.6). The advice cannot be followed in this repo's own env.
- Proposed zh: "改用 **Firth 懲罰概似法**（Python 目前沒有維護良好的套件；`firthlogist` 已停止更新且與 scikit-learn ≥ 1.6 不相容，可改用 R 的 `logistf`，或下列的精確邏輯斯迴歸／貝氏弱訊息先驗）"
- en: same issue, book_en/chapters/06_logistic_regression.md:530 ("Switch to **Firth's penalized likelihood** (the `firthlogist` package)"). Proposed en: "Use **Firth's penalized likelihood** (no well-maintained Python package today: `firthlogist` has been unreleased since 2022 and breaks on scikit-learn >= 1.6; use R `logistf` or a weakly-informative Bayesian prior instead)".
- severity: high

### 2. Ch07 presents Prophet as "the modern option" and has no mention of foundation models
- book/chapters/07_time_series.md:185 "**Prophet**（好上手的現代選項）"; :188 "是免調參版的 SARIMA 替代方案"; :628 "Prophet 是 Meta 開源的預測工具"; :736 "要快速上手、… → Prophet"; :24 learning-objective bullet; image alt :182 and the SVGs `images/timeseries_method_map.svg`, `images/prophet_decomposition.svg`. Same in notebook 07_time_series_baseline.ipynb (Step 11 cells, summary table "⑦ Prophet" ~line 19 of cell) and exercise Q9 (exercises/07_time_series_exercise.ipynb "題目 9").
- Why dated: Prophet's official README carries a 2026 notice that the project is in maintenance mode (bug fixes and dependency bumps only, no new features) (https://raw.githubusercontent.com/meta/prophet/main/README.md ; search summary 2026-11). Google TimesFM 3.0 was released 2026-08-31 (330M-param zero-shot, multivariate/covariates, google/timesfm-3.0-pytorch on Hugging Face; weights under a NON-COMMERCIAL licence while code is Apache-2.0) (https://thenewstack.io/google-timesfm-3-multivariate-forecasting/ ; https://gigazine.net/news/20260901-google-timesfm-3/). Time-series foundation models (TimesFM, Chronos-2, Moirai, TabPFN-TS) are now the standard "no tuning, uncertainty included" baseline, which is exactly the niche the chapter sells Prophet for. The chapter's "method map" ends at Prophet.
- Proposed zh (replace :185 "好上手的現代選項" with): "好上手的經典選項（目前已進入維護模式，不再新增功能）"; replace :188 with: "是免調參版的 SARIMA 替代方案；2026 年起更省事的做法是時間序列基礎模型（見 Step 12 後的「延伸：時間序列基礎模型」）". Add a new short section after Step 11/12 and a bullet in the decision list at :736: "- **完全不想調參、有多條相關序列或外部變數（氣溫、假日）** → 時間序列基礎模型（Google TimesFM 3.0、Amazon Chronos-2 等）：零樣本（zero-shot）直接預測，不需訓練。⚠️ 注意：TimesFM 3.0 權重僅限非商業使用；基礎模型一樣會在疫情轉折點失靈，且要與本章的 rolling mean / SARIMA 基準比 MAE，不能只看圖。" Add to 常見錯誤 (:798) a note that Prophet is maintenance-only. Add one non-executed (or `# 需另外安裝`) code sketch, e.g. `import timesfm` -> `model.forecast(horizon=7, inputs=[train.values])`, keeping notebooks fast (build executes every cell).
- en: same issue, book_en/chapters/07_time_series.md:24, 178-184, 598-600, ~708 (decision list), ~770 (mistake #8); same notebook cells in book_en/.
- severity: high (explicit task item; chapter's closing recommendation is dated)

## MEDIUM

### 3. esda 2.10: conditional-randomization p-values change in next major release (DeprecationWarning, shown in solution; hidden in notebook by warnings.filterwarnings("ignore"))
- book/chapters/08_spatial.md:562 `lisa = Moran_Local(main["rate"].values, w, permutations=999, seed=8)` and :593 `gi = G_Local(main["rate"].values, w_b, permutations=999, seed=8, star=True)`; notebooks/08_spatial_statistics.ipynb:245 and :296 (warning suppressed at its cell 2 `warnings.filterwarnings("ignore")`); solutions/08_spatial_solution.ipynb:426 and :465; exercises/08_spatial_exercise.ipynb:336 and :362 (hints).
- Evidence (uv run, esda 2.10.0): "esda/moran.py:1374: DeprecationWarning: The alternative hypothesis for conditional randomization is changing in the next major release of esda. We recommend setting alternative='two-sided', which will generally double the p-value returned. To retain the current behavior, set alternative='directed'." Same for esda/getisord.py:374. The book's quadrant/hotspot significance thresholds (p<0.05) would silently halve in power after upgrade; text "p_sim" explanations assume the one-sided value.
- Proposed: pass the argument explicitly and say why: `Moran_Local(main["rate"].values, w, permutations=999, seed=8, alternative="two-sided")` and `G_Local(..., star=True, alternative="two-sided")`; add table row "`alternative="two-sided"` | 雙尾檢定；esda 下一個大版本會改成預設，現在明確寫出可避免 p 值突然變動（p 值約為舊版 `directed` 的兩倍）". Re-check the "幾個 HH/熱點縣市" counts quoted in prose after the change (two-sided doubles p).
- en: same issue, book_en/chapters/08_spatial.md:562, :593 and the same notebooks/solutions in book_en/.
- severity: medium

### 4. Choropleth notebook teaches disabling TLS verification
- book/chapters/notebooks/08_spatial_choropleth.ipynb:42 (Step 1 cell: `ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE`, "SSL 驗證失敗 → 改試停用驗證重新下載"; tag "（⚠ 已停用 SSL 驗證）"). Also the comment "針對台灣政府站憑證缺 SKID 問題".
- Why inappropriate in 2026: silently falling back to unverified HTTPS for downloaded data/zip is a MITM risk and is flagged by every current linter/security guidance; the cited "missing SKID" cert quirk could not be verified (hosts blocked: od.cdc.gov.tw, maps.nlsc.gov.tw -> "could not verify"). The notebook already has a repo-bundled GeoJSON (`data/geojson/county_smooth_inset.geojson`) and a tilegram fallback, so the insecure path is unnecessary.
- Proposed zh: remove the `insecure` retry; on SSL error print "憑證驗證失敗，請改用 data/external 手動下載後放入，或使用內建示範資料" and set `_DEMO=True`. If a government cert truly lacks SKID, ship a pinned copy of the CSV under data/ instead.
- en: same, book_en/chapters/notebooks/08_spatial_choropleth.ipynb:42.
- severity: medium

### 5. Choropleth rates use one 2023 population snapshot for 2003-2025; "至今" and fallback year range frozen at 2024
- book/chapters/notebooks/08_spatial_choropleth.ipynb:74 "# 近似縣市人口（2023 年估計，單位：人）" with a single `COUNTY_POP` applied to every year (and `.fillna(500_000)`); :58 demo `for yr in range(2003, 2025)`; :0 title "（2003–至今）"; Step 6 label "最新年度". In Nov 2026 the data run through 2025 (complete) and Taiwan's population has been falling; a 2023 constant makes 2003-2012 rates biased (e.g. 新北市 was ~3.9M, 桃園市 ~2.0M then). Also md 08_spatial.md:377 "（2003–）" and :430 "最新年度".
- Proposed zh: "# 縣市人口（內政部戶政司 2025 年底資料，僅供示範；嚴謹分析請依年度用各年人口）" and change `range(2003, 2025)` -> `range(2003, 2026)`; add a one-line warning "固定人口數只適合看相對高低，不適合比較不同年份的發生率". Replace "至今" with "2003–2025". Replace the numbers with the current MOI figures (I did not verify the numbers; could not reach ris.gov.tw).
- en: same, book_en/chapters/notebooks/08_spatial_choropleth.ipynb:74 ("Approximate county populations (2023 estimates, in people)").
- severity: medium

### 6. Rule-of-thumb "10-15 events per predictor" presented as current guidance
- book/chapters/06_logistic_regression.md:825 "經驗法則：每個 predictor 至少需要 10-15 個 events"
- Why dated: EPV rules have been superseded by sample-size calculations based on expected shrinkage/precision (Riley et al., BMJ 2020;368:m441, "Calculating the sample size required for developing a clinical prediction model"; van Smeden et al. 2019 show EPV is not a valid criterion). Also, the point here is estimating associations in an outbreak (not prediction), where the concern is separation/sparse data (see item 1). Note: "280 筆" has 121 events, i.e. ~8 per variable for 15 variables, so the warning is right but the justification is dated.
- Proposed zh: "經驗上變項太多會過度擬合（例如 121 個病例放 15+ 變項）。傳統『每個變項 10 個事件（EPV）』的說法已不被建議當作標準；較新的做法是依預期收縮量與估計精確度計算樣本數（Riley 2020），或改用 Firth／懲罰式迴歸。"
- en: same, book_en/chapters/06_logistic_regression.md:793.
- severity: medium

### 7. pandas 3.x: `DatetimeIndex.dayofweek` / `Timestamp.dayofyear` emit Pandas4Warning (will be removed in pandas 4)
- exercises/07_time_series_exercise.ipynb:256 `dow = dates_all.dayofweek` (also the `.dayofyear` list-comp in the data-generation cells at ~159/173/187: `np.array([d.dayofyear for d in dates_all])`), solutions/07_time_series_solution.ipynb:233 (`dayofweek`) and the same data-gen cells (~145-173).
- Evidence (pandas 3.1.1): "Pandas4Warning: Timestamp.dayofyear is deprecated and will be removed in a future version. Use Timestamp.day_of_year instead." (730 repeats per notebook because it is in a loop) and "DatetimeIndex.dayofweek is deprecated ... Use DatetimeIndex.day_of_week". Not triggered under the lock (pandas 2.3.3) but pyproject allows `pandas>=2.2.0` and Colab/`pip install -e .` can resolve pandas 3.1; 1,460 warning lines will flood student output.
- Proposed: `dates_all.day_of_week`, `d.day_of_year` (both exist in pandas >= 1.x, so safe with the pin). Also `dates_all.dayofweek` in the notebook's own Part B cells if present (checked: only exercise/solution).
- en: same issue, book_en/chapters/exercises/07_time_series_exercise.ipynb:256, book_en/chapters/solutions/07_time_series_solution.ipynb:233 and the same data-gen cells.
- severity: medium (latent under lock, certain on unpinned installs)

### 8. statsmodels 0.15: `adfuller` tuple return is deprecated
- book/chapters/07_time_series.md:551 `adf_stat, p_value, *_ = adfuller(synth)`; notebooks/07_time_series_baseline.ipynb:291; solutions/07_time_series_solution.ipynb (Q5 cell, `adfuller(daily)`).
- Evidence (statsmodels 0.15.0): "FutureWarning: adfuller currently returns a plain tuple ... In release 0.16 or after July 2027 ... the default behavior will switch to always returning an ADFullerResult. Set result_object=True to switch now, or result_object=False to keep the current behavior and silence this warning." Not shown with the locked 0.14.6, but pyproject allows >=0.14.4 and uv lock refresh will pull 0.15.
- Proposed: `adf = adfuller(synth, result_object=True); adf_stat, p_value = adf.statistic, adf.pvalue` (requires >=0.15; bump the pyproject floor) — or keep the unpack and add `result_object=False` once the floor is raised. Update the table row at :568 accordingly.
- en: same, book_en/chapters/07_time_series.md:523 and :540, and the same notebooks.
- severity: medium

## LOW

### 9. Colab setup cell uses `pip` while the project mandates uv
- All 05-09 notebooks/exercises/solutions: e.g. book/chapters/notebooks/05_stratified_analysis.ipynb:22, 06_logistic_regression.ipynb:30, 07_time_series_baseline.ipynb:30, 08_spatial_rates.ipynb:31, 08_spatial_statistics.ipynb:35, 09_survival_analysis.ipynb:31, 08_spatial_choropleth.ipynb:26 (`!pip install -q -e . pillow`), exercises/*:26-27, solutions/*:22-26: `!pip install -q -e .`
- CLAUDE.md: "uv is the sole package manager — never pip". Colab now ships uv-friendly images; `!pip install uv` is not needed since Colab preinstalls it (verify before changing).
- Proposed: `!uv pip install --system -q -e .` (if uv absent: `!pip install -q uv && uv pip install --system -q -e .`). Note pyproject `requires-python >=3.12`, `.python-version` 3.14.
- en: same in all book_en/ notebooks (1 occurrence each, same lines).
- severity: low (policy deviation; works)

### 10. Typo `|| True` (capital T) in the Colab clone line of ch06
- book/chapters/notebooks/06_logistic_regression.ipynb:28 and book/chapters/exercises/06_logistic_regression_exercise.ipynb:25: `!git clone ... 2>/dev/null || True` (all other notebooks use `|| true`). On a re-run in Colab the clone fails (dir exists) and `True: command not found` is printed/returned non-zero.
- Proposed: `|| true`.
- en: same at book_en/chapters/notebooks/06_logistic_regression.ipynb:28 and book_en/chapters/exercises/06_logistic_regression_exercise.ipynb:25.
- severity: low

## Checked, no finding (for the record)
- Zero cell errors in ch05-09 (notebooks, exercises, solutions) on both locked and latest libs; no `resample('M')`/`freq='M'`/`applymap`/`inplace`/`fillna(method=)`/`geopandas.datasets`/`mapbox` uses in these chapters; ch07 uses `asfreq("D")`/`freq="D"` only. lifelines/prophet internal Pandas4Warnings (`utcnow`, positional `sum(0)`, `inplace=`) come from the libraries (lifelines 0.30.3 latest), not from book code.
- No named AI tools/models, "latest/recently" claims, or story dates clashing with 2026-11-11 (outbreak 2026-01, synthetic series 2025-10..2026-04 are all in the past). Exercise 07 Q9 holiday list (元旦/清明 2026) is past and fine.
- External data URLs (od.cdc.gov.tw/eic/Age_County_Gender_4828.csv, maps.nlsc.gov.tw/download/縣市界線(TWD97經緯度).zip, 08_spatial.md:376-377) and YouTube IDs: could not verify (proxy 403). github.com/ancientsky/python4epi returns 200.
- Chapter 05/09 epi content (Mantel-Haenszel, Breslow-Day, 10% change-in-estimate, KM/log-rank/Cox) not superseded.
