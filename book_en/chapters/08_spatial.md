# 08 空間流病：哪個樓層翼區最危險？

## 你將學到

- 按 **floor × wing** 計算侵襲率，辨識高風險區域
- 用 seaborn **heatmap** 呈現樓層翼區的侵襲率分布
- 按 **room** 計算每間房的侵襲率，繪製 **spot map**
- 看懂 `groupby().agg()` / `pivot()` / scatter 座標設計的邏輯
- 知道什麼情況下選熱力圖、選 spot map、或選 choropleth
- 觀察到空間差異後，如何進一步分析（CFR、暴露因子比較）
- 用 **GeoJSON + Plotly** 畫地理 choropleth（概念延伸）
- 空間分析常見陷阱與 debug checklist

## 情境故事

長官問：**「在哪裡最嚴重？」**

松柏護理之家有 **3 層樓 × 2 翼區（A / B）**，共 280 位住民。
你需要畫出空間分布圖，找出哪些樓層翼區侵襲率最高。
如果特定翼區明顯偏高，可能暗示那裡的水源系統（蓮蓬頭、熱水管線）是傳播途徑。

---

## 核心概念

### 空間分析的三個層次

不同規模的空間問題，需要不同工具。

```{figure} images/spatial_analysis_levels.svg
:name: spatial-analysis-levels
:alt: 空間分析三個層次：建築內部、行政區、全球
:width: 100%

空間分析從建築內部到全球分三個尺度，每層對應不同的視覺化工具。
```

### 什麼時候用哪種圖？

```{figure} images/spatial_chart_decision.svg
:name: spatial-chart-decision
:alt: 空間視覺化決策圖
:width: 100%

根據資料結構選擇最適合的空間視覺化方式。本章 Part 1 使用熱力圖和 Spot Map；Part 2 延伸到 Choropleth。
```

---

## Part 1：樓層翼區侵襲率（`08_spatial_rates.ipynb`）

### Step 1 — 資料準備

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
df["died"]     = (df["outcome"] == "dead").astype(int)
```

> **逐行拆解**
>
> - `df["clinical_severity"] != "not_ill"` 找出所有「有症狀或確診」的住民，結果是 True/False 序列
> - `.astype(int)` 把 True → 1、False → 0，建立 **感染旗標**（indicator variable）
> - `df["outcome"] == "dead"` 同理建立 **死亡旗標**
> - 旗標欄位的好處：之後可以直接對它做 `.sum()`（加總 1 = 計算人數）或 `.mean()`（平均 = 計算比例）

### Step 2 — floor × wing 侵襲率

```python
spatial = df.groupby(["floor", "wing"]).agg(
    total    = ("case_id",   "count"),
    infected = ("infected",  "sum"),
    died     = ("died",      "sum"),
).reset_index()
spatial["attack_rate"] = (spatial["infected"] / spatial["total"] * 100).round(1)
spatial["cfr"]         = (spatial["died"] / spatial["infected"] * 100).round(1)
```

> **逐行拆解：`groupby().agg()`**
>
> | 程式碼片段 | 白話意思 |
> |---|---|
> | `groupby(["floor", "wing"])` | 「把資料依 floor 和 wing 兩個欄位分組」 |
> | `agg(total=("case_id","count"))` | 「在每個組裡，數 case_id 的筆數 → 存成 total 欄」 |
> | `agg(infected=("infected","sum"))` | 「在每個組裡，把 infected 旗標加總 → 存成 infected 欄」（旗標加總 = 感染人數）|
> | `agg(died=("died","sum"))` | 同理，計算每組死亡人數 |
> | `.reset_index()` | 把分組鍵（floor、wing）從 DataFrame 的「索引」變回普通欄位，方便後續操作 |
>
> **為什麼要用 `agg()` 而不是三次 `groupby()`？**
> `agg()` 一次算出所有指標，程式碼更簡潔，速度也更快。
>
> `agg()` 語法公式：`新欄位名 = ("來源欄位", "統計函數")`，統計函數常用 `"count"`、`"sum"`、`"mean"`、`"max"`、`"min"`。

**解讀輸出**

執行後你會看到一張 6 × 5 的表格（3 層 × 2 翼 = 6 組）。
讀法：`attack_rate` 是侵襲率（越高代表那個翼區感染越嚴重），`cfr` 是致死率（感染者中死亡的比例）。

### Step 3 — 侵襲率熱力圖

```python
heatmap_ar = spatial.pivot(index="floor", columns="wing", values="attack_rate")
sns.heatmap(heatmap_ar, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={"label": "%"})
plt.title("侵襲率 (%) by Floor × Wing")
```

> **逐行拆解**
>
> - `pivot(index="floor", columns="wing", values="attack_rate")`
>   把「長表」（每行是一個 floor-wing 組合）轉成「矩陣」（行 = floor，列 = wing，格子 = 侵襲率）。
>   heatmap 需要矩陣格式才能畫色塊，這一行是關鍵前處理。
> - `annot=True`：在每個色塊上顯示數值（不然只有顏色沒有數字）
> - `fmt=".1f"`：數值格式化為一位小數
> - `cmap="YlOrRd"`：色板從黃（低）到橘（中）到紅（高），直覺對應危險程度
>
> **何時用熱力圖？**
> 分組變數剛好是**兩個類別**（這裡是 floor × wing），天然形成矩陣 → 熱力圖最直覺。
> 如果只有一個類別變數，用長條圖更合適。

### Step 4 — 每間房侵襲率

```python
room_stats = df.groupby("room").agg(
    total    = ("case_id",  "count"),
    infected = ("infected", "sum"),
).reset_index()
room_stats["attack_rate"] = (room_stats["infected"] / room_stats["total"] * 100).round(1)

# 解析 room 名稱 "2A-03" → floor_num=2, wing_code="A", room_num=3
room_stats["floor_num"] = room_stats["room"].str[0].astype(int)
room_stats["wing_code"] = room_stats["room"].str[1]
room_stats["room_num"]  = room_stats["room"].str.split("-").str[1].astype(int)
```

> **逐行拆解：字串解析**
>
> 房間代號格式是 `"2A-03"`（樓層 + 翼區 + 連字號 + 房間號）。
>
> | 操作 | 結果（以 "2A-03" 為例） |
> |---|---|
> | `room.str[0]` | `"2"` → 第 0 個字元 = 樓層 |
> | `room.str[1]` | `"A"` → 第 1 個字元 = 翼區 |
> | `room.str.split("-").str[1]` | `"03"` → 以 `-` 切割後取第二段 = 房間號 |
> | `.astype(int)` | `2`, `3` → 轉成整數，才能當座標用 |
>
> **為什麼要解析，而不是直接用 `room` 字串？**
> 畫 Spot Map 時需要 x/y 數值座標。字串 "2A-03" 無法直接放在座標軸上，需要拆解成數字才行。

### Step 5 — 樓層翼區 spot map（bubble chart）

```python
max_room_a = room_stats[room_stats["wing_code"] == "A"]["room_num"].max()
gap = 5  # A 翼和 B 翼之間留 5 個單位的間隔

room_stats["x"] = room_stats.apply(
    lambda r: r["room_num"] if r["wing_code"] == "A"
              else r["room_num"] + max_room_a + gap,
    axis=1,
)

fig, ax = plt.subplots(figsize=(14, 5))
sc = ax.scatter(
    room_stats["x"],
    room_stats["floor_num"],
    s = room_stats["total"] * 50,       # 圓點大小 = 住民數 × 縮放因子
    c = room_stats["attack_rate"],      # 顏色 = 侵襲率
    cmap="YlOrRd",
    edgecolors="black", linewidth=0.5, alpha=0.8,
)
plt.colorbar(sc, label="侵襲率 (%)")
```

> **逐行拆解**
>
> **為什麼需要 x offset？**
> 護理之家有 A 翼和 B 翼。如果兩翼的房間號都從 01 開始，直接用 `room_num` 當 x 座標，A 翼和 B 翼的點會疊在一起。
> 解法：B 翼的 x = B 翼房間號 + A 翼最大房間號 + gap，這樣兩翼就分開排列，模擬真實平面圖的左右佈局。
>
> | 參數 | 代表什麼 |
> |---|---|
> | `x = room_stats["x"]` | 房間的水平位置（A 翼靠左、B 翼靠右）|
> | `y = room_stats["floor_num"]` | 房間所在樓層（y 軸 = 樓層）|
> | `s = total × 50` | 圓點面積 ∝ 住民數（住民多的房間點較大）|
> | `c = attack_rate` | 圓點顏色對應侵襲率（越紅越危險）|
>
> **何時用 Spot Map？**
> 每個觀察單元（這裡是「房間」）可以對應到 **x/y 位置**（或可以推算出來）時，Spot Map 最合適。
> 它能直接呈現「哪裡聚集了高風險點」，比熱力圖更精細。

```{figure} images/spatial_spot_map_guide.svg
:name: spatial-spot-map-guide
:alt: Spot Map 讀圖指南
:width: 100%

Spot Map 讀圖四步驟：顏色找群聚、大小看可信度、左右比翼區、上下比樓層。
```

### Step 6 — 翼區侵襲率排序條圖

```python
spatial["label"] = spatial["floor"].astype(str) + "F-" + spatial["wing"]
spatial_sorted = spatial.sort_values("attack_rate", ascending=True)
ax.barh(spatial_sorted["label"], spatial_sorted["attack_rate"],
        color=["#e34a33" if ar > 50 else "#2c7fb8" for ar in spatial_sorted["attack_rate"]])
```

> 排序水平條圖讓高風險翼區一目了然。顏色條件式上色（>50% 用紅色）突出需要優先處理的區域。
> 最右側的翼區 = 最危險，環境採樣和調查資源應優先分配到那裡。

---

### 進階：發現翼區差異後，下一步怎麼做？

找到高侵襲率翼區只是第一步。疫調員接下來需要回答：**「為什麼那個翼區比較嚴重？」**

**方向 1：比較致死率（CFR）空間分布**

侵襲率高的翼區，死亡風險是否也比較高？還是只是感染率高、但病情相似？

```python
# 已在 notebook Step 2 的 spatial 表格中計算 cfr
# 用 sns.heatmap 畫致死率熱力圖（notebook 中 Step 3 示範）
heatmap_cfr = spatial.pivot(index="floor", columns="wing", values="cfr")
sns.heatmap(heatmap_cfr, annot=True, fmt=".1f", cmap="Reds")
```

**方向 2：比較特定暴露因子的空間分布**

退伍軍人病的主要傳播途徑是受汙染的熱水霧化（蓮蓬頭、按摩浴缸）。
如果某翼區侵襲率高，那個翼區的淋浴使用率是否也特別高？

```python
# 各翼區淋浴使用率
shower_by_wing = df.groupby("wing").agg(
    total        = ("case_id",     "count"),
    shower_users = ("shower_use",  "sum"),
).reset_index()
shower_by_wing["shower_pct"] = (shower_by_wing["shower_users"] / shower_by_wing["total"] * 100).round(1)
print(shower_by_wing)
```

**方向 3：環境採樣優先順序**

空間分析的最終目的之一是指導環境採樣：
- 侵襲率最高的翼區 → 優先採集蓮蓬頭、熱水管水樣
- 侵襲率低但相鄰翼區高 → 確認管線是否共用
- 發現孤立的高侵襲率房間 → 可能有個別的暴露源（如個人使用的加濕器）

---

## Part 2：Choropleth 地圖（`08_spatial_choropleth.ipynb`）

Choropleth（分級著色地圖）是社區層級疫調的核心技能。本 notebook 使用**真實政府開放資料**：
- **地圖邊界**：[國土測繪中心縣市界線 SHP (TWD97 EPSG:3824)](https://maps.nlsc.gov.tw)
- **疫情資料**：[疾管署退伍軍人病地區年齡性別統計表（2003–）](https://od.cdc.gov.tw)

### 台/臺 正規化

製作 Choropleth 最容易踩的坑之一：**台/臺字形不一致**。

| 縣市 | 台（俗字）| 臺（正體，政府公文用字）|
|---|---|---|
| 北部 | 台北市 | **臺北市** |
| 中部 | 台中市 | **臺中市** |
| 南部 | 台南市 | **臺南市** |
| 東部 | 台東縣 | **臺東縣** |

其他縣市（新北、桃園、高雄、嘉義…）**沒有台/臺差異**。

```python
TAI_NORMALIZE = {
    "台北市": "臺北市",  "台中市": "臺中市",
    "台南市": "臺南市",  "台東縣": "臺東縣",
    # 2010 年改制：台北縣 → 新北市，台中縣/市 → 臺中市 …
    "臺北縣": "新北市",  "台北縣": "新北市",
    "臺中縣": "臺中市",  "高雄縣": "高雄市",
    "桃園縣": "桃園市",
}
def normalize_county(name):
    return TAI_NORMALIZE.get(str(name).strip(), str(name).strip())
```

JOIN 前必須對 SHP 和 CDC CSV **雙邊都套用**這個函數，否則地圖上會出現大量空白。

### 工作流程

```python
# 1. 下載 SHP（ZIP）→ 解壓縮 → geopandas.read_file()
gdf = gpd.read_file(shp_path).to_crs(epsg=4326)

# 2. 自動偵測縣市名稱欄位（NLSC SHP 欄位名稱依版本而異）
# 3. 下載 CDC CSV → 偵測欄位 → 台/臺 正規化

# 4. ID 比對（最重要的 debug 步驟）
shp_counties  = set(gdf[county_col].apply(normalize_county))
data_counties = set(df["county"].unique())
print("只在 SHP：", sorted(shp_counties - data_counties))  # 地圖空白
print("只在資料：", sorted(data_counties - shp_counties))   # 不顯示

# 5. 按年度彙總 + 人口標準化 → 每十萬人發生率
annual = df.groupby(["year","county"])["cases"].sum().reset_index()
annual["rate_per_100k"] = annual["cases"] / annual["county"].map(COUNTY_POP) * 100_000

# 6. 靜態 Choropleth（最新年度）
gdf_merged = gdf.merge(latest, left_on="county_norm", right_on="county", how="left")
gdf_merged.plot(column="rate_per_100k", cmap="Reds", legend=True, ax=ax)

# 7. 動態 Choropleth（年度動畫 → GIF）
anim = FuncAnimation(fig, update_func, frames=years, interval=800)
anim.save("animation.gif", writer="pillow", fps=1, dpi=80)
```

> **為什麼用 GeoPandas + matplotlib 而不是 Plotly？**
> SHP 格式需要 `geopandas.read_file()` 讀取，而 GeoPandas 本身就能直接用 `.plot()` 畫 choropleth。
> 動畫（`FuncAnimation`）也需要 matplotlib。Plotly 適合 GeoJSON + 互動式地圖；GeoPandas 適合 SHP + 靜態/動畫圖。

### 每十萬人發生率 vs 絕對病例數

人口多的縣市（如臺北市 253 萬人）絕對病例數自然多，但不代表風險比人口少的縣市高。
比較縣市時**一定要用每十萬人發生率**：

```
發生率（/10萬）= 確定病例數 / 縣市人口 × 100,000
```

---

## 練習題

- 作業版：[`08_spatial_exercise.ipynb`](exercises/08_spatial_exercise.ipynb)
- 解答版（講師）：[`08_spatial_solution.ipynb`](solutions/08_spatial_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/08_spatial_solution.ipynb>)

## 常見誤用

| 錯誤 | 正確做法 |
|------|---------|
| 只看病例數，不看分母 | 一定要算「侵襲率 = 病例 / 住民」 |
| 房間大小不同但圓點一樣大 | Spot Map 圓點大小應反映住民數 |
| 圓點大小沒意義，只看顏色 | 住民數少的房間（如 1/1 = 100%）侵襲率不可靠，不能與大房間直接比較 |
| GeoJSON ID 與資料不一致 | 先做字串比對（`set.difference()`），確認 ID 吻合 |
| 不同時間窗混在同一張圖 | 統一分析時間段 |
| 把空間群聚當成因果 | Ecological fallacy：翼區高侵襲率只是假設，需要暴露因子分析才能確認原因 |

## 下一步

空間分析告訴我們「在哪裡」最嚴重。
下一章（Ch09），我們追問更難的問題：**發病後，誰的存活時間比較長？哪些因子影響預後？** → 存活分析。
