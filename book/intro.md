# Epi With Python — 用 Python 學流行病學

## 一通電話，一場調查

> 週五下午四點，你接到衛生局的電話：
>
> 「松柏護理之家有多名住民出現肺炎症狀，疑似退伍軍人症群聚，請盡速前往調查。」
>
> 你帶著筆電趕到現場。280 位住民、3 層樓、2 翼區——面對這些數字，你打開了 Python⋯⋯

這本書的每一章都是這場調查的一個環節。你將從零開始，用 Python 一步步完成一場完整的疫情調查。

```{button-ref} chapters/00_guide
:ref-type: doc
:color: primary
:expand:
:class: sd-fs-5 sd-font-weight-bold

翻到 Ch00，接起那通電話 →
```

## 這場調查的資料

全書使用同一份合成資料集：**松柏護理之家退伍軍人症群聚事件**

::::{grid} 2 2 3 3
:gutter: 3

:::{grid-item-card} 280
:text-align: center
住民總數
:::

:::{grid-item-card} 121
:text-align: center
感染人數（侵襲率 43.2%）
:::

:::{grid-item-card} 19
:text-align: center
死亡人數（致死率 15.7%）
:::

:::{grid-item-card} 32
:text-align: center
資料欄位（人口學／共病／暴露／臨床／結果）
:::

:::{grid-item-card} 3 × 2
:text-align: center
3 層樓 × 2 翼區（A/B）
:::

:::{grid-item-card} 17 天
:text-align: center
發病期間 2026-01-12 至 01-28
:::

::::

## 故事線：五幕疫調

::::{grid} 1 1 2 3
:gutter: 3

:::{grid-item-card} 🎬 第一幕：接獲通報
**Ch00–02**
^^^
導讀、Python 基礎、資料處理與視覺化。接起電話，架好工具，讀進 280 筆 line list 開始整理。
:::

:::{grid-item-card} 🔬 第二幕：從描述到推論
**Ch03–04**
^^^
2×2 表、風險比與卡方檢定——淋浴是不是危險因子？產出第一份 SitRep 給長官。
:::

:::{grid-item-card} 🕵️ 第三幕：深入分析
**Ch05–08**
^^^
分層分析與干擾因子、邏輯斯迴歸、時間序列預測、空間流病——哪裡最危險？為什麼？
:::

:::{grid-item-card} 🧠 第四幕：進階建模
**Ch09–12**
^^^
存活分析、機器學習、深度學習、因果推論——從預測重症到釐清淋浴暴露的因果效應。
:::

:::{grid-item-card} 📋 第五幕：收尾與實戰
**Ch13–14**
^^^
可重現研究與完整疫調報告——讓同事一鍵重現你的分析，從接到通報走到結案報告。
:::

:::{grid-item-card} 📚 附錄與練習
**Ch15–17**
^^^
術語對照表、資料集欄位字典、套件速查，以及 14 組作業與解答。
:::

::::

## 適合誰

- **零基礎學員**：從 Python 語法開始，逐步進入流行病學分析
- **公衛研究生**：學習用程式取代 Excel 做疫調分析
- **現職流行病學家**：從傳統工具轉型 Python 工作流
- **對傳染病有興趣的人**：透過真實感的案例學習分析思維

## 如何使用

### 線上閱讀：兩個版本

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🎓 學生版
課文 + 作業（不含解答）
+++
```{button-link} https://ancientsky.github.io/python4epi/
:color: primary
:expand:
開啟學生版
```
:::

:::{grid-item-card} 👩‍🏫 教師版
課文 + 作業 + 解答
+++
```{button-link} https://ancientsky.github.io/python4epi/instructor/
:color: secondary
:expand:
開啟教師版
```
:::

::::

每個 notebook 頁面右上角都有 **Open in Colab** 按鈕，也可以在本機執行：

```bash
uv sync && uv run jupyter lab
```

Google Colab 上不需安裝任何東西——每個 notebook 頂部都有自動偵測 Colab 的 setup cell。

### 建議學習順序

按章節順序走——每一章的分析結果會引出下一章的問題。這就是真實疫調的節奏。

## 語言與術語

- 內文以**繁體中文**撰寫，技術名詞保留英文；右上角可切換 **English** 版本
- 流行病學術語採用**台灣標準譯名**（例如：侵襲率、致死率、信賴區間）
- 完整術語對照表見 {doc}`Ch15 附錄 <chapters/15_appendix>`

## 開始吧

翻到 Ch00，接起那通電話。
