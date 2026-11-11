---
title: "Mabuhay!（歡迎！）"
description: "Bantay Python 是給菲律賓疾病監測人員的免費入門課程：與一位你學會檢查的 AI 副駕駛一起學 Python、保護病患隱私，並打造一份疫情儀表板。"
---

:::{div}
:class: ph-hero
**菲律賓特別版 · Epi With Python**

## Bantay Python

從一疊紙本通報單，到市長一個畫面就能看懂的疫情儀表板。不需要任何程式基礎。你負責帶來流行病學專業；AI 副駕駛負責寫出程式碼的初稿；**你要學會讀懂它、執行它、檢查它。**

{button}`Sakay na!（上車囉！）開始這趟旅程 → <chapters/00_start_here.md>`
:::

*Bantay* 的意思是守望、看顧。這正是監測的本質：守望一個社區，讓問題及早被看見、被迅速回應。這門課為你的工作再多添一項工具。

## 你將打造什麼

到最後一章，你會做出 **Bantay Santa Luz 儀表板**：一個可以在任何瀏覽器開啟（離線也行）的單一 HTML 檔，可以用電子郵件寄出，或分享給地方衛生委員會（Local Health Board）。上面的每一個數字，都來自你讀過、檢查過的程式碼。

::::{grid} 1 2 3 3

:::{card} 重點數字卡
鉤端螺旋體病（leptospirosis）與登革熱的病例數、死亡數與致死率，一眼看清。
:::

:::{card} 流行曲線
依發病日或發病週統計病例數，讓疫情的形狀自己說故事。
:::

:::{card} Barangay 地圖
在 24 個 barangay（描籠涯，菲律賓最基層的行政區，類似台灣的村里）的地圖上，呈現每 10,000 居民的侵襲率，而不是原始病例數。
:::

:::{card} 警戒閾值
今年每週的登革熱病例數，對照同一季節的常態水準。
:::

:::{card} 7-1-7 成績單
每個事件多快被偵測、通報與回應。
:::

:::{card} 隱私頁尾
小格遮蔽，不含姓名與住址，附上資料來源與日期。
:::
::::

你會在[第 09 章](chapters/09_dashboard.md)完成它。在那之前，每一章都會替它添上一塊拼圖。

:::{div}
:class: ph-banderitas
:::

## 認識主角群

:::::{div}
:class: ph-cast
::::{grid} 2 3 3 3

:::{card} Maya
![Maya Dela Cruz，疾病監測專員，手拿記事板](chapters/images/cast_maya.svg)

*疾病監測專員（DSO），CESU*

「Ate Maya」（瑪雅姊）。護理師，第一份疾病監測專員（DSO）工作做到第四個月。擅長與人相處、處理紙本表單，從沒寫過程式。她會和你一起學。
:::

:::{card} Doc Mon
![Ramon Bautista 醫師，省級流行病學家，戴著眼鏡](chapters/images/cast_doc_mon.svg)

*省級流行病學家，PESU*

Ramon Bautista 醫師，FETP 畢業，是 Maya 的導師。總是問：「分母呢？病例定義呢？誰看得到這個檔案？」
:::

:::{card} Tala
![Tala，AI 寫程式助理，畫成一顆微笑的星星](chapters/images/cast_tala.svg)

*AI 寫程式助理*

*Tala* 是明亮的星星。又快又親切又樂於幫忙，有時也會很有自信地講錯。這本書兩面都會讓你看到。
:::

:::{card} Aling Nena
![Aling Nena Ramos，村里衛生員，手拿手機](chapters/images/cast_aling_nena.svg)

*村里衛生員（Barangay Health Worker, BHW），Ilog*

第一個察覺不對勁的人。她提醒大家：每一列資料都是一位鄰居。
:::

:::{card} Jun
![Jun Villanueva，資料文書人員，戴著耳機、拿著隨身碟](chapters/images/cast_jun.svg)

*市衛生局資訊與文書人員*

共用雲端硬碟的守門人，也是一堆超級凌亂試算表的來源。
:::
::::
:::::

## 故事

```{figure} chapters/images/scene_flood_riverside.svg
:alt: 颱風過後被洪水淹沒的河岸 barangay。男人涉水搬運殘骸，經過高腳屋；附近雨中漂著一艘小船。
:width: 100%
颱風 Amihan 過後的 Santa Luz（虛構的城市、虛構的颱風）。
```

**2026 年 7 月 18 日星期六**，颱風 Amihan 在 Kalinaw 省的 Santa Luz 市登陸。Marilag 河溢堤，八個河岸 barangay 在及腰的洪水中泡了三天。男人們涉水清理殘骸與水溝。

一週後，Aling Nena 傳訊息給市流行病學與監測單位（CESU）：Ilog 的好幾位男性發燒、眼睛紅、小腿痛。看起來是**鉤端螺旋體病（leptospirosis）**，一種細菌感染，人們因為接觸被受感染動物（尤其是老鼠）尿液汙染的水或土壤而感染。Maya 的通報單越堆越高。接著，積水孳生蚊子，每週的**登革熱**病例也跟著攀升。

Maya 有一份試算表、一個死線，卻沒有分析人員。Doc Mon 的建議是：*「問 Tala，但它給你的每一樣東西都要檢查。」*

## 數字看 Santa Luz

以下是這個故事虛構資料的重點數字。你會用自己的程式碼，重現每一個數字。

:::::{div}
:class: ph-stat
::::{grid} 2 2 4 4

:::{card} 186,000
人，分布在 24 個 barangay
:::

:::{card} 449.1 mm
颱風 Amihan 那一週的降雨量
:::

:::{card} 637
Jun 匯出的原始 line list（造冊）列數
:::

:::{card} 618
清理後的病例數
:::

:::{card} 230
鉤端螺旋體病病例
:::

:::{card} 388
登革熱病例
:::

:::{card} 8.7%
鉤端螺旋體病致死率（20 人死亡）
:::

:::{card} 33
登革熱超過流行閾值的第一週病例數
:::
::::
:::::

所有病例都是截至 2026 年 9 月 30 日資料凍結日前，通報到 CESU 的病例。

## 路線圖

這本書像一趟搭吉普尼（jeepney）的旅程，分四幕、共十二站。從起點上車；每一站都建立在上一站之上。

:::{div}
:class: ph-wide
```{figure} chapters/images/route_map_zh.svg
:alt: 一條吉普尼路線經過十二站，從 Mabuhay 到第 00 至 10 章，以顏色分成四幕。
:width: 100%
四幕：收到通報、來數一數、守望、呈現成果。
```
:::

:::{div}
:class: ph-route ph-act-1
**I · May ulat!**（有通報！）

- [00 從這裡開始：你、Colab 與 AI 副駕駛](chapters/00_start_here.md)
- [01 Kumusta, Python?（你好，Python）](chapters/01_python_with_ai.md)
- [02 隱私優先：每一列都是鄰居](chapters/02_privacy_first.md)
:::

:::{div}
:class: ph-route ph-act-2
**II · Bilangin natin**（來數一數）

- [03 從雜亂的造冊到乾淨的資料](chapters/03_clean_linelist.md)
- [04 時間、地點、人](chapters/04_time_place_person.md)
- [05 找出感染源](chapters/05_find_the_source.md)
:::

:::{div}
:class: ph-route ph-act-3
**III · Bantay**（守望）

- [06 訊號、閾值與 7-1-7](chapters/06_signals_and_thresholds.md)
- [07 下個月的登革熱：用 TimesFM 預測](chapters/07_forecast_timesfm.md)
- [08 在哪裡？地圖](chapters/08_maps.md)
:::

:::{div}
:class: ph-route ph-act-4
**IV · Ipakita**（呈現成果）

- [09 打造 Bantay Santa Luz 儀表板](chapters/09_dashboard.md)
- [10 疫情摘要、檢核表與下一步](chapters/10_wrap_up.md)
:::

## 這門課適合誰

這門課寫給在菲律賓從事監測工作、而且**從沒寫過程式**的人：疾病監測專員（DSO）、流行病學與監測單位（ESU）的護理師、第一線的 FETP（野外流行病學訓練計畫）學員，以及村里衛生員的督導。只要你會填病例調查表、會用試算表，就準備好了。

你需要一個網頁瀏覽器、一個免費的 Google 帳號（用來使用 Colab，第 00 章會說明），以及一個你的單位允許使用的 AI 助理。不需要安裝任何東西。

**每一章怎麼進行。** 一幕短短的故事場景、一個搭配圖片的觀念、Maya 輸入的提示詞與回傳的程式碼、一個教你如何**檢查**的方塊、一個小遊戲，以及帶回家的 *baon*（帶走重點）。然後，你在筆記本裡自己把一切跑一遍。留意紅色的 **Tala 搞錯了**方塊：它們展示 AI 助理真實會犯的錯誤，以及 Maya 怎麼抓出來。

## 故事是虛構的，系統是真實的

:::{admonition} 虛構與真實
:class: note
**虛構的：** Santa Luz 市、Kalinaw 省、Marilag 河、颱風 Amihan、故事裡的每一個人，以及 Santa Luz 資料集裡的每一個姓名、電話、住址和數字。原始 line list（造冊）裡的姓名是假的，但刻意做得像真的，讓你可以安全地練習隱私保護。這本書裡沒有任何真實病患。

**真實的：** 故事背後的監測系統。法定傳染病透過 PIDSR（菲律賓整合性疾病監測與應變系統）與其 EDCS 資訊系統通報，事件則透過事件監測與應變（Event-based Surveillance and Response, ESR）通報；依據[《法定傳染病與公共衛生關注健康事件強制通報法》（RA 11332）](https://lawphil.net/statutes/repacts/ra2019/ra_11332_2019.html)及其[2020 年修訂施行細則](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf)，通報由醫療機構逐級上傳，經市、鄉鎮、省、區的流行病學與監測單位，抵達 DOH（菲律賓衛生部）流行病學局。書中的真實法律、系統與統計數字，都附有來源連結。
:::

## 更大一本書的一部分

*Bantay Python* 是 [**Epi With Python**](https://ancientsky.github.io/python4epi/) 的菲律賓特別版。完整版是一本免費開放的書，透過調查一間護理之家的群突發，教你用 Python 學傳染病流行病學，從基礎一路到統計、地圖與機器學習。讀完這裡之後，它就是下一趟旅程。

{button}`Sakay na!（上車囉！）從這裡開始 → <chapters/00_start_here.md>`
