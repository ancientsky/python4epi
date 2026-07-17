# 00 Getting Started & Tools (Beginner-Friendly Edition)

## What you'll learn

- Why epidemiology needs programming tools (not just spreadsheets)
- Why this book chose Python instead of R or Excel
- Why we use `uv` instead of the traditional `pip`—and how `uv` installs Python, packages, and Jupyter Lab all in one place
- What is a virtual environment? Why does an epidemiologist's multi-project work need it?
- A hands-on, step-by-step first epidemiology "Hello World" (uv + pandas + epidemic curve)
- Besides pandas, what other data-cleaning tools can you choose from?
- Jupyter Lab, `.py` scripts, VS Code—which style suits which situation? How do you convert an `.ipynb` into a `.py` for scheduling?
- Git version control basics: the situations and commands epidemiologists use most (including collaborating on Excel files)
- How to install all the tools on your own computer, step by step

---

## First, a story: a phone call at 4 p.m. on Friday

Imagine you're a newcomer who just joined the public health department. At 4 p.m. on Friday, your supervisor calls:

> "There's a suspected Legionnaires' disease cluster at a nursing home. Of the 280 residents reported so far, over a hundred have developed pneumonia symptoms and some have already died. I need you to give me, **before you leave today**: What's the attack rate? What's the case fatality rate? Which floor is worst affected? Are the showers the source of infection? Can you draw an epidemic curve of onset dates?"

You open the Excel file you have on hand: 280 records, 32 columns—age, comorbidities, floor, exposure history, onset date, hospitalization date, death date… Just filtering and cross-tabulating makes your head spin. Not to mention your supervisor then asks: "Make me a 2×2 table for the risk ratio of shower use," "Now stratify by floor and calculate again," "How many new cases will we have next week?" That's when you realize—

- Excel's row limits start to slow you down
- Manual filtering and copy-pasting is error-prone
- Every time your supervisor says "change one condition and recalculate," you have to redo it from scratch
- When a colleague takes over your file, they have no idea how you did the calculations

**Programming isn't meant to replace your epidemiological judgment—it's meant to automate the steps that are repetitive, error-prone, and need handing over.** You write the code once, and no matter whether the data grows to 300 records or 30,000, one press of a button reruns it, checks it, and passes it to the next person.

That's why more and more epidemiology practitioners are starting to learn programming.

---

## Tutorial videos

Every concept comes with an accompanying animated tutorial video (about 3 minutes), embedded in the corresponding section below. Each video includes: main lesson → an extra public health example → busting common beginner blind spots.

Watching the video before reading the text works even better!

## Why not just use Excel / Google Sheets?

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Why use Python</div>
  <div class="youtube-lite" data-id="eMWQ-IqYjvM">
    <img src="https://img.youtube.com/vi/eMWQ-IqYjvM/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">Video contents: Excel's pain points → Python's advantages → Python vs R → a large-scale COVID-19 investigation example → blind spots: the math, "finish learning first," version issues</p>
</div>
```

You might think: "I've used Excel for years—why should I learn a new tool?"

Excel and Google Sheets really are good enough for many situations, especially **small amounts of data and one-off quick looks**. But epidemiological analysis has a few special needs where spreadsheets hit their limits:

| Situation | The spreadsheet's difficulty | The programming advantage |
|------|-------------|-----------|
| Large data (thousands to tens of thousands of line-list records) | Slow to operate, prone to crashing | Processed in seconds, no row-count limit |
| Repeated analysis (recalculating metrics as data updates weekly) | You have to redo it by hand every time | Run the same code, produce new results in seconds |
| Reproducibility (someone else needs to verify your results) | "How did you calculate this?" is hard to answer | The code itself is the complete analysis record |
| Multi-step pipelines (clean → analyze → plot → report) | Requires switching among many worksheets | One script runs the whole thing end to end |
| Advanced analysis (regression, time series, machine learning) | Basically not possible | A single line calls a mature statistics package |
| Team collaboration and version control | "final_v2_really_final.xlsx" | Git tracks every change |

**The point isn't "Excel is bad," it's "different tools suit different stages."** If your job only requires looking at a few dozen reports and calculating a percentage, Excel is perfectly fine. But if you want to:

- Handle large volumes of surveillance data
- Automatically produce weekly reports
- Do deeper statistics or predictive modeling
- Let your analysis be rerun and verified by colleagues

then learning a programming tool will, in the long run, save you a great deal of time.

---

## Why choose Python? Aren't more epidemiologists using R?

That's a very reasonable question. **R really does have deep roots in traditional epidemiology.** Packages like `epitools`, `EpiEstim`, and `surveillance` are very mature, and the WHO and various national CDCs have plenty of R teaching materials too.

So why did this book choose Python? Three reasons:

### 1. A single pipeline from statistics to machine learning

Epidemiology is evolving rapidly. Beyond traditional descriptive and inferential statistics, more and more research and practice draws on:

- **Machine learning** (e.g., using random forests to predict the risk of an outbreak spreading)
- **Deep learning** (e.g., using LSTMs to forecast dengue case trends)
- **Natural language processing** (e.g., detecting outbreak signals from social media)

Python's ecosystem in these areas (`scikit-learn`, `PyTorch`, `transformers`) is far more mature than R's. If you finish your traditional statistics in R, you'll have to learn Python again when you move to ML/DL—effectively learning twice. **Use Python to cover the whole path, and you only need to learn one language.**

### 2. Smoother data engineering and automation

In real public health work, "analysis" is only one step. You might also need to:

- Automatically pull the latest reported data from a database
- Run a metric calculation automatically every morning
- Write results into a report or push them to LINE / email

Python is much stronger than R at these **automation, scheduling, and system-integration** tasks, because it's a general-purpose programming language to begin with.

### 3. The job market and cross-disciplinary collaboration

If you'll be working with data engineers or software developers in the future (for example, building an outbreak dashboard or a data platform), they almost all use Python. Knowing Python makes it easier for you to communicate with technical teams.

### But I already know R—what should I do?

**There's absolutely no need to give up R.** R is still an excellent statistical tool. If you're already fluent in R, keep using it. This book's goal is: **if you want to learn one more tool, or if you're starting from scratch, Python is a worthwhile investment.**

---

## Why use `uv` instead of the traditional `pip`?

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: uv and environment setup</div>
  <div class="youtube-lite" data-id="AnPBQW8Vqq0">
    <img src="https://img.youtube.com/vi/AnPBQW8Vqq0/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">Video contents: why you can't just pip install → the virtual environment metaphor → installing uv → the uv three-step workflow → blind spots: command not found, uv run, pyproject.toml</p>
</div>
```

If you Google "install Python packages," almost every tutorial will teach you to use `pip install`. So why do we use the newer tool `uv`?

### First, the problems with `pip`

`pip` is Python's built-in package installer, and it's been around for many years. It works, but in a teaching setting it has a few pain points:

- **Environment conflicts**: You may have heard "it runs on my computer, but not on my colleague's." Inconsistent package versions installed by `pip` are one of the most common frustrations for beginners.
- **You have to manage virtual environments by hand**: `python -m venv`, `source activate`… just the steps to activate an environment can get a beginner lost.
- **Slow**: Installing a bunch of data science packages (pandas, matplotlib, scikit-learn…) can take several minutes.

### What `uv` solves

[`uv`](https://docs.astral.sh/uv/) is a next-generation Python package manager written in Rust. Its highlights are:

- **Much faster**: installation speeds 10–100× faster than `pip` (no exaggeration).
- **Installs Python for you too**: no need to download Python from the official site in advance—`uv` handles it in one command.
- **Manages the virtual environment automatically**: you don't need to create or activate a virtual environment by hand; `uv sync` handles it in one command.
- **Locks versions**: the `uv.lock` file ensures you use the exact same package versions as your classmates and colleagues, so you never get "mine runs, yours doesn't."
- **One command does everything**: installing Python, installing packages, running programs, managing environments—all start with `uv`.

### The actual difference: `pip` vs `uv`

| Task | The traditional way (`pip`) | This book's way (`uv`) |
|------|-------------------|-------------------|
| Install Python | Download from the official site and install manually | `uv python install 3.13` |
| Create an environment | `python -m venv .venv && source .venv/bin/activate` | `uv sync` (creates and activates automatically) |
| Install packages | `pip install pandas matplotlib` | `uv add pandas matplotlib` or `uv sync` |
| Open a notebook | `jupyter lab` (make sure it's installed first) | `uv run jupyter lab` |
| Run tests | `pytest` (make sure the environment is right first) | `uv run pytest` |
| Ensure consistent versions | Manage `requirements.txt` yourself (easy to forget to update) | `uv.lock` locks automatically |

**In short: `uv` helps you avoid 80% of environment landmines, so you can spend more time on actual learning.**

---

## Relax: you don't need to "already be good at programming"

Reading this far, you might still be a little nervous: "I've genuinely never written a single line of code—can I learn this?"

**Yes, you can.** This book is designed for learners with a public health, epidemiology, or medical background. The design principles are:

1. **Every code snippet can be copied, pasted, and run directly**—you don't have to start from a blank screen.
2. **See the result first, understand the theory second**—each chapter first produces a chart or a number, then goes back and explains how it was done.
3. **Learn programming through epidemiology scenarios**—we won't teach you to build a calculator or a number-guessing game; every example is a line list, an attack rate, an epidemic curve.

Your learning path is:

```
Copy the code → run it and see the result → change a few numbers and rerun → gradually understand the logic
```

Your programming skills will grow naturally through the chapters—you don't need to complete an entire "Intro to Python" course before coming back.

---

## Installing the tools: just install `uv`, and it handles the rest

Next come the actual installation steps. The good news is: **you only need to install one tool—`uv`.** You don't need to install Python itself in advance; `uv` will automatically download and manage the correct version of Python for you.

### Wait, I don't need to install Python first?

**Nope!** This is one of the most convenient things about `uv`. The traditional way is: download the installer from the Python website → install Python → then install a package manager. But `uv` combines these steps:

| The traditional way | The `uv` way |
|----------|----------------|
| ① Download the Python installer from the website | ① Install `uv` (one command) |
| ② Install Python | ② `uv python install 3.13` (`uv` downloads Python automatically) |
| ③ Configure the PATH environment variable | ③ Not needed—`uv` manages it for you |
| ④ Install pip / create a virtual environment | ④ Not needed—`uv sync` handles it all |

**In short: once `uv` is installed, you have everything.**

If your computer already has Python, that's fine too—`uv` will detect and use it, with no conflicts.

### Installing `uv`

#### macOS / Linux

Open the terminal (on macOS you can search "Terminal" with Spotlight) and type:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After it finishes, close the terminal and reopen it, then verify:

```bash
uv --version
```

#### Windows (PowerShell)

Press `Win + X`, choose "Windows PowerShell" or "Terminal," and type:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close PowerShell and reopen it, then verify:

```powershell
uv --version
```

> **Success looks like**: seeing `uv 0.x.x` (any version number) is all you need.
>
> **Common issue**: if it shows `command not found: uv`, close the terminal and reopen it once more. The installer adds `uv` to your PATH, but you need to restart the terminal for it to take effect.

### Installing Python with `uv`

Once `uv` is installed, a single command installs Python:

```bash
uv python install 3.13
```

`uv` automatically downloads Python 3.13 and installs it into its own managed directory, so it won't conflict with any Python already on your computer.

Verify:

```bash
uv run python --version
# You'll see: Python 3.13.x
```

> **Why recommend 3.13?** Python 3.13 is the current stable release (published in October 2024). It has better performance, clearer error messages, and all the major data science packages already support it. If your computer already has Python 3.12 or 3.11, you can still use this book normally, but we recommend the latest version for the best experience.

---

## Why do you need a "virtual environment"? What does it have to do with epidemiology?

You may hear someone say "remember to use a virtual environment," and think it's just another programming buzzword. Let me explain it with an epidemiology scenario:

### The problem: package versions clashing

Imagine you're working on two projects at the same time:

- **Project A: dengue weekly report**—uses `pandas 1.5`, written a year ago, runs rock-solid
- **Project B: COVID dashboard**—uses `pandas 2.2`, needs new features

If both projects share the same Python environment, then after you install `pandas 2.2`, Project A might break (because some syntax changed in the new version). Install `pandas 1.5` back, and Project B breaks again.

**A virtual environment gives each project its own "isolated package space."** Project A has its own pandas 1.5, Project B has its own pandas 2.2, and they don't interfere with each other.

```
Your computer
├── Project A (dengue weekly report)/.venv/
│   └── pandas 1.5, matplotlib 3.7 ...
├── Project B (COVID dashboard)/.venv/
│   └── pandas 2.2, plotly 6.0 ...
└── Project C (this book)/.venv/
    └── pandas 2.2, matplotlib 3.10 ...
```

### How does `uv` manage virtual environments?

Good news: **you don't need to create a virtual environment by hand—`uv` does it automatically.** When you run `uv sync` inside a project folder, it will:

1. Create a `.venv/` directory inside the folder (that's the virtual environment)
2. Install all the packages listed in `pyproject.toml` into `.venv/`
3. From then on, every command you run with `uv run ...` automatically uses this virtual environment

You never need to run `source .venv/bin/activate`—`uv run` handles it automatically.

```bash
# This one line both creates the virtual environment and installs all packages
uv sync

# From then on, prefix every command with uv run to run it inside the virtual environment
uv run python my_script.py
uv run jupyter lab
uv run pytest
```

---

## The complete `uv` guide: from installing packages to opening Jupyter Lab

### Scenario 1: following along with this book (the simplest)

If you're downloading this book's code to learn from, you only need:

```bash
cd python4epi        # Enter the book's folder
uv sync              # Install all packages (about 1–2 minutes the first time)
uv run jupyter lab   # Open Jupyter Lab
```

That's it—three lines, and everything is installed: pandas, matplotlib, scikit-learn, and Jupyter Lab are all included.

### Scenario 2: I want to build my own new epidemiology analysis project

Suppose you want to build a dengue analysis project from scratch:

```bash
# Create the project folder
mkdir dengue-analysis
cd dengue-analysis

# Initialize the project (uv creates pyproject.toml)
uv init

# Pin the Python version
uv python pin 3.13

# Install the packages you need
uv add pandas matplotlib jupyterlab openpyxl

# Open Jupyter Lab
uv run jupyter lab
```

**What does `uv add` do?** It will:
1. Automatically download and install the specified packages
2. Write the package names into `pyproject.toml` (the package list)
3. Update `uv.lock` (the exact version lock file)
4. Create the virtual environment too, if it doesn't exist yet

Later, all you or a colleague need to do on another computer is run `uv sync` to get the exact same environment.

### Scenario 3: installing a new package from inside Jupyter Lab

You're already writing code in Jupyter Lab when you suddenly realize you need a new package (say, `seaborn` for prettier plots).

**Method A: install from the terminal (recommended)**

```bash
# Run in the terminal (no need to close Jupyter Lab)
uv add seaborn
```

Then go back to Jupyter Lab, restart the kernel (menu → Kernel → Restart Kernel), and you can `import seaborn`.

**Method B: install from within a notebook cell**

If you don't want to switch to the terminal, you can run this directly in a notebook code cell:

```python
# Run in a notebook cell (note the leading exclamation mark)
!uv add seaborn
```

After it finishes, you'll also need to restart the kernel.

```{tip}
We recommend Method A (installing from the terminal). Method B is convenient, but it sometimes can't find `uv` due to path issues. If you hit `uv: command not found` with Method B, switch to Method A.
```

### `uv` command cheat sheet

| I want to… | Command | Notes |
|---------|------|------|
| Install Python | `uv python install 3.13` | Download the specified Python version |
| Initialize a new project | `uv init` | Create `pyproject.toml` |
| Pin the project's Python version | `uv python pin 3.13` | Create a `.python-version` file |
| Install all packages | `uv sync` | Install according to `pyproject.toml` |
| Add one package | `uv add pandas` | Install and record it in `pyproject.toml` |
| Add multiple packages | `uv add pandas matplotlib seaborn` | Install several at once |
| Remove a package | `uv remove seaborn` | Uninstall and delete it from `pyproject.toml` |
| Run a command in the virtual environment | `uv run python script.py` | Automatically uses the virtual environment |
| Open Jupyter Lab | `uv run jupyter lab` | Launch it inside the virtual environment |
| Run tests | `uv run pytest` | Run tests inside the virtual environment |
| See which packages are installed | `uv pip list` | List all installed packages |

---

## Hands-on tutorial: an epidemiology Hello World from scratch

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: your first program, Hello Epi</div>
  <div class="youtube-lite" data-id="VcxttnJxwG4">
    <img src="https://img.youtube.com/vi/VcxttnJxwG4/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">Video contents: git clone + uv sync → open Jupyter → run the analysis → see an attack rate of 43.2% → blind spots: clone failure, slow sync, red Warnings</p>
</div>
```

Just reading commands can still feel abstract. Let's start from a computer with nothing installed and, step by step, build an epidemiologist's first "Hello World"—not printing a line of text, but **reading a line list from a nursing home cluster, calculating the attack rate and case fatality rate, and drawing an epidemic curve**.

### Step 1: install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After it finishes, **close the terminal and reopen it**.

### Step 2: create the project

```bash
mkdir epi-hello-world
cd epi-hello-world
uv init
uv python pin 3.13
```

### Step 3: install the epidemiology analysis packages

```bash
uv add pandas matplotlib jupyterlab openpyxl
```

This one line installs:
- `pandas`: reading and processing tabular data (the line list)
- `matplotlib`: plotting (the epidemic curve)
- `jupyterlab`: an interactive coding environment
- `openpyxl`: lets pandas read and write Excel (`.xlsx`) files

### Step 4: open Jupyter Lab

```bash
uv run jupyter lab
```

Your browser will open automatically. Click **"Python 3 (ipykernel)"** on the right to create a new notebook.

### Step 5: type the following code into the notebook

Press `Shift + Enter` to run each cell:

**Cell 1: read in the nursing-home Legionnaires' disease line list**

```python
import pandas as pd

# Read the line list from the Songbai nursing home Legionnaires' disease cluster (280 residents)
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# Look at the first few rows—each row is one resident's complete record
df.head(10)
```

**Cell 2: calculate the attack rate and case fatality rate**

```python
# len(df) = how many rows the data has (= number of residents)
total_residents = len(df)

# (df["clinical_severity"] != "not_ill") → produces a Series of True/False
# .sum() → counts True as 1 = number of infected people
infected = (df["clinical_severity"] != "not_ill").sum()
deaths = (df["outcome"] == "dead").sum()

# Attack rate = infected ÷ total × 100
attack_rate = infected / total_residents * 100
# Case fatality rate (CFR) = deaths ÷ infected × 100 (note the denominator is the infected!)
cfr = deaths / infected * 100

# f-string: inside f"..." the {variable_name} is replaced by the variable's value
# :.1f → show to 1 decimal place
print(f"Total residents: {total_residents}")
print(f"Infected: {infected}")
print(f"Attack rate: {attack_rate:.1f}%")
print(f"Deaths: {deaths}")
print(f"Case fatality rate (CFR): {cfr:.1f}%")
```

**Cell 3: draw the epidemic curve**

```python
import matplotlib.pyplot as plt  # plt = the conventional shorthand for matplotlib

# -- CJK font setup (avoid Chinese labels showing as boxes □□□) --
# matplotlib only recognizes Latin fonts by default; Chinese characters turn into "tofu" boxes
# The line below tells it: "try these Chinese fonts in order, and use whichever one you find"
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False  # prevent the minus sign from showing as a box
plt.style.use("ggplot")        # apply an academic style (light gray background + white gridlines)
plt.rcParams["figure.dpi"] = 150  # raise the image resolution (the default 100 is too blurry)

# Convert the onset-date text to a date format, and count "how many onsets per day"
onset = pd.to_datetime(df["symptom_onset_date"])  # text → date
epi_curve = onset.dropna().dt.date.value_counts().sort_index()
# dropna() = drop people with no onset date (the uninfected)
# .dt.date = keep only the date (drop hours/minutes/seconds)
# .value_counts() = how many times each date appears = daily case count
# .sort_index() = sort by date

# fig = the whole sheet of paper, ax = the canvas on it (all plotting commands act on ax)
fig, ax = plt.subplots(figsize=(10, 4))  # figsize=(width, height) in inches
ax.bar(epi_curve.index, epi_curve.values, color="#2980B9", edgecolor="white")
ax.set_xlabel("Onset Date")   # X-axis label
ax.set_ylabel("Cases")          # Y-axis label
ax.set_title("Epidemic Curve — Songbai Nursing Home Legionnaires' Disease Cluster")  # chart title
fig.autofmt_xdate()    # automatically rotate the date labels to avoid overlap
plt.tight_layout()     # automatically adjust the margins to prevent labels being cut off
plt.show()             # display the chart
```

**Cell 4: attack rate by floor and wing**

```python
# Create an infection flag: anything other than not_ill counts as infected, True→1, False→0
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# Group by floor + wing, and count both residents and infections
wing_summary = df.groupby(["floor", "wing"]).agg(
    total=("case_id", "count"),     # how many residents in each group
    cases=("infected", "sum"),      # how many infected in each group
).reset_index()  # flatten the group index back into ordinary columns

# Attack rate = infected ÷ residents in that area × 100 (note the denominator is each area's population!)
wing_summary["attack_rate_%"] = (wing_summary["cases"] / wing_summary["total"] * 100).round(1)

wing_summary  # in Jupyter, the last line is automatically displayed as a table
```

### Step 6: see the results

You should now see:
- A table showing the first 10 rows of the line list (including 32 columns like age, comorbidities, exposure history)
- An attack rate of 43.2% and a case fatality rate of 15.7%
- An **epidemic curve bar chart**, showing a peak in onsets around January 20—the classic pattern of a common-source exposure
- A comparison of attack rates by floor and wing (the 2nd–3rd floor B wing is clearly higher)

**Congratulations! This is an epidemiologist's first analysis in Python.** The whole process needs only one tool, `uv`—no need to install Python in advance, no need to set up a virtual environment, no need to deal with pip.

```{tip}
Try modifying the code above: group by the `"shower_use"` column to look at the attack rate, or filter to only `"confirmed"` cases to draw the epidemic curve. Every time you change something, press `Shift + Enter` to see the result immediately. That's the power of programming—change one condition, and the whole analysis recalculates automatically.
```

---

## What's the `#` in the code?—an introduction to Python comments

In the Hello World code just now, you should have seen something like this:

```python
# Read the line list from the Songbai nursing home Legionnaires' disease cluster
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
```

That line starting with `#` is a **comment**—Python **completely ignores** it and won't run it.

### Why do you need comments?

- **For yourself**: coming back to the code three months later, you'll have forgotten why you wrote it this way
- **For colleagues**: when handing over an outbreak report, comments let them follow your analytical logic
- **For reviewers**: journals require reproducible research, and comments are the code's user manual

### How to write comments

```python
# A full-line comment: everything after the # is not executed
attack_rate = infected / total * 100  # end-of-line comment: you can also add one after code

# Multi-line comments? Python has nothing like C's /* ... */
# Every line needs its own # (which is actually a good thing—it lines up more neatly)

# ✅ A good comment: explains the "why"
# Fill missing ages with the median, because the mean is easily skewed by extreme values
df["age"].fillna(df["age"].median(), inplace=True)

# ❌ A bad comment: just repeats what the code already says
# Set x to 5 (who couldn't see that?)
x = 5
```

```{tip}
**Beginner advice: build the habit of adding `#` comments first.** Even if they're wordy at the start, that's fine—it's a hundred times better than none at all. As you gain experience, you'll increasingly know which spots need explaining and which don't.
```

---

## Markdown formatting in Jupyter notebooks

Jupyter Lab cells come in two types:

| Cell type | Purpose | How to switch |
|----------|------|---------|
| **Code** | Write Python code | Select the cell → press `Y` |
| **Markdown** | Write text, headings, lists | Select the cell → press `M` |

Markdown cells turn your notebook from just a pile of code into an **illustrated analysis report**.

### The most common Markdown syntax

```markdown
# Big heading (one # sign)
## Second-level heading (two # signs)
### Third-level heading (three # signs)

**Bold text** (two asterisks on each side)
*Italic text* (one asterisk on each side)
`inline code` (one backtick on each side)

- Unordered list item 1
- Unordered list item 2

1. Ordered list item 1
2. Ordered list item 2

> Quoted text (add > in front like this)

| Column | Description |
|------|------|
| age  | Age |
| sex  | Sex |
```

### An example inside a notebook

Suppose you're analyzing the Songbai nursing home data. A Markdown cell might read like this:

```markdown
## Attack rate analysis

This analysis uses the line list from the Songbai nursing home Legionnaires' disease cluster (n=280).

### Key findings

1. **Attack rate**: 43.2% (121/280)
2. **Case fatality rate**: 15.7% (19/121)
3. The 2nd–3rd floor B wing has a clearly higher attack rate

> ⚠️ Note: the denominator for the case fatality rate is the number infected (121), not all residents (280)
```

### Handy tips

- **Quick switching**: in command mode (press `Esc`), press `M` to turn a cell into Markdown, and `Y` to turn it back into Code
- **Running Markdown**: just like a Code cell, press `Shift + Enter` and the Markdown renders into nicely formatted text
- **Double-click to edit**: double-click a rendered Markdown cell to go back to edit mode
- **Use Markdown for analysis notes**: a good habit is to add a Markdown cell before each analysis section explaining "what this does and why"

```{tip}
**A good notebook = code + Markdown explanations + chart outputs.** Think of your notebook as an outbreak investigation report that anyone can open and understand your analysis process. That's the spirit of reproducible research.
```

---

## Besides pandas, what other data-cleaning tools are there?

`pandas` is the most mainstream package for tabular data in the Python ecosystem, and this book relies on it as well. But as the amount of data you handle grows, you may hear about other options. Here's a brief comparison:

| Package | Highlights | Best for | Installation |
|------|------|----------|----------|
| **pandas** | Most widely used, most tutorials, most complete features | Most epidemiological analyses (thousands to hundreds of thousands of records) | `uv add pandas` |
| **polars** | Extremely fast (5–50× faster than pandas), more memory-efficient | Large data (millions of surveillance records or more) | `uv add polars` |
| **DuckDB** | Query tabular data with SQL syntax, no database server needed | People used to SQL, huge CSV files | `uv add duckdb` |
| **pyjanitor** | Adds more intuitive data-cleaning syntax on top of pandas | Making cleaning steps more readable | `uv add pyjanitor` |

### Which is best for beginners?

**Just learn pandas.** The reasons are:

1. **95% of tutorials, examples, and StackOverflow answers use pandas**—so when you hit a problem, it's easiest to find a solution
2. **pandas' features are more than enough for epidemiological analysis**—unless you're handling millions of records or more, you don't need to switch
3. **Other tools have syntax very similar to pandas**—once you know pandas, the cost of moving to polars or DuckDB is low

### When should you consider other tools?

| The problem you hit | A tool to consider |
|-------------|---------------|
| pandas reads CSVs slowly (over 1 million records) | `polars` (many times faster to read) |
| Not enough memory (a laptop with only 8GB) | `polars` (more memory-efficient) |
| You already know SQL | `duckdb` (run SQL directly on CSV/Parquet) |
| Too many cleaning steps, making the code long | `pyjanitor` (method chains read better) |

```{tip}
Every chapter in this book uses pandas. If you hit a performance bottleneck in future work, come back to this table to choose the right tool. There's no need to learn several packages right now.
```

---

## Why recommend Jupyter Lab? Can't I just write `.py`?

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: getting started with Jupyter Lab</div>
  <div class="youtube-lite" data-id="iELUPwdPk7M">
    <img src="https://img.youtube.com/vi/iELUPwdPk7M/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">Video contents: what is Jupyter → how to launch it → the cell concept → Shift+Enter → blind spots: execution order, Restart Kernel, stuck on [*]</p>
</div>
```

You might think: "Isn't a program just a text file? Why use Jupyter Lab, this thing that looks like a web page?"

That's a great question. The answer is: **it depends on your goal.** Different tools suit different stages of work.

### Jupyter Lab's advantage: "see results as you write"

Epidemiological analysis has one distinctive trait: you usually **explore the data and make decisions at the same time**.

For example, when you get a line list:
1. First look at what the data looks like (`df.head()`)
2. Notice the date column is in the wrong format, and clean it
3. Calculate an attack rate and check whether the number looks right
4. Draw an epidemic curve and notice one day has an unusually high case count
5. Go back to that day's raw data and find it was a duplicate report
6. Delete the duplicate and redraw

This process is **interactive and exploratory**—you don't know the final analysis steps at the outset.

Jupyter Lab's notebooks (`.ipynb` files) suit exactly this way of working:

- **Run cell by cell**: write a snippet, press `Shift + Enter`, and immediately see the result
- **Charts display right below the code**: no need to open a separate window to view them
- **You can interleave text explanations**: use a Markdown cell to write "this step calculates each area's attack rate"
- **Results sit alongside the code**: a colleague who opens your notebook sees the complete analysis process and results

### So what are `.py` scripts good for?

A `.py` file is a plain-text Python program. It has no "cell by cell" concept—you press "run," and the whole file runs from top to bottom.

**A `.py` file suits the scenario "you already know the steps and want them to run automatically":**

| Scenario | The right tool | Why |
|------|-----------|------|
| Exploring new data, trying different analysis methods | Jupyter Lab (`.ipynb`) | You need to adjust as you look |
| A fixed weekly outbreak report | A `.py` script | Fixed steps, runs automatically |
| Building a reusable function library | A `.py` module | Lets multiple notebooks call it |
| Scheduled automation (run once every morning at 8) | A `.py` script | Schedulers can only run `.py`, not `.ipynb` |
| Learning, teaching, sharing analysis | Jupyter Lab (`.ipynb`) | Illustrated, easy for colleagues to follow |

**The ideal workflow in practice is:**

```
Explore and experiment in a notebook (.ipynb)
         ↓
Once the analysis steps are settled, tidy them into a script (.py)
         ↓
Run it automatically with a scheduler (cron / Windows Task Scheduler)
```

### Other editors: VS Code, PyCharm

Besides Jupyter Lab, you can also write Python in other code editors:

| Editor | Highlights | Who it's for |
|--------|------|--------|
| **Jupyter Lab** | Interactive, charts display instantly, great for exploratory analysis | Epidemiology analysts, data science beginners |
| **VS Code** | Full-featured, can edit both `.py` and `.ipynb`, has AI assistance | People who want an all-in-one development environment |
| **PyCharm** | Purpose-built for Python, powerful debugging tools | Advanced Python developers |
| **Google Colab** | Free cloud Jupyter, no installation needed | People short on computing power or wanting a free GPU |

```{tip}
**This book recommends Jupyter Lab for beginners.** Once you're more comfortable, try VS Code—it can open `.ipynb` files directly (the experience is almost identical to Jupyter Lab) and also edit `.py` files, handling both formats in one environment.
```

### Converting `.ipynb` to `.py`: three methods

Once your analysis workflow is settled and you want to turn the notebook into a `.py` script (for example, to schedule automatic runs), there are three ways:

#### Method 1: export directly from within Jupyter Lab

In the Jupyter Lab menu:

```
File → Save and Export Notebook As → Executable Script
```

This produces a `.py` file that strings all the code cells together, with Markdown cells becoming comments starting with `# `.

#### Method 2: use the `jupyter nbconvert` command

```bash
uv run jupyter nbconvert --to script my_analysis.ipynb
```

This produces `my_analysis.py` in the same directory.

If you have many notebooks to convert at once:

```bash
uv run jupyter nbconvert --to script notebooks/*.ipynb
```

#### Method 3: tidy it by hand (most recommended for a proper scheduled script)

The `.py` files produced by the first two methods contain some clutter (like `# In[1]:` cell markers). If this is a scheduled script for long-term use, we recommend tidying it by hand:

1. Open the exported `.py`
2. Delete cell markers like `# In[1]:`
3. Delete exploratory code (like `df.head()` and `print(df.shape)`—steps that only look at the data)
4. Keep the important steps and add clear comments
5. Change output paths (like where the report is saved) to absolute paths

This book's `notebooks/run_sitrep.py` is an example of a tidied `.py` script—it reads the line list, calculates the CFR and attack rate, and outputs a summary table by area:

```bash
uv run python notebooks/run_sitrep.py
```

### In practice: scheduling an analysis script to run automatically

Suppose you've tidied up a `weekly_report.py` and want it to run automatically every Monday at 8 a.m. to produce a dengue weekly report.

#### macOS: use launchd (recommended)

**launchd** is macOS's native scheduler. It's more stable than cron and won't be blocked by macOS's security mechanisms. Create a plist file at `~/Library/LaunchAgents/com.epi.weekly.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.epi.weekly</string>
    <key>ProgramArguments</key>
    <array>
        <!-- Use `which uv` to find your uv absolute path -->
        <string>/Users/your-username/.local/bin/uv</string>
        <string>run</string>
        <string>python</string>
        <string>/Users/your-username/projects/python4epi/weekly_report.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/your-username/projects/python4epi</string>
    <!-- Every Monday (Weekday=1) at 8:00 a.m. -->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/your-username/projects/python4epi/output/weekly_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/your-username/projects/python4epi/output/weekly_stderr.log</string>
</dict>
</plist>
```

```bash
# Load the schedule
launchctl load ~/Library/LaunchAgents/com.epi.weekly.plist

# Confirm it loaded successfully
launchctl list | grep epi

# Remove the schedule
launchctl unload ~/Library/LaunchAgents/com.epi.weekly.plist
```

```{tip}
For a complete launchd tutorial (including a daily SitRep scheduling example), see Ch04 Step 9.
```

#### Linux / macOS: use cron

macOS can also use cron, but on newer macOS versions it may require granting "Full Disk Access"—**macOS users are advised to prefer launchd above**.

```bash
# Open the cron editor
crontab -e

# Add this line (runs every Monday at 8 a.m.)
0 8 * * 1 cd /path/to/your/project && uv run python weekly_report.py >> /path/to/logs/weekly_report.log 2>&1
```

What each field means:

```
0 8 * * 1
│ │ │ │ │
│ │ │ │ └── day of week (1 = Monday)
│ │ │ └──── month (* = every month)
│ │ └────── day of month (* = every day)
│ └──────── hour (8 = 8 a.m.)
└────────── minute (0 = on the hour)
```

#### Windows: use Task Scheduler

1. Search for "Task Scheduler"
2. Click "Create Basic Task"
3. Set the trigger: every Monday at 8:00 a.m.
4. Action: Start a program
   - Program/script: `cmd`
   - Add arguments: `/c cd /d C:\path\to\your\project && uv run python weekly_report.py`

You can also do it in one line from the command line with `schtasks`:

```powershell
schtasks /create /tn "Weekly_Report" /tr "cmd /c cd /d C:\path\to\your\project && uv run python weekly_report.py" /sc weekly /d MON /st 08:00
```

#### Tips for scheduled scripts

| Tip | Why |
|------|------|
| Write input/output paths at the top of the script | The working directory during scheduling may not be what you expect |
| Add `try/except` error handling | When the schedule runs, you're not at the computer, so save the error messages |
| Save results to a file, don't just print | `print` only goes to the log; saving to a file is how you actually get the report |
| macOS: prefer launchd | launchd is the native scheduler—it won't be blocked by security mechanisms, and its logging is easier to manage |
| Run it once by hand first to confirm it works | Then set up the schedule, to avoid errors every Monday |

### Summary: an epidemiologist's tool selection guide

```
Step 1: Learning & exploratory analysis
  → Jupyter Lab (.ipynb)

Step 2: Once the analysis workflow is settled
  → Convert to a .py script

Step 3: Automation & scheduling
  → launchd / cron / Task Scheduler + .py script

Advanced: for a better development experience
  → VS Code (supports both .ipynb and .py)
```

**You don't have to pick a single tool from the start.** Do the analysis in Jupyter Lab first, convert to `.py` when you need scheduling, and switch to VS Code later if it feels smoother. Tools are there to serve you, not to make you anxious.

---

## What is Git? Why do epidemiologists need it?

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: Git version control</div>
  <div class="youtube-lite" data-id="SdtrxhPbRqk">
    <img src="https://img.youtube.com/vi/SdtrxhPbRqk/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">Video contents: the nightmare of version chaos → Git as a time machine metaphor → the three areas → git add/commit/push → blind spots: git add ., commit messages, push rejected</p>
</div>
```

### First, a scenario

You spend a whole day writing a dengue outbreak analysis script and produce a beautiful epidemic curve. The next day your supervisor says, "Change the denominator from confirmed cases to reported cases," and you do it. Two days later, your supervisor says, "Actually, change it back."

If your file is called `analysis.py`, at this point your folder might look like this:

```
analysis.py
analysis_v2.py
analysis_v2_final.py
analysis_v2_final_really_final.py
analysis_v2_final_really_final_supervisor_edits.py
```

You can't tell what differs between versions, and you're not sure whether "changing it back" really matches the original.

**Git is the tool that solves this problem.** Think of it as a "time machine":

- Every time you feel the code has reached a stable state, you take a "snapshot" (called a **commit**)
- Each snapshot has a description (e.g., "change the denominator to reported cases"), a timestamp, and who made it
- You can return to any snapshot at any time and compare the differences between two versions
- When several people modify the same code at once, Git helps you merge without overwriting each other

**Once you use Git, you only need one `analysis.py`, and all historical versions are safely preserved behind the scenes.**

```{figure} images/git_version_chaos_en.svg
:name: fig-git-version-chaos
:alt: File version chaos without Git vs only needing one file with Git
:width: 100%

Without Git, your folder fills up with all kinds of file versions, and you can't tell which is the latest. With Git, you only need one file, and all historical versions are safely preserved in the commit history.
```

The diagram below shows the core concept of how Git works—four areas and three key commands. Just get a general impression for now; we'll walk you through the operations step by step later:

```{figure} images/git_three_areas_en.svg
:name: fig-git-three-areas
:alt: Git's four areas: working directory, staging area, local repository, remote GitHub
:width: 100%

Git's four areas: you modify files in the **working directory**, use `git add` to put them in the **staging area**, use `git commit` to take a **snapshot** into the local repository, and finally use `git push` to upload it to GitHub.
```

### The Git situations epidemiologists use most

You don't need to learn all of Git's features. Below are the situations you'll most often encounter in epidemiology work, with the corresponding commands:

#### Situation 1: first-time setup (only needs to be done once)

Right after installing Git, tell it who you are. That way, every future commit automatically records the author:

```bash
git config --global user.name "Wang Xiaoming"
git config --global user.email "xiaoming@health.gov.tw"
```

#### Situation 2: the daily workflow—after editing code, save a version

This is what you'll do most often. Suppose you modified the epidemic curve script today:

```bash
# 1) First check which files have been modified
git status

# 2) Add the edited file to the "ready to save" area (staging area)
git add notebooks/02_visualization_epi_charts.ipynb

# 3) Take a snapshot with a note
git commit -m "feat: add a 7-day moving average to the epidemic curve"
```

```{figure} images/git_daily_workflow_en.svg
:name: fig-git-daily-workflow
:alt: The daily Git workflow: edit → git status → git add → git commit
:width: 100%

The daily workflow is these four steps: edit the code, check the status, add to staging, take a snapshot to save. Repeat once for each small step you complete.
```

**The message in `git commit -m "..."` matters a lot**—it's the only clue the future you (or your colleague) has when looking back. A good message looks like this:

| Good commit message | Bad commit message |
|---|---|
| `fix: correct CFR denominator to confirmed cases, not reported cases` | `update` |
| `feat: add a bar chart comparing attack rates by area` | `changed some things` |
| `docs: add an explanation of confidence intervals to Chapter 3` | `final` |

#### Situation 3: see what you changed before

Next week your supervisor asks: "What did you change in that CFR formula last time?"

```bash
# See a summary of the 5 most recent commits
git log --oneline -5
```

You'll see a list like this:

```
a1b2c3d fix: correct CFR denominator to confirmed cases, not reported cases
e4f5g6h feat: add a 7-day moving average to the epidemic curve
i7j8k9l docs: add an explanation of the data-cleaning steps to Chapter 2
```

To see exactly which lines a particular commit changed:

```bash
git show a1b2c3d
```

#### Situation 4: sync your code to GitHub (cloud backup + team sharing)

GitHub is like Git's "cloud drive." Push your code there and you needn't worry if your computer breaks, and colleagues can see the latest version:

```bash
# Push your local commits to GitHub
git push
```

Conversely, if a colleague updated the code and you want to pull down the latest version:

```bash
# Pull the latest version from GitHub to your machine
git pull
```

#### Situation 5: you want to try a new approach, but aren't sure it'll work

Suppose you want to try a different statistical method to estimate R0 (the basic reproduction number), but you don't want to break the currently working version. You can open a "branch":

```bash
# Create a new branch called try-r0-method
git checkout -b try-r0-method

# Change and experiment freely on this branch
# ... write code ...
git add .
git commit -m "feat: try estimating R0 with the EpiEstim method"

# If it works, merge back into the main branch
git checkout main
git merge try-r0-method

# If it fails, just switch back—nothing is affected
git checkout main
```

```{figure} images/git_branching_en.svg
:name: fig-git-branching
:alt: The Git branching concept: branch off main to experiment, merge if it works, discard if it fails
:width: 100%

A branch is like a parallel universe—branch off main to experiment, merge back if it works, or just switch back to main if it fails, leaving the original code completely unaffected.
```

A branch is like a parallel universe—experiment on a separate line, merge back if it works, discard it if it fails, all without affecting the original code.

### Git command cheat sheet

Below are the commands you'll use in daily work; bookmark them for quick reference:

| I want to… | Command | In plain words |
|---------|------|---------|
| See which files have been changed | `git status` | See which changes aren't saved yet |
| Add files to be saved | `git add filename` | Tell Git "I want to save these changes" |
| Add all changed files at once | `git add .` | Add everything (careful not to add secret files) |
| Save (take a snapshot) | `git commit -m "message"` | Create a version record |
| See the history | `git log --oneline -10` | See a summary of the 10 most recent versions |
| See a file's change history | `git log --oneline filename` | See how many times this file was changed |
| Compare the current and last version | `git diff` | See which lines I changed |
| Upload to GitHub | `git push` | Sync to the cloud |
| Download the latest version from GitHub | `git pull` | Pull your colleagues' updates |
| Open a new branch to experiment | `git checkout -b branchname` | Open a parallel universe |
| Switch back to the main branch | `git checkout main` | Return to the main line |
| Return to a previous version (look only, no changes) | `git log --oneline` → `git show commit-hash` | View a past snapshot |

### When should you commit?

A simple rule: **commit once after each "meaningful small step."** For example:

- Finished cleaning the missing values in the line list → commit
- Finished drawing an epidemic curve → commit
- Corrected the attack rate calculation formula → commit

Don't wait until "the whole analysis is done" to commit. A commit that's too big is hard to trace problems in; frequent small commits let you return to any step at any time.

### A worked example: managing Excel investigation files with Git

You might ask: "We do all our investigations in Excel—can Git manage Excel too?"

**The answer is yes.** Git can track any file, including `.xlsx`. It's just that Excel is a **binary file**, so Git can't compare it "line by line" the way it does plain text. But it will still preserve a complete snapshot of every version, letting you return to any previous state at any time.

Below is a complete team collaboration example. Suppose you're responsible for a dengue investigation Excel file at the public health department, and your team is you and a colleague, Xiao Li.

#### Step 1: create a GitHub repository and put the Excel file in it

First create a new repository on GitHub, then on your computer:

```bash
# Create the project folder
mkdir dengue-investigation-2025
cd dengue-investigation-2025
git init

# Put your Excel file in here
# (assuming you've copied line_list.xlsx into this folder)

# The first commit
git add line_list.xlsx
git commit -m "feat: add the initial version of the dengue investigation line list"

# Link to the repository on GitHub, then push it up
git remote add origin https://github.com/your-team/dengue-investigation-2025.git
git push -u origin main
```

Now your Excel file is on GitHub, with a cloud backup, and all team members can access it.

#### Step 2: you modify a record and add a chart

The next day you receive a new report and need to update the data. You open `line_list.xlsx`:
- Corrected the onset date of case #23 (originally mistyped)
- Added a new "case counts by area" chart worksheet (sheet)

After saving your changes, go back to the terminal:

```bash
# See what changes Git detected
git status
# You'll see: modified: line_list.xlsx

# Add to the staging area
git add line_list.xlsx
```

```bash
# Save it, writing clearly what you changed
git commit -m "fix: correct the onset date of case #23; add a chart of case counts by area"
```

#### Step 3: push to GitHub (`git push`)

```bash
git push
```

Just this one command, and your local latest version is synced to GitHub.

**Pushed to where?** To the GitHub repository you set up in Step 1. You can use `git remote -v` to see the currently linked remote location.

#### Step 4: why use a Pull Request? Can't I just push?

If it's a small solo project of your own, pushing directly to `main` is perfectly fine.

But for team collaboration, a better approach is to use a **Pull Request (PR for short)**. The workflow goes like this:

```bash
# First open a branch and make changes on it
git checkout -b update-case-23

# Edit the Excel file, then commit
git add line_list.xlsx
git commit -m "fix: correct the onset date of case #23"

# Push the branch to GitHub
git push -u origin update-case-23
```

Then, on the GitHub website, click "**Create Pull Request**."

**The value of a PR is:**

- **It leaves a review record**: a colleague can comment on the PR, "Checked the original report—the date really is 6/15, not 6/5"
- **It prevents errors reaching the main file**: someone reviews it before the merge
- **It's easy to trace**: if someone asks three months later "why was this record changed," the PR has a complete discussion record

**Who can merge?** That depends on the repository's permission settings. The usual practice is:

| Role | Permission |
|------|------|
| Project owner / team lead | Can merge PRs and manage repository settings |
| Team member | Can open PRs, review, and comment, but needs the owner's approval to merge |
| External collaborator | Can fork and open a PR, but cannot merge directly |

In a public health department setting, it might be the **investigation team lead** who is responsible for merging, ensuring every data change goes through review.

```{figure} images/git_pull_request_flow_en.svg
:name: fig-git-pr-flow
:alt: The Pull Request flow: open a branch → edit → push to GitHub → open a PR → review → merge
:width: 100%

The Pull Request flow: branch off main to make changes, push to GitHub and open a PR, and after team members review and confirm, the owner merges it back into main. This way, every change has a review record.
```

#### Step 5: your colleague Xiao Li also needs to edit the same Excel file

Xiao Li also needs to add a few case records. The correct approach is:

```bash
# Xiao Li first pulls down the latest version
git clone https://github.com/your-team/dengue-investigation-2025.git
cd dengue-investigation-2025

# Open a branch of their own
git checkout -b add-new-cases-lili

# Open the Excel file, make changes, and save
# ...done editing...

git add line_list.xlsx
git commit -m "feat: add 8 new cases reported on 6/16"
git push -u origin add-new-cases-lili
```

Then Xiao Li opens a PR on GitHub, and after the owner reviews it, it's merged.

#### Step 6: Xiao Li is done—how do you sync?

After Xiao Li's PR is merged, your local file is still the old one. You need to pull down the latest version:

```bash
# First switch back to the main branch
git checkout main

# Pull the latest version from GitHub
git pull
```

Now your `line_list.xlsx` includes the 8 cases Xiao Li added.

#### Important reminder: Excel's merge limitation

One thing to note: **if you and Xiao Li modify different parts of the same Excel file at the same time, Git cannot merge them automatically.** Because Excel is a binary file, Git sees "the whole file changed" and doesn't know who changed which cell.

In this case Git will report a "**merge conflict**," and you'll need to decide by hand whose version to keep.

**Practical ways to avoid conflicts:**

| Method | Notes |
|------|------|
| **Agree on time slots** | "I edit in the morning, you edit in the afternoon," to avoid editing at the same time |
| **Split by worksheet** | You handle Sheet1 (the case list), Xiao Li handles Sheet2 (the statistics summary) |
| **Switch to CSV** | Save the data as `.csv` (plain text), and Git can compare line by line and merge automatically |
| **Pull before editing** | Before you start editing each time, run `git pull` first to make sure you have the latest version |

```{tip}
If your team often needs several people editing the same data at once, consider splitting the Excel file into CSV (data) plus a notebook (analysis and charts). CSV is a plain-text file, so Git can compare differences line by line, and when several people modify different rows at once it can merge automatically—far friendlier than Excel. This is also the workflow this book recommends.
```

#### The complete flowchart

Stringing the steps above together gives the complete workflow of an epidemiology team collaborating with Git:

```
You edit the Excel file
    ↓
git add → git commit (save locally)
    ↓
git checkout -b branchname → git push (push to GitHub)
    ↓
Open a Pull Request on GitHub
    ↓
Colleagues review and comment to confirm
    ↓
The team lead merges into main
    ↓
Everyone else git pull (sync the latest version to their machine)
```

> **For those who don't want to learn Git at all**: if you just want to focus on epidemiology and Python right now, you can skip this section for now. Git is not a requirement for this book—every chapter can be completed without it. Come back to this section the day you run into "I want to recover last week's code" or "I want to share an analysis script with a colleague."

---

## 10-minute hands-on: from installation to your first epidemic curve

Below is a complete hands-on exercise. Follow along and, within 10 minutes, you'll draw your first epidemic curve—a classic chart you've seen in textbooks and will definitely use in real outbreak investigations.

### Step 1: confirm `uv` is installed

```bash
uv --version
```

Seeing a version number means you can move on. (You don't need to install Python in advance; `uv sync` will handle it automatically.)

### Step 2: download the book's source code to your computer

All of this book's code, data files, and notebooks live in a single **GitHub repository**. Think of it as "a cloud folder holding all the files for the whole book."

We need to **download this folder to your computer** to run the code locally. There are two ways to download it—pick whichever feels smoother:

#### Option A: use `git clone` (recommended)

`git clone` is the "download a project" command developers use most. It copies the entire folder to your computer while preserving the full version history, so when the book is updated in the future you can sync easily.

Open the terminal and type:

```bash
git clone https://github.com/ancientsky/python4epi.git
cd python4epi
```

> **See a `fatal: ...` error?** Your computer may not have Git installed yet:
> - **macOS**: type `xcode-select --install` and follow the prompts to install
> - **Windows**: download and install from [https://git-scm.com](https://git-scm.com), then reopen the terminal
> - **Linux**: type `sudo apt install -y git`

#### Option B: download the ZIP directly (no Git needed)

If you don't want to install Git, you can download the archive directly:

1. Open [https://github.com/ancientsky/python4epi](https://github.com/ancientsky/python4epi) in your browser
2. Click the green **"Code"** button → choose **"Download ZIP"**
3. Unzip it wherever you like (e.g., the Desktop or a documents folder)
4. Open the terminal and use `cd` to switch to the unzipped folder:

```bash
# Example: if you unzipped it on the Desktop
cd ~/Desktop/python4epi-main
```

> **The difference between Option A and B**: after `git clone`, when the book is updated you just run `git pull` in the folder to get the latest version. With a ZIP download, you have to download again. Either way works fine for the rest of your learning.

### Step 3: install all the packages

No matter which download option you used, once you're inside the book's folder, run:

```bash
uv sync
```

- `uv sync`: reads the book's package list and automatically downloads the correct version of Python, creates the virtual environment, and installs all the needed Python packages (pandas, matplotlib, etc.). All in one line.

The first `uv sync` usually takes 1–2 minutes (there are quite a few packages to download); after that, it's very fast.

### Step 4: open Jupyter Lab

```bash
uv run jupyter lab
```

Your browser will automatically open a file-explorer-like screen—this is **Jupyter Lab**, the working environment where we write code and view results.

### Step 5: open the first notebook

In the file list on the left, click into `notebooks/` → open `02_visualization_epi_charts.ipynb`.

You'll see a series of "cells," some with text explanations and some with code.

### Step 6: run all the code

Two ways:

- **Run everything at once**: top menu → `Run` → `Run All Cells`
- **Run cell by cell**: click a cell and press `Shift + Enter`

### Step 7: see your first epidemic curve

Scroll down and you'll see a bar chart:

- **Title**: `Epidemic Curve (By Onset Date)`
- **X-axis**: onset date
- **Y-axis**: cases per day

This is one of epidemiology's most central charts: the **epidemic curve**. It tells you whether the outbreak is rising, at its peak, or subsiding.

**Congratulations! You've completed your first epidemiology data visualization task.**

---

## Frequently asked questions (beginner edition)

| Problem | Solution |
|------|------|
| `git clone` shows a `fatal` error | Your computer may not have Git installed—see the installation notes in Step 2, or use the ZIP download instead |
| `command not found: uv` | Close the terminal and reopen it, or confirm the install path was added to `PATH` |
| `python --version` isn't 3.13 | That's fine—`uv sync` will automatically download the correct version of Python |
| `uv sync` fails | Check your internet connection, then run it again. The first run needs to download quite a few packages |
| Jupyter Lab opens blank | Try manually entering the `http://localhost:8888/...` URL shown in the terminal into your browser |
| The notebook throws an error | Confirm you've run `uv sync`, then rerun from the first cell |

---

## This book's learning roadmap

```{raw} html
<div class="video-card">
  <div class="video-title">Tutorial video: the course map and learning strategy</div>
  <div class="youtube-lite" data-id="H3fMhNhj3u4">
    <img src="https://img.youtube.com/vi/H3fMhNhj3u4/hqdefault.jpg" loading="lazy" alt="Tutorial video">
  </div>
<p style="font-size:0.85em;color:#6b6b6b;margin-top:0.3em;">Video contents: the five-act structure → the required track Ch00-04 → the elective track Ch05-14 → learning paths for different roles → blind spots: where to start, whether you can skip chapters, Colab vs local</p>
</div>
```

You don't need to learn all the chapters in one go. This book uses the **Songbai nursing home Legionnaires' disease cluster** as the thread running through the whole book, with each chapter taking you one layer deeper into the analysis—just like a real investigation, gradually uncovering the truth.

```
== Act One: The Report Comes In ==
  00 Getting Started (you are here) — tool installation, Hello World
  01 Python basics — attack rate, CFR, minimal syntax
  02 Data handling and visualization — read in the 280-record line list, draw the epidemic curve

== Act Two: From Description to Inference ==
  03 The association between exposure and disease — 2×2 tables, RR, OR, chi-square test
  04 The cluster investigation workflow — produce the first SitRep for the boss

== Act Three: Going Deeper ==
  05 Stratified analysis and confounders — bedridden seniors don't shower and don't get sick: protection or confounding?
  06 Logistic regression — adjust for age, comorbidities, and exposure simultaneously to get the adjusted OR
  07 Time series and forecasting — how many new cases will there be next week?
  08 Spatial epidemiology — which floor and wing is most dangerous? Draw a spot map

== Act Four: Advanced Modeling ==
  09 Survival analysis — the time from onset to death: which factors affect survival?
  10 Machine learning — use 32 columns of features to predict infection and severe illness
  11 Deep learning — the PyTorch version of the predictive model
  12 Causal inference — the causal effect of shower exposure: how do you draw a DAG?

== Act Five: Wrapping Up and Real-World Practice ==
  13 Reproducible research — let colleagues reproduce your analysis with one click
  14 A real-world case — from receiving the report to the final case report, all the way through
```

**The first 4 chapters are the foundation**, and we recommend learning them in order. From Chapter 5 onward you can skip around, picking the topics your work or research needs.

```{figure} images/learning_roadmap_en.svg
:name: fig-learning-roadmap
:alt: Learning roadmap: Ch 00-04 the required foundation, Ch 05-14 advanced electives
:width: 100%

The blue blocks are the required foundation (Ch 00–04), which we recommend completing in order. The purple blocks are advanced electives (Ch 05–14), which you can choose from as needed after finishing the foundation.
```

---

## Next steps

Ready? Run the following commands, then turn to Chapter 01 to begin your epidemiology × Python journey:

```bash
uv sync
uv run jupyter lab
```
