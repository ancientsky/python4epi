# Santa Luz City datasets (Philippines edition)

> **ALL SANTA LUZ DATA ARE SYNTHETIC.** Santa Luz City, the Province of Kalinaw,
> Typhoon Amihan, the Marilag River, every barangay polygon, every person, name,
> phone number, street address and every count in the `santa_luz_*`,
> `lepto_case_control` and `signals_717` files are **invented** for teaching.
> They describe no real place, patient or event. Names and phone numbers in
> `santa_luz_linelist_raw.csv` are fake but deliberately *look* like PII so that
> chapters 02–03 can teach privacy on them.
> The only real-world data here are `ph_regions_stats.csv` (exported, with a
> source for every value, from the book's research file) and `ph_regions.topo.json`.

This README is the **authoritative schema**. Chapter authors read column names
and the headline numbers from here; never guess them.

| File | Rows | Used in | Real or synthetic |
|------|-----:|---------|-------------------|
| `santa_luz_barangays.csv` | 24 | 04, 08, 09 | synthetic |
| `santa_luz_barangays.geojson` | 24 features | 08, 09 | synthetic |
| `santa_luz_linelist_raw.csv` | 637 (+1 note line) | 02, 03 | synthetic, fake PII |
| `santa_luz_linelist.csv` | 618 | 04 → 09 | synthetic, de-identified |
| `lepto_case_control.csv` | 360 | 05 | synthetic |
| `santa_luz_dengue_weekly.csv` | 404 | 06, 07, 09 | synthetic |
| `signals_717.csv` | 40 | 06 | synthetic |
| `ph_regions_stats.csv` | 18 | 08 | **real**, sourced |
| `ph_regions.topo.json` | 18 regions | 08 | **real** boundaries (not generated) |

## Regenerating

```bash
uv run python data/synthetic/ph/generate_santa_luz.py
uv run pytest tests/test_ph_data.py      # byte-for-byte check, schemas, headline numbers
```

`generate_santa_luz.py` is deterministic: one master seed (`SEED = 20260755`)
feeds independent `numpy.random.Generator` streams per component (geometry,
population, leptospirosis, rainfall, dengue, raw-file mess, case-control,
signals), so retuning one component does not reshuffle the others. Nothing
depends on the wall clock. All CSVs are UTF-8 with `\n` line endings.

**Seed.** The design parameters were fixed first; the master seed was then
picked from a scan of 20260718–20260757 as the first one in which the random
draws tell the story cleanly (dengue first crosses its threshold in the
post-typhoon surge, the crude wading OR lies in 4–7 and is mildly confounded,
boots and doxycycline look protective). The generator refuses to write files if
the dengue threshold is crossed before 2026-W31.

## Story calendar

| Date | Event |
|------|-------|
| Sat 18 Jul 2026 | Typhoon Amihan makes landfall (449.1 mm of rain in 2026-W29) |
| 18–20 Jul | Waist-deep floodwater in the 8 riverside barangays (3 days) |
| 21 Jul – ~2 Aug | Clean-up of debris and canals |
| Mon 20 Jul (2026-W30) | Enhanced post-typhoon line list starts (onsets from this date) |
| Mon 27 Jul | Peak leptospirosis onset day (19 cases); Aling Nena texts the CESU |
| 3–9 Aug (2026-W32) | Dengue first exceeds its epidemic threshold |
| Wed 30 Sep 2026 | Data freeze: the line list holds every case **reported** by this date |

## Headline numbers (quote these exactly)

### Population (santa_luz_barangays.csv)

| | riverside | coastal | upland | **city** |
|---|---:|---:|---:|---:|
| Barangays | 8 | 8 | 8 | **24** |
| Population | 96,064 | 58,852 | 31,084 | **186,000** |

### Line list (santa_luz_linelist.csv, 618 cases)

| | Leptospirosis | Dengue |
|---|---:|---:|
| Cases | **230** | **388** |
| Confirmed / probable / suspect | 119 / 52 / 59 | 49 / 172 / 167 |
| Hospitalised | 143 (62.2%) | 206 (53.1%) |
| Deaths | **20** | **1** |
| CFR (deaths / cases) | **8.7%** | **0.3%** |
| Male | 155 (67%) | 50% |
| Median age (years) | 32 | 18 |
| Onset range | 22 Jul – 23 Aug | 20 Jul – 27 Sep |
| Peak | onset week 2026-W31 (108 cases); peak day 27 Jul (19) | onset week 2026-W37 (63) |
| Dengue severity | — | 241 without warning signs, 132 with warning signs, 15 severe |
| Median onset → consult / consult → report | 3 d / 2 d | 3 d / 1 d |
| Median consult → lab confirmation | 18 d (reference lab) | 8 d |

Leptospirosis cases by onset week: W30 35, W31 108, W32 68, W33 15, W34 2.

**Attack rates per 10,000** (cases ÷ band population × 10,000):

| | riverside | coastal | upland | city |
|---|---:|---:|---:|---:|
| Leptospirosis | **19.7** | 5.6 | 2.6 | 12.4 |
| Dengue | 20.3 | **29.6** | 6.1 | 20.9 |

Highest barangay attack rates: leptospirosis Tabing-Ilog 29.8, Ilog 29.1;
dengue Talaba 43.4, Buhangin 35.5 (per 10,000).

Seven cases have a missing age, twelve a missing consultation date, two a
missing onset date (see cleaning rule C4), and 14 leptospirosis cases have
missing exposure answers — so counts by these fields need `dropna` awareness.

### Case-control study (lepto_case_control.csv)

120 cases, 240 barangay-matched controls (8 riverside barangays). Crude odds
ratios with Woolf 95% CI (a = exposed cases, b = exposed controls,
c = unexposed cases, d = unexposed controls):

| Exposure | a | b | c | d | OR | 95% CI | True design value |
|----------|--:|--:|--:|--:|---:|--------|-------------------|
| `waded_floodwater` | 90 | 84 | 30 | 156 | **5.57** | 3.41–9.10 | 6.0 without boots / 1.8 with boots |
| `wore_boots` (waders only, n = 174) | 10 | 22 | 80 | 62 | **0.35** | 0.16–0.80 | 0.30 (= 1.8 / 6.0) |
| `doxy_prophylaxis` | 11 | 46 | 109 | 194 | **0.43** | 0.21–0.86 | 0.30 |
| `skin_wound` | 54 | 51 | 66 | 189 | 3.03 | 1.89–4.87 | 2.0 |
| `cleanup_work` | 67 | 68 | 53 | 172 | 3.20 | 2.03–5.05 | 1.6 |
| male sex | 89 | 121 | 31 | 119 | 2.82 | 1.75–4.57 | 1.3 |
| `rats_near_home` | 57 | 112 | 63 | 128 | 1.03 | 0.67–1.60 | 1.0 (null) |
| waded **without** boots vs everyone else | 80 | 62 | 40 | 178 | 5.74 | 3.56–9.25 | — |

**The confounder to notice: `cleanup_work`.** Clean-up volunteers waded far more
often and had their own extra risk, so the crude wading OR (5.57) shrinks to
**4.28** (Mantel–Haenszel, stratified by `cleanup_work`). Stratum ORs: 5.56
(no clean-up), 2.88 (clean-up). Sex is confounded the same way (crude 2.82 vs a
true 1.3). Crude ORs differ from the true design values because of this
confounding, mutual confounding between exposures and sampling error — a point
worth making in chapter 05.

True design values = the conditional odds ratios of the logistic model that
generated the disease (`TRUE_OR` in the generator): waded without boots 6.0,
waded with boots 1.8, skin wound 2.0, doxycycline 0.30, clean-up work 1.6,
male 1.3, rats near home 1.0, plus 5.0 per metre of barangay flood depth
(constant within a matched set, so not estimable from this study).

### Weekly dengue (santa_luz_dengue_weekly.csv)

* Epidemic threshold for ISO week *w* = mean + 2 SD (sample SD, ddof = 1) of
  the counts in weeks *w*−1, *w*, *w*+1 of the non-epidemic baseline years
  **2022–2025** (12 values; 2019 is excluded as an epidemic year, 2020–2021 as
  COVID-19-disrupted years). `epidemic_threshold()` in the generator is the
  reference implementation.
* **2026 first exceeds the threshold in 2026-W32 (3–9 Aug): 33 cases vs a
  threshold of 17.5.** It stays above it every week through W39. No 2026 week
  before W32 is above it.
* 2026 weekly cases W28–W39: 4, 6, 14, 11, **33**, 28, 48, 34, 58, **63**, 54, 45.
  W39 is incomplete (reporting delay at the freeze) — that is why it dips.
* Annual totals: 2019 713 (epidemic year, peak W33), 2020 214 and 2021 236
  (COVID-era dip), 2022 479, 2023 386, 2024 443, 2025 353, 2026 (to W39) 497.
* Rainfall leads cases: the correlation between `rainfall_mm` shifted by *k*
  weeks and `cases` is highest at *k* = 7 (r = 0.56). The wettest week of the
  whole series is 2026-W29 (Amihan).

### 7-1-7 (signals_717.csv, 40 events, Jan 2025 – Aug 2026)

| Target | Met | Missed |
|--------|----:|-------:|
| Detection ≤ 7 days after emergence | 26 (65%) | 14 |
| Notification ≤ 1 day after detection | 31 (78%) | 9 |
| Early response complete ≤ 7 days after notification | 27 (68%) | 13 |
| **All three** | **15 (38%)** | 25 |

Median delays: detection 6 d, notification 1 d, response 6 d. The last two
events are the story's: leptospirosis in Ilog (EV-039: detection 4 d ✓,
notification 2 d ✗, response 5 d ✓) and the dengue surge in Baybay (EV-040:
emergence = Monday of the threshold week, detection 7 d ✓, notification 1 d ✓,
response 10 d ✗).

## Schemas

Missing values are empty cells in every CSV. Binary columns are `0`/`1`.
Dates are ISO `YYYY-MM-DD` except in the raw file.

### santa_luz_barangays.csv

| Column | Type | Values | Meaning |
|--------|------|--------|---------|
| `barangay_id` | str | `SL01`–`SL24` | key; joins the GeoJSON, line list and case-control file |
| `barangay` | str | canonical name, e.g. `Ilog`, `Santo Niño` | |
| `band` | str | `riverside` (SL01–08), `coastal` (SL09–16), `upland` (SL17–24) | |
| `population` | int | 3,173–13,411 | residents (sums to 186,000) |
| `households` | int | | population ÷ mean household size (4.3 / 4.8 / 4.5 by band) |
| `area_km2` | float | | polygon area (equirectangular approximation) |
| `density_per_km2` | int | | population ÷ area |
| `centroid_lon`, `centroid_lat` | float | | polygon centroid (WGS 84), for labels |
| `flood_depth_m` | float | 0.0–1.4 | peak floodwater depth during Amihan |

### santa_luz_barangays.geojson

RFC 7946 FeatureCollection, WGS 84 lon/lat, 24 `Polygon` features (exterior
rings counter-clockwise) with properties `barangay_id`, `barangay`, `band`,
`population`, `flood_depth_m`. Polygons share edges exactly (no gaps or
overlaps) and together form one block: a southern coastal strip, the Marilag
valley floor (riverside) across the middle, uplands to the north; the river
reaches the sea at Wawa in the south-east.

**The coordinates are a made-up frame**: the city sits in a box around
130.10–130.30 °E, 14.80–14.89 °N, in the open Philippine Sea roughly 600 km
east of Luzon, where there is no land — so the map cannot be mistaken for a
real place, and it must never be drawn on top of the real 18-region map.
Read it with `geopandas.read_file(...)`.

### santa_luz_linelist_raw.csv (the messy export)

The first line is a note (`# SYNTHETIC TRAINING DATA ... Read with skiprows=1.`);
the file contains no other `#`, so `comment="#"` also works. All 19 columns are
free text as typed by different encoders:

| Column | Example values |
|--------|----------------|
| `Date Reported`, `Date of Onset`, `Date Consulted`, `Date Lab Confirmed` | `07/24/2026`, `7/24/2026`, `2026-07-24`, `24-Jul-26`, `July 24 2026`, `July 24, 2026`, `46227` (Excel serial); one style per row |
| `Reporting Unit` | `Santa Luz City District Hospital`, `Kalinaw Provincial Hospital`, `Santa Luz City Health Office`, `Marilag Medical Clinic`, `St. Agatha Family Clinic`, `Ilog Barangay Health Station` … |
| `Patient Name` | `Juan P. Santos` (invented; **PII-shaped**) |
| `Sex` | `M`, `Male`, `male`, `m`, `lalaki`, `F`, `Female`, `female`, `f`, `babae` |
| `Age` | `34`, `34 y/o`, `34 yrs`, `34yo`, `8 mos`, `8 months`, `8mos`, blank, one `150` |
| `Contact No.` | `+63 900 555 1234`, `0900-555-1234`, `09005551234`, `0900 555 1234`, `wala`, `none`, blank — all in the fictional 0900 555 block |
| `Address` | `253 Rizal St., Purok 2`, `Blk 19 Lot 1, Sampaguita St.` (invented) |
| `Barangay` | `Ilog`, `Brgy. Ilog`, `ILOG`, `Bgy Ilog ` (trailing space), `ilog`, `Barangay Ilog`, `Sto. Nino`, `Tabing Ilog`, typos `Pobalcion`, `Dalampasig`, `Kawayan` |
| `Disease` | `Leptospirosis`, `Lepto`, `LEPTO`, `leptospirosis`, `Dengue`, `DENGUE`, `Dengue Fever`, `DF`, `dengue` |
| `Classification` | `Suspect`, `SUSPECT`, `Suspected`, `sus`, `Probable`, `PROBABLE`, `prob.`, `Confirmed`, `CONFIRMED`, `Conf`, `lab confirmed` |
| `Admitted`, `Waded in Floodwater`, `Did Cleanup Work` | `Y`, `Yes`, `yes`, `oo`, `Oo`, `N`, `No`, `no`, `hindi`, `Hindi`, blank, `N/A` (dengue rows) |
| `Outcome` | `Alive`, `alive`, `A`, `buhay`, `Died`, `D`, `Namatay`, `Expired` |
| `Dengue Severity` | `Without warning signs`, `w/o warning signs`, `no WS`, `With warning signs`, `w/ warning signs`, `WS+`, `Severe dengue`, `SEVERE`, `SD`; blank for leptospirosis |
| `Remarks` | Taglish free text, e.g. `lumusong sa baha, walang bota`, `low platelet sa CBC`, `anak/kapatid ni Dennis (kapitbahay)` — can contain PII about *other* people |

The mess, counted: 19 duplicate rows (6 exact copies, 13 near-duplicates: the
same patient re-notified by the City Health Office with a re-typed name,
another date style and barangay spelling), 22 rows with Excel serial dates, 1
age of `150`, 2 onset dates typed one month late (after the consultation), 6
blank ages, 12 blank consultation dates, 14 leptospirosis rows with blank
exposure answers, 5 barangay typos.

### santa_luz_linelist.csv (clean, de-identified)

One row per case (618). No names, phones, addresses, reporting units or remarks.

| Column | Type | Values | Meaning |
|--------|------|--------|---------|
| `case_id` | str | `SLC-0001`… | pseudonymous ID, in raw-file order of first appearance |
| `disease` | str | `leptospirosis`, `dengue` | |
| `case_class` | str | `suspect`, `probable`, `confirmed` | at the 30 Sep freeze: confirmed = lab result back (lepto MAT/PCR at the reference lab; dengue RT-PCR); probable = positive rapid test (lepto RDT; dengue NS1/CBC criteria); else suspect |
| `date_onset` | date | 2026-07-20 … 2026-09-27; 2 missing | symptom onset |
| `date_consult` | date | 12 missing | first consultation |
| `date_report` | date | 2026-07-22 … 2026-09-30 | notification received by the CESU |
| `date_lab_confirmed` | date | only when `case_class == confirmed` | positive lab result |
| `age` | int | 0–93; 7 missing | completed years (infants = 0) |
| `age_group` | str | `0-4`, `5-14`, `15-24`, `25-44`, `45-64`, `65+` | missing when age is |
| `sex` | str | `M`, `F` | |
| `barangay_id`, `barangay`, `band` | str | as in the barangay file | residence |
| `hospitalised` | 0/1 | | admitted |
| `outcome` | str | `alive`, `died` | status at the freeze |
| `dengue_severity` | str | `no_warning`, `warning_signs`, `severe`; blank for leptospirosis | WHO 2009 dengue classification |
| `waded_floodwater` | 0/1 | blank for dengue and 14 lepto rows | waded in floodwater after Amihan (CIF question) |
| `cleanup_work` | 0/1 | blank for dengue and 14 lepto rows | did flood clean-up work |

### Cleaning rules (raw → clean)

Chapter 03 teaches these; `reference_clean()` in `tests/test_ph_data.py`
implements them and must reproduce `santa_luz_linelist.csv` byte for byte.

* **C1 Read** with `skiprows=1`, every column as text, blanks as empty strings.
* **C2 Standardise every field:**
  * **Dates** — D1 `M/D/YYYY` with or without leading zeros is always
    month/day/year (Philippine convention; there are no day/month dates);
    D3 `YYYY-MM-DD`; D4 `DD-Mon-YY` (years are 20YY); D5 `Month D YYYY` or
    `Month D, YYYY`; D6 a 5-digit number is an Excel serial (days since
    1899-12-30, e.g. `46227` = 2026-07-24); blank = missing. Do not let
    `pd.to_datetime` guess: Excel serials are not dates to it.
  * **Barangay** — B1 strip accents (`ñ` → `n`), lower-case, trim; B2 remove a
    leading `barangay`, `brgy`, `brgy.`, `bgy`, `bgy.`; B3 `sto`/`sto.` →
    `santo`; B4 hyphens and dots → spaces, collapse spaces; B5 fix the known
    typos `pobalcion` → `poblacion`, `dalampasig` → `dalampasigan`,
    `kawayan` → `kawayanan` (exact matches only); then look the key up among
    the canonical names normalised the same way and take `barangay_id`,
    canonical `barangay` and `band` from `santa_luz_barangays.csv`.
  * **Age** — A1 take the leading whole number; A2 if the text contains `mo`
    it is months → years = months // 12 (so `8 mos` → 0); A3 ages above 110
    are impossible → missing (the `150`). Then derive `age_group`.
  * **Sex** `m`/`male`/`lalaki` → `M`, `f`/`female`/`babae` → `F` (case-insensitive).
  * **Disease** starts with `lep` → `leptospirosis`; starts with `deng` or is
    `df` → `dengue`.
  * **Classification** contains `conf` → `confirmed`; starts with `prob` →
    `probable`; starts with `sus` → `suspect`.
  * **Yes/no** `y`/`yes`/`oo` → 1, `n`/`no`/`hindi` → 0, blank/`n/a` → missing.
  * **Outcome** `alive`/`a`/`buhay` → `alive`; `died`/`d`/`namatay`/`expired` → `died`.
  * **Dengue severity** (checked in this order) contains `severe` or is `sd` →
    `severe`; contains `without`/`w/o` or is `no ws` → `no_warning`; contains
    `with`/`w/` or is `ws+` → `warning_signs`. Leptospirosis rows → missing.
* **C3 De-duplicate** on (name normalised as upper case, dots removed, single
  spaces; disease; parsed onset date), keeping the **first** row. This removes
  all 19 duplicates (exact copies would also go with `drop_duplicates()`, the
  13 near-duplicates would not).
* **C4 Impossible dates** — if onset is after the consultation date (or after
  the report date when consultation is blank), set onset to missing (2 rows;
  in real life: call the DRU). Do this after C3.
* **C5 Pseudonymise** — number the remaining rows `SLC-0001`, `SLC-0002`, … in
  file order.
* **C6 Drop direct identifiers** — name, contact number, address, reporting
  unit and remarks never reach the clean file.
* **C7 Column order and names** as in the schema above; binary/age columns as
  nullable integers (`Int64`).
* **C8 Save** with `to_csv(index=False)`.

### lepto_case_control.csv

Cases: every probable/confirmed leptospirosis case aged ≥ 15 living in a
riverside barangay (120). Controls: two residents aged ≥ 15 without
leptospirosis from the case's barangay, drawn at random from the synthetic
population (240). Interviews are complete (no missing answers).

| Column | Type | Values | Meaning |
|--------|------|--------|---------|
| `study_id` | str | `CC-001`…`CC-360` | participant ID |
| `matched_set` | int | 1–120 | one case + its two controls |
| `status` | str | `case`, `control` | |
| `case` | 0/1 | | 1 = case |
| `case_id` | str | `SLC-…` for cases, blank for controls | joins `santa_luz_linelist.csv` |
| `barangay_id`, `barangay` | str | riverside barangays | matching variable |
| `age` | int | ≥ 15 | years |
| `sex` | str | `M`, `F` | |
| `waded_floodwater` | 0/1 | | waded in floodwater 18 Jul – 2 Aug |
| `wore_boots` | 0/1 | **blank when `waded_floodwater == 0`** | wore boots whenever in floodwater |
| `skin_wound` | 0/1 | | cut or wound on the legs/feet at the time |
| `doxy_prophylaxis` | 0/1 | | took doxycycline prophylaxis (given at evacuation centres and to clean-up volunteers) |
| `cleanup_work` | 0/1 | | did flood clean-up work |
| `rats_near_home` | 0/1 | | saw rats near the house (a null exposure) |

For a case, `waded_floodwater`/`cleanup_work` agree with the line list wherever
the line list has an answer.

### santa_luz_dengue_weekly.csv

| Column | Type | Meaning |
|--------|------|---------|
| `iso_year`, `iso_week` | int | ISO 8601 year and week of onset (2020 has a W53) |
| `morbidity_week` | str | `2019-W01` … `2026-W39` |
| `week_start` | date | Monday of the week |
| `cases` | int | dengue cases by week of onset |
| `rainfall_mm` | float | weekly rainfall at the (fictional) city weather station |

This file uses ISO weeks (Monday–Sunday) as its morbidity weeks; it makes no
claim about the official PIDSR morbidity-week calendar.

Model: cases ~ negative binomial (dispersion k = 20) with mean = year factor ×
(2.5 + 0.11 × rainfall averaged over lags 5–9 weeks, weights 0.1/0.2/0.4/0.2/0.1)
plus, after Amihan, a gamma-shaped surge of 330 expected extra cases peaking
6 weeks after landfall. Year factors: 2019 1.7, 2020 1.0 until W11 then 0.45
(COVID-19), 2021 0.5, 2022 1.1, 2023 0.9, 2024 1.0, 2025 0.95, 2026 0.75.

**Reconciliation with the line list.** For 2026-W30 … W39, `cases` equals the
number of dengue rows in `santa_luz_linelist.csv` with `date_onset` in that ISO
week (onset weeks of the line list's 388 dengue cases: all fall in W30–W39; no
dengue case with onset 28–30 Sep had been reported by the freeze). Because the
line list holds cases *reported* by 30 Sep, the last week (W39) is
right-truncated, exactly as a real extract would be. Weeks before 2026-W30 are
drawn from the model.

### signals_717.csv

| Column | Type | Meaning |
|--------|------|---------|
| `event_id` | str | `EV-001`…`EV-040`, in order of emergence |
| `disease` | str | e.g. `dengue`, `measles`, `acute watery diarrhoea`, `rabies (human)` |
| `barangay` | str | canonical barangay name |
| `date_emergence` | date | first case onset / event start |
| `date_detection` | date | event first recorded by any part of the system |
| `date_notification` | date | reported to the public-health authority (PESU) |
| `date_response_complete` | date | all early-response actions completed |
| `bottleneck` | str | what caused each missed target (several joined with `; `), or `none` when all three targets were met |

7-1-7: detect within 7 days of emergence, notify within 1 day of detection,
complete early response within 7 days of notification.

### ph_regions_stats.csv (real data)

One row per region (18, current boundaries with the Negros Island Region),
exported by `make_regions()` from
`book_ph/research/ph_surveillance_research_2026-11-09.json` (`regions.regs`).
Nothing is estimated here; a value the research did not find is blank.

| Column | Meaning |
|--------|---------|
| `region_id` | 2-digit PSGC region code (text, keep leading zero) |
| `adm1_psgc` | integer PSGC code; **joins `adm1_psgc` in `ph_regions.topo.json`** |
| `psgc` | 10-digit PSGC code as text |
| `region_short`, `region_name`, `region_name_zh`, `island_group` | labels |
| 13 value columns | see below |

Each value column `X` comes with `X_year` (reference year), `X_source`
(`cited` = taken from a fetched source; `derived` = arithmetic by the
researcher from cited inputs, no URL of its own) and `X_source_url` (resolved
through the research file's `alias` → `sources`). Year/source/URL are blank
when the value is blank.

| Value column | Coverage | Notes |
|--------------|---------:|-------|
| `population_2020` | 16 | 2020 CPH; VI, VII, IX and NIR are *derived* (re-aggregated to current boundaries); XII and BARMM blank |
| `population_2024` | 18 | 2024 POPCEN |
| `land_area_km2` | 18 | |
| `density_2024_per_km2` | 18 | derived: population_2024 ÷ land_area_km2 |
| `urbanization_2020_pct` | 0 | regional values not found by the research |
| `poverty_incidence_2021_pct`, `poverty_incidence_2023_pct` | 18 | among population; 2023 BARMM still includes Sulu |
| `grdp_2024_php_million`, `grdp_per_capita_2024_php` | 18 | current prices |
| `functional_literacy_2024_pct` | 18 | FLEMMS 2024, ages 10–64 |
| `household_internet_2024_pct` | 4 | |
| `hospital_beds_2019`, `hospital_beds_per_10k_2019` | 16 | **17-region boundaries** (NIR did not exist; VI/VII are the old regions); Caraga blank after fact-check; per-10k is derived |

Caveats from the research (`regions.model`): the 17 → 18 region change (RA 12000,
2024: NIR from Negros Occidental incl. Bacolod, Negros Oriental and Siquijor)
and Sulu's move from BARMM to Region IX make some cross-year and BARMM/IX
comparisons unsafe. Quote any figure with its `_source_url`.

### ph_regions.topo.json (not generated)

18-region TopoJSON, object `PH_Adm1_Regions`, properties `adm1_en`,
`adm1_psgc`. From **faeldon/philippines-json-maps v1.1.1** (MIT licence for the
repository); underlying boundaries **CC BY-IGO — credit NAMRIA and PSA via
OCHA COD-AB**. Credit it wherever it is drawn, e.g. *"Boundaries: NAMRIA, PSA
via OCHA COD-AB (CC BY-IGO); TopoJSON: faeldon/philippines-json-maps (MIT)."*
