# Epi With Python — Learning Epidemiology with Python

## One Phone Call, One Investigation

> It's four o'clock on a Friday afternoon, and you get a call from the health department:
>
> "Pine & Cypress Nursing Home has multiple residents showing signs of pneumonia — a suspected Legionnaires' disease cluster. Please get there as soon as you can to investigate."
>
> You grab your laptop and rush to the scene. 280 residents, 3 floors, 2 wings — facing all these numbers, you open up Python…

Every chapter in this book is one piece of that investigation. Starting from scratch, you'll use Python to carry out a complete outbreak investigation, step by step.

```{button-ref} chapters/00_guide
:ref-type: doc
:color: primary
:expand:
:class: sd-fs-5 sd-font-weight-bold

Turn to Ch00 and pick up the phone →
```

## The Data Behind This Investigation

The whole book uses a single synthetic dataset: **the Pine & Cypress Nursing Home Legionnaires' disease cluster**

::::{grid} 2 2 3 3
:gutter: 3

:::{grid-item-card} 280
:text-align: center
Total residents
:::

:::{grid-item-card} 121
:text-align: center
Infected (attack rate 43.2%)
:::

:::{grid-item-card} 19
:text-align: center
Deaths (case fatality rate 15.7%)
:::

:::{grid-item-card} 32
:text-align: center
Data columns (demographics / comorbidities / exposures / clinical / outcomes)
:::

:::{grid-item-card} 3 × 2
:text-align: center
3 floors × 2 wings (A/B)
:::

:::{grid-item-card} 17 days
:text-align: center
Onset period 2026-01-12 to 01-28
:::

::::

## The Storyline: A Five-Act Investigation

::::{grid} 1 1 2 3
:gutter: 3

:::{grid-item-card} 🎬 Act I — The Call
**Ch00–02**
^^^
Orientation, Python basics, data wrangling and visualization. You pick up the phone, set up your tools, and read in the 280-record line list to start cleaning it up.
:::

:::{grid-item-card} 🔬 Act II — From Description to Inference
**Ch03–04**
^^^
2×2 tables, risk ratios, and the chi-square test — is showering a risk factor? You produce your first SitRep for the boss.
:::

:::{grid-item-card} 🕵️ Act III — Digging Deeper
**Ch05–08**
^^^
Stratified analysis and confounders, logistic regression, time-series forecasting, spatial epidemiology — where is the highest risk? And why?
:::

:::{grid-item-card} 🧠 Act IV — Advanced Modeling
**Ch09–12**
^^^
Survival analysis, machine learning, deep learning, causal inference — from predicting severe cases to pinning down the causal effect of shower exposure.
:::

:::{grid-item-card} 📋 Act V — Wrap-Up & Real Cases
**Ch13–14**
^^^
Reproducible research and a complete outbreak report — let colleagues reproduce your entire analysis with one click, from the first notification to the final report.
:::

:::{grid-item-card} 📚 Appendix & Exercises
**Ch15–17**
^^^
Glossary, dataset column dictionary, package quick reference, plus 14 sets of exercises and solutions.
:::

::::

## Who It's For

- **Complete beginners**: start from Python syntax and move step by step into epidemiological analysis
- **Public health graduate students**: learn to replace Excel with code for outbreak analysis
- **Practicing epidemiologists**: transition from traditional tools to a Python workflow
- **Anyone curious about infectious diseases**: learn analytical thinking through a realistic case

## How to Use This Book

### Read Online: Two Editions

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🎓 Student edition
Lessons + exercises (no solutions)
+++
```{button-link} https://ancientsky.github.io/python4epi/
:color: primary
:expand:
Open the student edition
```
:::

:::{grid-item-card} 👩‍🏫 Instructor edition
Lessons + exercises + solutions
+++
```{button-link} https://ancientsky.github.io/python4epi/instructor/
:color: secondary
:expand:
Open the instructor edition
```
:::

::::

Every notebook page has an **Open in Colab** button in the top-right corner, or you can run it locally:

```bash
uv sync && uv run jupyter lab
```

On Google Colab there's nothing to install — every notebook has a setup cell at the top that automatically detects Colab.

### Suggested Learning Path

Go through the chapters in order — each chapter's results lead naturally into the next chapter's questions. That's the rhythm of a real outbreak investigation.

## Language and Terminology

- The main text is written in **Traditional Chinese**, with technical terms kept in English; you can switch to the **English** edition from the top-right corner
- Epidemiological terms follow **Taiwan standard translations** (e.g., 侵襲率, 致死率, 信賴區間)
- For the full glossary, see {doc}`Ch15 Appendix <chapters/15_appendix>`

## Let's Get Started

Turn to Ch00 and pick up the phone.
