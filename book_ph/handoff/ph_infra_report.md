# Philippines edition — build infrastructure report

## What changed

**New**
- `book_ph/{en,zh,fil}/` — three MyST projects: `myst.yml` (per-language title/description/keywords,
  intro + 4 title-only act groups with the §4 stems, same theme sha + `error_rules` as `book/myst.yml`,
  zh/fil `numbering.figure.enabled: false`, `favicon`/`logo`/`logo_dark` from `_static`, `style: _static/ph.css`,
  `folders: true`), `_site/navbar_end.md` (links `a.ph-lang.ph-lang-{en,zh,fil}` + `a.ph-book-link`, absolute
  production URLs as no-JS fallback), `_site/footer.md` (says story/data are fictional), placeholder `intro.md`,
  11 chapter pages, 9 notebooks (title cell + standard Colab cell id `colab-setup` + `print("Mabuhay!")`).
- Symlinks `book_ph/<lang>/_static -> ../_static`, `book_ph/<lang>/chapters/images -> ../../images`.
- `book_ph/_static/ph-site.js` (mine) — language switch, full-book link, Colab link, standalone-page clicks.
- `scripts/build_ph_dashboard.py` — `build_dashboard(lang: str, out_dir: Path) -> Path`, placeholder page
  (+ small CLI `--lang --out-dir`).

**Modified**
- `scripts/build_book.py` — `Edition(lang, edition="student", series="main")`; `series="ph"` adds
  `is_ph`, `meta`, `alternates()`; `MAIN_EDITIONS` (4) + `PH_EDITIONS` (3) = `ALL_EDITIONS`;
  `PH_LANG_META` (prefixes `ph/`, `ph/zh/`, `ph/fil/`; html lang `en`/`zh-Hant`/`fil`; og locales
  `en_PH`/`zh_TW`/`tl_PH`; per-language description, Colab label, full-book target). `site_config()`,
  `copy_static()`, `load_dashboard_builder()`, `selected_editions()` added; `head_links_and_scripts()`
  takes `alternate_langs`/`static_files` (old `has_counterpart` kw still works); hreflang among the three
  PH languages, x-default = PH English; repeated `og:locale:alternate` tags; no JB1 redirect stubs for PH;
  `broken_links(..., site_url=)` resolves absolute `https://ancientsky.github.io/python4epi/...` links —
  used only by the fully assembled (7-edition) check. Main-book output unchanged (all old tests pass).
  CLI: `--lang/--edition` as before; `--series ph --lang en|zh|fil`; `--all` = seven; `--series X --all`.
- `book/_static/epi-site.js` — comment only (PH relies on its book part being inert without `alternate`).
- `book/intro.md`, `book_en/intro.md` — one line + `{button}` to `/ph/zh/` resp. `/ph/` (absolute
  production URL, same pattern as the instructor-edition button; verified by the assembled check).
- Tests: `tests/test_build_book.py` (+12 tests: PH Edition props/validation, symlinks, PH head/config/
  script order, zh book-root + missing optional files, PH postprocess end-to-end incl. dashboard + link,
  required ph-site.js, og-image choice, dashboard placeholder, PH CLI, absolute-link check, nested PH
  skip), `tests/test_book_toc.py` (bible stems/order, title-only acts, zh/fil parity with translated act
  titles, files exist, theme pin equal across 5 configs, error_rules/style/numbering),
  `tests/test_notebook_smoke.py` (PH notebook roots + 3-language parity with Colab cell).
- `.github/workflows/ci.yml` — new step `build_book.py --series ph --all`.
  `.github/workflows/pages.yml` — "Build all seven editions"; sanity checks for `ph/`, `ph/zh/`,
  `ph/fil/` (index, notebook page, `dashboard/index.html`, `ph-site.js`, post-processed, html lang);
  solution-leak check unchanged (its root scan already covers `ph/`).
- `CLAUDE.md` — new "Philippines Edition (`book_ph/`)" section; build script docstring updated.
- `.gitignore` — no change needed (`_build/` already matches `book_ph/*/_build`).

## Contracts as implemented
- **Images:** files in `book_ph/images/`; in a chapter `![alt](images/x.svg)` (relative to `chapters/`).
- **Dashboard link:** root-relative MyST link `[Open the dashboard](/dashboard/)`; MyST prefixes BASE_URL
  → `/python4epi/ph/fil/dashboard/`. Relative `../../dashboard/` does NOT survive (becomes
  `/python4epi/ph/../../dashboard/`). Placeholder in each `chapters/09_dashboard.md`. The page is written by
  `build_dashboard(lang, <edition>/_build/html/dashboard)` during the post-build step, before the link
  check. `ph-site.js` forces a full page load on click (the theme router would otherwise try to load it as
  a MyST page) — verified in headless Chrome.
- **Script order on PH pages:** `<link rel=stylesheet ph-games.css>`, `window.EPI_SITE={...}`,
  `epi-site.js` (provides `window.epiWhenHydrated`), `ph-site.js`, `ph-games.js` (all `defer`).
  `ph.css` is MyST's `style`. No youtube-lite.js. Guaranteed for ph-games.js: `window.epiWhenHydrated(cb)`
  exists; `window.EPI_SITE.lang` ∈ `en|zh|fil`. EPI_SITE also has `series:"ph"`, `root`, `languages[]`,
  `book{root,title}`, `standalone:["dashboard/"]`, `colab`, `colabLabel`, `htmlLang`.
- **Language switch:** `a.ph-lang.ph-lang-<code>` retargeted to same page in that language,
  `aria-current="true"` on the current one (style hook for ph.css), `target` removed; click → HEAD check
  → fallback to that language's home. `a.ph-book-link` → `/python4epi/` (zh) or `/python4epi/en/`.
  Colab link class `epi-colab-link ph-colab-link` in `.myst-fm-block-header`.
- **Optional static files:** `ph-games.css/js` skipped with `⚠` if absent; `ph-site.js` required;
  missing `ph.css` → MyST `⛔` line but exit 0 + our `⚠`. og-image: `og-image_<lang>.png` →
  `book_ph/_static/og-image.png` → main book's. (All design files exist now, tolerance kept.)

## Commands and results
- `uv run pytest` → all pass, no failures (incl. new tests). `uv run ruff check scripts/build_book.py
  scripts/build_ph_dashboard.py tests` → clean. `uv run ruff check scripts tests src` reports 9
  pre-existing issues in files I did not touch (`scripts/generate_og_image.py`,
  `src/epi_learning/{cleaning,viz}.py`) and in another agent's new `src/epi_learning/tsfm.py`.
- `uv run python scripts/build_book.py --series ph --lang en|zh|fil` → each ✔ `{'pages': 21,
  'notebooks': 9, 'redirects': 0, 'standalone': 1, 'warnings': 0}` (at that time ph.css/ph-games were
  absent → warnings as designed).
- Headless Chrome (puppeteer-core) on the three PH builds served under `/python4epi/ph/`: hydration hook
  present, `<html lang>` right, three lang links + aria-current, book link, Colab link on notebook pages
  and removed after client-side nav, links re-targeted after client-side nav, zh switch lands on the same
  page, dashboard click = full page load; no React/page errors (only blocked external fonts and
  un-served main-book URLs).
- Full `--all --site-dir <scratchpad>/site` (run twice):
  - 1st run: all seven editions ✔ (zh student 26 min cold, 0 warnings everywhere), then the assembled
    check failed on one link: en-instructor `dl-timesfm` hreflang → zh-instructor page that did not exist.
    Cause: another agent added `11_dl_timesfm.ipynb` to both trees/TOCs mid-build (after zh instructor
    was built) — the new absolute-URL check caught a real snapshot inconsistency.
  - 2nd run (warm cache): EXIT 0. zh student 55 pages/36 nb, zh instr 71/51, en student 55/36,
    en instr 71/51, ph en/zh/fil 21 pages/9 nb/1 standalone each, all 0 warnings;
    "✔ site assembled" with the full 7-edition + absolute-link check passing.
  - The pages.yml sanity-check block, run against that site: OK. Main-book home pages link
    `/ph/zh/` (zh) and `/ph/` (en).
- Removed all `_build/` dirs I created (git-ignored); site output was only in the scratchpad.

## Local-environment notes (not repo changes)
- The sandbox proxy blocks `github.com/.../archive/*.zip`, so I seeded MyST's template cache
  (`<project>/_build/templates/site/<sha256(url)>/`) from a `git fetch` of the pinned sha. CI is unaffected.
- Running as root: Jupyter server refuses; I used `JUPYTER_CONFIG_DIR` with `allow_root` (scratchpad only).

## Unfinished / for the director
- The bible (§7) says `ph-site.js` replaces game blocks; as instructed, games live in `ph-games.js` and
  `ph-site.js` is the language/edition script — the bible line should be updated.
- intro.md is a top-level index entry above Act I (as in the main book), not inside Act I.
- Pre-existing: `book_en/intro.md` "Open the student edition" button points to the zh root `/python4epi/`.
