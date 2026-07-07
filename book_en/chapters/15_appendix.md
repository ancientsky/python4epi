# 15 Appendix

## A. Epidemiology Glossary (English–Chinese)

### General epidemiology

| English | Taiwan translation | Description |
|------|---------|------|
| Attack rate (AR) | 侵襲率 | New cases during a defined period / exposed population |
| Case fatality rate (CFR) | 致死率 | Deaths / infected persons |
| Risk ratio (RR) | 風險比 | Attack rate in the exposed / attack rate in the unexposed |
| Odds ratio (OR) | 勝算比 | Odds of infection in the exposed / odds of infection in the unexposed |
| Confidence interval (CI) | 信賴區間 | Range of uncertainty around a parameter estimate |
| Incidence rate | 發生率 | New cases per unit of person-time |
| Prevalence | 盛行率 | Proportion of existing cases at a point in time |
| Epidemic curve | 流行曲線 | Time distribution of cases plotted by date of onset |
| Outbreak / cluster | 群聚 | An unusual aggregation of cases at a specific time and place |
| Surveillance | 監測 | Systematic collection and analysis of health data |
| Case notification | 通報 | Reporting a case to the health authorities |
| Epidemiological investigation | 疫調 / 流行病學調查 | Systematic investigation of a cluster event |
| Basic reproduction number (R₀) | 基本再生數 | Average number of people one case infects in a fully susceptible population |
| Sensitivity | 敏感度 | True positive rate (test metric) |
| Specificity | 特異度 | True negative rate (test metric) |
| Exposure | 暴露 | Contact with a risk factor |
| Confounding | 干擾作用 | A third variable that affects both the exposure and the outcome |
| Stratified analysis | 分層分析 | Analyzing separately within groups defined by a potential confounder |
| Attributable risk (AR) | 歸因風險 | Risk in the exposed − risk in the unexposed |
| Population attributable risk (PAR) | 族群歸因風險 | The proportion of population risk attributable to the exposure |

### Legionnaires' disease

| English | Chinese | Description |
|------|------|------|
| Legionnaires' disease | 退伍軍人症 | Severe pneumonia caused by *Legionella* bacteria |
| *Legionella pneumophila* | 退伍軍人桿菌 / 嗜肺性退伍軍人桿菌 | The pathogen |
| Pontiac fever | 龐提亞克熱 | A milder, self-limiting illness caused by *Legionella* |
| Cooling tower | 冷卻水塔 | A common site where *Legionella* proliferates |
| Biofilm | 生物膜 | A film of microorganisms attached to pipe walls |
| Water system disinfection | 水系統消毒 | Heating (>70°C) or chlorination |
| Urinary antigen test | 尿液抗原檢測 | A rapid diagnostic tool for Legionnaires' disease |

### Survival analysis

| English | Chinese | Description |
|------|------|------|
| Kaplan-Meier estimator | Kaplan-Meier 估計式 | Non-parametric method for estimating the survival function |
| Log-rank test | Log-rank 檢定 | Statistical test comparing survival curves between two groups |
| Cox proportional hazards | Cox 等比例風險模型 | Semi-parametric survival regression model |
| Hazard ratio (HR) | 風險比（存活分析） | The effect size of an exposure in a Cox model; shares the Chinese term with RR, used in the survival-analysis context |
| Censoring | 設限 / 截斷 | The event has not yet occurred when observation ends |
| Time-to-event | 事件時間 | Time from origin to the occurrence of the event |

---

## B. Pine & Cypress Nursing Home Dataset Column Dictionary

File: `data/synthetic/legionella_outbreak.csv` (280 rows × 32 columns)

### Demographics and housing

| Column | Type | Range | Description |
|------|------|------|------|
| `case_id` | str | R001–R280 | Resident ID |
| `age` | int | 60–98 | Age |
| `sex` | str | M / F | Sex |
| `floor` | int | 1 / 2 / 3 | Floor |
| `wing` | str | A / B | Wing |
| `room` | str | e.g. 1A-01 | Room number |
| `bed` | int | 1 / 2 | Bed number |
| `facility_admission_date` | date | — | Date admitted to the facility |

### Comorbidities and health status

| Column | Type | Range | Description |
|------|------|------|------|
| `comorbidity_chf` | int | 0 / 1 | Congestive heart failure |
| `comorbidity_dm` | int | 0 / 1 | Diabetes mellitus |
| `comorbidity_cancer` | int | 0 / 1 | Cancer |
| `comorbidity_copd` | int | 0 / 1 | Chronic obstructive pulmonary disease |
| `immunosuppressed` | int | 0 / 1 | Immunosuppressed |
| `smoking_history` | str | never / former / current | Smoking history |
| `functional_status` | str | independent / assisted / bedridden | Ability to perform daily activities |

### Exposure factors

| Column | Type | Range | Description |
|------|------|------|------|
| `shower_use` | int | 0 / 1 | Whether the resident used the shower |
| `hydrotherapy_use` | int | 0 / 1 | Whether the resident used the hydrotherapy pool |

### Clinical and outcomes

| Column | Type | Range | Description |
|------|------|------|------|
| `clinical_severity` | str | not_ill / asymptomatic / mild / moderate / severe | Clinical severity |
| `symptom_onset_date` | date | — | Symptom onset date (blank for those not infected) |
| `fever` | int | 0 / 1 | Fever |
| `cough` | int | 0 / 1 | Cough |
| `dyspnea` | int | 0 / 1 | Shortness of breath |
| `confusion` | int | 0 / 1 | Confusion |
| `diarrhea` | int | 0 / 1 | Diarrhea |
| `lab_confirmed` | int | 0 / 1 | Laboratory-confirmed |
| `case_classification` | str | not_a_case / probable / confirmed | Case classification |
| `hospitalized` | int | 0 / 1 | Whether hospitalized |
| `hospitalization_date` | date | — | Hospitalization date |
| `icu_admission` | int | 0 / 1 | Whether admitted to the ICU |
| `outcome` | str | survived / dead | Outcome |
| `death_date` | date | — | Date of death (blank for survivors) |
| `notification_date` | date | — | Notification date |

---

## C. Package Quick Reference

### Core packages

| Package | Purpose | Chapters |
|------|------|------|
| `pandas` | Data manipulation | Whole book |
| `numpy` | Numerical computing | Whole book |
| `matplotlib` | Basic plotting | Ch02+ |
| `seaborn` | Statistical charts | Ch03+ |
| `scipy.stats` | Chi-square and other statistical tests | Ch03, Ch05 |
| `statsmodels` | Logistic regression, OLS | Ch06, Ch12 |
| `plotly` | Interactive charts, choropleths | Ch08 |

### Advanced packages

| Package | Purpose | Chapters |
|------|------|------|
| `lifelines` | Kaplan-Meier, Cox PH survival analysis | Ch09 |
| `scikit-learn` | ML pipelines, RF, cross-validation | Ch10 |
| `torch` | PyTorch deep learning | Ch11 |

### Common commands

```bash
# Environment management
uv sync                         # Install all dependencies
uv run pytest                   # Run tests
uv run jupyter lab              # Start Jupyter Lab

# Building the book
uv run jupyter-book build book/ # Build the Jupyter Book

# Version control
git status                      # View changes
git add <file>                  # Stage changes
git commit -m "message"         # Commit
```

---

## D. Troubleshooting Common Errors

| Problem | Likely cause | Fix |
|------|---------|------|
| `ModuleNotFoundError` | Package not installed | `uv sync` |
| `FileNotFoundError: legionella_outbreak.csv` | Wrong working directory | Make sure you run from the project root |
| `KeyError: 'column_name'` | Misspelled column name | Check the correct names with `df.columns` |
| Variables disappear after the notebook kernel restarts | Kernel state was reset | Re-run all cells from the top |
| `SettingWithCopyWarning` | Assigning to a slice | Use `.copy()` or `.loc` |
| Date columns can't be computed | Not converted to datetime | `pd.to_datetime(df["col"])` |
| Chinese characters show as boxes | matplotlib is missing a CJK font | See [E. Chinese chart display troubleshooting](#e-chinese-chart-display-troubleshooting-matplotlib--plotly) below |
| Plotly charts are blank in Jupyter Book | Wrong renderer setting | See [E. Chinese chart display troubleshooting](#e-chinese-chart-display-troubleshooting-matplotlib--plotly) below |

---

## E. Chinese Chart Display Troubleshooting (matplotlib & Plotly)

When using Traditional Chinese labels, matplotlib and Plotly each have their own traps. This section records the pitfalls this book actually ran into across CI/CD and local environments, along with the fixes.

### E-1. Matplotlib: Chinese shows as boxes □□□

#### Symptom

The chart's Chinese titles and axis labels all show as empty boxes, accompanied by a flood of UserWarnings:

```
UserWarning: Glyph 30332 (\N{CJK UNIFIED IDEOGRAPH-767C}) missing from font(s) DejaVu Sans.
```

This means matplotlib can't find any font capable of displaying CJK characters, and falls back to the default DejaVu Sans (which has no Chinese glyphs).

#### Root cause: the `.ttc` font collection's face-0 trap

This is a **very easy trap to overlook**. On a Linux CI environment (such as GitHub Actions), after installing `fonts-noto-cjk` the system gets `NotoSansCJK-Regular.ttc` — this is a **TrueType Collection** (`.ttc`), a single file containing multiple font variants:

| Face index | Font name | Language |
|-----------|---------|------|
| 0 | Noto Sans CJK JP | Japanese (default) |
| 1 | Noto Sans CJK KR | Korean |
| 2 | Noto Sans CJK SC | Simplified Chinese |
| 3 | Noto Sans CJK TC | Traditional Chinese |
| 4 | Noto Sans CJK HK | Hong Kong Traditional |

**The problem:** when matplotlib's `fontManager.addfont()` processes a `.ttc` file, it **only registers face 0** (the Japanese variant, "Noto Sans CJK JP"). If your `font.sans-serif` candidate list only contains `"Noto Sans CJK TC"`, matplotlib will never find it — because TC was never registered.

```
The list you wrote          Fonts matplotlib knows about
─────────────────         ──────────────────
"Noto Sans CJK TC" ──✗    "Noto Sans CJK JP" ← only face 0 is registered
"Noto Sans TC"     ──✗
"WenQuanYi Zen Hei"──✗    (CI didn't install this package)
"SimHei"           ──✗
                   ↓
              all miss → fall back to DejaVu Sans → □□□
```

#### Fixes

**Method 1 (simplest): list every Noto Sans CJK variant as a candidate**

No matter which language face 0 is, if you list JP, KR, SC, TC, and HK all together, one of them is bound to match:

```python
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC",    # Traditional Chinese (ideal choice)
    "Noto Sans CJK SC",    # Simplified Chinese (CJK characters are shared)
    "Noto Sans CJK JP",    # Japanese (face 0, always registered)
    "Noto Sans TC",
    "Microsoft JhengHei",  # Windows Microsoft JhengHei
    "WenQuanYi Zen Hei",   # Linux WenQuanYi
    "SimHei",
    "Arial Unicode MS",    # macOS
    "Heiti TC",            # macOS
    "DejaVu Sans",         # last resort (no Chinese)
]
plt.rcParams["axes.unicode_minus"] = False
plt.style.use("ggplot")
plt.rcParams["figure.dpi"] = 150
```

```{note}
All Noto Sans CJK variants cover the complete set of CJK Unified Ideographs; they differ only in the glyph-shape preferences of a few characters (for example, "直" looks slightly different in the Japanese and Traditional Chinese glyph forms). For chart labels this is more than sufficient.
```

**Method 2 (more robust): dynamically detect the registered font names**

After `addfont()`, scan `fontManager.ttflist` to find which CJK fonts were actually registered, and prefer those:

```python
import pathlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1) Scan for and register system CJK fonts
for font_dir in map(pathlib.Path, ["/usr/share/fonts", "/usr/local/share/fonts"]):
    if font_dir.exists():
        for fp in sorted(font_dir.rglob("*")):
            if fp.suffix.lower() in {".ttf", ".ttc", ".otf"} and (
                "CJK" in fp.name or "WenQuanYi" in fp.name or "wqy" in fp.name
            ):
                try:
                    fm.fontManager.addfont(str(fp))
                except Exception:
                    pass

# 2) Dynamically detect the names of the CJK fonts actually registered
discovered = []
for entry in fm.fontManager.ttflist:
    if any(kw in entry.name.lower() for kw in ("cjk", "wenquanyi", "wqy")):
        if entry.name not in discovered:
            discovered.append(entry.name)

# 3) Prefer the detected fonts, then append the static candidate list
preferred = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei", "WenQuanYi Zen Hei",
    "SimHei", "Arial Unicode MS", "Heiti TC",
]
candidates = list(discovered)
for name in preferred:
    if name not in candidates:
        candidates.append(name)

plt.rcParams["font.sans-serif"] = candidates + ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
```

This book's `epi_learning.viz.configure_chinese_font()` uses Method 2.

**Method 3: install fonts in CI + clear the cache**

In CI environments such as GitHub Actions, you need to clear matplotlib's font cache after installing the fonts:

```yaml
# .github/workflows/ci.yml
- name: Install CJK fonts
  run: |
    sudo apt-get update
    sudo apt-get install -y fonts-noto-cjk
    rm -rf ~/.cache/matplotlib    # Clear the cache to force rebuilding the font index
```

```{warning}
Even after installing `fonts-noto-cjk` and clearing the cache, you still have to combine it with Method 1 or Method 2 for it to work — because the `.ttc` face-0 trap is still there.
```

#### Default CJK fonts by platform

| Operating system | Installation | Available font name |
|---------|---------|-------------|
| Ubuntu / Debian | `sudo apt install fonts-noto-cjk` | Noto Sans CJK JP (face 0) |
| Ubuntu / Debian | `sudo apt install fonts-wqy-zenhei` | WenQuanYi Zen Hei |
| macOS | Built in | Heiti TC, Arial Unicode MS |
| Windows | Built in | Microsoft JhengHei |
| Google Colab | Preinstalled | Noto Sans CJK JP |

### E-2. Plotly: charts are blank when Jupyter Book builds

#### Symptom

An interactive Plotly chart renders fine in Jupyter Lab, but the static HTML produced by `jupyter-book build` is just blank.

#### Root cause

Jupyter Book executes notebooks in headless mode, and Plotly's default renderer (`plotly_mimetype`) can't produce HTML output in this environment.

#### Fix

Set the following in your notebook (or via `_config.yml`'s `nb_execution_pre_code`):

```python
import plotly.io as pio
pio.renderers.default = "notebook"
```

The `"notebook"` renderer outputs the chart as complete HTML + JS, which can be embedded in a static page.

```{tip}
This book already sets `pio.renderers.default = "notebook"` globally in `book/_config.yml`'s `nb_execution_pre_code`, so no notebook needs to set it individually. But if you run into the same problem in your own project, just add those two lines to your build script.
```

### E-3. Quick self-check list

When your Python charts have Chinese-display problems, check in this order:

| # | Check item | Command / method |
|---|---------|-------------|
| 1 | Does the system have a CJK font? | `fc-list :lang=zh` (Linux / macOS) |
| 2 | Which CJK fonts does matplotlib know about? | `[f.name for f in fm.fontManager.ttflist if "cjk" in f.name.lower()]` |
| 3 | Does the `font.sans-serif` candidate list include the names found in step 2? | `plt.rcParams["font.sans-serif"]` |
| 4 | Which font does matplotlib actually render with? | `fm.findfont(fm.FontProperties(family=["Noto Sans CJK JP"]))` |
| 5 | Is the Plotly renderer set to `"notebook"`? | `pio.renderers.default` |

---

## F. Infectious Disease Time Period Concepts

Outbreak investigations often require deciding "how long to isolate," "how many days to quarantine," and "when the exposure window was." All of these decisions rest on correctly distinguishing the following four time-period concepts.

```{figure} images/incubation_periods.svg
:name: fig-incubation-periods
:alt: Comparison of infectious disease time periods: a timeline comparing the incubation period, latent period, infectious period, and serial interval
:width: 100%

Timeline comparison of the four time-period concepts. Note: when the **latent period is shorter than the incubation period**, it means the infected person is already infectious **before** symptoms appear (asymptomatic transmission). In that case, symptom-based isolation measures have gaps and preemptive isolation is needed.
```

| Term | English | Definition | Relevance to the investigation |
|------|------|------|------------|
| **潛伏期** | Incubation period | Time from exposure to the **appearance of symptoms** | Determines how far back to trace the exposure window (the traceback period) |
| **潛藏期** | Latent period | Time from exposure to **becoming infectious** | Latent period < incubation period → risk of asymptomatic transmission |
| **可傳染期** | Infectious period | The duration for which an infected person can transmit the pathogen | Determines how many days of isolation are needed (the trace-forward period) |
| **世代間隔** | Serial / Generation interval | The time difference between onset in an index case and onset in a secondary case | Used to estimate the basic reproduction number R₀; forecasts the next onset peak |

> ⚠️ **Key distinction**: the **incubation period** is a clinical concept (when symptoms appear), whereas the **latent period** is a transmission concept (when infectiousness begins). Quarantine duration should be set based on the maximum of the **incubation period**; whether an asymptomatic isolation policy is necessary depends on **whether the latent period is shorter than the incubation period**.

### Legionnaires' disease (this book's main case)

| Metric | Value |
|------|------|
| Incubation period | 2–10 days (usually 5–6 days) |
| Infectious period | Extremely low (essentially no person-to-person spread); the main route is inhalation of environmental aerosols |
| Serial interval | Not applicable (sporadic; the source is the water system, not patients) |
| Quarantine implication | Because there's no person-to-person spread, contacts don't need mandatory quarantine; the focus is on removing the environmental source |

---

## G. The Six Links of the Chain of Infection and Intervention Strategies

For an infectious disease to spread from a pathogen to a susceptible host, it must pass through six links in sequence. Breaking any single link interrupts the chain of transmission.

```{figure} images/chain_of_infection.svg
:name: fig-chain-of-infection
:alt: The six links of the chain of infection: pathogen → reservoir → portal of exit → mode of transmission → portal of entry → susceptible host, plus three intervention strategies
:width: 100%

The six links of the chain of infection (top row) and the three main intervention strategies (bottom row). The chain of infection for Legionnaires' disease: *Legionella pneumophila* → water towers / shower water systems → aerosols → inhalation (vehicle-borne transmission) → respiratory tract → elderly / immunosuppressed residents.
```

### The six links explained

| # | Link | English | Legionnaires' disease example | Norovirus (for contrast) |
|---|------|------|--------------|---------------|
| ① | Pathogen | Pathogen | *Legionella pneumophila* | Norovirus |
| ② | Reservoir | Reservoir | Warm-water piping, cooling towers, shower heads | Infected people |
| ③ | Portal of exit | Portal of exit | Aerosols | Feces, vomit |
| ④ | Mode of transmission | Mode of transmission | Inhalation (vehicle-borne) | Fecal-oral route, contaminated food/water |
| ⑤ | Portal of entry | Portal of entry | Respiratory tract | Digestive tract |
| ⑥ | Susceptible host | Susceptible host | Elderly, immunosuppressed, chronic lung disease | All ages (more severe in those with weak immunity) |

### The three main intervention strategies

| Strategy | Link addressed | Common measures |
|------|---------|---------|
| **① Remove/control the source** | ①② | Isolation of infected people, animal culling and vaccination, environmental disinfection (chlorinating water towers, >70°C hot flushing) |
| **② Break the chain of transmission** | ③④⑤ | Handwashing, air ventilation, food safety, shutting down contaminated facilities, standard precautions (PPE) |
| **③ Protect the susceptible host** | ⑥ | Vaccination, post-exposure prophylaxis (PEP), evacuation of high-risk groups, health monitoring |

> 💡 **Investigation practice**: control measures don't have to wait until the investigation is complete. As long as you have a reasonable hypothesis (for example, suspecting a water tower), you should immediately launch "remove the source" measures and then refine them as the investigation proceeds.

---

## H. Quick Reference for Common Foodborne Pathogens

In a food-poisoning investigation, the length of the incubation period is the key basis for estimating the "suspect food time window." The table below is ordered by incubation period from shortest to longest.

| Pathogen | Incubation period | Main symptoms | Mode of transmission | Key identifying clue |
|--------|--------|---------|---------|------------|
| **Histamine** (Histamine / Scombroid) | 1–60 minutes (usually 10–30 min) | Facial flushing, whole-body warmth, hives, gastrointestinal symptoms | Eating spoiled tuna, mackerel, bonito, mahi-mahi, etc. | Very rapid onset; antihistamines are effective |
| **Staph aureus enterotoxin** | 0.5–8 hours (usually 2–4 hours) | Nausea, vomiting, abdominal cramps, diarrhea (the toxin is heat-stable, so reheated food can still cause poisoning) | Contamination from wounds on food handlers' hands; food left out too long | Mostly vomiting; fever is rare |
| **B. cereus emetic type** (*B. cereus* emetic) | 0.5–6 hours | Nausea, vomiting (little diarrhea) | Rice products such as fried rice left at room temperature | Symptoms resemble Staph; usually linked to fried rice |
| **Vibrio parahaemolyticus** (*V. parahaemolyticus*) | 2–48 hours (usually 12–18 hours) | Nausea, vomiting, diarrhea (watery/bloody), fever | Raw or undercooked seafood | Summer peak; common in Taiwan |
| **B. cereus diarrheal type** (*B. cereus* diarrheal) | 6–24 hours | Diarrhea, abdominal pain (little vomiting) | Various foods (meat, vegetables) improperly stored | Mostly diarrhea; longer incubation than the emetic type |
| **Clostridium perfringens** (*C. perfringens*) | 6–24 hours | Diarrhea, abdominal pain (little vomiting, little fever) | Large batches of cooked meat that were reheated insufficiently | Common at banquets and large catered events; mild symptoms but many affected |
| **Salmonella** (*Salmonella* spp.) | 6–72 hours (usually 12–36 hours) | Vomiting, diarrhea, fever, muscle aches | Eggs, poultry, dairy, vegetables | Prominent fever; bacteremia risk (in the immunosuppressed) |
| **Norovirus** (Norovirus) | 24–48 hours | Vomiting (children), diarrhea (adults), low fever | Contaminated food and water; person-to-person (fecal-oral route, droplets) | Symptoms resolve quickly (24–72 hours); highly transmissible, a small dose can infect |
| **E. coli O157 (EHEC)** | 1–10 days (usually 3–4 days) | Hemorrhagic colitis, severe abdominal pain; hemolytic uremic syndrome (HUS) | Undercooked beef, raw vegetables, unpasteurized juice | Bloody stool (no fever); children at risk of kidney failure |
| **Hepatitis A** (HAV) | 15–50 days (usually 28–30 days) | Fever, fatigue, jaundice, nausea | Contaminated food/water; raw shellfish | Longest incubation; infectious before jaundice appears |
| **Clostridium botulinum** (*C. botulinum*) | Usually 12–36 hours (can be several days) | Flaccid, symmetric, descending paralysis, double vision, difficulty swallowing (no fever) | Home-canned goods, pickled foods, honey (infants) | Mostly neurological symptoms (not GI); high fatality, report immediately |
| **Listeria (invasive)** (*L. monocytogenes*) | 3–70 days (usually 2–3 weeks) | Sepsis, meningitis; in pregnant women: miscarriage or premature birth | Ready-to-eat refrigerated foods (deli meats, cheese) | Longest incubation; high risk: pregnant women, immunosuppressed, elderly |

> 📌 **Investigation application**: when your cases' mean incubation period is about 12–24 hours, suspect Salmonella and Vibrio parahaemolyticus first. If it's <2 hours with vomiting, suspect Staph aureus toxin or histamine poisoning first (the latter comes with facial flushing). If there are neurological symptoms (paralysis, double vision), consider botulism immediately and report it.

### Key points for designing a food-poisoning questionnaire

The dietary-history recall period in a food-poisoning questionnaire should be determined by the **incubation period**:

| Suspected pathogen | Dietary-history recall window |
|---------|-------------|
| Histamine, Staph toxin | 1–4 hours before onset |
| Vibrio parahaemolyticus, Salmonella | 12–72 hours before onset |
| Norovirus | 24–48 hours before onset (also check contact history) |
| Unknown pathogen | **at least 3 days** (about 72 hours) of dietary history |
| Hepatitis A, Listeria | 2–6 weeks before onset |

```{tip}
**Designing the exposure columns of a line list**: give each suspect food its own column (0/1), have each respondent record "ate it or not," then use RR (cohort study) or OR (case-control study) to assess the association between each dish and illness. See the 2×2 table analysis in Ch03 for details.
```
