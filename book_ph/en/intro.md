---
title: "Mabuhay!"
description: "Bantay Python is a free beginner's course for Philippine disease surveillance staff: learn Python with an AI co-pilot you learn to check, protect patient privacy, and build an outbreak dashboard."
---

:::{div}
:class: ph-hero
**Philippines Edition · Epi With Python**

## Bantay Python

From a stack of paper notification forms to an outbreak dashboard the Mayor can read in
one screen. No coding experience needed. You bring the epidemiology; an AI co-pilot
writes the first draft of the code; **you learn to read it, run it and check it.**

{button}`Sakay na! Start the ride → <chapters/00_start_here.md>`
:::

*Bantay* means to watch over, to guard. That is what surveillance is: watching over a
community so that a problem is seen early and answered fast. This course gives you one
more tool for that work.

## What you will build

By the last chapter you will have made the **Bantay Santa Luz dashboard**: a single
HTML file that opens in any browser, even offline, and can be emailed or shared with a
Local Health Board. Every number on it comes from code you have read and checked.

::::{grid} 1 2 3 3

:::{card} Headline tiles
Cases, deaths and the case fatality rate for leptospirosis and dengue, at a glance.
:::

:::{card} Epidemic curve
Cases by day or week of onset, so the shape of the outbreak tells its story.
:::

:::{card} Barangay map
Attack rates per 10,000 residents, not raw counts, on a map of the 24 barangays.
:::

:::{card} Alert threshold
This year's weekly dengue counts against the usual level for the season.
:::

:::{card} 7-1-7 scorecard
How fast each event was detected, notified and answered.
:::

:::{card} Privacy footer
Small counts hidden, no names or addresses, a source line and a date.
:::
::::

You will build it in [chapter 09](chapters/09_dashboard.md). Each chapter before it
adds one piece.

:::{div}
:class: ph-banderitas
:::

## Meet the cast

:::::{div}
:class: ph-cast
::::{grid} 2 3 5 5

:::{card} Maya
![Maya Dela Cruz, the Disease Surveillance Officer, holding a clipboard](chapters/images/cast_maya.svg)

*Disease Surveillance Officer, CESU*

"Ate Maya". A nurse, four months into her first DSO post. Great with people and paper forms; has never written code. She learns alongside you.
:::

:::{card} Doc Mon
![Dr. Ramon Bautista, the provincial epidemiologist, wearing glasses](chapters/images/cast_doc_mon.svg)

*Provincial epidemiologist, PESU*

Dr. Ramon Bautista, FETP graduate and Maya's mentor. Always asks: "Denominator? Case definition? Who can see this file?"
:::

:::{card} Tala
![Tala, the AI coding assistant, drawn as a smiling star](chapters/images/cast_tala.svg)

*The AI coding assistant*

*Tala* means bright star. Fast, friendly and helpful, and sometimes confidently wrong. This book shows both.
:::

:::{card} Aling Nena
![Aling Nena Ramos, the barangay health worker, holding a phone](chapters/images/cast_aling_nena.svg)

*Barangay Health Worker, Ilog*

The first to notice something is off. Reminds everyone that every row is a neighbour.
:::

:::{card} Jun
![Jun Villanueva, the records clerk, with headphones and a USB stick](chapters/images/cast_jun.svg)

*IT and records clerk, City Health Office*

Guardian of the shared drive and source of very messy spreadsheets.
:::
::::
:::::

## The story

```{figure} chapters/images/scene_flood_riverside.svg
:alt: Riverside barangay under floodwater after a typhoon. Men wade through the water carrying debris past houses on stilts; a small boat floats nearby in the rain.
:width: 100%
Santa Luz after Typhoon Amihan (an invented city and an invented typhoon).
```

On **Saturday 18 July 2026**, Typhoon Amihan makes landfall over Santa Luz City, in the
Province of Kalinaw. The Marilag River overflows. The eight riverside barangays stay
under waist-deep water for three days. Men wade through the flood to clear debris and
canals.

A week later, Aling Nena texts the City Epidemiology and Surveillance Unit (CESU): several
men in Barangay Ilog have fever, red eyes and calf pain. It looks like **leptospirosis**,
a bacterial infection people catch through contact with water or soil contaminated by
the urine of infected animals, especially rats. Maya's notification forms pile up. Then,
as standing water breeds mosquitoes, weekly **dengue** cases climb too.

Maya has a spreadsheet, a deadline and no analyst. Doc Mon's advice: *"Ask Tala, but
check everything it gives you."*

## Santa Luz in numbers

These are the headline numbers of the story's invented data. You will reproduce every
one of them with your own code.

:::::{div}
:class: ph-stat
::::{grid} 2 2 4 4

:::{card} 186,000
people in 24 barangays
:::

:::{card} 449.1 mm
of rain in the week of Typhoon Amihan
:::

:::{card} 637
rows in Jun's raw line list export
:::

:::{card} 618
cases after cleaning
:::

:::{card} 230
leptospirosis cases
:::

:::{card} 388
dengue cases
:::

:::{card} 8.7%
leptospirosis case fatality rate (20 deaths)
:::

:::{card} 33
dengue cases in the first week above the epidemic threshold
:::
::::
:::::

All cases are those reported to the CESU by the data freeze on 30 September 2026.

## The route

The book is a jeepney ride with twelve stops in four acts. Get on at the start; every
stop builds on the one before.

:::{div}
:class: ph-wide
```{figure} chapters/images/route_map_en.svg
:alt: A jeepney route through twelve stops, from Mabuhay through chapters 00 to 10, coloured in four acts.
:width: 100%
Four acts: get the report, count, keep watch, show it.
```
:::

:::{div}
:class: ph-route ph-act-1
**I · May ulat!** *(A report!)*

- [00 Start here: you, Colab and an AI co-pilot](chapters/00_start_here.md)
- [01 Kumusta, Python?](chapters/01_python_with_ai.md)
- [02 Privacy first: every row is a neighbour](chapters/02_privacy_first.md)
:::

:::{div}
:class: ph-route ph-act-2
**II · Bilangin natin** *(Let's count)*

- [03 From messy line list to clean data](chapters/03_clean_linelist.md)
- [04 Time, place, person](chapters/04_time_place_person.md)
- [05 Find the source](chapters/05_find_the_source.md)
:::

:::{div}
:class: ph-route ph-act-3
**III · Bantay** *(Keep watch)*

- [06 Signals, thresholds and 7-1-7](chapters/06_signals_and_thresholds.md)
- [07 Next month's dengue: forecasting with TimesFM](chapters/07_forecast_timesfm.md)
- [08 Where is it? Maps](chapters/08_maps.md)
:::

:::{div}
:class: ph-route ph-act-4
**IV · Ipakita** *(Show it)*

- [09 Build the Bantay Santa Luz dashboard](chapters/09_dashboard.md)
- [10 Sitrep, checklist and where next](chapters/10_wrap_up.md)
:::

## Who this is for

This course is for people who do surveillance work in the Philippines and have **never
written code**: Disease Surveillance Officers, nurses in an Epidemiology and Surveillance
Unit (ESU), frontline FETP trainees, and supervisors of Barangay Health Workers. If you
can fill in a case investigation form and use a spreadsheet, you are ready.

You need a web browser, a free Google account for Colab (chapter 00 explains), and an AI
assistant your office allows you to use. You do not need to install anything.

**How each chapter works.** A short story scene, one idea with a picture, the prompt Maya
types and the code that comes back, a box on how to **check** it, a small game, and the
*baon* (take-away) to carry home. Then you run everything yourself in a notebook. Watch
for the red **Tala got it wrong** boxes: they show the mistakes AI assistants really
make, and how Maya catches them.

## The story is invented. The system is real.

:::{admonition} Fiction and fact
:class: note
**Invented:** Santa Luz City, the Province of Kalinaw, the Marilag River, Typhoon
Amihan, every person in the story, and every name, phone number, address and count in the
Santa Luz datasets. The names in the raw line list are fake but made to *look* real, so
you can practise privacy safely. No real patient is in this book.

**Real:** the surveillance system around the story. Notifiable diseases are reported
through PIDSR and its EDCS information system, events through Event-based Surveillance
and Response (ESR), and reports climb from facilities through city, municipal,
provincial and regional Epidemiology and Surveillance Units to the DOH Epidemiology
Bureau, under the [Mandatory Reporting of Notifiable Diseases and Health Events of Public
Health Concern Act (RA 11332)](https://lawphil.net/statutes/repacts/ra2019/ra_11332_2019.html)
and its [2020 Revised Implementing Rules and Regulations](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf).
Real laws, systems and statistics in this book carry a link to their source.
:::

## Part of a bigger book

*Bantay Python* is the Philippines edition of
[**Epi With Python**](https://ancientsky.github.io/python4epi/en/), a free, open book
that teaches infectious disease epidemiology with Python, from the basics up to
statistics, maps and machine learning, through the investigation of an outbreak at a
nursing home. When you finish here, it is the next ride.

{button}`Sakay na! Start here → <chapters/00_start_here.md>`
