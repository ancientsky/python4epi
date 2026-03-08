# 03 描述性統計與 2×2 表

## 情境

松柏護理之家退伍軍人症群聚事件，疫調團隊已經完成資料清理和視覺化（Ch02）。現在主管問你：**「使用淋浴設備的人，感染風險是不是比較高？有沒有統計上的證據？」**

要回答這個問題，你需要學會：建立 2×2 列聯表、計算風險比（RR）、估計信賴區間、做卡方檢定。

## 你將學到

- 從 line list 建立 2×2 列聯表
- 計算風險比（Risk Ratio, RR）及其意義
- 估計 RR 的 95% 信賴區間（CI）
- 使用卡方檢定（chi-square test）判斷統計顯著性
- 同時比較多個危險因子的粗 RR

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

### 95% 信賴區間

信賴區間表達估計值的不確定性。如果 95% CI 不包含 1，則 RR 在 α=0.05 水準下有統計顯著性。

$$\ln(RR) \pm 1.96 \times SE(\ln RR)$$

其中 $SE(\ln RR) = \sqrt{\frac{1}{a} - \frac{1}{a+b} + \frac{1}{c} - \frac{1}{c+d}}$

### 卡方檢定

測試兩個類別變項是否獨立（p-value < 0.05 → 有統計顯著關聯）。

---

## Step 1: 資料準備

```python
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from epi_learning.metrics import risk_ratio

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
print(f"全體：{len(df)} 人，感染：{df['infected'].sum()} 人")
```

## Step 2: 建立 2×2 表（淋浴 × 感染）

```python
# 用 pd.crosstab 快速建立列聯表
ct_shower = pd.crosstab(
    df["shower_use"], df["infected"],
    margins=True, margins_name="合計",
)
ct_shower.index = ["未使用淋浴", "使用淋浴", "合計"]
ct_shower.columns = ["未感染", "感染", "合計"]
print(ct_shower)
```

## Step 3: 計算 Risk Ratio

```python
# 從列聯表提取四格
a = int(ct_shower.loc["使用淋浴", "感染"])        # 暴露+感染
b = int(ct_shower.loc["使用淋浴", "未感染"])      # 暴露+未感染
c = int(ct_shower.loc["未使用淋浴", "感染"])      # 未暴露+感染
d = int(ct_shower.loc["未使用淋浴", "未感染"])    # 未暴露+未感染

rr = risk_ratio(a, a + b, c, c + d)
print(f"淋浴使用 → 感染的 RR = {rr:.3f}")
print(f"  暴露組風險: {a/(a+b):.1%}")
print(f"  未暴露組風險: {c/(c+d):.1%}")
```

## Step 4: 95% 信賴區間

```python
# RR 的 95% CI（對數轉換法）
ln_rr = np.log(rr)
se_ln_rr = np.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))

ci_lower = np.exp(ln_rr - 1.96 * se_ln_rr)
ci_upper = np.exp(ln_rr + 1.96 * se_ln_rr)

print(f"RR = {rr:.3f} (95% CI: {ci_lower:.3f} – {ci_upper:.3f})")

if ci_lower > 1:
    print("→ 95% CI 不包含 1，暴露與感染有統計顯著關聯")
else:
    print("→ 95% CI 包含 1，無法排除暴露與感染無關")
```

## Step 5: 卡方檢定

```python
contingency = [[a, b], [c, d]]
chi2, p, dof, expected = chi2_contingency(contingency)

print(f"卡方統計量 = {chi2:.3f}")
print(f"自由度 = {dof}")
print(f"p-value = {p:.4f}")
print(f"\n期望值表：")
print(pd.DataFrame(
    expected.round(1),
    index=["使用淋浴", "未使用淋浴"],
    columns=["感染", "未感染"],
))
```

## Step 6: 第二個暴露因子 — 水療使用

```python
ct_hydro = pd.crosstab(df["hydrotherapy_use"], df["infected"])
a2, b2 = int(ct_hydro.loc[1, 1]), int(ct_hydro.loc[1, 0])
c2, d2 = int(ct_hydro.loc[0, 1]), int(ct_hydro.loc[0, 0])

rr2 = risk_ratio(a2, a2 + b2, c2, c2 + d2)
chi2_2, p2, _, _ = chi2_contingency([[a2, b2], [c2, d2]])

print(f"水療使用 → 感染的 RR = {rr2:.3f}, p = {p2:.4f}")
```

## Step 7: 多因子粗 RR 彙整表

一次比較所有可能的危險因子，找出「嫌疑最大」的暴露：

```python
factors = [
    "shower_use", "hydrotherapy_use",
    "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed",
]

# smoking_history 是三分類（never/former/current），先轉為二分類
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
    chi2_i, p_i, _, _ = chi2_contingency([[a_i, b_i], [c_i, d_i]])
    # 95% CI
    ln_rr_i = np.log(rr_i)
    se_i = np.sqrt(1/a_i - 1/(a_i+b_i) + 1/c_i - 1/(c_i+d_i))
    ci_lo = np.exp(ln_rr_i - 1.96 * se_i)
    ci_hi = np.exp(ln_rr_i + 1.96 * se_i)
    results.append({
        "factor": factor,
        "RR": round(rr_i, 3),
        "95% CI lower": round(ci_lo, 3),
        "95% CI upper": round(ci_hi, 3),
        "p-value": round(p_i, 4),
    })

rr_table = pd.DataFrame(results).sort_values("RR", ascending=False)
print(rr_table.to_string(index=False))
```

---

## 解讀重點

| 指標 | 意義 |
|------|------|
| RR > 1 且 CI 不含 1 | 暴露可能增加感染風險 |
| RR ≈ 1 或 CI 含 1 | 暴露與感染無顯著關聯 |
| p < 0.05 | 統計顯著（但不代表因果） |
| 粗 RR 彙整表 | 快速掃描所有因子，找出線索 |

## 常見錯誤

1. **只看 p-value**：p < 0.05 不代表效果大，要看 RR 和 CI
2. **忽略交絡因子**：粗 RR 可能受年齡、共病等干擾 → 需要 Ch05 分層分析
3. **混淆 RR 和 OR**：本章因為有完整世代資料，可以算 RR；若是病例對照研究才用 OR
4. **樣本數太小**：期望值 < 5 的格子應改用 Fisher 精確檢定

## 下一步

粗 RR 只是初步線索。淋浴使用的 RR 看起來很高，但如果高樓層同時淋浴使用率高又靠近水塔，那 RR 可能被**交絡（confounding）**膨脹了。Ch05 會用**分層分析**和 **Mantel-Haenszel 法**來處理這個問題。

## 練習本

- 課堂筆記：{ref}`03_stats_basics.ipynb`
- 作業版：[`03_stats_exercise.ipynb`](exercises/03_stats_exercise.ipynb)
- 解答版（教師版）：[`03_stats_solution.ipynb`](solutions/03_stats_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/03_stats_solution.ipynb>)
