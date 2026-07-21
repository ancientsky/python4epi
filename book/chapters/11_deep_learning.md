# 11 深度學習（PyTorch）：什麼時候該用，什麼時候別殺雞用牛刀

## 你將學到

- 用 PyTorch 撰寫**訓練迴圈**（forward → loss → backward → step）與**早停法**（early stopping），避免小樣本過擬合
- 把**序列預測**（sequence forecasting）用 LSTM / CNN 做出來，看懂為什麼「領先指標」能讓深度學習打敗 naive 基準
- 一套**決策框架**：什麼時候該上深度學習，什麼時候傳統統計或簡單 ML 就夠了（別殺雞用牛刀）
- 現代深度學習全景導覽：GNN（圖神經網路）、時空 Transformer / TFT、DeepSurv、時序基礎模型（TSFM）、PINN（物理知情神經網路）
- 怎麼**評估**預測 / 分類模型、怎麼用 SHAP、attention 權重打開黑盒子

## 情境故事

Ch10 的長官問題還在耳邊：「能不能建一個模型，一看到新住民的基本資料就預測他會不會感染？」你在 Ch10 用 sklearn 老老實實跑過一輪——Logistic Regression 和 Random Forest 在 280 筆資料上打成平手，AUC 都在 0.6 上下，誠實但不算亮眼。

這次換一位同事湊過來：
> 「聽說深度學習很強，要不要試試看？說不定能抓到我們沒想到的複雜交互作用。」

這是個好問題，但答案不是「上就對了」。這一章分兩部分老實回答它：

**Part A（動手做）** 先在同一份 280 筆資料上真的跑一次 PyTorch 神經網路，看它能不能贏過 Ch10 的 sklearn baseline——然後換一個深度學習真正擅長的任務（**序列預測**），看它怎麼贏、為什麼贏。**Part B（全景導覽）** 帶你快速認識深度學習的現代版圖——圖神經網路、Transformer、時序基礎模型、物理知情神經網路——這些工具不會在本書裡執行，但知道它們何時該登場，跟知道怎麼寫 `nn.Sequential` 一樣重要。

---

## 🧠 超白話特別篇：訓練一位新手偵探

> 覺得 neuron、backprop、epoch 這堆黑話看得頭很暈？別怕。這一段用**一個比喻**把整個深度學習的訓練過程串起來：**把訓練一個神經網路，想成訓練一位新手偵探破案。**

一位新手偵探（模型）一開始什麼都不會，只能**憑直覺亂猜**。你給他一疊已經知道答案的舊案子（訓練資料），讓他一次次練習：猜一次、對答案、檢討哪裡想錯、調整判斷方式——練到他培養出「經驗」，看到新案子也能猜對七八成。這整套養成流程，就是深度學習的訓練迴圈。

```{figure} images/dl_intern_detective.svg
:name: fig-dl-intern-detective
:alt: 新手偵探訓練五步驟：憑直覺猜對應 neuron、帶答案反覆練習對應 training loop、檢討哪裡想錯對應 backprop、見好就收對應 early stopping、出師上線對應 deploy；下方標註 weights=經驗、loss=錯多少、epoch=練一輪
:width: 100%

一位新手偵探的養成 = 一套深度學習訓練法：憑直覺 → 反覆練習 → 檢討 → 見好就收 → 出師。
```

### 五句話看懂整套訓練法

> 💡 **neuron（神經元）＝憑直覺猜**：偵探看到一堆線索（input），心裡對每條線索的「可信度」（weight）加權評估，湊出一個判斷。
>
> 📖 **training loop（訓練迴圈）＝帶答案反覆練習**：拿一疊已知結局的舊案子，一次次讓偵探猜、再告訴他正確答案——猜（forward）→ 對答案算差多少（loss）→ 檢討（backward）→ 調整判斷方式（update），一輪一輪重複。
>
> 🔍 **backprop（反向傳播）＝檢討哪裡想錯**：案子破錯了，不能只說「這次沒猜對」，得往回追查：是哪一步的判斷（哪個 weight）該負責，才知道該往哪個方向調整。
>
> 🛑 **early stopping（早停法）＝見好就收**：練習不是練越久越好——練過頭，偵探開始「死背」這批舊案子的細節（overfitting），遇到真正的新案子反而表現變差。**epoch（訓練週期）** 是「練完一整輪舊案子」；見好就收，就是連續好幾輪都沒進步就喊停，把獎盃頒給表現最好的那一次練習，而不是頒給練到走火入魔的最後一次。
>
> 🎓 **deploy（部署上線）＝出師辦真案**：練習結束，帶著累積下來的經驗（weights）去接真正的新案子。

### 偵探的世界 ↔ DL 術語對照

| 偵探的世界 | DL 術語 | 一句話 |
|---|---|---|
| 憑直覺對案情做出判斷 | **Neuron**（神經元） | 每條線索（input）乘上「有多可信」（weight），加總後決定要不要採信（activation） |
| 累積辦案經驗 | **Weights**（權重） | 訓練前是隨機瞎猜，訓練後變成「這類案子通常是這樣」的經驗值 |
| 帶著標準答案反覆練習 | **Training loop**（訓練迴圈） | forward 猜一次、loss 算錯多少、backward 檢討、update 調整經驗 |
| 這次錯了多少 | **Loss**（損失） | 猜測跟正確答案的差距，數字越小代表猜得越準 |
| 往回追查「哪一步判斷該負責」 | **Backprop**（反向傳播） | 從錯誤結果往回推，算出每個 weight 該調整多少 |
| 練完一整輪案例 | **Epoch**（訓練週期） | 把所有訓練案例都看過一遍，叫一個 epoch |
| 死背考古題，換新案子就不會了 | **Overfitting**（過擬合） | 練習案例記得滾瓜爛熟，換一批新案子表現卻大幅變差 |
| 見好就收，不練到走火入魔 | **Early stopping**（早停法） | 驗證表現不再進步就喊停，回頭用最佳那次的經驗 |

不同案子要找不同專長的偵探——這套邏輯在 Part B 會展開成完整的「模型動物園」：MLP 是什麼案子都能接的通才、LSTM 是記性好、能讀懂整段案情脈絡的老偵探、CNN 是專找局部指紋的鑑識官、GNN 是熟悉社群網絡的分析師……每一種都有各自最適合的案子類型。

> ⚠️ **誠實話：深度學習是牛刀，不是萬靈丹**。再厲害的偵探，案子線索太少（像本書的 280 筆資料）也破不了案——這時候找一位資深老偵探（邏輯斯迴歸）反而更快、更準、更容易對法官（臨床醫師）解釋辦案邏輯。下一節的決策框架，就是教你怎麼判斷「這次要不要磨這把刀」。

---

## 核心概念

在動手寫 PyTorch 之前，先把上一節的比喻翻譯成正式的技術名詞。

### Neuron、layer、activation：神經網路到底在算什麼

```{figure} images/neuron_layer_anatomy.svg
:name: fig-neuron-layer-anatomy
:alt: 神經元解剖：inputs 乘上 weights 加總再加 bias，經過 activation（ReLU）得到 output；把同一個 neuron 排成一排、疊成好幾層，就是「深度」學習的「深」
:width: 100%

一個 neuron 只做一件事：加權加總 → 加 bias → 過 activation。排成一排、疊成好幾層，就是一整個網路。
```

一個 **neuron（神經元）** 的計算，濃縮成一行數學式：

$$z = \sum_i x_i w_i + b, \qquad \hat{y} = \text{ReLU}(z) = \max(0, z)$$

- 每個輸入 $x_i$ 先乘上自己的 **weight（權重）** $w_i$——這是「這條線索有多可信」
- 全部加總，再加上一個 **bias（偏差）** $b$——調整「基準線」在哪裡
- 丟進 **activation（激勵函數）**，這裡用最常見的 **ReLU**：負的通通歸零，正的原樣輸出
- 沒有 activation 會怎樣？多層 `Linear` 疊再多層，數學上還是等價於一層線性迴歸——activation 才是讓神經網路真正「非線性」、能抓複雜交互作用的關鍵

把同一個 neuron 排成一排（**layer，層**），輸入層 → 隱藏層 → 輸出層一層接一層往下疊——這就是「深度」學習的「深」：層數疊得越多，理論上能表達的函數越複雜（但也越容易過擬合，見下段）。

### 訓練迴圈：loss、gradient descent、backprop、epoch

```{figure} images/training_loop.svg
:name: fig-training-loop
:alt: 訓練迴圈四步驟：forward 算出目前的猜測、loss 算跟正確答案差多少、backprop 反向傳播追查誰該負責、update 微調 weights；一圈為一個 epoch；旁邊圖示 val loss 回升代表過擬合警訊，用 early stopping 在早停點喊卡
:width: 100%

訓練迴圈繞一圈＝一個 epoch。右邊看什麼時候該喊卡——val loss 不再進步（甚至回升）就是過擬合警訊。
```

每個 PyTorch 模型的訓練，永遠是同一個四拍節奏：

1. **forward（前向傳播）**：資料流過網路，得到目前的猜測
2. **loss（損失函數）**：拿猜測跟正確答案比，算出「錯多少」的一個數字——分類常用 `BCEWithLogitsLoss`，迴歸常用 `MSELoss`
3. **backprop（反向傳播）**：從 loss 往回推，用鏈式法則算出每個 weight 對這次錯誤該負多少責任（梯度）
4. **update（gradient descent，梯度下降）**：優化器（如 Adam）依梯度方向，把每個 weight 微調一點點，讓下次的 loss 更小

把所有訓練資料都跑過一輪這四拍，叫一個 **epoch（訓練週期）**。訓練通常要跑很多個 epoch，一輪一輪把 loss 壓低。

### 過擬合與早停法：什麼時候該喊卡

如果一直練下去會怎樣？**過擬合（overfitting）**：模型把訓練資料的每個細節（連同噪音）都死記下來，train loss 一路探底，但 val loss 先降後升、出現「V 型反彈」——那個反彈點，就是模型開始死背訓練資料、卻學不會舉一反三的訊號。

**早停法（early stopping）** 就是解方：一邊訓練一邊監控驗證集的 loss，只要連續 `patience` 輪都沒有刷新紀錄，就提早喊停，回頭用表現最好的那組權重——而不是用訓練結束當下（很可能已經 overfit）的權重。這正是「新手偵探」比喻裡「見好就收」的技術版本。

---

## 🧭 決策框架：該用 DL 嗎？（別殺雞用牛刀）

```{figure} images/dl_decision_tree.svg
:name: fig-dl-decision-tree
:alt: 該用深度學習嗎決策樹：資料小於1000筆就用傳統統計或簡單ML；需要明確因果或機制就用SEIR加簡單ML；高維非線性時空長序列且資料量大才用DL；新病原初期資料極少但外部有大量其他疫情資料就用TSFM零樣本或少樣本；以上皆非就用Ch10的sklearn baseline最省力
:width: 100%

由上而下依序檢查，符合哪一格就停在那一格——大多數流病資料集，答案停在第一格。
```

四個問題，依序往下問：

1. **資料 < 1,000 筆？**（例如本書的 280 筆 Legionella 資料）→ 用傳統統計 / 簡單 ML，小樣本上更穩、更好解釋
2. **需要明確因果或機制，不只是「會不會」而是「為什麼」？** → 機制模型（如 Ch07 的 SEIR）+ 少量特徵，DL 在這裡是黑盒子，幫不上忙
3. **高維非線性、時空、長序列，而且資料量真的夠大？** → 才輪到 DL（CNN / LSTM / Transformer 等）
4. **新病原、初期資料極少，但外面已經有大量其他疫情的資料？** → 借用預訓練的 TSFM 做零樣本 / 少樣本預測，不用等自己的資料累積夠

大多數流病資料集（包括本書的 Legionella 資料）在**第一格**就停下來了。

### 適合用 DL vs. 殺雞用牛刀（別用）

| ✅ 適合用 DL | ❌ 殺雞用牛刀（別用） |
|---|---|
| 資料量大（數千筆以上） | 小樣本（< 1,000 筆） |
| 高維、非線性、有複雜交互作用 | 低維表格資料，線性 / 樹模型已經夠表達 |
| 影像、長序列、時空資料 | 橫斷面資料，一列一列互相獨立 |
| 有相關的預訓練模型可遷移（TSFM 零樣本） | 沒有相關預訓練資源、資料又稀少 |
| 已經跑過傳統 / ML baseline，還是不夠好 | 還沒跑過 baseline 就想上 DL |

### 280 筆的 Legionella 資料，合理嗎？

把決策框架套到本書的資料上，答案很清楚：

| 考量 | 結論 |
|------|------|
| 樣本量 | 280 筆遠低於 DL 通常需要的數千筆 |
| 特徵維度 | 約 15 維，邏輯斯迴歸已經足夠表達 |
| 過擬合風險 | DL 參數量 ≫ 樣本數 → 過擬合風險極高 |
| 教學價值 | 值得學 PyTorch 語法和訓練迴圈——未來遇到影像、大樣本資料就能派上用場 |
| 實務建議 | 用 Ch10 的 sklearn baseline，DL 留作學習工具（下面 Part A Step 1 會親自驗證這個結論） |

> 🧭 **鐵律**：先跑傳統統計 / ML baseline，不夠好、且符合上面決策樹裡的條件，才考慮上 DL。深度學習是一把牛刀——本章 Part A 會讓你親眼看到：牛刀殺雞（280 筆分類）殺不出優勢，但殺牛（序列預測）就真的比較利。

---

## 資料切分：時間序列的 train / val / test

Ch10 教過橫斷面資料的 train / val / test 三切分——可以放心 `shuffle=True`，因為每一列資料互相獨立。**時間序列完全不行**：資料有方向性，未來不能穿越回去污染過去。

```{figure} images/timeseries_split.svg
:name: fig-timeseries-split
:alt: 時間序列切分示意：隨機打亂K-fold會讓未來的test片段混進過去的訓練資料，模型偷看到答案；正確做法是滾動或擴張窗口，train到val到test沿著時間排好，箭頭永遠指向未來
:width: 100%

❌ 隨機打亂：未來的 test 片段混進訓練資料，模型偷看到答案。✅ 按時間切：train → val → test 沿時間排好，箭頭永遠指向未來。
```

> ⚠️ **為什麼絕對不能對時間序列隨機打亂？** 如果用一般 ML 常見的隨機 K-fold，某一折的訓練集可能包含「未來」的資料點，模型等於考試前先偷看了答案——離線的驗證分數會嚴重高估，上線後才發現根本不準。這是時間序列版本的資料洩漏（**未來洩漏 future leakage**）。

正確做法是**依時間順序切**，常見兩種窗口：

- **滾動窗口（rolling window）**：固定訓練窗口的長度，隨時間往前滑動（例如永遠用「過去 300 天」訓練）
- **擴張窗口（expanding window）**：訓練集只增不減，每次往後多納入一段新的時間（例如「從第 1 天到現在」都拿來訓練）

**切分比例**：一個常見起點是 **train 70% / val 15% / test 15%**，且三段**必須按時間先後排列**——train 永遠是最早的一段，test 永遠是最晚的一段，val 夾在中間，絕不能讓 val / test 的時間點早於 train。下面 Part A Step 2 的序列預測範例，就是照這個精神切分：最前面一大段當訓練＋驗證區間，最後一段完全沒被模型看過的日子當測試集。

---

## Part A — 動手做（可執行、免 GPU）

Part A 分兩步，完整程式碼都在對應的 notebook 裡跑得動、不需要 GPU：

- **Step 1**：在 280 筆 Legionella 資料上跑一次 PyTorch 分類模型，誠實檢驗「深度學習在小樣本上贏得了 sklearn 嗎」——完整程式見 [`11_dl_baseline.ipynb`](notebooks/11_dl_baseline.ipynb)
- **Step 2**：換一個深度學習真正擅長的任務——用 LSTM / CNN 做**序列預測**，看深度學習怎麼贏、為什麼贏——完整程式見 [`11_dl_sequence.ipynb`](notebooks/11_dl_sequence.ipynb)

下面只挑每個 notebook 裡最關鍵的幾段程式碼講解；完整流程（含學習曲線、permutation importance 等）請打開 notebook 逐格執行。

### Step 1 — MLP baseline（280 筆分類）

**① 資料前處理：把病歷表格轉成 PyTorch 看得懂的張量**

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `pd.get_dummies(..., drop_first=True)` | 類別欄位（`sex`、`wing`…）one-hot 編碼成 0/1 虛擬變數 |
> | `X_np = X_df.values.astype(np.float32)` | 轉成 NumPy 陣列並轉型為 `float32`——PyTorch 權重預設是單精度浮點，型別要對齊 |
> | `scaler.fit_transform(X_np[:, 0:1])` | 只標準化 `age`；神經網路對輸入尺度敏感，不縮放會拖慢甚至搞砸收斂 |
> | `np.random.shuffle(idx)` → 70/30 切 | 手動打亂索引、切出訓練 / 驗證集（跟 Ch10 的橫斷面資料一樣，可以放心 shuffle） |
> | `y_train = torch.tensor(...).unsqueeze(1)` | 把 y 從一維 `(N,)` 轉成二維 `(N, 1)`，對齊模型輸出的形狀 |

> 💡 **翻譯病歷成張量**：PyTorch 不吃 DataFrame，只吃 **tensor**。這幾行看起來瑣碎，但每一步都對應 sklearn `Pipeline` 幫你自動做掉的事——刻意拆開來手動做一遍，才看得清楚每個環節在幹嘛。

**② 模型架構：三層線性層疊出一個最小的神經網路**

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
print(f"總參數量：{n_params}，參數 / 樣本比：{n_params / len(X_train):.1f}")
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `nn.Sequential(Linear → ReLU → Linear → ReLU → Linear)` | 把層堆疊成一條管線：`Linear` 做線性組合，`ReLU` 加入非線性，最後 `Linear(16, 1)` 輸出單一 logit |
> | 最後一層不接 activation | 交給下一段的 `BCEWithLogitsLoss` 內部處理 sigmoid，數值更穩定 |
> | `n_params = sum(p.numel() ...)` | 加總所有權重 + 偏差的元素數，量化這個模型「有多少東西可以調」 |

> ⚠️ **參數 / 樣本比 > 1**：這個架構大約 700 個參數，訓練集只有約 196 筆——參數比樣本還多，過擬合風險極高。這行印出來的數字，就是「殺雞用牛刀」的具體證據。

**③ 訓練迴圈 + 早停法**

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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `optimizer.zero_grad()` | 清空上一輪殘留的梯度（PyTorch 預設梯度會累加，不清空會越加越大） |
> | `loss = loss_fn(model(X_train), y_train)` | forward + 算 loss：資料流過網路得到 logits，再跟真實標籤比對 |
> | `loss.backward()` | backprop：自動微分算出每個參數對 loss 的梯度 |
> | `optimizer.step()` | 依剛算好的梯度更新每個參數（Adam optimizer 的規則） |
> | `if val_loss < best_val_loss: ... else: counter += 1` | 早停的核心：val_loss 進步就存檔、`counter` 歸零；沒進步就累加 |
> | `model.load_state_dict(best_state)` | 訓練結束後「倒帶」回 val_loss 最低的那次權重快照 |

> 🧭 **見好就收**：連續 `patience` 輪都沒有刷新紀錄，就把獎盃頒給表現最好的那一輪，而不是頒給訓練結束當下（很可能已經開始過擬合）的自己。

**誠實的結果**：跑完 [`11_dl_baseline.ipynb`](notebooks/11_dl_baseline.ipynb) 全部流程（含學習曲線、AUC 評估、與 sklearn 比較），驗證集 **AUC ≈ 0.63**——跟 Ch10 的 Logistic Regression、Random Forest（都在 0.6 上下）幾乎打平，並沒有展現明顯優勢。

| 模型 | Val AUC（相同 train/val 切分） |
|---|---|
| Logistic Regression | ≈ 0.6 上下 |
| Random Forest | ≈ 0.6 上下 |
| PyTorch DL（MLP） | ≈ 0.63 |

原因跟第 5 節的決策框架完全吻合：280 筆遠不夠支撐一個 700 參數的神經網路去學到 sklearn 學不到的東西——**小資料上，DL 不佔優勢**。這一步的教學價值不是「打敗 sklearn」，而是扎扎實實學會 PyTorch 的訓練迴圈語法，為 Step 2 真正適合 DL 的任務做準備。

### Step 2 — 序列預測：LSTM / CNN

280 筆橫斷面資料讓 DL 打了平手，那換一個**序列預測（sequence forecasting）**任務呢？[`11_dl_sequence.ipynb`](notebooks/11_dl_sequence.ipynb) 不用松柏護理之家的資料（那組資料沒有足夠長的每日序列），改用一組**教學合成的「登革熱 × 氣溫」每日序列**：氣溫是每天有噪音、有季節性的**領先指標**（可提前取得），病例數則受「7 天前氣溫」與「前一天病例數」共同驅動。任務是：用過去 21 天的 (病例數, 氣溫)，預測 **7 天後**的病例數。

**① 合成資料：藏一個「作弊碼」——領先指標**

```python
torch.manual_seed(1)
np.random.seed(1)

n = 360
t = np.arange(n)

# 氣溫：季節性正弦波 + 隨機噪音（已知、可提前取得的領先指標）
temp = 24 + 7 * np.sin(2 * np.pi * (t - 30) / 365) + np.random.normal(0, 1.0, n)
drive = np.clip(temp - 24, 0, None)  # 氣溫超過 24 度才有驅動力（越熱、病媒蚊越活躍）

cases = np.zeros(n)
for i in range(n):
    lag = cases[i - 1] if i >= 1 else 0
    cases[i] = max(
        0,
        0.55 * lag                                   # 前一天病例數的延續性
        + 3.2 * (drive[i - 7] if i >= 7 else 0)       # 7 天前氣溫的延遲效應（領先指標）
        + 4 * np.sin(2 * np.pi * t[i] / 7)            # 每週通報節律
        + 6                                            # 基準病例數
        + np.random.normal(0, 2.0),                   # 隨機噪音
    )
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `temp = 24 + 7*sin(...) + noise` | 氣溫：季節性波動 + 噪音，是「已知、可提前取得」的**領先指標** |
> | `drive = np.clip(temp - 24, 0, None)` | 氣溫超過 24 度的部分才有驅動力（越熱、病媒蚊活動越旺盛） |
> | `3.2 * drive[i - 7]` | 今天的病例數受**7 天前**氣溫驅動——這就是領先指標的延遲效應 |
> | `0.55 * lag` | 前一天病例數的延續性（傳播的自相關） |

> 💡 **這條資料生成流程（DGP）刻意藏了一個「作弊碼」**：氣溫比病例數早 7 天就知道答案。LSTM / CNN 要贏，靠的不是「模型比較潮」，而是它能不能學會利用這個領先指標。

**② 滑動窗口 + 時間切分（絕不 shuffle）**

```python
H = 7   # 預測「幾天後」
L = 21  # 回看「幾天」歷史
feats = np.stack([cases, temp], axis=1).astype(np.float32)

split = n - 60  # 最後 60 天當測試集
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

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `mu = feats[:split].mean(...)` / `sd = feats[:split].std(...)` | 標準化的平均值 / 標準差**只用訓練區間**算，不偷看測試集 |
> | `windows(s, e)` | 滑動窗口：每個樣本 X = 過去 L 天、y = H 天後的病例數 |
> | `train_mask = idxtr_full < val_start` | 依時間序（不 shuffle）切出驗證集 |
> | `Xte, yte, idxte = windows(...)` | 最後 60 天當測試集，模型從沒看過 |

> ⚠️ 這裡沒有一行 `shuffle=True`——序列資料一旦隨機打亂切分，未來的窗口就會混進訓練集，模型等於看過答案，離線表現嚴重高估（對照第 6 節的時間序列切分圖）。

**③ LSTM 模型：有記憶的偵探**

```python
class LSTMModel(nn.Module):
    """用 LSTM 讀過去 L 天的 (cases, temp)，輸出對 H 天後病例數的預測。"""

    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=2, hidden_size=32, batch_first=True)
        self.fc = nn.Linear(32, 1)

    def forward(self, x):
        out, _ = self.lstm(x)      # out 形狀：(batch, L, 32)
        last_step = out[:, -1, :]  # 只取「看完整段序列後」最後一個時間點的隱藏狀態
        return self.fc(last_step)
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `nn.LSTM(input_size=2, hidden_size=32, batch_first=True)` | 2 個輸入特徵（cases, temp），每個時間點更新一個 32 維的「記憶」 |
> | `out, _ = self.lstm(x)` | 讓 LSTM 讀過 21 天的序列，每一步都更新內部記憶 |
> | `last_step = out[:, -1, :]` | 只取「讀完整段歷史後」的最後一個隱藏狀態，當作整段案情的摘要 |
> | `self.fc(last_step)` | 把摘要轉成一個數字：7 天後的病例數預測 |

> 🕵️ **LSTM = 有記憶的偵探**：讀完 21 天的線索後，腦中留下的不是最後一天的片段記憶，而是**整段案情的摘要**——「病例數這週是不是一直在爬升？氣溫是不是連續偏高？」這正是它能抓住趨勢與延遲效應的原因。訓練迴圈跟 Step 1 完全一樣的四拍節奏，額外加上「暖身期」：先讓模型訓練一段時間，才開始算 patience，避免太早被還在震盪的驗證分數騙走（1D-CNN 用同一套訓練函式，只把模型換成兩層 `nn.Conv1d` 疊出的卷積網路，改用一個很小的滑動視窗抓局部形狀）。

**④ Persistence 基準 + 結果比較**

```python
persistence_pred = np.array([cases[j - H] for j in idxte])


def mae_score(pred, idxs):
    return np.mean(np.abs(pred - cases[idxs]))


print(f"{'模型':<24}{'MAE':>8}")
for name, pred in [
    ("Persistence（naive 基準）", persistence_pred),
    ("LSTM", lstm_pred),
    ("1D-CNN", cnn_pred),
]:
    print(f"{name:<24}{mae_score(pred, idxte):>8.3f}")
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `persistence_pred = ... cases[j - H]` | **naive 基準**：假設「7 天後的病例數 = 現在最後已知的病例數」，完全不用氣溫、不用模型 |
> | `mae_score(pred, idxs)` | 平均絕對誤差（MAE）：預測跟真實病例數差幾個 |
> | 迴圈印出三個模型的 MAE | 把 DL 跟「什麼都不做」放在同一張成績單上比 |

> 🧭 **序列預測評估的第一道關卡**：模型如果贏不過 persistence，代表複雜度是白費的。

**誠實的結果**：

| 模型 | MAE |
|---|---|
| Persistence（naive 基準） | 2.88 |
| LSTM | **2.15** |
| 1D-CNN | 2.20 |

這次 DL 真的贏了，而且贏得不小。**為什麼？**

1. **用到了領先指標**：persistence 只看得到病例數本身，完全不知道 7 天前氣溫已經升高、7 天後病例數大概率會跟著漲；LSTM / CNN 把氣溫這個額外訊號一起餵進去
2. **DGP 裡有非線性、有時間延遲的交互作用**（7 天前氣溫驅動今天病例數），這正是神經網路擅長抓的模式

**什麼時候 naive 基準很難打敗？** 如果曲線是單純、平滑的單變量序列（沒有額外的領先指標、沒有明顯的非線性延遲），persistence 或簡單的移動平均往往已經很強，複雜模型不見得能顯著超越——這時候多加一層 LSTM / CNN 可能只是徒增複雜度和過擬合風險。實務上遇到序列預測，**永遠要先跑一個 naive 基準**，再決定要不要上模型；這跟第 5 節的決策框架是同一個精神。

---

## Part B — 現代 DL 全景（概念導覽，非本書執行）

Part A 讓你看到深度學習的兩種面貌：在小樣本分類上殺雞用牛刀（贏不了 sklearn），在有領先指標的序列預測上真的比較利。但深度學習的版圖遠不止 MLP、LSTM、CNN。以下工具**不在本書執行**（需要額外套件、GPU，或連網下載大型預訓練權重），用「比喻 + epi 用途 + 何時用 + 工具 + 示意程式」快速導覽，讓你知道未來遇到什麼問題，該去找哪個工具。

```{figure} images/dl_model_zoo.svg
:name: fig-dl-model-zoo
:alt: DL Model Zoo：MLP是表格資料的預設起點、LSTM是有記憶的偵探適合有時間相關性的序列、CNN是看局部指紋的鑑識官適合抓局部特徵、GNN是社群網絡分析師適合空間傳播與接觸網絡、Transformer或TFT懂得分配注意力適合長序列多變量預測、PINN是綁著物理定律的模型適合資料少但機制明確如SEIR、TSFM是讀遍全球案件的老手適合零樣本少樣本與新病原早期
:width: 100%

看題目長什麼樣子，就知道該找誰幫忙——不同任務，找不同專長的模型。
```

### GNN（圖神經網路）——社群網絡分析師

- **比喻**：像一位熟悉社群網絡的分析師，不只看每個人自己的特質，還看「誰跟誰有連結」
- **epi 用途**：接觸者追蹤網絡（誰跟誰同房、共同活動）、跨機構轉診網絡、地理鄰接的空間傳播
- **何時用**：資料自然長成「節點 + 邊」的圖結構，而且關係本身帶有預測力（例如：某住民感染風險高，部分是因為他跟很多已感染者有接觸）
- **工具**：`torch-geometric`（PyG）、`DGL`

```python
# 示意，非本書執行 —— GNN：把接觸者網絡當圖來學
import torch
from torch_geometric.nn import GCNConv

class ContactGNN(torch.nn.Module):
    """節點 = 住民，邊 = 有接觸史（同房、共同活動）。"""

    def __init__(self, n_features, hidden=16):
        super().__init__()
        self.conv1 = GCNConv(n_features, hidden)
        self.conv2 = GCNConv(hidden, 1)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        return self.conv2(x, edge_index)  # 每位住民的感染風險分數
```

### 時空 Transformer / TFT——懂得分配注意力

- **比喻**：像一位懂得分配注意力的秘書，在一長串資料裡自動找出「這次預測該多看哪一天、哪個變數」
- **epi 用途**：同時看病例數、氣溫、人流、疫苗覆蓋率等多個領先指標，且要預測很多天以後
- **何時用**：序列夠長（通常要幾百到幾千個時間點）、有多個共變量、需要可解釋的 attention 權重
- **工具**：`pytorch-forecasting`（Temporal Fusion Transformer, TFT）、Hugging Face 的時序 transformer 模型

```python
# 示意，非本書執行 —— Temporal Fusion Transformer：多變量疫情預測
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

### DeepSurv——神經網路版本的 Cox 迴歸

- **比喻**：Ch09 的 Cox 迴歸假設每個因子對 log(hazard) 的貢獻是線性相加；DeepSurv 把這條線性關係換成一個神經網路，讓風險因子之間的非線性、交互作用有機會被學到
- **epi 用途**：存活分析（呼應 Ch09）但懷疑風險因子之間有非線性、交互作用，或資料是高維的（基因體、影像）
- **何時用**：Cox 的比例風險假設可能不成立、而且資料量夠大，足以支撐神經網路而不過擬合
- **工具**：`pycox`（DeepSurv、CoxTime、DeepHit）

```python
# 示意，非本書執行 —— DeepSurv：用神經網路取代 Cox 的線性 log(HR)
import torchtuples as tt
from pycox.models import CoxPH

net = tt.practical.MLPVanilla(in_features=10, num_nodes=[32, 32], out_features=1)
model = CoxPH(net, tt.optim.Adam)
model.fit(x_train, (duration_train, event_train), epochs=100)
```

### TSFM（時序基礎模型）——讀遍全球案件的老手

**時序基礎模型（Time Series Foundation Model, TSFM）** 是在海量、跨領域的時間序列上預訓練好的模型，拿來預測新的序列時，通常不需要重新訓練（**零樣本 zero-shot**）或只需要極少量資料微調（**少樣本 few-shot**）——這正是**遷移學習（transfer learning）**的思路：借用在別的大量資料上已經學好的知識，直接套在你手上這條資料量不多的新序列。

| TSFM | 核心 | 優勢 | 工具 |
|---|---|---|---|
| **TimesFM**（Google） | Decoder-only transformer，在海量時序上預訓練 | 零樣本預測，不用重新訓練 | `timesfm` |
| **Chronos**（Amazon） | 把時序數值 token 化，套用語言模型架構訓練 | 開源、多種模型尺寸可選 | `chronos-forecasting` |
| **Moirai**（Salesforce） | 通用型多變量時序基礎模型 | 支援不同頻率、多變量輸入 | `uni2ts` |
| **TimeGPT**（Nixtla） | 商用 API，GPT 風格時序模型 | 好上手，有 hosted API | `nixtla` |

```python
# 示意，非本書執行 —— TSFM 零樣本預測（不用任何本地訓練）
import timesfm

tfm = timesfm.TimesFm(context_len=512, horizon_len=14, backend="cpu")
tfm.load_from_checkpoint(repo_id="google/timesfm-1.0-200m")
forecast, _ = tfm.forecast([cases_history], freq=[0])  # 直接預測，沒有 fit() 這一步
```

> ⚠️ **TSFM 需要下載大權重、需要連網**，本書的 build 不會執行這段程式——但這正是第 5 節決策樹第④格的答案：新病原初期資料極少，卻能借用「別人的疫情資料」預訓練好的模型，不用從零開始等資料累積。

### 混合 / 知識注入（最推薦給流行病學家）

單純的「黑盒 DL」跟單純的「機制模型」各有極限：DL 不懂生物機制、容易在資料稀少時預測出不合理的曲線；機制模型（如 Ch07 的 SEIR）懂機制，但參數難配適、遇到複雜非線性關係會 fit 不準。把兩者結合，是流行病學最務實的路線。

**PINN（Physics-Informed Neural Network，物理知情神經網路）**：讓模型同時考兩張考卷——一張問「跟觀測資料對不對得上」，一張問「符不符合 SEIR 微分方程式」。

```{figure} images/pinn_seir_loss.svg
:name: fig-pinn-seir-loss
:alt: PINN示意：模型必須同時做對兩件事，L_data資料誤差衡量模型預測與實際觀測病例數的差距讓模型準，L_physics物理殘差衡量S、E、I、R是否遵守SEIR微分方程式讓模型合理，兩者相加成總loss
:width: 100%

PINN 的 loss = L_data（貼近資料）+ L_physics（遵守 SEIR 方程式）——兩者缺一不可。
```

- **比喻**：綁著物理定律的模型——不管猜得多準，只要違反 SEIR 方程式的邏輯（例如人數變成負的、康復的人又重新變成易感），就要被扣分
- **epi 用途**：資料稀少但機制明確的新興傳染病（群突發剛爆發，只有零星每日通報數，但 SEIR 結構已知）
- **何時用**：樣本極少、生物 / 傳播機制清楚，想要一條「符合流行病學常理」的曲線，而不是只 fit 噪音
- **工具**：通常自己用 PyTorch 手刻（`nn.Module` + 自訂 loss），或用 `DeepXDE` 等通用 PINN 框架

```python
# 示意，非本書執行 —— PINN：SEIR 方程式寫進 loss
def pinn_loss(model, t_data, y_data, t_physics, beta):
    # L_data：模型預測 vs. 實際觀測病例數，讓模型「準」
    pred = model(t_data)
    l_data = torch.mean((pred - y_data) ** 2)

    # L_physics：S 對 t 的自動微分，是否滿足 SEIR 微分方程式，讓模型「合理」
    S, E, I, R = model(t_physics).split(1, dim=1)
    dS_dt = torch.autograd.grad(S.sum(), t_physics, create_graph=True)[0]
    residual = dS_dt - (-beta * S * I)  # 只示範 dS/dt 這一條方程式
    l_physics = torch.mean(residual ** 2)

    return l_data + l_physics
```

**Mechanistic-AI ensemble（機制模型 + ML 集成）**：讓機制模型先給一個「有物理常識」的初步猜測，再讓 ML / DL 只學「機制模型猜錯的殘差」——不用從頭學整條曲線，也不會脫離流行病學常理。

- **比喻**：資深主治醫師（機制模型）先給一個粗略但合理的診斷，實習醫師（ML）只需要專注修正主治醫師容易忽略的細節
- **epi 用途**：結合 Ch07 的 SEIR 時間序列模型與 Ch10 / Ch11 的 ML / DL，兼顧可解釋性與擬合力
- **何時用**：想要模型輸出符合流行病學常識（不會預測出負的病例數、不會忽略 $R_0$ 的限制），但 SEIR 本身 fit 不夠準
- **工具**：手動組裝（把 SEIR 模擬輸出當 ML 特徵），或參考 CDC FluSight 一類的模型集成框架概念

```python
# 示意，非本書執行 —— Mechanistic-AI ensemble：SEIR 當基準，殘差交給 ML
seir_forecast = run_seir_simulation(beta, gamma, sigma, initial_state)  # Ch07 的機制模型
residual = observed_cases - seir_forecast                              # 機制模型猜不準的部分

residual_model = RandomForestRegressor(n_estimators=200)
residual_model.fit(X_covariates, residual)          # 讓 ML 只學殘差，不用從頭學整條曲線

final_forecast = seir_forecast + residual_model.predict(X_covariates_future)
```

---

## 評估與可解釋性

### 指標怎麼選

| 任務 | 指標 | 白話意思 |
|---|---|---|
| 預測（迴歸） | **MAE** | 平均差幾個病例數，最直覺 |
| | **RMSE** | 對大誤差更敏感，一次離群值會被放大 |
| | **MAPE / sMAPE** | 誤差佔真實值的百分比，方便跨情境比較 |
| | **CRPS**（機率預測） | 整條預測分布跟真實值的距離，不只看點估計 |
| 分類 | **AUC** | 排序能力（見 Ch10）；**F1** 平衡精確率與召回率；**PR-AUC** 適合不平衡資料 |
| 校準 | **Calibration 曲線 / Brier score** | 模型說「70% 機率」的那群，真的約 70% 發生嗎？會排序 ≠ 機率準（呼應 Ch10） |
| epi 專屬 | **Peak-timing error** | 預測的疫情高峰日期，跟實際高峰差幾天 |
| | **Outbreak detection delay** | 模型比真正的疫情上升晚幾天才抓到訊號 |

### 打開黑盒子

- **SHAP**：跟 Ch10 一樣的公平分紅邏輯——問「少了這個特徵，預測差多少」，可以直接套用在 DL 模型上（`shap.DeepExplainer`），對單一病人 / 單一時間點給出「哪些線索貢獻了多少」
- **Attention 權重**：Transformer / TFT 這類模型內建「注意力」機制，可以直接印出模型在做這次預測時，最看重哪一天、哪個變數——比 SHAP 更輕量，是模型本身自帶的解釋
- **PDP（partial dependence plot，部分依賴圖）**：固定其他變量，只讓一個特徵變化，看預測值怎麼跟著變——DL 模型一樣適用，適合檢查「模型有沒有學到符合常理的劑量反應關係」

> 🧭 跟 Ch10 一樣的提醒：**重要 ≠ 因果**。SHAP、attention 告訴你模型有多依賴某條線索來預測，不代表改變這個特徵就能改變結果——真正要問因果，要看 Ch06 校正干擾後的 adjusted OR，或 Ch12 的因果推論方法。

## 練習題

- 作業版：[`11_dl_exercise.ipynb`](exercises/11_dl_exercise.ipynb)
- 解答版（講師）：[`11_dl_solution.ipynb`](solutions/11_dl_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/11_dl_solution.ipynb>)

## 常見誤用

| 錯誤 | 正確做法 |
|------|---------|
| 時序資料隨機切分（`shuffle=True`） | 按時間切，用滾動 / 擴張窗口（第 6 節），未來絕不能混進訓練集 |
| 小資料集用複雜架構 | 先看參數 / 樣本比；280 筆最多用 1–2 層隱藏層，甚至乾脆別用 DL |
| 只報訓練集結果 | 一定要用獨立的 validation / test 評估，且序列預測要贏過 naive 基準 |
| 沒固定 random seed | `torch.manual_seed()` + `np.random.seed()` 確保可重現 |
| 忽略不確定性，只給單一預測值 | 政策決策需要信賴區間 / 機率分布，不能只給一個數字就下判斷 |
| 黑箱模型盲目信任 | 用 SHAP / attention 權重 / PINN 的物理約束打開黑盒子 |
| 以為 DL 一定贏傳統 ML | 280 筆分類上 DL 跟 logistic 打平；序列預測 DL 會贏，是因為有領先指標 + 非線性延遲，不是 DL 天生比較強 |

## 為什麼流行病學家要學 DL？——10 週學習路徑

**為什麼值得學**：現實中的流行病學資料正在變得更像 DL 的主場——高維、嘈雜、非線性的資料（基因體、影像、穿戴式裝置訊號）、需要建模空間擴散與接觸網絡的時空資料（GNN 的主場）、以及新興病原爆發初期資料極度稀缺、卻能借用全球其他疫情經驗的情境（TSFM 零樣本預測的主場）。這些都不是傳統統計方法擅長的地形。

一個務實的 10 週自學路徑，把本章的內容拆成漸進的專案：

| 週次 | 主題 |
|---|---|
| 1–2 | Python / PyTorch 基礎、tensor、資料前處理（對應本章 Part A Step 1） |
| 3–4 | 訓練迴圈、早停法、過擬合診斷（本章核心概念 + Part A） |
| 5–6 | 序列預測：滑動窗口、時間切分、LSTM、CNN（本章 Part A Step 2） |
| 7 | GNN：空間傳播、接觸網絡 |
| 8 | 時空 Transformer / TFT：多變量長序列預測 |
| 9 | TSFM 零樣本預測 + PINN / Mechanistic-AI ensemble |
| 10 | 專案實作：挑一個真實資料集，完整跑一輪 + 用 SHAP / attention 寫一份可解釋性報告 |

## 下一步

這章用 DL 老實回答了兩個問題：280 筆能不能靠深度學習贏過 sklearn（不太行），以及深度學習在哪裡真正發威（有領先指標、非線性延遲的序列預測）。但不管模型多準，**預測力強不等於因果關係**。

下一章（Ch12），我們回到最根本的問題：**淋浴暴露真的「導致」感染嗎？還是只是統計上的相關？** → 因果推論。
