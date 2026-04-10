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

## 核心概念

### 干擾因子的三要件

一個變項 C 要被認定為干擾因子（confounder），必須**同時滿足**以下三個條件——少一個都不算：

1. **C 與暴露有關聯**：例如功能狀態影響住民會不會去淋浴（能走動的人才會走進淋浴間）
2. **C 與結果有關聯**：例如功能狀態影響感染風險（能走動的人活動範圍大，接觸水霧的機會也多）
3. **C 不是中間變項**：C 不是暴露到結果因果路徑上的「中繼站」。例如「水霧吸入量」是淋浴→感染路徑上的中間步驟，不能當作干擾因子來控制

> 🧪 **記憶口訣**：干擾因子像「雙面間諜」——它同時混在暴露組和結果組裡，讓你誤以為暴露和結果有關係（或關係被誇大/壓縮）。三個條件缺一不可，少驗一個就可能「冤枉好人」或「放走嫌犯」。

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

## Step 3: 檢查干擾三要件

在分層之前，先驗證「功能狀態」是不是真的符合干擾因子的三個條件。少驗一個就可能白做工：

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

## Step 4: 分層分析

> 這是整章的核心步驟——把資料按功能狀態（ambulatory、wheelchair、bedridden）分成三層，每一層內分別算 RR 和 95% 信賴區間。

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

## Step 5: 森林圖

森林圖（forest plot）把每一層的 RR 和信賴區間畫在同一張圖上，一眼就能看出各層的效應大小和精確度：

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

## Step 6: Mantel-Haenszel 加權 RR

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

## Step 7: 同質性檢定——有沒有交互作用？

> 🍜 **麻辣鍋比喻**：你調查「吃麻辣鍋會不會拉肚子」，把人分成「胃好的」和「胃不好的」兩組。如果胃好的人 RR=1.2，胃不好的人 RR=4.5——這不是干擾，而是**交互作用**（effect modification）：麻辣鍋的影響「因人而異」。這時候你不能只報一個合併的 RR，必須分開說：「胃好的人影響不大，胃不好的人要小心。」

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
