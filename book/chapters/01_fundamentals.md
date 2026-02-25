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
4. 字串（文字）要加引號，如 `"North"`。
5. 百分比通常用 `:.2%` 顯示。

## 情境故事

某社區出現疑似群聚，你需要在 10 分鐘內回覆主管：

- 目前侵襲率（attack rate）多少？
- 致死率（CFR）多少？
- 哪個地區病例最多？

## 核心概念

- **Case definition**：病例定義，先定義再分析。
- **Line list**：每列一位個案、每欄一個變數。
- **Attack rate**：`cases / population`。
- **Case fatality rate (CFR)**：`deaths / cases`。
- **Bias / confounding**：資料蒐集與解釋時最常見偏差來源。

## Python 基礎練習（一步一步）

```python
# 1) 數值變數
cases = 125
population = 2450

# 2) 計算指標
attack_rate = cases / population

# 3) 顯示結果（百分比）
print(f"Attack rate: {attack_rate:.2%}")
```

```python
# 4) 字典：把同一主題的資料放一起
report = {
    "cases": 125,
    "deaths": 4,
    "population": 2450,
}

cfr = report["deaths"] / report["cases"]
print(f"CFR: {cfr:.2%}")
```

```python
# 5) 條件判斷：把指標轉成行動訊號
if attack_rate > 0.05:
    print("需要啟動加強監測")
else:
    print("維持常規監測")
```

## 流病到程式的翻譯模板

1. 先定義名詞：`cases`, `deaths`, `population`。
2. 再寫公式：`attack_rate = cases / population`。
3. 最後寫判讀規則：例如 `if attack_rate > 閾值`。

## 常見錯誤（新手最容易踩）

- 把 `cases` 放成文字（`"125"`）而不是數字（`125`）。
- 忘記分母不能是 0。
- 直接改結果數字，不改原始輸入值。

## 練習題

1. 設定 `cases=80`, `population=2000`，算 attack rate。
2. 設定 `deaths=3`, `cases=80`，算 CFR。
3. 把規則改成 attack rate 超過 `3%` 才啟動加強監測。

## 最小可執行環境命令

```bash
uv sync
uv run jupyter lab
```

## 練習本

- 作業版：[`notebooks/exercises/01_fundamentals_exercise.ipynb`](../../notebooks/exercises/01_fundamentals_exercise.ipynb)
- 解答版：[`notebooks/exercises/01_fundamentals_solution.ipynb`](../../notebooks/exercises/01_fundamentals_solution.ipynb)
