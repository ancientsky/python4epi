# 04 群聚調查工作流：從 Line List 到 SitRep

## 情境

松柏護理之家退伍軍人症群聚事件爆發後第三天下午，你的長官說：

> 「兩小時內交出第一份疫情日報（SitRep），內容要包含：多少人感染、哪裡最嚴重、致死率多少、流行曲線長什麼樣。之後每天早上九點前更新。」

你手上有一份 280 筆 × 32 欄的 line list CSV。這一章教你如何用 Python **自動化**產出一份結構化的 SitRep，而且每天只要重跑一次腳本就能更新。

## 你將學到

- 從 raw line list 到 SitRep 的完整自動化流程
- 描述性流行病學三要素：**人、時、地**
- 關鍵指標計算：侵襲率、CFR、住院率、ICU 率
- 按個案分類（確診/可能/非個案）分層摘要
- 輸出結構化報告（含表格 + 圖表）
- 把分析流程做成可重跑腳本

## SitRep 的基本架構

一份標準的疫情日報至少包含：

1. **摘要指標**：截至目前的累計數字
2. **人**（Person）：年齡、性別、共病分布
3. **時**（Time）：流行曲線、新增趨勢
4. **地**（Place）：按地點的侵襲率比較
5. **行動建議**：根據數據的初步判斷

---

## Step 1: 讀取與資料準備

```python
import pandas as pd
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

df = pd.read_csv("data/synthetic/legionella_outbreak.csv")

# 日期轉換
date_cols = [
    "facility_admission_date", "symptom_onset_date",
    "hospitalization_date", "death_date", "notification_date",
]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# 衍生變項
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)
df["age_group"] = pd.cut(
    df["age"], bins=[59, 69, 79, 89, 100],
    labels=["60-69", "70-79", "80-89", "90+"],
)
comorbidity_cols = [
    "comorbidity_chf", "comorbidity_dm",
    "comorbidity_cancer", "comorbidity_copd", "immunosuppressed",
]
df["n_comorbidities"] = df[comorbidity_cols].sum(axis=1)
```

## Step 2: 摘要指標

```python
total = len(df)
infected = df["infected"].sum()
confirmed = (df["case_classification"] == "confirmed").sum()
probable = (df["case_classification"] == "probable").sum()
hospitalized = df["hospitalized"].sum()
icu = df["icu_admission"].sum()
deaths = (df["outcome"] == "dead").sum()

print("=" * 50)
print("松柏護理之家退伍軍人症群聚 — SitRep")
print("=" * 50)
print(f"住民總數：{total}")
print(f"感染人數：{infected}（侵襲率 {infected/total:.1%}）")
print(f"  確診：{confirmed}　可能：{probable}")
print(f"住院：{hospitalized}（住院率 {hospitalized/infected:.1%}）")
print(f"ICU：{icu}（ICU 率 {icu/hospitalized:.1%}）")
print(f"死亡：{deaths}（CFR {deaths/infected:.1%}）")
```

## Step 3: 人 — Person

```python
cases = df[df["infected"] == 1]

print("=== 人口學特徵（感染者）===")
print(f"年齡中位數：{cases['age'].median():.0f} 歲"
      f"（範圍 {cases['age'].min()}-{cases['age'].max()}）")
print(f"男性比例：{(cases['sex'] == 'M').mean():.1%}")
print(f"\n--- 年齡組分布 ---")
print(cases["age_group"].value_counts().sort_index().to_string())
print(f"\n--- 共病分布 ---")
for col in comorbidity_cols:
    label = col.replace("comorbidity_", "").upper()
    n = cases[col].sum()
    print(f"  {label}: {n} ({n/len(cases):.1%})")
```

## Step 4: 時 — Time

```python
import matplotlib.dates as mdates

daily = cases.groupby("symptom_onset_date").size().rename("cases")

# 補齊完整日期範圍（含爆發前 3 天背景期）
date_range = pd.date_range(
    daily.index.min() - pd.Timedelta(days=3),
    daily.index.max() + pd.Timedelta(days=1),
    freq="D",
)
daily = daily.reindex(date_range, fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(daily.index, daily.values, width=1.0,
       color="#2c7fb8", edgecolor="white", linewidth=0.5)
ax.set_title("松柏護理之家退伍軍人症流行曲線，依發病日，2026 年 1 月",
             fontsize=13, fontweight="bold")
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

print(f"流行期間：{cases['symptom_onset_date'].min().date()} – {cases['symptom_onset_date'].max().date()}")
print(f"高峰日：{daily.idxmax().date()}（{daily.max()} 例）")
```

## Step 5: 地 — Place

```python
wing_stats = (
    df.groupby(["floor", "wing"])
    .agg(
        residents=("case_id", "size"),
        infected=("infected", "sum"),
        deaths=("outcome", lambda x: (x == "dead").sum()),
    )
    .reset_index()
)
wing_stats["AR%"] = (wing_stats["infected"] / wing_stats["residents"] * 100).round(1)
wing_stats["CFR%"] = (wing_stats["deaths"] / wing_stats["infected"] * 100).round(1)
wing_stats["label"] = wing_stats["floor"].astype(str) + wing_stats["wing"]

print("=== 各翼區疫情摘要 ===")
print(wing_stats[["label", "residents", "infected", "AR%", "deaths", "CFR%"]]
      .to_string(index=False))
```

## Step 6: 個案分類分層摘要

```python
classification = (
    df.groupby("case_classification")
    .agg(
        n=("case_id", "size"),
        hospitalized=("hospitalized", "sum"),
        icu=("icu_admission", "sum"),
        deaths=("outcome", lambda x: (x == "dead").sum()),
    )
)
classification["hosp_rate"] = (
    classification["hospitalized"] / classification["n"] * 100
).round(1)

print("=== 按個案分類分層 ===")
print(classification.to_string())
```

## Step 7: 輸出結構化 SitRep

把以上所有步驟包成一個函式，每天重跑即可更新：

```python
def generate_sitrep(csv_path):
    """從 CSV 產出 SitRep 摘要字典。"""
    df = pd.read_csv(csv_path)
    for col in ["symptom_onset_date", "hospitalization_date",
                "death_date", "notification_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

    total = len(df)
    infected = int(df["infected"].sum())
    deaths = int((df["outcome"] == "dead").sum())

    return {
        "total_residents": total,
        "infected": infected,
        "attack_rate": round(infected / total * 100, 1),
        "deaths": deaths,
        "cfr": round(deaths / infected * 100, 1) if infected else 0,
        "hospitalized": int(df["hospitalized"].sum()),
        "icu": int(df["icu_admission"].sum()),
    }

sitrep = generate_sitrep("data/synthetic/legionella_outbreak.csv")
print(sitrep)
```

## Step 8: 產出專業報告

`generate_sitrep()` 回傳的字典就是你的**資料層**。但長官看不懂 Python dict——他要的是一份漂亮的報告。這一步教你用四種格式把分析結果包裝成專業輸出：

| 格式 | 適合場景 | Python 套件 |
|------|---------|------------|
| 互動儀表板 | 即時檢視、團隊內部討論 | plotly（已安裝） |
| Word 文件 (.docx) | 交給主管、email 附件 | python-docx |
| 簡報投影片 (.pptx) | 疫調會議簡報 | python-pptx |
| PDF 報告 | 正式歸檔、列印 | fpdf2 |

### 共用前置：儲存圖表與建立輸出資料夾

```python
import pathlib
from io import BytesIO
from datetime import datetime

# 建立輸出資料夾（不會進 git）
pathlib.Path("output").mkdir(exist_ok=True)

# 重新產生流行曲線（Step 4 的 fig），存入記憶體緩衝區
# 這樣 DOCX / PPTX / PDF 都能直接嵌入，不用寫暫存檔
epicurve_buf = BytesIO()
fig.savefig(epicurve_buf, format="png", dpi=150, bbox_inches="tight")
epicurve_buf.seek(0)

# 報告時間戳記
report_time = datetime.now().strftime("%Y-%m-%d %H:%M")
```

### 8a: 互動式儀表板（Plotly Dashboard）

```{note}
在 JupyterLab / Google Colab 中，以下圖表是**互動的**（可縮放、懸停檢視數值）。在 Jupyter Book 靜態網頁中，你看到的是自動產生的靜態截圖。
```

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 建立 2×2 子圖面板
dashboard = make_subplots(
    rows=2, cols=2,
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}],
        [{"type": "xy"}, {"type": "xy"}],
    ],
    subplot_titles=("", "", "流行曲線（依發病日）", "各翼區侵襲率"),
    vertical_spacing=0.15,
    horizontal_spacing=0.1,
)

# ── 左上：感染人數 + 侵襲率 ──
dashboard.add_trace(
    go.Indicator(
        mode="number+delta",
        value=infected,
        title={"text": "感染人數（侵襲率）"},
        number={"suffix": f"  ({infected/total:.1%})"},
        delta={"reference": 0, "position": "bottom"},
    ),
    row=1, col=1,
)

# ── 右上：死亡人數 + CFR ──
dashboard.add_trace(
    go.Indicator(
        mode="number+delta",
        value=deaths,
        title={"text": "死亡人數（CFR）"},
        number={"suffix": f"  ({deaths/infected:.1%})"},
        delta={"reference": 0, "position": "bottom"},
    ),
    row=1, col=2,
)

# ── 左下：流行曲線 ──
daily_cases = cases.groupby("symptom_onset_date").size()
dashboard.add_trace(
    go.Bar(
        x=daily_cases.index,
        y=daily_cases.values,
        marker_color="#D97757",
        name="每日病例數",
    ),
    row=2, col=1,
)

# ── 右下：各翼區侵襲率（水平長條圖）──
dashboard.add_trace(
    go.Bar(
        y=wing_stats["label"],
        x=wing_stats["AR%"],
        orientation="h",
        marker_color="#6A9BCC",
        name="侵襲率 %",
        text=wing_stats["AR%"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
    ),
    row=2, col=2,
)

dashboard.update_layout(
    title_text=f"松柏護理之家退伍軍人症 SitRep Dashboard（{report_time}）",
    height=600,
    showlegend=False,
    template="plotly_white",
)
dashboard.show()
```

### 8b: Word 文件（DOCX）

> **注意**：套件名稱是 `python-docx`，但匯入時寫 `from docx import ...`——這是很多新手搞混的地方。

```python
from docx import Document
from docx.shared import Inches, Pt

doc = Document()

# ── 標題與時間 ──
doc.add_heading("松柏護理之家退伍軍人症 SitRep", level=1)
doc.add_paragraph(f"報告時間：{report_time}")
doc.add_paragraph(
    f"資料來源：legionella_outbreak.csv（{total} 筆住民資料）"
)

# ── 摘要指標表格 ──
doc.add_heading("摘要指標", level=2)
table = doc.add_table(rows=6, cols=2, style="Light Grid Accent 1")
metrics = [
    ("住民總數", str(total)),
    ("感染人數", f"{infected}（侵襲率 {infected/total:.1%}）"),
    ("確診", str(confirmed)),
    ("可能病例", str(probable)),
    ("住院", f"{hospitalized}（住院率 {hospitalized/infected:.1%}）"),
    ("死亡", f"{deaths}（CFR {deaths/infected:.1%}）"),
]
for i, (label, value) in enumerate(metrics):
    table.rows[i].cells[0].text = label
    table.rows[i].cells[1].text = value

# ── 嵌入流行曲線 ──
doc.add_heading("流行曲線", level=2)
epicurve_buf.seek(0)  # 重設讀取位置
doc.add_picture(epicurve_buf, width=Inches(6))

# ── 各翼區統計 ──
doc.add_heading("各翼區疫情摘要", level=2)
wing_table = doc.add_table(
    rows=len(wing_stats) + 1, cols=5, style="Light Grid Accent 1"
)
headers = ["翼區", "住民數", "感染數", "侵襲率%", "CFR%"]
for j, h in enumerate(headers):
    wing_table.rows[0].cells[j].text = h
for i, row in wing_stats.iterrows():
    wing_table.rows[i + 1].cells[0].text = str(row["label"])
    wing_table.rows[i + 1].cells[1].text = str(row["residents"])
    wing_table.rows[i + 1].cells[2].text = str(row["infected"])
    wing_table.rows[i + 1].cells[3].text = str(row["AR%"])
    wing_table.rows[i + 1].cells[4].text = str(row["CFR%"])

doc.save("output/sitrep_report.docx")
print("✅ Word 報告已儲存：output/sitrep_report.docx")
```

### 8c: 簡報投影片（PPTX）

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()

# ── 投影片 1：標題頁 ──
slide1 = prs.slides.add_slide(prs.slide_layouts[0])  # 標題版面
slide1.shapes.title.text = "松柏護理之家退伍軍人症 SitRep"
slide1.placeholders[1].text = f"報告時間：{report_time}"

# ── 投影片 2：關鍵數據（使用空白版面 + 文字方塊）──
slide2 = prs.slides.add_slide(prs.slide_layouts[5])  # 空白版面
txBox = slide2.shapes.add_textbox(
    Inches(1), Inches(0.5), Inches(8), Inches(1),
)
txBox.text_frame.text = "關鍵摘要指標"
txBox.text_frame.paragraphs[0].font.size = Pt(28)
txBox.text_frame.paragraphs[0].font.bold = True

# 加入指標文字
body = slide2.shapes.add_textbox(
    Inches(1), Inches(1.8), Inches(8), Inches(4),
)
tf = body.text_frame
tf.word_wrap = True
kpi_lines = [
    f"感染人數：{infected}（侵襲率 {infected/total:.1%}）",
    f"確診：{confirmed}　可能病例：{probable}",
    f"住院：{hospitalized}　ICU：{icu}",
    f"死亡：{deaths}（CFR {deaths/infected:.1%}）",
]
for line in kpi_lines:
    p = tf.add_paragraph()
    p.text = line
    p.font.size = Pt(20)
    p.space_after = Pt(12)

# ── 投影片 3：流行曲線 ──
slide3 = prs.slides.add_slide(prs.slide_layouts[5])
txBox3 = slide3.shapes.add_textbox(
    Inches(1), Inches(0.3), Inches(8), Inches(0.8),
)
txBox3.text_frame.text = "流行曲線（依發病日）"
txBox3.text_frame.paragraphs[0].font.size = Pt(24)
txBox3.text_frame.paragraphs[0].font.bold = True

epicurve_buf.seek(0)
slide3.shapes.add_picture(epicurve_buf, Inches(0.5), Inches(1.3), Inches(9), Inches(5))

# ── 投影片 4：各翼區侵襲率 ──
slide4 = prs.slides.add_slide(prs.slide_layouts[5])
txBox4 = slide4.shapes.add_textbox(
    Inches(1), Inches(0.3), Inches(8), Inches(0.8),
)
txBox4.text_frame.text = "各翼區疫情摘要"
txBox4.text_frame.paragraphs[0].font.size = Pt(24)
txBox4.text_frame.paragraphs[0].font.bold = True

# 建立表格
rows_n = len(wing_stats) + 1
tbl = slide4.shapes.add_table(rows_n, 5, Inches(0.5), Inches(1.3), Inches(9), Inches(4)).table
for j, h in enumerate(["翼區", "住民", "感染", "AR%", "CFR%"]):
    tbl.cell(0, j).text = h
for i, row in wing_stats.iterrows():
    tbl.cell(i + 1, 0).text = str(row["label"])
    tbl.cell(i + 1, 1).text = str(row["residents"])
    tbl.cell(i + 1, 2).text = str(row["infected"])
    tbl.cell(i + 1, 3).text = str(row["AR%"])
    tbl.cell(i + 1, 4).text = str(row["CFR%"])

prs.save("output/sitrep_slides.pptx")
print("✅ 簡報已儲存：output/sitrep_slides.pptx")
```

### 8d: PDF 正式報告（fpdf2）

```python
import pathlib
from fpdf import FPDF

# ── CJK 字型偵測（跟 matplotlib 一樣，要找中文字型才能顯示中文）──
cjk_font_path = None
for font_dir in ["/usr/share/fonts", "/usr/local/share/fonts"]:
    for fp in sorted(pathlib.Path(font_dir).rglob("*")):
        if fp.suffix.lower() in {".ttf", ".ttc"} and (
            "CJK" in fp.name or "WenQuanYi" in fp.name or "wqy" in fp.name
        ):
            cjk_font_path = str(fp)
            break
    if cjk_font_path:
        break

pdf = FPDF()
pdf.add_page()

# 註冊中文字型（如果找到的話）
if cjk_font_path:
    pdf.add_font("CJK", "", cjk_font_path)
    pdf.set_font("CJK", size=16)
else:
    pdf.set_font("Helvetica", size=16)
    print("⚠️ 未找到 CJK 字型，中文可能無法顯示。請安裝 fonts-noto-cjk")

# ── 標題 ──
pdf.cell(0, 12, text="松柏護理之家退伍軍人症 SitRep", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font_size(10)
pdf.cell(0, 8, text=f"報告時間：{report_time}", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(8)

# ── 摘要指標 ──
pdf.set_font_size(13)
pdf.cell(0, 10, text="摘要指標", new_x="LMARGIN", new_y="NEXT")
pdf.set_font_size(10)
kpi_lines = [
    f"住民總數：{total}",
    f"感染人數：{infected}（侵襲率 {infected/total:.1%}）",
    f"確診：{confirmed}　可能病例：{probable}",
    f"住院：{hospitalized}（住院率 {hospitalized/infected:.1%}）",
    f"死亡：{deaths}（CFR {deaths/infected:.1%}）",
]
for line in kpi_lines:
    pdf.cell(0, 7, text=line, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

# ── 嵌入流行曲線 ──
pdf.set_font_size(13)
pdf.cell(0, 10, text="流行曲線", new_x="LMARGIN", new_y="NEXT")
epicurve_buf.seek(0)
epicurve_tmp = pathlib.Path("output/epicurve_tmp.png")
epicurve_tmp.write_bytes(epicurve_buf.read())
pdf.image(str(epicurve_tmp), w=pdf.w - 30)
epicurve_tmp.unlink()  # 刪除暫存檔
pdf.ln(5)

# ── 各翼區統計表 ──
pdf.add_page()
pdf.set_font_size(13)
pdf.cell(0, 10, text="各翼區疫情摘要", new_x="LMARGIN", new_y="NEXT")
pdf.set_font_size(9)

# 表頭
col_widths = [25, 25, 25, 30, 30]
headers = ["翼區", "住民", "感染", "侵襲率%", "CFR%"]
for w, h in zip(col_widths, headers):
    pdf.cell(w, 8, text=h, border=1, align="C")
pdf.ln()

# 表格內容
for _, row in wing_stats.iterrows():
    vals = [str(row["label"]), str(row["residents"]), str(row["infected"]),
            str(row["AR%"]), str(row["CFR%"])]
    for w, v in zip(col_widths, vals):
        pdf.cell(w, 7, text=v, border=1, align="C")
    pdf.ln()

pdf.output("output/sitrep_report.pdf")
print("✅ PDF 報告已儲存：output/sitrep_report.pdf")
```

> **小結**：四種格式各有適用場景。互動儀表板適合團隊內部即時檢視，DOCX 適合 email 給長官，PPTX 適合疫調會議簡報，PDF 適合正式歸檔。在實務中，你可以把這些程式碼整合進 `run_sitrep.py`，每天更新 CSV 後重跑一次，就能同時產出四種格式的最新報告。

---

## 常見錯誤

1. **每天改定義**：個案定義（case definition）一旦確定就不要改，否則趨勢不可比
2. **只放圖不放表**：SitRep 必須有可查核的數字表格
3. **忘記標註資料截止時間**：每份報告都要註明「資料截至 YYYY-MM-DD HH:MM」
4. **侵襲率沒算分母**：直接比較病例數不公平，要除以各翼區住民數

## 進階：可重跑腳本

```bash
uv run python notebooks/run_sitrep.py
```

把整個 SitRep 流程存成 `.py` 腳本，每天更新 CSV 後重跑一次就能自動產出最新日報。

## 練習本

- 課堂筆記：{ref}`04_outbreak_workflow.ipynb`
- 作業版：[`04_outbreak_workflow_exercise.ipynb`](exercises/04_outbreak_workflow_exercise.ipynb)
- 解答版（教師版）：[`04_outbreak_workflow_solution.ipynb`](solutions/04_outbreak_workflow_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/04_outbreak_workflow_solution.ipynb>)
