# 03 The Association Between Exposure and Disease: 2×2 Tables and Inferential Statistics

## Scenario

The outbreak team investigating the Legionnaires' disease cluster at Songbai Nursing Home has already finished cleaning and visualizing the data (Ch02). Now your supervisor asks: **"Do people who use the shower facilities have a higher risk of infection? Is there any statistical evidence for that?"**

You're about to answer "the shower group has a higher attack rate," when a senior outbreak investigator cuts in:

> "Hold on—are you talking about **description** or **inference**? Just saying it 'looks higher' isn't enough. How do you use statistics to rule out that this is just random error? And with the data you have in hand, is it even appropriate to compute an RR or an OR?"

This chapter is all about answering those questions.

## What You'll Learn

- The difference between descriptive and inferential statistics
- How epidemiological study design (cohort study vs. case-control study) determines which effect measure to use
- How to build a 2×2 contingency table from a line list
- How to compute the risk ratio (RR) and what it means
- How to compute the odds ratio (OR) and how RR and OR differ
- How to estimate the 95% confidence interval (CI) for RR and OR
- How to use the chi-square test and Fisher's exact test to judge statistical significance
- How to compare multiple risk factors at once and visualize them with a forest plot

---

## Descriptive vs. Inferential Statistics

In Ch02 we used **descriptive statistics** (means, frequency distributions, charts) to summarize what the data looked like. But the supervisor's question isn't "what does the data look like," it's "is there **an association** between shower use and infection."

That calls for **inferential statistics**—using sample data to make inferences: is the observed difference a real association, or purely the result of **chance (random error)**?

| Type | Purpose | Example |
|------|---------|---------|
| Descriptive statistics | Summarize the features of the data | Mean age 72, attack rate 43.2%, epidemic curve |
| Inferential statistics | Infer about the population from a sample, test hypotheses | 95% CI for RR, chi-square test p-value |

### Key Terms

- **Null hypothesis (H₀)**: shower use and infection are independent (no association)
- **Alternative hypothesis (H₁)**: shower use and infection are associated
- **p-value**: the probability of observing the current data (or something more extreme) assuming H₀ is true. The smaller the p, the more reason to reject H₀
- **Confidence interval (CI)**: a plausible range for the effect measure. If the 95% CI does not include the "no-effect value" (RR=1 or OR=1), the result is statistically significant at the α=0.05 level

---

## A Quick Tour of Epidemiological Study Designs

What measures you can calculate depends on your **study design**. Here we use everyday analogies to explain four common designs:

```{figure} images/study_designs_en.svg
:name: fig-study-designs
:alt: Four epidemiological study designs: cohort study (following-along documentary), case-control (detective work), nested case-control (reviewing surveillance footage), matched case-control (twin experiment)
:width: 100%
```

### ❶ Cohort Study—A Following-Along Documentary

Imagine you're a documentary director: you pick two groups of people up front (those who got rained on vs. those who didn't), then follow them the whole way to see who catches a cold later.

- **Group by exposure status**, then follow forward for the disease outcome
- You know **exactly** how many exposed and unexposed people there are (you have complete denominators)
- You can directly compute **risk (risk = number who got sick ÷ total in that group)** and the **RR (risk ratio)**

> 🎬 This nursing home investigation = a **retrospective cohort study**: all 280 residents are included, and both exposure and outcome are known → you can directly compute the **RR**.

### ❷ Case-Control Study—Detective Work

Imagine you're a detective: first you find the "victims" (people who are already sick, called cases), then you separately select a group of "non-victims" (people who aren't sick, called controls), and you look back to ask whether they had contact with the suspect (exposure) in the past.

- **Group by disease status** (find cases first, then select controls), then look back at exposure history
- The number of controls is **decided by the researcher** (e.g., 1:1 or 1:4 matching), and doesn't reflect the true incidence in the population
- Because the denominator is artificially set, **you can't compute risk → you can only compute the OR (odds ratio)**

> 🕵️ When is it used? Rare diseases (like CJD or Ebola) or large nationwide investigations (like vaccine effectiveness/VE studies)—tracking millions of people is too expensive and slow, so it's better to pick a few hundred cases to study.

### ❸ Nested Case-Control Study—Reviewing Surveillance Footage

Your community is already running a cohort study (like having surveillance cameras rolling the whole time), but sending everyone's blood off for expensive biomarker testing costs too much. What do you do?

- Once someone develops disease, **pull those cases out of the cohort**
- Then select matched controls from **the same cohort** and go back to run the tests
- You get both the **representativeness** of a cohort and the **efficiency** of a case-control design

> 🏠 Common in biomarker sub-studies within large prospective cohorts (like the Nurses' Health Study).

### ❹ Matched Case-Control Study—A Twin Experiment

You find a 70-year-old male case, so you deliberately go find someone of **similar age and sex who isn't sick** to pair them up. That way the effects of age and sex "cancel out."

- The matching variables (like age and sex) are controlled at the design stage
- The analysis must use **conditional logistic regression**, not an ordinary chi-square test
- The matching ratio can be 1:1, 1:2, or even 1:4 (more controls means greater statistical power)

> 👯 Analogy: find a "near-clone with similar conditions," where the only difference between the two is whether they were exposed.

### Quick Reference: Choosing a Design

| Study design | Sampling approach | Measure available | Use case | Analogy |
|---------|---------|---------|---------|------|
| Cohort study | Group by exposure, follow for outcome | **RR** | Outbreak investigation (data on everyone) | 🎬 Following-along documentary |
| Case-control | Group by disease, look back at exposure | **OR** | Rare disease, large populations | 🕵️ Detective work |
| Nested case-control | Pick cases + controls from a cohort | **OR** | Sub-study within a large cohort | 🏠 Reviewing footage |
| Matched case-control | Match 1:n on matching variables | **OR** (conditional) | Need to control known confounders | 👯 Twin experiment |

---

## 🍢 Super Simple Special: Understanding the 2×2 Table and Risk Ratio with "Half the Class Got Diarrhea After the BBQ Trip"

> 2×2 tables, attack rate, risk ratio, chi-square test... a lot of new vocabulary this chapter? Don't be scared. This section sets the nursing home aside for a moment and uses a disaster **everyone dreads**—**"half the class ended up running to the bathroom after a class BBQ trip"**—to walk through the single most important trick in this whole chapter, in a way that'll make even a 7th grader get it instantly. Master this one trick, and the 2×2 table, RR, and chi-square test later on are all just it wearing different costumes.

### The tragedy of a class BBQ

40 classmates go on a class trip and have a BBQ. Afterward, **20 of them start having diarrhea** 😖. The teacher wants to find out: **which dish is to blame?**

The dishes on the table line up like a row of "suspects": 🥗 green salad, 🌭 grilled sausage, 🍚 plain rice, 🍗 grilled chicken... any one of them could be guilty. How do you catch the real culprit?

### The key to cracking the case: an "ate it vs. skipped it" face-off for every dish 🥊

For **each dish**, we split the whole class into two teams:

- **The "ate this dish" team**—what fraction of them got diarrhea?
- **The "skipped this dish" team**—what fraction of them got diarrhea?

If a dish shows "**the people who ate it got diarrhea way more often than the people who skipped it**," it's a prime suspect. On the other hand, if both teams have **about the same** diarrhea rate, that dish is probably innocent.

### Why do you have to look at "the people who skipped it"? (beginners' #1 trap)

You might say: "Can't I just ask the sick kids what they ate?"—**that's exactly the classic mistake!**

> 🚨 **"80% of the sick kids ate the salad! So it's the salad!"**—this sentence actually **proves nothing**. What if 80% of the kids who *didn't* get sick also ate the salad? (Then the salad would have nothing to do with it at all.)

> ⚽ Remember it in one line: **counting how many goals one team scored doesn't tell you who won the game.** You always have to look at "the salad-eating team's hit rate" **against** "the salad-skipping team's hit rate"—only a face-off between the two teams tells you whether the salad is really the problem. This habit of "never forget to compare against the unexposed" is the bedrock of all epidemiology.

### Attack rate: it all comes down to the denominator

We're not comparing "how many people got sick"—we're comparing **the proportion who got sick within each team**. That proportion is called the **attack rate**:

$$\text{attack rate} = \frac{\text{number sick in this team}}{\text{total in this team}}$$

> 🔑 **The denominator is everything**: "3 people got sick after eating the grilled chicken" sounds scary, right? But if **100 people in total ate the chicken**, the attack rate is only 3%; if instead **only 3 people ate the chicken and all 3 got sick**, that's 100%! Same "3 people sick," wildly different meaning—**before you react to a number, always ask what the denominator is.**

```{figure} images/bbq_attack_rate_en.svg
:name: fig-bbq-attack-rate
:alt: BBQ 2x2 table and attack-rate face-off: in the green salad group, 80% (16/20) of those who ate it got diarrhea versus 20% (4/20) of those who skipped it, RR=4.0 makes it suspect #1, expanded into a 2x2 table with a=16, b=4, c=4, d=16; in the plain rice group both eaters and skippers are 50%, RR=1.0, innocent; a reminder that "counting only the sick people's plates" is a denominator trap, bridging finally to the nursing home's shower_use x infection
:width: 100%

Left: for the green salad, the "ate it" team is 80% vs. the "skipped it" team at 20%, RR=4.0—prime suspect #1. These two rows of little stick figures are literally a 2x2 table. Right: for plain rice, both teams are at 50%, RR=1.0—innocent. Don't forget the denominator.
```

### Try it yourself: catch the guilty dish with your own two hands

```python
from scipy.stats import chi2_contingency

# 40 classmates go on a BBQ trip, 20 get diarrhea. Build a 2x2 table for each dish:
# compare the diarrhea rate (attack rate) of "people who ate this dish" vs. "people who didn't"
# each tuple = (ate and sick, ate and not sick, skipped and sick, skipped and not sick)
foods = {
    "Green salad":     (16, 4, 4, 16),
    "Grilled sausage": (10, 8, 10, 12),
    "Plain rice":       (10, 10, 10, 10),
}

for name, (a, b, c, d) in foods.items():
    ar_eat = a / (a + b)      # attack rate among people who ate this dish
    ar_skip = c / (c + d)     # attack rate among people who skipped it
    rr = ar_eat / ar_skip
    print(f"{name}: ate {ar_eat:.0%} sick vs skipped {ar_skip:.0%} → RR = {rr:.1f}")

# Suspect #1 is the green salad (highest RR). Is this gap real, or did the 40 kids just get unlucky differently? -> chi-square test
a, b, c, d = foods["Green salad"]
chi2, p, dof, _ = chi2_contingency([[a, b], [c, d]], correction=False)
print(f"\nGreen salad 2x2 chi-square test: p = {p:.4f} (p < 0.001 → a gap this big is almost impossible by chance)")
```

Running this, you'll see:

```text
Green salad: ate 80% sick vs skipped 20% → RR = 4.0
Grilled sausage: ate 56% sick vs skipped 45% → RR = 1.2
Plain rice: ate 50% sick vs skipped 50% → RR = 1.0

Green salad 2x2 chi-square test: p = 0.0001 (p < 0.001 → a gap this big is almost impossible by chance)
```

### What does RR = 4 actually feel like? RR is an "innocence-o-meter"

**Risk ratio (RR) = the "ate it" team's attack rate ÷ the "skipped it" team's attack rate.**

> 🎟️ **RR = 4 isn't "4% more"—it's a full 4 times over**—eating that dish quadruples your chance of getting hit. Picture the same scratch-card game: **for people who ate the salad, 1 out of every 4 cards is a "diarrhea" winner; for people who skipped it, you'd need 16 cards to hit one.**

RR works like an "innocence-o-meter"—**the farther from 1, the more suspicious**:

- **RR ≈ 1** (plain rice): both teams have the same hit rate → **innocent**
- **RR = 4** (salad): the "ate it" team gets hit four times as often → **prime suspect**

### Is the gap real, or just bad luck? → the chi-square test

Even if the salad's two teams show different hit rates, could it just be that **these particular 40 kids happened to get unlucky in different ways**?

> 🎲 **The chi-square test asks exactly this**: "Is this gap too big to be a coincidence from rolling the dice?" It hands you back a **p-value**. For the salad, **p = 0.0001** means: **if the salad were actually innocent, the chance of a gap this big showing up from pure luck alone is less than 1 in 10,000**—so we can be almost certain the salad's guilt is for real.

### ⚠️ Four honest caveats

1. **Statistics can only flag a "suspect," not deliver a "conviction"**: a high RR only means the salad is **suspicious**—an actual conviction needs a lab to culture the pathogen off the salad, plus further investigation. Statistics points the direction; evidence closes the case.
2. **With enough dishes, one of them will "just happen" to look suspicious**: if you compare 20 dishes at once, even if all of them are innocent, one or two might get a small p-value from pure luck. Don't pop the champagne the moment you spot a suspect (you'll learn how to correct for this "multiple comparisons" problem later).
3. **Some dishes always show up as a pair**: salad is often eaten together with salad dressing—so which one is the real culprit? When two exposures are tangled together, each pointing the finger at the other, you need **the stratified analysis from Ch05** to untangle them (remember the "big feet"?).
4. **When a cell has too few people (< 5), the chi-square test gets unreliable**: switch to **Fisher's exact test** instead (covered in the main text of this chapter).

> 💡 A little extra: here, we **know every single classmate** and what each of them ate—that's a **cohort study**, so **RR** is exactly the right tool. If instead we could only find "the people who already got sick" and had to ask them afterward what they'd eaten, we'd need the **OR (odds ratio)**—the "casino odds" idea from the main text of this chapter.

### Cheat sheet for reading the chart (save this)

| What you see... | What it means |
|---|---|
| Looking only at "what the sick kids ate" | ❌ Forgetting the denominator—you'll get fooled |
| "Attack rate of the 'ate it' team vs. the 'skipped it' team" | ✔ The correct comparison (the soul of the 2×2 table) |
| Attack rate | The **proportion** sick within one team (denominator = that team's total) |
| RR ≈ 1 | Both teams the same → this exposure is probably innocent |
| RR much greater than 1 | The "ate it" team got hit way more → prime suspect |
| RR < 1 | The "ate it" team actually got hit less → possibly a protective factor (like a vaccine) |
| Chi-square p-value is small (< 0.05) | This gap is unlikely to be just luck |
| A cell has < 5 people | Switch to Fisher's exact test |

### Back to reality: salad → showering

Now swap the BBQ scenario for the nursing home version:

| BBQ world | Real nursing home case |
|---|---|
| Each dish (salad, rice...) | Each exposure (`shower_use`, `hydrotherapy_use`...) |
| Ate / skipped this dish | Showered / didn't shower |
| Diarrhea / fine | Infected / not infected |
| "Ate vs. didn't × sick vs. not" laid out in a grid | 2×2 table (a / b / c / d) |
| Attack rate of the "ate it" team | Attack rate among those who showered |
| Attack rate of the "skipped it" team | Attack rate among those who didn't shower |
| Dividing the two teams' hit rates | Risk ratio (RR) |
| "Is this gap just luck?" | Chi-square test / p-value |
| Catching the guilty dish | Finding the source of infection |

Every trick you just learned at the BBQ table—splitting into two teams for a face-off, computing the attack rate, never forgetting the denominator, RR as an innocence-o-meter, and asking the chi-square test whether it's just luck—**is exactly what Steps 2–5 of this chapter do with the nursing home data**. Now scroll back down to those 2×2 tables and RR and OR—doesn't it suddenly feel a lot friendlier? 😉

---

## Core Concepts

### The 2×2 Contingency Table

|  | Infected | Not infected | Total |
|--|------|--------|------|
| **Exposed** | a | b | a+b |
| **Unexposed** | c | d | c+d |

### Risk Ratio—Weighing Which Side Is Heavier ⚖️

$$RR = \frac{a / (a+b)}{c / (c+d)}$$

**In plain language**: RR = 2 means "people who were exposed have **twice** the risk of disease as people who weren't." It's like placing the two groups' risks on a scale and seeing how many times heavier the exposed group is than the unexposed group.

- RR = 1: exposure and disease are unrelated (both sides weigh the same)
- RR > 1: exposure may increase risk (the exposed side is heavier)
- RR < 1: exposure may be protective (the exposed side is lighter—e.g., a vaccine)

### Odds Ratio—Casino Betting Odds 🎰

**Odds** and **risk** are different:

- **Risk = p**: 30 out of 100 people get sick → risk = 30/100 = 0.3 (divide by **everyone**)
- **Odds = p / (1-p)**: 30 sick vs. 70 not sick → odds = 30/70 ≈ 0.43 (sick ÷ **not sick**)

$$OR = \frac{a \times d}{b \times c}$$

**In plain language**: OR = 3 means "people who were exposed have 3 times the **odds** of disease as people who weren't." Note this is about "odds," not "risk"—just like a casino quoting 3:1 odds doesn't mean you have a 300% chance of winning.

```{figure} images/or_rr_relationship_en.svg
:name: fig-or-rr-relationship
:alt: The relationship between RR and OR: they're similar for rare diseases, but the higher the attack rate, the more the OR diverges from the RR
:width: 100%
```

### RR and OR: When Are They the Same, and When Are They Different?

This is where beginners get confused most, so let's clear it up once and for all:

#### 1️⃣ For Rare Diseases, OR ≈ RR (the 10% Rule)

**The mathematical reason**: Risk = p, Odds = p/(1−p). When p is small (say &lt; 10%), (1−p) ≈ 1, so Odds ≈ p ≈ Risk. Both groups' odds are ≈ their risk, so OR ≈ RR.

> 🍬 Analogy: a bag of 100 candies has 3 sour ones. The "probability of drawing a sour one (risk)" = 3/100 = 3%. The "odds of drawing a sour one" = 3/97 ≈ 3.1%. The difference is just 0.1%—practically the same! But if 50 are sour, risk = 50% while odds = 50/50 = 100%—that's double, completely different.

#### 2️⃣ When the Attack Rate Is High, OR Is Systematically Larger Than RR

When the disease is common (like this dataset's attack rate of ~43%), the (1−p₁) of the exposed group is smaller than the (1−p₀) of the unexposed group, which inflates the exposed group's odds even more → the OR gets "stretched" larger.

Concrete numbers: suppose Risk₁ = 55% and Risk₀ = 30% (RR = 1.83), but Odds₁ = 55/45 = 1.22 and Odds₀ = 30/70 = 0.43 → OR = 1.22/0.43 = **2.86**, 56% higher than the RR!

> ⚠️ **Practical implication**: this outbreak's attack rate is 43%, so if you use the OR to say "risk is X times higher," you'll seriously overestimate. Reports should use the **RR**, not the OR.

#### 3️⃣ OR Is the Native Output of Logistic Regression

A logistic regression model has the mathematical form log(odds) = β₀ + β₁×exposure + ..., so the model directly gives you the **difference in log-odds**, and exp(β₁) = OR.

No matter whether your data comes from a cohort study or a case-control study, if you run logistic regression, **what comes out is an OR**. Ch06 will teach you how to do this.

### How Do You Estimate Vaccine Effectiveness (VE)? Can You Use Both RR and OR?

**Vaccine effectiveness (VE)** measures how much a vaccine reduces disease risk in the real world:

| Study design | VE formula | Common use case |
|---------|---------|---------|
| Cohort study | VE = 1 − RR | Clinical trials (RCTs), outbreak investigations |
| Case-control | VE = 1 − OR | Large-scale post-marketing surveillance (test-negative design) |

- **Cohort study**: directly compare the incidence of vaccinated vs. unvaccinated → VE = 1 − RR. For example, RR = 0.2 → VE = 80% (the vaccine reduces risk by 80%)
- **Case-control study**: first find the sick (cases) and the not sick (controls), then compare the vaccination rates of the two groups → VE = 1 − OR. Many COVID-19 vaccine effectiveness figures were computed with a **test-negative case-control design**

> **When do you choose which?**
> - If you're running a clinical trial or an outbreak investigation (data on everyone) → **cohort study → RR → VE = 1−RR**
> - If you're doing nationwide post-marketing surveillance (tracking millions is too expensive) → **case-control → OR → VE = 1−OR**
> - When the disease is rare (most vaccine-preventable diseases), OR ≈ RR, and the two VE formulas give roughly the same result

### The 95% Confidence Interval

**CI for RR** (Katz method):

$$\ln(RR) \pm 1.96 \times SE(\ln RR)$$

where $SE(\ln RR) = \sqrt{\frac{1}{a} - \frac{1}{a+b} + \frac{1}{c} - \frac{1}{c+d}}$

**CI for OR** (Woolf method):

$$\ln(OR) \pm 1.96 \times SE(\ln OR)$$

where $SE(\ln OR) = \sqrt{\frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}}$

If the 95% CI does not include 1, the effect measure is statistically significant at the α=0.05 level.

### The Chi-Square Test and Fisher's Exact Test

- **Chi-square test**: compares observed counts with expected counts (what you'd expect under H₀); appropriate when expected values are ≥ 5
- **Fisher's exact test**: directly computes the exact probability of observing the current or more extreme results under H₀; appropriate for small samples (expected values < 5)

---

## Step 1: Prepare the Data

```python
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact
from epi_learning.metrics import risk_ratio, odds_ratio

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# Create a binary "infected" column (0/1)
# clinical_severity == "not_ill" means no symptoms and not infected; everything else counts as infected
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

print(f"Total: {len(df)} people, infected: {df['infected'].sum()} people")
print(f"Overall attack rate: {df['infected'].mean():.1%}")
```

```{raw} html
<div class="video-card">
  <div class="video-title">Video: The 2×2 Contingency Table—Turning Outbreak Data into a Four-Cell Table</div>
  <div class="youtube-lite" data-id="MrBUJ3iTyaw">
    <img src="https://img.youtube.com/vi/MrBUJ3iTyaw/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

## Step 2: Build the 2×2 Table (Shower × Infection)

We already have 280 residents and an `infected` column. Now we'll organize it into a **2×2 contingency table**—the fundamental data structure for epidemiological association analysis. The diagram below shows how each cell maps to the formulas.

```{figure} images/two_by_two_anatomy_en.svg
:name: fig-two-by-two-anatomy
:alt: A map of the a, b, c, d cells of a 2×2 contingency table, showing how each cell is used to compute the RR and OR
:width: 100%
```

```python
# The first argument to pd.crosstab() → rows, the second → columns
# margins=True automatically adds a subtotal row and a subtotal column
ct_shower = pd.crosstab(
    df["shower_use"], df["infected"],
    margins=True, margins_name="Total",
)
# Rename for readability (the raw 0/1 values aren't intuitive)
ct_shower.index = ["No shower", "Shower", "Total"]
ct_shower.columns = ["Not infected", "Infected", "Total"]
print(ct_shower)

# ── Extract the four cells of the 2×2 table (see the diagram above) ──
# crosstab's row order follows the sort order of the raw values (0 before 1)
# After renaming, we extract by the renamed labels so we don't have to remember which is 0 and which is 1
a = int(ct_shower.loc["Shower", "Infected"])        # a = exposed + infected
b = int(ct_shower.loc["Shower", "Not infected"])      # b = exposed + not infected
c = int(ct_shower.loc["No shower", "Infected"])      # c = unexposed + infected
d = int(ct_shower.loc["No shower", "Not infected"])    # d = unexposed + not infected

# Compute the attack rate for each group separately
print(f"\nExposed group (Shower) attack rate: {a/(a+b):.1%}")
print(f"Unexposed group (No shower) attack rate: {c/(c+d):.1%}")
```

```{raw} html
<div class="video-card">
  <div class="video-title">Video: The Risk Ratio (RR)—Did the Exposure Actually Increase Risk?</div>
  <div class="youtube-lite" data-id="wUOt40SNZvA">
    <img src="https://img.youtube.com/vi/wUOt40SNZvA/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

## Step 3: Compute the Risk Ratio

```python
rr = risk_ratio(a, a + b, c, c + d)
print(f"Shower use → infection RR = {rr:.3f}")
print(f"  Interpretation: shower users' infection risk is {rr:.1f}x that of non-users")
print(f"  RR = 1 → no association | RR > 1 → exposure may increase risk | RR < 1 → may be protective")
```

> **Note**: RR > 1 indicates an "association," not "causation." There may be confounders—Ch05 will deal with that.

---

You've just computed the RR, but papers and reports often show the OR too. What's the difference? **Risk is a probability; odds is a ratio**—the figure below explains.

```{figure} images/rr_vs_or_intuition_en.svg
:name: fig-rr-vs-or-intuition
:alt: An intuition diagram for Risk vs Odds: of 10 residents, 3 are infected, so Risk = 3/10 and Odds = 3/7; cohort studies use RR, case-control studies use OR
:width: 100%
```

```{raw} html
<div class="video-card">
  <div class="video-title">Video: The Odds Ratio (OR)—How Is It Different from the RR?</div>
  <div class="youtube-lite" data-id="tOloIGqUFvs">
    <img src="https://img.youtube.com/vi/tOloIGqUFvs/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

## Step 4: Compute the Odds Ratio

```python
or_val = odds_ratio(a, b, c, d)
print(f"Shower use → infection OR = {or_val:.3f}")
print(f"  (compared with RR = {rr:.3f})")
print(f"\nThis dataset's attack rate = {df['infected'].mean():.1%} (not a rare disease)")
print(f"→ OR ({or_val:.3f}) is greater than RR ({rr:.3f}), which is expected")
print(f"→ When disease is rare, OR ≈ RR; the higher the attack rate, the more OR deviates from RR")
print(f"\n⚠️ This case's attack rate ~43%, so don't use OR to say 'how many times the risk'!")
print(f"   Correct wording: 'shower users' infection risk is {rr:.1f}x that of non-users (RR)'")
print(f"   Wrong wording: 'shower users' infection risk is {or_val:.1f}x that of non-users (OR)' ← overestimated!")
```

> **Choosing between RR and OR**: this is a cohort study (all 280 people included), so report the effect measure as the **RR**. We compute the OR as well because: (1) it's practice for understanding the difference between the two, and (2) it prepares us for Ch06's logistic regression (whose native output = OR).

```{raw} html
<div class="video-card">
  <div class="video-title">Video: The 95% Confidence Interval—Why Take the log First and Then exp Back?</div>
  <div class="youtube-lite" data-id="Z_eYSHtyHxM">
    <img src="https://img.youtube.com/vi/Z_eYSHtyHxM/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

## Step 5: 95% Confidence Interval (RR and OR)

The CI is the part that makes beginners' heads spin the most. The key intuition: the scale of RR/OR is **asymmetric** (from 0 to infinity), so you can't just add and subtract a margin of error directly. First we **log-transform** to a symmetric scale, do the work, and then **exp back**. The figure below explains it in three steps:

```{figure} images/ci_log_transform_en.svg
:name: fig-ci-log-transform
:alt: Why do we take the log to compute the CI? A three-step diagram: original scale (asymmetric) → log scale (symmetric, where the normal distribution applies) → exp back
:width: 100%
```

```python
# ── 95% CI for RR: Katz method ──

# (a) Take the natural log: move RR from the asymmetric scale (0, ∞) to the symmetric scale (-∞, +∞)
ln_rr = np.log(rr)

# (b) Compute the standard error (SE): a measure of how precise the ln(RR) estimate is
#     The formula comes from Katz (1978), derived from the four cells of the 2×2 table
se_ln_rr = np.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))

# (c) On the log scale, ±1.96 × SE (1.96 is the z-value for 95% of the normal distribution)
# (d) Use exp() to convert back to the original scale → get the lower and upper bounds of the CI
ci_rr_lo = np.exp(ln_rr - 1.96 * se_ln_rr)
ci_rr_hi = np.exp(ln_rr + 1.96 * se_ln_rr)

# ── 95% CI for OR: Woolf method ──
# Same principle, only the SE formula differs (using the sum of the reciprocals of a, b, c, d)
ln_or = np.log(or_val)
se_ln_or = np.sqrt(1/a + 1/b + 1/c + 1/d)
ci_or_lo = np.exp(ln_or - 1.96 * se_ln_or)
ci_or_hi = np.exp(ln_or + 1.96 * se_ln_or)

print("=== 95% Confidence Interval Comparison ===")
print(f"RR = {rr:.3f} (95% CI: {ci_rr_lo:.3f} – {ci_rr_hi:.3f})")
print(f"OR = {or_val:.3f} (95% CI: {ci_or_lo:.3f} – {ci_or_hi:.3f})")
```

> **Interpretation**: if you repeated this investigation 100 times, roughly 95 of the computed CIs would contain the true RR/OR. A CI that doesn't include 1 = statistically significant at α=0.05, equivalent to p < 0.05.

```{raw} html
<div class="video-card">
  <div class="video-title">Video: The Chi-Square Test—A Showdown Between Observed and Expected Values</div>
  <div class="youtube-lite" data-id="qv3j0CSfHT0">
    <img src="https://img.youtube.com/vi/qv3j0CSfHT0/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

## Step 6: The Chi-Square Test

The core logic of the chi-square test: if exposure and infection really were "unrelated" (H₀ is true), how many people should we observe in each cell? How far are the actual numbers from that expectation?

```{figure} images/chi_square_intuition_en.svg
:name: fig-chi-square-intuition
:alt: An intuition diagram for the chi-square test: comparing observed and expected values—the larger the gap → the larger the χ² → the smaller the p
:width: 100%
```

```python
# H₀: shower use and infection are independent (no association)
contingency = [[a, b], [c, d]]
chi2, p, dof, expected = chi2_contingency(contingency)

print(f"Chi-square statistic = {chi2:.3f}")
print(f"Degrees of freedom = {dof}")
print(f"p-value = {p:.4f}")
print(f"\nExpected-value table (expected counts when H₀ is true):")
print(pd.DataFrame(
    expected.round(1),
    index=["Shower", "No shower"],
    columns=["Infected", "Not infected"],
))

min_expected = expected.min()
print(f"\nMinimum expected value = {min_expected:.1f}", end="")
if min_expected >= 5:
    print(" → meets the chi-square test assumption")
else:
    print(" → < 5, recommend using Fisher's exact test instead")
```

```{raw} html
<div class="video-card">
  <div class="video-title">Video: Fisher's Exact Test—The Savior for Small Samples</div>
  <div class="youtube-lite" data-id="x8n7wUWtfz0">
    <img src="https://img.youtube.com/vi/x8n7wUWtfz0/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

## Step 7: Fisher's Exact Test

```python
oddsr_fisher, p_fisher = fisher_exact(contingency)
print(f"Fisher's exact test:")
print(f"  OR = {oddsr_fisher:.3f}")
print(f"  p-value = {p_fisher:.4f}")
print(f"\nChi-square test p = {p:.4f} vs Fisher p = {p_fisher:.4f}")
print("(This example's sample is large enough that the two tests agree closely; the difference is more pronounced with small samples)")
```

> Fisher's exact test doesn't rely on a large-sample approximation, making it more reliable when expected values are < 5 or the total sample size is < 30.

## Step 8: A Second Exposure Factor — Hydrotherapy Use

Apply the same analysis workflow to a second exposure factor. The code is exactly the same as Steps 2–6, just swapping `shower_use` for `hydrotherapy_use`. Step 9 will use a loop to automate this process, so you won't have to copy and paste by hand anymore.

```python
# The exact same workflow as Steps 2–6, swapped to hydrotherapy exposure
ct_hydro = pd.crosstab(df["hydrotherapy_use"], df["infected"])
a2, b2 = int(ct_hydro.loc[1, 1]), int(ct_hydro.loc[1, 0])  # exposed+infected, exposed+not infected
c2, d2 = int(ct_hydro.loc[0, 1]), int(ct_hydro.loc[0, 0])  # unexposed+infected, unexposed+not infected

# Effect measures
rr2 = risk_ratio(a2, a2 + b2, c2, c2 + d2)
or2 = odds_ratio(a2, b2, c2, d2)
chi2_2, p2, _, _ = chi2_contingency([[a2, b2], [c2, d2]])

# RR CI (Katz method, same as Step 5)
ln_rr2 = np.log(rr2)
se_rr2 = np.sqrt(1/a2 - 1/(a2+b2) + 1/c2 - 1/(c2+d2))
ci_rr2_lo = np.exp(ln_rr2 - 1.96 * se_rr2)
ci_rr2_hi = np.exp(ln_rr2 + 1.96 * se_rr2)

# OR CI (Woolf method, same as Step 5)
ln_or2 = np.log(or2)
se_or2 = np.sqrt(1/a2 + 1/b2 + 1/c2 + 1/d2)
ci_or2_lo = np.exp(ln_or2 - 1.96 * se_or2)
ci_or2_hi = np.exp(ln_or2 + 1.96 * se_or2)

print("Hydrotherapy use → infection")
print(f"  RR = {rr2:.3f} (95% CI: {ci_rr2_lo:.3f} – {ci_rr2_hi:.3f})")
print(f"  OR = {or2:.3f} (95% CI: {ci_or2_lo:.3f} – {ci_or2_hi:.3f})")
print(f"  chi-square p-value = {p2:.4f}")
```

## Step 9: A Multi-Factor Crude Effect-Measure Summary Table + Forest Plot

In a real outbreak investigation you won't just look at one or two factors. The loop below **systematically applies Steps 2–6 to every candidate exposure**, then uses a forest plot to compare them at a glance.

```python
import matplotlib.pyplot as plt

# List all exposure factors to test (binary 0/1 variables)
factors = [
    "shower_use", "hydrotherapy_use",
    "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed",
]
# Convert "ever smoked" into a binary variable
df["ever_smoker"] = (df["smoking_history"] != "never").astype(int)
factors.append("ever_smoker")

# ── Loop: repeat Steps 2–6 for each factor ──
# Each iteration does 5 things: (a) build the 2×2 table → (b) compute RR/OR → (c) compute the CI → (d) chi-square test → (e) store the results
results = []
for factor in factors:
    # (a) Build the 2×2 table, extract a, b, c, d
    ct = pd.crosstab(df[factor], df["infected"])
    a_i = int(ct.loc[1, 1])   # exposed + infected
    b_i = int(ct.loc[1, 0])   # exposed + not infected
    c_i = int(ct.loc[0, 1])   # unexposed + infected
    d_i = int(ct.loc[0, 0])   # unexposed + not infected

    # (b) Effect measures: RR and OR
    rr_i = risk_ratio(a_i, a_i + b_i, c_i, c_i + d_i)
    or_i = odds_ratio(a_i, b_i, c_i, d_i)

    # (c) 95% CI for RR (Katz method, same as Step 5)
    ln_rr_i = np.log(rr_i)
    se_i = np.sqrt(1/a_i - 1/(a_i+b_i) + 1/c_i - 1/(c_i+d_i))
    ci_lo = np.exp(ln_rr_i - 1.96 * se_i)
    ci_hi = np.exp(ln_rr_i + 1.96 * se_i)

    # (d) Chi-square test
    chi2_i, p_i, _, _ = chi2_contingency([[a_i, b_i], [c_i, d_i]])

    # (e) Store this factor's results
    results.append({
        "factor": factor,
        "RR": round(rr_i, 3),
        "CI_lower": round(ci_lo, 3),
        "CI_upper": round(ci_hi, 3),
        "OR": round(or_i, 3),
        "p-value": round(p_i, 4),
    })

# Assemble into a table, sorted by RR from high to low (most suspicious factors first)
rr_table = pd.DataFrame(results).sort_values("RR", ascending=False)
display_df = rr_table.copy()
display_df["95% CI"] = display_df.apply(
    lambda r: f"{r['CI_lower']:.3f}–{r['CI_upper']:.3f}", axis=1
)
print("=== Multi-Factor Crude Effect-Measure Summary Table ===")
print(display_df[["factor", "RR", "95% CI", "OR", "p-value"]].to_string(index=False))
```

```{raw} html
<div class="video-card">
  <div class="video-title">Video: The Forest Plot—Spotting the Prime Suspect at a Glance</div>
  <div class="youtube-lite" data-id="K8dMlS5lr3A">
    <img src="https://img.youtube.com/vi/K8dMlS5lr3A/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

### The Forest Plot

The **forest plot** is one of the most common charts in epidemiology and evidence-based medicine, often used in systematic reviews and meta-analyses, but it's also very useful in outbreak investigations—it lets you **compare the effect sizes and statistical significance of multiple exposure factors at a glance**.

How to read a forest plot:
- **Dot (●)**: the point estimate (RR in this example)
- **Horizontal line segment (─)**: the 95% confidence interval
- **Dashed line (RR = 1)**: the no-effect line. A CI that crosses the dashed line = not significant; a CI entirely to the right of the dashed line = exposure significantly increases risk

```{figure} images/forest_plot_reading_guide_en.svg
:name: fig-forest-plot-reading-guide
:alt: A guide to reading a forest plot: the dot shows the point estimate, the horizontal line segment shows the 95% CI, and the dashed line shows the RR=1 no-effect line
:width: 100%
```

```python
import pathlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# -- CJK font setup (prevents Chinese labels showing as boxes □□□) --
for _font_dir in map(pathlib.Path, ["/usr/share/fonts", "/usr/local/share/fonts"]):
    if _font_dir.exists():
        for _fp in sorted(_font_dir.rglob("*")):
            if _fp.suffix.lower() in {".ttf", ".ttc", ".otf"} and (
                "CJK" in _fp.name or "WenQuanYi" in _fp.name or "wqy" in _fp.name
            ):
                try:
                    fm.fontManager.addfont(str(_fp))
                except Exception:
                    pass

plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
```

```python
fig, ax = plt.subplots(figsize=(8, 5))
rr_sorted = rr_table.reset_index(drop=True)
y_pos = range(len(rr_sorted))
ax.errorbar(
    rr_sorted["RR"], y_pos,
    xerr=[rr_sorted["RR"] - rr_sorted["CI_lower"],
          rr_sorted["CI_upper"] - rr_sorted["RR"]],
    fmt="o", color="#D97757", ecolor="#6B6B6B", capsize=4, markersize=7,
)
ax.axvline(x=1, color="#6B6B6B", linestyle="--", alpha=0.7, label="RR = 1 (no effect)")
ax.set_yticks(list(y_pos))
ax.set_yticklabels(rr_sorted["factor"])
ax.set_xlabel("Risk Ratio (95% CI)")
ax.set_title("Crude Risk Ratio by Factor (Forest Plot)")
ax.legend(loc="lower right")
ax.invert_yaxis()
plt.tight_layout()
plt.show()
```

---

## Key Points for Interpretation

| Situation | Measure | Interpretation | Plain language |
|------|------|------|--------|
| RR > 1 and CI excludes 1 | RR | Exposure may increase infection risk | Exposed people get sick more easily, and it's unlikely to be a coincidence |
| RR ≈ 1 or CI includes 1 | RR | No significant association between exposure and infection | Exposed or not, the chance of getting sick is about the same |
| RR < 1 and CI excludes 1 | RR | Exposure may be protective | Like a vaccine—exposure actually makes you less likely to get sick |
| p < 0.05 | p-value | Statistically significant (but not causation) | "Doesn't look like a coincidence" ≠ "it must be the cause" |
| Cohort study (complete denominators) | Use **RR** | You can compute risk directly | You know everyone → report RR |
| Case-control study (no complete denominators) | Use **OR** | You can only compute odds | You chose the controls → can only report OR |
| Logistic regression output | **OR** | Model native = log-odds | Running the regression gives an OR, regardless of study design |
| Rare disease (attack rate < 10%) | OR ≈ RR | The two are interchangeable | Few sour candies in the bag → risk ≈ odds |
| High attack rate (> 10%) | OR > RR | OR overestimates the risk multiple | This outbreak is 43% → can only report risk with RR |
| Vaccine effectiveness (cohort) | VE = 1−RR | Computed directly from incidence | RR=0.2 → VE=80% |
| Vaccine effectiveness (case-control) | VE = 1−OR | Computed from the odds ratio | ≈ 1−RR when the disease is rare |
| Multi-factor scan | Crude RR summary table | Quickly screen suspect factors | But watch out for multiple comparisons and confounders |

## Common Mistakes

1. **Looking only at the p-value**: p < 0.05 doesn't mean the effect is large; you have to look at the size of the RR/OR and the width of the CI at the same time. p = 0.001 but RR = 1.01 → statistically significant but clinically meaningless
2. **Ignoring confounders**: a crude RR can be confounded by age, comorbidities, etc. → you need Ch05's stratified analysis
3. **Confusing RR and OR**: report RR for cohort studies, OR for case-control studies. When the attack rate is ~43%, using the OR as a "risk multiple" seriously overestimates! Correct phrasing: "RR = 1.8, the risk is 1.8 times higher"; wrong phrasing: "OR = 3.2, the risk is 3.2 times higher"
4. **Using the OR to say "risk is X times higher"**: the OR measures the multiple of the **odds**, not the risk. Only when the disease is rare (OR ≈ RR) can they be approximately interchanged
5. **Sample size too small**: cells with expected values < 5 should use Fisher's exact test
6. **Equating statistical significance with causation**: association ≠ causation. You also need to consider temporality, dose-response, biological plausibility (Hill's criteria)
7. **The multiple comparisons problem**: testing 8 factors at once, by chance alone you could get ~0.4 false positives (at α=0.05)
8. **Running logistic regression on cohort data but reporting the OR directly**: logistic regression's native output is an OR, but if your data comes from a cohort study with a high attack rate, you should convert it to an RR (Ch06 will teach the method)

## Next Steps

A crude RR / OR is just a preliminary clue—like a detective who has a list of suspects but can't convict anyone yet.

- The RR for shower use looks high, but if **residents who can walk independently have both a high shower-use rate and more exposure opportunities**, then the RR may be inflated by **confounding**—like a burger that looks huge but is really just propped up by lettuce
- **Ch05** will use **stratified analysis** and the **Mantel-Haenszel method** to "control for" confounders and get an adjusted RR
- **Ch06** will use **logistic regression** to adjust for multiple factors at once and compute an adjusted OR (remember: the regression's native output is an OR, and you have to interpret it carefully when the attack rate is high)

From crude association (Ch03) → controlling for confounding (Ch05) → multivariable models (Ch06), this is the standard three-part progression of epidemiological analysis. The same framework applies to vaccine effectiveness studies too—just swap the exposure variable for "vaccinated or not," where RR < 1 means the vaccine is protective.

## Practice Notebooks

- Lesson notes: {ref}`03_stats_basics.ipynb`
- Exercise version: [`03_stats_exercise.ipynb`](exercises/03_stats_exercise.ipynb)
- Solution version (instructor edition): [`03_stats_solution.ipynb`](solutions/03_stats_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/03_stats_solution.ipynb>)
