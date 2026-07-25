# 07 Time Series and Forecasting: From Rolling Averages to ARIMA/SARIMA

## Scenario

The Legionnaires' disease outbreak at Songbai Nursing Home has entered its second week, and at the outbreak investigation meeting the supervisor throws out two questions:

> "How many more people will get sick next week? How many hospital beds do we need to prepare?"
>
> "Will **tomorrow** be another peak day? Should we trigger an alert early?"

The first question asks for a **continuous number** forecast (next week's case count); the second asks for a **yes/no signal** (whether tomorrow is a peak). A single rolling average may not be enough for both needs—so we'll compare **seven models** to see which fits best.

The main thread of this chapter: **going from the simplest rolling mean all the way to ARIMA/SARIMA**, using the nursing home data to demonstrate short-term forecasting, and using 90 days of synthetic influenza-like data to demonstrate long-term + seasonal forecasting.

## What You Will Learn

- Building a daily case time series from a line list (using `asfreq` to fill in dates)
- Making short-term forecasts with a **rolling mean** (baseline)
- Building **lagged features** (turning "yesterday, the day before" into features)
- Forecasting count data with **Poisson regression + lag**
- Handling overdispersion with **Negative Binomial regression**
- Making "peak day alert" binary predictions with **Logistic regression**
- Capturing trend + seasonality on longer series with **ARIMA / SARIMA**
- Automatically decomposing trend/seasonality/holidays and producing forecasts with uncertainty intervals using **Prophet**
- Systematically comparing seven models with **MAE / AIC**

## 🔮 Super Simple Special: Understanding Time-Series Forecasting with a "Bubble-Tea Shop Owner's Crystal Ball"

> ARIMA, SARIMA, autocorrelation, stationarity... does that pile of jargon make your head spin? Don't be scared. This section sets the outbreak aside for a moment and brings in a super down-to-earth character—**a bubble-tea shop owner trying to predict how many cups she'll sell tomorrow**—to walk through the entire logic of time-series forecasting in a way that'll make even a 7th grader nod along. Once you're done, go back and look at the seven models below—you'll notice they're all just doing what the shop owner does every single day!

### The Owner's Dilemma: How Much Should I Prep for Tomorrow?

Every morning, the bubble-tea shop owner is betting on one thing:

> "How many tapioca pearls should I cook today? How many staff should I schedule? Prep too much and it goes to waste; prep too little and customers will chew me out."

How she wishes she had a **crystal ball** that could show roughly how many cups she'll sell tomorrow. That's exactly what **time-series forecasting** does—and it turns out her dilemma is **identical** to an outbreak commander's:

> 🛏️ **"Roughly how many people will fall ill tomorrow? How many hospital beds and how much staff do we need to prepare?"** The shop's "pearls and staff" are the outbreak's "hospital beds and healthcare workers." **Forecasting exists so you can prepare ahead of time.**

### Move One: Rolling Average — Don't Panic Over a Single Day

When the owner looks at daily sales, she notices they're **jagged, jumping up and down like a sawtooth**: Saturdays are a mob scene, Mondays are dead quiet. If she just looks at "yesterday was crazy busy" and preps like crazy, Monday's leftovers are a disaster. What should she do?

> ⚖️ **The weighing-yourself metaphor**: Would you panic because "I'm 0.5 kg heavier this morning"? No—that's probably just drinking an extra glass of water. You need to look at the **average over a whole week** to get an accurate picture. Daily case counts work the same way: a **7-day rolling average (rolling mean)** is like putting on a pair of "de-jaggifying glasses"—it smooths out the ups and downs of the weekend and reveals the **real underlying trend** hiding beneath.

### Move Two: Autoregression — Tomorrow Looks a Lot Like Your Recent Self

The owner's most intuitive forecasting method: "Sales were high yesterday and the day before, so today probably won't be too bad either."

> 🌡️ This is called **autoregression**—just like weather has momentum ("cold yesterday, probably cold today too"). Business has momentum too, so you can **use the last few days' numbers to guess tomorrow**. The Poisson + lag model in Part A of this chapter is doing exactly that: "using yesterday and the day before as features to predict today."

### Move Three: Seasonality — Saturday Always Gets Slammed

The owner has also noticed an ironclad rule: **every single Saturday gets slammed**, week after week.

> 📅 **The folding-the-calendar metaphor**: Fold the calendar into stacks of 7 days each, and you'll notice the "Saturday" square is always the most crowded one. This fixed rerun that plays **exactly every 7 days** is **seasonality, with period s=7**. The `s=7` in SARIMA's name is reminding the model: "every 7 days, look back and check the same day of the week again."

> 🔑 One sentence to tell them apart: **autoregression is "short-term momentum" (the lingering warmth of the last few days), while seasonality is "long-term rhythm" (the same fixed day every week)**—use both together for an accurate forecast.

### Move Four: Train/Test — No Peeking at the Answers!

The owner comes up with a forecasting formula—how does she know if it's actually accurate? **She can't brag using days she's already seen.**

> 📝 **The old-exam-questions metaphor**: If you quiz yourself with a test you've already checked the answers to, of course you'll score 100%—but that doesn't mean you can solve **tomorrow's** brand-new questions. The right approach: **cover up** the actual sales from the last week first, force yourself to predict without seeing the answers, and only then lift the cover to check. Peeking at the future = **cheating (data leakage)**—the model will "ace the test" but flop badly once it's actually deployed.

This is exactly what a **train/test split** is: use the earlier data to come up with the formula (training), then check it against the hidden last few days (testing), and score it with **MAE (average error in cups)**—the smaller, the more accurate.

```{figure} images/bubbletea_forecast_en.svg
:name: fig-bubbletea-forecast
:alt: Daily bubble-tea sales time series: jagged bars showing weekend spikes, a green 7-day rolling-average line that smooths out the sawtooth pattern, a covered-up test week with a dashed forecast line, and the three key terms rolling average / autoregression / seasonality s=7
:width: 100%

The bars are cups sold each day (orange spikes on weekends), the green line is the 7-day average (smoothing out the sawtooth to reveal the trend), the last week is "covered up" as the test week, and the orange dashed line is the forecast—only by lifting the cover do we know if it was accurate.
```

### Try It Yourself: Forecast the Owner's Next Week, and See Which Formula Wins

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
# 8 weeks = 56 days of daily cups sold (business slowly improves, weekends spike)
days = pd.date_range("2026-03-02", periods=56, freq="D")   # starts on a Monday
t = np.arange(56)
weekend_bonus = np.where(days.weekday >= 5, 40, 0)         # Sat/Sun get +40 cups
cups = (60 + 1.2 * t + weekend_bonus + rng.normal(0, 8, 56)).round().astype(int)
sales = pd.DataFrame({"date": days, "cups": cups}).set_index("date")

# Move One: 7-day rolling average, smooths out the sawtooth to reveal the trend
sales["rolling7"] = sales["cups"].rolling(7).mean()

# Move Four: "cover up" the last 7 days as the test set, the first 49 days are the training set
train, test = sales.iloc[:-7], sales.iloc[-7:]

# Two forecasting formulas, lift the cover and compare MAE (mean absolute error, smaller = more accurate)
pred_naive = np.full(7, train["cups"].iloc[-1])        # (a) Naive: tomorrow ~= today (the plainest form of autoregression)
pred_seasonal = train["cups"].iloc[-7:].to_numpy()     # (b) Same-day-last-week: captures the 7-day cycle

mae_naive = np.abs(test["cups"].to_numpy() - pred_naive).mean()
mae_seasonal = np.abs(test["cups"].to_numpy() - pred_seasonal).mean()
print(f"Naive (yesterday)  MAE = {mae_naive:.1f} cups")
print(f"Same-day-last-week MAE = {mae_seasonal:.1f} cups  <- captures the weekly 'Saturday spike' -> more accurate!")
```

Running this, you'll see:

```text
Naive (yesterday)  MAE = 23.7 cups
Same-day-last-week MAE = 16.0 cups  <- captures the weekly 'Saturday spike' -> more accurate!
```

**Do you see it?** Simply factoring in the "replays every 7 days" cycle drops the average error from 23.7 cups to 16. That's exactly why a slightly fancier method like **SARIMA** (which automatically picks up on seasonality) so often beats the plain, naive forecast.

### ⚠️ Four Caveats You Must Remember (These Really Matter)

1. **This is weather forecasting, not fortune-telling**: the model assumes "tomorrow ≈ the last few days," so it **breaks down at turning points**—it can't guess which day the outbreak will hit its **peak**, and it can't predict a sudden superspreading event or the sharp drop after "shutting off the water source." It's like the shop owner using "this week" to predict "next week"—a typhoon day will still catch her off guard. **Fine for the short term, but the further out you go, the less accurate it gets.**
2. **An outbreak's "weekend dip" is often fake**: the bubble-tea shop's Saturday spike is **real** (customers genuinely increase); but the weekend drop in outbreak case counts is **often just an illusion caused by "fewer people seeking care, getting tested, and reporting on weekends"**—the virus doesn't take weekends off. This is the **one place the bubble-tea metaphor will trick you**—make sure to remember it.
3. **The rolling average always "lags a beat behind"**: it's an average looking backward at the past, so on the very day things truly spike, the smoothed line is still slowly catching up—**don't rely on it alone to catch a sudden peak**.
4. **An outbreak won't climb forever**: if you stubbornly extrapolate an "always rising" trend out to infinity, you'll end up predicting infinite cases. Real outbreaks eventually **turn the corner and cool off**, because the pool of susceptible people who can still be infected runs low—which is exactly why we keep a close eye on whether the rolling-average line's "head is starting to droop."

> 📏 One more practical reminder: the nursing home's data spans only **17 days**—too short to pick up an "every 7 days" cycle (SARIMA needs at least 2 full cycles). That's exactly why Part B of this chapter switches to **90 days of synthetic influenza-like data** to demonstrate seasonal forecasting—**you can't work out "monthly patterns" when the shop's only been open a week**.

### Cheat Sheet for Reading the Chart (Save This)

| What you see... | What it means |
|---|---|
| Daily numbers jumping up and down (sawtooth) | Raw noise—don't panic over a single day |
| 7-day rolling average line | The **real trend** after smoothing out the sawtooth |
| The smoothed line's head tilts upward | Still growing (the outbreak is still burning -> prep more beds fast) |
| The smoothed line's head droops downward | Cooling off (you can breathe a little easier) |
| Highs and lows repeating at a fixed interval | Seasonality (s=7 = weekly) |
| "Using yesterday, the day before to predict today" | Autoregression (lag features) |
| Hiding the last few days to test against | Train/test split (guards against cheating) |
| Smaller MAE | Less average forecasting error (more accurate) |
| Model loses accuracy at peaks and sharp drops | Normal! Models can't tell fortunes—turning points are always the hardest |

### Back to Reality: Pearls -> Cases

Now swap the bubble-tea shop for the nursing home:

| Bubble-tea shop owner | Real nursing home case |
|---|---|
| How many cups sold each day | Daily **symptom onset** count (daily case count) |
| Sawtooth pattern from weekend spikes | Noise in the daily numbers (but the weekend dip might be a reporting effect!) |
| 7-day rolling average | The epidemic curve's 7-day average, for spotting the trend |
| "Busy yesterday, probably busy today too" | Autoregression (Part A: Poisson + lag) |
| "Always slammed every Saturday" | Seasonality (Part B: SARIMA, s=7) |
| Cover last week, forecast, then check the answer | Train/test split + MAE |
| How many pearls to prep, how many staff to schedule | How many hospital beds and how much staff to prepare |

Every move you just helped the owner learn—rolling average, autoregression, seasonality, train/test—**is exactly what Part A and Part B of this chapter do with the outbreak data**. Now scroll down and look at that big showdown between seven models—doesn't it suddenly feel a lot friendlier? 😉

---

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

<!-- video: ch07_01_ts_basics -->
<!-- /video -->

## Method Overview

```{figure} images/timeseries_method_map_en.svg
:name: fig-timeseries-method-map
:alt: Comparison of seven time series forecasting methods — rolling mean, Poisson+lag, Negative Binomial, Logistic, ARIMA, SARIMA, Prophet
:width: 100%

**Map of time series forecasting methods**: seven models laid out from simple to complex — the full-width green card at the bottom is **Prophet** (the easy, modern option). Less data → further left; need to capture seasonality → furthest right. Each card tells you "how many days of data at minimum," "whether it can give confidence intervals," and "which situation it suits."
```

> 📌 The full-width green card at the bottom is that seventh option—**Prophet**: it replaces manual selection of `(p,d,q)(P,D,Q,s)` with three building blocks—**trend + seasonality + holidays**—a tuning-free alternative to SARIMA. **Step 11** walks through it hands-on.

---

## Step 1: Build the Daily Onset Series

This code turns the raw line list into a time series of **daily onset case counts**—the starting point for every model that follows.

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

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `df = pd.read_csv(...)` | Reads in the full line list of 280 residents |
> | `pd.to_datetime(..., errors="coerce")` | Converts date strings to a real date type; `errors="coerce"` turns unparseable dates into `NaT` instead of crashing the whole script |
> | `df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)` | Anything other than "not ill" counts as infected, converted to 1/0 |
> | `cases = df[df["infected"] == 1]` | Keeps only the cases who actually got sick |
> | `cases.groupby("symptom_onset_date").size()` | Groups by onset date and counts → daily case counts |
> | `daily.asfreq("D", fill_value=0)` | **Fills in the dates with no onsets**, setting the missing days to 0 |
>
> 🔑 **`asfreq` is the soul of this step**: `groupby` only produces "dates that had cases"—if a day has zero cases, it simply vanishes. Without `asfreq("D", fill_value=0)` to fill the gaps, the time series would "skip dates," throwing off both the rolling average and ARIMA later on.

## Step 2: Epidemic Curve + Rolling Average Visualization

Here we plot the daily case counts as a bar chart with a 7-day rolling average line on top, so the jagged sawtooth reveals the real underlying trend.

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

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `daily.rolling(window=7, min_periods=1).mean()` | Computes the 7-day rolling average; `min_periods=1` lets it produce a value even at the very start of the series (before 7 days have accumulated), instead of returning `NaN` for that whole stretch |
> | `ax.bar(daily.index, daily.values, ...)` | Plots the daily case counts as bars (the raw sawtooth) |
> | `ax.plot(rolling_7.index, rolling_7.values, ...)` | Overlays the rolling average line (the trend after smoothing out the sawtooth) |
>
> 💡 **Bars + line on the same chart**: the bars show "day-to-day noise," the orange line shows "the overall trend"—look at both together so you don't get spooked (or falsely reassured) by a single day's number.

---

## Part A ── Short-Term Outbreak Forecasting (Nursing Home Data, 17 Days)

### Step 3: Baseline —— Rolling Mean Forecast

Before reaching for a regression model, start with the simplest possible baseline—the **rolling mean**: guess "tomorrow" using the average of the previous w days, and sweep across a few window sizes to find the most accurate one.

<!-- video: ch07_02_rolling_baseline -->
<!-- /video -->

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

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `daily.rolling(window=w).mean()` | Computes the rolling average over the previous w days |
> | `.shift(1)` | **Pushes the prediction forward by one day**: guesses "today" using the average through "yesterday," never using today's own value |
> | `.dropna()` | The first few days of the series can't fill a full window of w days, so those `NaN` rows get dropped |
> | `mean_absolute_error(actual_w, pred_w)` | Computes how far off the predictions are from the actual values (MAE, smaller = more accurate) |
>
> ⚠️ **`shift(1)` cannot be skipped**: using "today's rolling average" to predict "today" is equivalent to peeking at today's answer (data leakage)—the MAE looks unrealistically great, then collapses the moment it's deployed.

Advantages of the rolling mean: **simple, intuitive, usable from day one**. Drawbacks: it's always "the average of the past few days," so it can't predict turning points, has no confidence intervals, and can't incorporate other variables (like floor or day of week).

### Step 4: Lagged Features —— Building "Past k Days" Features for Regression Models

This step doesn't build a model—it just **gives the time series a makeover**: adding a few columns of "case counts from the past few days" to each day, so regression models can actually consume time-series data.

```{figure} images/lag_features_explained_en.svg
:name: fig-lag-features
:alt: Using shift(1) to move past values to today's row, becoming lag_1 / lag_2 features
:width: 100%

**Lag features**: `df["lag_1"] = df["cases"].shift(1)` pushes the whole column down one row, so "yesterday's cases" appears in "today's row." Combined with `lag_2` and `lag_3`, you can **turn a time series into a table that ordinary regression can consume**.
```

<!-- video: ch07_03_lag_features -->
<!-- /video -->

```python
ts = daily.to_frame("cases").reset_index(names="date")
ts["day_idx"] = range(len(ts))       # Day number (trend)
ts["lag_1"] = ts["cases"].shift(1)   # Yesterday's case count
ts["lag_2"] = ts["cases"].shift(2)   # The day before yesterday's case count
ts_model = ts.dropna().reset_index(drop=True)  # Drop the first two rows (NaN)
print(ts_model.head())
print(f"Usable rows: {len(ts_model)}")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `ts = daily.to_frame("cases").reset_index(names="date")` | Converts the Series back into an ordinary table, turning `date` into a normal column |
> | `ts["day_idx"] = range(len(ts))` | Adds a "day number" column so the model can pick up a rising/falling trend over time |
> | `ts["lag_1"] = ts["cases"].shift(1)` | **Pushes the whole column down one row**: today's row now also holds "yesterday's case count" |
> | `ts["lag_2"] = ts["cases"].shift(2)` | Same idea, adding a column for "the day before yesterday's case count" |
> | `ts.dropna()` | The first two days have no "yesterday/day before" to draw on, so those rows are `NaN` and get dropped |
>
> 🧭 **What a lag feature really is**: `shift(1)` simply "moves" a column's data down one row, turning "what happened yesterday" into "a column on today's row"—the time series becomes an ordinary regression table, which is exactly what the models in Steps 5-7 need to consume.

```{note}
Why add lags? Because infection is transmissible—today's case count is highly correlated with yesterday's (autocorrelation). By using "yesterday's value" as a feature, the regression model can learn: "many yesterday, many today" and "a surge yesterday means today might surge again."
```

### Step 5: Poisson Regression + Lag

Count data (daily counts are 0, 1, 2, ...) are naturally suited to the **Poisson** distribution. We use `statsmodels`' GLM to include the lag features + a trend term:

<!-- video: ch07_04_poisson_lag -->
<!-- /video -->

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

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `smf.glm("cases ~ lag_1 + lag_2 + day_idx", data=ts_model, family=sm.families.Poisson())` | Builds a Poisson GLM: explains today's case count using yesterday's and the day before's counts plus a day-trend term |
> | `.fit()` | Actually **estimates the parameters** (runs maximum likelihood estimation) and returns the fitted model object |
> | `model_pois.predict(ts_model)` | Uses the fitted model to compute an "expected case count" for every row |
> | `mean_absolute_error(...)` | Computes the MAE, on the same scale as the rolling-mean baseline for comparison |
> | `np.exp(model_pois.params)` | Converts the log-scale coefficients into the **IRR (incidence rate ratio)**, which is what you can actually interpret in plain terms |
>
> 💡 **Poisson coefficients only make sense after `exp()`**: `coef` is on the log scale and isn't meaningful on its own; `exp(coef)` is the IRR—"for each extra unit, the case count multiplies by this much."

**In plain terms**: `IRR(lag_1) ≈ 1.15` means "for each additional person who fell ill yesterday, today's expected value is 15% higher."

### Step 6: Negative Binomial Regression —— Handling Overdispersion

This step is a "check-up" first—verify whether the data is overdispersed before deciding whether to swap Step 5's Poisson model for a Negative Binomial model that can absorb the extra variance.

```{figure} images/poisson_vs_nb_dispersion_en.svg
:name: fig-poisson-vs-nb
:alt: Poisson assumes variance = mean; Negative Binomial allows overdispersion where variance > mean
:width: 100%

**Poisson's big assumption**: `variance = mean`. But outbreak investigation data often misbehaves—once cluster infection occurs, the variance is far greater than the mean (**overdispersion**). In that case you should switch to **Negative Binomial**, which adds a parameter α specifically to absorb the "extra" variance.
```

<!-- video: ch07_05_negative_binomial -->
<!-- /video -->

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

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `ts_model["cases"].var() / ts_model["cases"].mean()` | Computes the **dispersion ratio**: variance ÷ mean |
> | `family=sm.families.NegativeBinomial(alpha=1.0)` | Switches to the Negative Binomial distribution; `alpha` is the extra parameter that absorbs the "overdispersion" |
> | `model_nb.predict(ts_model)` / `mean_absolute_error(...)` | Same workflow as Step 5: predict, then compute MAE, so the two can be compared directly |
>
> ⚠️ **Only switch models when dispersion > 1.5**: Poisson assumes variance = mean; once the actual variance is far greater than the mean (overdispersion), Poisson's confidence intervals come out too narrow, making you think the results are more certain than they really are.

### Step 7: Logistic Regression —— "Will Tomorrow Be a Peak Day?"

The supervisor's second question is a **yes/no alert**, not a continuous number. The approach: **binarize** each day's case count (above a certain threshold → 1, otherwise → 0), then use logistic regression to predict the probability.

<!-- video: ch07_06_logistic_threshold -->
<!-- /video -->

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

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `ts_model["cases"].quantile(0.75)` | Takes the 75th percentile of the case counts as the "peak day" threshold |
> | `(ts_model["cases"] > threshold).astype(int)` | **Binarizes** the continuous case count: above the threshold = 1 (peak day), otherwise = 0 |
> | `smf.logit("high_day ~ lag_1 + lag_2", data=ts_model).fit(disp=False)` | Uses yesterday's and the day before's case counts to predict "is today a peak day"; `disp=False` just suppresses the optimizer's step-by-step progress messages |
> | `model_logit.predict(ts_model)` | Computes a **probability** (not 0/1), representing how likely "tomorrow is a peak day" is |
> | `(prob > 0.5).astype(int)` | Converts the probability back to 0/1 so accuracy can be computed |
>
> 🔑 **Logistic regression gives you a probability, not a case count**: `predict()` returns a probability between 0 and 1—exactly where a statement like "there's a 72% chance tomorrow exceeds the alert line" comes from.

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

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `trend = np.linspace(3, 7, n_days)` | Builds a slowly rising **trend line** (daily mean climbing from 3 to 7) |
> | `seasonal = 3 * np.sin(2 * np.pi * np.arange(n_days) / 7)` | Uses a sine wave to manufacture **seasonality**: one full cycle every 7 days |
> | `noise = rng.normal(0, 1.2, n_days)` | Adds random noise, simulating the fact that real data is never this "clean" |
> | `np.maximum(0, (trend + seasonal + noise).round())` | Adds the three components together, rounds, and clips negative values to 0 (a case count can't be negative) |
>
> 💡 **This is practice data with a known answer key**: because trend, seasonal, and noise were all specified by us, we already know what to expect—so we can judge for ourselves whether ARIMA / SARIMA actually pick up on the seasonality below. That makes this a great way to verify a model is doing its job.

### Step 9: ARIMA —— AutoRegressive Integrated Moving Average

Before actually fitting an ARIMA model, first run an ADF test to confirm the series is stationary enough, then split off a train/test set to check how accurate the forecast is.

```{figure} images/arima_sarima_decomposition_en.svg
:name: fig-arima-sarima
:alt: A time series can be decomposed into trend + seasonal + residual; ARIMA(p,d,q) is made of three parts, and SARIMA adds a seasonal component
:width: 100%

**ARIMA's three letters**: **AR(p)** looks at the past p days of itself; **I(d)** takes d differences to make the series stationary; **MA(q)** looks at the past q forecast errors. **SARIMA** additionally adds a set of (P, D, Q, s) specifically to capture the seasonal cycle s.
```

<!-- video: ch07_07_arima_sarima -->
<!-- /video -->

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

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `adfuller(synth)` | **ADF stationarity test**: checks whether the series' mean/variance drift over time |
> | `train, test = synth.iloc[:-7], synth.iloc[-7:]` | Splits train/test: the last 7 days are held out as the test set |
> | `ARIMA(train, order=(1, 1, 1))` | Builds the ARIMA model; `order=(p, d, q)` = **(number of autoregressive lags, number of differences, number of moving-average lags)**: `p=1` looks at itself 1 day back, `d=1` differences once to make the series stationary, `q=1` looks at the forecast error from 1 step back |
> | `.fit()` | **Estimates the parameters** using the training set |
> | `model_arima.forecast(steps=7)` | Uses the fitted model to **forecast 7 steps ahead** (matching the held-out test days) |
> | `mean_absolute_error(test.values, forecast_arima.values)` | Lifts the cover on the test set and computes the forecast error |
>
> 🔑 **Remember `(p, d, q)` in plain terms**: `p` = how many days back the autoregression looks at itself, `d` = how many times it differences the series to make it stationary, `q` = how many past forecast errors the moving-average term looks at. These three numbers aren't picked at random—`d` should follow the ADF test result, while `p` and `q` are usually chosen with the ACF/PACF plots or by comparing AIC.

### Step 10: SARIMA —— Adding Seasonality

On top of ARIMA, SARIMA adds a set of seasonal parameters specifically to capture the "repeats every 7 days" cycle, so the forecast follows the rhythm of the day of the week.

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

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))` | `order=(p,d,q)` is the same "regular" autoregression/differencing/moving-average as ARIMA; `seasonal_order=(P,D,Q,s)` is the **seasonal version** of the same trio, with `s=7` meaning a 7-day cycle |
> | `.fit(disp=False)` | Estimates the parameters; `disp=False` keeps the optimizer from flooding the output with progress messages |
> | `model_sarima.forecast(steps=7)` | Forecasts 7 days ahead, using the same test set as ARIMA for comparison |
>
> 🧭 **The four numbers in `seasonal_order`**: `(P, D, Q, s)` are the seasonal autoregressive order, seasonal differencing order, seasonal moving-average order, and the length of the seasonal cycle—`s=7` is what tells the model "every 7 days, look back and compare against the same day of the week again." This is exactly the extra piece SARIMA has over ARIMA, and it's what lets it catch the weekend surge.

**Key observation**: SARIMA's MAE is clearly smaller than ARIMA's, because it captured the 7-day weekly cycle. For data with **no seasonality**, adding SARIMA is actually wasteful (more parameters, prone to overfitting).

---

## Step 11: Prophet —— Meta's "Auto-Decompose" Crystal Ball

Prophet is Meta's open-source forecasting tool. It **automatically decomposes** a series into three additive building blocks—**trend + seasonality + holidays**—needs only two columns (`ds`/`y`), requires almost no tuning, and comes with uncertainty intervals built in.

```{figure} images/prophet_decomposition_en.svg
:name: fig-prophet-decomposition
:alt: Prophet automatically decomposes an observed series into trend plus seasonality plus holidays, and outputs a forecast with an uncertainty interval
:width: 100%

Prophet's core idea: observed = trend + seasonality + holidays, plus an uncertainty interval.
```

```python
import logging
logging.getLogger("cmdstanpy").setLevel(logging.ERROR)  # Silence Stan's noisy logging
from prophet import Prophet

# Prophet only accepts two columns: ds (date) + y (value)
pdf = synth.reset_index()
pdf.columns = ["ds", "y"]
p_train = pdf.iloc[:-7]                    # Same train/test split as before

m = Prophet(weekly_seasonality=True, yearly_seasonality=False,
            daily_seasonality=False, interval_width=0.9)
m.fit(p_train)                             # Auto-detects trend changepoints + fits seasonality

future = m.make_future_dataframe(periods=7)   # Extend 7 days into the future
forecast = m.predict(future)
yhat = forecast["yhat"].iloc[-7:].values
mae_prophet = mean_absolute_error(test.values, yhat)
print(f"Prophet:  MAE={mae_prophet:.3f}  (fitting needs almost no tuning, and comes with an uncertainty interval)")
print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(7).to_string(index=False))

# Visualization: forecast + 90% uncertainty interval
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(train.index[-30:], train.values[-30:], color="#6B6B6B",
        linewidth=1.2, label="Training (last 30 days)")
ax.plot(test.index, test.values, color="#1A1A1A", linewidth=2,
        marker="o", markersize=5, label="Actual")
ax.plot(test.index, yhat, color="#788C5D", linewidth=1.8,
        marker="D", markersize=5, linestyle="--", label=f"Prophet (MAE={mae_prophet:.2f})")
ax.fill_between(test.index, forecast["yhat_lower"].iloc[-7:].values,
                forecast["yhat_upper"].iloc[-7:].values,
                color="#788C5D", alpha=0.2, label="90% uncertainty interval")
ax.set_title("Prophet 7-day forecast (with uncertainty interval)", fontweight="bold")
ax.set_xlabel("Date"); ax.set_ylabel("Daily case count")
ax.legend(loc="upper left"); ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.autofmt_xdate(); plt.tight_layout(); plt.show()
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `logging.getLogger("cmdstanpy").setLevel(logging.ERROR)` | Prophet uses Stan under the hood for Bayesian estimation, which by default prints a flood of training-progress messages; this line silences that noise |
> | `pdf.columns = ["ds", "y"]` | **Prophet only recognizes these two column names**: `ds` (date, datestamp) and `y` (the value to forecast)—only after renaming the columns will it accept the data |
> | `Prophet(weekly_seasonality=True, yearly_seasonality=False, daily_seasonality=False, interval_width=0.9)` | Turns on weekly-seasonality detection (our data's cycle is s=7), turns off the yearly/daily seasonality we don't need; `interval_width=0.9` sets the output to a **90% uncertainty interval** |
> | `m.fit(p_train)` | Feeds in the training data; Prophet automatically decomposes trend + seasonality (it even auto-detects trend changepoints) |
> | `m.make_future_dataframe(periods=7)` | **Appends 7 more days** of blank rows after the existing dates, getting ready for the model to forecast into the future |
> | `m.predict(future)` | For every day, outputs `yhat` (the forecast) plus `yhat_lower` / `yhat_upper` (the lower/upper bounds of the uncertainty interval) |
> | `forecast["yhat"].iloc[-7:]` | Pulls out the forecast for the last 7 days (matching the held-out test set), to compare against the other models on the same scale (MAE) |
>
> 🔑 **`ds`/`y` are Prophet's only rule**: no manual lag features, no choosing `(p,d,q)`—just rename the date column to `ds` and the target column to `y`, and the model handles everything else automatically.

💡 **Not more accurate, but it saves a mountain of tuning effort**: on this series, Prophet gets **MAE ≈ 0.774**, essentially tying **the tuned SARIMA (0.770)**—but SARIMA requires you to choose `(p,d,q)(P,D,Q,s)` yourself and deal with stationarity, while Prophet only needs two columns of data to get started. Prophet's real advantage is **being easy to pick up + automatically capturing seasonality/holidays/changepoints + free uncertainty intervals**, not higher accuracy.

⚠️ **Prophet is not a silver bullet**: it's an **additive model** that assumes the future is a continuation of "the trend and seasonality it has already learned"; it can't catch the nonlinear feedback of an outbreak in full swing (like SEIR transmission dynamics), and it can't learn much from data shorter than roughly 2 cycles either—what it adds to your toolbox is an **honest option**, not a more accurate crystal ball.

---

## Step 12: Model Showdown

This lays out the MAE, minimum data requirement, and whether a confidence interval is available for all seven models in one table, so you can compare them directly.

<!-- video: ch07_08_ts_model_comparison -->
<!-- /video -->

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
    {"model": "⑦ Prophet",                 "dataset": "synth 90d", "MAE": mae_prophet,
     "min data": "~14 days", "captures seasonality": "Strong (auto)", "confidence interval": "Yes"},
])
print(comparison.to_string(index=False))
```

> 💡 **The point of this table isn't the numbers themselves—it's the "min data" and "captures seasonality" columns**: don't force SARIMA onto data that's too short, and don't reach for it just to show off when there's no seasonality to capture.

**Conclusions in plain terms**:
- **Only one or two weeks of data** (outbreak just started) → Rolling mean or Poisson + lag is enough
- **Clear overdispersion** (cluster, sudden outbreak) → switch to Negative Binomial
- **Need a yes/no alert** (whether to escalate the response level) → Logistic regression
- **Medium-to-long-term surveillance** (> a month, no obvious cycle) → ARIMA
- **Influenza-like, weekly surveillance** (obvious weekly cycle) → SARIMA
- **Want to get started fast, and want trend/seasonality/holidays auto-decomposed + uncertainty intervals** → Prophet

## Step 13: Onset vs Hospitalization Curve (Lag Effect)

Here we overlay the onset curve and the hospitalization curve to see how many days the hospitalization peak lags behind the onset peak.

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

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `cases[...].groupby("hospitalization_date").size()` | Groups by hospitalization date and counts → daily hospitalization counts |
> | `pd.date_range(...)` + `hosp_daily.reindex(all_dates, fill_value=0)` | **Aligns** the hospitalization curve to the onset curve's full date range, filling missing dates with 0, so the two lines can be overlaid on the same time axis |
> | `hosp_aligned.idxmax() - daily.idxmax()` | Finds the hospitalization peak date and the onset peak date, and subtracts to get the **day gap (lag)** |
>
> 💡 **Aligning the dates is a prerequisite for overlaying the curves**: without `reindex` to fill the gaps, the two curves' date ranges might not line up, and the resulting lag would be distorted.

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
8. **Assuming Prophet is always more accurate than ARIMA/SARIMA**: its strength is being easy to use and automated—its accuracy is on par with a well-tuned SARIMA, not inherently higher

## Next Step

Once you know "when" the outbreak is most severe, the next question is "where" it's most severe? → Ch08 Spatial Epidemiology.

## Notebooks

- Class notes: {ref}`07_time_series_baseline.ipynb`
- Exercise version: [`07_time_series_exercise.ipynb`](exercises/07_time_series_exercise.ipynb)
- Solution version (instructor): [`07_time_series_solution.ipynb`](solutions/07_time_series_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/07_time_series_solution.ipynb>)
