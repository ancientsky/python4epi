# 10 機器學習：能否預測誰會感染、誰會變重症？

## 你將學到

- 如何定義流病場景的**二元分類問題**
- 使用 sklearn **Pipeline + ColumnTransformer** 避免資料洩漏
- 建立 **Logistic Regression** baseline 與 **Random Forest** 進階模型
- 用 **交叉驗證 + AUC** 正確評估模型
- 用 **Permutation Importance** 找出最重要的特徵
- 比較 ML 特徵重要性 vs. Ch06 邏輯斯迴歸的 adjusted OR

## 情境故事

長官又來了：
> 「能不能建一個模型，一看到新住民的基本資料就能預測他會不會感染？」
> 「哪些特徵最重要？」

這就是機器學習的任務——不只解釋（Ch06 迴歸），還要**預測**。

---

## Step 1 — 問題定義

我們定義兩個預測任務：

| 任務 | 目標變數 | 定義 | 正例比例 |
|------|---------|------|---------|
| Task A | `infected` | 是否感染 | 121/280 = 43% |
| Task B | `severe_outcome` | 是否住院或死亡 | 68/280 = 24% |

```python
import pandas as pd

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
df["severe_outcome"] = ((df["hospitalized"] == 1) | (df["outcome"] == "dead")).astype(int)
```

## Step 2 — 特徵工程

```python
# 數值特徵
num_cols = ["age"]

# 類別特徵（OneHotEncoder）
cat_cols = ["sex", "smoking_history", "functional_status", "wing"]

# 二元特徵（直接使用）
bin_cols = [
    "floor", "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed", "shower_use", "hydrotherapy_use",
]

X = df[num_cols + cat_cols + bin_cols]
y = df["infected"]
```

> **注意**：不能把症狀（fever, cough 等）當特徵——因為症狀是「感染後」才出現的，會造成 data leakage。

## Step 3 — Pipeline 建立

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

## Step 4 — 交叉驗證 + AUC

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(clf_lr, X, y, cv=5, scoring="roc_auc")
print(f"5-fold CV AUC = {scores.mean():.3f} ± {scores.std():.3f}")
```

## Step 5 — Random Forest 進階模型

```python
from sklearn.ensemble import RandomForestClassifier

clf_rf = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42)),
])
scores_rf = cross_val_score(clf_rf, X, y, cv=5, scoring="roc_auc")
print(f"Random Forest 5-fold CV AUC = {scores_rf.mean():.3f} ± {scores_rf.std():.3f}")
```

## Step 6 — 特徵重要性

```python
from sklearn.inspection import permutation_importance

clf_rf.fit(X, y)
result = permutation_importance(clf_rf, X, y, n_repeats=10, random_state=42)
```

---

## 練習題

- 作業版：[`10_ml_exercise.ipynb`](exercises/10_ml_exercise.ipynb)
- 解答版（講師）：[`10_ml_solution.ipynb`](solutions/10_ml_solution.ipynb)

## 常見誤用

| 錯誤 | 正確做法 |
|------|---------|
| 先標準化再切分 | 用 Pipeline，在 fold 內部標準化 |
| 用 accuracy 評估不平衡資料 | 用 AUC 或 F1 |
| 把症狀放入特徵 | 症狀是結果的一部分，會造成 data leakage |
| 280 筆就用複雜模型 | 簡單模型 + 交叉驗證更可靠 |

## 下一步

ML 告訴我們「能預測」，但 280 筆資料的 ML 模型可靠嗎？
下一章（Ch11），我們嘗試 PyTorch 深度學習——同時討論「何時該用 / 不該用 DL」。
