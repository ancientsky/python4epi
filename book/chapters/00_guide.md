# 00 導讀與工具（新手友善版）

## 你將學到

- 為什麼流行病學需要程式工具（而不只是試算表）
- 為什麼這份教材選 Python，而不是 R 或 Excel
- 為什麼用 `uv` 而不是傳統的 `pip`
- Git 版本控制基礎：流行病學家最常用的情境與指令
- 如何一步一步在你的電腦上安裝好所有工具
- 安裝完後怎麼驗證、怎麼開始學

---

## 先說一個故事：禮拜五下午 4 點的電話

想像你是一位剛進入衛生局的新人。禮拜五下午 4 點，主管打電話來：

> 「某國小疑似食物中毒群聚，目前通報 45 人嘔吐腹瀉。我需要你在 **今天下班前** 給我：攻擊率多少？致死率多少？哪個班級最嚴重？能不能畫一張發病時間的流行曲線？」

你打開手邊的 Excel，45 筆資料勉強處理得完。但下一週，你遇到一場跨縣市的登革熱疫情，line list 有 3,000 筆。再下一個月，你需要回溯三年的監測資料趨勢。這時你會發現——

- Excel 的列數限制開始卡你
- 手動篩選、複製貼上很容易出錯
- 每次主管問「換個條件再算一次」，你就要從頭重做
- 同事接手你的檔案，根本不知道你當初怎麼算的

**程式不是要取代你的流病判斷，而是幫你把「重複、容易出錯、需要交接」的步驟自動化。** 你寫一次程式碼，以後不管資料換成 300 筆還是 30,000 筆，按一個鍵就能重跑、檢查、交給下一個人。

這就是為什麼越來越多流行病學工作者開始學程式。

---

## 為什麼不用 Excel / Google Sheets 就好？

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

如果你 Google「Python 安裝套件」，幾乎所有教學都會教你用 `pip install`。那為什麼我們要用 `uv` 這個比較新的工具？

### 先說 `pip` 的問題

`pip` 是 Python 內建的套件安裝工具，已經存在很多年了。它能用，但在教學場景中有幾個痛點：

- **環境衝突**：你可能聽過「我的電腦上可以跑，但同事的不行」。`pip` 裝的套件版本不一致，是新手最常遇到的挫折。
- **需要手動管理虛擬環境**：`python -m venv`、`source activate`… 光是啟動環境的步驟就能讓新手迷路。
- **速度慢**：裝一堆資料科學套件（pandas、matplotlib、scikit-learn…）可能要等好幾分鐘。

### `uv` 解決了什麼

[`uv`](https://docs.astral.sh/uv/) 是一個用 Rust 語言寫的新一代 Python 套件管理工具，特色是：

- **快非常多**：安裝速度比 `pip` 快 10～100 倍（不誇張）。
- **自動管理虛擬環境**：你不需要手動建立、啟動虛擬環境，`uv sync` 一個指令就搞定。
- **鎖定版本**：`uv.lock` 檔案確保你跟同學、同事用的套件版本一模一樣，不會出現「我的可以跑，你的不行」。
- **一個指令做所有事**：安裝、執行、管理，全部用 `uv` 開頭。

### 實際差異：`pip` vs `uv`

| 任務 | 傳統做法（`pip`） | 本教材做法（`uv`） |
|------|-------------------|-------------------|
| 建立環境 | `python -m venv .venv && source .venv/bin/activate` | `uv sync`（自動建立並啟用） |
| 安裝套件 | `pip install pandas matplotlib` | `uv sync`（讀 `pyproject.toml` 自動安裝） |
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
3. **用流病情境學程式**——不會教你寫計算機或猜數字遊戲，所有範例都是 line list、攻擊率、流行曲線。

你的學習路徑是：

```
複製程式碼 → 執行看結果 → 改幾個數字再跑 → 慢慢理解邏輯
```

程式能力會在章節中自然成長，不需要先去上完一整門「Python 入門」才回來。

---

## 安裝 Python（建議 3.11）

接下來是實際的安裝步驟。請根據你的作業系統，選擇對應的區塊操作。

### macOS

打開「終端機」應用程式（可以用 Spotlight 搜尋 "Terminal"），然後輸入：

```bash
brew install python@3.11
python3 --version
```

> 如果你沒有 `brew`，請先到 [https://brew.sh](https://brew.sh) 安裝 Homebrew。

### Windows（PowerShell）

按 `Win + X`，選擇「Windows PowerShell」或「終端機」，然後輸入：

```powershell
winget install Python.Python.3.11
python --version
```

### Linux（Ubuntu/Debian）

打開終端機，輸入：

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv
python3.11 --version
```

> **驗證成功**：不管哪個系統，你看到類似 `Python 3.11.x` 的版本號就表示安裝成功了。

---

## 安裝 `uv`

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

### Windows（PowerShell）

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
```

> **驗證成功**：看到 `uv 0.x.x`（任何版本號）就可以了。
>
> **常見問題**：如果顯示 `command not found: uv`，請關掉終端機再重新打開一次。安裝程式會把 `uv` 加入你的 PATH，但需要重新啟動終端機才會生效。

---

## `uv` 基本操作（最常用 5 個）

安裝完之後，整個教材只會用到這 5 個指令：

```bash
uv python pin 3.11               # ① 指定專案要用 Python 3.11
uv sync                          # ② 安裝所有需要的套件（第一次會比較久）
uv run jupyter lab                # ③ 開啟 notebook 環境
uv run pytest                    # ④ 跑測試（檢查程式碼是否正確）
uv run jupyter-book build book/   # ⑤ 建置教學網站（進階，可先略過）
```

你不需要背這些指令，用到的時候回來查就好。

---

## Git 是什麼？為什麼流行病學家需要它？

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
| `feat: 新增地區別攻擊率比較長條圖` | `改了一些東西` |
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
- 修正攻擊率的計算公式 → commit

不要等到「整個分析做完」才 commit。太大的 commit 很難回頭找問題；頻繁的小 commit 讓你隨時能回到任何一步。

> **給完全不想學 Git 的人**：如果你現在只想專心學流病和 Python，可以先跳過這一段。Git 不是本教材的必要條件——所有章節都可以在沒有 Git 的情況下完成。等你有一天遇到「我想找回上週的程式碼」或「我想跟同事共用分析腳本」的時候，再回來看這段就好。

---

## 10 分鐘動手做：從安裝到第一張流行曲線

以下是一個完整的動手練習。跟著做，10 分鐘內你就能畫出第一張流行曲線——一個你在教科書上看過、在真實疫調中一定會用到的經典圖表。

### Step 1：確認工具已安裝

```bash
python3 --version
uv --version
```

兩個都看到版本號，就可以往下走。

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
uv python pin 3.11
uv sync
```

- `uv python pin 3.11`：告訴 `uv` 這個專案要用 Python 3.11。
- `uv sync`：讀取教材的套件清單，自動建立虛擬環境並安裝所有需要的 Python 套件（pandas、matplotlib 等）。

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
| `python --version` 不是 3.11 | 沒關係，先執行 `uv python pin 3.11`，`uv` 會自動幫你管理版本 |
| `uv sync` 失敗 | 檢查網路連線，然後再執行一次。第一次需要下載較多套件 |
| Jupyter Lab 打開是空白 | 試試在瀏覽器手動輸入終端機顯示的 `http://localhost:8888/...` 網址 |
| notebook 跑出錯誤 | 確認已執行 `uv sync`，然後從第一個 cell 重新開始執行 |

---

## 這份教材的學習路線圖

你不需要一口氣學完所有章節。以下是建議的路線：

```
00 導讀（你現在在這裡）
 ↓
01 流病核心概念 ── 攻擊率、CFR、Python 最小語法
 ↓
02 資料處理與視覺化 ── pandas、流行曲線、三種畫圖套件
 ↓
03 統計基礎 ── 風險比、信賴區間、卡方檢定
 ↓
04 疫調工作流程 ── 把單一步驟串成完整分析
 ↓
05–11 進階主題 ── 時間序列、空間分析、ML、DL…
```

**前 4 章是基礎**，建議按順序學。第 5 章之後可以跳著看，挑你工作或研究需要的主題。

```{figure} images/learning_roadmap.svg
:name: fig-learning-roadmap
:alt: 學習路線圖：Ch 00-04 基礎必修，Ch 05-11 進階選修
:width: 100%

藍色區塊是基礎必修（Ch 00–04），建議按順序完成。紫色區塊是進階選修（Ch 05–11），完成基礎後可依需求任選。
```

---

## 下一步

準備好了嗎？執行以下指令，然後翻到第 01 章開始你的流病 × Python 之旅：

```bash
uv sync
uv run jupyter lab
```
