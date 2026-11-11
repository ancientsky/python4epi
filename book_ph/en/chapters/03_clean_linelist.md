---
title: "03 From messy line list to clean data"
description: "Maya turns Jun's messy post-typhoon export into a clean, de-identified line list with pandas and AI help, checking every step, including a date mistake Tala made."
---

:::{div}
:class: ph-story
*Tuesday 28 July · CESU office, Santa Luz City Health Office*

**Jun:** Ate Maya, here's the export. All the fever notifications since the typhoon.

**Maya:** Salamat, Jun! Why does Ilog appear six different ways?

**Jun:** Six? Ay, many hands typed it. Hospital, health stations, us. Some write `Brgy. Ilog`, some `ILOG`. Dates too… each encoder has a style.

**Doc Mon:** Before anyone counts anything: names off the table. Then clean. Then prove it is clean.

> How do we turn Jun's export into a line list we can trust — and share?
:::

```{figure} images/scene_cesu_office.svg
:alt: Maya at her desk in the CESU office with a laptop showing a rising epidemic curve, paper forms and a map of the city on the wall.
:width: 100%
Maya's desk, the week after Typhoon Amihan. Santa Luz, its people and its data are fictional.
```

## What "clean" means

A **line list** is a table with one row per case and one column per piece of information:
onset date, age, sex, barangay and so on. It is *clean* when:

- every row is **one real case** (no duplicates);
- every column uses **one style** (`2026-07-24`, never four ways of writing the same day);
- every value is **possible** (no one is 150 years old or falls ill after consulting);
- **no one can be identified** from it.

Jun's file, `santa_luz_linelist_raw.csv`, breaks all four rules on purpose. The copy
you work with is his export at the 30 September data freeze (637 rows), so it already
holds the dengue cases that come later in the story. It is synthetic training data: the names, phone numbers and addresses in it are invented, but
they *look* real so that you can practise protecting them.

The tool is **pandas**, Python's spreadsheet library. A pandas table is called a
**DataFrame**; one column of it is a **Series**. We read every column as text first,
so that pandas changes nothing behind our backs:

```python
raw = pd.read_csv(RAW_PATH, skiprows=1, dtype=str, keep_default_na=False)
```

## Step one is privacy

Chapter 02 set the rule: identifiers leave the table *before* analysis. But we still need
the name for one job, which is finding the same patient notified twice. So Maya turns
each name into a **pseudonymous key**: a short code made from the tidied name plus a
secret word (a *salt*). The same name always gives the same code, but no one can read
the name back from it.

:::{admonition} Tala says
:class: ph-tala-says
```python
def name_key(name: str) -> str:
    """Turn a patient name into a short code that cannot be read back."""
    tidy = " ".join(name.replace(".", " ").upper().split())  # "Juan P. Santos" -> "JUAN P SANTOS"
    return hashlib.sha256((SECRET_SALT + tidy).encode()).hexdigest()[:12]


df = raw.copy()
df.insert(0, "name_key", df["Patient Name"].map(name_key))
df = df.drop(columns=["Patient Name", "Contact No.", "Address", "Reporting Unit", "Remarks"])
```
:::

:::{admonition} Privacy stop
:class: ph-privacy
- Drop the **remarks** too: free text like *"anak ni Dennis (kapitbahay)"* names other people.
- A key made with a salt is still linked to a person while the salt exists. Keep the
  real salt off shared drives and out of notebooks you share, and treat the keyed file
  as confidential.
- When you ask Tala for help, describe the columns and invent two or three rows. Never
  paste Jun's real rows into an AI chat.
:::

## Dates: the mistake that makes no error

Jun's dates come as `07/24/2026`, `7/24/2026`, `2026-07-24`, `24-Jul-26`,
`July 24, 2026` and plain numbers like `46227`, which is how Excel stores a date
(a count of days since 30 December 1899).

:::{admonition} Ask Tala
:class: ph-ask-tala
My column `date_of_onset` has dates in mixed formats. Convert it to datetime.
:::

:::{admonition} Tala says
:class: ph-tala-says
Use `format="mixed"` with `dayfirst=True`, because most of the world writes the day first:
```python
naive_onset = pd.to_datetime(df["date_of_onset"], format="mixed", dayfirst=True, errors="coerce")
```
:::

It runs, and nothing turns red. Maya asks two nurse's questions: how many dates
**failed**, and does anyone **fall ill after consulting**?

:::{admonition} Tala got it wrong
:class: ph-oops
- **22 onset dates became `NaT`** ("not a time"). Those were the Excel serial numbers,
  which pandas does not see as dates.
- **56 patients now "fell ill after they consulted".** With `dayfirst=True`, `8/1/2026`
  (1 August) became 8 January. Dates like `7/29/2026` were still right, because there
  is no month 29, so the mistake hid among good rows.

In the Philippines the slash style is month/day/year, and Jun confirmed that every
slash date in his export follows it. The fix: **one explicit rule per format**, and no
guessing.
:::

:::{admonition} Ask Tala
:class: ph-ask-tala
Write a function `parse_dates(s)` for a pandas Series of text dates. Formats: `M/D/YYYY`
(month first, leading zeros optional), `YYYY-MM-DD`, `DD-Mon-YY` (years are 20YY),
`Month D YYYY` with or without a comma, and 5-digit Excel serial numbers (days since
1899-12-30). Blank means missing. Parse each format explicitly; do not let pandas guess.
:::

:::{admonition} Tala says
:class: ph-tala-says
```python
def parse_dates(s: pd.Series) -> pd.Series:
    """Parse Jun's date styles one explicit format at a time."""
    s = s.str.strip()
    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    serial = s.str.fullmatch(r"\d{5}")  # Excel counts days from 30 Dec 1899
    out[serial] = pd.to_datetime(s[serial].astype(int), unit="D", origin="1899-12-30")
    for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%d-%b-%y", "%B %d %Y"]:
        attempt = pd.to_datetime(s.str.replace(",", "", regex=False), format=fmt, errors="coerce")
        out = out.fillna(attempt)  # only fills dates that are still missing
    return out
```
:::

:::{admonition} Check it
:class: ph-check
1. **A case you can check by eye:** the same day written seven ways must give
   `2026-07-24` seven times, and a blank must stay missing.
2. **Count what failed:** a text date that is not blank must never become `NaT`. The
   notebook stops with an `assert` if one does.
3. **Ask the epidemiology question again:** onset after consultation drops from 56 rows
   to **2**. Those two are real typing errors in Jun's file, and we deal with them below.
:::

Try it yourself. Some dates in the game below are ambiguous on purpose; when a date
could mean two things, the right answer is to ask, not to guess.

:::{div}
:class: ph-game ph-game-date-fixer
Parse each known date format explicitly, map Filipino month names, convert Excel serial
numbers and flag ambiguous dates instead of guessing.
:::

## Places, codes and ages

The other columns follow the same pattern: write the rule down, apply it, then check
that nothing fell through.

| Column | Raw values | Rule | Clean |
|---|---|---|---|
| Barangay | `Brgy. Ilog`, `ILOG`, `Bgy Ilog `, `Sto. Nino` | remove accents and prefixes, lower-case, `sto` → `santo`, fix 3 known typos, look up the official list | `Ilog`, `Santo Niño` + `barangay_id`, `band` |
| Sex | `male`, `lalaki`, `F`, `babae` | lookup table | `M` / `F` |
| Yes/no | `Y`, `oo`, `hindi`, `N/A` | lookup table | `1` / `0` / missing |
| Outcome | `buhay`, `Namatay`, `Expired` | lookup table | `alive` / `died` |
| Age | `34 y/o`, `8 mos`, `150` | first number; months ÷ 12; above 110 → missing | `34`, `0`, missing |

Jun's 137 barangay spellings become 23 barangays. The 24th, upland Bukid, had no
notifications at all, and chapter 04 will need to remember that. The age rule fits in
a few lines:

```python
def parse_age(s: pd.Series) -> pd.Series:
    """Completed years from text like '34', '34 y/o', '34yo', '8 mos', '8 months'."""
    text = s.str.strip().str.lower()
    number = text.str.extract(r"^(\d+)")[0].astype("Int64")
    years = number.where(~text.str.contains("mo"), number // 12)  # months -> years
    return years.where(years <= 110).astype("Int64")             # 150 -> missing
```

## Duplicates, impossible dates and the proof

`df.duplicated()` finds **6 exact copies**. But the City Health Office also re-notified
some patients with the name re-typed, a different date style and another barangay
spelling. After cleaning, those rows match on what matters, so we de-duplicate on
*(name key, disease, onset date)*. That finds **19 duplicates** in all: the 6 exact
copies and 13 near-duplicates.

```python
duplicate = df.duplicated(subset=["name_key", "disease", "date_onset"], keep="first")
```

The two onsets typed after the consultation date are set to missing (in real life,
Maya would phone the reporting unit). The 618 cases left get new IDs, `SLC-0001` to
`SLC-0618`. Then come the **validation rules**: sentences about the data that must
always be true, written as `assert` so that a bad future export stops the notebook
loudly.

```python
both = clean.dropna(subset=["date_onset", "date_consult"])
assert (both["date_onset"] <= both["date_consult"]).all()          # ill before consulting
```

:::{admonition} Check it
:class: ph-check
Doc Mon asks: *"Is yours the same as the official clean file?"* The notebook ends by
letting pandas compare the two tables cell by cell:

```python
pd.testing.assert_frame_equal(ours, official)
```

No message means they are identical: 618 rows × 18 columns, the file every later
chapter uses (`santa_luz_linelist.csv`).
:::

:::{div}
:class: ph-game ph-game-quiz
**Quick check: cleaning a line list**

1. Your date column has no errors after `pd.to_datetime(..., dayfirst=True)`. Is it safe?
   - ✓ Not yet: count the `NaT`s and check that onset is never after consultation — a wrong parse raises no error.
   - Yes: if there were a problem, pandas would raise an error — silent mis-parses raise nothing.
2. Why turn names into a salted key instead of just deleting them?
   - ✓ We still need to find duplicate notifications of the same person — the key matches without showing the name.
   - Because a keyed file is safe to publish — it is still confidential while the salt exists.
   - So we can read the name back later — a good key cannot be read back.
3. `df.duplicated()` found 6 rows. Are those all the duplicates?
   - Yes — a duplicate is an identical row. Re-notified patients were typed differently, so they are not identical.
   - ✓ No — it only finds rows identical in every column. 13 more near-duplicates appear after cleaning, on name key, disease and onset.
:::

:::{admonition} Baon
:class: ph-baon
- Protect identities first: key the name, drop names, phones, addresses and remarks.
- Never let the computer guess a date: one explicit rule per format, then count `NaT`s
  and check onset ≤ consultation.
- Write your rules as `assert`s and prove the result: `assert_frame_equal` against a
  trusted version.

Open the notebook: [](notebooks/03_clean_linelist.ipynb)
:::
