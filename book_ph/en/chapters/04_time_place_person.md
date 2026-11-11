---
title: "04 Time, place, person"
description: "With the clean line list, Maya defines cases, draws the epidemic curve with the typhoon marked, computes attack rates per 10,000 with real denominators, and describes who fell ill and who died."
---

:::{div}
:class: ph-story
*Monday 3 August · video call with the Provincial Health Office*

**Doc Mon:** Clean list, good. Now tell me three things: when, where, who.

**Maya:** Most cases are from the riverside, Doc. Eighty-two percent!

**Doc Mon:** Eighty-two percent of *cases*. Most people in Santa Luz also live by the river. Denominator?

**Aling Nena:** *(on the line from Ilog)* Doc, it's the men who cleared the canals. I know every one of them.

> When did people fall ill, where is the risk highest, and who is affected?
:::

```{figure} images/scene_flood_riverside.svg
:alt: Riverside stilt houses after the typhoon, men wading waist-deep through brown floodwater carrying debris, a small boat, rain falling.
:width: 100%
After Typhoon Amihan, riverside residents waded through floodwater for days. Santa Luz and the outbreak are fictional.
```

## Who counts as a case?

Before counting, we agree on a **case definition**: a short list of criteria that
decides who is counted, so that every health facility counts the same way. Surveillance
usually grades cases by certainty. The definitions below are **simplified teaching
versions** used in this book's story. Official wording is in the PIDSR Manual of
Procedures and its updates
([catalogue entry](https://www.medbox.org/document/manual-of-procedures-for-the-philippine-integrated-disease-surveillance-and-response)).

| Level | Leptospirosis (in this story) | Dengue (in this story) |
|---|---|---|
| **Suspect** | sudden fever with symptoms such as headache, muscle pain (often the calves) or red eyes, after contact with floodwater, mud or animals | fever with symptoms such as headache, pain behind the eyes, body or joint pain or rash, in someone living in or visiting a dengue area |
| **Probable** | suspect + a positive rapid test | suspect + a positive NS1 rapid test or typical blood-count findings |
| **Confirmed** | suspect + a positive laboratory test at the reference lab | suspect + a positive laboratory test (RT-PCR) |

At the 30 September freeze, the 230 leptospirosis cases were 119 confirmed, 52 probable
and 59 suspect. The 388 dengue cases were 49 confirmed, 172 probable and 167 suspect.
Lab results take time, so "suspect" often only means "waiting for the lab".

## Time: the epidemic curve

An **epidemic curve** (epi curve) is a bar chart of cases by **date of onset**: one bar
per day or week, with no gaps between bars and the empty days kept in.

:::{admonition} Ask Tala
:class: ph-ask-tala
My DataFrame `lepto` has a datetime column `date_onset` (made-up rows: `2026-07-24`,
`2026-07-24`, `2026-07-27`). Draw an epidemic curve: one bar per day from 15 July to
31 August 2026, **including days with zero cases**, no gaps between bars. Mark 18 July
with a red dashed line labelled 'Typhoon Amihan landfall', shade the flood days
18–20 July and the clean-up 21 July – 2 August.
:::

:::{admonition} Tala says
:class: ph-tala-says
The key is to lay the daily counts onto a full calendar:
```python
lepto = ll[ll["disease"] == "leptospirosis"]
days = pd.date_range("2026-07-15", "2026-08-31", freq="D")
daily = lepto["date_onset"].value_counts().reindex(days, fill_value=0)
```
Then draw the bars with `ax.bar`, the landfall with `ax.axvline` and the shaded periods
with `ax.axvspan`.
:::

:::{admonition} Check it
:class: ph-check
1. The bars must add up to the cases **with** an onset date: 228 + 2 without = 230.
2. The weekly totals must match the outbreak report: ISO weeks 30–34 give 35, **108**,
   68, 15 and 2 cases.
3. The peak day is **27 July, with 19 cases**, the day Aling Nena texted the CESU.
:::

**Reading the shape.** Three classic shapes help:

- **Point source**: everyone exposed at one moment, such as one meal. You get one
  sharp peak, about one incubation period wide. The **incubation period** is the time
  from infection to the first symptoms.
- **Continuing common source**: the same source over days or weeks. The curve rises,
  stays high while exposure lasts, then falls.
- **Propagated**: person-to-person spread, in successive waves about one generation
  apart.

The leptospirosis curve has one wave. The first onset is 22 July, four days after
landfall; the median onset is **14 days** after landfall. Cases stay high from about
24 July to 6 August, then fade by mid-August. That fits a **continuing common source**:
days of wading during the flood and the clean-up, then a delay for incubation.
Leptospirosis does not usually spread from person to person, so a propagated pattern
would be surprising. Real floods show the same delay. After the late-July 2025 floods,
the DOH warned in early August that leptospirosis cases might still rise
([Philstar, 9 Aug 2025](https://www.philstar.com/headlines/2025/08/09/2464294/doh-warns-leptospirosis-cases-may-still-rise-coming-days)).

Dengue looks different. Its symptoms usually begin 4–10 days after the mosquito bite
([WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue)),
but *Aedes* mosquitoes first had to breed in the standing water. Weekly dengue cases
climb for weeks and peak in ISO week 37 (63 cases).

:::{div}
:class: ph-game ph-game-epicurve-builder
One sharp wave within about one incubation period suggests a point source; a wave that
stays high while exposure continues suggests a continuing source; successive waves
suggest person-to-person spread.
:::

## Place: attack rates need a denominator

:::{admonition} Tala got it wrong
:class: ph-oops
Maya asked: *"Compute the dengue attack rate by band."* Tala answered with
`dengue["band"].value_counts(normalize=True) * 100`: riverside 50.3%, coastal 44.8%,
upland 4.9%.

Those numbers add up to 100%. That is the clue. They show **where the cases are**, not
**how risky it is to live there**. The denominator was the number of *cases*. The
riverside has the most cases partly because it has the most people: 96,064 of 186,000.
:::

An **attack rate** is the number of new cases in a group divided by the **people at
risk** in that group. For a city we give it **per 10,000 residents**. The populations
come from `santa_luz_barangays.csv`, not from the line list:

```python
population = barangays.groupby("band")["population"].sum()
cases = pd.crosstab(ll["band"], ll["disease"])

attack = cases.div(population, axis=0) * 10_000
attack.loc["city"] = cases.sum() / population.sum() * 10_000
```

:::::{div}
:class: ph-stat
::::{grid} 2 2 4 4

:::{card} 19.7
leptospirosis per 10,000, riverside
:::

:::{card} 29.6
dengue per 10,000, coastal
:::

:::{card} 12.4
leptospirosis per 10,000, whole city
:::

:::{card} 20.9
dengue per 10,000, whole city
:::
::::
:::::

| Per 10,000 | riverside | coastal | upland | city |
|---|---:|---:|---:|---:|
| Leptospirosis | **19.7** | 5.6 | 2.6 | 12.4 |
| Dengue | 20.3 | **29.6** | 6.1 | 20.9 |

With real denominators, the dengue story turns around: the **coastal** band carries
the highest risk, not the riverside. **Check it** by hand for one cell:
189 riverside leptospirosis cases ÷ 96,064 residents × 10,000 = 19.7.

By barangay, the highest leptospirosis rates are in Tabing-Ilog (29.8) and Ilog (29.1),
both on the river. The highest dengue rates are in the coastal barangays Talaba (43.4)
and Buhangin (35.5). Start from the barangay table, not the case list, so that upland
Bukid, with no cases, still appears with a rate of 0. Chapter 08 turns these numbers
into a map.

```{figure} images/santa_luz_map_en.svg
:alt: Illustrated map of fictional Santa Luz City with upland hills in the north, riverside barangays along the Marilag River in the middle and coastal barangays by the sea in the south.
:width: 100%
Santa Luz City's three bands: upland, riverside and coastal. A fictional city.
```

## Person: who fell ill, and who died

Leptospirosis hit **working-age men**: 155 of the 230 cases were male (67%), and the
median age was 32. That matches Aling Nena's "the men who cleared the canals". Dengue
was spread evenly by sex (50% male) and was younger, with a median age of 18. The notebook draws both as side-by-side age–sex charts.

The **case-fatality rate** (CFR) is deaths divided by **cases**. This time the cases
*are* the right denominator, because the question is "of those who got sick, how many
died?"

| | Cases | Deaths | CFR | Hospitalised |
|---|---:|---:|---:|---:|
| Leptospirosis | 230 | 20 | **8.7%** | 143 (62.2%) |
| Dengue | 388 | 1 | **0.3%** | 206 (53.1%) |

:::{admonition} Privacy stop
:class: ph-privacy
Counts by barangay, age group and sex get small fast. A cell such as "one death,
female, 65+, in one barangay" can point to one family. Inside the CESU, the full table is fine. Before
anything is published, small counts are suppressed (chapter 09 shows how).
:::

:::{div}
:class: ph-game ph-game-quiz
**Quick check: time, place, person**

1. Which number is an attack rate?
   - 50.3% of dengue cases live in the riverside band — that is a share of cases; it adds up to 100% across bands.
   - ✓ 29.6 dengue cases per 10,000 coastal residents — cases divided by the people at risk.
   - 8.7% of leptospirosis cases died — that is the case-fatality rate.
2. The leptospirosis curve rises 4 days after the flood, stays high for about two weeks and fades. The best fit is…
   - A point source — that would be one sharp peak from one moment of exposure.
   - ✓ A continuing common source — exposure lasted through the flood and clean-up.
   - Person-to-person spread — that gives successive waves, and leptospirosis rarely spreads that way.
3. Why must the epidemic curve keep days with zero cases?
   - ✓ Leaving them out squeezes time and changes the shape you interpret.
   - Zero days are errors and should be dropped — they are real information.
:::

:::{admonition} Baon
:class: ph-baon
- Define a case before you count: suspect, probable, confirmed.
- Read the epi curve's shape against the incubation period and the exposure window.
- An attack rate needs the population at risk as its denominator; a CFR uses cases.
  Shares of cases are not risk.

Open the notebook: [](notebooks/04_time_place_person.ipynb)
:::
