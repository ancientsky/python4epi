# 05 分層分析與交絡因子

## 情境

在 Ch03 中，我們發現淋浴使用者的感染風險比（RR）明顯大於 1。但資深疫調人員提出一個質疑：

> 「臥床住民幾乎不使用淋浴，而臥床住民本來活動範圍就小、暴露機會也少。你看到的高 RR，會不會只是因為**能走動的人同時也在用淋浴**？」

這就是**交絡（confounding）**的問題。這一章教你如何辨識交絡因子，用分層分析把它「控制」住，再用 Mantel-Haenszel 法得到調整後的 RR。

## 你將學到

- 什麼是交絡因子（confounder）及其三要件
- 如何用 DAG（有向無環圖）辨識交絡路徑
- 如何進行分層分析（stratified analysis）
- 各層 RR 的森林圖（forest plot）視覺化
- Mantel-Haenszel 加權 RR 及同質性檢定
- 比較粗 RR vs. 調整後 RR 的差異

## 核心概念

### 交絡因子的三要件

一個變項 C 是交絡因子，必須同時滿足：

1. C 與**暴露**有關聯（例：功能狀態影響是否使用淋浴）
2. C 與**結果**有關聯（例：功能狀態影響感染風險）
3. C **不是**暴露→結果因果路徑上的中間變項

### DAG（有向無環圖）

```
functional_status → shower_use → infected
functional_status ─────────────→ infected
```

- `functional_status → shower_use`：能自主行走的人才用淋浴
- `functional_status → infected`：功能狀態好的人活動範圍大、暴露機會多
- 如果不控制 `functional_status`，淋浴的 RR 會被**膨脹**

### 分層分析的邏輯

把資料按交絡因子分層（例如按功能狀態分成三組），在各層內分別計算 RR。如果各層的 RR 都比粗 RR 小，就表示粗 RR 確實被交絡膨脹了。

### Mantel-Haenszel 法

跨層加權合併的方法，給每一層一個權重（取決於各層的樣本大小），算出一個「調整後的 RR」。

$$RR_{MH} = \frac{\sum_i \frac{a_i \cdot (c_i + d_i)}{N_i}}{\sum_i \frac{c_i \cdot (a_i + b_i)}{N_i}}$$

---

## Step 1: 資料準備

```python
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from epi_learning.metrics import risk_ratio

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
```

## Step 2: 粗 RR 回顧

```python
ct = pd.crosstab(df["shower_use"], df["infected"])
a = int(ct.loc[1, 1])
b = int(ct.loc[1, 0])
c = int(ct.loc[0, 1])
d = int(ct.loc[0, 0])

crude_rr = risk_ratio(a, a + b, c, c + d)
print(f"粗 RR (shower_use → infected) = {crude_rr:.3f}")
```

## Step 3: 檢查交絡條件

```python
# 條件 1：functional_status 與 shower_use 有關聯嗎？
print("=== 功能狀態 × 淋浴使用 ===")
print(pd.crosstab(df["functional_status"], df["shower_use"],
                  margins=True, normalize="index").round(3))

# 條件 2：functional_status 與 infected 有關聯嗎？
print("\n=== 功能狀態 × 感染 ===")
print(pd.crosstab(df["functional_status"], df["infected"],
                  margins=True, normalize="index").round(3))
```

## Step 4: 分層分析

```python
strata = df["functional_status"].unique()
stratum_results = []

for s in sorted(strata):
    sub = df[df["functional_status"] == s]
    ct_s = pd.crosstab(sub["shower_use"], sub["infected"])

    # 有些層可能缺某些組合，需要檢查
    if ct_s.shape != (2, 2):
        continue

    a_s = int(ct_s.loc[1, 1])
    b_s = int(ct_s.loc[1, 0])
    c_s = int(ct_s.loc[0, 1])
    d_s = int(ct_s.loc[0, 0])
    n_s = a_s + b_s + c_s + d_s

    rr_s = risk_ratio(a_s, a_s + b_s, c_s, c_s + d_s)

    # 95% CI
    ln_rr = np.log(rr_s)
    se = np.sqrt(1/a_s - 1/(a_s+b_s) + 1/c_s - 1/(c_s+d_s))
    ci_lo = np.exp(ln_rr - 1.96 * se)
    ci_hi = np.exp(ln_rr + 1.96 * se)

    stratum_results.append({
        "stratum": s,
        "n": n_s,
        "a": a_s, "b": b_s, "c": c_s, "d": d_s,
        "RR": rr_s,
        "CI_lower": ci_lo,
        "CI_upper": ci_hi,
    })

results_df = pd.DataFrame(stratum_results)
print("=== 分層 RR ===")
for _, row in results_df.iterrows():
    print(f"  {row['stratum']:20s}  RR={row['RR']:.3f}  "
          f"(95% CI: {row['CI_lower']:.3f}–{row['CI_upper']:.3f})  n={row['n']}")

print(f"\n  粗 RR = {crude_rr:.3f}")
```

## Step 5: 森林圖

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
plt.style.use("ggplot")
plt.rcParams["figure.dpi"] = 150

fig, ax = plt.subplots(figsize=(8, 4))
y_pos = range(len(results_df))

ax.errorbar(
    results_df["RR"], y_pos,
    xerr=[results_df["RR"] - results_df["CI_lower"],
          results_df["CI_upper"] - results_df["RR"]],
    fmt="o", color="#2c7fb8", capsize=4, markersize=8,
)
ax.axvline(x=1, color="gray", linestyle="--", alpha=0.5)
ax.axvline(x=crude_rr, color="red", linestyle=":", alpha=0.7, label=f"粗 RR={crude_rr:.2f}")
ax.set_yticks(y_pos)
ax.set_yticklabels(results_df["stratum"])
ax.set_xlabel("Risk Ratio (RR)")
ax.set_title("分層分析森林圖：淋浴使用 → 感染（按功能狀態分層）")
ax.legend()
plt.tight_layout()
plt.show()
```

## Step 6: Mantel-Haenszel 加權 RR

```python
numerator = 0
denominator = 0

for _, row in results_df.iterrows():
    a_i, b_i, c_i, d_i = row["a"], row["b"], row["c"], row["d"]
    n_i = a_i + b_i + c_i + d_i
    numerator += a_i * (c_i + d_i) / n_i
    denominator += c_i * (a_i + b_i) / n_i

rr_mh = numerator / denominator

print(f"Mantel-Haenszel 調整後 RR = {rr_mh:.3f}")
print(f"粗 RR                     = {crude_rr:.3f}")
print(f"差異                      = {crude_rr - rr_mh:.3f}")

if crude_rr - rr_mh > 0.1:
    print("→ 粗 RR 被交絡膨脹了！控制功能狀態後，淋浴的效應變小")
```

## Step 7: 同質性檢定

```python
# Breslow-Day 同質性檢定的簡化版
# 如果各層 RR 差異大 → 可能有交互作用（effect modification）
rr_values = results_df["RR"].values
rr_range = rr_values.max() - rr_values.min()

print(f"各層 RR 範圍：{rr_values.min():.3f} – {rr_values.max():.3f}")
print(f"RR 變異幅度：{rr_range:.3f}")

if rr_range > 0.5:
    print("→ 各層 RR 差異較大，可能存在效果修飾（effect modification）")
    print("  建議分層報告，不宜只報告合併的 RR_MH")
else:
    print("→ 各層 RR 相近，可合理使用 MH 加權合併值")
```

## Step 8: 第二個範例 — 按樓層分層

```python
print("=== 按樓層分層分析：淋浴 → 感染 ===")

for floor in sorted(df["floor"].unique()):
    sub = df[df["floor"] == floor]
    ct_f = pd.crosstab(sub["shower_use"], sub["infected"])
    if ct_f.shape != (2, 2):
        continue
    a_f, b_f = int(ct_f.loc[1, 1]), int(ct_f.loc[1, 0])
    c_f, d_f = int(ct_f.loc[0, 1]), int(ct_f.loc[0, 0])
    rr_f = risk_ratio(a_f, a_f + b_f, c_f, c_f + d_f)
    print(f"  {floor}F: RR={rr_f:.3f}  (shower: {a_f}/{a_f+b_f}, "
          f"no shower: {c_f}/{c_f+d_f})")
```

---

## 解讀重點

| 比較 | 意義 |
|------|------|
| 粗 RR > 調整 RR | 交絡因子將效應**膨脹** |
| 粗 RR < 調整 RR | 交絡因子將效應**壓抑** |
| 各層 RR ≈ 調整 RR | 無交互作用，合併值可信 |
| 各層 RR 差異大 | 有交互作用，應分層報告 |

## 常見錯誤

1. **不驗證交絡三要件**：直接分層卻不檢查 C 是否真的與暴露和結果都有關
2. **分層太細**：每層樣本太小，RR 估計不穩定
3. **忽略交互作用**：各層 RR 差很大時只報告 MH 合併值是不恰當的
4. **只控制一個交絡**：分層分析一次只能控制一個變項 → Ch06 邏輯斯迴歸可同時調整多個

## 下一步

分層分析一次只能控制一個交絡因子。但如果同時有年齡、功能狀態、共病等多個交絡因子呢？Ch06 的**邏輯斯迴歸**可以一次調整所有變項，算出 adjusted OR。

## 練習本

- 課堂筆記：{ref}`05_stratified_analysis.ipynb`
- 作業版：[`05_stratified_exercise.ipynb`](../exercises/05_stratified_exercise.ipynb)
- 解答版（教師版）：[`05_stratified_solution.ipynb`](../solutions/05_stratified_solution.ipynb)
