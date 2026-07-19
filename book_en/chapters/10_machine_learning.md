# 10 Machine Learning: Can We Predict Who Gets Infected and Who Becomes Severe?

## What You'll Learn

**Part A — (`10_ml_baseline`) Doing the workflow right on real data**

- How to frame an epidemiological scenario as a **binary classification problem**
- The **train / validation / test split** and how to prevent **data leakage**
- Using sklearn **Pipeline + ColumnTransformer**, **cross-validation + AUC**
- Facing the truth honestly: on 280 weak-signal rows, **RF barely beats logistic**—real prediction is humble

**Part B — (`10_ml_advanced`) Seeing the power of ML in a bigger sandbox**

- A **model zoo**: decision tree, random forest, XGBoost, LASSO (each with a clinical metaphor)
- **Ensembles**: bagging / boosting / **stacking (Super Learner)**
- An **evaluation suite**: ROC-AUC, PR-AUC, sensitivity/specificity/PPV/NPV, **calibration**
- **SHAP**: explaining a black-box model to clinicians
- **Class imbalance, overfitting, and "ML is a tool, not a replacement for epidemiological judgment"**

## The Scenario

The director is back again:
> "Can you build a model that predicts whether a new resident will get infected, just from their basic information?"
> "And which features matter the most?"

That's exactly what machine learning is for—not just explaining (Ch06 regression), but also **predicting**.

---

## Part A: Doing the Workflow Right on Real Data (`10_ml_baseline`)

Let's first run through a complete ML workflow "by the book" on the **real** Legionella data (280 rows)—the point is not to show off, but to **avoid mistakes** and **face the results honestly**.

### Foundation: the train / validation / test split

Ch07 taught us "you can't peek at the future"; the ML version is to split the data into three parts, each with its own job:

```{figure} images/train_val_test_split_en.svg
:name: fig-train-val-test
:alt: Three-way data split: train 60% learns the formula, validation 20% tunes hyperparameters and selects the model, test 20% is opened only once for the final evaluation; below, a red warning about data leakage (standardizing/SMOTE before splitting, using the outcome as a feature, peeking at the future)
:width: 100%

**train** (learn the formula) → **validation** (tune parameters, select the model) → **test** (the final exam you open only once). Once the test set has been seen, it's spent.
```

> 🚨 **Data leakage is the number-one killer in ML**: the moment information from the test set sneaks into training, the model will "score high but fail in production." The three cardinal sins: ① standardizing / SMOTE **before** splitting (it must be done inside each fold); ② using "part of the outcome" as a feature (e.g., predicting infection from symptoms); ③ using future information. For **time series** use `TimeSeriesSplit`, and for **spatial data** use spatial CV—you can't just shuffle randomly.

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

## Part B: Advanced ML—the Model Zoo, Ensembles, Evaluation, and SHAP (`10_ml_advanced`)

Part A honestly showed you: **on 280 weak-signal rows, RF barely beats logistic.** So when does ML actually "win handsomely"? The answer: **when risk is non-linear, has interactions, and the dataset is large enough.** Part B switches to a bigger synthetic sandbox (imagine the CDC's AI office pooling notifications from many facilities, n≈2500, deliberately seeded with a "U-shaped age" effect and an "immunosuppressed × exposure" interaction) and walks you through the full workflow. See the complete code in [`10_ml_advanced.ipynb`](notebooks/10_ml_advanced.ipynb).

### The Model Zoo (each with a clinical metaphor)

| Model | Clinical metaphor | In one sentence |
|---|---|---|
| 🩺 **Decision Tree** | ER **triage flowchart** | Asks yes/no questions all the way down; super easy to understand, but too rigid and prone to overfitting |
| 👥 **Random Forest** | **multi-specialty case-conference vote** (bagging) | A group of doctors each see part of the data, each cast a vote, majority rules → stable |
| 📈 **XGBoost** | **error-book cram school** (boosting) | Each round targets the residual errors of the previous one → accurate, but easy to over-correct |
| 🧳 **LASSO** (L1 logistic regression) | **weight-limited packing** | The L1 penalty forces unimportant coefficients to zero, keeping only a few key factors → lean and interpretable, epidemiology's favorite baseline |

On the sandbox data, **LASSO (linear) reaches only ~0.71 AUC, while tree-based models reach ~0.85**—this is exactly where ML wins when there's "non-linearity + interactions."

### Ensembles: three ways to "pool the wisdom of the crowd"

```{figure} images/bagging_vs_boosting_en.svg
:name: fig-bagging-boosting
:alt: Bagging (parallel voting, many trees each see part of the data and vote independently, majority rules = random forest) vs Boosting (relay tutoring, each round targets the residuals of the previous one = XGBoost)
:width: 100%

**Bagging** votes in parallel and reduces variance (more stable); **Boosting** relays to patch residuals and reduces bias (more accurate).
```

> 🎯 **Stacking = the commander at the control centre (Super Learner)**: the tree, forest, XGBoost, and LASSO each give a probability, and the **commander (meta-model) doesn't examine the patient itself**—instead it learns "in which situation should I listen more to which expert" and combines them with weights. This is the **Super Learner** from the epidemiology literature (van der Laan), which reduces the bias of any single model.

### The Evaluation Suite: Don't Look at Just One Number

The key idea in one sentence: in the **screening phase**, prioritize "don't miss anyone" (sensitivity, NPV, PR-AUC); in the **confirmation / resource-allocation phase**, prioritize "don't false-alarm, and get the probabilities right" (specificity, PPV, calibration).

| Metric | When to look at it | In plain epi language |
|---|---|---|
| **ROC-AUC** | Selecting a model, across thresholds | The probability a case ranks ahead of a healthy person; overly optimistic when imbalanced |
| **PR-AUC** | **Rare positives** (severe/death) | Focuses on "how real are the positives you caught," more honest than AUC |
| **Sensitivity** | Screening, when misses are costly | What fraction of true cases you caught |
| **Specificity** | When false alarms are costly | What fraction of the truly healthy you correctly let through |
| **PPV** (heavily affected by prevalence) | Clinical decision at the point of care | "The model says positive—what's the chance they really are sick"—what clinicians care about most |
| **NPV** | For ruling out | "It says you're fine—can you really relax?" |
| **Calibration / Brier** | When you'll use the probability as a number (bed allocation, risk communication) | Of the group told 70%, do about 70% really get sick? **Ranking well ≠ well-calibrated** |

### SHAP: Explaining the Black Box to Clinicians

> 💰 **A fair year-end bonus**: SHAP uses the Shapley value from game theory, asking "how much does the prediction change without this feature?", averaging each feature's **with vs. without** marginal contribution over all orderings. So it can tell you, for a **single patient**: "he was flagged high-risk because immunosuppressed +0.3, exposure +0.2, age 80 +0.15"—exactly the language you need to explain a black box to clinicians. In the sandbox, SHAP successfully recovered the "U-shaped age risk" we deliberately seeded, something a linear age term can never draw.

## Exercises

- Exercise version: [`10_ml_exercise.ipynb`](exercises/10_ml_exercise.ipynb)
- Solution version (instructor): [`10_ml_solution.ipynb`](solutions/10_ml_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/10_ml_solution.ipynb>)

## Common Pitfalls

| Mistake | Correct approach |
|------|---------|
| Standardizing / SMOTE before splitting | Use a Pipeline and do it **inside** each fold (otherwise data leakage) |
| Evaluating imbalanced data with accuracy | When severe cases are only 8%, "always guess healthy" scores 92% accuracy yet is useless → look at PR-AUC / sensitivity |
| Putting symptoms into the features | Symptoms are part of the outcome and cause data leakage |
| Reaching for a complex model with only 280 rows | A simple model + cross-validation is more reliable; training AUC 1.0, test 0.7 = overfitting |
| Using the probabilities for bed allocation just because AUC is high | Ranking well ≠ well-calibrated—look at **calibration** |
| Treating SHAP importance as an "intervention target" | Important ≠ causal; changing that feature won't necessarily prevent disease (causality is Ch12) |
| Going live right after training | Always do **external validation**: switch to another facility or another time period and the model may collapse (dataset shift) |
| Looking only at overall performance | Check **fairness**: is subgroup performance consistent across sexes / age groups? |

## Next Steps

ML tells us that prediction is possible, but is an ML model trained on 280 rows trustworthy?
In the next chapter (Ch11), we'll try deep learning with PyTorch—and discuss when you should and shouldn't use DL.
