---
title: "09 Build the Bantay Santa Luz dashboard"
description: "Maya turns ten weeks of surveillance into one self-contained HTML screen for the Local Health Board: headline numbers, an epidemic curve, a map of rates and the dengue threshold, and a publish check that blocks small cells and line-level data."
---

:::::{div}
:class: ph-story
*Wednesday 30 September · City Health Office, Santa Luz*

::::{div}
:class: ph-say-jun
**Jun:** Ate Maya, the Mayor's office called. The Local Health Board meets on Friday. The Mayor wants "one screen, not forty slides".
::::

::::{div}
:class: ph-say-maya
**Maya:** One screen? I have an epi curve, a map, the threshold chart, the 7-1-7 table, the case-control results…
::::

::::{div}
:class: ph-say-mon
**Doc Mon:** Then choose. A board member has two minutes. How many, where, up or down, and what do we do. And Maya — nothing leaves this office until I have checked it.
::::

::::{div}
:class: ph-say-tala
**Tala:** I can put it all in one HTML file! Shall I add the full line list, so people can download the data?
::::

> How do we build one screen that answers the Board's questions and protects every neighbour on it?
:::::

**[Open the Bantay Santa Luz dashboard](/dashboard/)** — the finished screen this chapter
builds towards. It works offline, on a phone and on paper (one landscape page). Santa Luz and
every number on it are invented for this course.

## What a good dashboard answers

A **dashboard** is a single page of the most important numbers and charts, updated on a
schedule, for people who must decide something. It is not a report: no long text, no
methods chapter. It answers four questions, in this order:

| Question | What answers it on the Santa Luz screen |
|---|---|
| **How many?** | headline tiles: cases, deaths, case fatality rate, weeks above the threshold |
| **Where?** | a map of **attack rates** by barangay (cases per 10,000 residents), not raw counts |
| **Going up or down?** | the epidemic curve and the weekly dengue count against its **epidemic threshold** |
| **What do we do?** | a short, numbered action list for this week |

Who is affected (age and sex), how fast the system reacted (7-1-7) and what drove the
leptospirosis cluster (the odds ratios from chapter 05) come next, smaller.

:::::{div}
:class: ph-stat
::::{grid} 2 2 4 4

:::{card} 618
cases reported by 30 Sept (230 leptospirosis, 388 dengue)
:::

:::{card} 21
deaths (20 leptospirosis, 1 dengue)
:::

:::{card} 8
weeks in a row with dengue above the threshold, since W32
:::

:::{card} 38%
of 40 events met all three 7-1-7 targets
:::
::::
:::::

```{figure} images/scene_cesu_office.svg
:alt: Maya at her desk in the CESU office with a laptop showing a rising epidemic curve and Tala the star on the screen, paper forms beside her, a map on the wall and an electric fan.
:width: 100%
Ten weeks of forms, cleaning and analysis become one screen. Santa Luz and its CESU are fictional.
```

## Step 1: the headline numbers

Maya starts with the tiles. She describes the columns and gives three made-up rows.

:::{admonition} Ask Tala
:class: ph-ask-tala
I have a pandas DataFrame `ll`, one row per case, with columns `case_id`, `disease`
(`leptospirosis` or `dengue`), `outcome` (`alive` or `died`) and `hospitalised` (0/1).
Made-up rows: `X-1, dengue, alive, 0` · `X-2, leptospirosis, died, 1` · `X-3, dengue,
alive, 1`. Write a function `compute_kpis(ll)` that returns cases, deaths, hospitalised and
the case fatality rate in % (one decimal) for each disease and for the whole city.
:::

:::{admonition} Tala says
:class: ph-tala-says
```python
def compute_kpis(ll: pd.DataFrame) -> pd.DataFrame:
    """Cases, deaths, hospitalised and CFR (%) by disease, plus a city total row."""
    kpis = ll.groupby("disease").agg(
        cases=("case_id", "size"),
        deaths=("outcome", lambda s: (s == "died").sum()),
        hospitalised=("hospitalised", "sum"),
    )
    kpis.loc["total"] = kpis.sum()
    kpis["cfr_pct"] = (100 * kpis["deaths"] / kpis["cases"]).round(1)
    return kpis
```
:::

:::{admonition} Check it
:class: ph-check
1. Run it on Tala's three made-up rows: dengue must have 2 cases, leptospirosis a CFR of 100%.
2. Count deaths a second way, `(ll["outcome"] == "died").sum()`, and compare with the total row.
3. Read the **denominator** of the case fatality rate (CFR): deaths ÷ *cases*, not ÷ population.
   For Santa Luz: leptospirosis 20 ÷ 230 = **8.7%**, dengue 1 ÷ 388 = **0.3%**.
:::

## Step 2: three charts, one rule

In the notebook Maya makes three Plotly charts: the **epidemic curve** by week of onset with
Typhoon Amihan marked, a **map** of dengue attack rates (Talaba 43.4 and Buhangin 35.5 per
10,000 are the highest), and the weekly dengue count against the **epidemic threshold**
(mean + 2 standard deviations of the same weeks in 2022–2025, chapter 06). Weeks, not days:
a daily count of 1 would give away one person's onset date.

Every chart follows one rule, written once as a function:

```python
def suppress(counts: pd.Series | pd.DataFrame, threshold: int = 5) -> pd.Series | pd.DataFrame:
    """Replace counts from 1 to threshold - 1 with '<5' (zero stays 0)."""
    small = (counts > 0) & (counts < threshold)
    return counts.astype(object).mask(small, f"<{threshold}")
```

:::{admonition} Privacy stop
:class: ph-privacy
A dashboard leaves the office, so treat it as public. **Small-cell suppression** means hiding
any count from 1 to 4 in a small group (one barangay, one week, one age group) and withholding
its rate, because "one case aged 65+ in a barangay of 3,000" is a person the neighbours can
name. Zero stays zero: it describes no one. Whole-city totals for the whole period may be shown,
as in routine bulletins. The publish rules of your own office and the Data Privacy Act of 2012
(RA 10173) come first; this rule is the minimum the course uses.
:::

## Step 3: one self-contained HTML file

A **self-contained** HTML file carries everything it needs inside it: text, styles, data and
the charting code. It opens without internet, from an e-mail or a USB stick. Python's
`string.Template` fills a small page with `$placeholders`; each Plotly figure becomes an HTML
fragment with `fig.to_html(full_html=False, ...)`, and only the first one carries the Plotly
library:

```python
figures = [fig.to_html(full_html=False, include_plotlyjs=(i == 0), config={"responsive": True})
           for i, fig in enumerate([fig_curve, fig_map, fig_thr])]
page_html = PAGE.substitute(
    title="Bantay Santa Luz",
    as_of=AS_OF,
    kpis="".join(f'<div class="kpi">{label}<b>{value}</b></div>' for label, value in tiles),
    figures="\n".join(figures),
    notes="".join(f"<li>{note}</li>" for note in notes),
)
```

The notebook writes the result to your computer's **temporary folder** (about 4.9 MB, mostly
the Plotly library) and prints where it is. Open it in a browser, then on your phone.

## Step 4: Doc Mon's publish check

Some items of Doc Mon's checklist can be tested by code, every time, in a second:

```python
def publish_check(page: str) -> list[str]:
    """Return the problems Doc Mon would block (an empty list means OK to publish)."""
    problems = []
    if re.search(r"SLC-\d{4}", page):
        problems.append("case IDs found: line-level data must not be published")
    for column in ["case_id", "date_onset", "date_report"]:
        if column in page:
            problems.append(f"line-list column {column!r} found")
    small = re.findall(r"<td>\s*[1-4]\s*</td>", page)
    if small:
        problems.append(f"{len(small)} table cell(s) with 1-4 cases: suppress them")
    for must in ["As of", "Data notes", "synthetic"]:
        if must not in page:
            problems.append(f"missing: {must!r}")
    return problems
```

Maya's page passes. Then the Mayor's staff asked for "more detail".

:::{admonition} Tala got it wrong
:class: ph-oops
Maya asked Tala to *add a table of cases by barangay and age group, and a button to download
the data*. Tala added `pd.crosstab(ll["barangay"], ll["age_group"])` — raw counts with dozens
of 1s and 2s — and put `ll.to_json()` inside a `<script>`: **the whole line list**, with case
IDs, ages and exact onset dates, readable by anyone with *View source*. The page looked
exactly the same. The publish check did not: it blocked case IDs, three line-list columns and
55 small cells. The fix was to publish only aggregates: a coarser table (band × age group),
suppressed, and no download of case-level data at all.
:::

Code cannot check everything. The rest of the checklist stays human:

1. **Aggregate only.** No names, addresses, phone numbers, case IDs or exact dates of individual cases — on the page *or* hidden in its code.
2. **Suppress small cells** (1–4 → "<5", no rate) and do not publish a total that lets someone subtract a hidden cell back.
3. **Rates, not counts, on maps**, with the denominator named.
4. **Honest axes**: bar charts start at zero; the incomplete last week is labelled.
5. **Data notes**: synthetic or real, source, definitions, what was suppressed.
6. **An "as of" date** on the screen and on the printout.
7. **Tested on a phone**, and read aloud once by a second person.

:::{div}
:class: ph-game ph-game-publish-check
Before publishing: no names or exact addresses, suppress counts of 1–4, no case-level
downloads, axes that start at zero, and a source line.
:::

## The full dashboard: the same idea, taken further

The [Bantay Santa Luz dashboard](/dashboard/) on this site is built by the script
`scripts/build_ph_dashboard.py` in the book's repository, with the same steps as your
notebook: `load_data()`, `compute_kpis()`, `suppress_small_cells()`, `render_html()`. It goes
further in four ways:

- **Hand-drawn charts.** A short script draws them from a small block of embedded numbers,
  so the whole page is under 0.1 MB, works offline and prints on one landscape page.
- **Stricter suppression.** When a total is published and a column hides only one small cell,
  a second cell is hidden too (marked `x`), so nobody can get the small one back by subtraction.
- **More panels.** Age and sex, 7-1-7 timeliness with the most common bottlenecks, the
  case-control odds ratios, and the TimesFM forecast fan from [chapter 07](07_forecast_timesfm.md)
  when its cached forecast is present.
- **Three languages, light and dark, keyboard and touch.**

The notebook imports two of its functions and checks that they give the same headline
numbers as yours.

:::{div}
:class: ph-game ph-game-quiz
**Quick check: dashboards**

1. The Board asks "where is dengue worst?". What goes on the map?
   - Number of cases per barangay — big barangays always look worst.
   - ✓ Cases per 10,000 residents (attack rate) — it compares risk fairly.
   - The address of each case — never on a public screen.
2. A barangay has 3 dengue cases. What does the public table show?
   - 3 and its rate — that can point to a family.
   - ✓ "<5" and no rate — a count of 1–4 is suppressed, and the rate would give it back.
   - 0 — that would be false.
3. The last week's bar is lower. Is dengue going down?
   - Yes, the bar is lower.
   - ✓ Not yet known — the last week is incomplete because of reporting delay.
4. Tala offers a "download the data" button with the line list inside the page. Doc Mon says…
   - Fine if the file is small.
   - ✓ No — case-level data never goes into a public page, even hidden in the code.
:::

:::{admonition} Baon
:class: ph-baon
- A dashboard answers four questions: how many, where, up or down, what do we do.
- Suppress counts of 1–4 in every small group, map rates, and stamp an "as of" date.
- Run the publish check every time; then a person checks it on a phone.

Open the notebook: [](notebooks/09_dashboard.ipynb) · [Open the dashboard](/dashboard/)
:::
