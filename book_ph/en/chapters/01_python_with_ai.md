---
title: "01 Kumusta, Python?"
description: "The least Python you need to read AI-written code: variables, lists, dictionaries, loops, if, functions and f-strings, a first look at the line list with pandas, and how to read an error calmly."
---

::::{div}
:class: ph-story
*Tuesday 28 July 2026 · 7:40 a.m. · CESU office*

:::{div}
:class: ph-say-maya
**Maya:** Six new forms on my desk, and a tally sheet. *Isa, dalawa, tatlo...* One, two, three leptospirosis. I'll be doing this every morning?
:::

:::{div}
:class: ph-say-tala
**Tala:** I can count them for you in four lines of Python.
:::

:::{div}
:class: ph-say-mon
**Doc Mon:** Good. But Maya, if you cannot read those four lines, you cannot sign the report. Learn enough Python to *read* what Tala writes.
:::

> How much Python do you need to read, and check, code that someone else wrote?
::::

Less than you think. You do not need to *write* programs from memory. You need to
recognise about seven building blocks, the way you recognise the sections of a case
investigation form. This chapter teaches those seven, using Maya's six forms.

## Seven building blocks

| Block | Looks like | Think of it as |
|---|---|---|
| **Variable** | `barangay = "Ilog"` | a label on a folder; `=` means *put this in* |
| **Text and numbers** | `"Ilog"`, `34`, `True` | text goes in quotes; `True`/`False` are yes/no |
| **List** | `ages = [34, 9, 41]` | a column of values, in order |
| **Dictionary** | `{"disease": "dengue", "age": 9}` | one form: labels (keys) and answers (values) |
| **Loop** | `for f in forms:` | going through the stack one form at a time |
| **`if`** | `if f["disease"] == "dengue":` | a yes/no question; `==` asks *"is it equal?"* |
| **Function** | `def percent(part, whole):` | a named recipe you can reuse; `return` gives back the result |

Two more things you will see everywhere. An **f-string**, `f"{n} cases"`, puts a value
inside a sentence. A **comment** starts with `#`; Python ignores it, so it is a note for
humans. Good AI-written code has many.

One trap: Python counts list positions from **0**. The first item of `ages` is
`ages[0]`, not `ages[1]`. This "off-by-one" slip is common in AI code too.

## Maya's stack, in Python

Maya types her six forms as a **list of dictionaries**, one dictionary per form. She uses
a letter, not a name, for each form. All six are invented.

```python
forms = [
    {"form": "A", "barangay": "Ilog",   "disease": "leptospirosis", "age": 34, "waded": True},
    {"form": "B", "barangay": "Ilog",   "disease": "dengue",        "age": 9,  "waded": False},
    {"form": "C", "barangay": "Wawa",   "disease": "leptospirosis", "age": 41, "waded": True},
    {"form": "D", "barangay": "Sapa",   "disease": "dengue",        "age": 15, "waded": False},
    {"form": "E", "barangay": "Ilog",   "disease": "leptospirosis", "age": 52, "waded": False},
    {"form": "F", "barangay": "Talaba", "disease": "dengue",        "age": 23, "waded": True},
]
```

:::{admonition} Ask Tala
:class: ph-ask-tala
I have a Python list called `forms`. Each item is a dictionary with keys `form`,
`barangay`, `disease`, `age`, `waded` (True/False). Two made-up items:
`{"form": "A", "barangay": "Ilog", "disease": "leptospirosis", "age": 34, "waded": True}` and
`{"form": "B", "barangay": "Ilog", "disease": "dengue", "age": 9, "waded": False}`.
Write beginner-friendly code that counts the leptospirosis forms. Explain each line.
:::

:::{admonition} Tala says
:class: ph-tala-says
```python
lepto_count = 0                      # start the tally at zero
for f in forms:                      # look at each form, one at a time
    if f["disease"] == "leptospirosis":   # == asks "is it equal?"
        lepto_count = lepto_count + 1     # add one tally mark

print(f"Leptospirosis forms: {lepto_count}")
```
:::

Read it like Maya's tally sheet: start at zero, look at each form, and **if** it is
leptospirosis, add one mark. The indented lines (four spaces in) belong to the loop and
to the `if`; indentation is how Python knows what is inside what.

:::{admonition} Check it
:class: ph-check
1. **Count by hand first**, before you run anything: forms A, C and E are leptospirosis.
   That is **3**.
2. Run the code. It prints `Leptospirosis forms: 3`.
3. Make the check automatic: `assert lepto_count == 3` stops with an error if the
   numbers disagree, and stays silent if they agree.
:::

## Tala got it wrong: "percent of what?"

Maya's next question: *what percentage of the leptospirosis forms waded in floodwater?*
Tala's code ran without any error and printed **33.3%**.

```python
waded_lepto = 0
for f in forms:
    if f["disease"] == "leptospirosis" and f["waded"]:
        waded_lepto = waded_lepto + 1
percent_waded = waded_lepto / len(forms) * 100
```

:::{admonition} Tala got it wrong
:class: ph-oops
Count by hand. Leptospirosis forms: A, C, E, so **3**. Of those, waded: A and C, so **2**.
Two out of three is **66.7%**, not 33.3%.

The numerator was right. The **denominator** was wrong: `len(forms)` counts **all six**
forms, dengue included. The code looks tidy, runs cleanly and gives the wrong answer.
That is the most dangerous kind of mistake, and only a hand count catches it.
:::

The fix is a small **function** with the denominator as an explicit input, so you have
to decide what it is every time you use it. It also refuses to divide by zero.

```python
def percent(part: int, whole: int) -> float:
    # Return part as a percentage of whole.
    if whole == 0:
        raise ValueError("The denominator is 0: there is nothing to take a percentage of.")
    return part / whole * 100


lepto_forms = [f for f in forms if f["disease"] == "leptospirosis"]   # only the lepto forms
waded_lepto = len([f for f in lepto_forms if f["waded"]])

answer = percent(waded_lepto, len(lepto_forms))
print(f"{waded_lepto} of {len(lepto_forms)} leptospirosis forms waded: {answer:.1f}%")
```

This prints `2 of 3 leptospirosis forms waded: 66.7%`. The line
`[f for f in forms if ...]` is a one-line loop: it keeps only the forms that pass the
test. The `: int` and `-> float` labels are optional notes on what goes in and what
comes out.

## Find the bug

Five pieces of AI-written code, each with one mistake. Tap the line that is wrong.

:::{div}
:class: ph-game ph-game-bug-hunt
AI code can look right and still be wrong: read it line by line, run it on a
case you can count by hand, and read the error message.
:::

## From six forms to 618 cases: pandas

For hundreds of rows, Python has **pandas**, a spreadsheet you control with code. In
the notebook you open the **clean, de-identified** Santa Luz line list. It has no names,
phones or addresses; [chapter 02](02_privacy_first.md) shows how a file gets that way.

```python
import pandas as pd

df = pd.read_csv("data/synthetic/ph/santa_luz_linelist.csv")
print(df.shape)
print(list(df.columns))
df.head()
```

`df.shape` prints `(618, 18)`: 618 cases and 18 columns. Copy column names **exactly**
when you ask Tala for code: `date_onset`, not "onset date". Then
`df["disease"].value_counts()` does what Maya's loop did, for the whole file:
**388** dengue and **230** leptospirosis cases. The check: `388 + 230 = 618`, the number
of rows.

## Reading an error calmly

Errors are messages, not insults. When Maya typed `df["Disease"]`, Python stopped with a
long block of red text. The part that matters is the **last line**:

```text
KeyError: 'Disease'
```

The **error type** says what kind of problem it is. `KeyError` means *"I looked for this
key, here a column name, and it is not there."* The column is `disease` with a small
*d*: Python treats capitals as different letters. Three errors you will meet often:

| Error | Usually means |
|---|---|
| `KeyError` | a column or key name is misspelled |
| `NameError` | a variable is used before the cell that creates it was run |
| `SyntaxError` | a missing bracket, quote or colon |

When a line confuses you, ask Tala to explain **that line only**: code, never data.

:::{admonition} Ask Tala
:class: ph-ask-tala
Explain this line of pandas to a beginner, word by word, and tell me what it would print
for a tiny made-up table with 3 rows: `df["disease"].value_counts()`.
:::

Then run the line and compare: does it really do what Tala said?

:::{admonition} Privacy stop
:class: ph-privacy
When you paste an error message into an AI chat, look at it first. Error messages can
show the values of the cell that failed, and in a real line list those values could be
a name. Paste the **code and the error type**, and replace any data in the message with
made-up values.
:::

## Quick check

:::{div}
:class: ph-game ph-game-quiz
**Quick check: reading Python**

1. `ages = [34, 9, 41]`. What is `ages[1]`?
   - `34` — that is `ages[0]`: Python counts from 0.
   - ✓ `9` — position 1 is the second item, because counting starts at 0.
   - `41` — that is `ages[2]`, or `ages[-1]`.
2. Code that computes a percentage runs without an error. What do you check first?
   - Nothing: no error means it is right — no, Tala's 33.3% ran perfectly and was wrong.
   - ✓ The denominator, on a tiny example counted by hand — "percent of what?"
   - The colours of the chart — useful later, but the number comes first.
3. Python says `KeyError: 'Barangay'`. What is the most likely fix?
   - ✓ Check the spelling and capitals of the column name — the file has `barangay`, small b.
   - Reinstall pandas — the library is fine; the name is wrong.
   - Delete the row with the error — a `KeyError` is about a name, not a row.
:::

:::{admonition} Baon
:class: ph-baon
- Seven building blocks (variables, text and numbers, lists, dictionaries, loops,
  `if`, functions) are enough to *read* most AI-written analysis code.
- Count a tiny example by hand before you trust a number. Always ask *"percent of
  what?"*: Tala's code divided by all forms instead of the leptospirosis forms.
- Read the last line of an error first. A `KeyError` usually means a misspelled column.

Run it yourself: [Open the notebook](notebooks/01_python_with_ai.ipynb)
:::
