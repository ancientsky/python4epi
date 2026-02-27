# 09 因果推論與政策評估

## 你將學到

- 用簡化資料示範 Difference-in-Differences (DiD)
- 讀懂政策前後與對照組差異
- 何時不能直接做因果解釋

## 情境故事

某地區在第 4 週開始防疫介入措施，你要評估是否降低發病率。

## 最小可執行程式碼

```python
import pandas as pd
import statsmodels.formula.api as smf

panel = pd.DataFrame(
    {
        "week": [1, 2, 3, 4, 5, 6] * 2,
        "treated": [0] * 6 + [1] * 6,
        "cases": [30, 28, 29, 27, 26, 25, 31, 30, 32, 24, 22, 21],
    }
)
panel["post"] = (panel["week"] >= 4).astype(int)

model = smf.ols("cases ~ treated + post + treated:post", data=panel).fit()
print(model.summary().tables[1])
```

`treated:post` 係數即 DiD 效果估計（在平行趨勢假設下）。

## 練習題

1. 改變介入起始週，檢查估計是否穩定。
2. 加入虛擬共變數（如氣溫）測試敏感度。

## 常見誤用

- 沒檢查平行趨勢就做 DiD 結論。
- 把觀察性關聯直接視為政策因果效果。

## 練習本

- 作業版：[`notebooks/exercises/09_causal_exercise.ipynb`](../../notebooks/exercises/09_causal_exercise.ipynb)
- 解答版：[`notebooks/exercises/09_causal_solution.ipynb`](../../notebooks/exercises/09_causal_solution.ipynb)
