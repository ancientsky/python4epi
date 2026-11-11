# Philippines Special Edition — production bible

**Working title:** *Bantay Python — Epi With Python, Philippines Edition*
(*bantay* = to watch over / guard: surveillance.)

This file is the single source of truth for everyone (human or AI) producing the
Philippines edition. Read all of it before writing anything. Progress is tracked
in the checklist at the bottom; update it when a unit is accepted.

## 1. What we are making

A condensed, self-contained sister book to *Epi With Python* for frontline
Philippine surveillance staff (Disease Surveillance Officers, ESU nurses, FETP
frontline trainees, BHW supervisors) who have **never written code**.

- Starts from zero, ends with the learner **building a striking, shareable
  outbreak dashboard** (one self-contained HTML file).
- Shorter than the main book (11 pages + 9 notebooks instead of 18 chapters).
- **AI-assisted coding is the method**: the learner asks an AI assistant for code,
  then learns to *read, run, check and correct* it. Python is taught through
  that loop, not as syntax drills.
- **Data privacy is a first-class topic**, not a footnote: Data Privacy Act of
  2012 (RA 10173), RA 11332 (mandatory reporting), what must never be pasted into
  an AI chat, de-identification, small-cell suppression before publishing.
- Philippine context everywhere: PIDSR/EDCS, ESR, ESUs (CESU/MESU/PESU/RESU),
  BHWs, typhoons and *habagat*, leptospirosis and dengue, 4S, 7-1-7 timeliness.
- Three languages, same structure, same code: **English** (source of truth),
  **繁體中文** (Taiwan terminology, see the glossary table in `/CLAUDE.md`) and
  **Filipino**.
- Visual tone: warm, festive, unmistakably Filipino. Illustrations, CSS/SVG
  animation and small interactive games carry the teaching. **No videos.**

## 2. Source material

- `book_ph/research/ph_surveillance_research_2026-11-09.json` — the research
  compiled on 2026-11-09 (surveillance systems inventory `surv.systems`, gaps,
  timeline `surv.tl`, recent outbreaks `surv.obs`, information ecosystem `info`,
  regions/provinces statistics `regions`, 237 sources in `sources`).
  **Rules for using it:** every real-world figure quoted in the book must come
  from this file (or another source you fetched and cite) and carry its source
  link. Respect its flags: anything marked estimate / inference / unverified is
  either left out or labelled as such. Never invent real-world statistics.
- `data/synthetic/ph/ph_regions.topo.json` — 18-region TopoJSON
  (object `PH_Adm1_Regions`, properties `adm1_en`, `adm1_psgc`), from
  faeldon/philippines-json-maps v1.1.1 (MIT; boundaries CC BY-IGO, credit NAMRIA
  and PSA via OCHA COD-AB). Credit it wherever it is drawn.
- The main book (`book_en/`) for tone, pedagogy and notebook conventions.

## 3. The story (fictional — every person, place and number in it is invented)

**Place.** *Santa Luz City*, a fictional river-and-coast component city of about
186,000 people in the fictional *Province of Kalinaw*. 24 barangays in three
bands: riverside (flood-prone, dense), coastal (fishing, informal settlers) and
upland (farming, far from the health centre). The Marilag River runs through it.

**People.**
- **Maya Dela Cruz** ("Ate Maya") — nurse, four months into her first post as
  Disease Surveillance Officer at the Santa Luz City Epidemiology and
  Surveillance Unit (CESU). Good with people and paper forms; has never coded.
  She is the learner's stand-in.
- **Dr. Ramon Bautista** ("Doc Mon") — provincial epidemiologist (PESU), FETP
  graduate, Maya's mentor. Asks the hard questions: *denominator? case
  definition? who can see this file?*
- **Tala** — the AI coding assistant Maya uses (*tala* = bright star). Tala is
  fast and helpful and **sometimes wrong**; the book shows both.
- **Aling Nena Ramos** — veteran Barangay Health Worker in Barangay Ilog, the
  first to notice something is off. Community voice; reminds everyone that every
  row is a neighbour.
- **Jun Villanueva** — the City Health Office IT/records clerk; guardian of the
  shared drive, source of messy spreadsheets.

**Plot.**
1. *Sat 18 July 2026*: Typhoon **Amihan** makes landfall; the Marilag overflows;
   riverside barangays are under waist-deep water for three days.
2. *Late July*: Aling Nena texts the CESU — several men who waded through the
   flood to clear debris have fever, red eyes and calf pain. Maya's notification
   forms pile up: a **leptospirosis** cluster. She has a spreadsheet, a deadline
   and no analyst. Doc Mon: "Ask Tala — but check everything it gives you."
3. Maya cleans the line list, de-identifies it, describes time/place/person,
   and runs a case-control analysis: wading without boots is the exposure; early
   doxycycline prophylaxis protected.
4. *August–September*: standing water breeds *Aedes*. Weekly **dengue** counts
   climb past the alert threshold. Maya learns thresholds, timeliness (7-1-7)
   and forecasting with a time-series foundation model.
5. *30 Sept 2026*: the City Mayor wants "one screen" for the Local Health Board.
   Maya builds the **Bantay Santa Luz dashboard** — and passes Doc Mon's privacy
   check before it goes out.

Tone: warm, a little funny, never mocking. Light Taglish in dialogue is welcome
in the English edition (with the meaning clear from context); typhoon/flood
losses are treated with respect.

## 4. Table of contents (identical in all three languages)

| # | File stem | Title (EN) | Core skills | Notebook |
|---|-----------|------------|-------------|----------|
| — | `intro.md` | Mabuhay! | what you will build, cast, how to read | — |
| 00 | `00_start_here` | Start here: you, Colab and an AI co-pilot | Colab, the Ask → Run → Check loop, privacy pledge | — |
| 01 | `01_python_with_ai` | Kumusta, Python? | variables, lists, dicts, functions, reading AI-written code, errors | `01_python_with_ai.ipynb` |
| 02 | `02_privacy_first` | Privacy first: every row is a neighbour | RA 10173 / RA 11332, PII, de-identification, safe prompting | `02_privacy_first.ipynb` |
| 03 | `03_clean_linelist` | From messy line list to clean data | pandas, dates, text cleanup, validation | `03_clean_linelist.ipynb` |
| 04 | `04_time_place_person` | Time, place, person | case definitions, epi curve, attack rate, CFR | `04_time_place_person.ipynb` |
| 05 | `05_find_the_source` | Find the source | 2×2 tables, risk ratio, odds ratio, CI | `05_find_the_source.ipynb` |
| 06 | `06_signals_and_thresholds` | Signals, thresholds and 7-1-7 | weekly series, alert/epidemic thresholds, reporting delay, 7-1-7 | `06_signals_and_thresholds.ipynb` |
| 07 | `07_forecast_timesfm` | Next month's dengue: forecasting with TimesFM | baselines, zero-shot foundation model, honest evaluation | `07_forecast_timesfm.ipynb` |
| 08 | `08_maps` | Where is it? Maps | choropleths, barangay and 18-region maps | `08_maps.ipynb` |
| 09 | `09_dashboard` | Build the Bantay Santa Luz dashboard | assembling a self-contained HTML dashboard, publish checklist | `09_dashboard.ipynb` |
| 10 | `10_wrap_up` | Sitrep, checklist and where next | AI-use checklist, PH surveillance system map, glossary, links to the full book | — |

Five acts group them in the sidebar: **I. May ulat!** (intro, 00–02) ·
**II. Bilangin natin** (03–05) · **III. Bantay** (06–08) · **IV. Ipakita** (09–10).

Every chapter page follows the same rhythm:

1. **Story beat** (≤ 150 words, a scene with dialogue) ending in the question the
   chapter answers.
2. **Concept**, explained with an illustration or animated diagram.
3. **🤖 Ask Tala** box: the actual prompt Maya types (good prompts name the
   columns, give 2–3 *synthetic* example rows, state the output wanted — never
   real data), then the code that comes back.
4. **✅ Check it** box: how to verify the AI's code (run on a tiny case you can
   count by hand, check the denominator, read the error). At least three
   chapters include a **"Tala got it wrong"** episode — a plausible AI mistake
   (wrong denominator, invented function, silent date mis-parse, leaking a name)
   and how Maya catches it.
5. **Mini-game or interactive** (see §7).
6. **🔒 Privacy stop** where relevant.
7. **Baon** (take-away) — 3 bullets — and a link to the notebook.

## 5. Datasets (all synthetic, generated by one deterministic script)

Generator: `data/synthetic/ph/generate_santa_luz.py` (seeded; documented in
`data/synthetic/ph/README.md`, which is the authoritative schema — chapter
authors read it, never guess a column name). Target files in `data/synthetic/ph/`:

- `santa_luz_barangays.geojson` + `santa_luz_barangays.csv` — 24 fictional
  barangays (name, band riverside/coastal/upland, population, households,
  centroid, flood_depth_m).
- `santa_luz_linelist_raw.csv` — the messy notification line list as Jun exports
  it (≈ 650 febrile-illness notifications 20 Jul–30 Sep 2026: leptospirosis and
  dengue): invented full names, phone numbers, street addresses, mixed date
  formats, inconsistent barangay spellings, Taglish free-text remarks,
  duplicates. Used in chapters 02–03. Names/phones are fake but must *look* like
  PII; the file header comment and README say so.
- `santa_luz_linelist.csv` — the cleaned, de-identified version (pseudonymous
  `case_id`, age, age_group, sex, barangay, onset/consult/report dates, disease,
  case classification suspect/probable/confirmed, hospitalised, outcome,
  exposures). Used from chapter 04 on.
- `lepto_case_control.csv` — cases and barangay-matched controls with exposures
  (waded_floodwater, wore_boots, skin_wound, doxy_prophylaxis, cleanup_work…),
  built so wading without boots has a clear OR and prophylaxis is protective.
- `santa_luz_dengue_weekly.csv` — weekly dengue counts by morbidity week,
  2019-W01 … 2026-W39 (rainy-season seasonality, a 2019-style peak, a COVID-era
  dip, the 2026 post-typhoon surge), plus rainfall_mm as a covariate.
- `signals_717.csv` — ~40 public-health events with emergence, detection,
  notification and early-response-completed dates for 7-1-7 metrics.
- `ph_regions_stats.csv` — real, sourced regional statistics (population 2020 /
  2024, density, urbanisation…) exported from the research JSON with a `source`
  column; `ph_regions.topo.json` already present.

Headline numbers are fixed once the generator is accepted and then quoted
consistently in all prose (the README lists them).

## 6. Site architecture

- Three MyST projects: `book_ph/en/`, `book_ph/zh/`, `book_ph/fil/`, each with
  `myst.yml`, `intro.md`, `chapters/`, `chapters/notebooks/`. Shared assets live
  once: `book_ph/_static/` (CSS, JS, logos) and `book_ph/images/` (SVG
  illustrations with text-free artwork where possible; per-language variants
  use suffixes `_en` / `_zh` / `_fil`), reached through symlinks like the main
  book's `book_en/_static`.
- Deploy paths: `/ph/` (English), `/ph/zh/`, `/ph/fil/`. No instructor edition.
- Built by `scripts/build_book.py` (same strict execution, post-build step and
  link check as the main book); `--all` builds the main four **and** these three.
- Notebooks: same Colab setup cell convention as the main book; they must run
  top-to-bottom in the strict build in well under a minute each, and on Colab.
- Content syntax limits are those in `/CLAUDE.md` (MyST, no raw HTML beyond
  `class`/`id`/`style`/`href`).
- A three-way language switch (EN / 中文 / Filipino) on every page, plus a link
  back to the full *Epi With Python* book.

## 7. Design system and interactives

**Palette.** Flag blue `#0038A8`, scarlet `#CE1126`, sun yellow `#FCD116`, with
mango, sampaguita white, banana-leaf green and jeepney chrome/teal accents; a
dark theme that still feels warm. **Motifs:** the eight-rayed sun, jeepney
signboards (chapter headers as route signs), banderitas (fiesta bunting) as
section dividers, banig weave and capiz-window patterns as textures, bangka and
bahay kubo in illustrations. Body text stays highly readable; decoration never
sits behind paragraphs. All motion respects `prefers-reduced-motion`; all
interactives work with keyboard and touch at 390 px.

**Interactive contract.** An author places a block
```
:::{div}
:class: ph-game ph-game-<name>
Fallback text shown without JavaScript.
:::
```
and `book_ph/_static/ph-games.js` replaces it after hydration (`ph-site.js` is the language-switch script). All UI strings come
from a per-language dictionary inside the script (`en`, `zh`, `fil`). Planned set:

| Name | Chapter | What the learner does |
|------|---------|-----------------------|
| `prompt-pick` | 00 | choose the better of two prompts; explains why |
| `bug-hunt` | 01 | click the line where AI-written code is wrong |
| `spot-pii` | 02 | tap the columns/cells that must not leave the office |
| `date-fixer` | 03 | sort messy date strings into the right ISO date |
| `epicurve-builder` | 04 | drop cases onto days to build an epi curve; guess the source type |
| `two-by-two` | 05 | sort people into a 2×2 table; RR/OR update live |
| `threshold-watch` | 06 | a weekly curve plays; raise the alert at the right week; 7-1-7 score |
| `forecast-guess` | 07 | draw next 8 weeks, then compare with the model and the truth |
| `map-paint` | 08 | choose class breaks/colours; see how the map's message changes |
| `lamok-patrol` | 08/09 | 4S search-and-destroy: find breeding sites before the timer ends |
| `publish-check` | 09 | approve or block dashboard elements (small cells, names, exact addresses) |
| `quiz` | any | generic multiple-choice card, questions given as a list in the fallback |

## 8. Quality bar (the director's acceptance checklist)

- Builds strict with zero new warnings; link check passes; `uv run pytest` green.
- Every code cell runs; every number in prose matches what the code prints.
- No real person's data; fake PII appears only in the raw file and chapter 02–03.
- Real-world facts carry a source link; fictional elements are never presented
  as real (each intro page says the story and data are invented).
- AI guidance is honest: shows failure modes, never implies AI output can be
  trusted unchecked, never suggests pasting identifiable data into an AI tool.
- zh edition follows the Taiwan terminology table; Filipino edition reads as
  natural Filipino as used in Philippine health offices (English technical terms
  are kept where practitioners keep them) and carries a note inviting
  native-speaker corrections.
- Looks right in light/dark, desktop and 390 px; no console errors.

## 9. Progress

- [x] P1 infrastructure: build script, three MyST skeletons, tests, workflows
- [x] P1 datasets + README + tests
- [x] P1 design system: CSS and illustrations (see STYLEGUIDE.md)
- [x] P1 interactives (ph-games.js, GAMES.md)
- [x] P2 English chapters 00–02 + notebooks (browser QA passed)
- [x] P2 English chapters 03–05 + notebooks (browser QA passed)
- [x] P2 English chapters 06–08 + notebooks (browser QA passed)
- [x] P2 English chapters 09–10 + dashboard (browser QA passed)
- [~] P3 中文 edition — both halves translated; copy-chief pass (harmonise terms, build, browser QA) was IN PROGRESS when work paused
- [~] P3 Filipino edition — both halves translated; copy-chief pass (harmonise terms, fix shared fil strings, build, browser QA) was IN PROGRESS when work paused
- [ ] P4 full build, browser QA (light/dark, desktop/phone), fixes

## 10. Director's handoff notes (paused 2026-11-11 ~16:55 Asia/Taipei; resume 19:00)

Done and committed: staleness audit + fixes for the main book (34 findings; reports in
`book_ph/handoff/audit_*.md`, `fix_*_report.md`), chapter 11 TimesFM 3.0 rewrite + notebook
(`handoff/timesfm_report.md`), PH infrastructure, datasets, theme, games, English edition (QA passed,
`handoff/qa_en_report.md`), dashboard, first-draft zh and fil translations.

Paused mid-flight (workers were stopped; their partial edits are in the tree, unreviewed):
1. **zh copy chief** — harmonise the two translators' terms, check completeness against English, build
   `--series ph --lang zh` strict, browser QA. Decided glossary: box titles 問問 Tala / Tala 說 /
   檢查一下 / Tala 搞錯了 / 隱私停看聽 / Baon（帶走重點）; `barangay` kept in English with first-use gloss
   「barangay（描籠涯，菲律賓最基層的行政區，類似台灣的村里）」; 村里衛生員（BHW）; 市／省流行病學與監測單位
   （CESU／PESU）; 疾病監測專員（DSO）; 小格遮蔽; 單一時點共同感染源／持續性共同感染源／連鎖傳播;
   警戒閾值／流行閾值; plus the Taiwan terminology table in CLAUDE.md.
2. **fil copy chief** — same for Filipino, plus fixes to shared fil strings reported by the translators:
   dashboard ("lisensya"→"lisensiya", forest-plot title, band label "Lugar", "Protektado…" overstates an
   OR); games ("Good try." untranslated, "Laro ulit"→"Maglaro ulit", "Tinaob!"→"Itinaob!", plant-saucer
   item must say throw away the *water*, awkward threshold-watch sentence); SVGs (`timeline_717_fil.svg`
   wording, `mosquito_4s_fil.svg` "proteksiyon"); check the ch09 fil notebook's dashboard link
   (`/ph/fil/dashboard/`) works under the `/python4epi/` base path.
   On resume: re-dispatch both passes (they must first look at what is already changed in the tree).

Still to do after those two:
3. Full seven-edition build `scripts/build_book.py --all --site-dir <tmp>` (strict, link check) + `uv run pytest`.
4. Final director review of screenshots (zh, fil, assembled site); tick the Progress list; final commit.
5. Delete the recurring check-in scheduled task ("python4epi 總監復工檢查") when everything is done.
6. Final report to the user, including items needing their decision: the dashboard shows city-wide
   totals unsuppressed (incl. 1 dengue death); zh wording of barangay/box titles; `videos/` scripts still
   use `slide_layouts[5]`; 8 pre-existing ruff findings; external links that could not be verified from
   the sandbox; legal statements (RA 10173 / RA 11332) and all Filipino text need a native/legal review;
   six Hugging Face hosts were added to the `first_flight` environment allow-list.

Sandbox notes for whoever builds: run builds with `JUPYTER_CONFIG_DIR=book_ph/handoff/jcfg` (Jupyter
refuses to run as root otherwise); the theme zip download is blocked here, so each project needs
`_build/templates/site/<sha256>/` seeded (copy from another project's `_build/templates`, or git-fetch the
pinned sha); notebooks are executed from the repo root (nbclient with path '.'), not with plain nbconvert.
Worker briefs: `book_ph/handoff/writer_brief.md`, `translator_brief.md`. Workers never commit; the
director commits. The `book_ph/handoff/` folder is temporary and should be removed before the final commit.
