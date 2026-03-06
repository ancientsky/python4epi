# 02 資料處理與視覺化（Python 零基礎版）

## 情境

松柏護理之家退伍軍人症群聚事件爆發後第三天，疫調團隊已彙整出一份 **280 筆 × 32 欄**的個案名冊（line list）。你的任務是：把這份 CSV 讀進 Python，確認資料品質，建立分析用的衍生變項，然後用圖表呈現疫情的時間趨勢、空間分布與族群特徵。

## 你將學到

- 用 `pandas` 讀取並檢視 line list 結構
- 轉換日期欄位、處理遺漏值
- 建立衍生變項（年齡組、共病數、發病到住院天數、流行病學週）
- 用 `groupby` 做分組統計
- 用 `matplotlib` 畫流行曲線
- 用 `seaborn` 畫統計比較圖
- 用 `plotly` 畫互動式圖表

## 先備說明（給零基礎學員）

這章只要掌握這些就能開始：

1. `pd.read_csv(...)`：讀取資料
2. `df.info()` / `df.describe()`：檢視資料結構
3. `pd.to_datetime(...)`：日期轉換
4. `groupby(...).size()` / `.mean()`：分組統計
5. `plt.bar(...)` / `sns.barplot(...)` / `px.bar(...)`：各種圖表

## 視覺化套件選擇

| 套件 | 適合場景 | 特色 |
|------|---------|------|
| `matplotlib` | 正式報告圖、完全控制細節 | 最基礎、最靈活 |
| `seaborn` | 統計圖（分布、比較、關係） | 預設美觀、語法精簡 |
| `plotly` | 互動式探索、簡報 | 滑鼠懸停看數值 |

## 流病常用圖表對照

| 分析需求 | 推薦圖表 |
|---------|---------|
| 疫情隨時間變化 | 流行曲線（epidemic curve）、折線圖 |
| 地區/翼區比較 | 長條圖、排序條圖 |
| 年齡或指標分布 | 直方圖、箱型圖 |
| 時間 × 地區強度 | 熱圖（heatmap） |
| 互動探索與簡報 | Plotly 互動圖 |

---

## Part 1：資料處理

### Step 1: 讀入 line list

```python
import pandas as pd

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
print(f"資料維度：{df.shape[0]} 筆 × {df.shape[1]} 欄")
df.head()
```

### Step 2: 檢視資料結構

```python
df.info()
```

```python
df.describe()
```

重點觀察：哪些欄位有遺漏值？數值欄位的範圍合理嗎？

### Step 3: 日期轉換

line list 中有 5 個日期欄位，讀入時是文字，必須轉成 datetime 才能做時間分析。

```python
date_cols = [
    "facility_admission_date",
    "symptom_onset_date",
    "hospitalization_date",
    "death_date",
    "notification_date",
]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")
```

### Step 4: 建立衍生變項

疫調分析常需要從原始資料衍生新變項：

```python
# 1) 年齡組
df["age_group"] = pd.cut(
    df["age"],
    bins=[59, 69, 79, 89, 100],
    labels=["60-69", "70-79", "80-89", "90+"],
)

# 2) 共病數
comorbidity_cols = [
    "comorbidity_chf", "comorbidity_dm",
    "comorbidity_cancer", "comorbidity_copd",
    "immunosuppressed",
]
df["n_comorbidities"] = df[comorbidity_cols].sum(axis=1)

# 3) 是否感染（二元變項）
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# 4) 發病到住院天數
df["onset_to_hosp_days"] = (
    df["hospitalization_date"] - df["symptom_onset_date"]
).dt.days

# 5) 流行病學週
df["epi_week"] = df["symptom_onset_date"].dt.isocalendar().week
```

### Step 5: 處理遺漏值

未感染者不會有 `symptom_onset_date`、`hospitalization_date` 等，這些 NaT 不是資料錯誤而是合理的結構性遺漏。

```python
# 確認：未感染者的 onset 日期應全為空
print("未感染者有 onset 日期的數量：",
      df.loc[df["infected"] == 0, "symptom_onset_date"].notna().sum())
```

### Step 6: groupby 分組統計

```python
# 按 floor × wing 計算侵襲率
wing_stats = (
    df.groupby(["floor", "wing"])
    .agg(residents=("case_id", "size"), infected=("infected", "sum"))
    .reset_index()
)
wing_stats["attack_rate"] = wing_stats["infected"] / wing_stats["residents"]
wing_stats["attack_rate_pct"] = (wing_stats["attack_rate"] * 100).round(1)
print(wing_stats.to_string(index=False))
```

---

## Part 2：視覺化

### Step 7: 流行曲線（matplotlib）

流行曲線是流行病學最經典的圖表——X 軸是發病日期，Y 軸是新增病例數。從曲線形狀可推斷傳播模式。

```python
import matplotlib.pyplot as plt

# -- CJK font setup (避免中文標籤顯示為方框) --
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False

cases = df[df["infected"] == 1]
daily = cases.groupby("symptom_onset_date").size().rename("cases")

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, color="#2c7fb8", edgecolor="white")
ax.set_title("退伍軍人症流行曲線（依發病日）", fontsize=14)
ax.set_xlabel("發病日期")
ax.set_ylabel("新增病例數")
fig.autofmt_xdate()
plt.tight_layout()
plt.show()
```

**解讀**：峰值集中在幾天內 → 共同暴露源（point source）型態。

### Step 8: 年齡分布（seaborn）

```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(
    data=df, x="age", hue="infected", bins=15,
    multiple="stack", palette={0: "#cccccc", 1: "#e34a33"}, ax=ax,
)
ax.set_title("年齡分布：感染 vs 未感染")
ax.set_xlabel("年齡")
ax.set_ylabel("人數")
ax.legend(title="感染", labels=["未感染", "感染"])
plt.tight_layout()
plt.show()
```

### Step 9: 翼區侵襲率長條圖（seaborn）

```python
wing_stats["label"] = wing_stats["floor"].astype(str) + wing_stats["wing"]
wing_stats = wing_stats.sort_values("attack_rate", ascending=False)

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(
    data=wing_stats, x="label", y="attack_rate_pct",
    hue="label", palette="YlOrRd", legend=False, ax=ax,
)
ax.set_title("各翼區侵襲率比較")
ax.set_xlabel("翼區")
ax.set_ylabel("侵襲率 (%)")
for i, row in wing_stats.iterrows():
    ax.text(
        list(wing_stats["label"]).index(row["label"]),
        row["attack_rate_pct"] + 1,
        f'{row["attack_rate_pct"]}%',
        ha="center", fontsize=10,
    )
plt.tight_layout()
plt.show()
```

### Step 10: 嚴重度 × 共病熱力圖（seaborn）

```python
severity_order = ["mild", "moderate", "severe"]
heat_data = (
    cases[cases["clinical_severity"].isin(severity_order)]
    .groupby(["clinical_severity", "n_comorbidities"])
    .size()
    .unstack(fill_value=0)
    .reindex(severity_order)
)

fig, ax = plt.subplots(figsize=(8, 3.5))
sns.heatmap(heat_data, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
ax.set_title("臨床嚴重度 × 共病數")
ax.set_xlabel("共病數")
ax.set_ylabel("嚴重度")
plt.tight_layout()
plt.show()
```

### Step 11: 互動式分層流行曲線（Plotly）

```python
import plotly.express as px

daily_floor = (
    cases.groupby(["symptom_onset_date", "floor"])
    .size()
    .rename("cases")
    .reset_index()
)
daily_floor["floor"] = daily_floor["floor"].astype(str) + "F"

fig = px.bar(
    daily_floor,
    x="symptom_onset_date", y="cases", color="floor",
    barmode="stack",
    title="互動式流行曲線（依樓層分層）",
    labels={"symptom_onset_date": "發病日期", "cases": "病例數", "floor": "樓層"},
)
fig.show()
```

---

## 圖表解讀重點

| 圖表 | 觀察重點 |
|------|---------|
| 流行曲線 | 峰值時間、上升/下降速度 → 傳播模式 |
| 年齡分布 | 感染者是否集中在特定年齡層 |
| 翼區長條圖 | 哪些翼區侵襲率異常偏高 → 空間線索 |
| 嚴重度×共病 | 共病多的人是否更容易重症 |
| 互動曲線 | 各樓層的流行高峰是否同步 |

## 常見錯誤

1. **日期沒轉換**：`symptom_onset_date` 仍是字串，時間排序會亂掉
2. **忽略分母**：直接比病例數而不算侵襲率，大翼區天生病例多
3. **圖表缺標題/軸標籤**：讀者無法獨立解讀
4. **混淆感染者與全體**：畫年齡分布時忘了區分

## 練習本

- 資料處理課堂筆記：{ref}`02_data_wrangling_for_beginners.ipynb`
- 視覺化課堂筆記：{ref}`02_visualization_epi_charts.ipynb`
- 作業版：[`02_data_wrangling_exercise.ipynb`](../exercises/02_data_wrangling_exercise.ipynb)
- 解答版（教師版）：[`02_data_wrangling_solution.ipynb`](../solutions/02_data_wrangling_solution.ipynb)
