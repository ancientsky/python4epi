# 11 Deep Learning (PyTorch): When to Use It, and When It's Overkill

## What You'll Learn

- Write a PyTorch **training loop** (forward → loss → backward → step) and use **early stopping** to avoid overfitting on small samples
- Build out **sequence forecasting** with LSTM / CNN, and see why a "leading indicator" lets deep learning beat a naive baseline
- A **decision framework**: when deep learning is worth reaching for, and when traditional statistics or simple ML is already enough (don't bring a sledgehammer to swat a fly)
- A guided tour of the modern deep learning landscape: GNNs (graph neural networks), spatiotemporal Transformers / TFT, DeepSurv, time-series foundation models (TSFM), and PINNs (physics-informed neural networks)
- How to **evaluate** prediction / classification models, and how to open the black box with SHAP and attention weights

## The Scenario

The director's question from Ch10 is still ringing in your ears: "Can you build a model that, just from a new resident's basic information, predicts whether they'll get infected?" In Ch10 you ran the honest experiment with sklearn — Logistic Regression and Random Forest tied on the 280-row dataset, both hovering around AUC 0.6: honest, but not exactly dazzling.

This time a colleague leans over:
> "I hear deep learning is powerful — want to give it a try? Maybe it can pick up some complex interaction we haven't thought of."

That's a fair question, but the answer isn't "just go for it." This chapter answers it honestly in two parts:

**Part A (hands-on)** first actually runs a PyTorch neural network on the same 280-row dataset, to see whether it can beat the Ch10 sklearn baseline — then switches to a task deep learning is genuinely good at (**sequence forecasting**), to see how and why it wins. **Part B (a guided tour)** gives you a quick tour of deep learning's modern landscape — graph neural networks, Transformers, time-series foundation models, physics-informed neural networks — tools that won't be executed in this book, but knowing when they belong on the table matters just as much as knowing how to write `nn.Sequential`.

---

## 🧠 Super-Simple Special: Training a Rookie Detective

> Feeling dizzy from all the jargon — neuron, backprop, epoch? Don't worry. This section uses **one single metaphor** to string together the entire deep learning training process: **think of training a neural network as training a rookie detective to solve cases.**

A rookie detective (the model) starts out knowing nothing, working purely on gut instinct. You hand them a stack of old cases whose answers you already know (the training data), and have them practice again and again: guess, check the answer, review what went wrong, adjust how they judge things — practicing until they build up "experience" and can get seven or eight out of ten right on a brand-new case. That whole training process is the deep learning training loop.

```{figure} images/dl_intern_detective_en.svg
:name: fig-dl-intern-detective
:alt: Five steps in training a rookie detective: guessing on instinct maps to the neuron, practicing repeatedly with known answers maps to the training loop, reviewing what went wrong maps to backprop, knowing when to stop maps to early stopping, and graduating to real casework maps to deploy; labeled below: weights = experience, loss = how wrong, epoch = one round of practice
:width: 100%

Training a rookie detective = a deep learning training recipe: gut instinct → repeated practice → review → know when to stop → graduate.
```

### The whole training process in five lines

> 💡 **neuron ＝ guessing on instinct**: the detective looks at a pile of clues (input), weighs each clue's "credibility" (weight) in their head, and combines them into a judgment.
>
> 📖 **training loop ＝ practicing with the answer key in hand**: take a stack of old cases with known outcomes, and over and over have the detective guess, then tell them the right answer — guess (forward) → score how far off (loss) → review (backward) → adjust how they judge (update), round after round.
>
> 🔍 **backprop ＝ tracing back where the judgment went wrong**: when a case gets solved wrong, it's not enough to say "missed it this time" — you have to trace backward: which step of the judgment (which weight) is responsible, so you know which direction to adjust.
>
> 🛑 **early stopping ＝ knowing when to stop**: practice isn't "the longer, the better" — over-practice and the detective starts "memorizing" the details of this particular batch of old cases (overfitting), and actually does worse on a genuinely new case. An **epoch** is "one full pass through all the old cases"; knowing when to stop means calling it quits once several rounds in a row bring no improvement, and handing the trophy to whichever round performed best — not to the very last round, which has probably gone off the rails from over-practicing.
>
> 🎓 **deploy ＝ graduating to real casework**: training is over; armed with the accumulated experience (weights), the detective heads out to handle real new cases.

### Detective's world ↔ DL terminology

| The detective's world | DL term | In one line |
|---|---|---|
| Judging a case on gut instinct | **Neuron** | Each clue (input) is multiplied by "how credible it is" (weight), summed up, and decides whether to act on it (activation) |
| Building up casework experience | **Weights** | Random guesses before training; after training, they become "cases like this are usually..." experience values |
| Practicing repeatedly with the answer key | **Training loop** | forward guesses once, loss scores how wrong, backward reviews, update adjusts the experience |
| How wrong this time | **Loss** | The gap between the guess and the right answer — the smaller the number, the more accurate the guess |
| Tracing back "which step of the judgment is responsible" | **Backprop** | Working backward from the wrong outcome to compute how much each weight should be adjusted |
| Finishing one full pass through all the cases | **Epoch** | Having seen every training case once is called one epoch |
| Memorizing past cases by rote, then failing on new ones | **Overfitting** | The practice cases are memorized cold, but performance collapses on a fresh batch of cases |
| Knowing when to stop, instead of practicing until it backfires | **Early stopping** | Stop once the validation score stops improving, and roll back to the experience from the best round |

Different cases call for detectives with different specialties — this logic unfolds into a full "model zoo" in Part B: the MLP is the generalist who can take on any case, the LSTM is the veteran detective with a good memory who can follow an entire case's narrative arc, the CNN is the forensic examiner who hunts for local fingerprints, the GNN is the analyst who knows the social network inside out... each has the type of case it's best suited for.

> ⚠️ **An honest word: deep learning is a sledgehammer, not a cure-all.** No matter how sharp the detective, too few clues in a case (like this book's 280 rows) still can't crack it — and in that situation, calling in a seasoned veteran detective (logistic regression) is faster, more accurate, and far easier to explain the reasoning to the judge (the treating clinician). The decision framework in the next section teaches you how to judge whether this particular job calls for swinging that sledgehammer.

---

<!-- video: ch11_01_dl_intuition -->
<!-- /video -->

## Core Concepts

Before writing any PyTorch, let's translate the metaphor from the last section into formal technical terms.

### Neuron, Layer, Activation: What Is a Neural Network Actually Computing?

```{figure} images/neuron_layer_anatomy_en.svg
:name: fig-neuron-layer-anatomy
:alt: Anatomy of a neuron: inputs are multiplied by weights, summed, plus a bias, then passed through an activation (ReLU) to produce the output; lining up the same neuron in a row and stacking several rows is what makes "deep" learning "deep"
:width: 100%

A neuron does exactly one thing: weighted sum → add bias → pass through activation. Line them up in a row, stack several rows, and you get a whole network.
```

A **neuron**'s computation boils down to one line of math:

$$z = \sum_i x_i w_i + b, \qquad \hat{y} = \text{ReLU}(z) = \max(0, z)$$

- Each input $x_i$ is first multiplied by its own **weight** $w_i$ — how credible this particular clue is
- Everything is summed, plus a **bias** $b$ — adjusting where the "baseline" sits
- The result is fed through an **activation** function — here the most common choice, **ReLU**: negatives are zeroed out, positives pass through unchanged
- What happens without an activation? Stack as many `Linear` layers as you like, and mathematically it's still equivalent to a single layer of linear regression — the activation is what makes a neural network genuinely "non-linear," able to capture complex interactions

Line the same neuron up in a row (a **layer**), and stack input layer → hidden layer → output layer one after another — that's the "deep" in "deep learning": the more layers stacked, the more complex a function it can, in theory, express (but also the more prone to overfitting — see the next section).

<!-- video: ch11_02_neuron_layer -->
<!-- /video -->

### The Training Loop: Loss, Gradient Descent, Backprop, Epoch

```{figure} images/training_loop_en.svg
:name: fig-training-loop
:alt: Four steps of the training loop: forward computes the current guess, loss scores how far off it is from the right answer, backprop traces backward to assign responsibility, update nudges the weights; one full circuit is one epoch; a side panel shows val loss ticking back up as a warning sign of overfitting, with early stopping calling it quits at the early-stop point
:width: 100%

One trip around the training loop = one epoch. The right-hand panel shows when to call it quits — val loss no longer improving (or even climbing back up) is the overfitting warning sign.
```

Every PyTorch model's training follows the same four-beat rhythm:

1. **forward**: data flows through the network, producing the current guess
2. **loss**: compare the guess against the right answer and compute a single number for "how wrong" — classification typically uses `BCEWithLogitsLoss`, regression typically uses `MSELoss`
3. **backprop**: working backward from the loss, the chain rule computes how responsible each weight is for this error (the gradient)
4. **update (gradient descent)**: the optimizer (e.g. Adam) nudges each weight a little in the direction of the gradient, so next time the loss is a bit smaller

Running all the training data through this four-beat rhythm once is called one **epoch**. Training usually needs many epochs, gradually driving the loss down round after round.

<!-- video: ch11_03_training_loop -->
<!-- /video -->

### Overfitting and Early Stopping: When to Call It Quits

What happens if you just keep training? **Overfitting**: the model memorizes every detail of the training data (noise included), the train loss keeps sinking, but the val loss falls and then rises — a "V-shaped rebound." That rebound point is the signal that the model has started rote-memorizing the training data instead of learning to generalize.

**Early stopping** is the fix: monitor the validation loss while training, and the moment `patience` rounds in a row go by without a new record, stop early and roll back to the weights from the best-performing round — not the weights at the moment training happened to end (which is likely already overfit). This is the technical version of "knowing when to stop" from the rookie-detective metaphor.

---

<!-- video: ch11_04_overfitting_earlystop -->
<!-- /video -->

## 🧭 Decision Framework: Should You Use DL? (Don't Bring a Sledgehammer to Swat a Fly)

```{figure} images/dl_decision_tree_en.svg
:name: fig-dl-decision-tree
:alt: Should-you-use-deep-learning decision tree: under 1,000 rows, use traditional statistics or simple ML; if you need clear causality or mechanism, use SEIR plus simple ML; only reach for DL when the data is high-dimensional, non-linear, spatiotemporal, long-sequence, and large enough; for a new pathogen with very little data early on but plenty of other outbreak data available externally, use TSFM zero-shot or few-shot; if none of the above applies, the Ch10 sklearn baseline is the most efficient choice
:width: 100%

Work through it top to bottom, and stop at whichever box fits — for most epi datasets, the answer stops at the very first box.
```

Four questions, asked in order:

1. **Fewer than 1,000 rows?** (e.g. this book's 280-row Legionella dataset) → use traditional statistics / simple ML, which is steadier and more interpretable on small samples
2. **Do you need clear causality or mechanism — not just "will it happen" but "why"?** → a mechanistic model (like Ch07's SEIR) + a handful of features; DL is a black box here and won't help
3. **High-dimensional, non-linear, spatiotemporal, long sequences — and genuinely enough data?** → now it's DL's turn (CNN / LSTM / Transformer, etc.)
4. **A new pathogen with barely any data yet, but plenty of data already out there from other outbreaks?** → borrow a pretrained TSFM for zero-shot / few-shot prediction, instead of waiting for your own data to accumulate

Most epi datasets — this book's Legionella data included — stop right at **the first box**.

### Good Fit for DL vs. Overkill (Skip It)

| ✅ Good fit for DL | ❌ Overkill (skip DL) |
|---|---|
| Large data volume (thousands of rows or more) | Small samples (< 1,000 rows) |
| High-dimensional, non-linear, with complex interactions | Low-dimensional tabular data that linear / tree models already express well |
| Images, long sequences, spatiotemporal data | Cross-sectional data, one row independent of the next |
| A relevant pretrained model to transfer from (TSFM zero-shot) | No relevant pretrained resource, and data is scarce |
| Traditional / ML baselines already tried and still not good enough | DL reached for before any baseline has even been run |

### Is It Reasonable for the 280-Row Legionella Data?

Run the decision framework against this book's data, and the answer is clear:

| Consideration | Conclusion |
|------|------|
| Sample size | 280 rows is far below the thousands DL usually needs |
| Feature dimensionality | About 15 dimensions — logistic regression already expresses this fine |
| Overfitting risk | DL parameter count ≫ sample size → overfitting risk is very high |
| Educational value | Worth learning PyTorch syntax and the training loop — it'll pay off later with images or large-sample data |
| Practical advice | Use the Ch10 sklearn baseline; keep DL as a learning tool (Part A Step 1 below verifies this conclusion firsthand) |

> 🧭 **Iron rule**: run the traditional statistics / ML baseline first; only consider DL if it's not good enough **and** the conditions in the decision tree above are met. Deep learning is a sledgehammer — Part A of this chapter will let you see with your own eyes: swung at a fly (280-row classification) the sledgehammer shows no advantage, but swung at what it's built for (sequence forecasting), it really does cut sharper.

---

<!-- video: ch11_05_when_to_use_dl -->
<!-- /video -->

## Splitting the Data: Train / Val / Test for Time Series

Ch10 taught the train / val / test three-way split for cross-sectional data — `shuffle=True` was safe there, because every row is independent of every other. **Time series is completely different**: the data has a direction, and the future must never be allowed to leak back and contaminate the past.

```{figure} images/timeseries_split_en.svg
:name: fig-timeseries-split
:alt: Illustration of time series splitting: randomly shuffled K-fold lets future test segments leak into past training data, letting the model peek at the answer; the correct approach is a rolling or expanding window, with train, val, and test laid out in time order, the arrow always pointing toward the future
:width: 100%

❌ Random shuffling: future test segments leak into the training data, and the model peeks at the answer. ✅ Split by time: train → val → test laid out in time order, the arrow always pointing toward the future.
```

> ⚠️ **Why can time series never be randomly shuffled?** With an ordinary ML-style random K-fold, a given fold's training set might include "future" data points — the model effectively gets to peek at the exam answers ahead of time. The offline validation score will be badly inflated, and only once it's live do you discover it's actually not accurate at all. This is the time-series version of data leakage (**future leakage**).

The correct approach is to **split in chronological order**, typically with one of two kinds of windows:

- **Rolling window**: keep the training window's length fixed and slide it forward through time (e.g. always train on "the past 300 days")
- **Expanding window**: the training set only ever grows, adding a new chunk of time each round (e.g. "from day 1 to now" all goes into training)

**Split ratio**: a common starting point is **train 70% / val 15% / test 15%**, with all three segments **laid out in chronological order** — train is always the earliest segment, test is always the latest, and val sits in between; val / test must never fall earlier in time than train. The sequence-forecasting example in Part A Step 2 below is split in exactly this spirit: a large early stretch for training + validation, and a final stretch of days the model has never seen at all as the test set.

---

## Part A — Hands-On (Runnable, No GPU Needed)

Part A has two steps, and the full code for both runs fine without a GPU in the matching notebooks:

- **Step 1**: run a PyTorch classification model on the 280-row Legionella data, and honestly check whether "deep learning beats sklearn on a small sample" — full code in [`11_dl_baseline.ipynb`](notebooks/11_dl_baseline.ipynb)
- **Step 2**: switch to a task deep learning is genuinely good at — **sequence forecasting** with LSTM / CNN — and see how and why it wins — full code in [`11_dl_sequence.ipynb`](notebooks/11_dl_sequence.ipynb)

Below, only the most important snippets from each notebook are walked through; for the full pipeline (including learning curves, permutation importance, and more) open the notebook and run it cell by cell.

### Step 1 — MLP Baseline (280-Row Classification)

**① Data preprocessing: turning the medical-chart table into tensors PyTorch can read**

```python
import pandas as pd
import numpy as np
import torch
from torch import nn
from sklearn.preprocessing import StandardScaler

torch.manual_seed(42)
np.random.seed(42)

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

num_cols = ["age"]
cat_cols = ["sex", "smoking_history", "functional_status", "wing"]
bin_cols = [
    "floor", "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed", "shower_use", "hydrotherapy_use",
]

X_df = pd.get_dummies(df[num_cols + cat_cols + bin_cols], drop_first=True)
X_np = X_df.values.astype(np.float32)
y_np = df["infected"].values.astype(np.float32)

scaler = StandardScaler()
X_np[:, 0] = scaler.fit_transform(X_np[:, 0:1]).ravel()

idx = np.arange(len(X_np))
np.random.shuffle(idx)
split = int(0.7 * len(idx))
train_idx, val_idx = idx[:split], idx[split:]

X_train = torch.tensor(X_np[train_idx])
y_train = torch.tensor(y_np[train_idx]).unsqueeze(1)
X_val = torch.tensor(X_np[val_idx])
y_val = torch.tensor(y_np[val_idx]).unsqueeze(1)
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `pd.get_dummies(..., drop_first=True)` | One-hot encodes categorical columns (`sex`, `wing`, …) into 0/1 dummy variables |
> | `X_np = X_df.values.astype(np.float32)` | Converts to a NumPy array and casts to `float32` — PyTorch weights default to single precision, so the types must match |
> | `scaler.fit_transform(X_np[:, 0:1])` | Standardizes only `age`; neural networks are sensitive to input scale, and skipping this slows convergence or breaks it outright |
> | `np.random.shuffle(idx)` → 70/30 split | Manually shuffle the indices and split out train / validation sets (same as the cross-sectional data in Ch10 — safe to shuffle here) |
> | `y_train = torch.tensor(...).unsqueeze(1)` | Reshapes y from a 1-D `(N,)` array into 2-D `(N, 1)`, matching the model's output shape |

> 💡 **Translating a medical chart into tensors**: PyTorch doesn't eat DataFrames, only **tensors**. These lines look fiddly, but each step corresponds to something sklearn's `Pipeline` normally handles for you automatically — doing it by hand, deliberately spelled out, makes it much clearer what's happening at every stage.

**② Model architecture: three linear layers stacked into the smallest useful neural network**

```python
input_dim = X_train.shape[1]

model = nn.Sequential(
    nn.Linear(input_dim, 32),
    nn.ReLU(),
    nn.Linear(32, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
)

n_params = sum(p.numel() for p in model.parameters())
print(f"Total parameters: {n_params}, parameter/sample ratio: {n_params / len(X_train):.1f}")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `nn.Sequential(Linear → ReLU → Linear → ReLU → Linear)` | Stacks layers into a pipeline: `Linear` does the linear combination, `ReLU` adds non-linearity, and the final `Linear(16, 1)` outputs a single logit |
> | No activation after the last layer | Left for `BCEWithLogitsLoss` in the next step to handle the sigmoid internally, which is more numerically stable |
> | `n_params = sum(p.numel() ...)` | Sums the element count of every weight + bias, quantifying "how much this model has to tune" |

> ⚠️ **Parameter/sample ratio > 1**: this architecture has roughly 700 parameters, and the training set only has about 196 rows — more parameters than samples, so the overfitting risk is extremely high. This printed number is the concrete evidence of "bringing a sledgehammer to swat a fly."

**③ Training loop + early stopping**

```python
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

best_val_loss = float("inf")
patience, counter = 15, 0
best_state = None

for epoch in range(300):
    model.train()
    optimizer.zero_grad()
    loss = loss_fn(model(X_train), y_train)
    loss.backward()
    optimizer.step()

    model.eval()
    with torch.no_grad():
        val_loss = loss_fn(model(X_val), y_val).item()

    if val_loss < best_val_loss:
        best_val_loss = val_loss
        best_state = {k: v.clone() for k, v in model.state_dict().items()}
        counter = 0
    else:
        counter += 1

    if counter >= patience:
        print(f"Early stopping at epoch {epoch}")
        break

model.load_state_dict(best_state)
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `optimizer.zero_grad()` | Clears gradients left over from the previous round (PyTorch accumulates gradients by default — skip this and they'd keep piling up) |
> | `loss = loss_fn(model(X_train), y_train)` | forward + compute loss: data flows through the network to produce logits, then compared against the true labels |
> | `loss.backward()` | backprop: automatic differentiation computes the gradient of the loss with respect to every parameter |
> | `optimizer.step()` | Updates every parameter based on the just-computed gradients (following the Adam optimizer's rule) |
> | `if val_loss < best_val_loss: ... else: counter += 1` | The heart of early stopping: save a checkpoint and reset `counter` to zero whenever val_loss improves; otherwise increment it |
> | `model.load_state_dict(best_state)` | After training ends, "rewind" to the weight snapshot from the lowest val_loss |

> 🧭 **Knowing when to stop**: once `patience` rounds in a row go by without a new record, hand the trophy to whichever round performed best — not to the model's state at the moment training happened to end (which has likely already started overfitting).

**The honest result**: running the complete pipeline in [`11_dl_baseline.ipynb`](notebooks/11_dl_baseline.ipynb) (including the learning curve, AUC evaluation, and comparison with sklearn), the validation set comes out at **AUC ≈ 0.63** — almost dead even with Ch10's Logistic Regression and Random Forest (both around 0.6), with no clear advantage on display.

| Model | Val AUC (same train/val split) |
|---|---|
| Logistic Regression | ≈ 0.6-ish |
| Random Forest | ≈ 0.6-ish |
| PyTorch DL (MLP) | ≈ 0.63 |

The reason lines up exactly with the decision framework earlier in this chapter: 280 rows is nowhere near enough to support a 700-parameter neural network learning anything sklearn couldn't already learn — **on small data, DL has no edge.** The educational value of this step isn't "beating sklearn" — it's genuinely learning PyTorch's training-loop syntax, in preparation for a task in Step 2 where DL is truly the right tool.

<!-- video: ch11_06_mlp_baseline -->
<!-- /video -->

### Step 2 — Sequence Forecasting: LSTM / CNN

280 rows of cross-sectional data leave DL tied with sklearn — so what about a **sequence forecasting** task instead? [`11_dl_sequence.ipynb`](notebooks/11_dl_sequence.ipynb) doesn't use the Pine and Cypress Nursing Home data (it doesn't have a long enough daily sequence) — instead it uses a **synthetic teaching dataset of daily "dengue fever × temperature" series**: temperature is a noisy, seasonal **leading indicator** available ahead of time each day, and case counts are driven jointly by "temperature 7 days ago" and "yesterday's case count." The task: given the past 21 days of (cases, temperature), predict the case count **7 days ahead**.

**① Synthesizing the data: hiding a "cheat code" — the leading indicator**

```python
torch.manual_seed(1)
np.random.seed(1)

n = 360
t = np.arange(n)

# Temperature: seasonal sine wave + random noise (a known leading indicator available ahead of time)
temp = 24 + 7 * np.sin(2 * np.pi * (t - 30) / 365) + np.random.normal(0, 1.0, n)
drive = np.clip(temp - 24, 0, None)  # Only temperatures above 24°C drive transmission (hotter -> more active mosquito vectors)

cases = np.zeros(n)
for i in range(n):
    lag = cases[i - 1] if i >= 1 else 0
    cases[i] = max(
        0,
        0.55 * lag                                   # carryover from yesterday's case count
        + 3.2 * (drive[i - 7] if i >= 7 else 0)       # delayed effect of temperature 7 days ago (the leading indicator)
        + 4 * np.sin(2 * np.pi * t[i] / 7)            # weekly reporting rhythm
        + 6                                            # baseline case count
        + np.random.normal(0, 2.0),                   # random noise
    )
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `temp = 24 + 7*sin(...) + noise` | Temperature: seasonal fluctuation + noise, a **leading indicator** that's "known, available ahead of time" |
> | `drive = np.clip(temp - 24, 0, None)` | Only the portion of temperature above 24°C drives transmission (hotter → more active mosquito vectors) |
> | `3.2 * drive[i - 7]` | Today's case count is driven by temperature **7 days ago** — this is the leading indicator's delayed effect |
> | `0.55 * lag` | Carryover from yesterday's case count (autocorrelation of transmission) |

> 💡 **This data-generating process (DGP) deliberately hides a "cheat code"**: temperature knows the answer 7 days before case counts do. For LSTM / CNN to win, it's not because "the model is fancier" — it's whether it can learn to exploit this leading indicator.

**② Sliding window + time split (never shuffle)**

```python
H = 7   # forecast horizon: how many days ahead
L = 21  # lookback: how many days of history
feats = np.stack([cases, temp], axis=1).astype(np.float32)

split = n - 60  # the last 60 days are the test set
mu = feats[:split].mean(axis=0)
sd = feats[:split].std(axis=0)
z = (feats - mu) / sd


def windows(s, e):
    Xs, ys, idxs = [], [], []
    for i in range(s, e - H):
        Xs.append(z[i - L:i])
        ys.append(z[i + H - 1, 0])
        idxs.append(i + H - 1)
    return np.array(Xs, dtype=np.float32), np.array(ys, dtype=np.float32), np.array(idxs)


Xtr_full, ytr_full, idxtr_full = windows(L, split)
val_start = split - 40
train_mask = idxtr_full < val_start
Xtr, ytr = Xtr_full[train_mask], ytr_full[train_mask]
Xval, yval = Xtr_full[~train_mask], ytr_full[~train_mask]
Xte, yte, idxte = windows(split - H + 1, n + 1)
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `mu = feats[:split].mean(...)` / `sd = feats[:split].std(...)` | The standardization mean / std are computed **only from the training range** — no peeking at the test set |
> | `windows(s, e)` | Sliding window: each sample's X = the past L days, y = the case count H days ahead |
> | `train_mask = idxtr_full < val_start` | Splits out the validation set in chronological order (no shuffling) |
> | `Xte, yte, idxte = windows(...)` | The last 60 days become the test set, which the model has never seen |

> ⚠️ Not a single `shuffle=True` appears here — shuffle a sequence dataset's split and future windows leak into the training set, the model effectively gets to see the answer, and the offline performance is badly overstated (compare against the time-series split figure earlier in the chapter).

**③ LSTM model: a detective with a memory**

```python
class LSTMModel(nn.Module):
    """Reads the past L days of (cases, temp) with an LSTM and outputs a prediction for the case count H days ahead."""

    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=2, hidden_size=32, batch_first=True)
        self.fc = nn.Linear(32, 1)

    def forward(self, x):
        out, _ = self.lstm(x)      # out shape: (batch, L, 32)
        last_step = out[:, -1, :]  # take only the hidden state at the final time step, after reading the whole sequence
        return self.fc(last_step)
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `nn.LSTM(input_size=2, hidden_size=32, batch_first=True)` | Two input features (cases, temp); a 32-dimensional "memory" is updated at every time step |
> | `out, _ = self.lstm(x)` | Lets the LSTM read through the 21-day sequence, updating its internal memory at each step |
> | `last_step = out[:, -1, :]` | Takes only the final hidden state, after reading the entire history — a summary of the whole case narrative |
> | `self.fc(last_step)` | Turns the summary into a single number: the predicted case count 7 days ahead |

> 🕵️ **LSTM = a detective with a memory**: after reading through 21 days of clues, what's left in its head isn't a fragment of the last day, but **a summary of the whole case narrative** — "has the case count been climbing all week? has temperature stayed elevated?" That's exactly why it's able to pick up trends and delayed effects. The training loop follows the exact same four-beat rhythm as Step 1, with one addition — a "warm-up period": let the model train for a while first before patience starts counting, so it isn't fooled into stopping too early by a validation score that's still bouncing around. (The 1D-CNN uses the same training function, just swapping in a two-layer `nn.Conv1d` stack, with a small sliding window that picks up local shapes instead.)

**④ Persistence baseline + result comparison**

```python
persistence_pred = np.array([cases[j - H] for j in idxte])


def mae_score(pred, idxs):
    return np.mean(np.abs(pred - cases[idxs]))


print(f"{'Model':<24}{'MAE':>8}")
for name, pred in [
    ("Persistence (naive baseline)", persistence_pred),
    ("LSTM", lstm_pred),
    ("1D-CNN", cnn_pred),
]:
    print(f"{name:<24}{mae_score(pred, idxte):>8.3f}")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `persistence_pred = ... cases[j - H]` | The **naive baseline**: assumes "the case count 7 days from now = the last known case count right now," using no temperature and no model at all |
> | `mae_score(pred, idxs)` | Mean absolute error (MAE): how many cases off the prediction is from the truth |
> | The loop prints all three models' MAE | Puts DL on the same scorecard as "doing nothing at all" |

> 🧭 **The first checkpoint for evaluating a sequence forecast**: if a model can't beat persistence, all its added complexity was wasted.

**The honest result**:

| Model | MAE |
|---|---|
| Persistence (naive baseline) | 2.88 |
| LSTM | **2.15** |
| 1D-CNN | 2.20 |

This time DL really does win, and by a solid margin. **Why?**

1. **It uses the leading indicator**: persistence can only see the case count itself, with no idea that temperature already rose 7 days ago and case counts are, in all likelihood, about to rise 7 days from now; LSTM / CNN feed that extra temperature signal in alongside cases
2. **The DGP contains a non-linear, time-delayed interaction** (temperature 7 days ago drives today's case count), exactly the kind of pattern a neural network is good at picking up

**When is a naive baseline hard to beat?** If a curve is a simple, smooth univariate series (no extra leading indicator, no obvious non-linear delay), persistence or a simple moving average is often already quite strong, and a complex model may not clear it by much — adding an LSTM / CNN in that case may just be piling on complexity and overfitting risk. In practice, whenever you face a sequence forecasting task, **always run a naive baseline first** before deciding whether to reach for a model — the exact same spirit as the decision framework earlier in the chapter.

---

<!-- video: ch11_07_lstm_cnn_sequence -->
<!-- /video -->

## Part B — A Tour of Modern DL (Conceptual Overview, Not Executed in This Book)

Part A showed you two faces of deep learning: overkill on small-sample classification (can't beat sklearn), genuinely sharper on sequence forecasting once there's a leading indicator to exploit. But deep learning's territory extends far beyond MLP, LSTM, and CNN. The tools below **are not executed in this book** (they need extra packages, a GPU, or an internet connection to download large pretrained weights) — presented here as "metaphor + epi use case + when to use it + tools + illustrative code" for a quick tour, so you know which tool to reach for when you run into a given problem down the road.

```{figure} images/dl_model_zoo_en.svg
:name: fig-dl-model-zoo
:alt: The DL model zoo: MLP is the default starting point for tabular data; LSTM is the detective with a memory, suited to sequences with time dependence; CNN is the forensic examiner who spots local fingerprints, suited to extracting local features; GNN is the social-network analyst, suited to spatial transmission and contact networks; Transformer or TFT knows how to allocate attention, suited to long-sequence multivariate forecasting; PINN is the model bound by physical law, suited to scarce data with a clear mechanism such as SEIR; TSFM is the veteran who has read every case worldwide, suited to zero-shot, few-shot, and the early days of a new pathogen
:width: 100%

Look at the shape of the problem, and you'll know who to call — different tasks call for models with different specialties.
```

### GNN (Graph Neural Network) — The Social-Network Analyst

- **Metaphor**: like an analyst who knows the social network inside out, looking not just at each person's own traits but at "who's connected to whom"
- **epi use case**: contact-tracing networks (who shared a room, who shared an activity), cross-facility referral networks, spatially adjacent transmission
- **When to use it**: the data naturally forms a "nodes + edges" graph structure, and the relationships themselves carry predictive power (e.g. a resident's infection risk is high partly because they had contact with many already-infected people)
- **Tools**: `torch-geometric` (PyG), `DGL`

```python
# illustrative only — NOT executed in this book — GNN: learning the contact network as a graph
import torch
from torch_geometric.nn import GCNConv

class ContactGNN(torch.nn.Module):
    """Nodes = residents, edges = contact history (shared room, shared activity)."""

    def __init__(self, n_features, hidden=16):
        super().__init__()
        self.conv1 = GCNConv(n_features, hidden)
        self.conv2 = GCNConv(hidden, 1)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        return self.conv2(x, edge_index)  # each resident's infection risk score
```

### Spatiotemporal Transformer / TFT — Knowing How to Allocate Attention

- **Metaphor**: like a secretary who knows how to allocate attention, automatically figuring out, across a long stretch of data, "which day, which variable deserves more attention for this particular prediction"
- **epi use case**: watching case counts, temperature, foot traffic, vaccination coverage, and other leading indicators all at once, forecasting many days ahead
- **When to use it**: the sequence is long enough (usually hundreds to thousands of time points), there are multiple covariates, and interpretable attention weights are needed
- **Tools**: `pytorch-forecasting` (Temporal Fusion Transformer, TFT), Hugging Face's time-series transformer models

```python
# illustrative only — NOT executed in this book — Temporal Fusion Transformer: multivariate outbreak forecasting
from pytorch_forecasting import TemporalFusionTransformer, TimeSeriesDataSet

training = TimeSeriesDataSet(
    df, time_idx="day", target="cases", group_ids=["region"],
    time_varying_known_reals=["temperature", "humidity"],
    time_varying_unknown_reals=["cases"],
    max_encoder_length=60, max_prediction_length=14,
)
tft = TemporalFusionTransformer.from_dataset(
    training, hidden_size=16, attention_head_size=4,
)
```

### DeepSurv — A Neural-Network Version of Cox Regression

- **Metaphor**: Ch09's Cox regression assumes every factor's contribution to log(hazard) adds up linearly; DeepSurv swaps that linear relationship for a neural network, giving non-linearity and interactions among risk factors a chance to be learned
- **epi use case**: survival analysis (echoing Ch09) where you suspect non-linearity or interaction among risk factors, or the data is high-dimensional (genomic, imaging)
- **When to use it**: Cox's proportional-hazards assumption may not hold, and there's enough data to support a neural network without overfitting
- **Tools**: `pycox` (DeepSurv, CoxTime, DeepHit)

```python
# illustrative only — NOT executed in this book — DeepSurv: replacing Cox's linear log(HR) with a neural network
import torchtuples as tt
from pycox.models import CoxPH

net = tt.practical.MLPVanilla(in_features=10, num_nodes=[32, 32], out_features=1)
model = CoxPH(net, tt.optim.Adam)
model.fit(x_train, (duration_train, event_train), epochs=100)
```

### TSFM (Time Series Foundation Model) — The Veteran Who's Read Every Case Worldwide

**Time Series Foundation Models (TSFM)** are pretrained on massive, cross-domain time series, and when applied to a new series, usually need no retraining at all (**zero-shot**) or only a tiny bit of fine-tuning data (**few-shot**) — exactly the idea behind **transfer learning**: borrowing knowledge already learned from someone else's mountain of data, and applying it directly to your own short new series.

| TSFM | Core idea | Advantage | Tool |
|---|---|---|---|
| **TimesFM** (Google) | Decoder-only transformer, pretrained on massive time series | Zero-shot forecasting, no retraining needed | `timesfm` |
| **Chronos** (Amazon) | Tokenizes time-series values and applies a language-model architecture | Open source, multiple model sizes available | `chronos-forecasting` |
| **Moirai** (Salesforce) | A general-purpose multivariate time-series foundation model | Supports different frequencies and multivariate input | `uni2ts` |
| **TimeGPT** (Nixtla) | Commercial API, a GPT-style time-series model | Easy to get started, hosted API available | `nixtla` |

```python
# illustrative only — NOT executed in this book — TSFM zero-shot forecasting (no local training at all)
import timesfm

tfm = timesfm.TimesFm(context_len=512, horizon_len=14, backend="cpu")
tfm.load_from_checkpoint(repo_id="google/timesfm-1.0-200m")
forecast, _ = tfm.forecast([cases_history], freq=[0])  # predicts directly, with no fit() step at all
```

> ⚠️ **TSFM needs to download large weights and needs an internet connection** — this book's build doesn't execute this snippet — but this is exactly the answer to box ④ of the decision tree earlier: with barely any data in the early days of a new pathogen, you can still borrow a model pretrained on "someone else's outbreak data," instead of starting from scratch and waiting for your own data to accumulate.

### Hybrid / Knowledge Injection (Most Recommended for Epidemiologists)

Pure "black-box DL" and pure "mechanistic models" each hit their own limits: DL doesn't understand biological mechanism and can produce implausible curves when data is scarce; mechanistic models (like Ch07's SEIR) understand the mechanism, but their parameters are hard to fit and they struggle with complex non-linear relationships. Combining the two is epidemiology's most pragmatic path.

**PINN (Physics-Informed Neural Network)**: the model sits two exams at once — one asking "does this match the observed data," the other asking "does this obey the SEIR differential equations."

```{figure} images/pinn_seir_loss_en.svg
:name: fig-pinn-seir-loss
:alt: Illustration of a PINN: the model must get two things right at once — L_data, the data error, measures the gap between the model's prediction and the actually observed case counts, keeping the model accurate; L_physics, the physics residual, measures whether S, E, I, R obey the SEIR differential equations, keeping the model plausible; the two are added together into the total loss
:width: 100%

A PINN's loss = L_data (fitting the data) + L_physics (obeying the SEIR equations) — neither one is optional.
```

- **Metaphor**: a model bound by physical law — no matter how accurate the guess, if it violates the logic of the SEIR equations (e.g. a headcount going negative, or a recovered person turning susceptible again), it gets penalized
- **epi use case**: an emerging disease with scarce data but a clear mechanism (an outbreak has just started, with only a handful of daily notification counts, but the SEIR structure is already known)
- **When to use it**: very few samples, a clear biological / transmission mechanism, and you want a curve that is "epidemiologically sensible" rather than one that's just fitting noise
- **Tools**: typically hand-coded in PyTorch (`nn.Module` + a custom loss), or a general-purpose PINN framework like `DeepXDE`

```python
# illustrative only — NOT executed in this book — PINN: writing the SEIR equations into the loss
def pinn_loss(model, t_data, y_data, t_physics, beta):
    # L_data: model prediction vs. actually observed case counts, keeping the model "accurate"
    pred = model(t_data)
    l_data = torch.mean((pred - y_data) ** 2)

    # L_physics: automatic differentiation of S w.r.t. t, checking it satisfies the SEIR differential equations, keeping the model "plausible"
    S, E, I, R = model(t_physics).split(1, dim=1)
    dS_dt = torch.autograd.grad(S.sum(), t_physics, create_graph=True)[0]
    residual = dS_dt - (-beta * S * I)  # demonstrating only the dS/dt equation here
    l_physics = torch.mean(residual ** 2)

    return l_data + l_physics
```

**Mechanistic-AI ensemble (mechanistic model + ML ensemble)**: let the mechanistic model give a first, "physically sensible" rough guess, then let ML / DL learn only the **residual the mechanistic model got wrong** — no need to learn the whole curve from scratch, and it never strays from epidemiological common sense.

- **Metaphor**: a senior attending physician (the mechanistic model) gives a rough but sensible diagnosis first, and the resident (ML) only needs to focus on correcting the details the attending is prone to miss
- **epi use case**: combining Ch07's SEIR time-series model with the ML / DL of Ch10 / Ch11, balancing interpretability against fit
- **When to use it**: you want the model's output to respect epidemiological common sense (never predicting a negative case count, never ignoring the constraint from $R_0$), but SEIR alone doesn't fit well enough on its own
- **Tools**: assembled by hand (feeding the SEIR simulation's output in as an ML feature), or by borrowing the model-ensembling concepts behind frameworks like CDC FluSight

```python
# illustrative only — NOT executed in this book — Mechanistic-AI ensemble: SEIR as the baseline, ML handles the residual
seir_forecast = run_seir_simulation(beta, gamma, sigma, initial_state)  # Ch07's mechanistic model
residual = observed_cases - seir_forecast                              # the part the mechanistic model got wrong

residual_model = RandomForestRegressor(n_estimators=200)
residual_model.fit(X_covariates, residual)          # ML learns only the residual, not the whole curve from scratch

final_forecast = seir_forecast + residual_model.predict(X_covariates_future)
```

---

<!-- video: ch11_08_dl_landscape -->
<!-- /video -->

## Evaluation and Interpretability

### Choosing Metrics

| Task | Metric | In plain words |
|---|---|---|
| Forecasting (regression) | **MAE** | Average number of cases off — the most intuitive |
| | **RMSE** | More sensitive to large errors; a single outlier gets amplified |
| | **MAPE / sMAPE** | Error as a percentage of the true value, handy for comparing across contexts |
| | **CRPS** (probabilistic forecast) | Distance between the whole predicted distribution and the true value, not just a point estimate |
| Classification | **AUC** | Ranking ability (see Ch10); **F1** balances precision and recall; **PR-AUC** suits imbalanced data |
| Calibration | **Calibration curve / Brier score** | Of the group the model calls "70% probability," does about 70% actually happen? Ranking well ≠ well-calibrated (echoing Ch10) |
| Epi-specific | **Peak-timing error** | How many days off the predicted outbreak peak date is from the actual one |
| | **Outbreak detection delay** | How many days late the model catches the signal compared to the real upswing |

### Opening the Black Box

- **SHAP**: the same fair-bonus-splitting logic as Ch10 — asking "how much worse would the prediction be without this feature" — and it applies directly to DL models too (`shap.DeepExplainer`), giving a "which clues contributed how much" breakdown for a single patient / single time point
- **Attention weights**: models like Transformer / TFT have a built-in "attention" mechanism, letting you print out directly which day, which variable, the model weighted most heavily for a given prediction — lighter-weight than SHAP, and it's an explanation the model carries with it natively
- **PDP (partial dependence plot)**: hold everything else fixed, let one feature vary, and see how the prediction moves — this works for DL models too, and is good for checking "did the model learn a dose-response relationship that makes sense"

> 🧭 The same reminder as Ch10: **important ≠ causal**. SHAP and attention tell you how heavily the model leans on a given clue to make its prediction — not that changing that feature would change the outcome. For genuine causal questions, look at Ch06's confounder-adjusted OR, or the causal inference methods in Ch12.

## Exercises

- Exercise version: [`11_dl_exercise.ipynb`](exercises/11_dl_exercise.ipynb)
- Solution version (instructor): [`11_dl_solution.ipynb`](solutions/11_dl_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/11_dl_solution.ipynb>)

## Common Misuses

| Mistake | Correct approach |
|------|---------|
| Randomly splitting time-series data (`shuffle=True`) | Split by time, using rolling / expanding windows (see the data-splitting section above); the future must never leak into training |
| Using a complex architecture on a small dataset | Check the parameter-to-sample ratio first; with 280 rows use at most 1–2 hidden layers, or skip DL altogether |
| Reporting only training-set results | Always evaluate on an independent validation / test set, and a sequence forecast must beat the naive baseline |
| Not fixing the random seed | `torch.manual_seed()` + `np.random.seed()` to ensure reproducibility |
| Ignoring uncertainty, giving only a single predicted value | Policy decisions need a confidence interval / probability distribution — not just one number to act on |
| Blind trust in a black-box model | Open the black box with SHAP / attention weights / a PINN's physical constraints |
| Assuming DL always beats traditional ML | DL ties Logistic Regression on 280-row classification; DL wins on sequence forecasting because of the leading indicator + non-linear delay, not because DL is inherently stronger |

## Why Should Epidemiologists Learn DL? — A 10-Week Learning Path

**Why it's worth learning**: real-world epidemiological data is increasingly moving onto DL's home turf — high-dimensional, noisy, non-linear data (genomics, imaging, wearable-device signals), spatiotemporal data that requires modeling spatial spread and contact networks (GNN's home turf), and situations where data is extremely scarce in the early days of an emerging pathogen's outbreak, yet global experience from other outbreaks can be borrowed (TSFM zero-shot forecasting's home turf). None of this is terrain traditional statistical methods are especially good at.

A practical 10-week self-study path, breaking this chapter's content into progressive projects:

| Week | Topic |
|---|---|
| 1–2 | Python / PyTorch basics, tensors, data preprocessing (maps to this chapter's Part A Step 1) |
| 3–4 | Training loop, early stopping, diagnosing overfitting (this chapter's core concepts + Part A) |
| 5–6 | Sequence forecasting: sliding windows, time splits, LSTM, CNN (this chapter's Part A Step 2) |
| 7 | GNN: spatial transmission, contact networks |
| 8 | Spatiotemporal Transformer / TFT: multivariate long-sequence forecasting |
| 9 | TSFM zero-shot forecasting + PINN / Mechanistic-AI ensemble |
| 10 | Project work: pick a real dataset, run the full pipeline, and write an interpretability report using SHAP / attention |

## Next Step

This chapter gave an honest answer to two questions with DL: can deep learning beat sklearn on 280 rows (not really), and where does deep learning genuinely earn its keep (sequence forecasting with a leading indicator and a non-linear delay). But no matter how accurate a model is, **strong predictive power is not the same as a causal relationship.**

In the next chapter (Ch12), we return to the most fundamental question: **does shower exposure really "cause" infection — or is it just a statistical association?** → Causal inference.
