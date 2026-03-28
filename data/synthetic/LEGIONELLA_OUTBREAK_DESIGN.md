# 松柏護理之家退伍軍人症群聚事件 — 合成資料集設計文件

> **檔案位置**
> - 資料集：`data/synthetic/legionella_outbreak.csv`
> - 生成腳本：`data/synthetic/generate_legionella_outbreak.py`
> - 本文件：`data/synthetic/LEGIONELLA_OUTBREAK_DESIGN.md`

---

## 1. 情境設定 (Scenario)

### 1.1 機構背景

| 項目 | 設定 |
|------|------|
| 機構名稱 | 松柏護理之家（Songbai Nursing Home） |
| 住民人數 | 約 280 人 |
| 建築結構 | 3 層樓，每層 2 翼區（A 翼 / B 翼） |
| 每翼房間數 | 25 間（編號 01–25） |
| 每房床位 | 2 床（雙人房為主） |
| 總床位數 | 3 × 2 × 25 × 2 = 300 床（非滿床營運） |

### 1.2 群聚事件摘要

2026 年 1 月，松柏護理之家爆發一起退伍軍人症（Legionnaires' disease）群聚事件。經流行病學調查（疫調）及環境採檢，確認感染源為供應 **2 樓及 3 樓 B 翼**的中央熱水系統，遭受 *Legionella pneumophila* 血清型 1 汙染。住民透過 **淋浴**（主要暴露途徑）及 **水療池**（次要暴露途徑）吸入受汙染的氣溶膠（aerosol）而感染。

### 1.3 疾病特性（退伍軍人症）

| 項目 | 說明 |
|------|------|
| 病原體 | *Legionella pneumophila* serogroup 1 |
| 傳播途徑 | 吸入受汙染水源產生的氣溶膠（**非**人傳人） |
| 潛伏期 | 2–10 天（中位數 5–6 天） |
| 主要症狀 | 發燒、咳嗽、呼吸困難、意識混亂、腹瀉 |
| 高風險族群 | 年長者、吸菸者、慢性肺病、免疫抑制、糖尿病、癌症 |
| 確認方法 | 尿液抗原檢測（urinary antigen）、培養、PCR |
| 致死率 | 一般 5–30%，護理之家族群偏高 |

### 1.4 時間軸

| 時間點 | 日期 | 說明 |
|--------|------|------|
| 暴露開始 | 2026-01-10 | 最早可能暴露日（水系統汙染推估） |
| 流行高峰 | 2026-01-20 | 發病數最多的時段 |
| 最後發病日 | 2026-02-05 | 最晚的發病日（介入措施後漸緩） |
| 調查截止日 | 2026-02-10 | 資料凍結日（data freeze） |

---

## 2. 欄位定義 (Data Dictionary)

### 2.1 人口學與機構資訊

| 欄位名稱 | 中文說明 | 型態 | 值域 / 範例 |
|----------|---------|------|------------|
| `case_id` | 住民編號 | str | `R001`–`R280` |
| `age` | 年齡 | int | 60–98 |
| `sex` | 性別 | str | `M` / `F` |
| `floor` | 樓層 | int | 1 / 2 / 3 |
| `wing` | 翼區 | str | `A` / `B` |
| `room` | 房號 | str | `2B-14`（樓層+翼區-房號） |
| `bed` | 床位 | int | 1 / 2 |
| `facility_admission_date` | 入住護理之家日期 | date | `2018-05-01` |

### 2.2 共病與宿主因子

| 欄位名稱 | 中文說明 | 型態 | 值域 |
|----------|---------|------|------|
| `comorbidity_chf` | 充血性心衰竭 | int | 0 / 1 |
| `comorbidity_dm` | 糖尿病 | int | 0 / 1 |
| `comorbidity_cancer` | 癌症 | int | 0 / 1 |
| `comorbidity_copd` | 慢性阻塞性肺病 | int | 0 / 1 |
| `immunosuppressed` | 免疫抑制狀態 | int | 0 / 1 |
| `smoking_history` | 吸菸史 | str | `never` / `former` / `current` |
| `functional_status` | 功能狀態 | str | `independent` / `assisted` / `bedridden` |

### 2.3 暴露因子

| 欄位名稱 | 中文說明 | 型態 | 值域 | 設計意義 |
|----------|---------|------|------|---------|
| `shower_use` | 使用淋浴 | int | 0 / 1 | **主要暴露途徑**：直接吸入氣溶膠 |
| `hydrotherapy_use` | 使用水療池 | int | 0 / 1 | **次要暴露途徑**：間接氣溶膠接觸 |

> **注意**：`shower_use` 與 `functional_status` 有關聯——臥床住民幾乎不使用淋浴（改以擦澡），這是一個潛在的干擾因子（confounder），適合教分層分析。

### 2.4 臨床資訊

| 欄位名稱 | 中文說明 | 型態 | 值域 |
|----------|---------|------|------|
| `symptom_onset_date` | 發病日（症狀出現日） | date | `2026-01-15`（未感染者為空值） |
| `fever` | 發燒 | int | 0 / 1 |
| `cough` | 咳嗽 | int | 0 / 1 |
| `dyspnea` | 呼吸困難 | int | 0 / 1 |
| `confusion` | 意識混亂 | int | 0 / 1 |
| `diarrhea` | 腹瀉 | int | 0 / 1 |
| `clinical_severity` | 臨床嚴重度 | str | `not_ill` / `asymptomatic` / `mild` / `moderate` / `severe` |
| `lab_confirmed` | 實驗室確認（尿液抗原/培養） | int | 0 / 1 |
| `case_classification` | 個案分類 | str | `confirmed` / `probable` / `not_a_case` |

### 2.5 結果與通報

| 欄位名稱 | 中文說明 | 型態 | 值域 |
|----------|---------|------|------|
| `hospitalized` | 是否住院 | int | 0 / 1 |
| `hospitalization_date` | 住院日期 | date | 發病後 1–5 天 |
| `icu_admission` | 是否入住 ICU | int | 0 / 1 |
| `outcome` | 結果 | str | `survived` / `dead` |
| `death_date` | 死亡日期 | date | 發病後 3–14 天 |
| `notification_date` | 通報日期 | date | 發病後 1–4 天 |

---

## 3. 資料生成模型 (Data Generation Model)

### 3.1 共病盛行率（護理之家基準值）

| 共病 | 盛行率 | 參考依據 |
|------|--------|---------|
| CHF | 25% | 護理之家心衰竭盛行率約 20–30% |
| DM | 35% | 老年糖尿病盛行率偏高 |
| 癌症 | 15% | 含各類型癌症 |
| COPD | 20% | 長期吸菸族群 |
| 免疫抑制 | 10% | 含類固醇長期使用、化療等 |

吸菸史分布：never 45% / former 40% / current 15%
功能狀態分布：independent 25% / assisted 50% / bedridden 25%

### 3.2 暴露機率（依功能狀態）

| 功能狀態 | 淋浴使用機率 | 水療池使用機率 |
|----------|-------------|---------------|
| independent | 90% | 30% |
| assisted | 60% | 10% |
| bedridden | 5% | 0% |

### 3.3 感染機率模型

採用**加法風險模型**，基礎感染機率 `BASE_ATTACK_PROB = 0.08`，各危險因子疊加後 clamp 至 [0.01, 0.95]：

```
P(感染) = 0.08
         + 地點加權（floor × wing）
         + 淋浴使用加權
         + 水療池使用加權
         + 共病加權
         + 宿主因子加權
```

| 危險因子 | 加權值 | 設計意義 |
|----------|--------|---------|
| 2 樓 B 翼 | +0.25 | 最接近汙染熱水器 |
| 3 樓 B 翼 | +0.20 | 次接近（管線延伸） |
| 2 樓 A 翼 | +0.10 | 同樓層但較遠 |
| 3 樓 A 翼 | +0.08 | 同上 |
| 1 樓 A/B 翼 | +0.00 | 使用不同熱水器（對照組） |
| 使用淋浴 | +0.18 | 主要氣溶膠暴露途徑 |
| 使用水療池 | +0.12 | 次要氣溶膠暴露途徑 |
| COPD | +0.10 | 肺部易受侵犯 |
| 目前吸菸 | +0.08 | 呼吸道防禦受損 |
| 曾經吸菸 | +0.04 | 殘餘效應 |
| 免疫抑制 | +0.10 | 免疫防禦下降 |
| 年齡 ≥80 | +0.06 | 老年免疫衰退 |
| CHF | +0.04 | 心肺功能差 |
| DM | +0.03 | 免疫功能受損 |
| 癌症 | +0.05 | 免疫功能受損 |

### 3.4 嚴重度模型

感染後的基礎嚴重度分布：

| 嚴重度 | 基礎機率 |
|--------|---------|
| asymptomatic | 12% |
| mild | 28% |
| moderate | 30% |
| severe | 30% |

**高風險因子會將機率質量從 asymptomatic/mild 移向 severe**：

| 因子 | 嚴重度偏移量 |
|------|-------------|
| 年齡 ≥85 | +0.12 |
| 年齡 80–84 | +0.06 |
| COPD | +0.08 |
| CHF | +0.06 |
| 免疫抑制 | +0.10 |
| 癌症 | +0.06 |

### 3.5 症狀機率（依嚴重度）

| 症狀 | asymptomatic | mild | moderate | severe |
|------|-------------|------|----------|--------|
| 發燒 | 0% | 70% | 90% | 95% |
| 咳嗽 | 0% | 50% | 70% | 85% |
| 呼吸困難 | 0% | 15% | 50% | 80% |
| 意識混亂 | 0% | 5% | 15% | 40% |
| 腹瀉 | 0% | 25% | 35% | 40% |

### 3.6 實驗室確認率

| 嚴重度 | 確認率 | 說明 |
|--------|--------|------|
| asymptomatic | 30% | 僅透過接觸者篩檢發現 |
| mild | 50% | 部分就醫後送驗 |
| moderate / severe | 85% | 住院後常規送驗 |

### 3.7 個案分類邏輯

```
if lab_confirmed → "confirmed"
elif 有症狀但未確認 → "probable"
elif 無症狀且未確認 → "not_a_case"
```

### 3.8 住院與 ICU 模型

| 嚴重度 | 住院機率 | ICU 機率（住院者中） |
|--------|---------|---------------------|
| severe | 90% | 40% |
| moderate | 45% | 0% |
| mild | 5% | 0% |
| asymptomatic | 0% | 0% |

- 住院時間：發病後 1–5 天
- ICU 僅限 severe + 已住院者

### 3.9 死亡模型

| 嚴重度 | 基礎死亡率 | 額外加權 |
|--------|-----------|---------|
| severe | 25% | 年齡≥85 +10%、CHF +5%、免疫抑制 +8% |
| moderate | 4% | 年齡≥85 +3% |
| mild | 0% | — |
| asymptomatic | 0% | — |

- 死亡時間：發病後 3–14 天

### 3.10 發病日分布

採用**三角分布（triangular distribution）**，中心為 `OUTBREAK_PEAK`（2026-01-20），前後各 10 天展開，再 clamp 至 `[OUTBREAK_START, OUTBREAK_END]`。此設計產生一個具有單一高峰的流行曲線，符合共同暴露源（common source）群聚事件的典型型態。

---

## 4. 生成結果摘要 (Dataset Summary)

> 以下為 `SEED = 42` 生成結果。

### 4.1 整體統計

| 指標 | 數值 |
|------|------|
| 住民總數 | 280 |
| 感染人數（含無症狀） | 121 (43.2%) |
| 確診個案（confirmed） | 89 |
| 可能個案（probable） | 25 |
| 非個案（not_a_case） | 166 |
| 住院人數 | 68 |
| ICU 人數 | 23 |
| 死亡人數 | 19 |
| 致死率（CFR，所有感染者） | 15.7% |

### 4.2 按樓層翼區的侵襲率

| 樓層 | 翼區 | 住民數 | 感染數 | 侵襲率 |
|------|------|--------|--------|--------|
| 1 | A | 44 | 15 | 34.1% |
| 1 | B | 47 | 10 | 21.3% |
| 2 | A | 44 | 24 | 54.5% |
| 2 | B | 50 | 25 | 50.0% |
| 3 | A | 48 | 20 | 41.7% |
| 3 | B | 47 | 27 | 57.4% |

### 4.3 按暴露因子的侵襲率

| 淋浴使用 | 住民數 | 感染數 | 侵襲率 |
|----------|--------|--------|--------|
| 否 (0) | 132 | 45 | 34.1% |
| 是 (1) | 148 | 76 | 51.4% |

### 4.4 按嚴重度的致死率

| 嚴重度 | 個案數 | 死亡數 | 致死率 |
|--------|--------|--------|--------|
| mild | 24 | 0 | 0.0% |
| moderate | 39 | 2 | 5.1% |
| severe | 49 | 17 | 34.7% |

---

## 5. 代表性 Sample Cases

### Case 1：R017 — 重症 → ICU → 死亡

- **82 歲男性**，3 樓 B 翼 (3B-21)
- 共病：CHF + 癌症 + COPD，曾吸菸（former）
- 暴露：使用淋浴
- 2026-01-20 發病：發燒、咳嗽、呼吸困難
- 2026-01-23 住院 → ICU
- 2026-01-27 死亡
- **個案分類**：confirmed

### Case 2：R006 — 重症 → ICU → 存活

- **83 歲男性**，3 樓 B 翼 (3B-01)
- 共病：CHF + DM，目前吸菸（current）
- 暴露：使用淋浴 + 水療池
- 2026-01-20 發病：發燒、咳嗽
- 2026-01-21 住院 → ICU
- 存活
- **個案分類**：confirmed

### Case 3：R008 — 中度 → 住院 → 死亡

- **77 歲女性**，2 樓 A 翼 (2A-11)
- 免疫抑制、目前吸菸（current）
- 暴露：使用淋浴
- 2026-01-19 發病：發燒、咳嗽、意識混亂
- 2026-01-23 住院
- 2026-01-30 死亡
- **個案分類**：confirmed

### Case 4：R001 — 輕症可能個案

- **95 歲女性**，2 樓 A 翼 (2A-04)
- 共病：CHF + DM + 癌症 + 免疫抑制
- 暴露：使用淋浴
- 2026-01-20 發病：咳嗽、呼吸困難（無發燒）
- 未住院、未實驗室確認
- **個案分類**：probable

### Case 5：R091 — 無症狀確診

- **84 歲女性**，2 樓 B 翼 (2B-14)
- 無慢性病
- 暴露：使用淋浴
- 接觸者篩檢陽性（尿液抗原）
- 無任何症狀
- **個案分類**：confirmed

### Case 6：R010 — 未感染住民

- **95 歲男性**，3 樓 A 翼 (3A-13)
- 無慢性病
- 暴露：使用淋浴（但未感染）
- **個案分類**：not_a_case

---

## 6. 可應用的分析方法與對應章節

### 6.1 描述性流行病學 (Descriptive Epidemiology)

| 分析 | 使用欄位 | 預期教學重點 |
|------|---------|-------------|
| **流行曲線（Epidemic curve）** | `symptom_onset_date` | 辨識共同暴露源型態（common source）；按日/週分組 |
| **人的描述** | `age`, `sex`, `clinical_severity` | 年齡分組的侵襲率、性別分布 |
| **地的描述** | `floor`, `wing`, `room` | 按樓層翼區製作侵襲率地圖（spot map） |
| **時的描述** | `symptom_onset_date`, `notification_date` | 通報延遲分析 |

### 6.2 分析性流行病學 (Analytical Epidemiology)

| 分析 | 使用欄位 | 預期教學重點 |
|------|---------|-------------|
| **2×2 表與風險比（Risk Ratio）** | `shower_use` × `infected` | 暴露與疾病的關聯量化 |
| **2×2 表（水療池）** | `hydrotherapy_use` × `infected` | 第二種暴露因子 |
| **卡方檢定** | 各危險因子 × `infected` | 關聯的統計顯著性 |
| **分層分析（Stratified analysis）** | `shower_use` × `infected`，按 `floor` 分層 | 干擾因子控制、Mantel-Haenszel 法 |
| **多變項邏輯斯迴歸** | `age`, `sex`, 所有共病, `shower_use`, `floor`, `wing` | 同時調整多個危險因子，計算 adjusted OR |

### 6.3 臨床與結果分析

| 分析 | 使用欄位 | 預期教學重點 |
|------|---------|-------------|
| **致死率（CFR）分析** | `outcome`, `clinical_severity` | 按嚴重度 / 共病分組的 CFR |
| **住院風險因子** | `hospitalized`, 各共病 | 誰比較容易住院？ |
| **ICU 入住預測** | `icu_admission`, `age`, 共病, `severity` | 重症預測因子 |
| **發病到住院間隔** | `symptom_onset_date`, `hospitalization_date` | 就醫延遲分析 |
| **發病到死亡間隔** | `symptom_onset_date`, `death_date` | 存活時間分析 |
| **症狀群分析** | `fever`, `cough`, `dyspnea`, `confusion`, `diarrhea` | 症狀組合與嚴重度的關聯 |

### 6.4 進階分析

| 分析 | 使用欄位 | 預期教學重點 |
|------|---------|-------------|
| **存活分析（Survival analysis）** | `symptom_onset_date`, `death_date`, `outcome` | Kaplan-Meier 曲線、Cox regression |
| **空間分析（Spot map）** | `floor`, `wing`, `room`, `infected` | 視覺化感染分布、辨識高風險區域 |
| **機器學習分類** | 所有特徵 → `infected` 或 `outcome` | Random Forest / Logistic Regression 比較 |
| **聚類分析（Clustering）** | 症狀欄位 | 無監督式學習辨識臨床表型 |
| **干擾因子探討** | `functional_status` ↔ `shower_use` ↔ `infected` | DAG（Directed Acyclic Graph）教學 |

### 6.5 資料清理與前處理

| 練習 | 說明 |
|------|------|
| 日期欄位轉換 | 多個日期欄位需 `pd.to_datetime()` |
| 建立衍生變項 | 如 `age_group`、`n_comorbidities`、`onset_to_hosp_days` |
| 處理遺漏值 | 未感染者的日期欄位為空值 |
| 二元變項重新編碼 | `outcome` → 0/1、`case_classification` → 虛擬變項 |
| 計算流行病學週（epi week） | `symptom_onset_date` → epi week |

---

## 7. 生成腳本使用說明

### 7.1 基本使用

```bash
# 使用預設參數生成（SEED=42, 280 住民）
uv run python data/synthetic/generate_legionella_outbreak.py
```

### 7.2 可調整參數

腳本頂部的常數均可修改以調整資料特性：

```python
# 住民人數
TARGET_RESIDENTS = 280

# 群聚時間軸
OUTBREAK_START = date(2026, 1, 10)
OUTBREAK_PEAK  = date(2026, 1, 20)
OUTBREAK_END   = date(2026, 2, 5)

# 共病盛行率
PROB_CHF    = 0.25
PROB_DM     = 0.35
PROB_CANCER = 0.15
PROB_COPD   = 0.20

# 各危險因子對感染機率的加權
RISK_WEIGHTS = {
    "floor_2_wingB": 0.25,   # 調高 → 2B 翼侵襲率更高
    "shower_use":    0.18,   # 調高 → 淋浴暴露效應更強
    ...
}

# 基礎嚴重度分布
BASE_SEVERITY = {
    "asymptomatic": 0.12,
    "mild":         0.28,
    "moderate":     0.30,
    "severe":       0.30,
}
```

### 7.3 程式化呼叫

```python
from data.synthetic.generate_legionella_outbreak import generate_outbreak

# 生成不同規模的資料
df_small = generate_outbreak(n_residents=100)
df_large = generate_outbreak(n_residents=500)
```

### 7.4 重現性

- 固定 `SEED = 42`，相同參數會產生完全相同的資料
- 修改 `SEED` 可產生不同的隨機實現（realization），適合產生練習用的多組資料

---

## 8. 與現有資料集的關係

| 資料集 | 用途 | 差異 |
|--------|------|------|
| `line_list.csv` | 基礎教學（10 筆簡單資料） | 小型、4 個地區、簡單暴露 |
| `legionella_outbreak.csv` | 進階分析教學（280 筆完整資料） | 大型、多層危險因子、臨床細節豐富 |

`legionella_outbreak.csv` 涵蓋更豐富的欄位，適合進階章節教學，包括多變項分析、存活分析、機器學習等。原有的 `line_list.csv` 仍保留作為入門練習使用。

---

## 9. 教學應用建議：各章節適用分析

以下為建議的章節整合方式（供後續擴充參考）：

| 章節主題 | 可用的分析 | 關鍵欄位 |
|----------|-----------|---------|
| Line list 基礎 | 讀取、清理、瀏覽資料 | 全部 |
| 資料整理 | 日期轉換、衍生變項、groupby | 日期欄位、age、comorbidity |
| 描述性統計 | 頻率表、交叉表、集中/離散趨勢 | age、sex、severity、outcome |
| 流行曲線 | Epi curve 繪製 | `symptom_onset_date` |
| 2×2 表分析 | RR、OR、卡方檢定 | `shower_use`、`infected` |
| 分層分析 | 按 floor/wing 分層的 RR | `shower_use`、`floor`、`wing` |
| 邏輯斯迴歸 | Crude & adjusted OR | 所有危險因子 |
| 存活分析 | Kaplan-Meier、Cox regression | onset/death 日期、outcome |
| 空間視覺化 | Spot map / heatmap | floor、wing、room |
| 機器學習 | 分類預測 | 全部特徵 → outcome/severity |

---

## 10. 參考文獻與流行病學依據

1. **退伍軍人症臨床特徵**：潛伏期 2–10 天、CFR 5–30%（CDC / WHO 指引）
2. **護理之家群聚事件**：機構內群聚侵襲率可達 30–40%（脆弱族群）
3. **危險因子**：年齡、吸菸、COPD、免疫抑制為已知危險因子
4. **傳播途徑**：氣溶膠吸入為主要途徑，淋浴 / 冷卻水塔為常見感染源
5. **台灣通報定義**：依衛生福利部疾病管制署法定傳染病分類，退伍軍人病屬第四類
