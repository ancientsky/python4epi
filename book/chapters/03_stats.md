# 03 暴露與疾病的關聯：2×2 表與推論統計

## 情境

松柏護理之家退伍軍人症群聚事件，疫調團隊已經完成資料清理和視覺化（Ch02）。現在主管問你：**「使用淋浴設備的人，感染風險是不是比較高？有沒有統計上的證據？」**

你正要回答「淋浴組侵襲率比較高」，資深疫調前輩打斷你：

> 「等等——你說的是**描述**還是**推論**？光是『看起來比較高』不夠，你怎麼用統計來排除這只是隨機誤差？而且，你現在手上的資料，到底適合算 RR 還是 OR？」

這一章就是要回答這些問題。

## 你將學到

- 描述統計與推論統計的差異
- 流行病學研究設計（世代研究 vs. 病例對照研究）如何決定效應量指標
- 從 line list 建立 2×2 列聯表
- 計算風險比（Risk Ratio, RR）及其意義
- 計算勝算比（Odds Ratio, OR）及 RR 與 OR 的差異
- 估計 RR 和 OR 的 95% 信賴區間（CI）
- 使用卡方檢定和 Fisher 精確檢定判斷統計顯著性
- 同時比較多個危險因子，用森林圖（forest plot）視覺化

---

## 描述統計 vs. 推論統計

Ch02 我們用**描述統計**（平均值、次數分布、圖表）整理了資料的樣貌。但主管問的問題不是「資料長什麼樣」，而是「淋浴使用和感染**有沒有關聯**」。

這就需要**推論統計（inferential statistics）**——用樣本資料去推論：觀察到的差異是真實的關聯，還是純粹**隨機誤差（chance）**造成的？

| 類型 | 目的 | 範例 |
|------|------|------|
| 描述統計 | 摘要資料的特徵 | 平均年齡 72 歲、侵襲率 43.2%、流行曲線 |
| 推論統計 | 從樣本推論母體、檢定假說 | RR 的 95% CI、卡方檢定 p-value |

### 核心術語

- **虛無假設（H₀）**：淋浴使用與感染互相獨立（無關聯）
- **對立假設（H₁）**：淋浴使用與感染有關聯
- **p-value**：假設 H₀ 為真時，觀察到現有數據（或更極端數據）的機率。p 越小，越有理由拒絕 H₀
- **信賴區間（CI）**：效應量的合理範圍。若 95% CI 不包含「無效果值」（RR=1 或 OR=1），則在 α=0.05 水準下有統計顯著性

---

## 流行病學研究設計速覽

你能算什麼指標，取決於你的**研究設計**：

### 世代研究（Cohort Study）

- 依**暴露狀態**分組，追蹤疾病結果
- 有完整分母（全部暴露者和未暴露者的人數）
- 可以直接計算**風險（risk）**和 **RR（風險比）**

### 病例對照研究（Case-Control Study）

- 依**疾病狀態**分組（先找病例，再選對照），回溯暴露史
- 分母是研究者人為決定的（例如選 1:2 配對），不代表真實族群的疾病發生率
- 無法算 risk → 只能算 **OR（勝算比）**

| 研究設計 | 抽樣方式 | 可算指標 | 適用場景 |
|---------|---------|---------|---------|
| 世代研究 | 依暴露分組，追蹤結果 | **RR**（風險比） | 群聚調查（有全員資料） |
| 病例對照 | 依疾病分組，回溯暴露 | **OR**（勝算比） | 罕見疾病、大規模族群 |

> **本次調查** = 回溯性世代研究（retrospective cohort）：280 位住民全部納入，暴露和結果都已知 → 可以直接計算 **RR**。我們也會同時算 **OR** 來比較兩者的差異，並為 Ch06 的邏輯斯迴歸做準備。

---

## 核心概念

### 2×2 列聯表

|  | 感染 | 未感染 | 合計 |
|--|------|--------|------|
| **暴露** | a | b | a+b |
| **未暴露** | c | d | c+d |

### Risk Ratio（風險比）

$$RR = \frac{a / (a+b)}{c / (c+d)}$$

- RR = 1：暴露與疾病無關
- RR > 1：暴露可能增加風險
- RR < 1：暴露可能是保護因子

### Odds Ratio（勝算比）

**勝算（odds）** 和**風險（risk）** 不同：

- 風險 = p（發生的機率）
- 勝算 = p / (1-p)（發生 vs. 不發生的比值）

$$OR = \frac{a \times d}{b \times c}$$

- 當疾病罕見時（侵襲率 < 10%），OR ≈ RR
- 當侵襲率高時（如本資料集 ~43%），OR 會大於 RR
- OR 是邏輯斯迴歸（Ch06）的原生輸出

### 95% 信賴區間

**RR 的 CI**（Katz method）：

$$\ln(RR) \pm 1.96 \times SE(\ln RR)$$

其中 $SE(\ln RR) = \sqrt{\frac{1}{a} - \frac{1}{a+b} + \frac{1}{c} - \frac{1}{c+d}}$

**OR 的 CI**（Woolf method）：

$$\ln(OR) \pm 1.96 \times SE(\ln OR)$$

其中 $SE(\ln OR) = \sqrt{\frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}}$

若 95% CI 不包含 1，則效應量在 α=0.05 水準下有統計顯著性。

### 卡方檢定與 Fisher 精確檢定

- **卡方檢定**：比較觀察次數與期望次數（H₀ 下的預期），適用於期望值 ≥ 5 的情況
- **Fisher 精確檢定**：直接計算在 H₀ 下觀察到當前或更極端結果的確切機率，適用於小樣本（期望值 < 5）

---

## Step 1: 資料準備

```python
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact
from epi_learning.metrics import risk_ratio, odds_ratio

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
print(f"全體：{len(df)} 人，感染：{df['infected'].sum()} 人")
print(f"整體侵襲率：{df['infected'].mean():.1%}")
```

## Step 2: 建立 2×2 表（淋浴 × 感染）

```python
ct_shower = pd.crosstab(
    df["shower_use"], df["infected"],
    margins=True, margins_name="合計",
)
ct_shower.index = ["未使用淋浴", "使用淋浴", "合計"]
ct_shower.columns = ["未感染", "感染", "合計"]
print(ct_shower)

# 提取四格
a = int(ct_shower.loc["使用淋浴", "感染"])        # 暴露+感染
b = int(ct_shower.loc["使用淋浴", "未感染"])      # 暴露+未感染
c = int(ct_shower.loc["未使用淋浴", "感染"])      # 未暴露+感染
d = int(ct_shower.loc["未使用淋浴", "未感染"])    # 未暴露+未感染

print(f"\n暴露組（使用淋浴）侵襲率: {a/(a+b):.1%}")
print(f"未暴露組（未使用淋浴）侵襲率: {c/(c+d):.1%}")
```

## Step 3: 計算 Risk Ratio（風險比）

```python
rr = risk_ratio(a, a + b, c, c + d)
print(f"淋浴使用 → 感染的 RR = {rr:.3f}")
print(f"  解讀：使用淋浴者的感染風險是未使用者的 {rr:.1f} 倍")
print(f"  RR = 1 → 無關聯 | RR > 1 → 暴露可能增加風險 | RR < 1 → 可能是保護因子")
```

> **注意**：RR > 1 代表有「關聯」，不代表有「因果」。可能有干擾因子——Ch05 會處理。

## Step 4: 計算 Odds Ratio（勝算比）

```python
or_val = odds_ratio(a, b, c, d)
print(f"淋浴使用 → 感染的 OR = {or_val:.3f}")
print(f"  （相比 RR = {rr:.3f}）")
print(f"\n本資料集侵襲率 = {df['infected'].mean():.1%}（非罕見疾病）")
print(f"→ OR ({or_val:.3f}) 大於 RR ({rr:.3f})，這是預期的")
print(f"→ 疾病罕見時 OR ≈ RR；侵襲率越高，OR 偏離 RR 越多")
```

## Step 5: 95% 信賴區間（RR 和 OR）

```python
# RR 的 CI：Katz method
ln_rr = np.log(rr)
se_ln_rr = np.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))
ci_rr_lo = np.exp(ln_rr - 1.96 * se_ln_rr)
ci_rr_hi = np.exp(ln_rr + 1.96 * se_ln_rr)

# OR 的 CI：Woolf method
ln_or = np.log(or_val)
se_ln_or = np.sqrt(1/a + 1/b + 1/c + 1/d)
ci_or_lo = np.exp(ln_or - 1.96 * se_ln_or)
ci_or_hi = np.exp(ln_or + 1.96 * se_ln_or)

print("=== 95% 信賴區間比較 ===")
print(f"RR = {rr:.3f} (95% CI: {ci_rr_lo:.3f} – {ci_rr_hi:.3f})")
print(f"OR = {or_val:.3f} (95% CI: {ci_or_lo:.3f} – {ci_or_hi:.3f})")
```

> **解讀**：如果你把這個調查重複做 100 次，大約 95 次算出的 CI 會包含真正的 RR/OR。CI 不包含 1 = 在 α=0.05 下有統計顯著性，等同於 p < 0.05。

## Step 6: 卡方檢定

```python
# H₀: 淋浴使用與感染互相獨立（無關聯）
contingency = [[a, b], [c, d]]
chi2, p, dof, expected = chi2_contingency(contingency)

print(f"卡方統計量 = {chi2:.3f}")
print(f"自由度 = {dof}")
print(f"p-value = {p:.4f}")
print(f"\n期望值表（H₀ 為真時的預期次數）：")
print(pd.DataFrame(
    expected.round(1),
    index=["使用淋浴", "未使用淋浴"],
    columns=["感染", "未感染"],
))

min_expected = expected.min()
print(f"\n最小期望值 = {min_expected:.1f}", end="")
if min_expected >= 5:
    print(" → 滿足卡方檢定前提")
else:
    print(" → < 5，建議改用 Fisher 精確檢定")
```

## Step 7: Fisher 精確檢定

```python
oddsr_fisher, p_fisher = fisher_exact(contingency)
print(f"Fisher 精確檢定:")
print(f"  OR = {oddsr_fisher:.3f}")
print(f"  p-value = {p_fisher:.4f}")
print(f"\n卡方檢定 p = {p:.4f} vs Fisher p = {p_fisher:.4f}")
print("（此例樣本夠大，兩種檢定結果相近；小樣本時差異會更明顯）")
```

> Fisher 精確檢定不依賴大樣本近似，在期望值 < 5 或總樣本數 < 30 時更為可靠。

## Step 8: 第二個暴露因子 — 水療使用

```python
ct_hydro = pd.crosstab(df["hydrotherapy_use"], df["infected"])
a2, b2 = int(ct_hydro.loc[1, 1]), int(ct_hydro.loc[1, 0])
c2, d2 = int(ct_hydro.loc[0, 1]), int(ct_hydro.loc[0, 0])

rr2 = risk_ratio(a2, a2 + b2, c2, c2 + d2)
or2 = odds_ratio(a2, b2, c2, d2)
chi2_2, p2, _, _ = chi2_contingency([[a2, b2], [c2, d2]])

# RR CI
ln_rr2 = np.log(rr2)
se_rr2 = np.sqrt(1/a2 - 1/(a2+b2) + 1/c2 - 1/(c2+d2))
ci_rr2_lo = np.exp(ln_rr2 - 1.96 * se_rr2)
ci_rr2_hi = np.exp(ln_rr2 + 1.96 * se_rr2)

# OR CI
ln_or2 = np.log(or2)
se_or2 = np.sqrt(1/a2 + 1/b2 + 1/c2 + 1/d2)
ci_or2_lo = np.exp(ln_or2 - 1.96 * se_or2)
ci_or2_hi = np.exp(ln_or2 + 1.96 * se_or2)

print("水療使用 → 感染")
print(f"  RR = {rr2:.3f} (95% CI: {ci_rr2_lo:.3f} – {ci_rr2_hi:.3f})")
print(f"  OR = {or2:.3f} (95% CI: {ci_or2_lo:.3f} – {ci_or2_hi:.3f})")
print(f"  卡方 p-value = {p2:.4f}")
```

## Step 9: 多因子粗效應量彙整表 + 森林圖

一次比較所有可能的危險因子，找出「嫌疑最大」的暴露：

```python
import matplotlib.pyplot as plt

factors = [
    "shower_use", "hydrotherapy_use",
    "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed",
]
df["ever_smoker"] = (df["smoking_history"] != "never").astype(int)
factors.append("ever_smoker")

results = []
for factor in factors:
    ct = pd.crosstab(df[factor], df["infected"])
    a_i = int(ct.loc[1, 1])
    b_i = int(ct.loc[1, 0])
    c_i = int(ct.loc[0, 1])
    d_i = int(ct.loc[0, 0])
    rr_i = risk_ratio(a_i, a_i + b_i, c_i, c_i + d_i)
    or_i = odds_ratio(a_i, b_i, c_i, d_i)
    chi2_i, p_i, _, _ = chi2_contingency([[a_i, b_i], [c_i, d_i]])
    ln_rr_i = np.log(rr_i)
    se_i = np.sqrt(1/a_i - 1/(a_i+b_i) + 1/c_i - 1/(c_i+d_i))
    ci_lo = np.exp(ln_rr_i - 1.96 * se_i)
    ci_hi = np.exp(ln_rr_i + 1.96 * se_i)
    results.append({
        "factor": factor,
        "RR": round(rr_i, 3),
        "CI_lower": round(ci_lo, 3),
        "CI_upper": round(ci_hi, 3),
        "OR": round(or_i, 3),
        "p-value": round(p_i, 4),
    })

rr_table = pd.DataFrame(results).sort_values("RR", ascending=False)
display_df = rr_table.copy()
display_df["95% CI"] = display_df.apply(
    lambda r: f"{r['CI_lower']:.3f}–{r['CI_upper']:.3f}", axis=1
)
print("=== 多因子粗效應量彙整表 ===")
print(display_df[["factor", "RR", "95% CI", "OR", "p-value"]].to_string(index=False))
```

### 森林圖（Forest Plot）

```python
fig, ax = plt.subplots(figsize=(8, 5))
rr_sorted = rr_table.reset_index(drop=True)
y_pos = range(len(rr_sorted))
ax.errorbar(
    rr_sorted["RR"], y_pos,
    xerr=[rr_sorted["RR"] - rr_sorted["CI_lower"],
          rr_sorted["CI_upper"] - rr_sorted["RR"]],
    fmt="o", color="#D97757", ecolor="#6B6B6B", capsize=4, markersize=7,
)
ax.axvline(x=1, color="#6B6B6B", linestyle="--", alpha=0.7, label="RR = 1（無效果）")
ax.set_yticks(list(y_pos))
ax.set_yticklabels(rr_sorted["factor"])
ax.set_xlabel("Risk Ratio (95% CI)")
ax.set_title("各因子粗風險比（Forest Plot）")
ax.legend(loc="lower right")
ax.invert_yaxis()
plt.tight_layout()
plt.show()
```

---

## 解讀重點

| 情境 | 指標 | 解讀 |
|------|------|------|
| RR > 1 且 CI 不含 1 | RR | 暴露可能增加感染風險 |
| RR ≈ 1 或 CI 含 1 | RR | 暴露與感染無顯著關聯 |
| p < 0.05 | p-value | 統計顯著（但不代表因果） |
| 世代研究（有完整分母） | 用 **RR** | 可以直接算風險 |
| 病例對照研究（無完整分母） | 用 **OR** | 只能算勝算 |
| 邏輯斯迴歸輸出 | **OR** | 模型原生輸出就是 log-odds |
| 罕見疾病（侵襲率 < 10%） | RR ≈ OR | 兩者可互換 |
| 多因子掃描 | 粗 RR 彙整表 | 快速篩出嫌疑因子，但需注意多重比較 |

## 常見錯誤

1. **只看 p-value**：p < 0.05 不代表效果大，要同時看 RR/OR 的大小和 CI 的寬度
2. **忽略干擾因子**：粗 RR 可能受年齡、共病等干擾 → 需要 Ch05 分層分析
3. **混淆 RR 和 OR**：世代研究用 RR，病例對照用 OR。本資料集侵襲率 ~43%，OR 明顯大於 RR
4. **樣本數太小**：期望值 < 5 的格子應改用 Fisher 精確檢定
5. **把統計顯著等同因果**：有關聯 ≠ 有因果。還需考慮時序性、劑量反應、生物合理性（Hill's criteria）
6. **多重比較問題**：同時測 8 個因子，光靠機率就可能有 ~0.4 個偽陽性（α=0.05 時）

## 下一步

粗 RR / OR 只是初步線索。

- 淋浴使用的 RR 看起來很高，但如果**能自主行走的住民同時淋浴使用率高又暴露機會多**，那 RR 可能被**干擾作用（confounding）**膨脹了。
- **Ch05** 會用**分層分析**和 **Mantel-Haenszel 法**把干擾因子「控制住」，得到調整後的 RR。
- **Ch06** 會用**邏輯斯迴歸**同時調整多個因子，算出 adjusted OR。

從粗關聯（Ch03）→ 控制干擾（Ch05）→ 多變項模型（Ch06），這是流行病學分析的標準三部曲。

## 練習本

- 課堂筆記：{ref}`03_stats_basics.ipynb`
- 作業版：[`03_stats_exercise.ipynb`](exercises/03_stats_exercise.ipynb)
- 解答版（教師版）：[`03_stats_solution.ipynb`](solutions/03_stats_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/03_stats_solution.ipynb>)
