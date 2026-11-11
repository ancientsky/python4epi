# Interactive games — authoring guide

The twelve teaching widgets of the production bible (§7) live in one script,
`book_ph/_static/ph-games.js`, styled by `book_ph/_static/ph-games.css`.
Vanilla JavaScript, no dependencies, no network requests. This page tells
chapter authors how to place each one.

## The contract

Write a MyST `{div}` whose classes name the widget. Its content is the
**fallback** that readers without JavaScript (and printouts) see:

```
:::{div}
:class: ph-game ph-game-<name>
Fallback text shown without JavaScript.
:::
```

- After React has hydrated the page (`window.epiWhenHydrated`), and again after
  every client-side navigation, the script finds blocks it has not mounted yet,
  hides the fallback (it is hidden, not removed, so React still owns it) and
  appends the game. Timers and listeners are released when the block leaves
  the page.
- The language comes from `window.EPI_SITE.lang` (`en` | `zh` | `fil`), else
  from `<html lang>`. **Every string is built in, in all three languages**, so
  the same snippet works in all three editions. Only the fallback text needs
  translating (and the questions of a list-based `quiz`).
- MyST keeps only `class`, `id`, `style` and `href`. Options are therefore
  extra classes (listed per widget below). Do not add `style=`.
- An unknown name, or a `quiz` with no questions, leaves the fallback visible.
- Everything works with keyboard (Tab, arrow keys, Enter/Space) and touch at
  390 px, announces feedback in a live region, honours
  `prefers-reduced-motion`, and follows the light/dark theme through the
  `--ph-*` tokens of `ph.css`.
- Every person, place and number inside the games is fictional and each game
  says so. Where a game shows Santa Luz itself it uses the **dataset's own
  numbers** (`threshold-watch`, `forecast-guess`, `map-paint`, the leptospirosis
  curve of `epicurve-builder`, the Ilog CFR of `bug-hunt` and the `ph-quiz-ch04`
  bank, the `publish-check` tiles). Any other numbers belong to a scenario
  labelled "practice" in the game (`two-by-two`, the other two curves); do not
  quote those in prose. Real-world facts in a game (e.g. the WHO incubation
  period of leptospirosis) carry their source in the chapter.
- Option for any widget: `ph-compact` (tighter spacing).

**Build integration:** `scripts/build_book.py` must inject
`_static/ph-games.css` and `_static/ph-games.js` into every PH page,
*after* `epi-site.js` and `ph-site.js` (see the header of `ph-site.js`).

Write a meaningful fallback: one or two sentences that make the same teaching
point, so the page still works when printed or read without JavaScript.

## The widgets

| Widget | Chapter | What it teaches |
|---|---|---|
| `prompt-pick` | 00 | Good prompts: name columns, give made-up rows, state the output, ask for a check |
| `bug-hunt` | 01 | Reading AI code: wrong CFR denominator, 0-based index, invented function, text vs number, missing `return` |
| `spot-pii` | 02 | Direct vs indirect identifiers, sensitive personal information (RA 10173), safe prompting |
| `date-fixer` | 03 | Mixed date formats, Filipino month names, Excel serials, ambiguous dates |
| `epicurve-builder` | 04 | One square per case, keep zero days; point source vs continuing source vs propagated |
| `two-by-two` | 05 | Filling a 2×2 table; RR (cohort) vs OR (case-control), 95% CI, OR ≠ RR when common |
| `threshold-watch` | 06 | Mean + 2 SD alert threshold, false alarms, 7-1-7 (detect ≤ 7 d, notify ≤ 1 d, respond ≤ 7 d) |
| `forecast-guess` | 07 | Forecast vs baselines, mean absolute error, 80% bands, a model cannot see a typhoon |
| `map-paint` | 08 | Rates vs counts, equal interval vs quantile, sequential vs rainbow colours |
| `lamok-patrol` | 08 / 09 | 4S: search and destroy *Aedes* breeding sites |
| `publish-check` | 09 | Small cells (suppress 1–4), no addresses or case-level data, honest axes, source line |
| `quiz` | any | Multiple-choice check written in the chapter itself |

### `prompt-pick` — chapter 00

Five rounds: Maya is about to message Tala; pick the better of two prompts.

```
:::{div}
:class: ph-game ph-game-prompt-pick
A good prompt names the columns, shows two or three made-up example rows,
says exactly what output you want, and asks for a way to check it.
:::
```

### `bug-hunt` — chapter 01

Five snippets of AI-written code; tap (or arrow to and press Enter on) the
line with the mistake. The fix is shown after each answer.

```
:::{div}
:class: ph-game ph-game-bug-hunt
AI code can look right and still be wrong: read it line by line, run it on a
case you can count by hand, and read the error message.
:::
```

### `spot-pii` — chapter 02

Round 1: tap the columns of Jun's raw export that must not leave the CESU.
Round 2: tap the pieces of Maya's draft AI prompt that identify a person.

```
:::{div}
:class: ph-game ph-game-spot-pii
Names, phone numbers, street addresses, PhilHealth numbers, exact birth dates
and free-text remarks never leave the office or go into an AI chat.
:::
```

### `date-fixer` — chapter 03

Tap a messy date (e.g. `24-Hul-2026`, `46226`), then tap the ISO date it
means, or "Ask Jun" when it is ambiguous (`08/07/2026`).

```
:::{div}
:class: ph-game ph-game-date-fixer
Parse each known date format explicitly, map Filipino month names, convert
Excel serial numbers and flag ambiguous dates instead of guessing.
:::
```

### `epicurve-builder` — chapter 04

Three scenarios: leptospirosis after the flood (a 1-in-4 sample of the Santa
Luz line list: a **continuing common source**, as in chapter 04), a practice
point source (diarrhoea after one shared lunch at an evacuation centre) and a
practice propagated dengue outbreak in a made-up village. Place each case on
its onset day/week, then name the curve's shape.

Option: `ph-curve-lepto`, `ph-curve-water` or `ph-curve-dengue` plays only
that scenario.

```
:::{div}
:class: ph-game ph-game-epicurve-builder ph-curve-lepto
A wave that stays high while the exposure lasts (wading through the flood and
the clean-up) suggests a continuing common source.
:::
```

### `two-by-two` — chapter 05

Round 1 (practice cohort, one Barangay Ilog clean-up crew of 24): wading
without boots, RR = 8.0. Round 2 (practice case-control pilot of 20 people,
not Maya's 360-person study): doxycycline prophylaxis, OR = 0.11, and the RR
row is marked "not valid". Live formulas and 95% CIs (log/Woolf method).
After six correct placements the learner may fill the rest automatically.

Option: `ph-2x2-cohort` or `ph-2x2-casecontrol` plays only that round.

```
:::{div}
:class: ph-game ph-game-two-by-two
Rows are exposure, columns are outcome. A cohort study compares risks (RR);
a case-control study compares odds of exposure (OR), never an RR.
:::
```

### `threshold-watch` — chapter 06

The real Santa Luz weekly dengue counts for 2026-W20…W39 appear one week at a
time against the chapter 06 alert threshold (mean + 2 SD of weeks w−1, w, w+1
in 2022–2025, 12 values; a "how is this computed?" panel shows the arithmetic).
The first crossing is W32 (33 vs 17.5), detected on Monday 10 August. Raise the alert at the right week, then decide
when to notify the PESU and which early-response plan fits — scored against
7-1-7.

```
:::{div}
:class: ph-game ph-game-threshold-watch
With weekly data, act the day the week's count arrives: detect within 7 days
of emergence, notify within 1 day, complete the early response within 7 days.
:::
```

### `forecast-guess` — chapter 07

Draw the next 8 weeks (drag, tap, or arrow keys on each dot), then reveal the
truth, the cached TimesFM 3.0 forecast of chapter 07 with its 80% band, and two
baselines, ranked by mean absolute error. Round 1 is an ordinary year (origin
2025-W31); round 2 is the take-off after Typhoon Amihan (history to 2026-W31),
where the model misses every week.

Option: `ph-forecast-normal` or `ph-forecast-typhoon`.

```
:::{div}
:class: ph-game ph-game-forecast-guess
Judge a forecast against simple baselines, report its error and uncertainty,
and say when something the model could not see has changed.
:::
```

### `map-paint` — chapter 08

A tile map of the 24 Santa Luz barangays with their dengue cases (chapter 08's
data; rates per 10,000). Switch counts ↔ rates, equal interval ↔ quantile,
sequential ↔ rainbow. Three missions: find the highest-*risk* barangay
(Talaba, though Ilog has the most cases), identify quantile classes, choose a
readable palette.

```
:::{div}
:class: ph-game ph-game-map-paint
Map rates, not counts; choose class breaks on purpose; use a light-to-dark
palette.
:::
```

### `lamok-patrol` — chapter 08 or 09

Two scenes (Aling Nena's yard, the school after the flood), 45 seconds each:
tap containers that can breed *Aedes*, leave the safe ones (covered drum,
upturned pail, pond with fish). Ends with the 4S. A "Relaxed mode" button turns
the timer off.

Option: `ph-lamok-relaxed` starts in relaxed mode.

```
:::{div}
:class: ph-game ph-game-lamok-patrol
4S: Search and destroy breeding sites, Secure self-protection, Seek early
consultation, Support fogging only in outbreak hotspots.
:::
```

### `publish-check` — chapter 09

Nine dashboard elements; approve or block each, as Doc Mon would.

```
:::{div}
:class: ph-game ph-game-publish-check
Before publishing: no names or exact addresses, suppress counts of 1–4, no
case-level downloads, axes that start at zero, and a source line.
:::
```

### `quiz` — any chapter

A multiple-choice card. Questions come from the fallback itself, which is an
ordinary markdown list:

- a paragraph before the list (optional) becomes the title;
- first-level items are the questions;
- nested items are the options; start the correct one with `✓ `;
- an option may end with ` — explanation` (space, em dash, space), shown
  when the option is chosen. Inline markup (`code`, **bold**) is kept.

If a question has no `✓` option, every answer counts as right (a poll).

```
:::{div}
:class: ph-game ph-game-quiz
**Quick check: time, place, person**

1. What is the denominator of an attack rate?
   - The number of cases — that is the numerator.
   - ✓ The population at risk — everyone who could have become a case.
   - The number of deaths — deaths over cases is the case fatality rate.
2. One sharp peak within one incubation period suggests…
   - ✓ A point source — everyone was exposed at about the same time.
   - Person-to-person spread — that gives successive, growing waves.
:::
```

Built-in banks: when the div contains **no list**, `ph-quiz-ch02` (privacy),
`ph-quiz-ch04` (rates and curves) or `ph-quiz-ch06` (thresholds, 7-1-7)
supply the questions in the page's language:

```
:::{div}
:class: ph-game ph-game-quiz ph-quiz-ch06
Check yourself: what do the numbers in 7-1-7 stand for?
:::
```

## Page hooks (not games)

- **`ph-stat`** — after hydration, each card title (the big number) of a
  `ph-stat` grid counts up from zero when it scrolls into view; without cards,
  the first number in the element's text does. The final text is always the
  original. Off under reduced motion.
- **`ph-reveal`** — `ph.css` fades these in with scroll-driven CSS; where the
  browser lacks that, `ph-games.js` does the same with an
  IntersectionObserver. Blocks already on screen are never hidden. Off under
  reduced motion.

## API for debugging

`window.PHGames.scan()` mounts any new blocks now;
`PHGames.widgets()` lists the names; `PHGames.instances()` counts live games.
