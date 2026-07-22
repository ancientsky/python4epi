# 07 時間序列與預測：從滾動平均到 ARIMA/SARIMA

## 情境

松柏護理之家退伍軍人症群聚事件進入第二週，長官在疫調會議上丟出兩個問題：

> 「下禮拜還會有多少人發病？醫院還要準備幾張床？」
>
> 「**明天**會不會又是一個高峰日？要不要提前啟動警報？」

第一個問題要**連續數字**的預測（下週的病例數），第二個問題要**是/否的訊號**（明天是不是高峰）。這兩種需求用同一個滾動平均可能不夠——我們要比較**七種模型**，看誰最適合。

這一章的主軸：**從最簡單的 rolling mean 一路走到 ARIMA/SARIMA**，用護理之家資料示範短期預測，用 90 天合成類流感資料示範長期 + 週期預測。

## 你將學到

- 從 line list 建立每日病例時間序列（`asfreq` 補齊日期）
- 用 **rolling mean**（baseline）做短期預測
- 建立 **lagged features**（把「昨天、前天」變成特徵）
- 用 **Poisson regression + lag** 做計數資料預測
- 用 **Negative Binomial regression** 處理過度離散（overdispersion）
- 用 **Logistic regression** 做「高峰日警報」二元預測
- 用 **ARIMA / SARIMA** 在較長序列上捕捉趨勢 + 週期
- 用 **Prophet** 自動拆解趨勢/週期/假日並產生帶不確定區間的預測
- 用 **MAE / AIC** 系統性比較七種模型

## 🔮 超白話特別篇：用「珍奶店老闆的水晶球」看懂時間序列預測

> ARIMA、SARIMA、自相關、平穩性……一堆名詞是不是看得頭很痛？別怕。這一段先把疫情放一邊，改用一個超接地氣的角色——**一位想預測明天要賣幾杯的珍奶店老闆**——把時間序列預測整套邏輯講到讓國中生也會點頭。看完再回頭看下面那七種模型，你會發現：它們全都在做老闆每天在做的事！

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

你剛剛幫老闆學會的每一招——滾動平均、自迴歸、週期、訓練/測試——**就是本章 Part A 與 Part B 在疫情資料上做的事**。現在往下看那七種模型的大比拼，是不是突然變親切了？😉

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
:alt: 七種時間序列預測方法比較 —— rolling mean, Poisson+lag, Negative Binomial, Logistic, ARIMA, SARIMA, Prophet
:width: 100%

**時間序列預測方法地圖**：七個模型從簡單到複雜排開，最下面整排的綠色寬卡是 **Prophet**（好上手的現代選項）。資料越少 → 越左邊；需要捕捉週期 → 最右邊。每張卡片告訴你「最少要幾天資料」「能不能給信賴區間」「適合哪種情境」。
```

> 📌 最下面那張綠色寬卡就是第七種——**Prophet**：用**趨勢＋週期＋假日**三塊積木取代手動選 `(p,d,q)(P,D,Q,s)`，是免調參版的 SARIMA 替代方案。本章 **Step 11** 會動手實作。

---

## Step 1: 建立每日發病序列

這段程式把原始線列資料整理成**每日發病病例數**的時間序列，是後面所有模型的起點。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `df = pd.read_csv(...)` | 讀入完整的 280 位住民線列資料 |
> | `pd.to_datetime(..., errors="coerce")` | 把日期字串轉成日期型別；`errors="coerce"` 讓無法解析的日期變成 `NaT`，不會讓整段程式當掉 |
> | `df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)` | 嚴重度不是「未發病」就算感染，轉成 1/0 |
> | `cases = df[df["infected"] == 1]` | 只留下確實發病的病例 |
> | `cases.groupby("symptom_onset_date").size()` | 依發病日分組計數 → 每日病例數 |
> | `daily.asfreq("D", fill_value=0)` | **補齊沒有發病的日期**，缺的天數填 0 |
>
> 🔑 **`asfreq` 是這一步的靈魂**：`groupby` 只會產生「有病例的日期」，中間如果有一天零確診，那天會直接消失。少了 `asfreq("D", fill_value=0)` 補齊，時間序列會「跳日期」，後面的滾動平均和 ARIMA 都會算錯。

## Step 2: 流行曲線 + 滾動平均視覺

這裡把每日病例數畫成長條圖，疊上 7 天滾動平均線，讓忽高忽低的鋸齒現出真正的走勢。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `daily.rolling(window=7, min_periods=1).mean()` | 算 7 天滾動平均；`min_periods=1` 讓序列一開始（不足 7 天）也能算出數值，不會整批變成 `NaN` |
> | `ax.bar(daily.index, daily.values, ...)` | 每日病例數畫成長條（原始鋸齒） |
> | `ax.plot(rolling_7.index, rolling_7.values, ...)` | 疊上滾動平均線（抹平鋸齒後的趨勢） |
>
> 💡 **長條 + 線疊在同一張圖**：長條看「單日波動」，橘線看「整體趨勢」——兩個一起看，才不會被單日的忽高忽低嚇到或報喜。

---

## Part A ── 短期 outbreak 預測（護理之家資料，17 天）

### Step 3: Baseline —— Rolling mean 預測

在正式上迴歸模型之前，先用最簡單的**滾動平均**當 baseline：用前 w 天的平均去猜「明天」，順便掃過幾個窗口大小找出最準的一個。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `daily.rolling(window=w).mean()` | 算前 w 天的滾動平均 |
> | `.shift(1)` | **把預測值往後推一天**：用「到昨天為止」的平均去猜「今天」，不能用到今天自己的值 |
> | `.dropna()` | 序列最前面幾天湊不齊 w 天，丟掉那些 `NaN` |
> | `mean_absolute_error(actual_w, pred_w)` | 算預測值和實際值差多少（MAE，越小越準） |
>
> ⚠️ **`shift(1)` 不能省略**：如果直接用「今天的滾動平均」去預測「今天」，等於偷看了今天的答案（data leakage）——MAE 會漂亮到不真實，一上線就崩潰。

Rolling mean 的優點：**簡單、直覺、在第一天就能用**。缺點：它永遠是「看過去幾天的平均」，不會預測轉折、沒有信賴區間、也沒辦法放其他變項（例如樓層、星期幾）。

### Step 4: Lagged features —— 為迴歸模型建立「過去 k 天」特徵

這一步不建模型，只是**把時間序列改頭換面**：幫每一天多加幾欄「過去幾天的病例數」，讓迴歸模型能吃得下時間序列資料。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `ts = daily.to_frame("cases").reset_index(names="date")` | 把 Series 轉回一般表格，`date` 變成正常欄位 |
> | `ts["day_idx"] = range(len(ts))` | 加一欄「第幾天」，讓模型能抓到隨時間上升/下降的趨勢 |
> | `ts["lag_1"] = ts["cases"].shift(1)` | **把整欄往下推一格**：今天這一列多了「昨天的病例數」 |
> | `ts["lag_2"] = ts["cases"].shift(2)` | 同樣道理，多一欄「前天的病例數」 |
> | `ts.dropna()` | 前兩天沒有「昨天/前天」可用，會是 `NaN`，直接丟掉 |
>
> 🧭 **lag 特徵的本質**：`shift(1)` 只是把整欄資料「搬」到下一列，讓「昨天發生的事」變成「今天這一列的一個欄位」——時間序列從此變成一張普通的迴歸表格，Step 5-7 的模型才吃得下。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `smf.glm("cases ~ lag_1 + lag_2 + day_idx", data=ts_model, family=sm.families.Poisson())` | 建立 Poisson GLM：用昨天、前天的病例數 + 天數趨勢，去解釋今天的病例數 |
> | `.fit()` | 真正**估計參數**（跑最大概似估計），回傳配適好的模型物件 |
> | `model_pois.predict(ts_model)` | 用配適好的模型，對每一列算出「預期病例數」 |
> | `mean_absolute_error(...)` | 算 MAE，和 baseline 的 rolling mean 放在同一把尺上比較 |
> | `np.exp(model_pois.params)` | 把 log scale 的係數換成 **IRR（incidence rate ratio）**，才有白話可解讀 |
>
> 💡 **Poisson 係數要先取 `exp()` 才看得懂**：`coef` 是 log scale，直接看沒有意義；`exp(coef)` 才是「每多一單位，病例數變成幾倍」的 IRR。

**白話解讀**：`IRR(lag_1) ≈ 1.15` 表示「昨天每多 1 人發病，今天預期值會多 15%」。

### Step 6: Negative Binomial regression —— 處理過度離散

這一步先「驗傷」——檢查資料是不是過度離散（overdispersion），再決定要不要把 Step 5 的 Poisson 換成能吸收額外變異的 Negative Binomial。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `ts_model["cases"].var() / ts_model["cases"].mean()` | 算 **dispersion ratio**：變異數 ÷ 平均數 |
> | `family=sm.families.NegativeBinomial(alpha=1.0)` | 換成 Negative Binomial 分布，`alpha` 是額外吸收「過度離散」的參數 |
> | `model_nb.predict(ts_model)` / `mean_absolute_error(...)` | 和 Step 5 一樣的流程：預測、算 MAE，方便互相比較 |
>
> ⚠️ **dispersion > 1.5 才需要換模型**：Poisson 假設 variance = mean；一旦實際變異遠大於平均（過度離散），Poisson 的信賴區間會算得太窄，讓你誤以為結果比實際上更確定。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `ts_model["cases"].quantile(0.75)` | 抓病例數的 75th 百分位數，當「高峰日」的門檻 |
> | `(ts_model["cases"] > threshold).astype(int)` | 把連續病例數**二值化**：超過門檻 = 1（高峰日），否則 = 0 |
> | `smf.logit("high_day ~ lag_1 + lag_2", data=ts_model).fit(disp=False)` | 用昨天、前天的病例數去預測「今天是不是高峰日」；`disp=False` 只是不印出最佳化過程的逐次訊息 |
> | `model_logit.predict(ts_model)` | 算出**機率**（不是 0/1），代表「明天是高峰日」的可能性 |
> | `(prob > 0.5).astype(int)` | 把機率轉回 0/1，方便算準確率 |
>
> 🔑 **Logistic 給的是機率，不是病例數**：`predict()` 回傳的是 0～1 之間的機率，這正是「明天超過警戒線的機率是 72%」這種早期預警語言的來源。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `trend = np.linspace(3, 7, n_days)` | 打造一條慢慢上升的**趨勢線**（每日平均從 3 升到 7） |
> | `seasonal = 3 * np.sin(2 * np.pi * np.arange(n_days) / 7)` | 用正弦波製造**季節性**：每 7 天完整繞一圈 |
> | `noise = rng.normal(0, 1.2, n_days)` | 加入隨機噪音，模擬真實資料不會這麼「乾淨」 |
> | `np.maximum(0, (trend + seasonal + noise).round())` | 三者相加後四捨五入，並把負值夾在 0（病例數不能是負的） |
>
> 💡 **這是「已知答案」的練習資料**：因為 trend、seasonal、noise 都是自己指定的，等一下 ARIMA / SARIMA 抓不抓得到週期，我們自己心裡有底——這是驗證模型有沒有用的好方法。

### Step 9: ARIMA —— AutoRegressive Integrated Moving Average

在真正配適 ARIMA 之前，先用 ADF 檢定確認序列夠不夠平穩，再切出訓練/測試集看預測準不準。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `adfuller(synth)` | **ADF 平穩性檢定**：檢查序列的均值/變異有沒有隨時間漂移 |
> | `train, test = synth.iloc[:-7], synth.iloc[-7:]` | 切訓練／測試集：最後 7 天蓋起來當測試 |
> | `ARIMA(train, order=(1, 1, 1))` | 建立 ARIMA 模型，`order=(p, d, q)` = **(自迴歸落後項數, 差分次數, 移動平均落後項數)**：`p=1` 看前 1 天自己、`d=1` 做 1 次差分讓序列平穩、`q=1` 看前 1 次的預測誤差 |
> | `.fit()` | 用訓練集**估計參數** |
> | `model_arima.forecast(steps=7)` | 用配適好的模型，往前**預測 7 步**（對應蓋起來的測試集天數） |
> | `mean_absolute_error(test.values, forecast_arima.values)` | 掀開測試集答案，算預測誤差 |
>
> 🔑 **記住 `(p, d, q)` 的白話翻譯**：`p` = 自迴歸看幾天前的自己，`d` = 差分幾次讓序列平穩，`q` = 移動平均看幾次前的誤差。三個數字不是隨便選的，`d` 要參考 ADF 檢定的結果，`p`、`q` 通常要配合 ACF / PACF 圖或用 AIC 比較。

### Step 10: SARIMA —— 加入季節性

SARIMA 在 ARIMA 之外多一組季節參數，專門捕捉「每 7 天重複一次」的週期，讓預測跟著星期幾的節奏走。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))` | `order=(p,d,q)` 跟 ARIMA 一樣是「一般」的自迴歸/差分/移動平均；`seasonal_order=(P,D,Q,s)` 是**季節版**的同一組東西，`s=7` 代表週期 = 7 天 |
> | `.fit(disp=False)` | 估計參數；`disp=False` 讓最佳化過程不要一直印訊息洗版 |
> | `model_sarima.forecast(steps=7)` | 往前預測 7 天，和 ARIMA 用同一組測試集比較 |
>
> 🧭 **`seasonal_order` 的四個數字**：`(P, D, Q, s)` 分別是「季節自迴歸項數、季節差分次數、季節移動平均項數、季節週期長度」——`s=7` 就是告訴模型「每隔 7 天，回頭比對一次同一個星期幾」，這正是 SARIMA 比 ARIMA 多出來、能抓住週末爆量的關鍵。

**關鍵觀察**：SARIMA 的 MAE 明顯小於 ARIMA，因為它抓到了 7 天的週循環。對於**沒有週期性**的資料，多加 SARIMA 反而浪費（參數多、容易過配）。

---

## Step 11: Prophet —— Meta 的「自動拆積木」水晶球

Prophet 是 Meta 開源的預測工具，把序列**自動拆成 趨勢(trend) + 週期(seasonality) + 假日(holidays)** 三塊積木相加，只要 `ds`/`y` 兩欄、幾乎免調參，還自帶不確定區間。

```{figure} images/prophet_decomposition.svg
:name: fig-prophet-decomposition
:alt: Prophet 把觀測序列自動拆成趨勢加週期加假日三塊積木相加，並輸出帶不確定區間的預測
:width: 100%

Prophet 的核心：觀測 = 趨勢 + 週期 + 假日，還附一條不確定區間。
```

```python
import logging
logging.getLogger("cmdstanpy").setLevel(logging.ERROR)  # 關掉 Stan 的雜訊 log
from prophet import Prophet

# Prophet 只吃兩欄：ds（日期）+ y（值）
pdf = synth.reset_index()
pdf.columns = ["ds", "y"]
p_train = pdf.iloc[:-7]                    # 跟前面同一個 train/test 切分

m = Prophet(weekly_seasonality=True, yearly_seasonality=False,
            daily_seasonality=False, interval_width=0.9)
m.fit(p_train)                             # 自動偵測趨勢變點 + 擬合週期

future = m.make_future_dataframe(periods=7)   # 往後展 7 天
forecast = m.predict(future)
yhat = forecast["yhat"].iloc[-7:].values
mae_prophet = mean_absolute_error(test.values, yhat)
print(f"Prophet:  MAE={mae_prophet:.3f}  (fit 幾乎不用調參，還自帶不確定區間)")
print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(7).to_string(index=False))

# 視覺化：預測 + 90% 不確定區間
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(train.index[-30:], train.values[-30:], color="#6B6B6B",
        linewidth=1.2, label="訓練（最後 30 天）")
ax.plot(test.index, test.values, color="#1A1A1A", linewidth=2,
        marker="o", markersize=5, label="實際")
ax.plot(test.index, yhat, color="#788C5D", linewidth=1.8,
        marker="D", markersize=5, linestyle="--", label=f"Prophet (MAE={mae_prophet:.2f})")
ax.fill_between(test.index, forecast["yhat_lower"].iloc[-7:].values,
                forecast["yhat_upper"].iloc[-7:].values,
                color="#788C5D", alpha=0.2, label="90% 不確定區間")
ax.set_title("Prophet 未來 7 天預測（含不確定區間）", fontweight="bold")
ax.set_xlabel("日期"); ax.set_ylabel("每日通報數")
ax.legend(loc="upper left"); ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.autofmt_xdate(); plt.tight_layout(); plt.show()
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `logging.getLogger("cmdstanpy").setLevel(logging.ERROR)` | Prophet 底層用 Stan 做貝氏估計，預設會印一堆訓練過程訊息；這行把雜訊關掉 |
> | `pdf.columns = ["ds", "y"]` | **Prophet 只認這兩個欄名**：`ds`（日期，datestamp）和 `y`（要預測的值）——改完欄名它才吃得下 |
> | `Prophet(weekly_seasonality=True, yearly_seasonality=False, daily_seasonality=False, interval_width=0.9)` | 打開「每週週期」偵測（我們的資料週期 s=7）、關掉不需要的年/日週期；`interval_width=0.9` 設定輸出 **90% 不確定區間** |
> | `m.fit(p_train)` | 餵訓練資料，Prophet 自動拆解趨勢 + 週期（連趨勢轉折點都會自動抓） |
> | `m.make_future_dataframe(periods=7)` | 在既有日期後面**再接 7 天**空白列，準備讓模型往未來預測 |
> | `m.predict(future)` | 對每一天輸出 `yhat`（預測值）+ `yhat_lower` / `yhat_upper`（不確定區間上下界） |
> | `forecast["yhat"].iloc[-7:]` | 取出最後 7 天（對應蓋起來的測試集）的預測值，跟其他模型用同一把尺（MAE）比較 |
>
> 🔑 **`ds`/`y` 是 Prophet 的唯一規矩**：不用手動做 lag、不用選 `(p,d,q)`，只要把日期欄改名 `ds`、目標欄改名 `y`，其餘全部交給模型自動處理。

💡 **準度沒有更神，但省下一大堆調參功夫**：Prophet 在這條序列上 **MAE ≈ 0.774**，跟**調好的 SARIMA（0.770）幾乎打平**——但 SARIMA 要自己選 `(p,d,q)(P,D,Q,s)`、還要處理平穩性，Prophet 只要兩欄資料就能上手。Prophet 真正的優勢是**好上手 + 自動抓週期/假日/變點 + 免費附不確定區間**，不是準度更高。

⚠️ **Prophet 不是萬靈丹**：它是**加法模型**，假設未來是「已學到的趨勢＋週期」的延續；疫情爆發期那種非線性回饋（像 SEIR 的傳播動力）它抓不到，資料太短（不到約 2 個週期）也學不動——它加入工具箱的是**誠實的選項**，不是更準的水晶球。

---

## Step 12: 模型大比拼

把前面七個模型的 MAE、資料需求、能不能給信賴區間全部攤開放進同一張表，方便直接比較。

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
    {"model": "⑦ Prophet",                 "資料集": "synth 90d", "MAE": mae_prophet,
     "最少資料": "~14 天", "捕捉週期": "強(自動)", "信賴區間": "是"},
])
print(comparison.to_string(index=False))
```

> 💡 **這張表的重點不是數字本身，是「最少資料」和「捕捉週期」兩欄**——資料不夠長就不用勉強上 SARIMA，沒有季節性也不用為了炫技硬上。

**結論白話版**：
- **資料只有一兩週**（outbreak 剛爆發）→ Rolling mean 或 Poisson + lag 就夠
- **過度離散明顯**（群聚、突發疫情）→ 改 Negative Binomial
- **需要是/否警報**（要不要啟動應變層級）→ Logistic regression
- **中長期監測**（> 一個月、無明顯週期）→ ARIMA
- **類流感、每週監測**（有明顯週循環）→ SARIMA
- **要快速上手、想要趨勢/週期/假日自動拆解 + 不確定區間** → Prophet

## Step 13: 發病 vs 住院曲線（Lag 效應）

這裡疊圖比較發病曲線和住院曲線，看住院高峰比發病高峰晚了幾天。

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `cases[...].groupby("hospitalization_date").size()` | 依住院日期分組計數 → 每日住院人數 |
> | `pd.date_range(...)` + `hosp_daily.reindex(all_dates, fill_value=0)` | 把住院曲線**對齊**發病曲線的完整日期範圍，缺的日期補 0，兩條線才能疊在同一個時間軸上比較 |
> | `hosp_aligned.idxmax() - daily.idxmax()` | 找出住院高峰日和發病高峰日，相減得到**天數差（lag）** |
>
> 💡 **對齊日期是疊圖比較的前提**：如果不用 `reindex` 補齊，兩條曲線的日期範圍可能對不齊，畫出來的 lag 會失真。

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
8. **以為 Prophet 一定比 ARIMA/SARIMA 準**：它強在好上手與自動化，準度是與調好的 SARIMA 相當，不是天生更準

## 下一步

知道「何時」疫情最嚴重後，接下來問「在哪裡」最嚴重？→ Ch08 空間流病。

## 練習本

- 課堂筆記：{ref}`07_time_series_baseline.ipynb`
- 作業版：[`07_time_series_exercise.ipynb`](exercises/07_time_series_exercise.ipynb)
- 解答版（教師版）：[`07_time_series_solution.ipynb`](solutions/07_time_series_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/07_time_series_solution.ipynb>)
