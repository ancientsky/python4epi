# 01 流行病學核心概念（Python 零基礎版）

## 你將學到

- 流病分析常見資料物件：變數、列表（list）、字典（dict）、DataFrame
- 4 個必要 Python 基礎：指定值、型別、條件、函式
- 流病核心指標：attack rate、CFR 的定義與計算
- 如何把「文字結論」轉成「可重跑程式碼」

## 先備說明（給零基礎學員）

如果你沒有 Python 經驗，請先記住這 5 點：

1. `=` 是「把右邊結果放到左邊變數」，不是數學等號。
2. `#` 後面是**註解（comment）**——Python 會完全忽略它，不會執行。註解是寫給人看的筆記。
3. `print(...)` 用來顯示結果。
4. 字串（文字）要加引號，如 `"confirmed"`。
5. 百分比通常用 `:.2%` 顯示。

### 關於 `#` 註解

```python
# 這整行是註解，Python 不會執行
total = 280        # 這是行尾註解，# 後面的文字不會執行

# 好習慣：用註解說明「為什麼」這樣做
# 分母用感染人數 121，不是全體 280（致死率的定義）
cfr = 19 / 121
```

在 Jupyter notebook 裡，你會看到兩種「說明文字」：
- **`#` 註解**：寫在 Code cell 裡，跟程式碼混在一起
- **Markdown cell**：獨立的文字區塊，可以有標題、粗體、列表、表格（詳見 Ch00）

## 情境故事

松柏護理之家爆發退伍軍人症群聚事件，主管剛把 line list 交到你手上。在你學會用 pandas 讀 CSV 之前（那是 Ch02 的事），他先要你回答：

- 全機構侵襲率（attack rate）多少？
- 致死率（CFR）多少？
- 住院率、ICU 率各多少？
- 要不要升級應變層級？

先用最基本的 Python 把指標算出來——這就是本章要做的事。

## 核心概念

- **Variable（變數）**：貼了標籤的盒子，用來儲存一個值，之後用名字取回。
- **Data type（資料型別）**：整數 `int`、浮點數 `float`、字串 `str`、布林 `bool`——決定這個值能做什麼運算。
- **Case definition（病例定義）**：先定義誰算個案，再計算指標。
- **Line list**：每列一位個案、每欄一個變數（本教材使用 280 位住民 × 32 欄位的 Legionella 群聚資料）。
- **Attack rate（侵襲率）**：`cases / population`——本群聚中為 121 / 280 = 43.2%。
- **Case fatality rate（致死率，CFR）**：`deaths / cases`——本群聚中為 19 / 121 = 15.7%。
- **Bias / confounding（偏差 / 干擾作用）**：資料蒐集與解釋時最常見的問題來源（Ch05 會深入探討）。

## 教學影片

每個概念都有配套的動畫教學影片（約 3 分鐘），嵌在下方對應的小節中。影片包含：主線教學 → 額外防疫範例 → 初學者常見盲點破解。

建議先看影片再讀程式碼，學習效果更好！

## Python 基礎練習（一步一步）

### 1) 數值變數——先把數字存起來

```{figure} images/python_variables.svg
:name: fig-python-variables
:alt: 變數 (variable) 是貼了標籤的盒子，以及 int / float / str / bool 四種基本資料型別
:width: 100%

**變數 (Variable)** 是貼了標籤的盒子；`=` 是「把右邊的值放進左邊的盒子」。四種基本資料型別：`int`（整數 integer）、`float`（浮點數 float）、`str`（字串 string）、`bool`（布林 boolean）。
```

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：數值變數</div>
  <div class="youtube-lite" data-id="RhqNl3LzjmU">
    <img src="https://img.youtube.com/vi/RhqNl3LzjmU/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">影片內容：變數是貼了標籤的盒子 → COVID-19 校園群聚範例 → 盲點：字串 vs 數字、大小寫、等號方向</p>
</div>
```

```python
# 松柏護理之家退伍軍人症群聚事件的基本數據
total_residents = 280       # 住民總數
infected = 121              # 感染人數（含無症狀）
confirmed = 89              # 確診個案
probable = 25               # 可能個案
hospitalized = 68           # 住院人數
icu = 23                    # ICU 人數
deaths = 19                 # 死亡人數
```

### 2) 計算指標——用除法得到比率

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：計算指標</div>
  <div class="youtube-lite" data-id="ZqqZmuVjoN0">
    <img src="https://img.youtube.com/vi/ZqqZmuVjoN0/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">影片內容：除法算侵襲率/致死率 + f-string 格式化 → 登革熱盛行率範例 → 盲點：除法類型、忘加 f、:.2% 拆解</p>
</div>
```

```python
# 侵襲率 = 感染人數 / 住民總數
attack_rate = infected / total_residents
print(f"侵襲率 (Attack rate): {attack_rate:.2%}")

# 致死率 = 死亡人數 / 感染人數
cfr = deaths / infected
print(f"致死率 (CFR): {cfr:.2%}")

# 住院率 = 住院人數 / 感染人數
hosp_rate = hospitalized / infected
print(f"住院率: {hosp_rate:.2%}")
```

### 3) 字典——把同一主題的資料放一起

```{figure} images/python_list_vs_dict.svg
:name: fig-python-list-vs-dict
:alt: 列表 (list) 和字典 (dict) 的比較——列表靠索引取值，字典靠 key 取值
:width: 100%

**列表 (List)** 是一排格子櫃，靠 index（索引、從 0 開始）取值；**字典 (Dict)** 是貼標籤的收納盒，靠 key（鍵）取值。下方先教字典，再教列表。
```

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：字典</div>
  <div class="youtube-lite" data-id="4iriq9cNG-A">
    <img src="https://img.youtube.com/vi/4iriq9cNG-A/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">影片內容：字典 = 有格子的收納盒 → 腸病毒通報個案範例 → 盲點：key 引號、() vs []、KeyError</p>
</div>
```

```python
# 用字典整理群聚事件摘要
outbreak = {
    "facility": "松柏護理之家",
    "pathogen": "Legionella pneumophila",
    "total_residents": 280,
    "infected": 121,
    "confirmed": 89,
    "deaths": 19,
}

# 從字典取值計算
cfr = outbreak["deaths"] / outbreak["infected"]
print(f"{outbreak['facility']} CFR: {cfr:.2%}")
```

### 4) 列表——存放一組同類資料

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：列表</div>
  <div class="youtube-lite" data-id="bwRKaJYyGCU">
    <img src="https://img.youtube.com/vi/bwRKaJYyGCU/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">影片內容：列表 = 一排格子櫃 → 每週 COVID 確診趨勢範例 → 盲點：索引從 0 開始、IndexError、列表不對齊</p>
</div>
```

```python
# 各樓層翼區的感染人數
floor_wing_cases = [15, 10, 24, 25, 20, 27]  # 1A, 1B, 2A, 2B, 3A, 3B
floor_wing_names = ["1A", "1B", "2A", "2B", "3A", "3B"]

# 找出最多感染的翼區
max_cases = max(floor_wing_cases)
max_index = floor_wing_cases.index(max_cases)
print(f"感染人數最多的翼區：{floor_wing_names[max_index]}（{max_cases} 人）")
```

### 5) 條件判斷——把指標轉成行動訊號

```{figure} images/python_if_else_flow.svg
:name: fig-python-if-else
:alt: if / elif / else 流程圖——CFR 經過多個條件判斷，走到對應的應變層級
:width: 100%

**條件判斷 (Conditional statement)** 讓資料依條件走不同路徑。`if`（如果）→ `elif`（否則如果）→ `else`（其他）。`>`、`<`、`==`、`!=` 是**比較運算子 (comparison operator)**，會回傳 `True` 或 `False`。
```

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：條件判斷</div>
  <div class="youtube-lite" data-id="8q6imxzb9mM">
    <img src="https://img.youtube.com/vi/8q6imxzb9mM/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">影片內容：if/elif/else 路口指示牌 → 疫苗接種率門檻範例 → 盲點：= vs ==、忘記冒號、縮排錯誤</p>
</div>
```

```python
# 根據致死率決定應變層級
if cfr > 0.15:
    print("致死率偏高（>15%），建議升級應變層級")
elif cfr > 0.10:
    print("致死率中等（10-15%），持續加強監測")
else:
    print("致死率尚可（<10%），維持常規應變")
```

### 6) 函式——把計算邏輯包成可重用的工具

```{figure} images/python_function_machine.svg
:name: fig-python-function
:alt: 函式 (function) 是自動計算機——輸入參數、經過函式本體、回傳輸出
:width: 100%

**函式 (Function)** 就像自動計算機：輸入 **參數 (parameters)** → 經過 **函式本體 (body)** → `return` **輸出 (output)**。一次定義、多次呼叫 (reusability)，改公式只改一個地方，不怕改漏。
```

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：函式</div>
  <div class="youtube-lite" data-id="CGux0-2swi8">
    <img src="https://img.youtube.com/vi/CGux0-2swi8/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">影片內容：函式 = 自動計算機 → 結核病發生率範例 → 盲點：忘加括號、忘記 return、參數順序搞錯</p>
</div>
```

```python
def calc_attack_rate(cases, population):
    """計算侵襲率。"""
    if population == 0:
        raise ValueError("分母（population）不能為 0")
    return cases / population

# 全機構侵襲率
ar_all = calc_attack_rate(121, 280)
print(f"全機構侵襲率: {ar_all:.2%}")

# 3 樓 B 翼侵襲率
ar_3b = calc_attack_rate(27, 47)
print(f"3 樓 B 翼侵襲率: {ar_3b:.2%}")
```

## 流病到程式的翻譯模板

1. 先定義名詞：`infected`, `deaths`, `total_residents`。
2. 再寫公式：`attack_rate = infected / total_residents`。
3. 最後寫判讀規則：例如 `if cfr > 0.15`。
4. 如果需要重複用，包成函式：`def calc_attack_rate(cases, population)`。

## 常見錯誤（新手最容易踩）

- 把 `infected` 放成文字（`"121"`）而不是數字（`121`）。
- 忘記分母不能是 0（例如某翼區沒有住民）。
- 直接改結果數字，不改原始輸入值（程式跑不出正確結果）。
- CFR 的分母是「感染人數」不是「住民總數」——概念要搞清楚。

## 練習本

- 課堂筆記：{ref}`01_fundamentals_python_basics.ipynb`
- 作業版：[`01_fundamentals_exercise.ipynb`](exercises/01_fundamentals_exercise.ipynb)
- 解答版（教師版）：[`01_fundamentals_solution.ipynb`](solutions/01_fundamentals_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/01_fundamentals_solution.ipynb>)

## 最小可執行環境命令

```bash
uv sync
uv run jupyter lab
```
