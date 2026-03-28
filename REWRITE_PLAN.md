# 全書改寫規劃：以松柏護理之家退伍軍人症群聚事件為主軸

> **目標**：將全書從「無聊的 10 筆假資料」轉型為「一場完整的退伍軍人症群聚調查」。
> 所有章節共享同一個故事線與資料集，每一章帶領學員更深入一層分析，
> 就像真實疫調一樣逐步揭開真相。

---

## 一、現況診斷

### 學員反饋的核心問題

| 問題 | 原因 |
|------|------|
| 太無趣、讀不下去 | 10 筆假資料毫無沉浸感，無法產生「想知道答案」的動機 |
| 章節之間斷裂 | 每章各自舉例，缺乏貫穿全書的主軸故事 |
| 分析深度不足 | 只有簡單 2×2，缺少分層分析、邏輯斯迴歸、存活分析等流病核心技能 |
| 從統計直接跳 ML | Ch03（卡方）→ Ch07（sklearn）中間缺乏邏輯斯迴歸的橋樑 |

### 現有章節盤點（15 章 + 13 notebook + 11 exercise/solution 對）

| 編號 | 現有主題 | 現有資料 | 評估 |
|------|---------|---------|------|
| 00 | 導讀與工具 | 無 | **微調** — 加入 Legionella 情境預告 |
| 01 | Python 基礎 | 手寫數字 | **改寫** — 用群聚事件數字當範例 |
| 02 | 資料處理與視覺化 | line_list.csv (10 筆) | **全面改寫** — 讀入 280 筆 Legionella line list |
| 03 | 描述與推論統計 | line_list.csv (10 筆) | **全面改寫** — shower_use 2×2 + 卡方 |
| 04 | 爆發調查工作流 | line_list.csv (10 筆) | **全面改寫** — 完整 Legionella SitRep |
| 05 | 時間序列 | line_list.csv (10 筆) | **改寫** — 每日發病數時間序列 |
| 06 | 空間流病 | line_list + GeoJSON | **改寫** — 樓層翼區 spot map + 保留 choropleth 概念 |
| 07 | 機器學習 | line_list.csv (10 筆) | **全面改寫** — 32 欄豐富特徵 |
| 08 | 深度學習 | line_list.csv (10 筆) | **全面改寫** — 同上 |
| 09 | 因果推論 | 合成 panel data | **改寫** — DAG + 干擾因子實例 |
| 10 | 可重現研究 | line_list.csv | **更新** — 改用 Legionella 工作流 |
| 11 | 實戰案例 | 登革熱情境 | **全面改寫** — Legionella 疫調總整合 |
| 12 | 附錄 | — | **更新** — 新增 Legionella 術語 |
| 13 | 作業區 | 11 exercises | **全面更新** — 配合各章改寫 |
| 14 | 解答區 | 11 solutions | **全面更新** — 配合各章改寫 |

### 現有章節的重大缺口

| 缺口 | 重要性 | Legionella 資料集支援度 |
|------|--------|----------------------|
| **分層分析與干擾因子** | ★★★ 流行病學核心技能 | `functional_status` → `shower_use` → `infected` 完美示範 |
| **邏輯斯迴歸** | ★★★ 從卡方到 ML 的必要橋樑 | 多個二元危險因子，crude/adjusted OR |
| **存活分析** | ★★☆ 臨床流病常用 | `symptom_onset_date` → `death_date` 可算存活時間 |

---

## 二、新章節架構（18 章）

### 總覽：故事線驅動的章節編排

```
【第一幕：接獲通報】
  Ch00  導讀 — 週五下午四點，你接到電話⋯⋯
  Ch01  Python 基礎 — 先學會算侵襲率和致死率
  Ch02  資料處理與視覺化 — 拿到 280 筆 line list，開始整理

【第二幕：描述性分析】
  Ch03  描述性統計與 2×2 表 — 誰生病了？淋浴是不是危險因子？
  Ch04  群聚調查工作流 — 產出第一份 SitRep 給長官

【第三幕：深入分析】
  Ch05  分層分析與干擾因子 [新增] — 臥床老人不淋浴也不生病，是真的保護還是干擾？
  Ch06  邏輯斯迴歸 [新增] — 同時調整年齡、共病、暴露，算出 adjusted OR
  Ch07  時間序列與預測 — 預測未來一週還會有多少新個案？
  Ch08  空間流病 — 哪個樓層翼區最危險？畫出 spot map

【第四幕：進階建模】
  Ch09  存活分析 [新增] — 發病到死亡的時間，哪些因子影響存活？
  Ch10  機器學習 — 用全部 32 欄特徵預測感染 / 重症
  Ch11  深度學習 — PyTorch 版本的預測模型
  Ch12  因果推論 — 淋浴暴露的因果效應，DAG 怎麼畫？

【第五幕：收尾與實戰】
  Ch13  可重現研究 — 讓同事能一鍵重現你的分析
  Ch14  實戰案例 — 從接到通報到結案報告，完整走一遍
  Ch15  附錄
  Ch16  作業區
  Ch17  解答區（講師版）
```

### 對照表：舊編號 → 新編號

| 新編號 | 主題 | 來源 | 變動程度 |
|--------|------|------|---------|
| 00 | 導讀與工具 | 原 Ch00 | 🟡 微調 |
| 01 | Python 基礎 | 原 Ch01 | 🟠 改寫範例 |
| 02 | 資料處理與視覺化 | 原 Ch02 | 🔴 全面改寫 |
| 03 | 描述性統計與 2×2 表 | 原 Ch03 | 🔴 全面改寫 |
| 04 | 群聚調查工作流 | 原 Ch04 | 🔴 全面改寫 |
| **05** | **分層分析與干擾因子** | **🆕 新增** | 🟣 全新 |
| **06** | **邏輯斯迴歸** | **🆕 新增** | 🟣 全新 |
| 07 | 時間序列與預測 | 原 Ch05 | 🟠 改寫 |
| 08 | 空間流病 | 原 Ch06 | 🟠 改寫 |
| **09** | **存活分析** | **🆕 新增** | 🟣 全新 |
| 10 | 機器學習 | 原 Ch07 | 🔴 全面改寫 |
| 11 | 深度學習 | 原 Ch08 | 🔴 全面改寫 |
| 12 | 因果推論 | 原 Ch09 | 🟠 改寫 |
| 13 | 可重現研究 | 原 Ch10 | 🟡 更新 |
| 14 | 實戰案例 | 原 Ch11 | 🔴 全面改寫 |
| 15 | 附錄 | 原 Ch12 | 🟡 更新 |
| 16 | 作業區 | 原 Ch13 | 🔴 全面更新 |
| 17 | 解答區（講師版） | 原 Ch14 | 🔴 全面更新 |

---

## 三、各章改寫詳細規劃

---

### Ch00 導讀與工具 `00_guide.md`
**變動：🟡 微調**

| 項目 | 說明 |
|------|------|
| 改動範圍 | 將開場情境從「食物中毒群聚」換成「退伍軍人症群聚」 |
| 故事線 | 「週五下午四點，你接到衛生局的電話：某護理之家有多名住民出現肺炎症狀⋯⋯」 |
| 工具部分 | 維持不變（uv、Jupyter Lab、Git 介紹） |
| Notebook | 無（本章為純 markdown） |
| Exercise | 無 |

**改寫要點：**
- 將 `cases = 125, population = 2450` 等食物中毒範例數字替換為 Legionella 情境
- 保留其餘工具安裝、環境設定等內容

---

### Ch01 Python 基礎 `01_fundamentals.md`
**變動：🟠 改寫範例**

| 項目 | 說明 |
|------|------|
| 教學目標 | 不變：變數、型態、條件判斷、函數、字典 |
| 改動 | 所有範例數字換成 Legionella 群聚數據 |
| Notebook | `01_fundamentals_python_basics.ipynb` — 改寫 |
| Exercise | `01_fundamentals_exercise.ipynb` — 改寫 |

**範例替換對照：**

| 原範例 | 新範例 |
|--------|--------|
| `cases = 125, population = 2450` | `total_residents = 280, infected = 121, confirmed = 89` |
| `attack_rate = cases / population` | `attack_rate = infected / total_residents` |
| `deaths = 4` | `deaths = 19, hospitalized = 68, icu = 23` |
| `report = {"cases": 125, ...}` | `report = {"facility": "松柏護理之家", "total_residents": 280, "infected": 121, "confirmed": 89, "deaths": 19}` |
| 閾值判斷 `> 0.05` | `if cfr > 0.10: print("致死率偏高，需啟動加強監測")` |

---

### Ch02 資料處理與視覺化 `02_data_wrangling.md`
**變動：🔴 全面改寫**

| 項目 | 說明 |
|------|------|
| 教學目標 | pandas 讀取、日期轉換、groupby、5 種流病圖表 |
| 資料來源 | `legionella_outbreak.csv`（取代 `line_list.csv`） |
| Notebook 1 | `02_data_wrangling_for_beginners.ipynb` — 全面改寫 |
| Notebook 2 | `02_visualization_epi_charts.ipynb` — 全面改寫 |
| Exercise | `02_data_wrangling_exercise.ipynb` — 全面改寫 |

**Notebook 1 改寫內容（資料處理）：**

```
1. 讀入 legionella_outbreak.csv（280 筆 × 32 欄）
2. 檢視資料結構：df.info(), df.describe(), df.head()
3. 日期轉換：5 個日期欄位 → pd.to_datetime()
4. 建立衍生變項：
   - age_group（60-69 / 70-79 / 80-89 / 90+）
   - n_comorbidities（共病數加總）
   - onset_to_hosp_days（發病到住院天數）
   - epi_week（流行病學週）
   - infected（二元：clinical_severity != 'not_ill'）
5. 處理遺漏值：未感染者的日期欄位為空值
6. groupby 練習：按 floor × wing 計算侵襲率
```

**Notebook 2 改寫內容（視覺化）：**

| 圖表 | 使用欄位 | 教學重點 |
|------|---------|---------|
| 流行曲線 (epi curve) | `symptom_onset_date` | 辨識共同暴露源型態 |
| 年齡分布直方圖 | `age`（感染 vs 未感染） | 年齡是否為危險因子 |
| 樓層翼區侵襲率長條圖 | `floor`, `wing`, `infected` | 地點關聯初探 |
| 嚴重度 × 共病熱力圖 | `clinical_severity`, comorbidities | 多因子視覺化 |
| 互動式時間趨勢 (Plotly) | `symptom_onset_date` by `floor` | 分組比較流行曲線 |

---

### Ch03 描述性統計與 2×2 表 `03_stats.md`
**變動：🔴 全面改寫**

| 項目 | 說明 |
|------|------|
| 教學目標 | 2×2 列聯表、風險比 (RR)、卡方檢定、信賴區間 |
| Notebook | `03_stats_basics.ipynb` — 全面改寫 |
| Exercise | `03_stats_exercise.ipynb` — 全面改寫 |

**Notebook 改寫內容：**

```
1. 定義「個案」：clinical_severity != 'not_ill' → infected = 1
2. 建立 2×2 表：shower_use × infected
   ┌─────────────┬──────────┬────────────┐
   │             │ Infected │ Not infected│
   ├─────────────┼──────────┼────────────┤
   │ Shower user │    76    │     72     │
   │ Non-user    │    45    │     87     │
   └─────────────┴──────────┴────────────┘
3. 計算 Risk Ratio：RR = (76/148) / (45/132)
4. 計算 95% 信賴區間
5. 卡方檢定：scipy.stats.chi2_contingency()
6. 第二個 2×2：hydrotherapy_use × infected
7. 多個危險因子的粗 RR 彙整表（一次看所有因子）
```

**Exercise 設計：**
- 練習：建立 `comorbidity_copd × infected` 的 2×2 表，計算 RR 和卡方
- 進階：計算各共病的 RR 並排序，哪個共病關聯最強？

---

### Ch04 群聚調查工作流 `04_outbreak_workflow.md`
**變動：🔴 全面改寫**

| 項目 | 說明 |
|------|------|
| 教學目標 | 從原始 line list 產出完整 SitRep |
| Notebook | `04_outbreak_workflow.ipynb` — 全面改寫 |
| Exercise | `04_outbreak_workflow_exercise.ipynb` — 全面改寫 |

**Notebook 改寫內容：**

```
完整模擬一份疫情調查日報（SitRep）產出流程：

1. 讀取與清理 line list
2. 描述性流行病學三要素：
   【人】年齡中位數、性別比、共病分布
   【時】流行曲線 + 流行期間
   【地】按樓層翼區的侵襲率表格
3. 關鍵指標計算：
   - 整體侵襲率：121/280 = 43.2%
   - 致死率 (CFR)：19/121 = 15.7%
   - 住院率：68/121 = 56.2%
   - ICU 率：23/68 = 33.8%
4. 按確診 / 可能 / 非個案分層摘要
5. 輸出結構化 SitRep（含表格 + 圖表）
```

**故事推進：** 你的長官要求在兩小時內交出第一份 SitRep，內容要包含「多少人感染」「哪裡最嚴重」「致死率多少」——這一章教你如何用 Python 自動化產出。

---

### Ch05 分層分析與干擾因子 `05_stratified.md` 🆕
**變動：🟣 全新章節**

| 項目 | 說明 |
|------|------|
| 教學目標 | 干擾因子概念、分層分析、Mantel-Haenszel 法 |
| 新 Notebook | `05_stratified_analysis.ipynb` |
| 新 Exercise | `05_stratified_exercise.ipynb` |

**Notebook 內容設計：**

```
核心問題：Ch03 發現「淋浴使用者侵襲率較高」——但會不會是
因為臥床老人本來就不淋浴、也比較不容易被感染（接觸少）？

1. 回顧 Ch03 的粗 RR：shower_use → infected
2. 觀察干擾因子嫌疑人：
   - functional_status 與 shower_use 的關聯（臥床者僅 5% 淋浴）
   - functional_status 與 infected 的關聯（臥床者暴露機會低）
3. DAG（有向無環圖）概念介紹：
   functional_status → shower_use → infected
   functional_status ─────────────→ infected
4. 分層分析實作：
   - 按 functional_status 分三層，各層計算 shower_use 的 RR
   - 視覺化：各層 RR 的森林圖（forest plot）
5. Mantel-Haenszel 加權 RR：
   - 手算步驟 + scipy/statsmodels 函數
   - 比較 crude RR vs. adjusted RR_MH
6. 交互作用檢定（homogeneity test）
7. 第二個範例：按 floor 分層分析 shower_use
```

**為什麼需要這一章：**
- 干擾因子是流行病學最核心的概念之一
- 從 2×2（Ch03）到邏輯斯迴歸（Ch06）的關鍵橋樑
- Legionella 資料的 `functional_status → shower_use → infected` 路徑是教科書級的干擾範例

---

### Ch06 邏輯斯迴歸 `06_logistic_regression.md` 🆕
**變動：🟣 全新章節**

| 項目 | 說明 |
|------|------|
| 教學目標 | 邏輯斯迴歸、crude OR、adjusted OR、模型解讀 |
| 新 Notebook | `06_logistic_regression.ipynb` |
| 新 Exercise | `06_logistic_regression_exercise.ipynb` |

**Notebook 內容設計：**

```
核心問題：在同時考慮多個危險因子後，淋浴使用是否仍為顯著危險因子？

1. 為什麼需要多變項分析？（Ch05 的分層分析一次只能控制一個變項）
2. 邏輯斯迴歸原理（簡明版）：
   - log(odds) = β₀ + β₁x₁ + β₂x₂ + ...
   - OR = exp(β)
   - OR 的解讀方式
3. 單變項（crude）邏輯斯迴歸：
   - 逐一對 shower_use, age, sex, 各共病 算 crude OR
   - 彙整成表格：變項 / crude OR / 95% CI / p-value
4. 多變項（adjusted）邏輯斯迴歸：
   - 模型：infected ~ shower_use + age + sex + 所有共病 + floor + wing
   - statsmodels 實作：sm.Logit() 或 smf.logit()
   - 解讀 adjusted OR 表格
   - 比較 crude vs. adjusted OR（淋浴效應是否仍在？）
5. 模型診斷：
   - AIC / BIC 比較
   - 變項選擇策略（流行病學驅動 vs. 統計驅動）
6. 結果呈現：標準的 Table 2 格式
```

**為什麼需要這一章：**
- 邏輯斯迴歸是流行病學論文最常見的分析方法
- 填補 Ch03（卡方）到 Ch10（sklearn ML）的巨大鴻溝
- 學員學完 statsmodels 後轉 sklearn 會更順暢

---

### Ch07 時間序列與預測 `07_time_series.md`
**變動：🟠 改寫**（原 Ch05）

| 項目 | 說明 |
|------|------|
| 教學目標 | 不變：日別時間序列、滾動平均預測、MAE |
| Notebook | `07_time_series_baseline.ipynb` — 改寫 |
| Exercise | `07_time_series_exercise.ipynb` — 改寫 |

**Notebook 改寫內容：**

```
1. 從 symptom_onset_date 建立每日發病數序列
2. 補齊無發病日（fill_value=0）
3. 流行曲線 + 7 日滾動平均疊圖
4. 預測：用 3 日滾動平均預測次日發病數
5. MAE 評估
6. 情境延伸：預測下週住院床位需求
   - 用 hospitalization_date 建立每日住院數
   - 對比發病曲線 vs 住院曲線（lag 效應）
```

**故事推進：** 長官問你「下禮拜還會有多少人發病？醫院夠不夠床位？」

---

### Ch08 空間流病 `08_spatial.md`
**變動：🟠 改寫**（原 Ch06）

| 項目 | 說明 |
|------|------|
| 教學目標 | 空間分布視覺化、高風險區域辨識 |
| Notebook 1 | `08_spatial_rates.ipynb` — 改寫 |
| Notebook 2 | `08_spatial_choropleth.ipynb` — 改寫 |
| Exercise | `08_spatial_exercise.ipynb` — 改寫 |

**Notebook 1 改寫內容（樓層翼區侵襲率）：**

```
1. 按 floor × wing 計算侵襲率
2. 樓層翼區的侵襲率熱力圖（heatmap）
3. 按 room 計算每間房的侵襲率
4. 識別高風險區域：2F-B 翼、3F-B 翼
5. 與汙染水源位置的對應關係
```

**Notebook 2 改寫內容（建築 spot map）：**

```
1. 用 matplotlib 繪製護理之家樓層平面圖（spot map）
   - 3 層 × 2 翼的格狀圖
   - 每個房間用圓點標記（大小 = 住民數，顏色 = 侵襲率）
2. Plotly 互動版本
3. 保留 choropleth 概念教學（用 admin_areas.geojson 示範地理 choropleth 的原理）
```

**故事推進：** 你畫出 spot map 後，發現 2 樓和 3 樓 B 翼明顯偏高——你開始懷疑水源系統。

---

### Ch09 存活分析 `09_survival.md` 🆕
**變動：🟣 全新章節**

| 項目 | 說明 |
|------|------|
| 教學目標 | Kaplan-Meier 存活曲線、Log-rank 檢定、Cox 迴歸 |
| 新 Notebook | `09_survival_analysis.ipynb` |
| 新 Exercise | `09_survival_exercise.ipynb` |

**Notebook 內容設計：**

```
核心問題：發病後，哪些因子影響存活？

1. 存活分析基本概念：
   - 存活時間 = death_date - symptom_onset_date（設限 = survived）
   - 設限資料（censored data）的概念
2. 建立分析資料集：
   - 限定有症狀的個案（排除 asymptomatic、not_ill）
   - 計算 time_to_event（天數）
   - event 指標（1=dead, 0=survived/censored at investigation date）
3. Kaplan-Meier 存活曲線：
   - lifelines 套件：KaplanMeierFitter
   - 全體存活曲線
   - 按嚴重度分組的存活曲線（severe vs moderate vs mild）
   - 按 COPD 有無分組的存活曲線
4. Log-rank 檢定：
   - 比較兩組存活曲線是否有顯著差異
5. Cox 比例風險迴歸：
   - CoxPHFitter()
   - 變項：age, sex, 各共病, severity
   - 解讀 HR（hazard ratio）
   - 森林圖（forest plot）呈現各因子的 HR
6. 模型診斷：比例風險假設檢定
```

**為什麼需要這一章：**
- 存活分析是臨床流行病學的核心方法
- Legionella 資料有完整的 onset → death 時間，天然適合
- `lifelines` 套件語法簡潔，適合教學

**套件需求：** 需在 `pyproject.toml` 加入 `lifelines`

---

### Ch10 機器學習 `10_machine_learning.md`
**變動：🔴 全面改寫**（原 Ch07）

| 項目 | 說明 |
|------|------|
| 教學目標 | sklearn pipeline、特徵工程、分類模型、AUC 評估 |
| Notebook | `10_ml_baseline.ipynb` — 全面改寫 |
| Exercise | `10_ml_exercise.ipynb` — 全面改寫 |

**Notebook 改寫內容：**

```
核心問題：能否從住民的基本資料預測誰會感染 / 誰會變重症？

1. 問題定義：
   - 任務 A：預測 infected（是否感染）
   - 任務 B：預測 severe_outcome（住院或死亡）
2. 特徵工程：
   - 數值特徵：age, n_comorbidities
   - 類別特徵：sex, smoking_history, functional_status, floor, wing
   - 二元特徵：各 comorbidity, shower_use, hydrotherapy_use
3. sklearn Pipeline：
   - ColumnTransformer（StandardScaler + OneHotEncoder）
   - LogisticRegression 作為 baseline
   - RandomForestClassifier 作為進階
4. 交叉驗證 + AUC 評估
5. 特徵重要性排序（permutation importance）
6. 比較：Ch06 邏輯斯迴歸 OR vs. sklearn 特徵重要性
```

---

### Ch11 深度學習 `11_deep_learning.md`
**變動：🔴 全面改寫**（原 Ch08）

| 項目 | 說明 |
|------|------|
| 教學目標 | PyTorch 二元分類、訓練迴圈、早停法 |
| Notebook | `11_dl_baseline.ipynb` — 全面改寫 |
| Exercise | `11_dl_exercise.ipynb` — 全面改寫 |

**Notebook 改寫內容：**

```
1. 資料前處理（與 Ch10 同源，但手動處理 tensor）
2. 架構：input_dim → 32 → 16 → 1 (sigmoid)
3. 訓練迴圈 + 驗證集監控
4. 與 Ch10 sklearn 結果比較：
   - 「280 筆資料用 DL 是否過殺？」的討論
   - 讓學員思考何時該用/不該用 DL
```

---

### Ch12 因果推論 `12_causal.md`
**變動：🟠 改寫**（原 Ch09）

| 項目 | 說明 |
|------|------|
| 教學目標 | DAG、因果效應 vs. 關聯、DiD（保留）、反事實概念 |
| Notebook | `12_causal_did.ipynb` — 改寫 |
| Exercise | `12_causal_exercise.ipynb` — 改寫 |

**Notebook 改寫內容：**

```
1. DAG 實作（Legionella 情境）：
   - 用 graphviz/networkx 畫出：
     floor_wing → water_contamination → shower_aerosol → infection
     functional_status → shower_use → infection
     age → comorbidities → severity → death
   - 辨識干擾路徑、中介變項、碰撞因子
2. 反事實思考：
   - 「如果所有住民都不淋浴，會減少多少感染？」
   - Attributable Risk 與 Population Attributable Risk
3. DiD 保留（改寫情境）：
   - 情境：1 月 25 日實施水系統消毒，比較前後病例數
   - 介入組：2-3 樓 B 翼（汙染源附近）
   - 對照組：1 樓（不同水源）
   - OLS 迴歸：cases ~ treated + post + treated:post
```

---

### Ch13 可重現研究 `13_reproducibility.md`
**變動：🟡 更新**（原 Ch10）

| 項目 | 說明 |
|------|------|
| Notebook | `13_reproducibility_workflow.ipynb` — 更新資料路徑 |
| 改動 | 將範例從 line_list.csv 改為 legionella_outbreak.csv |

---

### Ch14 實戰案例 `14_case_studies.md`
**變動：🔴 全面改寫**（原 Ch11）

| 項目 | 說明 |
|------|------|
| Notebook | `14_case_study_legionella.ipynb` — 全面改寫 |
| Exercise | `14_case_study_exercise.ipynb` — 全面改寫 |

**Notebook 改寫內容：**

```
模擬完整的疫情調查報告（Outbreak Investigation Report）：

1. 背景：接到通報 → 啟動調查
2. 方法：個案定義、資料收集
3. 結果：
   a. 描述性流行病學（Ch02–04 技能整合）
   b. 分析性流行病學（Ch03, 05, 06 技能整合）
   c. 時間空間分析（Ch07, 08 技能整合）
4. 討論：感染源研判、介入措施建議
5. 結論：關閉水系統、消毒、持續監測
6. 附錄：完整程式碼 + 圖表

目標：學員完成後能產出一份近似真實的疫調報告
```

---

### Ch15 附錄 `15_appendix.md`
**變動：🟡 更新**（原 Ch12）

- 新增退伍軍人症相關術語
- 新增 `lifelines` 套件說明（存活分析）
- 更新資料集欄位對照表

---

### Ch16 作業區 `16_exercises.md` + Ch17 解答區 `17_solutions.md`
**變動：🔴 全面更新**（原 Ch13 + Ch14）

新增 3 個 exercise/solution 對（Ch05, Ch06, Ch09），更新 11 個既有的。
共 **14 組** exercise + solution。

---

## 四、檔案異動清單

### 需要重新命名的檔案（舊編號 → 新編號）

| 類型 | 舊檔名 | 新檔名 |
|------|--------|--------|
| chapter md | `05_time_series.md` | `07_time_series.md` |
| chapter md | `06_spatial.md` | `08_spatial.md` |
| chapter md | `07_machine_learning.md` | `10_machine_learning.md` |
| chapter md | `08_deep_learning.md` | `11_deep_learning.md` |
| chapter md | `09_causal.md` | `12_causal.md` |
| chapter md | `10_reproducibility.md` | `13_reproducibility.md` |
| chapter md | `11_case_studies.md` | `14_case_studies.md` |
| chapter md | `12_appendix.md` | `15_appendix.md` |
| chapter md | `13_exercises.md` | `16_exercises.md` |
| chapter md | `14_solutions.md` | `17_solutions.md` |
| notebooks | 對應的 .ipynb 全部重新編號 | （同上邏輯） |

### 需要新建的檔案

| 類型 | 檔名 |
|------|------|
| chapter md | `05_stratified.md` |
| chapter md | `06_logistic_regression.md` |
| chapter md | `09_survival.md` |
| notebook | `05_stratified_analysis.ipynb` |
| notebook | `06_logistic_regression.ipynb` |
| notebook | `09_survival_analysis.ipynb` |
| exercise | `05_stratified_exercise.ipynb` |
| exercise | `06_logistic_regression_exercise.ipynb` |
| exercise | `09_survival_exercise.ipynb` |
| solution | `05_stratified_solution.ipynb` |
| solution | `06_logistic_regression_solution.ipynb` |
| solution | `09_survival_solution.ipynb` |

### 需要更新的配置檔

| 檔案 | 改動 |
|------|------|
| `book/_toc_student.yml` | 新增 3 章、重新編號 |
| `book/_toc_instructor.yml` | 同上 + solution 區更新 |
| `pyproject.toml` | 加入 `lifelines` 依賴 |
| `tests/test_notebook_smoke.py` | 更新 notebook 路徑 |

---

## 五、執行順序與里程碑

> **原則：每完成一章 → commit & push → 等待 merge → 再做下一章**

### Phase 0：基礎設施（先做一次）

| 步驟 | 工作內容 |
|------|---------|
| 0-1 | 將所有舊編號檔案 rename 為新編號 |
| 0-2 | 建立 3 個新章節的空白 md + notebook 骨架 |
| 0-3 | 更新 `_toc_student.yml` 和 `_toc_instructor.yml` |
| 0-4 | 在 `pyproject.toml` 加入 `lifelines` |
| 0-5 | 更新 smoke tests |
| 0-6 | 確認 `uv run pytest` 通過 |

### Phase 1：基礎章節（Ch00–Ch02）

| 步驟 | 章節 | 預估工作量 |
|------|------|-----------|
| 1-1 | Ch00 導讀 — 微調開場情境 | 小 |
| 1-2 | Ch01 Python 基礎 — 改寫範例數字 + notebook + exercise | 中 |
| 1-3 | Ch02 資料處理與視覺化 — 全面改寫 2 notebooks + exercise | 大 |

### Phase 2：核心分析（Ch03–Ch06）

| 步驟 | 章節 | 預估工作量 |
|------|------|-----------|
| 2-1 | Ch03 描述性統計與 2×2 表 — 全面改寫 | 大 |
| 2-2 | Ch04 群聚調查工作流 — 全面改寫 | 大 |
| 2-3 | Ch05 分層分析與干擾因子 — 🆕 全新 | 大 |
| 2-4 | Ch06 邏輯斯迴歸 — 🆕 全新 | 大 |

### Phase 3：進階方法（Ch07–Ch12）

| 步驟 | 章節 | 預估工作量 |
|------|------|-----------|
| 3-1 | Ch07 時間序列與預測 — 改寫 | 中 |
| 3-2 | Ch08 空間流病 — 改寫 | 大 |
| 3-3 | Ch09 存活分析 — 🆕 全新 | 大 |
| 3-4 | Ch10 機器學習 — 全面改寫 | 大 |
| 3-5 | Ch11 深度學習 — 全面改寫 | 中 |
| 3-6 | Ch12 因果推論 — 改寫 | 大 |

### Phase 4：收尾（Ch13–Ch17）

| 步驟 | 章節 | 預估工作量 |
|------|------|-----------|
| 4-1 | Ch13 可重現研究 — 更新 | 小 |
| 4-2 | Ch14 實戰案例 — 全面改寫 | 大 |
| 4-3 | Ch15 附錄 — 更新 | 小 |
| 4-4 | Ch16 作業區 — 更新所有 14 exercises | 大 |
| 4-5 | Ch17 解答區 — 更新所有 14 solutions | 大 |

### Phase 5：最終驗證

| 步驟 | 工作內容 |
|------|---------|
| 5-1 | `uv run pytest` 全部通過 |
| 5-2 | `uv run jupyter-book build book/` 成功建置 |
| 5-3 | 全書敘事連貫性檢查 |

---

## 六、注意事項

### 向下相容
- 原有的 `data/synthetic/line_list.csv` 保留不刪（避免影響其他可能的引用）
- 原有的 `src/epi_learning/` 函數保持不變，僅視需要新增函數

### 需要新增的 `epi_learning` 函數（暫定）
- `odds_ratio()` — 計算 OR 和 95% CI（Ch06 需要）
- `mantel_haenszel()` — MH 加權 RR/OR（Ch05 需要）
- `plot_spot_map()` — 建築平面圖視覺化（Ch08 需要）

### Notebook 標準結構
每個 notebook 開頭均保持標準的 Colab setup cell：
```python
# Colab 環境自動設定（本機執行時會自動跳過）
try:
    import google.colab
    !git clone https://github.com/ancientsky/python4epi.git /content/python4epi
    %cd /content/python4epi
    !pip install -e .
except ImportError:
    pass
```

### Exercise 設計原則
- 每個 exercise 至少包含 3 題：基礎題、應用題、挑戰題
- 所有題目均使用 `legionella_outbreak.csv`
- 題目銜接該章主題，但要求學員自行探索不同的變項組合
