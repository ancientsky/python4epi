---
title: "08 在哪裡？地圖"
description: "Maya 把登革熱畫在 Santa Luz 的 24 個 barangay 上——比較病例數與侵襲率、分級切點與色盲友善配色、不穩定的小數字、一個悄悄弄丟兩個 barangay 的合併——接著畫出菲律賓真實的 18 個行政區地圖，最後做出一張可以安全公開的地圖。"
---

:::{div}
:class: ph-story
*9 月 30 日（週三）· 市長辦公室*

**市長：** Maya 姐，我不需要表格。你就告訴我：登革熱*在哪裡*？

**Maya：** Ilog 的病例最多，市長……

**Doc Mon：** Ilog 的人口也最多。居民在哪裡最*可能*得登革熱？那是另一張地圖。

**Aling Nena：** 還有，拜託——不要在我們家的位置上點點。大家會知道是誰家的孩子生病了。

> 登革熱在哪裡——我們要怎麼畫一張說真話、又不會指著任何人的地圖？
:::

```{figure} images/santa_luz_map_zh.svg
:alt: 虛構的 Santa Luz 市分成三個區帶：北邊是山區，沿著 Marilag 河的是河岸，南邊是沿海，並標出 CESU 與各衛生站。
:width: 100%
Santa Luz 市與它的三個區帶。這座城市、它的 24 個 barangay（描籠涯，菲律賓最基層的行政區，類似台灣的村里）和所有數字都是虛構的。
```

## 病例數還是侵襲率？

**面量圖（choropleth）**是依照一個數字，把每個區域塗上顏色的地圖。第一個決定是：要畫*哪一個*數字。

- **病例數**回答「工作量在哪裡？」：有多少病人、4S 小組要去多少戶人家。
- **侵襲率**回答「風險在哪裡？」：病例數 ÷ 人口 × 10,000，也就是居民成為病例的機率（每 10,000 人）。

在 Santa Luz，**Ilog**（河岸）的登革熱病例最多：31 例。但它同時也是人口最多的 barangay 之一，所以侵襲率是每 10,000 人 23.1 例。**Talaba**（沿海）只有 6,688 位居民，卻有 29 例：**每 10,000 人 43.4 例**，是最高的。接下來是 Buhangin，35.5。在病例數的地圖上，河岸最亮；在侵襲率的地圖上，沿海最亮。把原始病例數當成風險來畫地圖，是最常見的地圖錯誤之一。

:::{admonition} 問問 Tala
:class: ph-ask-tala
我有一個 GeoDataFrame `brgy`（24 列；欄位有 `barangay_id`、`barangay`、`band`、`population`、`geometry`），還有一份造冊 `ll`（每一列是一位病例；欄位有 `barangay_id`、`disease`）。虛構範例：`ll` 的列有 `("SL01", "dengue")`、`("SL01", "dengue")`、`("SL02", "leptospirosis")`。請依 `barangay_id` 計算登革熱病例數，**用 `barangay_id`** 把計數併進 `brgy`，沒有病例的 barangay 填 0，並新增 `attack_rate` = 病例數 / 人口 × 10,000。結果必須仍然是 24 列。
:::

:::{admonition} Tala 說
:class: ph-tala-says
```python
dengue_counts = ll[ll["disease"] == "dengue"].groupby("barangay_id").size().rename("cases")
brgy = brgy.merge(pop, on="barangay_id", how="left")
brgy = brgy.merge(dengue_counts, left_on="barangay_id", right_index=True, how="left")
brgy["cases"] = brgy["cases"].fillna(0).astype(int)        # 沒有病例的 barangay 是 0，不是缺值
brgy["attack_rate"] = brgy["cases"] / brgy["population"] * 10_000
```
:::

:::{admonition} 檢查一下
:class: ph-check
1. 合併之後仍是 **24 列**：`assert len(brgy) == 24`。
2. **總數**：各 barangay 的病例數加起來要等於全部 388 例登革熱。
3. **手算一個侵襲率**：Talaba，29 ÷ 6,688 × 10,000 = 43.4。
4. **那個零**：山區的 Bukid 沒有登革熱病例，所以 `groupby` 只給出 23 列。如果沒有 `fillna(0)`，Bukid 會變成空白（「沒有資料」），而不是 0。
:::

## 分級切點與顏色

面量圖通常會把數值分成幾個**級別**。切點不同，傳達的訊息就不同：

- **等距分級（equal interval）：** 各級的寬度相同（這裡每級約每 10,000 人 11 例）。分成 4 級時，只有 2 個 barangay 落在最高級。
- **分位數分級（quantile）：** 每一級有相同數量的 barangay（24 ÷ 4 = 6）。每種顏色都用得到，但相鄰兩級的數值可能很接近。

兩者都沒有絕對的對錯。要刻意地選，並且把切點寫在圖例上。

顏色同樣重要。請使用**循序式（sequential）**色盤，低值淺、高值深，例如 `YlOrRd` 或 `viridis`。讀者不用看圖例就能依序解讀，色盲也看得懂，黑白列印也不會失真。避免使用**彩虹**色盤（`jet`）：它沒有自然的順序，而且正中間那片亮黃色會把目光拉到*中等*的數值上。

:::{div}
:class: ph-game ph-game-map-paint
畫侵襲率，不要畫病例數；刻意選擇分級切點；使用由淺到深的色盤。
:::

## 小數字會亂跳

山區的 barangay 只有 3,000–5,000 位居民，病例也只有寥寥幾例。Maligaya 有 **1 例：每 10,000 人 3.0**。再多一例，就會變成兩倍的 6.1。筆記本 為每個侵襲率算出精確的 95% 信賴區間：Maligaya 是 0.1 到 16.9，Talaba 是 29.0 到 62.3。區間很寬，代表**不要光憑顏色就替那個 barangay 排名**。請把病例數加進滑鼠懸停的提示文字，或放在地圖旁的表格裡。

## 互動式地圖

在螢幕上，plotly 可以畫出同一張地圖，滑鼠移上去會顯示 barangay、區帶、病例數、人口與侵襲率。它需要以 GeoJSON 格式提供的多邊形，以及把每一列資料連到對應多邊形的鍵 `featureidkey="properties.barangay_id"`。我們不畫任何底圖：Santa Luz 是虛構的，它的座標刻意落在外海，所以絕不會被誤認為真實的地點。

:::{admonition} Tala 搞錯了
:class: ph-oops
Jun 傳來一份手打的、依 barangay **名稱**列出登革熱病例數的簡單表格。Tala 就**用名稱**把它併到地圖上。地圖看起來沒問題。但 Jun 把 `Santo Niño` 打成了 `Santo Nino`（沒有 ñ），把 `Tabing-Ilog` 打成了 `Tabing Ilog`（沒有連字號）。用內部合併（inner join）時，這兩列就這樣消失了：沒有錯誤，也沒有警告。兩個河岸 barangay，合計 41 例，會在市長的地圖上變成一片空白。

Maya 怎麼抓到的：

```python
merged = brgy[["barangay_id", "barangay", "geometry"]].merge(jun, on="barangay", how="inner")   # Tala 的合併
assert len(merged) == 24, f"join kept {len(merged)} of 24 barangays"
```

這個 assert 會失敗，訊息是 *"join kept 22 of 24 barangays"*，再用帶有 `indicator=True` 的外部合併（outer join），就能看出是哪兩個名稱對不上。解法：**用代碼**（`barangay_id`）**來合併**，絕不要用手打的名稱。[第 03 章](03_clean_linelist.md)示範了如何把雜亂的名稱轉成代碼。
:::

## 拉遠一點：18 個行政區

在簡報時，把整個國家秀出來會有幫助。`ph_regions.topo.json` 存有 18 個行政區**真實的**邊界，格式是 TopoJSON，一種比 GeoJSON 更精簡的表示法。`geopandas.read_file` 可以直接讀。我們用 PSGC 代碼 **`adm1_psgc`** 把 `ph_regions_stats.csv` 裡真實的統計數字併進來，並 assert 剛好 18 列。

筆記本 畫的是 **2024 年的人口密度**。NCR 每平方公里有 **22,015 人**，大約是第二名 CALABARZON（1,004）的 22 倍。如果用等寬分級，其他所有行政區都會是同一種顏色，所以我們改用分位數分級。密度是由 2024 年人口與土地面積算出來的，兩者都取自
[菲律賓行政區（維基百科）](https://en.wikipedia.org/wiki/Regions_of_the_Philippines)，透過本書的研究檔案引用。CSV 裡的每個數值都附有自己的來源網址；引用數字時，請一併引用來源。

用這個檔案畫出的每一張地圖，都要附上這行版權標示：*Boundaries: NAMRIA, PSA via OCHA COD-AB (CC BY-IGO); TopoJSON: faeldon/philippines-json-maps (MIT).*

這是一張真實國家的**背景**地圖。絕不要把虛構的 Santa Luz 畫在上面。

:::{admonition} 隱私停看聽
:class: ph-privacy
有病例的住戶**點狀圖（dot map）**，等於是把一份地址清單畫成點。任何認得那條街的人都能指出是哪一棟房子。在 CESU 內部，它可以用來引導 4S 小組。但在公開網頁上，它會讓鄰居被認出來，這正是[第 02 章](02_privacy_first.md)關切的事。公開地圖應顯示**彙總的區域**（barangay），即使如此，病例很少的 barangay 仍可能指向某個人。本書的規則是：**遮蔽 1–4 的數字**（顯示「<5」），同時也要遮蔽它們的**侵襲率**，因為侵襲率 × 人口就能把病例數算回來。在 Santa Luz，這會讓公開地圖上 24 個 barangay 中的 5 個被遮蔽。筆記本 把它們畫成斜線填滿，標示為「1–4 例：不顯示」。
:::

## 回到 lamok

地圖告訴 4S 小組*該去哪裡*。他們到了那裡要做的，是搜尋並清除孳生源：任何裝著乾淨靜水的容器。

```{figure} images/mosquito_4s_zh.svg
:alt: 圍繞著一隻斑蚊的對抗登革熱 4S：搜尋並清除孳生源、自我防護、及早就醫、只在疫情熱區配合噴藥。
:width: 100%
對抗登革熱的 4S。
```

:::{div}
:class: ph-game ph-game-lamok-patrol
4S：搜尋並清除孳生源（Search and destroy）、自我防護（Secure self-protection）、及早就醫（Seek early consultation）、只在疫情熱區配合噴藥（Support fogging）。
:::

:::{div}
:class: ph-game ph-game-quiz
**小測驗：地圖**

1. Ilog 的登革熱病例最多，Talaba 的侵襲率最高。居民的風險在哪裡最高？
   - Ilog — 它的病例最多，但居民也多很多。
   - ✓ Talaba — 侵襲率會除以有風險的人口。
2. 你合併後的地圖資料表只有 22 列，而不是 24 列。你該怎麼做？
   - 什麼都不用做，地圖還是畫得出來 — 現在有兩個 barangay 變成空白或消失了。
   - ✓ 找出對不上的名稱，改用 `barangay_id` 來合併。
3. 登革熱侵襲率地圖應該用哪一種色盤？
   - ✓ 由淺到深的循序式色盤 — 讀起來有順序，色盲也看得懂。
   - 彩虹色盤 — 它沒有自然的順序，還會凸顯中間的數值。
4. 某個 barangay 有 3 例。在公開地圖上你要顯示……
   - 病例數和侵襲率 — 小數字可能指向某個人。
   - ✓ 「<5」，而且不顯示侵襲率 — 侵襲率乘以人口就能把病例數算回來。
:::

:::{admonition} Baon（帶走重點）
:class: ph-baon
- 要看風險就畫**侵襲率**，看工作量才畫病例數。要說清楚你顯示的是哪一個。
- 用**代碼**合併、保留零病例的區域，並且用 `assert` 檢查列數。
- 循序式色盤、刻意選的切點、版權標示，而且公開的地圖不要出現未遮蔽的小格，也不要畫點。

開啟 筆記本：[](notebooks/08_maps.ipynb)
:::
