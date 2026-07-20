# 06 Multivariable Analysis: Adjusted Risk Ratios and Logistic Regression

## The Scenario

The stratified analysis in Ch05 told us that functional status really is a confounder of shower use. But at the investigation meeting, the infection-control nurse pressed on:

> "After we account for age, all the comorbidities, functional status, and floor all at once, is shower use **still** a significant risk factor?"

Stratified analysis can only control one variable at a time. To **adjust for several factors simultaneously**, we need a regression model.

> 🔑 **Key recap**: Ch03 framed this investigation as a **retrospective cohort study**, with the effect measure being the **RR (risk ratio)**. The stratified analysis in Ch05 also computed an **MH adjusted RR**. To keep using the same yardstick throughout, the main method in this chapter will be **Modified Poisson regression**—which directly yields an **adjusted RR**. We'll also run logistic regression as a comparison, so you can see how much the OR overestimates the effect on the very same data.

## What You'll Learn

- Modified Poisson regression (Zou 2004) to adjust for multiple factors at once and compute an adjusted RR
- The logic behind logistic regression—understanding the "probability → odds → log(odds)" three-step ladder in plain language
- How the OR overestimates the effect in a high-attack-rate cohort study (compared against the actual RR values)
- Comparing crude RR → MH adjusted RR (Ch05) → adjusted RR → adjusted OR
- Presenting the results in the standard epidemiological Table 2 format
- Model diagnostics (AIC) and variable selection

## 🎯 Super Simple Special: Understanding Multivariable Analysis with "Does Cram School Really Work?"

> "Multivariable analysis," "adjusted OR," "odds ratio" sound like grown-up territory? Don't be scared. This section sets the nursing home aside for a moment and uses a question **you and your friends have argued about since you were kids**—**"Does cram school actually work?"**—to walk through the whole idea in a way that'll make even a 7th grader get it instantly. Once you're done, go back and look at the regression table below—you'll suddenly find every number is telling this exact same story!

### An argument that never ends: does cram school really make you smarter?

Someone surveys a bunch of middle schoolers and finds:

> **Among kids who go to cram school, 64% score 80 or above. Among kids who don't, only 29% do.**

If you jumped straight to a conclusion—**"Cram school doubles your chance of a high score, sign up now!"**—you might have fallen into the same "big feet" trap as Ch05. Because...

> 🤔 **Kids who go to cram school usually already have more books at home, and their parents already care more about studying.** In other words, there's a "family background" factor that **simultaneously** makes a kid "more likely to go to cram school" and "more likely to score high anyway."

That "family background" is a **confounder** lurking behind the scenes—playing the exact same role that "age" played in the big-feet story.

### But this time it's different: cram school might have "a little bit of real effect"

In Ch05, once we stratified the big-feet story, the RR dropped all the way from 2.1 down to **1.0**—foot size turned out to have **zero effect at all**, a pure illusion. Cram school is a bit different: **it might really have a small genuine effect, just wildly "inflated" by family background.** What we want to ask is:

> **After "subtracting out" family background, how much real credit does cram school get to keep on its own?**

This is where **multivariable analysis** comes in.

### Key intuition #1: the parallel-universe twin

How do you "subtract out" family background? Picture this:

> 👯 **You have an identical twin in a parallel universe**—just as smart, with just as many books at home, with parents who feel the same way about studying—**the only difference is "they went to cram school and you didn't."** So do they score higher than you? By how much? **That "extra score"—that's cram school's real, honest contribution.**

That's exactly what multivariable regression does: mathematically, it "**pretends everything else is equal**," letting only the cram-school variable differ, and calculates cram school's effect **by itself**. This is called "**holding others constant**."

### Key intuition #2: why do you have to put everything "together" in one model?

You might ask: why not just analyze each variable one at a time, separately?

> 🕵️ **The interrogation room metaphor**: question suspects one at a time, separately, and each one will take credit for everyone else's work ("it was all me!"). But **lock all the suspects in the same interrogation room and confront them together**, and you can finally squeeze out how much each one **actually** did. A multivariable model is that interrogation room—it throws cram school, family background, age, comorbidities... all into the **same** model at once, so each factor's effect is its net contribution "**after subtracting out everyone else**."

This is exactly where multivariable analysis beats the stratified analysis from Ch05: **stratifying can only control one variable at a time, while regression can control a whole bunch at once.**

```{figure} images/cram_school_multivariable_en.svg
:name: fig-cram-school-multivariable
:alt: Multivariable analysis of cram school: looking at cram school alone, the cram-school group scores high 64% of the time versus 29% for the no-cram-school group (crude OR≈4.3), but the real culprit is family background (books at home); once cram school and books at home are put into the regression model together, cram school's OR shrinks from 4.3 to 1.5, meaning cram school's own effect is much smaller
:width: 100%

Top left: looking at cram school alone, it looks super effective (crude OR 4.3); top right: the real culprit "family background" drives both cram school attendance and high scores; bottom: once both are put into the model together, cram school's OR **shrinks to 1.5**—not zero, "shrunk but still alive."
```

### While we're at it: odds and the odds ratio (OR)

The number that comes out of a regression is called an **OR (odds ratio)**, not an RR. What's "odds"? The fastest way to think about it is betting odds:

> 🎲 **Probability** is "6 out of 30 people are infected" = 6/30 = 20%.
> **Odds** is "the 6 infected **against** the 24 not infected" = 6:24 = 0.25, like the **betting odds** on a scoreboard.
> The **odds ratio (OR)** is just the two groups' odds **divided by each other**. A cram-school OR of 4.3 means: "the **betting odds** of 'scoring high' for the cram-school group are 4.3 times those of the no-cram-school group."

### Try it yourself: calculate cram school's "real skill" with your own two hands

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(42)
n = 800

# For each student: number of books at home (in tens), whether they go to cram school, whether they score 80+
# Books at home is an "upstream" factor: more books -> more likely to go to cram school AND more likely to score high anyway (a true confounder)
home_books = rng.normal(10, 3, n).clip(2, 20)
p_cram = 1 / (1 + np.exp(-(home_books - 10) / 2))   # kids with more books at home are more likely to go to cram school
cram = rng.binomial(1, p_cram)
# Scoring high: mostly driven by family background; cram school "itself" only adds a little (true effect OR = e^0.4 ~= 1.5)
p_high = 1 / (1 + np.exp(-(-6 + 0.55 * home_books + 0.4 * cram)))
high_score = rng.binomial(1, p_high)

students = pd.DataFrame({"cram": cram, "home_books": home_books, "high_score": high_score})

# (1) Cram school alone (univariate): how far apart are the two groups' high-score rates?
r1 = students.loc[students.cram == 1, "high_score"].mean()
r0 = students.loc[students.cram == 0, "high_score"].mean()
print(f"Cram group high-score {r1:.0%}, no-cram {r0:.0%}")

# Crude OR: the model only includes "cram"
crude = smf.logit("high_score ~ cram", data=students).fit(disp=0)
print(f"Crude OR (cram only)               = {np.exp(crude.params['cram']):.2f}")

# (2) Multivariable: put "cram + books at home" into the same model together (that interrogation room)
adj = smf.logit("high_score ~ cram + home_books", data=students).fit(disp=0)
print(f"Adjusted OR (cram + books at home) = {np.exp(adj.params['cram']):.2f}")
```

Running this, you'll see:

```text
Cram group high-score 64%, no-cram 29%
Crude OR (cram only)               = 4.33
Adjusted OR (cram + books at home) = 1.51
```

> 💡 **Here's the "aha" moment**: more than half of cram school's glow was actually borrowed from "already having more books at home"—peel that glow away layer by layer, and the OR drops from **4.3 to 1.5**. Most of the credit belonged to someone else, but **the remaining 1.5 is cram school's own, honest earning**.

### ⚠️ Three caveats you must remember

1. **Adjusting doesn't always make the number smaller**: this time cram school shrank from 4.3 to 1.5, but adjusting can also make a number **bigger**, or even **flip its direction**. The point isn't "it always shrinks"—it's that "**as soon as adjusting changes the number, that proves there was confounding**."
2. **A model can only expose the suspects you actually bring into the interrogation room**: any factor you didn't think of and didn't put into the model (say, "whether the kid got enough sleep") is still running free outside—this is called **residual confounding**. So the adjusted number is only the best estimate "**given what's currently known**," not an ironclad guarantee of causation.
3. **OR is not "how many times the probability"**: OR = 4.3 means 4.3 times the **odds**, not 4.3 times the **risk**. And **the more common the disease, the more OR exaggerates the number**—our outbreak has an attack rate as high as 43% (very common!), which is exactly why this chapter's **main method is Modified Poisson**, which computes the honest **RR (risk ratio)** directly, instead of the OR, which tends to overestimate.

### Cheat sheet for reading the numbers (save this)

| What you see... | What it means |
|---|---|
| An OR/RR computed from just one variable | The **crude** value—possibly inflated by a confounder |
| A model with a bunch of variables in it | **Multivariable**: each coefficient is the net effect "holding the other factors constant" |
| Crude OR 4.3 → adjusted OR 1.5 | Shrunk but not zeroed out: part borrowed glow, part real skill |
| The number changes after adjusting (bigger/smaller/flips) | A confounder is at work |
| The number barely changes after adjusting | That variable probably isn't an important confounder |
| OR (from logistic regression) | How many times the **odds**—overestimates risk when the attack rate is high |
| RR (from Modified Poisson) | How many times the **risk**—the go-to, more honest choice for cohort studies |
| exp(coefficient) | Turns the regression coefficient β back into an OR or RR ($e^\beta$) |

### Back to reality: cram school → shower use

Now swap the characters in the story for the nursing home version:

| Cram school story | Real nursing home case |
|---|---|
| Whether the kid goes to cram school (exposure) | Whether the resident used the **shower** (`shower_use`) |
| Scoring high (outcome) | Whether infected with Legionnaires' disease |
| Family background / books at home (confounder) | **Age, comorbidities, functional status** (`age`, `comorbidity_*`, `functional_status`) |
| The parallel-universe twin | A regression coefficient = the effect "holding the other factors constant" |
| Locked in the interrogation room together | A multivariable model, adjusting several factors at once |
| Cram school's "betting odds" multiplier | Odds ratio OR (logistic regression) |
| Cram school's "number of kids who scored high" multiplier | Risk ratio RR (Modified Poisson, this chapter's main method) |

Every trick you just learned from the cram-school story—crude vs. adjusted, the twin intuition, the interrogation room, OR vs. RR—**is exactly what Steps 2–5 of this chapter do with the nursing home data**. Now scroll down and look at those regression tables and Table 2 again—doesn't it suddenly feel a lot friendlier? 😉

---

## Core Concepts

### Why do we keep talking about RR?

Ch03 already explained it: in a cohort study we can directly compute "risk" (risk = number of cases ÷ total number of people), so the effect measure should be the **RR**. Only in a case-control study—where risk cannot be computed—do we fall back on the **OR**.

> ⚠️ In this investigation the attack rate is as high as **43%**. Ch03 already warned: when a disease is not rare, the OR will **systematically overestimate** the effect. If you tell your supervisor "the OR for shower use is 3.5," they'll think the risk is 3.5 times higher—but the true risk ratio (RR) might only be about 2.0. That's a big difference!

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Why use RR instead of OR?</div>
  <div class="youtube-lite" data-id="PrbPC5cAyxM">
    <img src="https://img.youtube.com/vi/PrbPC5cAyxM/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

### Two routes to multivariable analysis

```{figure} images/multivariate_methods_en.svg
:name: fig-multivariate-methods
:alt: A comparison of three methods for controlling confounders: stratified analysis (Ch05), Modified Poisson (the main method of Ch06), and logistic regression (the Ch06 comparison)
:width: 100%

Stratified analysis can only control one factor at a time; both Modified Poisson and logistic regression can control several at once, but the former outputs an RR and the latter an OR.
```

| Method | Output | Suitable for cohort studies? | When to use |
|------|------|--------------|---------|
| Stratified analysis (Ch05) | MH adjusted RR | Yes, but only 1 factor at a time | Few confounders (1–2) |
| **Modified Poisson** (this chapter's main method) | **adjusted RR** | **First choice** | Cohort study + multiple confounders |
| Logistic regression (this chapter's comparison) | adjusted OR | Overestimates at high attack rates | Case-control studies, rare diseases |

### Modified Poisson: a Poisson shell holding an RR soul

> 🎩 **The "borrowed hat" metaphor**: Poisson regression was originally designed for "count data" (e.g., how many new cases per day). But the epidemiologist Zou (2004) discovered a clever trick: throw a binary outcome (0/1) into a Poisson regression, then correct the standard errors with a **robust sandwich variance**—and the resulting coefficient turns out to be exactly **log(RR)**! It's like borrowing a hat from a friend: the size isn't quite right, but slap on a correction sticker and it fits perfectly.

Why does this work? The three-sentence version:

1. Poisson regression models **log(E[Y])**; when Y is 0/1, E[Y] = P(Y=1) = risk, so the coefficient = **log(risk ratio)**
2. But the Poisson model assumes variance = mean, which is wrong for binary data → the standard errors are off
3. The **robust (sandwich) SE** doesn't rely on the distributional assumption; it estimates the variance directly from the data → this fixes the bias above → the CI and p-value are both correct

> 💡 Why not use **log-binomial** (Binomial + log link)? In theory it's the most "correct," but in practice it often fails to converge (convergence failure), especially when the exposure and outcome are strongly associated. Modified Poisson almost never has convergence problems.
>
> Why not use **Cox regression** (proportional hazards)? Cox requires "time-to-event" data, whereas ours is a binary outcome (infected / not infected) with no differences in follow-up time.

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Modified Poisson—the borrowed-hat magic for computing RR</div>
  <div class="youtube-lite" data-id="A_KHcLHITN0">
    <img src="https://img.youtube.com/vi/A_KHcLHITN0/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

### Logistic regression in plain language

Although Modified Poisson is the first choice for this investigation, logistic regression remains one of the most widely used multivariable analysis methods in the world. Understanding how it works is essential knowledge for an epidemiologist.

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: The logistic regression three-step ladder—probability → odds → logit</div>
  <div class="youtube-lite" data-id="o-bRxWzK_xo">
    <img src="https://img.youtube.com/vi/o-bRxWzK_xo/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```{figure} images/logit_intuition_en.svg
:name: fig-logit-intuition
:alt: The three-step ladder of logistic regression: probability (0–1) → odds (0–∞) → log(odds) (−∞ to +∞)
:width: 100%

The three steps for "straightening out" a probability: a stuck spring → a balance scale → a straightened line.
```

**Step 1: probability**—the squashed spring

The infection probability $p$ is stuck between 0 and 1. The output of a linear regression can be any number ($-\infty$ to $+\infty$), but a probability can't—you can't say someone's infection probability is -0.3 or 1.5. It's like stuffing a spring into a small box: the closer to the edges, the more cramped it gets, so you can't run a linear regression directly.

**Step 2: odds**—the balance scale

$$\text{odds} = \frac{p}{1-p}$$

> ⚖️ **The balance-scale metaphor**: if the infection probability is $p = 0.70$, the odds = $0.70 / 0.30 = 2.33$. This means that on the scale, the "will be infected" side is 2.33 times heavier than the "won't be infected" side. Odds range from 0 to $+\infty$: the right side is freed, but the left side is still stuck at 0.

**Step 3: log(odds) = logit**—the straightened spring

$$\text{logit}(p) = \log\left(\frac{p}{1-p}\right)$$

After taking the log, the range becomes $-\infty$ to $+\infty$—both sides are free! Linear regression can finally work properly.

The logistic regression model is simply:

$$\text{logit}(p) = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots$$

**How do we interpret $\beta$?** Suppose the $\beta_1$ for shower use is 0.50:

- $\text{OR} = e^{0.50} = 1.65$
- In plain language: "after controlling for other factors, residents who used the shower have **odds** of infection that are **1.65 times** those of non-users"
- Note: this is "how many times the **odds**," not "how many times the **risk**"! At a high attack rate the two differ substantially

---

## Step 1: Data Preparation

This step loads the raw line list and does two things: it turns categorical columns into numbers the regression can use (binary or ordered), and computes the attack rate as an early clue for whether to trust the RR or the OR later on.

```python
# === Step 1: Load the data + recode variables ===

import pandas as pd
import numpy as np
import statsmodels.api as sm               # GLM (Modified Poisson)
import statsmodels.formula.api as smf       # formula API (logistic)
import matplotlib.pyplot as plt
import warnings

# --- Load the Legionnaires' disease cluster data ---
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# --- Build the binary outcome variable ---
# clinical_severity != "not_ill" means infected (includes mild/moderate/severe)
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# --- smoking_history three categories → two categories ---
# never / former / current → anything that isn't never counts as ever_smoker
df["ever_smoker"] = (df["smoking_history"] != "never").astype(int)

# --- Convert functional status to an ordered numeric score ---
# bedridden=0 < assisted=1 < independent=2
fs_map = {"bedridden": 0, "assisted": 1, "independent": 2}
df["functional_score"] = df["functional_status"].map(fs_map)

# --- Quick check of the attack rate ---
ar = df["infected"].mean()
print(f"Attack rate = {ar:.1%} ({df['infected'].sum()}/{len(df)})")
print(f"→ An attack rate of {ar:.0%} is far above 10%, so the OR will markedly overestimate the effect; rely on RR")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `import statsmodels.api as sm` and `import statsmodels.formula.api as smf` | Two different interfaces: `sm` is used later with `family=` to specify a GLM by hand (needed for Modified Poisson), while `smf` provides the `"y ~ x"` formula syntax (needed for logistic regression) |
> | `df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)` | Converts boolean `True`/`False` to `1`/`0`, building the **binary outcome variable** the regression needs |
> | `df["ever_smoker"] = (df["smoking_history"] != "never").astype(int)` | Collapses the three categories never/former/current into two, reducing the model's degrees of freedom |
> | `fs_map = {...}`, `df["functional_score"] = df["functional_status"].map(fs_map)` | Uses `.map()` to turn the text categories (bedridden/assisted/independent) into an **ordered number** (0/1/2) so the regression can treat it as continuous |
> | `ar = df["infected"].mean()` | `infected` only holds 0 and 1, so its mean is the "proportion of 1s"—that's the attack rate, a handy pandas trick |
>
> 💡 **Key point**: the attack rate Step 1 computes (43%) is far above the 10% "rare disease" threshold—that's exactly why this chapter's main method is **Modified Poisson for RR**, with logistic regression only as a comparison.

## Step 2: Univariable Analysis—Crude RR vs Crude OR

This step loops over each candidate factor and fits both Modified Poisson (for the crude RR) and logistic regression (for the crude OR), lining up the two effect measures in a single table so you can see, up front, how far apart RR and OR are for a single factor.

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Univariable crude RR vs OR—compare them all in one for loop</div>
  <div class="youtube-lite" data-id="LBf3HvGOLAA">
    <img src="https://img.youtube.com/vi/LBf3HvGOLAA/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
# === Step 2: Univariable analysis loop ===
# Run Modified Poisson (for crude RR) and logistic (for crude OR) at the same time,
# so you can see how much the RR and OR differ for the same variable.

from epi_learning.metrics import risk_ratio  # the 2×2 hand-computed RR from Ch03

factors = [
    "shower_use", "hydrotherapy_use", "ever_smoker",
    "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed",
    "age", "functional_score",
]

crude_results = []

for var in factors:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        # --- (A) Modified Poisson → crude RR ---
        try:
            mod_p = smf.glm(
                f"infected ~ {var}", data=df,
                family=sm.families.Poisson(),   # borrow the Poisson shell
            ).fit(cov_type="HC0", disp=0)       # robust SE correction
            rr = np.exp(mod_p.params[var])       # exp(β) = RR
            rr_ci = np.exp(mod_p.conf_int().loc[var])
            rr_p = mod_p.pvalues[var]
        except Exception:
            continue

        # --- (B) Logistic Regression → crude OR ---
        try:
            mod_l = smf.logit(
                f"infected ~ {var}", data=df,
            ).fit(disp=0, method="lbfgs")
            if not mod_l.mle_retvals["converged"]:
                print(f"⚠ {var}: logistic did not converge, skipping")
                continue
            or_val = np.exp(mod_l.params[var])    # exp(β) = OR
            or_ci = np.exp(mod_l.conf_int().loc[var])
            or_p = mod_l.pvalues[var]
        except Exception:
            continue

    # --- (C) 2×2 hand-computed RR for cross-validation (binary variables only) ---
    hand_rr = ""
    if df[var].dropna().isin([0, 1]).all():
        a = ((df[var] == 1) & (df["infected"] == 1)).sum()
        b = ((df[var] == 1) & (df["infected"] == 0)).sum()
        c = ((df[var] == 0) & (df["infected"] == 1)).sum()
        d = ((df[var] == 0) & (df["infected"] == 0)).sum()
        hand_rr = f"{risk_ratio(a, a+b, c, c+d):.3f}"

    crude_results.append({
        "variable": var,
        "crude_RR": round(rr, 3),
        "RR 95% CI": f"{rr_ci[0]:.3f}–{rr_ci[1]:.3f}",
        "crude_OR": round(or_val, 3),
        "OR 95% CI": f"{or_ci[0]:.3f}–{or_ci[1]:.3f}",
        "hand_RR": hand_rr,
    })

crude_df = pd.DataFrame(crude_results)
print("=== Crude RR vs Crude OR (univariable) ===")
print(crude_df.to_string(index=False))
print()
print("💡 Note: crude_OR is generally larger than crude_RR — this is the OR overestimation at high attack rates")
print("   The hand_RR column is the 2×2 hand-computed result from Ch03; it should match crude_RR almost exactly")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `for var in factors:` | Loops through the candidate factors, fitting one univariable model per variable |
> | `smf.glm(f"infected ~ {var}", data=df, family=sm.families.Poisson()).fit(cov_type="HC0", disp=0)` | **Modified Poisson**: a Poisson-family GLM with robust SEs (`cov_type="HC0"`)—the chapter's standard way to compute an RR |
> | `rr = np.exp(mod_p.params[var])` | The Poisson model's coefficient is log(RR); `exp()` converts it back to the crude RR |
> | `smf.logit(f"infected ~ {var}", data=df).fit(disp=0, method="lbfgs")` | The same variable, refit as logistic regression (Binomial family + logit link) |
> | `or_val = np.exp(mod_l.params[var])` | The logistic model's coefficient is log(OR); `exp()` converts it back to the crude OR |
> | `if df[var].dropna().isin([0, 1]).all(): ...` | For binary variables only, cross-checks against the Ch03 2x2-table hand calculation to confirm the model's RR isn't off |
>
> ⚠️ **Key point**: `cov_type="HC0"` isn't optional—the Poisson model assumes variance = mean, which is wrong for a binary (0/1) outcome. Without the robust SE, the confidence intervals and p-values would both be wrong.

### Reading the formula syntax

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: A quick guide to statsmodels formula syntax</div>
  <div class="youtube-lite" data-id="G-cJPHaz7ag">
    <img src="https://img.youtube.com/vi/G-cJPHaz7ag/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

statsmodels borrows the **formula syntax** from the R language, letting you describe "which variables predict the outcome" in a single line:

| Symbol | Meaning | Example |
|------|------|------|
| `~` | "is predicted by" | `infected ~ age` → use age to predict infected |
| `+` | "plus" | `~ age + sex` → put both age and sex into the model |
| `C()` | "treat as categorical" | `C(floor)` → split floor into dummy variables (dummy coding), one 0/1 indicator per floor |

In plain language, `infected ~ shower_use + age + C(floor)` says "use shower use, age, and floor to predict infection." The model automatically adds an intercept term (Intercept), so you don't need to write it.

### Which variables go into the model?—starting from the Ch03 and Ch05 results

A multivariable model isn't about throwing in every column; there needs to be a reason for each one. Reviewing the findings from earlier chapters, we split the model variables into four groups:

| Group | Variables | Role | Reason for inclusion |
|------|------|------|----------|
| **Exposure factors** | `shower_use`, `hydrotherapy_use` | Study focus | The significant risk factors screened in Ch03—the question we most want to answer: "are the shower and hydrotherapy the source of infection?" |
| **Host factors** | `age`, `immunosuppressed`, `functional_score` | Potential confounders | `age` = a factor epidemiology routinely adjusts for; `immunosuppressed` = one of the factors with the highest crude RR in Ch03; `functional_score` = the confounder already confirmed in Ch05 |
| **Comorbidities** | `comorbidity_chf`, `comorbidity_dm`, `comorbidity_cancer`, `comorbidity_copd` | Potential confounders | The candidate factors screened in Ch03, put into the full model to see whether the exposure factors' RR changes after adjustment |
| **Location** | `C(floor)` | Potential confounder | Different floors may have different plumbing systems or exposure opportunities, so we need to control for floor differences |

```{tip}
**Why not include `ever_smoker`?** In the Ch03 univariable screening, smoking had a crude RR close to 1 and did not reach statistical significance. On top of that, it is highly correlated with several comorbidities (collinearity), so including it in the model would only increase the instability of the estimates. That's why we leave it out of the multivariable model.
```

## Step 3: Multivariable Modified Poisson—Adjusted RR

This step is the chapter's main analysis: it puts every exposure factor and potential confounder into a single Modified Poisson model at once, directly producing the adjusted RR.

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Multivariable adjusted RR—building a beautiful Table 2</div>
  <div class="youtube-lite" data-id="XIfx82VxVaA">
    <img src="https://img.youtube.com/vi/XIfx82VxVaA/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
# === Step 3: Modified Poisson — adjust for all factors at once ===
# This is the main analysis of the chapter: a Poisson GLM + robust SE to compute the adjusted RR.
# coefficient = log(RR), so exp() gives the RR.

# --- Formula explanation ---
# infected ~ : use the variables on the right to predict "infected or not"
# shower_use + hydrotherapy_use : exposure factors (study focus)
# age + immunosuppressed + functional_score : host factors (potential confounders)
# comorbidity_chf/dm/cancer/copd : comorbidities (potential confounders)
# C(floor) : floor as a categorical variable (control for location differences)
formula = (
    "infected ~ shower_use + hydrotherapy_use + age + "
    "comorbidity_chf + comorbidity_dm + comorbidity_cancer + "
    "comorbidity_copd + immunosuppressed + functional_score + "
    "C(floor)"     # C(floor) = treat floor as a categorical variable (dummy coding)
)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model_poisson = smf.glm(
        formula, data=df,
        family=sm.families.Poisson(),   # the Poisson shell
    ).fit(cov_type="HC0")               # robust (sandwich) SE

# --- Format into Table 2 layout ---
adj_rr_results = []
for var in model_poisson.params.index:
    if var == "Intercept":
        continue
    coef = model_poisson.params[var]
    ci = model_poisson.conf_int().loc[var]
    adj_rr_results.append({
        "variable": var,
        "adjusted_RR": round(np.exp(coef), 3),        # exp(β) = adjusted RR
        "95% CI": f"{np.exp(ci[0]):.3f}–{np.exp(ci[1]):.3f}",
        "p-value": round(model_poisson.pvalues[var], 4),
    })

adj_rr_df = pd.DataFrame(adj_rr_results)
print("=== Adjusted RR (Modified Poisson, Table 2) ===")
print(adj_rr_df.to_string(index=False))
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `formula = "infected ~ shower_use + ... + C(floor)"` | Puts the exposure factors, host factors, comorbidities, and floor into the **same** formula, so every coefficient is the effect "holding the other variables constant" |
> | `smf.glm(formula, data=df, family=sm.families.Poisson())` | Builds the **Modified Poisson** model: the outcome is the binary `infected`, but it's fit with a Poisson-family shell—the outcome is not a count, it's binary |
> | `.fit(cov_type="HC0")` | Corrects the standard errors with a **robust (sandwich) SE**, because the Poisson assumption variance = mean does not hold for binary data; with the correction the CI and p-value are valid |
> | `coef = model_poisson.params[var]` | Pulls out that variable's coefficient, which is **log(adjusted RR)** |
> | `np.exp(coef)` | `exp()` converts log(RR) back into the **adjusted RR** (not an adjusted OR) |
> | `model_poisson.conf_int().loc[var]` | Pulls out the coefficient's 95% CI (still on the log scale); it also needs `exp()` before it can sit alongside the RR |
>
> 🔑 **Key point**: this is a "Poisson shell with an RR soul"—the outcome really is binary (infected or not), but fitting it with a Poisson family plus robust SE means `exp(coef)` reads out as an honest **adjusted RR**, not an OR.

## Step 4: Multivariable Logistic Regression—Adjusted OR (the comparison)

This step reuses the exact same formula, swapping only the family for logistic regression, to compute the adjusted OR so it can be compared directly against Step 3's adjusted RR.

```python
# === Step 4: Logistic Regression — same formula, switch to logistic ===
# Goal: let you see how much the OR and RR differ for the same covariates.

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model_logit = smf.logit(formula, data=df).fit(disp=0, method="lbfgs")

# --- Format into Table 2 layout ---
adj_or_results = []
for var in model_logit.params.index:
    if var == "Intercept":
        continue
    coef = model_logit.params[var]
    ci = model_logit.conf_int().loc[var]
    adj_or_results.append({
        "variable": var,
        "adjusted_OR": round(np.exp(coef), 3),         # exp(β) = adjusted OR
        "95% CI": f"{np.exp(ci[0]):.3f}–{np.exp(ci[1]):.3f}",
        "p-value": round(model_logit.pvalues[var], 4),
    })

adj_or_df = pd.DataFrame(adj_or_results)
print("=== Adjusted OR (Logistic Regression, Table 2) ===")
print(adj_or_df.to_string(index=False))
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `smf.logit(formula, data=df)` | Uses **the exact same formula** as Step 3 (identical variables), but this time as logistic regression (Binomial family + logit link) |
> | `.fit(disp=0, method="lbfgs")` | `disp=0` suppresses the iteration log; `method="lbfgs"` switches to a solver that converges more reliably than the default on this data |
> | `coef = model_logit.params[var]` | Pulls out that variable's coefficient, which is **log(adjusted OR)** |
> | `np.exp(coef)` | `exp()` converts it back into the **adjusted OR** |
>
> 💡 **Key point**: the only difference between Step 3 and Step 4 is the `family` (Poisson vs. logistic)—the formula is identical, which is exactly what lets you cleanly see how far apart RR and OR are on the same data.

```{admonition} Why do some variables "fail to converge"?
:class: tip, dropdown

When one category of a binary predictor corresponds completely (or almost completely) to a particular outcome, this is called **complete separation** or **quasi-complete separation**. In that case the maximum likelihood estimate (MLE) of the OR tends toward 0 or ∞, the Hessian matrix cannot be inverted, and the model fails to converge.

Common ways to handle it:
1. Check the 2×2 table to see whether any cell = 0
2. Switch to **Firth's penalized likelihood** (the `firthlogist` package)
3. Switch to **Exact logistic regression**
4. In a teaching setting, skip that variable for now and include it in the multivariable model instead
```

## Step 5: Comparing the Three Effect Measures Side by Side

This step lines up the crude RR from Step 2, the adjusted RR from Step 3, and the adjusted OR from Step 4 into one merged table, so you can see both the confounding effect (crude to adjusted) and the OR's overestimation (adjusted RR to OR) in a single view.

```python
# === Step 5: Crude RR vs Adjusted RR vs Adjusted OR side by side ===
# This is the most important table in the chapter: see all three effect measures at once.

key_vars = ["shower_use", "hydrotherapy_use", "age",
            "comorbidity_chf", "immunosuppressed", "functional_score"]

comparison = []
for var in key_vars:
    # Get crude RR from crude_df
    c_row = crude_df[crude_df["variable"] == var]
    if len(c_row) == 0:
        continue
    c_rr = c_row.iloc[0]["crude_RR"]

    # Get adjusted RR from adj_rr_df
    a_rr_row = adj_rr_df[adj_rr_df["variable"] == var]
    if len(a_rr_row) == 0:
        continue
    a_rr = a_rr_row.iloc[0]["adjusted_RR"]

    # Get adjusted OR from adj_or_df
    a_or_row = adj_or_df[adj_or_df["variable"] == var]
    if len(a_or_row) == 0:
        continue
    a_or = a_or_row.iloc[0]["adjusted_OR"]

    # Compute the magnitude of change
    rr_change = ((a_rr - c_rr) / c_rr * 100) if c_rr != 0 else 0
    or_vs_rr = ((a_or - a_rr) / a_rr * 100) if a_rr != 0 else 0

    comparison.append({
        "variable": var,
        "crude_RR": c_rr,
        "adj_RR": a_rr,           # Modified Poisson
        "adj_OR": a_or,           # Logistic
        "crude→adj RR": f"{rr_change:+.1f}%",    # confounding effect
        "adj RR→OR": f"{or_vs_rr:+.1f}%",        # magnitude of OR overestimation
    })

comp_df = pd.DataFrame(comparison)
print("=== Crude RR → Adjusted RR → Adjusted OR comparison ===")
print(comp_df.to_string(index=False))
print()
print("📊 Interpretation:")
print("  • crude→adj RR column: the change in RR after controlling for confounders (compare with the Ch05 MH conclusion)")
print("  • adj RR→OR column: how much the OR overestimates relative to the RR in the same model (attack-rate effect)")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `c_row = crude_df[crude_df["variable"] == var]` | Pulls this variable's crude RR out of the Step 2 table |
> | `a_rr_row = adj_rr_df[adj_rr_df["variable"] == var]` | Pulls this variable's adjusted RR out of the Step 3 table |
> | `a_or_row = adj_or_df[adj_or_df["variable"] == var]` | Pulls this variable's adjusted OR out of the Step 4 table |
> | `rr_change = ((a_rr - c_rr) / c_rr * 100)` | How many % the RR changed from crude to adjusted—quantifying the size of **confounding** (echoing the Ch05 logic) |
> | `or_vs_rr = ((a_or - a_rr) / a_rr * 100)` | For the same variable, how many % the adjusted OR overestimates the adjusted RR by—quantifying how much the **OR is inflated at a high attack rate** |
>
> 🧭 **Key point**: this table stitches together the results of three separately fitted models—the `crude→adj RR` column answers "was there confounding," and the `adj RR→OR` column answers "how much did the OR overestimate." Don't mix up the two questions.

```{admonition} When is OR ≈ RR?
:class: note

Only when the **disease is rare** (prevalence < 10%) does $(1-p) \approx 1$, so odds $\approx$ risk and OR $\approx$ RR. In this investigation the attack rate is 43%, so the OR will systematically **inflate** the effect. That's why, when reporting results from a cohort study, you should use the RR rather than the OR.

If you're reading someone else's paper and see them analyze a **cohort study** with logistic regression for a disease that isn't rare, watch for whether they used Modified Poisson or at least mentioned the issue that OR ≠ RR.
```

## Step 6: Forest Plot (Adjusted RR)

This step turns Step 3's adjusted RR table into a forest plot, trading a wall of numbers for point estimates and confidence-interval bars you can read at a glance.

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: The adjusted RR forest plot—spot the real risk factors at a glance</div>
  <div class="youtube-lite" data-id="7GgpIOKr_CY">
    <img src="https://img.youtube.com/vi/7GgpIOKr_CY/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
# === Step 6: Forest Plot — present the adjusted RR graphically ===
# A standard epidemiological forest plot: dot = point estimate, horizontal line = 95% CI, dashed line = RR=1 (no effect)

# Prepare the plotting data (exclude Intercept and the floor dummies)
plot_vars = [r for r in adj_rr_df["variable"] if not r.startswith("C(floor)")]
plot_data = adj_rr_df[adj_rr_df["variable"].isin(plot_vars)].copy()

# Recover the numeric values from the CI string
plot_data["ci_lo"] = plot_data["95% CI"].str.split("–").str[0].astype(float)
plot_data["ci_hi"] = plot_data["95% CI"].str.split("–").str[1].astype(float)

fig, ax = plt.subplots(figsize=(8, 5))

y_pos = range(len(plot_data))
ax.errorbar(
    plot_data["adjusted_RR"], y_pos,
    xerr=[plot_data["adjusted_RR"] - plot_data["ci_lo"],
          plot_data["ci_hi"] - plot_data["adjusted_RR"]],
    fmt="o", color="#D97757", ecolor="#6A9BCC",   # brand colors
    elinewidth=2, capsize=4, markersize=7,
)
ax.axvline(x=1, color="#6B6B6B", linestyle="--", linewidth=1, label="RR = 1 (no effect)")
ax.set_yticks(list(y_pos))
ax.set_yticklabels(plot_data["variable"])
ax.set_xlabel("Adjusted RR (95% CI)")
ax.set_title("Forest Plot — Adjusted Risk Ratio (Modified Poisson)")
ax.legend(loc="lower right", fontsize=9)
ax.invert_yaxis()              # first variable on top
plt.tight_layout()
plt.show()
```

> 💡 **Key point**: this forest plot reuses Step 3's `adj_rr_df` directly—`ax.errorbar`'s `xerr` is the error length computed by subtracting `ci_lo`/`ci_hi` from `adjusted_RR`, and the dashed vertical line marks the RR = 1 no-effect reference; only a horizontal bar that doesn't cross that line is a statistically significant factor.

## Step 7: Model Diagnostics

This step uses AIC to compare the "full model" with more variables against a "reduced model" with only the core variables, to judge whether the full model is carrying too many variables.

```python
# === Step 7: Model diagnostics — AIC comparison ===
# Use AIC to compare the "full model" and the "reduced model" and judge whether we put in too many variables.

# --- Reduced model ---
# Remove the comorbidities that were non-significant or had small effect sizes in the Ch03 screening, plus floor.
# Keep: the core exposure factors (shower_use, hydrotherapy_use)
#       + the theoretically most important adjustment factors (age, immunosuppressed, functional_score)
formula_reduced = (
    "infected ~ shower_use + hydrotherapy_use + age + "
    "immunosuppressed + functional_score"
)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model_reduced = smf.glm(
        formula_reduced, data=df,
        family=sm.families.Poisson(),
    ).fit(cov_type="HC0")

print(f"Full model AIC = {model_poisson.aic:.1f}")
print(f"Reduced model AIC = {model_reduced.aic:.1f}")
print()

# --- Plain-language interpretation ---
if model_reduced.aic < model_poisson.aic:
    print("📉 The reduced model has a smaller AIC → it strikes a better balance between explanatory power and complexity")
else:
    print("📈 The full model has a smaller AIC → the extra variables really do contribute")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `formula_reduced = "infected ~ shower_use + hydrotherapy_use + age + immunosuppressed + functional_score"` | The reduced model: keeps only the core exposure factors and the most important adjustment factors, dropping the remaining comorbidities and floor |
> | `smf.glm(formula_reduced, data=df, family=sm.families.Poisson()).fit(cov_type="HC0")` | Refits with the same Modified Poisson setup but fewer variables, so its AIC can be fairly compared against the full model's |
> | `model_poisson.aic` / `model_reduced.aic` | Reads out both models' AIC values to compare—the number itself has no absolute meaning, only a **relative** one |
> | `if model_reduced.aic < model_poisson.aic:` | A smaller AIC means a better trade-off between explanatory power and complexity; this condition judges whether the reduced model wins |
>
> 💡 **Key point**: AIC can only be compared **within the same family** (both Poisson here)—it can't be compared against Step 4's logistic-regression AIC, a point the admonition below repeats.

> 🍽️ **The ordering-food metaphor**: AIC is like ordering dishes at a restaurant. Too many dishes (too many variables) → you can't finish them and waste money (overfitting). Too few dishes (too few variables) → you go hungry (underfitting). AIC helps you find the balance where you're "just full without waste." The smaller the AIC, the better.

```{admonition} AIC can only compare models of the same family
:class: warning

The AIC of Modified Poisson (Poisson family) and Logistic Regression (Binomial family) cannot be compared directly, because the likelihoods are computed on different bases. That's why above we only compared the AIC between two Poisson models.
```

### How do we choose variables? A comparison of three strategies

Above we only compared the two models "full vs reduced." But in practice, which variables should go into the model? There are three common strategies:

| Strategy | How it works | Pros | Cons |
|------|------|------|------|
| **Forward (add in)** | Start from the empty model and each step add the variable that lowers AIC the most | Simple and intuitive | Easily misses joint effects; the order of addition affects the result |
| **Backward (drop out)** | Start from the full model and each step remove the variable with the smallest effect on AIC | Can see the joint effect of all variables | Needs a large enough sample to include all variables |
| **Change-in-estimate** | Remove candidate confounders one at a time and see whether the exposure factor's RR changes by ≥ 10% | **The epidemiological gold standard**—judges based on "does it confound the exposure effect" | You must define the "exposure factor" first |

```{tip}
**Epidemiology recommends change-in-estimate**, not stepwise (automatic variable selection). The reason is simple: the purpose of our multivariable analysis is to **correctly estimate the effect of the exposure factor**, not to make predictions. Even if a variable's p-value is not significant, as long as it is a confounder (removing it changes the RR by ≥ 10%), it should stay in the model.

Stepwise uses the p-value as its criterion and may remove "variables that are non-significant but genuinely confounding," which distorts the exposure factor's RR.
```

Below we implement the **change-in-estimate method** in Python to see which candidate confounders truly affect the RR of shower_use and hydrotherapy_use:

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: The 10% rule—choosing variables with change-in-estimate</div>
  <div class="youtube-lite" data-id="OQLEUHJQv7s">
    <img src="https://img.youtube.com/vi/OQLEUHJQv7s/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

```python
# === Step 7b: Change-in-Estimate variable selection ===
# The standard epidemiological approach: remove candidate confounders one at a time
# and see how much the exposure factors' (shower_use, hydrotherapy_use) adjusted RR changes.
# A change of ≥ 10% → that variable is a confounder and must stay in the model.

# --- The exposure factors' RR from the full model (baseline) ---
full_rr = {
    var: np.exp(model_poisson.params[var])
    for var in ["shower_use", "hydrotherapy_use"]
}
print("Exposure factors' RR from the full model (baseline):")
for var, rr in full_rr.items():
    print(f"  {var}: {rr:.3f}")
print()

# --- Candidate confounders: test by removing each one ---
confounders = [
    "age", "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed", "functional_score", "C(floor)",
]

cie_results = []
for drop_var in confounders:
    # Build the formula with one variable removed
    keep = [c for c in confounders if c != drop_var]
    formula_test = "infected ~ shower_use + hydrotherapy_use + " + " + ".join(keep)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = smf.glm(formula_test, data=df, family=sm.families.Poisson()).fit(
            cov_type="HC0", disp=0
        )

    for exposure in ["shower_use", "hydrotherapy_use"]:
        rr_without = np.exp(m.params[exposure])
        pct_change = (rr_without - full_rr[exposure]) / full_rr[exposure] * 100
        cie_results.append({
            "removed variable": drop_var,
            "exposure factor": exposure,
            "RR after removal": round(rr_without, 3),
            "RR change %": f"{pct_change:+.1f}%",
            "confounder?": "✓ confounder" if abs(pct_change) >= 10 else "",
        })

cie_df = pd.DataFrame(cie_results)
print("=== Change-in-Estimate analysis ===")
print("(After removing a variable, if an exposure factor's RR changes by ≥ 10% → that variable is a confounder)\n")
print(cie_df.to_string(index=False))
```

> 📋 **How do you use this table?** Look at the "RR change %" column. If, after removing a variable, the RR of shower_use or hydrotherapy_use changes by more than 10%, that variable is a confounder and must stay in the model—even if its own p-value is not significant.

---

## Key Takeaways for Interpretation

| Result | Meaning |
|------|------|
| Adjusted RR > 1 and p < 0.05 | Still an independent risk factor after controlling for other factors |
| Crude RR ≫ Adjusted RR | The crude RR was inflated by confounding (consistent with the Ch05 MH conclusion) |
| Adjusted RR ≈ 1 | The effect disappears after adjustment; the original association may have been spurious |
| Adjusted OR > Adjusted RR | The OR overestimates the effect (inevitable at a high attack rate) |
| Smaller AIC | The model strikes a better balance between explanatory power and complexity |

## Common Mistakes

1. **Reporting only the OR in a cohort study**: at a high attack rate OR ≠ RR. You should use Modified Poisson to compute the RR, or at least report both so readers know the difference
2. **Using the OR as if it were the RR**: telling your supervisor "OR = 3.5 means the risk is 3.5 times higher" is wrong at a high attack rate. Clearly distinguish "how many times the odds" from "how many times the risk"
3. **Putting in too many variables**: 280 records with 15+ variables → overfitting. Rule of thumb: each predictor needs at least 10–15 events
4. **Ignoring multicollinearity**: don't include highly correlated variables together (for example, functional_status and age may be highly correlated)
5. **Automatic variable selection**: stepwise is not recommended → use epidemiological knowledge and a DAG to select variables
6. **Not reporting the CI**: reporting only the p-value isn't enough. The CI tells you the precision and clinical significance of the effect

## Next Step

The multivariable analysis answered "which factors independently affect the risk of infection." But your supervisor then asks: "How many new cases will there be next week?" → Ch07 time series forecasting.

## Practice Notebooks

- Class notes: {ref}`06_logistic_regression.ipynb`
- Exercise version: [`06_logistic_regression_exercise.ipynb`](exercises/06_logistic_regression_exercise.ipynb)
- Solution version (instructor edition): [`06_logistic_regression_solution.ipynb`](solutions/06_logistic_regression_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/06_logistic_regression_solution.ipynb>)
