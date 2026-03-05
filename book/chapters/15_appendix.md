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
| 中文字型顯示為方框 | matplotlib 缺中文字型 | 在 import 後加 `plt.rcParams["font.sans-serif"] = ["Noto Sans CJK TC", "WenQuanYi Zen Hei", "SimHei"]` |
