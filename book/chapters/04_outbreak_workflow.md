# 04 群聚調查工作流：從 Line List 到 SitRep

## 情境

松柏護理之家退伍軍人症群聚事件爆發後第三天下午，你的長官說：

> 「兩小時內交出第一份疫情日報（SitRep），內容要包含：多少人感染、哪裡最嚴重、致死率多少、流行曲線長什麼樣。之後每天早上九點前更新。」

你手上有一份 280 筆 × 32 欄的 line list CSV。這一章教你如何用 Python **自動化**產出一份結構化的 SitRep，而且每天只要重跑一次腳本就能更新。

## 你將學到

- 從 raw line list 到 SitRep 的完整自動化流程
- 描述性流行病學三要素：**人、時、地**
- 關鍵指標計算：侵襲率、CFR、住院率、ICU 率
- 按個案分類（確診/可能/非個案）分層摘要
- 輸出結構化報告（含表格 + 圖表）
- 把分析流程做成可重跑腳本

## SitRep 的基本架構

一份標準的疫情日報至少包含：

1. **摘要指標**：截至目前的累計數字
2. **人**（Person）：年齡、性別、共病分布
3. **時**（Time）：流行曲線、新增趨勢
4. **地**（Place）：按地點的侵襲率比較
5. **行動建議**：根據數據的初步判斷

---

## Step 1: 讀取與資料準備

```python
import pandas as pd
import matplotlib.pyplot as plt

# -- CJK font setup (避免中文標籤顯示為方框) --
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
plt.style.use("ggplot")
plt.rcParams["figure.dpi"] = 150

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# 日期轉換
date_cols = [
    "facility_admission_date", "symptom_onset_date",
    "hospitalization_date", "death_date", "notification_date",
]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# 衍生變項
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
df["age_group"] = pd.cut(
    df["age"], bins=[59, 69, 79, 89, 100],
    labels=["60-69", "70-79", "80-89", "90+"],
)
comorbidity_cols = [
    "comorbidity_chf", "comorbidity_dm",
    "comorbidity_cancer", "comorbidity_copd", "immunosuppressed",
]
df["n_comorbidities"] = df[comorbidity_cols].sum(axis=1)
```

## Step 2: 摘要指標

```python
total = len(df)
infected = df["infected"].sum()
confirmed = (df["case_classification"] == "confirmed").sum()
probable = (df["case_classification"] == "probable").sum()
hospitalized = df["hospitalized"].sum()
icu = df["icu_admission"].sum()
deaths = (df["outcome"] == "dead").sum()

print("=" * 50)
print("松柏護理之家退伍軍人症群聚 — SitRep")
print("=" * 50)
print(f"住民總數：{total}")
print(f"感染人數：{infected}（侵襲率 {infected/total:.1%}）")
print(f"  確診：{confirmed}　可能：{probable}")
print(f"住院：{hospitalized}（住院率 {hospitalized/infected:.1%}）")
print(f"ICU：{icu}（ICU 率 {icu/hospitalized:.1%}）")
print(f"死亡：{deaths}（CFR {deaths/infected:.1%}）")
```

## Step 3: 人 — Person

```python
cases = df[df["infected"] == 1]

print("=== 人口學特徵（感染者）===")
print(f"年齡中位數：{cases['age'].median():.0f} 歲"
      f"（範圍 {cases['age'].min()}-{cases['age'].max()}）")
print(f"男性比例：{(cases['sex'] == 'M').mean():.1%}")
print(f"\n--- 年齡組分布 ---")
print(cases["age_group"].value_counts().sort_index().to_string())
print(f"\n--- 共病分布 ---")
for col in comorbidity_cols:
    label = col.replace("comorbidity_", "").upper()
    n = cases[col].sum()
    print(f"  {label}: {n} ({n/len(cases):.1%})")
```

## Step 4: 時 — Time

```python
import matplotlib.dates as mdates

daily = cases.groupby("symptom_onset_date").size().rename("cases")

# 補齊完整日期範圍（含爆發前 3 天背景期）
date_range = pd.date_range(
    daily.index.min() - pd.Timedelta(days=3),
    daily.index.max() + pd.Timedelta(days=1),
    freq="D",
)
daily = daily.reindex(date_range, fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, width=1.0,
       color="#2c7fb8", edgecolor="white", linewidth=0.5)
ax.set_title("松柏護理之家退伍軍人症流行曲線，依發病日，2026 年 1 月",
             fontsize=13, fontweight="bold")
ax.set_xlabel("發病日期（Date of Symptom Onset）")
ax.set_ylabel("病例數（Number of Cases）")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)
ax.set_xlim(daily.index.min() - pd.Timedelta(hours=12),
            daily.index.max() + pd.Timedelta(hours=12))
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()

print(f"流行期間：{cases['symptom_onset_date'].min().date()} – {cases['symptom_onset_date'].max().date()}")
print(f"高峰日：{daily.idxmax().date()}（{daily.max()} 例）")
```

## Step 5: 地 — Place

```python
wing_stats = (
    df.groupby(["floor", "wing"])
    .agg(
        residents=("case_id", "size"),
        infected=("infected", "sum"),
        deaths=("outcome", lambda x: (x == "dead").sum()),
    )
    .reset_index()
)
wing_stats["AR%"] = (wing_stats["infected"] / wing_stats["residents"] * 100).round(1)
wing_stats["CFR%"] = (wing_stats["deaths"] / wing_stats["infected"] * 100).round(1)
wing_stats["label"] = wing_stats["floor"].astype(str) + wing_stats["wing"]

print("=== 各翼區疫情摘要 ===")
print(wing_stats[["label", "residents", "infected", "AR%", "deaths", "CFR%"]]
      .to_string(index=False))
```

## Step 6: 個案分類分層摘要

```python
classification = (
    df.groupby("case_classification")
    .agg(
        n=("case_id", "size"),
        hospitalized=("hospitalized", "sum"),
        icu=("icu_admission", "sum"),
        deaths=("outcome", lambda x: (x == "dead").sum()),
    )
)
classification["hosp_rate"] = (
    classification["hospitalized"] / classification["n"] * 100
).round(1)

print("=== 按個案分類分層 ===")
print(classification.to_string())
```

## Step 7: 輸出結構化 SitRep

把以上所有步驟包成一個函式，每天重跑即可更新：

```python
def generate_sitrep(csv_path):
    """從 CSV 產出 SitRep 摘要字典。"""
    df = pd.read_csv(csv_path)
    for col in ["symptom_onset_date", "hospitalization_date",
                "death_date", "notification_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

    total = len(df)
    infected = int(df["infected"].sum())
    deaths = int((df["outcome"] == "dead").sum())

    return {
        "total_residents": total,
        "infected": infected,
        "attack_rate": round(infected / total * 100, 1),
        "deaths": deaths,
        "cfr": round(deaths / infected * 100, 1) if infected else 0,
        "hospitalized": int(df["hospitalized"].sum()),
        "icu": int(df["icu_admission"].sum()),
    }

sitrep = generate_sitrep("data/synthetic/legionella_outbreak.csv")
print(sitrep)
```

---

## 常見錯誤

1. **每天改定義**：個案定義（case definition）一旦確定就不要改，否則趨勢不可比
2. **只放圖不放表**：SitRep 必須有可查核的數字表格
3. **忘記標註資料截止時間**：每份報告都要註明「資料截至 YYYY-MM-DD HH:MM」
4. **侵襲率沒算分母**：直接比較病例數不公平，要除以各翼區住民數

## 進階：可重跑腳本

```bash
uv run python notebooks/run_sitrep.py
```

把整個 SitRep 流程存成 `.py` 腳本，每天更新 CSV 後重跑一次就能自動產出最新日報。

## 練習本

- 課堂筆記：{ref}`04_outbreak_workflow.ipynb`
- 作業版：[`04_outbreak_workflow_exercise.ipynb`](exercises/04_outbreak_workflow_exercise.ipynb)
- 解答版（教師版）：[`04_outbreak_workflow_solution.ipynb`](solutions/04_outbreak_workflow_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/04_outbreak_workflow_solution.ipynb>)
