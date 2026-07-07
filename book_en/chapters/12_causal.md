# 12 Causal Inference and Policy Evaluation: Does Showering Really "Cause" Infection?

## What You Will Learn

- Visualize causal relationships with a **DAG (directed acyclic graph)**
- Distinguish **causal effects** from **statistical associations**
- Identify **confounding paths, mediators, and colliders**
- Calculate **attributable risk (AR)** and **population attributable risk (PAR)**
- Evaluate intervention effects with **difference-in-differences (DiD)**

## The Story So Far

By this chapter, you have already used descriptive statistics, stratified analysis, regression, ML, and DL—all pointing to "shower exposure is associated with infection."

But the director asked the most fundamental question of all:
> "Does showering really *cause* infection? Or is it just a statistical coincidence?"
> "If we disinfect the water system, will infections really go down?"

These are the questions **causal inference** aims to answer.

---

## Part 1: DAG — Visualizing Causal Relationships

### What Is a DAG?

A **directed acyclic graph (DAG)** uses arrows to represent the direction of causation:

```
floor_wing → water_contamination → shower_aerosol → infection
functional_status → shower_use → infection
age → comorbidities → severity → death
```

### Identifying Causal Structures

| Structure | Description | Example in This Case |
|------|------|---------|
| **Confounder** | Affects both the exposure and the outcome | `functional_status` → `shower_use` and `infection` |
| **Mediator** | Sits on the path between exposure and outcome | `shower_aerosol` between `water_contamination` → `infection` |
| **Collider** | Affected by both the exposure and the outcome | `hospitalized` ← `severity` and `infection` |

> **The collider trap**: If you only analyze "people who were hospitalized," you are conditioning on a collider, which creates a spurious association.

---

## Part 2: Attributable Risk

### Attributable Risk (AR)

```python
# Attack rate in exposed group - attack rate in unexposed group
AR = risk_exposed - risk_unexposed
```

### Population Attributable Risk (PAR)

```python
# If no one showered, how many infections could be prevented?
PAR = risk_total - risk_unexposed
PAR_pct = PAR / risk_total * 100
```

---

## Part 3: Difference-in-Differences (DiD)

### The Scenario

On January 25, the nursing home carried out emergency disinfection of the water system for Wing B on floors 2–3 (the high-attack-rate area).
Floor 1 serves as the control group (a different water supply system).

```python
import statsmodels.formula.api as smf

# treated = Wing B on floors 2-3, control = floor 1
# post = after January 25
model = smf.ols("daily_cases ~ treated + post + treated:post", data=panel).fit()
```

The `treated:post` coefficient is the DiD effect estimate—under the parallel trends assumption, it represents the causal effect of the intervention.

### The Parallel Trends Assumption

The core assumption of DiD: absent the intervention, the two groups would have followed the same trend.

- **How to check it**: look at whether the pre-intervention trends are parallel
- **If they are not parallel**: the DiD estimate is not trustworthy

---

## Exercises

- Exercise version: [`12_causal_exercise.ipynb`](exercises/12_causal_exercise.ipynb)
- Solution version (instructor): [`12_causal_solution.ipynb`](solutions/12_causal_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/12_causal_solution.ipynb>)

## Common Pitfalls

| Mistake | The Right Approach |
|------|---------|
| Statistical significance = causation | Association is not causation; you need DAG analysis |
| Running DiD without checking parallel trends | Plot the pre-intervention trends first |
| Conditioning on a collider | Use a DAG to identify variables you should NOT control for |
| Interpreting AR as "removing the exposure will prevent it" | AR assumes the causal relationship holds and there are no other pathways |

## Next Steps

Causal inference helps us clarify "what causes what."
In the next chapter (Ch13), we make sure all of our analyses are **reproducible** → reproducible research.
