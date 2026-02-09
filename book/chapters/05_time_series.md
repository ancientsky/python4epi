# 05 時間序列與預測

## 你將學到

- 建立每日病例序列
- 用 baseline 模型做短期預測
- 用 MAE 檢查預測誤差

## 情境故事

醫療量能管理需要未來 7 天病例估計，作為病床與檢驗資源規劃。

## 核心概念

- **Baseline**：先用簡單模型當對照
- **Rolling mean**：常見的短期平滑預測
- **Backtesting**：用歷史資料回測方法穩定度

## 最小可執行程式碼

```python
import pandas as pd
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("data/synthetic/line_list.csv", parse_dates=["date_onset"])
series = df.groupby("date_onset").size().asfreq("D", fill_value=0)

# 用前3天平均預測下一天
pred = series.rolling(window=3).mean().shift(1).dropna()
actual = series.loc[pred.index]
mae = mean_absolute_error(actual, pred)
print(f"MAE={mae:.3f}")
```

## 練習題

1. 把 window 從 3 改成 5，比較 MAE。
2. 試作 week-over-week baseline：用前 7 天同曜日平均預測。

## 常見誤用

- 用未來資訊做特徵（data leakage）。
- 只回報單一指標，沒有對照 baseline。

## 常用圖表（時間序列）

- 流行曲線：每日病例 `bar chart`（觀察峰值與變化）
- 趨勢線：每日病例 + rolling mean（看短期方向）
- 預測對照圖：`actual vs predicted` 折線圖

```python
import matplotlib.pyplot as plt

plot_df = actual.reset_index()
plot_df.columns = ["date_onset", "actual"]
plot_df["pred"] = pred.values

plt.figure(figsize=(8, 3.5))
plt.plot(plot_df["date_onset"], plot_df["actual"], marker="o", label="Actual")
plt.plot(plot_df["date_onset"], plot_df["pred"], marker="o", label="Predicted")
plt.legend()
plt.title("Actual vs Predicted Cases")
plt.tight_layout()
plt.show()
```

## 練習本

- 作業版：[`notebooks/exercises/05_time_series_exercise.ipynb`](../../notebooks/exercises/05_time_series_exercise.ipynb)
- 解答版：[`notebooks/exercises/05_time_series_solution.ipynb`](../../notebooks/exercises/05_time_series_solution.ipynb)
