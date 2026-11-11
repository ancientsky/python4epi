# Bantay Python — style guide for authors

This is the visual language of the Philippines edition: what each class looks like,
how to write it in MyST, which illustration goes where, and the design tokens the
interactive games share. The production bible (`PRODUCTION.md` §7) sets the
direction; this file is how to apply it.

- Stylesheet: `book_ph/_static/ph.css` (loaded by every `book_ph/*/myst.yml` via
  `site.options.style`; it replaces the main book's `site.css`).
- Logos: `book_ph/_static/logo.svg`, `logo-dark.svg`, `favicon.svg`.
- Social cards: `book_ph/_static/og-image.png` (EN), `og-image_zh.png`,
  `og-image_fil.png` (1200 × 630; sources `images/og_image_{en,zh,fil}.svg`).
- Illustrations: `book_ph/images/*.svg`, reached from chapters as `images/…`
  (`chapters/images` is a symlink) and from `intro.md` as `chapters/images/…`.

## Ground rules

1. **MyST, not HTML.** MyST keeps only `class`, `id`, `style` and `href` from raw
   HTML. Every component below is a `{div}` or an admonition with `:class:`.
   No `{raw}`, no `data-*`, no `aria-*`, no `<span class>`.
2. **Nesting fences: the outer fence has *more* colons.** A `:::` block inside a
   `:::` block silently ends the outer one early.
   ```
   :::::{div}          ← 5 colons, outer
   :class: ph-cast
   ::::{grid} 2 3 5 5  ← 4 colons
   :::{card} Maya      ← 3 colons, innermost
   :::
   ::::
   :::::
   ```
3. **No emoji in box titles.** Each box already has its own icon (star, check,
   stop sign…); `🤖 Ask Tala` would show two icons.
4. **Decoration never sits behind running text.** Textures (banig, capiz,
   bunting) live in borders, header strips and empty corners only. Don't put
   paragraphs on a patterned background.
5. **Keep words out of art.** Most illustrations are wordless; the five that
   need words come in `_en`, `_zh`, `_fil` versions. Use the one that matches
   the edition. Captions carry the names and the teaching.
6. **Alt text is required.** Describe what matters for the lesson, not the
   colours: `:alt: Six levels of reporting, from BHW up to the DOH Epidemiology Bureau`.
7. **Fictional is labelled.** Santa Luz, Kalinaw and the cast are invented; the
   map says so itself; say it in prose too (bible §8).

## Page anatomy (bible §4 rhythm)

The page title is drawn automatically as a **jeepney signboard** (chrome frame,
flag-blue plate, sun-yellow painted letters). `##` headings get a small
eight-rayed sun and a flag stripe. You don't need to do anything for either.

```
# Privacy first: every row is a neighbour

:::{div}                       ← 1. story beat
:class: ph-story
…
:::

## …concept + illustration…    ← 2.

:::{admonition} Ask Tala       ← 3.
:class: ph-ask-tala
:::

:::{admonition} Tala says
:class: ph-tala-says
:::

:::{admonition} Check it       ← 4.
:class: ph-check
:::

:::{div}                       ← 5. game (owned by ph-games.js)
:class: ph-game ph-game-spot-pii
:::

:::{admonition} Privacy stop   ← 6.
:class: ph-privacy
:::

:::{admonition} Baon           ← 7.
:class: ph-baon
:::
```

## Components

Every box class works in **two forms**:

- **Admonition form** (preferred when there is a title): a coloured header strip
  with the icon, the title in white, a tinted body.
  `:::{admonition} Title` + `:class: ph-…`
- **Div form** (no title bar): the icon sits in the top-left corner. If the first
  paragraph is only bold text (`**Check it**`), it is coloured like a title.

### `ph-hero`: home page hero

Flag-blue sky with bunting along the top, a slowly turning eight-rayed sun, three
stars, and a jeepney driving along the road at the bottom. Only on `intro.md`.
The first line, if it is only bold or only italic, becomes a sun-yellow kicker
pill. A `##` heading becomes the big painted title. A `{button}` becomes a yellow
button.

```
:::{div}
:class: ph-hero
**Philippines Edition**

## Bantay Python

Learn outbreak analytics from zero — with an AI co-pilot you learn to **check**.

{button}`Sakay na! Start the ride → <chapters/00_start_here.md>`
:::
```

### `ph-story`: story beat (komiks panel)

An ink-bordered panel with a flag-blue offset shadow and a speech-bubble badge.

- The first line in *italics only* becomes the scene slug (date · place).
- `**Name:**` at the start of a paragraph becomes a coloured name chip
  (flag blue by default).
- A `>` quote at the end becomes the question the chapter answers (red, dashed,
  with a "?").

```
:::{div}
:class: ph-story
*Monday 27 July · CESU office, Santa Luz*

**Aling Nena:** Ate Maya, three more men from Purok 2 — fever, red eyes, calf pain.

**Maya:** That makes eleven. Doc Mon wants the line list by Friday.

**Doc Mon:** Ask Tala — but check everything it gives you.

> How do we share the line list without sharing our neighbours?
:::
```

**Per-speaker chip colours** (optional): wrap a line in a nested div with
`ph-say-maya` (teal), `ph-say-mon` (blue), `ph-say-tala` (indigo),
`ph-say-nena` (green) or `ph-say-jun` (scarlet). The outer fence needs more colons:

```
::::{div}
:class: ph-story
*Same afternoon*

:::{div}
:class: ph-say-maya
**Maya:** Tala, can you count cases by barangay?
:::

:::{div}
:class: ph-say-tala
**Tala:** Of course! Here's a pandas one-liner.
:::
::::
```

### `ph-ask-tala`: the prompt Maya types

Flag-blue, styled like a message composer, with a blinking caret after the last
paragraph. Name the columns, give 2–3 **made-up** rows, and state the output you
want. Never use real data.

```
:::{admonition} Ask Tala
:class: ph-ask-tala
I have a pandas DataFrame `df` with columns `barangay`, `onset_date`, `disease`.
Here are three made-up rows: … Count cases per barangay, most to fewest.
:::
```

### `ph-tala-says`: the AI's answer

Indigo speech bubble with a pearly capiz-window header and Tala's star face. It
usually holds the code that came back.

````
:::{admonition} Tala says
:class: ph-tala-says
```python
counts = df["barangay"].value_counts()
```
:::
````

### `ph-check`: verify box

Banana-leaf green with a check stamp. Use a numbered list of concrete checks:
count a tiny case by hand, check the denominator, read the error.

```
:::{admonition} Check it
:class: ph-check
1. Run it on five rows you can count by hand.
2. Does the total equal `len(df)`?
:::
```

### `ph-oops`: "Tala got it wrong"

Scarlet, dashed border, faint warning stripes, a warning sign that wobbles on
hover. One per AI-mistake episode (at least three chapters have one).

```
:::{admonition} Tala got it wrong
:class: ph-oops
Tala divided by the number of **cases** instead of the barangay **population**.
:::
```

### `ph-privacy`: privacy stop

Deep blue with caution tape and a red stop-sign padlock. Use it for RA 10173 /
RA 11332 points, small-cell suppression, and the rule against pasting
identifiable data into AI chats.

```
:::{admonition} Privacy stop
:class: ph-privacy
Never paste names, phone numbers or exact addresses into an AI chat.
:::
```

### `ph-baon`: take-aways

Wrapped in a banana leaf. Bullets become little suns. End with the notebook link.

```
:::{admonition} Baon
:class: ph-baon
- Ask with column names and fake rows — never real data.
- Run it, read the error, check a case you can count by hand.
- Every row is a neighbour: de-identify before you share.

Open the notebook: [](notebooks/02_privacy_first.ipynb)
:::
```

### `ph-cast`: character cards

A `{grid}` of `{card}`s inside a `ph-cast` div. Each card has a portrait, an
*italic role line* and one sentence. The portrait is moved above the name
automatically, and a banig-weave band runs across the top. **Card order sets the
colours**: Maya (teal), Doc Mon (blue), Tala (indigo), Aling Nena (mango),
Jun (scarlet). Keep that order.

```
:::::{div}
:class: ph-cast
::::{grid} 2 3 5 5

:::{card} Maya
![Maya, the surveillance officer](chapters/images/cast_maya.svg)

*Surveillance officer*

Four months into her first DSO post. Has never coded.
:::

:::{card} Doc Mon
![Doc Mon, the provincial epidemiologist](chapters/images/cast_doc_mon.svg)

*Epidemiologist*

"Denominator? Who can see this file?"
:::

…Tala, Aling Nena, Jun…
::::
:::::
```

### `ph-stat`: big-number tiles

A grid of cards inside a `ph-stat` div. The card **title is the number**,
painted in signboard lettering and sized to fit the tile. The body is the label.
Colours cycle blue, red, sun, green, teal, mango. Use the dataset README's
headline numbers only.

```
:::::{div}
:class: ph-stat
::::{grid} 2 2 4 4

:::{card} 186,000
people in 24 barangays
:::

:::{card} 650
febrile notifications
:::
::::
:::::
```

### `ph-route`: act / route signboard

A chrome-framed jeepney route board. The first bold line is the route name,
painted in the act colour with a sun-yellow shadow. A list holds the stops,
which can be links. Add `ph-act-1` (blue) … `ph-act-4` (mango) for the act colour.
It stays a cream signboard in dark mode too.

```
:::{div}
:class: ph-route ph-act-1
**I · May ulat!**

- [Start here](chapters/00_start_here.md)
- [Kumusta, Python?](chapters/01_python_with_ai.md)
- [Privacy first](chapters/02_privacy_first.md)
:::
```

### `ph-banderitas`: fiesta bunting divider

Two strings of swaying pennants. Leave the div empty (any content is hidden).
Use at most two per page, between major sections.

```
:::{div}
:class: ph-banderitas
:::
```

### Utilities

| Class | Effect |
|---|---|
| `ph-reveal` | Fades a block in as it scrolls into view (pure CSS; no-op where unsupported or with reduced motion). The boxes above already *lift* gently into view without fading. |
| `ph-wide` | On phones (≤ 640 px), keeps a wide diagram at 600 px and lets it scroll sideways. Wrap the figure: `:::{div}` / `:class: ph-wide` / figure / `:::`. |
| `ph-center` | Centres text and inline content. |

### Restyled built-ins (nothing to do)

- **Tables**: flag-blue header row with a sun underline, zebra rows, rounded frame.
  DataFrame index cells are soft blue.
- **Code**: night-blue blocks with a flag strip on top in both themes; notebook
  inputs get a mango rail. Inline code is a sun-tinted pill.
- **Buttons** (`` {button}`Text <file.md>` ``): scarlet "sticker" pills that press down.
- **Cards and grids**: rounded, with a colour band on top cycling through the palette.
- **`note` / `tip` / `warning` / `danger`**: the palette's blue / teal / mango / red.
- **Blockquotes**: sun-yellow quote bar with a large mango quotation mark.
- **Prev/next links, sidebar**: the active page has a scarlet (dark mode: sun) rail.

## Header and language switch (contract with `scripts/build_book.py`)

`_site/navbar_end.md` may use either markup:

```
<div class="ph-switch">
<a class="ph-lang ph-lang-en" href="…/ph/">EN</a>
<a class="ph-lang ph-lang-zh" href="…/ph/zh/">中文</a>
<a class="ph-lang ph-lang-fil" href="…/ph/fil/">Filipino</a>
<a class="ph-book-link" href="…/en/">Full book</a>
</div>
```

or plain `a.epi-lang-switch` links. The language links render as one segmented
pill. The current language is highlighted **from `<html lang>`** (`en`,
`zh-Hant`, `fil`, written by the post-build step). A script may also mark it with
`aria-current` or the class `is-current` / `epi-lang-current`. On phones the
"Full book" link hides, the logo shrinks to the shield, and below 400 px
"Filipino" shows as "FIL". `a.epi-colab-link` (Open in Colab) is styled too.

## Illustrations

All are original, hand-built flat SVGs. Each one carries its own rounded
background panel, so it reads the same on light and dark pages. They have
`<title>`/`<desc>`, a viewBox, gentle CSS animation, and a
`prefers-reduced-motion` switch-off.

| File | What it shows | Use in |
|---|---|---|
| `cast_maya.svg` | Maya, DSO, clipboard, teal badge | intro cast, any story |
| `cast_doc_mon.svg` | Doc Mon, glasses, barong-style shirt, blue badge | intro cast |
| `cast_tala.svg` | Tala, a smiling star with a code tag (twinkles) | intro cast, 00 |
| `cast_aling_nena.svg` | Aling Nena, BHW vest, phone, mango badge | intro cast, 02 |
| `cast_jun.svg` | Jun, records clerk, headphones, USB stick | intro cast, 03 |
| `cast_all.svg` | the five badges in a row | intro, 10 |
| `scene_flood_riverside.svg` | Typhoon Amihan flood: stilt houses, men wading with debris, bangka, rain | intro / 00 story, 04 (exposure) |
| `scene_cesu_office.svg` | Maya at her desk: laptop with rising epi curve + Tala, forms, jalousie window, map, electric fan | 00, 01, 03 |
| `scene_health_station.svg` | barangay health station, flag, waiting bench under a mango tree, Aling Nena at the door, covered water drum | 02, 04, 08 |
| `ask_run_check_{en,zh,fil}.svg` | the Ask → Run → Check loop with Tala in the middle | 00 (method), 01, 10 |
| `reporting_ladder_{en,zh,fil}.svg` | BHW → RHU/health centre → CESU/MESU → PESU → RESU → DOH EB, with reports climbing and feedback flowing down | 06 (delay), 10 (system map) |
| `timeline_717_{en,zh,fil}.svg` | 7-1-7: emergence → detection ≤ 7 d → notification ≤ 1 d → early response ≤ 7 d | 06 |
| `mosquito_4s_{en,zh,fil}.svg` | 4S against dengue around a buzzing *Aedes* | 06, 08 (`lamok-patrol`) |
| `route_map_{en,zh,fil}.svg` | jeepney route through the 12 stops (Mabuhay + 00–10) in four act colours | intro, 10 |
| `santa_luz_map_{en,zh,fil}.svg` | fictional Santa Luz City: upland / riverside / coastal bands, Marilag River, CESU, health stations, Brgy. Ilog | intro, 04, 08 |
| `og_image_{en,zh,fil}.svg` | social card sources (PNG in `_static/`) | `project.thumbnail` |

The diagrams carry text, so their *visible* text is translated, but proper nouns
(Santa Luz, Kalinaw, Marilag, Ilog) and the act names (May ulat!, Bilangin natin,
Bantay, Ipakita) stay as they are in all three. zh uses Taiwan terms (通報, 監測,
回饋). The Filipino strings need a native-speaker check, like the rest of the
Filipino edition.

Figure snippet:

````
```{figure} images/reporting_ladder_en.svg
:alt: Six levels of reporting, from the barangay health worker up to the DOH Epidemiology Bureau, with feedback flowing back down.
:width: 100%
Reports climb the ladder; feedback should come back down.
```
````

Diagrams are 760–900 units wide with 16–24 unit labels. On a phone they shrink to
about 45 %. If a diagram must be read closely on a phone, wrap it in `ph-wide`.

## Design tokens (`--ph-*`, defined on `:root`, dark values on `html.dark`)

The games (`ph-games.css`) should use these instead of hard-coded colours, so a
game sits naturally on the page in both themes.

**Brand fills** (same in both themes; put `--ph-on-fill` text on them, which is
white and ≥ 5:1):

| Token | Value | Use |
|---|---|---|
| `--ph-flag-blue` | `#0038a8` | primary fill, header rows, current-state |
| `--ph-flag-red` | `#ce1126` | primary action buttons, alerts |
| `--ph-sun` / `--ph-sun-deep` | `#fcd116` / `#e0a800` | highlights, stars, focus in dark; **text on it: `--ph-on-sun`** (ink); never as text colour on light |
| `--ph-mango` | `#ff9f1c` | accents, rails; text on it: `--ph-on-sun` |
| `--ph-leaf-fill` | `#2f7d32` | success / correct |
| `--ph-teal-fill` | `#00737d` | tips, Maya |
| `--ph-indigo-fill` | `#4b3fb0` | Tala |
| `--ph-mango-fill` | `#b45309` | act IV, white-text fills |
| `--ph-chrome-1/2/3` | `#f4f6f8` `#aeb7c0` `#6e7882` | jeepney chrome frames |
| `--ph-ink`, `--ph-night`, `--ph-sampaguita` | `#1c1b29`, `#13183a`, `#fffcf4` | outlines, night sky, cream |

**Theme-dependent** (light → dark):

| Token | Light | Dark |
|---|---|---|
| `--ph-bg` / `--ph-bg-alt` | `#fffbf2` / `#fff4de` | `#11152a` / `#161b33` |
| `--ph-surface` / `--ph-surface-alt` | `#ffffff` / `#fff8ea` | `#1b2140` / `#222949` |
| `--ph-text` / `--ph-text-muted` | `#1c1b29` / `#4d4a5e` | `#f4efe2` / `#c8c2b2` |
| `--ph-border` / `--ph-border-strong` | `#eadcc0` / `#cdb98f` | `#313a62` / `#4a5384` |
| text-safe accents `--ph-blue` `--ph-red` `--ph-leaf` `--ph-mango-text` `--ph-teal` `--ph-indigo` | `#0038a8` `#b30e22` `#276b2a` `#9a4600` `#006d77` `#4b3fb0` | `#9bbaff` `#ff8f9b` `#8ed88a` `#ffb861` `#5fd8cc` `#bcb3ff` |
| soft tints `--ph-soft-{blue,red,sun,leaf,mango,teal,indigo}` | pale pastels | deep tinted navies |
| `--ph-code-bg` / `--ph-code-text` | `#13183a` / `#f3efe3` | `#0b0f26` / same |
| `--ph-focus` | flag blue | sun yellow |
| `--ph-shadow`, `--ph-shadow-pop`, `--ph-plate-shadow` | soft / lifted / 5 px "signboard" drop | darker |

Accent text on `--ph-bg`, `--ph-surface` and the matching soft tint is AA
(≥ 5.3:1 light, ≥ 7:1 dark). The ratios were checked for every pair above.

**Shape, type and motion:** `--ph-radius` 16px, `--ph-radius-sm` 10px,
`--ph-ease` (a small overshoot), `--ph-font-display` (Bungee → Arial Black →
CJK bold fallbacks; only for short signboard text), `--ph-font-sans`,
`--ph-font-mono`.

**Motifs as images:** `--ph-img-sun`, `--ph-img-sun-small`, `--ph-img-jeepney`,
`--ph-img-stars`, `--ph-img-bunting`, `--ph-img-bunting-alt`, `--ph-img-banig`,
`--ph-img-capiz`, `--ph-img-tala`. Use them as `background: var(--ph-img-tala) center / contain no-repeat;`.
Bunting, capiz and small-sun switch to dark-mode versions automatically.

Example for a game:

```css
.ph-game { background: var(--ph-surface); color: var(--ph-text);
  border: 2px solid var(--ph-border); border-radius: var(--ph-radius); }
.ph-game button.primary { background: var(--ph-flag-red); color: var(--ph-on-fill); }
.ph-game .is-correct { background: var(--ph-soft-leaf); color: var(--ph-leaf); }
```

## Motion

- Hero: the sun turns once in 140 s; the jeepney drives across in 16 s. Bunting
  sways. The Ask Tala caret blinks.
- Boxes, story panels, route boards and cards lift gently into view with
  scroll-driven CSS, without JavaScript. They never fade, so screenshots,
  printing and link previews still show everything. `ph-reveal` opts a block
  into a real fade-in.
- Everything above, plus the SVGs' own animation, stops under
  `prefers-reduced-motion: reduce`. Hover lifts are disabled there too.

## Dos and don'ts

- **Do** put one hero on the home page only; use `ph-route` boards for act
  overviews and `ph-banderitas` sparingly.
- **Do** keep box titles short ("Ask Tala", "Check it", "Privacy stop",
  "Baon"). Translate them per edition (zh: 問問 Tala, 檢查一下, 隱私停看聽,
  帶走重點; fil: Tanungin si Tala, Suriin, Privacy muna, Baon).
- **Do** write `**Name:**` exactly so (bold, colon inside) for story speakers.
- **Don't** add `style=` colours. Use the classes and tokens, so dark mode keeps working.
- **Don't** put code or tables inside `ph-route`, `ph-stat` or `ph-cast`.
- **Don't** link solution files or put real data in any box. `ph-ask-tala`
  examples are always made-up rows.
- **Don't** nest boxes in boxes (a code block inside one is fine).
- **Don't** reuse an illustration's language variant across editions. Pick
  `_en`, `_zh` or `_fil`.
