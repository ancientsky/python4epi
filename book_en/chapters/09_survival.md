# 09 Survival Analysis: After Onset, Whose Prognosis Is Worse?

## What You'll Learn

- The core ideas of survival analysis: **survival time**, **censored data**, **hazard (instantaneous risk)**, and the **proportional hazards assumption**
- How to draw survival curves with the **Kaplan-Meier method**, and how to truly read the steps and ticks on the curve
- How to compare two survival curves with the **log-rank test**, and interpret the p-value correctly
- How to analyze the effect of multiple factors on survival with **Cox proportional hazards regression**, and read the `print_summary()` table column by column
- How to interpret the **hazard ratio (HR)** and draw an HR forest plot
- How to verify the **proportional hazards assumption** with `cph.check_assumptions()`, and what to do when it's violated

## The Scenario

The Legionella outbreak at Songbai Nursing Home has entered its third week.
Of the 121 infected residents, 19 have sadly died, and the rest survived.

You need to answer the attending physician's questions:
> "After onset, which residents had a higher risk of death? Age? Comorbidities? Severity?"
> "Is there a way to quantify the effect of these factors?"

This is the core task of **survival analysis**—not just looking at "whether someone died," but at "how quickly they died" and "what factors accelerate death."

---

## 🔋 Super Simple Special: Understanding Survival Analysis with a "Phone Battery Contest"

> Does survival analysis sound scary? Don't worry. In this section we're going to swap every scary term for something you use every single day: your **phone battery**. Read this first, then go back and look at the charts below—you'll go "oh, THAT'S what this means!"

### A phone battery contest

Imagine everyone in class brings a fully charged (100%) phone to a contest: **whoever's phone lasts the longest before it dies wins.**

- Survival analysis doesn't just care about "will it die" (every phone eventually will)—it cares about **"how long did it last before dying?"** That's exactly what makes it powerful: **it looks not just at whether something happens, but at "how long until" it happens.**
- The phone dying (battery hits zero) = the "**event**" we're waiting for. In a hospital, the event might be "death," "recovery and discharge," or "relapse."
- The number of hours from 100% to shutdown = **survival time**.

### The single most important trick: some phones are "still on when class ends"

Halfway through the contest, the bell rings and you have to go home—but some phones are **still on**. How do you record that?

- Write "0 hours"? Nope, it clearly lasted a while.
- Write "broken / no data"? Also wrong, it's working perfectly fine.
- The correct answer: **"This phone lasted at least 12 hours, but I don't know exactly how much longer it would have gone."**

This kind of data—where you only know a lower bound and never saw the ending—is called **censoring (censored data)**.

> 🔑 Remember it in one line: **Censored ≠ dead, and ≠ broken. It means "we only saw half the story."** The clever part of survival analysis is that it can still use these phones in the calculation instead of just throwing them away.

```{figure} images/km_battery_metaphor_en.svg
:name: fig-km-battery
:alt: Phone battery metaphor for the Kaplan-Meier curve: of 8 phones, 6 die at different times while 2 are still on when class ends (censored), matched to a survival curve that steps downward, plus the median survival time
:width: 100%

Top row: 8 phones. Bottom row: a staircase heading downward—**every time a phone dies, the staircase drops one step.**
```

### The KM curve: a line that "walks down stairs"

Put time on the x-axis and "**the percentage of phones still on right now**" on the y-axis. It starts at 100% (everyone's phone is on), and every time one phone dies, the line **drops one step**—which is why the Kaplan-Meier curve looks like a **staircase heading downward**:

- **The steeper the staircase** = phones are dying one after another very quickly (**poor survival**).
- **The flatter the staircase** = phones last a long time (**good survival**).
- The moment **the line crosses 50%** is called the **median survival time**—"half the phones have died by this point."
- Small tick marks or "+" symbols on the line = **censored** phones (you collected them at that moment), so the line does **not** step down there.

### Comparing two brands: the log-rank test

Split the phones into "Apple brand" and "Banana brand," and draw a staircase for each:

- If Banana brand's staircase **stays below** Apple brand's the whole time (dropping faster), that means Banana brand phones don't last as long.
- But could that gap **just be luck**? The **log-rank test** asks exactly that: **"Is the gap between these two staircases real, or just chance?"** It gives you a **p-value**, and **p < 0.05** roughly means "this gap is unlikely to be just luck."

### "Battery drain speed": hazard and the hazard ratio (HR)

**Hazard** sounds scary, but it's really just **"how fast the battery is draining right this instant"**—how quickly the phone is losing charge right now. Divide one brand's drain speed by the other's, and you get the **hazard ratio (HR)**:

- **HR = 2**: Banana brand's battery **drains twice as fast** (twice the risk).
- **HR = 1**: both brands drain at the same speed (no difference).
- **HR = 0.5**: Banana brand **only drains at half the speed** (it lasts longer—it's a **protective factor**).

Reading an **HR forest plot** works the same way: a dot **to the right of 1** = higher risk; **to the left of 1** = lower risk (protective). The horizontal line through the dot is the **confidence interval (CI)**—if that line **doesn't touch 1**, the difference is real.

### Try it yourself: draw a KM curve for a battery contest

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

rng = np.random.default_rng(7)

# 40 phones per brand, simulating "hours until the battery dies"
apple = rng.gamma(shape=9, scale=1.1, size=40)    # Apple brand: longer lasting
banana = rng.gamma(shape=5, scale=1.1, size=40)   # Banana brand: drains faster

# We only observe until hour 12, then "class ends" -> anything past that is censored (still on)
CUTOFF = 12
def make(times, brand):
    return pd.DataFrame({
        "brand": brand,
        "hours": np.minimum(times, CUTOFF),
        "died": (times <= CUTOFF).astype(int),   # 1=died (event), 0=censored
    })
phones = pd.concat([make(apple, "Apple brand"), make(banana, "Banana brand")], ignore_index=True)

fig, ax = plt.subplots(figsize=(7, 4.5))
kmf = KaplanMeierFitter()
for brand, color in [("Apple brand", "#6A9BCC"), ("Banana brand", "#D97757")]:
    g = phones[phones["brand"] == brand]
    kmf.fit(g["hours"], g["died"], label=brand)
    kmf.plot_survival_function(ax=ax, color=color)
    print(f"{brand} median survival (time when half have died): {kmf.median_survival_time_:.1f} hours")

ax.axhline(0.5, ls="--", color="#6B6B6B", lw=1)   # 50% reference line -> median survival
ax.set_xlabel("Time (hours)")
ax.set_ylabel("Proportion of phones still on")
ax.set_title("Phone Battery Contest: Kaplan-Meier Survival Curve")
plt.tight_layout()
plt.show()

# Is the gap between brands real, or just luck? -> log-rank test
a = phones[phones.brand == "Apple brand"]
b = phones[phones.brand == "Banana brand"]
res = logrank_test(a["hours"], b["hours"], a["died"], b["died"])
verdict = "the gap is real (p < 0.05)" if res.p_value < 0.05 else "no significant difference detected"
print(f"Log-rank p-value = {res.p_value:.4f} -> {verdict}")
```

Go ahead and run it: Apple brand's median survival is roughly double Banana brand's, and the log-rank p-value is tiny—**the two brands really are different**. Congratulations, you've just done a complete survival analysis!

### Cheat sheet for reading the chart (save this)

| What you see... | What it means |
|---|---|
| KM staircase is steep | Events happen fast (poor survival) |
| KM staircase is flat | Lasts a long time (good survival) |
| Two lines are far apart | The two groups are very different |
| Two lines stick together | The two groups are about the same |
| Line crosses 50% | Median survival time |
| Small tick mark (+) on the line | Censored: we only saw half the story |
| p < 0.05 | The gap is unlikely to be just luck |
| HR > 1 (dot to the right of 1) | Higher risk (drains faster) |
| HR < 1 (dot to the left of 1) | Protective effect (lasts longer) |
| Confidence interval doesn't touch 1 | This difference is real |

### Back to reality: phones → patients

Swap "phone" for "patient," "died" for "death," and "brand" for "disease severity"—and every trick you just learned is exactly what Steps 2–6 of this chapter are doing. Now go back and look at those KM curves, the log-rank test, and the HR forest plot again—doesn't it all make a lot more sense now? 😉

---

## Core Concepts

### Survival Time

Imagine placing a **stopwatch** beside each infected resident:

- **Press start** = the starting point of the event (date of symptom onset)
- **Press stop** = the outcome occurs (death), or observation ends
- The seconds in between are the `time_to_event`

In this case: `time_to_event = death_date − symptom_onset_date` (for those who died) or `investigation_end − symptom_onset_date` (for those still alive).

### Censored Data

For some people, the stopwatch is still running when the race ends—this is called being **censored**.

Here's an analogy: you want to compare "which of two running routes makes people give up more easily," but you can only observe for 30 minutes.
Some runners give up at 10 minutes (event observed), while others are still going at 30 minutes without giving up (**censored**)—you only know they "lasted at least 30 minutes," not whether they would eventually give up.

```{figure} images/survival_censoring_timeline_en.svg
:name: fig-survival-censoring-timeline
:alt: Follow-up timelines for six patients showing three outcomes: death, censoring, and loss to follow-up
:width: 100%

Censoring is not a missing value—every censored case carries the information "observed for at least this long," which KM and Cox correctly incorporate.
```

In this chapter:
- **Those who died**: `event = 1`, `time_to_event` runs until the date of death
- **Those who survived**: `event = 0` (**right-censored**), `time_to_event` runs until the investigation end date
- **Those lost to follow-up**: also `event = 0` (right-censored, but with a shorter time)

⚠️ **Common mistake**: treating a survivor's time as 0, or just dropping them—the former underestimates survival time, the latter wastes important information.

### Hazard and Hazard Ratio (HR)

- **Hazard h(t)** = "the **instantaneous rate at which someone still alive right now experiences the event in the next instant**"
  - In plain words: "for someone who has made it to day t, the immediate risk of dying on day t"
  - The unit is "events per unit time"—think of it as the "heartbeat speed of the event"
- **Hazard ratio (HR)** = the ratio of two groups' hazards
  - `HR > 1` → the exposed group "dies faster" (a risk factor)
  - `HR < 1` → the exposed group "dies slower" (a protective factor)
  - `HR = 1` → the two groups have the same speed (no association)

```{figure} images/hazard_ratio_intuition_en.svg
:name: fig-hazard-ratio-intuition
:alt: A comparison of RR, OR, and HR, plus a visual explanation of the proportional hazards assumption
:width: 100%

HR is a "ratio of rates," not a "ratio of probabilities." It considers both "who dies" and "how fast they die"—this is the biggest difference from RR and OR.
```

> **Remember it in one line**:
> - **RR / OR**: look at "whether it happened" (no time involved)
> - **HR**: look at "how fast it happened" (includes time + handles censoring)

### The Proportional Hazards (PH) Assumption

Cox regression has a key assumption: **the ratio of hazards between the two groups stays constant throughout the entire follow-up period**.

- ✓ Holds: the exposed group is "consistently" 1.5 times faster than the unexposed group from start to finish
- ✗ Violated: the exposed group is much faster in the first two weeks, but becomes slower in the last two weeks (e.g., a treatment that is harmful early and beneficial later)

Visually, when PH holds, the two **log(-log(S(t)))** curves will be roughly **parallel**; when it's violated they will **cross** (the right-hand figure).

⚠️ This assumption matters—if it's violated, the Cox HR becomes an "average effect" rather than the true effect. Step 7 will teach you how to verify it.

---

## The Method Map

```{figure} images/survival_method_map_en.svg
:name: fig-survival-method-map
:alt: The four steps of survival analysis: KM description, log-rank inference, Cox regression, and PH assumption diagnosis
:width: 100%

Survival analysis is four things: **describe → infer → regress → diagnose**. Steps 2-6 of this chapter cover the first three; Step 7 adds the diagnosis.
```

---

## Step 1 — Build the Analysis Dataset

Survival data is different from an ordinary table: it needs **three things**—how **long** each person was observed (time), whether an **event happened** in the end (event, 1/0), and who is **censored** (observation ended before the event). This Step turns the raw line list into those three columns.

```python
import pandas as pd

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["symptom_onset_date"] = pd.to_datetime(df["symptom_onset_date"])
df["death_date"] = pd.to_datetime(df["death_date"])
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

cases = df[df["infected"] == 1].copy()

# Event indicator: 1=died, 0=survived (censored)
cases["event"] = (cases["outcome"] == "dead").astype(int)

# Survival time
investigation_end = cases["symptom_onset_date"].max() + pd.Timedelta(days=14)
cases["end_date"] = cases.apply(
    lambda r: r["death_date"] if r["event"] == 1 else investigation_end, axis=1
)
cases["time_to_event"] = (cases["end_date"] - cases["symptom_onset_date"]).dt.days
```

> **Line-by-line** (this is the most important preprocessing in the whole chapter—read it slowly):
>
> | This line | What it does |
> |---|---|
> | `pd.to_datetime(...)` | Turns date strings into a real "date type" so we can subtract them to get a number of days (subtracting strings directly raises an error) |
> | `df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)` | Boolean `True/False` → `1/0`; anything other than `not_ill` counts as infected |
> | `cases = df[df["infected"] == 1].copy()` | Survival analysis only looks at people who **actually got sick**; `.copy()` lets us edit columns later without the `SettingWithCopyWarning` |
> | `cases["event"] = (cases["outcome"] == "dead").astype(int)` | **Event flag**: death=1, survived=0 (censored). The second of the three things |
> | `investigation_end = ...max() + Timedelta(days=14)` | People who didn't die still need an "observed until when" cutoff; take the last onset date plus 14 days |
> | `cases.apply(lambda r: death_date if event==1 else cutoff, axis=1)` | Each person's stopwatch **stop time**: the death date if they died, the cutoff if they survived |
> | `(end_date - onset).dt.days` | stop − start = **survival time** (days). The first of the three things, done |

> **Key point**: for survivors, `time_to_event` uses "the last onset date + 14 days" as the observation cutoff—meaning "we observed at least this long and saw no death." This value is **not** 0, and it is **not** missing.

## Step 2 — Kaplan-Meier Survival Curve for Everyone

First, one curve for **everyone**: feed the `time_to_event` and `event` we just built to `KaplanMeierFitter`, and it draws that "going-downstairs" survival curve.

```python
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

# -- CJK font setup (avoids Chinese labels showing as boxes) --
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
plt.style.use("ggplot")
plt.rcParams["figure.dpi"] = 150

kmf = KaplanMeierFitter()
kmf.fit(cases["time_to_event"], event_observed=cases["event"],
        label="All")
kmf.plot_survival_function()
plt.title("Kaplan-Meier Survival Curve (all infected residents)")
plt.xlabel("Days since onset")
plt.ylabel("Survival probability")
plt.show()
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `plt.rcParams["font.sans-serif"] = [...]` | A **font-fallback template** (kept identical across editions) so any CJK characters render instead of boxes (□□□) |
> | `kmf = KaplanMeierFitter()` | Build a "KM estimator machine," waiting to be fed data |
> | `kmf.fit(cases["time_to_event"], event_observed=cases["event"], label="All")` | **Feed just two columns**: how long each person lasted + whether the event happened. Censoring (event=0) is handled automatically by lifelines |
> | `kmf.plot_survival_function()` | Draw the downstairs curve (with the 95% CI shaded band) |
>
> 💡 **KM's magic needs only two columns**: time + event flag. Hand the censored people (`event=0`) to `fit()`, and it lets each of them "count in the denominator up to the last moment, but never make the curve step down"—that is exactly where censoring is correctly included instead of thrown away.

### How to Read a KM Curve

```{figure} images/km_step_function_anatomy_en.svg
:name: fig-km-step-function
:alt: Anatomy of the four key elements of a Kaplan-Meier curve: steps, ticks, median survival time, and the CI band
:width: 100%

Every step and every tick means something—learn this figure, and from now on you'll know exactly what you're looking at in any KM curve.
```

Four steps for reading the curve:

| Element | Meaning | How to read it |
|------|------|--------|
| **Step down** | Someone died on that day | More steps, steeper drops → events are more concentrated |
| **Small vertical tick** | Censoring (still alive / lost to follow-up) | Doesn't change the curve height, but reduces the later risk set |
| **The point crossing y=0.5** | Median survival time | The day when half the people have not yet died; if it never crosses → `median = inf` (good news) |
| **Shaded band (CI)** | 95% confidence interval | Widens at the tail = smaller risk set, more uncertain CI |

> **Clue for this case**: if the median survival time shows `inf`, it means more than half of the infected residents did not die during the observation period (CFR < 50%, which makes sense since 19/121 ≈ 15.7%).

## Step 3 — Survival Curves by Severity Group

One curve for everyone can't reveal "who has the worse prognosis," so we **split into three groups by severity** and draw one curve each, layered on the same figure to compare.

```python
for severity in ["mild", "moderate", "severe"]:
    mask = cases["clinical_severity"] == severity
    kmf.fit(cases.loc[mask, "time_to_event"],
            event_observed=cases.loc[mask, "event"],
            label=severity)
    kmf.plot_survival_function()
plt.title("Survival curves (grouped by severity)")
plt.show()
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `for severity in ["mild", "moderate", "severe"]:` | Draw one curve for each severity |
> | `mask = cases["clinical_severity"] == severity` | A boolean mask selecting the people in "this group" |
> | `kmf.fit(cases.loc[mask, ...], ...)` | Re-fit using only this group's data (reusing the same `kmf` is fine—each `fit` overwrites the previous one) |
> | `plt.show()` is **outside** the loop | All three curves must be drawn on the **same figure** to be comparable |
>
> 🧭 **The key is "the same figure"**: `plot_survival_function()` always draws on the current axes, so three loop iterations stack up three curves. To compare groups, never call `plt.show()` **inside** the loop (that would split it into three figures with one curve each—nothing to compare).

### Three Perspectives for Reading Grouped KM Curves

1. **Point of separation**: when do the two curves start to diverge?
   - The **earlier** they separate → the more immediate the factor's effect (e.g., the effect of severity usually shows up within the first week)
2. **Size of the gap**: the vertical distance between the curves
   - The **larger** the gap → the stronger the effect
3. **Whether they cross**: do the curves cross each other?
   - Crossing → the PH assumption may be violated (interpret Cox results with caution; Step 7 will verify)

> **Expectation for this case**: the `severe` group's curve should drop the **earliest and fastest**; the `mild` group's curve should be nearly flat. If you actually observe `severe` and `moderate` crossing, flag it as "the effect of severity may change over time."

## Step 4 — Log-rank Test

Step 3 used our eyes to see whether two curves separate; Step 4 uses the **Log-rank test** to ask a stricter question: **is this gap real, or just chance?**

```python
from lifelines.statistics import logrank_test

severe = cases[cases["clinical_severity"] == "severe"]
non_severe = cases[cases["clinical_severity"] != "severe"]
result = logrank_test(
    severe["time_to_event"], non_severe["time_to_event"],
    event_observed_A=severe["event"],
    event_observed_B=non_severe["event"],
)
print(f"Log-rank p-value = {result.p_value:.4f}")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `severe = cases[... == "severe"]` / `non_severe = cases[... != "severe"]` | Split people into the **two groups to compare** |
> | `logrank_test(A_time, B_time, event_observed_A=, event_observed_B=)` | Feed **each group's own** times and event flags; returns a result object |
> | `result.p_value` | Pull out the p-value—the answer to "is this gap just chance?" |
>
> ⚠️ **Log-rank needs four things fed in**: both groups' times + both groups' event flags, none optional. It compares the **whole curve**, not one single day—so even if the two medians are equal, a different curve shape can still be significant.

### The Log-rank Test in Plain Words

- **Null hypothesis H₀**: the two groups' survival curves have the **same shape** (the hazard is identical at every time point)
- **Alternative hypothesis H₁**: the two groups' hazards differ at at least one time point
- **Test statistic**: approximately follows a χ²(df=1) distribution
- **p-value**:
  - `p < 0.05` → reject H₀; the two survival curves are **statistically significantly** different
  - `p ≥ 0.05` → cannot reject H₀; insufficient evidence

⚠️ **Important limitation**: the log-rank test **only tells you "whether there's a difference," not "how big the difference is."** To quantify the effect (HR + CI), you must use Cox regression.

> **Analogy**: the log-rank test is like the red "abnormal" flag on a health checkup report—it warns you there's a problem, but doesn't tell you how severe it is. To gauge severity you need a separate test (= Cox regression).

## Step 5 — Cox Proportional Hazards Regression

Log-rank only says "is there a difference"; **Cox regression** goes further and answers "how much," and it can put age, sex, comorbidities, and more into the model **simultaneously**, giving each its own HR (the effect after adjusting for the others).

```python
from lifelines import CoxPHFitter

cox_df = cases[["time_to_event", "event", "age", "sex",
                "comorbidity_copd", "comorbidity_chf",
                "comorbidity_dm", "comorbidity_cancer",
                "immunosuppressed"]].copy()
cox_df["is_male"] = (cox_df["sex"] == "M").astype(int)
cox_df = cox_df.drop(columns=["sex"])

cph = CoxPHFitter()
cph.fit(cox_df, duration_col="time_to_event", event_col="event")
cph.print_summary()
```

> **Line-by-line** (the point is shaping the data into something Cox can eat):
>
> | This line | What it does |
> |---|---|
> | `cox_df = cases[[...]].copy()` | Pick the columns to go into the model: **time + event + each predictor** |
> | `cox_df["is_male"] = (cox_df["sex"] == "M").astype(int)` | Cox only eats numbers, so convert the text category `sex` into a 0/1 `is_male` |
> | `cox_df.drop(columns=["sex"])` | The original text column must be **dropped**—leaving it in makes `fit()` raise an error |
> | `cph.fit(cox_df, duration_col="time_to_event", event_col="event")` | Tell Cox **which column is time and which is the event**; every remaining column is treated as a predictor |
>
> 💡 **Cox's two required arguments**: `duration_col` (time) and `event_col` (event flag). It treats every other column as a factor to estimate an HR for—so `cox_df` **must not smuggle in** irrelevant columns like `case_id` or names, which would be estimated as nonsense factors.

### Reading Every Column of `print_summary()`

`print_summary()` prints a big, intimidating-looking table. Column by column, it's actually simple:

| Column | Meaning | How to read it |
|------|------|--------|
| `coef` | log(HR) | Positive → risk factor; negative → protective factor; 0 → no association |
| `exp(coef)` | **HR** (the most important one) | 1.5 = risk speed is 1.5 times faster; 0.6 = risk speed is only 0.6 times |
| `se(coef)` | Standard error of coef | No need to read directly (the CI below has already done the math for you) |
| `z` | `coef / se` | The test statistic corresponding to the p-value |
| `p` | p-value | `< 0.05` is treated as statistically significant |
| `exp(coef) lower 95%` | Lower bound of the HR's 95% CI | Read together with the upper bound |
| `exp(coef) upper 95%` | Upper bound of the HR's 95% CI | **CI crosses 1 → not significant** |

> **Rule of thumb**: "Just look at `exp(coef)` and its CI"—the HR tells you the direction and strength, the CI tells you the certainty.

### Interpreting Concordance (c-index)

At the very bottom, `print_summary()` prints a `Concordance`, which is the model's **ranking ability**:

| c-index | Interpretation |
|---------|------|
| 0.50 | Equivalent to random guessing (useless) |
| 0.60-0.70 | Fair |
| 0.70-0.80 | Acceptable |
| > 0.80 | Good |

### ⚠️ Sample Size Warning (events per variable, EPV)

This demonstration dataset has only **19 death events**, but we put in **7 variables** (age, is_male, 4 comorbidities, immunosuppressed).

The epidemiological rule of thumb (Peduzzi 1995): **each variable needs at least 10 events**.
- 19 events / 7 variables ≈ 2.7 → far below 10
- This chapter is a **teaching demonstration**; in practice a model like this easily overfits, and the HRs and CIs are unreliable
- In real research, you should do variable selection first (like the Modified Poisson selection in Ch06), keeping at most 1-2 of the most crucial variables

> This is also why many variables in the Cox results look "not significant"—it's not that they're truly unimportant, but that **the sample size isn't large enough to support this many variables**.

## Step 6 — HR Forest Plot

Reading the `print_summary()` table with your eyes is dizzying; a **forest plot** draws each variable's HR and confidence interval as a "dot + horizontal line," so you see at a glance who's risky and who's not significant.

```python
cph.plot()
plt.title("Cox Regression — Hazard Ratio")
plt.show()
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `cph.plot()` | One line draws the **forest plot**: it plots each variable's log(HR) and CI from the Step 5 table as a dot + horizontal line |
>
> 💡 **A forest plot = the graphical version of `print_summary()`**: same numbers, different view. A dot to the right of 0 = risk factor; a horizontal line crossing 0 = not significant—far faster than reading the table column by column.

### How to Read the HR Forest Plot

The forest plot `lifelines` draws uses **log(HR)** as the x-axis by default:

| What to look at | Meaning |
|--------|------|
| **The dashed line at x = 0** | Represents HR = 1 (the reference line for no association) |
| **The position of the dot** | The point estimate log(HR) |
| **The horizontal line** | The 95% confidence interval |
| **Dot to the right of x=0** | log(HR) > 0, i.e. HR > 1 (risk factor) |
| **Dot to the left of x=0** | log(HR) < 0, i.e. HR < 1 (protective factor) |
| **Horizontal line crosses x=0** | 95% CI crosses 1 → not significant |
| **Very long horizontal line** | Wide CI → high uncertainty (usually a variable with few samples) |

> **Reading order**: ① first look at which side of 0 the point is on (direction) → ② see whether the line crosses 0 (significance) → ③ look at the length of the line (certainty).

## Step 7 — Verify the PH Assumption

### Why Check?

If Cox regression's **proportional hazards (PH) assumption** is violated, interpreting the HR becomes unreliable.
Step 5 gives us a pile of HR numbers, but those numbers were computed under the premise that "the hazard ratio between the two groups stays constant throughout"—we need to verify that premise.

### One Line with `check_assumptions()`

```python
# Check the PH assumption (show_plots=False prints text conclusions only, avoiding extra subplots)
results = cph.check_assumptions(cox_df, show_plots=False)
```

> **Line-by-line**: `cph.check_assumptions(cox_df, show_plots=False)` —— using the **same** `cox_df`, it runs a Schoenfeld-residuals test on each variable; `show_plots=False` makes it print only the text conclusion instead of drawing a pile of subplots.

This function will:
1. Run a Schoenfeld residuals test for each variable
2. Print the p-value for each variable
3. List the variables that violate the PH assumption, and **give recommendations**

### How to Interpret the Output?

| Output | Meaning |
|------|------|
| `No violation detected` | ✓ All variables pass; the Cox results are trustworthy |
| `Variable X: p < 0.05` | ✗ Variable X violates PH —— its HR changes over time |
| The output plots (when `show_plots=True`) | The scatter of Schoenfeld residuals over time—a trend = violation |

### Remedies When the Assumption Is Violated

1. **Stratify (strata)**: treat the violating variable as a "stratification variable," allowing its baseline hazard to vary freely
   ```python
   cph.fit(cox_df, duration_col="time_to_event", event_col="event",
           strata=["the violating variable"])
   ```
2. **Add a time-varying coefficient**: let the variable's effect change over time
3. **Switch to an AFT (Accelerated Failure Time) model**: bypass the PH assumption entirely
4. **Split into time periods**: run separate Cox models for "the first two weeks" and "the last two weeks"

> **Note**: when the number of events is small (19 events in this case), the power of `check_assumptions()` is inherently low—even if no violation is detected, it doesn't mean the PH assumption definitely holds. Always pair it with a visual check (do the grouped KM curves cross?).

---

## Exercises

- Exercise version: [`09_survival_exercise.ipynb`](exercises/09_survival_exercise.ipynb)
- Solution version (instructor): [`09_survival_solution.ipynb`](solutions/09_survival_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/09_survival_solution.ipynb>)

## Common Misuses

| Mistake | Correct approach |
|------|---------|
| Using only CFR without survival analysis | CFR ignores time; survival analysis is more precise |
| Simply excluding survivors | Survivors are censored data and must be included in the analysis |
| Ignoring the proportional hazards assumption | Verify it with `cph.check_assumptions()` (Step 7) |
| Interpreting HR as a "probability ratio" | HR is a "**ratio of rates**": the ratio of the instantaneous rate of the event occurring in the next second |
| Treating `hospitalized` as a risk factor | ⚠️ This is **confounding by indication**—people are hospitalized because they are severely ill, not that hospitalization makes them die faster. You must adjust for severity |
| Cramming 10 variables into 19 events | **≥ 10 events per variable** (events per variable rule). When events are few, do variable selection first |
| Ignoring competing causes of death | This case only looks at "death vs survival"; if you care about multiple events at once (e.g., death vs discharge), use **competing risks** (`lifelines.CRCCumulativeIncidenceFitter`) |

## Next Step

Survival analysis tells us "whose prognosis is worse."
In the next chapter (Ch10), we take on a bigger question: **can we use all 32 feature columns to train a machine learning model to predict infection and severe illness?** → Machine learning.
