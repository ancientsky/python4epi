# 07 機器學習

## 你將學到

- 如何定義流病二元分類問題
- 使用 pipeline 避免資料洩漏
- 以 AUC 與 calibration 檢查模型

## 情境故事

你想預測個案是否可能發展成嚴重結局，以便早期介入。

## 最小可執行程式碼

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("data/synthetic/line_list.csv")
df["target"] = (df["outcome"] == "dead").astype(int)
X = df[["age", "sex", "location", "exposed"]]
y = df["target"]

num_cols = ["age", "exposed"]
cat_cols = ["sex", "location"]

preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ]
)

clf = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("model", LogisticRegression(max_iter=500)),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
clf.fit(X_train, y_train)
proba = clf.predict_proba(X_test)[:, 1]
print(f"AUC={roc_auc_score(y_test, proba):.3f}")
```

## 練習題

1. 用 `class_weight="balanced"` 比較 AUC 變化。
2. 加上時間切分（早期資料訓練、晚期資料測試）。

## 常見誤用

- 先對全資料標準化再切分。
- 不處理類別不平衡卻直接比較準確率（accuracy）。

## 練習本

- 作業版：[`notebooks/exercises/07_ml_exercise.ipynb`](../../notebooks/exercises/07_ml_exercise.ipynb)
- 解答版：[`notebooks/exercises/07_ml_solution.ipynb`](../../notebooks/exercises/07_ml_solution.ipynb)
