# 15 附錄

## A. 流行病學術語字典（中英對照）

### 一般流行病學

| 英文 | 台灣譯名 | 說明 |
|------|---------|------|
| Attack rate (AR) | 侵襲率 | 特定期間內新發病例數 / 暴露人口 |
| Case fatality rate (CFR) | 致死率 | 死亡數 / 感染者數 |
| Risk ratio (RR) | 風險比 | 暴露組侵襲率 / 非暴露組侵襲率 |
| Odds ratio (OR) | 勝算比 | 暴露組感染勝算 / 非暴露組感染勝算 |
| Confidence interval (CI) | 信賴區間 | 參數估計的不確定性範圍 |
| Incidence rate | 發生率 | 單位人時的新發病例數 |
| Prevalence | 盛行率 | 特定時間點的現有病例比例 |
| Epidemic curve | 流行曲線 | 依發病日繪製的病例時間分布圖 |
| Outbreak / cluster | 群聚 | 特定時間地點的異常病例聚集 |
| Surveillance | 監測 | 系統性收集與分析健康資料 |
| Case notification | 通報 | 向衛生主管機關報告病例 |
| Epidemiological investigation | 疫調 / 流行病學調查 | 針對群聚事件的系統性調查 |
| Basic reproduction number (R₀) | 基本再生數 | 完全易感人群中一個病例平均傳染人數 |
| Sensitivity | 敏感度 | 真正陽性率（檢驗指標） |
| Specificity | 特異度 | 真正陰性率（檢驗指標） |
| Exposure | 暴露 | 接觸危險因子 |
| Confounding | 交絡 | 第三變項同時影響暴露與結果 |
| Stratified analysis | 分層分析 | 按潛在交絡因子分組後分別分析 |
| Attributable risk (AR) | 歸因風險 | 暴露組風險 − 非暴露組風險 |
| Population attributable risk (PAR) | 族群歸因風險 | 族群中可歸因於暴露的風險比例 |

### 退伍軍人症相關

| 英文 | 中文 | 說明 |
|------|------|------|
| Legionnaires' disease | 退伍軍人症 | 退伍軍人桿菌引起的嚴重肺炎 |
| *Legionella pneumophila* | 退伍軍人桿菌 / 嗜肺性退伍軍人桿菌 | 病原體 |
| Pontiac fever | 乓乒克熱 | 退伍軍人桿菌引起的較輕微自限性疾病 |
| Cooling tower | 冷卻水塔 | 常見的退伍軍人桿菌滋生處 |
| Biofilm | 生物膜 | 微生物附著在管壁形成的薄膜 |
| Water system disinfection | 水系統消毒 | 加熱（>70°C）或加氯消毒 |
| Urinary antigen test | 尿液抗原檢測 | 退伍軍人症快速診斷工具 |

### 存活分析

| 英文 | 中文 | 說明 |
|------|------|------|
| Kaplan-Meier estimator | Kaplan-Meier 估計式 | 非參數存活函數估計法 |
| Log-rank test | Log-rank 檢定 | 比較兩組存活曲線的統計檢定 |
| Cox proportional hazards | Cox 等比例風險模型 | 半參數存活迴歸模型 |
| Hazard ratio (HR) | 風險比 / 危險比 | Cox 模型中暴露的效應量 |
| Censoring | 設限 / 截斷 | 觀察結束時事件尚未發生 |
| Time-to-event | 事件時間 | 從起始到事件發生的時間 |

---

## B. 松柏護理之家資料集欄位對照表

檔案：`data/synthetic/legionella_outbreak.csv`（280 列 × 32 欄）

### 人口學與住房

| 欄位 | 型態 | 值域 | 說明 |
|------|------|------|------|
| `case_id` | str | R001–R280 | 住民編號 |
| `age` | int | 60–98 | 年齡 |
| `sex` | str | M / F | 性別 |
| `floor` | int | 1 / 2 / 3 | 樓層 |
| `wing` | str | A / B | 翼區 |
| `room` | str | 1A-01 等 | 房號 |
| `bed` | int | 1 / 2 | 床號 |
| `facility_admission_date` | date | — | 入住日期 |

### 共病與健康狀態

| 欄位 | 型態 | 值域 | 說明 |
|------|------|------|------|
| `comorbidity_chf` | int | 0 / 1 | 心衰竭 |
| `comorbidity_dm` | int | 0 / 1 | 糖尿病 |
| `comorbidity_cancer` | int | 0 / 1 | 癌症 |
| `comorbidity_copd` | int | 0 / 1 | 慢性阻塞性肺病 |
| `immunosuppressed` | int | 0 / 1 | 免疫低下 |
| `smoking_history` | str | never / former / current | 吸菸史 |
| `functional_status` | str | independent / assisted / bedridden | 日常活動功能 |

### 暴露因子

| 欄位 | 型態 | 值域 | 說明 |
|------|------|------|------|
| `shower_use` | int | 0 / 1 | 是否使用淋浴 |
| `hydrotherapy_use` | int | 0 / 1 | 是否使用水療池 |

### 臨床與結果

| 欄位 | 型態 | 值域 | 說明 |
|------|------|------|------|
| `clinical_severity` | str | not_ill / asymptomatic / mild / moderate / severe | 臨床嚴重度 |
| `symptom_onset_date` | date | — | 發病日期（未感染者為空） |
| `fever` | int | 0 / 1 | 發燒 |
| `cough` | int | 0 / 1 | 咳嗽 |
| `dyspnea` | int | 0 / 1 | 呼吸困難 |
| `confusion` | int | 0 / 1 | 意識混亂 |
| `diarrhea` | int | 0 / 1 | 腹瀉 |
| `lab_confirmed` | int | 0 / 1 | 實驗室確認 |
| `case_classification` | str | not_a_case / probable / confirmed | 個案分類 |
| `hospitalized` | int | 0 / 1 | 是否住院 |
| `hospitalization_date` | date | — | 住院日期 |
| `icu_admission` | int | 0 / 1 | 是否入 ICU |
| `outcome` | str | survived / dead | 結果 |
| `death_date` | date | — | 死亡日期（存活者為空） |
| `notification_date` | date | — | 通報日期 |

---

## C. 套件速查

### 核心套件

| 套件 | 用途 | 章節 |
|------|------|------|
| `pandas` | 資料處理 | 全書 |
| `numpy` | 數值計算 | 全書 |
| `matplotlib` | 基礎繪圖 | Ch02+ |
| `seaborn` | 統計圖表 | Ch03+ |
| `scipy.stats` | 卡方檢定、統計檢定 | Ch03, Ch05 |
| `statsmodels` | 邏輯斯迴歸、OLS | Ch06, Ch12 |
| `plotly` | 互動式圖表、choropleth | Ch08 |

### 進階套件

| 套件 | 用途 | 章節 |
|------|------|------|
| `lifelines` | Kaplan-Meier、Cox PH 存活分析 | Ch09 |
| `scikit-learn` | 機器學習 Pipeline、RF、交叉驗證 | Ch10 |
| `torch` | PyTorch 深度學習 | Ch11 |

### 常用指令

```bash
# 環境管理
uv sync                         # 安裝所有相依套件
uv run pytest                   # 執行測試
uv run jupyter lab              # 啟動 Jupyter Lab

# 書籍建置
uv run jupyter-book build book/ # 建置 Jupyter Book

# 版本控制
git status                      # 查看變更
git add <file>                  # 加入暫存
git commit -m "message"         # 提交
```

---

## D. 常見錯誤排查

| 問題 | 可能原因 | 解法 |
|------|---------|------|
| `ModuleNotFoundError` | 套件未安裝 | `uv sync` |
| `FileNotFoundError: legionella_outbreak.csv` | 工作目錄不對 | 確認在專案根目錄執行 |
| `KeyError: 'column_name'` | 欄位名稱打錯 | `df.columns` 查看正確名稱 |
| Notebook kernel 重啟後變數消失 | Kernel 狀態重置 | 從頭重新執行所有 cell |
| `SettingWithCopyWarning` | 在 slice 上賦值 | 使用 `.copy()` 或 `.loc` |
| 日期欄位無法計算 | 未轉換為 datetime | `pd.to_datetime(df["col"])` |
| 中文字型顯示為方框 | matplotlib 缺中文字型 | 見下方 [E. 中文圖表顯示排錯](#e-中文圖表顯示排錯matplotlib--plotly) |
| Plotly 圖表在 Jupyter Book 中空白 | 渲染器設定不對 | 見下方 [E. 中文圖表顯示排錯](#e-中文圖表顯示排錯matplotlib--plotly) |

---

## E. 中文圖表顯示排錯（matplotlib & Plotly）

在使用繁體中文標籤時，matplotlib 和 Plotly 各有不同的陷阱。這一節記錄本教材在 CI/CD 及本機環境實際踩過的坑，以及解法。

### E-1. Matplotlib：中文顯示為方框 □□□

#### 症狀

圖表的中文標題、軸標籤全部顯示為空白方框，並伴隨大量 UserWarning：

```
UserWarning: Glyph 30332 (\N{CJK UNIFIED IDEOGRAPH-767C}) missing from font(s) DejaVu Sans.
```

這表示 matplotlib 找不到任何能顯示 CJK 字元的字型，退回到預設的 DejaVu Sans（不含中文字符）。

#### 根本原因：`.ttc` 字型集合的 face 0 陷阱

這是一個**非常容易被忽略的陷阱**。在 Linux CI 環境（如 GitHub Actions）安裝 `fonts-noto-cjk` 後，系統會取得 `NotoSansCJK-Regular.ttc`——這是一個 **TrueType Collection**（`.ttc`），單一檔案裡面包含多個字型變體：

| Face 索引 | 字型名稱 | 語言 |
|-----------|---------|------|
| 0 | Noto Sans CJK JP | 日文（預設） |
| 1 | Noto Sans CJK KR | 韓文 |
| 2 | Noto Sans CJK SC | 簡體中文 |
| 3 | Noto Sans CJK TC | 繁體中文 |
| 4 | Noto Sans CJK HK | 香港繁體 |

**問題在於：** matplotlib 的 `fontManager.addfont()` 在處理 `.ttc` 檔案時，**只會註冊 face 0**（即日文變體 "Noto Sans CJK JP"）。如果你的 `font.sans-serif` 候選清單只寫了 `"Noto Sans CJK TC"`，matplotlib 永遠找不到它——因為 TC 根本沒被註冊。

```
你寫的候選清單             matplotlib 認識的字型
─────────────────         ──────────────────
"Noto Sans CJK TC" ──✗    "Noto Sans CJK JP" ← 只有 face 0 被註冊
"Noto Sans TC"     ──✗
"WenQuanYi Zen Hei"──✗    （CI 沒裝這個套件）
"SimHei"           ──✗
                   ↓
              全部 miss → 退回 DejaVu Sans → □□□
```

#### 解法

**方法 1（最簡單）：把所有 Noto Sans CJK 變體都列入候選**

不管 face 0 是哪個語言，只要把 JP、KR、SC、TC、HK 全部列進去，一定能中一個：

```python
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC",    # 繁體中文（理想選擇）
    "Noto Sans CJK SC",    # 簡體中文（CJK 字符通用）
    "Noto Sans CJK JP",    # 日文（face 0，一定被註冊）
    "Noto Sans TC",
    "Microsoft JhengHei",  # Windows 微軟正黑體
    "WenQuanYi Zen Hei",   # Linux 文泉驛
    "SimHei",
    "Arial Unicode MS",    # macOS
    "Heiti TC",            # macOS
    "DejaVu Sans",         # 最終退路（無中文）
]
plt.rcParams["axes.unicode_minus"] = False
```

```{note}
所有 Noto Sans CJK 變體都涵蓋完整的 CJK Unified Ideographs 字集，差別只在少數字符的字形偏好（例如「直」在日文字形和繁中字形略有不同）。用於圖表標籤完全夠用。
```

**方法 2（更穩健）：動態偵測已註冊的字型名稱**

在 `addfont()` 之後，掃描 `fontManager.ttflist` 找出實際註冊了哪些 CJK 字型，並優先使用：

```python
import pathlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1) 掃描並註冊系統 CJK 字型
for font_dir in map(pathlib.Path, ["/usr/share/fonts", "/usr/local/share/fonts"]):
    if font_dir.exists():
        for fp in sorted(font_dir.rglob("*")):
            if fp.suffix.lower() in {".ttf", ".ttc", ".otf"} and (
                "CJK" in fp.name or "WenQuanYi" in fp.name or "wqy" in fp.name
            ):
                try:
                    fm.fontManager.addfont(str(fp))
                except Exception:
                    pass

# 2) 動態偵測實際註冊的 CJK 字型名稱
discovered = []
for entry in fm.fontManager.ttflist:
    if any(kw in entry.name.lower() for kw in ("cjk", "wenquanyi", "wqy")):
        if entry.name not in discovered:
            discovered.append(entry.name)

# 3) 已偵測到的字型優先，再接靜態候選清單
preferred = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei", "WenQuanYi Zen Hei",
    "SimHei", "Arial Unicode MS", "Heiti TC",
]
candidates = list(discovered)
for name in preferred:
    if name not in candidates:
        candidates.append(name)

plt.rcParams["font.sans-serif"] = candidates + ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
```

本教材的 `epi_learning.viz.configure_chinese_font()` 即採用方法 2。

**方法 3：CI 安裝字型 + 清除快取**

在 GitHub Actions 等 CI 環境，需要在安裝字型後清除 matplotlib 的字型快取：

```yaml
# .github/workflows/ci.yml
- name: Install CJK fonts
  run: |
    sudo apt-get update
    sudo apt-get install -y fonts-noto-cjk
    rm -rf ~/.cache/matplotlib    # 清除快取，強制重建字型索引
```

```{warning}
即使安裝了 `fonts-noto-cjk` 並清除快取，仍然必須搭配方法 1 或方法 2 才有效——因為 `.ttc` 的 face 0 陷阱依然存在。
```

#### 各平台預設 CJK 字型

| 作業系統 | 安裝方式 | 可用字型名稱 |
|---------|---------|-------------|
| Ubuntu / Debian | `sudo apt install fonts-noto-cjk` | Noto Sans CJK JP（face 0） |
| Ubuntu / Debian | `sudo apt install fonts-wqy-zenhei` | WenQuanYi Zen Hei |
| macOS | 內建 | Heiti TC, Arial Unicode MS |
| Windows | 內建 | Microsoft JhengHei（微軟正黑體） |
| Google Colab | 預裝 | Noto Sans CJK JP |

### E-2. Plotly：Jupyter Book 建置時圖表空白

#### 症狀

Plotly 互動圖在 Jupyter Lab 中正常顯示，但透過 `jupyter-book build` 產生的靜態 HTML 卻只有空白。

#### 根本原因

Jupyter Book 使用無頭方式（headless）執行 notebook，Plotly 的預設渲染器（`plotly_mimetype`）在此環境下無法產出 HTML 輸出。

#### 解法

在 notebook 中（或透過 `_config.yml` 的 `nb_execution_pre_code`）設定：

```python
import plotly.io as pio
pio.renderers.default = "notebook"
```

`"notebook"` 渲染器會將圖表輸出為完整的 HTML + JS，可以嵌入靜態頁面。

```{tip}
本教材已在 `book/_config.yml` 的 `nb_execution_pre_code` 中全域設定 `pio.renderers.default = "notebook"`，所有 notebook 不需再個別設定。但如果你在自己的專案中遇到同樣問題，只要在建置腳本中加上面那兩行即可。
```

### E-3. 快速自檢清單

當你的 Python 圖表出現中文問題時，依序檢查：

| # | 檢查項目 | 指令 / 方法 |
|---|---------|-------------|
| 1 | 系統是否有 CJK 字型？ | `fc-list :lang=zh`（Linux / macOS） |
| 2 | matplotlib 認識哪些 CJK 字型？ | `[f.name for f in fm.fontManager.ttflist if "cjk" in f.name.lower()]` |
| 3 | `font.sans-serif` 候選清單是否包含步驟 2 找到的名稱？ | `plt.rcParams["font.sans-serif"]` |
| 4 | matplotlib 實際用哪個字型渲染？ | `fm.findfont(fm.FontProperties(family=["Noto Sans CJK JP"]))` |
| 5 | Plotly 渲染器是否設為 `"notebook"`？ | `pio.renderers.default` |
