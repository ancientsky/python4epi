# fix_C report
Verification: nbconvert-executed 10_ml_advanced (zh via audit-style run, en), 04 and 14 (zh, en, standalone) OK (en/standalone run from a scratch dir with a data symlink; plain nbconvert in book_en/ lacks the data symlink, pre-existing). `uv run pytest -q`: all pass (100%).
- F1 fixed: book/ + book_en/ chapters/15_appendix.md (E-2 text; kernel startup / configure_book_kernel).
- F2 changed differently: verified layout 5 = Title Only, 6 = Blank. Code switched to slide_layouts[6] (the code uses textboxes, so Blank is intended) + prose, in 14_case_studies.md, 04_outbreak_workflow.md (same pattern, outside audit), 14/04 notebooks, notebooks/14. videos/scenes/ch04_07, ch14_04 still use [5] (not touched; listed for owner).
- F3 fixed: appendix C command + E-2 sentence (zh/en). REWRITE_PLAN.md only got the historical banner.
- F4 fixed differently: compat `l1_kw` (l1_ratio=1 on sklearn>=1.8, penalty="l1" below; pyproject floor is >=1.6 where l1_ratio alone would silently be L2). 10_ml_advanced zh/en/standalone. Removing the blanket filterwarnings: notebook runs clean without it on 1.8 (only a tqdm/ipywidgets notice), filter left in place.
- F5 skipped (instructed). F9 not fixed: only in 11_deep_learning.md (forbidden file).
- F6 fixed (pandas 3.0 released 2026-01-21 per PyPI). F7 fixed. F8 fixed: `uv sync --locked` + explanation in Ch13 zh/en (lock verified consistent). F12 fixed doc-side (script reads demo line_list.csv; pointer to Step 2 summary); run_sitrep.py unchanged.
- F10 banner added. F13 AGENTS.md fixed (08_ name, git history sentence, primary dataset). README unchanged (audit found no stale claim).
- F11 changed differently: sources blocked (newtalk, cdc.gov.tw), so facts unverified; hedged both cases and labelled the DAG hypothetical, no new factual claims added.
- F14 fixed: `|| True` -> `|| true` in all 15 non-symlinked notebooks (06 and 14 families, all zh/en/standalone).
- F15 fixed: 01b row added to 16/17 (zh/en); solution slug `b-python-toolbox-solution` copied from existing Ch01b link.
- F16 fixed. F17 fixed (hedged "usually preinstalled" + apt fallback line).
- F18 unverifiable (ancientsky.github.io blocked); links unchanged, incl. the new 01b links.
