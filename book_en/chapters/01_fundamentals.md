# 01 Core Epidemiology Concepts (Python From Scratch)

## What you'll learn

- Common data objects in epi analysis: variables, lists, dictionaries (dict), DataFrames
- 4 essential Python basics: assignment, types, conditionals, functions
- Core epi metrics: the definitions and calculations of attack rate and CFR
- How to turn a "written conclusion" into "reusable, re-runnable code"

## Prerequisites (for absolute beginners)

If you have no Python experience, just keep these 5 points in mind:

1. `=` means "put the result on the right into the variable on the left" — it is not a math equals sign.
2. Anything after `#` is a **comment** — Python ignores it completely and won't run it. Comments are notes written for humans.
3. `print(...)` is used to display results.
4. Strings (text) need quotes, like `"confirmed"`.
5. Percentages are usually displayed with `:.2%`.

### About `#` comments

```python
# This whole line is a comment; Python won't run it
total = 280        # This is an inline comment; text after # is not executed

# Good habit: use comments to explain "why" you did something
# The denominator is the 121 infected, not the 280 total (that's the definition of CFR)
cfr = 19 / 121
```

In a Jupyter notebook, you'll see two kinds of "explanatory text":
- **`#` comments**: written inside Code cells, mixed in with the code
- **Markdown cells**: standalone text blocks that can have headings, bold text, lists, and tables (see Ch00 for details)

## The story

An outbreak of Legionnaires' disease has broken out at Songbai Nursing Home, and your supervisor has just handed you the line list. Before you learn how to read a CSV with pandas (that's Ch02), they first want you to answer:

- What's the facility-wide attack rate?
- What's the case fatality rate (CFR)?
- What are the hospitalization rate and ICU rate?
- Should we escalate the response level?

Let's compute these metrics using the most basic Python — that's what this chapter is all about.

## Core concepts

- **Variable**: a labeled box that stores a value, which you retrieve later by name.
- **Data type**: integer `int`, float `float`, string `str`, boolean `bool` — this determines what operations a value can do.
- **Case definition**: first define who counts as a case, then compute the metrics.
- **Line list**: one row per case, one column per variable (this course uses Legionella outbreak data of 280 residents × 32 columns).
- **Attack rate**: `cases / population` — in this outbreak, 121 / 280 = 43.2%.
- **Case fatality rate (CFR)**: `deaths / cases` — in this outbreak, 19 / 121 = 15.7%.
- **Bias / confounding**: the most common sources of problems in data collection and interpretation (explored in depth in Ch05).

## Tutorial videos

Each concept comes with a companion animated tutorial video (about 3 minutes), embedded in the corresponding section below. Each video includes: the main lesson → an extra outbreak-response example → busting common beginner blind spots.

We recommend watching the video before reading the code — it makes learning much easier!

## Python basics practice (step by step)

### 1) Numeric variables — store the numbers first

```{figure} images/python_variables_en.svg
:name: fig-python-variables
:alt: A variable is a labeled box, plus the four basic data types int / float / str / bool
:width: 100%

A **variable** is a labeled box; `=` means "put the value on the right into the box on the left." The four basic data types: `int` (integer), `float` (floating-point number), `str` (string), `bool` (boolean).
```

<!-- video: ch01_01_variables -->
<!-- /video -->

```python
# Basic data from the Legionnaires' disease outbreak at Songbai Nursing Home
total_residents = 280       # Total number of residents
infected = 121              # Number infected (including asymptomatic)
confirmed = 89              # Confirmed cases
probable = 25               # Probable cases
hospitalized = 68           # Number hospitalized
icu = 23                    # Number in ICU
deaths = 19                 # Number of deaths
```

### 2) Computing metrics — use division to get rates

<!-- video: ch01_02_arithmetic -->
<!-- /video -->

```python
# Attack rate = number infected / total residents
attack_rate = infected / total_residents
print(f"Attack rate: {attack_rate:.2%}")

# Case fatality rate = number of deaths / number infected
cfr = deaths / infected
print(f"CFR: {cfr:.2%}")

# Hospitalization rate = number hospitalized / number infected
hosp_rate = hospitalized / infected
print(f"Hospitalization rate: {hosp_rate:.2%}")
```

### 3) Dictionaries — keep data on the same topic together

```{figure} images/python_list_vs_dict_en.svg
:name: fig-python-list-vs-dict
:alt: Comparison of list and dict — a list retrieves values by index, a dict retrieves values by key
:width: 100%

A **list** is a row of pigeonholes; you retrieve values by index (starting from 0). A **dict** is a set of labeled storage boxes; you retrieve values by key. We'll cover dictionaries first, then lists.
```

<!-- video: ch01_03_dictionaries -->
<!-- /video -->

```python
# Use a dictionary to organize the outbreak summary
outbreak = {
    "facility": "Songbai Nursing Home",
    "pathogen": "Legionella pneumophila",
    "total_residents": 280,
    "infected": 121,
    "confirmed": 89,
    "deaths": 19,
}

# Pull values out of the dictionary to compute
cfr = outbreak["deaths"] / outbreak["infected"]
print(f"{outbreak['facility']} CFR: {cfr:.2%}")
```

### 4) Lists — store a group of same-kind data

<!-- video: ch01_04_lists -->
<!-- /video -->

```python
# Number of infections in each floor-wing
floor_wing_cases = [15, 10, 24, 25, 20, 27]  # 1A, 1B, 2A, 2B, 3A, 3B
floor_wing_names = ["1A", "1B", "2A", "2B", "3A", "3B"]

# Find the wing with the most infections
max_cases = max(floor_wing_cases)
max_index = floor_wing_cases.index(max_cases)
print(f"Wing with the most infections: {floor_wing_names[max_index]} ({max_cases} people)")
```

### 5) Conditionals — turn metrics into action signals

```{figure} images/python_if_else_flow_en.svg
:name: fig-python-if-else
:alt: An if / elif / else flowchart — the CFR passes through several conditions and arrives at the corresponding response level
:width: 100%

A **conditional statement** lets data take different paths depending on conditions. `if` → `elif` (else if) → `else`. `>`, `<`, `==`, `!=` are **comparison operators** that return `True` or `False`.
```

<!-- video: ch01_05_conditionals -->
<!-- /video -->

```python
# Decide the response level based on the case fatality rate
if cfr > 0.15:
    print("CFR is high (>15%); recommend escalating the response level")
elif cfr > 0.10:
    print("CFR is moderate (10-15%); keep strengthening surveillance")
else:
    print("CFR is acceptable (<10%); maintain routine response")
```

### 6) Functions — package your calculation logic into a reusable tool

```{figure} images/python_function_machine_en.svg
:name: fig-python-function
:alt: A function is an automatic calculator — inputs go in as parameters, pass through the function body, and an output is returned
:width: 100%

A **function** is like an automatic calculator: inputs go in as **parameters** → pass through the **body** → `return` an **output**. Define it once, call it many times (reusability); to change the formula you only change one place, so nothing slips through the cracks.
```

<!-- video: ch01_06_functions -->
<!-- /video -->

```python
def calc_attack_rate(cases, population):
    """Calculate the attack rate."""
    if population == 0:
        raise ValueError("The denominator (population) cannot be 0")
    return cases / population

# Facility-wide attack rate
ar_all = calc_attack_rate(121, 280)
print(f"Facility-wide attack rate: {ar_all:.2%}")

# Attack rate for 3rd floor, wing B
ar_3b = calc_attack_rate(27, 47)
print(f"3rd floor wing B attack rate: {ar_3b:.2%}")
```

## A template for translating epi into code

1. First define the terms: `infected`, `deaths`, `total_residents`.
2. Then write the formula: `attack_rate = infected / total_residents`.
3. Finally write the interpretation rule: for example, `if cfr > 0.15`.
4. If you need to reuse it, wrap it in a function: `def calc_attack_rate(cases, population)`.

## Common mistakes (the easiest traps for beginners)

- Storing `infected` as text (`"121"`) instead of a number (`121`).
- Forgetting that the denominator can't be 0 (e.g., a wing with no residents).
- Editing the result number directly without changing the original input values (the code won't produce the correct result).
- The CFR denominator is the "number infected," not the "total number of residents" — be clear on the concept.

## Practice notebooks

- Class notes: {ref}`01_fundamentals_python_basics.ipynb`
- Exercise version: [`01_fundamentals_exercise.ipynb`](exercises/01_fundamentals_exercise.ipynb)
- Solution version (instructor edition): [`01_fundamentals_solution.ipynb`](solutions/01_fundamentals_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/01_fundamentals_solution.ipynb>)

## Minimal runnable environment commands

```bash
uv sync
uv run jupyter lab
```
