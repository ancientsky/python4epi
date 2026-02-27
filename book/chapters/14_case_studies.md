# 11 任務支線（Case Studies）

## 你將學到

- 如何把前面章節方法串成端到端任務
- 如何在有限資料下做實務決策分析
- 如何整理「可行動」的監測結論

## 情境故事

你負責某市登革熱週報，需要在 30 分鐘內回答三個問題：

1. 哪些地區病例率最高？
2. 本週是否有異常上升訊號？
3. 下週資源該優先投放到哪裡？

## 任務框架

1. 讀取並清理 line list。
2. 產生地區病例率表。
3. 產生近期趨勢與簡單預測。
4. 輸出行動建議（高、中、低風險區）。

## 最小可執行程式碼

```python
import pandas as pd

line = pd.read_csv("data/synthetic/line_list.csv", parse_dates=["date_onset"])
by_loc = line.groupby("location").size().rename("cases").reset_index()

pop = pd.DataFrame({
    "location": ["North", "South", "East", "West"],
    "population": [12000, 10000, 8000, 9000],
})

risk = by_loc.merge(pop, on="location", how="left")
risk["incidence_per_100k"] = risk["cases"] / risk["population"] * 100000
risk = risk.sort_values("incidence_per_100k", ascending=False)
print(risk)
```

## 建議輸出格式（給決策者）

- `Top 3` 高風險地區（依病例率）
- 最近 7 天病例變化方向（上升/持平/下降）
- 下週建議資源配置（檢驗、人力、衛教）

## 建議圖表組合（決策簡報版）

- 圖 1：經典流行曲線（每日病例 bar）
- 圖 2：地區病例率排序圖（bar）
- 圖 3：地區 x 週別熱圖（heatmap）
- 圖 4：互動趨勢圖（plotly line）
- 圖 5：地區 choropleth（GeoJSON）

```python
import json
import plotly.express as px

with open("data/synthetic/admin_areas.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

fig = px.choropleth(
    risk,
    geojson=geojson,
    locations="location",
    featureidkey="properties.location",
    color="incidence_per_100k",
    color_continuous_scale="Reds",
    title="Case Study Risk Map",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()
```

## 練習題

1. 加入年齡分層，找出高風險年齡帶。
2. 新增一個簡單異常偵測規則（如：高於過去 3 日均值 1.5 倍）。

## 常見誤用

- 直接用病例數排序當成風險排序。
- 沒有先確認資料更新延遲（report lag）就下結論。

## 練習本

- 作業版：[`notebooks/exercises/11_case_study_exercise.ipynb`](../../notebooks/exercises/11_case_study_exercise.ipynb)
- 解答版：[`notebooks/exercises/11_case_study_solution.ipynb`](../../notebooks/exercises/11_case_study_solution.ipynb)
