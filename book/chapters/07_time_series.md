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

## 🔮 超白話特別篇：用「珍奶店老闆的水晶球」看懂時間序列預測

> ARIMA、SARIMA、自相關、平穩性……一堆名詞是不是看得頭很痛？別怕。這一段先把疫情放一邊，改用一個超接地氣的角色——**一位想預測明天要賣幾杯的珍奶店老闆**——把時間序列預測整套邏輯講到讓國中生也會點頭。看完再回頭看下面那六種模型，你會發現：它們全都在做老闆每天在做的事！

### 老闆的煩惱：明天到底要備多少料？

珍奶店老闆每天早上都在賭一件事：

> 「今天要煮多少珍珠？要排幾個店員？備太多會浪費，備太少會被客人罵翻。」

他多希望有顆**水晶球**，能看到明天大概會賣幾杯。這正是**時間序列預測**在做的事——而且這個煩惱跟疫情指揮官的煩惱**一模一樣**：

> 🛏️ **「明天大概多少人發病？醫院要準備幾張床、排多少醫護？」** 珍奶店的「珍珠和店員」，就是疫情裡的「病床和人力」。**預測，是為了提前準備。**

### 招式一：滾動平均——別被「今天一天」嚇到

老闆看每天的銷量，會發現它**忽高忽低像鋸齒**：週六爆單、週一冷清。如果他只看「昨天賣爆」就狂備料，週一就慘了。怎麼辦？

> ⚖️ **量體重比喻**：你會因為「今天早上重了 0.5 公斤」就崩潰嗎？不會——今天多喝幾杯水就這樣。要看**一整週的平均**才準。每日病例數也一樣：**7 天滾動平均（rolling mean）**像戴上一副「除鋸齒眼鏡」，把週末的忽高忽低抹平，露出底下**真正的走勢**。

### 招式二：自迴歸——明天會長得像最近的自己

老闆最直覺的預測法：「昨天、前天賣很多，今天大概也不會太差。」

> 🌡️ 這叫**自迴歸（autoregression）**——就像天氣有慣性，「昨天冷，今天大概也冷」。生意有慣性，所以**用最近幾天的數字推明天**。本章 Part A 的 Poisson＋lag 模型，做的就是「拿昨天、前天當特徵，預測今天」。

### 招式三：週期性——每逢週六必爆單

老闆還發現一個鐵律：**每個星期六都爆單**，週而復始。

> 📅 **折日曆比喻**：把日曆每 7 天疊成一疊，你會發現「週六」那一格永遠最擠。這種**每 7 天準時重播**的固定戲碼，就是**週期性（seasonality），s=7**。SARIMA 名字裡的 `s=7` 就是在提醒模型：「每隔 7 天，回頭看一次同一個星期幾。」

> 🔑 一句話分清楚：**自迴歸是「短期慣性」（最近幾天的餘溫），週期性是「長期節奏」（每週固定那一天）**——兩個一起用，預測才準。

### 招式四：訓練/測試——不准偷看答案！

老闆想出一條預測公式，怎麼知道它準不準？**不能拿他已經看過的日子來自誇。**

> 📝 **考古題比喻**：拿一張你已經對過答案的考卷考自己，當然一百分——但那不代表你會算**明天**的新題目。正確做法是：**把最後一週的真實銷量先「蓋起來」**，逼自己在看不到答案的情況下預測，最後再掀開對答案。偷看未來 = **作弊（data leakage）**，模型會「考」很高、實際上線卻慘敗。

這就是**訓練集／測試集切分**：用前面的資料想公式（訓練），用藏起來的最後幾天檢驗（測試），並用 **MAE（平均差幾杯）**打分數，越小越準。

```{figure} images/bubbletea_forecast.svg
:name: fig-bubbletea-forecast
:alt: 珍奶店每日銷量時間序列：週末爆單的鋸齒狀長條、抹平鋸齒的 7 天滾動平均綠線、被蓋起來的測試週與虛線預測，以及滾動平均／自迴歸／週期 s=7 三個關鍵詞
:width: 100%

長條是每天賣的杯數（週末橘色爆單），綠線是 7 天平均（抹平鋸齒看趨勢），最後一週被「蓋起來」當測試週，橘色虛線是預測——掀開才知道準不準。
```

### 動手玩玩看：幫老闆預測下一週，還比兩種公式誰準

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
# 8 週 = 56 天的每日賣出杯數（生意慢慢變好，週末爆單）
days = pd.date_range("2026-03-02", periods=56, freq="D")   # 從週一開始
t = np.arange(56)
weekend_bonus = np.where(days.weekday >= 5, 40, 0)         # 週六日 +40 杯
cups = (60 + 1.2 * t + weekend_bonus + rng.normal(0, 8, 56)).round().astype(int)
sales = pd.DataFrame({"date": days, "cups": cups}).set_index("date")

# 招式一：7 天滾動平均，抹平鋸齒看趨勢
sales["rolling7"] = sales["cups"].rolling(7).mean()

# 招式四：把最後 7 天「蓋起來」當測試集，前面 49 天當訓練集
train, test = sales.iloc[:-7], sales.iloc[-7:]

# 兩種預測公式，掀開答案比 MAE（平均絕對誤差，越小越準）
pred_naive = np.full(7, train["cups"].iloc[-1])        # (a) 昨天法：明天≈今天（自迴歸最陽春版）
pred_seasonal = train["cups"].iloc[-7:].to_numpy()     # (b) 上週同一天法：抓住每 7 天的週期

mae_naive = np.abs(test["cups"].to_numpy() - pred_naive).mean()
mae_seasonal = np.abs(test["cups"].to_numpy() - pred_seasonal).mean()
print(f"昨天法       MAE = {mae_naive:.1f} 杯")
print(f"上週同一天法 MAE = {mae_seasonal:.1f} 杯  ← 抓住『週六爆單』的週期，猜得更準！")
```

跑出來會看到：

```text
昨天法       MAE = 23.7 杯
上週同一天法 MAE = 16.0 杯  ← 抓住『週六爆單』的週期，猜得更準！
```

**看懂了嗎？** 光是把「每 7 天重播一次」的週期考慮進去，平均誤差就從 23.7 杯降到 16 杯。這就是為什麼複雜一點的 **SARIMA**（會自動抓週期）常常贏過陽春的預測法。

### ⚠️ 四個必記的但書（這些超重要）

1. **這是天氣預報，不是算命**：模型假設「明天 ≈ 最近幾天」，所以它**在轉折點會失靈**——它猜不到疫情的**最高峰**哪天到、也猜不到突然的超級傳播事件或「關閉水源」之後的驟降。就像珍奶店老闆用「這週」推「下週」，遇到颱風天照樣被打臉。**短期還行，越遠越不準。**
2. **疫情的「週末低點」常是假的**：珍奶店週六爆單是**真的**（客人真的變多）；但疫情資料的週末病例下降，**常常是「週末比較少人就醫、檢驗、通報」造成的假象**，不是病毒放假。這是珍奶比喻**唯一會騙你**的地方，一定要記得。
3. **滾動平均會「慢半拍」**：它是回頭看過去的平均，所以真正暴衝的那一天，平滑線還在慢慢反應——**別只靠它抓突發高峰**。
4. **疫情不會永遠往上爬**：如果你硬把「一直上升」的趨勢無限外推，會預測出無限多病例。真實疫情會因為「可感染的人被感染得差不多了」而**轉彎、退燒**——這也是我們緊盯滾動平均那條線「頭有沒有往下垂」的原因。

> 📏 還有一個實務提醒：護理之家的資料只有 **17 天**，太短了，抓不出「每 7 天」的週期（SARIMA 至少需要 2 個完整週期）。這就是為什麼本章 Part B 要改用 **90 天的合成類流感資料**來示範週期預測——**開店才一週，別急著算「每月規律」**。

### 讀圖小抄（存起來）

| 你看到… | 白話意思 |
|---|---|
| 每日數字忽高忽低（鋸齒） | 原始 noise，先別被單日嚇到 |
| 7 天滾動平均線 | 抹平鋸齒後的**真趨勢** |
| 平滑線的頭往上翹 | 還在成長（疫情還在燒 → 快多備床） |
| 平滑線的頭往下垂 | 正在退燒（可以稍微鬆口氣） |
| 每隔固定天數重複的高低 | 週期性（s=7 = 每週） |
| 「用昨天、前天預測今天」 | 自迴歸（lag 特徵） |
| 把最後幾天藏起來測試 | train/test split（防作弊） |
| MAE 越小 | 預測平均差越少（越準） |
| 模型碰到高峰、驟降就失準 | 正常！模型不會算命，轉折點最難 |

### 回到真實：珍珠 → 病例

現在把珍奶店換成護理之家：

| 珍奶店老闆 | 護理之家真實案例 |
|---|---|
| 每天賣幾杯 | 每日**發病**人數（每日病例數） |
| 週末爆單的鋸齒 | 每日數字的 noise（但週末低點可能是通報效應！） |
| 7 天滾動平均 | 流行曲線的 7 天平均，看趨勢 |
| 「昨天旺，今天大概也旺」 | 自迴歸（Part A：Poisson＋lag） |
| 「每逢週六必爆」 | 週期性（Part B：SARIMA，s=7） |
| 蓋住上週、預測再對答案 | 訓練／測試切分 + MAE |
| 備多少珍珠、排幾個店員 | 準備多少病床、多少醫護人力 |

你剛剛幫老闆學會的每一招——滾動平均、自迴歸、週期、訓練/測試——**就是本章 Part A 與 Part B 在疫情資料上做的事**。現在往下看那六種模型的大比拼，是不是突然變親切了？😉

---

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

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：時間序列基本概念——asfreq、自相關、平穩性</div>
  <div class="youtube-lite" data-id="VYo8QnHEi74">
    <img src="https://img.youtube.com/vi/VYo8QnHEi74/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

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

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：Rolling mean baseline 與 shift(1) 救命符</div>
  <div class="youtube-lite" data-id="8VP3e7FSKPQ">
    <img src="https://img.youtube.com/vi/8VP3e7FSKPQ/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

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

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：Lag features——把時間序列變成迴歸資料</div>
  <div class="youtube-lite" data-id="1DTX1bomJ4E">
    <img src="https://img.youtube.com/vi/1DTX1bomJ4E/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
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

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：Poisson regression + lag——IRR 解讀每日病例</div>
  <div class="youtube-lite" data-id="zYXleAV-l2U">
    <img src="https://img.youtube.com/vi/zYXleAV-l2U/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

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

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：Negative Binomial——過度離散的救星</div>
  <div class="youtube-lite" data-id="5ZzrjUBGN8c">
    <img src="https://img.youtube.com/vi/5ZzrjUBGN8c/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
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

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：Logistic regression——明天會不會是高峰日？</div>
  <div class="youtube-lite" data-id="xzOQKhFM9js">
    <img src="https://img.youtube.com/vi/xzOQKhFM9js/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

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

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：ARIMA vs SARIMA——經典武器 + 週期性捕捉</div>
  <div class="youtube-lite" data-id="u6Tl3toQGZc">
    <img src="https://img.youtube.com/vi/u6Tl3toQGZc/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
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

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：六模型大比拼——誰適合什麼情境？</div>
  <div class="youtube-lite" data-id="u9gxSIb57a0">
    <img src="https://img.youtube.com/vi/u9gxSIb57a0/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

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
