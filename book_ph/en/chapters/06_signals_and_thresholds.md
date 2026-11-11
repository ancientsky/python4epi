---
title: "06 Signals, thresholds and 7-1-7"
description: "Maya learns where outbreak signals come from in the Philippine system, builds a dengue epidemic threshold, reads an endemic channel, sees why the latest weeks look low, and measures 7-1-7 timeliness."
---

:::{div}
:class: ph-story
*Wednesday 12 August · CESU office, Santa Luz*

**Aling Nena:** Ate Maya, the leptospirosis is quieting down. But now it's *lamok* — the kids in Baybay have high fever, and the drums are full of wigglers.

**Maya:** The dengue forms are piling up too. Is this already an outbreak, or just August?

**Doc Mon:** Good question. "A lot" is a feeling. An alert threshold is a number. And once you raise the alert, the clock starts: seven, one, seven.

> When does "a lot of dengue" become an alert — and how fast did we act on it?
:::

## Two kinds of signals

A **signal** is anything that might mean an outbreak. The Philippine system collects
them in two ways.

**Indicator-based surveillance** counts cases that meet a case definition, through
routine reports. That is **PIDSR**, the Philippine Integrated Disease Surveillance and
Response system, with its web-based information system **EDCS**. Disease reporting units
(hospitals, RHUs, clinics, laboratories) report Category I diseases within 24 hours and
Category II diseases, such as dengue, weekly
([2020 Revised IRR of RA 11332](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf)).
Reports climb from the facility to the city or municipal ESU, then to the PESU, the RESU and
the DOH Epidemiology Bureau
([WHO Joint External Evaluation, 2018](https://extranet.who.int/sph/sites/default/files/document-library/document/JEE%20Report%20Republic%20of%20the%20Philippines%202018.pdf)).

**Event-based surveillance** picks up *unusual events* that no form was designed for: a
cluster of sick children, a rumour, a news story, a text message. The DOH runs it as
**ESR** (Event-based Surveillance and Response), in place since 2010
([WPSAR, 2015](https://ojs.wpro.who.int/ojs/index.php/wpsar/article/download/368/578?inline=1)).
Community reporting by **barangay health workers** — exactly what Aling Nena does — was
piloted in parts of Central Luzon in 2024, and the 2024 Joint External Evaluation lists
making it routine as a priority
([WHO JEE, 2024](https://www.who.int/publications/i/item/9789240116795)).

```{figure} images/reporting_ladder_en.svg
:alt: Six levels of reporting, from the barangay health worker up to the DOH Epidemiology Bureau, with feedback flowing back down.
:width: 100%
Reports climb the ladder; feedback should come back down. Every step takes time.
```

Every rung takes time. WHO's Western Pacific office describes **reporting delays of 2–3
weeks** in PIDSR dengue data
([WHO WPRO Dengue Situation Update 731, 2025](https://cdn.who.int/media/docs/default-source/wpro---documents/emergency/surveillance/dengue/dengue_202510021edf3700-e2a6-4e48-8e7c-acd86a16d530.pdf?sfvrsn=ba2e2c46_1)).
Keep that in mind; we come back to it below.

## Morbidity weeks

Dengue is counted per **morbidity week**. Our file uses ISO weeks: Monday to Sunday,
labelled like `2026-W32` (3–9 August 2026). It makes no claim about the official PIDSR
calendar. The columns `iso_year` and `iso_week` let us line up "the same week" across
years. The data run from 2019-W01 to 2026-W39. They are **synthetic**: Santa Luz, its
rainfall and its cases are invented.

## An alert threshold

An **epidemic threshold** answers: *how high can this week be in an ordinary year?* The
rule for this series:

1. For ISO week *w*, take weeks *w*−1, *w* and *w*+1 of the **baseline years 2022–2025**:
   4 years × 3 weeks = 12 numbers.
2. Threshold = their **mean + 2 standard deviations**.
3. Leave out unusual years. 2019 was an epidemic year; 2020–2021 were disrupted by
   COVID-19. A baseline must describe *ordinary* years.

:::{admonition} Ask Tala
:class: ph-ask-tala
I have a pandas DataFrame `weekly` with columns `iso_year`, `iso_week` (1–53) and
`cases`. Made-up rows: `(2022, 31, 9)`, `(2022, 32, 12)`, `(2023, 32, 7)`. For every
ISO week w from 1 to 53, compute an epidemic threshold = mean + 2 × sample SD of `cases`
in weeks w−1, w, w+1 of the years 2022–2025 only (week 1's window wraps to week 52).
Return it by week. Then tell me the first 2026 week whose cases are above its threshold.
Keep it readable for a beginner.
:::

:::{admonition} Tala says
:class: ph-tala-says
```python
BASELINE_YEARS = [2022, 2023, 2024, 2025]   # ordinary years only: not 2019, 2020, 2021, and never 2026


def window_weeks(week):
    # Weeks w-1, w, w+1; week 1 wraps to 52 and week 52 to 1 (week 53 uses 52, 53, 1)
    if week == 53:
        return {52, 53, 1}
    return {(week - 2) % 52 + 1, week, week % 52 + 1}


def epidemic_threshold(weekly, years):
    base = weekly[weekly["iso_year"].isin(years)]
    rows = {}
    for week in range(1, 54):
        values = base.loc[base["iso_week"].isin(window_weeks(week)), "cases"]
        rows[week] = {"n_values": len(values), "baseline_mean": values.mean(),
                      "threshold": values.mean() + 2 * values.std(ddof=1)}
    return pd.DataFrame(rows).T
```
:::

The answer: **2026 first crosses the threshold in W32 (3–9 August), with 33 cases
against a threshold of 17.5**. It stays above every week through W39.

:::{admonition} Check it
:class: ph-check
1. **By hand for one week.** The notebook lists the 12 baseline values for W32 and
   recomputes mean + 2 SD with Python's `statistics` module. Both give 17.45.
2. **The window size.** Every week 1–52 must have exactly 12 values.
3. **The story.** No 2026 week before W32 is above the threshold, and every week after
   it is.
:::

## The endemic channel

An **endemic channel** draws the usual level for every week of the year. In the
notebook, thin grey lines are the four baseline years, the green line is their mean
(what we expect), and the dashed orange line is the threshold. The 2026 bars sit on top;
red bars are above the threshold. Before Typhoon Amihan (W29), 2026 stays low — the
year began quieter than usual. Then, from W32, the bars burst through the channel.

:::{admonition} Tala got it wrong
:class: ph-oops
Maya's first prompt said "use all the years in the file". Tala did exactly that, so
the baseline included **2019** (an epidemic year) and **2026 itself**. An epidemic
inside its own baseline raises the mean and the SD, so the bar rises with the curve.
The W32 threshold jumped from **17.5 to 32.8**. The alarm rang only by a hair (33 cases),
then went **silent in W33 and W35** while the epidemic was climbing.

How Maya catches it: one line before every threshold calculation,
`assert 2026 not in years`, plus a check that no known epidemic year is in the list.
And she reads the baseline years out loud to Doc Mon.
:::

## Why the latest weeks always look low

The file counts cases by **week of onset**, but a case reaches the CESU only after the
patient consults and the facility notifies. In Santa Luz the median delay from onset to
report is 4 days. So the newest weeks are always incomplete. The notebook replays this
with the line list: the same weeks, counted on three different days.

| Week of onset | W35 | W36 | W37 | W38 |
|---|---:|---:|---:|---:|
| known on 2 Sep | 30 | 2 | 0 | 0 |
| known on 16 Sep | 34 | 58 | 54 | 1 |
| known on 30 Sep | 34 | 58 | 63 | 54 |

On 2 September, W36 looked like 2 cases. It ended at 58. That is why the last week of
our file, **W39 (45 cases), is incomplete**, and why it dips. Read the newest bars as
"at least this many", never as "it is going down". Real PIDSR data have the longer
delays described above.

:::{div}
:class: ph-game ph-game-threshold-watch
With weekly data, act the day the week's count arrives: detect within 7 days of
emergence, notify within 1 day, complete the early response within 7 days.
:::

## 7-1-7: how fast did we act?

Crossing a threshold is a **detection**. **7-1-7** is a target for what happens around it:

```{figure} images/timeline_717_en.svg
:alt: A timeline from emergence to detection within 7 days, notification within 1 day, and early response completed within 7 days.
:width: 100%
7-1-7: detect within 7 days of emergence, notify within 1 day of detection, complete the early response within 7 days of notification.
```

In the Philippines, the 2024 Joint External Evaluation found 7-1-7 applied only *ad
hoc*; in one city ESU, 56% of events were detected within 7 days
([WHO JEE, 2024](https://www.who.int/publications/i/item/9789240116795)).

`signals_717.csv` holds 40 **synthetic** Santa Luz events from January 2025 to August
2026, each with four dates and a `bottleneck` column.

:::{admonition} Ask Tala
:class: ph-ask-tala
I have a DataFrame `events` with date columns `date_emergence`, `date_detection`,
`date_notification`, `date_response_complete` (made-up row: 2025-03-01, 2025-03-05,
2025-03-06, 2025-03-12). Add the three delays in whole days, three True/False columns
for the 7-1-7 targets (≤ 7, ≤ 1, ≤ 7) and one for "all three met". Print how many
events met each target, as counts and percentages.
:::

:::{admonition} Tala says
:class: ph-tala-says
```python
events["days_to_detect"] = (events["date_detection"] - events["date_emergence"]).dt.days
events["days_to_notify"] = (events["date_notification"] - events["date_detection"]).dt.days
events["days_to_respond"] = (events["date_response_complete"] - events["date_notification"]).dt.days

events["detect_ok"] = events["days_to_detect"] <= 7
events["notify_ok"] = events["days_to_notify"] <= 1
events["respond_ok"] = events["days_to_respond"] <= 7
events["all_ok"] = events[["detect_ok", "notify_ok", "respond_ok"]].all(axis=1)
```
:::

| Target | Met | Missed |
|---|---:|---:|
| Detect ≤ 7 days | 26 (65%) | 14 |
| Notify ≤ 1 day | 31 (78%) | 9 |
| Respond ≤ 7 days | 27 (68%) | 13 |
| **All three** | **15 (38%)** | 25 |

Median delays: detection 6 days, notification 1 day, response 6 days. Each target alone
looks "mostly fine", but only 15 of 40 events met all three.

:::{admonition} Check it
:class: ph-check
1. **One event by hand.** EV-040 is the story's dengue surge in Baybay: emergence
   3 August (the Monday of W32), detection 10 August, notification 11 August, response
   complete 21 August. On paper: 7, 1 and 10 days. Detection ✓, notification ✓,
   response ✗. Tala's columns must agree.
2. **Logic.** "All three" can never be more than any single target.
3. **No negative delays.** A negative number means a typo in a date. Call the DRU.
:::

### Reading the bottleneck column

Percentages say **how often**; the `bottleneck` column says **why**. Split it on `"; "`
and count. The top causes in Santa Luz: *cases seen at a private clinic that is not yet a
PIDSR disease reporting unit* (5 events), *competing priorities* (5), *one DSO for 24
barangays* (5), and *a BHW noticed the cluster but had no load to text the CESU* (4).
None of these is fixed by better code. They are fixed by a memo, a back-up DSO and
prepaid load. Bring that list to the Local Health Board.

:::{admonition} Privacy stop
:class: ph-privacy
A signal needs *what, where and when* — "five children with fever, Purok 3, Baybay, since
Monday". It does not need names in a group chat. One Santa Luz bottleneck was *"notified
by personal chat message, not logged"*: send signals through the official channel, so
they are recorded and seen only by the people who need them. And as always, never paste
a line list into an AI chat. Describe the columns and use made-up rows.
:::

:::{div}
:class: ph-game ph-game-quiz
**Quick check: signals and thresholds**

1. Why are 2019, 2020 and 2021 left out of the baseline?
   - ✓ They were not ordinary years — an epidemic year and two COVID-19-disrupted years would distort "usual".
   - To make the code faster — speed has nothing to do with it.
2. The latest week of your series is much lower than the week before. What do you say?
   - The outbreak is over — not yet: recent weeks are incomplete.
   - ✓ "At least this many so far" — late reports will still arrive.
3. An event was detected on day 6, notified on day 9 and the response completed on day 12. Which 7-1-7 target was missed?
   - Detection — 6 days is within 7.
   - ✓ Notification — 3 days after detection, the target is 1.
   - Response — 3 days after notification is within 7.
4. A BHW texts the CESU about several feverish children in one purok. This is…
   - ✓ Event-based surveillance — an unusual event reported outside the routine forms.
   - Indicator-based surveillance — that would be counted case reports from facilities.
:::

:::{admonition} Baon
:class: ph-baon
- A threshold is only as good as its baseline: ordinary years only, never the season
  you are judging. Assert it.
- The newest weeks are always incomplete. Read them as "at least".
- Measure 7-1-7 for every event, then read the bottlenecks. Most fixes are not code.

Open the notebook: [](notebooks/06_signals_and_thresholds.ipynb)
:::
