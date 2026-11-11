# QA report: Bantay Python, English edition (book_ph/en)

Final state: `build_book.py --series ph --lang en` is strict and passes with **0 warnings**, and the link check passes. `uv run pytest -q` passes in full. `uv run ruff check scripts/build_ph_dashboard.py tests` passes.

Browser QA covered 22 URLs (all 21 pages plus the dashboard) in 4 modes: 1280 and 390 px, light and dark. There are no React hydration errors, no horizontal scroll at 390 px, no raw MyST text (`:::`, `{button}`, class names), no broken images, no images without alt text, and every `ph-game` block mounts. The language switch (EN/中文/FIL) and the "Full book" link appear on every page, and the Colab link appears on all 9 notebook pages.

## 1. Issues found and what I changed

### Games disagreed with the book (book_ph/_static/ph-games.js; en, zh and fil strings kept in sync)

| Game | Problem | Fix |
|---|---|---|
| `threshold-watch` (TW data and `baseline()`, about lines 1441–1470) | Invented 2021–2025 baseline and an invented 2026 curve (peak 71). The threshold was built from the same week only. | Now uses the real series: 2026-W20…W39 and the baseline years 2022–2025 over weeks w−1, w and w+1 (12 values), as in chapter 06 and the README. The first crossing is W32 (33 vs 17.5) and detection is 10 Aug, matching EV-040. The intro and the "how is it computed" panel now say 2022–2025 and the 12-value window. |
| `epicurve-builder` (CURVES, about lines 1118–1141) | The leptospirosis scenario gave "point source" as the answer and "incubation 5–14 days". Chapter 04 says continuing common source, and WHO gives 7–10 days. The Baybay dengue scenario used numbers unrelated to Baybay's data. | Leptospirosis is now a 1-in-4 sample of the real daily curve (22 Jul–10 Aug), answer "continuing", with the incubation as "usually 7–10 days, range 2–30 (WHO)". The water scenario is now a labelled practice **point source** (one shared lunch), so all three shapes remain. The dengue scenario is relabelled "Practice scenario: … made-up village". |
| `ph-quiz-ch04` bank (about line 748) | Used "wading after Amihan" as the example of a point source. Ilog CFR was given as 31 cases, 2 deaths and 6,200 residents. | The point-source example is now "one shared meal". Ilog now uses its real numbers: 39 cases, 6 deaths, 13,411 residents, CFR 15.4%. |
| `bug-hunt` (about lines 556 and 593) | Same invented Ilog numbers. The attack rate was per 1,000. | Real Ilog numbers. The attack rate is now per 10,000 (`attack_rate(39, 13411)` gives 29.08, which matches the README's 29.1). |
| `prompt-pick` | Example prompt used a rate per 1,000. | Changed to per 10,000, the book's unit. |
| `map-paint` (BRGY, about lines 1840–1975) | 24 invented barangay names (Bangkaan, Tulay, Bundok…), invented populations, leptospirosis counts and rates per 1,000. Chapter 08 maps **dengue** per 10,000. | Now the 24 real Santa Luz barangays with real populations and dengue counts. Long names are split onto two lines. Rates are per 10,000. Mission 1's answer is Talaba and the "most cases" barangay is Ilog. The rate message now says the coast stands out. The "only N barangays in the top class" count is computed instead of hard-coded. The aria label is corrected (left/centre/right). |
| `forecast-guess` (FORECASTS, about line 1668) | Invented series and an "illustrative TimesFM-style" model. Round 2 said the truth left the band "from the second week" and that rainfall "can help". Chapter 07 says the truth missed in all 8 weeks and rainfall barely helped. | Both rounds now use real weeks and the cached TimesFM 3.0 forecasts from `data/tsfm_cache/ph07_dengue.json`: backtest origin 2025-W31 and the take-off forecast with history to 2026-W31. The lessons now match chapter 07 (7 of 8 weeks in band; 0 of 8). The model is labelled "TimesFM 3.0 (chapter 07 run)". |
| `publish-check` | Tiles said 1,284 dengue cases and 7 deaths; the curve, the barangay table (including "Bundok", which is not a Santa Luz barangay) and the age×sex table were invented. | All now use dataset numbers: 618 cases and 21 deaths; W30–W39 dengue counts; Ilog 39, Pampang 31, Kawayanan 5, Talahib 1; real age×sex counts. |
| `two-by-two` | The doxycycline OR was 0.11 while chapter 05 says 0.43 for the same question. | Both rounds are now labelled "Practice cohort … (made-up numbers)" and "Practice case-control: a small pilot of 20 people (made-up numbers, not Maya's 360)". |
| `spot-pii`, `prompt-pick` | Fake phones 0917/0918 555 … use real mobile prefixes. Case IDs used the `SLZ-` prefix. | Phones are in the README's fictional 0900 555 block. IDs use the book's `SLC-` prefix. |
| Legal claims in games | "PhilHealth number = sensitive personal information under RA 10173" and "pasting a name is a disclosure under the DPA". Neither is in the research file and I could not fetch the law (lawphil and privacy.gov.ph are blocked). | Reworded without the legal claim, for example "Government-issued ID number: it points to exactly one person". |

### Chapters (book_ph/en)

- **intro.md:67.** The cast grid changed from `2 3 5 5` to `2 3 3 3`. At 5 columns the cards were about 100 px wide and "EPIDEMIOLOGIST" overflowed its card. STYLEGUIDE.md has the same change.
- **00_start_here.md:17.** "That's eleven this week" (said on a Monday) became "eleven forms since Friday".
- **00_start_here.md, quiz.** The quiz said "Colab runs everything in the browser", which contradicts the chapter (Colab runs on Google's computers). Fixed.
- **02_privacy_first.md:52–55.** I removed two unsourced legal statements: the RA 11332 prohibited-acts wording and "the DPA treats health as sensitive personal information". The text now says the DPA governs personal information, health is among the most sensitive things a file holds, and the reader should ask their DPO.
- **03_clean_linelist.md:8–10.** The story date was Tue 28 Jul, the day before chapter 02 (Wed 29 Jul), while chapter 03 continues from it. It is now Thu 30 Jul, and Jun's line now continues on from chapter 02.
- **04_time_place_person.md, about line 93.** Added the sourced incubation period and rare person-to-person spread: "usually 7–10 days, with a range of 2–30 days", from WHO Disease Outbreak News 2022-DON403 (fetched from who.int).
- **07_forecast_timesfm.md.**
  - The story said the Board "meets next week"; it is now "meets on Friday", matching chapters 09 and 10 (Fri 2 Oct).
  - Tala's leaky 3.27 is now compared explicitly with TimesFM's 3.86 over the same 94 forecasts.
  - The licence box now cites the TimesFM 2.5 model card and says Google "points to TimesFM in BigQuery for official support", instead of "offers commercial and production use through Google Cloud".
- **09_dashboard.md, step 3.** Added a sentence that Plotly's map downloads a world outline the first time it draws, so the simple notebook dashboard's map is empty offline. I observed this: `cdn.plot.ly/un/world_110m.json` is fetched even with `visible=False`.
- **10_wrap_up.md:79.** Removed "Health information is sensitive personal information under RA 10173" (unsourced). The checklist now says to follow the DPA as the office DPO applies it. The sitrep now reads "Median time **from consultation** to leptospirosis lab confirmation: 18 days".

### Notebooks (book_ph/en/chapters/notebooks)

- **01:** the title cell said "Monday morning"; it is now "Tuesday morning" (chapter 01 is Tue 28 Jul).
- **08, "Your turn" cell:** it printed the **mean of barangay rates** (riverside 19.6), which disagreed with chapter 04 and the README (19.7). It now sums cases and population per band and prints 19.7 / 5.6 / 2.6, with a comment explaining why.
- **All 9:** added `metadata.description`. MyST reads page frontmatter keys from notebook metadata. Before this, notebook pages had the generic site description. The diffs are minimal: one line per notebook, and formatting is kept.

### Other files

- **scripts/build_ph_dashboard.py, action a4_b (en, zh, fil):** "longer than the 2–30-day incubation period" became "longer than the longest leptospirosis incubation period (2–30 days, WHO)". The same sourced figure now appears in chapter 04, the epicurve game and the dashboard.
- **book_ph/{en,zh,fil}/myst.yml:** added `project.thumbnail` (`_static/og-image.png`, `og-image_zh.png`, `og-image_fil.png`).
- **book_ph/GAMES.md:** updated the descriptions of the games I changed. Also rewrote the rule "game numbers are illustrative, not the dataset's". It now says which games use dataset numbers and which use labelled practice numbers.
- **tests/test_notebook_smoke.py:78–79:** a pre-existing ruff PLC0206 error made the requested `ruff check … tests` fail. I fixed it in two lines with `.items()`. Note that the agent working on chapter 11 may also touch this file.

## 2. Checked and found fine

- **Notebooks.** All 9 ran top to bottom through nbclient in 2–6 s each, with no errors, no stderr, warnings or tracebacks, and no debug prints. Each has a title cell followed by the exact standard English Colab cell (the form used in 115 notebooks in the repo). All have "Your turn" sections.
- **Colab import in notebook 09.** It loads `scripts/build_ph_dashboard.py` with `spec_from_file_location("scripts/…")`. This works on Colab because the setup cell chdirs to `/content/python4epi`, and the script finds its data through `Path(__file__)`.
- **Prose numbers against notebook output.** Every number I compared matches: 618/18 columns; 388/230; 40 remarks; k-anonymity 99.0/80.9/17.5/1.3; 22 NaT and 56 → 2; 137 spellings → 23; 6 and 19 duplicates; 228+2; W30–34 35/108/68/15/2; peak day 27 Jul (19); median 14 days; 50.3/44.8/4.9%; 19.7/29.6/12.4/20.9; 189/96,064; 155 (67%) male and median age 32 / 18; OR 5.57 (3.41–9.10), conditional 5.54; fake "RR" 3.21/2.37 and OR 5.18; boots 0.35, doxycycline 0.43, rats 1.03; 21.5/69.1%; strata 5.56/2.88; MH 4.28 (2.53–7.27), p=0.24; threshold 17.45; wrong baseline 32.8, silent in W33 and W35; delay table; 7-1-7 26/31/27/15 and EV-040 7/1/10; MAE table, 3.27/3.95/3.86, 0.54/31.50, 29%, rainfall 3.47/5.27, W40 42 (24–63), W47 16 (6–44), sum 215, 75, 53, 46; Talaba 29 ÷ 6,688; 22 of 24; NCR 22,015 vs 1,004; 5 barangays suppressed; 4.9 MB and 96 kB; 55 small cells.
- **Story calendar** after the fixes: ch00 Mon 27 Jul → ch01 Tue 28 → ch02 Wed 29 → ch03 Thu 30 → ch04 Mon 3 Aug → ch05 Mon 10 / Fri 14 Aug → ch06 Wed 12 Aug → ch07, 08, 09 and 10 Wed 30 Sep → Board Fri 2 Oct. Names, places and voice are consistent with the bible.
- **Chapter links.** Forward and back links resolve (the link check passes). Each chapter has the full rhythm. "Tala got it wrong" appears in chapters 01–09, and every episode reproduces when the code is run.
- **Every game:** the randomized driver played each one to its end screen and restarted it, with a mouse at 1280 px and with taps on a 390 px touch viewport. All 22 widget instances showed feedback. Keyboard: Tab reaches each game, with a visible 3 px outline and a sun-coloured ring, and Enter activates. Quizzes parse.
- **Sourced facts I verified:**
  - From the research JSON: the IRR's Category I within 24 h and Category II weekly every Friday; ESR since 2010; the Central Luzon CBS pilot in 2024; JEE 2024 (7-1-7 ad hoc, 56%); WPRO's 2–3 week delay; SPEED within 48 h; FETP 128 and 49 graduates; FHSIS monthly/quarterly; JMC 2020-0002.
  - Fetched myself: TimesFM 3.0 weights are under the Non-Commercial License (Hugging Face), the 2.5 weights are Apache-2.0 (HF API), and the timesfm code is Apache-2.0 (PyPI).
- **AI guidance** is tool-neutral and never suggests pasting identifiable data.
- No placeholder text; alt text is present on every figure; the dashboard link from chapter 09 works.

## 3. Could not verify

- **RA 10173 and RA 11332 section text.** lawphil.net, privacy.gov.ph and the UP Law PDF are blocked from this session, so I softened the claims rather than state them. A reviewer with access could restore precise wording with a source, without section numbers.
- **The Philstar 2025 leptospirosis link** in chapter 04 is in the research file but philstar.com is blocked here.
- **Plotly maps on notebook pages 08 and 09 are blank** in the sandbox because cdn.plot.ly is blocked. They should render on the live site, but I could not confirm it.
- **The TimesFM GitHub page** returns 403, so the "TimesFM in BigQuery" wording comes from the Hugging Face model card.
- **Stat tiles in screenshots** are sometimes caught mid count-up. This is a timing artifact; the final text is the README number.
- **I did not review the zh and fil trees** beyond myst.yml. Their games pick up the synced strings.

## 4. Screenshots for the director

Folder: /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/ (all 22 URLs × 4 modes). Key files:

- Home: /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/home__d-light.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/home__d-dark.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/home__p-light.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/home__p-dark.png
- Chapter 04: /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/chapters_time-place-person__d-light.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/chapters_time-place-person__d-dark.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/chapters_time-place-person__p-light.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/chapters_time-place-person__p-dark.png
- Notebook 04: /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/chapters_notebooks_time-place-person__d-light.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/chapters_notebooks_time-place-person__d-dark.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/chapters_notebooks_time-place-person__p-light.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/chapters_notebooks_time-place-person__p-dark.png
- Dashboard: /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/dashboard__d-light.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/dashboard__d-dark.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/dashboard__p-light.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/dashboard__p-dark.png
- Changed games (phone, dark): /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/g/tw_alert_p_dark.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/g/curve1_p_dark.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/g/mappaint_p_dark.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/g/forecast2_p_dark.png, /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/g/publish_p_dark.png

The machine-readable per-page results (console errors, overflow, games, links) are in /tmp/claude-0/-home-user-python4epi/1b9e0100-ca71-5bd0-b68b-709b2b944b80/scratchpad/shots/final/report.json.
