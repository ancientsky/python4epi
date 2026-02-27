# 10 可重現研究與報告

## 你將學到

- 如何用 `uv` 鎖定環境與版本
- 如何設計可重跑（reproducible）的分析流程
- 如何建立最小可驗證報告（data + code + result）

## 情境故事

你需要在一週後重新產出同一份疫情報告，並保證同事在另一台機器上得到一致結果。

## 核心概念

- **Environment lock**：以 `uv.lock` 固定相依版本
- **Single command workflow**：用單一命令重跑分析
- **Traceability**：每個結果都能追到資料來源與程式版本

## 最小可執行程式碼

```bash
uv sync
uv run pytest
uv run python notebooks/run_sitrep.py
```

```python
from pathlib import Path
import pandas as pd

path = Path("data/synthetic/line_list.csv")
df = pd.read_csv(path)

summary = {
    "n_rows": len(df),
    "n_locations": df["location"].nunique(),
    "n_deaths": int((df["outcome"] == "dead").sum()),
}
print(summary)
```

## 可重現檢查清單

1. 是否有 `uv.lock`。
2. 是否能從乾淨環境執行 `uv sync && uv run pytest`。
3. 是否有固定資料欄位契約（line list schema）。
4. 是否有最小可重跑腳本（例如 `run_sitrep.py`）。

## 練習題

1. 新增 `scripts/rebuild_report.sh`（或等效指令）一鍵重跑流程。
2. 將 `summary` 寫入 `data/processed/summary.csv`。

## 常見誤用

- 在 notebook 手動改資料卻不記錄。
- 只分享結果圖，不分享可重跑程式與版本資訊。

## 練習本

- 作業版：[`notebooks/exercises/10_reproducibility_exercise.ipynb`](../../notebooks/exercises/10_reproducibility_exercise.ipynb)
- 解答版：[`notebooks/exercises/10_reproducibility_solution.ipynb`](../../notebooks/exercises/10_reproducibility_solution.ipynb)
