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

```{figure} images/survival_censoring_timeline.svg
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

```{figure} images/hazard_ratio_intuition.svg
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

```{figure} images/survival_method_map.svg
:name: fig-survival-method-map
:alt: The four steps of survival analysis: KM description, log-rank inference, Cox regression, and PH assumption diagnosis
:width: 100%

Survival analysis is four things: **describe → infer → regress → diagnose**. Steps 2-6 of this chapter cover the first three; Step 7 adds the diagnosis.
```

---

## Step 1 — Build the Analysis Dataset

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

> **Key point**: for survivors, `time_to_event` uses "the last onset date + 14 days" as the observation cutoff—meaning "we observed at least this long and saw no death." This value is **not** 0, and it is **not** missing.

## Step 2 — Kaplan-Meier Survival Curve for Everyone

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

### How to Read a KM Curve

```{figure} images/km_step_function_anatomy.svg
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

### Three Perspectives for Reading Grouped KM Curves

1. **Point of separation**: when do the two curves start to diverge?
   - The **earlier** they separate → the more immediate the factor's effect (e.g., the effect of severity usually shows up within the first week)
2. **Size of the gap**: the vertical distance between the curves
   - The **larger** the gap → the stronger the effect
3. **Whether they cross**: do the curves cross each other?
   - Crossing → the PH assumption may be violated (interpret Cox results with caution; Step 7 will verify)

> **Expectation for this case**: the `severe` group's curve should drop the **earliest and fastest**; the `mild` group's curve should be nearly flat. If you actually observe `severe` and `moderate` crossing, flag it as "the effect of severity may change over time."

## Step 4 — Log-rank Test

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

```python
cph.plot()
plt.title("Cox Regression — Hazard Ratio")
plt.show()
```

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
