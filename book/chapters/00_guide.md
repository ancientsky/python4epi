# 00 導讀與工具（新手友善版）

## 你將學到

- 為什麼流行病學需要程式工具（而不只是試算表）
- 為什麼這份教材選 Python，而不是 R 或 Excel
- 為什麼用 `uv` 而不是傳統的 `pip`——以及如何用 `uv` 一站式安裝 Python、套件與 Jupyter Lab
- 虛擬環境是什麼？為什麼流行病學家的多專案工作需要它？
- 手把手完成你的第一個流行病學 Hello World（uv + pandas + 流行曲線）
- 除了 pandas，還有哪些資料清理工具可以選？
- Jupyter Lab、`.py` 腳本、VS Code——哪種寫法適合什麼場景？`.ipynb` 怎麼轉成 `.py` 做排程？
- Git 版本控制基礎：流行病學家最常用的情境與指令（包含 Excel 檔案協作）
- 如何一步一步在你的電腦上安裝好所有工具

---

## 先說一個故事：禮拜五下午 4 點的電話

想像你是一位剛進入衛生局的新人。禮拜五下午 4 點，主管打電話來：

> 「某護理之家疑似退伍軍人症群聚，目前通報 280 位住民中有上百人出現肺炎症狀、已有住民死亡。我需要你在 **今天下班前** 給我：侵襲率多少？致死率多少？哪個樓層最嚴重？淋浴設備是不是感染源？能不能畫一張發病時間的流行曲線？」

你打開手邊的 Excel，280 筆資料、32 個欄位——年齡、共病、樓層、暴露史、發病日、住院日、死亡日⋯⋯光是篩選和交叉分析就讓你頭昏眼花。更別說主管接著又問：「幫我做個 2×2 表看淋浴使用的風險比」「按樓層分層再算一次」「下禮拜還會有多少新個案？」。這時你會發現——

- Excel 的列數限制開始卡你
- 手動篩選、複製貼上很容易出錯
- 每次主管問「換個條件再算一次」，你就要從頭重做
- 同事接手你的檔案，根本不知道你當初怎麼算的

**程式不是要取代你的流病判斷，而是幫你把「重複、容易出錯、需要交接」的步驟自動化。** 你寫一次程式碼，以後不管資料換成 300 筆還是 30,000 筆，按一個鍵就能重跑、檢查、交給下一個人。

這就是為什麼越來越多流行病學工作者開始學程式。

---

## 教學影片

每個概念都有配套的動畫教學影片（約 3 分鐘），嵌在下方對應的小節中。影片包含：主線教學 → 額外防疫範例 → 初學者常見盲點破解。

建議先看影片再讀文字，學習效果更好！

## 為什麼不用 Excel / Google Sheets 就好？

:::{admonition} 教學影片：為什麼用 Python
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/eMWQ-IqYjvM" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：Excel 的痛點 → Python 的優勢 → Python vs R → COVID-19 大規模疫調範例 → 盲點：數學、先學完、版本問題
:::

你可能會想：「我用 Excel 用了好幾年，為什麼還要學新工具？」

Excel 和 Google Sheets 在很多場景確實夠用，尤其是**小量資料、一次性的快速查看**。但流行病學分析有幾個特殊需求，試算表在這些地方會遇到瓶頸：

| 情境 | 試算表的困難 | 程式的優勢 |
|------|-------------|-----------|
| 資料量大（數千～數萬筆 line list） | 操作變慢、容易當機 | 幾秒內處理完，不受列數限制 |
| 重複分析（每週更新資料重算指標） | 每次都要手動重做一遍 | 跑同一份程式碼，幾秒產出新結果 |
| 可重現性（別人要驗證你的結果） | 「你是怎麼算出來的？」很難回答 | 程式碼就是完整的分析紀錄 |
| 多步驟串接（清理 → 統計 → 畫圖 → 報表） | 需要在多個工作表之間切換 | 一份腳本從頭跑到尾 |
| 進階分析（迴歸、時間序列、機器學習） | 基本上做不到 | 一行指令呼叫成熟的統計套件 |
| 團隊協作與版本控制 | 「final_v2_真的最終版.xlsx」 | Git 追蹤每一次修改 |

**重點不是「Excel 不好」，而是「不同工具適合不同階段」。** 如果你的工作只需要看幾十筆通報、算個百分比，Excel 完全夠。但如果你想要：

- 處理大量監測資料
- 自動產出每週報表
- 做更深入的統計或預測模型
- 讓你的分析能被同事重跑、檢驗

那學一個程式工具，長期來看會幫你省下非常多時間。

---

## 為什麼選 Python？R 不是更多流行病學家在用嗎？

這是一個非常合理的問題。**R 在傳統流行病學領域確實有深厚的根基**，像 `epitools`、`EpiEstim`、`surveillance` 這些套件都非常成熟，WHO 和各國 CDC 也有大量 R 的教材。

那為什麼這份教材選 Python？原因有三：

### 1. 從統計到機器學習的「一條龍」

流行病學正在快速演進。除了傳統的描述性統計和推論統計，越來越多研究和實務會用到：

- **機器學習**（例如用隨機森林預測疫情擴散風險）
- **深度學習**（例如用 LSTM 預測登革熱病例趨勢）
- **自然語言處理**（例如從社群媒體偵測疫情訊號）

Python 在這些領域的生態系（`scikit-learn`、`PyTorch`、`transformers`）遠比 R 成熟。如果你用 R 做完傳統統計，要轉到 ML/DL 時又得學 Python，等於多學一次。**用 Python 打通整條路，你只需要學一個語言。**

### 2. 資料工程與自動化更順

在真實的公衛工作中，「分析」只是其中一步。你可能還需要：

- 自動從資料庫抓最新通報資料
- 每天早上自動跑一次指標計算
- 把結果寫入報表或推送到 LINE / Email

Python 在這些**自動化、排程、系統串接**的工作上比 R 強很多，因為它本來就是一個通用程式語言。

### 3. 就業市場與跨領域合作

如果你未來會跟資料工程師、軟體開發者合作（例如建置疫情儀表板、資料平台），他們幾乎都用 Python。會 Python 讓你更容易跟技術團隊溝通。

### 那我已經會 R，怎麼辦？

**完全不需要放棄 R。** R 仍然是優秀的統計工具。如果你已經用 R 做得很順，可以繼續用。這份教材的目標是：**如果你想多學一個工具，或者你是從零開始，Python 是一個值得投資的選擇。**

---

## 為什麼用 `uv` 而不是傳統的 `pip`？

:::{admonition} 教學影片：uv 與環境設定
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/AnPBQW8Vqq0" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：為什麼不能直接 pip install → 虛擬環境比喻 → 安裝 uv → uv 三步驟工作流 → 盲點：command not found、uv run、pyproject.toml
:::

如果你 Google「Python 安裝套件」，幾乎所有教學都會教你用 `pip install`。那為什麼我們要用 `uv` 這個比較新的工具？

### 先說 `pip` 的問題

`pip` 是 Python 內建的套件安裝工具，已經存在很多年了。它能用，但在教學場景中有幾個痛點：

- **環境衝突**：你可能聽過「我的電腦上可以跑，但同事的不行」。`pip` 裝的套件版本不一致，是新手最常遇到的挫折。
- **需要手動管理虛擬環境**：`python -m venv`、`source activate`… 光是啟動環境的步驟就能讓新手迷路。
- **速度慢**：裝一堆資料科學套件（pandas、matplotlib、scikit-learn…）可能要等好幾分鐘。

### `uv` 解決了什麼

[`uv`](https://docs.astral.sh/uv/) 是一個用 Rust 語言寫的新一代 Python 套件管理工具，特色是：

- **快非常多**：安裝速度比 `pip` 快 10～100 倍（不誇張）。
- **連 Python 都幫你裝**：不用事先去官網下載 Python，`uv` 一行指令就幫你搞定。
- **自動管理虛擬環境**：你不需要手動建立、啟動虛擬環境，`uv sync` 一個指令就搞定。
- **鎖定版本**：`uv.lock` 檔案確保你跟同學、同事用的套件版本一模一樣，不會出現「我的可以跑，你的不行」。
- **一個指令做所有事**：安裝 Python、安裝套件、執行程式、管理環境，全部用 `uv` 開頭。

### 實際差異：`pip` vs `uv`

| 任務 | 傳統做法（`pip`） | 本教材做法（`uv`） |
|------|-------------------|-------------------|
| 安裝 Python | 去官網下載、手動安裝 | `uv python install 3.13` |
| 建立環境 | `python -m venv .venv && source .venv/bin/activate` | `uv sync`（自動建立並啟用） |
| 安裝套件 | `pip install pandas matplotlib` | `uv add pandas matplotlib` 或 `uv sync` |
| 開 notebook | `jupyter lab`（要先確定裝過） | `uv run jupyter lab` |
| 跑測試 | `pytest`（要先確定環境對） | `uv run pytest` |
| 確保版本一致 | 自己管 `requirements.txt`（容易忘記更新） | `uv.lock` 自動鎖定 |

**簡單說：`uv` 讓你少踩 80% 的環境地雷，多花時間在真正的學習上。**

---

## 先放心：你不用「先很會寫程式」

讀到這裡，你可能還是有點緊張：「我真的一行程式都沒寫過，能學嗎？」

**可以。** 這份教材是給公衛、流病、醫學背景的學習者設計的。設計原則是：

1. **每段程式碼都可以直接複製、貼上、執行**——你不需要從空白畫面開始寫。
2. **先看結果，再理解原理**——每章都會先跑出一個圖表或數字，再回頭解釋怎麼做到的。
3. **用流病情境學程式**——不會教你寫計算機或猜數字遊戲，所有範例都是 line list、侵襲率、流行曲線。

你的學習路徑是：

```
複製程式碼 → 執行看結果 → 改幾個數字再跑 → 慢慢理解邏輯
```

程式能力會在章節中自然成長，不需要先去上完一整門「Python 入門」才回來。

---

## 安裝工具：只要裝 `uv`，其他它幫你搞定

接下來是實際的安裝步驟。好消息是：**你只需要安裝一個工具——`uv`。** Python 本身不用事先安裝，`uv` 會自動幫你下載並管理正確版本的 Python。

### 等等，我不用先安裝 Python 嗎？

**不用！** 這是 `uv` 最方便的地方之一。傳統的方式是：先去 Python 官網下載安裝程式 → 安裝 Python → 再來裝套件管理工具。但 `uv` 把這些步驟合在一起了：

| 傳統方式 | 用 `uv` 的方式 |
|----------|----------------|
| ① 去官網下載 Python 安裝程式 | ① 安裝 `uv`（一行指令） |
| ② 安裝 Python | ② `uv python install 3.13`（`uv` 自動下載 Python） |
| ③ 設定環境變數 PATH | ③ 不需要，`uv` 幫你管理 |
| ④ 安裝 pip / 建立虛擬環境 | ④ 不需要，`uv sync` 全部搞定 |

**簡單說：裝好 `uv`，你就什麼都有了。**

如果你的電腦上已經有 Python 也沒關係，`uv` 會自動偵測並使用它，不會衝突。

### 安裝 `uv`

#### macOS / Linux

打開終端機（macOS 可以用 Spotlight 搜尋 "Terminal"），輸入：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安裝完關掉終端機再重新打開，然後驗證：

```bash
uv --version
```

#### Windows（PowerShell）

按 `Win + X`，選擇「Windows PowerShell」或「終端機」，輸入：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

關掉 PowerShell 再重新打開，然後驗證：

```powershell
uv --version
```

> **驗證成功**：看到 `uv 0.x.x`（任何版本號）就可以了。
>
> **常見問題**：如果顯示 `command not found: uv`，請關掉終端機再重新打開一次。安裝程式會把 `uv` 加入你的 PATH，但需要重新啟動終端機才會生效。

### 用 `uv` 安裝 Python

安裝好 `uv` 之後，一行指令就能安裝 Python：

```bash
uv python install 3.13
```

`uv` 會自動下載 Python 3.13 並安裝到它自己管理的目錄中，不會跟你電腦上現有的 Python 衝突。

驗證：

```bash
uv run python --version
# 你會看到：Python 3.13.x
```

> **為什麼建議 3.13？** Python 3.13 是目前最新的穩定版（2024 年 10 月發布），效能更好、錯誤訊息更清楚，而且所有主要的資料科學套件都已支援。如果你的電腦上已經有 Python 3.12 或 3.11，仍然可以正常使用本教材，但我們建議用最新版以獲得最佳體驗。

---

## 為什麼需要「虛擬環境」？跟流行病學有什麼關係？

你可能會聽到有人說「記得要用虛擬環境」，覺得又是一個程式術語。讓我用流病的情境來解釋：

### 問題：套件版本打架

想像你同時在做兩個專案：

- **專案 A：登革熱週報**——用 `pandas 1.5`，一年前寫的，跑得很穩
- **專案 B：COVID 儀表板**——用 `pandas 2.2`，需要新功能

如果兩個專案共用同一個 Python 環境，裝了 `pandas 2.2` 之後，專案 A 可能就壞了（因為某些語法在新版改了）。裝回 `pandas 1.5`，專案 B 又壞了。

**虛擬環境（virtual environment）就是幫每個專案建立一個「獨立的套件空間」。** 專案 A 有自己的 pandas 1.5，專案 B 有自己的 pandas 2.2，互不干擾。

```
你的電腦
├── 專案 A（登革熱週報）/.venv/
│   └── pandas 1.5、matplotlib 3.7 ...
├── 專案 B（COVID 儀表板）/.venv/
│   └── pandas 2.2、plotly 6.0 ...
└── 專案 C（本教材）/.venv/
    └── pandas 2.2、matplotlib 3.10 ...
```

### `uv` 怎麼管理虛擬環境？

好消息：**你不需要手動建立虛擬環境，`uv` 會自動幫你做。** 當你在專案資料夾裡執行 `uv sync`，它會：

1. 在資料夾內建立一個 `.venv/` 目錄（這就是虛擬環境）
2. 安裝 `pyproject.toml` 裡列出的所有套件到 `.venv/` 中
3. 之後每次用 `uv run ...` 執行任何指令，都自動使用這個虛擬環境

你完全不需要執行什麼 `source .venv/bin/activate`——`uv run` 會自動處理。

```bash
# 這一行就同時建好虛擬環境 + 安裝所有套件
uv sync

# 之後所有指令都用 uv run 開頭，自動在虛擬環境中執行
uv run python my_script.py
uv run jupyter lab
uv run pytest
```

---

## `uv` 完整操作指南：從安裝套件到開 Jupyter Lab

### 情境 1：跟著本教材學習（最簡單）

如果你是下載本教材的程式碼來學習，只需要：

```bash
cd python4epi        # 進入教材資料夾
uv sync              # 安裝所有套件（第一次約 1-2 分鐘）
uv run jupyter lab   # 開啟 Jupyter Lab
```

就這樣三行，所有東西都裝好了——pandas、matplotlib、scikit-learn、Jupyter Lab 全部包含在內。

### 情境 2：我想自己建一個新的流病分析專案

假設你想從頭建立一個登革熱分析專案：

```bash
# 建立專案資料夾
mkdir dengue-analysis
cd dengue-analysis

# 初始化專案（uv 會建立 pyproject.toml）
uv init

# 指定 Python 版本
uv python pin 3.13

# 安裝你需要的套件
uv add pandas matplotlib jupyterlab openpyxl

# 開啟 Jupyter Lab
uv run jupyter lab
```

**`uv add` 做了什麼？** 它會：
1. 自動下載並安裝指定的套件
2. 把套件名稱寫入 `pyproject.toml`（套件清單）
3. 更新 `uv.lock`（精確版本鎖定檔案）
4. 如果虛擬環境還不存在，順便建立

以後你或同事在另一台電腦上只要執行 `uv sync`，就能裝到一模一樣的環境。

### 情境 3：在 Jupyter Lab 裡面安裝新套件

你已經在 Jupyter Lab 裡面寫程式了，突然發現需要一個新套件（例如 `seaborn` 用來畫更漂亮的圖）。

**方法 A：回到終端機安裝（推薦）**

```bash
# 在終端機執行（Jupyter Lab 不用關）
uv add seaborn
```

然後回到 Jupyter Lab，重新啟動 kernel（選單 → Kernel → Restart Kernel），就能 `import seaborn` 了。

**方法 B：在 notebook cell 裡安裝**

如果你不想切到終端機，也可以在 notebook 的 code cell 裡直接執行：

```python
# 在 notebook cell 中執行（注意前面的驚嘆號）
!uv add seaborn
```

執行完之後同樣需要重新啟動 kernel。

```{tip}
建議用方法 A（終端機安裝）。方法 B 雖然方便，但有時候會因為路徑問題找不到 `uv`。如果你用方法 B 遇到 `uv: command not found`，就改用方法 A。
```

### `uv` 指令速查表

| 我想要… | 指令 | 說明 |
|---------|------|------|
| 安裝 Python | `uv python install 3.13` | 下載指定版本的 Python |
| 初始化新專案 | `uv init` | 建立 `pyproject.toml` |
| 指定專案的 Python 版本 | `uv python pin 3.13` | 建立 `.python-version` 檔案 |
| 安裝所有套件 | `uv sync` | 依照 `pyproject.toml` 安裝 |
| 新增一個套件 | `uv add pandas` | 安裝並記錄到 `pyproject.toml` |
| 新增多個套件 | `uv add pandas matplotlib seaborn` | 一次裝多個 |
| 移除一個套件 | `uv remove seaborn` | 移除並從 `pyproject.toml` 刪除 |
| 在虛擬環境中執行指令 | `uv run python script.py` | 自動使用虛擬環境 |
| 開 Jupyter Lab | `uv run jupyter lab` | 在虛擬環境中啟動 |
| 跑測試 | `uv run pytest` | 在虛擬環境中執行測試 |
| 看目前裝了哪些套件 | `uv pip list` | 列出所有已安裝套件 |

---

## 手把手教學：從零開始的流行病學 Hello World

:::{admonition} 教學影片：第一支程式 Hello Epi
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/VcxttnJxwG4" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：git clone + uv sync → 開 Jupyter → 跑分析 → 看到侵襲率 43.2% → 盲點：clone 失敗、sync 很慢、紅色 Warning
:::

光看指令可能還是抽象。讓我們從一台什麼都沒裝的電腦開始，一步一步做出流行病學家的第一個「Hello World」——不是印出一行字，而是**讀取一份護理之家群聚事件的 line list、計算侵襲率與致死率、畫一張流行曲線**。

### Step 1：安裝 uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows（PowerShell）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安裝完**關掉終端機再重新打開**。

### Step 2：建立專案

```bash
mkdir epi-hello-world
cd epi-hello-world
uv init
uv python pin 3.13
```

### Step 3：安裝流病分析套件

```bash
uv add pandas matplotlib jupyterlab openpyxl
```

這一行會安裝：
- `pandas`：讀取和處理表格資料（line list）
- `matplotlib`：畫圖（流行曲線）
- `jupyterlab`：互動式程式編輯環境
- `openpyxl`：讓 pandas 能讀寫 Excel（`.xlsx`）檔案

### Step 4：開啟 Jupyter Lab

```bash
uv run jupyter lab
```

瀏覽器會自動打開。點右邊的 **「Python 3 (ipykernel)」** 建立一個新的 notebook。

### Step 5：在 notebook 裡輸入以下程式碼

每一個 cell 按 `Shift + Enter` 執行：

**Cell 1：讀入護理之家退伍軍人症群聚的 line list**

```python
import pandas as pd

# 讀入松柏護理之家退伍軍人症群聚事件的 line list（280 位住民）
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# 看前幾筆——每一列是一位住民的完整紀錄
df.head(10)
```

**Cell 2：計算侵襲率與致死率**

```python
# len(df) = 資料有幾列（= 住民人數）
total_residents = len(df)

# (df["clinical_severity"] != "not_ill") → 產生 True/False 的 Series
# .sum() → True 當作 1 加總 = 感染人數
infected = (df["clinical_severity"] != "not_ill").sum()
deaths = (df["outcome"] == "dead").sum()

# 侵襲率 = 感染人數 ÷ 全體人數 × 100
attack_rate = infected / total_residents * 100
# 致死率（CFR）= 死亡人數 ÷ 感染人數 × 100（注意分母是感染者！）
cfr = deaths / infected * 100

# f-string：f"..." 裡面的 {變數名} 會被替換成變數的值
# :.1f → 顯示到小數點後 1 位
print(f"住民總數：{total_residents} 人")
print(f"感染人數：{infected} 人")
print(f"侵襲率：{attack_rate:.1f}%")
print(f"死亡人數：{deaths} 人")
print(f"致死率 (CFR)：{cfr:.1f}%")
```

**Cell 3：畫流行曲線（epidemic curve）**

```python
import matplotlib.pyplot as plt  # plt = matplotlib 的慣用縮寫

# -- CJK font setup (避免中文標籤顯示為方框 □□□) --
# matplotlib 預設只認英文字型，中文字會變成「豆腐塊」
# 下面這行告訴它：「依序嘗試這些中文字型，找到哪個就用哪個」
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False  # 防止負號顯示為方塊
plt.style.use("ggplot")        # 套用學術風格（淡灰背景 + 白色格線）
plt.rcParams["figure.dpi"] = 150  # 提高圖片解析度（預設 100 太模糊）

# 將發病日期的文字轉為日期格式，並算出「每天有幾人發病」
onset = pd.to_datetime(df["symptom_onset_date"])  # 文字 → 日期
epi_curve = onset.dropna().dt.date.value_counts().sort_index()
# dropna() = 丟掉沒有發病日期的人（未感染者）
# .dt.date = 只取日期（去掉時分秒）
# .value_counts() = 每個日期出現幾次 = 每日病例數
# .sort_index() = 按日期排序

# fig = 整張圖紙, ax = 圖紙上的畫布（所有繪圖指令都對 ax 操作）
fig, ax = plt.subplots(figsize=(10, 4))  # figsize=(寬, 高) 單位是英吋
ax.bar(epi_curve.index, epi_curve.values, color="#2980B9", edgecolor="white")
ax.set_xlabel("Onset Date（發病日期）")   # X 軸標籤
ax.set_ylabel("Cases（病例數）")          # Y 軸標籤
ax.set_title("Epidemic Curve — 松柏護理之家退伍軍人症群聚")  # 圖表標題
fig.autofmt_xdate()    # 自動旋轉日期標籤，避免重疊
plt.tight_layout()     # 自動調整邊距，防止標籤被裁切
plt.show()             # 顯示圖表
```

**Cell 4：按樓層翼區統計侵襲率**

```python
# 建立感染旗標：not_ill 以外都算感染，True→1, False→0
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# 按樓層 + 翼區分組，同時算住民數和感染數
wing_summary = df.groupby(["floor", "wing"]).agg(
    total=("case_id", "count"),     # 每組有幾位住民
    cases=("infected", "sum"),      # 每組有幾位感染者
).reset_index()  # 把分組索引攤平回普通欄位

# 侵襲率 = 感染人數 ÷ 該區住民數 × 100（注意分母是各區人數！）
wing_summary["attack_rate_%"] = (wing_summary["cases"] / wing_summary["total"] * 100).round(1)

wing_summary  # 在 Jupyter 裡，最後一行會自動顯示成表格
```

### Step 6：看到結果

你現在應該看到：
- 一張表格顯示 line list 的前 10 筆資料（包含年齡、共病、暴露史等 32 個欄位）
- 侵襲率 43.2%、致死率 15.7%
- 一張**流行曲線長條圖**，顯示 1 月 20 日前後為發病高峰——典型的共同暴露源型態
- 按樓層翼區分的侵襲率比較（2–3 樓 B 翼明顯較高）

**恭喜！這就是流行病學家用 Python 做的第一個分析。** 整個過程只需要 `uv` 一個工具就能搞定——不用事先裝 Python、不用設定虛擬環境、不用管 pip。

```{tip}
試著修改上面的程式碼：改用 `"shower_use"` 欄位分組看侵襲率、或只篩選 `"confirmed"` 個案畫流行曲線。每次改完按 `Shift + Enter` 就能立刻看到結果。這就是程式的威力——改一個條件，整個分析自動重算。
```

---

## 程式碼裡的 `#` 是什麼？——Python 註解入門

你剛才在 Hello World 的程式碼裡應該有看到這樣的東西：

```python
# 讀入松柏護理之家退伍軍人症群聚事件的 line list
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
```

那一行 `#` 開頭的文字就是**註解（comment）**——Python 會**完全忽略**它，不會執行。

### 為什麼需要註解？

- **給自己看**：三個月後回來看程式碼，你會忘記當初為什麼這樣寫
- **給同事看**：疫調報告要交接給別人時，有註解他才看得懂你的分析邏輯
- **給審稿人看**：期刊要求可重現研究（reproducible research），註解是程式碼的說明書

### 註解的寫法

```python
# 整行註解：# 後面的所有文字都不會被執行
attack_rate = infected / total * 100  # 行尾註解：程式碼後面也可以加

# 多行註解？Python 沒有像 C 語言的 /* ... */
# 每一行都要加 #（這其實是好事，因為對齊起來更整齊）

# ✅ 好的註解：解釋「為什麼」
# 用中位數填補年齡遺漏值，因為平均數容易受極端值影響
df["age"].fillna(df["age"].median(), inplace=True)

# ❌ 壞的註解：只重複程式碼已經說的事
# 把 x 設為 5（這誰看不出來？）
x = 5
```

```{tip}
**新手建議：先養成加 `#` 註解的習慣。** 哪怕一開始寫得很囉嗦也沒關係，比完全不寫好一百倍。隨著經驗增加，你會越來越知道哪些地方需要解釋、哪些不用。
```

---

## Jupyter 筆記本中的 Markdown 格式

Jupyter Lab 的 cell 有兩種類型：

| Cell 類型 | 用途 | 切換方式 |
|----------|------|---------|
| **Code** | 寫 Python 程式碼 | 選中 cell → 按 `Y` |
| **Markdown** | 寫文字說明、標題、列表 | 選中 cell → 按 `M` |

Markdown cell 讓你的 notebook 不只是一堆程式碼，而是一份**圖文並茂的分析報告**。

### 最常用的 Markdown 語法

```markdown
# 大標題（一個 # 號）
## 二級標題（兩個 # 號）
### 三級標題（三個 # 號）

**粗體文字**（前後兩個星號）
*斜體文字*（前後一個星號）
`行內程式碼`（前後一個反引號）

- 無序列表項目 1
- 無序列表項目 2

1. 有序列表項目 1
2. 有序列表項目 2

> 引用文字（像這樣加 > 在前面）

| 欄位 | 說明 |
|------|------|
| age  | 年齡 |
| sex  | 性別 |
```

### 在 Notebook 裡的使用範例

假設你正在分析松柏護理之家的資料，Markdown cell 可以這樣寫：

```markdown
## 侵襲率分析

本分析使用松柏護理之家退伍軍人症群聚事件的 line list（n=280）。

### 主要發現

1. **侵襲率**：43.2%（121/280）
2. **致死率**：15.7%（19/121）
3. 2-3 樓 B 翼的侵襲率明顯較高

> ⚠️ 注意：致死率的分母是感染人數（121），不是全體住民（280）
```

### 常用小技巧

- **快速切換**：在命令模式（按 `Esc`）下，按 `M` 把 cell 變成 Markdown，按 `Y` 變回 Code
- **執行 Markdown**：跟 Code cell 一樣按 `Shift + Enter`，Markdown 就會渲染成漂亮的格式
- **雙擊編輯**：雙擊已渲染的 Markdown cell 可以回到編輯模式
- **用 Markdown 做分析筆記**：好習慣是每段分析前加一個 Markdown cell 說明「這段在做什麼、為什麼」

```{tip}
**好的 notebook = 程式碼 + Markdown 說明 + 圖表輸出。** 把你的 notebook 想像成一份疫調報告，任何人打開它都能理解你的分析過程。這就是可重現研究（reproducible research）的精神。
```

---

## 除了 pandas，還有哪些資料清理工具？

`pandas` 是 Python 生態系中最主流的表格資料處理套件，本教材也以它為主。但隨著你處理的資料量越來越大，你可能會聽到其他選擇。以下是一個簡要的比較：

| 套件 | 特色 | 適合場景 | 安裝方式 |
|------|------|----------|----------|
| **pandas** | 最多人用、教材最多、功能最完整 | 大多數流病分析（數千～數十萬筆） | `uv add pandas` |
| **polars** | 速度極快（比 pandas 快 5～50 倍）、記憶體更省 | 大量資料（百萬筆以上的監測資料） | `uv add polars` |
| **DuckDB** | 用 SQL 語法查表格資料，不需要資料庫伺服器 | 習慣 SQL 的人、超大 CSV 檔案 | `uv add duckdb` |
| **pyjanitor** | 在 pandas 基礎上加入更直覺的資料清理語法 | 讓清理步驟更易讀 | `uv add pyjanitor` |

### 哪個最適合初學者？

**先學 pandas 就對了。** 原因是：

1. **95% 的教材、範例、StackOverflow 回答都用 pandas**——你遇到問題時最容易找到解法
2. **pandas 的功能對流病分析絕對夠用**——除非你要處理數百萬筆以上的資料，否則不需要換
3. **其他工具的語法跟 pandas 很像**——學會 pandas 之後，轉去 polars 或 DuckDB 的學習成本很低

### 什麼時候考慮其他工具？

| 你遇到的問題 | 可以考慮的工具 |
|-------------|---------------|
| pandas 讀 CSV 很慢（超過 100 萬筆） | `polars`（讀取速度快很多倍） |
| 記憶體不夠（筆電只有 8GB） | `polars`（記憶體使用更省） |
| 你本來就會 SQL | `duckdb`（直接對 CSV/Parquet 下 SQL） |
| 清理步驟太多，程式碼變得很長 | `pyjanitor`（方法鏈更好讀） |

```{tip}
本教材所有章節都使用 pandas。如果你未來工作中遇到效能瓶頸，再回來看這張表選擇合適的工具即可。不需要現在就學多個套件。
```

---

## 為什麼建議用 Jupyter Lab？不能直接寫 `.py` 嗎？

:::{admonition} 教學影片：Jupyter Lab 入門
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/iELUPwdPk7M" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：什麼是 Jupyter → 啟動方法 → Cell 概念 → Shift+Enter → 盲點：執行順序、Restart Kernel、[*] 卡住
:::

你可能會想：「程式不就是一個文字檔嗎？為什麼要用 Jupyter Lab 這個看起來像網頁的東西？」

這是一個很好的問題。答案是：**要看你的目的是什麼。** 不同的工具適合不同的工作階段。

### Jupyter Lab 的優勢：「邊寫邊看結果」

流行病學分析有一個特點：你通常是**一邊探索資料、一邊做決定**。

比如你拿到一份 line list：
1. 先看看資料長什麼樣（`df.head()`）
2. 發現日期欄位格式不對，清理一下
3. 算個侵襲率，看看數字對不對
4. 畫一張流行曲線，發現有一天的病例數異常高
5. 回頭看那天的原始資料，原來是重複通報
6. 刪掉重複的，重畫一次

這個過程是**互動式、反覆試探**的——你不會一開始就知道最終的分析步驟是什麼。

Jupyter Lab 的 notebook（`.ipynb` 檔案）正好適合這種工作方式：

- **一格一格執行**：寫一段程式碼按 `Shift + Enter`，馬上看到結果
- **圖表直接顯示在程式碼下方**：不用另開視窗看圖
- **可以穿插文字說明**：用 Markdown cell 寫「這一步是在算各區的侵襲率」
- **結果跟程式碼放在一起**：同事打開你的 notebook 就能看到完整的分析過程和結果

### 那 `.py` 腳本適合什麼？

`.py` 檔案就是一個純文字的 Python 程式。它沒有「一格一格」的概念——你按「執行」，整個檔案從頭跑到尾。

**`.py` 適合的場景是「你已經知道要做什麼步驟，想讓它自動跑」：**

| 場景 | 適合的工具 | 原因 |
|------|-----------|------|
| 探索新資料、試不同分析方法 | Jupyter Lab（`.ipynb`） | 需要邊看邊調整 |
| 每週固定的疫情報表 | `.py` 腳本 | 步驟固定，自動執行 |
| 建立可重複使用的函式庫 | `.py` 模組 | 讓多個 notebook 都能呼叫 |
| 排程自動化（每天早上 8 點跑一次） | `.py` 腳本 | 排程工具只能跑 `.py`，不能跑 `.ipynb` |
| 學習、教學、分享分析 | Jupyter Lab（`.ipynb`） | 圖文並茂，同事看得懂 |

**實務上的理想流程是：**

```
用 notebook 探索、實驗（.ipynb）
         ↓
分析步驟確定後，整理成腳本（.py）
         ↓
用排程工具自動執行（cron / Windows 工作排程器）
```

### 其他編輯器：VS Code、PyCharm

除了 Jupyter Lab，你也可以用其他程式編輯器寫 Python：

| 編輯器 | 特色 | 適合誰 |
|--------|------|--------|
| **Jupyter Lab** | 互動式、圖表即時顯示、適合探索分析 | 流病分析師、資料科學初學者 |
| **VS Code** | 功能全面、可以同時編輯 `.py` 和 `.ipynb`、有 AI 輔助 | 想要一站式開發環境的人 |
| **PyCharm** | 專為 Python 設計、強大的偵錯工具 | 進階 Python 開發者 |
| **Google Colab** | 免費雲端 Jupyter，不用安裝任何東西 | 電腦效能不夠、想用免費 GPU |

```{tip}
**本教材建議初學者用 Jupyter Lab。** 當你比較熟悉之後，可以試試 VS Code——它可以直接打開 `.ipynb` 檔案（體驗跟 Jupyter Lab 幾乎一樣），同時也能編輯 `.py` 檔案，兩種格式在同一個環境中搞定。
```

### 把 `.ipynb` 轉成 `.py`：三種方法

當你的分析流程確定了，想把 notebook 轉成 `.py` 腳本（例如要排程自動執行），有三種方式：

#### 方法 1：在 Jupyter Lab 裡直接匯出

在 Jupyter Lab 的選單中：

```
File → Save and Export Notebook As → Executable Script
```

這會產生一個 `.py` 檔案，把所有 code cell 串起來，Markdown cell 會變成 `# ` 開頭的註解。

#### 方法 2：用 `jupyter nbconvert` 指令

```bash
uv run jupyter nbconvert --to script my_analysis.ipynb
```

這會在同一個目錄下產生 `my_analysis.py`。

如果你有很多 notebook 要一次轉換：

```bash
uv run jupyter nbconvert --to script notebooks/*.ipynb
```

#### 方法 3：手動整理（最推薦用於正式的排程腳本）

前兩種方法轉出來的 `.py` 會包含一些多餘的東西（例如 `# In[1]:` 之類的 cell 標記）。如果這是要長期使用的排程腳本，建議手動整理：

1. 打開轉出的 `.py`
2. 刪掉 `# In[1]:` 這類的 cell 標記
3. 刪掉探索性的程式碼（例如 `df.head()`、`print(df.shape)` 這些只是在看資料的步驟）
4. 把重要的步驟保留下來，加上清楚的註解
5. 把輸出路徑（例如報表存檔的位置）改成絕對路徑

本教材中的 `notebooks/run_sitrep.py` 就是一個整理好的 `.py` 腳本範例——它讀取 line list、計算 CFR 和侵襲率、輸出各區統計表：

```bash
uv run python notebooks/run_sitrep.py
```

### 實戰：把分析腳本排程自動執行

假設你整理好了一個 `weekly_report.py`，要讓它每週一早上 8 點自動執行、產出登革熱週報。

#### Linux / macOS：用 `cron`

```bash
# 打開 cron 編輯器
crontab -e

# 加入這一行（每週一早上 8 點執行）
0 8 * * 1 cd /path/to/your/project && uv run python weekly_report.py >> /path/to/logs/weekly_report.log 2>&1
```

各欄位的意思：

```
0 8 * * 1
│ │ │ │ │
│ │ │ │ └── 星期幾（1 = 星期一）
│ │ │ └──── 月份（* = 每月）
│ │ └────── 日期（* = 每天）
│ └──────── 小時（8 = 早上 8 點）
└────────── 分鐘（0 = 整點）
```

#### Windows：用「工作排程器」

1. 搜尋「工作排程器」或「Task Scheduler」
2. 點「建立基本工作」
3. 設定觸發條件：每週一上午 8:00
4. 動作：啟動程式
   - 程式或指令碼：`cmd`
   - 新增引數：`/c cd /d C:\path\to\your\project && uv run python weekly_report.py`

#### 排程腳本的建議

| 建議 | 原因 |
|------|------|
| 在腳本開頭寫好輸入/輸出路徑 | 排程時的工作目錄可能不是你預期的 |
| 加上 `try/except` 錯誤處理 | 排程執行時你不在電腦前，要把錯誤訊息存起來 |
| 把結果存成檔案，不要只 print | `print` 只會輸出到 log，存檔才看得到報表 |
| 先手動跑一次確認沒問題 | 再設定排程，避免每週一都跑出錯誤 |

### 總結：流行病學家的工具選擇指南

```
第一步：學習 & 探索分析
  → Jupyter Lab（.ipynb）

第二步：分析流程固定後
  → 轉成 .py 腳本

第三步：自動化 & 排程
  → cron / 工作排程器 + .py 腳本

進階：想要更好的開發體驗
  → VS Code（同時支援 .ipynb 和 .py）
```

**不用一開始就選定一個工具。** 先用 Jupyter Lab 把分析做出來，需要排程再轉成 `.py`，之後覺得 VS Code 更順手就換過去。工具是為你服務的，不是拿來焦慮的。

---

## Git 是什麼？為什麼流行病學家需要它？

:::{admonition} 教學影片：Git 版本控制
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/SdtrxhPbRqk" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：版本混亂的惡夢 → Git 時光機比喻 → 三區域 → git add/commit/push → 盲點：git add .、commit message、push 被拒
:::

### 先說一個場景

你花了一整天寫好登革熱疫情分析腳本，跑出漂亮的流行曲線。隔天主管說：「把分母從確診數改成通報數」，你照做了。又過了兩天，主管說：「還是改回來好了。」

如果你的檔案叫 `analysis.py`，這時候你手邊可能是這樣的狀態：

```
analysis.py
analysis_v2.py
analysis_v2_final.py
analysis_v2_final_真的最終版.py
analysis_v2_final_真的最終版_主管修改.py
```

你根本分不清哪個版本有什麼差異，也不確定改回來之後是不是真的跟原本一樣。

**Git 就是解決這個問題的工具。** 你可以把它想像成一台「時光機」：

- 每次你覺得程式碼到了一個穩定的狀態，就拍一張「快照」（叫做 **commit**）
- 每張快照都有說明（例如「把分母改為通報數」）、時間戳記、誰改的
- 你隨時可以回到任何一張快照，比對兩個版本之間的差異
- 多人同時修改同一份程式碼時，Git 會幫你合併，不會互相覆蓋

**用了 Git 之後，你只需要一個 `analysis.py`，所有歷史版本都安全地保存在背後。**

```{figure} images/git_version_chaos.svg
:name: fig-git-version-chaos
:alt: 沒有 Git 時檔案版本混亂 vs 有 Git 時只需要一個檔案
:width: 100%

沒有 Git 時，你的資料夾會充滿各種版本的檔案，根本分不清哪個是最新的。有了 Git，只需要一個檔案，所有歷史版本都安全地保存在 commit 紀錄中。
```

下圖是 Git 運作的核心概念——四大區域與三個關鍵指令。先有個印象就好，後面會一步一步帶你操作：

```{figure} images/git_three_areas.svg
:name: fig-git-three-areas
:alt: Git 四大區域：工作目錄、暫存區、本地儲存庫、遠端 GitHub
:width: 100%

Git 的四大區域：你在**工作目錄**修改檔案，用 `git add` 放進**暫存區**，用 `git commit` 拍成**快照**存入本地儲存庫，最後用 `git push` 上傳到 GitHub。
```

### 流行病學家最常用的 Git 情境

你不需要學會 Git 的全部功能。以下是流病工作中最常遇到的情境，以及對應的指令：

#### 情境 1：第一次設定（只需要做一次）

剛裝好 Git 之後，先告訴它你是誰。這樣未來每次存檔（commit）都會自動記錄作者：

```bash
git config --global user.name "王小明"
git config --global user.email "xiaoming@health.gov.tw"
```

#### 情境 2：每天的工作流程——改完程式碼，存一個版本

這是你最常做的事。假設你今天修改了流行曲線的腳本：

```bash
# 1) 先看一下目前有哪些檔案被修改了
git status

# 2) 把改好的檔案加入「準備存檔」的區域（staging area）
git add notebooks/02_visualization_epi_charts.ipynb

# 3) 拍一張快照，附上一句說明
git commit -m "feat: 流行曲線加入 7 日移動平均線"
```

```{figure} images/git_daily_workflow.svg
:name: fig-git-daily-workflow
:alt: 每天的 Git 工作流程：修改 → git status → git add → git commit
:width: 100%

每天的工作流程就是這四步：修改程式碼、檢查狀態、加入暫存、拍快照存檔。每完成一個小步驟就重複一次。
```

**`git commit -m "..."` 裡面的訊息很重要**——它是未來的你（或你的同事）回頭查的時候唯一的線索。好的訊息長這樣：

| 好的 commit 訊息 | 不好的 commit 訊息 |
|---|---|
| `fix: 修正 CFR 分母為確診數而非通報數` | `更新` |
| `feat: 新增地區別侵襲率比較長條圖` | `改了一些東西` |
| `docs: 補充第 3 章信賴區間的解讀說明` | `final` |

#### 情境 3：看看之前改了什麼

下週主管問你：「上次那個 CFR 的公式你改了什麼？」

```bash
# 看最近 5 筆 commit 的摘要
git log --oneline -5
```

你會看到類似這樣的清單：

```
a1b2c3d fix: 修正 CFR 分母為確診數而非通報數
e4f5g6h feat: 流行曲線加入 7 日移動平均線
i7j8k9l docs: 補充第 2 章資料清理步驟說明
```

想看某一筆 commit 具體改了哪幾行：

```bash
git show a1b2c3d
```

#### 情境 4：把程式碼同步到 GitHub（雲端備份 + 團隊共享）

GitHub 就像 Git 的「雲端硬碟」。把程式碼推上去，電腦壞了也不怕，同事也能看到最新版：

```bash
# 把本機的 commit 推到 GitHub
git push
```

反過來，如果同事更新了程式碼，你要把最新版拉下來：

```bash
# 從 GitHub 拉最新版到本機
git pull
```

#### 情境 5：想嘗試新方法，但不確定會不會搞砸

假設你想試試看用不同的統計方法算 R0（基本再生數），但不想弄壞目前能跑的版本。這時候可以開一條「分支（branch）」：

```bash
# 建立一條新分支，叫做 try-r0-method
git checkout -b try-r0-method

# 在這條分支上隨便改、隨便試
# ... 寫程式碼 ...
git add .
git commit -m "feat: 嘗試用 EpiEstim 方法估計 R0"

# 如果試成功了，合併回主分支
git checkout main
git merge try-r0-method

# 如果試失敗了，直接切回去，什麼都沒影響
git checkout main
```

```{figure} images/git_branching.svg
:name: fig-git-branching
:alt: Git 分支概念：從 main 岔出分支實驗，成功則合併，失敗則捨棄
:width: 100%

分支就像平行宇宙——從 main 岔出一條線去實驗，成功了合併（merge）回來，失敗了直接切回 main，完全不影響原本的程式碼。
```

分支就像平行宇宙——在另一條線上實驗，成功了再合併回來，失敗了就丟掉，不會影響原本的程式碼。

### Git 指令速查表

以下是日常工作會用到的指令，可以收藏起來隨時查：

| 我想要… | 指令 | 白話說明 |
|---------|------|---------|
| 看現在什麼檔案被改了 | `git status` | 看看有哪些變動還沒存檔 |
| 把檔案加入準備存檔 | `git add 檔案名稱` | 告訴 Git「這些修改我要存」 |
| 把所有改過的檔案一起加入 | `git add .` | 全部加入（注意不要加到機密檔案） |
| 存檔（拍快照） | `git commit -m "說明"` | 建立一個版本紀錄 |
| 看歷史紀錄 | `git log --oneline -10` | 看最近 10 筆版本摘要 |
| 看某個檔案的修改歷程 | `git log --oneline 檔案名稱` | 看這個檔案被改過幾次 |
| 比對目前和上次的差異 | `git diff` | 看我改了哪幾行 |
| 上傳到 GitHub | `git push` | 同步到雲端 |
| 從 GitHub 下載最新版 | `git pull` | 把同事的更新拉下來 |
| 開一條新分支去實驗 | `git checkout -b 分支名稱` | 開平行宇宙 |
| 切回主分支 | `git checkout main` | 回到主線 |
| 回到上一個版本（只看，不改） | `git log --oneline` → `git show commit代碼` | 查看過去的快照 |

### 什麼時候該 commit？

一個簡單的原則：**每完成一個「有意義的小步驟」就 commit 一次。** 例如：

- 清理完 line list 的缺失值 → commit
- 畫好一張流行曲線 → commit
- 修正侵襲率的計算公式 → commit

不要等到「整個分析做完」才 commit。太大的 commit 很難回頭找問題；頻繁的小 commit 讓你隨時能回到任何一步。

### 實戰範例：用 Git 管理 Excel 疫調檔案

你可能會問：「我們疫調都用 Excel，Git 也能管 Excel 嗎？」

**答案是可以的。** Git 可以追蹤任何檔案，包括 `.xlsx`。只是 Excel 是**二進位檔案（binary file）**，Git 沒辦法像純文字檔一樣「逐行比對差異」，但它仍然會幫你保存每一個版本的完整快照，讓你隨時能回到之前的狀態。

以下是一個完整的團隊協作範例。假設你在衛生局負責一份登革熱疫調的 Excel 檔案，團隊有你和另一位同事小李。

#### 第一步：建立 GitHub 儲存庫，把 Excel 放進去

先在 GitHub 上建立一個新的儲存庫（repository），然後在你的電腦上：

```bash
# 建立專案資料夾
mkdir dengue-investigation-2025
cd dengue-investigation-2025
git init

# 把你的 Excel 檔案放進來
# （假設你把 line_list.xlsx 複製到這個資料夾了）

# 第一次 commit
git add line_list.xlsx
git commit -m "feat: 新增登革熱疫調 line list 初始版本"

# 連結到 GitHub 上的儲存庫，然後推上去
git remote add origin https://github.com/your-team/dengue-investigation-2025.git
git push -u origin main
```

現在你的 Excel 檔案已經在 GitHub 上了，有雲端備份，團隊成員都能存取。

#### 第二步：你修改了一筆資料、新增了一張圖表

隔天你收到新的通報，需要更新資料。你打開 `line_list.xlsx`：
- 修正了第 23 筆病例的發病日期（原本打錯了）
- 新增了一個「各區病例統計圖」的工作表（sheet）

改完存檔後，回到終端機：

```bash
# 看看 Git 偵測到什麼變動
git status
# 你會看到：modified: line_list.xlsx

# 加入暫存區
git add line_list.xlsx

# 存檔，寫清楚你改了什麼
git commit -m "fix: 修正第 23 筆病例發病日期；新增各區病例統計圖表"
```

#### 第三步：推到 GitHub（`git push`）

```bash
git push
```

就這樣一行指令，你本機的最新版就同步到 GitHub 了。

**推到哪裡？** 推到你在第一步設定的那個 GitHub 儲存庫。你可以用 `git remote -v` 查看目前連結的遠端位置。

#### 第四步：為什麼要用 Pull Request？不能直接 push 嗎？

如果是你一個人的小專案，直接 push 到 `main` 完全沒問題。

但在團隊協作時，更好的做法是用 **Pull Request（簡稱 PR）**。流程是這樣的：

```bash
# 先開一條分支，在分支上修改
git checkout -b update-case-23

# 修改 Excel、commit
git add line_list.xlsx
git commit -m "fix: 修正第 23 筆病例發病日期"

# 把分支推到 GitHub
git push -u origin update-case-23
```

然後到 GitHub 網頁上點「**Create Pull Request**」。

**PR 的價值在於：**

- **留下審查紀錄**：同事可以在 PR 上留言「確認過原始通報單，日期的確是 6/15 不是 6/5」
- **防止錯誤進入主檔案**：在 merge（合併）之前，有人先看過一遍
- **方便追溯**：三個月後如果有人問「這筆資料為什麼改了」，PR 裡有完整的討論記錄

**誰可以 merge？** 這取決於儲存庫的權限設定。通常的做法是：

| 角色 | 權限 |
|------|------|
| 專案負責人 / 組長 | 可以 merge PR、管理儲存庫設定 |
| 團隊成員 | 可以開 PR、審查（review）、留言，但需要負責人批准才能 merge |
| 外部協作者 | 可以 fork 後開 PR，但不能直接 merge |

在衛生局的場景中，可能是**疫調組長**負責 merge，確保每次資料修改都經過審核。

```{figure} images/git_pull_request_flow.svg
:name: fig-git-pr-flow
:alt: Pull Request 流程：開分支 → 修改 → 推上 GitHub → 開 PR → 審查 → Merge
:width: 100%

Pull Request 流程：從 main 開一條分支修改，推到 GitHub 後開 PR，團隊成員審查確認後，由負責人合併回 main。這樣每一筆修改都有審查紀錄。
```

#### 第五步：同事小李也要編輯同一個 Excel 檔

小李也需要新增幾筆病例資料。正確的做法是：

```bash
# 小李先把最新版抓下來
git clone https://github.com/your-team/dengue-investigation-2025.git
cd dengue-investigation-2025

# 開一條自己的分支
git checkout -b add-new-cases-lili

# 打開 Excel 修改、存檔
# ...修改完畢...

git add line_list.xlsx
git commit -m "feat: 新增 6/16 通報的 8 筆新病例"
git push -u origin add-new-cases-lili
```

然後小李到 GitHub 上開一個 PR，等負責人審查後 merge。

#### 第六步：小李改完了，你要怎麼同步？

小李的 PR 被 merge 之後，你本機的檔案還是舊的。你需要把最新版拉下來：

```bash
# 先切回主分支
git checkout main

# 從 GitHub 拉最新版
git pull
```

現在你的 `line_list.xlsx` 就包含小李新增的那 8 筆病例了。

#### 重要提醒：Excel 的合併限制

有一點必須注意：**如果你和小李同時修改同一個 Excel 檔案的不同部分，Git 無法自動合併。** 因為 Excel 是二進位檔案，Git 看到的是「整個檔案變了」，不知道誰改了哪一格。

這時候 Git 會提示「**merge conflict（合併衝突）**」，你需要手動決定要保留誰的版本。

**避免衝突的實務做法：**

| 方法 | 說明 |
|------|------|
| **約定時段** | 「上午我編輯，下午你編輯」，避免同時修改 |
| **分工作表** | 你負責 Sheet1（病例清單），小李負責 Sheet2（統計彙整） |
| **改用 CSV** | 把資料存成 `.csv`（純文字），Git 就能逐行比對、自動合併 |
| **先 pull 再改** | 每次開始修改前，先 `git pull` 確保手上是最新版 |

```{tip}
如果你的團隊經常需要多人同時編輯同一份資料，考慮把 Excel 拆成 CSV（資料）加上 notebook（分析和圖表）。CSV 是純文字檔案，Git 可以逐行比對差異，多人同時修改不同列時能自動合併，比 Excel 友善很多。這也是本教材推薦的工作流程。
```

#### 完整流程圖

把上面的步驟串起來，就是一個流行病學團隊用 Git 協作的完整流程：

```
你修改 Excel
    ↓
git add → git commit（存檔到本機）
    ↓
git checkout -b 分支名 → git push（推到 GitHub）
    ↓
在 GitHub 上開 Pull Request
    ↓
同事審查（review）、留言確認
    ↓
組長 merge 到 main
    ↓
其他人 git pull（同步最新版到本機）
```

> **給完全不想學 Git 的人**：如果你現在只想專心學流病和 Python，可以先跳過這一段。Git 不是本教材的必要條件——所有章節都可以在沒有 Git 的情況下完成。等你有一天遇到「我想找回上週的程式碼」或「我想跟同事共用分析腳本」的時候，再回來看這段就好。

---

## 10 分鐘動手做：從安裝到第一張流行曲線

以下是一個完整的動手練習。跟著做，10 分鐘內你就能畫出第一張流行曲線——一個你在教科書上看過、在真實疫調中一定會用到的經典圖表。

### Step 1：確認 `uv` 已安裝

```bash
uv --version
```

看到版本號就可以往下走。（不需要事先安裝 Python，`uv sync` 會自動幫你處理。）

### Step 2：下載教材原始碼到你的電腦

這份教材的所有程式碼、資料檔、notebook 都放在一個 **GitHub 儲存庫（repository）** 裡。你可以把它想像成「一個雲端資料夾，裡面裝著整套教材的所有檔案」。

我們需要把這個資料夾**下載到你的電腦上**，才能在本機執行程式碼。下載的方式有兩種，選一種你覺得順的就好：

#### 方式 A：用 `git clone`（推薦）

`git clone` 是程式開發者最常用的「下載專案」指令。它會把整個資料夾複製到你的電腦，而且保留完整的版本歷史，未來教材有更新時可以輕鬆同步。

打開終端機，輸入：

```bash
git clone https://github.com/ancientsky/python4epi.git
cd python4epi
```

> **看到 `fatal: ...` 錯誤？** 可能是你的電腦還沒安裝 Git：
> - **macOS**：輸入 `xcode-select --install`，按提示安裝
> - **Windows**：到 [https://git-scm.com](https://git-scm.com) 下載安裝，裝完後重開終端機
> - **Linux**：輸入 `sudo apt install -y git`

#### 方式 B：直接下載 ZIP（不需要 Git）

如果你不想安裝 Git，也可以直接下載壓縮檔：

1. 用瀏覽器打開 [https://github.com/ancientsky/python4epi](https://github.com/ancientsky/python4epi)
2. 點綠色的 **「Code」** 按鈕 → 選 **「Download ZIP」**
3. 解壓縮到你喜歡的位置（例如桌面或文件夾）
4. 打開終端機，用 `cd` 切換到解壓縮後的資料夾：

```bash
# 範例：如果你解壓在桌面
cd ~/Desktop/python4epi-main
```

> **方式 A 和 B 的差異**：`git clone` 之後，未來教材更新時只要在資料夾裡執行 `git pull` 就能拿到最新版。ZIP 下載則需要重新下載。兩種方式都不影響後續的學習。

### Step 3：安裝所有套件

不管用哪種方式下載，進入教材資料夾後，執行：

```bash
uv sync
```

- `uv sync`：讀取教材的套件清單，自動下載正確版本的 Python、建立虛擬環境、安裝所有需要的 Python 套件（pandas、matplotlib 等）。一行搞定。

第一次執行 `uv sync` 通常需要 1～2 分鐘（要下載不少套件），之後再執行就會很快。

### Step 4：開啟 Jupyter Lab

```bash
uv run jupyter lab
```

你的瀏覽器會自動打開一個類似檔案總管的畫面，這就是 **Jupyter Lab**——我們寫程式、看結果的工作環境。

### Step 5：開啟第一份 notebook

在左邊的檔案列表中，點進 `notebooks/` → 打開 `02_visualization_epi_charts.ipynb`。

你會看到一格一格的「cell」，有些是文字說明，有些是程式碼。

### Step 6：執行所有程式碼

兩種方式：

- **一次全部執行**：上方選單 → `Run` → `Run All Cells`
- **一格一格執行**：點選一個 cell，按 `Shift + Enter`

### Step 7：看到你的第一張流行曲線

往下捲，你會看到一張長條圖：

- **標題**：`Epidemic Curve (By Onset Date)`
- **X 軸**：發病日期（onset date）
- **Y 軸**：每天的病例數（cases）

這就是流行病學最核心的圖表之一：**流行曲線（epidemic curve）**。它告訴你疫情是在上升、到達高峰、還是正在趨緩。

**恭喜！你已經完成了第一個流病資料視覺化任務。**

---

## 常見問題（新手版）

| 問題 | 解法 |
|------|------|
| `git clone` 顯示 `fatal` 錯誤 | 你的電腦可能還沒安裝 Git，請參考 Step 2 的安裝說明，或改用 ZIP 下載 |
| `command not found: uv` | 關掉終端機再重新打開，或確認安裝路徑已加入 `PATH` |
| `python --version` 不是 3.13 | 沒關係，`uv sync` 會自動下載正確版本的 Python |
| `uv sync` 失敗 | 檢查網路連線，然後再執行一次。第一次需要下載較多套件 |
| Jupyter Lab 打開是空白 | 試試在瀏覽器手動輸入終端機顯示的 `http://localhost:8888/...` 網址 |
| notebook 跑出錯誤 | 確認已執行 `uv sync`，然後從第一個 cell 重新開始執行 |

---

## 這份教材的學習路線圖

:::{admonition} 教學影片：課程地圖與學習策略
:class: tip, dropdown

```{raw} html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin-bottom: 1em;">
  <iframe src="https://www.youtube.com/embed/H3fMhNhj3u4" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allowfullscreen></iframe>
</div>
```

影片內容：五幕劇結構 → 必修路線 Ch00-04 → 選修路線 Ch05-14 → 不同角色學習路線 → 盲點：從哪開始、可否跳章、Colab vs 本機
:::

你不需要一口氣學完所有章節。本教材以**松柏護理之家退伍軍人症群聚事件**為貫穿全書的主軸，每一章帶你更深入一層分析，就像真實疫調一樣逐步揭開真相。

```
【第一幕：接獲通報】
  00 導讀（你現在在這裡）── 工具安裝、Hello World
  01 Python 基礎 ── 侵襲率、CFR、最小語法
  02 資料處理與視覺化 ── 讀入 280 筆 line list、畫流行曲線

【第二幕：從描述到推論】
  03 暴露與疾病的關聯 ── 2×2 表、RR、OR、卡方檢定
  04 群聚調查工作流 ── 產出第一份 SitRep 給長官

【第三幕：深入分析】
  05 分層分析與干擾因子 ── 臥床老人不淋浴也不生病，是保護還是干擾？
  06 邏輯斯迴歸 ── 同時調整年齡、共病、暴露，算 adjusted OR
  07 時間序列與預測 ── 下週還會有多少新個案？
  08 空間流病 ── 哪個樓層翼區最危險？畫 spot map

【第四幕：進階建模】
  09 存活分析 ── 發病到死亡的時間，哪些因子影響存活？
  10 機器學習 ── 用 32 欄特徵預測感染與重症
  11 深度學習 ── PyTorch 版本的預測模型
  12 因果推論 ── 淋浴暴露的因果效應，DAG 怎麼畫？

【第五幕：收尾與實戰】
  13 可重現研究 ── 讓同事能一鍵重現你的分析
  14 實戰案例 ── 從接到通報到結案報告，完整走一遍
```

**前 4 章是基礎**，建議按順序學。第 5 章之後可以跳著看，挑你工作或研究需要的主題。

```{figure} images/learning_roadmap.svg
:name: fig-learning-roadmap
:alt: 學習路線圖：Ch 00-04 基礎必修，Ch 05-14 進階選修
:width: 100%

藍色區塊是基礎必修（Ch 00–04），建議按順序完成。紫色區塊是進階選修（Ch 05–14），完成基礎後可依需求任選。
```

---

## 下一步

準備好了嗎？執行以下指令，然後翻到第 01 章開始你的流病 × Python 之旅：

```bash
uv sync
uv run jupyter lab
```
