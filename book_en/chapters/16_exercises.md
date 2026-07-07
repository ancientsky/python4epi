# 16 Exercises

This section collects the exercise notebooks for each chapter (without solutions). All exercises use the same dataset:
**the Pine & Cypress Nursing Home Legionnaires' disease cluster** (`data/synthetic/legionella_outbreak.csv`, 280 rows × 32 columns).

## How to Use

1. First read the main chapter's concepts and example notebook.
2. Open the exercise notebook for that chapter.
3. Complete all the code blocks marked with `TODO`.
4. When you're done, compare your work against the reference solutions in Ch17.

```{admonition} Where are the solutions?
:class: tip

The solution notebooks are in [Ch17 Solutions](17_solutions.md), available only in the **instructor edition**.

- **Student edition** (this site): `https://ancientsky.github.io/python4epi/`
- **Instructor edition** (with solutions): `https://ancientsky.github.io/python4epi/instructor/`
```

> **Tip**: Each exercise set has 3 questions, and the 3rd is a challenge question.

## Exercise List

| Ch | Topic | Practice focus | Exercise |
|----|------|---------|------|
| 01 | Python basics | Practice variables, dicts, and functions with the cluster numbers | [Exercise](exercises/01_fundamentals_exercise.ipynb) |
| 02 | Data wrangling and visualization | Read the line list, convert dates, build the epi curve | [Exercise](exercises/02_data_wrangling_exercise.ipynb) |
| 03 | Descriptive statistics and 2×2 tables | Shower-exposure 2×2 table, RR, chi-square test | [Exercise](exercises/03_stats_exercise.ipynb) |
| 04 | Outbreak investigation workflow | Complete SitRep production pipeline | [Exercise](exercises/04_outbreak_workflow_exercise.ipynb) |
| 05 | Stratified analysis and confounders | Stratify by functional_status, Mantel-Haenszel test | [Exercise](exercises/05_stratified_exercise.ipynb) |
| 06 | Logistic regression | Crude vs. adjusted OR, model comparison | [Exercise](exercises/06_logistic_regression_exercise.ipynb) |
| 07 | Time series and forecasting | Moving average, MAE, hospitalization time series | [Exercise](exercises/07_time_series_exercise.ipynb) |
| 08 | Spatial epidemiology | Spatial distribution of CFR, shower × space cross-tabulation | [Exercise](exercises/08_spatial_exercise.ipynb) |
| 09 | Survival analysis | KM curve, log-rank, Cox regression | [Exercise](exercises/09_survival_exercise.ipynb) |
| 10 | Machine learning | class_weight, feature importance, ROC | [Exercise](exercises/10_ml_exercise.ipynb) |
| 11 | Deep learning | PyTorch architecture design, effect of dropout | [Exercise](exercises/11_dl_exercise.ipynb) |
| 12 | Causal inference | AR/PAR calculation, DiD date sensitivity | [Exercise](exercises/12_causal_exercise.ipynb) |
| 13 | Reproducible research | Summary dict, checklist, version log | [Exercise](exercises/13_reproducibility_exercise.ipynb) |
| 14 | Real-world case study | Outbreak summary, RR screening, mini SitRep | [Exercise](exercises/14_case_study_exercise.ipynb) |

## FAQ

**Q: Can I solve the problems a different way?**
A: Absolutely. The solutions are just a reference — any method that gets the right result is a good method.

**Q: What if the challenge question is too hard?**
A: Finish the first two questions first; you can come back to the challenge question after reviewing the solution. The point is to understand the analytical logic.

**Q: Where is the dataset?**
A: Every notebook reads from `data/synthetic/legionella_outbreak.csv`, so just make sure you run it from the project root directory.
