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

## 🩺 Super Simple Special: Think of the Model as an Intern Doctor in Training

> Feature engineering, cross-validation, AUC… feeling dizzy from all the jargon? Don't worry. This section uses **one single metaphor** to tie all of Part A together: **think of the model as an intern doctor in training, getting ready to sit the licensing exam.** Once you've seen this one figure, every Step below is just a stop along this intern's journey.

All of Part A is really just the process of **training an intern doctor from a raw rookie into someone who can see patients on their own.** First they have to learn "which clues on a chart are actually useful" (**feature engineering**), then attend classes and practice (**train**), sit a few practice exams where they can peek at the answers and adjust their study method as they go (**validation**), and finally take one real licensing exam they can't retake (**test**). And **AUC** is their **report card**.

```{figure} images/ml_intern_journey_en.svg
:name: fig-ml-intern-journey
:alt: An intern doctor's journey mapped onto the whole ML workflow: organize the chart clues (feature engineering) → attend classes to learn the formula (train) → practice exams you can retake (validation) → rotate through 5 question banks as mock exams (cross-validation, used in this chapter) → the licensing exam is taken only once (test); below, a red warning that peeking at past exam papers = data leakage; the report card = AUC
:width: 100%

An intern doctor's training = the entire ML workflow. Because this chapter has only 280 rows, we replace the fixed practice exam (validation) with "cross-validation."
```

### The whole journey in five lines

> 🔑 **The model isn't a genius, it's an intern**: everything it knows is a chart clue you "fed" it. Give it the wrong clues (using the diagnosis as a clue) and it cheats; give it too many messy clues and it can't learn.
>
> 📚 **train is class, validation is the practice exam, test is the licensing exam**: in class you can open the book, in a practice exam you can review and improve, but **the licensing exam is taken only once—once it's opened, it's spent**—you can't retake the same paper just because you're unhappy with your score.
>
> 🔁 **Cross-validation = sit a mock exam with each of 5 different question banks**: taking just one exam leaves room for the luck of "happening to get the questions you knew"; rotating through 5 different papers and averaging is how you find out their **real ability** (and how steady they are).
>
> 🎯 **AUC isn't "how many you got right," it's "the eye for ranking patients"**: grab one person who really will get infected and one who won't—can this intern put the "will get infected" one ahead? The probability of getting that order right is the AUC. 0.5 = eyes-closed guessing, 0.7 = a pass, 0.8 = pretty good.
>
> 🤖 **Giving the intern a smarter brain (Random Forest) doesn't guarantee a higher score**: if the chart clues themselves are thin (280 rows, and a weak signal at that), no brain—however smart—can conjure information out of nothing. That's the honest conclusion of Part A.

### Intern doctor ↔ ML terminology

| The intern's world | ML term | In one line |
|---|---|---|
| Circling the "useful clues" on a chart and tidying them into a readable format | **feature engineering** | The model only eats numbers: age must be scaled, sex must be encoded, symptoms can't be used (cheating) |
| Attending class to learn the formula | **training set** (train) | This is where the model "learns" the coefficients/rules (`fit`) |
| A practice exam where you can see the answers and improve as you go | **validation set** | Used to select models and tune parameters; can be reused repeatedly |
| The licensing exam, taken once, spent the moment it's opened | **test set** | The final evaluation, representing real-world performance after going live |
| Sitting a mock exam with each of 5 question banks and averaging | **cross-validation** (k-fold CV) | Lets every row take a turn as an exam question, giving a fairer, steadier score |
| Report card: the eye for putting patients in the right order | **AUC** | For a random pair (sick/not sick), the probability of ordering them correctly; 0.5 guessing, 0.8 good |
| Peeking at past exam papers (the exact questions that came up) | **data leakage** | Using symptoms/outcomes as clues, or standardizing before splitting → scores high, fails in production |

> ⚠️ **Four rookie traps**: ① scoring well on the practice exam ≠ the intern is strong (they may have peeked at the paper = leakage); ② using the licensing-exam questions to tune your study method → the test degrades into a validation set and you'll overestimate your ability; ③ a smarter brain isn't necessarily more accurate (when clues are thin, RF ≈ logistic, and it's even more prone to rote memorization); ④ the important clues you find ≠ the cause of disease (important ≠ causal—that's Ch12).

---

## Part A: Doing the Workflow Right on Real Data (`10_ml_baseline`)

Let's first run through a complete ML workflow "by the book" on the **real** Legionella data (280 rows)—the point is not to show off, but to **avoid mistakes** and **face the results honestly**. See the complete code in [`10_ml_baseline.ipynb`](notebooks/10_ml_baseline.ipynb).

## Step 0 — Data Splitting: Sort the "Exam Papers" First

Before feeding any data to the intern, split it apart: one part to **learn** from, one part to **score** with. Ch07 taught us "you can't peek at the future"; the ML version is the **train / validation / test three-way split**:

```{figure} images/train_val_test_split_en.svg
:name: fig-train-val-test
:alt: Three-way data split: train 60% learns the formula, validation 20% tunes hyperparameters and selects the model, test 20% is opened only once for the final evaluation; below, a red warning about data leakage (standardizing/SMOTE before splitting, using the outcome as a feature, peeking at the future)
:width: 100%

**train** (learn the formula) → **validation** (mock exam, tune parameters and select the model) → **test** (the licensing exam, opened only once). Once the test set has been seen, it's spent.
```

> 🚨 **Data leakage is the number-one killer in ML**: the moment information from the test set sneaks into training, the model will "score high but fail in production." The three cardinal sins: ① standardizing / SMOTE **before** splitting (it must be done inside each fold); ② using "part of the outcome" as a feature (e.g., predicting infection from symptoms); ③ using future information. For **time series** use `TimeSeriesSplit`, and for **spatial data** use spatial CV—you can't just shuffle randomly.

**So should you split 60/20/20, or 70/15/15, or 80/10/10?** In one line: **the more data you have, the smaller the validation/test "proportion" can be**, because 10% is already plenty in absolute terms.

| Data size | Suggested split | Why |
|---|---|---|
| **Small (< 1,000 rows, like this chapter's 280)** | **Don't carve out a fixed validation set → use k-fold cross-validation instead**; keep ~20% for test (or just report everything with CV) | A single fixed validation split leaves too few samples and the score is all down to luck; CV lets every row serve as an exam question, which is far steadier |
| **Medium (1k–100k)** | **60/20/20** or **70/15/15** | Val/test each have a few thousand rows, enough for a stable evaluation |
| **Large (> 100k)** | **80/10/10**, or even more extreme | 1% is already tens of thousands of rows, enough to evaluate; it pays to leave more data for training |

> 📌 **Two honest reminders**: ① **this chapter's 280 rows are the textbook case of "small"**—which is why you won't see anything called `X_val` below; the role of validation is taken over by the **cross-validation in Step 4**; ② **when imbalanced, split "stratified"** (severe cases are only 24%): the split/CV must be stratified (`StratifiedKFold`, `train_test_split(stratify=y)`), otherwise some fold may end up with almost no positives and the scores will jump around wildly.

## Step 1 — Defining the Problem: Turning the Director's Question into a 0/1 Label

ML can't work with a vague sentence like "predict who will get sick"—it needs one column with an explicit **0/1 label**. We define two prediction tasks:

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

> **Line-by-line breakdown**
>
> | Code | What it does |
> |---|---|
> | `(df["clinical_severity"] != "not_ill").astype(int)` | Anyone whose clinical severity is not "not ill" counts as infected (1), otherwise 0 |
> | `((df["hospitalized"]==1) \| (df["outcome"]=="dead")).astype(int)` | Hospitalized **or** died counts as a severe outcome (1) |
>
> 💡 **Why define the label first?** Because once the label is fixed, "which columns count as cheating" is fixed too. `infected` is defined using `clinical_severity`, so `clinical_severity`, symptoms, hospitalization, death—all these "outcome-side" columns **cannot be used as clues**; they are part of the answer. That's the iron rule for picking features in Step 2. (Also worth remembering: Task B has only 24% positives, and this "imbalance" is what decides, in Step 4, why we look at AUC rather than accuracy.)

## Step 2 — Feature Engineering: Translating a "Messy Chart" into Numbers the Model Understands

**Why do feature engineering?** The model only does math; it can't read strings like "male/female" or "Wing A," and it doesn't know that "age 85" and "floor 3" aren't on the same scale. Feature engineering is about **tidying the chart into numbers the model can eat, on the intern's behalf.**

```{figure} images/feature_engineering_en.svg
:name: fig-feature-engineering
:alt: The feature-engineering flow: a raw line list (age, sex, shower_use, and a crossed-out fever representing leakage) → three column types take three paths (numeric → StandardScaler standardization, categorical → OneHotEncoder split into 0/1 columns, binary → passthrough used directly) → a matrix that is all numbers → fed into the model; below, the three rules for picking features
:width: 100%

Three kinds of columns, three ways to handle them: numeric must be scaled, categorical must be encoded, binary goes straight through.
```

**Three kinds of columns, three ways to handle them (and why):**

| Type | Example | How to handle | Why |
|---|---|---|---|
| **numeric** | `age` | Standardize with `StandardScaler` (subtract the mean, divide by the standard deviation) | Age runs 20–100 while other columns are 0/1; without scaling, age's "big numbers" get mistaken for "important," and logistic also converges more slowly |
| **categorical** | `sex`, `wing`, `smoking_history`, `functional_status` | One-hot encode (split into several 0/1 columns) | "Wing A=1, Wing B=2" would be read by the model as an order "B > A," but wings have no size relationship; one-hot splits them into equal, independent switches |
| **binary** | each comorbidity, `immunosuppressed`, `shower_use` | Let it `passthrough` unchanged | Already 0/1, already numbers the model can eat, so leave them alone |

```python
num_cols = ["age"]                                                   # numeric → to be standardized
cat_cols = ["sex", "smoking_history", "functional_status", "wing"]   # categorical → to be one-hot encoded
bin_cols = [                                                         # binary → used directly
    "floor", "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed", "shower_use", "hydrotherapy_use",
]
X = df[num_cols + cat_cols + bin_cols]
y = df["infected"]
```

> 🧭 **How do you "pick" features? Don't dump the whole table in—three rules:**
> 1. **Domain knowledge first**: ask "would we know this clue at the moment the resident is **admitted / exposed**?" The known risks for Legionella are age, chronic disease, immunosuppression, and water exposure (shower / hydrotherapy)—pick those.
> 2. **The iron rule: never use columns that only appear "after the outcome"** (anti-cheating). Symptoms (fever, cough), `clinical_severity`, hospitalization, death, `icu_admission`, `lab_confirmed`, all kinds of dates—these are known only **after** infection, so using them to predict infection is **peeking at the answer**. Use symptoms and the AUC will look gorgeous at 0.99, and then in production you don't even have symptom data yet.
> 3. **Don't stuff in everything**: 280 rows can't support dozens of features; the more features, the easier it is to "rote-memorize" (overfit). Better few and sharp.
>
> (Side note: here we put `floor` in `bin_cols` and use it as 0/1; if there are multiple floors with no size relationship between them, a stricter approach is to treat it as a categorical column and one-hot encode it.)

## Step 3 — Pipeline: Tying "Preprocessing + Model" into One Chain, and Preventing Leakage Along the Way

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

> 🔒 **Why must you wrap it in a Pipeline instead of running `scaler.fit(X)` yourself first?** Because standardization uses "the mean and the standard deviation"—if you compute these two numbers on all the data **before splitting**, the test set's information quietly seeps into training, which is the most insidious data leakage. A Pipeline guarantees that within **each fold** of cross-validation, the scaling mean is **learned only from that fold's training data**, with the test fold taking no part at all. It's like "no peeking at the answers to the mock exam until after you've graded the paper."
>
> **Line-by-line breakdown**
>
> | Code | What it does |
> |---|---|
> | `ColumnTransformer([...])` | Applies different preprocessing to different column groups: scale the numeric, one-hot the categorical, pass the binary through |
> | `OneHotEncoder(handle_unknown="ignore", drop="first")` | `drop="first"` avoids collinearity; `handle_unknown="ignore"` keeps it from erroring when a test fold contains a category it hasn't seen |
> | `Pipeline([("preprocess",...), ("model",...)])` | Chains preprocessing + model into a single object, so `fit`/`predict` run together and the whole chain re-runs inside each fold during CV |

## Step 4 — Cross-Validation + AUC: What Exactly Are We Comparing?

This is the step where beginners most easily get lost. First get clear on **what cross-validation does**, then on **what AUC is**.

```{figure} images/cross_validation_kfold_en.svg
:name: fig-cross-validation
:alt: A 5-fold cross-validation diagram: the data is cut into 5 folds; each row uses 1 fold as the test set (green) and the other 4 for training (blue), the test fold rotating along the diagonal, yielding 5 AUCs, finally averaged with a standard deviation
:width: 100%

k-fold cross-validation: every row takes a turn as an "exam question," giving 5 AUCs → take the mean and standard deviation.
```

> 🔁 **What is cross-validation comparing?** `cross_val_score` itself **doesn't compare two models**—it gives a single model a more trustworthy score. It cuts the data into 5 folds, each time training on 4 and holding out 1 as the exam, rotating 5 times—**so every row serves as an exam question exactly once.** That yields 5 AUCs, and you read two numbers: the **mean** (`.mean()`) = roughly how strong; the **standard deviation** (`.std()`) = how steady (a large standard deviation = it collapses when the question bank changes, unreliable). The real "comparison" happens in your eyes: Step 4 gives logistic a score, Step 5 gives RF a score, and you lay the two report cards side by side—that's model selection.

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(clf_lr, X, y, cv=5, scoring="roc_auc")
print(f"5-fold CV AUC = {scores.mean():.3f} ± {scores.std():.3f}")
```

So **what exactly is AUC**? Forget the scary phrase "area under the curve":

```{figure} images/roc_auc_intuition_en.svg
:name: fig-roc-auc
:alt: AUC intuition: on the left, a leaderboard where the model ranks patients by risk score, with the truly infected (orange) mostly near the top; on the right, an AUC ruler—0.5 eyes-closed guessing, 0.7 a pass, 0.8 pretty good, 1.0 all correct; below, a reminder not to look at accuracy on imbalanced data
:width: 100%

AUC = grab one infected person and one healthy person at random, and it's the probability the model ranks the infected one ahead.
```

> 🎯 **The most plain-words definition of AUC**: **grab one person who truly will get infected and one who truly won't, and it's the probability the model gives the former a higher score than the latter.** Right order = points. **0.5** = eyes-closed guessing (a coin flip), **0.7** = a pass, **0.8** = pretty good, **1.0** = every pair ordered correctly (in reality, if it's this high, suspect leakage first).
>
> ⚠️ **Why not use "accuracy"?** Task B is only 24% severe. If the model **always guesses "not severe,"** its accuracy is 76%—sounds high, but it caught not a single patient and is completely useless. AUC looks at **ranking**, not "how many you guessed right," and isn't affected by whatever threshold you set. So on **imbalanced** data (rare events like severe cases and deaths), looking at AUC (and PR-AUC too, in Part B) is far more honest than looking at accuracy.

## Step 5 — Random Forest: Swapping in a Smarter Brain

```python
from sklearn.ensemble import RandomForestClassifier

clf_rf = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42)),
])
scores_rf = cross_val_score(clf_rf, X, y, cv=5, scoring="roc_auc")
print(f"Random Forest 5-fold CV AUC = {scores_rf.mean():.3f} ± {scores_rf.std():.3f}")
```

> 🌲 **Notice: nothing else in the pipeline changed**—only the `model` slot was swapped. This is exactly the payoff of wrapping things in a Pipeline in Step 3: swapping models means swapping one word. Logistic can only draw a straight-line boundary, while a Random Forest is a crowd of decision trees voting, able to capture non-linearity and interactions.
>
> **But the result is honest**: on these 280 weak-signal rows, RF's AUC barely edges out logistic (try it: both hover around 0.6). The reason isn't that RF is dumb—it's that **the chart clues are thin to begin with**—no matter how much smarter a brain you give the intern, it can't conjure information that isn't in the data. ML truly shows its power only in a **Part B**-style arena of "big data + non-linearity + interactions."

## Step 6 — Feature Importance: Which Clue Is Most Useful?

```python
from sklearn.inspection import permutation_importance

clf_rf.fit(X, y)
result = permutation_importance(clf_rf, X, y, n_repeats=10, random_state=42)
```

> 🔍 **The logic of permutation importance is dead intuitive**: **shuffle** one column's data, then see how much the model's AUC **drops**. The bigger the drop = the more important that column (the model relies on it heavily); almost no drop = it's dispensable. It's like pulling one clue off the intern's chart and seeing how much their judgment accuracy falls.
>
> 🧭 **Key reminder**: **important ≠ causal**. That a column helps **predict** doesn't mean changing it will **prevent disease** (that's Ch12, causal inference). It's worth cross-checking against Ch06's adjusted OR—if ML and regression point to the same set of risk factors, the conclusion is more credible.

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
