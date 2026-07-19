# 06 多變項分析：調整後風險比與邏輯斯迴歸

## 情境

Ch05 的分層分析告訴我們，功能狀態確實是淋浴使用的干擾因子。但疫調會議上，感控護理師追問：

> 「同時考慮年齡、所有共病、功能狀態、樓層以後，淋浴使用**還是**顯著的危險因子嗎？」

分層分析一次只能控制一個變項。要**同時調整多個因子**，需要迴歸模型。

> 🔑 **關鍵回顧**：Ch03 將本案定位為**回溯性世代研究**（retrospective cohort），效應測量用 **RR（風險比）**。Ch05 分層分析也算的是 **MH adjusted RR**。為了一路都用同一把尺，這章的主軸方法會是 **Modified Poisson regression**——直接算出 **adjusted RR**。我們也會用邏輯斯迴歸做對照，讓你看到同樣的資料算出 OR 會高估多少。

## 你將學到

- Modified Poisson regression（Zou 2004）同時調整多個因子，算出 adjusted RR
- 邏輯斯迴歸的原理——用白話文搞懂「機率→勝算→log(勝算)」三階梯
- 在高侵襲率世代研究中，OR 如何高估效應（與 RR 的實際數值比較）
- 比較 crude RR → MH adjusted RR (Ch05) → adjusted RR → adjusted OR
- 標準流行病學 Table 2 格式呈現結果
- 模型診斷（AIC）與變項選擇

## 🎯 超白話特別篇：用「補習班真的有效嗎」看懂多變項分析

> 「多變項分析」「校正 OR」「勝算比」聽起來像大人的世界？別怕。這一段先把護理之家放一邊，改用一個**你我從小吵到大**的問題——**「補習班到底有沒有用？」**——把整套邏輯講到讓國中生也秒懂。看完再回頭看下面的迴歸表，你會發現：喔～原來每個數字在講這件事！

### 一個吵不完的問題：補習班真的讓人變強嗎？

有人調查一群國中生，發現：

> **有補習的同學，考到 80 分以上的比例是 64%；沒補習的只有 29%。**

如果直接下結論——**「補習讓高分率翻倍，快去報名！」**——你可能又中了 Ch05 那個「大腳丫」的圈套。因為……

> 🤔 **會去補習的小孩，通常家裡本來就比較多書、爸媽比較重視讀書。** 也就是說，有一個「家庭背景」的東西，**同時**讓小孩「更會去補習」又「本來就更會考高分」。

這個「家庭背景」就是躲在背後的**干擾因子（confounder）**——跟大腳丫故事裡的「年齡」是同一種角色。

### 但這次不一樣：補習「可能真的有一點用」

Ch05 的大腳丫，分層之後 RR 從 2.1 一路掉到 **1.0**——腳大小根本**完全沒用**，是純粹的假象。但補習不太一樣：**它可能真的有一點點效果，只是被家庭背景「灌水」灌得太誇張。** 我們想問的是：

> **把家庭背景「扣掉」以後，補習「自己」還剩幾分真本事？**

這就需要**多變項分析**登場了。

### 關鍵直覺一：平行時空的雙胞胎

怎麼「扣掉家庭背景」？想像一個畫面：

> 👯 **有一個跟你一模一樣的雙胞胎**——一樣聰明、家裡一樣多書、爸媽一樣的態度——**唯一的差別是「他有去補習，你沒有」。** 那麼他考得比你高嗎？高多少？**那個「多出來的分數」，才是補習班自己的真本事。**

多變項迴歸做的就是這件事：它在數學上「**假裝其他條件都一樣**」，只讓補習這一項不同，算出補習**單獨**的效果。這叫作「**在其他因子固定下**（holding others constant）」。

### 關鍵直覺二：為什麼要「一起」放進一個模型？

你可能會問：那我一個一個變項分開分析不就好了？

> 🕵️ **偵訊室比喻**：一個一個分開問嫌犯，每個都會把別人的功勞攬在自己身上（「都是我做的！」）。但**把所有嫌犯關進同一間偵訊室、一起對質**，才擠得出每個人**真正**做了多少。多變項模型就是那間偵訊室——把補習、家庭背景、年齡、共病…全部放進**同一個**模型一起算，每個因子的效果都是「**扣掉其他人之後**」的淨貢獻。

這正是多變項分析比 Ch05 分層分析強的地方：**分層一次只能控制一個變項，迴歸可以一次控制一大票。**

```{figure} images/cram_school_multivariable.svg
:name: fig-cram-school-multivariable
:alt: 補習班多變項分析：只看補習時補習組高分率 64%、沒補習組 29%（粗 OR≈4.3），但真正功臣是家庭背景（家裡藏書）；把補習和家裡藏書一起放進迴歸模型後，補習的 OR 從 4.3 縮水到 1.5，代表補習自己的效果只加一點點
:width: 100%

左上：只看補習，好像超有效（粗 OR 4.3）；右上：真正功臣「家庭背景」同時牽動補習和高分；下方：把兩者一起放進模型後，補習的 OR **縮水到 1.5**——不是歸零，是「縮水但還活著」。
```

### 順便搞懂：勝算（odds）和勝算比（OR）

迴歸吐出來的數字叫 **OR（勝算比）**，不是 RR。「勝算」是什麼？用賭盤來想最快：

> 🎲 **機率**是「30 個人裡有 6 個感染」＝ 6/30 = 20%。
> **勝算（odds）**是「感染的 6 個 **對** 沒感染的 24 個」＝ 6:24 = 0.25，像賭盤上的**賠率**。
> **勝算比（OR）**就是把兩組的賠率**相除**。補習組 OR = 4.3 的意思是：「補習組『考到高分』的**賭盤賠率**，是沒補習組的 4.3 倍。」

### 動手玩玩看：親手把補習的「真本事」算出來

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

rng = np.random.default_rng(42)
n = 800

# 每個學生：家裡藏書量（十本）、有沒有補習、有沒有考到 80 分
# 家裡藏書是「上游」因子：書多 → 既更會去補習，也本來就更會考高分（真干擾因子）
home_books = rng.normal(10, 3, n).clip(2, 20)
p_cram = 1 / (1 + np.exp(-(home_books - 10) / 2))   # 書多的小孩更會去補習
cram = rng.binomial(1, p_cram)
# 考高分：主要靠家庭背景，補習「本身」只加一點點（真效果 OR = e^0.4 ≈ 1.5）
p_high = 1 / (1 + np.exp(-(-6 + 0.55 * home_books + 0.4 * cram)))
high_score = rng.binomial(1, p_high)

students = pd.DataFrame({"cram": cram, "home_books": home_books, "high_score": high_score})

# ① 只看補習（單變項）：兩組高分率差多少？
r1 = students.loc[students.cram == 1, "high_score"].mean()
r0 = students.loc[students.cram == 0, "high_score"].mean()
print(f"補習組 高分率 {r1:.0%}，沒補習組 {r0:.0%}")

# 粗 OR：模型裡只放「補習」
crude = smf.logit("high_score ~ cram", data=students).fit(disp=0)
print(f"粗 OR（只看補習）              = {np.exp(crude.params['cram']):.2f}")

# ② 多變項：把「補習 + 家裡藏書」一起放進同一個模型（那間偵訊室）
adj = smf.logit("high_score ~ cram + home_books", data=students).fit(disp=0)
print(f"校正 OR（同時放補習和家裡藏書）= {np.exp(adj.params['cram']):.2f}")
```

跑出來會看到：

```text
補習組 高分率 64%，沒補習組 29%
粗 OR（只看補習）              = 4.33
校正 OR（同時放補習和家裡藏書）= 1.51
```

> 💡 **這就是那個「aha」**：補習的光環，有一大半其實是「家裡本來就多書」借給它的——把光環一片一片撕掉，OR 從 **4.3 掉到 1.5**。原來大半是別人的功勞，但**剩下的 1.5 是補習自己賺的**。

### ⚠️ 三個必記的但書

1. **校正後不一定變小**：這次補習從 4.3 縮到 1.5，但校正也可能讓數字**變大**、甚至**改變方向**。重點不是「一定縮水」，而是「**只要一校正就變了，就代表有干擾**」。
2. **模型只能拆穿你請進偵訊室的嫌犯**：你沒想到、沒放進模型的因子（例如「有沒有睡飽」），照樣在外面逍遙——這叫**殘餘干擾（residual confounding）**。所以校正後的數字是「**目前已知條件下**」的最佳估計，不等於鐵板釘釘的因果。
3. **OR 不是「機率的幾倍」**：OR = 4.3 是**勝算**的 4.3 倍，不是**風險**的 4.3 倍。而且**疾病越常見，OR 把數字吹得越誇張**——本案侵襲率高達 43%（超常見！），所以本章的**主力方法是 Modified Poisson**，直接算老實的 **RR（風險比）**，而不是用容易高估的 OR。

### 讀數字小抄（存起來）

| 你看到… | 白話意思 |
|---|---|
| 只放一個變項算出的 OR/RR | **粗**（crude）值，可能被干擾因子灌水 |
| 模型裡放了一堆變項 | **多變項**：每個係數都是「其他因子固定下」的淨效果 |
| 粗 OR 4.3 → 校正 OR 1.5 | 縮水但沒歸零：一部分是借來的光環，一部分是真本事 |
| 校正後變了（變大/變小/翻向） | 有干擾因子在作用 |
| 校正後幾乎沒變 | 那個變項大概不是重要干擾因子 |
| OR（來自 logistic） | 「**勝算**」幾倍——高侵襲率下會高估風險 |
| RR（來自 Modified Poisson） | 「**風險**」幾倍——世代研究首選、比較誠實 |
| exp(係數) | 把迴歸係數 β 變回 OR 或 RR（$e^\beta$） |

### 回到真實：補習 → 淋浴

現在把故事裡的角色換成護理之家的版本：

| 補習班故事 | 護理之家真實案例 |
|---|---|
| 有沒有補習（暴露） | 有沒有用**淋浴**（`shower_use`） |
| 考到高分（結果） | 有沒有**感染**退伍軍人症 |
| 家庭背景／家裡藏書（干擾） | **年齡、共病、功能狀態**（`age`、`comorbidity_*`、`functional_status`） |
| 平行時空的雙胞胎 | 迴歸係數＝「其他因子固定下」的效果 |
| 一起關進偵訊室對質 | 多變項模型，一次調整多個因子 |
| 補習的「賭盤賠率」倍數 | 勝算比 OR（邏輯斯迴歸） |
| 補習的「上榜人數」倍數 | 風險比 RR（Modified Poisson，本章主力） |

你剛剛在補習班身上學會的每一招——粗值 vs 校正值、雙胞胎直覺、偵訊室一起算、OR vs RR——**就是本章 Step 2–5 在護理之家資料上做的事**。現在往下看那些迴歸表和 Table 2，是不是突然變親切了？😉

---

## 核心概念

### 為什麼還要繼續談 RR？

Ch03 已經解釋過：在世代研究中，我們能直接算出「風險」（risk = 得病人數 ÷ 總人數），所以效應測量應該用 **RR**。只有在病例對照研究（case-control）中，因為無法計算風險，才退而求其次用 **OR**。

> ⚠️ 本案侵襲率高達 **43%**。Ch03 已經警告過：當疾病不罕見時，OR 會**系統性高估**效應。如果你對主管說「淋浴使用的 OR 是 3.5」，他會以為風險是 3.5 倍——但真正的風險比（RR）可能只有 2.0 倍。差很多！

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：為什麼要用 RR 而不是 OR？</div>
  <div class="youtube-lite" data-id="PrbPC5cAyxM">
    <img src="https://img.youtube.com/vi/PrbPC5cAyxM/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

### 兩條多變項分析路線

```{figure} images/multivariate_methods.svg
:name: fig-multivariate-methods
:alt: 三種控制干擾因子的方法比較：分層分析（Ch05）、Modified Poisson（Ch06 主軸）、邏輯斯迴歸（Ch06 對照）
:width: 100%

分層分析一次只能控制一個因子；Modified Poisson 和邏輯斯迴歸都能同時控制多個，但前者輸出 RR、後者輸出 OR。
```

| 方法 | 輸出 | 世代研究適用？ | 何時用？ |
|------|------|--------------|---------|
| 分層分析（Ch05） | MH adjusted RR | 適合，但一次只能控制 1 個因子 | 干擾因子少（1-2 個） |
| **Modified Poisson**（本章主軸） | **adjusted RR** | **首選** | 世代研究 + 多個干擾因子 |
| 邏輯斯迴歸（本章對照） | adjusted OR | 高侵襲率下高估 | 病例對照研究、罕見疾病 |

### Modified Poisson：用 Poisson 的殼算 RR 的魂

> 🎩 **借帽子比喻**：Poisson 迴歸本來是給「計數資料」用的（例如每天新增幾例）。但流行病學家 Zou（2004 年）發現了一個巧妙的把戲：把二元結果（0/1）丟進 Poisson 迴歸，再用 **robust sandwich variance** 修正標準誤差——得到的 coefficient 就正好是 **log(RR)**！就像跟朋友借了一頂帽子，尺寸不對但貼個修正貼紙就完美合頭了。

為什麼能這樣做？三句話版：

1. Poisson 迴歸模型化的是 **log(E[Y])**，當 Y 是 0/1 時，E[Y] = P(Y=1) = risk，所以 coefficient = **log(risk ratio)**
2. 但 Poisson 模型假設 variance = mean，對二元資料來說這是錯的 → 標準誤差會偏掉
3. **Robust (sandwich) SE** 不依賴分佈假設，直接從資料估算變異 → 修正了上面的偏差 → CI 和 p-value 都正確

> 💡 為什麼不用 **log-binomial**（Binomial + log link）？理論上最「正確」，但實務上常常不收斂（convergence failure），特別是暴露和結果的關聯很強時。Modified Poisson 幾乎不會有收斂問題。
>
> 為什麼不用 **Cox regression**（proportional hazards）？Cox 需要「時間到事件」的資料，我們的資料是二元結果（感染/未感染），沒有隨訪時間差異。

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：Modified Poisson——借帽子算 RR 的魔法</div>
  <div class="youtube-lite" data-id="A_KHcLHITN0">
    <img src="https://img.youtube.com/vi/A_KHcLHITN0/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

### 邏輯斯迴歸白話文

雖然 Modified Poisson 是本案的首選，邏輯斯迴歸（logistic regression）仍然是全世界最常用的多變項分析方法之一。理解它的原理對流行病學家是必備素養。

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：邏輯斯迴歸三階梯——機率→勝算→logit</div>
  <div class="youtube-lite" data-id="o-bRxWzK_xo">
    <img src="https://img.youtube.com/vi/o-bRxWzK_xo/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

```{figure} images/logit_intuition.svg
:name: fig-logit-intuition
:alt: 邏輯斯迴歸的三階梯：機率（0-1）→ 勝算（0-∞）→ log(勝算)（-∞ 到 +∞）
:width: 100%

把機率「拉直」的三個步驟：被卡住的彈簧 → 天平 → 拉直的直線。
```

**第一階：機率（probability）**——被壓扁的彈簧

感染機率 $p$ 被卡在 0 到 1 之間。線性迴歸的輸出可以是任意數字（$-\infty$ 到 $+\infty$），但機率不行——你不能說某人的感染機率是 -0.3 或 1.5。就像把彈簧塞進小盒子，越靠近邊界越擠，沒辦法直接做線性迴歸。

**第二階：勝算（odds）**——天平

$$\text{odds} = \frac{p}{1-p}$$

> ⚖️ **天平比喻**：如果感染機率 $p = 0.70$，勝算 = $0.70 / 0.30 = 2.33$。意思是天平上「會感染」那邊比「不會感染」那邊重了 2.33 倍。勝算的範圍是 0 到 $+\infty$，右邊解放了，但左邊還是卡在 0。

**第三階：log(勝算) = logit**——拉直的彈簧

$$\text{logit}(p) = \log\left(\frac{p}{1-p}\right)$$

取 log 之後，範圍變成 $-\infty$ 到 $+\infty$——兩邊都自由了！線性迴歸終於能正常工作。

邏輯斯迴歸的模型就是：

$$\text{logit}(p) = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots$$

**怎麼解讀 $\beta$？** 假設淋浴使用的 $\beta_1 = 0.50$：

- $\text{OR} = e^{0.50} = 1.65$
- 白話文：「控制其他因子後，使用淋浴的住民，感染的**勝算**是未使用者的 **1.65 倍**」
- 注意：這是「**勝算**幾倍」，不是「**風險**幾倍」！在高侵襲率下兩者差距很大

---

## Step 1: 資料準備

```python
# === Step 1: 載入資料 + 變項重新編碼 ===

import pandas as pd
import numpy as np
import statsmodels.api as sm               # GLM (Modified Poisson)
import statsmodels.formula.api as smf       # formula API (logistic)
import matplotlib.pyplot as plt
import warnings

# --- 載入退伍軍人症群聚資料 ---
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# --- 建立二元結果變項 ---
# clinical_severity != "not_ill" 代表有感染（包含 mild/moderate/severe）
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# --- smoking_history 三分類 → 二分類 ---
# never / former / current → 只要不是 never 就算 ever_smoker
df["ever_smoker"] = (df["smoking_history"] != "never").astype(int)

# --- 功能狀態轉有序數值 ---
# bedridden(臥床)=0 < assisted(需協助)=1 < independent(獨立行走)=2
fs_map = {"bedridden": 0, "assisted": 1, "independent": 2}
df["functional_score"] = df["functional_status"].map(fs_map)

# --- 快速確認侵襲率 ---
ar = df["infected"].mean()
print(f"侵襲率 = {ar:.1%}（{df['infected'].sum()}/{len(df)}）")
print(f"→ 侵襲率 {ar:.0%} 遠高於 10%，OR 會顯著高估效應，應以 RR 為主")
```

## Step 2: 單變項分析——Crude RR 與 Crude OR 對照

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：單變項 crude RR vs OR——for loop 一次比完</div>
  <div class="youtube-lite" data-id="LBf3HvGOLAA">
    <img src="https://img.youtube.com/vi/LBf3HvGOLAA/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

```python
# === Step 2: 單變項分析迴圈 ===
# 同時跑 Modified Poisson（算 crude RR）和 logistic（算 crude OR），
# 讓你看到同一個變項的 RR 和 OR 差多少。

from epi_learning.metrics import risk_ratio  # Ch03 的 2×2 手算 RR

factors = [
    "shower_use", "hydrotherapy_use", "ever_smoker",
    "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed",
    "age", "functional_score",
]

crude_results = []

for var in factors:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        # --- (A) Modified Poisson → crude RR ---
        try:
            mod_p = smf.glm(
                f"infected ~ {var}", data=df,
                family=sm.families.Poisson(),   # 借 Poisson 的殼
            ).fit(cov_type="HC0", disp=0)       # robust SE 修正
            rr = np.exp(mod_p.params[var])       # exp(β) = RR
            rr_ci = np.exp(mod_p.conf_int().loc[var])
            rr_p = mod_p.pvalues[var]
        except Exception:
            continue

        # --- (B) Logistic Regression → crude OR ---
        try:
            mod_l = smf.logit(
                f"infected ~ {var}", data=df,
            ).fit(disp=0, method="lbfgs")
            if not mod_l.mle_retvals["converged"]:
                print(f"⚠ {var}: logistic 未收斂，跳過")
                continue
            or_val = np.exp(mod_l.params[var])    # exp(β) = OR
            or_ci = np.exp(mod_l.conf_int().loc[var])
            or_p = mod_l.pvalues[var]
        except Exception:
            continue

    # --- (C) 2×2 手算 RR 交叉驗證（僅二元變項） ---
    hand_rr = ""
    if df[var].dropna().isin([0, 1]).all():
        a = ((df[var] == 1) & (df["infected"] == 1)).sum()
        b = ((df[var] == 1) & (df["infected"] == 0)).sum()
        c = ((df[var] == 0) & (df["infected"] == 1)).sum()
        d = ((df[var] == 0) & (df["infected"] == 0)).sum()
        hand_rr = f"{risk_ratio(a, a+b, c, c+d):.3f}"

    crude_results.append({
        "variable": var,
        "crude_RR": round(rr, 3),
        "RR 95% CI": f"{rr_ci[0]:.3f}–{rr_ci[1]:.3f}",
        "crude_OR": round(or_val, 3),
        "OR 95% CI": f"{or_ci[0]:.3f}–{or_ci[1]:.3f}",
        "hand_RR": hand_rr,
    })

crude_df = pd.DataFrame(crude_results)
print("=== Crude RR vs Crude OR（單變項）===")
print(crude_df.to_string(index=False))
print()
print("💡 注意：crude_OR 普遍大於 crude_RR，這就是高侵襲率下 OR 高估的效果")
print("   hand_RR 欄是 Ch03 的 2×2 表手算結果，應與 crude_RR 幾乎一致")
```

### 讀懂公式語法

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：statsmodels formula 語法速懂</div>
  <div class="youtube-lite" data-id="G-cJPHaz7ag">
    <img src="https://img.youtube.com/vi/G-cJPHaz7ag/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

statsmodels 的公式借用了 R 語言的 **formula 語法**，用一行字就能描述「用哪些變項來預測結果」：

| 符號 | 意思 | 範例 |
|------|------|------|
| `~` | 「被⋯預測」 | `infected ~ age` → 用 age 預測 infected |
| `+` | 「再加上」 | `~ age + sex` → 同時放 age 和 sex 進模型 |
| `C()` | 「當成類別變項」 | `C(floor)` → 把 floor 拆成虛擬變項（dummy coding），每個樓層一個 0/1 指標 |

白話文：`infected ~ shower_use + age + C(floor)` 就是說「用淋浴使用、年齡、樓層來預測感染」。模型會自動加上截距項（Intercept），不用額外寫。

### 模型放哪些變項？——從 Ch03 和 Ch05 的結果出發

多變項模型不是把所有欄位都丟進去，而是要有理由。回顧前面章節的發現，我們把模型變項分成四組：

| 組別 | 變項 | 角色 | 納入理由 |
|------|------|------|----------|
| **暴露因子** | `shower_use`, `hydrotherapy_use` | 研究焦點 | Ch03 篩選出的顯著危險因子——我們最想回答的問題：「淋浴和水療是不是感染源？」 |
| **宿主因子** | `age`, `immunosuppressed`, `functional_score` | 潛在干擾因子 | `age` = 流行病學常規必調整因子；`immunosuppressed` = Ch03 顯示 crude RR 最高的因子之一；`functional_score` = Ch05 已確認的干擾因子 |
| **共病** | `comorbidity_chf`, `comorbidity_dm`, `comorbidity_cancer`, `comorbidity_copd` | 潛在干擾因子 | Ch03 篩選出的候選因子，放入完整模型看控制後暴露因子的 RR 是否改變 |
| **場所** | `C(floor)` | 潛在干擾因子 | 不同樓層的水管系統或暴露機會可能不同，需要控制樓層差異 |

```{tip}
**為什麼不放 `ever_smoker`？** Ch03 的單變項篩選中，吸菸的 crude RR 接近 1 且未達統計顯著，加上它與多項共病高度相關（共線性），納入模型反而增加估計的不穩定性，因此不放進多變項模型。
```

## Step 3: 多變項 Modified Poisson——Adjusted RR

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：多變項 adjusted RR——打造漂亮的 Table 2</div>
  <div class="youtube-lite" data-id="XIfx82VxVaA">
    <img src="https://img.youtube.com/vi/XIfx82VxVaA/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

```python
# === Step 3: Modified Poisson — 同時調整所有因子 ===
# 這是本章的主軸分析：用 Poisson GLM + robust SE 算出 adjusted RR。
# coefficient = log(RR)，取 exp 就是 RR。

# --- 公式說明 ---
# infected ~ ：用右邊的變項預測「是否感染」
# shower_use + hydrotherapy_use ：暴露因子（研究焦點）
# age + immunosuppressed + functional_score ：宿主因子（潛在干擾）
# comorbidity_chf/dm/cancer/copd ：共病（潛在干擾）
# C(floor) ：樓層當類別變項（控制場所差異）
formula = (
    "infected ~ shower_use + hydrotherapy_use + age + "
    "comorbidity_chf + comorbidity_dm + comorbidity_cancer + "
    "comorbidity_copd + immunosuppressed + functional_score + "
    "C(floor)"     # C(floor) = 把 floor 當成類別變項（dummy coding）
)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model_poisson = smf.glm(
        formula, data=df,
        family=sm.families.Poisson(),   # Poisson 的殼
    ).fit(cov_type="HC0")               # robust (sandwich) SE

# --- 整理成 Table 2 格式 ---
adj_rr_results = []
for var in model_poisson.params.index:
    if var == "Intercept":
        continue
    coef = model_poisson.params[var]
    ci = model_poisson.conf_int().loc[var]
    adj_rr_results.append({
        "variable": var,
        "adjusted_RR": round(np.exp(coef), 3),        # exp(β) = adjusted RR
        "95% CI": f"{np.exp(ci[0]):.3f}–{np.exp(ci[1]):.3f}",
        "p-value": round(model_poisson.pvalues[var], 4),
    })

adj_rr_df = pd.DataFrame(adj_rr_results)
print("=== Adjusted RR（Modified Poisson, Table 2）===")
print(adj_rr_df.to_string(index=False))
```

## Step 4: 多變項邏輯斯迴歸——Adjusted OR（對照組）

```python
# === Step 4: Logistic Regression — 同一公式，改用 logistic ===
# 目的：讓你看到同樣的 covariates，OR 和 RR 差多少。

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model_logit = smf.logit(formula, data=df).fit(disp=0, method="lbfgs")

# --- 整理成 Table 2 格式 ---
adj_or_results = []
for var in model_logit.params.index:
    if var == "Intercept":
        continue
    coef = model_logit.params[var]
    ci = model_logit.conf_int().loc[var]
    adj_or_results.append({
        "variable": var,
        "adjusted_OR": round(np.exp(coef), 3),         # exp(β) = adjusted OR
        "95% CI": f"{np.exp(ci[0]):.3f}–{np.exp(ci[1]):.3f}",
        "p-value": round(model_logit.pvalues[var], 4),
    })

adj_or_df = pd.DataFrame(adj_or_results)
print("=== Adjusted OR（Logistic Regression, Table 2）===")
print(adj_or_df.to_string(index=False))
```

```{admonition} 為什麼有些變數「模型未收斂」？
:class: tip, dropdown

當某個二元預測變數的其中一個類別完全（或幾乎完全）對應到某個結果時，稱為**完美分離（complete separation）**或**準完美分離（quasi-complete separation）**。此時最大概似估計法（MLE）的 OR 會趨近 0 或 ∞，Hessian 矩陣無法反轉，導致模型無法收斂。

常見處理方式：
1. 檢查 2×2 表，確認是否有某個格子 = 0
2. 改用 **Firth's penalized likelihood**（`firthlogist` 套件）
3. 改用 **Exact logistic regression**
4. 在教學場景中，先跳過該變數，在多變項模型中一起納入
```

## Step 5: 三個效應測量並排比較

```python
# === Step 5: Crude RR vs Adjusted RR vs Adjusted OR 並排比較 ===
# 這是本章最重要的表格：一次看完三種效應測量的差異。

key_vars = ["shower_use", "hydrotherapy_use", "age",
            "comorbidity_chf", "immunosuppressed", "functional_score"]

comparison = []
for var in key_vars:
    # 從 crude_df 取 crude RR
    c_row = crude_df[crude_df["variable"] == var]
    if len(c_row) == 0:
        continue
    c_rr = c_row.iloc[0]["crude_RR"]

    # 從 adj_rr_df 取 adjusted RR
    a_rr_row = adj_rr_df[adj_rr_df["variable"] == var]
    if len(a_rr_row) == 0:
        continue
    a_rr = a_rr_row.iloc[0]["adjusted_RR"]

    # 從 adj_or_df 取 adjusted OR
    a_or_row = adj_or_df[adj_or_df["variable"] == var]
    if len(a_or_row) == 0:
        continue
    a_or = a_or_row.iloc[0]["adjusted_OR"]

    # 計算變化幅度
    rr_change = ((a_rr - c_rr) / c_rr * 100) if c_rr != 0 else 0
    or_vs_rr = ((a_or - a_rr) / a_rr * 100) if a_rr != 0 else 0

    comparison.append({
        "variable": var,
        "crude_RR": c_rr,
        "adj_RR": a_rr,           # Modified Poisson
        "adj_OR": a_or,           # Logistic
        "crude→adj RR": f"{rr_change:+.1f}%",    # 干擾效應
        "adj RR→OR": f"{or_vs_rr:+.1f}%",        # OR 高估幅度
    })

comp_df = pd.DataFrame(comparison)
print("=== Crude RR → Adjusted RR → Adjusted OR 比較 ===")
print(comp_df.to_string(index=False))
print()
print("📊 解讀：")
print("  • crude→adj RR 欄：控制干擾因子後 RR 的變化（與 Ch05 MH 結論比較）")
print("  • adj RR→OR 欄：同一模型下 OR 比 RR 高估多少（侵襲率效應）")
```

```{admonition} 何時 OR ≈ RR？
:class: note

只有當**疾病罕見**（盛行率 < 10%）時，$(1-p) \approx 1$，odds $\approx$ risk，OR $\approx$ RR。本案侵襲率 43%，OR 會系統性地**放大**效應。因此在世代研究中報告結果時，應該用 RR 而非 OR。

如果你在讀別人的論文，看到他們用 logistic regression 分析**世代研究**且疾病不罕見，可以留意他們是否有用 Modified Poisson 或至少提到 OR ≠ RR 的問題。
```

## Step 6: Forest Plot（Adjusted RR）

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：Adjusted RR 森林圖——一眼看穿真正危險因子</div>
  <div class="youtube-lite" data-id="7GgpIOKr_CY">
    <img src="https://img.youtube.com/vi/7GgpIOKr_CY/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

```python
# === Step 6: Forest Plot — 用圖表呈現 adjusted RR ===
# 標準的流行病學 forest plot：點 = 點估計，橫線 = 95% CI，虛線 = RR=1（無效應）

# 準備繪圖資料（排除 Intercept 和 floor dummy）
plot_vars = [r for r in adj_rr_df["variable"] if not r.startswith("C(floor)")]
plot_data = adj_rr_df[adj_rr_df["variable"].isin(plot_vars)].copy()

# 從 CI 字串還原數值
plot_data["ci_lo"] = plot_data["95% CI"].str.split("–").str[0].astype(float)
plot_data["ci_hi"] = plot_data["95% CI"].str.split("–").str[1].astype(float)

fig, ax = plt.subplots(figsize=(8, 5))

y_pos = range(len(plot_data))
ax.errorbar(
    plot_data["adjusted_RR"], y_pos,
    xerr=[plot_data["adjusted_RR"] - plot_data["ci_lo"],
          plot_data["ci_hi"] - plot_data["adjusted_RR"]],
    fmt="o", color="#D97757", ecolor="#6A9BCC",   # 品牌色
    elinewidth=2, capsize=4, markersize=7,
)
ax.axvline(x=1, color="#6B6B6B", linestyle="--", linewidth=1, label="RR = 1（無效應）")
ax.set_yticks(list(y_pos))
ax.set_yticklabels(plot_data["variable"])
ax.set_xlabel("Adjusted RR（95% CI）")
ax.set_title("Forest Plot — Adjusted Risk Ratio（Modified Poisson）")
ax.legend(loc="lower right", fontsize=9)
ax.invert_yaxis()              # 第一個變項在最上面
plt.tight_layout()
plt.show()
```

## Step 7: 模型診斷

```python
# === Step 7: 模型診斷 — AIC 比較 ===
# 用 AIC 比較「完整模型」和「精簡模型」，判斷是否放了太多變項。

# --- 精簡模型 ---
# 移除 Ch03 篩選中 crude RR 不顯著或效果量小的共病，以及樓層。
# 保留：核心暴露因子（shower_use, hydrotherapy_use）
#       + 理論上最重要的調整因子（age, immunosuppressed, functional_score）
formula_reduced = (
    "infected ~ shower_use + hydrotherapy_use + age + "
    "immunosuppressed + functional_score"
)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model_reduced = smf.glm(
        formula_reduced, data=df,
        family=sm.families.Poisson(),
    ).fit(cov_type="HC0")

print(f"完整模型 AIC = {model_poisson.aic:.1f}")
print(f"精簡模型 AIC = {model_reduced.aic:.1f}")
print()

# --- 白話解讀 ---
if model_reduced.aic < model_poisson.aic:
    print("📉 精簡模型 AIC 較小 → 精簡模型在「解釋力 vs 複雜度」之間取得更好平衡")
else:
    print("📈 完整模型 AIC 較小 → 多放的變項確實有貢獻")
```

> 🍽️ **點菜比喻**：AIC 就像在餐廳點菜。菜太多（變項太多）→ 吃不完浪費錢（overfitting）。菜太少（變項太少）→ 餓肚子（underfitting）。AIC 幫你找到「剛好吃飽又不浪費」的平衡點。AIC 越小越好。

```{admonition} AIC 只能比同一 family 的模型
:class: warning

Modified Poisson（Poisson family）和 Logistic Regression（Binomial family）的 AIC 不能直接比較，因為 likelihood 的計算基礎不同。所以上面只比較了兩個 Poisson 模型之間的 AIC。
```

### 變項怎麼選？三種策略比較

上面我們只比了「完整 vs 精簡」兩個模型。但實務上，到底要放哪些變項進模型？有三種常見策略：

| 策略 | 做法 | 優點 | 缺點 |
|------|------|------|------|
| **Forward（往前加）** | 從空模型開始，每次加入一個讓 AIC 下降最多的變項 | 簡單直覺 | 容易漏掉聯合效應；加入順序影響結果 |
| **Backward（往後刪）** | 從完整模型開始，每次移除一個對 AIC 影響最小的變項 | 能看到所有變項的聯合效應 | 需要夠多樣本才能放所有變項 |
| **Change-in-estimate（效應改變法）** | 逐一移除候選干擾因子，看暴露因子的 RR 是否改變 ≥ 10% | **流行病學金標準**——以「是否干擾暴露效應」為判斷依據 | 需要先定義「暴露因子」 |

```{tip}
**流行病學推薦用 change-in-estimate**，而不是 stepwise（自動選變項）。原因很簡單：我們做多變項分析的目的是**正確估計暴露因子的效應**，不是做預測。一個變項即使 p-value 不顯著，只要它是干擾因子（移除後讓 RR 改變 ≥ 10%），就應該留在模型裡。

Stepwise 以 p-value 為標準，可能會移除「不顯著但確實在干擾的變項」，導致暴露因子的 RR 被扭曲。
```

下面用 Python 實作 **change-in-estimate 法**，看哪些候選干擾因子真正影響了 shower_use 和 hydrotherapy_use 的 RR：

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：10% 法則——change-in-estimate 挑變項</div>
  <div class="youtube-lite" data-id="OQLEUHJQv7s">
    <img src="https://img.youtube.com/vi/OQLEUHJQv7s/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

```python
# === Step 7b: Change-in-Estimate 變項選擇 ===
# 流行病學標準做法：逐一移除候選干擾因子，
# 看暴露因子（shower_use, hydrotherapy_use）的 adjusted RR 改變多少。
# 改變 ≥ 10% → 該變項是干擾因子，必須留在模型裡。

# --- 完整模型的暴露因子 RR（基準值）---
full_rr = {
    var: np.exp(model_poisson.params[var])
    for var in ["shower_use", "hydrotherapy_use"]
}
print("完整模型的暴露因子 RR（基準）：")
for var, rr in full_rr.items():
    print(f"  {var}: {rr:.3f}")
print()

# --- 候選干擾因子：逐一移除測試 ---
confounders = [
    "age", "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed", "functional_score", "C(floor)",
]

cie_results = []
for drop_var in confounders:
    # 建立移除一個變項的公式
    keep = [c for c in confounders if c != drop_var]
    formula_test = "infected ~ shower_use + hydrotherapy_use + " + " + ".join(keep)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = smf.glm(formula_test, data=df, family=sm.families.Poisson()).fit(
            cov_type="HC0", disp=0
        )

    for exposure in ["shower_use", "hydrotherapy_use"]:
        rr_without = np.exp(m.params[exposure])
        pct_change = (rr_without - full_rr[exposure]) / full_rr[exposure] * 100
        cie_results.append({
            "移除的變項": drop_var,
            "暴露因子": exposure,
            "移除後 RR": round(rr_without, 3),
            "RR 改變%": f"{pct_change:+.1f}%",
            "是否干擾": "✓ 干擾" if abs(pct_change) >= 10 else "",
        })

cie_df = pd.DataFrame(cie_results)
print("=== Change-in-Estimate 分析 ===")
print("（移除某變項後，暴露因子的 RR 改變 ≥ 10% → 該變項是干擾因子）\n")
print(cie_df.to_string(index=False))
```

> 📋 **怎麼用這張表？** 看「RR 改變%」欄位。如果移除某個變項後，shower_use 或 hydrotherapy_use 的 RR 改變了 10% 以上，就表示那個變項是干擾因子，必須留在模型裡——即使它自己的 p-value 不顯著。

---

## 解讀重點

| 結果 | 意義 |
|------|------|
| Adjusted RR > 1 且 p < 0.05 | 控制其他因子後，仍為獨立危險因子 |
| Crude RR ≫ Adjusted RR | 粗 RR 被干擾作用膨脹（與 Ch05 MH 結論一致） |
| Adjusted RR ≈ 1 | 控制後效應消失，原來的關聯可能是假的 |
| Adjusted OR > Adjusted RR | OR 高估效應（侵襲率高的必然結果） |
| AIC 較小 | 模型在解釋力與複雜度間取得較好平衡 |

## 常見錯誤

1. **在世代研究中只報 OR**：侵襲率高時 OR ≠ RR。應該用 Modified Poisson 算 RR，或至少同時報告兩者讓讀者知道差異
2. **OR 當 RR 用**：對主管說「OR = 3.5 代表風險 3.5 倍」——在高侵襲率下是錯的。要明確區分「勝算幾倍」和「風險幾倍」
3. **放太多變項**：280 筆資料放 15+ 變項 → 過度擬合。經驗法則：每個 predictor 至少需要 10-15 個 events
4. **忽略多重共線性**：高度相關的變項不要同時放入（例如 functional_status 和 age 可能高度相關）
5. **自動選變項**：stepwise 不推薦 → 用流行病學知識和 DAG 選擇
6. **不報 CI**：只報 p-value 不夠。CI 告訴你效應的精確度和臨床意義

## 下一步

多變項分析回答了「哪些因子獨立影響感染風險」。但主管接著問：「下週還會有多少新個案？」→ Ch07 時間序列預測。

## 練習本

- 課堂筆記：{ref}`06_logistic_regression.ipynb`
- 作業版：[`06_logistic_regression_exercise.ipynb`](exercises/06_logistic_regression_exercise.ipynb)
- 解答版（教師版）：[`06_logistic_regression_solution.ipynb`](solutions/06_logistic_regression_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/06_logistic_regression_solution.ipynb>)
