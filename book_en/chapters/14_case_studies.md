# 14 Case Study: A Legionnaires' Disease Outbreak Investigation Report

## What You'll Learn

- How to walk through a complete outbreak investigation, from receiving the notification to finishing the final report
- How to integrate every skill learned in the previous 13 chapters into one narrative with a clear, continuous thread
- How to produce "actionable" analytic conclusions — not a pile of charts, but an answer your supervisor can actually act on
- How to export charts and summary numbers **directly into a PPTX slide deck / DOCX report with one click** — no more manually screenshotting into slides

## The Scenario

It all started with that phone call.

> In mid-January 2026, you receive a notification from Songbai Nursing Home: several residents have recently developed pneumonia symptoms.
> You grab your laptop, rush to the site, and begin an epidemiological investigation.
> Now the investigation is over — it's time to pull all of your analyses together into a formal **outbreak investigation report**.

This chapter is the final challenge: use Python to produce a complete, end-to-end outbreak investigation report — and not just "write it up." You'll **run the program once and it hands you a file ready to send to your supervisor.**

---

## 🧰 Super-Simple Special: Assembling the Tools from the Last 14 Chapters into a Report You Can Submit

> Does "writing a formal outbreak report" sound intimidating — like writing a paper from a blank page? Don't worry. This chapter doesn't teach any new moves — it's the book's final "grand review": every tool you've already learned gets laid out on the same table and assembled into a dish you can actually serve.

### An outbreak investigation is a detective's closing report

Think back over the thirteen chapters you've walked through: first, like in Ch02, you cleaned messy raw data into a tidy line list; then, like Ch03 and Ch04, you calculated attack rates and drew epidemic curves to sketch the outline of the "crime scene." Next, Ch05 and Ch06 helped you rule out confounders — those false witnesses — while Ch07 and Ch08 pinned down "when" and "where" it happened. Ch09 through Ch12 brought out more precise forensic tools: survival analysis to see how mortality risk changes over time, machine learning to catch interactions the naked eye misses, causal inference to turn "there's an association" into "there's reason to believe this is the cause." Ch13 taught you to write up the whole investigation so someone else can rerun it and land on the same conclusion.

**This chapter is the final scene of the detective drama: lay all the evidence out on the conference table, tell the whole story once, and state the conclusion.**

### From toolbox to table

A complete toolbox doesn't turn itself into a meal — someone has to decide "which sauce pairs with which dish" and plate a table you can actually serve. An outbreak report is the same: every skill from every chapter is an ingredient or a utensil, and this chapter's job is to assemble, plate, and serve them.

| Tool (chapter) | Role in the report | Question it answers |
|---|---|---|
| Line-list cleaning (Ch02) | Prep work: turning raw data into a clean table | What data do we actually have? |
| 2×2 table / attack rate (Ch03) | Appetizer: a headline number up front | How severe is this outbreak? |
| Stratified analysis (Ch05) | Deboning: pulling out confounders to see the real association | Is this association real, or a false one smuggled in by a confounder? |
| Logistic regression (Ch06) | The chef's signature sauce: adjusting for several factors at once | After adjusting for other variables, is this risk factor still significant? |
| Time series (Ch07) | The main course's narrative arc: the epidemic curve tells the story | When did the outbreak start, and is it slowing down? |
| Spatial analysis (Ch08) | Plating: the map marks the hotspots | Which floor, which zone, carries the highest risk? |
| Survival analysis (Ch09) | The side dish: not just whether someone died, but how fast | How does mortality risk change over time? |
| Machine learning / deep learning (Ch10, Ch11) | Dessert tasting: finding interactions the naked eye misses | Are there risk factors we overlooked? |
| Causal inference (Ch12) | The chef's signature: turning "there's an association" into "there's reason to believe this is the cause" | Is this really the source of infection, or just correlated with it? |
| Reproducible reporting (Ch13) | Kitchen standards: the same menu, no matter who cooks it | Would someone else rerunning the code get the same results? |

String these ten steps together and that's the path this chapter walks — and this time it's not "done analyzing, done working." The last step is to **plate it and put it on the table**: exporting everything into a PPTX deck and a DOCX report with one click (see the finale of this chapter).

> ⚠️ **An honest word**: no number of charts, and no fancy model, will by itself make a report persuasive. **A report's real value comes from "every number has context" + "every conclusion has an action attached to it"** — which is exactly why this chapter closes with a table of common misuses. Nine times out of ten, those mistakes aren't analysis errors — they're report-writing errors.

---

## Report Structure: 8 Sections ↔ Chapter Skills

A standard outbreak investigation report (also called a SitRep, or situation report) contains the following 8 sections, each mapped to a skill from an earlier chapter:

```{figure} images/sitrep_report_map_en.svg
:name: fig-sitrep-report-map
:alt: Diagram mapping the 8 sections of an outbreak report to their corresponding chapter skills: 1 Background & Notification (Ch00, Ch04) 2 Methods & line list (Ch02) 3 Descriptive Epidemiology (Ch02-04) 4 Analytic Epidemiology (Ch03, 05, 06) 5 Time & Space (Ch07, 08) 6 Advanced analysis: survival/ML/DL (Ch09-11) 7 Causal judgment & recommendations (Ch12) 8 Conclusion & action recommendations
:width: 100%

A report = the sum total of the skills from the first 14 chapters — behind every section stands a specific tool taught in an earlier chapter.
```

| Section | Related Chapters | Core Skills |
|------|---------|---------|
| 1. Background & Notification | Ch00, Ch04 | Case definition, notification workflow, outbreak-investigation trigger criteria |
| 2. Methods | Ch02 | Data collection, line-list cleaning, derived-variable construction |
| 3. Descriptive Epidemiology | Ch02–04 | Person-place-time distribution, epidemic curve, attack rate |
| 4. Analytic Epidemiology | Ch03, Ch05, Ch06 | 2×2 tables, risk ratio, stratified analysis, logistic regression (adjusted OR) |
| 5. Time & Space Analysis | Ch07, Ch08 | Time-series decomposition, spatial hotspot distribution |
| 6. Advanced Analysis | Ch09–11 | Survival analysis, machine-learning feature importance, deep-learning overview |
| 7. Causal Judgment & Recommendations | Ch12 | Causal inference framework, source-of-infection judgment, intervention recommendations |
| 8. Conclusion | Synthesis | Closing summary, concrete action recommendations |

---

## Summary of Key Findings

In the notebook, you'll produce the following key numbers:

- **280** residents, **121** infected (attack rate **43.2%**)
- **19** deaths (case fatality rate **15.7%**)
- Peak of onset: **2026-01-19 to 01-22**
- High-risk zones: **2F-A** (54.5%), **3F-B** (57.4%)
- Main risk factor: **shower use** (adjusted OR > 1, still significant after adjusting for age, sex, and comorbidities)
- Conclusion: **the shower water supply system is the most likely source of infection**

These numbers aren't independent findings — they're links in the same narrative chain: the shape of the epidemic curve points to a "common exposure source," the spatial hotspots point to "a specific floor's plumbing system," the exposure and stratified analyses rule out the competing hypothesis that "bedridden residents don't shower and also have lower infection rates," and finally the causal judgment ties the thread off into a sentence you can write directly into the closing report.

---

## Exporting Charts to a PPTX / DOCX Report

The analysis is done and the conclusions are written — but what your supervisor usually wants to see isn't the notebook, it's a slide deck or Word report ready to submit as-is. The traditional approach is to screenshot every chart and paste them one by one into PowerPoint or Word by hand — every time the data updates, you have to redo the whole thing, and it's easy to paste the wrong version or miss updating a number.

A better approach is to use `python-pptx` / `python-docx` to **programmatically assemble the report** directly from the charts and numbers you've already computed: no copy-pasting required, and it's **reproducible** — this is the direct extension of Ch13's point: just rerun the notebook once, and the report regenerates from the latest data, always staying in sync with the analysis.

```{figure} images/report_export_flow_en.svg
:name: fig-report-export-flow
:alt: Report export flow diagram: charts, tables, and key numbers produced by the analysis are converted into in-memory PNG images via io.BytesIO, then fed to python-pptx and python-docx, producing a SitRep.pptx slide deck and a report.docx document in one step
:width: 100%

Analysis output (charts / tables / key numbers) → saved as an in-memory PNG (`io.BytesIO`) → `python-pptx` / `python-docx` → a slide deck and a Word report, produced in one click.
```

The example below uses one chart (shower exposure vs. attack rate) and a set of summary numbers to demonstrate exporting a `.pptx` deck and a `.docx` report at the same time — for the full version (including the epidemic curve and additional charts), see the export section of `notebooks/14_case_study_legionella.ipynb`.

```python
import io
import os
import tempfile

import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches
from docx import Document
from docx.shared import Inches as DInches

# Reuse cases / n_total / n_infected / n_deaths already computed earlier in this chapter

# 1. Save the matplotlib figure as an in-memory PNG, without writing to disk
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(["No shower", "Shower"], [ar_no_shower, ar_shower], color=["#6A9BCC", "#D97757"])
ax.set_ylabel("Attack rate (%)")
ax.set_title("Shower Use vs Attack Rate")

buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
plt.close(fig)
buf.seek(0)

summary_rows = [
    ("Residents", f"{n_total}"),
    ("Infected", f"{n_infected} ({n_infected / n_total:.1%})"),
    ("Deaths", f"{n_deaths} ({n_deaths / n_infected:.1%})"),
]
outdir = tempfile.mkdtemp(prefix="sitrep_")

# 2. python-pptx: a title slide + a chart/table slide
prs = Presentation()
slide1 = prs.slides.add_slide(prs.slide_layouts[0])
slide1.shapes.title.text = "Songbai Nursing Home Legionnaires' Disease Outbreak SitRep"
slide1.placeholders[1].text = (
    f"Attack rate {n_infected / n_total:.1%} | Case fatality rate {n_deaths / n_infected:.1%}"
)

slide2 = prs.slides.add_slide(prs.slide_layouts[5])
buf.seek(0)   # BytesIO can only be read once -- always rewind before inserting the picture
slide2.shapes.add_picture(buf, Inches(0.4), Inches(1.1), width=Inches(6))

tbl = slide2.shapes.add_table(
    len(summary_rows) + 1, 2, Inches(6.8), Inches(1.1), Inches(2.7), Inches(1.6)
).table
tbl.cell(0, 0).text, tbl.cell(0, 1).text = "Item", "Value"
for i, (label, value) in enumerate(summary_rows, start=1):
    tbl.cell(i, 0).text, tbl.cell(i, 1).text = label, value

prs.save(os.path.join(outdir, "legionella_sitrep.pptx"))

# 3. python-docx: the same material, now as a Word report
doc = Document()
doc.add_heading("Songbai Nursing Home Legionnaires' Disease Outbreak Investigation Report", level=0)

doc.add_heading("Summary", level=1)
doc.add_paragraph(
    f"This outbreak involved {n_total} residents, of whom {n_infected} were infected"
    f" (attack rate {n_infected / n_total:.1%}), and {n_deaths} died"
    f" (case fatality rate {n_deaths / n_infected:.1%}). The presumed source of infection is the shower water supply system."
)

doc.add_heading("Shower Exposure vs Attack Rate", level=1)
buf.seek(0)   # This BytesIO was already read once in the PPTX section -- seek(0) again before reading
doc.add_picture(buf, width=DInches(5.5))

doc.add_heading("Key Numbers", level=1)
table = doc.add_table(rows=1, cols=2, style="Light Grid Accent 1")
table.rows[0].cells[0].text, table.rows[0].cells[1].text = "Item", "Value"
for label, value in summary_rows:
    row = table.add_row()
    row.cells[0].text, row.cells[1].text = label, value

doc.save(os.path.join(outdir, "legionella_sitrep.docx"))

print(f"Exported to: {outdir}")
```

> **Line-by-line**:
>
> | This line | What it does |
> |---|---|
> | `fig.savefig(buf, format="png", ...); buf.seek(0)` | Saves the chart into an in-memory `BytesIO` — no need to write to disk first before dropping it straight into the report |
> | `prs.slides.add_slide(prs.slide_layouts[0])` | Layout 0 = the title slide, with built-in main-title and subtitle placeholders |
> | `prs.slides.add_slide(prs.slide_layouts[5])` | Layout 5 = a blank slide, laid out yourself with a textbox / picture / table |
> | `slide2.shapes.add_picture(buf, ...)` | Inserts the in-memory PNG directly into the slide, no need to save it as a file first |
> | `slide2.shapes.add_table(rows, cols, ...).table` | Draws a table on the slide, filled row by row from `summary_rows` |
> | `buf.seek(0)` (second occurrence) | **`BytesIO` can only be read once**: after PPTX uses it, the cursor is parked at the end of the buffer; before DOCX reads it again you must rewind to the start, or you'll insert a blank image |
> | `doc.add_heading(..., level=0)` / `level=1` | Word's "Title" style (main title) / "Heading 1" style (section heading) |
> | `doc.add_picture(buf, width=DInches(5.5))` | Inserts the same chart; `DInches` is an alias for `docx.shared.Inches`, to avoid a name clash with pptx's `Inches` |
> | `doc.add_table(rows=1, cols=2, style="Light Grid Accent 1")` | Builds a table with a built-in style, starting with the header row, then adds data row by row with `add_row()` |
> | `tempfile.mkdtemp(prefix="sitrep_")` | Writes to the system's temp folder, not into the project directory, so it never gets tracked by git |

> 🎁 **Insight**: programmatic report generation = **one-click rerun, consistent formatting, zero manual errors**. When the data updates or a conclusion gets revised, rerunning the program once regenerates a consistently-formatted slide deck and Word report — no more manually screenshotting into slides, and no more wondering "which version of this chart is in the report." For the full pipeline (including the epidemic curve, spatial heatmap, and more fields), run [`14_case_study_legionella.ipynb`](notebooks/14_case_study_legionella.ipynb) directly — its final section is the complete version that produces the `.pptx` and `.docx` files for you.

## Exercises

- Exercise version: [`14_case_study_exercise.ipynb`](exercises/14_case_study_exercise.ipynb)
- Solution version (instructor): [`14_case_study_solution.ipynb`](solutions/14_case_study_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/14_case_study_solution.ipynb>)

## Common Misuses

| Mistake | Correct Approach |
|------|----------|
| Listing numbers with no context | Give every number a comparison baseline (e.g., national CFR, historical attack rates) |
| Too many charts, no clear focus | Pick 3–5 key charts, each with a clear conclusion — not "if it was computed, include it" |
| Stopping once the analysis is done | Always include an "action recommendations" section — a report should let people "act on it," not just "know it" |
| Inconsistent report formatting | Use a standard outbreak-report format (8 sections), so every deck/document you produce is laid out consistently |
| Manually screenshotting and pasting charts | Use `python-pptx` / `python-docx` for programmatic export — when data updates, just rerun the program |

## Next Step

Congratulations! Finishing this chapter means you now have the complete ability to conduct an outbreak investigation with Python and produce a report ready to submit — from receiving the notification, cleaning data, descriptive analysis, and statistical inference, through spatiotemporal modeling, all the way to causal judgment and automated report export.
The appendix (Ch15) collects advanced terminology and reference resources; Ch16/Ch17 are the book-wide overview of exercises and solutions.
