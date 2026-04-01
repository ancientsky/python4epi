# 02 資料處理與視覺化（Python 零基礎版）

## 情境

松柏護理之家退伍軍人症群聚事件爆發後第三天，疫調團隊已彙整出一份 **280 筆 × 32 欄**的個案名冊（line list）。你的任務是：把這份 CSV 讀進 Python，確認資料品質，建立分析用的衍生變項，然後用圖表呈現疫情的時間趨勢、空間分布與族群特徵。

## 你將學到

- 用 `pandas` 讀取並檢視 line list 結構
- 轉換日期欄位、處理遺漏值
- 建立衍生變項（年齡組、共病數、發病到住院天數、流行病學週）
- 用 `groupby` 做分組統計
- 用 `matplotlib` 畫流行曲線
- 用 `seaborn` 畫統計比較圖
- 用 `plotly` 畫互動式圖表

## 先備說明（給零基礎學員）

這章只要掌握這些就能開始：

1. `pd.read_csv(...)`：讀取資料
2. `df.info()` / `df.describe()`：檢視資料結構
3. `pd.to_datetime(...)`：日期轉換
4. `groupby(...).size()` / `.mean()`：分組統計
5. `plt.bar(...)` / `sns.barplot(...)` / `px.bar(...)`：各種圖表

> 💡 如果你剛從 Ch01b 過來，恭喜！`import`、`type()`、`for` 迴圈、`try/except` 這些你已經會了，接下來只需要學 pandas 的語法。
>
> 📄 **pandas 速查表**：建議列印這份一頁式 PDF 放在手邊——[Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

### 什麼是 pandas？什麼是 DataFrame？

**pandas** 是 Python 最常用的資料處理套件。你可以把它想成「Python 版的 Excel」，但功能更強大、更可重現。

pandas 有兩個核心物件：

- **DataFrame**：一張二維表格，有行（row）和列（column）——就像 Excel 的工作表
- **Series**：一個一維的欄位——就像 Excel 裡的「一行」或「一列」

```python
import pandas as pd

# 讀取 CSV → 得到一個 DataFrame
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# df 就是一張表格：280 行（每行 = 一位住民）× 32 列（每列 = 一個變項）
# 取出單一欄位 → 得到一個 Series
ages = df["age"]        # 280 位住民的年齡，就是一個 Series
```

**你需要記住的 DataFrame 概念：**

| 概念 | Excel 對照 | pandas 語法 |
|------|-----------|------------|
| 一張表格 | 整個工作表 | `df`（DataFrame） |
| 一行資料 | 某一列（row） | `df.iloc[0]`（第一行） |
| 一欄資料 | 某一行（column） | `df["age"]`（Series） |
| 某個儲存格 | A1 | `df.loc[0, "age"]` |
| 篩選 | 自動篩選 | `df[df["age"] > 80]` |
| 欄位數量 | 看最上面的字母 | `df.shape[1]` |
| 資料筆數 | 看最左邊的數字 | `df.shape[0]` 或 `len(df)` |

## 視覺化套件選擇

| 套件 | 適合場景 | 特色 |
|------|---------|------|
| `matplotlib` | 正式報告圖、完全控制細節 | 最基礎、最靈活 |
| `seaborn` | 統計圖（分布、比較、關係） | 預設美觀、語法精簡 |
| `plotly` | 互動式探索、簡報 | 滑鼠懸停看數值 |

## 流病常用圖表對照

| 分析需求 | 推薦圖表 |
|---------|---------|
| 疫情隨時間變化 | 流行曲線（epidemic curve）、折線圖 |
| 地區/翼區比較 | 長條圖、排序條圖 |
| 年齡或指標分布 | 直方圖、箱型圖 |
| 時間 × 地區強度 | 熱圖（heatmap） |
| 互動探索與簡報 | Plotly 互動圖 |

---

## 教學影片

每個重要概念都有搭配的教學影片，由老師傅手把手帶你從零學會。點擊展開即可觀看：

### Part 1 資料處理系列

````{dropdown} 🎬 DataFrame 是什麼？從 CSV 到表格的第一步
```{youtube} YOUTUBE_ID_02_01_DATAFRAME
```
````

````{dropdown} 🎬 一分鐘看懂你的資料——info() 與 describe()
```{youtube} YOUTUBE_ID_02_02_DATA_INSPECT
```
````

````{dropdown} 🎬 日期時間大魔王——to_datetime 完全攻略
```{youtube} YOUTUBE_ID_02_03_DATETIME
```
````

````{dropdown} 🎬 衍生變項四大招——cut, axis, astype, dt
```{youtube} YOUTUBE_ID_02_04_DERIVED
```
````

````{dropdown} 🎬 遺漏值偵探社——NaN, NaT, None 一次搞懂
```{youtube} YOUTUBE_ID_02_05_MISSING
```
````

````{dropdown} 🎬 分組統計秘密武器——groupby + agg 完全攻略
```{youtube} YOUTUBE_ID_02_06_GROUPBY
```
````

### Part 1.5 進階資料操作系列

````{dropdown} 🎬 頻率表速成——value_counts + crosstab 完全攻略
```{youtube} YOUTUBE_ID_02_09_VALUE_COUNTS
```
````

````{dropdown} 🎬 Excel 樞紐分析表——pivot_table 完全攻略
```{youtube} YOUTUBE_ID_02_10_PIVOT_TABLE
```
````

````{dropdown} 🎬 一行寫完分析——Method Chaining 流水線
```{youtube} YOUTUBE_ID_02_11_METHOD_CHAINING
```
````

````{dropdown} 🎬 合併資料表——merge 就是你的 VLOOKUP
```{youtube} YOUTUBE_ID_02_12_MERGE
```
````

````{dropdown} 🎬 文字清理三板斧——str + drop_duplicates + rename
```{youtube} YOUTUBE_ID_02_13_STR_CLEANUP
```
````

### Part 2 視覺化系列

````{dropdown} 🎬 用 matplotlib 畫出疫調等級的流行曲線
```{youtube} YOUTUBE_ID_02_07_EPICURVE
```
````

````{dropdown} 🎬 seaborn + plotly + 圖表輸出投稿密技
```{youtube} YOUTUBE_ID_02_08_SEABORN_PLOTLY
```
````

---

## Part 1：資料處理

### Step 1: 讀入 line list

```python
import pandas as pd

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
print(f"資料維度：{df.shape[0]} 筆 × {df.shape[1]} 欄")
df.head()
```

> **逐行解說：**
> - `import pandas as pd`：匯入 pandas 套件，取綽號 `pd`（全世界的約定俗成）
> - `pd.read_csv(...)`：讀取 CSV 檔案，回傳一個 **DataFrame**（就是一張表格）
> - `df.shape`：回傳 `(列數, 欄數)` 的元組（tuple），`df.shape[0]` 是列數、`df.shape[1]` 是欄數
> - `df.head()`：顯示前 5 筆資料（可以加數字，如 `df.head(10)` 看前 10 筆）

### Step 2: 檢視資料結構

拿到新資料的第一件事：搞清楚「長什麼樣」。

```python
df.info()
```

> **`df.info()` 告訴你：**
> - 總共幾列、幾欄
> - 每個欄位的**名稱**和**型別**（`int64` 整數、`float64` 小數、`object` 文字、`bool` 布林）
> - 每個欄位有幾個**非空值**——如果某欄只有 121 個非空值（而不是 280），就有遺漏值
>
> 💡 `object` 型別通常代表「文字」——日期欄位讀進來也是 `object`，需要手動轉換成 `datetime`。

```python
df.describe()
```

> **`df.describe()` 告訴你：**
> - `count`：非空值數量
> - `mean`：平均值、`std`：標準差
> - `min`：最小值、`max`：最大值
> - `25%`, `50%`, `75%`：四分位數
>
> 重點觀察：年齡 `min` 和 `max` 合理嗎？有沒有 -1 或 999 這種異常值？

### Step 3: 日期轉換

line list 中有 5 個日期欄位，讀入時都是**文字（object）**，Python 不知道它們是日期。必須手動轉成 `datetime` 型別，才能做時間排序、相減、取月份等操作。

```python
date_cols = [
    "facility_admission_date",
    "symptom_onset_date",
    "hospitalization_date",
    "death_date",
    "notification_date",
]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")
```

> **逐行解說：**
> - `pd.to_datetime(df[col])`：把文字型別的日期（如 `"2026-01-15"`）轉成 pandas 的 **datetime64** 物件
> - `errors="coerce"`：如果遇到無法轉換的值（空白、`"N/A"` 等），不要報錯，改成 **NaT**（Not a Time，日期版的遺漏值）
> - `df[col] = ...`：把轉換結果存回原本的欄位，覆蓋掉舊的文字值
>
> **轉換後你可以做什麼？**

```python
# 日期相減 → 得到天數
delay = df["hospitalization_date"] - df["symptom_onset_date"]
print(delay.head())  # 顯示如 "3 days", "2 days"...

# 取出「月份」或「星期幾」
print(df["symptom_onset_date"].dt.month.head())   # 1（一月）
print(df["symptom_onset_date"].dt.day_name().head())  # "Thursday"
```

> 💡 **什麼是 `.dt`？** 這是 pandas 的「日期存取器（accessor）」。當一個 Series 是 datetime 型別時，你可以用 `.dt` 取出日期的各個部分：`.dt.year`（年）、`.dt.month`（月）、`.dt.day`（日）、`.dt.days`（天數差）、`.dt.isocalendar().week`（ISO 週次）。

### Step 4: 建立衍生變項

疫調分析常需要從原始資料**衍生新變項**——也就是用現有的欄位計算出新的欄位。語法很簡單：`df["新欄位名"] = 計算公式`。

#### 4a) 年齡組 — 用 `pd.cut()` 把連續數字分組

```python
df["age_group"] = pd.cut(
    df["age"],
    bins=[59, 69, 79, 89, 100],
    labels=["60-69", "70-79", "80-89", "90+"],
)
```

> **`pd.cut()` 做了什麼？** 把連續的年齡值「切」成幾組，就像把考試分數分成 A/B/C/D 等級。
>
> | 參數 | 意思 | 範例 |
> |------|------|------|
> | `df["age"]` | 要分組的欄位 | 72, 85, 68, 91... |
> | `bins=[59, 69, 79, 89, 100]` | 切割點（左開右閉） | (59,69], (69,79], (79,89], (89,100] |
> | `labels=["60-69", ...]` | 每組的標籤 | 72 → "70-79", 91 → "90+" |
>
> 💡 為什麼 bins 從 59 開始而不是 60？因為 `pd.cut()` 預設是**左開右閉**：`(59, 69]` 表示 60~69 歲。

#### 4b) 共病數 — 用 `sum(axis=1)` 橫向加總

```python
comorbidity_cols = [
    "comorbidity_chf", "comorbidity_dm",
    "comorbidity_cancer", "comorbidity_copd",
    "immunosuppressed",
]
df["n_comorbidities"] = df[comorbidity_cols].sum(axis=1)
```

> **`axis=1` 是什麼？** 這是 pandas 最容易搞混的概念之一。
>
> | 參數 | 方向 | 意思 | 比喻 |
> |------|------|------|------|
> | `axis=0` | ↓ 往下 | 對每個**欄**做運算（跨列加總） | 每科的全班平均 |
> | `axis=1` | → 往右 | 對每個**列**做運算（跨欄加總） | 每個學生的總分 |
>
> 這裡我們要算每位住民有幾種共病，所以是「橫向（axis=1）」加總那 5 個 0/1 欄位。

#### 4c) 感染旗標 — 布林運算 + `astype(int)`

```python
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
```

> **拆解這行：**
> 1. `df["clinical_severity"] != "not_ill"` → 產生一個 True/False 的 Series（感染者為 True）
> 2. `.astype(int)` → 把 True 轉成 1、False 轉成 0
>
> 這叫做**布林索引**（Boolean indexing），是 pandas 最常用的篩選方式。

#### 4d) 發病到住院天數 — 日期相減 + `.dt.days`

```python
df["onset_to_hosp_days"] = (
    df["hospitalization_date"] - df["symptom_onset_date"]
).dt.days
```

> **拆解：** 兩個 datetime 欄位相減 → 得到 timedelta（時間差），用 `.dt.days` 取出天數整數。
> 例如：`2026-01-18` 減 `2026-01-15` = `3 days` → `.dt.days` = `3`

#### 4e) 流行病學週 — ISO 週次

```python
df["epi_week"] = df["symptom_onset_date"].dt.isocalendar().week
```

> **什麼是 ISO 週次？** ISO 8601 標準的週次編號（1~53），疫調常用來建立「每週」的統計。`.dt.isocalendar()` 回傳年份、週次、星期幾三個欄位，我們只取 `.week`。

### Step 5: 處理遺漏值

未感染者不會有 `symptom_onset_date`、`hospitalization_date` 等——這些空值不是資料錯誤，而是**結構性遺漏**（structural missing）：沒生病當然沒有發病日期。

> **遺漏值的型別：**
>
> | 型別 | 出現在 | 代表 |
> |------|--------|------|
> | `NaN` | 數值欄位 | 缺少數值（Not a Number） |
> | `NaT` | 日期欄位 | 缺少日期（Not a Time） |
> | `None` | 文字欄位 | 缺少文字 |

```python
# 查看每個欄位有多少遺漏值
print(df.isnull().sum())
```

> **`df.isnull()`** 回傳一個同樣大小的 True/False 表格（空值 = True），接著用 `.sum()` 計算每欄有幾個 True。

```python
# 確認：未感染者的 onset 日期應全為空
print("未感染者有 onset 日期的數量：",
      df.loc[df["infected"] == 0, "symptom_onset_date"].notna().sum())
```

> **`.loc[列條件, 欄位名]` 語法解說：**
> - `df.loc[df["infected"] == 0, "symptom_onset_date"]`
>   - 第一部分 `df["infected"] == 0` → 篩選未感染的列
>   - 第二部分 `"symptom_onset_date"` → 只看發病日期這一欄
> - `.notna()` → True/False（有值 = True）
> - `.sum()` → 加總 True 的數量
> - 如果結果是 0，代表結構性遺漏沒問題

### Step 6: groupby 分組統計

**`groupby` 是什麼？** 想像你在 Excel 裡做樞紐分析表（Pivot Table）：先選擇「依照哪個欄位分組」，再對每組做計算（計數、加總、平均等）。pandas 的 `groupby` 做的就是這件事。

```
                   ┌─ 1A 組 ──→ 計算侵襲率
df ──→ groupby ──→ ├─ 1B 組 ──→ 計算侵襲率
      (floor,wing) ├─ 2A 組 ──→ 計算侵襲率
                   ├─ 2B 組 ──→ 計算侵襲率
                   ├─ 3A 組 ──→ 計算侵襲率
                   └─ 3B 組 ──→ 計算侵襲率
```

```python
# 按 floor × wing 計算侵襲率
wing_stats = (
    df.groupby(["floor", "wing"])
    .agg(residents=("case_id", "size"), infected=("infected", "sum"))
    .reset_index()
)
wing_stats["attack_rate"] = wing_stats["infected"] / wing_stats["residents"]
wing_stats["attack_rate_pct"] = (wing_stats["attack_rate"] * 100).round(1)
print(wing_stats.to_string(index=False))
```

> **逐行拆解：**
>
> | 程式碼 | 做了什麼 |
> |--------|---------|
> | `df.groupby(["floor", "wing"])` | 按樓層 + 翼區分成 6 組 |
> | `.agg(residents=("case_id", "size"))` | 對每組計算列數（= 住民人數），命名為 `residents` |
> | `.agg(infected=("infected", "sum"))` | 對每組把 `infected` 欄位加總（= 感染人數） |
> | `.reset_index()` | 把分組結果從「多層索引」轉回普通的表格 |
> | `wing_stats["attack_rate"] = ...` | 新增一個侵襲率欄位 |
> | `.round(1)` | 四捨五入到小數第一位 |
>
> **`.agg()` 語法小抄：**
> ```python
> .agg(
>     新欄位名 = ("來源欄位", "聚合函數")
> )
> ```
> 常用聚合函數：`"size"` 計數、`"sum"` 加總、`"mean"` 平均、`"max"` 最大值、`"min"` 最小值

### Step 6b: 進階資料操作——Excel 使用者必學

學完 `groupby` 之後，你已經可以做基本的分組統計了。但在實際疫調中，你還會需要以下技巧。這些都是 Excel 使用者轉換到 pandas 時最常問的問題。

> 📄 **官方速查表**：pandas 官方提供了一頁式的速查表 PDF，建議列印出來放在手邊：[Pandas Cheat Sheet (PDF)](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

#### 頻率表：`value_counts()` — 你的第一張統計表

疫調的第一步通常是看各欄位的次數分布。`value_counts()` 就是 Excel 裡的 `COUNTIF`。

```python
# 臨床嚴重度分布
print(df["clinical_severity"].value_counts())

# 加上百分比
print(df["clinical_severity"].value_counts(normalize=True).round(3) * 100)
```

> **常用參數：**
>
> | 參數 | 效果 |
> |------|------|
> | `normalize=True` | 顯示比例而非次數 |
> | `sort=False` | 不依次數排序，保持原始順序 |
> | `dropna=False` | 把遺漏值也算進去 |

#### 樞紐分析表：`pivot_table()` — Excel 最愛的功能

如果你在 Excel 常用樞紐分析表（Pivot Table），`pd.pivot_table()` 就是它的 Python 版本。

```python
# Excel 的 Pivot Table：欄 = 樓層, 列 = 翼區, 值 = 侵襲率
pivot = pd.pivot_table(
    df,
    values="infected",       # 要計算的欄位
    index="wing",            # 列標籤（Excel 的「列」區域）
    columns="floor",         # 欄標籤（Excel 的「欄」區域）
    aggfunc="mean",          # 聚合函數：mean = 侵襲率
)
print((pivot * 100).round(1))  # 轉成百分比
```

> **`pivot_table` vs `groupby`？**
>
> | 場景 | 用哪個 |
> |------|--------|
> | 單一分組 + 一個統計量 | `groupby` 更簡潔 |
> | 兩個維度交叉 + 需要表格輸出 | `pivot_table` 更直覺 |
> | 需要加小計（margins） | `pivot_table(margins=True)` |
>
> ```python
> # 加上小計列和小計欄（Excel 的「總計」）
> pivot_with_totals = pd.pivot_table(
>     df, values="infected", index="wing", columns="floor",
>     aggfunc="mean", margins=True, margins_name="合計",
> )
> print((pivot_with_totals * 100).round(1))
> ```

#### 交叉表：`pd.crosstab()` — 做 2×2 表的捷徑

Ch03 會大量使用 `crosstab` 來建 2×2 列聯表。先在這裡認識它：

```python
# 性別 × 感染狀態的交叉表
print(pd.crosstab(df["sex"], df["infected"], margins=True))
```

> `crosstab` 和 `pivot_table` 很像，差別是：`crosstab` 直接吃兩個 Series，預設做計數；`pivot_table` 吃 DataFrame，需要指定 `aggfunc`。

#### 新增欄位的三種方式

```python
# 方法 1：直接賦值（你已經會了）
df["bmi_category"] = pd.cut(df["age"], bins=[0, 70, 80, 100], labels=["<70", "70-80", "80+"])

# 方法 2：用 assign()——適合 method chaining（見下節）
df = df.assign(
    is_elderly = df["age"] >= 80,
    has_comorbidity = df["n_comorbidities"] > 0,
)

# 方法 3：用 apply()——需要複雜邏輯時
def classify_risk(row):
    if row["age"] >= 80 and row["n_comorbidities"] >= 2:
        return "high"
    elif row["age"] >= 70 or row["n_comorbidities"] >= 1:
        return "medium"
    return "low"

df["risk_level"] = df.apply(classify_risk, axis=1)
print(df["risk_level"].value_counts())
```

> **什麼時候用哪種？**
>
> | 方法 | 適合場景 | 速度 |
> |------|---------|------|
> | `df["new"] = ...` | 簡單運算（加減乘除、比較） | 最快 |
> | `.assign()` | 串接多步操作（method chaining） | 快 |
> | `.apply(func, axis=1)` | 需要 if/else 判斷、跨欄邏輯 | 較慢（逐列計算） |

#### Method Chaining — 現代 pandas 風格

傳統寫法把每一步拆開，中間產生很多暫時變數。**Method chaining**（方法鏈）把多步操作串成一條流水線，可讀性更高：

```python
# 傳統寫法（很多暫時變數）
cases = df[df["infected"] == 1]
cases = cases[cases["age"] >= 70]
result = cases.groupby("floor").size()
result = result.reset_index(name="n_cases")
result = result.sort_values("n_cases", ascending=False)
print(result)

# Method chaining（一氣呵成）
result = (
    df
    .query("infected == 1 and age >= 70")     # 篩選（取代布林索引）
    .groupby("floor")
    .size()
    .reset_index(name="n_cases")
    .sort_values("n_cases", ascending=False)
)
print(result)
```

> **`.query()` 語法重點：**
> - 條件用字串寫，`and` / `or` / `not` 取代 `&` / `|` / `~`
> - 欄位名不用加引號（除非欄位名有空格或特殊字元）
> - 可以引用外部變數：`df.query("age > @threshold")`
>
> **更複雜的 chaining 範例：**
>
> ```python
> summary = (
>     df
>     .assign(age_group=pd.cut(df["age"], bins=[59, 69, 79, 89, 100],
>                              labels=["60-69", "70-79", "80-89", "90+"]))
>     .groupby("age_group", observed=True)
>     .agg(
>         n_residents=("case_id", "size"),
>         n_infected=("infected", "sum"),
>         n_dead=("outcome", lambda x: (x == "dead").sum()),
>     )
>     .assign(
>         attack_rate=lambda d: (d["n_infected"] / d["n_residents"] * 100).round(1),
>         cfr=lambda d: (d["n_dead"] / d["n_infected"] * 100).round(1),
>     )
> )
> print(summary)
> ```

#### 合併資料表：`merge()` — 疫調最常見的需求

實際疫調中，個案名冊和檢驗結果、環境檢體資料往往存在不同的檔案裡。`merge()` 就是 Excel 的 `VLOOKUP`，但更強大。

```python
# 假設有兩張表：個案名冊和檢驗結果
cases_df = df[["case_id", "age", "sex", "infected"]].head(10)
lab_df = pd.DataFrame({
    "case_id": [1, 2, 3, 5, 8],
    "lab_method": ["culture", "PCR", "culture", "PCR", "culture"],
    "ct_value": [25.3, 28.1, 22.5, 31.0, 24.8],
})

# 合併（以 case_id 為 key）
merged = pd.merge(cases_df, lab_df, on="case_id", how="left")
print(merged)
```

> **`how` 參數——四種合併方式：**
>
> | `how` | 行為 | Excel 對照 |
> |-------|------|-----------|
> | `"left"` | 保留左表所有列 | VLOOKUP（找不到 = 空白） |
> | `"right"` | 保留右表所有列 | 反向 VLOOKUP |
> | `"inner"` | 只保留兩邊都有的 | VLOOKUP 再刪除空白列 |
> | `"outer"` | 兩邊全部保留 | 完整合併 |
>
> 💡 疫調最常用 `"left"`：以個案名冊為主表，把檢驗結果「補」上去。

#### 文字清理：`.str` accessor

```python
# 清理翼區欄位：統一大小寫
df["wing_clean"] = df["wing"].str.upper()

# 檢查欄位是否包含特定文字
severe_mask = df["clinical_severity"].str.contains("severe", na=False)
print(f"含有 'severe' 的筆數：{severe_mask.sum()}")
```

> **常用 `.str` 方法：**
>
> | 方法 | 效果 |
> |------|------|
> | `.str.upper()` / `.str.lower()` | 轉大寫 / 小寫 |
> | `.str.strip()` | 去除前後空白 |
> | `.str.contains("pattern")` | 是否包含特定文字（回傳 True/False） |
> | `.str.replace("old", "new")` | 取代文字 |
> | `.str.split("_")` | 以分隔符切割 |
> | `.str.len()` | 文字長度 |

#### 去重與排名

```python
# 去除重複通報（以 case_id 為準）
df_unique = df.drop_duplicates(subset="case_id", keep="first")

# 重新命名欄位
df_renamed = df.rename(columns={"symptom_onset_date": "onset_date"})

# 找出侵襲率最高的前 3 個翼區
print(wing_stats.nlargest(3, "attack_rate_pct"))
```

---

## Part 2：視覺化

### matplotlib 的 `fig, ax` 模式——看到不要怕

在你看到下面的程式碼之前，先搞懂一件事：matplotlib 有兩種寫法。

**簡單寫法（適合快速探索）：**
```python
import matplotlib.pyplot as plt
plt.bar(["A", "B", "C"], [10, 20, 15])
plt.title("My Chart")
plt.show()
```

**專業寫法（本教材使用）：**
```python
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(["A", "B", "C"], [10, 20, 15])
ax.set_title("My Chart")
plt.show()
```

兩種寫法結果一樣，但專業寫法更靈活。**你只需要記住這個公式：**

```
fig, ax = plt.subplots()     # fig = 整張畫布, ax = 畫布上的一塊畫板
ax.bar(...)                   # 在畫板上畫圖（把 plt.bar 改成 ax.bar）
ax.set_title(...)             # 設定標題（把 plt.title 改成 ax.set_title）
ax.set_xlabel(...)            # 設定 X 軸標籤
ax.set_ylabel(...)            # 設定 Y 軸標籤
plt.tight_layout()            # 自動調整邊距，避免文字被裁切
plt.show()                    # 顯示圖表
```

> 💡 **為什麼用 `fig, ax`？** 因為之後你需要在同一張畫布上畫多個子圖（如上下兩張流行曲線比較），只有 `fig, ax` 寫法能做到。現在先習慣這個模式，以後會感謝自己。

### 三套繪圖工具的差異

| 特性 | matplotlib | seaborn | plotly |
|------|-----------|---------|--------|
| **定位** | 底層引擎，什麼都能畫 | matplotlib 的高級包裝 | 互動式圖表引擎 |
| **語法** | 手動設定每個元素 | 一行搞定統計圖 | 一行搞定互動圖 |
| **互動** | 靜態圖片 | 靜態圖片 | 可懸停、縮放、點選 |
| **投稿期刊** | ✅ 首選（完全可控） | ✅ 可以（底層是 matplotlib） | ⚠️ 需匯出靜態圖 |
| **適合場景** | 需要精確控制、客製化 | 統計圖（分布、比較） | 簡報、互動儀表板 |
| **學習曲線** | 最陡 😰 | 最平 😊 | 中等 |

**簡單記法：**
- **matplotlib** = 你自己從零搭建房子（累但完全自由）
- **seaborn** = 住預售屋（設計師幫你配好，稍微改裝即可）
- **plotly** = 住智慧宅（互動功能多，但不好改內裝）

### Step 7: 流行曲線（matplotlib）

流行曲線（epidemic curve）是流行病學最經典的圖表——X 軸是發病日期，Y 軸是新增病例數。從曲線形狀可推斷傳播模式。

```{admonition} 流行曲線繪製規範（依 CDC / ECDC 指引）
:class: important

流行曲線本質上是一種**直方圖（histogram）**，不是一般的長條圖（bar chart）。以下是根據 [CDC Epi Chart](https://www.cdc.gov/wcms/4.0/cdc-wp/data-presentation/epi-chart.html) 及 [CDC Field Epidemiology Manual](https://www.cdc.gov/field-epi-manual/php/chapters/describing-epi-data.html) 整理的繪製規範：

**結構與比例**
1. **相鄰長條不留間隙**：X 軸是連續時間軸，長條之間不應有空隙，以忠實反映時間的連續性。
2. **補齊沒有病例的日期**：即使某天新增 0 例，也要讓它佔據 X 軸上的位置，否則間距會失真。
3. **不使用 Y 軸截斷（scale break）**：Y 軸必須從 0 開始，不可以截斷，否則會誇大或縮小趨勢。
4. **顯示爆發前後的背景期**：X 軸應包含疫情爆發前 1–2 個潛伏期的日期，讓讀者看到疫情何時開始偏離背景值。

**時間間距**
5. **時間間距 ≈ 潛伏期的 1/4**：退伍軍人症潛伏期 2–10 天（平均 5–6 天），以 1 天為單位是適當的。病例數很多時可縮短間距，很少時可拉長。

**標題與標籤**
6. **標題要能獨立閱讀**：包含疾病名稱、地點、時間範圍，例如「松柏護理之家退伍軍人症流行曲線，依發病日，2026 年 1 月」。
7. **X 軸**：標示「發病日期（Date of Symptom Onset）」——明確說明時間基準。若使用通報日等替代日期，須在圖表下方註明。
8. **Y 軸**：標示「病例數（Number of Cases）」，必須使用整數刻度。

**視覺風格**
9. **隱藏格線**：CDC 建議隱藏水平和垂直格線以減少視覺干擾（reduce chart clutter）。
10. **去除多餘框線**：移除上方和右方的邊框（`spines`）。
11. **個案分類用顏色區分**：若同時呈現確診（confirmed）與疑似（probable）個案，須用不同顏色區分並附圖例。
12. **不在長條上標數字**：ECDC 指引建議不要在圖表上同時呈現數位（數字）與類比（圖形）資訊，以免互相干擾。

**標註（Annotation）**
13. **加入關鍵事件標註**：在流行曲線上標註重要事件（如暴露時間、介入措施、通報日），可以幫助說明病例分布的原因。
```

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -- 全域圖表風格設定 --
plt.style.use("ggplot")                 # 學術風格：淡灰背景 + 白色格線
plt.rcParams["figure.dpi"] = 150        # 提高解析度（預設 100 太模糊）

# -- CJK font setup (避免中文標籤顯示為方框) --
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
```

```{admonition} 圖表風格與解析度設定
:class: tip, dropdown

**`plt.style.use("ggplot")`** 套用 R 語言 ggplot2 的經典風格——淡灰背景搭配白色格線，整體視覺更專業。matplotlib 內建多種風格，可用 `plt.style.available` 查看完整列表，常見選擇：

| 風格 | 特色 |
|------|------|
| `ggplot` | R 語言 ggplot2 風格，學術論文常用 |
| `seaborn-v0_8` | seaborn 預設風格，柔和色調 |
| `bmh` | Bayesian Methods for Hackers，清爽配色 |
| `fivethirtyeight` | FiveThirtyEight 新聞網站風格 |
| `default` | matplotlib 原始預設 |

**`plt.rcParams["figure.dpi"] = 150`** 將圖片解析度從預設的 100 DPI 提升到 150 DPI，在 Jupyter Notebook 和網頁上顯示更清晰。若需要出版品質可設為 300。

> 💡 `plt.style.use()` 會改變全域設定，建議放在 notebook 最前面。如果只想對單一圖表套用風格，可用 `with plt.style.context("ggplot"):` 包住繪圖程式碼。
```

```{admonition} 為什麼候選清單要列這麼多字型？
:class: tip, dropdown

matplotlib 會從 `font.sans-serif` 清單中**由左到右**嘗試每個字型名稱，找到第一個已安裝的就使用。不同作業系統預裝的字型不同：

- **macOS**：Heiti TC, Arial Unicode MS
- **Windows**：Microsoft JhengHei（微軟正黑體）
- **Linux (Ubuntu)**：`sudo apt install fonts-noto-cjk` 安裝後可用 Noto Sans CJK 系列

特別注意：Noto Sans CJK 系列通常以 `.ttc`（TrueType Collection）格式安裝，一個檔案裡包含 JP/KR/SC/TC/HK 五種變體。但 matplotlib 的 `addfont()` **只會註冊第一個變體（通常是 JP）**，所以候選清單中需要把 JP、SC 也列進去——它們的 CJK 字集相同，都能顯示繁體中文。

詳細排錯步驟見 [Ch15 附錄 E. 中文圖表顯示排錯](15_appendix.md#e-中文圖表顯示排錯matplotlib--plotly)。
```

#### 標準流行曲線

```python
cases = df[df["infected"] == 1]
daily = cases.groupby("symptom_onset_date").size().rename("cases")

# 補齊完整日期範圍：包含爆發前 3 天（顯示背景期）
date_range = pd.date_range(
    daily.index.min() - pd.Timedelta(days=3),
    daily.index.max() + pd.Timedelta(days=1),
    freq="D",
)
daily = daily.reindex(date_range, fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(
    daily.index, daily.values,
    width=1.0,                         # 相鄰長條緊密貼合（直方圖風格）
    color="#2c7fb8", edgecolor="white", linewidth=0.5,
)
ax.set_title(
    "松柏護理之家退伍軍人症流行曲線，依發病日，2026 年 1 月",
    fontsize=13, fontweight="bold",
)
ax.set_xlabel("發病日期（Date of Symptom Onset）")
ax.set_ylabel("病例數（Number of Cases）")

# 日期格式化
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)

# X 軸緊貼資料範圍、Y 軸從 0 開始且整數刻度
ax.set_xlim(daily.index.min() - pd.Timedelta(hours=12),
            daily.index.max() + pd.Timedelta(hours=12))
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

# CDC 風格：隱藏格線、去除上右邊框
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
```

**解讀**：峰值集中在幾天內 → 共同暴露源（point source）型態。爆發前 3 天（01/09–01/11）沒有病例，顯示疫情的起始時間點清晰。

#### 依個案分類分層（confirmed vs. probable）

CDC 建議：若同時呈現不同分類的個案，須用顏色區分。這裡我們用堆疊長條圖，將確診與疑似個案分開呈現。

```python
# 按日期 × 個案分類計算每日病例數
daily_class = (
    cases.groupby(["symptom_onset_date", "case_classification"])
    .size()
    .unstack(fill_value=0)
)
daily_class = daily_class.reindex(date_range, fill_value=0)

colors = {"confirmed": "#2c7fb8", "probable": "#a6bddb"}
fig, ax = plt.subplots(figsize=(10, 4))

bottom = None
for cls in ["confirmed", "probable"]:
    if cls not in daily_class.columns:
        continue
    ax.bar(
        daily_class.index, daily_class[cls],
        width=1.0, bottom=bottom,
        color=colors[cls], edgecolor="white", linewidth=0.5,
        label="確診（Confirmed）" if cls == "confirmed" else "疑似（Probable）",
    )
    bottom = daily_class[cls] if bottom is None else bottom + daily_class[cls]

ax.set_title(
    "松柏護理之家退伍軍人症流行曲線，依個案分類與發病日，2026 年 1 月",
    fontsize=12, fontweight="bold",
)
ax.set_xlabel("發病日期（Date of Symptom Onset）")
ax.set_ylabel("病例數（Number of Cases）")
ax.legend(loc="upper left", frameon=False)

ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)
ax.set_xlim(daily.index.min() - pd.Timedelta(hours=12),
            daily.index.max() + pd.Timedelta(hours=12))
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
```

#### 加入關鍵事件標註

CDC 建議在流行曲線上標註重要事件，幫助讀者理解病例分布的原因。

```python
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(
    daily.index, daily.values,
    width=1.0, color="#2c7fb8", edgecolor="white", linewidth=0.5,
)

# 標註關鍵事件
ax.annotate(
    "首例通報",
    xy=(pd.Timestamp("2026-01-14"), daily.get(pd.Timestamp("2026-01-14"), 0)),
    xytext=(pd.Timestamp("2026-01-10"), daily.max() * 0.85),
    fontsize=9,
    arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2),
    bbox=dict(boxstyle="round,pad=0.3", fc="#ffffcc", ec="#cccccc"),
)
ax.annotate(
    "水系統消毒",
    xy=(pd.Timestamp("2026-01-22"), daily.get(pd.Timestamp("2026-01-22"), 0)),
    xytext=(pd.Timestamp("2026-01-25"), daily.max() * 0.85),
    fontsize=9,
    arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2),
    bbox=dict(boxstyle="round,pad=0.3", fc="#ffffcc", ec="#cccccc"),
)

ax.set_title(
    "松柏護理之家退伍軍人症流行曲線（含關鍵事件標註）",
    fontsize=13, fontweight="bold",
)
ax.set_xlabel("發病日期（Date of Symptom Onset）")
ax.set_ylabel("病例數（Number of Cases）")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)
ax.set_xlim(daily.index.min() - pd.Timedelta(hours=12),
            daily.index.max() + pd.Timedelta(hours=12))
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
```

#### 經典方格式流行曲線（依個案分類著色）

在教科書和 CDC 疫調報告中常見的**方格式（unit chart / stacked squares）**流行曲線——每個小方格代表一個病例。這裡我們用顏色區分確診與疑似個案。

```python
# 準備每日 confirmed / probable 的病例數
daily_class = (
    cases.groupby(["symptom_onset_date", "case_classification"])
    .size()
    .unstack(fill_value=0)
)
daily_class = daily_class.reindex(date_range, fill_value=0)
colors_map = {"confirmed": "#2c7fb8", "probable": "#a6bddb"}

fig, ax = plt.subplots(figsize=(10, 5))
box_size = 1.0

for date in daily_class.index:
    x = mdates.date2num(date)
    j = 0  # 目前堆疊高度
    for cls in ["confirmed", "probable"]:
        count = daily_class.at[date, cls] if cls in daily_class.columns else 0
        for _ in range(int(count)):
            rect = plt.Rectangle(
                (x - box_size / 2, j * box_size),
                box_size, box_size,
                facecolor=colors_map[cls],
                edgecolor="white", linewidth=0.8,
            )
            ax.add_patch(rect)
            j += 1

# 座標軸設定
ax.set_xlim(mdates.date2num(daily_class.index.min()) - 1.5,
            mdates.date2num(daily_class.index.max()) + 1.5)
y_max = daily_class.sum(axis=1).max()
ax.set_ylim(0, y_max + 1)
ax.set_aspect("equal")

ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

ax.set_title(
    "松柏護理之家退伍軍人症流行曲線 — 方格式（依個案分類）",
    fontsize=13, fontweight="bold",
)
ax.set_xlabel("發病日期（Date of Symptom Onset）")
ax.set_ylabel("病例數（Number of Cases）")

# 手動圖例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#2c7fb8", edgecolor="white", label="確診（Confirmed）"),
    Patch(facecolor="#a6bddb", edgecolor="white", label="疑似（Probable）"),
]
ax.legend(handles=legend_elements, loc="upper left", frameon=False)

ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
```

```{tip}
方格式流行曲線特別適合**小規模群聚**（數十至一百多例），每個方格都可以用不同顏色代表個案屬性（例如確診 / 疑似、男 / 女、各樓層），讓讀者同時看到時間分布和個案組成。當病例數太大（> 200）時，方格會變得太小，此時改用標準直方圖更合適。
```

### Step 8: 年齡分布（seaborn）

seaborn 用一行就能畫出漂亮的統計圖，不用像 matplotlib 那樣手動設定每個元素。

```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(
    data=df, x="age", hue="infected", hue_order=[1, 0], bins=15,
    multiple="stack", palette={1: "#e34a33", 0: "#cccccc"}, ax=ax,
)
ax.set_title("年齡分布：感染 vs 未感染")
ax.set_xlabel("年齡")
ax.set_ylabel("人數")
ax.legend(title="感染", labels=["感染", "未感染"])
plt.tight_layout()
plt.show()
```

> **`sns.histplot()` 參數解說：**
>
> | 參數 | 意思 |
> |------|------|
> | `data=df` | 資料來源（整個 DataFrame） |
> | `x="age"` | X 軸用哪個欄位 |
> | `hue="infected"` | 按哪個欄位分色 |
> | `hue_order=[1, 0]` | 圖例順序：感染者排前面 |
> | `bins=15` | 分成 15 組（直方圖的柱子數量） |
> | `multiple="stack"` | 堆疊而非重疊（`"layer"` 則是重疊） |
> | `palette={1: "#e34a33", 0: "#cccccc"}` | 指定每組的顏色 |
> | `ax=ax` | 畫在哪個畫板上 |
>
> 💡 seaborn 的函式可以直接接收 DataFrame + 欄位名稱，不用像 matplotlib 那樣先把資料取出來。

### Step 9: 翼區侵襲率長條圖（seaborn）

> ⚠️ **不能直接比病例數！** 1A 翼區 15 人感染、3B 翼區 27 人感染——看起來 3B 比較嚴重？不一定！如果 1A 只有 30 位住民而 3B 有 47 位，侵襲率才是公平的比較基準。

```python
wing_stats["label"] = wing_stats["floor"].astype(str) + wing_stats["wing"]
wing_stats = wing_stats.sort_values("attack_rate", ascending=False)

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(
    data=wing_stats, x="label", y="attack_rate_pct",
    hue="label", palette="YlOrRd", legend=False, ax=ax,
)
ax.set_title("各翼區侵襲率比較")
ax.set_xlabel("翼區")
ax.set_ylabel("侵襲率 (%)")
for i, row in wing_stats.iterrows():
    ax.text(
        list(wing_stats["label"]).index(row["label"]),
        row["attack_rate_pct"] + 1,
        f'{row["attack_rate_pct"]}%',
        ha="center", fontsize=10,
    )
plt.tight_layout()
plt.show()
```

### Step 10: 嚴重度 × 共病熱力圖（seaborn）

熱力圖用**顏色深淺**表示數值大小——像是溫度計一樣，顏色越深代表值越大。非常適合看兩個變項的交叉關係。

```python
severity_order = ["mild", "moderate", "severe"]
heat_data = (
    cases[cases["clinical_severity"].isin(severity_order)]
    .groupby(["clinical_severity", "n_comorbidities"])
    .size()
    .unstack(fill_value=0)
    .reindex(severity_order)
)

fig, ax = plt.subplots(figsize=(8, 3.5))
sns.heatmap(heat_data, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
# annot=True: 在每格顯示數字  fmt="d": 整數格式  cmap: 配色方案
ax.set_title("臨床嚴重度 × 共病數")
ax.set_xlabel("共病數")
ax.set_ylabel("嚴重度")
plt.tight_layout()
plt.show()
```

### Step 11: 互動式分層流行曲線（Plotly）

Plotly 最大的優勢是**互動性**——滑鼠懸停就能看到數值，可以縮放、平移。特別適合在簡報中展示疫調結果，讓聽眾自己探索資料。

> **Plotly 語法跟 matplotlib 完全不同：**
> - matplotlib 用 `fig, ax = plt.subplots()` → `ax.bar()`
> - plotly 用 `fig = px.bar(data, x=..., y=...)` → `fig.update_layout()`
> - Plotly 不需要 `plt.show()`，直接用 `fig.show()`

Plotly 的互動式圖表同樣需要遵循 CDC 流行曲線繪製規範：無間隙、描述性標題、隱藏格線、Y 軸從 0 開始。

```python
import plotly.express as px
import plotly.graph_objects as go

# 依樓層分層，並補齊完整日期範圍
daily_floor = (
    cases.groupby(["symptom_onset_date", "floor"])
    .size()
    .rename("cases")
    .reset_index()
)
daily_floor["floor"] = daily_floor["floor"].astype(str) + "F"

# 補齊所有日期 × 樓層組合（含 0 例的天數）
all_dates = pd.date_range(
    cases["symptom_onset_date"].min() - pd.Timedelta(days=3),
    cases["symptom_onset_date"].max() + pd.Timedelta(days=1),
    freq="D",
)
all_floors = sorted(daily_floor["floor"].unique())
full_idx = pd.MultiIndex.from_product([all_dates, all_floors], names=["symptom_onset_date", "floor"])
daily_floor = (
    daily_floor.set_index(["symptom_onset_date", "floor"])
    .reindex(full_idx, fill_value=0)
    .reset_index()
)

fig = px.bar(
    daily_floor,
    x="symptom_onset_date", y="cases", color="floor",
    barmode="stack",
    color_discrete_sequence=["#2c7fb8", "#41ae76", "#fe9929"],
    title="松柏護理之家退伍軍人症流行曲線，依樓層與發病日，2026 年 1 月",
    labels={"symptom_onset_date": "發病日期（Date of Symptom Onset）",
            "cases": "病例數（Number of Cases）",
            "floor": "樓層"},
)

# CDC 風格：無間隙、隱藏格線、Y 軸從 0 開始
fig.update_layout(
    bargap=0,                              # 長條之間無間隙
    xaxis=dict(showgrid=False),            # 隱藏垂直格線
    yaxis=dict(showgrid=False, rangemode="tozero"),  # 隱藏水平格線、Y 軸從 0
    plot_bgcolor="white",                  # 白色背景
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
)
fig.show()
```

---

### Step 12: 匯出圖表——疫調報告與期刊投稿

做完圖不存檔就白費了。以下教你如何輸出專業品質的圖表。

#### 基本匯出：`savefig()`

```python
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, width=1.0, color="#2c7fb8")
ax.set_title("流行曲線")
ax.set_xlabel("發病日期")
ax.set_ylabel("病例數")
plt.tight_layout()

# 存成 PNG（適合報告、簡報）
fig.savefig("epi_curve.png", dpi=300, bbox_inches="tight")

# 存成 PDF（適合期刊投稿，向量圖不會糊掉）
fig.savefig("epi_curve.pdf", bbox_inches="tight")

# 存成 SVG（適合網頁、可後製編輯）
fig.savefig("epi_curve.svg", bbox_inches="tight")
```

> **參數說明：**
>
> | 參數 | 意思 | 建議值 |
> |------|------|--------|
> | `dpi=300` | 解析度（每吋像素數） | 報告用 150~200，期刊投稿 300~600 |
> | `bbox_inches="tight"` | 自動裁切白邊 | 永遠加上 |
> | `facecolor="white"` | 背景色 | 投稿時加上，避免透明背景 |
> | `transparent=True` | 透明背景 | 簡報疊在有色背景上時使用 |

#### Plotly 匯出

```python
# 存成互動 HTML（可嵌入網頁報告）
fig.write_html("epi_curve_interactive.html")

# 存成靜態 PNG（需要安裝 kaleido 套件）
# uv add kaleido
fig.write_image("epi_curve_plotly.png", scale=2)

# 存成 PDF
fig.write_image("epi_curve_plotly.pdf")
```

#### 期刊投稿的圖表規格

如果你的疫調報告要投稿 NEJM、Lancet、JAMA 等期刊，圖表有嚴格要求：

```{admonition} 期刊等級圖表規格（NEJM / Lancet / JAMA）
:class: important

**檔案格式**
- **首選**：PDF 或 EPS（向量圖，放大不失真）
- **可接受**：TIFF 或 PNG（點陣圖，需要高 DPI）
- **不接受**：JPG（有壓縮失真，不適合科學圖表）

**解析度要求**
- 線條圖（line art）：≥ 1000 DPI
- 灰階圖（halftone）：≥ 300 DPI
- 混合圖（combination）：≥ 600 DPI

**尺寸**
- 單欄寬：8.3 cm（3.27 inch）
- 雙欄寬：17.1 cm（6.73 inch）
- 最大高度：23.4 cm（9.21 inch）

**字型**
- 建議：Arial、Helvetica（無襯線字型）
- 圖表內文字：8~10 pt
- 座標軸標籤：不小於 6 pt

**配色**
- 使用色盲友善（colorblind-safe）的配色方案
- 避免紅/綠同時出現（約 8% 的男性有紅綠色盲）
- 推薦配色套件：`seaborn` 的 `"colorblind"` 調色盤
```

**實際操作範例——投稿等級圖表：**

```python
# 投稿 Lancet 的流行曲線
fig, ax = plt.subplots(figsize=(6.73, 3.5))  # 雙欄寬

ax.bar(daily.index, daily.values, width=1.0,
       color="#2c7fb8", edgecolor="white", linewidth=0.3)

# 標題和軸標籤用英文（國際期刊要求）
ax.set_title("Epidemic curve of Legionnaires' disease outbreak\n"
             "Pine Cedar Nursing Home, January 2026",
             fontsize=10, fontweight="bold")
ax.set_xlabel("Date of symptom onset", fontsize=9)
ax.set_ylabel("Number of cases", fontsize=9)

# 字型大小：軸刻度 8 pt
ax.tick_params(labelsize=8)

# 日期格式化
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
fig.autofmt_xdate(rotation=45)

ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

# 存成投稿用的 PDF（向量圖）
fig.savefig("Figure1_epi_curve.pdf",
            bbox_inches="tight", facecolor="white")

# 或存成 TIFF（某些期刊要求）
fig.savefig("Figure1_epi_curve.tiff",
            dpi=600, bbox_inches="tight", facecolor="white")
plt.show()
```

> 💡 **色盲友善配色**：用 `sns.color_palette("colorblind")` 取得預設的色盲友善色票，或用 [ColorBrewer](https://colorbrewer2.org/) 網站挑選。

---

## 圖表解讀重點

| 圖表 | 觀察重點 |
|------|---------|
| 流行曲線 | 峰值時間、上升/下降速度 → 傳播模式 |
| 年齡分布 | 感染者是否集中在特定年齡層 |
| 翼區長條圖 | 哪些翼區侵襲率異常偏高 → 空間線索 |
| 嚴重度×共病 | 共病多的人是否更容易重症 |
| 互動曲線 | 各樓層的流行高峰是否同步 |

## pandas 常用語法速查表

初學者隨時回來翻這張表就好。更完整的版本請參考 [Pandas Cheat Sheet (PDF)](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)。

**基本操作**

| 需求 | 語法 | 說明 |
|------|------|------|
| 讀取 CSV | `pd.read_csv("file.csv")` | 回傳 DataFrame |
| 看前 N 筆 | `df.head(10)` | 預設 5 筆 |
| 看結構 | `df.info()` | 欄位名、型別、非空值 |
| 看統計 | `df.describe()` | 平均、標準差、四分位 |
| 看維度 | `df.shape` | `(列數, 欄數)` |
| 取一欄 | `df["age"]` | 回傳 Series |
| 取多欄 | `df[["age", "sex"]]` | 回傳 DataFrame |
| 篩選列 | `df[df["age"] > 80]` | 布林索引 |
| 可讀篩選 | `df.query("age > 80")` | 字串語法，適合 chaining |
| 新增欄位 | `df["new"] = ...` | 直接賦值 |
| 新增（鏈式） | `df.assign(new=...)` | 適合 method chaining |
| 日期轉換 | `pd.to_datetime(df["col"])` | 文字 → datetime |
| 日期部分 | `df["col"].dt.year` | `.dt.month`, `.dt.day` |

**統計與聚合**

| 需求 | 語法 | 說明 |
|------|------|------|
| 頻率表 | `df["col"].value_counts()` | 每個值出現幾次 |
| 遺漏值 | `df.isnull().sum()` | 每欄遺漏值數量 |
| 填補遺漏 | `df["col"].fillna(0)` | 用 0 填補空值 |
| 分組統計 | `df.groupby("col").size()` | 每組計數 |
| 樞紐分析 | `pd.pivot_table(df, ...)` | Excel Pivot Table |
| 交叉表 | `pd.crosstab(df["a"], df["b"])` | 2×2 列聯表 |
| 前 N 大 | `df.nlargest(3, "col")` | 最大的 N 筆 |
| 排序 | `df.sort_values("col")` | 依欄位排序 |
| 四捨五入 | `df["col"].round(1)` | 保留 1 位小數 |

**資料整理**

| 需求 | 語法 | 說明 |
|------|------|------|
| 合併表格 | `pd.merge(df1, df2, on="key")` | VLOOKUP 等價物 |
| 去除重複 | `df.drop_duplicates("col")` | 依欄位去重 |
| 重新命名 | `df.rename(columns={"old": "new"})` | 改欄位名 |
| 文字大寫 | `df["col"].str.upper()` | `.str.lower()`, `.str.strip()` |
| 文字搜尋 | `df["col"].str.contains("pattern")` | 回傳 True/False |
| 自定義函數 | `df.apply(func, axis=1)` | 逐列套用函數 |

## 常見錯誤

1. **日期沒轉換**：`symptom_onset_date` 仍是字串，時間排序會亂掉（`"2026-01-09"` < `"2026-01-15"` 用字串排序碰巧正確，但 `"2026-1-9"` 就會出錯）
2. **忽略分母**：直接比病例數而不算侵襲率，大翼區天生病例多
3. **圖表缺標題/軸標籤**：讀者無法獨立解讀——任何圖表都要能「離開上下文也能看懂」
4. **混淆感染者與全體**：畫年齡分布時忘了區分
5. **`axis=0` 和 `axis=1` 搞反**：加總共病數用 `axis=1`（橫向），算每欄平均用 `axis=0`（直向）
6. **忘了 `.reset_index()`**：`groupby` 後的結果索引是分組欄位，需要 `reset_index()` 才能正常使用

## 練習本

- 資料處理課堂筆記：{ref}`02_data_wrangling_for_beginners.ipynb`
- 視覺化課堂筆記：{ref}`02_visualization_epi_charts.ipynb`
- 作業版：[`02_data_wrangling_exercise.ipynb`](exercises/02_data_wrangling_exercise.ipynb)
- 解答版（教師版）：[`02_data_wrangling_solution.ipynb`](solutions/02_data_wrangling_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/02_data_wrangling_solution.ipynb>)
