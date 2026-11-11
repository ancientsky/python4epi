---
title: "05 Find the source"
description: "Maya analyses a case-control study of leptospirosis after Typhoon Amihan: 2×2 tables, odds ratios with 95% confidence intervals, boots and doxycycline as protective factors, and a confounder untangled with Mantel–Haenszel."
---

:::{div}
:class: ph-story
*Monday 10 August · Barangay Ilog Health Station*

**Aling Nena:** Done, Ate Maya. Every case in the riverside, two neighbours each. Same questions for all.

**Maya:** Did you wade? Boots? Any wound? Clean-up work? Doxycycline?

**Doc Mon:** And rats near the house. Now the City Health Officer wants one answer: what do we tell people before the next flood?

**Maya:** Wading, obviously…

**Doc Mon:** "Obviously" is not an odds ratio.

> Which exposures really raised — or lowered — the odds of leptospirosis?
:::

```{figure} images/scene_health_station.svg
:alt: A barangay health station with a flag, a waiting bench under a mango tree and Aling Nena at the door, ready for interviews.
:width: 100%
Interviews at the health station. The study, its 360 participants and every number are fictional.
```

## Why a case-control study?

In a **cohort study** you follow everyone who was exposed or not and count who gets
sick. For Santa Luz that means interviewing tens of thousands of residents to find a
few hundred cases. In a **case-control study** you start from the people who are sick
(**cases**), pick similar people who are not (**controls**), and compare how often each
group was **exposed**.

Doc Mon's team took the 120 probable or confirmed leptospirosis cases aged 15 and over
in the eight riverside barangays. For each case they chose two controls from the same
barangay: 240 controls, 360 people in all (`lepto_case_control.csv`).

## The 2×2 table

Every exposure becomes a **2×2 table**: rows for exposed and not exposed, columns for
cases and controls.

|  | Cases | Controls |
|---|---|---|
| **Exposed** | a | b |
| **Not exposed** | c | d |

The **odds ratio** (OR) is $\frac{a \times d}{b \times c}$. An OR of 1 means no
association. Above 1, the exposure was more common among cases (a risk factor). Below 1,
it was less common among cases (a protective factor).

:::{admonition} Ask Tala
:class: ph-ask-tala
In `cc`, `waded_floodwater` is 0/1 and `status` is `case`/`control`. Make the 2×2 table
and compute the odds ratio for wading.
:::

:::{admonition} Tala says
:class: ph-tala-says
```python
t = pd.crosstab(cc["waded_floodwater"], cc["status"])
a, b = t.iloc[0, 0], t.iloc[0, 1]
c, d = t.iloc[1, 0], t.iloc[1, 1]
print(t)
print("Tala's OR =", round(a * d / (b * c), 2))
```
The odds ratio is **0.18**.
:::

:::{admonition} Tala got it wrong
:class: ph-oops
An OR of 0.18 says wading *protected* people. Aling Nena would laugh. Maya catches it
two ways:

1. **Read the labels.** `crosstab` sorts rows 0 before 1, so the first row is "did
   **not** wade". Tala read the cells by position, so her *a* was the unexposed cases.
   One axis was flipped, which turns the OR upside down: 0.18 = 1 ÷ 5.57. (Swapping
   rows *and* columns would not change the OR, so check each axis.)
2. **Sanity-check the direction first.** **75%** of cases waded, against **35%** of
   controls. The OR has to be well above 1.
:::

The safe way is to fix the order and name the rows and columns, so anyone can read
the table:

```python
def two_by_two(data: pd.DataFrame, exposure: str) -> pd.DataFrame:
    """2x2 table: rows exposed / not exposed, columns cases / controls."""
    table = pd.crosstab(data[exposure], data["case"]).loc[[1, 0], [1, 0]]
    table.index = ["Exposed", "Not exposed"]
    table.columns = ["Cases", "Controls"]
    return table
```

For wading this gives a = 90, b = 84, c = 30, d = 156, and **OR = 5.57**.

## How sure are we? The 95% confidence interval

An OR from 360 people carries sampling error. The **95% confidence interval** (CI)
gives the range of values compatible with our data. If the whole interval sits above 1
(or below 1), chance alone is an unlikely explanation. The simple *Woolf* method works
on the log scale:

$$95\%\ CI = \exp\left(\ln OR \pm 1.96\sqrt{\tfrac1a+\tfrac1b+\tfrac1c+\tfrac1d}\right)$$

```python
se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
low, high = math.exp(math.log(or_wading) - 1.96 * se), math.exp(math.log(or_wading) + 1.96 * se)
```

:::{admonition} Check it
:class: ph-check
1. **By hand, scipy and statsmodels must agree.** All three give **5.57 (3.41–9.10)**.
2. **Read the documentation default.** scipy's `odds_ratio` must be told
   `kind="sample"`. Its default is the *conditional* OR (5.54), which is a different
   estimator, not a bug.
3. **Direction:** the OR is above 1, and more cases than controls waded. They agree.
:::

## Risk ratio or odds ratio?

A **risk ratio** (RR) divides the *risk* in the exposed by the risk in the unexposed,
$\frac{a/(a+b)}{c/(c+d)}$. That needs everyone at risk, which is what a cohort gives you.
In a case-control study *we chose* how many controls to take, so "risk" in our table
depends on our design. The notebook shows it: with two controls per case the fake "RR"
is 3.21; with one control per case it becomes 2.37, while the OR barely moves (5.57 vs
5.18). **Cohort → RR. Case-control → OR.** When a disease is rare, the OR is close to
the RR.

:::{div}
:class: ph-game ph-game-two-by-two
Rows are exposure, columns are outcome. A cohort study compares risks (RR); a
case-control study compares odds of exposure (OR), never an RR.
:::

## Boots and doxycycline

Boots only matter for people who were in the water, so that question was asked of
**waders only** (174 people). Among them, wearing boots had an **OR of 0.35**
(95% CI 0.16–0.80). Taking **doxycycline prophylaxis**, which was handed out at
evacuation centres and to clean-up volunteers, had an **OR of 0.43** (0.21–0.86). Both
are protective factors *in this fictional outbreak*. Seeing rats near the house made
no difference here (OR 1.03, 0.67–1.60).

For real-world use of doxycycline prophylaxis (who should get it, when and at what
dose), follow current Department of Health guidance and your physicians, not this book.

## The confounder: wading or clean-up?

Doc Mon spots it: *"Clean-up volunteers waded more, didn't they? And clean-up had its
own risks."* A **confounder** is a third factor that is linked to the exposure **and**
is a risk factor for the disease on its own, so its effect gets mixed into the crude OR.
Among controls, 69.1% of clean-up workers waded, against 21.5% of everyone else, and
clean-up work itself had an OR of 3.20.

So Maya **stratifies**: she computes the wading OR separately for people who did and
did not do clean-up work. Then she combines the two with the **Mantel–Haenszel** (MH)
odds ratio, a weighted average of the stratum ORs:

| Stratum | a | b | c | d | OR |
|---|---:|---:|---:|---:|---:|
| No clean-up work | 32 | 37 | 21 | 135 | 5.56 |
| Did clean-up work | 58 | 47 | 9 | 21 | 2.88 |
| **Crude (everyone)** | 90 | 84 | 30 | 156 | **5.57** |
| **Mantel–Haenszel** | | | | | **4.28** (2.53–7.27) |

**What changed, and why?** Once clean-up work is held fixed, the wading OR falls from
5.57 to 4.28. Part of the crude number belonged to clean-up work, because clean-up
workers waded more. Wading is still strongly linked to leptospirosis. The two stratum
ORs look different, but with these numbers a test cannot tell them apart from chance
(p ≈ 0.24), so one MH summary is reasonable. Male sex looks risky in the crude table
(OR 2.82) for the same reason: men waded more. The notebook lets you check that.

:::{admonition} Check it
:class: ph-check
statsmodels' `StratifiedTable` must reproduce the hand-made MH OR:
`math.isclose(st.oddsratio_pooled, or_mh)` passes, and it adds the 95% CI (2.53–7.27).
:::

:::{div}
:class: ph-game ph-game-quiz
**Quick check: find the source**

1. Your OR comes out at 0.18, but 75% of cases and 35% of controls were exposed. What happened?
   - ✓ One axis of the table is flipped — read the row and column labels; the true OR is 1 ÷ 0.18.
   - The exposure is protective — not when cases were exposed more often than controls.
2. In a case-control study you should report…
   - A risk ratio — the number of controls is chosen by the investigators, so risks are not real.
   - ✓ An odds ratio with its 95% confidence interval.
3. After stratifying by clean-up work, the wading OR fell from 5.57 to 4.28. This means…
   - Wading does not matter — it is still strongly associated, with an OR around 4.
   - ✓ Clean-up work confounded the crude OR — part of its effect was mixed in.
:::

## What Maya tells the City Health Officer

:::{div}
:class: ph-story
*Friday 14 August · Office of the City Health Officer*

**Maya:** Wading in floodwater after Amihan was strongly associated with leptospirosis, even after accounting for clean-up work (adjusted OR about 4), and wearing boots was associated with much lower odds among those who waded. Before the next flood, the city should supply boots and wound care to clean-up crews and residents who must wade, and tell anyone with fever after floodwater exposure to consult early. Doxycycline prophylaxis was associated with lower odds of disease in this study, so its distribution to high-exposure groups should continue, following current DOH guidance.
:::

:::{admonition} Baon
:class: ph-baon
- Fix and name the rows and columns of every 2×2 table; check the direction with plain
  percentages before trusting a formula.
- Case-control → odds ratio with a 95% CI; check it with a second method.
- Stratify on a suspected confounder and compare the crude and Mantel–Haenszel ORs.

Open the notebook: [](notebooks/05_find_the_source.ipynb)
:::
