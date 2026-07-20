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

## 🩺 超白話特別篇：把模型當成「一個正在受訓的實習醫師」

> 特徵工程、交叉驗證、AUC……一堆名詞快看暈了？別怕。這一段用**一個比喻**把整個 Part A 串起來：**把模型想成一位正在受訓、準備考執照的實習醫師。** 看完這張圖，下面每一個 Step 都只是這位實習醫師養成路上的一站。

整個 Part A，其實就是**把一位實習醫師從菜鳥訓練到能獨立看診**的過程。他要先學會「看懂病歷上哪些線索有用」（**特徵工程**），然後上課練功（**train**），考幾次可以看答案、邊考邊改讀書方法的模擬考（**validation**），最後上一次不能重來的正式執照考（**test**）。而 **AUC**，就是他的**成績單**。

```{figure} images/ml_intern_journey.svg
:name: fig-ml-intern-journey
:alt: 一位實習醫師的養成對應整套 ML 工作流：整理病歷線索（特徵工程）→ 上課學公式（train）→ 模擬考可重考（validation）→ 換 5 份題庫輪流模擬考（交叉驗證，本章用這招）→ 執照考只考一次（test）；下方紅色警告偷看考古題＝資料洩漏；成績單＝AUC
:width: 100%

一位實習醫師的養成 = 整套 ML 工作流。本章因為資料只有 280 筆，用「交叉驗證」取代固定的模擬考（validation）。
```

### 五句話看懂整條路

> 🔑 **模型不是天才，是實習醫師**：他知道的每一件事，都是你「餵」給他的病歷線索。線索給錯（把病名當線索），他就作弊；線索太雜，他就學不動。
>
> 📚 **train 是上課，validation 是模擬考，test 是執照考**：上課可以翻書、模擬考可以檢討改進，但**執照考只考一次，掀開就作廢**——不能考完不滿意再重考同一份。
>
> 🔁 **交叉驗證 = 換 5 種題庫各模擬考一次**：只考一次會有「剛好考到會的」的運氣成分；輪流用 5 份不同考卷、取平均，才知道他**真正的實力**（還有他穩不穩）。
>
> 🎯 **AUC 不是「答對幾題」，是「排序病人的眼力」**：隨便抓一個真的會感染的、一個不會感染的，這位實習醫師能不能把「會感染的」排在前面？排對的機率就是 AUC。0.5＝閉眼猜、0.7＝及格、0.8＝不錯。
>
> 🤖 **給實習醫師換一顆更聰明的腦袋（Random Forest），不一定考更高**：如果病歷本身線索就很薄（280 筆、訊號又弱），再聰明的腦袋也變不出資訊——這就是 Part A 誠實的結論。

### 實習醫師 ↔ ML 術語對照

| 實習醫師的世界 | ML 術語 | 一句話 |
|---|---|---|
| 從病歷圈出「有用的線索」、整理成看得懂的格式 | **特徵工程** feature engineering | 模型只吃數字：年齡要縮放、性別要編碼、症狀不能用（作弊） |
| 上課學公式 | **訓練集** train | 模型在這裡「學」係數/規則（`fit`） |
| 可看答案、邊考邊改的模擬考 | **驗證集** validation | 選模型、調參數用；可反覆使用 |
| 只考一次、掀開作廢的執照考 | **測試集** test | 最終評估，代表上線後的真實表現 |
| 換 5 份題庫各模擬考一次、取平均 | **交叉驗證** k-fold CV | 讓每筆資料都輪流當考題，成績更公平、更穩 |
| 成績單：把病人排對順序的眼力 | **AUC** | 隨機一對（病/沒病），排對的機率；0.5 猜、0.8 好 |
| 偷看考古題（正好考過的題目） | **資料洩漏** data leakage | 用症狀/結果當線索、先標準化再切分 → 考很高、上線慘敗 |

> ⚠️ **四個新手雷**：① 模擬考考很好 ≠ 實習醫師很強（可能偷看過考卷 = leakage）；② 拿執照考的題目來調讀書方法 → test 就退化成 validation，你會高估實力；③ 換更聰明的腦袋不一定更準（線索薄時 RF ≈ logistic，還更容易死背）；④ 找到的重要線索 ≠ 致病原因（重要 ≠ 因果，那是 Ch12）。

---

## Part A：在真實資料上把工作流做對（`10_ml_baseline`）

先在**真實的**退伍軍人症資料（280 筆）上，把一套 ML 工作流「規規矩矩」做一遍——重點不是炫技，而是**別犯錯**、並**誠實面對結果**。完整程式見 [`10_ml_baseline.ipynb`](notebooks/10_ml_baseline.ipynb)。

## Step 0 — 資料切分：先把「考卷」分好

在餵資料給實習醫師之前，先把資料切開：一部分拿來**學**、一部分拿來**評分**。Ch07 教過「不能偷看未來」；ML 的版本就是 **train / validation / test 三切分**：

```{figure} images/train_val_test_split.svg
:name: fig-train-val-test
:alt: 資料三切分：train 60% 學公式、validation 20% 調參選模型、test 20% 只掀一次做最終評估；下方紅色警告資料洩漏（先標準化/SMOTE 再切分、把結果當特徵、偷看未來）
:width: 100%

**train**（上課學公式）→ **validation**（模擬考、調參選模型）→ **test**（執照考，只掀一次）。測試集看過就作廢。
```

> 🚨 **資料洩漏（data leakage）是 ML 的頭號殺手**：只要測試集的資訊偷偷混進訓練，模型就會「考很高、上線慘敗」。三大禁忌：① 先標準化 / SMOTE **再**切分（要在 fold 內部做）；② 把「結果的一部分」當特徵（如用症狀預測感染）；③ 用到未來資訊。**時間序列**要用 `TimeSeriesSplit`、**空間資料**要用 spatial CV，不能隨機打亂。

**那到底要切 60/20/20 還是 70/15/15、80/10/10？** 一句話：**資料越多，validation/test 的「比例」可以越小**，因為 10% 的絕對數量已經夠多。

| 資料量 | 建議切法 | 為什麼 |
|---|---|---|
| **小（< 1,000 筆，像本章 280 筆）** | **別切固定 validation → 改用 k-fold 交叉驗證**；test 留 ~20%（或直接全用 CV 報告） | 固定切一份 val 出來樣本太少、成績全看運氣；CV 讓每筆都當過考題，穩得多 |
| **中（1k–100k）** | **60/20/20** 或 **70/15/15** | val/test 各有幾千筆，足以穩定評估 |
| **大（> 100k）** | **80/10/10**，甚至更極端 | 1% 已是上萬筆，足夠評估；把更多資料留給訓練更划算 |

> 📌 **兩個誠實提醒**：① **本章 280 筆就是「小」的典型**——所以下面你看不到一個叫 `X_val` 的東西，validation 的角色被 **Step 4 的交叉驗證**接手了；② **不平衡時要「分層切」**（重症只佔 24%）：切分/CV 要用 stratified（`StratifiedKFold`、`train_test_split(stratify=y)`），否則某一折可能幾乎沒有正例、成績亂跳。

## Step 1 — 問題定義：把長官的問題變成 0/1 標籤

ML 不會optimize「預測誰會生病」這種模糊句子——它需要一欄明確的 **0/1 標籤**。我們定義兩個預測任務：

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

> **逐行拆解**
>
> | 程式碼 | 做了什麼 |
> |---|---|
> | `(df["clinical_severity"] != "not_ill").astype(int)` | 只要臨床嚴重度不是「沒生病」就算感染（1），否則 0 |
> | `((df["hospitalized"]==1) \| (df["outcome"]=="dead")).astype(int)` | 住院**或**死亡就算重症結局（1） |
>
> 💡 **為什麼要先定義標籤？** 因為標籤一旦定了，「哪些欄位算作弊」也就定了。`infected` 是用 `clinical_severity` 定義的，所以 `clinical_severity`、症狀、住院、死亡這些「結果端」欄位**全部不能當線索**——它們是答案的一部分。這就是 Step 2 選特徵的鐵律。（順帶記住：Task B 只有 24% 正例，這個「不平衡」在 Step 4 會決定我們為什麼看 AUC、不看準確率。）

## Step 2 — 特徵工程：把「雜亂病歷」翻譯成模型看得懂的數字

**為什麼要做特徵工程？** 模型只會算數學，不會看懂「男/女」「A 棟」這種字，也不知道「年齡 85」和「floor 3」不是同一個尺度。特徵工程就是**幫實習醫師把病歷整理成模型能吃的數字**。

```{figure} images/feature_engineering.svg
:name: fig-feature-engineering
:alt: 特徵工程流程：原始 line list（age、sex、shower_use、以及被劃掉的 fever 代表洩漏）→ 三種欄位分三條路（數值→StandardScaler 標準化、類別→OneHotEncoder 拆成 0/1 欄、二元→passthrough 直接用）→ 一張全是數字的矩陣 → 丟進模型；下方列出挑特徵三原則
:width: 100%

三種欄位，三種處理法：數值要縮放、類別要編碼、二元直接放行。
```

**三種欄位、三種處理法（為什麼要這樣）：**

| 類型 | 例子 | 怎麼處理 | 為什麼 |
|---|---|---|---|
| **數值 numeric** | `age` | 標準化 `StandardScaler`（減平均、除標準差） | 年齡 20–100、其他欄位是 0/1；不縮放的話 age「數字大」會被誤當成「重要」，logistic 也收斂變慢 |
| **類別 categorical** | `sex`, `wing`, `smoking_history`, `functional_status` | One-hot 編碼（拆成多個 0/1 欄） | 「A棟=1、B棟=2」會被模型當成「B＞A」的順序，但棟別沒有大小之分；one-hot 把它們拆成平等的開關 |
| **二元 binary** | 各 comorbidity、`immunosuppressed`、`shower_use` | 直接放行 `passthrough` | 本來就是 0/1，已是模型能吃的數字，不用動 |

```python
num_cols = ["age"]                                                   # 數值 → 待標準化
cat_cols = ["sex", "smoking_history", "functional_status", "wing"]   # 類別 → 待 one-hot
bin_cols = [                                                         # 二元 → 直接用
    "floor", "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed", "shower_use", "hydrotherapy_use",
]
X = df[num_cols + cat_cols + bin_cols]
y = df["infected"]
```

> 🧭 **怎麼「挑」特徵？別把整張表倒進去——三原則：**
> 1. **領域知識優先**：問「這條線索在住民**入住/暴露當下**就知道嗎？」退伍軍人症的已知風險是年齡、慢性病、免疫低下、用水（淋浴/水療）暴露——選這些。
> 2. **鐵律：不准用「結果之後」才出現的欄位**（防作弊）。症狀（fever、cough）、`clinical_severity`、住院、死亡、`icu_admission`、`lab_confirmed`、各種日期——都是**感染之後**才知道的，拿來預測感染就是**偷看答案**。用了症狀，AUC 會漂亮到 0.99，然後上線時你根本還沒有症狀資料。
> 3. **不要什麼都塞**：280 筆撐不起幾十個特徵，特徵越多越容易「死背」（overfit）。寧可少而準。
>
> （小註：這裡把 `floor` 放在 `bin_cols` 當 0/1 用；若樓層有多層、且層與層無大小關係，更嚴謹的做法是當成類別欄位 one-hot。）

## Step 3 — Pipeline：把「前處理 + 模型」綁成一條，順便防洩漏

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

> 🔒 **為什麼一定要包成 Pipeline，不自己先 `scaler.fit(X)`？** 因為標準化要用「平均值和標準差」——如果你在**切分前**用全部資料算這兩個數字，測試集的資訊就偷偷滲進了訓練，這是最隱蔽的 data leakage。Pipeline 保證：在交叉驗證的**每一折**裡，縮放的平均值**只從那一折的訓練資料學**，測試折完全不參與。等於「模擬考的答案，改考卷前都不准偷看」。
>
> **逐行拆解**
>
> | 程式碼 | 做了什麼 |
> |---|---|
> | `ColumnTransformer([...])` | 對不同欄位群套不同前處理：數值縮放、類別 one-hot、二元放行 |
> | `OneHotEncoder(handle_unknown="ignore", drop="first")` | `drop="first"` 避免共線性；`handle_unknown="ignore"` 讓測試折出現沒看過的類別時不報錯 |
> | `Pipeline([("preprocess",...), ("model",...)])` | 把前處理 + 模型串成一個物件，`fit`/`predict` 一起走，CV 時整條在每折內重跑 |

## Step 4 — 交叉驗證 + AUC：到底在比什麼？

這是新手最容易迷路的一步。先搞懂**交叉驗證在做什麼**，再搞懂 **AUC 是什麼**。

```{figure} images/cross_validation_kfold.svg
:name: fig-cross-validation
:alt: 5-fold 交叉驗證示意：資料切 5 折，每一列用 1 折當測試（綠）、其餘 4 折訓練（藍），測試折沿對角線輪替，得到 5 個 AUC，最後取平均與標準差
:width: 100%

k-fold 交叉驗證：每一筆資料都輪流當一次「考題」，得到 5 個 AUC → 取平均與標準差。
```

> 🔁 **交叉驗證在比什麼？** `cross_val_score` 本身**不比較兩個模型**，它是在給**同一個模型**打一個更可信的分數。做法是切 5 折、每次拿 4 折訓練留 1 折當考題、輪 5 次——**每筆資料都剛好當過一次考題**。於是得到 5 個 AUC，看兩個數字：**平均**（`.mean()`）＝大概多強；**標準差**（`.std()`）＝穩不穩（標準差大＝換題庫就崩、不可靠）。真正的「比較」發生在你眼睛裡：Step 4 給 logistic 一個分數、Step 5 給 RF 一個分數，你把兩張成績單並排——這才是選模型。

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(clf_lr, X, y, cv=5, scoring="roc_auc")
print(f"5-fold CV AUC = {scores.mean():.3f} ± {scores.std():.3f}")
```

那 **AUC 到底是什麼**？忘掉「曲線下面積」這種嚇人的講法：

```{figure} images/roc_auc_intuition.svg
:name: fig-roc-auc
:alt: AUC 直覺：左邊是模型把病人依風險分數排出的排行榜，真感染者（橘）大多排在上面；右邊是 AUC 量尺 0.5 閉眼猜、0.7 及格、0.8 不錯、1.0 全對；下方提醒不平衡資料別看準確率
:width: 100%

AUC = 隨機抓一個感染者＋一個健康人，模型把感染者排前面的機率。
```

> 🎯 **最白話的 AUC 定義**：**隨機抓一個真的會感染的人、一個真的不會感染的人，模型給前者的分數比後者高的機率。** 排對＝加分。**0.5**＝閉眼猜（銅板）、**0.7**＝及格、**0.8**＝不錯、**1.0**＝每一對都排對（現實中這麼高，先懷疑是不是 leakage）。
>
> ⚠️ **為什麼不用「準確率 accuracy」？** Task B 只有 24% 重症。如果模型**全部猜「沒重症」**，準確率就有 76%——聽起來高，其實一個病人都沒抓到、完全沒用。AUC 看的是**排序**、不是「猜對幾個」，也不受你設哪個門檻影響。所以在**不平衡**資料（重症、死亡這種少數事件）上，看 AUC（Part B 再加看 PR-AUC）比看準確率誠實得多。

## Step 5 — Random Forest：換一顆更聰明的腦袋

```python
from sklearn.ensemble import RandomForestClassifier

clf_rf = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42)),
])
scores_rf = cross_val_score(clf_rf, X, y, cv=5, scoring="roc_auc")
print(f"Random Forest 5-fold CV AUC = {scores_rf.mean():.3f} ± {scores_rf.std():.3f}")
```

> 🌲 **注意：pipeline 其他部分完全沒動**——只換了 `model` 那一格。這正是 Step 3 包 Pipeline 的好處：換模型只換一個字。logistic 只能畫直線邊界，Random Forest 是一群決策樹投票，能抓非線性和交互作用。
>
> **但結果很誠實**：在這 280 筆弱訊號資料上，RF 的 AUC 幾乎追平 logistic（跑跑看：兩者都在 0.6 上下）。原因不是 RF 笨，是**病歷線索本來就薄**——實習醫師換再聰明的腦袋，也變不出資料裡沒有的資訊。ML 真正發威，要等 **Part B** 那種「大資料 + 非線性 + 交互作用」的場子。

## Step 6 — 特徵重要性：哪條線索最有用？

```python
from sklearn.inspection import permutation_importance

clf_rf.fit(X, y)
result = permutation_importance(clf_rf, X, y, n_repeats=10, random_state=42)
```

> 🔍 **置換重要性（permutation importance）的邏輯超直覺**：把某一欄的資料**打亂洗牌**，再看模型 AUC **掉多少**。掉越多＝這欄越重要（模型很依賴它）；幾乎沒掉＝可有可無。就像抽掉實習醫師病歷上的某一條線索，看他判斷準度掉多少。
>
> 🧭 **關鍵提醒**：**重要 ≠ 有因果**。這欄能幫忙**預測**，不代表改變它就能**防病**（那是 Ch12 因果推論）。值得跟 Ch06 的 adjusted OR 對照——若 ML 和迴歸指向同一批危險因子，結論更可信。

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
