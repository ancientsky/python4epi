# Brief for translators — Philippines edition ("Bantay Python")

Repo: /home/user/python4epi. The English edition in `book_ph/en/` is finished and is the source of truth.
You produce the same files in another language under `book_ph/<lang>/` (placeholders exist with the
same file names — overwrite the ones assigned to you). Read first: `book_ph/PRODUCTION.md` (bible),
the "Philippines Edition" section of `/home/user/python4epi/CLAUDE.md`, `book_ph/STYLEGUIDE.md`,
`book_ph/GAMES.md`.

## Rules
- Mirror the English file exactly in structure: same frontmatter keys, same headings in the same order,
  same directives/classes, same code, same links (by file path), same numbers. Translate prose, titles,
  `description`, figure captions and alt text, table text, admonition titles, the fallback text and quiz
  questions inside `ph-game` blocks (keep the authoring syntax GAMES.md documents, e.g. the leading "✓ "
  on correct options, class names untouched).
- Images: language-specific illustrations exist with suffix `_zh.svg` / `_fil.svg` for every `_en.svg`
  the English page uses (check `book_ph/images/`); switch the suffix. Language-free images stay as is.
  If the text inside a `_zh`/`_fil` SVG is wrong or unnatural, fix the SVG (keep it well-formed XML).
- Notebooks: copy the English notebook and translate markdown cells, code comments and user-facing
  strings (print text, plot titles/axis labels/legends, DataFrame display labels). Do NOT change code
  logic, identifiers, dataset column names, cell ids, cell order, or the Colab setup cell (keep it
  byte-identical). Do it with a small Python script over the notebook JSON (nbformat), not by hand-editing
  JSON. No stored outputs. Then execute every notebook from the repo root and fix until clean:
  `cd /home/user/python4epi && uv run python -c "import nbformat,sys;from nbclient import NotebookClient;nb=nbformat.read(sys.argv[1],4);NotebookClient(nb,timeout=300,resources={'metadata':{'path':'.'}}).execute();print('ok',sys.argv[1])" <notebook>`
  (the notebooks read `data/synthetic/ph/...` relative to the repo root). The TimesFM notebook replays a
  cache keyed on its numeric inputs — do not alter those inputs. Chinese plot labels need a CJK font:
  the book build configures one, and in the notebook use the same inline CJK font candidate list the
  main zh book notebooks use (see `book/chapters/notebooks/03_stats_basics.ipynb`) if labels are Chinese.
- Prompts to the AI assistant ("Ask Tala" boxes): translate them — a learner may prompt in their own
  language — but keep column names, code and file names in English.
- Names stay: Maya Dela Cruz, Doc Mon, Tala, Aling Nena, Jun, Santa Luz City, Kalinaw, Typhoon Amihan,
  barangay names, "Bantay Python", act titles' Filipino phrases (May ulat!, Bilangin natin, Bantay,
  Ipakita — in zh/en add the gloss as the English edition does).
- Links into the full Epi With Python book: zh → the zh edition (`https://ancientsky.github.io/python4epi/…`
  without `/en/`), fil → keep the English edition links.
- Keep every source link and every "this is fictional / synthetic" statement. Do not add facts.
- Other translators are working on other files at the same time: touch only your assigned files (and a
  `_zh`/`_fil` SVG you correct). Do NOT run git commands that change state and do NOT run
  `scripts/build_book.py` (the director builds). `myst.yml`, navbar and footer are already translated.
- When done: re-read each page once as a reader would; check no English paragraph was left behind
  (code and technical terms excepted); run `uv run pytest tests/test_notebook_smoke.py tests/test_book_toc.py -q`.
  Reply with a summary under 120 words: files done, terms you were unsure about, anything left.
