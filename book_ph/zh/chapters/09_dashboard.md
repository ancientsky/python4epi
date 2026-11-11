---
title: "09 打造 Bantay Santa Luz 儀表板"
description: "Maya 把十週的監測資料做成給地方衛生委員會看的一個獨立 HTML 畫面：關鍵數字、流行曲線、侵襲率地圖與登革熱閾值，並附上一道公開前檢查，擋下小格與逐筆個案資料。"
---

:::::{div}
:class: ph-story
*9 月 30 日（週三）· Santa Luz 市衛生局*

::::{div}
:class: ph-say-jun
**Jun：** Maya 姐，市長辦公室來電話了。地方衛生委員會週五開會。市長要的是「一個畫面，不要四十張投影片」。
::::

::::{div}
:class: ph-say-maya
**Maya：** 一個畫面？我有流行曲線、地圖、閾值圖、7-1-7 的表、病例對照研究的結果……
::::

::::{div}
:class: ph-say-mon
**Doc Mon：** 那就要取捨。委員只有兩分鐘。有多少、在哪裡、往上還是往下，以及我們要做什麼。還有 Maya——在我檢查過之前，任何東西都不准離開這間辦公室。
::::

::::{div}
:class: ph-say-tala
**Tala：** 我可以把全部放進一個 HTML 檔！要不要把完整的造冊也加進去，讓大家可以下載資料？
::::

> 我們要怎麼做出一個畫面，既回答委員會的問題，又保護畫面上的每一位鄰居？
:::::

**[開啟 Bantay Santa Luz 儀表板](/dashboard/)**——本章要做的完成品。它可以離線使用，在手機上看得到，也能印在紙上（一頁橫式）。Santa Luz 與上面的每一個數字，都是為了這門課虛構的。

## 好的儀表板回答什麼

**儀表板（dashboard）**是把最重要的數字與圖表放在同一頁，依固定時程更新，供必須做決定的人使用。它不是報告：沒有長篇文字，沒有方法學章節。它依序回答四個問題：

| 問題 | Santa Luz 畫面上用什麼回答 |
|---|---|
| **有多少？** | 關鍵數字方塊：病例數、死亡數、致死率、高於閾值的週數 |
| **在哪裡？** | 各 barangay（描籠涯，菲律賓最基層的行政區，類似台灣的村里）的**侵襲率**地圖（每 10,000 名居民的病例數），而不是原始病例數 |
| **往上還是往下？** | 流行曲線，以及每週登革熱病例數對照它的**流行閾值** |
| **我們要做什麼？** | 一份簡短、編了號的本週行動清單 |

誰受到影響（年齡與性別）、系統反應多快（7-1-7），以及鉤端螺旋體病群聚的成因（第 05 章的勝算比），接著以較小的篇幅呈現。

:::::{div}
:class: ph-stat
::::{grid} 2 2 4 4

:::{card} 618
截至 9 月 30 日通報的病例數（鉤端螺旋體病 230、登革熱 388）
:::

:::{card} 21
死亡數（鉤端螺旋體病 20、登革熱 1）
:::

:::{card} 8
自 W32 起，登革熱連續高於閾值的週數
:::

:::{card} 38%
40 起事件中，三項 7-1-7 目標皆達成的比例
:::
::::
:::::

```{figure} images/scene_cesu_office.svg
:alt: Maya 坐在市流行病學與監測單位（CESU）辦公室的書桌前，筆電螢幕上是上升的流行曲線，還有星星 Tala，旁邊有紙本表單、牆上的地圖與一台電風扇。
:width: 100%
十週的表單、資料清理與分析，變成一個畫面。Santa Luz 與它的 CESU 都是虛構的。
```

## 步驟 1：關鍵數字

Maya 從數字方塊開始。她描述欄位，並給三列虛構的資料。

:::{admonition} 問問 Tala
:class: ph-ask-tala
我有一個 pandas DataFrame `ll`，每一列是一位病例，欄位有 `case_id`、`disease`（`leptospirosis` 或 `dengue`）、`outcome`（`alive` 或 `died`）和 `hospitalised`（0/1）。虛構的列：`X-1, dengue, alive, 0` · `X-2, leptospirosis, died, 1` · `X-3, dengue, alive, 1`。請寫一個函式 `compute_kpis(ll)`，針對每一種疾病以及全市，回傳病例數、死亡數、住院數，以及致死率（%，取到小數一位）。
:::

:::{admonition} Tala 說
:class: ph-tala-says
```python
def compute_kpis(ll: pd.DataFrame) -> pd.DataFrame:
    """各疾病的病例數、死亡數、住院數與致死率（%），再加上全市總計列。"""
    kpis = ll.groupby("disease").agg(
        cases=("case_id", "size"),
        deaths=("outcome", lambda s: (s == "died").sum()),
        hospitalised=("hospitalised", "sum"),
    )
    kpis.loc["total"] = kpis.sum()
    kpis["cfr_pct"] = (100 * kpis["deaths"] / kpis["cases"]).round(1)
    return kpis
```
:::

:::{admonition} 檢查一下
:class: ph-check
1. 用 Tala 的三列虛構資料跑一次：登革熱必須是 2 例，鉤端螺旋體病的致死率是 100%。
2. 用第二種方式數死亡人數，`(ll["outcome"] == "died").sum()`，再和總計列比對。
3. 看清楚致死率（CFR）的**分母**：死亡數 ÷ *病例數*，而不是 ÷ 人口。Santa Luz 的數字：鉤端螺旋體病 20 ÷ 230 = **8.7%**，登革熱 1 ÷ 388 = **0.3%**。
:::

## 步驟 2：三張圖，一條規則

在 筆記本 裡，Maya 做了三張 Plotly 圖：依發病週別的**流行曲線**，並標出颱風 Amihan；登革熱侵襲率的**地圖**（Talaba 每 10,000 人 43.4 與 Buhangin 35.5 最高）；以及每週登革熱病例數對照**流行閾值**（2022–2025 年同一週的平均值 + 2 個標準差，見第 06 章）。用週，不用日：某一天只有 1 例，就等於洩漏了某個人的發病日。

每一張圖都遵守同一條規則，它被寫成一個函式：

```python
def suppress(counts: pd.Series | pd.DataFrame, threshold: int = 5) -> pd.Series | pd.DataFrame:
    """把 1 到 threshold - 1 的數字換成 '<5'（0 維持 0）。"""
    small = (counts > 0) & (counts < threshold)
    return counts.astype(object).mask(small, f"<{threshold}")
```

:::{admonition} 隱私停看聽
:class: ph-privacy
儀表板會離開辦公室，所以要把它當成公開資料。**小格遮蔽（small-cell suppression）**的意思是：在小群體（一個 barangay、一週、一個年齡組）中，遮蔽任何 1 到 4 的數字，並且不公布它的侵襲率，因為「3,000 人的 barangay 裡有一位 65 歲以上的病例」，鄰居叫得出名字。0 維持 0：它沒有描述任何人。整個期間的全市總數可以顯示，就像例行公報那樣。你們單位自己的公開規定與 2012 年的資料隱私法（Data Privacy Act, RA 10173）優先；這條規則是本課程使用的最低標準。
:::

## 步驟 3：一個獨立的 HTML 檔

**獨立（self-contained）**的 HTML 檔把需要的東西全都帶在身上：文字、樣式、資料和繪圖程式碼。它不需要網路就能開啟，可以從電子郵件或隨身碟打開。Python 的 `string.Template` 用 `$placeholders` 填入一個小小的頁面；每張 Plotly 圖用 `fig.to_html(full_html=False, ...)` 變成一段 HTML 片段，只有第一張帶有 Plotly 函式庫：

```python
figures = [fig.to_html(full_html=False, include_plotlyjs=(i == 0), config={"responsive": True})
           for i, fig in enumerate([fig_curve, fig_map, fig_thr])]
page_html = PAGE.substitute(
    title="Bantay Santa Luz",
    as_of=AS_OF,
    kpis="".join(f'<div class="kpi">{label}<b>{value}</b></div>' for label, value in tiles),
    figures="\n".join(figures),
    notes="".join(f"<li>{note}</li>" for note in notes),
)
```

筆記本 會把結果寫進你電腦的**暫存資料夾**（約 4.9 MB，大部分是 Plotly 函式庫），並印出它的位置。用瀏覽器開啟，再用手機開一次。「不需要網路」有一個例外：Plotly 的地圖第一次繪製時，會下載一份小小的世界輪廓檔，所以在這個簡化版裡，地圖區塊離線時會是空的。下面的完整儀表板自己畫地圖，完全不需要網路。

## 步驟 4：Doc Mon 的公開前檢查

Doc Mon 檢查表裡的某些項目，可以用程式碼每次在一秒內測完：

```python
def publish_check(page: str) -> list[str]:
    """回傳 Doc Mon 會擋下的問題（空清單代表可以公開）。"""
    problems = []
    if re.search(r"SLC-\d{4}", page):
        problems.append("發現病例編號：不得公開逐筆資料")
    for column in ["case_id", "date_onset", "date_report"]:
        if column in page:
            problems.append(f"發現造冊欄位 {column!r}")
    small = re.findall(r"<td>\s*[1-4]\s*</td>", page)
    if small:
        problems.append(f"{len(small)} 個表格儲存格是 1-4 例：請遮蔽")
    for must in ["資料截至", "資料說明", "合成資料"]:
        if must not in page:
            problems.append(f"缺少：{must!r}")
    return problems
```

Maya 的頁面通過了。然後市長的幕僚說想要「更多細節」。

:::{admonition} Tala 搞錯了
:class: ph-oops
Maya 請 Tala *加上依 barangay 與年齡組的病例表，再加一個下載資料的按鈕*。Tala 加了 `pd.crosstab(ll["barangay"], ll["age_group"])`——滿滿都是 1 和 2 的原始計數——還把 `ll.to_json()` 放進 `<script>` 裡：**整份造冊**，連同病例編號、年齡與確切的發病日，任何人用「檢視原始碼」都讀得到。頁面看起來跟原來一模一樣。但公開前檢查不一樣：它擋下了病例編號、三個造冊欄位與 55 個小格。解法是只公開彙總資料：一個較粗的表（區帶 × 年齡組），而且要遮蔽小格，完全不提供個案層級資料的下載。
:::

程式碼不可能檢查所有事情。檢查表的其餘部分仍須由人來做：

1. **只放彙總資料。** 沒有姓名、地址、電話、病例編號或個別病例的確切日期——不論是在頁面上，*還是*藏在它的程式碼裡。
2. **遮蔽小格**（1–4 → 「<5」，不列侵襲率），而且不要公布一個讓人能用減法把被遮蔽的格子算回來的總數。
3. **地圖上用侵襲率，不用病例數**，並寫明分母。
4. **誠實的座標軸：** 長條圖從 0 開始；不完整的最後一週要加註。
5. **資料說明：** 合成還是真實、來源、定義、遮蔽了什麼。
6. **「資料截至」日期**，同時標在畫面上與列印稿上。
7. **在手機上測試過**，並且由第二個人大聲唸過一遍。

:::{div}
:class: ph-game ph-game-publish-check
公開之前：沒有姓名或確切地址、遮蔽 1–4 的數字、不提供個案層級資料的下載、座標軸從 0 開始，並附上來源說明。
:::

## 完整的儀表板：同樣的想法，做得更深入

本站上的 [Bantay Santa Luz 儀表板](/dashboard/)，是由本書儲存庫裡的 `scripts/build_ph_dashboard.py` 建立的，步驟與你的 筆記本 相同：`load_data()`、`compute_kpis()`、`suppress_small_cells()`、`render_html()`。它在四個方面更進一步：

- **手繪圖表。** 一小段腳本用內嵌的一小塊數字畫出圖表，所以整個頁面不到 0.1 MB，可離線使用，也能印在一頁橫式紙張上。
- **更嚴格的遮蔽。** 當公布了總數，而某一欄只遮蔽了一個小格時，會再多遮蔽第二格（標示為 `x`），這樣就沒有人能用減法把那個小數字算回來。
- **更多面板。** 年齡與性別、7-1-7 時效與最常見的瓶頸、病例對照研究的勝算比，以及[第 07 章](07_forecast_timesfm.md)的 TimesFM 預測扇形圖（當它的快取預測存在時）。
- **三種語言、淺色與深色、鍵盤與觸控。**

筆記本 會匯入其中兩個函式，並檢查它們給出的關鍵數字與你的相同。

:::{div}
:class: ph-game ph-game-quiz
**小測驗：儀表板**

1. 委員會問「登革熱最嚴重的地方在哪裡？」。地圖上該放什麼？
   - 每個 barangay 的病例數 — 大的 barangay 看起來永遠最嚴重。
   - ✓ 每 10,000 名居民的病例數（侵襲率） — 它能公平地比較風險。
   - 每位病例的地址 — 絕不能放在公開畫面上。
2. 某個 barangay 有 3 例登革熱。公開的表格顯示什麼？
   - 3 和它的侵襲率 — 那可能指向某一個家庭。
   - ✓ 「<5」，而且不列侵襲率 — 1–4 的數字要遮蔽，侵襲率會把它洩漏回來。
   - 0 — 那是不實的。
3. 最後一週的長條比較低。登革熱在下降嗎？
   - 是的，長條比較低。
   - ✓ 還不知道 — 因為通報延遲，最後一週是不完整的。
4. Tala 提議做一個「下載資料」的按鈕，把造冊放在頁面裡。Doc Mon 說……
   - 檔案小的話就可以。
   - ✓ 不行 — 個案層級的資料絕不能放進公開頁面，即使藏在程式碼裡也不行。
:::

:::{admonition} Baon（帶走重點）
:class: ph-baon
- 儀表板要回答四個問題：有多少、在哪裡、往上還是往下、我們要做什麼。
- 每個小群體裡 1–4 的數字都要遮蔽，地圖用侵襲率，並蓋上「資料截至」的日期。
- 每次都跑公開前檢查；然後由人到手機上檢查一遍。

開啟 筆記本：[](notebooks/09_dashboard.ipynb) · [開啟儀表板](/dashboard/)
:::
