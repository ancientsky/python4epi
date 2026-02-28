# 11 深度學習（PyTorch）：280 筆資料用 DL 合理嗎？

## 你將學到

- 用 PyTorch 建立**二元分類神經網路**
- 手動撰寫**訓練迴圈（training loop）**與驗證集監控
- 實作**早停法（early stopping）**避免過擬合
- 比較 DL 與 Ch10 sklearn 結果，討論「何時該用 / 不該用 DL」

## 情境故事

你在 Ch10 用 sklearn 建了 baseline 模型。一位同事問：
> 「要不要試試深度學習？也許能抓到複雜的交互作用？」

你決定用 PyTorch 實作一個簡單的神經網路，看看在 280 筆資料上表現如何。

---

## Step 1 — 資料前處理（手動轉 tensor）

```python
import pandas as pd
import numpy as np
import torch
from torch import nn

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# 與 Ch10 相同的特徵
num_cols = ["age"]
cat_cols = ["sex", "smoking_history", "functional_status", "wing"]
bin_cols = [
    "floor", "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed", "shower_use", "hydrotherapy_use",
]

# One-hot 編碼
X_df = pd.get_dummies(df[num_cols + cat_cols + bin_cols], drop_first=True)
X_np = X_df.values.astype(np.float32)
y_np = df["infected"].values.astype(np.float32)

# 標準化數值特徵
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_np[:, 0] = scaler.fit_transform(X_np[:, 0:1]).ravel()  # age

# 轉 tensor
X_tensor = torch.tensor(X_np)
y_tensor = torch.tensor(y_np).unsqueeze(1)
```

## Step 2 — 模型架構

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

> **架構**：input → 32 → 16 → 1 (sigmoid)，共約 700 個參數。

## Step 3 — 訓練迴圈 + 驗證集

```python
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# 手動分割訓練 / 驗證
idx = np.arange(len(X_tensor))
np.random.seed(42)
np.random.shuffle(idx)
split = int(0.7 * len(idx))
train_idx, val_idx = idx[:split], idx[split:]

X_train, y_train = X_tensor[train_idx], y_tensor[train_idx]
X_val, y_val = X_tensor[val_idx], y_tensor[val_idx]
```

## Step 4 — 早停法

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

## Step 5 — 評估 + 與 sklearn 比較

```python
from sklearn.metrics import roc_auc_score

model.eval()
with torch.no_grad():
    proba = torch.sigmoid(model(X_val)).numpy()
auc = roc_auc_score(y_val.numpy(), proba)
print(f"DL Validation AUC = {auc:.3f}")
```

---

## 練習題

- 作業版：[`11_dl_exercise.ipynb`](../exercises/11_dl_exercise.ipynb)
- 解答版（講師）：[`11_dl_solution.ipynb`](../solutions/11_dl_solution.ipynb)

## 常見誤用

| 錯誤 | 正確做法 |
|------|---------|
| 只報訓練集結果 | 一定要用驗證集評估 |
| 沒固定 random seed | `torch.manual_seed(42)` 確保可重現 |
| 小資料集用複雜架構 | 280 筆最多用 1-2 層隱藏層 |
| 用 DL 就一定比 ML 好 | 小樣本中 DL 容易 overfit，通常不如簡單模型 |

## 280 筆用 DL 合理嗎？

| 考量 | 結論 |
|------|------|
| 樣本量 | 280 筆遠低於 DL 通常需要的數千筆 |
| 特徵維度 | ~15 維，邏輯斯迴歸已足夠 |
| 過擬合風險 | DL 參數 >> 樣本數 → 高風險 |
| 教學價值 | 學會 PyTorch 語法和訓練迴圈 |
| 實務建議 | 用 sklearn baseline，DL 作為學習工具 |

> **結論**：在本案中，DL 不太可能超越 sklearn。但學會 PyTorch 的基本語法，在未來遇到大規模資料（如影像、文本）時就能派上用場。

## 下一步

我們已經用了統計、ML、DL 來分析這場群聚。
下一章（Ch12），我們退一步思考更根本的問題：**淋浴暴露真的「導致」感染嗎？還是只是統計關聯？** → 因果推論。
