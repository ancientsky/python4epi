# 07 時間序列與預測：從滾動平均到 ARIMA/SARIMA

## 情境

松柏護理之家退伍軍人症群聚事件進入第二週，長官在疫調會議上丟出兩個問題：

> 「下禮拜還會有多少人發病？醫院還要準備幾張床？」
>
> 「**明天**會不會又是一個高峰日？要不要提前啟動警報？」

第一個問題要**連續數字**的預測（下週的病例數），第二個問題要**是/否的訊號**（明天是不是高峰）。這兩種需求用同一個滾動平均可能不夠——我們要比較**六種模型**，看誰最適合。

這一章的主軸：**從最簡單的 rolling mean 一路走到 ARIMA/SARIMA**，用護理之家資料示範短期預測，用 90 天合成類流感資料示範長期 + 週期預測。

## 你將學到

- 從 line list 建立每日病例時間序列（`asfreq` 補齊日期）
- 用 **rolling mean**（baseline）做短期預測
- 建立 **lagged features**（把「昨天、前天」變成特徵）
- 用 **Poisson regression + lag** 做計數資料預測
- 用 **Negative Binomial regression** 處理過度離散（overdispersion）
- 用 **Logistic regression** 做「高峰日警報」二元預測
- 用 **ARIMA / SARIMA** 在較長序列上捕捉趨勢 + 週期
- 用 **MAE / AIC** 系統性比較六種模型

## 核心概念

| 概念 | 說明 |
|------|------|
| **Time series（時間序列）** | 按時間排列的觀測值，相鄰點通常高度相關 |
| **Autocorrelation（自相關）** | 今天的值和昨天的值有關 → 可用 lag 特徵捕捉 |
| **Lag features** | 把「昨天、前天」的值搬過來當今天的特徵欄 |
| **Stationarity（平穩性）** | 均值與變異不隨時間漂移，是 ARIMA 的前提 |
| **Overdispersion（過度離散）** | variance > mean → Poisson 失準 → 改 Negative Binomial |
| **Seasonality（週期性）** | 7 天、12 個月等固定循環 → 需要 SARIMA |
| **MAE** | Mean Absolute Error，平均預測絕對誤差 |
| **AIC** | Akaike Information Criterion，愈小愈好，懲罰過度配適 |
| **Data leakage** | 用到未來資訊做預測 → 結果不可靠（一定要 `shift(1)`） |

## 方法總覽

```{figure} images/timeseries_method_map.svg
:name: fig-timeseries-method-map
:alt: 六種時間序列預測方法比較 —— rolling mean, Poisson+lag, Negative Binomial, Logistic, ARIMA, SARIMA
:width: 100%

**時間序列預測方法地圖**：六個模型從簡單到複雜排開。資料越少 → 越左邊；需要捕捉週期 → 最右邊。每張卡片告訴你「最少要幾天資料」「能不能給信賴區間」「適合哪種情境」。
```

---

## Step 1: 建立每日發病序列

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

# -- CJK font setup --
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
plt.style.use("ggplot")
plt.rcParams["figure.dpi"] = 150

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["symptom_onset_date"] = pd.to_datetime(df["symptom_onset_date"], errors="coerce")
df["hospitalization_date"] = pd.to_datetime(df["hospitalization_date"], errors="coerce")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

cases = df[df["infected"] == 1]

# 每日發病數，補齊無發病的日期（確保連續）
daily = cases.groupby("symptom_onset_date").size()
daily = daily.asfreq("D", fill_value=0)
daily.name = "cases"
print(f"序列長度：{len(daily)} 天 | 總病例：{daily.sum()}")
```

## Step 2: 流行曲線 + 滾動平均視覺

```python
rolling_7 = daily.rolling(window=7, min_periods=1).mean()
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, width=1.0,
       color="#6A9BCC", edgecolor="white", alpha=0.6, label="每日新增")
ax.plot(rolling_7.index, rolling_7.values, color="#D97757", linewidth=2,
        label="7 日滾動平均")
ax.set_title("松柏護理之家退伍軍人症流行曲線", fontweight="bold")
ax.set_xlabel("發病日期"); ax.set_ylabel("病例數")
ax.legend(); ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.autofmt_xdate(); plt.tight_layout(); plt.show()
```

---

## Part A ── 短期 outbreak 預測（護理之家資料，17 天）

### Step 3: Baseline —— Rolling mean 預測

```python
# 用前 w 天的平均預測「下一天」，shift(1) 避免 data leakage
mae_by_window = {}
for w in [3, 5, 7]:
    pred_w = daily.rolling(window=w).mean().shift(1).dropna()
    actual_w = daily.loc[pred_w.index]
    mae_by_window[w] = mean_absolute_error(actual_w, pred_w)
    print(f"  rolling mean (w={w}):  MAE={mae_by_window[w]:.3f}")

mae_rolling = mae_by_window[3]
print(f"\n→ 最佳：window=3, MAE={mae_rolling:.3f}")
```

Rolling mean 的優點：**簡單、直覺、在第一天就能用**。缺點：它永遠是「看過去幾天的平均」，不會預測轉折、沒有信賴區間、也沒辦法放其他變項（例如樓層、星期幾）。

### Step 4: Lagged features —— 為迴歸模型建立「過去 k 天」特徵

```{figure} images/lag_features_explained.svg
:name: fig-lag-features
:alt: 用 shift(1) 把過去的值搬到今天這一列變成 lag_1 / lag_2 特徵
:width: 100%

**Lag features**：`df["lag_1"] = df["cases"].shift(1)` 把整欄往下推一格，讓「昨天的 cases」出現在「今天那一列」。再配合 `lag_2`、`lag_3`，就能把時間序列**變成一般迴歸能吃的表格**。
```

```python
ts = daily.to_frame("cases").reset_index(names="date")
ts["day_idx"] = range(len(ts))       # 天數編號（趨勢）
ts["lag_1"] = ts["cases"].shift(1)   # 昨天的病例數
ts["lag_2"] = ts["cases"].shift(2)   # 前天的病例數
ts_model = ts.dropna().reset_index(drop=True)  # 掉掉前兩列（NaN）
print(ts_model.head())
print(f"可用列數：{len(ts_model)}")
```

```{note}
為什麼要加 lag？因為感染是傳染的——今天的病例數和昨天高度相關（autocorrelation）。把「昨天的值」當特徵，迴歸模型就能學會：「昨天多、今天多」「昨天激增、今天可能再增」。
```

### Step 5: Poisson regression + lag

計數資料（每日人數是 0, 1, 2, ...）天生適合 **Poisson** 分布。我們用 `statsmodels` 的 GLM 把 lag 特徵 + 趨勢項放進去：

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Poisson GLM：cases ~ 昨天 + 前天 + 天數趨勢
model_pois = smf.glm(
    "cases ~ lag_1 + lag_2 + day_idx",
    data=ts_model,
    family=sm.families.Poisson(),
).fit()

pred_pois = model_pois.predict(ts_model)
mae_pois = mean_absolute_error(ts_model["cases"], pred_pois)
print(f"Poisson + lag:  MAE={mae_pois:.3f},  AIC={model_pois.aic:.2f}")

# 解讀係數：exp(β) = incidence rate ratio (IRR)
coef_table = pd.DataFrame({
    "coef (log scale)": model_pois.params,
    "IRR exp(coef)": np.exp(model_pois.params),
})
print(coef_table.round(3))
```

**白話解讀**：`IRR(lag_1) ≈ 1.15` 表示「昨天每多 1 人發病，今天預期值會多 15%」。

### Step 6: Negative Binomial regression —— 處理過度離散

```{figure} images/poisson_vs_nb_dispersion.svg
:name: fig-poisson-vs-nb
:alt: Poisson 假設 variance = mean；Negative Binomial 允許 variance > mean 的過度離散
:width: 100%

**Poisson 的大前提**：`variance = mean`。但疫調資料常常不乖——一旦發生群聚感染，變異會遠大於平均（**overdispersion**）。此時應改用 **Negative Binomial**，它多一個參數 α 專門吸收「多出來的」變異。
```

```python
# 先檢查 dispersion ratio
disp = ts_model["cases"].var() / ts_model["cases"].mean()
print(f"dispersion = variance / mean = {disp:.2f}")
print("→ >1.5 視為過度離散 → 改用 Negative Binomial")

# Negative Binomial GLM
model_nb = smf.glm(
    "cases ~ lag_1 + lag_2 + day_idx",
    data=ts_model,
    family=sm.families.NegativeBinomial(alpha=1.0),
).fit()

pred_nb = model_nb.predict(ts_model)
mae_nb = mean_absolute_error(ts_model["cases"], pred_nb)
print(f"\nNegative Binomial + lag:  MAE={mae_nb:.3f},  AIC={model_nb.aic:.2f}")
```

### Step 7: Logistic regression —— 「明天會不會是高峰日？」

長官問的第二個問題是**是/否警報**，不是連續數字。做法：把每天的病例數**二值化**（超過某個門檻 → 1，否則 → 0），再用 logistic regression 預測機率。

```python
# 把 75th percentile 當「高峰日」門檻
threshold = ts_model["cases"].quantile(0.75)
ts_model["high_day"] = (ts_model["cases"] > threshold).astype(int)
print(f"高峰日門檻（>75th）= {threshold:.0f} 人")

# 用昨天、前天的病例數預測「明天會不會超過門檻」
model_logit = smf.logit("high_day ~ lag_1 + lag_2", data=ts_model).fit(disp=False)
prob = model_logit.predict(ts_model)
pred_binary = (prob > 0.5).astype(int)
acc = (pred_binary == ts_model["high_day"]).mean()
print(f"\nLogistic (threshold): accuracy = {acc:.3f}")
```

**這個模型不給你「明天會有幾人」，但會告訴你「明天超過警戒線的機率是 72%」**——這才是早期預警系統真正需要的輸出。

---

## Part B ── 長期監測預測（合成 90 天資料）

### Step 8: 為什麼 outbreak 資料不夠？+ 合成示範序列

ARIMA / SARIMA 需要 **≥ 30 天**（SARIMA 更需要**至少 2 個完整週期**）。護理之家資料只有 17 天，硬套會得到不穩的結果。這裡我們**現場合成一條 90 天的「類流感每日通報數」**，包含趨勢、每 7 天的週循環、隨機噪音：

```python
rng = np.random.default_rng(42)
n_days = 90
dates = pd.date_range("2025-10-01", periods=n_days, freq="D")

trend = np.linspace(3, 7, n_days)                   # 每日平均從 3 慢慢升到 7
seasonal = 3 * np.sin(2 * np.pi * np.arange(n_days) / 7)   # 7 天週期
noise = rng.normal(0, 1.2, n_days)                  # 隨機噪音

synth_cases = np.maximum(0, (trend + seasonal + noise).round()).astype(int)
synth = pd.Series(synth_cases, index=dates, name="cases")

fig, ax = plt.subplots(figsize=(10, 3.5))
ax.plot(synth.index, synth.values, color="#6A9BCC", linewidth=1.5)
ax.set_title("合成類流感每日通報數（trend + 7 天週期 + 噪音）", fontweight="bold")
ax.set_xlabel("日期"); ax.set_ylabel("每日通報數")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.autofmt_xdate(); plt.tight_layout(); plt.show()
```

### Step 9: ARIMA —— AutoRegressive Integrated Moving Average

```{figure} images/arima_sarima_decomposition.svg
:name: fig-arima-sarima
:alt: 時間序列可分解為 trend + seasonal + residual；ARIMA(p,d,q) 由三塊組成，SARIMA 多一個季節元件
:width: 100%

**ARIMA 三個字母**：**AR(p)** 看過去 p 天的自己；**I(d)** 做 d 次差分讓序列平穩；**MA(q)** 看過去 q 次的預測誤差。**SARIMA** 額外加一組 (P, D, Q, s) 專門抓週期 s。
```

```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# 先做平穩性檢定（ADF test）
adf_stat, p_value, *_ = adfuller(synth)
print(f"ADF statistic = {adf_stat:.3f}, p-value = {p_value:.3f}")
print(f"→ p < 0.05 表示序列平穩（不需要差分 d=0）；否則 d ≥ 1")

# 切訓練 / 測試集：前 83 天訓練，最後 7 天測試
train, test = synth.iloc[:-7], synth.iloc[-7:]

model_arima = ARIMA(train, order=(1, 1, 1)).fit()
forecast_arima = model_arima.forecast(steps=7)
mae_arima = mean_absolute_error(test.values, forecast_arima.values)
print(f"\nARIMA(1,1,1):  MAE={mae_arima:.3f},  AIC={model_arima.aic:.2f}")
```

### Step 10: SARIMA —— 加入季節性

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# 季節週期 s=7（每週）
model_sarima = SARIMAX(
    train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 7),
).fit(disp=False)

forecast_sarima = model_sarima.forecast(steps=7)
mae_sarima = mean_absolute_error(test.values, forecast_sarima.values)
print(f"SARIMA(1,1,1)(1,1,1,7):  MAE={mae_sarima:.3f},  AIC={model_sarima.aic:.2f}")

# 視覺化：預測 vs 實際
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.plot(train.index[-30:], train.values[-30:], color="#6B6B6B",
        linewidth=1.2, label="訓練（最後 30 天）")
ax.plot(test.index, test.values, color="#1A1A1A", linewidth=2,
        marker="o", markersize=5, label="實際")
ax.plot(test.index, forecast_arima.values, color="#6A9BCC", linewidth=1.8,
        marker="s", markersize=5, linestyle="--", label=f"ARIMA (MAE={mae_arima:.2f})")
ax.plot(test.index, forecast_sarima.values, color="#D97757", linewidth=1.8,
        marker="^", markersize=5, linestyle="--", label=f"SARIMA (MAE={mae_sarima:.2f})")
ax.set_title("ARIMA vs SARIMA 未來 7 天預測", fontweight="bold")
ax.set_xlabel("日期"); ax.set_ylabel("每日通報數")
ax.legend(loc="upper left"); ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.autofmt_xdate(); plt.tight_layout(); plt.show()
```

**關鍵觀察**：SARIMA 的 MAE 明顯小於 ARIMA，因為它抓到了 7 天的週循環。對於**沒有週期性**的資料，多加 SARIMA 反而浪費（參數多、容易過配）。

---

## Step 11: 模型大比拼

```python
comparison = pd.DataFrame([
    {"model": "① Rolling mean (w=3)",      "資料集": "outbreak", "MAE": mae_rolling,
     "最少資料": "5 天",  "捕捉週期": "否",    "信賴區間": "否"},
    {"model": "② Poisson + lag",           "資料集": "outbreak", "MAE": mae_pois,
     "最少資料": "10 天", "捕捉週期": "部分",  "信賴區間": "是"},
    {"model": "③ Negative Binomial + lag", "資料集": "outbreak", "MAE": mae_nb,
     "最少資料": "10 天", "捕捉週期": "部分",  "信賴區間": "是"},
    {"model": "④ Logistic (threshold)",    "資料集": "outbreak", "MAE": f"— (acc={acc:.2f})",
     "最少資料": "10 天", "捕捉週期": "否",    "信賴區間": "是（機率）"},
    {"model": "⑤ ARIMA(1,1,1)",            "資料集": "synth 90d", "MAE": mae_arima,
     "最少資料": "30 天", "捕捉週期": "弱",    "信賴區間": "是"},
    {"model": "⑥ SARIMA(1,1,1)(1,1,1,7)",  "資料集": "synth 90d", "MAE": mae_sarima,
     "最少資料": "60 天", "捕捉週期": "強",    "信賴區間": "是"},
])
print(comparison.to_string(index=False))
```

**結論白話版**：
- **資料只有一兩週**（outbreak 剛爆發）→ Rolling mean 或 Poisson + lag 就夠
- **過度離散明顯**（群聚、突發疫情）→ 改 Negative Binomial
- **需要是/否警報**（要不要啟動應變層級）→ Logistic regression
- **中長期監測**（> 一個月、無明顯週期）→ ARIMA
- **類流感、每週監測**（有明顯週循環）→ SARIMA

## Step 12: 發病 vs 住院曲線（Lag 效應）

```python
hosp_daily = (
    cases[cases["hospitalization_date"].notna()]
    .groupby("hospitalization_date").size()
)
all_dates = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
hosp_aligned = hosp_daily.reindex(all_dates, fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, width=1.0, alpha=0.55,
       color="#6A9BCC", edgecolor="white", label="發病")
ax.bar(hosp_aligned.index, hosp_aligned.values, width=1.0, alpha=0.55,
       color="#D97757", edgecolor="white", label="住院")
ax.set_title("發病 vs 住院曲線（Lag 效應）", fontweight="bold")
ax.set_xlabel("日期"); ax.set_ylabel("人數")
ax.legend(); ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.autofmt_xdate(); plt.tight_layout(); plt.show()

lag_days = (hosp_aligned.idxmax() - daily.idxmax()).days
print(f"發病高峰 → 住院高峰 lag = {lag_days} 天")
```

這個 lag 是**床位規劃的黃金指標**：發病高峰過了幾天後，住院需求才會到頂。

---

## 解讀重點

| 觀察 | 意義 |
|------|------|
| Dispersion ratio > 1.5 | Poisson 失準 → 用 Negative Binomial |
| ADF p-value > 0.05 | 序列不平穩 → ARIMA 的 d 要 ≥ 1 |
| SARIMA MAE < ARIMA | 資料有明顯週期 |
| Logistic 機率 > 0.5 | 預報「可能是高峰日」，建議啟動警報 |
| Rolling mean MAE 接近其他模型 | 資料太短、訊號太弱 → 不用為了炫技上 SARIMA |

## 常見錯誤

1. **Data leakage**：忘記 `shift(1)`，把今天的值拿來預測今天 → MAE 看起來超漂亮，但上線就崩
2. **沒補齊日期**：跳過無發病日，時間序列不連續，rolling / ARIMA 都會失真
3. **只報單一指標**：沒有 baseline 對照的 MAE 沒有意義
4. **忽略 overdispersion**：變異很大還硬用 Poisson → 信賴區間過窄，低估不確定性
5. **過度配適**：資料 17 天還想訓練 SARIMA → 參數比觀測值還多
6. **忽略平穩性**：不做 ADF test 就套 ARIMA → d 值亂猜
7. **ARIMA 階數亂試**：隨便選 (p,d,q) 不看 AIC / ACF / PACF → 結果碰運氣

## 下一步

知道「何時」疫情最嚴重後，接下來問「在哪裡」最嚴重？→ Ch08 空間流病。

## 練習本

- 課堂筆記：{ref}`07_time_series_baseline.ipynb`
- 作業版：[`07_time_series_exercise.ipynb`](exercises/07_time_series_exercise.ipynb)
- 解答版（教師版）：[`07_time_series_solution.ipynb`](solutions/07_time_series_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/07_time_series_solution.ipynb>)
