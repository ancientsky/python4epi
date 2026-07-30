# 01b The Python Developer's Toolbox

## Scenario

You just finished computing the attack rate and case fatality rate in Ch01. Your supervisor looks at your Python code and throws a barrage of questions at you:

- "Why the four spaces of indentation?"
- "What does `import` mean?"
- "What do I do when a red error message pops up?"
- "How do I install a new package?"

Before you step into the pandas world of Ch02, this chapter fills in the **Python developer common sense every epidemiologist needs**—not to turn you into a software engineer, but to keep you from freezing up when a problem hits.

## What you'll learn

- Python's indentation rules—why the four spaces are mandatory
- The `import` syntax—how to borrow tools other people have already built
- Types and conversion—how numbers, text, and booleans convert to one another
- Reading error messages—a traceback isn't a cryptic scroll
- `try/except`—handling the unexpected gracefully
- String methods and advanced loops—must-have skills for cleaning messy data
- Advanced `uv` usage—managing Python versions and third-party packages
- Handy Jupyter tricks—`!` commands, Tab auto-completion, looking up documentation

## Prerequisites (for absolute beginners)

This chapter assumes you already know the 6 things taught in Ch01:

1. Variables (`total_residents = 280`)
2. Arithmetic operations (`infected / total_residents`)
3. Dictionaries (`outbreak = {"deaths": 19, ...}`)
4. Lists (`[15, 10, 24, 25, 20, 27]`)
5. Conditionals (`if cfr > 0.15:`)
6. Functions (`def calc_attack_rate(cases, population):`)

If any of these still feel shaky, go back and work through the Ch01 exercises once more before continuing.

## Tutorial videos

Every concept comes with a companion animated tutorial video (about 3 minutes each), embedded in the corresponding section below. Each video covers: the main lesson → an extra outbreak example → common beginner blind spots debunked.

We recommend watching the video before reading the code—it makes the learning stick better!

---

## Part 1: Python Syntax Rules

### 1) Indentation—Python's non-negotiable rule

<!-- video: ch01b_01_indentation -->
```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Indentation: Python's Must-Follow Rule</div>
  <div class="youtube-lite" data-id="jOiqKrkqClg">
    <img src="https://img.youtube.com/vi/jOiqKrkqClg/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```
<!-- /video -->

In most programming languages, indentation just makes your code "look nice." But in Python, **indentation is part of the syntax**—one space too few or too many and the program breaks.

```python
# ✅ Correct: the code under if is indented 4 spaces
cfr = 19 / 121
if cfr > 0.15:
    print("CFR is high; recommend escalating the response level")
    print("Please notify the command center")
```

```python
# ❌ Wrong: forgetting to indent → IndentationError
cfr = 19 / 121
if cfr > 0.15:
print("CFR is high")  # IndentationError: expected an indented block
```

**Three indentation rules:**

| Rule | Explanation |
|------|------|
| Always use 4 spaces | This is what Python's official style guide (PEP 8) specifies |
| Don't mix tabs and spaces | Mixing produces a `TabError`; Jupyter uses spaces by default, so no need to worry |
| Align within the same block | The code under `if`, `for`, and `def` must sit at the same level |

**When do you need to indent?** Whenever you see a colon `:`, indent—`if:`, `for:`, `def:`, `while:`, `try:`, `except:`.

```python
# Nested indentation: an if inside a for
floor_cases = [15, 10, 24, 25, 20, 27]
for cases in floor_cases:       # first level
    if cases > 20:              # second level (indent 4 more spaces)
        print(f"{cases} infected, needs close attention")
```

### 2) import—borrowing other people's tools

<!-- video: ch01b_02_imports -->
```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: import: Borrow Other People's Tools</div>
  <div class="youtube-lite" data-id="vu8D3_MhAog">
    <img src="https://img.youtube.com/vi/vu8D3_MhAog/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```
<!-- /video -->

Every calculation in Ch01 used Python's built-in features. But when you do real outbreak analysis, you'll need to "borrow" powerful tools other people have already written—that's what `import` is for.

```{figure} images/python_import_forms_en.svg
:name: fig-python-import-forms
:alt: The three import forms — import module, from module import name, import module as alias
:width: 100%

**The three import forms**: ① `import statistics` hauls the whole box home, and you add a prefix when using it; ② `from statistics import mean` picks out just one tool, and you call it without a prefix; ③ `import pandas as pd` gives it an alias (community conventions: `pd`, `np`, `plt`, `sns`).
```

**The three import forms:**

```python
# Form 1: import the whole module
import math
print(math.sqrt(121))   # 11.0 (square root)

# Form 2: borrow just one feature
from math import sqrt
print(sqrt(121))         # 11.0 (no need for the math. prefix)

# Form 3: give it an alias (the most common!)
import statistics as stats
ages = [72, 68, 81, 75, 90, 66, 78, 85, 73, 69]
print(stats.median(ages))  # 73.5 (median age)
```

**imports you'll see in Ch02:**

```python
import pandas as pd          # pd is the conventional abbreviation
import matplotlib.pyplot as plt  # plt is also conventional
import seaborn as sns         # sns comes from Samuel Norman Seaborn (a TV character)
```

> 💡 **Convention**: import statements always go at the very top of the file. That way a single glance tells you which tools this program uses.

**Outbreak demo: analyzing case ages with the `statistics` module**

```{figure} images/python_dot_notation_en.svg
:name: fig-python-dot-notation
:alt: Dot notation — statistics.mean(ages) broken down into "toolbox.tool(input)"
:width: 100%

**Dot notation**: `statistics.mean(ages)` reads as "the mean feature **of** the statistics toolbox, passed ages." The `.` means "of"—first you name the source (a module or object), then you pull out the feature inside it. String objects have `.strip()` and `.split()`; a DataFrame has `.groupby()` and `.head()`—**it's all the same rule**.
```

```python
import statistics

# ages of 10 infected people
ages = [72, 68, 81, 75, 90, 66, 78, 85, 73, 69]

# dot notation: the mean feature "of" statistics, passed ages
print(f"Mean age: {statistics.mean(ages):.1f}")      # 75.7
print(f"Median:   {statistics.median(ages):.1f}")     # 73.5
print(f"Std dev:  {statistics.stdev(ages):.1f}")      # 7.8
```

### 3) Types and conversion—numbers, text, booleans

<!-- video: ch01b_03_types -->
```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Types and Conversion: Numbers, Text, Booleans</div>
  <div class="youtube-lite" data-id="KZTWa4BHCfY">
    <img src="https://img.youtube.com/vi/KZTWa4BHCfY/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```
<!-- /video -->

Every value in Python has a **type**. Get the type wrong and the program errors out.

```python
# use type() to check the type
print(type(280))        # <class 'int'>    integer
print(type(43.2))       # <class 'float'>  floating point (decimal)
print(type("confirmed"))# <class 'str'>    string (text)
print(type(True))       # <class 'bool'>   boolean
```

**Type conversion:** data read in from a CSV often comes in entirely as text. You need to convert it by hand before you can compute with it.

```python
# suppose these came in from a CSV as text
infected_str = "121"
total_str = "280"

# ❌ dividing text → TypeError
# result = infected_str / total_str

# ✅ convert to numbers first, then compute
infected = int(infected_str)
total = int(total_str)
attack_rate = infected / total
print(f"Attack rate: {attack_rate:.2%}")  # Attack rate: 43.21%
```

**Booleans:** `True` and `False` are Python's logical values. Comparison operations produce booleans.

```python
cfr = 19 / 121
print(cfr > 0.15)       # True (case fatality rate > 15%)
print(cfr > 0.20)       # False (case fatality rate is not > 20%)

# logical operations: and, or, not
high_cfr = cfr > 0.10
many_cases = 121 > 100

if high_cfr and many_cases:
    print("High CFR + many infections: recommend escalating the response level")

# not inverts
if not (cfr < 0.05):
    print("CFR is not low; continued surveillance needed")
```

### 3b) Bracket map—when do you use each of `( )` `[ ]` `{ }` `" "`?

What trips beginners up most is knowing "which bracket to use in which situation." Use the wrong one and the program breaks.

```{figure} images/python_brackets_guide_en.svg
:name: fig-python-brackets
:alt: A usage map of Python's four bracket types — parentheses ( ), square brackets [ ], curly braces { }, quotes " "
:width: 100%

**Bracket map**: `( )` parentheses = verbs (calling functions, computing, tuples); `[ ]` square brackets = nouns (lists, indexing, getting dictionary values); `{ }` curly braces = one-to-one (dictionary key:value, sets, f-string variables); `" "` quotes = text strings.
```

**A memory aid for the four bracket types:**

| Symbol | Main use | Example |
|------|----------|------|
| `( )` | **Action**—call a function, group an operation, tuple | `print("hi")`, `(a + b) * 2`, `(24.15, 120.67)` |
| `[ ]` | **Getting something**—create a list, index, get a dictionary value | `["1A", "1B"]`, `wings[0]`, `outbreak["deaths"]` |
| `{ }` | **One-to-one**—dictionary key:value, set, f-string variable | `{"deaths": 19}`, `{"1A", "1B"}`, `f"CFR: {cfr:.2%}"` |
| `" "` | **Text**—string data (single and double quotes are equivalent) | `"confirmed"`, `'Legionella'`, `"""multi-line docs"""` |

> ⚡ **Most common mistake**: `outbreak("deaths")` ← used parentheses. Getting a dictionary value needs square brackets: `outbreak["deaths"]`. Parentheses are for "calling"; square brackets are for "getting."

---

## Part 2: Debugging Survival Skills

### 4) Reading error messages—a traceback isn't a cryptic scroll

<!-- video: ch01b_04_errors -->
```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Reading Error Messages: Traceback Is Not Hieroglyphics</div>
  <div class="youtube-lite" data-id="00CEZEeFXMw">
    <img src="https://img.youtube.com/vi/00CEZEeFXMw/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```
<!-- /video -->

Don't panic at a screen full of red text. Python's error messages are actually quite considerate—just **read from the last line upward**.

```{figure} images/python_traceback_reading_en.svg
:name: fig-python-traceback
:alt: Reading a Python traceback — read from the bottom up; the last line is the error type, the middle is the execution path
:width: 100%

**The SOP for reading a traceback**: ① look at the **last line** first (error type + message, e.g. `TypeError: ...`); ② go back and find the line number in **your own file name** (for example `File "outbreak.py", line 15`) and look at the code on that line; ③ cross-reference the quick-lookup table on the right (`NameError`, `TypeError`, `KeyError`, `IndexError`, `IndentationError`).
```

**The mantra for reading a traceback: look at the last line → look at the error type → look at the line number**

Here are the 5 errors epidemiologists run into most:

```python
# 1) NameError: variable name typo
# infceted = 121   (misspelled!)
# print(infected)  → NameError: name 'infected' is not defined
# Fix: check the spelling; Python is case-sensitive

# correct version
infected = 121
print(infected)  # 121
```

```python
# 2) TypeError: wrong type
# "121" / "280"  → TypeError: unsupported operand type(s) for /: 'str' and 'str'
# Fix: convert the type first
print(int("121") / int("280"))  # 0.432...
```

```python
# 3) KeyError: the dictionary has no such key
outbreak = {"deaths": 19, "infected": 121}
# outbreak["death"]  → KeyError: 'death'
# Fix: check the key name; even one wrong letter fails
print(outbreak["deaths"])  # 19
```

```python
# 4) IndexError: list index out of range
wings = ["1A", "1B", "2A", "2B", "3A", "3B"]
# wings[6]  → IndexError: list index out of range
# Fix: 6 elements means indices are 0-5
print(wings[5])  # "3B"
```

```python
# 5) FileNotFoundError: file not found
# pd.read_csv("data/outbreak.csv")
# → FileNotFoundError: [Errno 2] No such file or directory: 'data/outbreak.csv'
# Fix: verify the path; this course's data lives at data/synthetic/legionella_outbreak.csv
```

**Debug quick-lookup table:**

| Error type | Common cause | How to fix |
|---------|---------|---------|
| `NameError` | Variable name typo / undefined | Check spelling and case |
| `TypeError` | Text and numbers mixed | Convert with `int()` / `float()` |
| `KeyError` | Wrong dictionary key name | Check all keys with `dict.keys()` |
| `IndexError` | List index out of range | Confirm the length with `len()` |
| `FileNotFoundError` | Wrong file path | Confirm the file exists with `!ls` |
| `IndentationError` | Inconsistent indentation | Always use 4 spaces |
| `SyntaxError` | Missing colon, mismatched quotes | Look carefully at the line that errored |

### 5) try/except—handling the unexpected gracefully

<!-- video: ch01b_05_try_except -->
```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: try/except: Handle Surprises Gracefully</div>
  <div class="youtube-lite" data-id="Gv_Ct86O8XM">
    <img src="https://img.youtube.com/vi/Gv_Ct86O8XM/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```
<!-- /video -->

Sometimes an error is an "expected surprise"—for example, missing values in the data. Rather than let the program crash, tell Python how to handle it.

```python
# without try/except: one piece of bad data and the whole thing crashes
ages_raw = ["72", "68", "N/A", "75", "unknown", "66"]
ages = []
for val in ages_raw:
    ages.append(int(val))  # "N/A" → ValueError, and the program stops right here!
```

```python
# with try/except: skip the bad data and keep going
ages_raw = ["72", "68", "N/A", "75", "unknown", "66"]
ages = []
skipped = 0
for val in ages_raw:
    try:
        ages.append(int(val))
    except ValueError:
        skipped += 1

print(f"Converted {len(ages)} successfully, skipped {skipped}")  # Converted 4 successfully, skipped 2
print(f"Mean age: {sum(ages) / len(ages):.1f}")          # Mean age: 70.2
```

**When should you use try/except?**

| Scenario | Recommendation |
|------|------|
| Reading an external CSV file | ✅ Yes—the file may not exist |
| Handling user-supplied data | ✅ Yes—the format is unpredictable |
| Your own internal calculations | ❌ No—fix the logic first |
| Division that might divide by zero | ✅ Yes—or check first with `if` |

---

## Part 3: Practical Development Techniques

### 6) Advanced strings and loops

<!-- video: ch01b_06_strings_loops -->
```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Strings and Advanced Loops: The Swiss Army Knife for Cleaning Outbreak Data</div>
  <div class="youtube-lite" data-id="ydQ-lOlN5Ec">
    <img src="https://img.youtube.com/vi/ydQ-lOlN5Ec/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```
<!-- /video -->

When you process CSV data in Ch02, you'll work heavily with strings and loops. Let's build the foundation here first.

**Common string methods:**

```python
# messy-string problems common in outbreak data
raw_name = "  Legionella pneumophila  "
print(raw_name.strip())      # "Legionella pneumophila" (strips leading/trailing whitespace)

raw_severity = "Mild,Moderate,Severe"
levels = raw_severity.split(",")
print(levels)                # ["Mild", "Moderate", "Severe"]

raw_status = "confirmed "
clean = raw_status.strip().lower()
print(clean)                 # "confirmed"

# check the start of / containment in a string
pathogen = "Legionella pneumophila serogroup 1"
print(pathogen.startswith("Legionella"))   # True
print("serogroup" in pathogen)             # True
```

**for loops with range() and enumerate():**

```python
# range(): generate a sequence of numbers
# print the new cases for days 1 through 5
daily_cases = [3, 7, 12, 8, 15]
for i in range(len(daily_cases)):
    print(f"Day {i+1}: {daily_cases[i]} cases")

# enumerate(): get the index and value at once (more Pythonic)
for i, cases in enumerate(daily_cases, start=1):
    print(f"Day {i}: {cases} cases")
```

**The `in` membership check—used heavily in Ch02:**

```python
# check whether a value is in a list
high_risk_floors = [2, 3]
patient_floor = 3
if patient_floor in high_risk_floors:
    print("This case is on a high-risk floor")

# check whether a dictionary has a given key
outbreak = {"pathogen": "Legionella", "cases": 121}
if "deaths" not in outbreak:
    print("The dictionary has no death-count data")
```

### 7) Advanced uv—managing Python versions and packages

<!-- video: ch01b_07_uv_advanced -->
```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Advanced uv: Manage Python Versions and Packages</div>
  <div class="youtube-lite" data-id="l-WcIwSMv5s">
    <img src="https://img.youtube.com/vi/l-WcIwSMv5s/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```
<!-- /video -->

Ch00 taught `uv sync` to install all of the course's dependencies. Here we go a step further into `uv`'s practical features.

**Managing Python versions:**

```bash
# see which Python versions are currently available
uv python list

# install a specific version of Python
uv python install 3.11

# pin the Python version the project uses (writes to .python-version)
uv python pin 3.12
```

**Installing third-party packages:**

```bash
# install a package (automatically updates pyproject.toml and uv.lock)
uv add pandas

# install a specific version
uv add "pandas>=2.0,<3.0"

# install a development package (not used in production)
uv add --dev pytest

# remove a package
uv remove pandas

# list all currently installed packages
uv pip list
```

**How do you find good third-party packages?**

| Method | URL / command | What to look at |
|------|------------|-----------|
| PyPI search | search keywords at `https://pypi.org` | last update date, download count |
| GitHub | search `topic:epidemiology python` | number of stars, issue response speed |
| Awesome lists | search `awesome-epidemiology` | community-curated package collections |

**Recommended packages for epidemiology:**

| Package | Use | Course chapters using it |
|------|------|-------------|
| `pandas` | Tabular data processing | Every chapter from Ch02 on |
| `matplotlib` | Basic plotting | Every chapter from Ch02 on |
| `seaborn` | Statistical charts | Ch02, 03 |
| `scipy` | Statistical tests | Ch03, 05 |
| `lifelines` | Survival analysis | Ch09 |
| `geopandas` | Spatial data | Ch08 |
| `plotly` | Interactive charts | Ch02, 08 |
| `scikit-learn` | Machine learning | Ch10 |
| `tensorflow` | Deep learning | Ch11 |

### 8) Handy Jupyter tricks

<!-- video: ch01b_08_jupyter_tips -->
```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Practical Jupyter Tips: Double Your Efficiency</div>
  <div class="youtube-lite" data-id="L9nzl_m2pnE">
    <img src="https://img.youtube.com/vi/L9nzl_m2pnE/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
</div>
```
<!-- /video -->

The following tricks make your work in Jupyter Lab more efficient.

**`!` runs shell commands:**

Put a `!` at the start of a code cell and you can run terminal commands directly.

```python
# check whether the data file exists
!ls data/synthetic/

# quickly preview the first few rows of the CSV
!head -5 data/synthetic/legionella_outbreak.csv

# check the number of lines in the file (to gauge the data volume)
!wc -l data/synthetic/legionella_outbreak.csv

# see the current working directory
!pwd
```

**Installing packages with uv inside Jupyter:**

```python
# install a new package
!uv add seaborn

# after installing, you must Restart Kernel before you can import
# Kernel → Restart Kernel (or use the keyboard shortcut)
```

> ⚠️ **Important**: after installing a package, always Restart Kernel, otherwise `import` won't find the package you just installed.

**Viewing a function's documentation:**

```python
# use ? for a brief description
len?

# use ?? to view the source code (if available)
len??
```

**Tab auto-completion:**

Pressing `Tab` in Jupyter can:
- Complete a variable name: type `out` + Tab → `outbreak`
- List an object's methods: type `outbreak.` + Tab → shows all available methods
- Complete a file path: type `"data/` inside a string + Tab → lists the directory's contents

**`%timeit` to measure execution time:**

```python
# when you're curious how fast a piece of code runs
%timeit sum(range(10000))
```

**A roundup of useful Magic commands:**

| Command | Function |
|------|------|
| `!command` | Run a shell command |
| `?obj` | View an object's description |
| `??obj` | View an object's source code |
| `%timeit expr` | Measure a single line's execution time |
| `%%timeit` | Measure the whole cell's execution time |
| `%who` | List all currently defined variables |
| `%whos` | List variables + types + values |
| `%pwd` | Show the working directory |
| `%history` | Show input history |

---

## Common Errors Roundup

| Error | Cause | Fix |
|------|------|------|
| `IndentationError` | Inconsistent indentation or forgetting to indent | The line after a colon must be indented 4 spaces |
| `ModuleNotFoundError` | Package not installed or name typo | `uv add packagename`, then Restart Kernel |
| `NameError` | Variable undefined or misspelled | Check spelling; Python is case-sensitive |
| `TypeError` | Wrong type (e.g. dividing text) | Check with `type()` first, then convert with `int()` / `float()` |
| `KeyError` | Dictionary key doesn't exist | Check first with `.keys()` or `if key in dict` |
| `SyntaxError` | Missing colon, mismatched quotes | Look carefully at the line that errored; usually a missing `:` or `"` |
| `TabError` | Mixing tabs and spaces | Jupyter uses spaces by default; don't use tabs |

## Ch01-to-Ch02 transition checklist

Before moving on to Ch02, make sure you can answer the following questions:

- [ ] What does the line `import pandas as pd` do?
- [ ] Why does the code under an `if` need to be indented 4 spaces?
- [ ] What's the difference between `type("121")` and `type(121)`?
- [ ] When you see `NameError: name 'df' is not defined`, what do you do?
- [ ] How do you install a new package inside Jupyter?
- [ ] What does the line `"Legionella" in pathogen` check?

If you can answer all of these, congratulations—you're ready to enter the pandas world of Ch02!

## Workbooks

- Class notes: {ref}`01b_python_toolbox.ipynb`
- Exercise version: [`01b_python_toolbox_exercise.ipynb`](exercises/01b_python_toolbox_exercise.ipynb)
- Solution version (instructor): [`01b_python_toolbox_solution.ipynb`](solutions/01b_python_toolbox_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/01b_python_toolbox_solution.ipynb>)
