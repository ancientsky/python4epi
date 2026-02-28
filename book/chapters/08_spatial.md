# 08 空間流病：哪個樓層翼區最危險？

## 你將學到

- 按 **floor × wing** 計算侵襲率，辨識高風險區域
- 用 seaborn **heatmap** 呈現樓層翼區的侵襲率分布
- 按 **room** 計算每間房的侵襲率，繪製 **spot map**
- 用 **GeoJSON + Plotly** 畫地理 choropleth（概念延伸）
- 空間分析常見陷阱與 debug checklist

## 情境故事

長官問：**「在哪裡最嚴重？」**

松柏護理之家有 **3 層樓 × 2 翼區（A / B）**，共 280 位住民。
你需要畫出空間分布圖，找出哪些樓層翼區侵襲率最高。
如果特定翼區明顯偏高，可能暗示那裡的水源系統（蓮蓬頭、熱水管線）是傳播途徑。

---

## Part 1：樓層翼區侵襲率（`08_spatial_rates.ipynb`）

### Step 1 — 資料準備

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
```

### Step 2 — floor × wing 侵襲率

```python
spatial = df.groupby(["floor", "wing"]).agg(
    total=("case_id", "count"),
    infected=("infected", "sum"),
).reset_index()
spatial["attack_rate"] = (spatial["infected"] / spatial["total"] * 100).round(1)
print(spatial)
```

### Step 3 — 侵襲率熱力圖

```python
heatmap_data = spatial.pivot(index="floor", columns="wing", values="attack_rate")
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlOrRd")
plt.title("侵襲率 (%) by Floor × Wing")
plt.show()
```

> **觀察**：2F-A、2F-B、3F-B 侵襲率超過 50%，明顯高於 1F。
> 這些翼區是否共用同一熱水系統？值得進一步調查水源。

### Step 4 — 每間房侵襲率

按 `room` 計算侵襲率，找出最危險的房間。

```python
room_stats = df.groupby("room").agg(
    total=("case_id", "count"),
    infected=("infected", "sum"),
).reset_index()
room_stats["attack_rate"] = (room_stats["infected"] / room_stats["total"] * 100).round(1)
```

### Step 5 — 樓層翼區 spot map（bubble chart）

用散點圖模擬護理之家平面圖：每個房間一個圓點，大小 = 住民數，顏色 = 侵襲率。

```python
# 從 room 名稱 (e.g. "2A-03") 解析出 floor, wing, room_num
room_stats["floor_num"] = room_stats["room"].str[0].astype(int)
room_stats["wing_code"] = room_stats["room"].str[1]
room_stats["room_num"] = room_stats["room"].str.split("-").str[1].astype(int)

# X 軸 = room_num, Y 軸 = floor (A 翼在左, B 翼在右)
room_stats["x"] = room_stats.apply(
    lambda r: r["room_num"] if r["wing_code"] == "A" else r["room_num"] + 30, axis=1
)

fig, ax = plt.subplots(figsize=(12, 5))
sc = ax.scatter(
    room_stats["x"], room_stats["floor_num"],
    s=room_stats["total"] * 40,
    c=room_stats["attack_rate"], cmap="YlOrRd",
    edgecolors="black", linewidth=0.5, alpha=0.8,
)
plt.colorbar(sc, label="侵襲率 (%)")
ax.set_title("Spot Map — 每間房的侵襲率")
plt.show()
```

---

## Part 2：Choropleth 地圖概念（`08_spatial_choropleth.ipynb`）

雖然本案是護理之家內部分析，但 choropleth 是空間流病的核心技能。
我們保留用 `admin_areas.geojson` 示範 GeoJSON choropleth 的做法。

### 概念：分級著色地圖

```python
import json
import plotly.express as px

# 讀取行政區邊界
with open("data/synthetic/admin_areas.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# 地區病例率
pop = pd.read_csv("data/synthetic/location_population.csv")
cases_by_loc = pd.read_csv("data/synthetic/line_list.csv") \
    .groupby("location").size().rename("cases").reset_index()
rate = pop.merge(cases_by_loc, on="location", how="left").fillna({"cases": 0})
rate["incidence_per_100k"] = rate["cases"] / rate["population"] * 100000

# Choropleth
fig = px.choropleth(
    rate, geojson=geojson,
    locations="location",
    featureidkey="properties.location",
    color="incidence_per_100k",
    color_continuous_scale="Reds",
    title="Incidence per 100k by Location",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()
```

### Debug Checklist

1. `locations` 欄位是否與 GeoJSON `featureidkey` 值完全一致
2. 資料表是否有重複或空值的區域代碼
3. CRS（座標系統）是否一致
4. 每個區域是否都有對應的病例率
5. 是否有 outlier 讓色帶幾乎看不出差異（可改用對數尺度）

```python
# 快速檢查 ID 一致性
geo_ids = {f["properties"]["location"].strip() for f in geojson["features"]}
data_ids = set(rate["location"].astype(str).str.strip())
print("Only in data:", sorted(data_ids - geo_ids))
print("Only in geojson:", sorted(geo_ids - data_ids))
```

---

## 練習題

- 作業版：[`08_spatial_exercise.ipynb`](../exercises/08_spatial_exercise.ipynb)
- 解答版（講師）：[`08_spatial_solution.ipynb`](../solutions/08_spatial_solution.ipynb)

## 常見誤用

| 錯誤 | 正確做法 |
|------|---------|
| 只看病例數，不看分母 | 一定要算「侵襲率 = 病例 / 住民」 |
| 房間大小不同但圓點一樣大 | 圓點大小應反映住民數 |
| GeoJSON ID 與資料不一致 | 先做字串比對，確認 ID 吻合 |
| 不同時間窗混在同一張圖 | 統一分析時間段 |

## 下一步

空間分析告訴我們「在哪裡」最嚴重。
下一章（Ch09），我們追問更難的問題：**發病後，誰的存活時間比較長？哪些因子影響預後？** → 存活分析。
