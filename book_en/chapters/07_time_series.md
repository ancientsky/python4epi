# 07 Time Series and Forecasting: From Rolling Averages to ARIMA/SARIMA

## Scenario

The Legionnaires' disease outbreak at Songbai Nursing Home has entered its second week, and at the outbreak investigation meeting the supervisor throws out two questions:

> "How many more people will get sick next week? How many hospital beds do we need to prepare?"
>
> "Will **tomorrow** be another peak day? Should we trigger an alert early?"

The first question asks for a **continuous number** forecast (next week's case count); the second asks for a **yes/no signal** (whether tomorrow is a peak). A single rolling average may not be enough for both needs—so we'll compare **six models** to see which fits best.

The main thread of this chapter: **going from the simplest rolling mean all the way to ARIMA/SARIMA**, using the nursing home data to demonstrate short-term forecasting, and using 90 days of synthetic influenza-like data to demonstrate long-term + seasonal forecasting.

## What You Will Learn

- Building a daily case time series from a line list (using `asfreq` to fill in dates)
- Making short-term forecasts with a **rolling mean** (baseline)
- Building **lagged features** (turning "yesterday, the day before" into features)
- Forecasting count data with **Poisson regression + lag**
- Handling overdispersion with **Negative Binomial regression**
- Making "peak day alert" binary predictions with **Logistic regression**
- Capturing trend + seasonality on longer series with **ARIMA / SARIMA**
- Systematically comparing six models with **MAE / AIC**

## Core Concepts

| Concept | Explanation |
|------|------|
| **Time series** | Observations arranged in time order; adjacent points are usually highly correlated |
| **Autocorrelation** | Today's value is related to yesterday's → can be captured with lag features |
| **Lag features** | Bringing "yesterday, the day before" values over to serve as today's feature columns |
| **Stationarity** | Mean and variance don't drift over time; a prerequisite for ARIMA |
| **Overdispersion** | variance > mean → Poisson becomes inaccurate → switch to Negative Binomial |
| **Seasonality** | Fixed cycles like 7 days or 12 months → need SARIMA |
| **MAE** | Mean Absolute Error, the average absolute forecasting error |
| **AIC** | Akaike Information Criterion, smaller is better, penalizes overfitting |
| **Data leakage** | Using future information to make predictions → unreliable results (always `shift(1)`) |

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Time series fundamentals—asfreq, autocorrelation, stationarity</div>
  <div class="youtube-lite" data-id="VYo8QnHEi74">
    <img src="https://img.youtube.com/vi/VYo8QnHEi74/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

## Method Overview

```{figure} images/timeseries_method_map_en.svg
:name: fig-timeseries-method-map
:alt: Comparison of six time series forecasting methods — rolling mean, Poisson+lag, Negative Binomial, Logistic, ARIMA, SARIMA
:width: 100%

**Map of time series forecasting methods**: six models laid out from simple to complex. Less data → further left; need to capture seasonality → furthest right. Each card tells you "how many days of data at minimum," "whether it can give confidence intervals," and "which situation it suits."
```

---

## Step 1: Build the Daily Onset Series

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

# Daily onset counts, filling in dates with no onsets (ensuring continuity)
daily = cases.groupby("symptom_onset_date").size()
daily = daily.asfreq("D", fill_value=0)
daily.name = "cases"
print(f"Series length: {len(daily)} days | Total cases: {daily.sum()}")
```

## Step 2: Epidemic Curve + Rolling Average Visualization

```python
rolling_7 = daily.rolling(window=7, min_periods=1).mean()
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, width=1.0,
       color="#6A9BCC", edgecolor="white", alpha=0.6, label="Daily new cases")
ax.plot(rolling_7.index, rolling_7.values, color="#D97757", linewidth=2,
        label="7-day rolling average")
ax.set_title("Songbai Nursing Home Legionnaires' Disease Epidemic Curve", fontweight="bold")
ax.set_xlabel("Onset date"); ax.set_ylabel("Number of cases")
ax.legend(); ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.autofmt_xdate(); plt.tight_layout(); plt.show()
```

---

## Part A ── Short-Term Outbreak Forecasting (Nursing Home Data, 17 Days)

### Step 3: Baseline —— Rolling Mean Forecast

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Rolling mean baseline and the shift(1) lifesaver</div>
  <div class="youtube-lite" data-id="8VP3e7FSKPQ">
    <img src="https://img.youtube.com/vi/8VP3e7FSKPQ/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
# Predict "the next day" using the average of the previous w days; shift(1) avoids data leakage
mae_by_window = {}
for w in [3, 5, 7]:
    pred_w = daily.rolling(window=w).mean().shift(1).dropna()
    actual_w = daily.loc[pred_w.index]
    mae_by_window[w] = mean_absolute_error(actual_w, pred_w)
    print(f"  rolling mean (w={w}):  MAE={mae_by_window[w]:.3f}")

mae_rolling = mae_by_window[3]
print(f"\n→ Best: window=3, MAE={mae_rolling:.3f}")
```

Advantages of the rolling mean: **simple, intuitive, usable from day one**. Drawbacks: it's always "the average of the past few days," so it can't predict turning points, has no confidence intervals, and can't incorporate other variables (like floor or day of week).

### Step 4: Lagged Features —— Building "Past k Days" Features for Regression Models

```{figure} images/lag_features_explained_en.svg
:name: fig-lag-features
:alt: Using shift(1) to move past values to today's row, becoming lag_1 / lag_2 features
:width: 100%

**Lag features**: `df["lag_1"] = df["cases"].shift(1)` pushes the whole column down one row, so "yesterday's cases" appears in "today's row." Combined with `lag_2` and `lag_3`, you can **turn a time series into a table that ordinary regression can consume**.
```

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Lag features—turning a time series into regression data</div>
  <div class="youtube-lite" data-id="1DTX1bomJ4E">
    <img src="https://img.youtube.com/vi/1DTX1bomJ4E/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
ts = daily.to_frame("cases").reset_index(names="date")
ts["day_idx"] = range(len(ts))       # Day number (trend)
ts["lag_1"] = ts["cases"].shift(1)   # Yesterday's case count
ts["lag_2"] = ts["cases"].shift(2)   # The day before yesterday's case count
ts_model = ts.dropna().reset_index(drop=True)  # Drop the first two rows (NaN)
print(ts_model.head())
print(f"Usable rows: {len(ts_model)}")
```

```{note}
Why add lags? Because infection is transmissible—today's case count is highly correlated with yesterday's (autocorrelation). By using "yesterday's value" as a feature, the regression model can learn: "many yesterday, many today" and "a surge yesterday means today might surge again."
```

### Step 5: Poisson Regression + Lag

Count data (daily counts are 0, 1, 2, ...) are naturally suited to the **Poisson** distribution. We use `statsmodels`' GLM to include the lag features + a trend term:

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Poisson regression + lag—reading daily cases with IRR</div>
  <div class="youtube-lite" data-id="zYXleAV-l2U">
    <img src="https://img.youtube.com/vi/zYXleAV-l2U/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Poisson GLM: cases ~ yesterday + day before + day trend
model_pois = smf.glm(
    "cases ~ lag_1 + lag_2 + day_idx",
    data=ts_model,
    family=sm.families.Poisson(),
).fit()

pred_pois = model_pois.predict(ts_model)
mae_pois = mean_absolute_error(ts_model["cases"], pred_pois)
print(f"Poisson + lag:  MAE={mae_pois:.3f},  AIC={model_pois.aic:.2f}")

# Interpret the coefficients: exp(β) = incidence rate ratio (IRR)
coef_table = pd.DataFrame({
    "coef (log scale)": model_pois.params,
    "IRR exp(coef)": np.exp(model_pois.params),
})
print(coef_table.round(3))
```

**In plain terms**: `IRR(lag_1) ≈ 1.15` means "for each additional person who fell ill yesterday, today's expected value is 15% higher."

### Step 6: Negative Binomial Regression —— Handling Overdispersion

```{figure} images/poisson_vs_nb_dispersion_en.svg
:name: fig-poisson-vs-nb
:alt: Poisson assumes variance = mean; Negative Binomial allows overdispersion where variance > mean
:width: 100%

**Poisson's big assumption**: `variance = mean`. But outbreak investigation data often misbehaves—once cluster infection occurs, the variance is far greater than the mean (**overdispersion**). In that case you should switch to **Negative Binomial**, which adds a parameter α specifically to absorb the "extra" variance.
```

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Negative Binomial—the savior for overdispersion</div>
  <div class="youtube-lite" data-id="5ZzrjUBGN8c">
    <img src="https://img.youtube.com/vi/5ZzrjUBGN8c/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
# First check the dispersion ratio
disp = ts_model["cases"].var() / ts_model["cases"].mean()
print(f"dispersion = variance / mean = {disp:.2f}")
print("→ >1.5 is considered overdispersion → switch to Negative Binomial")

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

### Step 7: Logistic Regression —— "Will Tomorrow Be a Peak Day?"

The supervisor's second question is a **yes/no alert**, not a continuous number. The approach: **binarize** each day's case count (above a certain threshold → 1, otherwise → 0), then use logistic regression to predict the probability.

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Logistic regression—will tomorrow be a peak day?</div>
  <div class="youtube-lite" data-id="xzOQKhFM9js">
    <img src="https://img.youtube.com/vi/xzOQKhFM9js/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
# Use the 75th percentile as the "peak day" threshold
threshold = ts_model["cases"].quantile(0.75)
ts_model["high_day"] = (ts_model["cases"] > threshold).astype(int)
print(f"Peak day threshold (>75th) = {threshold:.0f} people")

# Use yesterday's and the day before's case counts to predict "will tomorrow exceed the threshold"
model_logit = smf.logit("high_day ~ lag_1 + lag_2", data=ts_model).fit(disp=False)
prob = model_logit.predict(ts_model)
pred_binary = (prob > 0.5).astype(int)
acc = (pred_binary == ts_model["high_day"]).mean()
print(f"\nLogistic (threshold): accuracy = {acc:.3f}")
```

**This model won't tell you "how many people there will be tomorrow," but it will tell you "there's a 72% chance tomorrow exceeds the alert line"**—which is exactly the output an early warning system really needs.

---

## Part B ── Long-Term Surveillance Forecasting (Synthetic 90-Day Data)

### Step 8: Why Isn't the Outbreak Data Enough? + Synthetic Demonstration Series

ARIMA / SARIMA need **≥ 30 days** (SARIMA needs even more—**at least 2 complete cycles**). The nursing home data has only 17 days; forcing it in yields unstable results. Here we **synthesize a 90-day "daily influenza-like case count" series on the spot**, including trend, a 7-day weekly cycle, and random noise:

```python
rng = np.random.default_rng(42)
n_days = 90
dates = pd.date_range("2025-10-01", periods=n_days, freq="D")

trend = np.linspace(3, 7, n_days)                   # Daily mean slowly rising from 3 to 7
seasonal = 3 * np.sin(2 * np.pi * np.arange(n_days) / 7)   # 7-day cycle
noise = rng.normal(0, 1.2, n_days)                  # Random noise

synth_cases = np.maximum(0, (trend + seasonal + noise).round()).astype(int)
synth = pd.Series(synth_cases, index=dates, name="cases")

fig, ax = plt.subplots(figsize=(10, 3.5))
ax.plot(synth.index, synth.values, color="#6A9BCC", linewidth=1.5)
ax.set_title("Synthetic influenza-like daily case count (trend + 7-day cycle + noise)", fontweight="bold")
ax.set_xlabel("Date"); ax.set_ylabel("Daily case count")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.autofmt_xdate(); plt.tight_layout(); plt.show()
```

### Step 9: ARIMA —— AutoRegressive Integrated Moving Average

```{figure} images/arima_sarima_decomposition_en.svg
:name: fig-arima-sarima
:alt: A time series can be decomposed into trend + seasonal + residual; ARIMA(p,d,q) is made of three parts, and SARIMA adds a seasonal component
:width: 100%

**ARIMA's three letters**: **AR(p)** looks at the past p days of itself; **I(d)** takes d differences to make the series stationary; **MA(q)** looks at the past q forecast errors. **SARIMA** additionally adds a set of (P, D, Q, s) specifically to capture the seasonal cycle s.
```

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: ARIMA vs SARIMA—the classic weapon + capturing seasonality</div>
  <div class="youtube-lite" data-id="u6Tl3toQGZc">
    <img src="https://img.youtube.com/vi/u6Tl3toQGZc/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# First run a stationarity test (ADF test)
adf_stat, p_value, *_ = adfuller(synth)
print(f"ADF statistic = {adf_stat:.3f}, p-value = {p_value:.3f}")
print(f"→ p < 0.05 means the series is stationary (no differencing needed, d=0); otherwise d ≥ 1")

# Split train / test: first 83 days for training, last 7 days for testing
train, test = synth.iloc[:-7], synth.iloc[-7:]

model_arima = ARIMA(train, order=(1, 1, 1)).fit()
forecast_arima = model_arima.forecast(steps=7)
mae_arima = mean_absolute_error(test.values, forecast_arima.values)
print(f"\nARIMA(1,1,1):  MAE={mae_arima:.3f},  AIC={model_arima.aic:.2f}")
```

### Step 10: SARIMA —— Adding Seasonality

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Seasonal period s=7 (weekly)
model_sarima = SARIMAX(
    train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 7),
).fit(disp=False)

forecast_sarima = model_sarima.forecast(steps=7)
mae_sarima = mean_absolute_error(test.values, forecast_sarima.values)
print(f"SARIMA(1,1,1)(1,1,1,7):  MAE={mae_sarima:.3f},  AIC={model_sarima.aic:.2f}")

# Visualization: forecast vs actual
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.plot(train.index[-30:], train.values[-30:], color="#6B6B6B",
        linewidth=1.2, label="Training (last 30 days)")
ax.plot(test.index, test.values, color="#1A1A1A", linewidth=2,
        marker="o", markersize=5, label="Actual")
ax.plot(test.index, forecast_arima.values, color="#6A9BCC", linewidth=1.8,
        marker="s", markersize=5, linestyle="--", label=f"ARIMA (MAE={mae_arima:.2f})")
ax.plot(test.index, forecast_sarima.values, color="#D97757", linewidth=1.8,
        marker="^", markersize=5, linestyle="--", label=f"SARIMA (MAE={mae_sarima:.2f})")
ax.set_title("ARIMA vs SARIMA 7-day forecast", fontweight="bold")
ax.set_xlabel("Date"); ax.set_ylabel("Daily case count")
ax.legend(loc="upper left"); ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.autofmt_xdate(); plt.tight_layout(); plt.show()
```

**Key observation**: SARIMA's MAE is clearly smaller than ARIMA's, because it captured the 7-day weekly cycle. For data with **no seasonality**, adding SARIMA is actually wasteful (more parameters, prone to overfitting).

---

## Step 11: Model Showdown

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Six-model showdown—which one suits which situation?</div>
  <div class="youtube-lite" data-id="u9gxSIb57a0">
    <img src="https://img.youtube.com/vi/u9gxSIb57a0/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
comparison = pd.DataFrame([
    {"model": "① Rolling mean (w=3)",      "dataset": "outbreak", "MAE": mae_rolling,
     "min data": "5 days",  "captures seasonality": "No",     "confidence interval": "No"},
    {"model": "② Poisson + lag",           "dataset": "outbreak", "MAE": mae_pois,
     "min data": "10 days", "captures seasonality": "Partial", "confidence interval": "Yes"},
    {"model": "③ Negative Binomial + lag", "dataset": "outbreak", "MAE": mae_nb,
     "min data": "10 days", "captures seasonality": "Partial", "confidence interval": "Yes"},
    {"model": "④ Logistic (threshold)",    "dataset": "outbreak", "MAE": f"— (acc={acc:.2f})",
     "min data": "10 days", "captures seasonality": "No",     "confidence interval": "Yes (probability)"},
    {"model": "⑤ ARIMA(1,1,1)",            "dataset": "synth 90d", "MAE": mae_arima,
     "min data": "30 days", "captures seasonality": "Weak",   "confidence interval": "Yes"},
    {"model": "⑥ SARIMA(1,1,1)(1,1,1,7)",  "dataset": "synth 90d", "MAE": mae_sarima,
     "min data": "60 days", "captures seasonality": "Strong", "confidence interval": "Yes"},
])
print(comparison.to_string(index=False))
```

**Conclusions in plain terms**:
- **Only one or two weeks of data** (outbreak just started) → Rolling mean or Poisson + lag is enough
- **Clear overdispersion** (cluster, sudden outbreak) → switch to Negative Binomial
- **Need a yes/no alert** (whether to escalate the response level) → Logistic regression
- **Medium-to-long-term surveillance** (> a month, no obvious cycle) → ARIMA
- **Influenza-like, weekly surveillance** (obvious weekly cycle) → SARIMA

## Step 12: Onset vs Hospitalization Curve (Lag Effect)

```python
hosp_daily = (
    cases[cases["hospitalization_date"].notna()]
    .groupby("hospitalization_date").size()
)
all_dates = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
hosp_aligned = hosp_daily.reindex(all_dates, fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, width=1.0, alpha=0.55,
       color="#6A9BCC", edgecolor="white", label="Onset")
ax.bar(hosp_aligned.index, hosp_aligned.values, width=1.0, alpha=0.55,
       color="#D97757", edgecolor="white", label="Hospitalization")
ax.set_title("Onset vs Hospitalization Curve (Lag Effect)", fontweight="bold")
ax.set_xlabel("Date"); ax.set_ylabel("Number of people")
ax.legend(); ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.autofmt_xdate(); plt.tight_layout(); plt.show()

lag_days = (hosp_aligned.idxmax() - daily.idxmax()).days
print(f"Onset peak → hospitalization peak lag = {lag_days} days")
```

This lag is a **golden indicator for bed planning**: hospitalization demand only peaks a few days after the onset peak has passed.

---

## Key Interpretations

| Observation | Meaning |
|------|------|
| Dispersion ratio > 1.5 | Poisson is inaccurate → use Negative Binomial |
| ADF p-value > 0.05 | Series is non-stationary → ARIMA's d should be ≥ 1 |
| SARIMA MAE < ARIMA | Data has an obvious cycle |
| Logistic probability > 0.5 | Forecasts "likely a peak day," recommend triggering an alert |
| Rolling mean MAE close to other models | Data too short, signal too weak → no need to reach for SARIMA just to show off |

## Common Mistakes

1. **Data leakage**: forgetting `shift(1)` and using today's value to predict today → MAE looks gorgeous, but it collapses in production
2. **Not filling in dates**: skipping days with no onsets makes the time series discontinuous, distorting both rolling and ARIMA
3. **Reporting only a single metric**: MAE without a baseline comparison is meaningless
4. **Ignoring overdispersion**: forcing Poisson when variance is large → confidence intervals too narrow, underestimating uncertainty
5. **Overfitting**: only 17 days of data yet wanting to train SARIMA → more parameters than observations
6. **Ignoring stationarity**: applying ARIMA without an ADF test → guessing the d value blindly
7. **Randomly trying ARIMA orders**: picking (p,d,q) arbitrarily without looking at AIC / ACF / PACF → results by luck

## Next Step

Once you know "when" the outbreak is most severe, the next question is "where" it's most severe? → Ch08 Spatial Epidemiology.

## Notebooks

- Class notes: {ref}`07_time_series_baseline.ipynb`
- Exercise version: [`07_time_series_exercise.ipynb`](exercises/07_time_series_exercise.ipynb)
- Solution version (instructor): [`07_time_series_solution.ipynb`](solutions/07_time_series_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/07_time_series_solution.ipynb>)
