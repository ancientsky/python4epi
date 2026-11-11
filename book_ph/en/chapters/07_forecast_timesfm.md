---
title: "07 Next month's dengue: forecasting with TimesFM"
description: "Maya forecasts the next eight weeks of dengue: simple baselines first, then the zero-shot time-series foundation model TimesFM 3.0 in an honest rolling-origin backtest, its failure at the outbreak take-off, and what its licence allows."
---

:::{div}
:class: ph-story
*Wednesday 30 September · CESU office, after the data freeze*

**Doc Mon:** The Local Health Board meets on Friday. They will ask three things: how many beds, how many fogging teams, how many NS1 kits for October and November.

**Maya:** So… they want me to predict the future?

**Doc Mon:** No. They want a range they can plan with, and an honest word on how good it is.

**Tala:** I can run a forecasting model that has learned from a huge collection of time series!

**Doc Mon:** Wonderful. First show me it beats copying last year.

> How many dengue cases should Santa Luz plan for in the next eight weeks — and how far can we trust the number?
:::

## What a forecast is for

In a health office, a forecast is a **planning tool**, not a prophecy. It turns "dengue is
high" into "plan for roughly 20 to 60 cases a week in early October, falling after that",
so the hospital can open beds, the city can schedule 4S and fogging teams, and the
pharmacy can order test kits. A good forecast comes with **three things**: a number, a
range, and a track record.

## Baselines first

A **baseline** is the simplest forecast a tired DSO could make on paper. Any model must
beat it, or it is not worth the trouble.

- **Last value:** next week = this week, repeated.
- **Seasonal naive:** next weeks = the same weeks last year.

To judge them fairly we use a **rolling-origin backtest**: we pretend to stand at a past
week (the **origin**), forecast the next 8 weeks using only what was known then, and only
afterwards compare with what happened. We do that every second week from 2023-W01 to
2026-W31: **94 forecasts**. The score is the **mean absolute error** (MAE): the average
size of the miss, in cases per week.

:::{admonition} Ask Tala
:class: ph-ask-tala
I have a NumPy array `y` of weekly dengue counts in time order (made-up example:
`[5, 9, 11, 4, ...]`, more than 52 weeks long). For a forecast made at row `o` (we know
`y[:o]` only) I want the next `H = 8` weeks from two baselines: "last value" (repeat
`y[o-1]`) and "seasonal naive" (copy `y[o-52 : o-52+8]`). Do it for a list of origins and
give me the MAE against the true values. Add a check I can do by hand.
:::

:::{admonition} Tala says
:class: ph-tala-says
```python
H = 8                                             # forecast horizon: 8 weeks
first, last = row_of["2023-W01"], row_of["2026-W39"] + 1
origins = list(range(first, last - H + 1, 2))     # every 2nd week; each forecast ends by 2026-W39
actual = np.stack([y[o:o + H] for o in origins])  # shape (94, 8): what really happened

last_value = np.stack([np.repeat(y[o - 1], H) for o in origins])
seasonal_naive = np.stack([y[o - 52:o - 52 + H] for o in origins])  # no ISO week 53 after 2020
```
:::

:::{admonition} Check it
:class: ph-check
1. Pick one origin and look: does "last value" really repeat the week *before* the origin?
   Does "seasonal naive" copy the same ISO weeks one year earlier?
2. Every history must stop at its origin: `len(context) == o`. If a forecast can see the
   weeks it is forecasting, its score means nothing.
:::

## A zero-shot foundation model: TimesFM 3.0

**TimesFM** is a **time-series foundation model** from Google. It was trained once on a
very large collection of time series. We use it **zero-shot**: no training on our data,
just "here is the history, give me the next 8 weeks". It returns a median forecast and
nine **quantiles**; the 0.1 and 0.9 quantiles bound an **80% prediction interval**, the
range that should contain the truth about 8 times out of 10.

The notebook shows the genuine calls, which run on Google Colab after
`pip install "timesfm[torch]"` (the weights, about 1.3 GB, download once):

```python
from timesfm3 import ModelConfig, TimesFM3Evaluator

config = ModelConfig(
    checkpoint_path="google/timesfm-3.0-pytorch",  # weights on Hugging Face (~1.3 GB, first run only)
    per_core_batch_size=32,                        # series per forward pass
    device=tsfm.default_device(),                  # "cuda" on a GPU runtime, else "cpu"
)
model = TimesFM3Evaluator(config)
```

```python
contexts = tsfm.rolling_origin_contexts(y, origins)
bt = tsfm.forecast_batch(model, contexts, H, cache_key="backtest_cases", cache_file=CACHE)
```

`tsfm.forecast_batch` (from this book's `epi_learning` package) calls
`model.predict_batch(...)` when the model is loaded. When this website is built, the
model is not downloaded; the helper replays forecasts saved from a real TimesFM 3.0 run
of the same notebook, and every cell prints which path it took.

## The scoreboard

| Period | Last value | Seasonal naive | TimesFM 3.0 | 80% band covered |
|---|---:|---:|---:|---:|
| Ordinary years 2023–2025 (75 forecasts) | 4.76 | 4.31 | **3.50** | 79% |
| 2026, the typhoon year (19 forecasts) | 6.22 | **5.21** | 5.32 | 72% |

*MAE in cases per week, averaged over the 8 weeks ahead.*

In ordinary years TimesFM is clearly the best, and its 80% band is honest. In 2026 it is
**no better than copying last year**. It is the best method for next week (MAE 1.97) but
falls behind by week 8 (10.08 against 8.68 for seasonal naive). One overall average would
have hidden this. **Always score the unusual period on its own.**

:::{admonition} Tala got it wrong
:class: ph-oops
Maya asked for "a better baseline: the average of the same week in all years". Tala's
version scored an MAE of **3.27** over all 94 forecasts, better than TimesFM's 3.86 on the
same forecasts. Doc Mon asked one question:
*"Which years went into that average?"* All of them, **including the weeks being
forecast**. That is **leakage**: the forecast had seen the answer. Averaging only the
three years *before* each origin gives **3.95**, slightly worse than TimesFM's 3.86.

The quieter trick is to report only the **best** week. TimesFM's best origin had an MAE of
0.54; its worst (2026-W31) 31.50. The honest number is the average over all of them, 3.86.

How to catch both: ask *"could this forecast have been made on that day?"* and report
the average over every origin, plus the worst one.
:::

## When the outbreak takes off

The weeks that matter most are the ones where the curve turns. Given the history up to
2026-W31, TimesFM forecast about **10 cases a week**. The next four weeks brought
**33, 28, 48 and 34**. Not one of the following eight weeks fell inside its 80% band.
From W32 the band covered 29% of the weeks; only from W34, when the surge was already
in the history, did it cover them all.

The model is not broken. It only knows what dengue curves *usually* do next. It cannot
know that a typhoon flooded the city three weeks earlier.

**Would rainfall help?** In this synthetic series, rain leads cases by about 7 weeks,
and TimesFM 3.0 accepts rainfall as a **covariate**. With rainfall the backtest MAE
barely moved (3.50 → 3.47 in 2023–2025, 5.32 → 5.27 in 2026), and from W31 the forecast
stayed at about 9–12 cases a week, even though Amihan's rain, the wettest week in the series, was already in the
history. A covariate is only useful if you prove it in the same backtest.

:::{div}
:class: ph-game ph-game-forecast-guess
Judge a forecast against simple baselines, report its error and uncertainty, and say
when something the model could not see has changed.
:::

## The forecast for October and November

From all the data up to 2026-W39, TimesFM's median falls from **42 cases in W40 (80%
interval 24–63)** to **16 in W47 (6–44)**. The weekly medians add up to 215 cases for the
eight weeks; the same eight weeks of 2025 had 75.

:::{admonition} Check it
:class: ph-check
1. **Is the last week complete?** No: W39 (45 cases) is still being reported (see
   [chapter 06](06_signals_and_thresholds.md)). From the data up to W38, the model
   expected 53 cases in W39. Leaving W39 out raises the W40 forecast from 42 to 46.
   When the latest week moves the forecast, say so.
2. **Is the band wide?** Yes, and it should be: 6 to 44 cases in W47 is an honest "we
   don't know exactly".
3. **Compare with a baseline.** Seasonal naive says 75 cases in 8 weeks. That is what a
   normal autumn looks like, not this one.
:::

What Maya writes for the Board: *"Plan for roughly 20 to 60 dengue cases a week in early
October, likely falling through November. We will update this every week; a new
typhoon or a rise in severe cases would change it."*

:::{admonition} The licence, in plain words
:class: warning
TimesFM's **code** is Apache-2.0. The **TimesFM 3.0 weights** are under the **TimesFM
Non-Commercial License v1.0**: research, evaluation and teaching, **no commercial and no
production use** ([licence on Hugging Face](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE)).
The older **TimesFM 2.5** weights are Apache-2.0
([model card](https://huggingface.co/google/timesfm-2.5-200m-pytorch)), and Google points to
TimesFM in BigQuery (Google Cloud) for official support
([TimesFM on GitHub](https://github.com/google-research/timesfm)).

For a government health office this means: learning, exploring and backtesting old data —
like this chapter — fits. Using 3.0 forecasts in a routine early-warning system or a public
bulletin does not. **Check the licence, and your office's rules, before any operational
use.** This is not legal advice.
:::

:::{admonition} Privacy stop
:class: ph-privacy
A forecast needs only **weekly counts**, never the line list. Weekly totals for a whole
city are aggregate data. Even so, run the model in your notebook, and don't paste your
office's surveillance tables into an AI chat. Ask Tala with made-up numbers, as above.
:::

:::{div}
:class: ph-game ph-game-quiz
**Quick check: forecasting**

1. A new model has an MAE of 5.3 in 2026. Is it good?
   - Yes, 5.3 is small — small compared with what?
   - ✓ Only if it beats the baselines on the same weeks — seasonal naive scored 5.2 here.
2. Tala's same-week average scored 3.27, better than TimesFM. What went wrong?
   - ✓ Leakage — the average included the very weeks being forecast.
   - Nothing — simple methods are often best, but this one had seen the answer.
3. Why did TimesFM miss the take-off after W31?
   - It needs more training — it is zero-shot; training is not the issue.
   - ✓ It only knows how curves usually continue; it could not see the typhoon's effect coming.
4. Can a city health office put TimesFM 3.0 weights into its routine early-warning system?
   - Yes, the code is open source — the code is Apache-2.0, but the 3.0 weights are not.
   - ✓ Not under the 3.0 weights' non-commercial, non-production licence — check the licence first.
:::

:::{admonition} Baon
:class: ph-baon
- Baselines first: a model must beat "last value" and "same weeks last year" in a fair
  rolling-origin backtest, scored separately for the unusual period.
- Never let a forecast see the answer, and report the average over all origins, not the
  best week.
- A forecast is a range for planning. It cannot see a typhoon or unreported cases — and
  check the licence before operational use.

Open the notebook: [](notebooks/07_forecast_timesfm.ipynb)
:::
