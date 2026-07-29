# 02 Data Wrangling and Visualization (Python From Scratch)

## Scenario

It's the third day since the Legionnaires' disease outbreak at Pine and Cypress Nursing Home. The investigation team has already compiled a **280-row × 32-column** line list of cases. Your job: read this CSV into Python, verify the data quality, build derived variables for analysis, and then use charts to show the outbreak's time trend, spatial distribution, and demographic features.

## What You'll Learn

- Use `pandas` to read and inspect the structure of a line list
- Convert date columns and handle missing values
- Build derived variables (age group, comorbidity count, days from onset to hospitalization, epi week)
- Use `groupby` for grouped statistics
- Use `matplotlib` to draw an epidemic curve
- Use `seaborn` to draw statistical comparison charts
- Use `plotly` to draw interactive charts

## Prerequisites (For Absolute Beginners)

You only need to grasp these to get started with this chapter:

1. `pd.read_csv(...)`: read data
2. `df.info()` / `df.describe()`: inspect data structure
3. `pd.to_datetime(...)`: date conversion
4. `groupby(...).size()` / `.mean()`: grouped statistics
5. `plt.bar(...)` / `sns.barplot(...)` / `px.bar(...)`: various charts

> 💡 If you've just come from Ch01b, congratulations! You already know `import`, `type()`, `for` loops, and `try/except`. All that's left is to learn the pandas syntax.
>
> 📄 **pandas cheat sheet**: We recommend printing this one-page PDF and keeping it handy—[Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

### What Is pandas? What Is a DataFrame?

**pandas** is Python's most widely used data-processing package. You can think of it as "Excel for Python," but far more powerful and reproducible.

pandas has two core objects:

- **DataFrame**: a two-dimensional table with rows and columns—just like an Excel worksheet
- **Series**: a one-dimensional column—just like a single row or column in Excel

```python
import pandas as pd

# Read the CSV → get a DataFrame
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# df is a table: 280 rows (each row = one resident) × 32 columns (each column = one variable)
# Pull out a single column → get a Series
ages = df["age"]        # the ages of all 280 residents — that's a Series
```

**DataFrame concepts you need to remember:**

| Concept | Excel equivalent | pandas syntax |
|------|-----------|------------|
| A whole table | The entire worksheet | `df` (DataFrame) |
| One record | A single row | `df.iloc[0]` (first row) |
| One field | A single column | `df["age"]` (Series) |
| A single cell | A1 | `df.loc[0, "age"]` |
| Filtering | AutoFilter | `df[df["age"] > 80]` |
| Number of columns | Look at the top letters | `df.shape[1]` |
| Number of records | Look at the left-side numbers | `df.shape[0]` or `len(df)` |

```{figure} images/pandas_dataframe_anatomy_en.svg
:name: pandas-dataframe-anatomy
:alt: DataFrame anatomy diagram: the structure of rows and columns, the difference between a Series and a DataFrame, and four value-access methods
:width: 100%

DataFrame anatomy: a table is made of rows and columns. Take one column and you get a Series (1D); take multiple columns and you still have a DataFrame (2D). Remember the four access patterns—`df["col"]`, `df.iloc[0]`, `df.loc[0, "col"]`, `df[condition]`—and you can solve 80% of your problems.
```

## Choosing a Visualization Package

| Package | Best for | Strength |
|------|---------|------|
| `matplotlib` | Formal report figures, full control over details | Most fundamental, most flexible |
| `seaborn` | Statistical charts (distributions, comparisons, relationships) | Attractive by default, concise syntax |
| `plotly` | Interactive exploration, presentations | Hover with the mouse to read values |

## Common Epi Charts at a Glance

| Analysis need | Recommended chart |
|---------|---------|
| Outbreak change over time | Epidemic curve, line chart |
| Comparison across areas/wings | Bar chart, sorted bar chart |
| Distribution of age or a metric | Histogram, box plot |
| Time × area intensity | Heatmap |
| Interactive exploration and presentation | Plotly interactive chart |

---

## Part 1: Data Wrangling

### Step 1: Read In the Line List

<!-- video: ch02_01_dataframe -->
<!-- /video -->

```python
import pandas as pd

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
print(f"Data dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
df.head()
```

> **Line by line:**
> - `import pandas as pd`: import the pandas package under the nickname `pd` (a worldwide convention)
> - `pd.read_csv(...)`: read a CSV file and return a **DataFrame** (a table)
> - `df.shape`: returns a `(n_rows, n_cols)` tuple; `df.shape[0]` is the row count and `df.shape[1]` is the column count
> - `df.head()`: shows the first 5 rows (you can pass a number, e.g. `df.head(10)` for the first 10)

### Step 2: Inspect the Data Structure

<!-- video: ch02_02_data_inspect -->
<!-- /video -->

The first thing to do with new data: figure out "what it looks like."

```python
df.info()
```

> **`df.info()` tells you:**
> - The total number of rows and columns
> - The **name** and **type** of each column (`int64` integer, `float64` float, `object` text, `bool` boolean)
> - How many **non-null values** each column has—if a column has only 121 non-null values (instead of 280), it has missing data
>
> 💡 The `object` type usually means "text"—date columns are also read in as `object` and need to be manually converted to `datetime`.

```python
df.describe()
```

> **`df.describe()` tells you:**
> - `count`: number of non-null values
> - `mean`: the mean, `std`: standard deviation
> - `min`: minimum, `max`: maximum
> - `25%`, `50%`, `75%`: quartiles
>
> Key thing to check: are the age `min` and `max` reasonable? Any anomalies like -1 or 999?

### Step 3: Date Conversion

<!-- video: ch02_03_datetime -->
<!-- /video -->

The line list has 5 date columns, and when read in they're all **text (object)**—Python doesn't know they're dates. You have to manually convert them to the `datetime` type before you can sort by time, subtract dates, extract months, and so on.

```python
date_cols = [
    "facility_admission_date",
    "symptom_onset_date",
    "hospitalization_date",
    "death_date",
    "notification_date",
]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")
```

> **Line by line:**
> - `pd.to_datetime(df[col])`: convert text-type dates (e.g. `"2026-01-15"`) into pandas **datetime64** objects
> - `errors="coerce"`: if it hits a value it can't convert (blanks, `"N/A"`, etc.), don't raise an error—turn it into **NaT** (Not a Time, the date version of a missing value)
> - `df[col] = ...`: store the converted result back into the original column, overwriting the old text values
>
> **What can you do after converting?**

```python
# Subtract dates → get a number of days
delay = df["hospitalization_date"] - df["symptom_onset_date"]
print(delay.head())  # shows e.g. "3 days", "2 days"...

# Extract the "month" or "day of week"
print(df["symptom_onset_date"].dt.month.head())   # 1 (January)
print(df["symptom_onset_date"].dt.day_name().head())  # "Thursday"
```

> 💡 **What is `.dt`?** It's pandas's "datetime accessor." When a Series is of datetime type, you can use `.dt` to pull out the parts of a date: `.dt.year`, `.dt.month`, `.dt.day`, `.dt.days` (day difference), `.dt.isocalendar().week` (ISO week).

### Step 4: Build Derived Variables

<!-- video: ch02_04_derived -->
<!-- /video -->

Outbreak analysis often requires **deriving new variables** from the raw data—that is, computing new columns from existing ones. The syntax is simple: `df["new_column_name"] = formula`.

#### 4a) Age group — use `pd.cut()` to bin continuous numbers

```python
df["age_group"] = pd.cut(
    df["age"],
    bins=[59, 69, 79, 89, 100],
    labels=["60-69", "70-79", "80-89", "90+"],
)
```

> **What does `pd.cut()` do?** It "cuts" continuous age values into groups, just like turning exam scores into A/B/C/D grades.
>
> | Parameter | Meaning | Example |
> |------|------|------|
> | `df["age"]` | The column to bin | 72, 85, 68, 91... |
> | `bins=[59, 69, 79, 89, 100]` | Cut points (left-open, right-closed) | (59,69], (69,79], (79,89], (89,100] |
> | `labels=["60-69", ...]` | The label for each group | 72 → "70-79", 91 → "90+" |
>
> 💡 Why do the bins start at 59 rather than 60? Because `pd.cut()` is **left-open, right-closed** by default: `(59, 69]` means ages 60–69.

#### 4b) Comorbidity count — sum across columns with `sum(axis=1)`

```python
comorbidity_cols = [
    "comorbidity_chf", "comorbidity_dm",
    "comorbidity_cancer", "comorbidity_copd",
    "immunosuppressed",
]
df["n_comorbidities"] = df[comorbidity_cols].sum(axis=1)
```

> **What is `axis=1`?** This is one of the most confusing concepts in pandas.
>
> | Parameter | Direction | Meaning | Analogy |
> |------|------|------|------|
> | `axis=0` | ↓ downward | Operate on each **column** (aggregate across rows) | Class average for each subject |
> | `axis=1` | → rightward | Operate on each **row** (aggregate across columns) | Each student's total score |
>
> Here we want to count how many comorbidities each resident has, so we sum "across columns (axis=1)" over those 5 columns of 0/1 values.

```{figure} images/pandas_axis_0_vs_1_en.svg
:name: pandas-axis-0-vs-1
:alt: axis=0 vs axis=1: a vertical arrow represents axis=0 (one result per column), a horizontal arrow represents axis=1 (one result per row)
:width: 100%

The `axis=0` arrow points ↓ (top to bottom), giving one result "per column" (e.g. the average of each subject); the `axis=1` arrow points → (left to right), giving one result "per row" (e.g. each person's comorbidity count). Mnemonic: "`axis=N` means the axis=N dimension of the result shape gets collapsed."
```

#### 4c) Infection flag — boolean operation + `astype(int)`

```python
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
```

> **Breaking down this line:**
> 1. `df["clinical_severity"] != "not_ill"` → produces a True/False Series (True for infected people)
> 2. `.astype(int)` → converts True to 1 and False to 0
>
> This is called **Boolean indexing**, the most common way to filter in pandas.

#### 4d) Days from onset to hospitalization — date subtraction + `.dt.days`

```python
df["onset_to_hosp_days"] = (
    df["hospitalization_date"] - df["symptom_onset_date"]
).dt.days
```

> **Breaking it down:** subtracting two datetime columns → gives a timedelta (a time difference); use `.dt.days` to extract the integer number of days.
> For example: `2026-01-18` minus `2026-01-15` = `3 days` → `.dt.days` = `3`

#### 4e) Epi week — ISO week number

```python
df["epi_week"] = df["symptom_onset_date"].dt.isocalendar().week
```

> **What is the ISO week number?** The ISO 8601 standard week number (1–53), often used in outbreak investigations to build "weekly" statistics. `.dt.isocalendar()` returns three columns—year, week, and day of week—and we take only `.week`.

### Step 5: Handle Missing Values

<!-- video: ch02_05_missing -->
<!-- /video -->

People who weren't infected won't have a `symptom_onset_date`, `hospitalization_date`, and so on—these blanks aren't data errors, they're **structural missingness**: if you never got sick, of course you have no onset date.

> **Types of missing values:**
>
> | Type | Appears in | Represents |
> |------|--------|------|
> | `NaN` | Numeric columns | A missing number (Not a Number) |
> | `NaT` | Date columns | A missing date (Not a Time) |
> | `None` | Text columns | Missing text |

```python
# See how many missing values each column has
print(df.isnull().sum())
```

> **`df.isnull()`** returns a same-sized True/False table (blank = True); then `.sum()` counts how many Trues are in each column.

```python
# Verify: onset dates for non-infected people should all be empty
print("Number of non-infected people with an onset date:",
      df.loc[df["infected"] == 0, "symptom_onset_date"].notna().sum())
```

> **Explaining the `.loc[row_condition, column_name]` syntax:**
> - `df.loc[df["infected"] == 0, "symptom_onset_date"]`
>   - The first part `df["infected"] == 0` → filters the non-infected rows
>   - The second part `"symptom_onset_date"` → looks only at the onset-date column
> - `.notna()` → True/False (has a value = True)
> - `.sum()` → adds up the number of Trues
> - If the result is 0, the structural missingness is fine

### Step 6: Grouped Statistics With groupby

<!-- video: ch02_06_groupby -->
<!-- /video -->

**What is `groupby`?** Imagine building a Pivot Table in Excel: first choose "which column to group by," then compute something for each group (count, sum, average, etc.). That's exactly what pandas's `groupby` does.

```
                   ┌─ 1A group ──→ compute attack rate
df ──→ groupby ──→ ├─ 1B group ──→ compute attack rate
      (floor,wing) ├─ 2A group ──→ compute attack rate
                   ├─ 2B group ──→ compute attack rate
                   ├─ 3A group ──→ compute attack rate
                   └─ 3B group ──→ compute attack rate
```

```python
# Compute attack rate by floor × wing
wing_stats = (
    df.groupby(["floor", "wing"])
    .agg(residents=("case_id", "size"), infected=("infected", "sum"))
    .reset_index()
)
wing_stats["attack_rate"] = wing_stats["infected"] / wing_stats["residents"]
wing_stats["attack_rate_pct"] = (wing_stats["attack_rate"] * 100).round(1)
print(wing_stats.to_string(index=False))
```

> **Line by line:**
>
> | Code | What it does |
> |--------|---------|
> | `df.groupby(["floor", "wing"])` | Splits into 6 groups by floor + wing |
> | `.agg(residents=("case_id", "size"))` | For each group, counts the rows (= number of residents), named `residents` |
> | `.agg(infected=("infected", "sum"))` | For each group, sums the `infected` column (= number infected) |
> | `.reset_index()` | Converts the grouped result from a "multi-level index" back to an ordinary table |
> | `wing_stats["attack_rate"] = ...` | Adds an attack-rate column |
> | `.round(1)` | Rounds to one decimal place |
>
> **`.agg()` syntax cheat sheet:**
> ```python
> .agg(
>     new_column_name = ("source_column", "aggregation_function")
> )
> ```
> Common aggregation functions: `"size"` count, `"sum"` sum, `"mean"` average, `"max"` maximum, `"min"` minimum

### Step 6b: Advanced Data Operations—Essentials for Excel Users

Once you've learned `groupby`, you can already do basic grouped statistics. But in real outbreak investigations you'll also need the techniques below. These are the questions Excel users most often ask when moving to pandas.

> 📄 **Official cheat sheet**: pandas provides an official one-page cheat sheet PDF—we recommend printing it and keeping it handy: [Pandas Cheat Sheet (PDF)](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

#### Frequency tables: `value_counts()` — your first summary table

<!-- video: ch02_09_value_counts -->
<!-- /video -->

The first step in an outbreak investigation is usually to look at the frequency distribution of each column. `value_counts()` is the `COUNTIF` of Excel.

```python
# Clinical severity distribution
print(df["clinical_severity"].value_counts())

# Add percentages
print(df["clinical_severity"].value_counts(normalize=True).round(3) * 100)
```

> **Common parameters:**
>
> | Parameter | Effect |
> |------|------|
> | `normalize=True` | Show proportions instead of counts |
> | `sort=False` | Don't sort by count; keep the original order |
> | `dropna=False` | Include missing values in the count |

#### Pivot tables: `pivot_table()` — Excel's favorite feature

<!-- video: ch02_10_pivot_table -->
<!-- /video -->

If you often use Pivot Tables in Excel, `pd.pivot_table()` is the Python version.

```python
# Excel Pivot Table: columns = floor, rows = wing, values = attack rate
pivot = pd.pivot_table(
    df,
    values="infected",       # the column to compute
    index="wing",            # row labels (Excel's "Rows" area)
    columns="floor",         # column labels (Excel's "Columns" area)
    aggfunc="mean",          # aggregation function: mean = attack rate
)
print((pivot * 100).round(1))  # convert to percentages
```

> **`pivot_table` vs `groupby`?**
>
> | Situation | Which to use |
> |------|--------|
> | Single grouping + one statistic | `groupby` is more concise |
> | Two dimensions crossed + need a table output | `pivot_table` is more intuitive |
> | Need subtotals (margins) | `pivot_table(margins=True)` |
>
> ```python
> # Add a subtotal row and column (Excel's "Grand Total")
> pivot_with_totals = pd.pivot_table(
>     df, values="infected", index="wing", columns="floor",
>     aggfunc="mean", margins=True, margins_name="Total",
> )
> print((pivot_with_totals * 100).round(1))
> ```

#### Cross-tabulation: `pd.crosstab()` — a shortcut for 2×2 tables

Ch03 will use `crosstab` heavily to build 2×2 contingency tables. Let's get to know it here first:

```python
# Cross-tabulation of sex × infection status
print(pd.crosstab(df["sex"], df["infected"], margins=True))
```

> `crosstab` and `pivot_table` are very similar. The difference: `crosstab` takes two Series directly and counts by default; `pivot_table` takes a DataFrame and requires you to specify `aggfunc`.

#### Three ways to add a column

```python
# Method 1: direct assignment (you already know this)
df["bmi_category"] = pd.cut(df["age"], bins=[0, 70, 80, 100], labels=["<70", "70-80", "80+"])

# Method 2: use assign()—good for method chaining (see the next section)
df = df.assign(
    is_elderly = df["age"] >= 80,
    has_comorbidity = df["n_comorbidities"] > 0,
)

# Method 3: use apply()—when you need complex logic
def classify_risk(row):
    if row["age"] >= 80 and row["n_comorbidities"] >= 2:
        return "high"
    elif row["age"] >= 70 or row["n_comorbidities"] >= 1:
        return "medium"
    return "low"

df["risk_level"] = df.apply(classify_risk, axis=1)
print(df["risk_level"].value_counts())
```

> **When should you use which?**
>
> | Method | Best for | Speed |
> |------|---------|------|
> | `df["new"] = ...` | Simple operations (arithmetic, comparisons) | Fastest |
> | `.assign()` | Chaining several steps together (method chaining) | Fast |
> | `.apply(func, axis=1)` | When you need if/else logic or cross-column logic | Slower (computed row by row) |

#### Method Chaining — modern pandas style

<!-- video: ch02_11_method_chaining -->
<!-- /video -->

The traditional style breaks each step apart, producing many temporary variables along the way. **Method chaining** links multiple operations into a single pipeline, which is more readable:

```{figure} images/pandas_method_chaining_en.svg
:name: pandas-method-chaining
:alt: Method chaining pipeline: each `.` represents a processing station, and the table changes shape between stations
:width: 100%

Method chaining = a factory assembly line. Each `.` is a processing station (`.query()` filters, `.groupby()` splits into piles, `.size()` counts, `.reset_index()` restores), and the data changes shape between stations (DataFrame → GroupBy object → Series → DataFrame). When you're lost, `print(type(...))` first to confirm the output type of each step.
```

```python
# Traditional style (lots of temporary variables)
cases = df[df["infected"] == 1]
cases = cases[cases["age"] >= 70]
result = cases.groupby("floor").size()
result = result.reset_index(name="n_cases")
result = result.sort_values("n_cases", ascending=False)
print(result)

# Method chaining (all in one go)
result = (
    df
    .query("infected == 1 and age >= 70")     # filter (replaces boolean indexing)
    .groupby("floor")
    .size()
    .reset_index(name="n_cases")
    .sort_values("n_cases", ascending=False)
)
print(result)
```

> **Key points of `.query()` syntax:**
> - Write conditions as a string, using `and` / `or` / `not` instead of `&` / `|` / `~`
> - Column names don't need quotes (unless the name has spaces or special characters)
> - You can reference external variables: `df.query("age > @threshold")`
>
> **A more complex chaining example:**
>
> ```python
> summary = (
>     df
>     .assign(age_group=pd.cut(df["age"], bins=[59, 69, 79, 89, 100],
>                              labels=["60-69", "70-79", "80-89", "90+"]))
>     .groupby("age_group", observed=True)
>     .agg(
>         n_residents=("case_id", "size"),
>         n_infected=("infected", "sum"),
>         n_dead=("outcome", lambda x: (x == "dead").sum()),
>     )
>     .assign(
>         attack_rate=lambda d: (d["n_infected"] / d["n_residents"] * 100).round(1),
>         cfr=lambda d: (d["n_dead"] / d["n_infected"] * 100).round(1),
>     )
> )
> print(summary)
> ```

#### Joining tables: `merge()` — the most common need in outbreak work

<!-- video: ch02_12_merge -->
<!-- /video -->

In real outbreak work, the line list, lab results, and environmental-sample data often live in different files. `merge()` is Excel's `VLOOKUP`, but more powerful.

```python
# Suppose there are two tables: a line list and lab results
cases_df = df[["case_id", "age", "sex", "infected"]].head(10)
lab_df = pd.DataFrame({
    "case_id": [1, 2, 3, 5, 8],
    "lab_method": ["culture", "PCR", "culture", "PCR", "culture"],
    "ct_value": [25.3, 28.1, 22.5, 31.0, 24.8],
})

# Merge (using case_id as the key)
merged = pd.merge(cases_df, lab_df, on="case_id", how="left")
print(merged)
```

> **The `how` parameter—four types of join:**
>
> | `how` | Behavior | Excel equivalent |
> |-------|------|-----------|
> | `"left"` | Keep all rows from the left table | VLOOKUP (no match = blank) |
> | `"right"` | Keep all rows from the right table | Reverse VLOOKUP |
> | `"inner"` | Keep only rows present in both | VLOOKUP then delete blank rows |
> | `"outer"` | Keep all rows from both | Full merge |
>
> 💡 Outbreak work most often uses `"left"`: treat the line list as the main table and "fill in" the lab results.

#### Text cleaning: the `.str` accessor

<!-- video: ch02_13_str_cleanup -->
<!-- /video -->

```python
# Clean the wing column: standardize the case
df["wing_clean"] = df["wing"].str.upper()

# Check whether a column contains specific text
severe_mask = df["clinical_severity"].str.contains("severe", na=False)
print(f"Number of rows containing 'severe': {severe_mask.sum()}")
```

> **Common `.str` methods:**
>
> | Method | Effect |
> |------|------|
> | `.str.upper()` / `.str.lower()` | Uppercase / lowercase |
> | `.str.strip()` | Remove leading/trailing whitespace |
> | `.str.contains("pattern")` | Whether it contains specific text (returns True/False) |
> | `.str.replace("old", "new")` | Replace text |
> | `.str.split("_")` | Split by a delimiter |
> | `.str.len()` | Text length |

#### Deduplication and ranking

```python
# Remove duplicate reports (based on case_id)
df_unique = df.drop_duplicates(subset="case_id", keep="first")

# Rename a column
df_renamed = df.rename(columns={"symptom_onset_date": "onset_date"})

# Find the top 3 wings with the highest attack rate
print(wing_stats.nlargest(3, "attack_rate_pct"))
```

---

## Part 2: Visualization

### matplotlib's `fig, ax` Pattern—Don't Be Scared When You See It

Before you look at the code below, get one thing straight: matplotlib has two styles.

**The simple style (good for quick exploration):**
```python
import matplotlib.pyplot as plt
plt.bar(["A", "B", "C"], [10, 20, 15])
plt.title("My Chart")
plt.show()
```

**The professional style (used in this material):**
```python
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(["A", "B", "C"], [10, 20, 15])
ax.set_title("My Chart")
plt.show()
```

Both styles give the same result, but the professional style is more flexible. **You just need to remember this formula:**

```
fig, ax = plt.subplots()     # fig = the whole canvas, ax = one drawing panel on the canvas
ax.bar(...)                   # draw on the panel (change plt.bar to ax.bar)
ax.set_title(...)             # set the title (change plt.title to ax.set_title)
ax.set_xlabel(...)            # set the X-axis label
ax.set_ylabel(...)            # set the Y-axis label
plt.tight_layout()            # auto-adjust margins so text isn't clipped
plt.show()                    # display the chart
```

> 💡 **Why use `fig, ax`?** Because later you'll need to draw multiple subplots on the same canvas (like two epidemic curves stacked for comparison), and only the `fig, ax` style can do that. Get used to this pattern now and you'll thank yourself later.

```{figure} images/matplotlib_fig_ax_anatomy_en.svg
:name: matplotlib-fig-ax
:alt: matplotlib anatomy diagram: the Figure is the outer canvas, the Axes is the actual drawing panel, with the functions that correspond to each component
:width: 100%

**fig (Figure) = the whole canvas** (blue dashed outer frame); **ax (Axes) = the drawing panel** (orange solid inner frame, containing the axes, gridlines, and title). Remember the formula: change `plt.bar` to `ax.bar`, and change `plt.title/xlabel/ylabel` to `ax.set_title/set_xlabel/set_ylabel` (add a `set_`) and you're good.
```

### Differences Between the Three Plotting Tools

| Feature | matplotlib | seaborn | plotly |
|------|-----------|---------|--------|
| **Positioning** | Low-level engine, can draw anything | A high-level wrapper over matplotlib | Interactive charting engine |
| **Syntax** | Set every element manually | Statistical charts in one line | Interactive charts in one line |
| **Interactivity** | Static images | Static images | Hover, zoom, click |
| **Journal submission** | ✅ First choice (full control) | ✅ Works (built on matplotlib) | ⚠️ Need to export a static image |
| **Best for** | Precise control, customization | Statistical charts (distributions, comparisons) | Presentations, interactive dashboards |
| **Learning curve** | Steepest 😰 | Flattest 😊 | Medium |

**Easy way to remember:**
- **matplotlib** = building a house from scratch yourself (tiring but completely free)
- **seaborn** = a pre-built home (a designer set it up for you; a little redecorating is all you need)
- **plotly** = a smart home (lots of interactive features, but hard to change the interior)

### Step 7: Epidemic Curve (matplotlib)

<!-- video: ch02_07_epicurve -->
<!-- /video -->

The epidemic curve is the most iconic chart in epidemiology—the X-axis is the date of symptom onset and the Y-axis is the number of new cases. The shape of the curve lets you infer the mode of transmission.

```{admonition} Epidemic curve drawing standards (per CDC / ECDC guidance)
:class: important

An epidemic curve is essentially a **histogram**, not an ordinary bar chart. Below are drawing standards compiled from the [CDC Epi Chart](https://www.cdc.gov/wcms/4.0/cdc-wp/data-presentation/epi-chart.html) and the [CDC Field Epidemiology Manual](https://www.cdc.gov/field-epi-manual/php/chapters/describing-epi-data.html):

**Structure and proportion**
1. **No gaps between adjacent bars**: the X-axis is a continuous time axis, so there should be no space between bars, to faithfully reflect the continuity of time.
2. **Fill in dates with no cases**: even if a day has 0 new cases, it should still occupy its position on the X-axis, otherwise the spacing is distorted.
3. **No Y-axis scale break**: the Y-axis must start at 0 and must not be truncated, otherwise the trend is exaggerated or minimized.
4. **Show the pre- and post-outbreak background period**: the X-axis should include dates 1–2 incubation periods before the outbreak began, so readers can see when the outbreak started to deviate from baseline.

**Time interval**
5. **Time interval ≈ 1/4 of the incubation period**: Legionnaires' disease has an incubation period of 2–10 days (average 5–6 days), so a 1-day unit is appropriate. When there are many cases you can shorten the interval; when there are few you can lengthen it.

**Title and labels**
6. **The title should be self-contained**: include the disease name, location, and time range, e.g. "Pine and Cypress Nursing Home Legionnaires' disease epidemic curve, by date of symptom onset, January 2026."
7. **X-axis**: label it "Date of Symptom Onset"—clearly state the time basis. If you use a surrogate date such as the report date, note it below the chart.
8. **Y-axis**: label it "Number of Cases," and it must use integer tick marks.

**Visual style**
9. **Hide gridlines**: CDC recommends hiding horizontal and vertical gridlines to reduce chart clutter.
10. **Remove unnecessary borders**: remove the top and right `spines`.
11. **Distinguish case classification by color**: if you show both confirmed and probable cases, distinguish them with different colors and include a legend.
12. **Don't label numbers on the bars**: ECDC guidance recommends not presenting digital (numeric) and analog (graphical) information at the same time, to avoid interference.

**Annotation**
13. **Add key-event annotations**: annotating important events (exposure time, interventions, report date) on the epidemic curve helps explain the reasons behind the case distribution.
```

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -- Global chart style settings --
plt.style.use("ggplot")                 # academic style: light gray background + white gridlines
plt.rcParams["figure.dpi"] = 150        # increase resolution (the default 100 is too blurry)

# -- CJK font setup (avoid Chinese labels showing as boxes) --
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
```

```{admonition} Chart style and resolution settings
:class: tip, dropdown

**`plt.style.use("ggplot")`** applies the classic style of R's ggplot2—a light gray background with white gridlines, for a more professional look overall. matplotlib has several built-in styles; use `plt.style.available` to see the full list. Common choices:

| Style | Character |
|------|------|
| `ggplot` | R's ggplot2 style, common in academic papers |
| `seaborn-v0_8` | seaborn's default style, soft tones |
| `bmh` | Bayesian Methods for Hackers, clean colors |
| `fivethirtyeight` | The FiveThirtyEight news-site style |
| `default` | matplotlib's original default |

**`plt.rcParams["figure.dpi"] = 150`** raises the image resolution from the default 100 DPI to 150 DPI, for a sharper display in Jupyter Notebook and on the web. For publication quality, set it to 300.

> 💡 `plt.style.use()` changes global settings, so it's best placed at the very top of the notebook. If you only want to apply a style to a single chart, wrap the plotting code in `with plt.style.context("ggplot"):`.
```

```{admonition} Why list so many fonts in the candidate list?
:class: tip, dropdown

matplotlib tries each font name in the `font.sans-serif` list **from left to right** and uses the first one that's installed. Different operating systems ship with different fonts:

- **macOS**: Heiti TC, Arial Unicode MS
- **Windows**: Microsoft JhengHei
- **Linux (Ubuntu)**: after `sudo apt install fonts-noto-cjk`, the Noto Sans CJK family is available

Note in particular: the Noto Sans CJK family is usually installed in `.ttc` (TrueType Collection) format, with five variants (JP/KR/SC/TC/HK) in one file. But matplotlib's `addfont()` **only registers the first variant (usually JP)**, so the candidate list needs to include JP and SC as well—they share the same CJK glyph set and can all display Traditional Chinese.

For detailed troubleshooting steps, see [Ch15 Appendix E. Troubleshooting Chinese Chart Display](15_appendix.md#e-chinese-chart-display-troubleshooting-matplotlib--plotly).
```

#### Standard epidemic curve

```python
cases = df[df["infected"] == 1]
daily = cases.groupby("symptom_onset_date").size().rename("cases")

# Fill in the full date range: include 3 days before the outbreak (to show the background period)
date_range = pd.date_range(
    daily.index.min() - pd.Timedelta(days=3),
    daily.index.max() + pd.Timedelta(days=1),
    freq="D",
)
daily = daily.reindex(date_range, fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(
    daily.index, daily.values,
    width=1.0,                         # adjacent bars sit flush together (histogram style)
    color="#2c7fb8", edgecolor="white", linewidth=0.5,
)
ax.set_title(
    "Pine and Cypress Nursing Home Legionnaires' Disease Epidemic Curve, by Date of Symptom Onset, January 2026",
    fontsize=13, fontweight="bold",
)
ax.set_xlabel("Date of Symptom Onset")
ax.set_ylabel("Number of Cases")

# Date formatting
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)

# X-axis hugs the data range; Y-axis starts at 0 with integer ticks
ax.set_xlim(daily.index.min() - pd.Timedelta(hours=12),
            daily.index.max() + pd.Timedelta(hours=12))
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

# CDC style: hide gridlines, remove top and right spines
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
```

**Interpretation**: the peak is concentrated within a few days → a point-source (common exposure) pattern. There are no cases in the 3 days before the outbreak (01/09–01/11), showing a clear onset point for the outbreak.

#### Stratify by case classification (confirmed vs. probable)

CDC recommends: if you show cases of different classifications, distinguish them by color. Here we use a stacked bar chart to show confirmed and probable cases separately.

```python
# Compute daily case counts by date × case classification
daily_class = (
    cases.groupby(["symptom_onset_date", "case_classification"])
    .size()
    .unstack(fill_value=0)
)
daily_class = daily_class.reindex(date_range, fill_value=0)

colors = {"confirmed": "#2c7fb8", "probable": "#a6bddb"}
fig, ax = plt.subplots(figsize=(10, 4))

bottom = None
for cls in ["confirmed", "probable"]:
    if cls not in daily_class.columns:
        continue
    ax.bar(
        daily_class.index, daily_class[cls],
        width=1.0, bottom=bottom,
        color=colors[cls], edgecolor="white", linewidth=0.5,
        label="Confirmed" if cls == "confirmed" else "Probable",
    )
    bottom = daily_class[cls] if bottom is None else bottom + daily_class[cls]

ax.set_title(
    "Pine and Cypress Nursing Home Legionnaires' Disease Epidemic Curve, by Case Classification and Date of Symptom Onset, January 2026",
    fontsize=12, fontweight="bold",
)
ax.set_xlabel("Date of Symptom Onset")
ax.set_ylabel("Number of Cases")
ax.legend(loc="upper left", frameon=False)

ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)
ax.set_xlim(daily.index.min() - pd.Timedelta(hours=12),
            daily.index.max() + pd.Timedelta(hours=12))
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
```

#### Add key-event annotations

CDC recommends annotating important events on the epidemic curve to help readers understand the reasons behind the case distribution.

```python
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(
    daily.index, daily.values,
    width=1.0, color="#2c7fb8", edgecolor="white", linewidth=0.5,
)

# Annotate key events
ax.annotate(
    "First case reported",
    xy=(pd.Timestamp("2026-01-14"), daily.get(pd.Timestamp("2026-01-14"), 0)),
    xytext=(pd.Timestamp("2026-01-10"), daily.max() * 0.85),
    fontsize=9,
    arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2),
    bbox=dict(boxstyle="round,pad=0.3", fc="#ffffcc", ec="#cccccc"),
)
ax.annotate(
    "Water system disinfection",
    xy=(pd.Timestamp("2026-01-22"), daily.get(pd.Timestamp("2026-01-22"), 0)),
    xytext=(pd.Timestamp("2026-01-25"), daily.max() * 0.85),
    fontsize=9,
    arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2),
    bbox=dict(boxstyle="round,pad=0.3", fc="#ffffcc", ec="#cccccc"),
)

ax.set_title(
    "Pine and Cypress Nursing Home Legionnaires' Disease Epidemic Curve (with key-event annotations)",
    fontsize=13, fontweight="bold",
)
ax.set_xlabel("Date of Symptom Onset")
ax.set_ylabel("Number of Cases")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)
ax.set_xlim(daily.index.min() - pd.Timedelta(hours=12),
            daily.index.max() + pd.Timedelta(hours=12))
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
```

#### The classic unit-chart epidemic curve (colored by case classification)

The **unit chart (stacked squares)** epidemic curve, common in textbooks and CDC investigation reports—each little square represents one case. Here we use color to distinguish confirmed and probable cases.

```python
# Prepare the daily confirmed / probable case counts
daily_class = (
    cases.groupby(["symptom_onset_date", "case_classification"])
    .size()
    .unstack(fill_value=0)
)
daily_class = daily_class.reindex(date_range, fill_value=0)
colors_map = {"confirmed": "#2c7fb8", "probable": "#a6bddb"}

fig, ax = plt.subplots(figsize=(10, 5))
box_size = 1.0

for date in daily_class.index:
    x = mdates.date2num(date)
    j = 0  # current stacking height
    for cls in ["confirmed", "probable"]:
        count = daily_class.at[date, cls] if cls in daily_class.columns else 0
        for _ in range(int(count)):
            rect = plt.Rectangle(
                (x - box_size / 2, j * box_size),
                box_size, box_size,
                facecolor=colors_map[cls],
                edgecolor="white", linewidth=0.8,
            )
            ax.add_patch(rect)
            j += 1

# Axis settings
ax.set_xlim(mdates.date2num(daily_class.index.min()) - 1.5,
            mdates.date2num(daily_class.index.max()) + 1.5)
y_max = daily_class.sum(axis=1).max()
ax.set_ylim(0, y_max + 1)
ax.set_aspect("equal")

ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

ax.set_title(
    "Pine and Cypress Nursing Home Legionnaires' Disease Epidemic Curve — Unit Chart (by Case Classification)",
    fontsize=13, fontweight="bold",
)
ax.set_xlabel("Date of Symptom Onset")
ax.set_ylabel("Number of Cases")

# Manual legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#2c7fb8", edgecolor="white", label="Confirmed"),
    Patch(facecolor="#a6bddb", edgecolor="white", label="Probable"),
]
ax.legend(handles=legend_elements, loc="upper left", frameon=False)

ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
```

```{tip}
The unit-chart epidemic curve is especially suited to **small clusters** (a few dozen to a hundred-something cases). Each square can use a different color to represent a case attribute (e.g. confirmed / probable, male / female, or floor), letting readers see the time distribution and case composition at once. When there are too many cases (> 200), the squares become too small, and a standard histogram is more appropriate.
```

### Step 8: Age Distribution (seaborn)

<!-- video: ch02_08_seaborn_plotly -->
<!-- /video -->

With seaborn you can draw an attractive statistical chart in one line, without setting every element manually the way you do in matplotlib.

```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(
    data=df, x="age", hue="infected", hue_order=[1, 0], bins=15,
    multiple="stack", palette={1: "#e34a33", 0: "#cccccc"}, ax=ax,
)
ax.set_title("Age Distribution: Infected vs. Not Infected")
ax.set_xlabel("Age")
ax.set_ylabel("Count")
ax.legend(title="Infection", labels=["Infected", "Not infected"])
plt.tight_layout()
plt.show()
```

> **Explaining the `sns.histplot()` parameters:**
>
> | Parameter | Meaning |
> |------|------|
> | `data=df` | Data source (the whole DataFrame) |
> | `x="age"` | Which column to use for the X-axis |
> | `hue="infected"` | Which column to color by |
> | `hue_order=[1, 0]` | Legend order: infected people first |
> | `bins=15` | Split into 15 bins (the number of histogram bars) |
> | `multiple="stack"` | Stack rather than overlay (`"layer"` overlays) |
> | `palette={1: "#e34a33", 0: "#cccccc"}` | Specify the color of each group |
> | `ax=ax` | Which panel to draw on |
>
> 💡 seaborn functions can take a DataFrame + column names directly, without first pulling out the data the way matplotlib requires.

### Step 9: Attack Rate by Wing Bar Chart (seaborn)

> ⚠️ **You can't compare case counts directly!** Wing 1A has 15 infected and wing 3B has 27—so 3B looks worse? Not necessarily! If 1A has only 30 residents while 3B has 47, then the attack rate is the fair basis for comparison.

```python
wing_stats["label"] = wing_stats["floor"].astype(str) + wing_stats["wing"]
wing_stats = wing_stats.sort_values("attack_rate", ascending=False)

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(
    data=wing_stats, x="label", y="attack_rate_pct",
    hue="label", palette="YlOrRd", legend=False, ax=ax,
)
ax.set_title("Attack Rate by Wing")
ax.set_xlabel("Wing")
ax.set_ylabel("Attack Rate (%)")
for i, row in wing_stats.iterrows():
    ax.text(
        list(wing_stats["label"]).index(row["label"]),
        row["attack_rate_pct"] + 1,
        f'{row["attack_rate_pct"]}%',
        ha="center", fontsize=10,
    )
plt.tight_layout()
plt.show()
```

### Step 10: Severity × Comorbidity Heatmap (seaborn)

A heatmap uses **color intensity** to represent magnitude—like a thermometer, the darker the color the larger the value. It's great for seeing the cross-relationship between two variables.

```python
severity_order = ["mild", "moderate", "severe"]
heat_data = (
    cases[cases["clinical_severity"].isin(severity_order)]
    .groupby(["clinical_severity", "n_comorbidities"])
    .size()
    .unstack(fill_value=0)
    .reindex(severity_order)
)

fig, ax = plt.subplots(figsize=(8, 3.5))
sns.heatmap(heat_data, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
# annot=True: show a number in each cell  fmt="d": integer format  cmap: color scheme
ax.set_title("Clinical Severity × Number of Comorbidities")
ax.set_xlabel("Number of Comorbidities")
ax.set_ylabel("Severity")
plt.tight_layout()
plt.show()
```

### Step 11: Interactive Stratified Epidemic Curve (Plotly)

Plotly's biggest advantage is **interactivity**—hover with the mouse to see values, and zoom and pan. It's especially good for presenting investigation results in a slideshow, letting the audience explore the data themselves.

> **Plotly's syntax is completely different from matplotlib's:**
> - matplotlib uses `fig, ax = plt.subplots()` → `ax.bar()`
> - plotly uses `fig = px.bar(data, x=..., y=...)` → `fig.update_layout()`
> - Plotly doesn't need `plt.show()`; use `fig.show()` directly

Plotly's interactive charts must follow the same CDC epidemic-curve standards: no gaps, a descriptive title, hidden gridlines, and a Y-axis starting at 0.

```python
import plotly.express as px
import plotly.graph_objects as go

# Stratify by floor and fill in the full date range
daily_floor = (
    cases.groupby(["symptom_onset_date", "floor"])
    .size()
    .rename("cases")
    .reset_index()
)
daily_floor["floor"] = daily_floor["floor"].astype(str) + "F"

# Fill in all date × floor combinations (including days with 0 cases)
all_dates = pd.date_range(
    cases["symptom_onset_date"].min() - pd.Timedelta(days=3),
    cases["symptom_onset_date"].max() + pd.Timedelta(days=1),
    freq="D",
)
all_floors = sorted(daily_floor["floor"].unique())
full_idx = pd.MultiIndex.from_product([all_dates, all_floors], names=["symptom_onset_date", "floor"])
daily_floor = (
    daily_floor.set_index(["symptom_onset_date", "floor"])
    .reindex(full_idx, fill_value=0)
    .reset_index()
)

fig = px.bar(
    daily_floor,
    x="symptom_onset_date", y="cases", color="floor",
    barmode="stack",
    color_discrete_sequence=["#2c7fb8", "#41ae76", "#fe9929"],
    title="Pine and Cypress Nursing Home Legionnaires' Disease Epidemic Curve, by Floor and Date of Symptom Onset, January 2026",
    labels={"symptom_onset_date": "Date of Symptom Onset",
            "cases": "Number of Cases",
            "floor": "Floor"},
)

# CDC style: no gaps, hidden gridlines, Y-axis starting at 0
fig.update_layout(
    bargap=0,                              # no gaps between bars
    xaxis=dict(showgrid=False),            # hide vertical gridlines
    yaxis=dict(showgrid=False, rangemode="tozero"),  # hide horizontal gridlines, Y-axis from 0
    plot_bgcolor="white",                  # white background
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
)
fig.show()
```

---

### Step 12: Export Charts—Investigation Reports and Journal Submission

Making a chart and not saving it is a waste. Here's how to export professional-quality charts.

#### Basic export: `savefig()`

```python
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, width=1.0, color="#2c7fb8")
ax.set_title("Epidemic Curve")
ax.set_xlabel("Date of Symptom Onset")
ax.set_ylabel("Number of Cases")
plt.tight_layout()

# Save as PNG (good for reports and presentations)
fig.savefig("epi_curve.png", dpi=300, bbox_inches="tight")

# Save as PDF (good for journal submission; a vector image won't blur)
fig.savefig("epi_curve.pdf", bbox_inches="tight")

# Save as SVG (good for the web; can be edited afterward)
fig.savefig("epi_curve.svg", bbox_inches="tight")
```

> **Parameter notes:**
>
> | Parameter | Meaning | Suggested value |
> |------|------|--------|
> | `dpi=300` | Resolution (pixels per inch) | 150–200 for reports, 300–600 for journal submission |
> | `bbox_inches="tight"` | Auto-crop white margins | Always include |
> | `facecolor="white"` | Background color | Add it when submitting, to avoid a transparent background |
> | `transparent=True` | Transparent background | Use when overlaying a slide on a colored background |

#### Plotly export

```python
# Save as interactive HTML (can be embedded in a web report)
fig.write_html("epi_curve_interactive.html")

# Save as a static PNG (requires the kaleido package)
# uv add kaleido
fig.write_image("epi_curve_plotly.png", scale=2)

# Save as PDF
fig.write_image("epi_curve_plotly.pdf")
```

#### Chart specifications for journal submission

If your investigation report is bound for a journal like NEJM, Lancet, or JAMA, the figure requirements are strict:

```{admonition} Journal-grade chart specifications (NEJM / Lancet / JAMA)
:class: important

**File format**
- **First choice**: PDF or EPS (vector, no loss on enlargement)
- **Acceptable**: TIFF or PNG (raster, needs high DPI)
- **Not accepted**: JPG (compression artifacts, unsuitable for scientific figures)

**Resolution requirements**
- Line art: ≥ 1000 DPI
- Halftone: ≥ 300 DPI
- Combination: ≥ 600 DPI

**Size**
- Single-column width: 8.3 cm (3.27 inch)
- Double-column width: 17.1 cm (6.73 inch)
- Maximum height: 23.4 cm (9.21 inch)

**Fonts**
- Recommended: Arial, Helvetica (sans-serif fonts)
- Text within the figure: 8–10 pt
- Axis labels: no smaller than 6 pt

**Colors**
- Use a colorblind-safe color scheme
- Avoid using red and green together (about 8% of men have red-green color blindness)
- Recommended palette: seaborn's `"colorblind"` palette
```

**A hands-on example—submission-grade chart:**

```python
# An epidemic curve for a Lancet submission
fig, ax = plt.subplots(figsize=(6.73, 3.5))  # double-column width

ax.bar(daily.index, daily.values, width=1.0,
       color="#2c7fb8", edgecolor="white", linewidth=0.3)

# Title and axis labels in English (required by international journals)
ax.set_title("Epidemic curve of Legionnaires' disease outbreak\n"
             "Pine and Cypress Nursing Home, January 2026",
             fontsize=10, fontweight="bold")
ax.set_xlabel("Date of symptom onset", fontsize=9)
ax.set_ylabel("Number of cases", fontsize=9)

# Font size: axis ticks 8 pt
ax.tick_params(labelsize=8)

# Date formatting
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)

ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

# Save as a PDF for submission (vector image)
fig.savefig("Figure1_epi_curve.pdf",
            bbox_inches="tight", facecolor="white")

# Or save as TIFF (required by some journals)
fig.savefig("Figure1_epi_curve.tiff",
            dpi=600, bbox_inches="tight", facecolor="white")
plt.show()
```

> 💡 **Colorblind-safe colors**: use `sns.color_palette("colorblind")` for a default colorblind-safe palette, or pick one at the [ColorBrewer](https://colorbrewer2.org/) website.

---

## Key Points for Interpreting Charts

| Chart | What to look for |
|------|---------|
| Epidemic curve | Peak timing, rate of rise/fall → transmission mode |
| Age distribution | Whether the infected are concentrated in a specific age band |
| Wing bar chart | Which wings have an unusually high attack rate → spatial clues |
| Severity × comorbidity | Whether people with more comorbidities are more prone to severe disease |
| Interactive curve | Whether the epidemic peaks are synchronized across floors |

## pandas Syntax Quick Reference

Beginners can come back to this table anytime. For a more complete version, see the [Pandas Cheat Sheet (PDF)](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf).

**Basic operations**

| Need | Syntax | Notes |
|------|------|------|
| Read a CSV | `pd.read_csv("file.csv")` | Returns a DataFrame |
| See the first N rows | `df.head(10)` | Default 5 |
| See the structure | `df.info()` | Column names, types, non-null counts |
| See statistics | `df.describe()` | Mean, standard deviation, quartiles |
| See the dimensions | `df.shape` | `(n_rows, n_cols)` |
| Take one column | `df["age"]` | Returns a Series |
| Take multiple columns | `df[["age", "sex"]]` | Returns a DataFrame |
| Filter rows | `df[df["age"] > 80]` | Boolean indexing |
| Readable filtering | `df.query("age > 80")` | String syntax, good for chaining |
| Add a column | `df["new"] = ...` | Direct assignment |
| Add (chained) | `df.assign(new=...)` | Good for method chaining |
| Date conversion | `pd.to_datetime(df["col"])` | Text → datetime |
| Date parts | `df["col"].dt.year` | `.dt.month`, `.dt.day` |

**Statistics and aggregation**

| Need | Syntax | Notes |
|------|------|------|
| Frequency table | `df["col"].value_counts()` | How many times each value appears |
| Missing values | `df.isnull().sum()` | Number of missing values per column |
| Fill missing | `df["col"].fillna(0)` | Fill blanks with 0 |
| Grouped statistics | `df.groupby("col").size()` | Count per group |
| Pivot table | `pd.pivot_table(df, ...)` | Excel Pivot Table |
| Cross-tabulation | `pd.crosstab(df["a"], df["b"])` | 2×2 contingency table |
| Top N | `df.nlargest(3, "col")` | The N largest rows |
| Sorting | `df.sort_values("col")` | Sort by a column |
| Rounding | `df["col"].round(1)` | Keep 1 decimal place |

**Data tidying**

| Need | Syntax | Notes |
|------|------|------|
| Join tables | `pd.merge(df1, df2, on="key")` | VLOOKUP equivalent |
| Remove duplicates | `df.drop_duplicates("col")` | Dedupe by a column |
| Rename | `df.rename(columns={"old": "new"})` | Change a column name |
| Uppercase text | `df["col"].str.upper()` | `.str.lower()`, `.str.strip()` |
| Text search | `df["col"].str.contains("pattern")` | Returns True/False |
| Custom function | `df.apply(func, axis=1)` | Apply a function row by row |

## Common Mistakes

1. **Not converting dates**: `symptom_onset_date` is still a string, so time-based sorting breaks down (`"2026-01-09"` < `"2026-01-15"` happens to sort correctly as strings, but `"2026-1-9"` will go wrong)
2. **Ignoring the denominator**: comparing case counts directly without computing the attack rate—larger wings naturally have more cases
3. **Missing chart title/axis labels**: readers can't interpret it on its own—every chart should be understandable "out of context"
4. **Confusing the infected with the whole population**: forgetting to distinguish them when drawing the age distribution
5. **Mixing up `axis=0` and `axis=1`**: use `axis=1` (across columns) to sum comorbidity counts, and `axis=0` (down columns) to average each column
6. **Forgetting `.reset_index()`**: after `groupby`, the result is indexed by the grouping columns, so you need `reset_index()` to use it normally

## Practice Notebooks

- Data wrangling class notes: {ref}`02_data_wrangling_for_beginners.ipynb`
- Visualization class notes: {ref}`02_visualization_epi_charts.ipynb`
- Exercise version: [`02_data_wrangling_exercise.ipynb`](exercises/02_data_wrangling_exercise.ipynb)
- Solution version (instructor edition): [`02_data_wrangling_solution.ipynb`](solutions/02_data_wrangling_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/02_data_wrangling_solution.ipynb>)
