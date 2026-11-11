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
| 01 | Python basics | Organizing outbreak data with dicts, wrapping logic in functions | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/fundamentals-solution/) |
| 01b | Python developer toolbox | The statistics module, type conversion, try/except, string cleaning | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/b-python-toolbox-solution/) |
| 02 | Data wrangling and visualization | Derived date columns, epi curve by age group | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/data-wrangling-solution/) |
| 03 | Descriptive statistics and 2×2 tables | Hydrotherapy RR, RR by age group, Fisher's exact | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/stats-solution/) |
| 04 | Outbreak investigation workflow | Automated SitRep function, severity analysis | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/outbreak-workflow-solution/) |
| 05 | Stratified analysis and confounders | Age stratification, comorbidity confounding, MH adjusted RR | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/stratified-solution/) |
| 06 | Logistic regression | Severe-case model, LRT comparison, predicted probabilities | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/logistic-regression-solution/) |
| 07 | Time series and forecasting | Hospitalization series, windowed MAE, severity stacked chart | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/time-series-solution/) |
| 08 | Spatial epidemiology | CFR heatmap, shower × space correlation, high-risk rooms | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/spatial-solution/) |
| 09 | Survival analysis | CHF KM curve, age grouping, multivariable Cox | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/survival-solution/) |
| 10 | Machine learning | Balanced classes, severe-case prediction, three-model ROC | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/ml-solution/) |
| 11 | Deep learning | Three-layer architecture, severe-case task, dropout comparison | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/dl-solution/) |
| 12 | Causal inference | Hydrotherapy AR/PAR, date sensitivity, collider bias | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/causal-solution/) |
| 13 | Reproducible research | Summary validation, environment check, version log | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/reproducibility-solution/) |
| 14 | Real-world case study | Summary table, RR comparison, mini SitRep chart | [Solution](https://ancientsky.github.io/python4epi/en/instructor/chapters/solutions/case-study-solution/) |

## Teaching Notes

- **Ch05 Stratified analysis**: the focus is helping students understand "why the crude RR and adjusted RR differ"
- **Ch06 Logistic regression**: emphasize the difference between crude OR and adjusted OR, complementing the stratified analysis in Ch05
- **Ch09 Survival analysis**: "hospitalized patients have higher mortality" is a classic example of confounding by indication
- **Ch12 Causal inference**: collider bias is the most commonly overlooked type of bias
- **Ch14 Real-world case study**: let students decide on the "recommended actions" themselves, practicing the leap from analysis to decision-making
