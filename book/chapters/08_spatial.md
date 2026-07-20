# 08 空間流病：哪個樓層翼區最危險？

## 你將學到

- 按 **floor × wing** 計算侵襲率，辨識高風險區域
- 用 seaborn **heatmap** 呈現樓層翼區的侵襲率分布
- 按 **room** 計算每間房的侵襲率，繪製 **spot map**
- 看懂 `groupby().agg()` / `pivot()` / scatter 座標設計的邏輯
- 知道什麼情況下選熱力圖、選 spot map、或選 choropleth
- 觀察到空間差異後，如何進一步分析（CFR、暴露因子比較）
- 用 **GeoJSON + Plotly** 畫地理 choropleth（概念延伸）
- 用 **空間統計**檢定群聚是真是假：全域 **Moran's I**、局部 **LISA**（HH/LL/HL/LH 四象限）、熱點 **Getis-Ord Gi\***
- 認識**空間權重**（Queen 接壤 / KNN）、掃描統計（SaTScan）與疾病製圖平滑（Empirical Bayes / BYM）的概念
- 空間分析常見陷阱與 debug checklist（含 MAUP、權重敏感度）

## 情境故事

長官問：**「在哪裡最嚴重？」**

松柏護理之家有 **3 層樓 × 2 翼區（A / B）**，共 280 位住民。
你需要畫出空間分布圖，找出哪些樓層翼區侵襲率最高。
如果特定翼區明顯偏高，可能暗示那裡的水源系統（蓮蓬頭、熱水管線）是傳播途徑。

---

## 🗺️ 超白話特別篇：用「教室感冒座位圖」看懂空間流病

> 空間自相關、Moran's I、熱點分析……這章的名詞聽起來很硬？別怕。這一段先把護理之家放一邊，用一張**教室座位圖**——看誰在咳嗽——把「空間流病到底在幹嘛」講到讓國中生也秒懂。學會這一招，後面的地圖和 Moran's I 全都是它的放大版。

### 後排一角三個人都在咳，是「傳染串」還是「湊巧」？

感冒會傳給隔壁同學，所以會咳嗽的座位常常**黏成一團**。某天老師發現**後排右下角一小群人都在咳**，心裡一驚：這是**真的一條傳染串**，還是**剛好各自在家中鏢、只是湊巧坐附近**？

**空間流病**就是在回答這種問題——把「感覺很擠」變成「統計上真的擠」。

### 為什麼「地點」會有意義？——近的東西比較像

> 🧲 **地理界的萬有引力（Tobler 第一定律）**：**「近的東西比較像。」** 你隔壁同學的感冒、你家隔壁的房價，都比對街的更像。疾病也是——會傳染的病，發病的人就會在空間上「物以類聚」。所以「在哪裡」不是廢話，它藏著**傳播的線索**。

但先講一個鐵則：

> 📏 **看地點，一定要先算「率」，不是比「人數」。** 人多的地方案例本來就多（廢話）。要比的是**侵襲率**（這一區生病的**比例**）——這跟 Ch03 烤肉「別忘了分母」是同一件事，只是搬到地圖上。

### 陷阱：一片紅≠真群聚（人腦會腦補）

> 🌌 **看星座的陷阱**：人腦是台「找圖案的機器」——把隨機的星星硬連成獵戶座。看著色地圖也一樣，你**一定**會「看到」群聚，但那可能只是顏色隨機排出來的錯覺。

怎麼分辨真假？流行病學家的方法很暴力，但超級聰明：

> 🔀 **洗牌檢定**：把咳嗽的標籤**從座位上剪下來、隨機洗牌、重新貼回去**，重複很多次（例如 1000 次）。如果**真實地圖**比這些「亂貼」的版本**擠很多**，那這個群聚就是真的；如果跟亂貼的差不多，那就是你腦補的。

```{figure} images/shuffle_test_intuition.svg
:name: fig-shuffle-test
:alt: 左邊是真實教室座位圖，咳嗽的紅色座位黏成右下角一團（相鄰咳嗽對=6）；右邊是把咳嗽標籤洗牌後散開的版本（相鄰咳嗽對≈2）；Moran's I 量的就是真實比洗牌多擠多少，得到 p 值
:width: 100%

左：真實地圖，咳嗽黏成一團；右：洗牌後散開了。**Moran's I 量的，就是「真實」比「洗牌一千次」擠多少 → p 值。**
```

### 動手玩玩看：親手做一次「洗牌檢定」

```python
import numpy as np

# 教室座位 5x5；有咳嗽的同學標 1。真實：右下角一群人黏在一起咳
seats = np.zeros((5, 5), dtype=int)
for r, c in [(3, 3), (3, 4), (4, 3), (4, 4), (2, 4), (4, 2)]:
    seats[r, c] = 1

def adjacent_cough_pairs(grid):
    """數『相鄰兩個座位都在咳』的配對數（只看上下左右）"""
    pairs = 0
    for r in range(5):
        for c in range(5):
            if grid[r, c] == 1:
                if c + 1 < 5 and grid[r, c + 1] == 1: pairs += 1   # 右邊鄰居
                if r + 1 < 5 and grid[r + 1, c] == 1: pairs += 1   # 下面鄰居
    return pairs

real = adjacent_cough_pairs(seats)

# 洗牌：把咳嗽標籤隨機重貼 200 次，每次數相鄰咳嗽對
rng = np.random.default_rng(8)
flat = seats.flatten()
shuffled = np.array([adjacent_cough_pairs(rng.permutation(flat).reshape(5, 5))
                     for _ in range(200)])
p = (shuffled >= real).mean()

print(f"真實地圖：相鄰咳嗽對 = {real}")
print(f"洗牌 200 次：平均 = {shuffled.mean():.1f}（最多 {shuffled.max()}）")
print(f"洗牌後 ≥ 真實 的比例 = p ≈ {p:.3f}")
print("→ 真實比亂貼的擠很多，p 很小 → 這是真的群聚！" if p < 0.05 else "→ 看不出顯著群聚")
```

跑出來會看到：

```text
真實地圖：相鄰咳嗽對 = 6
洗牌 200 次：平均 = 2.1（最多 5）
洗牌後 ≥ 真實 的比例 = p ≈ 0.000
→ 真實比亂貼的擠很多，p 很小 → 這是真的群聚！
```

> 💡 **這就是 Moran's I 的靈魂**：本章正文用 `esda` 一行算出來的 Moran's I 和 p 值，骨子裡就是這個「洗牌比一比」——只是它用更漂亮的公式，還會分辨「熱區核心（LISA）」和「顯著熱點（Gi\*）」。

### ⚠️ 幾個必記的但書

1. **先算率再比**：一律用侵襲率 / 每十萬人發生率，別直接比案例數。
2. **群聚 ≠ 原因（生態謬誤）**：找到熱區只回答了「在**哪裡**」，不是「**為什麼**」。熱區是問題的**路標**，不是答案——要回頭做暴露分析才知道兇手（是共用水源？還是那區剛好都吹到同一台冷氣？）。
3. **洗牌 p 值只跟「隨機」比**：它證明「不是巧合」，但不證明因果、也不告訴你原因。
4. **換鄰居定義 / 換空間單元，答案會變**：Queen 接壤 vs KNN、縣市 vs 村里（MAUP），結果可能整個翻掉；離島用「接壤」會 0 鄰居。
5. **小人口的率會亂跳**：分母小的地方（如連江縣），多 1 個案例率就暴衝——要用**平滑**，別直接畫原始率。

### 回到真實：座位圖 → 台灣地圖

把「教室座位」換成「台灣縣市」、「咳嗽」換成「登革熱發生率」、「相鄰座位」換成「接壤縣市」——你剛剛學的每一招（先算率、洗牌檢定、群聚≠原因）**就是本章 Part 3 在全台縣市資料上做的事**。現在往下看那些地圖、Moran's I、LISA 和 Gi\*，是不是突然變親切了？😉

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

先讀入清洗後的病例資料，再建立「有沒有感染」「有沒有死亡」這兩個 0/1 旗標欄位，之後所有分組統計都靠它們。

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

> **逐行拆解**
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `spatial["floor"].astype(str) + "F-" + spatial["wing"]` | 把數字樓層轉成字串，跟翼區代碼併起來，組成 `"1F-A"` 這種好讀的標籤 |
> | `sort_values("attack_rate", ascending=True)` | 依侵襲率由小到大排序，讓 `barh()` 畫出來時最高風險的翼區自然排在最上面 |
> | `color=[... for ar in ...]` | 用 list comprehension 逐一檢查每個翼區的侵襲率，超過 50% 上紅色、其餘上藍色 |
>
> 💡 `ascending=True` 搭配 `barh()` 是常見組合：水平長條圖由下往上畫，遞增排序後最大值自然落在最上方、最顯眼。

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

> 🔑 這裡重用 Step 3 的 `pivot()` + `sns.heatmap()` 套路，只把 `values` 換成 `cfr`——同一張矩陣、換一個欄位，就能比較「感染多的地方」和「死得多的地方」是不是同一群人。

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

> 🔑 這是 Step 2 `groupby().agg()` 的縮小版：只用一個分組欄位（`wing`），邏輯完全相同——先數總人數，再對旗標欄位加總，最後相除得到百分比。

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

> 💡 `TAI_NORMALIZE.get(key, key)` 是常見的「查表、查不到就用原字串」寫法：字典裡列出的舊縣市名/台臺變體會被轉換，沒列出的（如新北市、桃園市）原封不動地回傳。

JOIN 前必須對 SHP 和 CDC CSV **雙邊都套用**這個函數，否則地圖上會出現大量空白。

### 工作流程

以下把整個 Choropleth 流程串成七個步驟——從下載邊界檔到輸出動畫地圖：

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

> **逐行拆解**
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `gpd.read_file(shp_path).to_crs(epsg=4326)` | 讀入 SHP 檔案，並把座標系統轉成 WGS84（EPSG:4326）—— 網頁地圖（Plotly、Leaflet）都吃這種經緯度座標 |
> | `shp_counties - data_counties` | 集合相減：找出「SHP 有、疫情資料沒有」的縣市名 —— 這些地方地圖會空白 |
> | `data_counties - shp_counties` | 反過來找出「疫情資料有、SHP 沒有」的縣市名 —— 這些資料會被靜靜丟掉、不會顯示 |
> | `groupby(["year","county"])["cases"].sum()` | 依年度和縣市加總病例數，才能算出每年、每縣市各自的發生率 |
> | `cases / county.map(COUNTY_POP) * 100_000` | 除以人口數再乘以 100,000，把病例數換算成「每十萬人發生率」，才能公平比較大小縣市 |
> | `gdf.merge(latest, left_on="county_norm", right_on="county", how="left")` | 用正規化後的縣市名稱把地圖（`gdf`）和疫情資料（`latest`）合併，`how="left"` 保留所有地圖上的縣市，即使沒有對應資料也不會消失 |
> | `gdf_merged.plot(column="rate_per_100k", cmap="Reds", legend=True)` | GeoPandas 的 `.plot()` 直接依 `rate_per_100k` 欄位上色，畫出 choropleth |
>
> ⚠️ 第 4 步的 ID 比對是整個 choropleth 最容易出包的地方：merge 前如果 SHP 和資料的縣市名稱對不上（例如台/臺沒有正規化），合併出來的列會變成 NaN，地圖上就會出現一大片空白——而且**不會報錯**。務必先印出 `shp_counties - data_counties` 這種差集，肉眼確認完全吻合再往下做。

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

## Part 3：空間統計分析（`08_spatial_statistics.ipynb`）

Part 1、Part 2 教你**畫**空間分布圖。但地圖上出現一片紅，你怎麼知道那是**真的群聚**，還是眼睛自己腦補的？這一段用**空間統計**把「感覺」變成「證據」，回答三個問題：全臺是不是有群聚（**Moran's I**）、熱區核心在哪（**LISA**）、哪裡是顯著熱點（**Gi\***）。

> 🦟 **換個舞台：為什麼改用登革熱？**
> 退伍軍人病是「一棟樓」的故事，單一建築不適合縣市級空間統計。所以這一段換上**登革熱 × 全臺縣市**——這正是台灣空間流病最經典的應用（熱點年年落在南部）。方法一樣能**縮小尺度**，拿去在一座城市的各棟大樓找 Legionella 熱區。（notebook 的病例數為**合成教學資料**。）

### 為什麼不能「只用眼睛」看地圖？

> 🌌 **看星座的陷阱**：人腦是台「找圖案的機器」——把隨機的星星硬連成獵戶座。看著色地圖也一樣，你**一定**會「看到」群聚，但那可能只是隨機的顏色排列。

空間統計就是一把尺，量出「這個群聚是真的，還是我腦補的」。背後是地理鐵律 **Tobler 第一定律：「近的東西比較像」**。所以我們問的不是「有沒有群聚」，而是「**這相似程度，有沒有超過『隨機本來就會有』的程度**」。做法很直白：把各縣市的數字**剪下來、洗牌、隨機重貼**很多次，看真實地圖有沒有比洗出來的更集中。

### 第一步：定義「鄰居」——空間權重（spatial weights）

要說「跟鄰居像不像」，得先白紙黑字定義**誰是鄰居**。

```{figure} images/spatial_weights_neighbors.svg
:name: fig-spatial-weights
:alt: 空間權重示意：焦點縣市用綠線連到接壤的鄰居（Queen 接壤），權重矩陣 W 是「誰是誰的鄰居」點名表、row-standardized 讓鄰居各得 1/k；離島在海上用接壤定義得到 0 鄰居，改用 KNN 跨海抓最近的 k 個
:width: 100%

**Queen 接壤**：邊界碰到（連一個角）就是鄰居。權重矩陣 $W$ 是「誰是誰的鄰居」點名表；`transform="r"` 讓每個縣市的鄰居權重加起來 = 1（公平投票）。**離島**用接壤會得到 0 鄰居 → 改用 **KNN**（抓最近的 k 個）。
```

```python
from libpysal.weights import Queen, KNN

w_all = Queen.from_dataframe(gdf, use_index=False)
print("接壤定義下『沒有鄰居』的縣市：",
      [gdf.iloc[i]["COUNTYNAME"] for i in w_all.islands])   # 金門、澎湖、連江

# 群聚分析聚焦本島 19 個相連縣市；離島留到「平滑」再處理
main = gdf[~gdf["is_inset"]].reset_index(drop=True)
w = Queen.from_dataframe(main, use_index=False)
w.transform = "r"   # row-standardized
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `Queen.from_dataframe(gdf, use_index=False)` | 用 **Queen 接壤**（邊界碰到、含只碰一個角）自動建出「誰是誰的鄰居」權重矩陣 W |
> | `w_all.islands` | 列出**沒有任何鄰居**的縣市（離島）——它們在海上，接壤定義下誰都碰不到 |
> | `main = gdf[~gdf["is_inset"]]` | 聚焦本島 19 個相連縣市（離島留到平滑處理），免得離島的 0 鄰居壞了計算 |
> | `w.transform = "r"` | **row-standardized**：讓每個縣市的鄰居權重加起來 = 1，鄰居多的不會自動比較大聲（公平投票） |
>
> ⚠️ **換一種鄰居定義，答案就會變**——離島讓我們親眼看到這件事。這正是後面「權重敏感度」陷阱的現場。

### 第二步：全域 Moran's I —— 整張地圖的「物以類聚」指數

**全域 Moran's I** 用一個數字總結整座島：**I ≈ +1** 高聚高、低聚低（分區明顯）；**I ≈ 0** 隨機散布；**I ≈ −1** 高低相間（罕見）。光有 I 還不夠，要用**洗牌 p 值**確認不是巧合。

```python
from esda.moran import Moran

moran = Moran(main["rate"].values, w, permutations=999)
print(f"Moran's I = {moran.I:.3f}, p = {moran.p_sim:.4f}")   # ≈ 0.50, p < 0.05 → 有顯著群聚
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `Moran(main["rate"].values, w, permutations=999)` | 餵三樣：各縣市的**率**、剛剛的**鄰居權重 w**、**洗牌 999 次**。它算出全域 Moran's I，並把率剪下來洗 999 次當對照 |
> | `moran.I` | 全域指數：+1 物以類聚、0 隨機、−1 高低相間 |
> | `moran.p_sim` | **洗牌 p 值**：真實地圖的 I 比 999 次隨機洗牌高多少——< 0.05 才代表群聚不是碰巧 |
>
> 💡 **光看 I 不夠、要看 p_sim**：I = 0.5 看起來像有群聚，但要靠洗牌 p 值證明「這 0.5 不是隨機也會出現的」。只有 I 顯著，才值得往下做 LISA 找熱區核心。

### 第三步：局部 LISA —— 熱區核心到底在哪？

全域 Moran 給整座島**一個**分數；**LISA** 拉近鏡頭，問每一個縣市：「你跟你的鄰居，是哪一種關係？」同時看**自己的值**和**鄰居的平均值**，分成四象限：

```{figure} images/lisa_quadrants.svg
:name: fig-lisa-quadrants
:alt: LISA 四象限：橫軸是縣市自己的率、縱軸是鄰居平均率；HH 高-高（疫情震央）、LL 低-低（安全淨土）、HL 高-低與 LH 低-高是空間離群值；對角線是跟鄰居同調的群聚成員，反對角是唱反調的離群值
:width: 100%

橫軸 = 自己的率、縱軸 = 鄰居平均率。**HH**（震央）、**LL**（淨土）是「跟鄰居同調」的群聚成員；**HL**（孤島火苗）、**LH**（颱風眼）是「跟鄰居唱反調」的空間離群值——常是故事最有趣的地方。
```

```python
from esda.moran import Moran_Local

lisa = Moran_Local(main["rate"].values, w, permutations=999, seed=8)
# ⚠️ esda 象限編碼：.q 中 1=HH、2=LH、3=LL、4=HL（LH 是 2，不是 3！）
labels = {1: "HH 震央", 2: "LH 颱風眼", 3: "LL 淨土", 4: "HL 火苗"}
main["lisa"] = ["不顯著" if p >= 0.05 else labels[q]
                for q, p in zip(lisa.q, lisa.p_sim)]
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `Moran_Local(main["rate"].values, w, permutations=999, seed=8)` | 局部版：對**每一個**縣市各算一個 local Moran，同時看自己的率和鄰居平均率；`seed=8` 讓洗牌可重現 |
> | `lisa.q` | 每個縣市落在哪一象限的代碼——**esda 編碼是 1=HH、2=LH、3=LL、4=HL** |
> | `lisa.p_sim` | 每個縣市各自的洗牌 p 值（局部顯著性） |
> | `["不顯著" if p >= 0.05 else labels[q] ...]` | 先看顯著性：p ≥ 0.05 一律標「不顯著」，顯著的才翻成 HH/LH/LL/HL 標籤 |
>
> ⚠️ **最容易踩雷的是 `.q` 的編碼**：直覺會以為 1234 = HH/HL/LL/LH，但 esda 是 **1=HH、2=LH、3=LL、4=HL**（LH 是 2、不是 3！）。照對照表抄，別自己按順序填，否則「颱風眼」和「火苗」會標反。

在合成資料上，**臺南／高雄／嘉義**跳出來是 **HH 震央**，北部是 **LL 淨土**——南部登革熱熱區用統計坐實了。

### 第四步：熱點分析 Getis-Ord Gi\* —— 給長官看的熱區圖

> 🌡️ **紅外線熱像儀**：Gi\* 不管「你跟鄰居像不像」，只問「把你和鄰居圈成一圈，這一圈燙不燙？」輸出 **z 分數** = 燙了幾個標準差。跟 LISA 不同，Gi\* **沒有離群類別**，只給你一條紅到藍的溫度光譜，最適合做「哪裡優先派人」的熱區圖。

```python
from esda.getisord import G_Local

w_b = Queen.from_dataframe(main, use_index=False); w_b.transform = "B"
gi = G_Local(main["rate"].values, w_b, permutations=999, seed=8, star=True)
hot = main.loc[(gi.p_sim < 0.05) & (gi.Zs > 0), "COUNTYNAME"].tolist()   # 顯著熱點
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `w_b = Queen.from_dataframe(main); w_b.transform = "B"` | Gi\* 用 **binary（0/1）**權重（`"B"`），不做 row-standardize——它算「這一圈的總熱度」，不是平均 |
> | `G_Local(..., star=True)` | `star=True` = Gi\***（含自己）**：把焦點縣市自己也圈進「這一圈」一起算熱度 |
> | `gi.Zs` | 每個縣市的 z 分數：正=比整體平均熱、負=冷 |
> | `gi.p_sim` | 洗牌 p 值（小樣本要靠這個判顯著，不能只看 z 有沒有過 1.96） |
> | `(gi.p_sim < 0.05) & (gi.Zs > 0)` | **顯著熱點**的正確判準：p 值顯著**且** z 為正 |
>
> ⚠️ **別用 `Zs > 1.96` 硬篩熱點**：縣市只有 19 個，樣本太小時常態近似不準，要用**洗牌 p_sim** 判顯著，再用 **Zs 的正負號**分冷熱。冷熱點都顯著時，光看 z 的絕對值會把冷點也誤當熱點。

### 概念延伸：掃描統計與疾病製圖（平滑）

縣市層級最常用的就是上面三招。還有兩個更進階的工具，先建立概念（多半用 R 或專門軟體）：

- **📡 Kulldorff 掃描統計（SaTScan）**：在地圖上移動、放大圓圈，自動找「圈內特別多」的可疑集群，能抓不規則形狀、還能做時間-空間掃描。CDC 早期預警常用。工具：**SaTScan**、`rsatscan`。
- **📷 貝氏疾病製圖 / 平滑**：小人口的率**忽高忽低**（連江縣人口才 1.3 萬，多 1 例率就跳 7.7）。平滑「向鄰居借資訊」估出穩定風險。工具：**R-INLA**、`CARBayes`（BYM 模型）；Python 有 `esda.smoothing.Empirical_Bayes`。

### 判讀小抄（存起來）

**全域 Moran's I**

| 讀什麼 | 意思 |
|---|---|
| 正負號 | + 高聚高低聚低（群聚）；≈0 隨機；− 高低相間 |
| 大小 | 越接近 ±1 越強；期望值 ≈ −1/(n−1)（≈0）才是「無空間結構」 |
| p_sim | < 0.05 → 模式不是隨機。**只有 I 顯著才往下做 LISA** |

**LISA 四象限**（`.q`：1=HH、2=LH、3=LL、4=HL）

| 類別 | 白話 | 行動 |
|---|---|---|
| **HH** | 熱區核心（震央） | 全區作戰、找共同傳染源 |
| **LL** | 安全淨土 | 低優先、可當對照 |
| **HL** | 孤島火苗（離群值） | **立刻查**：獨立傳入？資料異常？ |
| **LH** | 颱風眼（離群值） | 高風險緩衝，快防守 / 找保護因子 |
| NS | `p_sim ≥ 0.05` | 不顯著，別解讀，塗灰 |

**Getis-Ord Gi\* z 分數**：`≥ +1.96` 顯著熱區、`≤ −1.96` 顯著冷區、中間不顯著（小樣本改看洗牌 `p_sim`）。

> **一句話分清 LISA vs Gi\***：LISA 回答「我是四種鄰里的**哪一種**（含唱反調的離群值）」；Gi\* 回答「我這一圈**有多燙**（只有冷熱、沒有離群）」。兩者互補。

完整可跑的程式、三張地圖（原始率、LISA 群聚圖、Gi\* 熱點圖）與平滑示範，見 [`08_spatial_statistics.ipynb`](notebooks/08_spatial_statistics.ipynb)。

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
| 只用眼睛判斷「有沒有群聚」 | 用 Moran's I + 洗牌 p 值檢定，區分真群聚與隨機錯覺 |
| 換空間單元（縣市↔村里）卻以為結論不變 | MAUP：改變面積單元，Moran's I 和熱區可能整個翻掉 |
| 只用一種鄰居定義就下結論 | 權重敏感度：Queen / KNN / k 值會移動結果，務必換一種檢查 |
| LISA/Gi\* 多個地區同時檢定不修正 | 多重比較：n 個地區＝n 次檢定，單一地區剛好顯著要存疑 |
| 直接畫小人口地區的原始率 | 小人口率不穩，應考慮 Empirical Bayes / 貝氏平滑 |

## 下一步

空間分析告訴我們「在哪裡」最嚴重。
下一章（Ch09），我們追問更難的問題：**發病後，誰的存活時間比較長？哪些因子影響預後？** → 存活分析。
