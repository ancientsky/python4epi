# 02 資料處理與視覺化（Python 零基礎版）

## 你將學到

- 用 `pandas` 完成 line list 的基本清理
- 使用 `matplotlib`、`seaborn`、`plotly` 畫流病常用圖表
- 繪製經典 **流行曲線（epidemic curve）**
- 為不同任務選對圖（監測、比較、溝通）

## 先備說明（給零基礎學員）

這章只要掌握這些就能開始畫圖：

1. `pd.read_csv(...)`：讀取資料
2. `groupby(...).size()`：做病例統計
3. `plt.figure(...)` + `plt.show()`：`matplotlib` 基本繪圖
4. `sns.<chart>(...)`：`seaborn` 快速美化統計圖
5. `px.<chart>(...)`：`plotly` 互動圖（滑鼠可看數值）

## 視覺化套件選擇地圖

- `matplotlib`：最基礎、可完全控制細節，適合正式報告圖。
- `seaborn`：在統計圖（分布、比較、關係）更快更漂亮。
- `plotly`：互動式圖表，適合簡報與探索式分析。

## 流病常用圖表對照

- 疫情隨時間變化：`流行曲線 (epidemic curve)`、折線圖
- 地區比較：長條圖、排序條圖
- 年齡或指標分布：直方圖、箱型圖
- 時間 x 地區強度：熱圖（heatmap）
- 對外溝通與探索：互動折線圖/長條圖

## Step 1: 讀資料與基本清理

```python
import pandas as pd

raw = pd.read_csv("data/synthetic/line_list.csv")
raw["date_onset"] = pd.to_datetime(raw["date_onset"], errors="coerce")
raw["epi_week"] = raw["date_onset"].dt.isocalendar().week
print(raw.head())
```

## Step 2: 經典流行曲線（matplotlib）

流行曲線的標準做法：

1. 以 onset date 聚合每日病例
2. 用 bar chart 顯示病例數
3. X 軸是日期，Y 軸是病例數

```python
import matplotlib.pyplot as plt

daily = raw.groupby("date_onset").size().rename("cases")

plt.figure(figsize=(9, 3.5))
plt.bar(daily.index.astype(str), daily.values)
plt.title("Epidemic Curve (By Onset Date)")
plt.xlabel("Onset Date")
plt.ylabel("Cases")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## Step 3: `seaborn` 做統計比較圖

### 3.1 地區病例排序長條圖

```python
import seaborn as sns

by_location = raw.groupby("location").size().rename("cases").reset_index()
by_location = by_location.sort_values("cases", ascending=False)

plt.figure(figsize=(6, 3.5))
sns.barplot(data=by_location, x="location", y="cases", hue="location", legend=False)
plt.title("Cases by Location")
plt.tight_layout()
plt.show()
```

### 3.2 年齡分布直方圖

```python
plt.figure(figsize=(6, 3.5))
sns.histplot(data=raw, x="age", bins=8, kde=True)
plt.title("Age Distribution")
plt.tight_layout()
plt.show()
```

### 3.3 地區 x 週別熱圖（監測常用）

```python
heat = raw.groupby(["location", "epi_week"]).size().unstack(fill_value=0)

plt.figure(figsize=(7, 3.5))
sns.heatmap(heat, annot=True, fmt="d", cmap="Reds")
plt.title("Cases Heatmap (Location x Epi Week)")
plt.tight_layout()
plt.show()
```

## Step 4: `plotly` 互動圖（簡報友善）

```python
import plotly.express as px

daily_df = daily.reset_index()
daily_df.columns = ["date_onset", "cases"]
fig = px.line(daily_df, x="date_onset", y="cases", markers=True, title="Interactive Epidemic Trend")
fig.show()
```

## 圖表解讀重點

- 流行曲線看「峰值時間」與「上升/下降速度」。
- 排序長條圖看「高負擔地區」。
- 熱圖看「哪個地區在何時異常升高」。
- 直方圖看「年齡分布是否偏態」。

## 常見錯誤（新手最容易踩）

- 日期欄位沒轉成 datetime，導致時間順序亂掉。
- 忽略分母（人口）就直接比較地區病例數。
- 圖表標題與軸標籤不完整，讀者難解讀。
- 顏色過多且無意義，反而降低可讀性。

## 練習題

1. 用 `matplotlib` 畫一張你自己的 epidemic curve。
2. 用 `seaborn` 畫地區病例排序圖，並標出最大值。
3. 用 `plotly` 畫互動折線圖，加入 marker。

## 最小可執行環境命令

```bash
uv sync
uv run jupyter lab
```

## 練習本

- 作業版：[`notebooks/exercises/02_data_wrangling_exercise.ipynb`](../../notebooks/exercises/02_data_wrangling_exercise.ipynb)
- 解答版：[`notebooks/exercises/02_data_wrangling_solution.ipynb`](../../notebooks/exercises/02_data_wrangling_solution.ipynb)
- 圖表大全：[`notebooks/02_visualization_epi_charts.ipynb`](../../notebooks/02_visualization_epi_charts.ipynb)
