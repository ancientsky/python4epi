# 07 時間序列與預測

## 情境

松柏護理之家退伍軍人症群聚事件進入第二週，長官在疫調會議上問：

> 「下禮拜還會有多少人發病？醫院還要準備幾張床？」

你需要從 line list 的 `symptom_onset_date` 建立每日發病數時間序列，用簡單的預測模型估算未來趨勢，並比較發病曲線與住院曲線的**時間差（lag）**。

## 你將學到

- 從 line list 建立每日病例時間序列
- 補齊無發病日（確保連續日期）
- 流行曲線 + 滾動平均疊圖
- 用滾動平均（rolling mean）做短期預測
- 用 MAE 評估預測品質
- 比較發病曲線 vs 住院曲線（lag 效應）

## 核心概念

| 概念 | 說明 |
|------|------|
| **Baseline 模型** | 先用最簡單的方法預測，作為比較基準 |
| **Rolling mean** | 用過去 k 天的平均值預測下一天 |
| **MAE** | Mean Absolute Error，預測誤差的絕對值平均 |
| **Lag 效應** | 發病到住院之間有時間差，住院高峰比發病高峰晚幾天 |
| **Data leakage** | 用到未來資訊做預測 → 結果不可靠 |

---

## Step 1: 建立每日發病數序列

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

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
df["symptom_onset_date"] = pd.to_datetime(df["symptom_onset_date"], errors="coerce")
df["hospitalization_date"] = pd.to_datetime(df["hospitalization_date"], errors="coerce")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

cases = df[df["infected"] == 1]

# 每日發病數，補齊無發病的日期
daily = cases.groupby("symptom_onset_date").size()
daily = daily.asfreq("D", fill_value=0)
daily.name = "cases"

print(f"序列長度：{len(daily)} 天")
print(f"日期範圍：{daily.index.min().date()} – {daily.index.max().date()}")
print(f"總病例：{daily.sum()}")
```

## Step 2: 流行曲線 + 滾動平均

```python
rolling_7 = daily.rolling(window=7, min_periods=1).mean()

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, width=1.0,
       color="#2c7fb8", edgecolor="white", linewidth=0.5,
       alpha=0.6, label="每日新增")
ax.plot(rolling_7.index, rolling_7.values, color="red", linewidth=2,
        label="7 日滾動平均")
ax.set_title("松柏護理之家退伍軍人症流行曲線 + 7 日滾動平均，2026 年 1 月",
             fontsize=12, fontweight="bold")
ax.set_xlabel("發病日期（Date of Symptom Onset）")
ax.set_ylabel("病例數（Number of Cases）")
ax.legend()
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.autofmt_xdate()
plt.tight_layout()
plt.show()
```

## Step 3: 滾動平均預測

```python
# 用前 3 天平均預測下一天（shift(1) 避免 data leakage）
pred_3 = daily.rolling(window=3).mean().shift(1).dropna()
actual = daily.loc[pred_3.index]

mae_3 = mean_absolute_error(actual, pred_3)
print(f"3 日滾動平均 MAE = {mae_3:.3f}")
```

## Step 4: 比較不同窗口

```python
for w in [3, 5, 7]:
    pred_w = daily.rolling(window=w).mean().shift(1).dropna()
    actual_w = daily.loc[pred_w.index]
    mae_w = mean_absolute_error(actual_w, pred_w)
    print(f"  window={w}  MAE={mae_w:.3f}")
```

## Step 5: Actual vs Predicted 對照圖

```python
pred_best = daily.rolling(window=3).mean().shift(1).dropna()
actual_best = daily.loc[pred_best.index]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(actual_best.index, actual_best.values, marker="o", markersize=4,
        label="實際", color="#2c7fb8")
ax.plot(pred_best.index, pred_best.values, marker="s", markersize=4,
        label="預測（3日MA）", color="#e34a33", linestyle="--")
ax.set_title("實際 vs 預測病例數（3 日滾動平均）",
             fontsize=13, fontweight="bold")
ax.set_xlabel("發病日期（Date of Symptom Onset）")
ax.set_ylabel("每日病例數（Number of Cases）")
ax.legend()
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.autofmt_xdate()
plt.tight_layout()
plt.show()
```

## Step 6: 發病 vs 住院曲線（Lag 效應）

```python
# 每日住院數
hosp_daily = (
    cases[cases["hospitalization_date"].notna()]
    .groupby("hospitalization_date").size()
)
# 對齊到相同日期範圍
all_dates = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
hosp_aligned = hosp_daily.reindex(all_dates, fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, width=1.0, alpha=0.5,
       color="#2c7fb8", edgecolor="white", linewidth=0.5, label="發病")
ax.bar(hosp_aligned.index, hosp_aligned.values, width=1.0, alpha=0.5,
       color="#e34a33", edgecolor="white", linewidth=0.5, label="住院")
ax.set_title("松柏護理之家退伍軍人症：發病 vs 住院曲線（Lag 效應），2026 年 1 月",
             fontsize=12, fontweight="bold")
ax.set_xlabel("日期（Date）")
ax.set_ylabel("人數（Number of Cases）")
ax.legend()
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.autofmt_xdate()
plt.tight_layout()
plt.show()

print("→ 住院高峰比發病高峰晚幾天，這個時間差可用於預測床位需求")
```

---

## 解讀重點

| 觀察 | 意義 |
|------|------|
| 流行曲線尖峰 | point source 共同暴露 |
| 滾動平均趨勢 | 疫情是在上升、持平或下降 |
| MAE 低 | 預測模型表現好 |
| Lag 效應 | 從發病高峰推估住院高峰時間 |

## 常見錯誤

1. **Data leakage**：用當天或未來資料做預測（忘記 `shift(1)`）
2. **沒補齊日期**：跳過無發病日，導致時間序列不連續
3. **只報單一指標**：沒有 baseline 對照的 MAE 沒有意義
4. **忽略 lag**：發病數下降不代表住院壓力馬上降

## 下一步

知道「何時」疫情最嚴重後，接下來問「在哪裡」最嚴重？→ Ch08 空間流病。

## 練習本

- 課堂筆記：{ref}`07_time_series_baseline.ipynb`
- 作業版：[`07_time_series_exercise.ipynb`](exercises/07_time_series_exercise.ipynb)
- 解答版（教師版）：[`07_time_series_solution.ipynb`](solutions/07_time_series_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/07_time_series_solution.ipynb>)
