# 00 導讀與工具（新手友善版）

## 你將學到

- 這個網站怎麼學最順
- 如何在 Mac / Windows / Linux 安裝 Python 與 `uv`
- `uv` 的日常基本操作
- Python 是什麼，以及它和 R 的差異

## 先放心：你不用「先很會寫程式」

這份教材是給公衛與流病學習者設計的。你只要先會「複製指令、執行、看結果」，就能開始做分析。程式能力會在章節中自然成長。

## 安裝 Python（建議 3.11）

### macOS

```bash
brew install python@3.11
python3 --version
```

### Windows（PowerShell）

```powershell
winget install Python.Python.3.11
python --version
```

### Linux（Ubuntu/Debian）

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv
python3.11 --version
```

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

## `uv` 基本操作（最常用 5 個）

```bash
uv python pin 3.11      # 指定專案 Python 版本
uv sync                 # 安裝/同步相依套件
uv run jupyter lab      # 開啟 notebook 環境
uv run pytest           # 跑測試
uv run jupyter-book build book/   # 建置教學網站
```

## Python 是什麼？（給流病學習者）

Python 可以把你每天重複的分析流程「寫成可重跑的步驟」，例如：

1. 讀 line list
2. 算 attack rate、CFR
3. 畫流行曲線
4. 自動產出報表

重點不是炫技，而是**快、可重現、可交接**。

## Python 和 R 怎麼選？

- R 優勢：統計套件成熟、流病社群歷史深。
- Python 優勢：資料工程、機器學習、深度學習整合好。
- 在這份教材：我們用 Python 打通「流病統計 → ML → DL」一條龍。

簡單說：
- 如果你原本熟 R，不需要放棄 R；
- 如果你想往 ML/DL 與產品化前進，Python 會更順。

## 常見問題（新手版）

- `command not found: uv`：重開終端機，或確認安裝路徑已加入 `PATH`。
- `python --version` 不是 3.11：先用 `uv python pin 3.11` 固定專案版本。
- 套件裝不起來：先執行 `uv sync`，再重試 notebook。

## 下一步

```bash
uv python pin 3.11
uv sync
uv run jupyter lab
```

打開後，請從 `01` 和 `02` 章開始，先建立最穩的基礎。

## 10 分鐘圖解流程：從安裝到第一張流行曲線

### Step 1: 確認工具

```bash
python --version
uv --version
```

看到版本號就可以往下走。

### Step 2: 固定 Python 版本並安裝環境

```bash
uv python pin 3.11
uv sync
```

這一步會建立專案環境，第一次執行通常會比較久。

### Step 3: 開啟 Jupyter Lab

```bash
uv run jupyter lab
```

瀏覽器打開後，進入 `notebooks/02_visualization_epi_charts.ipynb`。

### Step 4: 依序執行 notebook 的 cells

- 在 Jupyter Lab 上方按 `Run All Cells`。
- 或一格一格按 `Shift + Enter` 執行。

### Step 5: 你會看到第一張經典流行曲線

- 圖名通常是 `Epidemic Curve (By Onset Date)`。
- X 軸是發病日期（onset date）。
- Y 軸是病例數（cases）

這代表你已經成功完成第一個流病資料視覺化任務。
