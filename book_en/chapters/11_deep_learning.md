# 11 Deep Learning (PyTorch): Does DL Make Sense for 280 Rows?

## What You'll Learn

- Build a **binary classification neural network** with PyTorch
- Write a **training loop** by hand, with validation-set monitoring
- Implement **early stopping** to avoid overfitting
- Compare DL against the Ch10 sklearn results and discuss "when to use / when not to use DL"

## The Story

In Ch10 you built a baseline model with sklearn. A colleague asks:
> "Should we try deep learning? Maybe it can pick up complex interactions?"

You decide to build a simple neural network with PyTorch and see how it does on 280 rows of data.

---

## Step 1 — Data Preprocessing (converting to tensors by hand)

```python
import pandas as pd
import numpy as np
import torch
from torch import nn

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# Same features as Ch10
num_cols = ["age"]
cat_cols = ["sex", "smoking_history", "functional_status", "wing"]
bin_cols = [
    "floor", "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed", "shower_use", "hydrotherapy_use",
]

# One-hot encoding
X_df = pd.get_dummies(df[num_cols + cat_cols + bin_cols], drop_first=True)
X_np = X_df.values.astype(np.float32)
y_np = df["infected"].values.astype(np.float32)

# Standardize numeric features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_np[:, 0] = scaler.fit_transform(X_np[:, 0:1]).ravel()  # age

# Convert to tensors
X_tensor = torch.tensor(X_np)
y_tensor = torch.tensor(y_np).unsqueeze(1)
```

## Step 2 — Model Architecture

```python
input_dim = X_tensor.shape[1]

model = nn.Sequential(
    nn.Linear(input_dim, 32),
    nn.ReLU(),
    nn.Linear(32, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
)
```

> **Architecture**: input → 32 → 16 → 1 (sigmoid), about 700 parameters in total.

## Step 3 — Training Loop + Validation Set

```python
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# Split train / validation by hand
idx = np.arange(len(X_tensor))
np.random.seed(42)
np.random.shuffle(idx)
split = int(0.7 * len(idx))
train_idx, val_idx = idx[:split], idx[split:]

X_train, y_train = X_tensor[train_idx], y_tensor[train_idx]
X_val, y_val = X_tensor[val_idx], y_tensor[val_idx]
```

## Step 4 — Early Stopping

```python
best_val_loss = float("inf")
patience, counter = 10, 0
best_state = None

for epoch in range(200):
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
        best_state = model.state_dict().copy()
        counter = 0
    else:
        counter += 1

    if counter >= patience:
        print(f"Early stopping at epoch {epoch}")
        break

model.load_state_dict(best_state)
```

## Step 5 — Evaluation + Comparison with sklearn

```python
from sklearn.metrics import roc_auc_score

model.eval()
with torch.no_grad():
    proba = torch.sigmoid(model(X_val)).numpy()
auc = roc_auc_score(y_val.numpy(), proba)
print(f"DL Validation AUC = {auc:.3f}")
```

---

## Exercises

- Exercise version: [`11_dl_exercise.ipynb`](exercises/11_dl_exercise.ipynb)
- Solution version (instructor): [`11_dl_solution.ipynb`](solutions/11_dl_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/11_dl_solution.ipynb>)

## Common Mistakes

| Mistake | The right way |
|------|---------|
| Reporting only training-set results | Always evaluate on a validation set |
| Not fixing the random seed | `torch.manual_seed(42)` ensures reproducibility |
| Using a complex architecture on a small dataset | With 280 rows, use at most 1-2 hidden layers |
| Assuming DL always beats ML | On small samples DL overfits easily and usually loses to a simpler model |

## Does DL Make Sense for 280 Rows?

| Consideration | Conclusion |
|------|------|
| Sample size | 280 rows is far below the thousands DL usually needs |
| Feature dimensionality | ~15 dimensions; logistic regression is already enough |
| Overfitting risk | DL parameters >> sample size → high risk |
| Educational value | You learn PyTorch syntax and the training loop |
| Practical advice | Use an sklearn baseline; treat DL as a learning tool |

> **Bottom line**: In this case, DL is unlikely to beat sklearn. But learning the basics of PyTorch syntax pays off later, when you run into large-scale data (images, text, etc.).

## Next Step

We've now used statistics, ML, and DL to analyze this cluster.
In the next chapter (Ch12), we step back and think about a more fundamental question: **did shower exposure really "cause" the infections, or is it just a statistical association?** → Causal inference.
