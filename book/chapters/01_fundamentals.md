# 01 流行病學核心概念（Python 零基礎版）

## 你將學到

- 流病分析常見資料物件：變數、列表（list）、字典（dict）、DataFrame
- 4 個必要 Python 基礎：指定值、型別、條件、函式
- 流病核心指標：attack rate、CFR 的定義與計算
- 如何把「文字結論」轉成「可重跑程式碼」

## 先備說明（給零基礎學員）

如果你沒有 Python 經驗，請先記住這 5 點：

1. `=` 是「把右邊結果放到左邊變數」，不是數學等號。
2. `#` 後面是註解，不會執行。
3. `print(...)` 用來顯示結果。
4. 字串（文字）要加引號，如 `"confirmed"`。
5. 百分比通常用 `:.2%` 顯示。

## 情境故事

松柏護理之家爆發退伍軍人症群聚事件，主管剛把 line list 交到你手上。在你學會用 pandas 讀 CSV 之前（那是 Ch02 的事），他先要你回答：

- 全機構侵襲率（attack rate）多少？
- 致死率（CFR）多少？
- 住院率、ICU 率各多少？
- 要不要升級應變層級？

先用最基本的 Python 把指標算出來——這就是本章要做的事。

## 核心概念

- **Case definition（病例定義）**：先定義誰算個案，再計算指標。
- **Line list**：每列一位個案、每欄一個變數（本教材使用 280 位住民 × 32 欄位的 Legionella 群聚資料）。
- **Attack rate（侵襲率）**：`cases / population`——本群聚中為 121 / 280 = 43.2%。
- **Case fatality rate（致死率，CFR）**：`deaths / cases`——本群聚中為 19 / 121 = 15.7%。
- **Bias / confounding（偏差 / 交絡）**：資料蒐集與解釋時最常見的問題來源（Ch05 會深入探討）。

## Python 基礎練習（一步一步）

### 1) 數值變數——先把數字存起來

```python
# 松柏護理之家退伍軍人症群聚事件的基本數據
total_residents = 280       # 住民總數
infected = 121              # 感染人數（含無症狀）
confirmed = 89              # 確診個案
probable = 25               # 可能個案
hospitalized = 68           # 住院人數
icu = 23                    # ICU 人數
deaths = 19                 # 死亡人數
```

### 2) 計算指標——用除法得到比率

```python
# 侵襲率 = 感染人數 / 住民總數
attack_rate = infected / total_residents
print(f"侵襲率 (Attack rate): {attack_rate:.2%}")

# 致死率 = 死亡人數 / 感染人數
cfr = deaths / infected
print(f"致死率 (CFR): {cfr:.2%}")

# 住院率 = 住院人數 / 感染人數
hosp_rate = hospitalized / infected
print(f"住院率: {hosp_rate:.2%}")
```

### 3) 字典——把同一主題的資料放一起

```python
# 用字典整理群聚事件摘要
outbreak = {
    "facility": "松柏護理之家",
    "pathogen": "Legionella pneumophila",
    "total_residents": 280,
    "infected": 121,
    "confirmed": 89,
    "deaths": 19,
}

# 從字典取值計算
cfr = outbreak["deaths"] / outbreak["infected"]
print(f"{outbreak['facility']} CFR: {cfr:.2%}")
```

### 4) 列表——存放一組同類資料

```python
# 各樓層翼區的感染人數
floor_wing_cases = [15, 10, 24, 25, 20, 27]  # 1A, 1B, 2A, 2B, 3A, 3B
floor_wing_names = ["1A", "1B", "2A", "2B", "3A", "3B"]

# 找出最多感染的翼區
max_cases = max(floor_wing_cases)
max_index = floor_wing_cases.index(max_cases)
print(f"感染人數最多的翼區：{floor_wing_names[max_index]}（{max_cases} 人）")
```

### 5) 條件判斷——把指標轉成行動訊號

```python
# 根據致死率決定應變層級
if cfr > 0.15:
    print("致死率偏高（>15%），建議升級應變層級")
elif cfr > 0.10:
    print("致死率中等（10-15%），持續加強監測")
else:
    print("致死率尚可（<10%），維持常規應變")
```

### 6) 函式——把計算邏輯包成可重用的工具

```python
def calc_attack_rate(cases, population):
    """計算侵襲率。"""
    if population == 0:
        raise ValueError("分母（population）不能為 0")
    return cases / population

# 全機構侵襲率
ar_all = calc_attack_rate(121, 280)
print(f"全機構侵襲率: {ar_all:.2%}")

# 3 樓 B 翼侵襲率
ar_3b = calc_attack_rate(27, 47)
print(f"3 樓 B 翼侵襲率: {ar_3b:.2%}")
```

## 流病到程式的翻譯模板

1. 先定義名詞：`infected`, `deaths`, `total_residents`。
2. 再寫公式：`attack_rate = infected / total_residents`。
3. 最後寫判讀規則：例如 `if cfr > 0.15`。
4. 如果需要重複用，包成函式：`def calc_attack_rate(cases, population)`。

## 常見錯誤（新手最容易踩）

- 把 `infected` 放成文字（`"121"`）而不是數字（`121`）。
- 忘記分母不能是 0（例如某翼區沒有住民）。
- 直接改結果數字，不改原始輸入值（程式跑不出正確結果）。
- CFR 的分母是「感染人數」不是「住民總數」——概念要搞清楚。

## 最小可執行環境命令

```bash
uv sync
uv run jupyter lab
```
