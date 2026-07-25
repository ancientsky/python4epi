# 14 實戰案例：退伍軍人症疫調報告

## 你將學到

- 如何從接到通報到完成結案報告，走完一次完整疫調流程
- 如何整合前 13 章學到的所有技能，串成一份前後呼應、有邏輯脈絡的敘事
- 如何產出「可行動」的分析結論——不是丟一堆圖表，而是給長官一個能做決定的答案
- 如何把圖表和摘要數字**一鍵輸出成 PPTX 簡報 / DOCX 報告**，不再手動截圖貼投影片

## 情境故事

一切從那通電話開始。

> 2026 年 1 月中旬，你接到松柏護理之家的通報：近日多名住民出現肺炎症狀。
> 你帶著筆電趕到現場，開始進行流行病學調查。
> 現在，調查結束了——是時候把所有分析整合成一份正式的 **疫情調查報告**。

這一章就是最終考驗：用 Python 產出一份從頭到尾的疫調報告，而且不只是「寫出來」——是**跑一次程式就直接生出可以寄給長官的檔案**。

---

## 🧰 超白話特別篇：把前 14 章的工具，組裝成一份能上呈的報告

> 覺得「寫一份正式疫調報告」聽起來很嚇人、要從無到有寫一篇論文？別怕。這一章不教任何新招式——它是全書最後一次的「總複習」：把你已經學會的每一件工具，通通擺上同一張桌子，組成一道端得出去的菜。

### 疫調就是一場偵探辦案的總結報告

回想這十三章走過的路：你先像 Ch02 一樣把雜亂的原始資料整理成乾淨的 line list，再像 Ch03、Ch04 一樣算出侵襲率、畫出流行曲線，抓出「案發現場」的輪廓。接著 Ch05、Ch06 幫你排除「干擾因子」這種偽證人，Ch07、Ch08 把「案發時間」和「案發地點」釘死，Ch09 到 Ch12 則是動用更精密的鑑識工具——存活分析看死亡風險怎麼隨時間變化、機器學習抓出人眼漏看的交互作用、因果推論把「有關聯」講成「有理由相信是原因」。Ch13 教你把整套辦案過程寫成別人能重跑一次、得到同樣結論的紀錄。

**這一章要做的事，就是偵探辦案片的最後一幕：把所有物證攤開在會議桌上，講一次完整的案情，然後說出結論。**

### 工具箱 → 一桌菜

一套完整的工具箱擺在那裡不會自己變成一頓飯——要有人決定「這道菜配那道醬汁」，端出上得了檯面的一桌菜。疫調報告也一樣：每一章教的技能都是食材或器具，這一章負責把它們組裝、擺盤、端出去。

| 工具（章節） | 在報告裡的角色 | 回答的問題 |
|---|---|---|
| Line list 清理（Ch02） | 食材處理：把原始資料整理成一份乾淨的表 | 我們手上到底有什麼資料？ |
| 2×2 表／侵襲率（Ch03） | 開胃菜：先給一個總覽數字 | 這次疫情有多嚴重？ |
| 分層分析（Ch05） | 去骨：把干擾因子挑出來，看清真正的關聯 | 這個關聯是真的，還是被干擾因子混進來的假象？ |
| 邏輯斯迴歸（Ch06） | 主廚特調醬汁：同時校正多個因子 | 校正其他變項後，這個危險因子還顯著嗎？ |
| 時間序列（Ch07） | 主菜的敘事線：流行曲線說故事 | 疫情什麼時候開始、有沒有趨緩？ |
| 空間分析（Ch08） | 擺盤位置：地圖標出熱點 | 哪個樓層、哪個區域風險最高？ |
| 存活分析（Ch09） | 附餐點心：不只看有沒有死，還看多快 | 死亡風險怎麼隨時間變化？ |
| 機器學習／深度學習（Ch10、Ch11） | 甜點試驗：找出人眼看不出的交互作用 | 有沒有漏掉的危險因子？ |
| 因果推論（Ch12） | 主廚簽名：把「有關聯」講成「有理由相信是原因」 | 這真的是感染源，還是只是相關？ |
| 可重現報告（Ch13） | 出餐標準：同一張菜單，誰做都一樣 | 別人重跑一次程式，會得到同樣的結果嗎？ |

把這十道工序串起來，就是這一章要走的路——而且這次不只是「分析完就收工」，最後還要把成果**裝盤上桌**：一鍵輸出成 PPTX 簡報和 DOCX 報告（見本章壓軸段落）。

> ⚠️ **誠實話**：再多圖表、再花俏的模型，都不會讓一份報告變得有說服力。**報告真正的價值，在於「每個數字都有脈絡」+「每個結論都有行動建議」**——這也是為什麼本章最後特別把「常見誤用」整理成一張表，那些錯誤十之八九不是分析錯了，而是報告寫法錯了。

---

<!-- video: ch14_01_capstone_intuition -->
<!-- /video -->

## 報告架構：8 段落 ↔ 章節技能

一份標準的群聚調查報告（outbreak investigation report，或稱 SitRep／情勢報告）包含以下 8 個段落，每一段都對應到之前學過的章節技能：

```{figure} images/sitrep_report_map.svg
:name: fig-sitrep-report-map
:alt: 疫調報告 8 個段落與對應章節技能對照圖：1 背景與通報(Ch00,Ch04) 2 方法與 line list(Ch02) 3 描述性流行病學(Ch02–04) 4 分析性流行病學(Ch03,05,06) 5 時間與空間(Ch07,08) 6 進階分析：存活/ML/DL(Ch09–11) 7 因果研判與建議(Ch12) 8 結論與行動建議
:width: 100%

一份報告 = 前 14 章技能的總集成——每一段落背後，都是前面某一章教過的具體工具。
```

| 段落 | 對應章節 | 核心技能 |
|------|---------|---------|
| 1. 背景與通報 | Ch00, Ch04 | 個案定義、通報流程、群聚調查啟動時機 |
| 2. 方法 | Ch02 | 資料收集、line list 清理、衍生變項建立 |
| 3. 描述性流行病學 | Ch02–04 | 人時地分布（person-place-time）、流行曲線、侵襲率 |
| 4. 分析性流行病學 | Ch03, Ch05, Ch06 | 2×2 表、風險比、分層分析、邏輯斯迴歸（adjusted OR） |
| 5. 時間空間分析 | Ch07, Ch08 | 時間序列分解、空間熱點分布 |
| 6. 進階分析 | Ch09–11 | 存活分析、機器學習特徵重要性、深度學習全景 |
| 7. 因果研判與建議 | Ch12 | 因果推論框架、感染源研判、介入措施建議 |
| 8. 結論 | 總整理 | 結案摘要、可行動的具體建議 |

---

<!-- video: ch14_02_report_structure -->
<!-- /video -->

## 主要發現摘要

在 notebook 中，你將產出以下關鍵數字：

- **280** 位住民，**121** 人感染（侵襲率 **43.2%**）
- **19** 人死亡（致死率 **15.7%**）
- 發病高峰：**2026-01-19 至 01-22**
- 高風險區域：**2F-A**（54.5%）、**3F-B**（57.4%）
- 主要危險因子：**淋浴使用**（adjusted OR > 1，校正年齡、性別、共病後仍顯著）
- 結論：**淋浴供水系統為最可能的感染源**

這些數字不是各自獨立的——它們是同一條敘事線上的環節：流行曲線的形狀指向「共同暴露源」，空間熱點指向「特定樓層水管系統」，暴露分析和分層分析排除了「臥床者不淋浴、感染率也低」的競爭假說，最後因果研判把這條線收尾成一句可以寫進結案報告的結論。

---

<!-- video: ch14_03_key_findings -->
<!-- /video -->

## 把圖表輸出成 PPTX / DOCX 報告

分析做完、結論也寫好了，但長官要看的通常不是 notebook，而是一份可以直接上呈的簡報或 Word 報告。傳統做法是把圖表一張張截圖，手動貼進 PowerPoint、Word——資料一更新就要整套重做一遍，還很容易貼錯版本、漏改數字。

更好的做法是用 `python-pptx` / `python-docx` 直接把算好的圖表和數字**程式化組成報告**：完全不需要複製貼上，而且**可重現**——這正是 Ch13 那句話的延伸：只要重新執行一次 notebook，報告就會用最新資料重新產生一次，結果永遠跟分析同步。

```{figure} images/report_export_flow.svg
:name: fig-report-export-flow
:alt: 報告輸出流程圖：分析產出的圖表、表格、關鍵數字，透過 io.BytesIO 轉成記憶體中的 PNG 圖片，分別餵給 python-pptx 和 python-docx，一次產出 SitRep.pptx 簡報與報告.docx 文件
:width: 100%

分析產出（圖表／表格／關鍵數字）→ 存進記憶體 PNG（`io.BytesIO`）→ `python-pptx` / `python-docx` → 一鍵產出簡報與 Word 報告。
```

以下用一張圖（淋浴暴露 vs. 侵襲率）和一組摘要數字，示範同時輸出一份 `.pptx` 簡報和一份 `.docx` 報告——完整版（含流行曲線、多張圖表）請見 `notebooks/14_case_study_legionella.ipynb` 的匯出段落。

```python
import io
import os
import tempfile

import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches
from docx import Document
from docx.shared import Inches as DInches

# 沿用本章前面小節已經算好的 cases / n_total / n_infected / n_deaths

# 1. 把 matplotlib 圖存成記憶體裡的 PNG，不落地成檔案
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(["未淋浴", "淋浴"], [ar_no_shower, ar_shower], color=["#6A9BCC", "#D97757"])
ax.set_ylabel("侵襲率 (%)")
ax.set_title("淋浴使用 vs 侵襲率")

buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
plt.close(fig)
buf.seek(0)

summary_rows = [
    ("住民數", f"{n_total}"),
    ("感染", f"{n_infected}（{n_infected / n_total:.1%}）"),
    ("死亡", f"{n_deaths}（{n_deaths / n_infected:.1%}）"),
]
outdir = tempfile.mkdtemp(prefix="sitrep_")

# 2. python-pptx：標題投影片 + 圖表／表格投影片
prs = Presentation()
slide1 = prs.slides.add_slide(prs.slide_layouts[0])
slide1.shapes.title.text = "松柏護理之家退伍軍人症群聚 SitRep"
slide1.placeholders[1].text = (
    f"侵襲率 {n_infected / n_total:.1%}｜致死率 {n_deaths / n_infected:.1%}"
)

slide2 = prs.slides.add_slide(prs.slide_layouts[5])
buf.seek(0)   # BytesIO 只能讀一次，插入圖片前一定要重設游標
slide2.shapes.add_picture(buf, Inches(0.4), Inches(1.1), width=Inches(6))

tbl = slide2.shapes.add_table(
    len(summary_rows) + 1, 2, Inches(6.8), Inches(1.1), Inches(2.7), Inches(1.6)
).table
tbl.cell(0, 0).text, tbl.cell(0, 1).text = "項目", "數值"
for i, (label, value) in enumerate(summary_rows, start=1):
    tbl.cell(i, 0).text, tbl.cell(i, 1).text = label, value

prs.save(os.path.join(outdir, "legionella_sitrep.pptx"))

# 3. python-docx：同一套素材，換成 Word 報告
doc = Document()
doc.add_heading("松柏護理之家退伍軍人症群聚調查報告", level=0)

doc.add_heading("摘要", level=1)
doc.add_paragraph(
    f"本次群聚事件共 {n_total} 位住民，{n_infected} 人感染"
    f"（侵襲率 {n_infected / n_total:.1%}），{n_deaths} 人死亡"
    f"（致死率 {n_deaths / n_infected:.1%}）。推定感染源為淋浴供水系統。"
)

doc.add_heading("淋浴暴露 vs 侵襲率", level=1)
buf.seek(0)   # 同一份 BytesIO 在 PPTX 那格已讀過一次，這裡要再 seek(0) 才能重讀
doc.add_picture(buf, width=DInches(5.5))

doc.add_heading("關鍵數字", level=1)
table = doc.add_table(rows=1, cols=2, style="Light Grid Accent 1")
table.rows[0].cells[0].text, table.rows[0].cells[1].text = "項目", "數值"
for label, value in summary_rows:
    row = table.add_row()
    row.cells[0].text, row.cells[1].text = label, value

doc.save(os.path.join(outdir, "legionella_sitrep.docx"))

print(f"已輸出：{outdir}")
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `fig.savefig(buf, format="png", ...); buf.seek(0)` | 圖表存進記憶體 `BytesIO`，不用先寫進硬碟，就能直接塞進報告 |
> | `prs.slides.add_slide(prs.slide_layouts[0])` | 版面 0 = 標題投影片，內建主標題與副標題 placeholder |
> | `prs.slides.add_slide(prs.slide_layouts[5])` | 版面 5 = 空白投影片，自己用 textbox／picture／table 排版 |
> | `slide2.shapes.add_picture(buf, ...)` | 把記憶體裡的 PNG 直接插入投影片，不需要先存成檔案 |
> | `slide2.shapes.add_table(rows, cols, ...).table` | 在投影片上畫一個表格，逐列填入 `summary_rows` |
> | `buf.seek(0)`（第二次出現） | **`BytesIO` 只能讀一次**：PPTX 用過後游標停在檔案尾端，DOCX 要再讀之前必須先倒回開頭，否則會插入一張空白圖 |
> | `doc.add_heading(..., level=0)` / `level=1` | Word 的「標題」樣式（主標題）／「標題 1」樣式（小節標題） |
> | `doc.add_picture(buf, width=DInches(5.5))` | 插入同一張圖；`DInches` 是 `docx.shared.Inches` 的別名，避免跟 pptx 的 `Inches` 撞名 |
> | `doc.add_table(rows=1, cols=2, style="Light Grid Accent 1")` | 建一個套用內建樣式的表格，先放表頭，之後用 `add_row()` 逐列加資料 |
> | `tempfile.mkdtemp(prefix="sitrep_")` | 輸出到系統暫存資料夾，不寫進專案目錄，不會被 git 追蹤到 |

> 🎁 **洞見**：程式化產報告 = **一鍵重跑、格式一致、零手工錯誤**。資料更新、結論修正，重新執行一次程式就能重新產生格式一致的簡報和 Word 報告——不用再手動截圖貼投影片，也不會再有「這份報告用的是哪一版的圖」這種疑問。完整流程（含流行曲線、空間熱力圖、更多欄位）請直接執行 [`14_case_study_legionella.ipynb`](notebooks/14_case_study_legionella.ipynb)，最後一段就是可以直接跑出 `.pptx` 與 `.docx` 檔案的完整版本。

<!-- video: ch14_04_export_pptx -->
<!-- /video -->

<!-- video: ch14_05_export_docx -->
<!-- /video -->

## 練習題

- 作業版：[`14_case_study_exercise.ipynb`](exercises/14_case_study_exercise.ipynb)
- 解答版（講師）：[`14_case_study_solution.ipynb`](solutions/14_case_study_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/14_case_study_solution.ipynb>)

## 常見誤用

| 錯誤 | 正確做法 |
|------|----------|
| 只列數字，不給脈絡 | 每個數字都附上比較基準（如全國 CFR、往年侵襲率） |
| 圖表太多，缺乏重點 | 挑 3–5 張關鍵圖表，每張都有明確結論，不是「有算就放上去」 |
| 分析做完就結束 | 一定要有「行動建議」段落——報告要能讓人「照著做」，不只是「知道了」 |
| 報告格式不一致 | 使用標準疫調報告格式（8 段落），每次產出的簡報／文件排版一致 |
| 手動截圖、複製貼上圖表 | 用 `python-pptx` / `python-docx` 程式化輸出，資料更新只要重跑一次 |

## 下一步

恭喜！完成這章代表你已經具備用 Python 進行疫情調查、並產出可上呈報告的完整能力——從接獲通報、清理資料、描述分析、統計推論、時空建模，一路到因果研判與自動化報告輸出。
附錄（Ch15）收錄進階術語與參考資源，Ch16／Ch17 則是全書練習題與解答的總覽區。
