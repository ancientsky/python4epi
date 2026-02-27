# 06 空間流病

## 你將學到

- 地區層級病例率計算
- 用 `GeoJSON + Plotly` 畫 choropleth
- 解讀空間圖時的分母陷阱

## 情境故事

你要向地方政府說明「哪幾區病例率較高」，並以地圖方式清楚展示風險分布。

## 最小可執行程式碼

```python
import pandas as pd

pop = pd.read_csv("data/synthetic/location_population.csv")
cases = pd.read_csv("data/synthetic/line_list.csv").groupby("location").size().rename("cases").reset_index()
rate = pop.merge(cases, on="location", how="left").fillna({"cases": 0})
rate["incidence_per_100k"] = rate["cases"] / rate["population"] * 100000
print(rate)
```

## Choropleth（GeoJSON）完整流程

```python
import json
import plotly.express as px

with open("data/synthetic/admin_areas.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

fig = px.choropleth(
    rate,
    geojson=geojson,
    locations="location",
    featureidkey="properties.location",
    color="incidence_per_100k",
    color_continuous_scale="Reds",
    title="Incidence per 100k by Location (Choropleth)",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()
```

## 你會用到的欄位對應

- `locations="location"`：資料表中的地區代碼
- `featureidkey="properties.location"`：GeoJSON 裡對應欄位
- `color="incidence_per_100k"`：地圖著色依據

## 練習題

1. 加入「最近 7 天病例率」欄位，改成用新欄位著色。
2. 嘗試把色帶從 `Reds` 改成 `Viridis`，觀察可讀性差異。
3. 比較病例數排序與病例率排序差異。

## 常見誤用

- 只看病例數，不看人口分母。
- `locations` 和 GeoJSON 欄位值不一致，導致地圖空白。
- 用不同時間窗資料混在同一張圖比較。

## Mapping Pitfalls（地圖常見陷阱）

### 1) CRS 不一致（座標系統不一致）

- 現象：地圖位置偏移、疊圖錯位。
- 原因：邊界資料與點位資料不是同一座標系統（常見 `EPSG:4326` vs Web Mercator）。
- 處理：統一轉成同一 CRS，再進行視覺化。

### 2) 區域代碼對不起來（ID mismatch）

- 現象：部分區域沒有顏色或整張 choropleth 空白。
- 原因：`locations` 欄位與 `featureidkey` 指向值不一致（大小寫、空白、命名不同）。
- 處理：先做字串標準化（trim + upper/lower），再比對差集。

### 3) 邊界缺漏或無效幾何（invalid geometry）

- 現象：某些區域不顯示、圖層報錯。
- 原因：GeoJSON 幾何缺失或多邊形結構錯誤。
- 處理：先檢查 feature 數量、名稱是否完整，再做 geometry validation。

## 快速 Debug Checklist

1. `locations` 欄位是否與 GeoJSON `featureidkey` 的值完全一致。
2. 地圖資料是否有重複區域代碼或空值。
3. CRS 是否一致（若有空間疊圖需求）。
4. 每個區域是否都有對應病例率。
5. 是否有 outlier 讓色帶幾乎看不出差異（可改分段或對數尺度）。

```python
import json

with open("data/synthetic/admin_areas.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

geo_ids = {feat["properties"]["location"].strip().upper() for feat in geojson["features"]}
data_ids = {x.strip().upper() for x in rate["location"].astype(str)}

print("Only in data:", sorted(data_ids - geo_ids))
print("Only in geojson:", sorted(geo_ids - data_ids))
print("Any missing rate values:", rate["incidence_per_100k"].isna().any())
```

## 常用圖表（空間流病）

- 排序條圖：比較地區病例率
- 分級著色地圖（choropleth）：展示空間風險
- 互動地圖：給決策會議快速探索

## 練習本

- 作業版：[`notebooks/exercises/06_spatial_exercise.ipynb`](../../notebooks/exercises/06_spatial_exercise.ipynb)
- 解答版：[`notebooks/exercises/06_spatial_solution.ipynb`](../../notebooks/exercises/06_spatial_solution.ipynb)
- 地圖示範：[`notebooks/06_spatial_choropleth.ipynb`](../../notebooks/06_spatial_choropleth.ipynb)
