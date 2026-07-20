# 05 分層分析與干擾因子

## 情境

在 Ch03 中，我們發現淋浴使用者的感染風險比（RR）明顯大於 1。但資深疫調人員提出一個質疑：

> 「臥床住民幾乎不使用淋浴，而臥床住民本來活動範圍就小、暴露機會也少。你看到的高 RR，會不會只是因為**能走動的人同時也在用淋浴**？」

這就是**干擾作用（confounding）**的問題。想像一下：

> 🌧️ **穿雨衣的人比較容易感冒——所以穿雨衣會害你感冒？**
>
> 當然不是！是因為**下雨天**同時讓你穿雨衣（暴露）、也讓你容易感冒（結果）。「下雨天」就是那個藏在背後搞混你判斷的**干擾因子**。

在我們的護理之家案例中，「功能狀態」就是那個「下雨天」——它同時影響了住民會不會用淋浴、也影響了住民的感染風險。這一章教你如何找出干擾因子、用分層分析把它「控制」住，再用 Mantel-Haenszel 法得到調整後的 RR。

## 你將學到

- 什麼是干擾因子（confounder）及其三要件
- 如何用 DAG（有向無環圖）辨識干擾路徑
- 如何進行分層分析（stratified analysis）
- 各層 RR 的森林圖（forest plot）視覺化
- Mantel-Haenszel 加權 RR 及同質性檢定
- 如何解讀粗 RR vs. 調整後 RR（含量化判斷標準）

## 🔍 超白話特別篇：用「大腳丫的小孩比較會認字」看懂分層分析

> 「分層分析」「干擾因子」「Mantel-Haenszel」聽起來像三道咒語？別怕。這一段先不碰護理之家，改用一個**你一眼就知道哪裡怪怪的**小故事，把整套邏輯講到讓國中生也會拍桌大喊「原來如此」。看完再回頭看下面的 DAG 和森林圖，你會很有感覺。

### 一個聽起來超有道理、其實超級可疑的發現

假設有人跑去一所小學，量了每個小孩的**腳掌大小**，也測了他們**會不會認字**，結果算出來：

> **大腳丫的小孩，認字率 68%；小腳丫的小孩，認字率只有 32%。風險比 RR ≈ 2.1！**

照這個數字直接下結論的話，會變成——**「腳越大越會認字，想讓小孩聰明就多買大鞋？」** 你一定覺得哪裡怪怪的。沒錯，這個 RR 是**真的算出來的**，但這個**因果解讀是假的**。問題出在哪？

### 兇手藏在後面：其實是「年齡」在搞鬼

想一想：**10 歲的小孩，腳本來就比 6 歲的大，而且本來就比較會認字。** 也就是說，有一個東西**同時**讓小孩「腳變大」又「變得會認字」——那就是**年齡**。

- 不是腳大讓人會認字，而是**年齡大**讓人「腳大」＋「會認字」兩件事一起發生。
- 腳大小和認字之間，其實**沒有因果關係**，它們只是**都被年齡牽著走**，才看起來手牽手。

這個躲在背後、同時牽動暴露（腳大小）和結果（認字）、害我們誤判的傢伙，就叫**干擾因子（confounder）**。這裡的干擾因子就是**年齡**。

```{figure} images/confounding_shoe_size.svg
:name: fig-confounding-shoe-size
:alt: 大腳丫會認字的假象：全部混在一起看時大腳丫組認字率 68%、小腳丫組 32%（粗 RR≈2.1），但真兇是年齡；分年齡看時，6 歲組大小腳丫都 20%、10 歲組都 80%，腳大小其實毫無差別
:width: 100%

左上：全部混在一起看，大腳丫好像比較會認字（假象）；右上：真兇「年齡」同時牽動腳大小和認字；下排：**分年齡看**，同一個年齡裡腳大小根本沒差。
```

### 破案關鍵：分年齡「分開看」——這就是分層分析

既然懷疑年齡在搞鬼，那就**把年齡固定住**：不要把 6 歲和 10 歲混在一起算，而是**同一個年齡的小孩自己跟自己比**。

- **只看 6 歲的**：大腳丫認字率 20%，小腳丫也是 20%——**一模一樣！**
- **只看 10 歲的**：大腳丫認字率 80%，小腳丫也是 80%——**還是一樣！**

只要年齡一樣，腳大小**完全沒有差別**（每一層的 RR 都 = 1.0）。那個 2.1 的「假象」瞬間消失。

這個「**把大家依某個變項切成幾組（每組叫一個「層／stratum」），在每一組裡分開比較**」的做法，就是**分層分析（stratified analysis）**。這裡我們是**依年齡分層**。

### 為什麼一定要做這件事？（不做會怎樣）

因為**混在一起的「粗數字」會騙人**。如果不分層：

- 你會**冤枉好人**（以為是腳大小害的），又**放走真兇**（沒發現是年齡）。
- 換到真實疫調，就是：以為「淋浴」很危險而下令**全面停用淋浴**，結果白忙一場，因為真正的關鍵其實是「功能狀態」。**校正干擾，就是為了不要把力氣花錯地方、不要給錯防疫建議。**

### 怎麼把各層合成「一個」答案？Mantel-Haenszel 加權

分層之後，每一層各有一個 RR（這裡兩層都剛好是 1.0）。我們通常想要**一個**總結數字，這時用 **Mantel-Haenszel（MH）加權平均**把各層的 RR 依人數加權合起來，得到**校正後 RR（adjusted RR）**。

然後把兩個數字擺在一起比：

- **粗 RR = 2.1**（沒分年齡、被騙的版本）
- **校正後 RR = 1.0**（分年齡、講真話的版本）

兩者差了一大截 → 證明**年齡真的在干擾**。實務上有個好記的門檻：**粗 RR 和校正後 RR 相差 ≥ 10%，就認定有干擾**（change-in-estimate 法則）。

### 動手玩玩看：親手把這個干擾因子抓出來

```python
# 一份「腳大小 × 會不會認字」的造冊，依年齡分成兩層
# a=大腳丫且會認字, b=大腳丫不會認字, c=小腳丫且會認字, d=小腳丫不會認字
strata = {
    "6 歲組":  dict(a=4,  b=16, c=16, d=64),   # 這年齡大家認字率都低（20%）
    "10 歲組": dict(a=64, b=16, c=16, d=4),    # 這年齡大家認字率都高（80%）
}

def rr_2x2(a, b, c, d):
    """大腳丫 vs 小腳丫 的認字風險比"""
    return (a / (a + b)) / (c / (c + d))

# ① 全部混在一起（粗 RR）——先不分年齡
A = sum(s["a"] for s in strata.values())
B = sum(s["b"] for s in strata.values())
C = sum(s["c"] for s in strata.values())
D = sum(s["d"] for s in strata.values())
crude = rr_2x2(A, B, C, D)
print(f"粗 RR（沒分年齡）= {crude:.2f}"
      f"  →  大腳丫認字率 {A/(A+B):.0%}，小腳丫 {C/(C+D):.0%}")

# ② 分年齡看（分層）——同一年齡裡，腳大小還有差嗎？
for name, s in strata.items():
    print(f"  {name}：RR = {rr_2x2(**s):.2f}")

# ③ 把各層合成一個「校正後」答案：Mantel-Haenszel 加權 RR
num = den = 0
for s in strata.values():
    n = s["a"] + s["b"] + s["c"] + s["d"]
    num += s["a"] * (s["c"] + s["d"]) / n
    den += s["c"] * (s["a"] + s["b"]) / n
mh = num / den
print(f"Mantel-Haenszel 校正後 RR = {mh:.2f}")

# ④ 粗 RR 和校正後差多少？差 ≥ 10% 就代表有干擾
change = abs(crude - mh) / mh * 100
print(f"粗 RR {crude:.2f} vs 校正後 {mh:.2f}，相差 {change:.0f}% → 年齡是干擾因子！")
```

跑出來會看到：

```text
粗 RR（沒分年齡）= 2.12  →  大腳丫認字率 68%，小腳丫 32%
  6 歲組：RR = 1.00
  10 歲組：RR = 1.00
Mantel-Haenszel 校正後 RR = 1.00
粗 RR 2.12 vs 校正後 1.00，相差 112% → 年齡是干擾因子！
```

短短幾行，你就完整走了一遍分層分析：**先看粗 RR → 分層各看一次 → MH 合成校正後 RR → 比較兩者差多少**。恭喜，這正是本章 Step 4–7 在做的事！

### 干擾 vs. 效應修飾：一個超容易搞混的分岔

分層之後，一定要多看一眼：**各層的 RR 彼此像不像？** 這會把你帶到兩條完全不同的路：

| 你看到的狀況 | 這代表… | 該怎麼報告 |
|---|---|---|
| 各層 RR **彼此很接近**（都 1.0），但**和粗 RR 差很多**（2.1） | **干擾作用（confounding）** | 報告**一個**校正後 RR 就好 |
| 各層 RR **彼此差很多**（例如 6 歲 RR=1.0、10 歲 RR=3.0） | **效應修飾（effect modification）** | **不要合併**，分層各報一個，因為效應真的因組別而異 |

判斷是哪一種，統計上用**同質性檢定（homogeneity test）**：檢定「各層 RR 是否一致」。我們的大腳丫例子屬於**前者**——各層一致（都 1.0）、只是被年齡干擾，所以合成一個校正後 RR 是對的。

### 讀數字小抄（存起來）

| 你看到… | 白話意思 |
|---|---|
| 粗 RR 明顯 ≠ 1 | 先別急著下結論，可能有干擾因子在搞鬼 |
| 分層後各層 RR 都變 ≈ 1 | 原本的關聯是假象，被那個分層變項干擾了 |
| 粗 RR vs 校正後 RR 相差 ≥ 10% | 判定有干擾 → 要報告**校正後**的數字 |
| 各層 RR 彼此接近 | 是干擾 → 合成一個校正後 RR |
| 各層 RR 彼此差很多 | 是效應修飾 → 分層各報，別合併 |
| DAG 上有箭頭同時指向暴露和結果 | 那個源頭就是干擾因子的嫌疑犯 |
| 森林圖各層的點大致對齊 | 各層效應一致（同質）→ 可用 MH 合併 |

### 回到真實：認字 → 感染

現在把故事裡的角色換成護理之家的版本：

| 大腳丫故事 | 護理之家真實案例 |
|---|---|
| 腳大小（暴露） | 有沒有用**淋浴**（`shower_use`） |
| 會不會認字（結果） | 有沒有**感染**退伍軍人症 |
| 年齡（干擾因子） | **功能狀態**（`functional_status`，能不能走動） |
| 分年齡看 | **依功能狀態分層** |

你剛剛在大腳丫身上學會的每一招——看粗 RR、分層、MH 校正、比較差多少、分辨干擾 vs 效應修飾——**就是本章 Step 1–8 在護理之家資料上做的事**。現在往下看那張 DAG、那些 2×2 表和森林圖，是不是突然變親切了？😉

---

## 核心概念

### 干擾因子的三要件

一個變項 C 要被認定為干擾因子（confounder），必須**同時滿足**以下三個條件——少一個都不算：

1. **C 與暴露有關聯**：例如功能狀態影響住民會不會去淋浴（能走動的人才會走進淋浴間）
2. **C 與結果有關聯**：例如功能狀態影響感染風險（能走動的人活動範圍大，接觸水霧的機會也多）
3. **C 不是中間變項**：C 不是暴露到結果因果路徑上的「中繼站」。例如「水霧吸入量」是淋浴→感染路徑上的中間步驟，不能當作干擾因子來控制

> 🧪 **記憶口訣**：干擾因子像「雙面間諜」——它同時混在暴露組和結果組裡，讓你誤以為暴露和結果有關係（或關係被誇大/壓縮）。三個條件缺一不可，少驗一個就可能「冤枉好人」或「放走嫌犯」。

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：干擾因子的三要件——誰才算共犯</div>
  <div class="youtube-lite" data-id="2ZF6K8ylvtI">
    <img src="https://img.youtube.com/vi/2ZF6K8ylvtI/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

### 如何發現潛在的干擾因子？

故事開頭是「資深疫調人員」憑經驗提出功能狀態可能是干擾因子。但不可能每次都靠資深人員——有沒有更系統性的方法？其實有好幾條路可以走：

| 方法 | 做法 | 優點 | 限制 |
|------|------|------|------|
| **文獻回顧** | 查過去類似疫情調查的論文，看別人控制了哪些干擾因子 | 站在前人肩膀上，不漏掉已知的干擾因子 | 新型疾病可能沒有先例 |
| **畫 DAG** | 根據領域知識畫出因果關係圖，找出所有「後門路徑」 | 邏輯清晰，能區分干擾因子 vs. 中間變項 | 需要對因果機制有基本理解 |
| **統計篩選** | 檢查候選變項是否同時與暴露和結果顯著相關（干擾三要件 #1 + #2） | 用數據佐證，不完全靠直覺 | 統計顯著 ≠ 因果；可能忽略弱但真實的干擾 |
| **Change-in-estimate** | 在模型中加入/移除候選變項，看暴露的效應測量（RR 或 OR）是否改變 ≥ 10% | 直接回答「它有沒有在干擾」 | 需要先有迴歸模型（→ Ch06） |
| **專家諮詢** | 請教臨床醫師、感管人員、資深流行病學家 | 能捕捉到統計和文獻抓不到的實務因素 | 主觀，可能有遺漏 |

```{tip}
**實務上推薦「文獻 + DAG + 統計篩選」三管齊下**。先查文獻列出候選名單 → 畫 DAG 標示因果方向 → 用數據驗證干擾三要件。最後再請資深人員 review，看有沒有漏掉什麼。不要只靠一種方法，也不要只靠直覺。
```

### DAG（有向無環圖）

DAG 是一張「因果關係地圖」，用箭頭表示「誰影響誰」。畫出 DAG 就能一眼看出干擾因子藏在哪裡：

```{figure} images/confounding_dag.svg
:name: fig-confounding-dag
:alt: 干擾因子 DAG，顯示功能狀態同時影響淋浴使用和感染風險
:width: 100%

DAG 示意圖：功能狀態（C）同時影響淋浴使用（暴露）和感染風險（結果），如果不控制 C，淋浴的 RR 會被灌水。右下方的雨衣比喻幫助記憶干擾因子的邏輯。
```

從 DAG 可以看到兩條路徑：
- **直接路徑**（我們想研究的）：淋浴使用 → 感染
- **後門路徑**（干擾路徑）：淋浴使用 ← 功能狀態 → 感染

後門路徑就像考試時隔壁同學偷看你的答案——他的分數（結果）看起來跟你（暴露）有關，但其實是因為「坐你旁邊」（干擾因子）這個共同原因。分層分析就是把「坐旁邊的」和「沒坐旁邊的」分開看，消除這個虛假關聯。

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：DAG 有向無環圖——畫一張因果地圖</div>
  <div class="youtube-lite" data-id="87jXOHHNCog">
    <img src="https://img.youtube.com/vi/87jXOHHNCog/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

### 分層分析的邏輯

> 🍳 **煎蛋比喻**：你想知道「用橄欖油煎蛋是不是比較不焦」，但每次用橄欖油的時候你剛好用小火，用沙拉油的時候你剛好用大火。結果看起來橄欖油比較不焦——但真的是油的關係嗎？
>
> **分層分析的做法**：把「小火」和「大火」分開比。小火組裡比較橄欖油 vs. 沙拉油，大火組裡也比較。這樣火候（干擾因子）就被「鎖住」了，你看到的差異才是油的真正效果。

具體來說：把資料按干擾因子分層（例如按功能狀態分成 ambulatory、wheelchair、bedridden 三組），在每層內分別計算 RR。如果各層的 RR 都比粗 RR 小，就表示粗 RR 確實被干擾作用膨脹了。

### Mantel-Haenszel 法

分完層之後，我們需要一個「公平的合併方法」——不能簡單平均，因為各層的人數不同。Mantel-Haenszel（MH）法就是給每一層一個權重（取決於各層的樣本大小），算出一個加權的「調整後 RR」：

$$RR_{MH} = \frac{\sum_i \frac{a_i \cdot (c_i + d_i)}{N_i}}{\sum_i \frac{c_i \cdot (a_i + b_i)}{N_i}}$$

> 📊 **白話翻譯**：就像學期成績不能把小考和期末考直接平均——期末考佔比要大一點。MH 法就是按照「每一層有多少人」來決定權重，人多的層影響力大，人少的層影響力小。

---

## Step 1: 資料準備

這個 Step 把原始 line list 讀進來，並建立整章都會用到的 `infected` 欄位——後面每一次分層、每一次算 RR，都是以這一欄為基礎。

```python
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from epi_learning.metrics import risk_ratio

# --- 讀取護理之家資料 ---
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# clinical_severity 不是 "not_ill" 的都算感染
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `from epi_learning.metrics import risk_ratio` | 匯入本章要重複使用的風險比計算函式（Ch03 就寫好的工具） |
> | `df = pd.read_csv(...)` | 讀入 280 位住民的 line list |
> | `df["clinical_severity"] != "not_ill"` | 布林判斷：只要臨床嚴重度不是「未發病」就算感染 |
> | `.astype(int)` | 把 `True`/`False` 轉成 `1`/`0`，之後才能當 `pd.crosstab` 的欄位、加總、算 RR |
>
> 🔑 **`infected` 是整章的地基**：後面 Step 2–8 所有的粗 RR、分層 RR、MH 加權 RR，都是從這個 0/1 欄位延伸出去的。

## Step 2: 粗 RR 回顧

先算一次「沒有控制任何干擾因子」的粗 RR，作為後續比較的基準線：

```python
# --- 2×2 交叉表：淋浴使用 vs. 感染 ---
ct = pd.crosstab(df["shower_use"], df["infected"])
a = int(ct.loc[1, 1])   # 有淋浴、有感染
b = int(ct.loc[1, 0])   # 有淋浴、沒感染
c = int(ct.loc[0, 1])   # 沒淋浴、有感染
d = int(ct.loc[0, 0])   # 沒淋浴、沒感染

crude_rr = risk_ratio(a, a + b, c, c + d)
print(f"粗 RR (shower_use → infected) = {crude_rr:.3f}")
```

> 💡 **`pd.crosstab` 直接生出 2×2 表**：`ct.loc[1, 1]` 是先列後欄，取出「有淋浴、有感染」的人數；四格湊齊後丟給 Ch03 寫好的 `risk_ratio()`，就能算出粗 RR，不用手算。

## Step 3: 檢查干擾三要件

在分層之前，先驗證「功能狀態」是不是真的符合干擾因子的三個條件。少驗一個就可能白做工：

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：驗證三要件——pd.crosstab 實戰</div>
  <div class="youtube-lite" data-id="gPq3SstS3JE">
    <img src="https://img.youtube.com/vi/gPq3SstS3JE/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

```python
# --- 條件 1：功能狀態與淋浴使用有關聯嗎？ ---
# normalize="index" 讓每列加總 = 1，看比例
print("=== 功能狀態 × 淋浴使用 ===")
print(pd.crosstab(df["functional_status"], df["shower_use"],
                  margins=True, normalize="index").round(3))

# --- 條件 2：功能狀態與感染有關聯嗎？ ---
print("\n=== 功能狀態 × 感染 ===")
print(pd.crosstab(df["functional_status"], df["infected"],
                  margins=True, normalize="index").round(3))

# 條件 3（用邏輯判斷）：功能狀態不是淋浴→感染路徑的中間步驟
# （一個人不會因為「先用了淋浴」才變成能走動的——因果方向不對）
# → 三個條件都滿足，可以進行分層分析
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `pd.crosstab(df["functional_status"], df["shower_use"], ...)` | 交叉表：每一種功能狀態裡，用/不用淋浴各占多少比例——對應干擾三要件的**條件 1** |
> | `normalize="index"` | 讓每一「列」（每個功能狀態）的比例加總為 1，才能直接看百分比而不是人數 |
> | `margins=True` | 多印一列/欄「All」總計，方便對照整體比例 |
> | `pd.crosstab(df["functional_status"], df["infected"], ...)` | 同樣手法檢查功能狀態和感染的關聯——對應**條件 2** |
> | 條件 3 的註解（沒有對應程式碼） | 條件 3「不是中間變項」是**邏輯判斷**，不是算出來的——靠因果方向推理，程式跑不出答案 |
>
> 🧭 **三要件裡只有兩個能用 `pd.crosstab` 佐證**：條件 1、2 可以看數字，條件 3 永遠得靠對因果機制的理解，不是統計能單獨告訴你的。

## Step 4: 分層分析

> 這是整章的核心步驟——把資料按功能狀態（ambulatory、wheelchair、bedridden）分成三層，每一層內分別算 RR 和 95% 信賴區間。

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：分層分析——每一層都算一次 RR</div>
  <div class="youtube-lite" data-id="8yhHobtu_BU">
    <img src="https://img.youtube.com/vi/8yhHobtu_BU/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

```python
# --- 按 functional_status 分層，各層計算 RR + 95% CI ---
strata = df["functional_status"].unique()
stratum_results = []

for s in sorted(strata):
    sub = df[df["functional_status"] == s]
    ct_s = pd.crosstab(sub["shower_use"], sub["infected"])

    # 有些層可能只有暴露組或只有對照組 → 跳過
    if ct_s.shape != (2, 2):
        continue

    # 取出四格表的 a, b, c, d
    a_s = int(ct_s.loc[1, 1])
    b_s = int(ct_s.loc[1, 0])
    c_s = int(ct_s.loc[0, 1])
    d_s = int(ct_s.loc[0, 0])
    n_s = a_s + b_s + c_s + d_s

    rr_s = risk_ratio(a_s, a_s + b_s, c_s, c_s + d_s)

    # --- 95% 信賴區間（用 log 轉換法）---
    ln_rr = np.log(rr_s)
    se = np.sqrt(1/a_s - 1/(a_s+b_s) + 1/c_s - 1/(c_s+d_s))
    ci_lo = np.exp(ln_rr - 1.96 * se)
    ci_hi = np.exp(ln_rr + 1.96 * se)

    stratum_results.append({
        "stratum": s,
        "n": n_s,
        "a": a_s, "b": b_s, "c": c_s, "d": d_s,
        "RR": rr_s,
        "CI_lower": ci_lo,
        "CI_upper": ci_hi,
    })

results_df = pd.DataFrame(stratum_results)

# --- 印出各層結果 ---
print("=== 分層 RR ===")
for _, row in results_df.iterrows():
    print(f"  {row['stratum']:20s}  RR={row['RR']:.3f}  "
          f"(95% CI: {row['CI_lower']:.3f}–{row['CI_upper']:.3f})  n={row['n']}")

print(f"\n  粗 RR = {crude_rr:.3f}")
```

> **逐行拆解**（迴圈稍長，但每一輪做的事和 Ch03 算一次 RR 完全一樣）：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `strata = df["functional_status"].unique()` | 找出功能狀態有哪幾種類別，準備逐一分層 |
> | `for s in sorted(strata):` | 每一層各跑一次迴圈 |
> | `sub = df[df["functional_status"] == s]` | 篩出「這一層」的住民 |
> | `if ct_s.shape != (2, 2): continue` | 若這層缺暴露組或對照組（表不是 2×2），跳過避免報錯 |
> | `rr_s = risk_ratio(a_s, a_s + b_s, c_s, c_s + d_s)` | 算出這一層自己的 RR |
> | `ln_rr = np.log(rr_s)` | 信賴區間公式建立在 log(RR) 上（log 轉換後分布較接近常態） |
> | `se = np.sqrt(1/a_s - 1/(a_s+b_s) + 1/c_s - 1/(c_s+d_s))` | log(RR) 的標準誤公式 |
> | `ci_lo/ci_hi = np.exp(ln_rr ± 1.96 * se)` | 算完信賴區間，用 `np.exp()` 轉換回原本的 RR 尺度 |
> | `stratum_results.append({...})` | 把這一層的 n、a、b、c、d、RR、CI 存進一個 list |
> | `results_df = pd.DataFrame(stratum_results)` | 迴圈跑完後，把 list 轉成一張整齊的表格，供後面 Step 5–7 使用 |
>
> 🔑 **`if ct_s.shape != (2, 2): continue` 別漏掉**：只要有一層剛好沒有暴露組或對照組（例如全部都用淋浴、沒有對照），`.loc[1,1]` 這種寫法會直接報錯——這行是分層分析最常踩到的地雷之一。

## Step 5: 森林圖

森林圖（forest plot）把每一層的 RR 和信賴區間畫在同一張圖上，一眼就能看出各層的效應大小和精確度：

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：森林圖——一眼看穿各層 RR</div>
  <div class="youtube-lite" data-id="NhMpRmZgN10">
    <img src="https://img.youtube.com/vi/NhMpRmZgN10/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

```python
import matplotlib.pyplot as plt

# -- CJK font setup (避免中文標籤顯示為方框) --
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
plt.style.use("ggplot")
plt.rcParams["figure.dpi"] = 150

fig, ax = plt.subplots(figsize=(8, 4))
y_pos = range(len(results_df))

# --- 各層 RR ± 95% CI ---
ax.errorbar(
    results_df["RR"], y_pos,
    xerr=[results_df["RR"] - results_df["CI_lower"],
          results_df["CI_upper"] - results_df["RR"]],
    fmt="o", color="#2c7fb8", capsize=4, markersize=8,
)
# RR=1 參考線（虛線）：若信賴區間跨過 1，代表沒有統計顯著
ax.axvline(x=1, color="gray", linestyle="--", alpha=0.5)
# 粗 RR 參考線（紅色點線）
ax.axvline(x=crude_rr, color="red", linestyle=":", alpha=0.7, label=f"粗 RR={crude_rr:.2f}")
ax.set_yticks(y_pos)
ax.set_yticklabels(results_df["stratum"])
ax.set_xlabel("Risk Ratio (RR)")
ax.set_title("分層分析森林圖：淋浴使用 → 感染（按功能狀態分層）")
ax.legend()
plt.tight_layout()
plt.show()
```

> 💡 **森林圖就是把 Step 4 的 `results_df` 畫出來**：`ax.errorbar` 的 `xerr` 兩端分別是「RR 到 CI 下界」和「CI 上界到 RR」的距離；`axvline(x=1)` 畫出「無關聯」的參考線，`axvline(x=crude_rr)` 疊上粗 RR 方便對照——點的橫線只要沒有跨過灰色虛線，這一層就是統計顯著。

## Step 6: Mantel-Haenszel 加權 RR

這一步把 Step 4 各層的結果，用 Mantel-Haenszel 公式加權合併成「一個」校正後 RR——樣本數多的層權重大，樣本數少的層權重小。

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：Mantel-Haenszel 加權——公平的學期成績</div>
  <div class="youtube-lite" data-id="Fj3d4Jr0kQM">
    <img src="https://img.youtube.com/vi/Fj3d4Jr0kQM/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

```python
# --- Mantel-Haenszel 加權合併 ---
# 原理：人數多的層權重大，人數少的層權重小
numerator = 0
denominator = 0

for _, row in results_df.iterrows():
    a_i, b_i, c_i, d_i = row["a"], row["b"], row["c"], row["d"]
    n_i = a_i + b_i + c_i + d_i
    numerator += a_i * (c_i + d_i) / n_i
    denominator += c_i * (a_i + b_i) / n_i

rr_mh = numerator / denominator

print(f"Mantel-Haenszel 調整後 RR = {rr_mh:.3f}")
print(f"粗 RR                     = {crude_rr:.3f}")
print(f"差異                      = {crude_rr - rr_mh:.3f}")

# --- 用 10% 法則判斷是否有干擾作用 ---
change_pct = abs(crude_rr - rr_mh) / rr_mh * 100
print(f"變化幅度 = {change_pct:.1f}%")
if change_pct >= 10:
    print("→ 變化 ≥ 10%，粗 RR 被干擾作用影響了！")
    if crude_rr > rr_mh:
        print("  干擾方向：膨脹（粗 RR 偏高）")
    else:
        print("  干擾方向：壓抑（粗 RR 偏低）")
else:
    print("→ 變化 < 10%，干擾作用不明顯")
```

> **逐行拆解**（對照上面核心概念的 MH 公式，一行一行看更清楚）：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `for _, row in results_df.iterrows():` | 把 Step 4 存好的每一層結果拿出來，逐層累加 |
> | `n_i = a_i + b_i + c_i + d_i` | 這一層的總人數，是這一層權重的基礎 |
> | `numerator += a_i * (c_i + d_i) / n_i` | 累加 MH 公式的分子：每一層算一次、加進同一個總和 |
> | `denominator += c_i * (a_i + b_i) / n_i` | 累加 MH 公式的分母 |
> | `rr_mh = numerator / denominator` | 所有層都加總完，才做**最後一次**相除，得到一個校正後 RR |
> | `change_pct = abs(crude_rr - rr_mh) / rr_mh * 100` | 粗 RR 和校正後 RR 差多少百分比——對照核心概念裡的 10% 法則 |
> | `if change_pct >= 10:` | 依門檻判斷有沒有干擾，並依方向印出「膨脹」或「壓抑」 |
>
> ⚠️ **千萬別在迴圈裡面提早相除**：MH 公式是「每層先分別累加分子、分母，全部加總完才相除一次」——如果在迴圈裡就算 `a_i*(c_i+d_i) / c_i*(a_i+b_i)` 再逐層平均，得到的不是正確的 MH 加權值。

## Step 7: 同質性檢定——有沒有交互作用？

光用眼睛看各層 RR 像不像不夠精確；這一步用數字做一個簡化版的同質性判斷，決定各層效應能不能合併成一個 MH 值。

> 🍜 **麻辣鍋比喻**：你調查「吃麻辣鍋會不會拉肚子」，把人分成「胃好的」和「胃不好的」兩組。如果胃好的人 RR=1.2，胃不好的人 RR=4.5——這不是干擾，而是**交互作用**（effect modification）：麻辣鍋的影響「因人而異」。這時候你不能只報一個合併的 RR，必須分開說：「胃好的人影響不大，胃不好的人要小心。」

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：交互作用——暴露的影響因人而異</div>
  <div class="youtube-lite" data-id="I82KCu2kM_0">
    <img src="https://img.youtube.com/vi/I82KCu2kM_0/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

```python
# --- 同質性檢定（simplified Breslow-Day）---
# 看各層 RR 是不是差不多 → 決定能不能合併報告
rr_values = results_df["RR"].values
rr_range = rr_values.max() - rr_values.min()

print(f"各層 RR 範圍：{rr_values.min():.3f} – {rr_values.max():.3f}")
print(f"RR 變異幅度：{rr_range:.3f}")

if rr_range > 0.5:
    print("→ 各層 RR 差異較大，可能存在效果修飾（effect modification）")
    print("  建議分層報告每組的 RR，不宜只報告合併的 RR_MH")
else:
    print("→ 各層 RR 相近，可合理使用 MH 加權合併值")
    print("  報告一個 RR_MH 即可代表整體效應")
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `rr_values = results_df["RR"].values` | 把 Step 4 各層的 RR 取出來，變成一個陣列 |
> | `rr_range = rr_values.max() - rr_values.min()` | 本章使用的**簡化版**同質性判斷：最大 RR 減最小 RR，全距越大代表各層差越多 |
> | `if rr_range > 0.5:` | 用 0.5 當門檻——超過就懷疑有交互作用，不宜只報一個 MH 值 |
>
> ⚠️ **這是簡化版判斷，不是正式的統計檢定**：正式的同質性檢定應該用 Breslow-Day 或 Woolf 檢定算出 p-value；這裡的「RR 全距」法只是快速目測，正式報告建議兩者都做。

---

## 解讀重點

分層分析做完之後，你需要回答兩個問題。下面這張流程圖幫你做決定：

```{figure} images/stratified_interpretation.svg
:name: fig-stratified-interpretation
:alt: 分層分析解讀流程圖，說明如何判斷干擾作用和交互作用
:width: 100%

分層分析解讀流程圖：先問「有沒有干擾」（比較粗 RR vs. 調整 RR），再問「有沒有交互作用」（比較各層 RR 之間的差異）。
```

### 問題一：有沒有干擾作用？

比較**粗 RR** 和**調整後 RR**（MH 加權），用 **10% 法則**判斷：

$$\text{變化幅度} = \frac{|\text{粗 RR} - \text{調整 RR}|}{\text{調整 RR}} \times 100\%$$

| 情境 | 判斷 | 白話文 | 例子 |
|------|------|--------|------|
| 變化 ≥ 10% 且粗 RR > 調整 RR | 干擾因子把效應**膨脹**了 | 漢堡看起來很大，拿掉生菜才知道肉餅多厚 | 粗 RR=2.5 → 調整 RR=1.8 |
| 變化 ≥ 10% 且粗 RR < 調整 RR | 干擾因子把效應**壓抑**了 | 冰塊壓住溫度計，拿掉才看到真實溫度 | 粗 RR=1.2 → 調整 RR=1.8 |
| 變化 < 10% | 干擾作用**不明顯** | 有沒有生菜都差不多大 → 不需要太擔心 | 粗 RR=1.80 → 調整 RR=1.75 |

> 💡 **為什麼是 10%？** 這是流行病學的慣例門檻（convention），不是統計檢定。有些教科書用 5% 或 15%，但 10% 是最廣泛使用的。重點是「改變有沒有大到會影響你的結論」。

### 問題二：有沒有交互作用（效果修飾）？

比較**各層的 RR 之間**是否相近：

| 情境 | 判斷 | 白話文 | 怎麼報告 |
|------|------|--------|----------|
| 各層 RR 相近、CI 重疊、同質性 p > 0.05 | **沒有**交互作用 | 不管哪一組人，暴露的影響都差不多 | 報一個 RR_MH 就好 |
| 各層 RR 差很大、CI 不重疊、p ≤ 0.05 | **有**交互作用 | 暴露的影響因人而異——對某些人影響大、某些人影響小 | 分層報告每組的 RR |

> ⚠️ **交互作用 ≠ 干擾作用**：干擾作用是一個「假象」，控制後效應會變；交互作用是一個「真正的現象」，不同人群對暴露的反應確實不同。如果有交互作用，把它合併成一個數字反而會**遺失重要資訊**。

---

## Step 8: 第二個範例 — 按樓層分層

用同樣的方法，換一個分層變項（樓層）來練習：

```python
# --- 按樓層分層分析 ---
print("=== 按樓層分層分析：淋浴 → 感染 ===")

for floor in sorted(df["floor"].unique()):
    sub = df[df["floor"] == floor]
    ct_f = pd.crosstab(sub["shower_use"], sub["infected"])
    if ct_f.shape != (2, 2):
        continue
    a_f, b_f = int(ct_f.loc[1, 1]), int(ct_f.loc[1, 0])
    c_f, d_f = int(ct_f.loc[0, 1]), int(ct_f.loc[0, 0])
    rr_f = risk_ratio(a_f, a_f + b_f, c_f, c_f + d_f)
    print(f"  {floor}F: RR={rr_f:.3f}  (shower: {a_f}/{a_f+b_f}, "
          f"no shower: {c_f}/{c_f+d_f})")
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `for floor in sorted(df["floor"].unique()):` | 換成用**樓層**當分層變項，重複 Step 4 一模一樣的邏輯 |
> | `sub = df[df["floor"] == floor]` | 篩出這個樓層的住民 |
> | `if ct_f.shape != (2, 2): continue` | 同樣防呆：這個樓層若缺暴露組或對照組就跳過 |
> | `rr_f = risk_ratio(a_f, a_f + b_f, c_f, c_f + d_f)` | 算出這個樓層自己的 RR |
>
> 🔑 **和 Step 4 幾乎一模一樣**：只是把 `functional_status` 換成 `floor`——分層分析的邏輯可以直接複用，換一個分層變項就能重跑一次。

---

## 補充：病例對照研究也能用分層分析嗎？

到目前為止，我們的護理之家資料是**世代研究（cohort study）**——所有 280 位住民都在追蹤名單上，我們用侵襲率算 RR。但如果今天換成**病例對照研究（case-control study）**呢？

> 🏥 **情境**：假設感染人數太多，你沒辦法追蹤全部住民，只能挑 121 位感染者（病例）和 159 位未感染者（對照），然後回頭問他們有沒有用過淋浴。這時候你算不出侵襲率（因為你是刻意挑人、不是追蹤全體），所以**不能算 RR，只能算 OR（勝算比）**。

好消息：**分層分析的邏輯完全一樣**——一樣驗三要件、一樣按干擾因子分層、一樣用 Mantel-Haenszel 合併。唯一的差異是：

```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：病例對照版 MH——換個公式，邏輯一樣</div>
  <div class="youtube-lite" data-id="9441-KkyGqM">
    <img src="https://img.youtube.com/vi/9441-KkyGqM/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```

| | 世代研究（本章） | 病例對照研究 |
|---|---|---|
| **效應測量** | RR（風險比） | OR（勝算比） |
| **各層計算** | $RR_i = \frac{a_i/(a_i+b_i)}{c_i/(c_i+d_i)}$ | $OR_i = \frac{a_i \cdot d_i}{b_i \cdot c_i}$ |
| **MH 合併公式** | $RR_{MH} = \frac{\sum a_i(c_i+d_i)/N_i}{\sum c_i(a_i+b_i)/N_i}$ | $OR_{MH} = \frac{\sum a_i d_i / N_i}{\sum b_i c_i / N_i}$ |
| **判斷干擾** | 比較粗 RR vs. 調整 RR（10% 法則） | 比較粗 OR vs. 調整 OR（10% 法則） |

```{tip}
**口訣**：世代研究 → 分層 → MH adjusted **RR**；病例對照 → 分層 → MH adjusted **OR**。方法一樣，只是換了效應測量。

如果你的病例對照資料侵襲率很低（< 10%），OR ≈ RR，兩者幾乎一樣。但如果像我們的護理之家（侵襲率 43%），OR 會明顯高估——這也是 Ch06 會深入討論的重點。
```

---

## 常見錯誤

1. **不驗證干擾三要件就分層**：直接分層卻不檢查 C 是否真的與暴露和結果都有關。就像偵探沒有證據就抓人——可能抓錯人（控制了不該控制的變項），反而讓結果更偏
2. **分層太細、每層人太少**：如果一層只有 5 個人，算出來的 RR 會非常不穩定（信賴區間超寬）。經驗法則：每層至少要有 10–20 人
3. **有交互作用卻只報 MH 合併值**：各層 RR 差很大（例如 1.2 vs. 4.5），只報一個合併 RR = 2.8 會讓人以為「效應對所有人都是 2.8」——完全失真
4. **只控制一個干擾因子**：分層分析一次只能控制一個變項。如果同時有年齡、功能狀態、共病等多個干擾因子呢？→ Ch06 多變項分析（Modified Poisson + 邏輯斯迴歸）可以同時調整多個變項

## 下一步

分層分析一次只能控制一個干擾因子。但如果同時有年齡、功能狀態、共病等多個干擾因子呢？Ch06 的 **Modified Poisson regression** 可以一次調整所有變項，直接算出 **adjusted RR**——繼續用我們熟悉的風險比。同時也會用邏輯斯迴歸做對照，讓你看到 OR 在高侵襲率下高估了多少。就像從「一次只能鎖住一個變數」升級到「一次鎖住一打變數」。

## 練習本

- 課堂筆記：{ref}`05_stratified_analysis.ipynb`
- 作業版：[`05_stratified_exercise.ipynb`](exercises/05_stratified_exercise.ipynb)
- 解答版（教師版）：[`05_stratified_solution.ipynb`](solutions/05_stratified_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/05_stratified_solution.ipynb>)
