---
title: "01 Kumusta, Python?（你好，Python）"
description: "讀懂 AI 寫的程式碼所需的最少 Python：變數、串列、字典、迴圈、if、函式與 f-string，用 pandas 初探 line list（造冊），以及如何冷靜地讀懂錯誤訊息。"
---

::::{div}
:class: ph-story
*2026 年 7 月 28 日星期二 · 上午 7:40 · CESU 辦公室*

:::{div}
:class: ph-say-maya
**Maya：** 桌上又多了六張新單子，還有一張劃記表。*Isa, dalawa, tatlo...*（一、二、三……）三個鉤端螺旋體病。我以後每天早上都要這樣數嗎？
:::

:::{div}
:class: ph-say-tala
**Tala：** 我可以用四行 Python 幫你數。
:::

:::{div}
:class: ph-say-mon
**Doc Mon：** 很好。但 Maya，如果你看不懂那四行，你就不能在報告上簽名。學到足夠的 Python，能*讀懂* Tala 寫的東西就好。
:::

> 要讀懂並檢查別人寫的程式碼，你需要學多少 Python？
::::

比你想的少。你不需要憑記憶*寫*程式，你只需要認得大約七個基本積木，就像你認得病例調查表的各個欄區一樣。這一章用 Maya 的六張單子，教你這七個積木。

## 七個基本積木

| 積木 | 長相 | 可以這樣想 |
|---|---|---|
| **變數（Variable）** | `barangay = "Ilog"` | 貼在資料夾上的標籤；`=` 的意思是*放進去* |
| **文字與數字** | `"Ilog"`, `34`, `True` | 文字要加引號；`True`/`False` 是「是／否」 |
| **串列（List）** | `ages = [34, 9, 41]` | 依序排列的一欄值 |
| **字典（Dictionary）** | `{"disease": "dengue", "age": 9}` | 一張表單：標籤（鍵）與答案（值） |
| **迴圈（Loop）** | `for f in forms:` | 一張一張翻過整疊單子 |
| **`if`** | `if f["disease"] == "dengue":` | 一個是非題；`==` 問的是「*是否相等？*」 |
| **函式（Function）** | `def percent(part, whole):` | 一個有名字、可重複使用的食譜；`return` 把結果交回來 |

還有兩樣東西到處都會看到。**f-string**，`f"{n} cases"`，把一個值放進句子裡。**註解**（comment）以 `#` 開頭；Python 會忽略它，所以它是寫給人看的備忘。寫得好的 AI 程式碼會有很多註解。

有一個陷阱：Python 從 **0** 開始數串列的位置。`ages` 的第一項是 `ages[0]`，不是 `ages[1]`。這種「差一」的失誤，AI 寫的程式碼裡也很常見。

## Maya 的那疊單子，用 Python 來寫

Maya 把六張單子輸入成一個**字典組成的串列**，每張單子一個字典。每張單子她都用字母代替姓名，並記下病患來自哪個 barangay（描籠涯，菲律賓最基層的行政區，類似台灣的村里）。六張全是虛構的。

```python
forms = [
    {"form": "A", "barangay": "Ilog",   "disease": "leptospirosis", "age": 34, "waded": True},
    {"form": "B", "barangay": "Ilog",   "disease": "dengue",        "age": 9,  "waded": False},
    {"form": "C", "barangay": "Wawa",   "disease": "leptospirosis", "age": 41, "waded": True},
    {"form": "D", "barangay": "Sapa",   "disease": "dengue",        "age": 15, "waded": False},
    {"form": "E", "barangay": "Ilog",   "disease": "leptospirosis", "age": 52, "waded": False},
    {"form": "F", "barangay": "Talaba", "disease": "dengue",        "age": 23, "waded": True},
]
```

:::{admonition} 問問 Tala
:class: ph-ask-tala
我有一個叫 `forms` 的 Python 串列。每一項是一個字典，鍵有 `form`、`barangay`、`disease`、`age`、`waded`（True/False）。兩個虛構的項目：
`{"form": "A", "barangay": "Ilog", "disease": "leptospirosis", "age": 34, "waded": True}` 和
`{"form": "B", "barangay": "Ilog", "disease": "dengue", "age": 9, "waded": False}`。
請寫適合初學者的程式碼，計算鉤端螺旋體病（leptospirosis）的單子有幾張，並逐行說明。
:::

:::{admonition} Tala 說
:class: ph-tala-says
```python
lepto_count = 0                      # start the tally at zero
for f in forms:                      # look at each form, one at a time
    if f["disease"] == "leptospirosis":   # == asks "is it equal?"
        lepto_count = lepto_count + 1     # add one tally mark

print(f"Leptospirosis forms: {lepto_count}")
```
:::

像讀 Maya 的劃記表一樣讀它：從零開始，一張一張看，**如果**是鉤端螺旋體病，就多劃一筆。縮排的那幾行（往內縮四個空格）屬於迴圈和 `if`；Python 就是靠縮排知道誰包含在誰裡面。

:::{admonition} 檢查一下
:class: ph-check
1. 執行任何東西之前，**先用手數**：單子 A、C、E 是鉤端螺旋體病，所以是 **3** 張。
2. 執行程式碼。它印出 `Leptospirosis forms: 3`。
3. 讓檢查自動化：`assert lepto_count == 3` 在數字不一致時會報錯停下，一致時則保持沉默。
:::

## Tala 搞錯了：「百分比的分母是誰？」

Maya 的下一個問題：*鉤端螺旋體病的單子中，有百分之幾的人涉過洪水？* Tala 的程式碼執行時沒有任何錯誤，印出 **33.3%**。

```python
waded_lepto = 0
for f in forms:
    if f["disease"] == "leptospirosis" and f["waded"]:
        waded_lepto = waded_lepto + 1
percent_waded = waded_lepto / len(forms) * 100
```

:::{admonition} Tala 搞錯了
:class: ph-oops
用手數。鉤端螺旋體病的單子：A、C、E，共 **3** 張。其中涉過水的：A 和 C，共 **2** 張。三張裡有兩張，是 **66.7%**，不是 33.3%。

分子是對的，錯的是**分母**：`len(forms)` 數的是**全部六張**單子，把登革熱也算進去了。這段程式碼整齊漂亮、執行乾淨，卻給出錯誤答案。這是最危險的一種錯誤，只有用手數才抓得出來。
:::

修正的方法是寫一個小**函式**，把分母變成明確的輸入，這樣每次使用時你都必須決定分母是誰。它也會拒絕除以零。

```python
def percent(part: int, whole: int) -> float:
    # Return part as a percentage of whole.
    if whole == 0:
        raise ValueError("The denominator is 0: there is nothing to take a percentage of.")
    return part / whole * 100


lepto_forms = [f for f in forms if f["disease"] == "leptospirosis"]   # only the lepto forms
waded_lepto = len([f for f in lepto_forms if f["waded"]])

answer = percent(waded_lepto, len(lepto_forms))
print(f"{waded_lepto} of {len(lepto_forms)} leptospirosis forms waded: {answer:.1f}%")
```

它會印出 `2 of 3 leptospirosis forms waded: 66.7%`。`[f for f in forms if ...]` 這一行是一行版的迴圈：只留下通過條件的單子。`: int` 和 `-> float` 這兩個標註是選擇性的備忘，說明輸入是什麼、輸出是什麼。

## 找出錯誤

五段 AI 寫的程式碼，每段都有一個錯誤。點出有問題的那一行。

:::{div}
:class: ph-game ph-game-bug-hunt
AI 的程式碼可能看起來對卻是錯的：逐行閱讀、用你能手算的案例執行，並讀懂錯誤訊息。
:::

## 從六張單子到 618 個病例：pandas

面對幾百列資料，Python 有 **pandas**，一個用程式碼操控的試算表。在筆記本裡，你會打開**已清理、已去識別化**的 Santa Luz line list（造冊）。它沒有姓名、電話或住址；[第 02 章](02_privacy_first.md)會說明檔案是怎麼變成這樣的。

```python
import pandas as pd

df = pd.read_csv("data/synthetic/ph/santa_luz_linelist.csv")
print(df.shape)
print(list(df.columns))
df.head()
```

`df.shape` 印出 `(618, 18)`：618 個病例、18 個欄位。向 Tala 要程式碼時，欄位名稱要**完全照抄**：是 `date_onset`，不是「onset date」。接著 `df["disease"].value_counts()` 對整個檔案做的事，和 Maya 的迴圈一樣：**388** 例登革熱和 **230** 例鉤端螺旋體病。檢查：`388 + 230 = 618`，就是列數。

## 冷靜地讀錯誤訊息

錯誤是訊息，不是羞辱。Maya 輸入 `df["Disease"]` 時，Python 停下來，吐出一大段紅字。重要的部分是**最後一行**：

```text
KeyError: 'Disease'
```

**錯誤類型**告訴你這是哪一類問題。`KeyError` 的意思是「*我找了這個鍵（這裡是欄位名稱），但它不存在。*」欄位叫 `disease`，d 是小寫：Python 把大寫和小寫視為不同的字母。你會經常遇到三種錯誤：

| 錯誤 | 通常表示 |
|---|---|
| `KeyError` | 欄位或鍵的名稱拼錯了 |
| `NameError` | 在建立變數的儲存格執行之前，就先用了這個變數 |
| `SyntaxError` | 少了括號、引號或冒號 |

遇到哪一行讓你困惑時，請 Tala 解釋**那一行就好**：給程式碼，不給資料。

:::{admonition} 問問 Tala
:class: ph-ask-tala
請對初學者逐字解釋這一行 pandas，並說明在一個只有 3 列虛構資料的小表格上，它會印出什麼：`df["disease"].value_counts()`。
:::

然後執行那一行並比對：它真的做了 Tala 說的事嗎？

:::{admonition} 隱私停看聽
:class: ph-privacy
把錯誤訊息貼進 AI 聊天之前，先看一眼。錯誤訊息可能顯示出錯儲存格裡的值，而在真實的 line list 裡，那些值可能就是姓名。請貼上**程式碼和錯誤類型**，並把訊息中的任何資料換成虛構的值。
:::

## 小測驗

:::{div}
:class: ph-game ph-game-quiz
**小測驗：讀懂 Python**

1. `ages = [34, 9, 41]`。`ages[1]` 是多少？
   - `34` — 那是 `ages[0]`：Python 從 0 開始數。
   - ✓ `9` — 位置 1 是第二項，因為是從 0 開始數。
   - `41` — 那是 `ages[2]`，或 `ages[-1]`。
2. 計算百分比的程式碼執行時沒有錯誤。你先檢查什麼？
   - 什麼都不用：沒有錯誤就是對的 — 不對，Tala 的 33.3% 跑得很順，卻是錯的。
   - ✓ 分母，用一個能手算的小例子檢查 — 「百分比的分母是誰？」
   - 圖表的顏色 — 之後有用，但數字要先對。
3. Python 說 `KeyError: 'Barangay'`。最可能的修正是什麼？
   - ✓ 檢查欄位名稱的拼法和大小寫 — 檔案裡是 `barangay`，b 是小寫。
   - 重新安裝 pandas — 函式庫沒問題，是名稱錯了。
   - 刪掉出錯的那一列 — `KeyError` 是名稱的問題，不是某一列的問題。
:::

:::{admonition} Baon（帶走重點）
:class: ph-baon
- 七個基本積木（變數、文字與數字、串列、字典、迴圈、`if`、函式）就足以*讀懂*大多數 AI 寫的分析程式碼。
- 相信一個數字之前，先用手數一個小例子。永遠問「*百分比的分母是誰？*」：Tala 的程式碼除以全部的單子，而不是鉤端螺旋體病的單子。
- 先讀錯誤訊息的最後一行。`KeyError` 通常表示欄位名稱拼錯了。

自己動手跑跑看：[開啟筆記本](notebooks/01_python_with_ai.ipynb)
:::
