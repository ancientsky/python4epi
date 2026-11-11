/*
 * Page extras for Epi With Python (Jupyter Book 2 / MyST book-theme).
 *
 * MyST has no slot for custom JavaScript, so scripts/build_book.py injects
 * this file into every built page, preceded by a small inline config:
 *
 *   window.EPI_SITE = {
 *     lang: "zh" | "en",          // language of this build
 *     edition: "student" | "instructor",
 *     htmlLang: "zh-Hant" | "en", // value for <html lang>
 *     root: "/python4epi/",        // this edition's root path (trailing /)
 *     alternate: {                 // same edition in the other language
 *       root: "/python4epi/en/", hreflang: "en", title: "Switch to English"
 *     },
 *     colab: { "chapters/notebooks/stats-basics/": "https://colab..." },
 *     colabLabel: "Open in Colab"
 *   };
 *
 * It does two things on every page, and again after each client-side
 * navigation (the theme is a single-page app, so most page changes do not
 * reload the document):
 *
 * 1. Language switcher. The navbar part (_site/navbar_end.md) renders a plain
 *    link with class "epi-lang-switch" that points at the other language's
 *    home page (the no-JavaScript fallback). Here it is retargeted to the same
 *    page in the other language and the same edition (student <-> student,
 *    instructor <-> instructor). book/ and book_en/ mirror each other
 *    file-for-file, so the counterpart has the same path below the edition
 *    root. On click, a HEAD request checks that the counterpart exists; if not,
 *    the user lands on the other tree's home page instead of a 404.
 *
 * 2. "Open in Colab". On notebook pages a link that opens the notebook from
 *    GitHub `main` in Google Colab is added to the page header, next to the
 *    theme's GitHub/download buttons. The page -> notebook map is written by
 *    the build, so nothing here guesses file names.
 *
 * The page is server-rendered and then hydrated by React. Changing the DOM
 * before hydration has finished is a hydration mismatch (React error #418),
 * after which React re-renders the whole page and drops the changes. So DOM
 * changes wait until the browser is idle after the load event; the language
 * link's click handler does not depend on them and works from the start.
 */
(function () {
  "use strict";

  var cfg = window.EPI_SITE;
  if (!cfg || !cfg.root || !cfg.alternate) return;

  /** Path of the current page relative to this edition's root ("" = home). */
  function relativePath() {
    var path = window.location.pathname.replace(/index\.html$/, "");
    if (path.indexOf(cfg.root) === 0) {
      path = path.slice(cfg.root.length);
    } else if (path + "/" === cfg.root) {
      path = "";
    } else {
      path = path.replace(/^\//, "");
    }
    if (path && path.charAt(path.length - 1) !== "/") path += "/";
    return path;
  }

  function counterpartUrl() {
    return cfg.alternate.root + relativePath() + window.location.search + window.location.hash;
  }

  function wireLanguageLinks() {
    var target = counterpartUrl();
    var links = document.querySelectorAll("a.epi-lang-switch");
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      if (link.getAttribute("href") !== target) link.setAttribute("href", target);
      if (link.getAttribute("hreflang") !== cfg.alternate.hreflang) {
        link.setAttribute("hreflang", cfg.alternate.hreflang);
        link.setAttribute("title", cfg.alternate.title);
        link.setAttribute("aria-label", cfg.alternate.title);
        // The theme opens external links in a new tab; a language switch
        // should stay in this one.
        link.removeAttribute("target");
      }
    }
  }

  function onLanguageClick(event) {
    var link = event.target.closest && event.target.closest("a.epi-lang-switch");
    if (!link || event.defaultPrevented || event.button !== 0) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    event.stopPropagation();
    var target = counterpartUrl();
    var home = cfg.alternate.root;
    var done = false;
    function go(url) {
      if (done) return;
      done = true;
      window.location.href = url;
    }
    // Never trap the user behind a slow or blocked request.
    window.setTimeout(function () { go(target); }, 1500);
    try {
      fetch(target, { method: "HEAD", cache: "no-store" })
        .then(function (resp) { go(resp.ok ? target : home); })
        .catch(function () { go(target); });
    } catch (e) {
      go(target);
    }
  }

  function wireColab() {
    var url = cfg.colab && cfg.colab[relativePath()];
    var existing = document.querySelectorAll("a.epi-colab-link");
    for (var i = 0; i < existing.length; i++) {
      if (existing[i].getAttribute("href") !== url) existing[i].parentNode.removeChild(existing[i]);
    }
    if (!url) return;
    var header = document.querySelector(".myst-fm-block-header");
    if (!header || header.querySelector("a.epi-colab-link")) return;
    var link = document.createElement("a");
    link.className = "epi-colab-link";
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener";
    link.title = cfg.colabLabel;
    link.textContent = cfg.colabLabel;
    header.appendChild(link);
  }

  var ready = false;
  var scheduled = false;
  function update() {
    scheduled = false;
    if (cfg.htmlLang && document.documentElement.lang !== cfg.htmlLang) {
      document.documentElement.lang = cfg.htmlLang;
    }
    wireLanguageLinks();
    wireColab();
  }
  function schedule() {
    if (!ready || scheduled) return;
    scheduled = true;
    window.setTimeout(update, 0);
  }

  // The click handler reads the URL at click time, so it is safe right away.
  document.addEventListener("click", onLanguageClick, true);

  // Client-side navigation: react-router uses pushState/replaceState.
  ["pushState", "replaceState"].forEach(function (name) {
    var original = window.history[name];
    window.history[name] = function () {
      var result = original.apply(this, arguments);
      schedule();
      return result;
    };
  });
  window.addEventListener("popstate", schedule);
  window.addEventListener("hashchange", schedule);

  function start() {
    ready = true;
    update();
    // Re-apply whenever the app re-renders the header or the page body.
    new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
  }
  function whenIdle() {
    if (window.requestIdleCallback) window.requestIdleCallback(start, { timeout: 2000 });
    else window.setTimeout(start, 200);
  }
  if (document.readyState === "complete") whenIdle();
  else window.addEventListener("load", whenIdle);
})();
