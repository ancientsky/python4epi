# 01b Python 開發者工具箱

## 情境

你剛跑完 Ch01 的侵襲率、致死率計算，主管看了你的 Python 程式碼，丟出一堆問題：

- 「為什麼要空四格？」
- 「`import` 是什麼意思？」
- 「跑出紅字錯誤怎麼辦？」
- 「怎麼安裝新的套件？」

在你踏入 Ch02 的 pandas 世界之前，這一章幫你補齊**流行病學家的 Python 開發者常識**——不是要你變成軟體工程師，而是讓你遇到問題時不會手足無措。

## 你將學到

- Python 縮排規則——為什麼空 4 格是強制的
- `import` 語法——怎麼借用別人寫好的工具
- 型別與轉換——數字、文字、布林值的互相轉換
- 讀懂錯誤訊息——traceback 不是天書
- `try/except`——優雅處理意外狀況
- 字串方法與迴圈進階——清理髒資料的必備技能
- `uv` 進階用法——管理 Python 版本與第三方套件
- Jupyter 實用密技——`!` 指令、Tab 自動完成、查文件

## 先備說明（給零基礎學員）

這章假設你已經會 Ch01 教的 6 件事：

1. 變數（`total_residents = 280`）
2. 算術運算（`infected / total_residents`）
3. 字典（`outbreak = {"deaths": 19, ...}`）
4. 列表（`[15, 10, 24, 25, 20, 27]`）
5. 條件判斷（`if cfr > 0.15:`）
6. 函式（`def calc_attack_rate(cases, population):`）

如果還不熟，請先回 Ch01 練習一次再來。

## 教學影片

每個概念都有配套的動畫教學影片（約 3 分鐘），嵌在下方對應的小節中。影片包含：主線教學 → 額外防疫範例 → 初學者常見盲點破解。

建議先看影片再讀程式碼，學習效果更好！

---

## Part 1：Python 語法規範

### 1) 縮排——Python 的必修規矩

:::{admonition} 教學影片：縮排
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/YOUTUBE_ID_01B_01_INDENTATION" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：為什麼空 4 格、if/for/巢狀縮排 → 登革熱分區噴藥範例 → 盲點：忘記縮排、混用 Tab 和空格、多餘縮排
:::

在大多數程式語言裡，縮排只是讓程式「好看」。但在 Python 裡，**縮排是語法的一部分**——少一格或多一格，程式就會壞掉。

```python
# ✅ 正確：if 底下的程式碼縮排 4 格
cfr = 19 / 121
if cfr > 0.15:
    print("致死率偏高，建議升級應變層級")
    print("請通知指揮中心")
```

```python
# ❌ 錯誤：忘記縮排 → IndentationError
cfr = 19 / 121
if cfr > 0.15:
print("致死率偏高")  # IndentationError: expected an indented block
```

**三個縮排規則：**

| 規則 | 說明 |
|------|------|
| 統一用 4 個空格 | 這是 Python 官方風格指南（PEP 8）的規定 |
| 不要混用 Tab 和空格 | 混用會產生 `TabError`，Jupyter 預設用空格，不用擔心 |
| 同一個區塊要對齊 | `if`、`for`、`def` 底下的程式碼要在同一層 |

**什麼時候需要縮排？** 看到冒號 `:` 就要縮排——`if:`、`for:`、`def:`、`while:`、`try:`、`except:`。

```python
# 巢狀縮排：for 裡面的 if
floor_cases = [15, 10, 24, 25, 20, 27]
for cases in floor_cases:       # 第一層
    if cases > 20:              # 第二層（再縮 4 格）
        print(f"{cases} 人感染，需要重點關注")
```

### 2) import——借用別人的工具

:::{admonition} 教學影片：import
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/YOUTUBE_ID_01B_02_IMPORTS" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：import 三種寫法、約定俗成的別名 → 用 datetime 算發病天數 → 盲點：套件沒裝、import 放中間、from import 後用全名
:::

Ch01 裡所有計算都用 Python 內建功能。但真正做疫調分析時，你需要「借用」別人寫好的強大工具——這就是 `import`。

**三種 import 寫法：**

```python
# 寫法 1：import 整個模組
import math
print(math.sqrt(121))   # 11.0（開根號）

# 寫法 2：只借一個功能
from math import sqrt
print(sqrt(121))         # 11.0（不用加 math. 前綴）

# 寫法 3：取別名（最常見！）
import statistics as stats
ages = [72, 68, 81, 75, 90, 66, 78, 85, 73, 69]
print(stats.median(ages))  # 73.5（年齡中位數）
```

**Ch02 你會看到的 import：**

```python
import pandas as pd          # pd 是約定俗成的縮寫
import matplotlib.pyplot as plt  # plt 也是約定俗成
import seaborn as sns         # sns 取自 Samuel Norman Seaborn（影集人物）
```

> 💡 **慣例**：import 語句永遠放在檔案最上面。這樣一眼就知道這份程式用了哪些工具。

**疫調示範：用 `statistics` 模組分析個案年齡**

```python
import statistics

# 10 位感染者的年齡
ages = [72, 68, 81, 75, 90, 66, 78, 85, 73, 69]

print(f"平均年齡: {statistics.mean(ages):.1f}")      # 75.7
print(f"中位數:   {statistics.median(ages):.1f}")     # 73.5
print(f"標準差:   {statistics.stdev(ages):.1f}")      # 7.8
```

### 3) 型別與轉換——數字、文字、布林值

:::{admonition} 教學影片：型別與轉換
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/YOUTUBE_ID_01B_03_TYPES" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：type() 查型別、int/float/str/bool 四大型別、布林與邏輯運算 → 腸病毒年齡欄位清理 → 盲點：字串加法、"False" vs False、int("N/A")
:::

Python 裡每個值都有**型別（type）**。型別搞錯，程式就會出錯。

```python
# 用 type() 檢查型別
print(type(280))        # <class 'int'>    整數
print(type(43.2))       # <class 'float'>  浮點數（小數）
print(type("confirmed"))# <class 'str'>    字串（文字）
print(type(True))       # <class 'bool'>   布林值
```

**型別轉換：** 從 CSV 讀進來的資料，常常全部是文字。你需要手動轉型才能計算。

```python
# 假設從 CSV 讀到的是文字
infected_str = "121"
total_str = "280"

# ❌ 文字除法 → TypeError
# result = infected_str / total_str

# ✅ 先轉成數字再算
infected = int(infected_str)
total = int(total_str)
attack_rate = infected / total
print(f"侵襲率: {attack_rate:.2%}")  # 侵襲率: 43.21%
```

**布林值（Boolean）：** `True` 和 `False` 是 Python 的邏輯值。比較運算會產生布林值。

```python
cfr = 19 / 121
print(cfr > 0.15)       # True（致死率 > 15%）
print(cfr > 0.20)       # False（致死率沒有 > 20%）

# 邏輯運算：and, or, not
high_cfr = cfr > 0.10
many_cases = 121 > 100

if high_cfr and many_cases:
    print("高致死率 + 大量感染：建議升級應變層級")

# not 取反
if not (cfr < 0.05):
    print("致死率不算低，需持續監測")
```

---

## Part 2：Debug 生存技能

### 4) 讀懂錯誤訊息——traceback 不是天書

:::{admonition} 教學影片：讀懂錯誤訊息
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/YOUTUBE_ID_01B_04_ERRORS" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：traceback 由下往上讀、五大常見錯誤實演 → 批次讀取通報檔案 → 盲點：只看第一行、全複製問 AI、Warning vs Error
:::

看到滿螢幕的紅字別慌。Python 的錯誤訊息其實很貼心——**從最後一行往上讀**就好。

**閱讀 traceback 的口訣：看最後一行 → 看錯誤類型 → 看行號**

以下是流行病學家最常遇到的 5 種錯誤：

```python
# 1) NameError：變數名打錯
# infceted = 121   （拼錯了！）
# print(infected)  → NameError: name 'infected' is not defined
# 修正：檢查拼字，Python 區分大小寫

# 正確寫法
infected = 121
print(infected)  # 121
```

```python
# 2) TypeError：型別不對
# "121" / "280"  → TypeError: unsupported operand type(s) for /: 'str' and 'str'
# 修正：先轉型
print(int("121") / int("280"))  # 0.432...
```

```python
# 3) KeyError：字典裡沒有這個 key
outbreak = {"deaths": 19, "infected": 121}
# outbreak["death"]  → KeyError: 'death'
# 修正：檢查 key 名稱，差一個字母都不行
print(outbreak["deaths"])  # 19
```

```python
# 4) IndexError：列表索引超出範圍
wings = ["1A", "1B", "2A", "2B", "3A", "3B"]
# wings[6]  → IndexError: list index out of range
# 修正：6 個元素，索引是 0-5
print(wings[5])  # "3B"
```

```python
# 5) FileNotFoundError：找不到檔案
# pd.read_csv("data/outbreak.csv")
# → FileNotFoundError: [Errno 2] No such file or directory: 'data/outbreak.csv'
# 修正：確認路徑正確，本教材的資料在 data/synthetic/legionella_outbreak.csv
```

**Debug 速查表：**

| 錯誤類型 | 常見原因 | 修正方式 |
|---------|---------|---------|
| `NameError` | 變數名拼錯 / 未定義 | 檢查拼字和大小寫 |
| `TypeError` | 文字和數字混用 | 用 `int()` / `float()` 轉型 |
| `KeyError` | 字典 key 名稱錯誤 | 用 `dict.keys()` 檢查所有 key |
| `IndexError` | 列表索引超出範圍 | 用 `len()` 確認長度 |
| `FileNotFoundError` | 檔案路徑錯誤 | 用 `!ls` 確認檔案存在 |
| `IndentationError` | 縮排不一致 | 統一用 4 個空格 |
| `SyntaxError` | 忘記冒號、引號不配對 | 仔細看出錯的那一行 |

### 5) try/except——優雅處理意外

:::{admonition} 教學影片：try/except
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/YOUTUBE_ID_01B_05_TRY_EXCEPT" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：try/except 基本語法、疫調資料清洗實例、多重 except → 疫苗接種紀錄清洗 → 盲點：bare except、範圍太大、掩蓋 bug
:::

有時候錯誤是「預期中的意外」——例如資料裡有遺漏值。與其讓程式崩潰，不如告訴 Python 怎麼處理。

```python
# 沒有 try/except：一遇到壞資料就整個崩潰
ages_raw = ["72", "68", "N/A", "75", "unknown", "66"]
ages = []
for val in ages_raw:
    ages.append(int(val))  # "N/A" → ValueError，程式在這裡就停了！
```

```python
# 有 try/except：跳過壞資料，繼續跑
ages_raw = ["72", "68", "N/A", "75", "unknown", "66"]
ages = []
skipped = 0
for val in ages_raw:
    try:
        ages.append(int(val))
    except ValueError:
        skipped += 1

print(f"成功轉換 {len(ages)} 筆，跳過 {skipped} 筆")  # 成功轉換 4 筆，跳過 2 筆
print(f"平均年齡: {sum(ages) / len(ages):.1f}")          # 平均年齡: 70.2
```

**什麼時候該用 try/except？**

| 場景 | 建議 |
|------|------|
| 讀取外部 CSV 檔案 | ✅ 用——檔案可能不存在 |
| 處理使用者輸入的資料 | ✅ 用——格式不可預期 |
| 自己寫的內部計算 | ❌ 不用——先修好邏輯 |
| 除法可能除以零 | ✅ 用——或先用 `if` 檢查 |

---

## Part 3：實用開發技巧

### 6) 字串與迴圈進階

:::{admonition} 教學影片：字串與迴圈進階
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/YOUTUBE_ID_01B_06_STRINGS_LOOPS" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：strip/split/replace、for+range/enumerate、in 成員檢查 → TB 通報檢驗結果清理 → 盲點：strip 不改原值、迴圈中改列表、range 左閉右開
:::

Ch02 處理 CSV 資料時，你會大量操作字串和迴圈。先在這裡打好基礎。

**常用字串方法：**

```python
# 疫調資料常見的髒字串問題
raw_name = "  Legionella pneumophila  "
print(raw_name.strip())      # "Legionella pneumophila"（去除前後空白）

raw_severity = "Mild,Moderate,Severe"
levels = raw_severity.split(",")
print(levels)                # ["Mild", "Moderate", "Severe"]

raw_status = "confirmed "
clean = raw_status.strip().lower()
print(clean)                 # "confirmed"

# 檢查字串開頭/包含
pathogen = "Legionella pneumophila serogroup 1"
print(pathogen.startswith("Legionella"))   # True
print("serogroup" in pathogen)             # True
```

**for 迴圈搭配 range() 和 enumerate()：**

```python
# range()：產生數字序列
# 印出第 1 到第 5 天的新增病例
daily_cases = [3, 7, 12, 8, 15]
for i in range(len(daily_cases)):
    print(f"Day {i+1}: {daily_cases[i]} 例")

# enumerate()：同時拿到索引和值（更 Pythonic）
for i, cases in enumerate(daily_cases, start=1):
    print(f"Day {i}: {cases} 例")
```

**`in` 成員檢查——Ch02 會大量使用：**

```python
# 檢查某個值是否在列表中
high_risk_floors = [2, 3]
patient_floor = 3
if patient_floor in high_risk_floors:
    print("此個案位於高風險樓層")

# 檢查字典是否有某個 key
outbreak = {"pathogen": "Legionella", "cases": 121}
if "deaths" not in outbreak:
    print("字典中沒有死亡人數資料")
```

### 7) uv 進階——管理 Python 版本與套件

:::{admonition} 教學影片：uv 進階
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/YOUTUBE_ID_01B_07_UV_ADVANCED" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：uv python install/pin、uv add 安裝套件、找好用套件、uv sync → 從零建立疫苗覆蓋率分析專案 → 盲點：pip vs uv、忘了 uv run、不提交 uv.lock
:::

Ch00 教了 `uv sync` 安裝教材的所有依賴。這裡進一步介紹 `uv` 的實用功能。

**管理 Python 版本：**

```bash
# 查看目前可用的 Python 版本
uv python list

# 安裝指定版本的 Python
uv python install 3.11

# 鎖定專案使用的 Python 版本（寫入 .python-version）
uv python pin 3.12
```

**安裝第三方套件：**

```bash
# 安裝套件（自動更新 pyproject.toml 和 uv.lock）
uv add pandas

# 安裝指定版本
uv add "pandas>=2.0,<3.0"

# 安裝開發用套件（不會在正式環境使用）
uv add --dev pytest

# 移除套件
uv remove pandas

# 查看目前安裝的所有套件
uv pip list
```

**如何找到好用的第三方套件？**

| 方法 | 網址 / 指令 | 重點看什麼 |
|------|------------|-----------|
| PyPI 搜尋 | `https://pypi.org` 搜尋關鍵字 | 最後更新日期、下載量 |
| GitHub | 搜尋 `topic:epidemiology python` | Stars 數、issue 回覆速度 |
| Awesome 清單 | 搜尋 `awesome-epidemiology` | 社群推薦的套件整理 |

**流行病學常用套件推薦：**

| 套件 | 用途 | 本教材使用章節 |
|------|------|-------------|
| `pandas` | 表格資料處理 | Ch02 起所有章節 |
| `matplotlib` | 基礎繪圖 | Ch02 起所有章節 |
| `seaborn` | 統計圖表 | Ch02, 03 |
| `scipy` | 統計檢定 | Ch03, 05 |
| `lifelines` | 存活分析 | Ch09 |
| `geopandas` | 空間資料 | Ch08 |
| `plotly` | 互動式圖表 | Ch02, 08 |
| `scikit-learn` | 機器學習 | Ch10 |
| `tensorflow` | 深度學習 | Ch11 |

### 8) Jupyter 實用密技

:::{admonition} 教學影片：Jupyter 實用密技
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/YOUTUBE_ID_01B_08_JUPYTER_TIPS" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：! shell 指令、!uv add 安裝套件、? 查說明、Tab 自動完成、%timeit → 快速探索疫調 CSV → 盲點：裝完沒 Restart、! 在 .py 裡用、cell 執行順序
:::

以下技巧讓你在 Jupyter Lab 裡工作更有效率。

**`!` 執行 shell 指令：**

在 code cell 的開頭加上 `!`，就能直接執行終端機指令。

```python
# 查看資料檔案是否存在
!ls data/synthetic/

# 快速預覽 CSV 的前幾行
!head -5 data/synthetic/legionella_outbreak.csv

# 查看檔案行數（了解資料量）
!wc -l data/synthetic/legionella_outbreak.csv

# 查看目前的工作目錄
!pwd
```

**在 Jupyter 中用 uv 安裝套件：**

```python
# 安裝新套件
!uv add seaborn

# 安裝完成後，必須 Restart Kernel 才能 import
# Kernel → Restart Kernel（或按快捷鍵）
```

> ⚠️ **重要**：安裝套件後一定要 Restart Kernel，否則 `import` 會找不到剛裝的套件。

**查看函式說明文件：**

```python
# 用 ? 查看簡要說明
len?

# 用 ?? 查看原始碼（如果有的話）
len??
```

**Tab 自動完成：**

在 Jupyter 中按 `Tab` 鍵可以：
- 補全變數名：打 `out` + Tab → `outbreak`
- 列出物件方法：打 `outbreak.` + Tab → 顯示所有可用方法
- 補全檔案路徑：在字串中打 `"data/` + Tab → 列出目錄內容

**`%timeit` 測量執行時間：**

```python
# 當你好奇某段程式跑多快
%timeit sum(range(10000))
```

**實用 Magic 指令總整理：**

| 指令 | 功能 |
|------|------|
| `!command` | 執行 shell 指令 |
| `?obj` | 查看物件說明 |
| `??obj` | 查看物件原始碼 |
| `%timeit expr` | 測量單行執行時間 |
| `%%timeit` | 測量整個 cell 執行時間 |
| `%who` | 列出目前定義的所有變數 |
| `%whos` | 列出變數 + 型別 + 值 |
| `%pwd` | 顯示工作目錄 |
| `%history` | 顯示輸入歷史 |

---

## 常見錯誤總整理

| 錯誤 | 原因 | 修正 |
|------|------|------|
| `IndentationError` | 縮排不一致或忘記縮排 | 冒號後面的下一行要空 4 格 |
| `ModuleNotFoundError` | 套件沒裝或名字打錯 | `uv add 套件名` 再 Restart Kernel |
| `NameError` | 變數未定義或拼錯 | 檢查拼字，Python 區分大小寫 |
| `TypeError` | 型別不對（如文字做除法） | 先用 `type()` 檢查，再用 `int()` / `float()` 轉型 |
| `KeyError` | 字典 key 不存在 | 用 `.keys()` 或 `if key in dict` 先檢查 |
| `SyntaxError` | 忘記冒號、引號不配對 | 仔細看出錯那一行，通常少了 `:` 或 `"` |
| `TabError` | 混用 Tab 和空格 | Jupyter 預設空格，不要用 Tab |

## 從 Ch01 到 Ch02 的銜接檢查表

在進入 Ch02 之前，確認你能回答以下問題：

- [ ] `import pandas as pd` 這行在做什麼？
- [ ] 為什麼 `if` 下面的程式碼要空 4 格？
- [ ] `type("121")` 和 `type(121)` 有什麼不同？
- [ ] 看到 `NameError: name 'df' is not defined`，你會怎麼做？
- [ ] 怎麼在 Jupyter 中安裝新套件？
- [ ] `"Legionella" in pathogen` 這行在檢查什麼？

如果都能回答，恭喜你準備好進入 Ch02 的 pandas 世界了！

## 練習本

- 課堂筆記：{ref}`01b_python_toolbox.ipynb`
- 作業版：[`01b_python_toolbox_exercise.ipynb`](exercises/01b_python_toolbox_exercise.ipynb)
- 解答版（教師版）：[`01b_python_toolbox_solution.ipynb`](solutions/01b_python_toolbox_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/01b_python_toolbox_solution.ipynb>)
