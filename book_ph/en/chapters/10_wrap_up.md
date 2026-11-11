---
title: "10 Sitrep, checklist and where next"
description: "Maya's one-page situation report for 30 September 2026, a checklist for using an AI assistant in a health office, a plain map of the real Philippine surveillance system, a three-language glossary and where to go next."
---

:::::{div}
:class: ph-story
*Wednesday 30 September, 6:40 in the evening · CESU office, Santa Luz*

::::{div}
:class: ph-say-mon
**Doc Mon:** The dashboard passed. Now the sitrep — one page, the numbers that matter, what we are doing. The Board reads the dashboard; the Province files the sitrep.
::::

::::{div}
:class: ph-say-maya
**Maya:** Tala can draft it from my tables…
::::

::::{div}
:class: ph-say-mon
**Doc Mon:** It can. And you will check every number against the notebook, and write down that it helped. Your name goes at the bottom, not Tala's.
::::

> What does the finished work look like — and how do we keep using AI safely after this course?
:::::

## Maya's sitrep, 30 September 2026

A **situation report (sitrep)** is a short, dated summary of an event for the people who must
act on it: what happened, how big, where, what is being done, what is needed. Every number
below comes from the synthetic Santa Luz data and was printed by the notebooks of chapters
04–09.

:::{admonition} SITREP · Santa Luz City CESU · as of 30 September 2026 (data freeze)
:class: note
**Event.** Leptospirosis cluster and dengue outbreak after Typhoon Amihan (landfall 18 July;
riverside barangays flooded 18–20 July). *Fictional city, synthetic data — for training only.*

**Leptospirosis — cluster ending.** 230 cases (119 confirmed, 52 probable, 59 suspect),
143 hospitalised (62.2%), **20 deaths (CFR 8.7%)**. Onsets 22 July – 23 August, peak in
week 31 (108 cases). Attack rate 19.7 per 10,000 in the riverside band; highest in Tabing-Ilog
(29.8) and Ilog (29.1). Case-control study (120 cases, 240 matched controls): wading in
floodwater OR 5.57 (95% CI 3.41–9.10), 4.28 after adjusting for clean-up work; boots among
waders OR 0.35 (0.16–0.80); doxycycline prophylaxis OR 0.43 (0.21–0.86). No new onset since
23 August.

**Dengue — outbreak ongoing.** 388 cases (49 confirmed, 172 probable, 167 suspect),
206 hospitalised (53.1%), 132 with warning signs, 15 severe, **1 death (CFR 0.3%)**. Above the
epidemic threshold every week since week 32 (33 cases against 17.5); peak in week 37 (63);
week 38: 54. Week 39 is incomplete (reporting delay). Attack rate 29.6 per 10,000 in the
coastal band; highest in Talaba (43.4) and Buhangin (35.5).

**Timeliness (7-1-7).** 15 of 40 events since January 2025 (38%) met all three targets. This
cluster: notification took 2 days (target 1). The dengue response took 10 days (target 7).
Median time from consultation to leptospirosis lab confirmation: 18 days.

**Actions.** 4S search-and-destroy with BHWs in the coastal barangays; hospitals prepared
for severe dengue; leptospirosis close-out report; enrol the private clinic as a disease
reporting unit; follow up specimens at the reference laboratory.

**Prepared by** M. Dela Cruz, DSO. **Checked by** R. Bautista, PESU. *Drafting assisted by an
AI assistant; every figure verified against the analysis notebooks.*
:::

The full screen is the [Bantay Santa Luz dashboard](/dashboard/).

## The AI-use checklist for a health office

Print this and stick it next to the computer. It is the method of the whole course in one
list: **Ask → Run → Check**, with privacy around it.

![The Ask, Run, Check loop with Tala in the middle](images/ask_run_check_en.svg)

**Before you ask**

1. Use the assistant your office has approved, under its rules.
2. **Never paste identifiable data**: names, phone numbers, addresses, PhilHealth numbers,
   birth dates, free-text remarks, photos of forms. Follow the Data Privacy Act of 2012
   (RA 10173) as your office's Data Protection Officer applies it.
3. Describe the **columns** and give two or three **made-up** rows instead (chapter 02).
4. Say exactly what output you want and how you will check it.

**While you work**

5. Run the code on a tiny case you can count by hand.
6. Read every line you do not understand; ask the assistant to explain it, then check the
   explanation.
7. Check the **denominator**, the dates and the missing values.
8. Watch for confident mistakes: invented functions, wrong columns, a silent date mis-parse,
   a total that does not add up.

**After, before anything leaves the office**

9. Re-run the notebook from top to bottom; the numbers in your text must match the output.
10. Run the **publish check** (chapter 09): aggregates only, small cells suppressed, "as of"
    date, data notes.
11. A **person** is accountable: you sign it, and a second person checks it.
12. **Record what was AI-assisted** — which part, which day — in the report or the file notes.

## How surveillance works in the real Philippines

Santa Luz is invented; the system around it is real. Here it is in plain words, from the
research compiled for this book. (Details change; follow your current DOH and LGU issuances.)

```{figure} images/reporting_ladder_en.svg
:alt: Six levels of reporting, from the barangay health worker up to the DOH Epidemiology Bureau, with feedback flowing back down.
:width: 100%
Reports climb the ladder; feedback should come back down.
```

**Who reports to whom.** A disease reporting unit (rural health unit, hospital, clinic,
laboratory, port) reports to the city or municipal Epidemiology and Surveillance Unit
(**CESU/MESU**), which reports to the provincial unit (**PESU**), then the regional unit
(**RESU**, in the DOH regional office), then the DOH **Epidemiology Bureau**
([2018 Joint External Evaluation](https://extranet.who.int/sph/sites/default/files/document-library/document/JEE%20Report%20Republic%20of%20the%20Philippines%202018.pdf);
[2020 Revised IRR of RA 11332](https://law.upd.edu.ph/wp-content/uploads/2020/09/DOH-Revised-IRR-RA-11332.pdf)).
Under the IRR, Category I diseases are reported within 24 hours and Category II diseases
weekly, every Friday. RA 11332 (2019), the law on mandatory reporting of notifiable diseases,
and its rules call for these units at every level
([RA 11332](https://lawphil.net/statutes/repacts/ra2019/ra_11332_2019.html)).

| System | What it is for |
|---|---|
| **PIDSR**, entered in **EDCS** | case-based reporting of notifiable diseases such as dengue, leptospirosis and measles — what Maya's line list feeds |
| **ESR** (event-based surveillance and response) | signals that are not case reports: rumours, news, text messages, unusual events, reported within 24 hours ([JEE 2018](https://extranet.who.int/sph/sites/default/files/document-library/document/JEE%20Report%20Republic%20of%20the%20Philippines%202018.pdf)) |
| **FHSIS** | routine monthly and quarterly service statistics of health facilities ([Murai et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8880878/)) |
| **SPEED** | syndromic surveillance switched on after a disaster, to be activated within 48 hours ([WPSAR 2015](https://ojs.wpro.who.int/ojs/index.php/wpsar/article/download/368/578?inline=1)) |
| **RITM and the laboratory network** | confirmation of cases at reference and subnational laboratories ([2024 Joint External Evaluation](https://www.who.int/publications/i/item/9789240116795)) |
| **FETP** | the DOH Field Epidemiology Training Program, from frontline to advanced level ([TEPHINET](https://www.tephinet.org/training-programs/philippines-field-epidemiology-training-program)) |

**Three honest gaps** the evaluations name:

- **Reporting delay.** WHO's Western Pacific office notes reporting delays of 2–3 weeks for
  PIDSR dengue data ([Dengue Situation Update 731](https://cdn.who.int/media/docs/default-source/wpro---documents/emergency/surveillance/dengue/dengue_202510021edf3700-e2a6-4e48-8e7c-acd86a16d530.pdf?sfvrsn=ba2e2c46_1)).
  That is why the last week on Maya's chart is always too low.
- **No unique person ID across systems**, so de-duplication and linking lab results stay
  manual — the problem Jun's duplicates showed in chapter 03
  ([JEE 2018](https://extranet.who.int/sph/sites/default/files/document-library/document/JEE%20Report%20Republic%20of%20the%20Philippines%202018.pdf)).
- **Too few epidemiologists.** The 2024 Joint External Evaluation counted 128 advanced FETP
  graduates ([report](https://www.who.int/publications/i/item/9789240116795)); a 2023 review found
  only 49 advanced graduates working in government epidemiology in 2022
  ([Creating "boots on the ground"](https://pmc.ncbi.nlm.nih.gov/articles/PMC10632096/)).
  Tools like the ones in this course help a small team do more — they do not replace it.

## Glossary in three languages

The Filipino column keeps the English term where health offices usually do. Native speakers:
corrections are welcome. The 中文 column uses Taiwan terms.

| English | Filipino | 中文 |
|---|---|---|
| case | kaso | 病例 |
| case definition | case definition (pamantayan ng kaso) | 病例定義 |
| suspect / probable / confirmed case | suspect / probable / confirmed na kaso | 疑似 / 可能 / 確診病例 |
| line list | line list (talaan ng mga kaso) | 造冊（line list） |
| surveillance | surveillance, pagbabantay | 監測 |
| notification (reporting) | pag-uulat, notification | 通報 |
| cluster | cluster (kumpol ng mga kaso) | 群聚 |
| outbreak | outbreak, paglaganap | 群突發 |
| epidemic curve | epidemic curve | 流行曲線 |
| incubation period | incubation period | 潛伏期 |
| attack rate | attack rate | 侵襲率 |
| denominator | denominator (populasyong pinaghahatian) | 分母 |
| case fatality rate (CFR) | case fatality rate (CFR) | 致死率 |
| exposure | exposure (pagkalantad) | 暴露 |
| case-control study | case-control study | 病例對照研究 |
| odds ratio (OR) | odds ratio | 勝算比 |
| risk ratio (RR) | risk ratio | 風險比 |
| confidence interval (CI) | confidence interval | 信賴區間 |
| confounding | confounding | 干擾作用 |
| prophylaxis | prophylaxis (pang-iwas na gamot) | 預防性投藥 |
| epidemic threshold | epidemic threshold | 流行閾值 |
| reporting delay | reporting delay (pagkaantala ng ulat) | 通報延遲 |
| forecast | forecast, pagtataya | 預測 |
| de-identification | de-identification (pag-alis ng pagkakakilanlan) | 去識別化 |
| sensitive personal information | sensitive personal information | 敏感性個人資料 |
| small-cell suppression | small-cell suppression (pagtatago ng maliliit na bilang) | 小格數值隱藏 |
| dashboard | dashboard | 儀表板 |

## Where to go next

- **The full book.** *Epi With Python* goes deeper, with a Legionella outbreak at a nursing
  home as its story: the [outbreak workflow](https://ancientsky.github.io/python4epi/en/chapters/outbreak-workflow/),
  [stratified analysis and confounding](https://ancientsky.github.io/python4epi/en/chapters/stratified/),
  [logistic regression](https://ancientsky.github.io/python4epi/en/chapters/logistic-regression/),
  [time series](https://ancientsky.github.io/python4epi/en/chapters/time-series/),
  [spatial epidemiology](https://ancientsky.github.io/python4epi/en/chapters/spatial/),
  [deep learning and TimesFM](https://ancientsky.github.io/python4epi/en/chapters/deep-learning/)
  and [reproducible workflows](https://ancientsky.github.io/python4epi/en/chapters/reproducibility/).
- **FETP.** If field epidemiology is your path, the DOH Field Epidemiology Training Program
  trains at frontline, intermediate and advanced levels
  ([program page on TEPHINET](https://www.tephinet.org/training-programs/philippines-field-epidemiology-training-program)).
- **Your own data, safely.** Redo chapters 03–09 on a de-identified extract from your office,
  inside your office, with your supervisor's approval. Keep the publish check.

:::::{div}
:class: ph-story
*Friday 2 October · Session hall, Santa Luz City Hall*

::::{div}
:class: ph-say-maya
**Maya:** …so dengue is still above the threshold, but the last complete week is lower than the peak. We are asking for volunteers for 4S in the coastal barangays.
::::

::::{div}
:class: ph-say-nena
**Aling Nena:** *(from the back row, quietly)* I'll bring the BHWs of Ilog. The canals are clean now — the men wear boots.
::::

::::{div}
:class: ph-say-mon
**Doc Mon:** *(texting Maya under the table)* Good sitrep. Next week we teach Jun the notebook.
::::

::::{div}
:class: ph-say-tala
**Tala:** I made a mistake or two along the way. Thank you for checking.
::::

> Every row was a neighbour. Every number was checked. *Salamat, Bantay!*
:::::

```{figure} images/cast_all.svg
:alt: The five characters of the story side by side: Maya, Doc Mon, Tala, Aling Nena and Jun.
:width: 80%
Maya, Doc Mon, Tala, Aling Nena and Jun. All of them, and Santa Luz, are fictional.
```

:::{div}
:class: ph-game ph-game-quiz
**Final check: the whole route**

1. What may you paste into an AI chat to get help with your line list?
   - ✓ Column names and two or three made-up rows — never real data.
   - The first ten rows of the real file — those are real people.
   - A photo of a notification form — it shows names and addresses.
2. Tala's code runs without an error. What next?
   - Copy the result into the report.
   - ✓ Check it on a case you can count by hand and check the denominator — running is not the same as right.
3. Who is accountable for a sitrep drafted with an AI assistant?
   - The assistant.
   - ✓ The officer who signs it — and the report says which part was AI-assisted.
4. Why is the last week of the dengue chart lower?
   - The outbreak ended that week.
   - ✓ Reporting delay — cases with onset that week were still arriving.
5. In the real Philippine system, a city's surveillance unit reports next to…
   - The DOH Epidemiology Bureau directly.
   - ✓ The provincial unit (PESU), then the regional unit (RESU), then the Bureau.
:::

:::{admonition} Baon
:class: ph-baon
- A sitrep is short, dated and checked; it says what is being done and who signed it.
- Ask with fake rows, run it, check it, record that AI helped — and a person signs.
- You can now go from a messy line list to a dashboard. Keep going: the full book and FETP.

Back to the start: [](00_start_here.md) · [Open the dashboard](/dashboard/)
:::
