# 04 爆發調查工作流

## 你將學到

- 從 raw line list 到 SitRep 的最短流程
- 日報表（daily summary）與指標選擇
- 如何把程式碼做成可重跑腳本

## 情境故事

縣市衛生局要求你每天上午 9 點前提交前一日監測摘要（SitRep）。

## 工作流步驟

1. 讀取資料並標準化欄位。
2. 計算核心指標：病例數、死亡數、CFR、攻擊率。
3. 依地區和時間輸出彙整表。
4. 生成可複製到報告的表格。

## 最小可執行程式碼

```bash
uv run python notebooks/run_sitrep.py
```

```python
import pandas as pd
from epi_learning.cleaning import standardize_line_list
from epi_learning.tabulate import summarize_by_group

df = pd.read_csv("data/synthetic/line_list.csv")
clean = standardize_line_list(df)
by_location = summarize_by_group(clean, "location")
print(by_location)
```

## 練習題

1. 新增 `age_group` 分層（0-17, 18-49, 50+）後輸出摘要表。
2. 新增「最近 3 天新增病例」指標。

## 常見誤用

- 每天更改欄位定義，導致趨勢不可比。
- 報告只放圖，不提供可查核表格。

## 練習本

- 作業版：[`notebooks/exercises/04_outbreak_workflow_exercise.ipynb`](../../notebooks/exercises/04_outbreak_workflow_exercise.ipynb)
- 解答版：[`notebooks/exercises/04_outbreak_workflow_solution.ipynb`](../../notebooks/exercises/04_outbreak_workflow_solution.ipynb)
