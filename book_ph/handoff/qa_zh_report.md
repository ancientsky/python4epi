# zh copy-chief QA report

## Glossary state
Inspected first: the previous pass had already applied the decided glossary everywhere (box titles, barangay first-use gloss
on every page that uses the word, 村里衛生員（BHW）, CESU/PESU/DSO, 小格遮蔽, 單一時點/持續性共同感染源/連鎖傳播,
警戒/流行閾值, 流行病學週, 早期應變, Taiwan table). Grep for all "avoid" variants (攻擊率, 病死率, 比值比, 置信區間,
監控, 混淆, 發病率, 交絡, 流調 ...) over pages, notebooks, myst.yml, navbar/footer, ph-games.js zh strings,
build_ph_dashboard.py zh strings and `_zh` SVGs: none left (one hit, 「不會混淆」, is ordinary wording in a game string).

## Fixed in this pass
- Markdown emphasis was broken by CJK flanking rules (`**X（Y）**是…`, `*「…」*`, `**（…）**去重` printed literal asterisks):
  ~45 spots in 00-10 pages and 9 notebooks. Rewritten as `**X**（Y）`, `「*…*」`, `（**…**）`. Verified: built HTML has no
  literal `*` outside code.
- 00_start_here.md:38 duplicated gloss 「筆記本（筆記本）」 -> 筆記本（notebook）.
- Stray spaces around 筆記本 / after 」 between CJK (about 45 places, pages + notebook markdown).
- ph.css (end of file): `html[lang="zh-Hant"] main.article-grid {overflow-x: clip}` removes a 5-9 px horizontal
  scroll at 390 px on pages with long CJK headings (theme's invisible "¶" anchor).

## Completeness checks (all pass)
Same heading levels, directive sequence, links, fence blocks, image variants (_zh), quiz ✓ marks and list counts as English;
code blocks identical apart from translated strings/comments; notebooks: same cell ids/order/types, no outputs, Colab setup
cells identical; only intentional code changes are CJK font cell and DISEASE_ZH label maps. Game blocks (12) all render Chinese
UI and respond to clicks; no page errors.

## Build / tests
`build_book.py --series ph --lang zh`: strict, 0 warnings. `uv run pytest -q`: all pass.
Screenshots (22 pages incl. dashboard x 1280/390 x light/dark) taken to scratch dir; reviewed home, ch00, ch01, ch04, dashboard
by eye; the others only by automated overflow/console checks. Samples in `book_ph/handoff/qa_zh_shots/`.

## Not checked
Plotly figures (blocked CDN: blank here); every page visually at every size; real Noto CJK rendering (sandbox has WenQuanYi);
Chinese legal wording (RA 10173 / RA 11332) needs a native/legal reader. Notebook front-matter descriptions for 07/09 are
looser paraphrases of English (left as is).
