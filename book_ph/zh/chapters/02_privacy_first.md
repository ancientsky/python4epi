---
title: "02 隱私優先：每一列都是鄰居"
description: "為什麼隱私在監測中最優先、哪些欄位會識別出一個人、使用 AI 工具的三條規則，以及動手做去識別化：假名 ID、泛化、小數字隱匿與再識別檢查。"
---

::::{div}
:class: ph-story
*2026 年 7 月 29 日星期三 · CESU 辦公室*

:::{div}
:class: ph-say-jun
**Jun：** 這是共用雲端硬碟上的匯出檔，Ma'am Maya。洪水之後所有的通報資料都在裡面。姓名、聯絡電話，全部都有。
:::

:::{div}
:class: ph-say-maya
**Maya：** 太好了。我把前二十列貼給 Tala，讓它看看格式。
:::

:::{div}
:class: ph-say-nena
**Aling Nena：** Ate，等一下。那份名單上的每個人我都認識。Mang Lito（利托大叔）、Aguilar 家的男孩、Rizal 街上的那對雙胞胎。如果他們的名字流到不該去的地方，他們下次生病就再也不會告訴我了。
:::

:::{div}
:class: ph-say-mon
**Doc Mon：** 她說得對。任何東西離開這間辦公室之前，先問自己：誰看得到這個檔案？
:::

> 怎麼分享 line list（造冊），又不出賣我們的鄰居？
::::

```{figure} images/scene_health_station.svg
:alt: 一座描籠涯（barangay）衛生站，有旗子、芒果樹下的候診長椅，Aling Nena 站在門口。
:width: 100%
只有在人們信任衛生站的時候，監測才行得通。
```

## 為什麼隱私優先

**信任。** 監測靠的是人們願意站出來。如果一個家庭發現自己的病情被人議論，或姓名出現在群組聊天裡，他們就不再就診，下一次疫情就會更晚被發現。

**汙名。** 一個診斷可能讓人丟掉工作、失去學校的位子，或在描籠涯（barangay，菲律賓最基層的行政區，類似村里）裡失去名聲。有些疾病的汙名比較重，但沒有一種應該成為八卦。

**法律。** 兩部法律在你的工作中並肩而立：

| 你**必須**通報 | 你**必須**保護 |
|---|---|
| [RA 11332](https://lawphil.net/statutes/repacts/ra2019/ra_11332_2019.html)，2019 年的強制通報法，把通報法定傳染病定為義務。依其[2020 年修訂施行細則](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf)，第一類疾病須在 24 小時內通報，第二類每週通報。 | **2012 年資料隱私法（Data Privacy Act of 2012, RA 10173）**規範個人資訊如何蒐集、使用與分享，而一個人的健康狀況是檔案裡最敏感的資訊之一。你單位的資料保護長（Data Protection Officer）可以告訴你法律對你有什麼要求。 |

通報和保密並不衝突。通報是**沿著通報鏈往上送到需要的人手上**，不會去其他任何地方。DOH 與國家隱私委員會（National Privacy Commission）已就這種平衡發布聯合指引，例如針對 COVID-19 監測資料的 [JMC 2020-0002](https://law.upd.edu.ph/wp-content/uploads/2020/05/DOH-NPC-JMC-No-2020-0002.pdf)。

:::{admonition} 非法律意見
:class: warning
本章教的是訓練用的良好做法，不是法律意見，也不涵蓋適用於你單位的所有規定。有疑問時，請依照你單位的**資料保護長**（Data Protection Officer, DPO）以及適用於你的 DOH 指引。
:::

## 什麼會識別出一個人？

**line list（造冊）**是一張表，每一列是一個病例。它的欄位可以分成四類：

| 類別 | 是什麼 | 在 Jun 的匯出檔裡 |
|---|---|---|
| **直接識別資訊** | 單獨就能指向一個人 | `Patient Name`、`Contact No.`、`Address`（也包括 PhilHealth 或其他證號） |
| **間接識別資訊**（準識別碼） | 單獨無害，組合起來就能識別 | `Barangay`、`Age`、`Sex`、四個日期、`Reporting Unit` |
| **敏感的健康資訊** | 這一列「關於什麼」 | `Disease`、`Classification`、`Admitted`、`Outcome`、暴露 |
| **自由文字** | 什麼都可能有 | `Remarks`：在你讀過之前，都當成直接識別資訊處理 |

間接識別資訊是大家最容易忘記的。*一位住在 Ilog barangay、7 月 24 日開始發燒的 34 歲男性*，可能剛好只對得上一個人，而他的鄰居都知道是誰。

:::{admonition} 隱私停看聽
:class: ph-privacy
**使用 AI 工具的三條規則**

1. **絕不把可識別的資料列貼進** AI 聊天：不貼姓名、電話、住址、證號、完整出生日期或備註。
2. **改為描述結構：** 欄位名稱、值的種類，以及兩三列明顯是編造的資料。
3. **原始檔案留在單位內**，只放在單位核准的電腦與硬碟上。程式碼可以流動；資料留在原地。
:::

## 點出不能離開辦公室的東西

:::{div}
:class: ph-game ph-game-spot-pii
姓名、電話、街道住址、PhilHealth 號碼、完整出生日期和自由文字備註，絕不離開辦公室，也不進入 AI 聊天。
:::

## 動手做：將 Jun 的匯出檔去識別化

在筆記本裡，你處理的是 `santa_luz_linelist_raw.csv`，637 列、19 個欄位。

:::{admonition} 這份檔案裡的姓名是假的
:class: warning
`santa_luz_linelist_raw.csv` 裡的每一個姓名、電話和住址，都是電腦編出來的，刻意做得**看起來**像真的，供練習使用。電話號碼全都落在虛構的 `0900 555` 號段。檔案裡沒有任何真實的人。
:::

Maya 遵守規則 2。她只給 Tala 看欄位名稱。

:::{admonition} 問問 Tala
:class: ph-ask-tala
我有一個 pandas DataFrame `raw`，有 19 個文字欄位：Date Reported, Reporting Unit,
Patient Name, Sex, Age, Contact No., Address, Barangay, Disease, Date of Onset,
Date Consulted, Classification, Date Lab Confirmed, Admitted, Outcome,
Waded in Floodwater, Did Cleanup Work, Dengue Severity, Remarks。
我不能分享任何資料列：它們是機密的病患資料。
請寫 pandas 程式碼，移除直接識別資訊，這樣我才能把表格分享給我們的省級流行病學家。
:::

:::{admonition} Tala 說
:class: ph-tala-says
```python
direct_identifiers = ["Patient Name", "Contact No.", "Address"]
shared = raw.drop(columns=direct_identifiers)
```
:::

程式碼跑得動，這三個欄位也消失了。但「沒有錯誤」不等於「沒有姓名」。

:::{admonition} 檢查一下
:class: ph-check
1. 把剛剛移除的那一欄裡，每個名字（first name）都取出來。
2. 在**所有剩下的儲存格**裡，以完整單字搜尋這些名字。
3. 答案必須是零。如果不是，看看名字藏在哪裡。
:::

```python
first_names = sorted(set(raw["Patient Name"].str.split().str[0]))
pattern = r"\b(?:" + "|".join(first_names) + r")\b"

hits = shared.apply(lambda column: column.str.contains(pattern)).sum()
```

:::{admonition} Tala 搞錯了
:class: ph-oops
搜尋結果在 **40 筆備註**裡找到了名字，例如 *"anak/kapatid ni Dennis (kapitbahay)"*，意思是「Dennis 的孩子或手足，鄰居」。這則備註點名了**別人**，再加上 barangay，就直接指向一個家戶。其他備註也有風險：*"estudyante, Grade 5"*（學生，五年級）把一個孩子縮小到某一個班級。

Tala 移除了名稱*叫做*姓名、電話和住址的欄位。它看不到 `Remarks` 裡面，因為 Maya 做得很對，從沒給它看過任何資料列。**AI 只知道你告訴它的事。檢查結果是你的工作。**
:::

修正方法：刪掉 `Remarks`（先在單位內，把裡面有用的資訊編成是／否欄位），也刪掉 `Reporting Unit`，因為有些通報單位只送過一兩份報告，單位名稱就可能指向某個人。然後再跑一次同樣的搜尋，直到結果為零。

## 帶有秘密的假名 ID

Doc Mon 仍然需要能說*「再查一下第 17 號個案」*。這需要一個在辦公室以外毫無意義的 ID：**假名 ID（pseudonymous ID）**。

一個誘人的捷徑是把姓名做**雜湊（hash）**：用固定的配方把它變成一串亂碼。但同樣的姓名永遠得到同樣的亂碼，所以任何手上有常見姓名清單（選民名冊、班級名單、社群媒體）的人，都可以把每個姓名雜湊後找比對。在筆記本裡，一份只有五個名字的猜測清單，就立刻找出了「Juan P. Santos」。**未加鹽的姓名雜湊並不匿名。**

解法是**鹽（salt）**：混進雜湊裡的一串長長的隨機秘密。沒有鹽，沒有人能重做雜湊。單位要把鹽鎖好保管，絕不放在筆記本、絕不放進 AI 聊天、絕不跟資料一起寄出。

```python
def pseudo_id(name: str, salt: str) -> str:
    key = " ".join(name.upper().replace(".", " ").split())   # normalise the name
    digest = hmac.new(salt.encode(), key.encode(), hashlib.sha256).hexdigest()
    return "P-" + digest[:10]
```

最簡單的假名其實是流水號，`SLC-0001`、`SLC-0002` 依此類推，把號碼對應到姓名的對照表則鎖在辦公室裡。乾淨的 Santa Luz 檔案用的就是這種做法。

## 泛化：越粗略越安全

- **年齡 → 年齡組**（`0-4`、`5-14`、`15-24`、`25-44`、`45-64`、`65+`）。
- **住址 → barangay。** 保留 barangay（畫地圖需要它）；丟掉街道與 purok（分區）。
- **完整日期 → 週**，凡是要公開的資料都這樣處理。完整日期只留在單位內，用於流行曲線和延遲分析。

## 小數字隱匿

公開的 **1** 可能就是一個人。*「Buhangin 有一例登革熱死亡」*是整個 barangay 都能對上名字的消息。常見的規則是把 **1 到 4** 的數字顯示為 `<5`（零仍然是零）。

```python
def suppress(table: pd.DataFrame, threshold: int = 5) -> pd.DataFrame:
    if threshold < 1:
        raise ValueError("threshold must be at least 1")
    small = (table > 0) & (table < threshold)
    return table.astype(object).mask(small, f"<{threshold}")
```

還有一個陷阱。如果一欄**只有一個**被隱藏的儲存格，而它的總數是公開的，任何人都可以用減法把它算回來。在筆記本裡，各 barangay 的死亡數中，登革熱那一欄剛好只有一個被隱藏的儲存格，所以登革熱死亡數只以全市總數公布。就連那個總數（1）也是 Doc Mon 與 DPO 要做的決定，不是程式碼能決定的。

## 再識別檢查：誰是唯一的？

怎麼知道自己做得夠不夠？數一數有多少人在他們的間接識別資訊上是**唯一**的，也就是檔案裡沒有任何其他人和他們有同樣的組合。**k-匿名性（k-anonymity）**的想法是：每一種組合都該至少被 *k* 個人共有，比如五個。

在乾淨的 line list 上（排除有缺漏值的列）：

| 保留的間接識別資訊 | 唯一的人 |
|---|---:|
| barangay + 年齡 + 性別 + 疾病 + 發病日 | 99.0% |
| barangay + 年齡 + 性別 + 疾病 | 80.9% |
| barangay + 年齡組 + 性別 + 疾病 | 17.5% |
| 地帶（band）+ 年齡組 + 性別 + 疾病 | 1.3% |

用完整年齡加發病日，即使沒有姓名，幾乎**每個人**都是唯一的。粗略化才是保護他們的方法。

## 小測驗

:::{div}
:class: ph-game ph-game-quiz
**小測驗：隱私優先**

1. 下列哪一個是間接識別資訊？
   - `Patient Name` — 它單獨就能識別一個人：是直接識別資訊。
   - ✓ `Age` — 單獨無害，和 barangay、性別、日期合在一起就能識別。
   - `Disease` — 那是敏感的健康資訊，也就是這一列「關於什麼」。
2. 你清理資料時需要 Tala 幫忙。你貼上什麼？
   - 前 20 列，讓 Tala 看看格式 — 絕對不行：資料列會識別出人。
   - ✓ 欄位名稱和兩列明顯編造的資料 — 足夠換到好的程式碼。
   - 把姓名模糊掉的資料列 — 備註和日期仍可能識別出人。
3. 為什麼單純的姓名雜湊並不匿名？
   - 它是匿名的：沒有人讀得懂雜湊 — 他們不用讀懂：把猜測清單雜湊後比對就行。
   - ✓ 任何有常見姓名清單的人，都能雜湊後找出比對 — 秘密的鹽能阻止這件事。
   - 雜湊太短了 — 長度不是問題，缺少秘密才是。
4. 你要公開的表格在某個 barangay 顯示了 `2` 例死亡。你怎麼做？
   - ✓ 顯示成 `<5`，並檢查沒有任何一欄只有一個被隱藏的儲存格 — 小數字可能就是一個人。
   - 直接公布：它只是個數字 — 一個 barangay 的 2 可能指向一個家庭。
   - 把這個 barangay 從表格中刪掉 — 隱匿能讓表格保持有用。
:::

:::{admonition} 帶走重點（Baon）
:class: ph-baon
- 每一列都是鄰居。依 RA 11332 的要求沿通報鏈往上通報；其他地方一律不分享。
- 使用 AI 工具時：絕不貼可識別的資料列、改為描述結構、原始檔案留在單位內。然後**檢查**結果：Tala 的程式碼在備註裡留下了 40 個名字。
- 用秘密做假名化、把年齡與日期泛化、隱匿 1 到 4 的數字，並在任何東西公開之前，量一量還有誰是唯一的。

自己動手跑跑看：[開啟筆記本](notebooks/02_privacy_first.ipynb)
:::
