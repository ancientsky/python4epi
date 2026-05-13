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
| Confounding | 干擾作用 | 第三變項同時影響暴露與結果 |
| Stratified analysis | 分層分析 | 按潛在干擾因子分組後分別分析 |
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
| Hazard ratio (HR) | 風險比（存活分析） | Cox 模型中暴露的效應量；與 RR 同譯，語境為存活分析時使用 |
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
plt.style.use("ggplot")
plt.rcParams["figure.dpi"] = 150
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

---

## F. 傳染病期間概念對照

疫情調查時常常需要決定「隔離多久」「檢疫幾天」「暴露窗口是何時」，這些決策都建立在正確區分以下四個期間概念之上。

```{figure} images/incubation_periods.svg
:name: fig-incubation-periods
:alt: 傳染病期間概念對照：潛伏期、潛藏期、可傳染期、世代間隔的時間軸比較
:width: 100%

四個期間概念的時間軸對照。注意：**潛藏期短於潛伏期**時，代表感染者在出現症狀**之前**就已具有傳染性（無症狀傳播），此時以症狀為基礎的隔離措施就會有漏洞，需要預防性隔離。
```

| 術語 | 英文 | 定義 | 與疫調的關係 |
|------|------|------|------------|
| **潛伏期** | Incubation period | 從暴露到**出現症狀**的時間 | 決定暴露窗口往前推算多遠（traceback 期間） |
| **潛藏期** | Latent period | 從暴露到**開始具傳染性**的時間 | 潛藏期 < 潛伏期 → 存在無症狀傳播風險 |
| **可傳染期** | Infectious period | 感染者可傳播病原的持續時間 | 決定隔離需要多少天（trace-forward 期間） |
| **世代間隔** | Serial / Generation interval | 從指標個案發病到續發個案發病的時間差 | 估算基本再生數 R₀；預測下一波發病高峰 |

> ⚠️ **關鍵區分**：**潛伏期**是臨床概念（何時出現症狀），**潛藏期**是傳播概念（何時開始傳染）。檢疫時長應根據**潛伏期**的最大值設定；而無症狀隔離政策的必要性，則取決於**潛藏期是否短於潛伏期**。

### 退伍軍人症（本教材主要案例）

| 指標 | 數值 |
|------|------|
| 潛伏期 | 2–10 天（通常 5–6 天） |
| 可傳染期 | 極低（幾乎不人傳人）；主要傳播途徑為環境氣溶膠吸入 |
| 世代間隔 | 不適用（散發型，傳染源為水系統而非病人） |
| 檢疫意義 | 因不人傳人，接觸者不需強制檢疫；重點放在移除環境傳染源 |

---

## G. 傳染鏈六要素與介入策略

傳染病從病原體傳播到易感宿主，必須依序通過六個環節。只要阻斷任一環節，即可中斷傳播鏈。

```{figure} images/chain_of_infection.svg
:name: fig-chain-of-infection
:alt: 傳染鏈六要素：病原體→傳染窩→離開途徑→傳染途徑→入侵途徑→易感宿主，以及三大介入策略
:width: 100%

傳染鏈六要素（上排）與三大介入策略（下排）。退伍軍人症的傳染鏈：*Legionella pneumophila* → 水塔/淋浴水系統 → 氣溶膠 → 吸入（媒介物傳播）→ 呼吸道 → 年長/免疫低下住民。
```

### 六要素說明

| # | 要素 | 英文 | 退伍軍人症實例 | 諾羅病毒（對比） |
|---|------|------|--------------|---------------|
| ① | 病原體 | Pathogen | *Legionella pneumophila* | Norovirus |
| ② | 傳染窩 | Reservoir | 溫水管路、冷卻水塔、淋浴蓮蓬頭 | 感染者（人） |
| ③ | 離開途徑 | Portal of exit | 氣溶膠 | 排泄物、嘔吐物 |
| ④ | 傳染途徑 | Mode of transmission | 吸入（媒介物傳播 vehicle-borne） | 糞口途徑、食物/水污染 |
| ⑤ | 入侵途徑 | Portal of entry | 呼吸道 | 消化道 |
| ⑥ | 易感宿主 | Susceptible host | 年長、免疫低下、慢性肺病 | 全年齡（免疫力弱者更嚴重） |

### 三大介入策略

| 策略 | 對應環節 | 常見措施 |
|------|---------|---------|
| **①移除/控制傳染源** | ①② | 感染者隔離、動物撲殺疫苗、環境消毒（水塔加氯、>70°C 熱沖洗） |
| **②阻斷傳染鏈** | ③④⑤ | 洗手、空氣流通、食物安全、停用污染設施、標準防護措施（PPE） |
| **③保護易感宿主** | ⑥ | 疫苗接種、暴露後預防（PEP）、高危族群撤離、健康監測 |

> 💡 **疫調實務**：控制措施不必等調查完成才實施。只要有合理的假說（例如：懷疑水塔），就應立即啟動「移除傳染源」措施，再邊調查邊修正。

---

## H. 常見食媒病原速查表

食品中毒調查時，潛伏期長短是推估「嫌疑食物時間窗口」的關鍵依據。下表依潛伏期由短到長排列。

| 病原體 | 潛伏期 | 主要症狀 | 傳染方式 | 關鍵辨認線索 |
|--------|--------|---------|---------|------------|
| **組織胺**（Histamine / Scombroid） | 1–60 分鐘（通常 10–30 分） | 顏面發紅、全身發熱、蕁麻疹、胃腸症狀 | 食用腐敗鮪魚、鯖魚、鰹魚、鬼頭刀等 | 症狀出現極快；抗組織胺藥有效 |
| **金黃色葡萄球菌毒素**（Staph aureus enterotoxin） | 0.5–8 小時（通常 2–4 小時） | 噁心、嘔吐、腹絞痛、腹瀉（毒素耐熱，加熱食物仍可中毒） | 處理食物者手部傷口污染；常溫放置過久 | 嘔吐為主；發燒少見 |
| **仙人掌桿菌嘔吐型**（*B. cereus* emetic） | 0.5–6 小時 | 噁心、嘔吐（腹瀉少） | 炒飯等米飯製品放置室溫 | 症狀似Staph；通常與炒飯相關 |
| **腸炎弧菌**（*V. parahaemolyticus*） | 2–48 小時（通常 12–18 小時） | 噁心、嘔吐、腹瀉（水樣/血便）、發燒 | 生食或未充分熟煮的海鮮 | 夏季高峰；台灣常見 |
| **仙人掌桿菌腹瀉型**（*B. cereus* diarrheal） | 6–24 小時 | 腹瀉、腹痛（嘔吐少） | 多種食物（肉類、蔬菜）放置不當 | 腹瀉為主；潛伏期比嘔吐型長 |
| **產氣莢膜桿菌**（*C. perfringens*） | 6–24 小時 | 腹瀉、腹痛（嘔吐少、發燒少） | 大量烹煮的肉類再加熱不足 | 常見於辦桌、大型宴席；症狀輕但人數多 |
| **沙門氏菌**（*Salmonella* spp.） | 6–72 小時（通常 12–36 小時） | 嘔吐、腹瀉、發燒、肌肉痠痛 | 蛋、禽肉、乳製品、蔬菜 | 發燒明顯；菌血症風險（免疫低下者） |
| **諾羅病毒**（Norovirus） | 24–48 小時 | 嘔吐（兒童）、腹瀉（成人）、低燒 | 污染的食物、水；人傳人（糞口途徑、飛沫） | 症狀快速緩解（24–72 小時）；高傳播性，小劑量即可感染 |
| **大腸桿菌 O157（EHEC）** | 1–10 天（通常 3–4 天） | 出血性腸炎、嚴重腹痛；溶血性尿毒症候群（HUS） | 半生牛肉、生菜、未消毒果汁 | 血便（不發燒）；小孩有腎衰竭風險 |
| **A型肝炎**（HAV） | 15–50 天（通常 28–30 天） | 發燒、倦怠、黃疸、噁心 | 污染食物/水；生食貝類 | 潛伏期最長；黃疸出現前已可傳染 |
| **肉毒桿菌**（*C. botulinum*） | 通常 12–36 小時（可達數天） | 鬆弛性對稱向下麻痺、複視、吞嚥困難（無發燒） | 家庭自製罐頭、醃漬食品、蜂蜜（嬰兒） | 神經症狀為主（非腸胃症狀）；死亡率高，立即通報 |
| **李斯特菌（侵襲性）**（*L. monocytogenes*） | 3–70 天（通常 2–3 週） | 敗血症、腦膜炎；孕婦：流產或早產 | 即食冷藏食品（熟食肉品、起司） | 潛伏期最長；高危：孕婦、免疫低下、年長 |

> 📌 **疫調應用**：當你的案例平均潛伏期約 12–24 小時，優先懷疑沙門氏菌、腸炎弧菌。若 <2 小時且有嘔吐，優先懷疑 Staph aureus 毒素或組織胺中毒（後者有顏面潮紅）。若神經症狀（麻痺、複視），立即考慮肉毒桿菌並通報。

### 食物中毒問卷設計重點

食物中毒的問卷飲食史回溯期間，應依**潛伏期**決定：

| 懷疑病原 | 飲食史回溯時間 |
|---------|-------------|
| 組織胺、Staph 毒素 | 發病前 1–4 小時 |
| 腸炎弧菌、沙門氏菌 | 發病前 12–72 小時 |
| 諾羅病毒 | 發病前 24–48 小時（並查接觸史） |
| 不確定病原 | **至少 3 天**（約 72 小時）飲食史 |
| A 型肝炎、李斯特菌 | 發病前 2–6 週 |

```{tip}
**造冊（line list）的暴露欄設計**：每道嫌疑食物各一欄（0/1），讓每位受訪者填寫「有無食用」，再用 RR（世代研究）或 OR（病例對照研究）評估每道菜與發病的關聯。詳見 Ch03 的 2×2 表分析。
```
