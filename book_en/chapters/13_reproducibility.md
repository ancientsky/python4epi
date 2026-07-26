# 13 Reproducible Research and Reporting

## What You'll Learn

- How to lock package versions with `uv.lock`, turning "works on my machine" into "works on everyone's machine"
- What **determinism** is, and why fixing a **random seed** is the on/off switch that decides whether an analysis can be reproduced
- How to write a **schema contract** for your data columns, catching errors before an upstream data change slips through
- How to package an entire analysis into a **single-command workflow**, so anyone can reproduce your results with one command
- How to assemble a **minimal verifiable report**: data + code + environment + result — none of the four can be missing

## The Scenario

The analysis of the Legionella outbreak at Songbai Nursing Home is finally complete.
A week from now you'll need to regenerate the same outbreak report, and you have to guarantee that a colleague on a different machine gets identical results.

> "Last time it came out as 121 infected and 19 deaths, but when I rerun it I get something different?"

This is exactly the problem that **reproducible research** solves — not "did we get the right answer this time," but "given the same data and the same code, on a different machine, run by a different person, do we still get the same answer?"

---

## 🍰 Super-Simple Special: Reproducibility = a Good Recipe

> Does "reproducible research" sound serious and academic? Don't worry — let's think about it a different way: **reproducible research is just a recipe written carefully enough.**

A friend tastes your cake, is blown away, asks you for the recipe, and goes home wanting to recreate the exact same flavor. What do you give her?

- **Recipe = code**: every step is written down in words she can read and follow — not "add sugar to taste," but "120 grams of sugar." Analysis code works the same way: every transformation step should be a rerunnable line of code, not "I think I deleted a few weird-looking rows, if I remember right."
- **Ingredients = data**: the same brand of flour, the same egg — swap the ingredients and the taste changes. Analysis is the same: it uses the same raw data, and it **never quietly gets changed partway through without leaving a record**.
- **Kitchen setup = environment (`uv.lock`)**: your oven runs 180°C convection; your friend's oven reads a little off — the same recipe can still bake into a different result. The analysis equivalent of "oven settings" is package versions — `uv.lock` pins every package to an exact version number, so everyone bakes in the same "oven."
- **Rigged dice = seed (random seed)**: if one step in the recipe says "scatter a few sprinkles randomly," the two cakes obviously won't come out looking the same — unless you **rig the dice ahead of time** (fix the seed), so the "random" scattering follows the same order every time. Any step in an analysis that involves randomness (splitting train/test sets, initializing model weights) works exactly the same way.

```{figure} images/reproducibility_recipe_en.svg
:name: fig-reproducibility-recipe
:alt: The recipe metaphor for reproducible research: recipe (code), ingredients (data), kitchen setup (environment/uv.lock), and rigged dice (seed) come together into a plus sign, so anyone, on any machine, bakes the exact same cake (reproducible result)
:width: 100%

Gather all four things — code, data, environment, seed — and anyone, on any machine, bakes the same cake.
```

### Metaphor ↔ Technical Term Cross-Reference

| Metaphor | Technical term | In one line |
|---|---|---|
| Recipe | **Code** (source code / version control) | Every step written as readable, rerunnable code — not hand-tweaked from memory inside a notebook |
| Ingredients | **Data** | The same raw data, never quietly changed partway through without a record |
| Kitchen setup | **Environment** (`uv.lock`) | Package versions pinned, so you don't bake a different cake just because "your machine has a newer pandas and mine has an older one" |
| Rigged dice | **Seed** (random seed) | Every step that involves randomness (splitting train/test sets, initializing weights, sampling) has its seed fixed first, so "random" still comes out "randomly consistent" |
| Cake | **Reproducible result** | Anyone, on any machine, following the recipe produces the identical result |

> 🎂 At the end of the day, **reproducible means someone else can take your ingredients (code + data + environment + seed) and reproduce exactly the same result — no more, no less**. That single sentence beats any academic definition for being easy to remember.

---

<!-- video: ch13_01_repro_intuition -->
<!-- /video -->

## Core Concepts

Translating the recipe metaphor back into formal terms, reproducible research comes down to three things:

- **Environment lock**: `uv.lock` pins the version number of every dependency listed in `pyproject.toml` — not "roughly which version," but down to the exact patch number. Anyone who runs `uv sync` ends up with a virtual environment identical to yours.
- **Single-command workflow**: between "one piece of raw data" and "one report," there shouldn't be a single manual step that exists only inside your head. Ideally, someone clones your repo, runs a handful of fixed commands, and gets the exact same output you did.
- **Traceability**: every number in the report should be traceable back to "which data, which code version, which package version" produced it — the data path is hard-coded into the code, the analysis logic is under version control, and the output is saved together with its version information.

Put these three together and you get the "minimal rerunnable report" demonstrated next.

## Why Did My Rerun Give Different Results?

```{figure} images/reproducibility_drift_en.svg
:name: fig-reproducibility-drift
:alt: Why did my rerun give different results: on the left, three common landmines (unpinned package versions, no fixed random seed, manual notebook data edits left unrecorded) cause results to drift apart over time; on the right, three pillars (uv.lock pinning versions, a fixed seed, every transformation written into code) make results converge back to the same answer
:width: 100%

The landmines make each rerun "drift" a little further from the last; the three pillars make every rerun converge back to the same answer.
```

"Last time it was 121 infected and 19 deaths; this rerun gives different numbers" — more often than not, it's not that the analysis logic is wrong, but that you've stepped on one of the three landmines below.

### Three Common Landmines

1. **Unpinned package versions**: `pandas` upgrades from 2.0 to 2.2, and some function quietly changes its default handling of missing values or sort order — same code, same data, different numbers.
2. **No fixed random seed**: any time the code has a random step like `train_test_split`, `np.random`, or `torch.manual_seed`, failing to fix the seed means every run reshuffles the deck all over again. The next section proves this to you directly with a ten-line minimal example.
3. **Manual notebook edits to data, unrecorded**: deleting a few "weird-looking" rows by hand in a notebook, or manually correcting one field's value, without ever turning it into code — next time you rerun it, those hands have forgotten what they touched.

### Three Pillars (Matched One-to-One to the Landmines Above)

| Landmine | Pillar (the fix) |
|---|---|
| Unpinned package versions | `uv.lock` pins every package's version number; `uv sync` guarantees the installed environment matches the original author's |
| No fixed random seed | Every random step gets an explicit seed (`np.random.default_rng(42)`, `random_state=42`, `torch.manual_seed(42)`), so "random" comes out "randomly consistent" |
| Manual notebook edits to data, unrecorded | Every data transformation (dropping rows, editing values, deriving columns) is written as a visible line of code, not a few clicks of the mouse |

---

<!-- video: ch13_02_why_different_results -->
<!-- /video -->

## The Minimal Rerunnable Report: Code Walkthrough

A "minimal rerunnable report" needs to do this: starting from a clean environment, using **a fixed handful of commands + fixed code**, produce numbers identical to the original author's. Below it's broken into four parts: first rebuild and verify the environment, then produce the summary, then prove seed determinism, and finally lock down the data's structure with a schema contract.

### Step 1 — Three Commands, From a Clean Environment to a Report

```bash
uv sync
uv run pytest
uv run python notebooks/run_sitrep.py
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `uv sync` | Rebuilds the whole virtual environment according to the versions pinned in `uv.lock` — no matter which machine it runs on, the installed package versions come out identical |
> | `uv run pytest` | Runs the unit tests inside the freshly built environment, confirming the `epi_learning` package's core functions (`attack_rate`, `case_fatality_rate`, ...) behave correctly — passing tests means "the environment is alive, and the code is correct" |
> | `uv run python notebooks/run_sitrep.py` | Actually runs the analysis once: reads the line list, computes CFR and attack rate, outputs summary tables by zone — this is exactly the "minimal rerunnable report" this chapter is after |

> 💡 Three commands, zero manual steps — that's exactly the spirit of a single-command workflow: nobody needs to ask you "what else do I need to install, what else do I need to change." Copy, paste, and it reproduces.

<!-- video: ch13_03_min_reproducible_report -->
<!-- /video -->

### Step 2 — Read the Data, Produce a Summary: The One True Answer

```python
from pathlib import Path
import pandas as pd

path = Path("data/synthetic/legionella_outbreak.csv")
df = pd.read_csv(path)
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)  # Fixed rule: anything other than not_ill counts as infected

summary = {  # This dict is the "one true answer" for this analysis
    "n_residents": len(df),
    "n_zones": df.groupby(["floor", "wing"]).ngroups,
    "n_infected": int(df["infected"].sum()),
    "n_deaths": int((df["outcome"] == "dead").sum()),
    "attack_rate": f"{df['infected'].mean():.1%}",
    "cfr": f"{(df['outcome'] == 'dead').sum() / df['infected'].sum():.1%}",
}

print("=== Outbreak Summary ===")
for k, v in summary.items():
    print(f"  {k}: {v}")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `path = Path("data/synthetic/legionella_outbreak.csv")` | Pins the input file with a fixed path — the path itself is part of being "reproducible" |
> | `df = pd.read_csv(path)` | Reads the data with zero randomness involved — completely predictable behavior |
> | `df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)` | Derives a column with a fixed rule (anything other than not_ill counts as infected); the rule lives in the code, not in someone's memory of manually tagging cases |
> | `summary = {...}` | Collects every key number into one dict, serving as the "one true answer" for this analysis |

> 💡 **Why emphasize "determinism"**: `groupby(...).ngroups`, `.sum()`, `.mean()` are all pure math operations, with nothing to do with randomness, multi-threaded sort order, timezones, or other "invisible variables" — this is exactly what reproducible research is chasing: eliminating anything that could make "the same code, the same data" produce different results across two runs.

<!-- video: ch13_04_data_summary_contract -->
<!-- /video -->

### Step 3 — Seed Determinism: Even Randomness Needs to Be "Randomly Consistent"

The previous step used no randomness at all, since reading data and computing means are both deterministic operations. But the moment "randomness" shows up in an analysis — like `train_test_split` when training a model in Ch10, `torch.manual_seed` in Ch11, or any `np.random` sampling — failing to fix the seed means every run is a different experiment. Below, a minimal example proves it: **the same seed → the same random numbers; no seed set → different every time**.

```python
import numpy as np

def sample(seed=None):
    rng = np.random.default_rng(seed)
    return rng.integers(0, 100, 5)


print("seed=42, run 1:", sample(42))
print("seed=42, run 2:", sample(42), "-> exactly the same (reproducible)")
print("no seed set   :", sample(), "-> different every time (not reproducible)")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `rng = np.random.default_rng(seed)` | Creates an independent random number generator; the same `seed` always produces the same sequence of random numbers |
> | `rng.integers(0, 100, 5)` | Draws 5 integers between 0-99, simulating any "random sampling" action |
> | Calling `sample(42)` twice | Runs with the same seed twice, to verify whether the output comes out identical |
> | `sample()` (no seed given) | Lets the random number generator seed itself from system entropy, so every run differs |

> 🎲 **This is exactly why Ch10's `train_test_split(..., random_state=42)` and Ch11's `torch.manual_seed(42)` both fix the seed by hand** — without a fixed seed, the model's train/test split and weight initialization would differ every run, and the same code would produce a different accuracy on two runs, making it look like the code is broken when really someone just forgot to fix the randomness.

<!-- video: ch13_05_seed_determinism -->
<!-- /video -->

### Step 4 — Schema Contract: Catching Data Changes Before They Break You

Being reproducible isn't just "it reruns this time" — it also has to guarantee "it'll still be the same data structure the next time it runs." If the health department's system renames a column, `clinical_severity` picks up a new category, or `age` picks up negative values, every downstream analysis will quietly compute the wrong thing without ever throwing an error. Below, the raw data is read again, and `assert` statements spell out explicitly "what I'm assuming about this data" — required columns must exist, category values must fall within a known range, numeric values must be sane — and if any one of them fails, execution stops immediately instead of letting bad data quietly flow into Step 2's summary.

```python
raw = pd.read_csv(path)  # Read the raw data again, independent of any transformations done in earlier steps

REQUIRED_COLUMNS = {
    "case_id", "age", "sex", "floor", "wing", "room",
    "clinical_severity", "outcome",
    "symptom_onset_date", "hospitalized", "lab_confirmed",
}
VALID_SEVERITY = {"not_ill", "asymptomatic", "mild", "moderate", "severe"}
VALID_OUTCOME = {"survived", "dead"}

missing_cols = REQUIRED_COLUMNS - set(raw.columns)
assert not missing_cols, f"Missing required columns: {missing_cols}"

unexpected_severity = set(raw["clinical_severity"].dropna().unique()) - VALID_SEVERITY
assert not unexpected_severity, f"clinical_severity has unexpected categories: {unexpected_severity}"

unexpected_outcome = set(raw["outcome"].dropna().unique()) - VALID_OUTCOME
assert not unexpected_outcome, f"outcome has unexpected categories: {unexpected_outcome}"

assert pd.api.types.is_numeric_dtype(raw["age"]), "age column should be numeric dtype"
assert raw["age"].between(0, 120).all(), "age has unreasonable values (outside 0-120)"

print("✅ schema OK - columns, dtypes, and value ranges all as expected")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `REQUIRED_COLUMNS = {...}` | Lists the required columns this analysis depends on, as the first clause of the contract |
> | `missing_cols = REQUIRED_COLUMNS - set(raw.columns)` | Uses a set difference to find missing columns, listing all of them at once instead of checking one by one |
> | `assert not missing_cols, f"..."` | Stops immediately if columns are missing, with an error message that tells you exactly which ones |
> | `set(raw["clinical_severity"].dropna().unique()) - VALID_SEVERITY` | Checks whether a category value has "escaped" the known range with a new, unrecognized category |
> | `raw["age"].between(0, 120).all()` | Checks whether a numeric column has any value outside a reasonable range (e.g., negative, or an extra zero typed in) |

> 🧭 This kind of check is called a **schema contract** (data column contract) or data validation in the data science world — production projects often automate it with packages like `pandera` or `great_expectations` and wire it into the pipeline. Here, plain `assert` statements demonstrate the core idea, and the point is to **catch upstream data changes early**: assume the data might break, and write assertions to confirm it hasn't — rather than waiting until the analysis results look weird before going back to hunt for the data problem.

---

<!-- video: ch13_06_schema_contract -->
<!-- /video -->

## Reproducibility Checklist

1. Is there a `uv.lock`, and can `uv sync && uv run pytest` run from a clean environment?
2. Is there a fixed data column contract (schema contract / line list schema) that immediately gets caught by an `assert` the moment the data changes?
3. Is there a minimal rerunnable script (e.g., `run_sitrep.py`) that goes from data to report with a single command?
4. Are all random steps seeded (`np.random.default_rng(seed)`, `random_state=`, `torch.manual_seed()`)?
5. Are all data transformations written into code, rather than manually edited values in a notebook?
6. Does the result leave behind a "one true answer" (e.g., saved as `summary.csv` / `summary.json`) for diffing against the next rerun?
7. Is the execution environment's version information recorded (Python, pandas, numpy version numbers) for troubleshooting comparisons?

## Exercises

- Exercise version: [`13_reproducibility_exercise.ipynb`](exercises/13_reproducibility_exercise.ipynb)
- Solution version (instructor): [`13_reproducibility_solution.ipynb`](solutions/13_reproducibility_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/13_reproducibility_solution.ipynb>)

## Common Misuses

| Mistake | Correct approach |
|------|----------|
| Manually editing data in a notebook without recording it | Write all transformations in code — the logic for changing data is itself documentation |
| Sharing only the result figures, not the code | Include rerunnable code and version information so others can verify it themselves |
| Not pinning package versions | Pin the environment with `uv.lock`; `uv sync` installs everything in one shot |
| Random seed not fixed | Set `random_state=`, `np.random.default_rng(seed)`, or `torch.manual_seed()` |
| No data contract, so nobody notices when columns change | Write a schema contract with `assert` (or a package like `pandera`) so the data raises an error the moment it changes |
| Keeping only the "final result" in your head, relying on memory for the steps in between | Write the summary and version information into files (CSV/JSON) for diffing later |
| Manually installing packages with `pip install`, overriding the versions `uv.lock` pinned | Always install with `uv sync`; never manually install packages outside the locked environment |
| Only tested on your own machine, never verified it runs in a clean environment | CI (`.github/workflows/ci.yml`) only passes once `uv sync && uv run pytest` succeeds in a clean environment |

## Next Step

This chapter broke "reproducibility" down into four ingredients you need on hand — code, data, environment, seed — and added the schema contract as an extra line of defense, making sure a change in data structure gets caught immediately.
In the next chapter (Ch14), we integrate every skill into one **complete real-world case study** → an outbreak investigation SitRep.
