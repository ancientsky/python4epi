# 05 Stratified Analysis and Confounding

## Scenario

Back in Ch03, we found that shower users had a risk ratio (RR) for infection well above 1. But a senior outbreak investigator raised a challenge:

> "Bedridden residents almost never use the showers, and bedridden residents already have limited mobility and fewer exposure opportunities to begin with. Could the high RR you're seeing just be because **the people who can walk around are also the ones using the showers**?"

This is the problem of **confounding**. Picture this:

> 🌧️ **People who wear raincoats catch colds more often—so does wearing a raincoat give you a cold?**
>
> Of course not! It's because **rainy days** make you both put on a raincoat (the exposure) and catch a cold more easily (the outcome). "Rainy day" is the **confounder** hiding in the background, muddling your judgment.

In our nursing home case, "functional status" is that "rainy day"—it affects both whether a resident uses the shower and the resident's infection risk. This chapter teaches you how to spot a confounder, use stratified analysis to "control" for it, and then apply the Mantel-Haenszel method to obtain an adjusted RR.

## What You Will Learn

- What a confounder is and its three requirements
- How to use a DAG (directed acyclic graph) to identify confounding paths
- How to perform stratified analysis
- Forest plot visualization of stratum-specific RRs
- Mantel-Haenszel weighted RR and the test of homogeneity
- How to interpret crude RR vs. adjusted RR (with a quantitative decision rule)

## 🔍 Super Simple Special: Understanding Stratified Analysis with "Do Kids with Bigger Feet Read Better?"

> Do "stratified analysis," "confounder," and "Mantel-Haenszel" sound like three spells from a wizard's book? Don't be scared. This section sets the nursing home aside for a moment and tells a little story where **you'll spot something fishy at a glance**—walking through the whole idea in a way that'll make even a 7th grader slap the table and shout "OH, I get it now!" Once you're done, go back and look at the DAG and forest plot below—it'll click.

### A finding that sounds super convincing... and is actually super suspicious

Say someone goes to an elementary school, measures every kid's **foot size**, and tests whether they **can read**. Here's what they find:

> **Kids with big feet: 68% can read. Kids with small feet: only 32% can read. Risk ratio (RR) ≈ 2.1!**

If you took that number at face value, you'd conclude—**"Bigger feet make you better at reading, so buy your kid bigger shoes to make them smarter?"** Something's clearly off. That's right: the RR is a **real number, correctly calculated**, but the **causal story behind it is fake**. So what's going on?

### The real culprit is hiding behind the scenes: it's "age" pulling the strings

Think about it: **a 10-year-old naturally has bigger feet than a 6-year-old, and is also naturally better at reading.** In other words, there's something that **simultaneously** makes a kid's "feet bigger" and makes them "better at reading"—and that something is **age**.

- It's not that big feet make you read better—it's that **being older** makes "big feet" and "can read" happen together.
- Foot size and reading ability actually have **no causal relationship** at all. They just both **get dragged along by age**, which makes them look like they're holding hands.

This character hiding in the background—pulling the strings on both the exposure (foot size) and the outcome (reading), and tricking us into a wrong conclusion—is called a **confounder**. Here, the confounder is **age**.

```{figure} images/confounding_shoe_size_en.svg
:name: fig-confounding-shoe-size
:alt: The illusion of big feet and reading ability: lumped together, the big-feet group reads at 68% and the small-feet group at 32% (crude RR≈2.1), but the real culprit is age; split by age, both the 6-year-old and 10-year-old groups show 20% and 80% reading rates respectively regardless of foot size, meaning foot size makes no difference at all
:width: 100%

Top left: lumped together, big feet look like they go with better reading (an illusion); top right: the real culprit "age" pulls the strings on both foot size and reading ability; bottom row: **split by age**, foot size makes no difference at all within the same age group.
```

### Cracking the case: split it apart by age—this is stratified analysis

Since we suspect age is pulling the strings, let's **hold age constant**: instead of lumping 6-year-olds and 10-year-olds together, let's **compare kids of the same age against each other**.

- **Looking only at 6-year-olds**: big feet read at 20%, small feet also 20%—**identical!**
- **Looking only at 10-year-olds**: big feet read at 80%, small feet also 80%—**still identical!**

As long as age is held the same, foot size makes **absolutely no difference** (the RR in every stratum = 1.0). That 2.1 "illusion" vanishes instantly.

This approach—**"splitting everyone into groups based on some variable (each group is called a 'stratum'), then comparing within each group separately"**—is called **stratified analysis**. Here, we're **stratifying by age**.

### Why do you even need to bother? (What happens if you don't)

Because the **"crude" lumped-together number will deceive you**. Without stratifying:

- You'd **convict an innocent bystander** (blaming foot size) and **let the real culprit walk free** (missing that it's actually age).
- Translated to a real outbreak investigation: you might think "showering" is dangerous and order a **blanket ban on showers**, only to find it was a waste of effort, because the real key factor was actually "functional status." **Adjusting for confounding exists precisely so you don't waste your energy on the wrong target or give the wrong infection-control advice.**

### How do you combine the strata into "one" answer? Mantel-Haenszel weighting

Once you've stratified, each stratum has its own RR (here, both strata happen to be exactly 1.0). Usually you want **one** summary number, so you use a **Mantel-Haenszel (MH) weighted average** to combine the stratum-specific RRs, weighted by sample size, into an **adjusted RR**.

Then you put the two numbers side by side:

- **Crude RR = 2.1** (the deceptive version, not split by age)
- **Adjusted RR = 1.0** (the honest version, split by age)

The two are miles apart → this proves **age really was confounding the result**. In practice there's an easy rule of thumb: **if the crude RR and adjusted RR differ by ≥ 10%, that counts as confounding** (the change-in-estimate rule).

### Try it yourself: catch this confounder with your own two hands

```python
# A "shoe size x can read" line list, split into two strata by age
# a=big feet & can read, b=big feet & can't read, c=small feet & can read, d=small feet & can't read
strata = {
    "Age 6":  dict(a=4,  b=16, c=16, d=64),   # at this age, everyone's reading rate is low (20%)
    "Age 10": dict(a=64, b=16, c=16, d=4),    # at this age, everyone's reading rate is high (80%)
}

def rr_2x2(a, b, c, d):
    """Risk ratio of reading ability: big feet vs. small feet"""
    return (a / (a + b)) / (c / (c + d))

# (1) All mixed together (crude RR) -- not yet split by age
A = sum(s["a"] for s in strata.values())
B = sum(s["b"] for s in strata.values())
C = sum(s["c"] for s in strata.values())
D = sum(s["d"] for s in strata.values())
crude = rr_2x2(A, B, C, D)
print(f"Crude RR (not split by age) = {crude:.2f}"
      f"  ->  big feet read {A/(A+B):.0%}, small feet {C/(C+D):.0%}")

# (2) Split by age (stratified) -- within the same age, is there still a gap?
for name, s in strata.items():
    print(f"  {name}: RR = {rr_2x2(**s):.2f}")

# (3) Combine the strata into one "adjusted" answer: Mantel-Haenszel weighted RR
num = den = 0
for s in strata.values():
    n = s["a"] + s["b"] + s["c"] + s["d"]
    num += s["a"] * (s["c"] + s["d"]) / n
    den += s["c"] * (s["a"] + s["b"]) / n
mh = num / den
print(f"Mantel-Haenszel adjusted RR = {mh:.2f}")

# (4) How far apart are the crude and adjusted RR? A gap >= 10% means confounding
change = abs(crude - mh) / mh * 100
print(f"Crude RR {crude:.2f} vs. adjusted {mh:.2f}, a {change:.0f}% difference -> age is a confounder!")
```

Run it and you'll see:

```text
Crude RR (not split by age) = 2.12  ->  big feet read 68%, small feet 32%
  Age 6: RR = 1.00
  Age 10: RR = 1.00
Mantel-Haenszel adjusted RR = 1.00
Crude RR 2.12 vs. adjusted 1.00, a 112% difference -> age is a confounder!
```

In just a few lines, you've walked through the entire logic of stratified analysis: **look at the crude RR → check each stratum separately → combine them into an MH-adjusted RR → compare how far apart they are**. Congratulations—this is exactly what Steps 4–7 of this chapter are doing!

### Confounding vs. effect modification: a super easy fork to mix up

After stratifying, always take one more look: **how similar are the RRs across strata?** This sends you down one of two completely different paths:

| What you observe | What it means... | How to report it |
|---|---|---|
| Stratum RRs are **close to each other** (both 1.0), but **very different from the crude RR** (2.1) | **Confounding** | Report **one** adjusted RR |
| Stratum RRs are **very different from each other** (e.g., age 6 RR=1.0, age 10 RR=3.0) | **Effect modification** | **Don't combine them**—report each stratum separately, because the effect genuinely differs by group |

To tell which one you're dealing with, statisticians use a **test of homogeneity**: it tests whether "the stratum RRs are all consistent." Our big-feet example is the **former case**—the strata agree with each other (both 1.0), and the whole thing was just confounded by age, so combining into one adjusted RR is the right call.

### Cheat sheet for reading the numbers (save this)

| What you see... | What it means |
|---|---|
| Crude RR is clearly ≠ 1 | Don't jump to conclusions yet—a confounder might be pulling the strings |
| After stratifying, every stratum RR becomes ≈ 1 | The original association was an illusion, confounded by that stratifying variable |
| Crude RR vs. adjusted RR differ by ≥ 10% | Confounding confirmed → report the **adjusted** number |
| Stratum RRs are close to each other | It's confounding → combine into one adjusted RR |
| Stratum RRs are very different from each other | It's effect modification → report each stratum separately, don't combine |
| An arrow on the DAG points to both exposure and outcome | That source variable is a confounder suspect |
| Forest plot dots roughly line up across strata | The effect is consistent (homogeneous) across strata → MH pooling is fine |

### Back to reality: reading ability → infection

Now swap the characters in the story for the nursing home version:

| Big-feet story | Real nursing home case |
|---|---|
| Foot size (exposure) | Whether the resident used the **shower** (`shower_use`) |
| Can read or not (outcome) | Whether infected with Legionnaires' disease |
| Age (confounder) | **Functional status** (`functional_status`, i.e., mobility) |
| Split by age | **Stratify by functional status** |

Every trick you just learned from the big-feet story—look at the crude RR, stratify, MH-adjust, compare how much they differ, tell confounding apart from effect modification—**is exactly what Steps 1–8 of this chapter do with the nursing home data**. Now scroll down and look at that DAG, those 2x2 tables, and the forest plot again—doesn't it suddenly feel a lot friendlier? 😉

---

## Core Concepts

### The Three Requirements of a Confounder

For a variable C to be considered a confounder, it must **simultaneously satisfy** all three of the following conditions—missing even one disqualifies it:

1. **C is associated with the exposure**: e.g., functional status affects whether a resident uses the shower (only people who can walk get into the shower room)
2. **C is associated with the outcome**: e.g., functional status affects infection risk (people who can walk have a wider range of movement and more chances to encounter water mist)
3. **C is not an intermediate variable**: C is not a "way station" on the causal path from exposure to outcome. For example, "amount of water mist inhaled" is an intermediate step on the shower→infection path and must not be treated as a confounder to control for

> 🧪 **Memory aid**: A confounder is like a "double agent"—it mixes into both the exposure group and the outcome group, tricking you into thinking exposure and outcome are related (or exaggerating/shrinking the true relationship). All three conditions are essential; skip verifying even one and you may "wrongly convict an innocent" or "let the culprit go free."

<!-- video: ch05_01_confounder_concept -->
<!-- /video -->

### How Do You Discover Potential Confounders?

Our story opened with a "senior outbreak investigator" drawing on experience to suggest that functional status might be a confounder. But you can't rely on senior staff every time—is there a more systematic method? In fact, there are several routes you can take:

| Method | How it works | Advantage | Limitation |
|------|------|------|------|
| **Literature review** | Search papers from similar past outbreak investigations to see which confounders others controlled for | Stand on the shoulders of predecessors; don't miss known confounders | A novel disease may have no precedent |
| **Draw a DAG** | Draw a causal diagram based on domain knowledge and find all the "back-door paths" | Logically clear; can distinguish confounders vs. intermediate variables | Requires a basic understanding of the causal mechanism |
| **Statistical screening** | Check whether a candidate variable is significantly associated with both the exposure and the outcome (confounder requirements #1 + #2) | Backed by data, not purely intuition | Statistical significance ≠ causation; may miss weak but real confounding |
| **Change-in-estimate** | Add/remove the candidate variable in a model and see whether the exposure's effect measure (RR or OR) changes by ≥ 10% | Directly answers "is it confounding or not" | Requires a regression model first (→ Ch06) |
| **Expert consultation** | Consult clinicians, infection-control staff, and senior epidemiologists | Captures practical factors that statistics and literature miss | Subjective; may have omissions |

```{tip}
**In practice, we recommend a three-pronged approach: "literature + DAG + statistical screening."** First review the literature to draw up a candidate list → draw a DAG to mark causal directions → use data to verify the three confounder requirements. Finally, have senior staff review it to see if anything was missed. Don't rely on just one method, and don't rely on intuition alone.
```

### DAG (Directed Acyclic Graph)

A DAG is a "map of causal relationships" that uses arrows to show "who affects whom." Drawing a DAG lets you see at a glance where the confounder is hiding:

```{figure} images/confounding_dag_en.svg
:name: fig-confounding-dag
:alt: Confounder DAG showing functional status affecting both shower use and infection risk
:width: 100%

DAG illustration: functional status (C) affects both shower use (exposure) and infection risk (outcome). If you don't control for C, the RR for showering gets inflated. The raincoat analogy at the bottom right helps you remember the logic of confounding.
```

From the DAG you can see two paths:
- **Direct path** (the one we want to study): shower use → infection
- **Back-door path** (the confounding path): shower use ← functional status → infection

The back-door path is like a classmate next to you copying your answers during an exam—their score (the outcome) looks related to yours (the exposure), but really it's because of the common cause of "sitting next to you" (the confounder). Stratified analysis separates "those sitting next to you" from "those not sitting next to you," eliminating this spurious association.

<!-- video: ch05_02_dag -->
<!-- /video -->

### The Logic of Stratified Analysis

> 🍳 **The fried-egg analogy**: You want to know "whether frying an egg in olive oil burns it less," but every time you use olive oil you happen to use low heat, and every time you use salad oil you happen to use high heat. The result makes it look like olive oil burns less—but is it really the oil? 
>
> **What stratified analysis does**: compare low heat and high heat separately. Within the low-heat group, compare olive oil vs. salad oil; do the same within the high-heat group. Now the heat level (the confounder) is "locked down," and the difference you see is the oil's true effect.

Concretely: stratify the data by the confounder (e.g., split into three groups by functional status—ambulatory, wheelchair, bedridden), and compute the RR within each stratum. If every stratum-specific RR is smaller than the crude RR, that means the crude RR was indeed inflated by confounding.

### The Mantel-Haenszel Method

After stratifying, we need a "fair way to combine"—we can't just take a simple average, because the strata have different numbers of people. The Mantel-Haenszel (MH) method gives each stratum a weight (depending on that stratum's sample size) and computes a weighted "adjusted RR":

$$RR_{MH} = \frac{\sum_i \frac{a_i \cdot (c_i + d_i)}{N_i}}{\sum_i \frac{c_i \cdot (a_i + b_i)}{N_i}}$$

> 📊 **In plain language**: it's like a semester grade—you can't just average quizzes and the final exam; the final should count for more. The MH method decides the weights based on "how many people are in each stratum": strata with more people carry more influence, strata with fewer people carry less.

---

## Step 1: Data Preparation

This Step loads the raw line list and builds the `infected` column that the rest of the chapter depends on—every RR and every stratum from here on is built on top of this one column.

```python
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from epi_learning.metrics import risk_ratio

# --- Load the nursing home data ---
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# Anyone whose clinical_severity is not "not_ill" counts as infected
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `from epi_learning.metrics import risk_ratio` | Imports the risk-ratio helper we'll reuse throughout the chapter (the same tool built back in Ch03) |
> | `df = pd.read_csv(...)` | Loads the line list for all 280 residents |
> | `df["clinical_severity"] != "not_ill"` | Boolean test: anything other than "not ill" counts as infected |
> | `.astype(int)` | Converts `True`/`False` into `1`/`0`, so it can be used as a `pd.crosstab` column, summed, and fed into the RR formula |
>
> 🔑 **`infected` is the foundation of the whole chapter**: every crude RR, stratum RR, and MH-adjusted RR in Steps 2–8 is built from this single 0/1 column.

## Step 2: Recap of the Crude RR

First compute a crude RR "without controlling for any confounder" as the baseline for later comparisons:

```python
# --- 2×2 cross-tabulation: shower use vs. infection ---
ct = pd.crosstab(df["shower_use"], df["infected"])
a = int(ct.loc[1, 1])   # showered, infected
b = int(ct.loc[1, 0])   # showered, not infected
c = int(ct.loc[0, 1])   # no shower, infected
d = int(ct.loc[0, 0])   # no shower, not infected

crude_rr = risk_ratio(a, a + b, c, c + d)
print(f"Crude RR (shower_use -> infected) = {crude_rr:.3f}")
```

> 💡 **`pd.crosstab` builds the 2×2 table for you**: `ct.loc[1, 1]` indexes row-then-column, pulling out the count for "showered and infected"; once all four cells are in hand, they go straight into the `risk_ratio()` helper from Ch03—no manual arithmetic needed.

## Step 3: Check the Three Confounder Requirements

Before stratifying, verify that "functional status" really meets the three conditions of a confounder. Skip verifying one and you may be doing all the work for nothing:

<!-- video: ch05_03_verify_criteria -->
<!-- /video -->

```python
# --- Condition 1: Is functional status associated with shower use? ---
# normalize="index" makes each row sum to 1, so we see proportions
print("=== Functional status x Shower use ===")
print(pd.crosstab(df["functional_status"], df["shower_use"],
                  margins=True, normalize="index").round(3))

# --- Condition 2: Is functional status associated with infection? ---
print("\n=== Functional status x Infection ===")
print(pd.crosstab(df["functional_status"], df["infected"],
                  margins=True, normalize="index").round(3))

# Condition 3 (judged by logic): functional status is not an intermediate step
# on the shower->infection path
# (a person does not become ambulatory because they "used the shower first"
#  -- the causal direction is wrong)
# -> All three conditions are met, so we can proceed to stratified analysis
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `pd.crosstab(df["functional_status"], df["shower_use"], ...)` | Cross-tab: within each functional status, what proportion did/didn't use the shower—this checks confounder **requirement #1** |
> | `normalize="index"` | Makes each row (each functional status) sum to 1, so you read proportions instead of raw counts |
> | `margins=True` | Prints an extra "All" row/column for the overall total, useful for comparison |
> | `pd.crosstab(df["functional_status"], df["infected"], ...)` | The same technique checks the association between functional status and infection—**requirement #2** |
> | The comment for condition 3 (no code) | Requirement 3 ("not an intermediate variable") is a **logical judgment**, not something you compute—it relies on reasoning about causal direction, not a number |
>
> 🧭 **Only two of the three requirements can be backed up with `pd.crosstab`**: requirements #1 and #2 show up in the numbers, but #3 always depends on understanding the causal mechanism—no statistic can answer it for you.

## Step 4: Stratified Analysis

> This is the core step of the whole chapter—split the data by functional status (ambulatory, wheelchair, bedridden) into three strata, and within each stratum compute the RR and 95% confidence interval.

<!-- video: ch05_04_stratified_rr -->
<!-- /video -->

```python
# --- Stratify by functional_status, computing RR + 95% CI in each stratum ---
strata = df["functional_status"].unique()
stratum_results = []

for s in sorted(strata):
    sub = df[df["functional_status"] == s]
    ct_s = pd.crosstab(sub["shower_use"], sub["infected"])

    # Some strata may have only the exposed or only the unexposed group -> skip
    if ct_s.shape != (2, 2):
        continue

    # Extract a, b, c, d from the four-fold table
    a_s = int(ct_s.loc[1, 1])
    b_s = int(ct_s.loc[1, 0])
    c_s = int(ct_s.loc[0, 1])
    d_s = int(ct_s.loc[0, 0])
    n_s = a_s + b_s + c_s + d_s

    rr_s = risk_ratio(a_s, a_s + b_s, c_s, c_s + d_s)

    # --- 95% confidence interval (using the log-transform method) ---
    ln_rr = np.log(rr_s)
    se = np.sqrt(1/a_s - 1/(a_s+b_s) + 1/c_s - 1/(c_s+d_s))
    ci_lo = np.exp(ln_rr - 1.96 * se)
    ci_hi = np.exp(ln_rr + 1.96 * se)

    stratum_results.append({
        "stratum": s,
        "n": n_s,
        "a": a_s, "b": b_s, "c": c_s, "d": d_s,
        "RR": rr_s,
        "CI_lower": ci_lo,
        "CI_upper": ci_hi,
    })

results_df = pd.DataFrame(stratum_results)

# --- Print the results for each stratum ---
print("=== Stratum-specific RR ===")
for _, row in results_df.iterrows():
    print(f"  {row['stratum']:20s}  RR={row['RR']:.3f}  "
          f"(95% CI: {row['CI_lower']:.3f}-{row['CI_upper']:.3f})  n={row['n']}")

print(f"\n  Crude RR = {crude_rr:.3f}")
```

> **Line-by-line** (the loop is a bit long, but every iteration does exactly what Ch03 did for a single RR):
>
> | This line | What it does |
> |---|---|
> | `strata = df["functional_status"].unique()` | Finds the distinct functional-status categories to loop over |
> | `for s in sorted(strata):` | Runs one iteration of the loop per stratum |
> | `sub = df[df["functional_status"] == s]` | Filters down to just the residents in this stratum |
> | `if ct_s.shape != (2, 2): continue` | Skips a stratum that's missing the exposed or unexposed group (table isn't 2×2), avoiding a crash |
> | `rr_s = risk_ratio(a_s, a_s + b_s, c_s, c_s + d_s)` | Computes this stratum's own RR |
> | `ln_rr = np.log(rr_s)` | The CI formula works on log(RR) (its sampling distribution is closer to normal) |
> | `se = np.sqrt(1/a_s - 1/(a_s+b_s) + 1/c_s - 1/(c_s+d_s))` | The standard error formula for log(RR) |
> | `ci_lo/ci_hi = np.exp(ln_rr ± 1.96 * se)` | After computing the CI on the log scale, `np.exp()` converts it back to the RR scale |
> | `stratum_results.append({...})` | Stores this stratum's n, a, b, c, d, RR, and CI into a list |
> | `results_df = pd.DataFrame(stratum_results)` | Once the loop finishes, turns the list into a tidy table for Steps 5–7 to use |
>
> 🔑 **Don't drop the `if ct_s.shape != (2, 2): continue` line**: if even one stratum happens to have no exposed or no unexposed group (e.g., everyone in it used the shower), `.loc[1,1]`-style indexing crashes immediately—this is one of the most common traps in stratified analysis.

## Step 5: Forest Plot

A forest plot puts each stratum's RR and confidence interval on a single chart, so you can see at a glance the effect size and precision of each stratum:

<!-- video: ch05_05_stratified_forest_plot -->
<!-- /video -->

```python
import matplotlib.pyplot as plt

# -- CJK font setup (prevents Chinese labels from showing as boxes) --
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
plt.style.use("ggplot")
plt.rcParams["figure.dpi"] = 150

fig, ax = plt.subplots(figsize=(8, 4))
y_pos = range(len(results_df))

# --- Each stratum's RR ± 95% CI ---
ax.errorbar(
    results_df["RR"], y_pos,
    xerr=[results_df["RR"] - results_df["CI_lower"],
          results_df["CI_upper"] - results_df["RR"]],
    fmt="o", color="#2c7fb8", capsize=4, markersize=8,
)
# RR=1 reference line (dashed): if the CI crosses 1, it is not statistically significant
ax.axvline(x=1, color="gray", linestyle="--", alpha=0.5)
# Crude RR reference line (red dotted)
ax.axvline(x=crude_rr, color="red", linestyle=":", alpha=0.7, label=f"Crude RR={crude_rr:.2f}")
ax.set_yticks(y_pos)
ax.set_yticklabels(results_df["stratum"])
ax.set_xlabel("Risk Ratio (RR)")
ax.set_title("Stratified analysis forest plot: shower use -> infection (stratified by functional status)")
ax.legend()
plt.tight_layout()
plt.show()
```

> 💡 **The forest plot is just Step 4's `results_df` drawn on a chart**: `ax.errorbar`'s `xerr` gives the distance from the RR down to the CI lower bound and up to the CI upper bound; `axvline(x=1)` marks the "no association" reference line, and `axvline(x=crude_rr)` overlays the crude RR for comparison—if a stratum's horizontal line never crosses the gray dashed line, that stratum is statistically significant.

## Step 6: Mantel-Haenszel Weighted RR

This step takes Step 4's per-stratum results and pools them with the Mantel-Haenszel formula into a single adjusted RR—strata with more people get more weight, strata with fewer people get less.

<!-- video: ch05_06_mantel_haenszel -->
<!-- /video -->

```python
# --- Mantel-Haenszel weighted pooling ---
# Principle: strata with more people get more weight, strata with fewer get less
numerator = 0
denominator = 0

for _, row in results_df.iterrows():
    a_i, b_i, c_i, d_i = row["a"], row["b"], row["c"], row["d"]
    n_i = a_i + b_i + c_i + d_i
    numerator += a_i * (c_i + d_i) / n_i
    denominator += c_i * (a_i + b_i) / n_i

rr_mh = numerator / denominator

print(f"Mantel-Haenszel adjusted RR = {rr_mh:.3f}")
print(f"Crude RR                    = {crude_rr:.3f}")
print(f"Difference                  = {crude_rr - rr_mh:.3f}")

# --- Use the 10% rule to judge whether confounding is present ---
change_pct = abs(crude_rr - rr_mh) / rr_mh * 100
print(f"Magnitude of change = {change_pct:.1f}%")
if change_pct >= 10:
    print("-> Change >= 10%, the crude RR was affected by confounding!")
    if crude_rr > rr_mh:
        print("  Direction of confounding: inflation (crude RR is too high)")
    else:
        print("  Direction of confounding: suppression (crude RR is too low)")
else:
    print("-> Change < 10%, confounding is not notable")
```

> **Line-by-line** (compare each line against the MH formula in Core Concepts above):
>
> | This line | What it does |
> |---|---|
> | `for _, row in results_df.iterrows():` | Pulls out each stratum's saved results from Step 4, accumulating one at a time |
> | `n_i = a_i + b_i + c_i + d_i` | This stratum's total sample size, the basis for its weight |
> | `numerator += a_i * (c_i + d_i) / n_i` | Accumulates the MH formula's numerator, one stratum at a time |
> | `denominator += c_i * (a_i + b_i) / n_i` | Accumulates the MH formula's denominator |
> | `rr_mh = numerator / denominator` | Only after every stratum is summed does it divide **once** to get the single adjusted RR |
> | `change_pct = abs(crude_rr - rr_mh) / rr_mh * 100` | How many percent the crude RR and adjusted RR differ—compared against the 10% rule from Core Concepts |
> | `if change_pct >= 10:` | Applies the threshold to judge confounding, printing "inflation" or "suppression" depending on direction |
>
> ⚠️ **Don't divide too early inside the loop**: the MH formula sums each stratum's numerator and denominator separately first, and only divides **once** at the very end—computing `a_i*(c_i+d_i) / c_i*(a_i+b_i)` per stratum and averaging those would NOT give the correct MH-weighted value.

## Step 7: Test of Homogeneity—Is There Interaction?

Eyeballing whether the stratum RRs look similar isn't precise enough; this step uses a simplified numeric check of homogeneity to decide whether the strata can be pooled into a single MH value.

> 🍜 **The spicy hotpot analogy**: You're investigating "whether eating spicy hotpot causes diarrhea," and you split people into "strong-stomached" and "weak-stomached" groups. If the strong-stomached group has RR=1.2 and the weak-stomached group has RR=4.5—this isn't confounding, it's **interaction** (effect modification): the effect of spicy hotpot "varies from person to person." In that case you can't just report a single pooled RR; you must report them separately: "For strong-stomached people the effect is small; weak-stomached people should be careful."

<!-- video: ch05_07_effect_modification -->
<!-- /video -->

```python
# --- Test of homogeneity (simplified Breslow-Day) ---
# See whether the stratum-specific RRs are similar -> decide whether to pool the report
rr_values = results_df["RR"].values
rr_range = rr_values.max() - rr_values.min()

print(f"Range of stratum-specific RRs: {rr_values.min():.3f} - {rr_values.max():.3f}")
print(f"RR spread: {rr_range:.3f}")

if rr_range > 0.5:
    print("-> The stratum-specific RRs differ substantially; effect modification may be present")
    print("  Recommend reporting each stratum's RR separately, not just the pooled RR_MH")
else:
    print("-> The stratum-specific RRs are similar; the MH weighted pooled value is reasonable to use")
    print("  Reporting a single RR_MH is enough to represent the overall effect")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `rr_values = results_df["RR"].values` | Pulls Step 4's stratum RRs out into an array |
> | `rr_range = rr_values.max() - rr_values.min()` | This chapter's **simplified** homogeneity check: max RR minus min RR—the bigger the spread, the more the strata disagree |
> | `if rr_range > 0.5:` | Uses 0.5 as the cutoff—above it, suspect interaction and don't report just one MH value |
>
> ⚠️ **This is a simplified check, not a formal statistical test**: a proper test of homogeneity would use Breslow-Day or Woolf's test to get a p-value; the 'RR range' method here is a quick eyeball check—do both for a real report.

---

## Interpretation Highlights

After finishing the stratified analysis, you need to answer two questions. The flowchart below helps you decide:

```{figure} images/stratified_interpretation_en.svg
:name: fig-stratified-interpretation
:alt: Stratified analysis interpretation flowchart explaining how to judge confounding and interaction
:width: 100%

Stratified analysis interpretation flowchart: first ask "is there confounding?" (compare crude RR vs. adjusted RR), then ask "is there interaction?" (compare the differences among the stratum-specific RRs).
```

### Question One: Is There Confounding?

Compare the **crude RR** and the **adjusted RR** (MH weighted), using the **10% rule** to decide:

$$\text{Magnitude of change} = \frac{|\text{crude RR} - \text{adjusted RR}|}{\text{adjusted RR}} \times 100\%$$

| Situation | Judgment | Plain language | Example |
|------|------|--------|------|
| Change ≥ 10% and crude RR > adjusted RR | The confounder **inflated** the effect | The burger looks huge; only after removing the lettuce do you see how thick the patty really is | Crude RR=2.5 → adjusted RR=1.8 |
| Change ≥ 10% and crude RR < adjusted RR | The confounder **suppressed** the effect | An ice cube is pressing on the thermometer; remove it to see the true temperature | Crude RR=1.2 → adjusted RR=1.8 |
| Change < 10% | Confounding is **not notable** | With or without lettuce it's about the same size → no need to worry too much | Crude RR=1.80 → adjusted RR=1.75 |

> 💡 **Why 10%?** This is an epidemiological convention, not a statistical test. Some textbooks use 5% or 15%, but 10% is the most widely used. The point is "is the change big enough to affect your conclusion?"

### Question Two: Is There Interaction (Effect Modification)?

Compare whether the **stratum-specific RRs** are similar to one another:

| Situation | Judgment | Plain language | How to report |
|------|------|--------|----------|
| Stratum RRs are similar, CIs overlap, homogeneity p > 0.05 | **No** interaction | No matter which group of people, the exposure's effect is about the same | Report a single RR_MH |
| Stratum RRs differ greatly, CIs don't overlap, p ≤ 0.05 | **Has** interaction | The effect of exposure varies from person to person—large for some, small for others | Report each stratum's RR separately |

> ⚠️ **Interaction ≠ confounding**: confounding is an "illusion"—the effect changes after you control for it; interaction is a "real phenomenon"—different populations genuinely respond differently to the exposure. If there is interaction, pooling it into a single number would actually **lose important information**.

---

## Step 8: A Second Example — Stratifying by Floor

Using the same method, let's practice with a different stratifying variable (floor):

```python
# --- Stratified analysis by floor ---
print("=== Stratified analysis by floor: shower -> infection ===")

for floor in sorted(df["floor"].unique()):
    sub = df[df["floor"] == floor]
    ct_f = pd.crosstab(sub["shower_use"], sub["infected"])
    if ct_f.shape != (2, 2):
        continue
    a_f, b_f = int(ct_f.loc[1, 1]), int(ct_f.loc[1, 0])
    c_f, d_f = int(ct_f.loc[0, 1]), int(ct_f.loc[0, 0])
    rr_f = risk_ratio(a_f, a_f + b_f, c_f, c_f + d_f)
    print(f"  {floor}F: RR={rr_f:.3f}  (shower: {a_f}/{a_f+b_f}, "
          f"no shower: {c_f}/{c_f+d_f})")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `for floor in sorted(df["floor"].unique()):` | Swaps in **floor** as the stratifying variable, repeating Step 4's exact logic |
> | `sub = df[df["floor"] == floor]` | Filters down to just the residents on this floor |
> | `if ct_f.shape != (2, 2): continue` | Same safeguard: skip this floor if it's missing the exposed or unexposed group |
> | `rr_f = risk_ratio(a_f, a_f + b_f, c_f, c_f + d_f)` | Computes this floor's own RR |
>
> 🔑 **Almost identical to Step 4**—just swap `functional_status` for `floor`. The stratified-analysis logic is directly reusable; plug in a different stratifying variable and rerun it.

---

## Supplement: Can Case-Control Studies Also Use Stratified Analysis?

So far, our nursing home data is a **cohort study**—all 280 residents are on the follow-up roster, and we used attack rates to compute RR. But what if it were a **case-control study** instead?

> 🏥 **Scenario**: Suppose there were too many infected people to follow everyone, so you could only pick 121 infected people (cases) and 159 uninfected people (controls), then ask them retrospectively whether they had used the shower. In that case you can't compute an attack rate (because you deliberately selected people rather than following the whole population), so you **can't compute an RR—only an OR (odds ratio)**.

Good news: **the logic of stratified analysis is exactly the same**—still verify the three requirements, still stratify by the confounder, still pool with Mantel-Haenszel. The only difference is:

<!-- video: ch05_08_case_control_mh -->
<!-- /video -->

| | Cohort study (this chapter) | Case-control study |
|---|---|---|
| **Effect measure** | RR (risk ratio) | OR (odds ratio) |
| **Per-stratum calculation** | $RR_i = \frac{a_i/(a_i+b_i)}{c_i/(c_i+d_i)}$ | $OR_i = \frac{a_i \cdot d_i}{b_i \cdot c_i}$ |
| **MH pooling formula** | $RR_{MH} = \frac{\sum a_i(c_i+d_i)/N_i}{\sum c_i(a_i+b_i)/N_i}$ | $OR_{MH} = \frac{\sum a_i d_i / N_i}{\sum b_i c_i / N_i}$ |
| **Judging confounding** | Compare crude RR vs. adjusted RR (10% rule) | Compare crude OR vs. adjusted OR (10% rule) |

```{tip}
**Mnemonic**: cohort study → stratify → MH adjusted **RR**; case-control → stratify → MH adjusted **OR**. Same method, just a different effect measure.

If your case-control data has a very low attack rate (< 10%), then OR ≈ RR and the two are nearly identical. But if it's like our nursing home (attack rate 43%), the OR will clearly overestimate—which is exactly a key point Ch06 will explore in depth.
```

---

## Common Mistakes

1. **Stratifying without verifying the three confounder requirements**: jumping straight to stratifying without checking whether C is really associated with both the exposure and the outcome. It's like a detective arresting someone without evidence—you might arrest the wrong person (control for a variable you shouldn't have) and make the result even more biased
2. **Stratifying too finely, with too few people per stratum**: if a stratum has only 5 people, the computed RR will be extremely unstable (the confidence interval will be super wide). Rule of thumb: at least 10–20 people per stratum
3. **Reporting only the pooled MH value when interaction is present**: when stratum RRs differ greatly (e.g., 1.2 vs. 4.5), reporting a single pooled RR = 2.8 makes people think "the effect is 2.8 for everyone"—completely misleading
4. **Controlling for only one confounder**: stratified analysis can control for only one variable at a time. What if you have several confounders at once—age, functional status, comorbidities? → Ch06's multivariable analysis (Modified Poisson + logistic regression) can adjust for many variables simultaneously

## Next Step

Stratified analysis can control for only one confounder at a time. But what if you have several confounders at once—age, functional status, comorbidities? Ch06's **Modified Poisson regression** can adjust for all variables at once and directly compute an **adjusted RR**—still using the risk ratio we're familiar with. At the same time, it uses logistic regression as a comparison so you can see how much the OR overestimates at a high attack rate. It's like upgrading from "locking down one variable at a time" to "locking down a dozen at once."

## Workbook

- Lecture notes: {ref}`05_stratified_analysis.ipynb`
- Exercise version: [`05_stratified_exercise.ipynb`](exercises/05_stratified_exercise.ipynb)
- Solution version (instructor edition): [`05_stratified_solution.ipynb`](solutions/05_stratified_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/05_stratified_solution.ipynb>)
