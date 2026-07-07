# 17 Solutions (Instructor Edition)

This chapter provides reference solutions for each chapter's exercises. All solutions use the same dataset:
**the Pine & Cypress Nursing Home Legionnaires' disease cluster** (`data/synthetic/legionella_outbreak.csv`).

## Suggested Use

- Complete the corresponding questions in Ch16 Exercises first, then review the solutions.
- Each solution demonstrates one reasonable analysis workflow — it is **not the only correct answer**.
- When teaching, we recommend discussing the choice of methods and the analytical logic first, then showing the code.

## Solution List

| Ch | Topic | Solution focus | Solution |
|----|------|---------|------|
| 01 | Python basics | Organizing outbreak data with dicts, wrapping logic in functions | [Solution](solutions/01_fundamentals_solution.ipynb) |
| 02 | Data wrangling and visualization | Derived date columns, epi curve by age group | [Solution](solutions/02_data_wrangling_solution.ipynb) |
| 03 | Descriptive statistics and 2×2 tables | Hydrotherapy RR, RR by age group, Fisher's exact | [Solution](solutions/03_stats_solution.ipynb) |
| 04 | Outbreak investigation workflow | Automated SitRep function, severity analysis | [Solution](solutions/04_outbreak_workflow_solution.ipynb) |
| 05 | Stratified analysis and confounders | Age stratification, comorbidity confounding, MH adjusted RR | [Solution](solutions/05_stratified_solution.ipynb) |
| 06 | Logistic regression | Severe-case model, LRT comparison, predicted probabilities | [Solution](solutions/06_logistic_regression_solution.ipynb) |
| 07 | Time series and forecasting | Hospitalization series, windowed MAE, severity stacked chart | [Solution](solutions/07_time_series_solution.ipynb) |
| 08 | Spatial epidemiology | CFR heatmap, shower × space correlation, high-risk rooms | [Solution](solutions/08_spatial_solution.ipynb) |
| 09 | Survival analysis | CHF KM curve, age grouping, multivariable Cox | [Solution](solutions/09_survival_solution.ipynb) |
| 10 | Machine learning | Balanced classes, severe-case prediction, three-model ROC | [Solution](solutions/10_ml_solution.ipynb) |
| 11 | Deep learning | Three-layer architecture, severe-case task, dropout comparison | [Solution](solutions/11_dl_solution.ipynb) |
| 12 | Causal inference | Hydrotherapy AR/PAR, date sensitivity, collider bias | [Solution](solutions/12_causal_solution.ipynb) |
| 13 | Reproducible research | Summary validation, environment check, version log | [Solution](solutions/13_reproducibility_solution.ipynb) |
| 14 | Real-world case study | Summary table, RR comparison, mini SitRep chart | [Solution](solutions/14_case_study_solution.ipynb) |

## Teaching Notes

- **Ch05 Stratified analysis**: the focus is helping students understand "why the crude RR and adjusted RR differ"
- **Ch06 Logistic regression**: emphasize the difference between crude OR and adjusted OR, complementing the stratified analysis in Ch05
- **Ch09 Survival analysis**: "hospitalized patients have higher mortality" is a classic example of confounding by indication
- **Ch12 Causal inference**: collider bias is the most commonly overlooked type of bias
- **Ch14 Real-world case study**: let students decide on the "recommended actions" themselves, practicing the leap from analysis to decision-making
