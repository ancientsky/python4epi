---
title: "06 訊號、閾值與 7-1-7"
description: "Maya 先認識菲律賓體系中疫情訊號從哪裡來，接著建立登革熱的流行閾值、畫出地方性流行通道、弄懂為什麼最新幾週看起來偏低，最後計算 7-1-7 時效。"
---

:::{div}
:class: ph-story
*8 月 12 日（週三）· Santa Luz 市流行病學與監測單位（CESU）辦公室*

**Aling Nena：** Maya 姐，鉤端螺旋體病慢慢退了。可是現在換成 *lamok*（蚊子）了——Baybay 的小朋友一直高燒，水桶裡全是孑孓。

**Maya：** 登革熱的通報單也越堆越高。這已經算群突發了嗎？還是 8 月本來就是這樣？

**Doc Mon：** 問得好。「很多」只是一種感覺，警戒閾值才是一個數字。而且警戒一拉響，時鐘就開始走了：七、一、七。

> 登革熱多到什麼程度才算要拉警報？而我們拉了警報之後，動作有多快？
:::

## 兩種訊號

**訊號（signal）**指的是任何可能代表疫情的跡象。菲律賓的體系用兩種方式蒐集訊號。

**指標型監測（indicator-based surveillance）**是透過例行通報，計算符合病例定義的病例數。這就是 **PIDSR**（Philippine Integrated Disease Surveillance and Response，菲律賓整合性疾病監測與應變系統）以及它的網路資訊系統 **EDCS**。疾病通報單位（醫院、鄉鎮衛生所 RHU、診所、檢驗室）要在 24 小時內通報第一類疾病，而第二類疾病（例如登革熱）則是每週通報一次
（[RA 11332 的 2020 年修訂施行細則](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf)）。
通報由醫療院所往上送到市或鎮的流行病學與監測單位（ESU），再到省級的 PESU、區域的 RESU，最後是衛生部（DOH）的流行病學局
（[WHO 聯合外部評核，2018](https://extranet.who.int/sph/sites/default/files/document-library/document/JEE%20Report%20Republic%20of%20the%20Philippines%202018.pdf)）。

**事件型監測（event-based surveillance）**則是撈出表單沒預先設計到的*異常事件*：一群生病的孩子、一則謠言、一則新聞、一封簡訊。DOH 把它稱為 **ESR**（Event-based Surveillance and Response，事件型監測與應變），自 2010 年起運作
（[WPSAR，2015](https://ojs.wpro.who.int/ojs/index.php/wpsar/article/download/368/578?inline=1)）。
由**村里衛生員（Barangay Health Worker, BHW）**在社區通報——就像 Aling Nena 做的那樣——2024 年曾在中呂宋部分地區試辦，而 2024 年的聯合外部評核把「讓它成為常規」列為優先事項
（[WHO JEE，2024](https://www.who.int/publications/i/item/9789240116795)）。

```{figure} images/reporting_ladder_zh.svg
:alt: 通報分成六個層級，從村里衛生員一路往上到衛生部流行病學局，回饋則沿著階梯往下傳。
:width: 100%
通報沿著階梯往上爬，回饋應該往下傳。每一階都要花時間。
```

每一階都要花時間。WHO 西太平洋區署指出，PIDSR 的登革熱資料有 **2 至 3 週的通報延遲**
（[WHO WPRO 登革熱情勢更新第 731 期，2025](https://cdn.who.int/media/docs/default-source/wpro---documents/emergency/surveillance/dengue/dengue_202510021edf3700-e2a6-4e48-8e7c-acd86a16d530.pdf?sfvrsn=ba2e2c46_1)）。
先記住這一點，後面會再回來談。

## 流行病學週

登革熱是按**流行病學週（morbidity week）**來計算的。我們的檔案採用 ISO 週：週一到週日，標示成像 `2026-W32`（2026 年 8 月 3 日至 9 日）這樣。它並不代表官方 PIDSR 曆法。`iso_year` 與 `iso_week` 兩個欄位讓我們能把不同年份的「同一週」對齊。資料從 2019-W01 到 2026-W39，而且是**合成資料**：Santa Luz、當地雨量與病例全是虛構的。

## 警戒閾值

**流行閾值（epidemic threshold）**要回答的是：*在平常的年份，這一週最高可以到多高？* 這個序列用的規則是：

1. 針對 ISO 週 *w*，取**基準年 2022–2025** 的第 *w*−1、*w*、*w*+1 週：4 年 × 3 週 = 12 個數字。
2. 閾值 = 這些數字的**平均值 + 2 個標準差**。
3. 排除異常年份。2019 年是流行年，2020–2021 年受 COVID-19 擾亂。基準必須描述*平常*的年份。

:::{admonition} 問問 Tala
:class: ph-ask-tala
我有一個 pandas DataFrame `weekly`，欄位有 `iso_year`、`iso_week`（1–53）與 `cases`。虛構的範例列：`(2022, 31, 9)`、`(2022, 32, 12)`、`(2023, 32, 7)`。請對 1 到 53 的每個 ISO 週 w，計算流行閾值 = 只取 2022–2025 年第 w−1、w、w+1 週 `cases` 的平均值 + 2 × 樣本標準差（第 1 週的窗口要接到第 52 週）。請依週別回傳結果。然後告訴我 2026 年第一個病例數高於閾值的週別。程式碼請寫得讓初學者看得懂。
:::

:::{admonition} Tala 說
:class: ph-tala-says
```python
BASELINE_YEARS = [2022, 2023, 2024, 2025]   # 只用平常的年份：不含 2019、2020、2021，絕對不含 2026


def window_weeks(week):
    # 第 w-1、w、w+1 週；第 1 週接到 52，第 52 週接到 1（第 53 週用 52、53、1）
    if week == 53:
        return {52, 53, 1}
    return {(week - 2) % 52 + 1, week, week % 52 + 1}


def epidemic_threshold(weekly, years):
    base = weekly[weekly["iso_year"].isin(years)]
    rows = {}
    for week in range(1, 54):
        values = base.loc[base["iso_week"].isin(window_weeks(week)), "cases"]
        rows[week] = {"n_values": len(values), "baseline_mean": values.mean(),
                      "threshold": values.mean() + 2 * values.std(ddof=1)}
    return pd.DataFrame(rows).T
```
:::

答案是：**2026 年在 W32（8 月 3 日至 9 日）首度越過閾值，33 例對上閾值 17.5**，而且一路到 W39 每週都高於閾值。

:::{admonition} 檢查一下
:class: ph-check
1. **手算其中一週。** 筆記本 會列出 W32 的 12 個基準值，並用 Python 的 `statistics` 模組重算平均值 + 2 個標準差，兩邊都是 17.45。
2. **窗口大小。** 第 1–52 週每一週都必須剛好有 12 個值。
3. **故事對得上。** W32 之前沒有任何一個 2026 年的週別高於閾值，而之後每一週都高於。
:::

## 地方性流行通道

**地方性流行通道（endemic channel）**把一年中每一週的「平常水準」畫出來。在 筆記本 裡，細灰線是四個基準年，綠線是它們的平均值（預期值），橘色虛線是閾值。2026 年的長條疊在上面，紅色長條代表高於閾值。颱風 Amihan（W29）之前，2026 年一直很低——這一年開頭比往年安靜。接著從 W32 起，長條衝破了通道。

:::{admonition} Tala 搞錯了
:class: ph-oops
Maya 的第一個提示說「使用檔案裡所有的年份」。Tala 照做了，所以基準裡包含了 **2019 年**（流行年）以及 **2026 年本身**。把流行放進它自己的基準，會同時墊高平均值與標準差，於是閾值跟著曲線一起升高。W32 的閾值從 **17.5 跳到 32.8**。警報勉強響了一下（33 例），然後在流行還在爬升的 **W33 與 W35 反而沒聲音了**。

Maya 怎麼抓到的：在每次計算閾值之前加一行 `assert 2026 not in years`，再檢查名單裡沒有已知的流行年。而且她會把基準年份唸給 Doc Mon 聽。
:::

## 為什麼最新幾週永遠偏低

檔案是依**發病週**計算病例，但病例要等病人就醫、醫療院所通報之後才會到 CESU。在 Santa Luz，從發病到通報的中位數延遲是 4 天。所以最新幾週永遠是不完整的。筆記本 用造冊重現了這個現象：同樣幾週，在三個不同的日子來數。

| 發病週 | W35 | W36 | W37 | W38 |
|---|---:|---:|---:|---:|
| 9/2 時已知 | 30 | 2 | 0 | 0 |
| 9/16 時已知 | 34 | 58 | 54 | 1 |
| 9/30 時已知 | 34 | 58 | 63 | 54 |

9 月 2 日那天，W36 看起來只有 2 例，最後卻是 58 例。這就是為什麼我們檔案的最後一週 **W39（45 例）並不完整**，也是它看起來下滑的原因。請把最新的長條讀成「至少這麼多」，而不是「正在下降」。真實的 PIDSR 資料，延遲還要更長，如上所述。

:::{div}
:class: ph-game ph-game-threshold-watch
有了每週資料，就在那一週的數字送到的當天採取行動：疫情出現後 7 天內偵測、偵測後 1 天內通報、通報後 7 天內完成早期應變。
:::

## 7-1-7：我們動作有多快？

越過閾值是一次**偵測**。**7-1-7** 則是圍繞這件事的時效目標：

```{figure} images/timeline_717_zh.svg
:alt: 一條從疫情發生到偵測（7 天內）、通報（1 天內）、完成早期應變（7 天內）的時間軸。
:width: 100%
7-1-7：疫情出現後 7 天內偵測，偵測後 1 天內通報，通報後 7 天內完成早期應變。
```

在菲律賓，2024 年的聯合外部評核發現 7-1-7 只是*臨時性*地使用；某個市級 ESU 有 56% 的事件在 7 天內被偵測到
（[WHO JEE，2024](https://www.who.int/publications/i/item/9789240116795)）。

`signals_717.csv` 收錄 40 起 Santa Luz 的**合成**事件，時間從 2025 年 1 月到 2026 年 8 月，每起事件有四個日期，以及一個 `bottleneck` 欄位。

:::{admonition} 問問 Tala
:class: ph-ask-tala
我有一個 DataFrame `events`，日期欄位有 `date_emergence`、`date_detection`、`date_notification`、`date_response_complete`（虛構的一列：2025-03-01、2025-03-05、2025-03-06、2025-03-12）。請加上三個以整天計的延遲欄位、三個對應 7-1-7 目標（≤ 7、≤ 1、≤ 7）的 True/False 欄位，以及一個「三項都達成」的欄位。接著印出每個目標各有多少事件達成，包含件數與百分比。
:::

:::{admonition} Tala 說
:class: ph-tala-says
```python
events["days_to_detect"] = (events["date_detection"] - events["date_emergence"]).dt.days
events["days_to_notify"] = (events["date_notification"] - events["date_detection"]).dt.days
events["days_to_respond"] = (events["date_response_complete"] - events["date_notification"]).dt.days

events["detect_ok"] = events["days_to_detect"] <= 7
events["notify_ok"] = events["days_to_notify"] <= 1
events["respond_ok"] = events["days_to_respond"] <= 7
events["all_ok"] = events[["detect_ok", "notify_ok", "respond_ok"]].all(axis=1)
```
:::

| 目標 | 達成 | 未達成 |
|---|---:|---:|
| 偵測 ≤ 7 天 | 26（65%） | 14 |
| 通報 ≤ 1 天 | 31（78%） | 9 |
| 應變 ≤ 7 天 | 27（68%） | 13 |
| **三項皆達成** | **15（38%）** | 25 |

延遲的中位數：偵測 6 天、通報 1 天、應變 6 天。單看每一項目標，似乎都「差不多還行」，但 40 起事件中只有 15 起三項皆達成。

:::{admonition} 檢查一下
:class: ph-check
1. **手算一起事件。** EV-040 是故事裡 Baybay 的登革熱暴增：疫情出現日是 8 月 3 日（W32 的週一），偵測日 8 月 10 日，通報日 8 月 11 日，完成應變日 8 月 21 日。紙上算出來是 7、1、10 天。偵測 ✓、通報 ✓、應變 ✗。Tala 算出來的欄位必須一致。
2. **邏輯。**「三項皆達成」的件數絕不可能多過任何單一目標。
3. **沒有負的延遲。** 出現負數代表某個日期打錯了。去問通報單位（DRU）。
:::

### 讀懂 bottleneck 欄位

百分比告訴你的是*多常*發生；`bottleneck` 欄位告訴你的是*為什麼*。把它用 `"; "` 切開再計數。Santa Luz 最主要的原因是：*病例在尚未成為 PIDSR 疾病通報單位的私人診所就診*（5 起）、*其他業務排擠*（5 起）、*一位疾病監測專員（DSO）要顧 24 個 barangay（描籠涯，菲律賓最基層的行政區，類似台灣的村里）*（5 起），以及 *BHW 注意到群聚，但手機沒有儲值，無法傳簡訊給 CESU*（4 起）。barangay
這些都不是靠寫更好的程式能解決的。解方是一份公文、一位後備的 DSO，以及預付的手機儲值。把這份清單帶去地方衛生委員會。

:::{admonition} 隱私停看聽
:class: ph-privacy
訊號只需要*什麼、哪裡、何時*——「Baybay 第 3 purok（社區小組）有五個發燒的孩子，從週一開始」。它不需要把姓名貼在群組聊天室裡。Santa Luz 有一個瓶頸正是*「以私人聊天訊息通報，未登錄」*：請透過正式管道傳送訊號，這樣才有紀錄，也只有需要知道的人看得到。還有，一如既往，千萬不要把造冊貼進 AI 對話。請描述欄位，並使用虛構的資料列。
:::

:::{div}
:class: ph-game ph-game-quiz
**小測驗：訊號與閾值**

1. 為什麼基準要排除 2019、2020 和 2021 年？
   - ✓ 它們不是平常的年份 — 一個流行年和兩個受 COVID-19 擾亂的年份，會扭曲「平常水準」。
   - 為了讓程式跑得更快 — 這跟速度無關。
2. 你的序列最新一週比前一週低很多。你要怎麼說？
   - 疫情結束了 — 還不能這麼說：最近幾週是不完整的。
   - ✓ 「目前至少這麼多」 — 後面還會有遲到的通報進來。
3. 某起事件第 6 天偵測、第 9 天通報、第 12 天完成應變。哪一項 7-1-7 目標沒達成？
   - 偵測 — 6 天在 7 天之內。
   - ✓ 通報 — 偵測後過了 3 天，目標是 1 天。
   - 應變 — 通報後 3 天，在 7 天之內。
4. 一位 BHW 傳簡訊給 CESU，說某個 purok 有好幾個發燒的孩子。這屬於……
   - ✓ 事件型監測 — 在例行表單之外通報的異常事件。
   - 指標型監測 — 那是指醫療院所通報、經過計數的病例報告。
:::

:::{admonition} Baon（帶走重點）
:class: ph-baon
- 閾值的好壞取決於基準：只用平常的年份，絕對不要用你正在判斷的那一季。用 assert 把關。
- 最新幾週永遠不完整，請讀成「至少」。
- 每一起事件都要量 7-1-7，再去讀 bottleneck。大多數的解法都不是程式碼。

開啟 筆記本：[](notebooks/06_signals_and_thresholds.ipynb)
:::
