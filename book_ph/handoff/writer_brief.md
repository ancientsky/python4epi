# Brief for English chapter authors — Philippines edition ("Bantay Python")

Repo: /home/user/python4epi. You are writing part of the ENGLISH (source-of-truth) edition under
`book_ph/en/`. Placeholders exist for every page and notebook; you replace the ones assigned to you.

## Read first, completely
1. `/home/user/python4epi/book_ph/PRODUCTION.md` — the bible: audience, story, cast, chapter rhythm, quality bar.
2. `/home/user/python4epi/CLAUDE.md` — repo rules, MyST syntax limits, the "Philippines Edition" section.
3. `/home/user/python4epi/data/synthetic/ph/README.md` — authoritative dataset schema and the headline
   numbers you must quote. Never guess a column name; never quote a number the code does not print.
4. `/home/user/python4epi/book_ph/STYLEGUIDE.md` — every page component (`ph-story`, `ph-ask-tala`,
   `ph-tala-says`, `ph-check`, `ph-oops`, `ph-privacy`, `ph-baon`, `ph-stat`, `ph-cast`, …) with
   copy-paste MyST, and the list of illustrations (use them; reference as `images/<file>.svg`,
   English variants end in `_en.svg`).
5. `/home/user/python4epi/book_ph/GAMES.md` — the interactive widgets and their exact authoring syntax.
   Place the widgets the bible assigns to your chapters, plus a `quiz` near the end of each chapter
   (write the questions yourself in the documented list syntax).
6. One chapter + notebook of the main English book for house style, e.g. `book_en/chapters/03_stats.md`
   and `book_en/chapters/notebooks/03_stats_basics.ipynb` (note the standard Colab setup cell — keep it
   exactly as in the placeholder notebook, right after the title cell).
7. `book_ph/research/ph_surveillance_research_2026-11-09.json` when you need real Philippine facts
   (surveillance systems `surv.systems`, outbreaks `surv.obs`, timeline `surv.tl`, gaps, `info`,
   `regions`, `sources`). Real-world claims need a source link taken from that file (resolve ids through
   `alias`/`sources`) — or leave the claim out. Respect its estimate/inference/unverified flags. For laws
   (RA 10173 Data Privacy Act of 2012, RA 11332) state only what you are sure of or can read in the
   research file / official text; no legal advice, no invented section numbers.

## What a chapter is
- The page (`book_ph/en/chapters/NN_*.md`): frontmatter `title` and a one-sentence `description`; then the
  rhythm in bible §4 (story beat → concept with illustration → 🤖 Ask Tala prompt + the code that comes
  back → ✅ Check it → mini-game → 🔒 privacy stop where relevant → Baon take-aways → link to the
  notebook by file path, e.g. `[Open the notebook](notebooks/03_clean_linelist.ipynb)`). 900–1,600 words
  of prose; short paragraphs; plain English for second-language readers; define every epi term once.
  The page teaches; the notebook is where the learner runs things. Code shown on the page must be the
  same code as in the notebook.
- The notebook (`book_ph/en/chapters/notebooks/NN_*.ipynb`): 12–25 cells, beginner-paced, every code
  cell preceded by a markdown cell that says what we are about to ask and why. It must run top-to-bottom
  from the repo root in well under a minute with the project environment
  (`cd /home/user/python4epi && uv run jupyter nbconvert --to notebook --execute --stdout <nb> > /dev/null`),
  read data via repo-root-relative paths (`data/synthetic/ph/...`), use only packages already in
  pyproject.toml, produce good-looking charts (matplotlib/plotly; the book build applies fonts and
  style), include 2–3 "Your turn" exercises with hidden-free hints, and show the Ask → Run → Check loop
  for real: a markdown cell quoting the prompt, the code cell, then a cell that *checks* the result
  (assert on a hand-countable case, compare with a second method, test an edge case).
  "Tala got it wrong" episodes show the flawed code in a markdown code block or a cell that demonstrates
  the wrong answer safely, then the corrected cell. Write notebooks as valid nbformat 4 JSON (generate
  them with a small Python script using `nbformat`, stable cell ids, no stored outputs).
- AI guidance must be tool-neutral: "your AI assistant" / Tala — do not name commercial AI products or
  models, prices or quotas (they date quickly). Prompts never contain real or realistic identifiable
  data: they describe columns and give two or three obviously made-up rows.
- Fiction must never pass as fact: Santa Luz, Kalinaw, Typhoon Amihan, all people and all numbers from
  `data/synthetic/ph/` are invented; real systems, laws and statistics are real and sourced.
- Tone: warm, encouraging, lightly funny; light Taglish in dialogue is welcome if the meaning is clear.
  Respectful about disaster, illness and death.

## Rules of the shared workspace
- Other authors are writing other chapters at the same time. Touch only your assigned files (plus new
  image files under `book_ph/images/` if you add an illustration — original, well-formed SVG with
  `<title>`, `<desc>`, viewBox, readable on light and dark). Do not edit shared CSS/JS, `myst.yml`,
  the datasets, or other chapters. If you need something from a shared file, say so in your report.
- Do NOT run git commands that change state (no commit/stash/checkout/reset), and do NOT run
  `scripts/build_book.py` (concurrent builds of the same project collide; the director builds).
  Check MyST syntax carefully by reading STYLEGUIDE/GAMES snippets and existing chapters instead.
- Keep cross-chapter continuity: read the placeholder titles of the other chapters, refer forward and
  back by file path links (`[](04_time_place_person.md)`), keep names, dates and numbers per the bible
  and the data README.
- When finished: execute your notebooks (command above) and fix until clean; re-read your pages once as
  a tired nurse on a phone would. Then reply with a summary under 150 words: files written, the numbers
  you quote and where they come from, anything you could not verify, anything you need changed in shared
  files (CSS, games, data).
