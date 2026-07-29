# 04 Outbreak Investigation Workflow: From Line List to SitRep

## The scenario

Three days into the Legionnaires' disease cluster at Pine and Cypress Nursing Home, one afternoon your supervisor says:

> "Get me the first daily situation report (SitRep) within two hours. It needs to cover: how many people are infected, where it's worst, what the case fatality rate is, and what the epidemic curve looks like. After that, update it every morning before 9 a.m."

You have a line list CSV with 280 rows × 32 columns in hand. This chapter teaches you how to use Python to **automate** the production of a structured SitRep — one that you can update each day just by rerunning a single script.

## What you'll learn

- The full automated pipeline from raw line list to SitRep
- **PII protection**: de-identification techniques, k-anonymity, and the practical workflow
- The three pillars of descriptive epidemiology: **person, time, place**
- Key metric calculations: attack rate, CFR, hospitalization rate, ICU rate
- Stratified summaries by case classification (confirmed / probable / not-a-case)
- Producing a structured report (tables + charts)
- Turning the analysis into a rerunnable script

## 🩺 Super Simple Special: Understanding the Outbreak Investigation Workflow with "You're the School Nurse's Outbreak Lead"

> The FETP ten steps, line list, SitRep, Person/Time/Place... this chapter throws a lot of jargon at you — starting to feel dizzy? Don't worry. This section sets the nursing home aside for a moment and lets you be the **outbreak lead in the school nurse's office** — walking through the whole "how do you investigate an outbreak" process in a way that'll make even a 7th grader get it instantly. Once you've mastered this workflow, every Step later in this chapter is just a zoomed-in detail of it.

### 👀 Uh oh, one red eye after another across the whole class

Second week of school, and the line outside the nurse's office keeps growing — **a bunch of classmates have red, itchy, watery eyes** (acute conjunctivitis, a.k.a. "pink eye"). The principal calls you in: "Look into this! What's going on, is it going to spread, what do I do?"

All you have is a messy pile of absence slips and clinic visit records. **Your first instinct is to panic** — but panicking doesn't help. What a real outbreak-investigation pro does at this moment is one thing: **open the SOP and follow the recipe, step by step.**

> 🧑‍🍳 **The SOP is designed for "panicked you," not "calm you."** The more you panic, the easier it is to miscount or blame the wrong thing; following a checklist step by step means that even with shaky hands, you won't skip the box that says "who actually counts as sick." **An outbreak investigation isn't a contest of who guesses fastest — it's a contest of who misses nothing.**

### Step 1: Agree on "who counts as a hit" first — the case definition

Before you start counting, you need to **draw a line**: how red do the eyes have to be, is there discharge, within how many days — for it to count as "a case in this outbreak"? That's the **case definition**.

> 🥅 **Never change the rule while you're still counting!** If you change the criteria halfway through — something that didn't count yesterday counts today — the number becomes a rubber band anyone can stretch. That's not an investigation, that's haggling. **The case definition is that line: wherever you draw it, that's what the numbers will look like. So draw the line first, then start counting.**

(In practice this splits into three tiers — **confirmed / probable / not-a-case** — covered in detail in the main text of this chapter.)

### 🕵️ The three questions that crack the case: Person, Time, Place (descriptive epidemiology)

Once the line is drawn and you start building the **line list** (one row per person), you just keep asking three questions — **Person, Time, Place**:

| Question | In plain English | What it tells you |
|------|------|-----------|
| **Person** | Who got hit? Which people, what characteristics? | Who's especially at risk |
| **Time** | Which days did it break out? Which day was the peak? | Roughly **when** people got infected (draw it as an **epidemic curve**) |
| **Place** | Which classroom got hit hardest? (highest attack rate) | **Where** to go looking for the source |

> 🗺️ **Stack all three clues together, and the suspect source surfaces on its own.** Skip one, and you're working with only half a treasure map.

```{figure} images/school_outbreak_workflow_en.svg
:name: fig-school-outbreak-workflow
:alt: School pink-eye outbreak-investigation dashboard: at the top is the SOP step bar (define case → person → time → place → SitRep), the middle has three panels for person/time/place (person = red-eye stick figures 17/60, time = epidemic curve peaking on day 3, place = attack rate by classroom with Room A at 60% as the hotspot near the water fountain), and the bottom rolls it all up into a one-page SitRep that bridges to the 280-person Legionnaires' disease investigation at the nursing home
:width: 100%

An "outbreak-investigation dashboard": follow the SOP → ask the three questions Person/Time/Place → roll it up into a one-page SitRep. Zoom that exact same workflow up to full scale, and it's the 280-person Legionnaires' disease investigation at the nursing home.
```

### Try it yourself: run "Person, Time, Place" with your own two hands

```python
import pandas as pd

# The nurse's office line list: who in this "pink eye" outbreak got sick, on which day, in which classroom
line_list = pd.DataFrame({
    "classroom": (["Room A"] * 12 + ["Room B"] * 3 + ["Room C"] * 2),
    "onset_day": [1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6,   2, 3, 5,   3, 4],
})
class_size = {"Room A": 20, "Room B": 30, "Room C": 10}  # Each classroom has a different size (the denominator matters!)

# ── Time: draw the epidemic curve using the "onset date" (not the absence date!)—which day is the peak? ──
by_day = line_list["onset_day"].value_counts().sort_index()
print("[Time] New cases per day (mini epidemic curve, drawn using onset date):")
for day, n in by_day.items():
    print(f"  Day {day} | {'█' * n} {n}")
print(f"  -> Peak on day {by_day.idxmax()}\n")

# ── Place: compare the "attack rate," not the case count! ──
by_room = line_list["classroom"].value_counts()
ar = by_room / pd.Series(class_size)
print("[Place] Attack rate by classroom: case count vs. attack rate")
for room in class_size:
    print(f"  {room} | {by_room[room]} cases | {by_room[room]}/{class_size[room]} = {ar[room]:.0%}")
print(f"  -> Highest attack rate: {ar.idxmax()} (go check out what's special about that room!)")
print("     Note: Room B has 3 cases > Room C's 2, but Room B's attack rate of 10% < Room C's 20%—more people naturally means more cases, so you have to look at rates!\n")

# ── Person / Summary ──
total_cases, total_students = len(line_list), sum(class_size.values())
print(f"[Person/Summary] {total_students} students total, {total_cases} got sick, overall attack rate {total_cases/total_students:.0%}")
```

Running this, you'll see:

```text
[Time] New cases per day (mini epidemic curve, drawn using onset date):
  Day 1 | █ 1
  Day 2 | ███ 3
  Day 3 | ██████ 6
  Day 4 | ████ 4
  Day 5 | ██ 2
  Day 6 | █ 1
  -> Peak on day 3

[Place] Attack rate by classroom: case count vs. attack rate
  Room A | 12 cases | 12/20 = 60%
  Room B | 3 cases | 3/30 = 10%
  Room C | 2 cases | 2/10 = 20%
  -> Highest attack rate: Room A (go check out what's special about that room!)
     Note: Room B has 3 cases > Room C's 2, but Room B's attack rate of 10% < Room C's 20%—more people naturally means more cases, so you have to look at rates!

[Person/Summary] 60 students total, 17 got sick, overall attack rate 28%
```

### Reading the clues: stack the three pictures together

- **Time**: there's only **one peak** (day 3), then it drops off → this shape usually means **everyone got it from the same source**, rather than person-to-person spread dragging on and on. (Sound like something everyone shares? 💧)
- **Place**: **Room A has a 60% attack rate**, far higher than the other rooms → the source is likely right in that classroom.
- You go take a look: **there's a water fountain right outside Room A's door that everyone uses.**

> 💧 **Hold on — don't convict it yet!** The water fountain is now the **prime suspect**, not "the culprit." **Descriptive analysis (Person/Time/Place) can only "identify a suspect," not "prove guilt."** To prove guilt, you need the 2×2 tables and regression from later chapters, plus **environmental sampling** (actually culturing the pathogen from the fountain). That's exactly why Ch03, Ch05, and Ch06 of this book exist.

### The last step: write a one-page SitRep and hand it in

The principal doesn't have 30 minutes to listen to you talk. **A SitRep (situation report) is the "say it in one page" version**: how many are affected right now, where it's concentrated, whether that's up or down from yesterday, and what to do next.

> 📋 **A SitRep isn't something you write once and you're done — the outbreak changes daily, so you update a new version every day. Today's SitRep is the starting point for tomorrow's decisions.** That's exactly why this chapter teaches you to write "one script, rerun every day."

### ⚠️ Four honest caveats

1. **Description ≠ causation**: however beautifully you draw Person/Time/Place, it only "points at a suspect." Once the water fountain is named, you still need 2×2 tables, regression, plus environmental sampling later to confirm it.
2. **Draw the epidemic curve using the "onset date," not the "absence date" or "notification date"**: use the wrong date and the peak shifts, and you'll look in the wrong time window. (The main text of this chapter uses the dataset's `symptom_onset_date`, not `notification_date`.)
3. **For "Place," compare rates, not counts**: a bigger classroom naturally has more cases. You must divide by each classroom's headcount (the denominator) — comparing the **attack rate** is the only fair comparison. That's exactly why Room B's 3 cases is actually "safer" than Room C's 2.
4. **Following the SOP ≠ being rigid**: some steps loop back and rerun; and **you should start control measures the moment they're warranted** (like shutting off the fountain right away) — you don't have to wait for the whole investigation to finish before acting. Saving people comes first; investigation and response can run in parallel.

### Cheat sheet for reading the picture (save this)

| What you see... | What it means |
|---|---|
| Case definition set before counting starts | Draw the line first, so no one can fudge the numbers |
| Person | Who got hit, what characteristics |
| Time (epidemic curve) | Which days it broke out, which day peaked (drawn using **onset date**) |
| Place (attack rate by location) | Where's hit hardest → where to look for the source (compare **rates**, not counts) |
| A "single peak" epidemic curve | Usually means a common source |
| The location with the highest attack rate | Prime suspect, but **not proven guilty yet** |
| SitRep | A one-page situation report, updated daily |
| Descriptive analysis | Generates hypotheses, doesn't prove causation |

### Back to reality: pink eye → Legionnaires' disease

Now swap the school scenario for the nursing home:

| School pink-eye outbreak | Real nursing home case |
|---|---|
| Absence slips and clinic records in the nurse's office | 280-row line list (one row per person) |
| Agreeing up front on "how red counts as a hit" | Case definition (confirmed / probable / not-a-case) |
| Who got hit, which people | Person (age, sex, comorbidity distribution) |
| Which days it broke out, peaked day 3 | Time (epidemic curve, `symptom_onset_date`) |
| Which classroom got hit hardest (Room A at 60%) | Place (attack rate by floor/wing) |
| Room A's water fountain → suspect | Water supply system → hypothesis to be verified |
| The one page you reported to the principal | Daily SitRep to the incident commander |

Every trick you just learned in the nurse's office — follow the SOP, define the case first, ask Person/Time/Place, compare rates not counts, write a one-page SitRep — **is exactly what this chapter does with the 280-person nursing home data, from Step 1 through Step 8**. Now scroll down to the FETP ten-step framework and each individual Step — doesn't it suddenly feel a lot friendlier? 😉

---

## The FETP 10-step outbreak investigation: where this chapter fits

Outbreak investigation follows an internationally recognized **10-step systematic framework**, the one used by Taiwan CDC's FETP 2.0 training. This chapter centers on Step 5 (descriptive epidemiology) while also touching on the core concepts of Steps 1, 3, 4, 9, and 10.

```{figure} images/fetp_10_steps_en.svg
:name: fig-fetp-10-steps
:alt: The FETP 10-step outbreak investigation framework, highlighting which steps are enhanced by Python
:width: 100%

An overview of the FETP 10-step outbreak investigation. The orange steps (5, 7) are the parts Python can automate heavily; blue (10) is partially supported; the gray steps (1, 2, 3, 4, 6, 8, 9) require on-site human judgment and cannot be fully replaced by code. **The steps can run in parallel or be reordered, but none of them can be skipped.**
```

## The basic structure of a SitRep

A standard daily situation report contains at least:

1. **Summary metrics**: the cumulative numbers to date
2. **Person**: distribution by age, sex, comorbidities
3. **Time**: the epidemic curve and incidence trend
4. **Place**: attack rates compared across locations
5. **Recommended actions**: an initial read based on the data

---

<!-- video: ch04_01_sitrep_overview -->
<!-- /video -->

## FETP Step 1: Preparation (what to do before you set out)

Before opening any CSV, the field investigation team should complete three things:

### Team composition

| Role | Responsibilities | This cluster (Legionnaires' disease) |
|------|------|----------------------|
| Epidemiologist | Design the investigation, analyze the data | Lead investigator |
| Laboratory staff | Collect samples, match strains | Sputum / water sample PCR + culture |
| Infection control practitioner | Assess nosocomial infection, isolation measures | Evaluate the nursing home's movement flow |
| Environmental health staff | Sample cooling towers and shower equipment | Chlorinate towers, shut down equipment |
| Local health authority | Coordinate resources, statutory notification | Local health bureau investigation, CDC notification |

> Legionnaires' disease (*Legionella pneumophila*) does not spread person-to-person, so you do **not** need contact-isolation staff. For a fecal-oral pathogen such as norovirus, you would need to add contact-tracing personnel.

### Supplies checklist

Before setting out, confirm the following supplies are ready:

- **Sampling**: sterile water containers, sputum collection tubes, environmental swabs, refrigerated transport boxes
- **Personal protection**: N95 masks, gloves, isolation gowns (adjust to the pathogen)
- **Investigation tools**: standardized questionnaires (paper + electronic backup), tablets, encrypted USB drives
- **Communications**: local health bureau contact list, laboratory emergency phone numbers

### Literature preparation

Before the investigation, you should read up on:
1. The basic characteristics of the pathogen (incubation period, transmission route, high-risk groups)
2. Investigation reports of recent similar clusters (for clues to the environmental source)
3. The facility's past outbreak records (to check whether this is repeated exposure)

```{admonition} Quick reference: Legionnaires' disease background
:class: note
- Pathogen: *Legionella pneumophila* serogroup 1 (the most common, >80% of cases)
- Transmission route: inhalation of contaminated aerosols (cooling towers, showers, hydrotherapy pools)
- Not person-to-person: no concern for asymptomatic transmission; **no need** to set up isolation wards
- High-risk groups: age 65+, immunosuppressed, chronic lung disease, smokers
- Case fatality rate: community-acquired about 5–10%; institutional/severe cases can reach 20–30%
```

---

## Step 1: Read in and prepare the data

```python
import pandas as pd
import matplotlib.pyplot as plt

# ── CJK font setup: avoid Chinese labels rendering as boxes □□□ ──
# matplotlib doesn't support CJK by default, so we give it a candidate font list
# It tries them left to right and stops at the first one available
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False  # fix the minus sign showing as a box
plt.style.use("ggplot")        # use the ggplot style (gray background, white gridlines)
plt.rcParams["figure.dpi"] = 150  # raise the output resolution for sharper charts

# ── Read the CSV ──
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
# df is now a DataFrame (like an Excel spreadsheet)
# 280 rows (one per resident) × 32 columns (one per field)

# ── Convert date columns ──
# Dates in the CSV are strings (e.g. "2026-01-15"); we must turn them into
# datetime objects before we can compute time differences
date_cols = [
    "facility_admission_date", "symptom_onset_date",
    "hospitalization_date", "death_date", "notification_date",
]
for col in date_cols:
    # errors="coerce": on an unparseable value (blank, garbage) don't raise;
    # instead convert to NaT (Not a Time, the date-world equivalent of NaN)
    df[col] = pd.to_datetime(df[col], errors="coerce")

# ── Derive new columns ──
# Build a 0/1 "infected" column
# Anyone whose clinical_severity is not "not_ill" counts as infected (1), else 0
# The != comparison produces True/False, and astype(int) maps True→1, False→0
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# Build age groups: pd.cut slices a continuous variable into categories
# bins=[59, 69, 79, 89, 100] defines the cut points; intervals are left-open,
# right-closed: (59,69], (69,79]...
df["age_group"] = pd.cut(
    df["age"], bins=[59, 69, 79, 89, 100],
    labels=["60-69", "70-79", "80-89", "90+"],
)

# Count each resident's number of comorbidities
comorbidity_cols = [
    "comorbidity_chf", "comorbidity_dm",
    "comorbidity_cancer", "comorbidity_copd", "immunosuppressed",
]
# These columns are all 0/1; axis=1 means "sum across the row" (per resident)
# The result is how many comorbidities each resident has
df["n_comorbidities"] = df[comorbidity_cols].sum(axis=1)
```

## Step 1.5: PII protection — the first thing to do when you get a line list

In a real investigation, the line list you receive from a hospital or long-term care facility often contains **personally identifiable information (PII)**: names, national ID numbers, phone numbers, addresses, medical record numbers… Before you do any analysis, push it to git, or send it to a colleague, the **very first thing** is to deal with the PII. This section shows how to do that in Python.

> 📌 **Why doesn't this course's `legionella_outbreak.csv` have any PII?** Because it's **synthetic data** — from the start it has no real names, ID numbers, or other identifiers, which is standard practice for a teaching dataset. But the raw line list you get in the field usually isn't like that, so you need to learn the techniques below.

<!-- video: ch04_08_pii_protection -->
<!-- /video -->

```{figure} images/pii_protection_techniques_en.svg
:name: pii-protection-techniques
:alt: PII protection flowchart: raw line list with PII on the left, five de-identification techniques in the middle, clean de-identified data on the right
:width: 100%

Get the line list → first distinguish "direct identifiers / quasi-identifiers / sensitive attributes" → de-identify with five techniques → only then start analyzing. The bottom-right shows the practical three-stage workflow (raw → deidentify.py → deidentified).
```

### The three types of PII

| Category | Examples | Handling principle |
|------|------|---------|
| **Direct identifiers** | Name, national ID, medical record number, phone, address, email, photo | Always **remove or replace** |
| **Quasi-identifiers** | Age, sex, ZIP code, occupation, date of care, room number | Harmless alone, but **in combination** can identify → generalize |
| **Sensitive attributes** | HIV, mental illness, genetics, sexual orientation | Need special protection; consider k-anonymity |

> ⚠️ **The quasi-identifier trap**: Sweeney's (2000) classic study showed that **{ 5-digit ZIP + date of birth + sex }** uniquely identifies 87% of the U.S. population. A combination like age + sex + floor is just as dangerous in a nursing home — in a small group it's easy to work out who's who.

### Five de-identification techniques (with Python)

Suppose the raw line list has these columns: `name`, `national_id`, `phone`, `address`, `room_number`, `age`, `symptom_onset_date`.

#### ① Suppression — the most thorough approach

```python
# Simply delete the identifier columns you don't need
pii_columns = ["name", "national_id", "phone", "address"]
df_safe = df.drop(columns=pii_columns, errors="ignore")
# errors="ignore": don't raise if a column doesn't exist (defensive coding)
```

> 💡 **Principle**: any PII column your analysis doesn't use, just **delete it**. If you don't need to keep it, don't.

#### ② Pseudonymization — replace real names with codes

```python
# Replace the original IDs with sequential codes CASE_001, CASE_002...
df_safe = df_safe.reset_index(drop=True)
df_safe["case_id"] = ["CASE_" + str(i).zfill(3) for i in range(1, len(df_safe) + 1)]

# Build a "crosswalk table" stored separately in an encrypted location
# (only authorized staff can re-identify)
mapping = pd.DataFrame({
    "original_id": df["national_id"],
    "case_id": df_safe["case_id"],
})
# mapping.to_csv("data/restricted/id_mapping.csv", index=False)  # store on an encrypted drive
```

> ⚠️ **Pseudonymization ≠ anonymization**: as long as the crosswalk exists, re-identification is theoretically possible, so the crosswalk must be kept **strictly confidential** (a separate encrypted drive, an encrypted archive, tight access controls).

#### ③ Hashing — one-way and irreversible

```python
import hashlib

# Salted hashing: prevents an attacker from cracking it with a rainbow table
SALT = "PineAndCypressNursingHome2026"  # in practice read from an env var os.environ["PII_SALT"], never hard-coded

def hash_id(raw_id: str, salt: str = SALT) -> str:
    """Salt the raw ID, SHA-256 hash it, and take the first 12 chars as case_id."""
    combined = (salt + str(raw_id)).encode("utf-8")
    return "H_" + hashlib.sha256(combined).hexdigest()[:12]

df_safe["hashed_id"] = df["national_id"].apply(hash_id)
# A123456789 → "H_4f8a9c2e1b3d" (a fixed mapping, but you can't reverse it to the original ID)
```

> 💡 **Why add a salt?** If you hash the national ID directly, an attacker can crack it by hashing every possible ID number and comparing. Adding a secret string (salt) means they must obtain the salt first before they can reverse it — which makes it far harder.

#### ④ Generalization — turn exact values into ranges

```python
# Age: exact number → age group (already done in Step 1)
df_safe["age_group"] = pd.cut(df["age"], bins=[59, 69, 79, 89, 120],
                               labels=["60-69", "70-79", "80-89", "90+"])

# Date: exact date → epidemiological week (loses information but protects privacy)
df_safe["epi_week"] = df["symptom_onset_date"].dt.isocalendar().week

# Room number: exact 1A-101 → keep only the wing 1A
df_safe["wing"] = df["room_number"].str.split("-").str[0]

# You can then drop the original exact columns
df_safe = df_safe.drop(columns=["age", "symptom_onset_date", "room_number"],
                        errors="ignore")
```

#### ⑤ Masking — keep the format, hide the content

```python
def mask_phone(phone: str) -> str:
    """Turn phone 0912-345-678 → 0912-***-*** (keep the first 4-digit carrier prefix)"""
    if pd.isna(phone):
        return phone
    parts = str(phone).split("-")
    if len(parts) == 3:
        return f"{parts[0]}-***-***"
    return "***"

df_safe["phone_masked"] = df["phone"].apply(mask_phone)
```

> 💡 When would you mask instead of just deleting? When you need to **show an example** to your supervisor, or need to validate the format — masking keeps the "shape" of the field without leaking the real value.

### k-anonymity: everyone must "blend into at least k people"

Even after removing direct identifiers, combinations of quasi-identifiers can still expose someone's identity. **k-anonymity** is a widely used quantitative standard:

> Definition: for **any** record in the table, querying by the "combination of quasi-identifier columns" must return at least **k** records matching the same conditions.

```python
# Check the k-anonymity of the (age_group, sex, wing) quasi-identifier set
quasi_ids = ["age_group", "sex", "wing"]
group_sizes = df_safe.groupby(quasi_ids, observed=True).size()

print("Distribution of group sizes:")
print(group_sizes.describe())
print(f"\nSize of the smallest group (the k value): {group_sizes.min()}")

# Find the "high-risk" small groups (k < 5)
risky = group_sizes[group_sizes < 5]
print(f"\n⚠ Number of combinations below k=5: {len(risky)}")
if len(risky) > 0:
    print(risky)
```

**Rules of thumb**:

| Use case | Suggested k |
|---------|----------|
| Internal analysis, closed use | k ≥ 3 |
| Sharing across units | k ≥ 5 |
| Sensitive populations (children, mental illness, etc.) | k ≥ 10 |
| Public release / open data | k ≥ 20 |

If a group has n &lt; k, there are two ways to handle it:
1. **Merge groups** (e.g. fold 90+ into 80-89 to make 80+)
2. **Suppress** — don't output that record

### The practical workflow: separate raw from de-identified

```
Project structure
├── data/
│   ├── raw/               ← only authorized staff enter (encrypted, access-controlled)
│   │   └── line_list_RESTRICTED.csv   ← original PII data, .gitignore
│   └── deidentified/      ← safe to commit to git and share
│       └── line_list.csv  ← the de-identified version
├── scripts/
│   └── deidentify.py      ← run once to produce deidentified from raw
└── .gitignore             ← must include data/raw/
```

Put the PII-protection code in a **standalone script** (`deidentify.py`) rather than writing it inside the analysis notebook — this way:

- The analysis notebook only reads the de-identified file → you never accidentally commit PII to git
- The de-identification logic is centralized → easier to audit and modify
- When new data arrives, you just rerun the script

```python
# Skeleton of scripts/deidentify.py
from pathlib import Path
import pandas as pd
import hashlib, os

RAW = Path("data/raw/line_list_RESTRICTED.csv")
OUT = Path("data/deidentified/line_list.csv")
SALT = os.environ["PII_SALT"]  # read from an env var, never hard-code it

def main() -> None:
    df = pd.read_csv(RAW)
    df = df.drop(columns=["name", "national_id", "phone", "address"])
    df["case_id"] = ["CASE_" + str(i).zfill(4) for i in range(1, len(df) + 1)]
    df["age_group"] = pd.cut(df["age"], bins=[59, 69, 79, 89, 120],
                              labels=["60-69", "70-79", "80-89", "90+"])
    df = df.drop(columns=["age"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"✓ Wrote {len(df)} de-identified records → {OUT}")

if __name__ == "__main__":
    main()
```

```{warning}
**Things you must NEVER commit:**

- ❌ The original line list (with PII)
- ❌ The ID crosswalk table (mapping.csv)
- ❌ The salt used for hashing (put it in `.env`; exclude it in `.gitignore`)
- ❌ Jupyter Notebook outputs that contain PII (`nbstripout` can strip outputs automatically)

**Rules that MUST go in `.gitignore`:**
​```
data/raw/
data/restricted/
.env
*.key
​```
```

```{admonition} Taiwan regulations and international standards
:class: tip, dropdown

**Taiwan:**
- **Personal Data Protection Act (PDPA)**: Article 6 (special personal data, including medical, genetic, sex life, health checkups, criminal record) and Article 20 (use beyond the specified purpose)
- **Communicable Disease Control Act**: Article 10 (confidentiality obligation of investigation personnel), Article 11 (case data used only for outbreak analysis and control)
- **Human Subjects Research Act**: research using patient data requires **IRB (Institutional Review Board)** review

**International standards:**
- **HIPAA Safe Harbor (U.S.)**: lists 18 identifiers that must be removed
- **GDPR (EU)**: pseudonymization is defined in Art. 4(5); k-anonymity is a common practice

**Key references:**
- Sweeney L. *k-anonymity: A model for protecting privacy*. IJUFKS 2002;10(5):557-570.
- El Emam K, et al. *A systematic review of re-identification attacks on health data*. PLoS ONE 2011;6(12):e28071.
```

## FETP Step 3: Confirm the diagnosis — four time-period concepts you must not confuse

Before you start computing attack rates, get clear on the four time concepts related to Legionnaires' disease. These four concepts directly affect how you set the **traceback window** and how you choose the lag in the Ch07 time-series model.

```{figure} images/incubation_periods_en.svg
:name: fig-incubation-periods-ch04
:alt: Diagram of four concepts: incubation period, latent period, infectious period, serial interval
:width: 100%

The four key time-period concepts in infectious disease. When the **latent period is shorter than the incubation period**, the patient is already infectious before symptoms appear (presymptomatic transmission); in that case the basis for quarantine is the maximum incubation period, not the onset date.
```

| Concept | Definition | Legionnaires' example | Investigation meaning |
|------|------|----------------|----------|
| **Incubation period** | Exposure → symptom onset | 2–10 days (usually 5–6) | Traceback exposure window = latest onset date minus 10 days |
| **Latent period** | Exposure → becoming infectious | ≈ incubation period (person-to-person is extremely rare) | Determines the risk of presymptomatic transmission |
| **Infectious period** | Becoming infectious → losing infectiousness | Sporadic (non-communicable), not applicable | Legionnaires' is not person-to-person, so the infectious period doesn't affect contact tracing |
| **Serial interval** | Index case onset → secondary case onset | Not applicable (person-to-person is rare) | If there is a person-to-person cluster, this value is used to estimate R₀ |

> **What this means for this cluster investigation:**
> - The earliest onset date is 2026-01-12; the latest is 2026-01-28.
> - Traceback exposure window = 2026-01-02 to 2026-01-28 (latest onset date minus 10 days).
> - Residents who used the **cooling tower, showers, or hydrotherapy pool** during this window are the strongly suspected exposed cases.
> - When Ch07 builds the time-series forecasting model, the lag defaults to the median incubation period of 5–6 days.

```{seealso}
Full comparison table of time-period concepts (with diagrams and examples across four pathogens): → {ref}`appendix-f-incubation`
```

---

## Step 2: Summary metrics

```python
total = len(df)                          # total residents = number of rows in the DataFrame

# df["infected"] is a 0/1 column; .sum() adds them up = number infected
# (adding any number of 0s stays 0; only the 1s contribute)
infected = df["infected"].sum()

# == produces a True/False Series, and .sum() counts the Trues (True = 1)
confirmed  = (df["case_classification"] == "confirmed").sum()
probable   = (df["case_classification"] == "probable").sum()
hospitalized = df["hospitalized"].sum()  # hospitalized is also a 0/1 column
icu          = df["icu_admission"].sum()
deaths       = (df["outcome"] == "dead").sum()

print("=" * 50)
print("Pine and Cypress Nursing Home Legionnaires' Disease Cluster — SitRep")
print("=" * 50)
print(f"Total residents: {total}")
# {infected/total:.1%}: division gives a decimal; :.1% auto-multiplies by 100,
# adds %, and keeps 1 decimal place
print(f"Infected: {infected} (attack rate {infected/total:.1%})")
print(f"  Confirmed: {confirmed}   Probable: {probable}")
print(f"Hospitalized: {hospitalized} (hospitalization rate {hospitalized/infected:.1%})")
print(f"ICU: {icu} (ICU rate {icu/hospitalized:.1%})")
print(f"Deaths: {deaths} (CFR {deaths/infected:.1%})")
```

<!-- video: ch04_02_person -->
<!-- /video -->

## Step 3: Person

```python
# Use boolean indexing to filter the infected: df[condition] keeps only rows where condition is True
cases = df[df["infected"] == 1]
# cases is a new DataFrame containing only the 121 infected residents

print("=== Demographic characteristics (infected) ===")
print(f"Median age: {cases['age'].median():.0f} years"
      f" (range {cases['age'].min()}-{cases['age'].max()})")

# .mean() on True/False is equivalent to computing a proportion
# (cases['sex'] == 'M') produces True/False; mean() gives the proportion of Trues
print(f"Proportion male: {(cases['sex'] == 'M').mean():.1%}")

print(f"\n--- Age group distribution ---")
# value_counts(): count occurrences of each category (by default sorted descending by count)
# sort_index(): sort by age group order instead (60-69 → 70-79 → ...)
# to_string(): force-print the whole thing without truncating middle rows
print(cases["age_group"].value_counts().sort_index().to_string())

print(f"\n--- Comorbidity distribution ---")
for col in comorbidity_cols:
    # Strip the "comorbidity_" prefix from the column name and uppercase it into a tidy label
    # e.g. "comorbidity_chf" → "chf" → "CHF"
    label = col.replace("comorbidity_", "").upper()
    n = cases[col].sum()  # comorbidity columns are 0/1; sum() gives the count with that comorbidity
    print(f"  {label}: {n} ({n/len(cases):.1%})")
```

<!-- video: ch04_03_time -->
<!-- /video -->

## Step 4: Time

```python
import matplotlib.dates as mdates

# groupby("symptom_onset_date"): group by onset date
# .size(): count the rows in each group (= cases that day), like GROUP BY + COUNT(*)
# .rename("cases"): name the result column "cases" for easier reference later
daily = cases.groupby("symptom_onset_date").size().rename("cases")

# ── Fill in the full date range (including 3 days before the outbreak as a "baseline period") ──
# The raw data only has dates that had cases; a day with 0 cases won't appear in the groupby result
# reindex can "fill in" the missing dates, using fill_value=0
date_range = pd.date_range(
    daily.index.min() - pd.Timedelta(days=3),  # extend 3 days earlier (show the pre-outbreak baseline)
    daily.index.max() + pd.Timedelta(days=1),  # extend 1 day later (so the last day isn't clipped)
    freq="D",                                   # freq="D" means one point per day
)
daily = daily.reindex(date_range, fill_value=0)  # fill days with no cases as 0

# ── Build the chart ──
# plt.subplots() returns two objects at once:
# fig = the whole canvas (controls overall size, resolution, saving)
# ax  = the plotting area (controls axes, title, bars, lines, etc.)
fig, ax = plt.subplots(figsize=(10, 4))  # 10 inches wide, 4 inches tall

ax.bar(daily.index, daily.values, width=1.0,
       color="#2c7fb8", edgecolor="white", linewidth=0.5)
# width=1.0 makes the bars touch (standard for an epidemic curve, no gaps)

ax.set_title("Pine and Cypress Nursing Home Legionnaires' Disease Epidemic Curve, by Onset Date, January 2026",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Date of Symptom Onset")
ax.set_ylabel("Number of Cases")

# DateFormatter("%m/%d"): set the x-axis date display format
# %m = month (01–12), %d = day (01–31), giving e.g. "01/12"
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
# DayLocator(interval=2): place a tick every 2 days (avoid overlapping labels)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
# auto-rotate the date labels 45 degrees to prevent overlap
fig.autofmt_xdate(rotation=45)

# Leave a half-day (12-hour) margin on the far left and right so the first and last bars aren't clipped
ax.set_xlim(daily.index.min() - pd.Timedelta(hours=12),
            daily.index.max() + pd.Timedelta(hours=12))
ax.set_ylim(bottom=0)  # y-axis starts at 0
# MaxNLocator(integer=True): show only integer ticks on the y-axis (you can't have 0.5 cases)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
# Remove the top and right spines (cleaner look, standard for epidemiology papers)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()  # auto-adjust spacing so the title and labels aren't cut off
plt.show()

print(f"Outbreak period: {cases['symptom_onset_date'].min().date()} – {cases['symptom_onset_date'].max().date()}")
# idxmax(): find the "index" (date) of the maximum value, not the max value itself
# daily.max() is the maximum value (the case count)
print(f"Peak day: {daily.idxmax().date()} ({daily.max()} cases)")
```

<!-- video: ch04_04_place -->
<!-- /video -->

## Step 5: Place

```python
# ── Group by floor + wing, computing all metrics at once ──
# .agg() lets you apply different aggregation functions to different columns
# Format: new_column_name=("source_column", "aggregation function or lambda")
wing_stats = (
    df.groupby(["floor", "wing"])
    .agg(
        # "size" counts the total rows in each group (= total residents of that wing, infected and not)
        residents=("case_id", "size"),
        # "infected" is a 0/1 column, so "sum" gives the number infected
        infected=("infected", "sum"),
        # lambda for custom logic: count the values equal to "dead" in the outcome column
        deaths=("outcome", lambda x: (x == "dead").sum()),
    )
    .reset_index()
    # reset_index() turns the groupby keys (floor, wing) from the "index"
    # back into ordinary columns, so we can reference them by name below
)

# Compute attack rate and CFR, multiply by 100 to make percentages, round to 1 decimal
wing_stats["AR%"] = (wing_stats["infected"] / wing_stats["residents"] * 100).round(1)
wing_stats["CFR%"] = (wing_stats["deaths"] / wing_stats["infected"] * 100).round(1)
# Join the floor (number) and wing (letter) into one label, e.g. 1 + "A" → "1A"
# astype(str) first converts the integer to a string so it can be concatenated with the letter
wing_stats["label"] = wing_stats["floor"].astype(str) + wing_stats["wing"]

print("=== Outbreak summary by wing ===")
# Select the columns to display; to_string(index=False) prints without the left-side index numbers
print(wing_stats[["label", "residents", "infected", "AR%", "deaths", "CFR%"]]
      .to_string(index=False))
```

<!-- video: ch04_05_classification -->
<!-- /video -->

## FETP Step 4: Case definition — the trade-off between precision and detection

### Why do we need a three-tier case definition?

Early in an outbreak, information is scarce. A case definition that's too narrow will **miss real cases** (low sensitivity); one that's too broad will **include non-cases** (low specificity), inflating the attack rate and misallocating resources. So in practice, cases are split into three tiers:

| Tier | Criteria | This cluster (Legionnaires') | Sensitivity | Specificity |
|------|----------|----------------------|--------|--------|
| **Confirmed** | Laboratory confirmation (PCR / culture / urinary antigen) | Lab-positive | Low | High |
| **Probable** | Clinical symptoms + epidemiological link | Fever + pneumonia imaging + same-floor exposure | Medium | Medium |
| **Suspect** | Only partial clinical symptoms | Fever + cough, but no imaging or lab result | High | Low |

> **Practical advice:**
> - **Early in the outbreak**: use a looser "suspect" definition to cast a wide net and avoid missing early cases.
> - **Analysis stage**: compute the attack rate using "confirmed + probable" (as in this chapter's `case_classification != "not_a_case"`).
> - **Public reporting**: state clearly which tier's definition you used, so the numbers aren't compared out of context.

### Refining the case definition: a norovirus example

Here's a typical **broad-to-narrow** refinement of a case definition, illustrating how to leverage the sensitivity–specificity trade-off:

```
Initial definition (broad):
  "Anyone with gastrointestinal symptoms"
  → high sensitivity, but with many concurrent gastroenteritis cases, low specificity

Add a time condition:
  "Anyone with GI symptoms from Feb 14 to Feb 16"
  → narrows the scope, excludes background gastroenteritis

Add symptom intensity:
  "Vomiting ≥ 2 times or diarrhea ≥ 3 times within 24 hours"
  → further excludes mild cases, raising the confirmation rate

Add an exposure condition (final definition):
  "The above symptoms + attended the Feb 13 wedding banquet"
  → confirmed and probable case definitions are now complete
```

### The case definition for this cluster

The case definition used in this course (built into the dataset):

| Column | Logic |
|------|----------|
| `lab_confirmed = True` | Confirmed: urinary antigen or culture positive |
| `case_classification = "confirmed"` | Confirmed case |
| `case_classification = "probable"` | Clinically compatible + epidemiological link |
| `case_classification = "not_a_case"` | Excluded: asymptomatic and lab-negative |
| `infected = 1` | Confirmed + probable combined (the main basis for analysis) |

```{seealso}
Standard definitions of confirmed / probable / suspect cases and Taiwan's notifiable disease classification: → {ref}`appendix-a-glossary`
```

---

## Step 6: Stratified summary by case classification

```python
# Group by case classification (confirmed / probable / not_a_case) and compute per-tier metrics
# We don't add .reset_index() here, so case_classification stays as the index,
# making the printout more intuitive (the classification name appears in the leftmost column)
classification = (
    df.groupby("case_classification")
    .agg(
        n=("case_id", "size"),                              # count per tier
        hospitalized=("hospitalized", "sum"),               # hospitalized count (sum of 0/1 column)
        icu=("icu_admission", "sum"),                       # ICU count
        deaths=("outcome", lambda x: (x == "dead").sum()),  # death count
    )
)

# Compute hospitalization rate: hospitalized ÷ tier count × 100 (as a %)
# Note: if a tier has n=0, this raises ZeroDivisionError;
# with real data, always confirm each group has at least 1 person before computing
classification["hosp_rate"] = (
    classification["hospitalized"] / classification["n"] * 100
).round(1)

print("=== Stratified by case classification ===")
# .to_string() with no arguments keeps the index (= case_classification names) for easy reference
print(classification.to_string())
```

<!-- video: ch04_06_generate_sitrep -->
<!-- /video -->

## Step 7: Output a structured SitRep

Wrap all of the above steps into a single function, and just rerun it each day to update:

```python
def generate_sitrep(csv_path):
    """Produce a SitRep summary dictionary from a CSV.

    Each day, just rerun this function with the latest CSV to auto-update every metric.
    It returns a dict rather than printing directly, because a dict can be consumed
    directly by the later Step 8 (report output).
    """
    df = pd.read_csv(csv_path)
    # Only convert the columns that actually need date arithmetic, to cut unnecessary work
    for col in ["symptom_onset_date", "hospitalization_date",
                "death_date", "notification_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

    total = len(df)
    # int() converts numpy.int64 to a native Python int
    # Why: pandas / numpy .sum() returns a numpy integer type (numpy.int64)
    # Putting that straight into a dict and serializing to JSON raises a JSON serialization error
    # Getting into the habit of wrapping with int() avoids some hard-to-predict type issues
    infected = int(df["infected"].sum())
    deaths = int((df["outcome"] == "dead").sum())

    return {
        "total_residents": total,
        "infected": infected,
        # round(value, decimals): round to the given number of decimal places
        "attack_rate": round(infected / total * 100, 1),
        "deaths": deaths,
        # guard: if infected == 0 (no cases yet), return 0 to avoid ZeroDivisionError
        "cfr": round(deaths / infected * 100, 1) if infected else 0,
        "hospitalized": int(df["hospitalized"].sum()),
        "icu": int(df["icu_admission"].sum()),
    }

sitrep = generate_sitrep("data/synthetic/legionella_outbreak.csv")
# sitrep is a Python dict, ready to hand to the report-output function in Step 8
print(sitrep)
```

<!-- video: ch04_07_report_output -->
<!-- /video -->

## Step 8: Produce a professional report

The dictionary returned by `generate_sitrep()` is your **data layer**. But your supervisor doesn't read Python dicts — they want a polished report. This step shows how to package the analysis into four professional output formats:

| Format | Best for | Python package |
|------|---------|------------|
| Interactive dashboard | Real-time viewing, internal team discussion | plotly (already installed) |
| Word document (.docx) | Handing to a manager, email attachment | python-docx |
| Presentation slides (.pptx) | Investigation meeting presentations | python-pptx |
| PDF report | Formal filing, printing | fpdf2 |

### Shared setup: save the chart and create the output folder

```python
import pathlib
from io import BytesIO
from datetime import datetime

# exist_ok=True: don't raise if the folder already exists (you can rerun this line safely)
pathlib.Path("output").mkdir(exist_ok=True)

# ── BytesIO: save the figure into an "in-memory virtual file" ──
# Normally fig.savefig("epicurve.png") writes to disk;
# BytesIO() opens a "fake file" in memory that behaves exactly like a real file object,
# but the data lives only in RAM — no disk space used, nothing to clean up afterward.
# Bonus: DOCX / PPTX add_picture() both accept BytesIO objects,
#        and the same figure can be reused (just remember to .seek(0) before each use).
epicurve_buf = BytesIO()
fig.savefig(epicurve_buf, format="png", dpi=150, bbox_inches="tight")
# seek(0): move the read cursor back to the very start of the buffer
# Analogy: rewind a tape to the beginning so you can play it from the top
# If you read without seek(0), you'd read from the end and get empty data
epicurve_buf.seek(0)

# strftime format string: %Y=4-digit year, %m=2-digit month, %d=2-digit day, %H=hour (24h), %M=minute
report_time = datetime.now().strftime("%Y-%m-%d %H:%M")
```

### 8a: Interactive dashboard (Plotly Dashboard)

```{note}
In JupyterLab / Google Colab, the chart below is **interactive** (you can zoom and hover to inspect values). In the static Jupyter Book web page, what you see is an auto-generated static screenshot.
```

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# make_subplots builds a 2×2 grid of subplots
# specs sets each subplot's type:
#   "indicator" = a numeric indicator (large-font KPI display)
#   "xy"        = an ordinary x-y plot (bar chart, line chart, etc.)
# subplot_titles map to each cell (top-left and top-right titles are left blank; the Indicators carry their own)
dashboard = make_subplots(
    rows=2, cols=2,
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}],
        [{"type": "xy"}, {"type": "xy"}],
    ],
    subplot_titles=("", "", "Epidemic curve (by onset date)", "Attack rate by wing"),
    vertical_spacing=0.15,   # vertical gap between top and bottom subplots (0–1, a ratio)
    horizontal_spacing=0.1,  # horizontal gap between left and right subplots
)

# ── Top-left: infected-count KPI indicator ──
# go.Indicator is Plotly's "dashboard indicator" shape, made to show one big number + supporting info
# mode="number+delta": show the value + a change amount (delta)
dashboard.add_trace(
    go.Indicator(
        mode="number+delta",
        value=infected,
        title={"text": "Infected (attack rate)"},
        # number.suffix appends text after the number (the attack rate in parentheses)
        number={"suffix": f"  ({infected/total:.1%})"},
        delta={"reference": 0, "position": "bottom"},
    ),
    row=1, col=1,  # place in row 1, column 1 (top-left)
)

# ── Top-right: death-count KPI indicator ──
dashboard.add_trace(
    go.Indicator(
        mode="number+delta",
        value=deaths,
        title={"text": "Deaths (CFR)"},
        number={"suffix": f"  ({deaths/infected:.1%})"},
        delta={"reference": 0, "position": "bottom"},
    ),
    row=1, col=2,  # place in row 1, column 2 (top-right)
)

# ── Bottom-left: epidemic curve (histogram-style bar chart) ──
daily_cases = cases.groupby("symptom_onset_date").size()
dashboard.add_trace(
    go.Bar(
        x=daily_cases.index,    # x-axis: onset date
        y=daily_cases.values,   # y-axis: daily case count
        marker_color="#D97757", # Anthropic Orange, visually tied to disease
        name="Daily cases",
    ),
    row=2, col=1,
)

# ── Bottom-right: attack rate by wing (horizontal bar chart, easy to compare wings) ──
dashboard.add_trace(
    go.Bar(
        y=wing_stats["label"],  # y-axis holds wing names (the category axis of a horizontal bar chart)
        x=wing_stats["AR%"],    # x-axis holds attack-rate values
        orientation="h",        # "h" = horizontal
        marker_color="#6A9BCC",
        name="Attack rate %",
        # show a value label just outside each bar
        text=wing_stats["AR%"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
    ),
    row=2, col=2,
)

dashboard.update_layout(
    title_text=f"Pine and Cypress Nursing Home Legionnaires' SitRep Dashboard ({report_time})",
    height=600,
    showlegend=False,     # hide the legend (the subplot titles are explanation enough)
    template="plotly_white",  # clean white-background template
)
dashboard.show()
```

### 8b: Word document (DOCX)

> **Note**: the package is named `python-docx`, but you import it as `from docx import ...` — a common source of confusion for beginners.

```python
# Note: the package is called python-docx (when installing), but the import name is docx (no python- prefix)
from docx import Document
from docx.shared import Inches, Pt  # Inches/Pt: helper classes for specifying sizes

# Document() creates a new blank Word document
doc = Document()

# ── Title and time ──
# level=1 maps to Word's "Heading 1" (the largest heading)
doc.add_heading("Pine and Cypress Nursing Home Legionnaires' SitRep", level=1)
doc.add_paragraph(f"Report time: {report_time}")
doc.add_paragraph(
    f"Data source: legionella_outbreak.csv ({total} resident records)"
)

# ── Summary metrics table ──
doc.add_heading("Summary metrics", level=2)
# add_table(rows=6, cols=2): create a 6-row, 2-column table
# style="Light Grid Accent 1": apply Word's built-in table style (light grid, accent color 1)
table = doc.add_table(rows=6, cols=2, style="Light Grid Accent 1")
metrics = [
    ("Total residents", str(total)),
    ("Infected", f"{infected} (attack rate {infected/total:.1%})"),
    ("Confirmed", str(confirmed)),
    ("Probable", str(probable)),
    ("Hospitalized", f"{hospitalized} (hospitalization rate {hospitalized/infected:.1%})"),
    ("Deaths", f"{deaths} (CFR {deaths/infected:.1%})"),
]
# enumerate() gives both the index i and the value (label, value)
for i, (label, value) in enumerate(metrics):
    # table.rows[i] gets row i, .cells[0] gets cell 0 (the first column)
    table.rows[i].cells[0].text = label
    table.rows[i].cells[1].text = value

# ── Embed the epidemic curve ──
doc.add_heading("Epidemic curve", level=2)
epicurve_buf.seek(0)  # reset the BytesIO read cursor (always seek(0) before each read)
# width=Inches(6): set the image width to 6 inches (A4 is ~8.27 inches wide; ~6 after margins)
doc.add_picture(epicurve_buf, width=Inches(6))

# ── Per-wing stats (header + data rows) ──
doc.add_heading("Outbreak summary by wing", level=2)
# rows=len(wing_stats) + 1: number of data rows + 1 header row
wing_table = doc.add_table(
    rows=len(wing_stats) + 1, cols=5, style="Light Grid Accent 1"
)
headers = ["Wing", "Residents", "Infected", "AR%", "CFR%"]
# fill in row 0 (the header)
for j, h in enumerate(headers):
    wing_table.rows[0].cells[j].text = h
# fill in the data rows (starting from row 1; i is the wing_stats index)
for i, row in wing_stats.iterrows():
    wing_table.rows[i + 1].cells[0].text = str(row["label"])
    wing_table.rows[i + 1].cells[1].text = str(row["residents"])
    wing_table.rows[i + 1].cells[2].text = str(row["infected"])
    wing_table.rows[i + 1].cells[3].text = str(row["AR%"])
    wing_table.rows[i + 1].cells[4].text = str(row["CFR%"])

doc.save("output/sitrep_report.docx")
print("✅ Word report saved: output/sitrep_report.docx")
```

### 8c: Presentation slides (PPTX)

```python
from pptx import Presentation
from pptx.util import Inches, Pt  # Inches/Pt: helper classes for specifying position and size

prs = Presentation()  # create a new blank PPTX (defaults to 16:9 slides)

# ── Slide 1: title page ──
# slide_layouts[0] is PowerPoint's "Title Slide" layout (title + subtitle placeholders)
slide1 = prs.slides.add_slide(prs.slide_layouts[0])
slide1.shapes.title.text = "Pine and Cypress Nursing Home Legionnaires' SitRep"
# placeholders[1] is the subtitle placeholder (index 0 = main title, index 1 = subtitle)
slide1.placeholders[1].text = f"Report time: {report_time}"

# ── Slide 2: key figures ──
# slide_layouts[5] is the "Blank" layout with no placeholders;
# we position everything ourselves with add_textbox()
slide2 = prs.slides.add_slide(prs.slide_layouts[5])
# add_textbox(left, top, width, height): specify position and size with Inches
# left margin 1 inch, top margin 0.5 inch, width 8 inches, height 1 inch
txBox = slide2.shapes.add_textbox(
    Inches(1), Inches(0.5), Inches(8), Inches(1),
)
txBox.text_frame.text = "Key summary metrics"
txBox.text_frame.paragraphs[0].font.size = Pt(28)  # 28 pt heading
txBox.text_frame.paragraphs[0].font.bold = True

# Body text box (placed below the heading)
body = slide2.shapes.add_textbox(
    Inches(1), Inches(1.8), Inches(8), Inches(4),
)
tf = body.text_frame
tf.word_wrap = True  # allow word wrapping (prevents long text from overflowing)
kpi_lines = [
    f"Infected: {infected} (attack rate {infected/total:.1%})",
    f"Confirmed: {confirmed}   Probable: {probable}",
    f"Hospitalized: {hospitalized}   ICU: {icu}",
    f"Deaths: {deaths} (CFR {deaths/infected:.1%})",
]
for line in kpi_lines:
    p = tf.add_paragraph()   # add a new paragraph per line
    p.text = line
    p.font.size = Pt(20)     # 20 pt body text
    p.space_after = Pt(12)   # 12 pt space after the paragraph (like pressing Enter once)

# ── Slide 3: epidemic curve ──
slide3 = prs.slides.add_slide(prs.slide_layouts[5])
txBox3 = slide3.shapes.add_textbox(
    Inches(1), Inches(0.3), Inches(8), Inches(0.8),
)
txBox3.text_frame.text = "Epidemic curve (by onset date)"
txBox3.text_frame.paragraphs[0].font.size = Pt(24)
txBox3.text_frame.paragraphs[0].font.bold = True

epicurve_buf.seek(0)  # reset the BytesIO cursor to read the image data again
# add_picture(image, left, top, width, height): insert the image at a set position
slide3.shapes.add_picture(epicurve_buf, Inches(0.5), Inches(1.3), Inches(9), Inches(5))

# ── Slide 4: attack rate by wing ──
slide4 = prs.slides.add_slide(prs.slide_layouts[5])
txBox4 = slide4.shapes.add_textbox(
    Inches(1), Inches(0.3), Inches(8), Inches(0.8),
)
txBox4.text_frame.text = "Outbreak summary by wing"
txBox4.text_frame.paragraphs[0].font.size = Pt(24)
txBox4.text_frame.paragraphs[0].font.bold = True

# add_table(rows, cols, left, top, width, height).table gets the table object
# The full call chain: add_table() returns a GraphicFrame; .table is the operable Table object
rows_n = len(wing_stats) + 1  # data rows + 1 header row
tbl = slide4.shapes.add_table(rows_n, 5, Inches(0.5), Inches(1.3), Inches(9), Inches(4)).table
# fill in the header (row 0)
for j, h in enumerate(["Wing", "Residents", "Infected", "AR%", "CFR%"]):
    tbl.cell(0, j).text = h
# fill in the data rows (starting from row 1)
for i, row in wing_stats.iterrows():
    tbl.cell(i + 1, 0).text = str(row["label"])
    tbl.cell(i + 1, 1).text = str(row["residents"])
    tbl.cell(i + 1, 2).text = str(row["infected"])
    tbl.cell(i + 1, 3).text = str(row["AR%"])
    tbl.cell(i + 1, 4).text = str(row["CFR%"])

prs.save("output/sitrep_slides.pptx")
print("✅ Slides saved: output/sitrep_slides.pptx")
```

### 8d: Formal PDF report (fpdf2)

```python
import pathlib
from fpdf import FPDF

# ── CJK font detection (unlike a browser, a PDF can't auto-fallback; you must embed the font) ──
# By default fpdf2 only has Latin fonts (Helvetica, etc.); showing CJK needs an embedded TTF/TTC font
# Detection logic: scan the system font directories for a font file whose name contains "CJK", "WenQuanYi", or "wqy"
cjk_font_path = None
for font_dir in ["/usr/share/fonts", "/usr/local/share/fonts"]:
    for fp in sorted(pathlib.Path(font_dir).rglob("*")):
        if fp.suffix.lower() in {".ttf", ".ttc"} and (
            "CJK" in fp.name or "WenQuanYi" in fp.name or "wqy" in fp.name
        ):
            cjk_font_path = str(fp)
            break
    if cjk_font_path:
        break

pdf = FPDF()        # create a new PDF (defaults to A4 portrait)
pdf.add_page()      # you must add_page() first before you can write any content

# ── Font setup ──
if cjk_font_path:
    # add_font("alias", "style", "font file path")
    # the alias is up to you; call it later with set_font("CJK")
    # Note: fpdf2 v2.5.1+ doesn't need uni=True (Unicode is supported automatically)
    pdf.add_font("CJK", "", cjk_font_path)
    pdf.set_font("CJK", size=16)
else:
    pdf.set_font("Helvetica", size=16)
    print("⚠️ No CJK font found; Chinese may not display. Please install fonts-noto-cjk")

# ── Title ──
# cell(width, height, text, ...) is fpdf2's most basic content unit
# width=0 means "extend to the right margin" (auto-fill the page width)
# new_x="LMARGIN": the next cell starts at the left margin (back to the left)
# new_y="NEXT": the next cell moves to the next line
# align="C": center the text within the cell
pdf.cell(0, 12, text="Pine and Cypress Nursing Home Legionnaires' SitRep", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font_size(10)
pdf.cell(0, 8, text=f"Report time: {report_time}", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(8)  # ln(n): insert n points of blank line (layout spacing)

# ── Summary metrics (line by line) ──
pdf.set_font_size(13)
pdf.cell(0, 10, text="Summary metrics", new_x="LMARGIN", new_y="NEXT")
pdf.set_font_size(10)
kpi_lines = [
    f"Total residents: {total}",
    f"Infected: {infected} (attack rate {infected/total:.1%})",
    f"Confirmed: {confirmed}   Probable: {probable}",
    f"Hospitalized: {hospitalized} (hospitalization rate {hospitalized/infected:.1%})",
    f"Deaths: {deaths} (CFR {deaths/infected:.1%})",
]
for line in kpi_lines:
    pdf.cell(0, 7, text=line, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

# ── Embed the epidemic curve ──
# fpdf2's pdf.image() only accepts a "file path" string, not a BytesIO object
# Workaround: write the BytesIO contents to a temporary PNG, embed it, then delete it
pdf.set_font_size(13)
pdf.cell(0, 10, text="Epidemic curve", new_x="LMARGIN", new_y="NEXT")
epicurve_buf.seek(0)
epicurve_tmp = pathlib.Path("output/epicurve_tmp.png")
epicurve_tmp.write_bytes(epicurve_buf.read())  # write the BytesIO data to disk
# pdf.w is the page width (~210 mm); subtracting 30 leaves 15 mm margins on each side
pdf.image(str(epicurve_tmp), w=pdf.w - 30)
epicurve_tmp.unlink()  # delete the temp file after embedding (clean up)
pdf.ln(5)

# ── Per-wing stats table (manually drawn gridded table) ──
pdf.add_page()  # add a second page for the table
pdf.set_font_size(13)
pdf.cell(0, 10, text="Outbreak summary by wing", new_x="LMARGIN", new_y="NEXT")
pdf.set_font_size(9)

# col_widths defines each column's width (mm); the total should be less than the effective page width (~190 mm)
col_widths = [25, 25, 25, 30, 30]
headers = ["Wing", "Residents", "Infected", "AR%", "CFR%"]
# header row: border=1 draws all four borders
for w, h in zip(col_widths, headers):
    pdf.cell(w, 8, text=h, border=1, align="C")
pdf.ln()  # line break after the header

# data rows: _ means we don't need the index (just the value, row)
for _, row in wing_stats.iterrows():
    vals = [str(row["label"]), str(row["residents"]), str(row["infected"]),
            str(row["AR%"]), str(row["CFR%"])]
    for w, v in zip(col_widths, vals):
        pdf.cell(w, 7, text=v, border=1, align="C")
    pdf.ln()  # line break after each data row

pdf.output("output/sitrep_report.pdf")
print("✅ PDF report saved: output/sitrep_report.pdf")
```

> **In summary**: the four formats each suit a different scenario. An interactive dashboard is good for real-time internal review, DOCX for emailing to a supervisor, PPTX for presenting at an investigation meeting, and PDF for formal filing. In practice, you can fold this code into `run_sitrep.py` and, after updating the CSV each day, rerun it once to produce the latest report in all four formats at the same time.

---

## FETP Step 6: Form hypotheses — from descriptive analysis to causal inference

Once you've described person, time, and place (Steps 3–5) and produced the SitRep, the next step is to **propose testable hypotheses**: who is the source? what is the transmission route?

### Three routes to generating hypotheses

```
Route 1: known pathogen characteristics
  Confirmed as Legionnaires' → transmission route is known to be aerosol
  → Hypothesis: "some water source in the facility is contaminated with Legionella"
  → Possible sources: cooling tower, shower equipment, hydrotherapy pool, humidifier

Route 2: descriptive-epidemiology clues
  The epidemic curve shows a point-source pattern (concentrated within 3–5 days) → a single exposure source
  The map shows Wing A's attack rate is notably higher than B/C → spatial clustering
  → Hypothesis: "some facility in Wing A is the point source"

Route 3: case interviews + outlier analysis
  Differences in habits between uninfected residents (controls) and infected residents (cases)
  A 90-year-old resident, immune-competent but uninfected → asked: "doesn't use the shower, uses a bathing bed instead"
  → Refined hypothesis: "shower aerosol is the main exposure route, not merely drinking water"
```

### Initial hypothesis list for this cluster

| Hypothesis # | Content | Supporting clues |
|----------|----------|-----------|
| H1 | The cooling tower is contaminated; aerosol spreads to Wing A windows | High attack rate in Wing A; the cooling tower sits on the Wing A side |
| H2 | Standing water in Wing A's shower equipment is contaminated | Higher attack rate among shower users than non-users (to be verified) |
| H3 | The hydrotherapy pool is the source | Higher incidence among residents who used hydrotherapy (to be verified) |

> **Note**: hypotheses should be written down explicitly **before** the sampling / analysis results come in. Modifying a hypothesis afterward to "fit" the data invalidates the study design (see the FETP Step 7 analysis).

---

## FETP Step 7: Evaluate hypotheses — traceback and trace-forward

After forming hypotheses, you validate them with **analytic epidemiology** and **environmental sampling**.

### Traceback — find the source

**Concept**: from the case onset dates, work backward to find which exposure point is most likely the source.

```
Traceback window = maximum incubation period
Legionnaires' maximum incubation period = 10 days

This cluster:
  Earliest onset date = 2026-01-12
  Latest onset date = 2026-01-28
  
  → Traceback window = 2026-01-02 to 2026-01-28
  → During this window, check every possible aerosol exposure point (towers, showers, hydrotherapy pool)
```

**Environmental sampling priorities**:
- Collect water samples from the cooling tower, shower heads, hydrotherapy pool, and water heater
- Goal: confirm whether the *Legionella* species in the environment matches the residents' strain (serogroup comparison)
- Sampling timing: as early as possible, but disinfection (chlorination) should only start after sampling

**Statistical methods** (see Ch05 / Ch06):

| Analysis method | Hypothesis type | Application here |
|----------|----------|----------|
| Case-control study + odds ratio | Retrospective exposure comparison | Compare shower / hydrotherapy use rates between infected and uninfected |
| Cohort study + risk ratio | Known exposure, follow up for onset | If you can identify residents who "used Wing A showers" vs "did not" |
| Stratified analysis (Mantel-Haenszel) | Adjust for confounders | The exposure effect after adjusting for age / immune status |

### Trace-forward — assess the risk of spread

**Concept**: from a case's infectious period, work forward to track possible secondary cases.

```
Legionnaires': person-to-person is extremely rare → trace-forward is usually unnecessary
  ✗ No need to build a contact list for each case
  ✗ No need to set up a contact health-monitoring window

If the pathogen were COVID-19 / influenza / norovirus (person-to-person):
  Trace-forward period = infectious period (e.g. 2–14 days after COVID-19 infection)
  → You'd need to list close contacts + set a health-monitoring window
```

> **Investigation strategy for Legionnaires'**: concentrate resources on **traceback** (environmental sampling + analytic studies); there's no need to build a contact-tracing system.

```{seealso}
Python implementation of Mantel-Haenszel stratified analysis and odds-ratio calculation → {doc}`05_stratified`

Multivariable logistic regression (adjusting for multiple confounders) → {doc}`06_logistic_regression`
```

---

## FETP Step 9: Break the chain of infection — remove the source, break the chain, protect the host

Once you have hypotheses and analysis results, control measures can't wait. The ultimate goal of an outbreak investigation is to **interrupt transmission**, not just write a pretty report.

### The three intervention points in the chain of infection

Following the six-element chain-of-infection framework in {ref}`appendix-g-chain-of-infection`, intervention points fall into three categories:

| Intervention type | Strategy | Application to Legionnaires' |
|----------|------|----------------|
| **Remove the source** | Eliminate or isolate the pathogen | Immediately chlorinate the cooling tower (≥2 ppm residual chlorine), drain standing water |
| **Break the transmission route** | Cut off aerosol generation | Shut down suspect showers, suspend hydrotherapy pool service, install 60°C hot-water circulation |
| **Protect susceptible hosts** | Reduce host susceptibility | Move immunosuppressed residents (cancer / organ transplant) to an unaffected wing, assess prophylactic antibiotics |

### Concrete steps for Legionnaires'

```
Immediate measures (within 24 hours of detecting the cluster):
  1. Shut down suspect water sources (close showers, suspend hydrotherapy pool)
  2. Notify the local health bureau + CDC (Legionnaires' is a Category 3 notifiable disease)
  3. Start antibiotic treatment for symptomatic cases (azithromycin or levofloxacin)

Short-term measures (48–72 hours):
  4. Send environmental samples (towers, pipes) for testing
  5. Shock-chlorinate the cooling tower
  6. Perform thermal disinfection of the whole plumbing system (flush with hot water ≥60°C)

Long-term measures (after the cluster is resolved):
  7. Establish a regular water-quality monitoring program (quarterly sampling)
  8. Develop a facility Water Management Program (WMP)
  9. Train infection-control staff to recognize early symptoms
```

### Sequencing measures alongside the investigation

```{admonition} Important reminder
:class: warning
Control measures (chlorination) should be **started immediately** — no need to wait for the investigation to finish. But environmental sampling **must be done before disinfection**, or you won't be able to compare the water samples with the case strains afterward.

Correct order: sample → disinfect → keep monitoring
```

```{seealso}
A full diagram of the six-element chain of infection and the isolation vs quarantine definitions → {ref}`appendix-g-chain-of-infection`
```

---

## Common mistakes

1. **Changing the definition every day**: once the case definition is set, don't change it, or the trend won't be comparable
2. **Charts only, no tables**: a SitRep must have auditable tables of numbers
3. **Forgetting to note the data cutoff time**: every report must state "data as of YYYY-MM-DD HH:MM"
4. **Attack rate without a denominator**: comparing raw case counts isn't fair; divide by each wing's resident count

## Step 9: Schedule automatic updates

Your supervisor's request is clear: **every morning at 9 a.m., there should be an up-to-date SitRep in the inbox.** But manually opening the notebook every day, clicking Run All, waiting for it to finish, then emailing it out… you'll probably forget by day three. The solution: let the computer run it for you.

### 9a: Prepare the scheduling script

Step 7's `generate_sitrep()` and Step 8's report output are run interactively inside the notebook. To automate them on a schedule, you need to consolidate them into a standalone `.py` script. Here's an example script structure suited to scheduling:

```python
#!/usr/bin/env python3
"""Daily SitRep automatic generation script.

Usage (manual run):
    uv run python notebooks/run_sitrep.py

When run on a schedule, use absolute paths:
    /Users/yourname/.local/bin/uv run python /Users/yourname/projects/python4epi/notebooks/run_sitrep.py
"""
import logging
from pathlib import Path
from datetime import datetime

# ── Use pathlib to compute the absolute path of the project root ──
# __file__ is the path of "this script itself"
# .resolve() turns a relative path into an absolute one (e.g. ~/projects → /Users/xxx/projects)
# .parent goes up one level: run_sitrep.py → notebooks/ → project root
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "synthetic" / "legionella_outbreak.csv"
OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Set up logging (instead of print) ──
# When it runs on a schedule you're not at the computer, so print output vanishes into the void
# logging can write to a file, so you can go back later and check "did yesterday's run finish?"
LOG_PATH = OUTPUT_DIR / "sitrep.log"
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

def main():
    """Main logic: read the CSV → compute metrics → produce the report."""
    log.info("Starting SitRep generation...")

    # Put the core logic of Steps 1–8 here
    # sitrep = generate_sitrep(str(DATA_PATH))
    # ... produce DOCX / PDF, etc. ...

    # Timestamp the output filename for easy filing
    today = datetime.now().strftime("%Y%m%d")
    output_path = OUTPUT_DIR / f"sitrep_{today}.pdf"
    log.info(f"Report saved: {output_path}")

if __name__ == "__main__":
    # Wrap the main logic in try/except: if it fails, the error is written to the log instead of vanishing silently
    try:
        main()
    except Exception:
        log.exception("SitRep generation failed!")
        raise  # re-raise the exception so the scheduler knows "this run failed"
```

```{tip}
**Three ways to turn a notebook into a `.py` script** are covered in {doc}`Ch00 Developer Tools <00_guide>`. This course's `notebooks/run_sitrep.py` is a tidied-up example.
```

### 9b: macOS: launchd (recommended)

macOS's native scheduler is **launchd** (not cron). macOS does have cron, but recent versions impose security restrictions on it, and launchd is the officially recommended approach.

Create a plist config file `~/Library/LaunchAgents/com.epi.sitrep.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Label: the unique identifier name for this scheduled task -->
    <key>Label</key>
    <string>com.epi.sitrep</string>

    <!-- ProgramArguments: the command to run (same as what you'd type in the terminal) -->
    <!-- Each "space-separated part" is one <string>; you can't put them all in one -->
    <key>ProgramArguments</key>
    <array>
        <!-- ⚠️ Must use absolute paths! Use `which uv` to find where your uv lives -->
        <string>/Users/yourname/.local/bin/uv</string>
        <string>run</string>
        <string>python</string>
        <string>/Users/yourname/projects/python4epi/notebooks/run_sitrep.py</string>
    </array>

    <!-- WorkingDirectory: the working directory at run time (like cd-ing here first) -->
    <key>WorkingDirectory</key>
    <string>/Users/yourname/projects/python4epi</string>

    <!-- StartCalendarInterval: the schedule time (every day at 9:00 a.m.) -->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <!-- Log output paths (stdout and stderr stored separately) -->
    <key>StandardOutPath</key>
    <string>/Users/yourname/projects/python4epi/output/launchd_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/yourname/projects/python4epi/output/launchd_stderr.log</string>
</dict>
</plist>
```

Once set up, run these three steps:

```bash
# 1. Copy the plist into the LaunchAgents directory (skip if you created it there directly)
cp com.epi.sitrep.plist ~/Library/LaunchAgents/

# 2. Load the schedule (it will run automatically starting from the next 09:00)
launchctl load ~/Library/LaunchAgents/com.epi.sitrep.plist

# 3. Confirm it loaded successfully (you should see com.epi.sitrep)
launchctl list | grep epi
```

To remove the schedule:

```bash
launchctl unload ~/Library/LaunchAgents/com.epi.sitrep.plist
```

### 9c: Linux: cron

The most common scheduling tool on Linux is **cron**. Open the editor with `crontab -e` and add a line:

```bash
# Open the cron schedule editor
crontab -e

# Add the following line (runs every day at 9 a.m.)
0 9 * * * cd /home/yourname/projects/python4epi && /home/yourname/.local/bin/uv run python notebooks/run_sitrep.py >> output/sitrep_cron.log 2>&1
```

What the five fields mean:

```
0 9 * * *
│ │ │ │ │
│ │ │ │ └── day of week (* = every day, 0=Sunday, 1=Monday ...)
│ │ │ └──── month (* = every month)
│ │ └────── day of month (* = every day)
│ └──────── hour (9 = 9 a.m., 24-hour clock)
└────────── minute (0 = on the hour)
```

```{warning}
**The cron PATH trap:** cron's environment variables differ from those in your terminal. `uv` may not be on cron's PATH, causing `command not found`.

**Fix 1**: use `uv`'s absolute path (find it first with `which uv`, e.g. `/home/yourname/.local/bin/uv`).

**Fix 2**: add a PATH setting at the top of the crontab:
```bash
# Add this line at the very top of crontab -e
PATH=/home/yourname/.local/bin:/usr/local/bin:/usr/bin:/bin
```
```

### 9d: Windows 11: Task Scheduler

Windows has a built-in "Task Scheduler" that you can configure via the GUI or the command line.

**GUI method (4 steps):**

1. Press `Win` and search for "Task Scheduler", then open it
2. On the right, click "**Create Basic Task**" → name it `SitRep daily update`
3. Trigger: choose "**Daily**" → set the time to `09:00:00`
4. Action: choose "**Start a program**" → fill in the following:
   - Program/script: `cmd`
   - Add arguments: `/c cd /d C:\Users\yourname\projects\python4epi && uv run python notebooks\run_sitrep.py`

**Command-line method (one line):**

```powershell
schtasks /create /tn "SitRep_Daily" /tr "cmd /c cd /d C:\Users\yourname\projects\python4epi && uv run python notebooks\run_sitrep.py" /sc daily /st 09:00
```

What each flag means:

| Flag | Description |
|------|------|
| `/create` | Create a new scheduled task |
| `/tn "SitRep_Daily"` | Task Name |
| `/tr "..."` | The command to run (Task Run) |
| `/sc daily` | Schedule frequency: daily |
| `/st 09:00` | Start Time: 9 a.m. |

To delete the schedule:

```powershell
schtasks /delete /tn "SitRep_Daily" /f
```

### Common scheduling problems

| Problem | Cause | Fix |
|------|------|------|
| `command not found: uv` | The scheduler's PATH differs from the terminal's | Use `which uv` (Mac/Linux) or `where uv` (Windows) to find the absolute path |
| Can't find the CSV file | The working directory isn't the project root | Compute an absolute path in the script with `Path(__file__).resolve().parent` |
| Runs but no output appears | stdout/stderr not redirected | cron: `>> log 2>&1`; launchd: set `StandardOutPath` |
| macOS blocks permissions | Security restriction | System Settings → Privacy & Security → grant "Terminal" **Full Disk Access** |
| Windows task doesn't run | The computer was asleep | Task Scheduler → Conditions → uncheck "Start the task only if the computer is on AC power" |

```{tip}
**Advanced combo:** once the scheduling script is ready, pair it with the Git version control from Ch13 (Reproducible Research) — auto-commit the output after each scheduled run, so you don't just have the latest report but a full history you can go back through.
```

## Practice notebooks

- Class notes: {ref}`04_outbreak_workflow.ipynb`
- Exercise version: [`04_outbreak_workflow_exercise.ipynb`](exercises/04_outbreak_workflow_exercise.ipynb)
- Solution version (instructor): [`04_outbreak_workflow_solution.ipynb`](solutions/04_outbreak_workflow_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/04_outbreak_workflow_solution.ipynb>)
