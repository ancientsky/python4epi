# 06 邏輯斯迴歸

## 情境

Ch05 的分層分析告訴我們，功能狀態確實是淋浴使用的交絡因子。但疫調會議上，感控護理師追問：

> 「同時考慮年齡、所有共病、功能狀態、樓層以後，淋浴使用**還是**顯著的危險因子嗎？」

分層分析一次只能控制一個變項。要同時調整多個因子，需要**邏輯斯迴歸（logistic regression）**。

## 你將學到

- 邏輯斯迴歸的原理與適用場景
- Odds Ratio (OR) 與 Risk Ratio (RR) 的區別
- 用 statsmodels 建立單變項和多變項模型
- 比較 crude OR vs. adjusted OR
- 模型診斷（AIC/BIC）與變項選擇
- 結果呈現：標準的流行病學 Table 2 格式

## 核心概念

### 從 RR 到 OR

| 指標 | 公式 | 適用場景 |
|------|------|---------|
| RR（風險比） | P(disease\|exposed) / P(disease\|unexposed) | 世代研究 |
| OR（勝算比） | odds(exposed) / odds(unexposed) | 病例對照、迴歸 |

當疾病盛行率低時，OR ≈ RR。本資料集侵襲率 ~43%，OR 會比 RR 偏離較多。

### 邏輯斯迴歸模型

$$\log\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots$$

- $p$：感染機率
- $\beta_i$：迴歸係數
- $\text{OR}_i = e^{\beta_i}$：控制其他變項後，$x_i$ 每增加一單位的勝算比

### Crude OR vs. Adjusted OR

- **Crude OR**：只放一個自變項 → 未調整
- **Adjusted OR**：同時放多個自變項 → 控制了其他因子的效應

---

## Step 1: 資料準備

```python
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# 功能狀態轉數值
fs_map = {"bedridden": 0, "wheelchair": 1, "ambulatory": 2}
df["functional_score"] = df["functional_status"].map(fs_map)
```

## Step 2: 單變項 Crude OR 彙整

```python
factors = [
    "shower_use", "hydrotherapy_use", "smoking_history",
    "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed",
    "age", "functional_score",
]

crude_results = []
for var in factors:
    model = smf.logit(f"infected ~ {var}", data=df).fit(disp=0)
    coef = model.params[var]
    ci = model.conf_int().loc[var]
    crude_results.append({
        "variable": var,
        "crude_OR": round(np.exp(coef), 3),
        "95% CI": f"{np.exp(ci[0]):.3f}–{np.exp(ci[1]):.3f}",
        "p-value": round(model.pvalues[var], 4),
    })

crude_df = pd.DataFrame(crude_results)
print(crude_df.to_string(index=False))
```

## Step 3: 多變項 Adjusted OR

```python
formula = (
    "infected ~ shower_use + hydrotherapy_use + age + "
    "comorbidity_chf + comorbidity_dm + comorbidity_cancer + "
    "comorbidity_copd + immunosuppressed + functional_score + "
    "C(floor)"
)
model_full = smf.logit(formula, data=df).fit(disp=0)
print(model_full.summary2())
```

## Step 4: Adjusted OR 表格（Table 2）

```python
adj_results = []
for var in model_full.params.index:
    if var == "Intercept":
        continue
    coef = model_full.params[var]
    ci = model_full.conf_int().loc[var]
    adj_results.append({
        "variable": var,
        "adjusted_OR": round(np.exp(coef), 3),
        "95% CI": f"{np.exp(ci[0]):.3f}–{np.exp(ci[1]):.3f}",
        "p-value": round(model_full.pvalues[var], 4),
    })

adj_df = pd.DataFrame(adj_results)
print(adj_df.to_string(index=False))
```

## Step 5: Crude vs. Adjusted OR 比較

```python
key_vars = ["shower_use", "hydrotherapy_use", "age",
            "comorbidity_chf", "immunosuppressed"]

comparison = []
for var in key_vars:
    crude_row = crude_df[crude_df["variable"] == var].iloc[0]
    adj_row = adj_df[adj_df["variable"] == var]
    if len(adj_row) == 0:
        continue
    adj_row = adj_row.iloc[0]
    comparison.append({
        "variable": var,
        "crude_OR": crude_row["crude_OR"],
        "adjusted_OR": adj_row["adjusted_OR"],
        "change%": f"{((adj_row['adjusted_OR'] - crude_row['crude_OR']) / crude_row['crude_OR'] * 100):+.1f}%",
    })

print(pd.DataFrame(comparison).to_string(index=False))
```

## Step 6: 模型診斷

```python
formula_reduced = (
    "infected ~ shower_use + hydrotherapy_use + age + "
    "immunosuppressed + functional_score"
)
model_reduced = smf.logit(formula_reduced, data=df).fit(disp=0)

print(f"完整模型 AIC = {model_full.aic:.1f}")
print(f"精簡模型 AIC = {model_reduced.aic:.1f}")
```

---

## 解讀重點

| 結果 | 意義 |
|------|------|
| Adjusted OR > 1 且 p < 0.05 | 控制其他因子後，仍為獨立危險因子 |
| Crude OR ≫ Adjusted OR | 粗 OR 被交絡膨脹（與 Ch05 結論一致） |
| Adjusted OR ≈ 1 | 控制後效應消失，原來的關聯可能是假的 |
| AIC 較小 | 模型在解釋力與複雜度間取得較好平衡 |

## 常見錯誤

1. **OR 當 RR 用**：侵襲率高時 OR ≠ RR，要注意解讀
2. **放太多變項**：280 筆資料放 15+ 變項 → 過度擬合
3. **忽略多重共線性**：高度相關的變項不要同時放入
4. **只看 p-value**：OR 的大小和 CI 寬度也很重要
5. **自動選變項**：stepwise 不推薦 → 用流行病學知識選擇

## 下一步

邏輯斯迴歸回答了「哪些因子獨立影響感染風險」。但主管接著問：「下週還會有多少新個案？」→ Ch07 時間序列預測。

## 練習本

- 課堂筆記：{ref}`06_logistic_regression.ipynb`
- 作業版：[`06_logistic_regression_exercise.ipynb`](../exercises/06_logistic_regression_exercise.ipynb)
- 解答版（教師版）：[`06_logistic_regression_solution.ipynb`](../solutions/06_logistic_regression_solution.ipynb)
