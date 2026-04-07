# 03 暴露與疾病的關聯：2×2 表與推論統計

## 情境

松柏護理之家退伍軍人症群聚事件，疫調團隊已經完成資料清理和視覺化（Ch02）。現在主管問你：**「使用淋浴設備的人，感染風險是不是比較高？有沒有統計上的證據？」**

你正要回答「淋浴組侵襲率比較高」，資深疫調前輩打斷你：

> 「等等——你說的是**描述**還是**推論**？光是『看起來比較高』不夠，你怎麼用統計來排除這只是隨機誤差？而且，你現在手上的資料，到底適合算 RR 還是 OR？」

這一章就是要回答這些問題。

## 你將學到

- 描述統計與推論統計的差異
- 流行病學研究設計（世代研究 vs. 病例對照研究）如何決定效應量指標
- 從 line list 建立 2×2 列聯表
- 計算風險比（Risk Ratio, RR）及其意義
- 計算勝算比（Odds Ratio, OR）及 RR 與 OR 的差異
- 估計 RR 和 OR 的 95% 信賴區間（CI）
- 使用卡方檢定和 Fisher 精確檢定判斷統計顯著性
- 同時比較多個危險因子，用森林圖（forest plot）視覺化

---

## 描述統計 vs. 推論統計

Ch02 我們用**描述統計**（平均值、次數分布、圖表）整理了資料的樣貌。但主管問的問題不是「資料長什麼樣」，而是「淋浴使用和感染**有沒有關聯**」。

這就需要**推論統計（inferential statistics）**——用樣本資料去推論：觀察到的差異是真實的關聯，還是純粹**隨機誤差（chance）**造成的？

| 類型 | 目的 | 範例 |
|------|------|------|
| 描述統計 | 摘要資料的特徵 | 平均年齡 72 歲、侵襲率 43.2%、流行曲線 |
| 推論統計 | 從樣本推論母體、檢定假說 | RR 的 95% CI、卡方檢定 p-value |

### 核心術語

- **虛無假設（H₀）**：淋浴使用與感染互相獨立（無關聯）
- **對立假設（H₁）**：淋浴使用與感染有關聯
- **p-value**：假設 H₀ 為真時，觀察到現有數據（或更極端數據）的機率。p 越小，越有理由拒絕 H₀
- **信賴區間（CI）**：效應量的合理範圍。若 95% CI 不包含「無效果值」（RR=1 或 OR=1），則在 α=0.05 水準下有統計顯著性

---

## 流行病學研究設計速覽

你能算什麼指標，取決於你的**研究設計**。以下用日常比喻來解釋四種常見設計：

```{figure} images/study_designs.svg
:name: fig-study-designs
:alt: 四種流行病學研究設計：世代研究（跟拍紀錄片）、病例對照（偵探辦案）、巢式病例對照（翻監視器錄影帶）、配對病例對照（雙胞胎實驗）
:width: 100%
```

### ❶ 世代研究（Cohort Study）——跟拍紀錄片

想像你是紀錄片導演：先挑好兩組人（有淋雨的 vs. 沒淋雨的），然後一路跟拍，看誰後來感冒了。

- **依暴露狀態分組**，往前追蹤疾病結果
- 你知道**全部**暴露者和未暴露者各有多少人（有完整分母）
- 可以直接計算**風險（risk = 得病人數 ÷ 該組全部人數）**和 **RR（風險比）**

> 🎬 本次護理之家調查 = **回溯性世代研究**（retrospective cohort）：280 位住民全部納入，暴露和結果都已知 → 可以直接算 **RR**。

### ❷ 病例對照研究（Case-Control Study）——偵探辦案

想像你是偵探：先找到「受害者」（已經生病的人，叫病例 case），再另外選一群「沒受害的人」（沒生病的人，叫對照 control），回頭問他們以前有沒有接觸過嫌疑人（暴露）。

- **依疾病狀態分組**（先找病例，再選對照），回溯暴露史
- 對照組人數是研究者**自己決定**的（例如 1:1 或 1:4 配對），不代表真實族群中的發病率
- 因為分母是人為設定的，**無法算 risk → 只能算 OR（勝算比）**

> 🕵️ 什麼時候用？罕見疾病（如 CJD、Ebola）或全國性大規模調查（如疫苗效益 VE 研究）——去追蹤幾百萬人太貴太慢，不如挑幾百個病例來研究。

### ❸ 巢式病例對照研究（Nested Case-Control Study）——翻監視器錄影帶

你的社區已經在做世代研究（像裝了監視器全程錄影），但要把每個人的血液都拿去做昂貴的生物標記檢驗太花錢了。怎麼辦？

- 等到有人發病後，**從世代裡挑出**這些病例
- 再從**同一世代**中挑配對的對照組，回頭做檢驗
- 兼具世代的**代表性**和病例對照的**效率**

> 🏠 常見於大型前瞻性世代（如 Nurses' Health Study）中的生物標記子研究。

### ❹ 配對病例對照研究（Matched Case-Control Study）——雙胞胎實驗

找到一個 70 歲的男性病例，就特地去找一個**年齡、性別相近但沒生病**的人配成一對。這樣年齡和性別的影響就「抵消」了。

- 配對變項（如年齡、性別）在設計階段就被控制住了
- 分析時必須用**條件式邏輯斯迴歸（conditional logistic regression）**，不能用普通卡方檢定
- 配對比例可以是 1:1、1:2、甚至 1:4（對照越多，統計力越強）

> 👯 比喻：找一個「條件差不多的分身」，兩人唯一差別是有沒有暴露。

### 設計選擇快速對照表

| 研究設計 | 抽樣方式 | 可算指標 | 適用場景 | 比喻 |
|---------|---------|---------|---------|------|
| 世代研究 | 依暴露分組，追蹤結果 | **RR** | 群聚調查（全員資料）| 🎬 跟拍紀錄片 |
| 病例對照 | 依疾病分組，回溯暴露 | **OR** | 罕見疾病、大規模族群 | 🕵️ 偵探辦案 |
| 巢式病例對照 | 從世代中挑病例+對照 | **OR** | 大型世代中的子研究 | 🏠 翻監視器 |
| 配對病例對照 | 按配對變項 1:n 配對 | **OR**（條件式） | 需控制已知干擾因子 | 👯 雙胞胎實驗 |

---

## 核心概念

### 2×2 列聯表

|  | 感染 | 未感染 | 合計 |
|--|------|--------|------|
| **暴露** | a | b | a+b |
| **未暴露** | c | d | c+d |

### Risk Ratio（風險比）——秤重比大小 ⚖️

$$RR = \frac{a / (a+b)}{c / (c+d)}$$

**白話文**：RR = 2 的意思是「有暴露的人，得病風險是沒暴露的人的 **2 倍**」。就像把兩組的風險放到天平上，看暴露組是未暴露組的幾倍重。

- RR = 1：暴露與疾病無關（兩邊一樣重）
- RR > 1：暴露可能增加風險（暴露組那邊比較重）
- RR < 1：暴露可能是保護因子（暴露組那邊比較輕，例如疫苗）

### Odds Ratio（勝算比）——賭場賠率 🎰

**勝算（odds）** 和**風險（risk）** 不同：

- **風險 = p**：100 個人裡有 30 個生病 → 風險 = 30/100 = 0.3（除以**全部**）
- **勝算 = p / (1-p)**：30 個生病 vs. 70 個沒病 → 勝算 = 30/70 ≈ 0.43（生病 ÷ **沒生病**）

$$OR = \frac{a \times d}{b \times c}$$

**白話文**：OR = 3 的意思是「有暴露的人，得病的**勝算**是沒暴露的 3 倍」。注意這裡說的是「勝算」不是「風險」——就像賭場說賠率 3:1，不是說你有 300% 的機率贏。

```{figure} images/or_rr_relationship.svg
:name: fig-or-rr-relationship
:alt: RR 和 OR 的關係：罕見疾病時兩者近似，侵襲率越高 OR 偏離 RR 越多
:width: 100%
```

### RR 和 OR：什麼時候一樣，什麼時候不一樣？

這是新手最容易搞混的地方，一次講清楚：

#### 1️⃣ 罕見疾病時 OR ≈ RR（10% 法則）

**數學原因**：Risk = p，Odds = p/(1−p)。當 p 很小（例如 &lt; 10%），(1−p) ≈ 1，所以 Odds ≈ p ≈ Risk。兩組的 Odds 都 ≈ Risk，因此 OR ≈ RR。

> 🍬 比喻：一袋 100 顆糖果裡有 3 顆酸的。「抽到酸的機率（risk）」= 3/100 = 3%。「抽到酸的勝算（odds）」= 3/97 ≈ 3.1%。差別只有 0.1%，幾乎一樣！但如果 50 顆是酸的，risk = 50% 而 odds = 50/50 = 100%——差一倍，完全不同。

#### 2️⃣ 侵襲率高時 OR 系統性大於 RR

當疾病常見（如本資料集侵襲率 ~43%），暴露組的 (1−p₁) 比未暴露組的 (1−p₀) 更小，使得暴露組的 odds 被放大得更多 → OR 被「撐大」了。

具體數字：假設 Risk₁ = 55%、Risk₀ = 30%（RR = 1.83），但 Odds₁ = 55/45 = 1.22、Odds₀ = 30/70 = 0.43 → OR = 1.22/0.43 = **2.86**，比 RR 高了 56%！

> ⚠️ **實務含義**：本案侵襲率 43%，如果你拿 OR 來說「風險是幾倍」，會嚴重高估。報告時應該寫 **RR**，不要寫 OR。

#### 3️⃣ OR 是邏輯斯迴歸的原生輸出

邏輯斯迴歸模型的數學形式是 log(odds) = β₀ + β₁×暴露 + ...，所以模型直接給你的是 **log-odds 的差**，exp(β₁) = OR。

不管你的資料是世代研究還是病例對照研究，只要跑邏輯斯迴歸，**跑出來的就是 OR**。Ch06 會教你怎麼做。

### 疫苗效益 VE 怎麼估？RR 和 OR 都能用嗎？

**疫苗效益（Vaccine Effectiveness, VE）** 衡量疫苗在真實世界中減少多少疾病風險：

| 研究設計 | VE 公式 | 常用場景 |
|---------|---------|---------|
| 世代研究 | VE = 1 − RR | 臨床試驗（RCT）、群聚調查 |
| 病例對照 | VE = 1 − OR | 大規模上市後監測（test-negative design） |

- **世代研究**：直接比較打疫苗 vs. 沒打疫苗的發病率 → VE = 1 − RR。例如 RR = 0.2 → VE = 80%（疫苗減少 80% 的風險）
- **病例對照研究**：先找生病的（病例）和沒生病的（對照），比較兩組的疫苗接種率 → VE = 1 − OR。COVID-19 疫苗很多效益數據就是用 **test-negative case-control design** 算的

> **什麼時候選哪種？**
> - 如果你是做臨床試驗或群聚調查（有全員資料） → **世代研究 → RR → VE = 1−RR**
> - 如果你要做全國性上市後監測（追蹤幾百萬人太貴） → **病例對照 → OR → VE = 1−OR**
> - 當疾病罕見時（大部分疫苗可預防疾病），OR ≈ RR，兩個 VE 公式結果差不多

### 95% 信賴區間

**RR 的 CI**（Katz method）：

$$\ln(RR) \pm 1.96 \times SE(\ln RR)$$

其中 $SE(\ln RR) = \sqrt{\frac{1}{a} - \frac{1}{a+b} + \frac{1}{c} - \frac{1}{c+d}}$

**OR 的 CI**（Woolf method）：

$$\ln(OR) \pm 1.96 \times SE(\ln OR)$$

其中 $SE(\ln OR) = \sqrt{\frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}}$

若 95% CI 不包含 1，則效應量在 α=0.05 水準下有統計顯著性。

### 卡方檢定與 Fisher 精確檢定

- **卡方檢定**：比較觀察次數與期望次數（H₀ 下的預期），適用於期望值 ≥ 5 的情況
- **Fisher 精確檢定**：直接計算在 H₀ 下觀察到當前或更極端結果的確切機率，適用於小樣本（期望值 < 5）

---

## Step 1: 資料準備

```python
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact
from epi_learning.metrics import risk_ratio, odds_ratio

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# 建立「是否感染」的二元欄位 (0/1)
# clinical_severity == "not_ill" 表示沒有症狀也沒有感染，其餘都算感染
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

print(f"全體：{len(df)} 人，感染：{df['infected'].sum()} 人")
print(f"整體侵襲率：{df['infected'].mean():.1%}")
```

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：2×2 列聯表——把疫調資料變成四格表</div>
  <div class="youtube-lite" data-id="MrBUJ3iTyaw">
    <img src="https://img.youtube.com/vi/MrBUJ3iTyaw/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

## Step 2: 建立 2×2 表（淋浴 × 感染）

我們已有 280 位住民和 `infected` 欄位。現在要整理成 **2×2 列聯表**——流行病學關聯分析的基本資料結構。下方圖示說明每個格子如何對應公式。

```{figure} images/two_by_two_anatomy.svg
:name: fig-two-by-two-anatomy
:alt: 2×2 列聯表的 a, b, c, d 格子對應圖，顯示每個格子如何用於計算 RR 和 OR
:width: 100%
```

```python
# pd.crosstab() 的第一個參數 → 列（rows），第二個 → 欄（columns）
# margins=True 自動加上小計列和小計欄
ct_shower = pd.crosstab(
    df["shower_use"], df["infected"],
    margins=True, margins_name="合計",
)
# 重新命名，讓輸出更好讀（原始值 0/1 不直觀）
ct_shower.index = ["未使用淋浴", "使用淋浴", "合計"]
ct_shower.columns = ["未感染", "感染", "合計"]
print(ct_shower)

# ── 提取 2×2 表的四個格子（參考上方圖示）──
# crosstab 的列順序取決於原始值排序（0 在 1 前面）
# 重新命名後，我們用中文標籤來提取，就不用記哪個是 0、哪個是 1
a = int(ct_shower.loc["使用淋浴", "感染"])        # a = 暴露＋感染
b = int(ct_shower.loc["使用淋浴", "未感染"])      # b = 暴露＋未感染
c = int(ct_shower.loc["未使用淋浴", "感染"])      # c = 未暴露＋感染
d = int(ct_shower.loc["未使用淋浴", "未感染"])    # d = 未暴露＋未感染

# 分別計算兩組的侵襲率（attack rate）
print(f"\n暴露組（使用淋浴）侵襲率: {a/(a+b):.1%}")
print(f"未暴露組（未使用淋浴）侵襲率: {c/(c+d):.1%}")
```

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：風險比 RR——暴露到底有沒有增加風險？</div>
  <div class="youtube-lite" data-id="wUOt40SNZvA">
    <img src="https://img.youtube.com/vi/wUOt40SNZvA/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

## Step 3: 計算 Risk Ratio（風險比）

```python
rr = risk_ratio(a, a + b, c, c + d)
print(f"淋浴使用 → 感染的 RR = {rr:.3f}")
print(f"  解讀：使用淋浴者的感染風險是未使用者的 {rr:.1f} 倍")
print(f"  RR = 1 → 無關聯 | RR > 1 → 暴露可能增加風險 | RR < 1 → 可能是保護因子")
```

> **注意**：RR > 1 代表有「關聯」，不代表有「因果」。可能有干擾因子——Ch05 會處理。

---

剛算出 RR，但論文和報告裡也常看到 OR。差別在哪？**風險（risk）是機率，勝算（odds）是比值**——下圖說明。

```{figure} images/rr_vs_or_intuition.svg
:name: fig-rr-vs-or-intuition
:alt: Risk vs Odds 直覺圖：10 位住民中 3 位感染，Risk = 3/10，Odds = 3/7；世代研究用 RR，病例對照用 OR
:width: 100%
```

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：勝算比 OR——跟 RR 到底差在哪？</div>
  <div class="youtube-lite" data-id="tOloIGqUFvs">
    <img src="https://img.youtube.com/vi/tOloIGqUFvs/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

## Step 4: 計算 Odds Ratio（勝算比）

```python
or_val = odds_ratio(a, b, c, d)
print(f"淋浴使用 → 感染的 OR = {or_val:.3f}")
print(f"  （相比 RR = {rr:.3f}）")
print(f"\n本資料集侵襲率 = {df['infected'].mean():.1%}（非罕見疾病）")
print(f"→ OR ({or_val:.3f}) 大於 RR ({rr:.3f})，這是預期的")
print(f"→ 疾病罕見時 OR ≈ RR；侵襲率越高，OR 偏離 RR 越多")
print(f"\n⚠️ 本案侵襲率 ~43%，不能拿 OR 來說「風險是幾倍」！")
print(f"   正確寫法：「淋浴使用者的感染風險是未使用者的 {rr:.1f} 倍（RR）」")
print(f"   錯誤寫法：「淋浴使用者的感染風險是未使用者的 {or_val:.1f} 倍（OR）」← 高估了！")
```

> **RR vs OR 的選擇**：本案是世代研究（280 人全員納入），所以報告效應量用 **RR**。我們額外算 OR 是因為：(1) 練習兩者的差異，(2) 為 Ch06 邏輯斯迴歸（原生輸出 = OR）做準備。

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：95% 信賴區間——為什麼要先取 log 再 exp 回來？</div>
  <div class="youtube-lite" data-id="Z_eYSHtyHxM">
    <img src="https://img.youtube.com/vi/Z_eYSHtyHxM/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

## Step 5: 95% 信賴區間（RR 和 OR）

CI 是新手最容易「看到就頭暈」的部分。關鍵直覺：RR/OR 的尺度是**不對稱的**（0 到無限大），不能直接加減誤差範圍。我們先 **log 轉換**到對稱尺度，做完再 **exp 轉回**。下圖用三個步驟說明：

```{figure} images/ci_log_transform.svg
:name: fig-ci-log-transform
:alt: 為什麼算 CI 要先取 log？三步驟圖解：原始尺度（不對稱）→ log 尺度（對稱，可用常態分布）→ exp 轉回
:width: 100%
```

```python
# ── RR 的 95% CI：Katz method ──

# (a) 取自然對數：把 RR 從不對稱尺度 (0, ∞) 轉到對稱尺度 (-∞, +∞)
ln_rr = np.log(rr)

# (b) 計算標準誤（SE）：衡量 ln(RR) 估計值的精準度
#     公式來自 Katz（1978），利用 2×2 表的四格推導
se_ln_rr = np.sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))

# (c) 在 log 尺度上 ±1.96 × SE（1.96 是常態分布 95% 的 z 值）
# (d) 用 exp() 轉回原始尺度 → 得到 CI 的上下界
ci_rr_lo = np.exp(ln_rr - 1.96 * se_ln_rr)
ci_rr_hi = np.exp(ln_rr + 1.96 * se_ln_rr)

# ── OR 的 95% CI：Woolf method ──
# 原理相同，只是 SE 的公式不同（直接用 a, b, c, d 的倒數和）
ln_or = np.log(or_val)
se_ln_or = np.sqrt(1/a + 1/b + 1/c + 1/d)
ci_or_lo = np.exp(ln_or - 1.96 * se_ln_or)
ci_or_hi = np.exp(ln_or + 1.96 * se_ln_or)

print("=== 95% 信賴區間比較 ===")
print(f"RR = {rr:.3f} (95% CI: {ci_rr_lo:.3f} – {ci_rr_hi:.3f})")
print(f"OR = {or_val:.3f} (95% CI: {ci_or_lo:.3f} – {ci_or_hi:.3f})")
```

> **解讀**：如果你把這個調查重複做 100 次，大約 95 次算出的 CI 會包含真正的 RR/OR。CI 不包含 1 = 在 α=0.05 下有統計顯著性，等同於 p < 0.05。

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：卡方檢定——觀察值 vs 期望值的擂台賽</div>
  <div class="youtube-lite" data-id="qv3j0CSfHT0">
    <img src="https://img.youtube.com/vi/qv3j0CSfHT0/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

## Step 6: 卡方檢定

卡方檢定的核心邏輯：如果暴露和感染真的「無關」（H₀ 為真），每個格子應該觀察到多少人？實際數字離這個預期有多遠？

```{figure} images/chi_square_intuition.svg
:name: fig-chi-square-intuition
:alt: 卡方檢定直覺圖：觀察值與期望值的比較，差距越大 → χ² 越大 → p 越小
:width: 100%
```

```python
# H₀: 淋浴使用與感染互相獨立（無關聯）
contingency = [[a, b], [c, d]]
chi2, p, dof, expected = chi2_contingency(contingency)

print(f"卡方統計量 = {chi2:.3f}")
print(f"自由度 = {dof}")
print(f"p-value = {p:.4f}")
print(f"\n期望值表（H₀ 為真時的預期次數）：")
print(pd.DataFrame(
    expected.round(1),
    index=["使用淋浴", "未使用淋浴"],
    columns=["感染", "未感染"],
))

min_expected = expected.min()
print(f"\n最小期望值 = {min_expected:.1f}", end="")
if min_expected >= 5:
    print(" → 滿足卡方檢定前提")
else:
    print(" → < 5，建議改用 Fisher 精確檢定")
```

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：Fisher 精確檢定——小樣本的救星</div>
  <div class="youtube-lite" data-id="x8n7wUWtfz0">
    <img src="https://img.youtube.com/vi/x8n7wUWtfz0/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

## Step 7: Fisher 精確檢定

```python
oddsr_fisher, p_fisher = fisher_exact(contingency)
print(f"Fisher 精確檢定:")
print(f"  OR = {oddsr_fisher:.3f}")
print(f"  p-value = {p_fisher:.4f}")
print(f"\n卡方檢定 p = {p:.4f} vs Fisher p = {p_fisher:.4f}")
print("（此例樣本夠大，兩種檢定結果相近；小樣本時差異會更明顯）")
```

> Fisher 精確檢定不依賴大樣本近似，在期望值 < 5 或總樣本數 < 30 時更為可靠。

## Step 8: 第二個暴露因子 — 水療使用

用同一套分析流程處理第二個暴露因子。程式碼和 Steps 2–6 完全相同，只是把 `shower_use` 換成 `hydrotherapy_use`。Step 9 會用迴圈自動化這個過程，不用再手動複製貼上。

```python
# 和 Step 2–6 完全相同的流程，換成水療暴露
ct_hydro = pd.crosstab(df["hydrotherapy_use"], df["infected"])
a2, b2 = int(ct_hydro.loc[1, 1]), int(ct_hydro.loc[1, 0])  # 暴露+感染, 暴露+未感染
c2, d2 = int(ct_hydro.loc[0, 1]), int(ct_hydro.loc[0, 0])  # 未暴露+感染, 未暴露+未感染

# 效應量
rr2 = risk_ratio(a2, a2 + b2, c2, c2 + d2)
or2 = odds_ratio(a2, b2, c2, d2)
chi2_2, p2, _, _ = chi2_contingency([[a2, b2], [c2, d2]])

# RR CI（Katz method，同 Step 5）
ln_rr2 = np.log(rr2)
se_rr2 = np.sqrt(1/a2 - 1/(a2+b2) + 1/c2 - 1/(c2+d2))
ci_rr2_lo = np.exp(ln_rr2 - 1.96 * se_rr2)
ci_rr2_hi = np.exp(ln_rr2 + 1.96 * se_rr2)

# OR CI（Woolf method，同 Step 5）
ln_or2 = np.log(or2)
se_or2 = np.sqrt(1/a2 + 1/b2 + 1/c2 + 1/d2)
ci_or2_lo = np.exp(ln_or2 - 1.96 * se_or2)
ci_or2_hi = np.exp(ln_or2 + 1.96 * se_or2)

print("水療使用 → 感染")
print(f"  RR = {rr2:.3f} (95% CI: {ci_rr2_lo:.3f} – {ci_rr2_hi:.3f})")
print(f"  OR = {or2:.3f} (95% CI: {ci_or2_lo:.3f} – {ci_or2_hi:.3f})")
print(f"  卡方 p-value = {p2:.4f}")
```

## Step 9: 多因子粗效應量彙整表 + 森林圖

實際疫調中不會只看一兩個因子。下面的迴圈把 **Steps 2–6 系統性地套用到所有候選暴露**，再用森林圖一目瞭然地比較。

```python
import matplotlib.pyplot as plt

# 列出所有要檢驗的暴露因子（二元 0/1 變數）
factors = [
    "shower_use", "hydrotherapy_use",
    "comorbidity_chf", "comorbidity_dm", "comorbidity_cancer",
    "comorbidity_copd", "immunosuppressed",
]
# 把「曾經吸菸」轉成二元變數
df["ever_smoker"] = (df["smoking_history"] != "never").astype(int)
factors.append("ever_smoker")

# ── 迴圈：對每個因子重複 Steps 2–6 ──
# 每一輪做 5 件事：(a) 建 2×2 表 → (b) 算 RR/OR → (c) 算 CI → (d) 卡方檢定 → (e) 存結果
results = []
for factor in factors:
    # (a) 建立 2×2 表，提取 a, b, c, d
    ct = pd.crosstab(df[factor], df["infected"])
    a_i = int(ct.loc[1, 1])   # 暴露＋感染
    b_i = int(ct.loc[1, 0])   # 暴露＋未感染
    c_i = int(ct.loc[0, 1])   # 未暴露＋感染
    d_i = int(ct.loc[0, 0])   # 未暴露＋未感染

    # (b) 效應量：RR 和 OR
    rr_i = risk_ratio(a_i, a_i + b_i, c_i, c_i + d_i)
    or_i = odds_ratio(a_i, b_i, c_i, d_i)

    # (c) RR 的 95% CI（Katz method，同 Step 5）
    ln_rr_i = np.log(rr_i)
    se_i = np.sqrt(1/a_i - 1/(a_i+b_i) + 1/c_i - 1/(c_i+d_i))
    ci_lo = np.exp(ln_rr_i - 1.96 * se_i)
    ci_hi = np.exp(ln_rr_i + 1.96 * se_i)

    # (d) 卡方檢定
    chi2_i, p_i, _, _ = chi2_contingency([[a_i, b_i], [c_i, d_i]])

    # (e) 把這個因子的結果存起來
    results.append({
        "factor": factor,
        "RR": round(rr_i, 3),
        "CI_lower": round(ci_lo, 3),
        "CI_upper": round(ci_hi, 3),
        "OR": round(or_i, 3),
        "p-value": round(p_i, 4),
    })

# 彙整成表格，按 RR 由大到小排序（最可疑的因子排最前面）
rr_table = pd.DataFrame(results).sort_values("RR", ascending=False)
display_df = rr_table.copy()
display_df["95% CI"] = display_df.apply(
    lambda r: f"{r['CI_lower']:.3f}–{r['CI_upper']:.3f}", axis=1
)
print("=== 多因子粗效應量彙整表 ===")
print(display_df[["factor", "RR", "95% CI", "OR", "p-value"]].to_string(index=False))
```

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：森林圖——一眼看穿誰是最大嫌疑犯</div>
  <div class="youtube-lite" data-id="K8dMlS5lr3A">
    <img src="https://img.youtube.com/vi/K8dMlS5lr3A/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

### 森林圖（Forest Plot）

**森林圖**是流行病學和實證醫學中最常見的圖表之一，常用於系統性回顧（systematic review）和統合分析（meta-analysis），但在群聚調查中也非常實用——可以**一眼比較多個暴露因子的效應量大小和統計顯著性**。

怎麼看森林圖：
- **圓點（●）**：點估計值（本例為 RR）
- **水平線段（─）**：95% 信賴區間
- **虛線（RR = 1）**：無效果線。CI 與虛線交叉 = 不顯著；CI 完全在虛線右側 = 暴露顯著增加風險

```{figure} images/forest_plot_reading_guide.svg
:name: fig-forest-plot-reading-guide
:alt: 森林圖閱讀指南：圓點表示點估計值，水平線段表示 95% CI，虛線表示 RR=1 無效果線
:width: 100%
```

```python
import pathlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# -- CJK font setup (避免中文標籤顯示為方框 □□□) --
for _font_dir in map(pathlib.Path, ["/usr/share/fonts", "/usr/local/share/fonts"]):
    if _font_dir.exists():
        for _fp in sorted(_font_dir.rglob("*")):
            if _fp.suffix.lower() in {".ttf", ".ttc", ".otf"} and (
                "CJK" in _fp.name or "WenQuanYi" in _fp.name or "wqy" in _fp.name
            ):
                try:
                    fm.fontManager.addfont(str(_fp))
                except Exception:
                    pass

plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False

```python
fig, ax = plt.subplots(figsize=(8, 5))
rr_sorted = rr_table.reset_index(drop=True)
y_pos = range(len(rr_sorted))
ax.errorbar(
    rr_sorted["RR"], y_pos,
    xerr=[rr_sorted["RR"] - rr_sorted["CI_lower"],
          rr_sorted["CI_upper"] - rr_sorted["RR"]],
    fmt="o", color="#D97757", ecolor="#6B6B6B", capsize=4, markersize=7,
)
ax.axvline(x=1, color="#6B6B6B", linestyle="--", alpha=0.7, label="RR = 1（無效果）")
ax.set_yticks(list(y_pos))
ax.set_yticklabels(rr_sorted["factor"])
ax.set_xlabel("Risk Ratio (95% CI)")
ax.set_title("各因子粗風險比（Forest Plot）")
ax.legend(loc="lower right")
ax.invert_yaxis()
plt.tight_layout()
plt.show()
```

---

## 解讀重點

| 情境 | 指標 | 解讀 | 白話文 |
|------|------|------|--------|
| RR > 1 且 CI 不含 1 | RR | 暴露可能增加感染風險 | 有暴露的人比較容易得病，而且不太可能是巧合 |
| RR ≈ 1 或 CI 含 1 | RR | 暴露與感染無顯著關聯 | 有沒有暴露，得病的機會差不多 |
| RR < 1 且 CI 不含 1 | RR | 暴露可能是保護因子 | 像疫苗——暴露反而讓你比較不容易得病 |
| p < 0.05 | p-value | 統計顯著（但不代表因果） | 「不太像巧合」≠「一定是它害的」 |
| 世代研究（有完整分母） | 用 **RR** | 可以直接算風險 | 你知道全部人 → 報 RR |
| 病例對照研究（無完整分母） | 用 **OR** | 只能算勝算 | 對照組是你挑的 → 只能報 OR |
| 邏輯斯迴歸輸出 | **OR** | 模型原生 = log-odds | 跑迴歸就是 OR，不管哪種研究設計 |
| 罕見疾病（侵襲率 < 10%） | OR ≈ RR | 兩者可互換 | 糖果袋裡酸的很少 → 風險 ≈ 勝算 |
| 侵襲率高（> 10%） | OR > RR | OR 高估風險倍數 | 本案 43% → 只能用 RR 報風險 |
| 疫苗效益（世代） | VE = 1−RR | 直接從發病率算 | RR=0.2 → VE=80% |
| 疫苗效益（病例對照） | VE = 1−OR | 從勝算比算 | 罕見疾病時 ≈ 1−RR |
| 多因子掃描 | 粗 RR 彙整表 | 快速篩嫌疑因子 | 但需注意多重比較和干擾因子 |

## 常見錯誤

1. **只看 p-value**：p < 0.05 不代表效果大，要同時看 RR/OR 的大小和 CI 的寬度。p = 0.001 但 RR = 1.01 → 統計顯著但臨床無意義
2. **忽略干擾因子**：粗 RR 可能受年齡、共病等干擾 → 需要 Ch05 分層分析
3. **混淆 RR 和 OR**：世代研究報 RR，病例對照報 OR。侵襲率 ~43% 時拿 OR 當「風險倍數」會嚴重高估！正確寫法：「RR = 1.8，風險是 1.8 倍」；錯誤寫法：「OR = 3.2，風險是 3.2 倍」
4. **拿 OR 說「風險是 X 倍」**：OR 衡量的是**勝算**倍數，不是風險倍數。只有疾病罕見時 OR ≈ RR 才能近似互換
5. **樣本數太小**：期望值 < 5 的格子應改用 Fisher 精確檢定
6. **把統計顯著等同因果**：有關聯 ≠ 有因果。還需考慮時序性、劑量反應、生物合理性（Hill's criteria）
7. **多重比較問題**：同時測 8 個因子，光靠機率就可能有 ~0.4 個偽陽性（α=0.05 時）
8. **世代研究跑邏輯斯迴歸卻直接報 OR**：邏輯斯迴歸原生輸出是 OR，但如果你的資料是世代研究且侵襲率高，應轉換為 RR（Ch06 會教方法）

## 下一步

粗 RR / OR 只是初步線索，就像偵探拿到了嫌疑人名單，但還不能定罪。

- 淋浴使用的 RR 看起來很高，但如果**能自主行走的住民同時淋浴使用率高又暴露機會多**，那 RR 可能被**干擾作用（confounding）**膨脹了——就像漢堡看起來很大，但可能是生菜撐出來的
- **Ch05** 會用**分層分析**和 **Mantel-Haenszel 法**把干擾因子「控制住」，得到調整後的 RR
- **Ch06** 會用**邏輯斯迴歸**同時調整多個因子，算出 adjusted OR（記得：迴歸的原生輸出是 OR，侵襲率高時要小心解讀）

從粗關聯（Ch03）→ 控制干擾（Ch05）→ 多變項模型（Ch06），這是流行病學分析的標準三部曲。同樣的框架也適用於疫苗效益研究——只是暴露變項換成「有無接種」，RR < 1 表示疫苗有保護力。

## 練習本

- 課堂筆記：{ref}`03_stats_basics.ipynb`
- 作業版：[`03_stats_exercise.ipynb`](exercises/03_stats_exercise.ipynb)
- 解答版（教師版）：[`03_stats_solution.ipynb`](solutions/03_stats_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/03_stats_solution.ipynb>)
