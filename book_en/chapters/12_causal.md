# 12 Causal Inference and Policy Evaluation: Does Showering Really "Cause" Infection?

## What You Will Learn

- **Counterfactual thinking**: the starting point of causal inference—asking "if this exposure hadn't happened, what would have happened to this same group of people?"
- Using a **DAG (directed acyclic graph)** to identify three causal structures: **confounders** (should adjust), **mediators** (usually don't adjust), and **colliders** (never adjust)
- Calculating **attributable risk (AR)** and **population attributable risk (PAR)**, and deriving the population attributable fraction (PAF) with the **Levin formula**
- Using **difference-in-differences (DiD)** to evaluate the causal effect of a policy or intervention
- Checking the **parallel trends assumption** that DiD depends on, and understanding the logic of the event study
- Translating causal inference results into **policy evaluation** recommendations the administration can act on, while honestly acknowledging the method's limitations

## The Scenario

By this point in the book, you've run through descriptive statistics (Ch03), stratified analysis (Ch05), logistic regression (Ch06), time series (Ch07), spatial epidemiology (Ch08), survival analysis (Ch09), and even machine learning and deep learning (Ch10, Ch11)—every method pointing, from a different angle, to the same conclusion: "shower exposure is associated with infection."

But this time the director's office is asking a question that's not quite like the previous eleven chapters:

> "Does showering really *cause* infection? Or is it just a statistical coincidence?"
> "If we do emergency disinfection of the water system right now, will it actually bring the infection count down? Or would the outbreak have been winding down around this time anyway?"

Neither of these questions is asking "is there an association"—they're asking "if we do A, will Y turn out differently as a result." That's exactly the question **causal inference** exists to answer, and it's the deciding factor in whether the nursing home should commit real money to disinfecting the water system. This chapter does three things: first draw a clean line between "association" and "causation," then honestly lay out the causal structure with a DAG, and finally use DiD to honestly evaluate "did infections actually drop after disinfection."

---

## 🕵️ Super-Simple Special: Be a Causal Detective — "If It All Happened Again, Would You Still Get Sick?"

> Do terms like "causal inference," "DAG," and "counterfactual" sound intimidating? Don't worry. This section recasts the whole apparatus of causal inference as your favorite scene from a detective drama: **solving a case**. Once you've read through it, go back and look at the DAGs and formulas below—you'll find that, oh, every one of those scary terms was something the detective was already doing.

### The crime scene: association is not the culprit

A good detective never closes a case just because "two things happened at the same time." Weather reports often note: in months when ice cream sales go up, drownings go up too—does that mean you'd accuse ice cream of being the culprit behind drowning? Of course not. The real culprit is someone else entirely: **summer**. When it gets hot, people both love eating ice cream and love swimming—ice cream and drowning just happen to move together "because of a shared common cause," with no causal relationship between them at all.

```{figure} images/causal_vs_association_en.svg
:name: fig-causal-vs-association
:alt: A causal-detective illustration: ice cream sales and drownings look associated, but the real shared cause behind both is summer heat; the counterfactual question "if we took ice cream away, would drownings go down" has the answer no
:width: 100%

Ice cream and drowning "look" associated, but the real culprit is "summer" hiding behind both. A causal detective's first reflex: ask "is there a hidden culprit behind this?"
```

A true causal detective closes cases with one magic phrase: **"If we ran this over again and took this suspect out of the picture, would it still have happened?"** This magic phrase has a formal name: the **counterfactual**—imagining the same person, in the same situation, with the only difference being "exposed or not," and comparing the outcomes in these two parallel worlds.

### Three common traps in casework

While solving a case, a detective has to watch out for three characters that easily throw the investigation off course:

- **Confounder = the culprit hiding behind the scenes**: "summer," hiding behind ice cream and drowning, is the confounder—it influences both the "exposure" (ice cream sales) and the "outcome" (drownings), making two otherwise unrelated variables look like they're moving hand in hand. In the nursing home case, `functional_status` plays this role (Ch05 already caught it once).
- **Mediator = a messenger, not the culprit**: if the administration pushes a "water system disinfection" policy, the logic runs "disinfection → lower Legionella concentration in the water → changed foot traffic/exposure risk → fewer infections"—the links in the middle are just "messengers" carrying the policy's effect down the chain, not suspects to be removed. Mistakenly arresting the messenger (adjusting it away) will instead blind you to the policy's real effect.
- **Collider = an illusion created by selection**: if a detective only looks at cases that "got sent for autopsy" to find a pattern, they might turn up some strange, spurious associations—because "whether it gets sent for autopsy" is itself jointly determined by several other causes. Nursing home version: analyzing only patients who were "hospitalized" can produce an association between exposure and severity that doesn't actually exist (more on this in the next section).

### The detective's casebook ↔ causal inference terminology

| Detective's casebook | Causal inference term | In one line |
|---|---|---|
| Two things happening together doesn't mean one caused the other | **Association ≠ causation** | Association is just "moving together"; causation asks "would it be different if we took it away" |
| "If we ran this over again and took this suspect out, would it still happen?" | **Counterfactual** | Comparing the same individual's two parallel worlds: "exposed" vs. "not exposed" |
| The culprit hiding behind the scenes, pulling the strings on both things | **Confounder** | Should be caught and adjusted for |
| The messenger passing the case along | **Mediator** | Usually not adjusted for; adjusting it underestimates the total effect |
| The illusion created by only looking at cases sent for testing | **Collider** | Must never be adjusted for—it manufactures a false association |

> 🔑 **Remember the whole special in one line**: **Association ≠ causation, always ask "the counterfactual" first**—if this hadn't happened, would this same group of people have gotten a different outcome? The sections that follow teach you how to turn this magic phrase into a tool you can actually compute with and use to evaluate real policies.

---

<!-- video: ch12_01_causal_intuition -->
<!-- /video -->

## Part 1: Association ≠ Causation

### The counterfactual: a formal definition of causal inference

The last section built up the intuition through detective work; here, let's write it more formally. For a given person $i$, what causal inference really wants to know is the outcome in two "parallel worlds":

- $Y_i(1)$: what happens to this person if they **are** exposed (e.g., they do shower)
- $Y_i(0)$: what happens to the **same** person if they are **not** exposed

This person's **individual causal effect** is $Y_i(1) - Y_i(0)$. The problem is: the same person can never live in both worlds at once—**we can only ever observe one of them; the other is forever counterfactual, forever unobservable**. This is called the **fundamental problem of causal inference**.

Epidemiology's workaround is to step back and, instead of comparing "the same person's two worlds," compare "two groups of people with similar conditions"—using the exposed group's average outcome to approximate the counterfactual "what would the average outcome have been if the unexposed group had also been exposed." This is exactly what Ch05's stratified analysis and Ch06's regression adjustment are doing: trying to make the exposed and unexposed groups as similar as possible on everything except exposure status (i.e., the confounders), so that the gap between the two groups' outcomes can be credibly attributed to a causal effect of exposure, rather than an illusion produced by the groups simply being different to begin with.

### Background case: association and causation in the catered-lunch chicken-thigh incident

Background case (context only, not something this book computes): reports indicate that in 2019, New Taipei City had a school catered-lunch food poisoning incident, which investigators linked to braised chicken thighs served that day; health authorities subsequently detected **Clostridium perfringens** in specimens. This case is a good illustration of how "association" and "causation" get built up step by step in a real epidemiological investigation:

1. **Association first**: investigators handed out questionnaires and found that students "who ate the chicken thighs" were more likely to develop diarrhea and abdominal pain than "students who didn't"—this is only an **association**, not yet ironclad proof of causation.
2. **Watch out for confounding and bias**: did the students who ate the chicken thighs happen to also eat other suspect items (a potential confounder)? Might students who got sick remember eating the chicken thighs more vividly, while students who didn't get sick have a fuzzier memory of the menu (**recall bias**)? Either of these could make the observed "association" look stronger or weaker than the true causal effect.
3. **Only laboratory evidence lets you claim causation**: what truly turned this case from "suspected" to "confirmed" was the **laboratory evidence**—detecting the same pathogen in the suspect food item or in patient specimens, layered together with the exposure-history association from the investigation. Only when both are stacked together does the causal inference become reasonably solid. Questionnaire association alone, or pathogen detection alone, is not enough to draw a conclusion.

> ⚠️ This is exactly the point of this section: **a statistical association alone—no matter how small the p-value—is never enough to declare causation**. A real-world epidemiological investigation always needs "epidemiological association + laboratory/biological evidence + ruling out other explanations" stacked together before it can say "this is what caused it."

---

<!-- video: ch12_02_association_vs_causation -->
<!-- /video -->

## Part 2: Drawing Causation with a DAG

### Three structures, two completely opposite rules

```{figure} images/dag_structures_en.svg
:name: fig-dag-structures
:alt: Comparison of three DAG structures: in a confounder fork, C points to both exposure A and outcome Y, and needs adjusting; in a mediator chain, A goes through M to Y, and M should not be adjusted when looking at the total effect, only when looking at the direct effect; in a collider, exposure A and outcome Y both point into K, which must never be adjusted for
:width: 100%

Same idea—"a third variable gets involved"—but the direction of the arrows determines whether it's a confounder that should be adjusted, a mediator that usually shouldn't be, or a collider that must never be.
```

A DAG uses arrows to show "who affects whom," and the direction of the arrow is the direction of causation. Understanding the difference between the three structures below is the single most important lesson in causal inference:

| Structure | Shape | In plain words | What to do about it |
|---|---|---|---|
| **Confounder (fork)** | C → A, C → Y | C is a common cause of both exposure and outcome (the culprit hiding behind the scenes) | **Adjust for it** (stratification, regression adjustment—what Ch05/Ch06 did) |
| **Mediator (chain)** | A → M → Y | M sits on the causal path from exposure to outcome (the messenger) | **Do not adjust** for M if you want the **total effect**; only adjust for M if you specifically want the **direct effect** "net of M" |
| **Collider (two arrows pointing in)** | A → K ← Y | K is pointed into by both exposure and outcome (a selection trap) | **Never adjust** for it, and don't even restrict the analysis to some subset defined by K |

Mapped onto this book's nursing home case:

- **Confounder**: `functional_status` affects both `shower_use` and `infection`—this is the confounder Ch05 already caught and adjusted for with the Mantel-Haenszel method.
- **Mediator**: `water_contamination` can only affect `infection` by way of `shower_aerosol`—`shower_aerosol` is the mediator sitting in the middle of that causal path.
- **Collider**: `hospitalized` is pointed into by both `severity` and other factors (e.g., comorbidities, family preference)—a textbook collider.

<!-- video: ch12_03_dag -->
<!-- /video -->

### The collider trap: Berkson's paradox

If you **condition on** a collider—that is, restrict your analysis to a subset where "the collider equals some particular value"—you'll manufacture a spurious association between two variables that are otherwise unrelated. This phenomenon has a formal name: **Berkson's paradox**.

```{figure} images/collider_berkson_en.svg
:name: fig-collider-berkson
:alt: Illustration of Berkson's paradox: exposure and disease severity are unrelated in the full population, but both affect whether someone is hospitalized, a collider; restricting analysis to hospitalized patients produces a spurious negative correlation between exposure and severity
:width: 100%

In the full population, "exposure" and "disease severity" are unrelated—but restrict the view to people who were "hospitalized," and a spurious association appears out of nowhere. That's the price of conditioning on a collider.
```

Here's the intuitive version: suppose "exposure" and "severity" really are unrelated across the whole resident population, but **either one being high enough is, on its own, sufficient to get someone hospitalized**. Then within the "hospitalized" subset, people with low exposure are usually there because their severity was especially high; people whose severity wasn't that high are usually there because their exposure was especially heavy. The two get artificially tied together, showing up as a "trade-off" negative correlation among hospitalized patients—even though that negative correlation doesn't exist at all in the full population.

> ⚠️ **Common scenario**: restricting analysis to "cases that were notified/confirmed," to "patients who were hospitalized," or to "cases that had a follow-up visit"—these seemingly reasonable filtering criteria are all, in effect, conditioning on some collider, and can easily manufacture an association that doesn't actually exist, or mask one that does.

### A real-world DAG sketch: the Sanxia dengue cluster

Background case (context only, not something this book computes or precisely reconstructs): reports indicate that in 2020, Wuliao Village in Sanxia District, New Taipei City, saw a locally acquired dengue cluster, which investigators linked to an imported case together with mosquito breeding in nearby containers of standing water. Let's use this scenario to practice sketching the simplest possible DAG:

> **DAG sketch (illustrative only, not a formal epidemiological investigation output)**:
> - Imported case → locally acquired infection (direct path: a mosquito bites the imported case, then bites a community resident)
> - Standing water containers → mosquito vector density (**mediator**) → locally acquired infection (standing water itself doesn't make anyone sick—it only matters because it breeds mosquitoes that then transmit)
> - Locally acquired infection → whether it gets notified ← intensity of standing-water inspection (**collider**: both the number of locally acquired cases and inspection intensity push up the probability of "notification/further investigation"; if you only analyze cases that "were notified," you might see an association between local cases and inspection intensity that doesn't actually exist)

Once you've sketched this out, you've already completed the most critical step in causal inference: **think through who affects whom before deciding who to adjust for and who to leave alone**.

### Tools for drawing a DAG: the thinking matters, not the software

In practice, common tools for drawing a DAG include **draw.io** (drag-and-drop online, fastest to pick up), **graphviz** (describes nodes and arrows as text, good for version control), and Python's **daft** package (handy for embedding directly in a paper or notebook)—these are all just tools for "putting it on paper"; pick whichever you like, even pen and paper works fine. **What really matters is the thinking that happens before you draw**: who do you believe affects whom? Have you missed a possible confounder? Is a given variable a mediator or a confounder? Getting these questions straight matters far more than how slick the tool is.

---

<!-- video: ch12_04_collider_berkson -->
<!-- /video -->

## Part 3: Attributable Risk (AR) and Population Attributable Risk (PAR)

```{figure} images/attributable_risk_en.svg
:name: fig-attributable-risk
:alt: Illustration of attributable risk AR and population attributable risk PAR: on the left, AR compares the attack rate of the exposed group vs. the unexposed group as a difference; on the right, PAR uses the whole population's case composition to show how many cases could theoretically be prevented by removing the exposure
:width: 100%

AR asks the question at the "individual" level (how much extra risk does the exposed group carry compared to the unexposed group); PAR asks it at the "population" level (how many fewer cases could the whole population theoretically have if the exposure were removed).
```

### AR: how much extra risk the exposed group is carrying

**Attributable Risk (AR)** answers the question of how much the absolute risk **differs** between the "exposed" group and the "unexposed" group—note that it's a **subtraction**, not a division (division is the risk ratio, RR, already computed in Ch03). **Population Attributable Risk (PAR)** swaps the denominator for "the entire population," quantifying how much risk this exposure contributes to the population as a whole; its percentage version is called the **Population Attributable Fraction (PAF)**. Besides computing it directly as a subtraction divided by the total risk, PAF can also be derived from just two numbers—the "exposure prevalence Pe" and the "risk ratio RR"—via the **Levin formula**:

$$AR = I_{exposed} - I_{unexposed}, \qquad PAF = \frac{P_e (RR - 1)}{1 + P_e (RR - 1)} = \frac{I_{total} - I_{unexposed}}{I_{total}}$$

The two ways of computing PAF (the Levin formula vs. directly subtracting "unexposed risk" from "total risk") are theoretically exactly equivalent—below, we cross-check the two formulas against each other using the nursing home data.

```python
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

exposed = df[df["shower_use"] == 1]
unexposed = df[df["shower_use"] == 0]
risk_exposed = exposed["infected"].mean()
risk_unexposed = unexposed["infected"].mean()
risk_total = df["infected"].mean()

AR = risk_exposed - risk_unexposed          # Attributable risk: difference in attack rate between the two groups
PAR = risk_total - risk_unexposed           # Population attributable risk: total population vs. unexposed group

Pe = (df["shower_use"] == 1).mean()                     # Exposure prevalence
RR = risk_exposed / risk_unexposed
PAF_levin = Pe * (RR - 1) / (1 + Pe * (RR - 1))          # Levin formula
PAF_alt = (risk_total - risk_unexposed) / risk_total     # Equivalent formula: the I_total form
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `exposed = df[df["shower_use"] == 1]` | Filters out the "showered" exposed group |
> | `AR = risk_exposed - risk_unexposed` | Attributable risk: the absolute extra risk the exposed group carries compared to the unexposed group (a subtraction, not a division) |
> | `PAR = risk_total - risk_unexposed` | Population attributable risk: swap the denominator for the whole population, and see how much risk this exposure contributes to the entire population |
> | `PAF_levin = Pe * (RR - 1) / (1 + Pe * (RR - 1))` | Levin formula: using just the exposure prevalence Pe and risk ratio RR, derive the population attributable fraction (PAF, the percentage version of PAR) |
> | `PAF_alt = (risk_total - risk_unexposed) / risk_total` | Another equivalent formula: directly using the relative difference between "total risk" and "unexposed risk," to check that the two formulas agree |

Running the numbers on the nursing home data: attack rate among showerers is about 51.4% (76 infected out of 148), and among non-showerers about 34.1% (45 infected out of 132), giving AR ≈ 17.3 percentage points; converted to PAF (the Levin formula and the I_total form cross-check to the same value), that's about 21.1%.

> 💡 **AR and RR are two different questions asked of the same data**: RR answers "how many times higher is the risk," AR answers "how many percentage points higher." The two carry different meaning for public health decisions—a large RR with a small AR means that although the relative risk is high, the actual number of preventable cases is limited (common for rare diseases).

### Cross-checking with a clean set of numbers: a food-poisoning teaching 2×2 table

The nursing home data is only 280 rows, so the signal is weak and the numbers aren't especially "clean." Here we switch to a **teaching demonstration dataset** (not a real study, not a real event) and run through the same formulas once more with the classic 2×2 table format, to confirm you can really do the calculation and aren't just copy-pasting:

```python
# 2x2 table: a=exposed+ill, b=exposed+not ill, c=unexposed+ill, d=unexposed+not ill
a, b, c, d = 120, 280, 25, 375  # teaching demonstration numbers, not a real event

risk_exposed_fp = a / (a + b)        # Risk of illness in exposed group
risk_unexposed_fp = c / (c + d)      # Risk of illness in unexposed group
AR_fp = risk_exposed_fp - risk_unexposed_fp
RR_fp = risk_exposed_fp / risk_unexposed_fp
Pe_fp = (a + b) / (a + b + c + d)    # Exposure prevalence
PAF_fp = Pe_fp * (RR_fp - 1) / (1 + Pe_fp * (RR_fp - 1))
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `a, b, c, d = 120, 280, 25, 375` | Teaching demonstration numbers: a=exposed and ill, b=exposed and not ill, c=unexposed and ill, d=unexposed and not ill |
> | `risk_exposed_fp = a / (a + b)` | Risk of illness in the exposed group = 120/400 = 0.300 |
> | `risk_unexposed_fp = c / (c + d)` | Risk of illness in the unexposed group = 25/400 = 0.0625 |
> | `AR_fp = risk_exposed_fp - risk_unexposed_fp` | Attributable risk = 0.300 − 0.0625 = 0.2375 (about 23.7 percentage points) |
> | `RR_fp = risk_exposed_fp / risk_unexposed_fp` | Risk ratio = 0.300 / 0.0625 = 4.80 |
> | `PAF_fp = Pe_fp * (RR_fp - 1) / (1 + Pe_fp * (RR_fp - 1))` | Applying the Levin formula, with Pe=0.5 and RR=4.80 → PAF ≈ 65.5% |

> 🧭 **PAF's interpretation only holds if causation is real**: PAF≈65.5% means "if this exposure really does cause the disease, and the exposure could be entirely eliminated, roughly 65 percent of cases could theoretically be prevented." But if this exposure is actually just a bystander that happens to co-occur with the true cause (say, there's a confounder lurking behind it), eliminating the exposure won't actually make those cases go away—which is exactly why PAF must always be read together with the DAG from Part 2, and never handed straight to a policy recommendation just because it produced a tidy-looking number.

---

<!-- video: ch12_05_ar_par -->
<!-- /video -->

## Part 4: Evaluating Policy Effects with DiD

### Why you can't just compare before vs. after

Background case (context only, not something this book computes): in 2021, Taiwan raised its nationwide epidemic alert to Level 3 in response to a community cluster, and social-distancing and crowd-control measures rolled out at the same time. If you later wanted to evaluate "did Level-3 actually suppress the outbreak," simply "comparing daily case counts before vs. after the alert" is easily confounded by seasonality, changes in reporting practices, spontaneous risk-avoidance behavior by the public, and other things that were also changing at the same time—which is exactly the problem **Difference-in-Differences (DiD)** is built to solve: find a control group that "wasn't intervened on, but was originally following the same trend," and subtract "the treated group's change after the intervention" from "the control group's change over that same period"—only then can you credibly say the remaining difference is the effect of the intervention itself.

```{figure} images/did_parallel_trends_en.svg
:name: fig-did-parallel-trends
:alt: Illustration of DiD: the treatment group and control group follow parallel trends before the intervention; after the intervention, the treatment group departs from its original trend, and the gap between the actual outcome and the counterfactual extension line is the intervention effect estimated by DiD
:width: 100%

The core logic of DiD: first confirm the two groups followed parallel trends before the intervention; the gap after the intervention, between what actually happened to the treated group and "what would have happened without the intervention" (the counterfactual extension line), is the intervention effect DiD is estimating.
```

### The nursing home's intervention scenario

Continuing this book's story: on January 25, the nursing home carried out emergency disinfection of the water system for Wing B on floors 2-3 (the area with the higher attack rate, whose water system sits closer to the contamination source), with the rest of the floors/wings serving as the control group. Once the case data is organized into a long-format panel by "group × day" (aggregate by date with `groupby()`, and fill any missing dates with `reindex(..., fill_value=0)`), you can run the following DiD regression.

```python
import statsmodels.formula.api as smf

# treated      -> group main effect (2-3F Wing B=1, else=0)
# post         -> time main effect (after intervention=1, before=0)
# treated:post -> interaction term = the DiD estimate: how much extra the treated group changed after the intervention
model = smf.ols(
    "daily_cases ~ treated + post + treated:post", data=panel
).fit(cov_type="HC3")  # HC3: panel data commonly has unequal variance, so use robust standard errors to avoid overly optimistic p-values

did_effect = model.params["treated:post"]
did_p = model.pvalues["treated:post"]
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `treated` | Group main effect: the baseline difference between the treated and control groups, regardless of time |
> | `post` | Time main effect: the change that happened over the before/after period, regardless of group (e.g., the outbreak naturally winding down) |
> | `treated:post` | **The interaction term, the DiD estimate itself**: how much extra the treated group changed after the intervention, above and beyond "the plain group difference" plus "the plain time trend" |
> | `.fit(cov_type="HC3")` | Uses HC3 robust standard errors to handle the unequal variance common in panel data, avoiding an overly optimistic significance test |
> | `model.params["treated:post"]` / `model.pvalues["treated:post"]` | Pulls out just this term's coefficient and p-value—that's the actual answer DiD cares about |

> 💡 When reading DiD regression output, keep your eyes locked on the `treated:post` row—`treated` and `post` usually aren't what we care about; the model just uses them to "subtract out" the fixed group difference and the fixed time trend, so the interaction term can cleanly represent the intervention effect.

**The honest result**: running this on this book's synthetic data, the `treated:post` coefficient comes out at nearly 0 (p ≈ 1, not remotely significant). The reason isn't mysterious—the intervention date (1/25) in the data is only 3-4 days from the end of the observation window (1/28), and on top of that, the whole cluster event was already nearing its tail end, with daily case counts naturally declining. A window of just a few days simply doesn't provide enough statistical power to tell "the effect of the intervention" apart from "the outbreak was winding down anyway." This is exactly one of the traps covered in the next section: **an observation window that's too short, or a sample that's too small, leaving DiD unable to estimate a significant effect, does not mean the intervention didn't work—it only means this particular batch of data can't support that conclusion**.

<!-- video: ch12_06_did -->
<!-- /video -->

### The parallel trends assumption: DiD's lifeline

A DiD estimate is only trustworthy if the **parallel trends assumption** holds: if the two groups were already on different slopes before the intervention, the difference observed afterward might just be the two groups continuing to drift apart on their own, with nothing to do with the intervention itself.

> ⚠️ **Plot first, trust the model second**: before running the regression, always plot the treated and control groups' daily trends on the same chart, and look only at the side **before** the intervention date—do the two lines rise and fall roughly in parallel? If the two lines were already diverging—one climbing, one falling—before the intervention, the DiD estimate can't simply be read as "the effect of the intervention."

If you only have two time points—"before" and "after"—the parallel trends assumption is hard to check; a more rigorous approach is the **event study**, which breaks the before/after period into several smaller time windows (e.g., "3 weeks before intervention," "2 weeks before intervention," ..., "1 week after intervention") and estimates a separate effect coefficient for each one. Ideally, **every pre-intervention coefficient should be close to 0** (since the intervention hasn't happened yet, there shouldn't be an effect); only the post-intervention coefficients should deviate significantly from 0. If the pre-intervention coefficients are already significantly different from 0, that's a sign the two groups were already on different trajectories to begin with, and the parallel trends assumption doesn't hold.

---

<!-- video: ch12_07_parallel_trends -->
<!-- /video -->

## Exercises

- Exercise version: [`12_causal_exercise.ipynb`](exercises/12_causal_exercise.ipynb)
- Solution version (instructor): [`12_causal_solution.ipynb`](solutions/12_causal_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/12_causal_solution.ipynb>)

## Part 5: Common Beginner Pitfalls

| Mistake | Why it's dangerous | Correct approach |
|------|-----------|---------|
| Treating statistical significance as causation | p < 0.05 only means "unlikely to be chance"—it doesn't mean "A caused B" | Go back to the DAG, check whether there's a confounder/mediator/collider to handle, and combine it with other evidence (lab results, mechanism) to judge causation |
| Adjusting for a mediator as if it were a confounder | Adjusting away a mediator shuts off the causal pathway itself, underestimating or even completely hiding the total effect | Draw the DAG first to distinguish mediators from confounders; only adjust for a mediator when you specifically want the "direct effect" |
| Conditioning on a collider | Manufactures a spurious association between two variables that are actually unrelated (Berkson's paradox) | Use a DAG to identify colliders, and avoid restricting the analysis to a subset defined by a collider (e.g., only hospitalized patients, only notified cases) |
| Declaring an intervention effective without checking parallel trends | If the two groups were already on different trends before the intervention, the DiD estimate can be an illusion from start to finish | Plot the pre-intervention trend first, and follow up with an event study period by period if conditions allow |
| Reporting a number precise to the decimal point from a small sample | With a small sample, confidence intervals are usually wide, and an overly precise-looking number can mislead decision-makers into overconfidence | Always report a confidence interval or describe the uncertainty, and use cautious wording with small samples (e.g., "preliminary evidence suggests" rather than "confirms") |
| Ignoring time order and mistaking effect for cause | Causation requires "cause before effect"; treating a variable that only appears after infection as if it were the exposure reverses cause and effect | Confirm that every candidate exposure's timing genuinely precedes the outcome's timing |

## A 4-Week Learning Path for Beginners

What causal inference most requires practicing isn't the muscle memory of plugging numbers into formulas—it's the judgment to "draw the DAG correctly," and that only comes from repeated discussion with colleagues and cross-checking against the literature.

| Week | Topic |
|------|------|
| 1 | Pick 3-5 real outbreak investigations you've worked on (or read about), and for each one, sketch out a DAG, marking the possible confounders, mediators, and colliders |
| 2 | For one of those cases, first compute AR/PAR by hand with pencil and paper, then recompute it in Python (following this chapter's steps) and confirm the two match |
| 3 | Pick a scenario with a clear intervention date (a policy, disinfection, a screening measure—any of these work), organize it into a "group × time" panel, run a DiD, and plot the before/after trend to check parallel trends |
| 4 | Take the DAG you drew in Week 1 to a senior colleague or instructor to review together—ask "do you agree with this arrow?" "did I miss a confounder?"—the mistakes people most often make in causal inference usually aren't in the calculation, but in a wrongly drawn DAG |

## Next Step

Causal inference helps us pin down "what causes what," and gives us the confidence to make judgments about policy effects—but only if every step of the analysis can hold up to someone else checking it. In the next chapter (Ch13), we make sure every analysis is **reproducible** → reproducible research.
