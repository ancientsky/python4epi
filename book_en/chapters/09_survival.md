# 09 存活分析：發病後，誰的預後比較差？

## 你將學到

- 存活分析的核心概念：**存活時間**、**設限資料**、**hazard（瞬時風險）**、**比例風險假設**
- 如何用 **Kaplan-Meier 法**繪製存活曲線，並且真的看懂曲線上的階梯與 tick
- 如何用 **Log-rank 檢定**比較兩組存活曲線，並正確解讀 p-value
- 如何用 **Cox 比例風險迴歸**分析多因子對存活的影響，並逐欄讀懂 `print_summary()` 表格
- 如何解讀 **Hazard Ratio (HR)** 與繪製 HR 森林圖
- 如何用 `cph.check_assumptions()` 驗證 **比例風險假設**，並知道違反時怎麼辦

## 情境故事

松柏護理之家退伍軍人症群聚事件已進入第三週。
121 位感染住民中，19 人不幸死亡，其餘存活。

你需要回答主治醫師的問題：
> 「發病後，哪些住民的死亡風險比較高？年齡？共病？嚴重度？」
> 「有沒有辦法量化這些因子的影響？」

這就是**存活分析**的核心任務——不只看「有沒有死亡」，更要看「多快死亡」以及「什麼因子加速死亡」。

---

## 核心概念

### 存活時間（Survival Time）

想像你在每位感染住民身邊放一個**碼表**：

- **按下 start** ＝ 事件起點（發病日）
- **按下 stop** ＝ 結局發生（死亡），或觀察結束
- 中間的秒數就是 `time_to_event`

本案：`time_to_event = death_date − symptom_onset_date`（死亡者）或 `investigation_end − symptom_onset_date`（仍存活者）。

### 設限資料（Censored Data）

有些人的碼表還在跑，比賽就結束了——這就是「**設限（censored）**」。

打個比方：你想比較「兩條跑步路線誰比較容易讓人放棄」，但觀察時間只有 30 分鐘。
有些跑者在 10 分鐘就放棄（觀察到事件），有些人跑到 30 分鐘還沒放棄（**設限**）—— 你只知道他「至少撐了 30 分鐘」，不知道他最後會不會放棄。

```{figure} images/survival_censoring_timeline.svg
:name: fig-survival-censoring-timeline
:alt: 六位病人的追蹤時間軸，顯示死亡、設限、失聯三種結局
:width: 100%

設限不是遺漏值——每個設限個案都有「至少觀察到這麼久」的資訊，KM 和 Cox 能正確納入。
```

在本章：
- **死亡者**：`event = 1`，`time_to_event` 到死亡日為止
- **存活者**：`event = 0`（**右設限**），`time_to_event` 到調查結束日為止
- **失聯者**：也是 `event = 0`（右設限，但時間較短）

⚠️ **常見錯誤**：把存活者的 time 當成 0 或直接丟掉——前者低估存活時間，後者浪費重要資訊。

### Hazard 與 Hazard Ratio（HR）

- **Hazard h(t)** ＝ 「**此刻還活著的人，在下一瞬間發生事件的瞬時速率**」
  - 白話版：「撐到第 t 天的人，第 t 天死亡的即時風險」
  - 單位是「每單位時間的事件數」，可以想像成「事件的心跳速度」
- **Hazard Ratio（HR）** ＝ 兩組 hazard 的比值
  - `HR > 1` → 暴露組「死得比較快」（危險因子）
  - `HR < 1` → 暴露組「死得比較慢」（保護因子）
  - `HR = 1` → 兩組速度相同（無關聯）

```{figure} images/hazard_ratio_intuition.svg
:name: fig-hazard-ratio-intuition
:alt: RR、OR、HR 三者對照，以及比例風險假設視覺說明
:width: 100%

HR 是「速率比」，不是「機率比」。它同時考慮「誰死」和「多快死」，這是和 RR、OR 最大的差別。
```

> **一句話記起來**：
> - **RR / OR**：看「有沒有發生」（不含時間）
> - **HR**：看「多快發生」（含時間 + 處理設限）

### 比例風險（Proportional Hazards, PH）假設

Cox 迴歸有一個關鍵假設：**兩組的 hazard 比值在整段追蹤期間保持常數**。

- ✓ 成立：暴露組從頭到尾「一直」比未暴露組快 1.5 倍
- ✗ 違反：前兩週暴露組快很多，後兩週反而變慢（例如：治療早期有害、後期有益）

視覺上，PH 成立時，**兩條 log(-log(S(t)))** 的曲線會大致**平行**；違反時會**交叉**（右側圖）。

⚠️ 這個假設很重要——如果違反，Cox 的 HR 會是「平均效應」而不是真實效應。Step 7 會教怎麼驗證。

---

## 方法地圖

```{figure} images/survival_method_map.svg
:name: fig-survival-method-map
:alt: 存活分析四步驟：KM 描述、Log-rank 推論、Cox 迴歸、PH 假設診斷
:width: 100%

存活分析四件事：**描述 → 推論 → 迴歸 → 診斷**。本章 Step 2-6 走完前三步，Step 7 補上診斷。
```

---

## Step 1 — 建立分析資料集

```python
import pandas as pd

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
df["symptom_onset_date"] = pd.to_datetime(df["symptom_onset_date"])
df["death_date"] = pd.to_datetime(df["death_date"])
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

cases = df[df["infected"] == 1].copy()

# 事件指標：1=死亡, 0=存活（設限）
cases["event"] = (cases["outcome"] == "dead").astype(int)

# 存活時間
investigation_end = cases["symptom_onset_date"].max() + pd.Timedelta(days=14)
cases["end_date"] = cases.apply(
    lambda r: r["death_date"] if r["event"] == 1 else investigation_end, axis=1
)
cases["time_to_event"] = (cases["end_date"] - cases["symptom_onset_date"]).dt.days
```

> **重點**：存活者的 `time_to_event` 使用「最後發病日 + 14 天」當作觀察截止——代表「我們至少觀察了這麼久都沒看到死亡」。這個值**不是** 0，也**不是**遺漏。

## Step 2 — Kaplan-Meier 全體存活曲線

```python
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

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

kmf = KaplanMeierFitter()
kmf.fit(cases["time_to_event"], event_observed=cases["event"],
        label="全體")
kmf.plot_survival_function()
plt.title("Kaplan-Meier 存活曲線（全體感染住民）")
plt.xlabel("發病後天數")
plt.ylabel("存活機率")
plt.show()
```

### 怎麼讀 KM 曲線

```{figure} images/km_step_function_anatomy.svg
:name: fig-km-step-function
:alt: Kaplan-Meier 曲線四大元素解剖：階梯、tick、中位存活時間、CI 帶
:width: 100%

每個階梯、每個 tick 都有意義——學會這張圖，以後看任何 KM 曲線都心裡有數。
```

讀曲線四步驟：

| 元素 | 意思 | 怎麼看 |
|------|------|--------|
| **階梯下降** | 有人在那一天死亡 | 階梯越多、下降越陡 → 事件越密集 |
| **tick 小豎線** | 設限（仍存活/失聯） | 不影響曲線高度，但會減少之後的風險集 |
| **穿越 y=0.5 的點** | 中位存活時間 | 一半的人還沒死的那一天；若永遠沒穿過 → `median = inf`（好消息） |
| **陰影帶（CI）** | 95% 信賴區間 | 尾端變寬 = 風險集變少、CI 越不確定 |

> **本案線索**：如果中位存活時間顯示 `inf`，代表超過一半的感染住民在觀察期內都沒死亡（CFR < 50%，合理因為 19/121 ≈ 15.7%）。

## Step 3 — 按嚴重度分組的存活曲線

```python
for severity in ["mild", "moderate", "severe"]:
    mask = cases["clinical_severity"] == severity
    kmf.fit(cases.loc[mask, "time_to_event"],
            event_observed=cases.loc[mask, "event"],
            label=severity)
    kmf.plot_survival_function()
plt.title("存活曲線（按嚴重度分組）")
plt.show()
```

### 看分組 KM 曲線的三個視角

1. **分離時點**：兩條曲線什麼時候開始分開？
   - 越**早**分開 → 因子效應越立竿見影（例如嚴重度的效應通常在前一週就出現）
2. **間距大小**：曲線之間的垂直距離
   - 間距**越大** → 效應越強
3. **是否交叉**：曲線有沒有互相穿越？
   - 交叉 → PH 假設可能被違反（Cox 結果要小心解讀，Step 7 會驗證）

> **本案預期**：severe 組的曲線應該**最早、最快**下降；mild 組曲線近乎水平。若實際觀察到 severe 和 moderate 交叉，就要 flag「嚴重度的效應可能隨時間變化」。

## Step 4 — Log-rank 檢定

```python
from lifelines.statistics import logrank_test

severe = cases[cases["clinical_severity"] == "severe"]
non_severe = cases[cases["clinical_severity"] != "severe"]
result = logrank_test(
    severe["time_to_event"], non_severe["time_to_event"],
    event_observed_A=severe["event"],
    event_observed_B=non_severe["event"],
)
print(f"Log-rank p-value = {result.p_value:.4f}")
```

### Log-rank 白話版

- **虛無假設 H₀**：兩組的存活曲線**形狀相同**（任何時點的 hazard 都一樣）
- **對立假設 H₁**：兩組至少在某個時點的 hazard 不同
- **檢定統計量**：約略服從 χ²(自由度=1) 分布
- **p-value**：
  - `p < 0.05` → 拒絕 H₀，兩組存活曲線有**統計顯著**差異
  - `p ≥ 0.05` → 無法拒絕 H₀，證據不足

⚠️ **重要限制**：log-rank **只告訴你「有沒有差」，不告訴你「差多少」**。想要量化效應（HR + CI），必須用 Cox 迴歸。

> **類比**：log-rank 就像健康檢查報告上的「異常」紅字——提醒你有問題，但不會告訴你問題的嚴重度。要看嚴重度得另外做檢查（＝ Cox 迴歸）。

## Step 5 — Cox 比例風險迴歸

```python
from lifelines import CoxPHFitter

cox_df = cases[["time_to_event", "event", "age", "sex",
                "comorbidity_copd", "comorbidity_chf",
                "comorbidity_dm", "comorbidity_cancer",
                "immunosuppressed"]].copy()
cox_df["is_male"] = (cox_df["sex"] == "M").astype(int)
cox_df = cox_df.drop(columns=["sex"])

cph = CoxPHFitter()
cph.fit(cox_df, duration_col="time_to_event", event_col="event")
cph.print_summary()
```

### 讀懂 `print_summary()` 每一欄

`print_summary()` 會印出一個看起來嚇人的大表。逐欄看其實很簡單：

| 欄名 | 意思 | 怎麼看 |
|------|------|--------|
| `coef` | log(HR) | 正數 → 危險因子；負數 → 保護因子；0 → 無關 |
| `exp(coef)` | **HR**（最重要） | 1.5 = 風險速度快 1.5 倍；0.6 = 風險速度只有 0.6 倍 |
| `se(coef)` | coef 的標準誤 | 不需要直接看（下面的 CI 已經幫你算好） |
| `z` | `coef / se` | 對應到 p-value 的檢定統計量 |
| `p` | p-value | `< 0.05` 視為統計顯著 |
| `exp(coef) lower 95%` | HR 的 95% CI 下界 | 和上界一起看 |
| `exp(coef) upper 95%` | HR 的 95% CI 上界 | **CI 跨過 1 → 不顯著** |

> **口訣**：「看 `exp(coef)` 和它的 CI 就夠了」——HR 告訴你方向和強度，CI 告訴你確定性。

### Concordance（c-index）解讀

`print_summary()` 最下面會印一個 `Concordance`，這是模型的**排序能力**：

| c-index | 解讀 |
|---------|------|
| 0.50 | 等於隨機猜（沒用） |
| 0.60-0.70 | 普通 |
| 0.70-0.80 | 還可以 |
| > 0.80 | 好 |

### ⚠️ 樣本數警訊（events per variable, EPV）

這個示範資料集只有 **19 個死亡事件**，但我們放了 **7 個變項**（age, is_male, 4 個共病、immunosuppressed）。

流行病學的經驗法則（Peduzzi 1995）：**每個變項至少需要 10 個事件**。
- 19 events / 7 variables ≈ 2.7 → 遠低於 10
- 本章是**教學示範**，實務上這樣的模型容易過度配適，HR 和 CI 都不可靠
- 實際研究時，應該先做變項篩選（像 Ch06 做的 Modified Poisson 篩選），最多保留 1-2 個最關鍵的變項

> 這也是為什麼 Cox 結果裡很多變項看起來「不顯著」——不是真的不重要，而是**樣本量不夠撐起這麼多變項**。

## Step 6 — HR 森林圖

```python
cph.plot()
plt.title("Cox Regression — Hazard Ratio")
plt.show()
```

### 怎麼看 HR 森林圖

`lifelines` 畫的森林圖預設用 **log(HR)** 當 x 軸：

| 看什麼 | 意思 |
|--------|------|
| **x = 0 的虛線** | 代表 HR = 1（無關聯的參考線） |
| **點的位置** | 點估計值 log(HR) |
| **橫線** | 95% 信賴區間 |
| **點在 x=0 右邊** | log(HR) > 0，即 HR > 1（危險因子） |
| **點在 x=0 左邊** | log(HR) < 0，即 HR < 1（保護因子） |
| **橫線跨過 x=0** | 95% CI 跨 1 → 不顯著 |
| **橫線很長** | CI 寬 → 不確定性高（通常是該變項樣本少） |

> **閱讀順序**：① 先看 point 在 0 的哪一邊（方向） → ② 看 line 有沒有跨 0（顯著性） → ③ 看 line 的長度（確定性）。

## Step 7 — PH 假設驗證

### 為什麼要檢查？

Cox 迴歸的**比例風險（PH）假設**若被違反，HR 的解讀會失準。
Step 5 給我們一堆 HR 數字，但那些數字是在「假設兩組 hazard 比值從頭到尾保持常數」的前提下算出來的——我們得驗證這個前提。

### 用 `check_assumptions()` 一行搞定

```python
# 檢查 PH 假設（show_plots=False 讓輸出只印文字結論，避免多餘子圖）
results = cph.check_assumptions(cox_df, show_plots=False)
```

這個函式會：
1. 對每個變項做 Schoenfeld residuals 檢定
2. 印出每個變項的 p-value
3. 列出違反 PH 假設的變項，並**給出建議**

### 怎麼解讀輸出？

| 輸出 | 意思 |
|------|------|
| `No violation detected` | ✓ 全部變項通過，Cox 結果可信 |
| `Variable X: p < 0.05` | ✗ 變項 X 違反 PH —— HR 隨時間變化 |
| 輸出的圖（當 `show_plots=True`） | Schoenfeld residuals 隨時間的散佈——有趨勢 = 違反 |

### 違反時的補救辦法

1. **分層（strata）**：把違反變項當「分層變項」，允許它的 baseline hazard 自由變化
   ```python
   cph.fit(cox_df, duration_col="time_to_event", event_col="event",
           strata=["違反的變項"])
   ```
2. **加入時變係數（time-varying coefficient）**：讓該變項的效應隨時間變化
3. **改用 AFT（Accelerated Failure Time）模型**：完全繞開 PH 假設
4. **拆時間段**：分「前兩週」和「後兩週」分別跑 Cox

> **注意**：事件數少（本案 19 events）時，`check_assumptions()` 的檢定力本來就不高——即使沒偵測到違反，也不代表 PH 假設一定成立。永遠搭配視覺檢查（分組 KM 曲線有沒有交叉）。

---

## 練習題

- 作業版：[`09_survival_exercise.ipynb`](exercises/09_survival_exercise.ipynb)
- 解答版（講師）：[`09_survival_solution.ipynb`](solutions/09_survival_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/09_survival_solution.ipynb>)

## 常見誤用

| 錯誤 | 正確做法 |
|------|---------|
| 只用 CFR，不做存活分析 | CFR 不考慮時間，存活分析更精確 |
| 把存活者直接排除 | 存活者是設限資料，必須納入分析 |
| 忽略比例風險假設 | 用 `cph.check_assumptions()` 驗證（Step 7） |
| HR 解讀為「機率比」 | HR 是「**速率比**」：下一秒發生事件的瞬時速率的比值 |
| 把 `hospitalized` 當危險因子 | ⚠️ 這是 **confounding by indication**——住院是因為病重，不是住院讓人死得快。必須加入嚴重度校正 |
| 19 events 硬塞 10 個變項 | **每變項 ≥ 10 事件**（events per variable rule）。事件少時先做變項篩選 |
| 忽略多重死因 | 本案只看「死亡 vs 存活」；若同時關心多種事件（例如死亡 vs 出院），應用 **competing risks**（`lifelines.CRCCumulativeIncidenceFitter`）|

## 下一步

存活分析告訴我們「誰的預後比較差」。
下一章（Ch10），我們挑戰更大的問題：**能不能用全部 32 欄特徵，訓練機器學習模型來預測感染和重症？** → 機器學習。
