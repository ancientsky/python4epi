# 13 可重現研究與報告

## 你將學到

- 如何用 `uv` 鎖定環境與版本
- 如何設計可重跑（reproducible）的分析流程
- 如何建立最小可驗證報告（data + code + result）

## 情境故事

松柏護理之家退伍軍人症群聚事件的分析終於完成了。
你需要在一週後重新產出同一份疫情報告，並保證同事在另一台機器上得到一致結果。

> 「上次跑出來是 121 人感染、19 人死亡，但我重跑結果不一樣？」

這就是 **可重現研究** 要解決的問題。

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

path = Path("data/synthetic/legionella_outbreak.csv")
df = pd.read_csv(path)

summary = {
    "n_residents": len(df),
    "n_zones": df.groupby(["floor", "wing"]).ngroups,
    "n_infected": int((df["clinical_severity"] != "not_ill").sum()),
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

- 作業版：[`13_reproducibility_exercise.ipynb`](exercises/13_reproducibility_exercise.ipynb)
- 解答版（講師）：[`13_reproducibility_solution.ipynb`](solutions/13_reproducibility_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/13_reproducibility_solution.ipynb>)

## 常見誤用

| 錯誤 | 正確做法 |
|------|----------|
| 在 notebook 手動改資料卻不記錄 | 所有轉換寫在程式碼中 |
| 只分享結果圖，不分享程式 | 附上可重跑程式與版本資訊 |
| 未鎖定套件版本 | 用 `uv.lock` 固定環境 |
| 亂數種子未固定 | 設定 `random_state` 或 `torch.manual_seed` |

## 下一步

確保分析可重現之後，下一章（Ch14）我們將所有技能整合成一個 **完整實戰案例** → 疫情調查 SitRep。
