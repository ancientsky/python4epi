# 03 描述與推論統計

## 你將學到

- 如何從 line list 建立 2x2 表並計算 RR
- 如何估計比例的信賴區間（confidence interval）
- 何時用卡方檢定（chi-square test）

## 情境故事

某學校宿舍爆發腸胃炎。你想知道「共用餐廳暴露（exposure）」是否提高發病風險。

## 核心概念

- **Risk Ratio (RR)**：暴露組風險 / 非暴露組風險
- **95% CI**：估計值不確定性的範圍
- **p-value**：在虛無假設下觀察到資料的機率，不等於效果大小

## 最小可執行程式碼

```python
import pandas as pd
from scipy.stats import chi2_contingency
from epi_learning.metrics import risk_ratio

df = pd.read_csv("data/synthetic/line_list.csv")
# 假設 dead 代表嚴重不良結局，作為示範 outcome
df["bad_outcome"] = (df["outcome"] == "dead").astype(int)

exposed_cases = int(df.loc[df["exposed"] == 1, "bad_outcome"].sum())
exposed_total = int((df["exposed"] == 1).sum())
unexposed_cases = int(df.loc[df["exposed"] == 0, "bad_outcome"].sum())
unexposed_total = int((df["exposed"] == 0).sum())

rr = risk_ratio(exposed_cases, exposed_total, unexposed_cases, unexposed_total)
print(f"RR = {rr:.3f}")

contingency = [
    [exposed_cases, exposed_total - exposed_cases],
    [unexposed_cases, unexposed_total - unexposed_cases],
]
chi2, p, _, _ = chi2_contingency(contingency)
print(f"chi2={chi2:.3f}, p-value={p:.4f}")
```

## 練習題

1. 把 `bad_outcome` 改成「onset 後 2 天內回報」的延遲事件，重新計算 RR。
2. 用分層方式（例如 `location`）比較 RR 是否一致。

## 常見誤用

- 只看 p-value，不看效果大小（RR）和 CI。
- 未檢查資料品質就直接做推論。

## 練習本

- 作業版：[`notebooks/exercises/03_stats_exercise.ipynb`](../../notebooks/exercises/03_stats_exercise.ipynb)
- 解答版：[`notebooks/exercises/03_stats_solution.ipynb`](../../notebooks/exercises/03_stats_solution.ipynb)
