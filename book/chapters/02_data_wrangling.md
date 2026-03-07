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

## Part 1：資料處理

### Step 1: 讀入 line list

```python
import pandas as pd

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
print(f"資料維度：{df.shape[0]} 筆 × {df.shape[1]} 欄")
df.head()
```

### Step 2: 檢視資料結構

```python
df.info()
```

```python
df.describe()
```

重點觀察：哪些欄位有遺漏值？數值欄位的範圍合理嗎？

### Step 3: 日期轉換

line list 中有 5 個日期欄位，讀入時是文字，必須轉成 datetime 才能做時間分析。

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

### Step 4: 建立衍生變項

疫調分析常需要從原始資料衍生新變項：

```python
# 1) 年齡組
df["age_group"] = pd.cut(
    df["age"],
    bins=[59, 69, 79, 89, 100],
    labels=["60-69", "70-79", "80-89", "90+"],
)

# 2) 共病數
comorbidity_cols = [
    "comorbidity_chf", "comorbidity_dm",
    "comorbidity_cancer", "comorbidity_copd",
    "immunosuppressed",
]
df["n_comorbidities"] = df[comorbidity_cols].sum(axis=1)

# 3) 是否感染（二元變項）
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# 4) 發病到住院天數
df["onset_to_hosp_days"] = (
    df["hospitalization_date"] - df["symptom_onset_date"]
).dt.days

# 5) 流行病學週
df["epi_week"] = df["symptom_onset_date"].dt.isocalendar().week
```

### Step 5: 處理遺漏值

未感染者不會有 `symptom_onset_date`、`hospitalization_date` 等，這些 NaT 不是資料錯誤而是合理的結構性遺漏。

```python
# 確認：未感染者的 onset 日期應全為空
print("未感染者有 onset 日期的數量：",
      df.loc[df["infected"] == 0, "symptom_onset_date"].notna().sum())
```

### Step 6: groupby 分組統計

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

---

## Part 2：視覺化

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

# -- CJK font setup (避免中文標籤顯示為方框) --
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
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

```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(
    data=df, x="age", hue="infected", bins=15,
    multiple="stack", palette={0: "#cccccc", 1: "#e34a33"}, ax=ax,
)
ax.set_title("年齡分布：感染 vs 未感染")
ax.set_xlabel("年齡")
ax.set_ylabel("人數")
ax.legend(title="感染", labels=["未感染", "感染"])
plt.tight_layout()
plt.show()
```

### Step 9: 翼區侵襲率長條圖（seaborn）

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
ax.set_title("臨床嚴重度 × 共病數")
ax.set_xlabel("共病數")
ax.set_ylabel("嚴重度")
plt.tight_layout()
plt.show()
```

### Step 11: 互動式分層流行曲線（Plotly）

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

## 圖表解讀重點

| 圖表 | 觀察重點 |
|------|---------|
| 流行曲線 | 峰值時間、上升/下降速度 → 傳播模式 |
| 年齡分布 | 感染者是否集中在特定年齡層 |
| 翼區長條圖 | 哪些翼區侵襲率異常偏高 → 空間線索 |
| 嚴重度×共病 | 共病多的人是否更容易重症 |
| 互動曲線 | 各樓層的流行高峰是否同步 |

## 常見錯誤

1. **日期沒轉換**：`symptom_onset_date` 仍是字串，時間排序會亂掉
2. **忽略分母**：直接比病例數而不算侵襲率，大翼區天生病例多
3. **圖表缺標題/軸標籤**：讀者無法獨立解讀
4. **混淆感染者與全體**：畫年齡分布時忘了區分

## 練習本

- 資料處理課堂筆記：{ref}`02_data_wrangling_for_beginners.ipynb`
- 視覺化課堂筆記：{ref}`02_visualization_epi_charts.ipynb`
- 作業版：[`02_data_wrangling_exercise.ipynb`](../exercises/02_data_wrangling_exercise.ipynb)
- 解答版（教師版）：[`02_data_wrangling_solution.ipynb`](../solutions/02_data_wrangling_solution.ipynb)
