# 10 機器學習：能否預測誰會感染、誰會變重症？

## 你將學到

**Part A —（`10_ml_baseline`）在真實資料上把工作流做對**

- 如何定義流病場景的**二元分類問題**
- **train / validation / test 三切分**與**資料洩漏（data leakage）**的防治
- 使用 sklearn **Pipeline + ColumnTransformer**、**交叉驗證 + AUC**
- 誠實面對：280 筆弱訊號資料上，**RF 幾乎贏不了 logistic**——真實預測是謙卑的

**Part B —（`10_ml_advanced`）在更大的沙盒看 ML 的威力**

- **模型動物園**：決策樹、隨機森林、XGBoost、LASSO（各配一個臨床比喻）
- **Ensemble**：bagging / boosting / **stacking（Super Learner）**
- **評估套餐**：ROC-AUC、PR-AUC、敏感度/特異度/PPV/NPV、**校準（calibration）**
- **SHAP**：把黑盒模型解釋給醫師聽
- **類別不平衡、過擬合、以及「ML 是工具、不是取代流病判斷」**

## 情境故事

長官又來了：
> 「能不能建一個模型，一看到新住民的基本資料就能預測他會不會感染？」
> 「哪些特徵最重要？」

這就是機器學習的任務——不只解釋（Ch06 迴歸），還要**預測**。

---

## Part A：在真實資料上把工作流做對（`10_ml_baseline`）

先在**真實的**退伍軍人症資料（280 筆）上，把一套 ML 工作流「規規矩矩」做一遍——重點不是炫技，而是**別犯錯**、並**誠實面對結果**。

### 地基：train / validation / test 三切分

Ch07 教過「不能偷看未來」；ML 的版本是把資料切成三份，各司其職：

```{figure} images/train_val_test_split.svg
:name: fig-train-val-test
:alt: 資料三切分：train 60% 學公式、validation 20% 調參選模型、test 20% 只掀一次做最終評估；下方紅色警告資料洩漏（先標準化/SMOTE 再切分、把結果當特徵、偷看未來）
:width: 100%

**train**（學公式）→ **validation**（調參、選模型）→ **test**（只掀一次的期末考）。測試集看過就作廢。
```

> 🚨 **資料洩漏（data leakage）是 ML 的頭號殺手**：只要測試集的資訊偷偷混進訓練，模型就會「考很高、上線慘敗」。三大禁忌：① 先標準化 / SMOTE **再**切分（要在 fold 內部做）；② 把「結果的一部分」當特徵（如用症狀預測感染）；③ 用到未來資訊。**時間序列**要用 `TimeSeriesSplit`、**空間資料**要用 spatial CV，不能隨機打亂。

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

## Part B：進階 ML——模型動物園、Ensemble、評估與 SHAP（`10_ml_advanced`）

Part A 誠實地讓你看到：**在 280 筆弱訊號資料上，RF 幾乎贏不了 logistic。** 那 ML 什麼時候才「贏得漂亮」？答案是：**當風險是非線性、有交互作用、而且資料量夠大的時候。** Part B 換上一個更大的合成沙盒（想像 CDC AI 辦公室把很多機構的通報彙整起來，n≈2500，刻意埋了「年齡 U 型」和「免疫低下 × 暴露」的交互作用），帶你走完完整工作流。完整程式見 [`10_ml_advanced.ipynb`](notebooks/10_ml_advanced.ipynb)。

### 模型動物園（每個配一個臨床比喻）

| 模型 | 臨床比喻 | 一句話 |
|---|---|---|
| 🩺 **決策樹** Decision Tree | 急診**檢傷分流圖** | 一路問是非題走到底；超好懂，但問法太死、易過擬合 |
| 👥 **隨機森林** Random Forest | **多科會診投票**（bagging） | 一群醫師各看部分資料、各投一票、多數決 → 穩 |
| 📈 **XGBoost** | **錯題本補習班**（boosting） | 每一棒專攻上一棒的錯題殘差 → 準，但易補過頭 |
| 🧳 **LASSO**（L1 邏輯斯迴歸） | **行李限重打包** | L1 懲罰逼不重要的係數歸零，只留幾個關鍵因子 → 精簡可解釋，流病最愛的 baseline |

在沙盒資料上，**LASSO（線性）AUC 只有 ~0.71，樹系模型 ~0.85**——這就是「非線性 + 交互作用」時 ML 贏的地方。

### Ensemble：三種「集思廣益」

```{figure} images/bagging_vs_boosting.svg
:name: fig-bagging-boosting
:alt: Bagging（平行投票，多棵樹各看部分資料獨立投票、多數決＝隨機森林）vs Boosting（接力補課，每一棒專攻上一棒的殘差＝XGBoost）
:width: 100%

**Bagging** 平行投票、降變異（更穩）；**Boosting** 接力補殘差、降偏差（更準）。
```

> 🎯 **Stacking = 指揮中心總指揮（Super Learner）**：樹、森林、XGBoost、LASSO 各給一個機率，**總指揮（meta 模型）不自己看病人**，而是學「什麼情況該多聽哪位專家」，加權整合。這就是流病文獻的 **Super Learner**（van der Laan），能減少單一模型的偏差。

### 評估套餐：不要只看一個數字

一句話抓重點：**篩檢期**重「不能漏接」（sensitivity、NPV、PR-AUC）；**確認 / 資源分配期**重「別誤報、機率要準」（specificity、PPV、calibration）。

| 指標 | 何時看 | 流病白話 |
|---|---|---|
| **ROC-AUC** | 選模型、跨門檻 | 病人排在健康人前面的機率；不平衡時偏樂觀 |
| **PR-AUC** | **正例稀少**（重症/死亡） | 專注「抓到的陽性有多真」，比 AUC 誠實 |
| **Sensitivity** | 篩檢、漏接代價高 | 真病人裡抓到幾成 |
| **Specificity** | 誤報代價高 | 真沒病的裡正確放行幾成 |
| **PPV**（受盛行率影響大） | 臨床當下決策 | 「模型說陽性，他真有病的機率」——醫師最在意 |
| **NPV** | 排除用 | 「說沒事，真能放心嗎」 |
| **Calibration / Brier** | 要把機率當數字用（分床、風險溝通） | 說 70% 的那群，真的約 70% 發病嗎？**會排序 ≠ 機率準** |

### SHAP：把黑盒解釋給醫師聽

> 💰 **年終公平分紅**：SHAP 用賽局理論的 Shapley value，問「少了這個特徵，預測差多少？」，把每個特徵**加入 vs 不加入**的邊際貢獻對所有順序平均。所以它能對**單一病人**說：「他被判高風險，是因為免疫低下 +0.3、暴露 +0.2、年齡 80 +0.15」——正好是解釋黑盒給醫師聽的語言。在沙盒裡，SHAP 成功還原了我們刻意埋的「年齡 U 型風險」，那是線性 age 永遠畫不出來的。

## 練習題

- 作業版：[`10_ml_exercise.ipynb`](exercises/10_ml_exercise.ipynb)
- 解答版（講師）：[`10_ml_solution.ipynb`](solutions/10_ml_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/10_ml_solution.ipynb>)

## 常見誤用

| 錯誤 | 正確做法 |
|------|---------|
| 先標準化 / SMOTE 再切分 | 用 Pipeline，在 fold **內部**做（否則資料洩漏） |
| 用 accuracy 評估不平衡資料 | 重症只佔 8% 時，「全猜沒病」就有 92% 準確率卻沒用 → 看 PR-AUC / 敏感度 |
| 把症狀放入特徵 | 症狀是結果的一部分，會造成 data leakage |
| 280 筆就用複雜模型 | 簡單模型 + 交叉驗證更可靠；訓練 AUC 1.0、測試 0.7 = 過擬合 |
| AUC 高就拿機率去分床 | 會排序 ≠ 機率準——要看 **calibration** |
| 把 SHAP 重要性當「介入標的」 | 重要 ≠ 有因果；改變該特徵未必能防病（因果是 Ch12） |
| 訓練完就上線 | 一定要**外部驗證**：換一家機構、換一個時期，模型可能崩掉（dataset shift） |
| 只看整體表現 | 檢查**公平性**：不同性別 / 年齡層的 subgroup 表現一致嗎？ |

## 下一步

ML 告訴我們「能預測」，但 280 筆資料的 ML 模型可靠嗎？
下一章（Ch11），我們嘗試 PyTorch 深度學習——同時討論「何時該用 / 不該用 DL」。
