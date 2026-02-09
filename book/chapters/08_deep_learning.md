# 08 深度學習（PyTorch）

## 你將學到

- 用 PyTorch 建立最小二元分類模型
- 訓練迴圈與驗證流程
- 早停（early stopping）與過擬合觀察

## 情境故事

你想嘗試非線性模型來捕捉複雜風險因子交互作用。

## 最小可執行程式碼

```python
import torch
from torch import nn

torch.manual_seed(42)

X = torch.randn(64, 6)
y = (X[:, 0] + 0.4 * X[:, 1] > 0).float().unsqueeze(1)

model = nn.Sequential(
    nn.Linear(6, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
)

loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)

for epoch in range(50):
    optimizer.zero_grad()
    logits = model(X)
    loss = loss_fn(logits, y)
    loss.backward()
    optimizer.step()

with torch.no_grad():
    pred = (torch.sigmoid(model(X)) > 0.5).float()
    acc = (pred == y).float().mean().item()
print(f"train_acc={acc:.3f}")
```

## 練習題

1. 把隱藏層節點數從 16 改成 32，比較訓練表現。
2. 新增 validation split 與 early stopping。

## 常見誤用

- 只報訓練集結果，不報驗證集。
- 沒有固定 random seed，結果不可重現。

## 練習本

- 作業版：[`notebooks/exercises/08_dl_exercise.ipynb`](../../notebooks/exercises/08_dl_exercise.ipynb)
- 解答版：[`notebooks/exercises/08_dl_solution.ipynb`](../../notebooks/exercises/08_dl_solution.ipynb)
