# 10 Machine Learning: Can We Predict Who Gets Infected and Who Becomes Severe?

## What You'll Learn

- How to frame an epidemiological scenario as a **binary classification problem**
- How to use sklearn **Pipeline + ColumnTransformer** to avoid data leakage
- How to build a **Logistic Regression** baseline and a more advanced **Random Forest** model
- How to evaluate models correctly with **cross-validation + AUC**
- How to identify the most important features with **permutation importance**
- How to compare ML feature importance vs. the adjusted OR from the Ch06 logistic regression

## The Scenario

The director is back again:
> "Can you build a model that predicts whether a new resident will get infected, just from their basic information?"
> "And which features matter the most?"

That's exactly what machine learning is for—not just explaining (Ch06 regression), but also **predicting**.

---

## Step 1 — Defining the Problem

We define two prediction tasks:

| Task | Target variable | Definition | Positive-class share |
|------|---------|------|---------|
| Task A | `infected` | Whether infected | 121/280 = 43% |
| Task B | `severe_outcome` | Whether hospitalized or died | 68/280 = 24% |

```python
import pandas as pd

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
df["severe_outcome"] = ((df["hospitalized"] == 1) | (df["outcome"] == "dead")).astype(int)
```

## Step 2 — Feature Engineering

```python
# Numeric features
num_cols = ["age"]

# Categorical features (OneHotEncoder)
cat_cols = ["sex", "smoking_history", "functional_status", "wing"]

# Binary features (used directly)
bin_cols = [
    "floor", "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed", "shower_use", "hydrotherapy_use",
]

X = df[num_cols + cat_cols + bin_cols]
y = df["infected"]
```

> **Note**: We must not use symptoms (fever, cough, etc.) as features—symptoms only appear *after* infection, so including them would cause data leakage.

## Step 3 — Building the Pipeline

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression

preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), cat_cols),
    ("bin", "passthrough", bin_cols),
])

clf_lr = Pipeline([
    ("preprocess", preprocess),
    ("model", LogisticRegression(max_iter=500, random_state=42)),
])
```

## Step 4 — Cross-Validation + AUC

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(clf_lr, X, y, cv=5, scoring="roc_auc")
print(f"5-fold CV AUC = {scores.mean():.3f} ± {scores.std():.3f}")
```

## Step 5 — Random Forest, a More Advanced Model

```python
from sklearn.ensemble import RandomForestClassifier

clf_rf = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42)),
])
scores_rf = cross_val_score(clf_rf, X, y, cv=5, scoring="roc_auc")
print(f"Random Forest 5-fold CV AUC = {scores_rf.mean():.3f} ± {scores_rf.std():.3f}")
```

## Step 6 — Feature Importance

```python
from sklearn.inspection import permutation_importance

clf_rf.fit(X, y)
result = permutation_importance(clf_rf, X, y, n_repeats=10, random_state=42)
```

---

## Exercises

- Exercise version: [`10_ml_exercise.ipynb`](exercises/10_ml_exercise.ipynb)
- Solution version (instructor): [`10_ml_solution.ipynb`](solutions/10_ml_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/10_ml_solution.ipynb>)

## Common Pitfalls

| Mistake | Correct approach |
|------|---------|
| Standardizing before splitting | Use a Pipeline so standardization happens inside each fold |
| Using accuracy on imbalanced data | Use AUC or F1 |
| Putting symptoms into the features | Symptoms are part of the outcome and cause data leakage |
| Reaching for a complex model with only 280 rows | A simple model + cross-validation is more reliable |

## Next Steps

ML tells us that prediction is possible, but is an ML model trained on 280 rows trustworthy?
In the next chapter (Ch11), we'll try deep learning with PyTorch—and discuss when you should and shouldn't use DL.
