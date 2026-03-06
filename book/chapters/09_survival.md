# 09 存活分析：發病後，誰的預後比較差？

## 你將學到

- 存活分析的核心概念：**存活時間**與**設限資料（censored data）**
- 如何用 **Kaplan-Meier 法**繪製存活曲線
- 如何用 **Log-rank 檢定**比較兩組存活曲線
- 如何用 **Cox 比例風險迴歸**分析多因子對存活的影響
- 如何解讀 **Hazard Ratio (HR)** 與繪製 HR 森林圖

## 情境故事

松柏護理之家退伍軍人症群聚事件已進入第三週。
121 位感染住民中，19 人不幸死亡，其餘存活。

你需要回答主治醫師的問題：
> 「發病後，哪些住民的死亡風險比較高？年齡？共病？嚴重度？」
> 「有沒有辦法量化這些因子的影響？」

這就是**存活分析**的核心任務——不只看「有沒有死亡」，更要看「多快死亡」以及「什麼因子加速死亡」。

---

## 核心概念

### 存活時間（Survival Time）

- **定義**：從事件起點（發病日）到結局發生（死亡）的時間
- 本案：`time_to_event = death_date − symptom_onset_date`

### 設限資料（Censored Data）

- 不是所有人都死亡——存活者在觀察結束時仍活著
- 這些個案稱為「**右設限（right-censored）**」
- 不能直接丟掉，也不能當成「存活時間 = 觀察期」
- Kaplan-Meier 法正確處理設限資料

### Hazard Ratio (HR)

- 類似 Risk Ratio (RR)，但考慮「時間」因素
- HR > 1 → 死亡速度較快（風險較高）
- HR < 1 → 死亡速度較慢（保護因子）

---

## Step 1 — 建立分析資料集

```python
import pandas as pd

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["symptom_onset_date"] = pd.to_datetime(df["symptom_onset_date"])
df["death_date"] = pd.to_datetime(df["death_date"])
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

cases = df[df["infected"] == 1].copy()

# 事件指標：1=死亡, 0=存活（設限）
cases["event"] = (cases["outcome"] == "dead").astype(int)

# 存活時間
investigation_end = cases["symptom_onset_date"].max() + pd.Timedelta(days=14)
cases["end_date"] = cases.apply(
    lambda r: r["death_date"] if r["event"] == 1 else investigation_end, axis=1
)
cases["time_to_event"] = (cases["end_date"] - cases["symptom_onset_date"]).dt.days
```

> **重要**：存活者的 `time_to_event` 使用調查結束日（最後發病日 +14 天），代表「至少觀察了這麼久都沒死亡」。

## Step 2 — Kaplan-Meier 全體存活曲線

```python
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

# -- CJK font setup (避免中文標籤顯示為方框) --
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False

kmf = KaplanMeierFitter()
kmf.fit(cases["time_to_event"], event_observed=cases["event"],
        label="全體")
kmf.plot_survival_function()
plt.title("Kaplan-Meier 存活曲線（全體感染住民）")
plt.xlabel("發病後天數")
plt.ylabel("存活機率")
plt.show()
```

## Step 3 — 按嚴重度分組的存活曲線

```python
for severity in ["mild", "moderate", "severe"]:
    mask = cases["clinical_severity"] == severity
    kmf.fit(cases.loc[mask, "time_to_event"],
            event_observed=cases.loc[mask, "event"],
            label=severity)
    kmf.plot_survival_function()
plt.title("存活曲線（按嚴重度分組）")
plt.show()
```

## Step 4 — Log-rank 檢定

```python
from lifelines.statistics import logrank_test

severe = cases[cases["clinical_severity"] == "severe"]
non_severe = cases[cases["clinical_severity"] != "severe"]
result = logrank_test(
    severe["time_to_event"], non_severe["time_to_event"],
    event_observed_A=severe["event"],
    event_observed_B=non_severe["event"],
)
print(f"Log-rank p-value = {result.p_value:.4f}")
```

## Step 5 — Cox 比例風險迴歸

```python
from lifelines import CoxPHFitter

cox_df = cases[["time_to_event", "event", "age", "sex",
                "comorbidity_copd", "comorbidity_chf",
                "comorbidity_dm", "comorbidity_cancer",
                "immunosuppressed"]].copy()
cox_df["is_male"] = (cox_df["sex"] == "M").astype(int)
cox_df = cox_df.drop(columns=["sex"])

cph = CoxPHFitter()
cph.fit(cox_df, duration_col="time_to_event", event_col="event")
cph.print_summary()
```

## Step 6 — HR 森林圖

```python
cph.plot()
plt.title("Cox Regression — Hazard Ratio")
plt.show()
```

---

## 練習題

- 作業版：[`09_survival_exercise.ipynb`](../exercises/09_survival_exercise.ipynb)
- 解答版（講師）：[`09_survival_solution.ipynb`](../solutions/09_survival_solution.ipynb)

## 常見誤用

| 錯誤 | 正確做法 |
|------|---------|
| 只用 CFR，不做存活分析 | CFR 不考慮時間，存活分析更精確 |
| 把存活者直接排除 | 存活者是設限資料，必須納入分析 |
| 忽略比例風險假設 | 用 `check_assumptions()` 驗證 |
| HR 解讀為機率 | HR 是「速率比」，不是「機率比」 |

## 下一步

存活分析告訴我們「誰的預後比較差」。
下一章（Ch10），我們挑戰更大的問題：**能不能用全部 32 欄特徵，訓練機器學習模型來預測感染和重症？** → 機器學習。
