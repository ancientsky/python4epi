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

## Core Concepts

### The Three Requirements of a Confounder

For a variable C to be considered a confounder, it must **simultaneously satisfy** all three of the following conditions—missing even one disqualifies it:

1. **C is associated with the exposure**: e.g., functional status affects whether a resident uses the shower (only people who can walk get into the shower room)
2. **C is associated with the outcome**: e.g., functional status affects infection risk (people who can walk have a wider range of movement and more chances to encounter water mist)
3. **C is not an intermediate variable**: C is not a "way station" on the causal path from exposure to outcome. For example, "amount of water mist inhaled" is an intermediate step on the shower→infection path and must not be treated as a confounder to control for

> 🧪 **Memory aid**: A confounder is like a "double agent"—it mixes into both the exposure group and the outcome group, tricking you into thinking exposure and outcome are related (or exaggerating/shrinking the true relationship). All three conditions are essential; skip verifying even one and you may "wrongly convict an innocent" or "let the culprit go free."

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: The three requirements of a confounder—who counts as an accomplice</div>
  <div class="youtube-lite" data-id="2ZF6K8ylvtI">
    <img src="https://img.youtube.com/vi/2ZF6K8ylvtI/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

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

```{figure} images/confounding_dag.svg
:name: fig-confounding-dag
:alt: Confounder DAG showing functional status affecting both shower use and infection risk
:width: 100%

DAG illustration: functional status (C) affects both shower use (exposure) and infection risk (outcome). If you don't control for C, the RR for showering gets inflated. The raincoat analogy at the bottom right helps you remember the logic of confounding.
```

From the DAG you can see two paths:
- **Direct path** (the one we want to study): shower use → infection
- **Back-door path** (the confounding path): shower use ← functional status → infection

The back-door path is like a classmate next to you copying your answers during an exam—their score (the outcome) looks related to yours (the exposure), but really it's because of the common cause of "sitting next to you" (the confounder). Stratified analysis separates "those sitting next to you" from "those not sitting next to you," eliminating this spurious association.

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: The DAG—draw a map of causation</div>
  <div class="youtube-lite" data-id="87jXOHHNCog">
    <img src="https://img.youtube.com/vi/87jXOHHNCog/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

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

## Step 3: Check the Three Confounder Requirements

Before stratifying, verify that "functional status" really meets the three conditions of a confounder. Skip verifying one and you may be doing all the work for nothing:

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Verifying the three requirements—hands-on with pd.crosstab</div>
  <div class="youtube-lite" data-id="gPq3SstS3JE">
    <img src="https://img.youtube.com/vi/gPq3SstS3JE/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

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

## Step 4: Stratified Analysis

> This is the core step of the whole chapter—split the data by functional status (ambulatory, wheelchair, bedridden) into three strata, and within each stratum compute the RR and 95% confidence interval.

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Stratified analysis—compute an RR for every stratum</div>
  <div class="youtube-lite" data-id="8yhHobtu_BU">
    <img src="https://img.youtube.com/vi/8yhHobtu_BU/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

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

## Step 5: Forest Plot

A forest plot puts each stratum's RR and confidence interval on a single chart, so you can see at a glance the effect size and precision of each stratum:

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Forest plot—see through every stratum's RR at a glance</div>
  <div class="youtube-lite" data-id="NhMpRmZgN10">
    <img src="https://img.youtube.com/vi/NhMpRmZgN10/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

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

## Step 6: Mantel-Haenszel Weighted RR

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Mantel-Haenszel weighting—a fair semester grade</div>
  <div class="youtube-lite" data-id="Fj3d4Jr0kQM">
    <img src="https://img.youtube.com/vi/Fj3d4Jr0kQM/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

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

## Step 7: Test of Homogeneity—Is There Interaction?

> 🍜 **The spicy hotpot analogy**: You're investigating "whether eating spicy hotpot causes diarrhea," and you split people into "strong-stomached" and "weak-stomached" groups. If the strong-stomached group has RR=1.2 and the weak-stomached group has RR=4.5—this isn't confounding, it's **interaction** (effect modification): the effect of spicy hotpot "varies from person to person." In that case you can't just report a single pooled RR; you must report them separately: "For strong-stomached people the effect is small; weak-stomached people should be careful."

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Interaction—the effect of exposure varies from person to person</div>
  <div class="youtube-lite" data-id="I82KCu2kM_0">
    <img src="https://img.youtube.com/vi/I82KCu2kM_0/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

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

---

## Interpretation Highlights

After finishing the stratified analysis, you need to answer two questions. The flowchart below helps you decide:

```{figure} images/stratified_interpretation.svg
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

---

## Supplement: Can Case-Control Studies Also Use Stratified Analysis?

So far, our nursing home data is a **cohort study**—all 280 residents are on the follow-up roster, and we used attack rates to compute RR. But what if it were a **case-control study** instead?

> 🏥 **Scenario**: Suppose there were too many infected people to follow everyone, so you could only pick 121 infected people (cases) and 159 uninfected people (controls), then ask them retrospectively whether they had used the shower. In that case you can't compute an attack rate (because you deliberately selected people rather than following the whole population), so you **can't compute an RR—only an OR (odds ratio)**.

Good news: **the logic of stratified analysis is exactly the same**—still verify the three requirements, still stratify by the confounder, still pool with Mantel-Haenszel. The only difference is:

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: The case-control MH—swap the formula, same logic</div>
  <div class="youtube-lite" data-id="9441-KkyGqM">
    <img src="https://img.youtube.com/vi/9441-KkyGqM/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```

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
