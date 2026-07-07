/*
 * Language switcher for Epi With Python (繁體中文 <-> English).
 *
 * The site is built twice: the Traditional Chinese tree deploys at the site
 * root (e.g. https://host/python4epi/) and the English tree (book_en/) deploys
 * under a "/en/" prefix (https://host/python4epi/en/). Both trees mirror the
 * same internal file structure, so switching languages only means toggling the
 * "/en/" segment on the current page's path.
 *
 * This script derives the deploy base path from its own <script> src (which the
 * theme emits relative to each language build's _static/ dir), so it works both
 * for local builds served at "/" and for GitHub Pages served under a repo
 * sub-path -- no hard-coded base URL required.
 */
(function () {
  "use strict";

  var script =
    document.currentScript ||
    (function () {
      var s = document.getElementsByTagName("script");
      for (var i = s.length - 1; i >= 0; i--) {
        if (s[i].src && s[i].src.indexOf("lang-switch.js") !== -1) return s[i];
      }
      return null;
    })();
  if (!script) return;

  var marker = "/_static/lang-switch.js";
  var srcPath;
  try {
    srcPath = new URL(script.src, window.location.href).pathname;
  } catch (e) {
    return;
  }
  var idx = srcPath.indexOf(marker);
  if (idx < 0) return;

  // langRoot is the site root for the CURRENT language build:
  //   zh page -> "/python4epi"      en page -> "/python4epi/en"
  var langRoot = srcPath.slice(0, idx);
  var isEn = /\/en$/.test(langRoot);
  var baseRoot = isEn ? langRoot.replace(/\/en$/, "") : langRoot; // zh root
  var enRoot = baseRoot + "/en";

  var curRoot = isEn ? enRoot : baseRoot;
  var targetRoot = isEn ? baseRoot : enRoot;

  var pathname = window.location.pathname;
  // Relative path of the current page within its language tree.
  var rel = pathname.indexOf(curRoot) === 0 ? pathname.slice(curRoot.length) : pathname;
  if (rel.charAt(0) !== "/") rel = "/" + rel;

  var targetUrl = targetRoot + rel + window.location.search + window.location.hash;
  var homeUrl = targetRoot + "/";

  function wire() {
    var link = document.getElementById("lang-switch-link");
    if (!link) return;

    link.setAttribute("href", targetUrl);
    link.setAttribute("hreflang", isEn ? "zh-Hant" : "en");
    var label = link.querySelector(".lang-switch-label");
    if (label) label.textContent = isEn ? "中文" : "EN";
    var tip = isEn ? "切換為繁體中文" : "Switch to English";
    link.setAttribute("title", tip);
    link.setAttribute("aria-label", tip);

    // Graceful fallback: if the counterpart page does not exist in the other
    // tree (e.g. a page not yet translated), send the user to that tree's home
    // page instead of a 404. A cheap same-origin HEAD check gates the jump.
    link.addEventListener("click", function (ev) {
      ev.preventDefault();
      var done = false;
      var go = function (url) {
        if (done) return;
        done = true;
        window.location.href = url;
      };
      try {
        fetch(targetUrl, { method: "HEAD" })
          .then(function (resp) {
            go(resp && resp.ok ? targetUrl : homeUrl);
          })
          .catch(function () {
            go(targetUrl); // network/HEAD blocked -> just try the direct URL
          });
        // Safety net so a hung request never traps the user.
        window.setTimeout(function () {
          go(targetUrl);
        }, 1200);
      } catch (e) {
        go(targetUrl);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
