# 12 因果推論與政策評估：淋浴真的「導致」感染嗎？

## 你將學到

- 用 **DAG（有向無環圖）** 視覺化因果關係
- 區分 **因果效應** 與 **統計關聯**
- 辨識 **交絡路徑、中介變項、碰撞因子**
- 計算 **歸因風險（AR）** 與 **族群歸因風險（PAR）**
- 用 **Difference-in-Differences (DiD)** 評估介入效果

## 情境故事

到這一章，你已經用了描述統計、分層分析、迴歸、ML、DL，全都指向「淋浴暴露與感染有關」。

但長官問了最根本的問題：
> 「淋浴真的『導致』感染嗎？還是只是統計上的巧合？」
> 「如果我們消毒水系統，真的會減少感染嗎？」

這就是 **因果推論** 要回答的問題。

---

## Part 1：DAG — 因果關係的視覺化

### 什麼是 DAG？

**有向無環圖（Directed Acyclic Graph）** 用箭頭表示因果方向：

```
floor_wing → water_contamination → shower_aerosol → infection
functional_status → shower_use → infection
age → comorbidities → severity → death
```

### 辨識因果結構

| 結構 | 說明 | 本案範例 |
|------|------|---------|
| **交絡因子（Confounder）** | 同時影響暴露和結果 | `functional_status` → `shower_use` 和 `infection` |
| **中介變項（Mediator）** | 在暴露和結果之間的路徑上 | `shower_aerosol` 在 `water_contamination` → `infection` 之間 |
| **碰撞因子（Collider）** | 同時被暴露和結果影響 | `hospitalized` ← `severity` 和 `infection` |

> **碰撞因子陷阱**：如果你只分析「住院的人」，就是對碰撞因子做條件化，會產生假性關聯。

---

## Part 2：歸因風險

### Attributable Risk (AR)

```python
# 暴露組侵襲率 - 非暴露組侵襲率
AR = risk_exposed - risk_unexposed
```

### Population Attributable Risk (PAR)

```python
# 如果所有人都不淋浴，可以減少多少感染？
PAR = risk_total - risk_unexposed
PAR_pct = PAR / risk_total * 100
```

---

## Part 3：Difference-in-Differences (DiD)

### 情境

1 月 25 日，護理之家對 2-3 樓 B 翼（高侵襲率區域）實施水系統緊急消毒。
1 樓作為對照組（不同水源系統）。

```python
import statsmodels.formula.api as smf

# treated = 2-3F B翼, control = 1F
# post = 1月25日之後
model = smf.ols("daily_cases ~ treated + post + treated:post", data=panel).fit()
```

`treated:post` 係數就是 DiD 效果估計——在平行趨勢假設下，代表介入的因果效應。

### 平行趨勢假設

DiD 的核心假設：如果沒有介入，兩組的趨勢會一樣。

- **如何檢驗**：看介入前的趨勢是否平行
- **如果不平行**：DiD 估計就不可信

---

## 練習題

- 作業版：[`12_causal_exercise.ipynb`](../exercises/12_causal_exercise.ipynb)
- 解答版（講師）：[`12_causal_solution.ipynb`](../solutions/12_causal_solution.ipynb)

## 常見誤用

| 錯誤 | 正確做法 |
|------|---------|
| 統計顯著 = 因果 | 關聯不等於因果，需要 DAG 分析 |
| 沒檢查平行趨勢就做 DiD | 先畫介入前趨勢圖 |
| 對碰撞因子做條件化 | 用 DAG 辨識不該控制的變項 |
| AR 解釋為「消除暴露就能避免」 | AR 假設因果關係成立，且無其他路徑 |

## 下一步

因果推論幫我們釐清「什麼導致什麼」。
下一章（Ch13），我們確保所有分析都是 **可重現的** → 可重現研究。
