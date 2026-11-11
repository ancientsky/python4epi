/*
 * Page extras for the Philippines edition of Epi With Python ("Bantay Python").
 *
 * scripts/build_book.py injects, in this order, into every PH page:
 *
 *   <script>window.EPI_SITE = {...}</script>   inline config (below)
 *   _static/epi-site.js   from book/_static: defines window.epiWhenHydrated();
 *                         its main-book part is inert here (no EPI_SITE.alternate)
 *   _static/ph-site.js    this file
 *   _static/ph-games.js   the interactives (optional; loads after this file)
 *
 * Contract for scripts that load after this one: window.epiWhenHydrated(cb)
 * exists, and window.EPI_SITE.lang is "en" | "zh" | "fil".
 *
 *   window.EPI_SITE = {
 *     lang: "en" | "zh" | "fil",  series: "ph",  edition: "student",
 *     htmlLang: "en" | "zh-Hant" | "fil",
 *     root: "/python4epi/ph/",                 // this edition's root (trailing /)
 *     languages: [                             // all three, current included
 *       { lang: "en", root: "/python4epi/ph/", hreflang: "en", label: "EN",
 *         title: "Read this page in English" }, ...
 *     ],
 *     book: { root: "/python4epi/en/", title: "Epi With Python — the full book" },
 *     standalone: ["dashboard/"],              // non-MyST pages below root
 *     colab: { "chapters/notebooks/maps/": "https://colab..." },
 *     colabLabel: "Open in Colab"
 *   };
 *
 * On every page, and again after each client-side navigation, it:
 *
 * 1. Language switch. The navbar part (_site/navbar_end.md) renders plain links
 *    a.ph-lang.ph-lang-<code> to each language's home page (the no-JavaScript
 *    fallback). They are retargeted to the same page in that language; the
 *    current language's link gets aria-current="true". On click, a HEAD request
 *    checks that the page exists and falls back to that language's home page.
 * 2. Full book. a.ph-book-link is pointed at the main book (zh readers: "/",
 *    everyone else: "/en/") and kept in the same tab.
 * 3. "Open in Colab" on notebook pages (a.epi-colab-link.ph-colab-link in the
 *    page header), from the page -> notebook map the build writes.
 * 4. Standalone pages. Links into cfg.standalone (the chapter-9 dashboard at
 *    <root>dashboard/) are not MyST pages, so the theme's client-side router
 *    cannot open them; clicks on them do a full page load instead.
 *
 * Like epi-site.js, nothing touches the DOM before React has hydrated
 * (window.epiWhenHydrated); click handlers read the URL at click time and are
 * installed at once.
 */
(function () {
  "use strict";

  var cfg = window.EPI_SITE;
  if (!cfg || cfg.series !== "ph" || !cfg.root || !cfg.languages) return;
  var whenHydrated = window.epiWhenHydrated || function (fn) {
    // epi-site.js missing: degrade to "after load".
    if (document.readyState === "complete") window.setTimeout(fn, 0);
    else window.addEventListener("load", fn);
  };
  if (!window.epiWhenHydrated) window.epiWhenHydrated = whenHydrated;

  var byLang = {};
  cfg.languages.forEach(function (l) { byLang[l.lang] = l; });

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

  function langOf(link) {
    var m = /(?:^|\s)ph-lang-([a-z]+)(?:\s|$)/.exec(link.className || "");
    return m && byLang[m[1]] ? m[1] : null;
  }

  function targetFor(lang) {
    return byLang[lang].root + relativePath() + window.location.search + window.location.hash;
  }

  function setAttr(el, name, value) {
    if (value === null) {
      if (el.hasAttribute(name)) el.removeAttribute(name);
    } else if (el.getAttribute(name) !== value) {
      el.setAttribute(name, value);
    }
  }

  function wireLanguageLinks() {
    var links = document.querySelectorAll("a.ph-lang");
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      var lang = langOf(link);
      if (!lang) continue;
      var info = byLang[lang];
      setAttr(link, "href", targetFor(lang));
      setAttr(link, "hreflang", info.hreflang);
      setAttr(link, "lang", info.hreflang);
      setAttr(link, "title", info.title);
      setAttr(link, "aria-current", lang === cfg.lang ? "true" : null);
      // The theme opens "external" links in a new tab; a language switch stays.
      setAttr(link, "target", null);
    }
  }

  function wireBookLink() {
    if (!cfg.book) return;
    var links = document.querySelectorAll("a.ph-book-link");
    for (var i = 0; i < links.length; i++) {
      setAttr(links[i], "href", cfg.book.root);
      setAttr(links[i], "title", cfg.book.title);
      setAttr(links[i], "target", null);
    }
  }

  function wireColab() {
    var url = cfg.colab && cfg.colab[relativePath()];
    var existing = document.querySelectorAll("a.ph-colab-link");
    for (var i = 0; i < existing.length; i++) {
      if (existing[i].getAttribute("href") !== url) existing[i].parentNode.removeChild(existing[i]);
    }
    if (!url) return;
    var header = document.querySelector(".myst-fm-block-header");
    if (!header || header.querySelector("a.ph-colab-link")) return;
    var link = document.createElement("a");
    link.className = "epi-colab-link ph-colab-link";
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener";
    link.title = cfg.colabLabel;
    link.textContent = cfg.colabLabel;
    header.appendChild(link);
  }

  function plainClick(event) {
    return !(event.defaultPrevented || event.button !== 0 ||
             event.metaKey || event.ctrlKey || event.shiftKey || event.altKey);
  }

  function onLanguageClick(event, link) {
    var lang = langOf(link);
    if (!lang) return false;
    event.preventDefault();
    event.stopPropagation();
    var target = targetFor(lang);
    var home = byLang[lang].root;
    var done = false;
    function go(url) {
      if (done) return;
      done = true;
      window.location.href = url;
    }
    if (lang === cfg.lang) { go(target); return true; }
    // Never trap the user behind a slow or blocked request.
    window.setTimeout(function () { go(target); }, 1500);
    try {
      fetch(target, { method: "HEAD", cache: "no-store" })
        .then(function (resp) { go(resp.ok ? target : home); })
        .catch(function () { go(target); });
    } catch (e) {
      go(target);
    }
    return true;
  }

  function isStandalone(link) {
    if (!cfg.standalone || !cfg.standalone.length) return false;
    var url;
    try { url = new URL(link.getAttribute("href"), window.location.href); } catch (e) { return false; }
    if (url.origin !== window.location.origin) return false;
    var path = url.pathname.replace(/index\.html$/, "");
    if (path.charAt(path.length - 1) !== "/") path += "/";
    for (var i = 0; i < cfg.standalone.length; i++) {
      if (path.indexOf(cfg.root + cfg.standalone[i]) === 0) return true;
    }
    return false;
  }

  function onClick(event) {
    if (!plainClick(event)) return;
    var link = event.target.closest && event.target.closest("a[href]");
    if (!link) return;
    if (link.classList.contains("ph-lang") && onLanguageClick(event, link)) return;
    if (link.getAttribute("target") === "_blank") return;
    if (isStandalone(link)) {
      event.preventDefault();
      event.stopPropagation();
      window.location.href = link.href;
    }
  }

  var ready = false;
  var scheduled = false;
  function update() {
    scheduled = false;
    if (cfg.htmlLang && document.documentElement.lang !== cfg.htmlLang) {
      document.documentElement.lang = cfg.htmlLang;
    }
    wireLanguageLinks();
    wireBookLink();
    wireColab();
  }
  function schedule() {
    if (!ready || scheduled) return;
    scheduled = true;
    window.setTimeout(update, 0);
  }

  // Capture phase, so it runs before the theme's router sees the click.
  document.addEventListener("click", onClick, true);

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

  whenHydrated(function () {
    ready = true;
    update();
    // Re-apply whenever the app re-renders the header or the page body.
    new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
  });
})();
