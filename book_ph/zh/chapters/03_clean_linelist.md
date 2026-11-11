---
title: "03 從雜亂的造冊到乾淨的資料"
description: "Maya 用 pandas 和 AI 的協助，把 Jun 那份颱風後雜亂的匯出檔，整理成乾淨、已去識別化的 line list（造冊），每一步都檢查，包括 Tala 犯下的一個日期錯誤。"
---

:::{div}
:class: ph-story
*7 月 30 日星期四 · CESU 辦公室，Santa Luz 市衛生局*

**Jun：** Ate Maya，匯出檔又來了，這次只放在辦公室的電腦上。颱風之後所有發燒的通報都在裡面。

**Maya：** Salamat（謝謝），Jun！為什麼 Ilog 會出現六種寫法？

**Jun：** 六種？Ay（哎呀），很多人經手打字嘛。醫院、衛生站、我們自己。有人寫 `Brgy. Ilog`，有人寫 `ILOG`。日期也是……每個登打的人都有自己的風格。

**Doc Mon：** 在任何人開始數東西之前：先把姓名拿掉。然後清理。然後證明它乾淨了。

> 我們要怎麼把 Jun 的匯出檔，變成一份我們信得過、而且可以分享的 line list？
:::

```{figure} images/scene_cesu_office.svg
:alt: Maya 坐在 CESU 辦公室的桌前，筆電上有一條上升的流行曲線，旁邊有紙本通報單，牆上掛著一張城市地圖。
:width: 100%
颱風 Amihan 過後一週，Maya 的辦公桌。Santa Luz、當地居民與資料都是虛構的。
```

## 「乾淨」是什麼意思

**line list（造冊）**是一張表，每一列是一個病例，每一欄是一項資訊：發病日、年齡、性別、barangay（描籠涯，菲律賓最基層的行政區，類似台灣的村里）等等。符合下列條件才算*乾淨*：

- 每一列都是**一個真實的病例**（沒有重複）；
- 每一欄都用**同一種格式**（是 `2026-07-24`，而不是同一天的四種寫法）；
- 每個值都是**可能的**（沒有人 150 歲，也沒有人在就診之後才發病）；
- **無法從中識別出任何人**。

Jun 的檔案 `santa_luz_linelist_raw.csv`，故意違反了這四條規則。你手上這份是他在 9 月 30 日資料凍結時的匯出檔（637 列），所以裡面已經包含故事後段才出現的登革熱病例。它是虛構的訓練資料：裡面的姓名、電話和住址都是編的，但看起來很像真的，好讓你練習如何保護它們。

工具是 **pandas**，Python 的試算表函式庫。pandas 的表格叫做 **DataFrame**；它的一欄叫做 **Series**。我們先把每一欄都當成文字讀進來，這樣 pandas 就不會在背後偷偷改動任何東西：

```python
raw = pd.read_csv(RAW_PATH, skiprows=1, dtype=str, keep_default_na=False)
```

## 第一步是隱私

第 02 章立下規則：識別資訊要在分析*之前*離開表格。但我們仍然需要姓名來做一件事，就是找出被通報兩次的同一位病患。所以 Maya 先把每個姓名，轉成[第 02 章](02_privacy_first.md)的**加鹽假名 ID**。同一個整理過的姓名永遠得到同一個 ID，但沒有秘密的鹽，沒有人能重做它，也無法從中讀回姓名。

:::{admonition} Tala 說
:class: ph-tala-says
```python
SALT = secrets.token_hex(16)  # demo only: in real work, create once and lock it away (chapter 02)


def pseudo_id(name: str, salt: str) -> str:
    key = " ".join(name.upper().replace(".", " ").split())   # normalise the name
    digest = hmac.new(salt.encode(), key.encode(), hashlib.sha256).hexdigest()
    return "P-" + digest[:10]


df = raw.copy()
df.insert(0, "pseudo_id", df["Patient Name"].map(lambda n: pseudo_id(n, SALT)))
df = df.drop(columns=["Patient Name", "Contact No.", "Address", "Reporting Unit", "Remarks"])
```
:::

:::{admonition} 隱私停看聽
:class: ph-privacy
- 也要刪掉**備註**：像 *"anak ni Dennis (kapitbahay)"*（Dennis 的孩子，鄰居）這樣的自由文字會點出別人的名字。
- 只要鹽還存在，加鹽的 ID 就仍然連結著一個人。把真正的鹽鎖在辦公室裡，絕不放進筆記本或聊天，並把這份檔案當成機密處理。這裡的 ID 只是一個工作用的欄位：它永遠不會進入乾淨的檔案。
- 向 Tala 求助時，描述欄位並編造兩三列資料。絕不把 Jun 的真實資料列貼進 AI 聊天。
:::

## 日期：不出錯的那種錯誤

Jun 的日期有各種樣子：`07/24/2026`、`7/24/2026`、`2026-07-24`、`24-Jul-26`、`July 24, 2026`，還有像 `46227` 這樣的純數字，那是 Excel 儲存日期的方式（從 1899 年 12 月 30 日起算的天數）。

:::{admonition} 問問 Tala
:class: ph-ask-tala
我的欄位 `date_of_onset` 裡的日期格式很混亂。請把它轉成 datetime。
:::

:::{admonition} Tala 說
:class: ph-tala-says
因為世界上大多數地方都是日在前，所以請使用 `format="mixed"` 搭配 `dayfirst=True`：
```python
naive_onset = pd.to_datetime(df["date_of_onset"], format="mixed", dayfirst=True, errors="coerce")
```
:::

程式碼跑得動，也沒有任何紅字。Maya 問了兩個護理師會問的問題：有幾個日期**失敗**了？有沒有人**在就診之後才發病**？

:::{admonition} Tala 搞錯了
:class: ph-oops
- **22 個發病日變成了 `NaT`**（「不是時間」）。那些是 Excel 的序列數字，pandas 不會把它們當成日期。
- **56 位病患現在「在就診之後才發病」。** 用了 `dayfirst=True`，`8/1/2026`（8 月 1 日）變成了 1 月 8 日。像 `7/29/2026` 這樣的日期還是對的，因為沒有 29 月，所以錯誤藏在正確的資料列之間。

在菲律賓，斜線格式是月／日／年，而且 Jun 確認他匯出檔裡每一個斜線日期都是這樣。修正方法：**每種格式一條明確的規則**，不要猜。
:::

:::{admonition} 問問 Tala
:class: ph-ask-tala
請寫一個函式 `parse_dates(s)`，處理一個由文字日期組成的 pandas Series。格式有：`M/D/YYYY`（月在前，前導零可有可無）、`YYYY-MM-DD`、`DD-Mon-YY`（年份是 20YY）、有或沒有逗號的 `Month D YYYY`，以及 5 位數的 Excel 序列數字（從 1899-12-30 起算的天數）。空白代表缺漏。請明確地逐一解析每種格式；不要讓 pandas 去猜。
:::

:::{admonition} Tala 說
:class: ph-tala-says
```python
def parse_dates(s: pd.Series) -> pd.Series:
    """Parse Jun's date styles one explicit format at a time."""
    s = s.str.strip()
    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    serial = s.str.fullmatch(r"\d{5}")  # Excel counts days from 30 Dec 1899
    out[serial] = pd.to_datetime(s[serial].astype(int), unit="D", origin="1899-12-30")
    for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%d-%b-%y", "%B %d %Y"]:
        attempt = pd.to_datetime(s.str.replace(",", "", regex=False), format=fmt, errors="coerce")
        out = out.fillna(attempt)  # only fills dates that are still missing
    return out
```
:::

:::{admonition} 檢查一下
:class: ph-check
1. **一個用眼睛就能檢查的案例：** 同一天的七種寫法，必須得到七次 `2026-07-24`，而空白必須維持缺漏。
2. **數數失敗了幾個：** 不是空白的文字日期，絕不能變成 `NaT`。如果有，筆記本會用 `assert` 停下來。
3. **再問一次流行病學的問題：** 發病日晚於就診日的資料，從 56 列降到 **2** 列。那兩列是 Jun 檔案裡真正的打字錯誤，我們在下面處理。
:::

自己試試看。下面遊戲裡有些日期故意設計成有歧義；當一個日期可能有兩種意思時，正確的答案是去問，而不是去猜。

:::{div}
:class: ph-game ph-game-date-fixer
明確地解析每一種已知的日期格式、對應菲律賓語的月份名稱、轉換 Excel 序列數字，並把有歧義的日期標出來，而不是亂猜。
:::

## 地點、代碼與年齡

其他欄位遵循同樣的模式：把規則寫下來、套用規則，然後檢查有沒有漏網之魚。

| 欄位 | 原始值 | 規則 | 乾淨的結果 |
|---|---|---|---|
| Barangay | `Brgy. Ilog`、`ILOG`、`Bgy Ilog `、`Sto. Nino` | 移除重音與前綴、轉小寫、`sto` → `santo`、修正 3 個已知的錯字，再對照官方名單 | `Ilog`、`Santo Niño` + `barangay_id`、`band` |
| Sex | `male`、`lalaki`、`F`、`babae` | 對照表 | `M` / `F` |
| Yes/no | `Y`、`oo`、`hindi`、`N/A` | 對照表 | `1` / `0` / 缺漏 |
| Outcome | `buhay`、`Namatay`、`Expired` | 對照表 | `alive` / `died` |
| Age | `34 y/o`、`8 mos`、`150` | 取第一個數字；月數 ÷ 12；超過 110 → 缺漏 | `34`、`0`、缺漏 |

Jun 的 137 種 barangay 拼法，變成 23 個 barangay。第 24 個，山區的 Bukid，完全沒有通報，第 04 章要記得這件事。年齡的規則幾行就寫得完：

```python
def parse_age(s: pd.Series) -> pd.Series:
    """Completed years from text like '34', '34 y/o', '34yo', '8 mos', '8 months'."""
    text = s.str.strip().str.lower()
    number = text.str.extract(r"^(\d+)")[0].astype("Int64")
    years = number.where(~text.str.contains("mo"), number // 12)  # months -> years
    return years.where(years <= 110).astype("Int64")             # 150 -> missing
```

## 重複資料、不可能的日期，以及證明

`df.duplicated()` 找到 **6 筆完全相同的副本**。但市衛生局也曾經重新通報過一些病患，姓名重新打字、日期格式不同、barangay 拼法也不一樣。清理之後，這些列在重要的欄位上會對得上，所以我們依據*（假名 ID、疾病、發病日）*去重。這總共找到 **19 筆重複**：6 筆完全相同的副本和 13 筆近似重複。

```python
duplicate = df.duplicated(subset=["pseudo_id", "disease", "date_onset"], keep="first")
```

那兩個晚於就診日的發病日被設成缺漏（現實中，Maya 會打電話給通報單位）。剩下的 618 個病例拿到新的 ID，從 `SLC-0001` 到 `SLC-0618`。接著是**驗證規則**：關於資料、永遠必須為真的句子，寫成 `assert`，這樣未來如果有壞掉的匯出檔，筆記本會大聲地停下來。

```python
both = clean.dropna(subset=["date_onset", "date_consult"])
assert (both["date_onset"] <= both["date_consult"]).all()          # ill before consulting
```

:::{admonition} 檢查一下
:class: ph-check
Doc Mon 問：*「你的和官方的乾淨檔案一樣嗎？」* 筆記本最後讓 pandas 逐個儲存格比對這兩張表：

```python
pd.testing.assert_frame_equal(ours, official)
```

沒有任何訊息，代表兩者完全相同：618 列 × 18 欄，也就是之後每一章使用的檔案（`santa_luz_linelist.csv`）。
:::

:::{div}
:class: ph-game ph-game-quiz
**小測驗：清理 line list**

1. 你用 `pd.to_datetime(..., dayfirst=True)` 之後，日期欄沒有出現錯誤。這樣安全嗎？
   - ✓ 還不安全：數一數有幾個 `NaT`，並檢查發病日從不晚於就診日 — 解析錯誤不會跳出任何錯誤訊息。
   - 安全：如果有問題，pandas 會報錯 — 無聲的誤判不會引發任何錯誤。
2. 為什麼要把姓名變成加鹽的假名 ID，而不是直接刪掉？
   - ✓ 我們仍然需要找出同一個人的重複通報 — ID 能對得上，卻不顯示姓名。
   - 因為假名化的檔案可以安全公開 — 只要鹽還存在，它就仍然是機密。
   - 這樣之後才能讀回姓名 — 好的 ID 是無法讀回的。
3. `df.duplicated()` 找到 6 列。這些就是所有的重複嗎？
   - 是 — 重複就是完全相同的列。重新通報的病患是用不同方式打的字，所以並不完全相同。
   - ✓ 不是 — 它只能找出每一欄都相同的列。清理之後，依假名 ID、疾病和發病日，還會再找到 13 筆近似重複。
:::

:::{admonition} Baon（帶走重點）
:class: ph-baon
- 先保護身分：加鹽的假名 ID，然後刪掉姓名、電話、住址和備註。
- 絕不讓電腦去猜日期：每種格式一條明確的規則，然後數 `NaT`，並檢查發病日 ≤ 就診日。
- 把你的規則寫成 `assert`，並證明結果：用 `assert_frame_equal` 和一個可信的版本比對。

開啟筆記本：[](notebooks/03_clean_linelist.ipynb)
:::
