/*
 * ph-games.js — interactive teaching widgets for the Philippines edition
 * ("Bantay Python"). Vanilla JS, no dependencies, no network requests.
 * Full authoring guide with copy-paste snippets: book_ph/GAMES.md.
 *
 * AUTHORING CONTRACT
 * ------------------
 * Write a MyST div whose classes name the widget, with fallback content for
 * readers without JavaScript:
 *
 *   :::{div}
 *   :class: ph-game ph-game-<name> [extra option classes]
 *   Fallback text shown without JavaScript.
 *   :::
 *
 * <name> is one of: prompt-pick, bug-hunt, spot-pii, date-fixer,
 * epicurve-builder, two-by-two, threshold-watch, forecast-guess, map-paint,
 * lamok-patrol, publish-check, quiz. Content for every widget except `quiz`
 * is built into this file (all people, places and numbers are fictional).
 * MyST keeps only class/id/style/href, so per-instance options are classes:
 *
 *   quiz              questions come from the fallback list (see below);
 *                     if the div has no list, `ph-quiz-ch02|ch04|ch06`
 *                     selects a built-in question bank.
 *   epicurve-builder  `ph-curve-lepto|dengue|water` plays only that scenario.
 *   two-by-two        `ph-2x2-cohort|casecontrol` plays only that round.
 *   forecast-guess    `ph-forecast-normal|typhoon` plays only that round.
 *   lamok-patrol      `ph-lamok-relaxed` starts without the timer.
 *   any widget        `ph-compact` uses tighter spacing.
 *
 * Quiz fallback syntax (a plain markdown list; first-level items are the
 * questions, nested items the options; "✓ " marks the correct option; an
 * optional " — explanation" after an option is shown when it is chosen):
 *
 *   1. What is the denominator of an attack rate?
 *      - The number of cases — that is the numerator.
 *      - ✓ The population at risk — everyone who could have become a case.
 *
 * A paragraph before the list becomes the quiz title.
 *
 * RUNTIME
 * -------
 * The page is server-rendered and hydrated by React, so nothing here touches
 * the DOM before window.epiWhenHydrated(cb) fires (provided by epi-site.js,
 * injected before this file; a small fallback is used if it is missing).
 * The fallback children are hidden, not removed (React still owns them), and
 * the widget is appended as one extra child. After every client-side
 * navigation (pushState/popstate/DOM mutation) new blocks are mounted and
 * instances whose block left the document are destroyed (timers, frames and
 * global listeners released). Language: window.EPI_SITE.lang ("en" | "zh" |
 * "fil"), else <html lang>. Reusable page hooks: `.ph-reveal` (scroll reveal)
 * and `.ph-stat` (count-up of the number in its text); both are no-ops under
 * prefers-reduced-motion. window.PHGames exposes scan() and a small API.
 */
(function () {
  "use strict";

  var W = window;
  var D = document;
  if (W.PHGames && W.PHGames.version) return;

  var SVGNS = "http://www.w3.org/2000/svg";
  var MQ = W.matchMedia ? W.matchMedia("(prefers-reduced-motion: reduce)") : null;
  function reduced() { return !!(MQ && MQ.matches); }

  /* ---------------------------------------------------------------- lang */
  function detectLang() {
    var l = (W.EPI_SITE && W.EPI_SITE.lang) || D.documentElement.getAttribute("lang") || "en";
    l = String(l).toLowerCase();
    if (l.indexOf("zh") === 0) return "zh";
    if (l.indexOf("fil") === 0 || l.indexOf("tl") === 0) return "fil";
    return "en";
  }
  var LANGS = { en: 0, zh: 1, fil: 2 };
  var LI = 0;
  /** Pick the current language from ["en", "zh", "fil"] (or a plain string). */
  function L(v) {
    if (v == null) return "";
    if (typeof v === "string" || typeof v === "number") return String(v);
    return v[LI] != null ? v[LI] : v[0];
  }
  /** Replace {name} placeholders. */
  function fmt(s, o) {
    return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o && o[k] != null ? o[k] : m; });
  }
  function num(x, d) {
    if (x == null || !isFinite(x)) return "—";
    return Number(x).toFixed(d == null ? 0 : d);
  }

  var UI = {
    score: ["Score", "得分", "Puntos"],
    next: ["Next", "下一題", "Susunod"],
    nextRound: ["Next round", "下一回合", "Susunod na round"],
    check: ["Check", "檢查", "I-check"],
    again: ["Play again", "再玩一次", "Laro ulit"],
    start: ["Start", "開始", "Simulan"],
    seeScore: ["See my score", "看我的分數", "Tingnan ang puntos ko"],
    of: ["{i} of {n}", "第 {i} / {n} 題", "{i} sa {n}"],
    roundOf: ["Round {i} of {n}", "第 {i} / {n} 回合", "Round {i} sa {n}"],
    good: [["Correct!", "Nice one!", "Galing!", "Spot on!"], ["答對了！", "太棒了！", "正確！", "好眼力！"], ["Tama!", "Ayos!", "Galing!", "Husay!"]],
    bad: [["Not quite.", "Almost — have a look.", "Good try."], ["再想想。", "差一點！", "不太對喔。"], ["Hindi pa.", "Malapit na!", "Subukan ulit!"]],
    done: ["You scored {s} of {n}.", "你得到 {s} / {n} 分。", "Nakakuha ka ng {s} sa {n}."],
    perfect: ["Perfect! Tala is cheering for you.", "滿分！Tala 正在為你歡呼。", "Perpekto! Pinapalakpakan ka ni Tala."],
    fine: ["Well done — check the explanations and try again for a perfect round.", "做得好——看看說明，再挑戰一次滿分吧。", "Magaling! Basahin ang paliwanag at subukan ulit para perpekto."],
    low: ["Every expert started here. Read the explanations, then play again.", "每位專家都是從這裡開始的。讀完說明再玩一次。", "Lahat ng eksperto ay nagsimula rito. Basahin ang paliwanag, tapos laro ulit."],
    talaSays: ["Tala", "Tala", "Tala"],
    yourAnswer: ["Your answer", "你的答案", "Sagot mo"],
    rightAnswer: ["Right answer", "正確答案", "Tamang sagot"],
    selected: ["selected", "已選取", "napili"],
    tapFirst: ["First tap a card, then tap where it goes.", "先點選一張卡片，再點它該放的位置。", "I-tap muna ang card, tapos i-tap kung saan ito ilalagay."],
    noContent: ["This activity has no questions yet.", "這個活動還沒有題目。", "Wala pang tanong ang activity na ito."],
    fictional: ["All people, places and numbers here are fictional.", "此處所有人物、地點與數字皆為虛構。", "Kathang-isip lamang ang lahat ng tao, lugar at numero rito."]
  };
  function U(key, o) { return fmt(L(UI[key]), o); }
  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
  function goodWord() { return pick(L(UI.good)); }
  function badWord() { return pick(L(UI.bad)); }

  /* ------------------------------------------------------------- helpers */
  function append(el, kids) {
    if (kids == null || kids === false) return el;
    if (Array.isArray(kids)) { for (var i = 0; i < kids.length; i++) append(el, kids[i]); return el; }
    el.appendChild(typeof kids === "object" && kids.nodeType ? kids : D.createTextNode(String(kids)));
    return el;
  }
  /** Create an HTML element: h("button", {class: "x", onclick: fn}, ["text"]). */
  function h(tag, props, kids) {
    var el = D.createElement(tag);
    setProps(el, props);
    return append(el, kids);
  }
  /** Create an SVG element. */
  function s(tag, props, kids) {
    var el = D.createElementNS(SVGNS, tag);
    setProps(el, props);
    return append(el, kids);
  }
  function setProps(el, props) {
    if (!props) return;
    for (var k in props) {
      if (!Object.prototype.hasOwnProperty.call(props, k)) continue;
      var v = props[k];
      if (v == null || v === false) continue;
      if (k === "class") el.setAttribute("class", v);
      else if (k === "text") el.textContent = v;
      else if (k.slice(0, 2) === "on" && typeof v === "function") el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? "" : v);
    }
  }
  function clear(el) { while (el && el.firstChild) el.removeChild(el.firstChild); return el; }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function sum(a) { var t = 0; for (var i = 0; i < a.length; i++) t += a[i]; return t; }
  function mean(a) { return a.length ? sum(a) / a.length : NaN; }
  function sd(a) {
    if (a.length < 2) return NaN;
    var m = mean(a), t = 0;
    for (var i = 0; i < a.length; i++) t += (a[i] - m) * (a[i] - m);
    return Math.sqrt(t / (a.length - 1));
  }
  /** Inline code-ish rendering: text with `backticks` becomes <code>. */
  function rich(text) {
    var parts = String(text).split("`");
    var out = [];
    for (var i = 0; i < parts.length; i++) {
      if (!parts[i]) continue;
      out.push(i % 2 ? h("code", null, parts[i]) : parts[i]);
    }
    return out;
  }
  function focusQuiet(el) {
    if (!el || !el.focus) return;
    try { el.focus({ preventScroll: true }); } catch (e) { el.focus(); }
  }

  /* --------------------------------------------------------- Tala & party */
  var FLAG = ["#0038A8", "#CE1126", "#FCD116", "#ffffff", "#FCD116"];
  /** Tala, the bright star (inline SVG). */
  function talaStar(size) {
    var pts = [];
    for (var i = 0; i < 10; i++) {
      var r = i % 2 ? 19 : 44;
      var a = -Math.PI / 2 + (i * Math.PI) / 5;
      pts.push((50 + r * Math.cos(a)).toFixed(1) + "," + (52 + r * Math.sin(a)).toFixed(1));
    }
    return s("svg", { class: "ph-tala", viewBox: "0 0 100 100", width: size || 44, height: size || 44, "aria-hidden": "true", focusable: "false" }, [
      s("polygon", { class: "ph-tala-body", points: pts.join(" ") }),
      s("circle", { class: "ph-tala-eye", cx: 42, cy: 50, r: 3.6 }),
      s("circle", { class: "ph-tala-eye", cx: 58, cy: 50, r: 3.6 }),
      s("path", { class: "ph-tala-mouth", d: "M43 59 Q50 66 57 59" }),
      s("circle", { class: "ph-tala-cheek", cx: 37, cy: 58, r: 3 }),
      s("circle", { class: "ph-tala-cheek", cx: 63, cy: 58, r: 3 })
    ]);
  }
  /** Banderitas (fiesta bunting) strip. */
  function banderitas() {
    var n = 18, kids = [s("path", { class: "ph-bunting-line", d: "M0 3 Q180 12 360 3" })];
    var cols = ["#0038A8", "#CE1126", "#FCD116", "#2a9d8f", "#f4a261", "#ffffff"];
    for (var i = 0; i < n; i++) {
      var x = 4 + i * 20;
      var y = 3 + 9 * (1 - Math.pow((x - 180) / 180, 2)) * 0.95;
      kids.push(s("polygon", {
        class: "ph-flaglet", points: x + "," + y.toFixed(1) + " " + (x + 14) + "," + y.toFixed(1) + " " + (x + 7) + "," + (y + 14).toFixed(1),
        fill: cols[i % cols.length], style: "--i:" + i
      }));
    }
    return s("svg", { class: "ph-bunting", viewBox: "0 0 360 30", preserveAspectRatio: "none", "aria-hidden": "true", focusable: "false" }, kids);
  }

  /* ----------------------------------------------------------- instances */
  var WIDGETS = {};
  var instances = [];

  /** Context passed to a widget: shell parts, feedback, score, safe timers. */
  function makeCtx(host, name) {
    var ctx = {
      host: host, name: name, lang: detectLang(), alive: true,
      classes: (host.getAttribute("class") || "").split(/\s+/),
      _timers: [], _intervals: [], _frames: [], _listeners: [], _cleanups: []
    };
    ctx.has = function (cls) { return ctx.classes.indexOf(cls) >= 0; };
    ctx.option = function (prefix) {
      for (var i = 0; i < ctx.classes.length; i++) {
        if (ctx.classes[i].indexOf(prefix) === 0) return ctx.classes[i].slice(prefix.length);
      }
      return null;
    };
    ctx.later = function (fn, ms) {
      var id = W.setTimeout(function () { if (ctx.alive) fn(); }, ms || 0);
      ctx._timers.push(id);
      return id;
    };
    ctx.every = function (fn, ms) {
      var id = W.setInterval(function () { if (ctx.alive) fn(); }, ms);
      ctx._intervals.push(id);
      return id;
    };
    ctx.stopEvery = function (id) { W.clearInterval(id); };
    ctx.frame = function (fn) {
      var id = W.requestAnimationFrame(function (t) { if (ctx.alive) fn(t); });
      ctx._frames.push(id);
      return id;
    };
    ctx.listen = function (target, type, fn, opts) {
      target.addEventListener(type, fn, opts);
      ctx._listeners.push([target, type, fn, opts]);
    };
    ctx.onDestroy = function (fn) { ctx._cleanups.push(fn); };
    return ctx;
  }

  function destroyCtx(ctx) {
    if (!ctx || !ctx.alive) return;
    ctx.alive = false;
    ctx._timers.forEach(function (id) { W.clearTimeout(id); });
    ctx._intervals.forEach(function (id) { W.clearInterval(id); });
    ctx._frames.forEach(function (id) { W.cancelAnimationFrame(id); });
    ctx._listeners.forEach(function (l) { l[0].removeEventListener(l[1], l[2], l[3]); });
    ctx._cleanups.forEach(function (fn) { try { fn(); } catch (e) { /* ignore */ } });
    if (ctx.root && ctx.root.parentNode) ctx.root.parentNode.removeChild(ctx.root);
    if (ctx.host) {
      ctx.host.classList.remove("ph-game-ready");
      if (ctx.host.__phGame === ctx) ctx.host.__phGame = null;
    }
    var i = instances.indexOf(ctx);
    if (i >= 0) instances.splice(i, 1);
  }

  /**
   * Build the card shell: bunting, title row with score, body, feedback
   * (a polite live region with Tala) and a controls row.
   */
  function shell(ctx, title, intro) {
    var root = h("section", { class: "ph-w ph-w-" + ctx.name + (ctx.has("ph-compact") ? " ph-compact" : ""), "aria-label": title, lang: ["en", "zh-Hant", "fil"][LI] });
    var party = h("div", { class: "ph-party-layer", "aria-hidden": "true" });
    var scoreEl = h("span", { class: "ph-score", hidden: true });
    var head = h("div", { class: "ph-w-head" }, [
      h("div", { class: "ph-w-title", role: "heading", "aria-level": "3" }, title),
      scoreEl
    ]);
    var introEl = intro ? h("p", { class: "ph-w-intro" }, rich(intro)) : null;
    var body = h("div", { class: "ph-w-body" });
    var fbText = h("div", { class: "ph-fb-text" });
    var star = talaStar(40);
    var fb = h("div", { class: "ph-fb", "data-kind": "idle" }, [star, fbText]);
    var live = h("div", { class: "ph-sr", role: "status", "aria-live": "polite", "aria-atomic": "true" });
    var controls = h("div", { class: "ph-w-controls" });
    append(root, [banderitas(), party, head, introEl, body, fb, live, controls,
      h("p", { class: "ph-w-note" }, U("fictional"))]);
    fb.hidden = true;
    ctx.root = root; ctx.body = body; ctx.controls = controls; ctx.fb = fb; ctx.party = party;
    ctx.setScore = function (val, max) {
      scoreEl.hidden = false;
      scoreEl.textContent = U("score") + " " + val + (max != null ? " / " + max : "");
    };
    /** Show feedback. kind: good | bad | info | party. content: string or nodes. */
    ctx.say = function (kind, content, lead) {
      fb.hidden = false;
      fb.setAttribute("data-kind", kind);
      clear(fbText);
      if (lead) append(fbText, h("strong", { class: "ph-fb-lead" }, lead + " "));
      append(fbText, typeof content === "string" ? rich(content) : content);
      live.textContent = fbText.textContent;
      star.classList.remove("ph-cheer", "ph-think");
      void star.getBoundingClientRect();
      if (kind === "good" || kind === "party") star.classList.add("ph-cheer");
      if (kind === "bad") star.classList.add("ph-think");
    };
    ctx.hush = function () { fb.hidden = true; clear(fbText); };
    ctx.announce = function (text) { live.textContent = text; };
    ctx.celebrate = function (big) { celebrate(ctx, big); };
    ctx.button = function (label, fn, cls) {
      return h("button", { type: "button", class: "ph-btn " + (cls || ""), onclick: fn }, label);
    };
    return root;
  }

  function celebrate(ctx, big) {
    var root = ctx.root;
    if (!root) return;
    root.classList.remove("ph-party");
    void root.offsetWidth;
    root.classList.add("ph-party");
    ctx.later(function () { root.classList.remove("ph-party"); }, 2600);
    if (reduced()) return;
    var n = big ? 46 : 22;
    for (var i = 0; i < n; i++) {
      var piece = h("i", {
        class: "ph-confetto" + (i % 3 === 0 ? " ph-sun" : ""),
        style: "--x:" + (Math.random() * 100).toFixed(1) + "%;--d:" + (Math.random() * 0.6).toFixed(2) + "s;--r:" +
          Math.round(Math.random() * 720 - 360) + "deg;--c:" + FLAG[i % FLAG.length] + ";--s:" + (0.7 + Math.random() * 0.8).toFixed(2)
      });
      ctx.party.appendChild(piece);
    }
    ctx.later(function () { clear(ctx.party); }, 2800);
  }

  /**
   * Generic question sequence used by several widgets.
   * cfg.items(): fresh array of items; cfg.render(item, api) draws one item
   * into api.box and calls api.answer(points, maxPoints, kind, content).
   */
  function sequence(ctx, cfg) {
    var items = [], idx = 0, score = 0, max = 0;
    function start() {
      items = cfg.items() || [];
      idx = 0; score = 0; max = 0;
      for (var i = 0; i < items.length; i++) max += cfg.points ? cfg.points(items[i]) : 1;
      if (!items.length) { clear(ctx.body); append(ctx.body, h("p", null, U("noContent"))); return; }
      ctx.setScore(0, max);
      show(false);
    }
    function show(moveFocus) {
      ctx.hush();
      clear(ctx.body); clear(ctx.controls);
      var item = items[idx];
      var progress = h("p", { class: "ph-progress" }, [
        h("span", { class: "ph-dots", "aria-hidden": "true" }, items.map(function (_, k) {
          return h("i", { class: k < idx ? "done" : k === idx ? "now" : "" });
        })),
        h("span", null, U(cfg.roundLabel ? "roundOf" : "of", { i: idx + 1, n: items.length }))
      ]);
      var box = h("div", { class: "ph-item" });
      append(ctx.body, [progress, box]);
      var answered = false;
      cfg.render(item, {
        box: box,
        index: idx,
        answer: function (pts, kind, content, lead) {
          if (answered) return;
          answered = true;
          score += pts;
          ctx.setScore(score, max);
          ctx.say(kind, content, lead);
          if (kind === "good") ctx.celebrate(false);
          var last = idx === items.length - 1;
          var nb = ctx.button(last ? "★ " + U("seeScore") : U("next") + " →", function () {
            if (last) end(); else { idx++; show(true); }
          }, "ph-primary");
          clear(ctx.controls);
          append(ctx.controls, nb);
          focusQuiet(nb);
        }
      });
      if (moveFocus) {
        var q = box.querySelector("[data-focus]") || box;
        if (!q.hasAttribute("tabindex")) q.setAttribute("tabindex", "-1");
        focusQuiet(q);
      }
    }
    function end() {
      endScreen(ctx, score, max, start, cfg.endNote);
    }
    start();
    return { restart: start };
  }

  /** Final score card with replay. */
  function endScreen(ctx, score, max, replay, note) {
    ctx.hush();
    clear(ctx.body); clear(ctx.controls);
    var ratio = max ? score / max : 0;
    var msg = ratio === 1 ? U("perfect") : ratio >= 0.6 ? U("fine") : U("low");
    var box = h("div", { class: "ph-end", tabindex: "-1" }, [
      talaStar(88),
      h("p", { class: "ph-end-score" }, U("done", { s: score, n: max })),
      h("p", null, msg),
      note ? h("p", { class: "ph-end-note" }, rich(L(note))) : null
    ]);
    append(ctx.body, box);
    ctx.announce(box.textContent);
    if (ratio >= 0.6) ctx.celebrate(ratio === 1);
    var again = ctx.button("↻ " + U("again"), replay, "ph-primary");
    append(ctx.controls, again);
    focusQuiet(box);
  }

  /** Roving tabindex + arrow keys for a group of buttons. */
  function roving(container, selector, opts) {
    opts = opts || {};
    function items() { return Array.prototype.slice.call(container.querySelectorAll(selector)); }
    function setActive(el) {
      items().forEach(function (b) { b.setAttribute("tabindex", b === el ? "0" : "-1"); });
    }
    container.addEventListener("keydown", function (e) {
      var list = items();
      var i = list.indexOf(D.activeElement);
      if (i < 0) return;
      var cols = opts.cols || list.length;
      var j = -1;
      if (e.key === "ArrowRight" || (!opts.cols && e.key === "ArrowDown")) j = Math.min(list.length - 1, i + 1);
      else if (e.key === "ArrowLeft" || (!opts.cols && e.key === "ArrowUp")) j = Math.max(0, i - 1);
      else if (opts.cols && e.key === "ArrowDown") j = Math.min(list.length - 1, i + cols);
      else if (opts.cols && e.key === "ArrowUp") j = Math.max(0, i - cols);
      else if (e.key === "Home") j = 0;
      else if (e.key === "End") j = list.length - 1;
      if (j < 0) return;
      e.preventDefault();
      setActive(list[j]);
      focusQuiet(list[j]);
    });
    container.addEventListener("focusin", function (e) {
      if (items().indexOf(e.target) >= 0) setActive(e.target);
    });
    var first = items()[0];
    if (first) setActive(first);
  }

  /** Two-option button choice block. opts: [{label, value}] */
  function choiceButtons(options, onPick, cls) {
    var wrap = h("div", { class: "ph-choices " + (cls || ""), role: "group" });
    var buttons = options.map(function (o) {
      return h("button", {
        type: "button", class: "ph-choice", "data-value": o.value,
        onclick: function () { onPick(o, buttons, this); }
      }, o.label);
    });
    append(wrap, buttons);
    wrap.buttons = buttons;
    return wrap;
  }
  function lockChoices(buttons, correctValue, chosenBtn) {
    buttons.forEach(function (b) {
      b.disabled = true;
      if (b.getAttribute("data-value") === String(correctValue)) b.classList.add("is-right");
    });
    if (chosenBtn && chosenBtn.getAttribute("data-value") !== String(correctValue)) chosenBtn.classList.add("is-wrong");
    if (chosenBtn) chosenBtn.setAttribute("aria-pressed", "true");
  }

  /* ================================================== prompt-pick (ch 00) */
  var PROMPTS = [
    {
      bad: ["Make a chart of my dengue data.", "幫我把登革熱資料畫成圖。", "Gawan mo ng chart ang dengue data ko."],
      good: ["I have a pandas DataFrame `df`, one row per case. Columns: `onset_date` (text like 2026-08-03) and `barangay`. Write Python that counts cases per onset day and draws a bar chart with no gaps between days and dates on the x-axis.",
        "我有一個 pandas DataFrame `df`，每一列是一位病例。欄位：`onset_date`（文字，例如 2026-08-03）與 `barangay`。請寫 Python 依發病日計算病例數，畫出日與日之間沒有間隙、x 軸為日期的長條圖。",
        "May pandas DataFrame akong `df`, isang row bawat kaso. Columns: `onset_date` (text tulad ng 2026-08-03) at `barangay`. Sumulat ng Python na bibilang ng kaso bawat araw ng onset at gagawa ng bar chart na walang puwang sa pagitan ng mga araw, petsa sa x-axis."],
      why: ["The better prompt names the columns, says what one row is and describes the exact output. Tala cannot see your file — it has to guess everything you leave out.",
        "較好的提示寫出欄位名稱、說明每一列代表什麼，並描述確切的輸出。Tala 看不到你的檔案——你沒說的，它只能用猜的。",
        "Mas maganda ang prompt na may pangalan ng columns, sinasabi kung ano ang isang row, at kung ano mismo ang output. Hindi nakikita ni Tala ang file mo — huhulaan niya ang lahat ng hindi mo sinabi."]
    },
    {
      bad: ["Why is the age wrong in my first rows? Rodel Manalo, 5o, 0900 555 0142, 12 Mabini St. Purok 4 Brgy. Ilog / Liza Santos, , 0900 555 0199, Purok 1 Brgy. Sapa",
        "為什麼我前幾列的年齡有錯？Rodel Manalo, 5o, 0900 555 0142, 12 Mabini St. Purok 4 Brgy. Ilog / Liza Santos, , 0900 555 0199, Purok 1 Brgy. Sapa",
        "Bakit mali ang age sa unang rows ko? Rodel Manalo, 5o, 0900 555 0142, 12 Mabini St. Purok 4 Brgy. Ilog / Liza Santos, , 0900 555 0199, Purok 1 Brgy. Sapa"],
      good: ["Here are 3 made-up rows with the same columns as my file: `case_id`=C001, `age`='52' / C002, '5o' / C003, ''. Why does converting `age` to a number fail, and how do I list the bad values?",
        "這裡有 3 列虛構資料，欄位和我的檔案相同：`case_id`=C001, `age`='52' / C002, '5o' / C003, ''。為什麼把 `age` 轉成數字會失敗？要怎麼列出有問題的值？",
        "Heto ang 3 gawa-gawang rows na pareho ang columns sa file ko: `case_id`=C001, `age`='52' / C002, '5o' / C003, ''. Bakit pumapalya ang pag-convert ng `age` sa number, at paano ko ililista ang maling values?"],
      why: ["Never paste real names, phone numbers or addresses into an AI chat — that sends real people's personal information outside the office. Made-up rows with the same shape show the problem just as well: the letter o in '5o' and a blank.",
        "絕不要把真實姓名、電話或地址貼進 AI 對話——這等於把真實民眾的個人資料送出辦公室。相同結構的虛構資料一樣能呈現問題：'5o' 裡的字母 o，以及空白值。",
        "Huwag kailanman mag-paste ng totoong pangalan, numero ng telepono o address sa AI chat — inilalabas nito ng opisina ang personal information ng totoong tao. Kita pa rin ang problema sa gawa-gawang rows: ang letrang o sa '5o' at ang blangko."]
    },
    {
      bad: ["My code doesn't work. Fix it.", "我的程式不能跑，幫我修。", "Ayaw gumana ng code ko. Ayusin mo."],
      good: ["Running `df['Onset_Date']` gives `KeyError: 'Onset_Date'`. My columns are `case_id`, `onset_date`, `age`, `sex`. Explain what the error means, then fix the line.",
        "執行 `df['Onset_Date']` 出現 `KeyError: 'Onset_Date'`。我的欄位是 `case_id`、`onset_date`、`age`、`sex`。請解釋這個錯誤的意思，再修正那一行。",
        "Pag pinatakbo ko ang `df['Onset_Date']`, lumalabas ang `KeyError: 'Onset_Date'`. Ang columns ko ay `case_id`, `onset_date`, `age`, `sex`. Ipaliwanag ang error, tapos ayusin ang linya."],
      why: ["Give the exact error message and the column names. The error already tells the story: the column is `onset_date` in lower case, and Python names are case-sensitive.",
        "附上完整的錯誤訊息與欄位名稱。錯誤訊息本身就說明了一切：欄位叫 `onset_date`（小寫），而 Python 的名稱區分大小寫。",
        "Ibigay ang eksaktong error message at ang pangalan ng columns. Ang error na mismo ang nagsasabi: `onset_date` (maliit na titik) ang column, at case-sensitive ang mga pangalan sa Python."]
    },
    {
      bad: ["Compute the attack rate for each barangay.", "幫我算每個 barangay 的侵襲率。", "I-compute ang attack rate ng bawat barangay."],
      good: ["Compute the attack rate per barangay as cases ÷ barangay population × 10,000. Cases: count rows of `linelist` by `barangay`. Population: column `population` in `barangays`. Return a table sorted from the highest rate.",
        "請以「病例數 ÷ barangay 人口 × 10,000」計算各 barangay 的侵襲率。病例數：依 `barangay` 計算 `linelist` 的列數。人口：`barangays` 的 `population` 欄。輸出由高到低排序的表格。",
        "I-compute ang attack rate bawat barangay: kaso ÷ populasyon ng barangay × 10,000. Kaso: bilangin ang rows ng `linelist` ayon sa `barangay`. Populasyon: column na `population` sa `barangays`. Ibalik bilang table, mula pinakamataas na rate."],
      why: ["A rate needs a denominator. If you don't say which one, an AI may divide by the number of rows, or by the whole city. Name the numerator, the denominator and the unit (per 10,000).",
        "率一定要有分母。你沒指定，AI 可能拿列數或全市人口來除。請寫清楚分子、分母和單位（每 10,000 人）。",
        "Kailangan ng denominator ang rate. Kung hindi mo sasabihin, baka hatiin ng AI sa bilang ng rows, o sa buong lungsod. Sabihin ang numerator, denominator at unit (bawat 10,000)."]
    },
    {
      bad: ["Write the epi curve code. I'll paste the chart straight into the report.", "幫我寫流行曲線的程式，我會直接把圖貼進報告。", "Isulat mo ang code ng epi curve. Diretso ko nang ilalagay sa report."],
      good: ["Write the epi curve code, then give me 5 made-up rows I can count by hand and the count per day your code should print for them.",
        "請寫流行曲線的程式，並另外給我 5 列可以手算的虛構資料，以及程式對這 5 列應該印出的每日病例數。",
        "Isulat ang code ng epi curve, tapos bigyan mo ako ng 5 gawa-gawang rows na kaya kong bilangin nang mano-mano, at ang bilang bawat araw na dapat i-print ng code."],
      why: ["Ask → Run → Check. A tiny test you can count by hand turns 'looks right' into 'is right'. Unchecked AI output never goes into a report.",
        "提問 → 執行 → 檢查。一個能手算的小測試，讓「看起來對」變成「確定是對的」。未經檢查的 AI 產出，絕不放進報告。",
        "Ask → Run → Check. Ang maliit na test na kayang bilangin nang mano-mano ang nagpapatunay na tama talaga, hindi lang mukhang tama. Hindi pumapasok sa report ang AI output na hindi na-check."]
    }
  ];

  WIDGETS["prompt-pick"] = function (ctx) {
    var title = L(["Pick the better prompt", "選出比較好的提示", "Piliin ang mas magandang prompt"]);
    var intro = L(["Maya is about to ask Tala for help. Which message should she send?", "Maya 正要請 Tala 幫忙。她該送出哪一則訊息？", "Hihingi ng tulong si Maya kay Tala. Alin ang dapat niyang i-send?"]);
    ctx.host.appendChild(shell(ctx, title, intro));
    sequence(ctx, {
      items: function () { return shuffle(PROMPTS); },
      render: function (item, api) {
        var opts = shuffle([{ text: item.good, value: "good" }, { text: item.bad, value: "bad" }]);
        var buttons = opts.map(function (o, k) {
          return h("button", { type: "button", class: "ph-prompt", "data-value": o.value, "data-focus": k === 0 ? "" : null,
            onclick: function () {
              var ok = o.value === "good";
              lockChoices(buttons, "good", this);
              api.answer(ok ? 1 : 0, ok ? "good" : "bad", L(item.why), ok ? goodWord() : badWord());
            }
          }, [h("span", { class: "ph-prompt-tag" }, (k ? "B" : "A") + " · Maya → Tala"), h("span", { class: "ph-prompt-text" }, rich(L(o.text)))]);
        });
        append(api.box, h("div", { class: "ph-prompts" }, buttons));
      },
      endNote: ["Good prompts: name the columns, show made-up example rows, state the output — and ask for a way to check it.",
        "好的提示：寫出欄位名稱、附上虛構範例資料、說明想要的輸出——再請 AI 給你檢查的方法。",
        "Magandang prompt: pangalan ng columns, gawa-gawang sample rows, malinaw na output — at humingi ng paraan para i-check ito."]
    });
  };

  /* ===================================================== bug-hunt (ch 01) */
  var BUGS = [
    {
      task: ["Tala was asked for the case fatality rate (CFR) of leptospirosis in Barangay Ilog.", "Maya 請 Tala 計算 Barangay Ilog 鉤端螺旋體病的致死率（CFR）。", "Hiningi kay Tala ang case fatality rate (CFR) ng leptospirosis sa Barangay Ilog."],
      code: ["cases = 39", "deaths = 6", "population = 13411", "cfr = deaths / population * 100", "print(round(cfr, 1), \"%\")"],
      bug: [3],
      fix: "cfr = deaths / cases * 100      # 15.4 %",
      why: ["CFR is deaths among cases, so the denominator is the 39 cases, not the 13,411 residents. Dividing by the population gives a mortality rate (0.04 %), a different measure.",
        "致死率是「病例中」的死亡比例，分母是 39 位病例，不是 13,411 位居民。除以人口得到的是死亡率（0.04%），是另一種指標。",
        "Ang CFR ay mga namatay sa mga kaso, kaya ang denominator ay ang 39 kaso, hindi ang 13,411 residente. Kapag populasyon ang hinati, mortality rate (0.04%) ang lalabas — ibang sukatan iyon."]
    },
    {
      task: ["Print the last barangay in the list.", "印出清單中最後一個 barangay。", "I-print ang huling barangay sa listahan."],
      code: ["barangays = [\"Ilog\", \"Sapa\", \"Baybay\"]", "print(barangays[0])    # Ilog", "print(barangays[3])    # Baybay?"],
      bug: [2],
      fix: "print(barangays[2])    # or barangays[-1]",
      why: ["Python counts from 0: the three items are [0], [1] and [2]. Asking for [3] raises IndexError. [-1] always means 'the last one'.",
        "Python 從 0 開始數：三個項目是 [0]、[1]、[2]。要 [3] 會出現 IndexError。[-1] 永遠代表「最後一個」。",
        "Nagsisimula sa 0 ang bilang ng Python: [0], [1] at [2] ang tatlong items. Kapag [3] ang hiningi, IndexError. Ang [-1] ay laging 'ang huli'."]
    },
    {
      task: ["Read Jun's Excel export of the line list.", "讀入 Jun 匯出的 Excel 造冊（line list）。", "Basahin ang Excel export ni Jun ng line list."],
      code: ["import pandas as pd", "df = pd.read_spreadsheet(\"linelist.xlsx\")", "print(df.head())"],
      bug: [1],
      fix: "df = pd.read_excel(\"linelist.xlsx\")",
      why: ["Tala invented a function: pandas has no `read_spreadsheet`, so Python raises AttributeError. The real one is `pd.read_excel`. When a name looks plausible but fails, check the documentation.",
        "Tala 編造了一個函式：pandas 沒有 `read_spreadsheet`，Python 會出現 AttributeError。正確的是 `pd.read_excel`。名稱看似合理卻失敗時，去查官方文件。",
        "Nag-imbento si Tala ng function: walang `read_spreadsheet` ang pandas, kaya AttributeError. Ang totoo ay `pd.read_excel`. Kapag mukhang tama ang pangalan pero pumalya, tingnan ang documentation."]
    },
    {
      task: ["Flag cases aged 60 and over.", "標記 60 歲以上的病例。", "Markahan ang mga kasong 60 taong gulang pataas."],
      code: ["row = {\"case_id\": \"C017\", \"age\": \"64\", \"sex\": \"M\"}", "age = row[\"age\"]", "if age >= 60:", "    print(\"senior\", row[\"case_id\"])"],
      bug: [1, 2],
      fix: "age = int(row[\"age\"])          # \"64\" -> 64",
      why: ["The age arrived as text (\"64\" in quotes). Python cannot compare text with a number, so line 3 raises TypeError — the real fix is converting on line 2 with `int()`.",
        "年齡是以文字形式（加了引號的 \"64\"）讀進來的。Python 不能拿文字和數字比大小，所以第 3 行出現 TypeError——真正的修正是在第 2 行用 `int()` 轉換。",
        "Text ang dating ng age (\"64\" na may quotes). Hindi kayang ikumpara ng Python ang text sa number, kaya TypeError sa line 3 — ang tunay na ayos ay i-convert sa line 2 gamit ang `int()`."]
    },
    {
      task: ["A function for the attack rate per 10,000.", "計算每 10,000 人侵襲率的函式。", "Function para sa attack rate bawat 10,000."],
      code: ["def attack_rate(cases, population):", "    rate = cases / population * 10_000", "", "print(attack_rate(39, 13411))   # prints None"],
      bug: [1],
      fix: "    rate = cases / population * 10_000\n    return rate                  # 29.08...",
      why: ["The function computes `rate` but never hands it back. Without `return`, Python returns None. Add `return rate` at the end of the function.",
        "函式算出了 `rate` 卻沒有把它交回來。沒有 `return`，Python 就回傳 None。在函式最後加上 `return rate`。",
        "Kinukuwenta ng function ang `rate` pero hindi ibinabalik. Kapag walang `return`, None ang ibinabalik ng Python. Idagdag ang `return rate` sa dulo ng function."]
    }
  ];

  WIDGETS["bug-hunt"] = function (ctx) {
    var title = L(["Bug hunt: where did Tala go wrong?", "抓蟲：Tala 哪裡寫錯了？", "Bug hunt: saan nagkamali si Tala?"]);
    var intro = L(["Read the AI-written code and tap the line with the mistake.", "讀一讀 AI 寫的程式，點出有錯的那一行。", "Basahin ang code na isinulat ng AI at i-tap ang linyang may mali."]);
    ctx.host.appendChild(shell(ctx, title, intro));
    sequence(ctx, {
      items: function () { return shuffle(BUGS); },
      render: function (item, api) {
        append(api.box, h("p", { class: "ph-task", "data-focus": "" }, [h("strong", null, "🐞 "), L(item.task)]));
        var list = h("div", { class: "ph-code", role: "group", "aria-label": L(["Code lines", "程式碼行", "Mga linya ng code"]) });
        var buttons = item.code.map(function (line, i) {
          return h("button", { type: "button", class: "ph-line", "aria-label": L(["Line", "第", "Linya"]) + " " + (i + 1) + (LI === 1 ? " 行" : "") + ": " + (line || "—"),
            onclick: function () {
              var ok = item.bug.indexOf(i) >= 0;
              buttons.forEach(function (b, k) {
                b.disabled = true;
                if (item.bug.indexOf(k) >= 0) b.classList.add("is-right");
              });
              if (!ok) this.classList.add("is-wrong");
              var expl = [h("span", null, rich(L(item.why))), h("pre", { class: "ph-fix" }, [h("span", { class: "ph-fix-tag" }, "✓ fix"), "\n" + item.fix])];
              api.answer(ok ? 1 : 0, ok ? "good" : "bad", expl, ok ? goodWord() : badWord());
            }
          }, [h("span", { class: "ph-ln", "aria-hidden": "true" }, String(i + 1)), h("code", null, line || " ")]);
        });
        append(list, buttons);
        roving(list, ".ph-line");
        append(api.box, list);
      },
      endNote: ["AI code can look perfect and still be wrong. Read it line by line, run it on a case you can count by hand, and read the error message.",
        "AI 寫的程式看起來完美也可能是錯的。逐行閱讀、用能手算的小例子執行，並讀懂錯誤訊息。",
        "Kahit mukhang perpekto ang AI code, puwedeng mali pa rin. Basahin linya-linya, patakbuhin sa kasong kayang bilangin nang mano-mano, at basahin ang error message."]
    });
  };

  /* ================================================ publish-check (ch 09) */
  function miniTable(head, rows) {
    return h("table", { class: "ph-mini-table" }, [
      h("thead", null, h("tr", null, head.map(function (c) { return h("th", null, L(c)); }))),
      h("tbody", null, rows.map(function (r) { return h("tr", null, r.map(function (c) { return h("td", null, L(c)); })); }))
    ]);
  }
  function miniBars(values, labels, yStart) {
    var max = Math.max.apply(null, values), w = 240, hgt = 92, n = values.length, bw = w / n;
    var lo = yStart || 0;
    var kids = [s("line", { x1: 18, y1: hgt, x2: w + 18, y2: hgt, class: "ph-axis" }),
      s("text", { x: 14, y: hgt, class: "ph-tick", "text-anchor": "end" }, String(lo)),
      s("text", { x: 14, y: 10, class: "ph-tick", "text-anchor": "end" }, String(max))];
    values.forEach(function (v, i) {
      var bh = ((v - lo) / (max - lo)) * (hgt - 8);
      kids.push(s("rect", { x: 18 + i * bw, y: hgt - bh, width: bw - 0.5, height: Math.max(0, bh), class: "ph-bar" }));
      if (labels && i % 2 === 0) kids.push(s("text", { x: 18 + i * bw + bw / 2, y: hgt + 11, class: "ph-tick", "text-anchor": "middle" }, labels[i]));
    });
    return s("svg", { viewBox: "0 0 262 108", class: "ph-mini-chart", role: "img", "aria-label": values.join(", ") }, kids);
  }
  function miniDots() {
    var kids = [s("rect", { x: 0, y: 0, width: 240, height: 110, rx: 8, class: "ph-mini-land" }),
      s("path", { d: "M80 0 C 95 30, 70 60, 92 110", class: "ph-mini-river" })];
    var pts = [[60, 20], [66, 28], [98, 40], [102, 46], [74, 64], [88, 70], [120, 30], [160, 52], [64, 90], [110, 88], [98, 62]];
    pts.forEach(function (p) { kids.push(s("circle", { cx: p[0], cy: p[1], r: 4, class: "ph-mini-dot" })); });
    kids.push(s("text", { x: 104, y: 44, class: "ph-tick" }, "12 Mabini St."));
    return s("svg", { viewBox: "0 0 240 110", class: "ph-mini-chart", role: "img", "aria-label": L(["Map with one dot per case at the house", "每位病例住家一個點的地圖", "Mapa na may tuldok sa bahay ng bawat kaso"]) }, kids);
  }
  var PUBLISH = [
    { ok: true, kind: ["KPI tiles", "KPI 數字卡", "KPI tiles"],
      view: function () { return h("div", { class: "ph-kpis" }, [h("div", { class: "ph-kpi" }, [h("b", null, "618"), h("span", null, L(["cases, city, 20 Jul–30 Sep", "病例（全市，7/20–9/30）", "kaso, buong lungsod, 20 Hul–30 Set"]))]), h("div", { class: "ph-kpi" }, [h("b", null, "21"), h("span", null, L(["deaths, city", "死亡（全市）", "namatay, buong lungsod"]))])]); },
      why: ["City-wide totals do not point to any person. Approve.", "全市總數不會指向任何個人，可以發布。", "Hindi tumuturo sa sinumang tao ang kabuuan ng buong lungsod. Aprubado."] },
    { ok: false, kind: ["Table by barangay", "各 barangay 病例表", "Table ayon sa barangay"],
      view: function () { return miniTable([["Barangay", "Barangay", "Barangay"], ["Lepto cases", "鉤端螺旋體病例", "Lepto cases"]], [["Ilog", "39"], ["Pampang", "31"], ["Kawayanan", "5"], ["Talahib", "1"]]); },
      why: ["Small cell: 1 case in Talahib, a small upland barangay — neighbours can work out who they are. Suppress counts of 1–4 (show '<5') or merge areas before publishing.",
        "小格：人口少的山區 Talahib 只有 1 例——鄰居猜得出是誰。發布前將 1–4 的數字遮蔽（顯示「<5」）或合併區域。",
        "Small cell: 1 kaso sa Talahib, maliit na upland barangay — mahuhulaan ng kapitbahay kung sino sila. I-suppress ang bilang na 1–4 (ipakita bilang '<5') o pagsamahin ang lugar bago i-publish."] },
    { ok: false, kind: ["Case map", "病例地圖", "Mapa ng kaso"], view: miniDots,
      why: ["One dot per house is an address map. Publish rates by barangay (a choropleth) instead of exact locations.",
        "每戶一個點等於公布地址。改用各 barangay 的侵襲率面量圖（choropleth），不要公布確切位置。",
        "Ang isang tuldok bawat bahay ay mapa ng address. Rate bawat barangay (choropleth) ang i-publish, hindi eksaktong lokasyon."] },
    { ok: false, kind: ["'Latest deaths' box", "「最新死亡」區塊", "Kahon ng 'Pinakabagong namatay'"],
      view: function () { return h("p", { class: "ph-mini-note" }, L(["Female, 67, Purok 2, Brgy. Sapa — died 12 Sep 2026", "女性，67 歲，Brgy. Sapa 第 2 Purok——2026/9/12 死亡", "Babae, 67, Purok 2, Brgy. Sapa — namatay 12 Set 2026"])); },
      why: ["No name, but sex + age + purok + date together identify her to everyone on her street. Report deaths as a count at city level.",
        "雖然沒有姓名，但性別＋年齡＋purok＋日期加在一起，整條街的人都知道是誰。死亡只以全市總數呈現。",
        "Walang pangalan, pero ang kasarian + edad + purok + petsa ay sapat para makilala siya ng buong kalye. Iulat ang namatay bilang bilang sa antas ng lungsod."] },
    { ok: true, kind: ["Weekly epi curve", "每週流行曲線", "Lingguhang epi curve"],
      view: function () { return miniBars([14, 11, 33, 28, 48, 34, 58, 63, 54, 45], ["W30", "", "W32", "", "W34", "", "W36", "", "W38", ""]); },
      why: ["City-wide weekly counts starting at zero: informative and safe. Approve.", "全市每週病例數、y 軸從 0 開始：有資訊又安全，可以發布。", "Lingguhang bilang ng buong lungsod, nagsisimula sa zero: may silbi at ligtas. Aprubado."] },
    { ok: false, kind: ["Chart with a zoomed axis", "y 軸被截斷的圖", "Chart na naka-zoom ang axis"],
      view: function () { return miniBars([48, 50, 52, 55], ["Jun", "", "Aug", ""], 46); },
      why: ["The y-axis starts at 46, so a rise from 48 to 55 looks like a tripling. Bars must start at 0 — an honest dashboard is part of the publish check.",
        "y 軸從 46 開始，48 到 55 的增加看起來像翻了三倍。長條圖必須從 0 開始——誠實的儀表板也是發布檢查的一部分。",
        "Nagsisimula sa 46 ang y-axis, kaya ang pagtaas mula 48 hanggang 55 ay mukhang triple. Dapat magsimula sa 0 ang bars — kasama sa publish check ang pagiging tapat ng dashboard."] },
    { ok: true, kind: ["Age × sex table (city)", "年齡 × 性別表（全市）", "Table ng edad × kasarian (lungsod)"],
      view: function () { return miniTable([["Age", "年齡", "Edad"], ["Male", "男", "Lalaki"], ["Female", "女", "Babae"]], [["0–14", "86", "98"], ["15–44", "191", "126"], ["45+", "68", "42"]]); },
      why: ["City-wide groups, every cell well above 5. Approve.", "全市分組、每格都遠大於 5，可以發布。", "Pangkat sa buong lungsod, lahat ng cell ay higit sa 5. Aprubado."] },
    { ok: false, kind: ["Download button", "下載按鈕", "Download button"],
      view: function () { return h("span", { class: "ph-mini-btn" }, "⬇ " + L(["Download full line list (CSV)", "下載完整造冊（CSV）", "I-download ang buong line list (CSV)"])); },
      why: ["Case-level records never go on a public dashboard — even without names, rows can be linked back to people. Share aggregates only.",
        "個案層級資料絕不放上公開儀表板——即使沒有姓名，每一列仍可能被連回本人。只分享彙總資料。",
        "Hindi kailanman inilalagay sa public dashboard ang case-level records — kahit walang pangalan, puwedeng matunton ang tao. Aggregates lang ang ibahagi."] },
    { ok: true, kind: ["Footer", "頁尾說明", "Footer"],
      view: function () { return h("p", { class: "ph-mini-note" }, L(["Source: Santa Luz CESU, data as of 30 Sep 2026 (provisional). Counts below 5 shown as '<5'.", "資料來源：Santa Luz CESU，資料截至 2026/9/30（初步資料）。少於 5 的數字顯示為「<5」。", "Pinagmulan: Santa Luz CESU, datos hanggang 30 Set 2026 (provisional). Ang bilang na mas mababa sa 5 ay '<5'."])); },
      why: ["Source, date and the suppression rule tell readers how to read the numbers. Approve.", "資料來源、日期與小格遮蔽規則，告訴讀者如何解讀數字。可以發布。", "Ang source, petsa at suppression rule ay gabay sa pagbasa ng mga numero. Aprubado."] }
  ];

  WIDGETS["publish-check"] = function (ctx) {
    var title = L(["Doc Mon's publish check", "Doc Mon 的發布檢查", "Publish check ni Doc Mon"]);
    var intro = L(["The Bantay Santa Luz dashboard goes to the Local Health Board. Approve or block each element.", "Bantay Santa Luz 儀表板要送到地方衛生委員會。逐一決定每個元件：發布或擋下。", "Ipapadala ang Bantay Santa Luz dashboard sa Local Health Board. Aprubahan o i-block ang bawat bahagi."]);
    ctx.host.appendChild(shell(ctx, title, intro));
    sequence(ctx, {
      items: function () { return shuffle(PUBLISH); },
      render: function (item, api) {
        append(api.box, h("div", { class: "ph-dash-card", "data-focus": "", "aria-label": L(item.kind) }, [h("p", { class: "ph-dash-kind" }, L(item.kind)), item.view()]));
        var c = choiceButtons([
          { label: "✓ " + L(["Approve", "發布", "Aprubahan"]), value: "yes" },
          { label: "✕ " + L(["Block", "擋下", "I-block"]), value: "no" }
        ], function (o, buttons, btn) {
          var right = item.ok ? "yes" : "no";
          var ok = o.value === right;
          lockChoices(buttons, right, btn);
          api.answer(ok ? 1 : 0, ok ? "good" : "bad", L(item.why), ok ? goodWord() : badWord());
        }, "ph-approve");
        append(api.box, c);
      },
      endNote: ["Before anything leaves the office: no names or exact addresses, suppress small cells (1–4), no case-level downloads, honest axes, and a source line.",
        "任何資料離開辦公室前：不放姓名或確切地址、小格遮蔽（1–4）、不提供個案層級下載、座標軸誠實、註明資料來源。",
        "Bago lumabas ng opisina: walang pangalan o eksaktong address, i-suppress ang small cells (1–4), walang case-level download, tapat na axis, at may source line."]
    });
  };

  /* ========================================================= quiz (any) */
  var QUIZ_BANKS = {
    ch02: [
      { q: ["Which of these must never leave the office?", "下列何者絕不能離開辦公室？", "Alin dito ang hindi dapat lumabas ng opisina?"],
        o: [{ t: ["A PhilHealth number", "PhilHealth 號碼", "PhilHealth number"], ok: true, e: ["An ID number points to exactly one person: a direct identifier.", "識別號碼直接指向特定一人：直接識別資訊。", "Iisang tao lang ang tinutukoy ng ID number: direct identifier."] },
          { t: ["The name of the barangay", "barangay 名稱", "Pangalan ng barangay"], e: ["A barangay alone does not identify a person (but watch small counts).", "單獨的 barangay 不會識別個人（但要注意小數字）。", "Hindi nakikilala ang tao sa barangay lang (pero bantayan ang maliliit na bilang)."] },
          { t: ["The morbidity week", "流行病學週", "Morbidity week"], e: ["A week number on its own is not personal information.", "單獨的週別不是個人資料。", "Hindi personal information ang week number lang."] }] },
      { q: ["Maya needs Tala's help with a date error. What does she paste?", "Maya 需要 Tala 幫忙處理日期錯誤，她應該貼上什麼？", "Kailangan ni Maya ng tulong ni Tala sa date error. Ano ang ipe-paste niya?"],
        o: [{ t: ["The first 20 rows of the real line list", "真實造冊的前 20 列", "Unang 20 rows ng totoong line list"], e: ["Real rows contain names and contacts — never paste them into an AI chat.", "真實資料含姓名與聯絡方式——絕不貼進 AI 對話。", "May pangalan at contact ang totoong rows — huwag i-paste sa AI chat."] },
          { t: ["3 made-up rows with the same columns and the error message", "3 列欄位相同的虛構資料，加上錯誤訊息", "3 gawa-gawang rows na pareho ang columns, at ang error message"], ok: true, e: ["Same shape, no real people: Tala can still find the bug.", "結構相同、沒有真人：Tala 一樣找得到問題。", "Parehong hugis, walang totoong tao: makikita pa rin ni Tala ang bug."] },
          { t: ["A screenshot of the spreadsheet", "試算表的螢幕截圖", "Screenshot ng spreadsheet"], e: ["A screenshot shows the same personal data as the file.", "截圖顯示的個人資料和檔案一樣多。", "Pareho ring personal data ang makikita sa screenshot."] }] },
      { q: ["Why replace the exact birth date with an age group?", "為什麼要把確切出生日期改成年齡組？", "Bakit papalitan ng age group ang eksaktong birth date?"],
        o: [{ t: ["Age groups are easier to type", "年齡組比較好打字", "Mas madaling i-type ang age group"], e: ["Convenience is not the reason.", "方便不是重點。", "Hindi kaginhawahan ang dahilan."] },
          { t: ["Birth date + sex + barangay can single out one person", "出生日期＋性別＋barangay 可能鎖定特定一人", "Ang birth date + kasarian + barangay ay puwedeng tumukoy sa iisang tao"], ok: true, e: ["Indirect identifiers combine. Keep only the detail the analysis needs.", "間接識別資訊會互相組合。只保留分析需要的細節。", "Nagsasama-sama ang indirect identifiers. Ang kailangan lang ng analysis ang itira."] }] }
    ],
    ch04: [
      { q: ["What is the denominator of an attack rate?", "侵襲率的分母是什麼？", "Ano ang denominator ng attack rate?"],
        o: [{ t: ["The number of cases", "病例數", "Bilang ng kaso"], e: ["Cases are the numerator.", "病例數是分子。", "Ang kaso ang numerator."] },
          { t: ["The population at risk", "可能發病的族群（風險族群）人數", "Ang population at risk"], ok: true, e: ["Everyone who could have become a case, e.g. the residents of the barangay.", "所有可能成為病例的人，例如該 barangay 的居民。", "Lahat ng puwedeng maging kaso, hal. mga residente ng barangay."] },
          { t: ["The number of deaths", "死亡數", "Bilang ng namatay"], e: ["Deaths over cases is the case fatality rate.", "死亡數除以病例數是致死率。", "Ang namatay ÷ kaso ay case fatality rate."] }] },
      { q: ["An epi curve with one sharp peak that rises and falls within one incubation period suggests…", "流行曲線只有一個尖峰，且在一個潛伏期內上升又下降，代表……", "Ang epi curve na may isang matulis na peak na tumaas at bumaba sa loob ng isang incubation period ay nagpapahiwatig ng…"],
        o: [{ t: ["A point source", "單一時點共同感染源（所有人同時暴露）", "Point source"], ok: true, e: ["Everyone was exposed at about the same time, like one shared meal. (Santa Luz's leptospirosis curve stayed high for two weeks: a continuing source.)", "大家大約在同一時間暴露，例如同一餐。（Santa Luz 的鉤端螺旋體病曲線維持高峰兩週：持續性共同感染源。）", "Halos sabay-sabay na-expose ang lahat, gaya ng iisang kainan. (Nanatiling mataas nang dalawang linggo ang leptospirosis curve ng Santa Luz: continuing source.)"] },
          { t: ["Person-to-person spread", "人傳人", "Hawaan ng tao sa tao"], e: ["Propagated spread shows successive, growing waves.", "人傳人（連鎖傳播）會出現一波比一波高的連續波峰。", "Ang propagated ay may sunud-sunod at lumalaking alon."] }] },
      { q: ["39 leptospirosis cases and 6 deaths in Barangay Ilog. The case fatality rate is…", "Barangay Ilog 有 39 例鉤端螺旋體病、6 例死亡，致死率是……", "39 kaso ng leptospirosis at 6 namatay sa Barangay Ilog. Ang case fatality rate ay…"],
        o: [{ t: ["15.4%", "15.4%", "15.4%"], ok: true, e: ["6 ÷ 39 = 0.154.", "6 ÷ 39 = 0.154。", "6 ÷ 39 = 0.154."] },
          { t: ["0.04%", "0.04%", "0.04%"], e: ["That divides by Ilog's 13,411 residents — a mortality rate.", "那是除以 Ilog 的 13,411 位居民——死亡率。", "Hinati iyan sa 13,411 residente ng Ilog — mortality rate iyon."] },
          { t: ["650%", "650%", "650%"], e: ["39 ÷ 6 turns the fraction upside down.", "39 ÷ 6 把分數倒過來了。", "Baligtad: 39 ÷ 6."] }] }
    ],
    ch06: [
      { q: ["What do the three numbers of 7-1-7 stand for?", "7-1-7 的三個數字代表什麼？", "Ano ang ibig sabihin ng tatlong numero ng 7-1-7?"],
        o: [{ t: ["Detect ≤7 days, notify ≤1 day, complete early response ≤7 days", "≤7 天內偵測、≤1 天內通報、≤7 天內完成早期應變", "Detect ≤7 araw, notify ≤1 araw, tapusin ang early response ≤7 araw"], ok: true, e: ["Detection is counted from emergence, notification from detection, response from notification.", "偵測從事件出現起算、通報從偵測起算、應變從通報起算。", "Ang detection ay mula emergence, ang notification mula detection, ang response mula notification."] },
          { t: ["7 cases, 1 death, 7 barangays", "7 例、1 死、7 個 barangay", "7 kaso, 1 namatay, 7 barangay"], e: ["7-1-7 is a timeliness target, not a case count.", "7-1-7 是時效目標，不是病例數。", "Timeliness target ang 7-1-7, hindi bilang ng kaso."] }] },
      { q: ["The alert threshold in this book is…", "本書使用的警戒閾值是……", "Ang alert threshold sa librong ito ay…"],
        o: [{ t: ["The mean of the same week in past years + 2 standard deviations", "過去數年同一週的平均值 + 2 個標準差", "Mean ng parehong linggo sa mga nakaraang taon + 2 standard deviations"], ok: true, e: ["Weeks far above the usual range for that time of year raise a signal.", "遠高於該時節平常範圍的週數會發出訊號。", "Nagbibigay ng signal ang linggong lampas na lampas sa karaniwan para sa panahong iyon."] },
          { t: ["Any week with more cases than last week", "任何比上週多的一週", "Anumang linggong mas marami ang kaso kaysa noong nakaraang linggo"], e: ["Counts go up and down by chance; that would alarm every other week.", "病例數本來就會隨機起伏，這樣幾乎每隔一週就要警報。", "Tumataas-bumababa ang bilang nang nagkataon; halos linggu-linggo kang mag-a-alarm."] }] }
    ]
  };

  /** Split DOM content into [before, after] at the first " — " (em dash). */
  function splitAtDash(nodes) {
    var before = D.createDocumentFragment(), after = D.createDocumentFragment(), found = false;
    nodes.forEach(function (n) {
      if (found) { after.appendChild(n.cloneNode(true)); return; }
      if (n.nodeType === 3) {
        var t = n.nodeValue, i = t.search(/\s[—–]\s|\s--\s/);
        if (i >= 0) {
          found = true;
          var m = /\s([—–]|--)\s/.exec(t.slice(i));
          before.appendChild(D.createTextNode(t.slice(0, i)));
          after.appendChild(D.createTextNode(t.slice(i + m[0].length)));
          return;
        }
      }
      before.appendChild(n.cloneNode(true));
    });
    return [before, found ? after : null];
  }
  /** Inline content of a list item, without nested lists (unwraps <p>). */
  function inlineNodes(li) {
    var out = [];
    Array.prototype.forEach.call(li.childNodes, function (n) {
      if (n.nodeType === 1 && /^(UL|OL)$/.test(n.tagName)) return;
      if (n.nodeType === 1 && n.tagName === "P") { Array.prototype.forEach.call(n.childNodes, function (c) { out.push(c); }); out.push(D.createTextNode(" ")); return; }
      out.push(n);
    });
    while (out.length && out[out.length - 1].nodeType === 3 && !out[out.length - 1].nodeValue.trim()) out.pop();
    while (out.length && out[0].nodeType === 3 && !out[0].nodeValue.trim()) out.shift();
    return out;
  }
  /** Parse the fallback list into [{q: Node, o: [{t: Node, ok, e: Node}]}]. */
  function parseQuiz(host) {
    var list = null;
    Array.prototype.some.call(host.querySelectorAll("ol, ul"), function (l) {
      if (l.closest(".ph-w")) return false;
      list = l; return true;
    });
    if (!list) return null;
    var qs = [];
    Array.prototype.forEach.call(list.children, function (li) {
      if (li.tagName !== "LI") return;
      var sub = null;
      Array.prototype.forEach.call(li.children, function (c) { if (!sub && /^(UL|OL)$/.test(c.tagName)) sub = c; });
      if (!sub) return;
      var opts = [];
      Array.prototype.forEach.call(sub.children, function (oli) {
        if (oli.tagName !== "LI") return;
        var nodes = inlineNodes(oli).map(function (n) { return n.cloneNode(true); });
        var ok = false;
        if (nodes.length && nodes[0].nodeType === 3) {
          var t = nodes[0].nodeValue.replace(/^\s+/, "");
          var m = /^(✓|✔|☑)️?\s*/.exec(t);
          if (m) { ok = true; nodes[0] = D.createTextNode(t.slice(m[0].length)); }
        }
        var parts = splitAtDash(nodes);
        opts.push({ t: parts[0], ok: ok, e: parts[1] });
      });
      if (!opts.length) return;
      var qf = D.createDocumentFragment();
      inlineNodes(li).forEach(function (n) { qf.appendChild(n.cloneNode(true)); });
      qs.push({ q: qf, o: opts });
    });
    if (!qs.length) return null;
    var titleNode = null;
    Array.prototype.some.call(host.children, function (c) {
      if (c === list || c.contains(list)) return true;
      if (/^(P|H\d|DIV)$/.test(c.tagName) && c.textContent.trim() && !c.classList.contains("ph-w")) { titleNode = c; return true; }
      return false;
    });
    return { title: titleNode ? titleNode.textContent.trim() : null, qs: qs };
  }
  function bankToQuiz(bank) {
    return bank.map(function (b) {
      return {
        q: D.createTextNode(L(b.q)),
        o: b.o.map(function (o) { return { t: D.createTextNode(L(o.t)), ok: !!o.ok, e: o.e ? D.createTextNode(L(o.e)) : null }; })
      };
    });
  }

  WIDGETS.quiz = function (ctx) {
    var parsed = parseQuiz(ctx.host);
    var qs = parsed && parsed.qs;
    var bankName = ctx.option("ph-quiz-");
    if (!qs && bankName && QUIZ_BANKS[bankName]) qs = bankToQuiz(QUIZ_BANKS[bankName]);
    if (!qs || !qs.length) return false; // keep the fallback visible
    var title = (parsed && parsed.title) || L(["Quick check", "小測驗", "Mabilisang check"]);
    ctx.host.appendChild(shell(ctx, title, null));
    sequence(ctx, {
      items: function () { return qs.map(function (q) { return { q: q.q, o: shuffle(q.o) }; }); },
      render: function (item, api) {
        append(api.box, h("p", { class: "ph-q", "data-focus": "" }, item.q.cloneNode(true)));
        var hasRight = item.o.some(function (o) { return o.ok; });
        var wrap = h("div", { class: "ph-choices ph-stack", role: "group" });
        var buttons = item.o.map(function (o, k) {
          return h("button", { type: "button", class: "ph-choice", "data-value": String(k),
            onclick: function () {
              var ok = o.ok || !hasRight;
              buttons.forEach(function (b, j) { b.disabled = true; if (item.o[j].ok) b.classList.add("is-right"); });
              if (!ok) this.classList.add("is-wrong");
              this.setAttribute("aria-pressed", "true");
              var content = [];
              if (o.e) content.push(h("span", null, o.e.cloneNode(true)));
              if (!ok) {
                var right = item.o.filter(function (x) { return x.ok; })[0];
                content.push(h("span", { class: "ph-block" }, [U("rightAnswer") + ": ", right.t.cloneNode(true), right.e ? [" — ", right.e.cloneNode(true)] : null]));
              }
              api.answer(ok ? 1 : 0, ok ? "good" : "bad", content.length ? content : "", ok ? goodWord() : badWord());
            }
          }, [h("span", { class: "ph-opt-key", "aria-hidden": "true" }, String.fromCharCode(65 + k)), h("span", null, o.t.cloneNode(true))]);
        });
        append(wrap, buttons);
        append(api.box, wrap);
      }
    });
  };

  /* ===================================================== spot-pii (ch 02) */
  var PII_WHY = {
    direct: ["Direct identifier — remove it before the data leave the office.", "直接識別資訊——資料離開辦公室前要刪除。", "Direct identifier — tanggalin bago lumabas ng opisina ang datos."],
    gov: ["Government-issued ID number: it points to exactly one person. Remove.", "政府核發的識別號碼：直接指向特定一人，要刪除。", "Government-issued ID number: iisang tao lang ang tinutukoy nito. Tanggalin."],
    quasi: ["Indirect identifier — combined with sex and barangay it can single out one person. Keep only age or age group.", "間接識別資訊——和性別、barangay 組合起來可能鎖定特定一人。只保留年齡或年齡組。", "Indirect identifier — kapag isinama sa kasarian at barangay, puwedeng matukoy ang isang tao. Edad o age group lang ang itira."],
    free: ["Free text often hides names, relatives and workplaces. Remove it or read and clean every entry.", "自由文字常藏著姓名、親屬和工作地點。刪除，或逐筆閱讀清理。", "Madalas may nakatagong pangalan, kamag-anak at trabaho sa free text. Tanggalin, o basahin at linisin isa-isa."],
    keep: ["Fine to keep in a de-identified file (still watch small counts when you publish).", "可保留在去識別化的檔案中（發布時仍要注意小數字）。", "Puwedeng itira sa de-identified na file (bantayan pa rin ang maliliit na bilang sa pag-publish)."],
    pseudo: ["A pseudonymous code: fine, as long as the key linking it to the name stays in the office.", "假名代碼：可以保留，只要對照姓名的對照表留在辦公室內。", "Pseudonymous code: puwede, basta nasa opisina lang ang susi na nagdudugtong dito sa pangalan."]
  };
  var PII_COLUMNS = [
    { col: "case_id", v: ["SLC-0142", "SLC-0143"], pii: false, why: "pseudo" },
    { col: "full_name", v: ["Rodel Manalo", "Liza Santos"], pii: true, why: "direct" },
    { col: "contact_no", v: ["0900 555 0142", "0900 555 0199"], pii: true, why: "direct" },
    { col: "address", v: ["12 Mabini St., Purok 4", "Purok 1, near chapel"], pii: true, why: "direct" },
    { col: "barangay", v: ["Ilog", "Sapa"], pii: false, why: "keep" },
    { col: "birth_date", v: ["1974-03-09", "1990-11-21"], pii: true, why: "quasi" },
    { col: "age_group", v: ["50–59", "30–39"], pii: false, why: "keep" },
    { col: "sex", v: ["M", "F"], pii: false, why: "keep" },
    { col: "philhealth_no", v: ["12-345678901-2", "02-555123456-7"], pii: true, why: "gov" },
    { col: "onset_date", v: ["2026-07-26", "2026-07-28"], pii: false, why: "keep" },
    { col: "remarks", v: ["Kapatid ni Kap. Ruiz", "Tindera sa palengke"], pii: true, why: "free" },
    { col: "disease", v: ["Leptospirosis", "Leptospirosis"], pii: false, why: "keep" }
  ];
  var PII_MESSAGE = [
    { t: ["Tala, help me with this row: ", "Tala，幫我看這一列：", "Tala, tulungan mo ako sa row na ito: "] },
    { t: "Rodel Manalo", pii: true, why: "direct" },
    { t: [", 52 y/o, ", "，52 歲，", ", 52 taong gulang, "], why: "keep" },
    { t: "0900 555 0142", pii: true, why: "direct" },
    { t: [", lives at ", "，住在 ", ", nakatira sa "] },
    { t: "12 Mabini St., Purok 4", pii: true, why: "direct" },
    { t: [", Brgy. Ilog", "，Brgy. Ilog", ", Brgy. Ilog"], why: "keep" },
    { t: [", PhilHealth ", "，PhilHealth ", ", PhilHealth "] },
    { t: "12-345678901-2", pii: true, why: "gov" },
    { t: [". Onset ", "。發病日 ", ". Onset "] },
    { t: "'07/26/2026'", why: "keep" },
    { t: [" fails in pd.to_datetime — why?", " 在 pd.to_datetime 會出錯，為什麼？", " — pumapalya sa pd.to_datetime, bakit?"] }
  ];

  WIDGETS["spot-pii"] = function (ctx) {
    var title = L(["Spot the PII", "找出個人資料", "Hanapin ang PII"]);
    ctx.host.appendChild(shell(ctx, title, null));
    var round = 0, total = 0, totalMax = 0;
    var rounds = [tableRound, messageRound];
    function begin() { round = 0; total = 0; totalMax = 0; ctx.setScore(0); rounds[0](); }
    function after(score, max) {
      total += score; totalMax += max;
      ctx.setScore(total, totalMax);
      clear(ctx.controls);
      var last = round === rounds.length - 1;
      var b = ctx.button(last ? "★ " + U("seeScore") : U("nextRound") + " →", function () {
        if (last) endScreen(ctx, total, totalMax, begin, ["Remove direct identifiers, generalise indirect ones, clean free text — and never paste identifiable rows into an AI chat.", "刪除直接識別資訊、概化間接識別資訊、清理自由文字——也絕不把可識別個人的資料貼進 AI 對話。", "Tanggalin ang direct identifiers, gawing pangkalahatan ang indirect, linisin ang free text — at huwag mag-paste ng nakikilalang rows sa AI chat."]);
        else { round++; rounds[round](); }
      }, "ph-primary");
      append(ctx.controls, b);
      focusQuiet(b);
    }
    function grade(items, buttons) {
      var score = 0, misses = [];
      items.forEach(function (it, i) {
        var picked = buttons[i].getAttribute("aria-pressed") === "true";
        var right = picked === !!it.pii;
        if (right) score++;
        buttons[i].classList.add(right ? "is-right" : "is-wrong");
        buttons[i].classList.add(it.pii ? "is-pii" : "is-safe");
        buttons[i].disabled = true;
        if (!right) misses.push(h("li", null, [h("code", null, it.label), " — ", (it.pii ? L(["must not leave: ", "不可外流：", "bawal ilabas: "]) : L(["safe: ", "可保留：", "ligtas: "])) + L(PII_WHY[it.why])]));
      });
      var ok = score === items.length;
      ctx.say(ok ? "good" : "bad",
        ok ? L(["Every identifier caught. Doc Mon nods.", "所有識別資訊都抓到了，Doc Mon 點頭稱許。", "Nahuli lahat ng identifier. Tumango si Doc Mon."]) : [h("span", null, fmt(L(["{s} of {n} right. Look again:", "答對 {s} / {n}。再看一次：", "{s} sa {n} ang tama. Tingnan ulit:"]), { s: score, n: items.length })), h("ul", { class: "ph-misses" }, misses)],
        ok ? goodWord() : null);
      if (ok) ctx.celebrate(true);
      return score;
    }
    function toggle() {
      var on = this.getAttribute("aria-pressed") === "true";
      this.setAttribute("aria-pressed", on ? "false" : "true");
    }
    function tableRound() {
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      append(ctx.body, [
        h("p", { class: "ph-progress" }, U("roundOf", { i: 1, n: 2 })),
        h("p", { class: "ph-task", tabindex: "-1", "data-focus": "" }, L(["Jun's raw export. Tap every column that must NOT leave the CESU as it is (or go into an AI chat). Then press Check.", "這是 Jun 匯出的原始資料。點選所有「不可原樣離開 CESU（或貼進 AI 對話）」的欄位，再按「檢查」。", "Raw export ni Jun. I-tap ang bawat column na HINDI dapat lumabas ng CESU nang ganito (o ipasok sa AI chat). Tapos pindutin ang I-check."]))
      ]);
      var items = PII_COLUMNS.map(function (c) { return { label: c.col, pii: c.pii, why: c.why, v: c.v }; });
      var grid = h("div", { class: "ph-pii-grid", role: "group", "aria-label": L(["Columns", "欄位", "Mga column"]) });
      var buttons = items.map(function (it) {
        return h("button", { type: "button", class: "ph-pii-col", "aria-pressed": "false", onclick: toggle }, [
          h("span", { class: "ph-pii-name" }, it.label),
          h("span", { class: "ph-pii-val" }, it.v[0]),
          h("span", { class: "ph-pii-val" }, it.v[1])
        ]);
      });
      append(grid, buttons);
      append(ctx.body, h("div", { class: "ph-scroll-x" }, grid));
      var chk = ctx.button("✓ " + U("check"), function () { chk.disabled = true; after(grade(items, buttons), items.length); }, "ph-primary");
      append(ctx.controls, chk);
    }
    function messageRound() {
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      var task = h("p", { class: "ph-task", tabindex: "-1" }, L(["Maya's draft message to Tala. Tap every piece that identifies a person. Then press Check.", "這是 Maya 準備傳給 Tala 的訊息。點選所有能識別個人的片段，再按「檢查」。", "Draft na mensahe ni Maya kay Tala. I-tap ang bawat bahaging tumutukoy sa isang tao. Tapos pindutin ang I-check."]));
      append(ctx.body, [h("p", { class: "ph-progress" }, U("roundOf", { i: 2, n: 2 })), task]);
      var bubble = h("p", { class: "ph-bubble" });
      var items = [], buttons = [];
      PII_MESSAGE.forEach(function (m) {
        var text = L(m.t);
        if (!m.why) { append(bubble, text); return; }
        var b = h("button", { type: "button", class: "ph-token", "aria-pressed": "false", onclick: toggle }, text);
        items.push({ label: text.replace(/^[,，。.\s]+|[,，。.\s]+$/g, ""), pii: !!m.pii, why: m.why });
        buttons.push(b);
        bubble.appendChild(b);
      });
      append(ctx.body, bubble);
      var chk = ctx.button("✓ " + U("check"), function () {
        chk.disabled = true;
        var sc = grade(items, buttons);
        var safe = h("p", { class: "ph-bubble ph-bubble-safe" }, L(["Safer: \"Made-up row: case_id=C001, age=52, barangay=Ilog, onset='07/26/2026'. Why does pd.to_datetime fail on this onset date?\"", "較安全的寫法：「虛構資料：case_id=C001, age=52, barangay=Ilog, onset='07/26/2026'。為什麼 pd.to_datetime 處理這個發病日會出錯？」", "Mas ligtas: \"Gawa-gawang row: case_id=C001, age=52, barangay=Ilog, onset='07/26/2026'. Bakit pumapalya ang pd.to_datetime sa onset date na ito?\""]));
        append(ctx.body, safe);
        after(sc, items.length);
      }, "ph-primary");
      append(ctx.controls, chk);
      focusQuiet(task);
    }
    begin();
  };

  /* =================================================== date-fixer (ch 03) */
  var DATE_BINS = [
    { id: "a", label: "2026-07-23" },
    { id: "b", label: "2026-07-24" },
    { id: "c", label: "2026-08-07" },
    { id: "x", label: ["? Ask Jun", "？問 Jun", "? Tanungin si Jun"] }
  ];
  var DATE_CARDS = [
    { t: "2026-07-23", bin: "a", why: ["Already ISO 8601 (year-month-day). The format to aim for.", "已經是 ISO 8601（年-月-日），就是我們要的格式。", "ISO 8601 na (taon-buwan-araw). Ito ang target na format."] },
    { t: "23/07/2026", bin: "a", why: ["Day first: there is no month 23, so this must be 23 July.", "日在前：沒有 23 月，所以一定是 7 月 23 日。", "Araw muna: walang buwang 23, kaya 23 Hulyo ito."] },
    { t: "07/23/2026", bin: "a", why: ["Month first (US style): 23 can only be the day.", "月在前（美式）：23 只可能是日。", "Buwan muna (US style): araw lang ang puwedeng 23."] },
    { t: "46226", bin: "a", why: ["An Excel serial number: days since 30 Dec 1899. 46226 = 2026-07-23. Convert with `pd.to_datetime(x, unit='D', origin='1899-12-30')`.", "Excel 序號：自 1899-12-30 起的天數。46226 = 2026-07-23。可用 `pd.to_datetime(x, unit='D', origin='1899-12-30')` 轉換。", "Excel serial number: bilang ng araw mula 30 Dis 1899. 46226 = 2026-07-23. I-convert gamit ang `pd.to_datetime(x, unit='D', origin='1899-12-30')`."] },
    { t: "July 24, 2026", bin: "b", why: ["Month written in words: unambiguous.", "月份用文字寫出：不會混淆。", "Nakasulat ang buwan: walang kalituhan."] },
    { t: "24-Hul-2026", bin: "b", why: ["'Hul' is Hulyo (July) in Filipino — pandas will not know it; map the Filipino month names first.", "'Hul' 是菲律賓語的 Hulyo（7 月）——pandas 不認得，要先把菲律賓語月份對應好。", "Ang 'Hul' ay Hulyo — hindi ito kilala ng pandas; i-map muna ang mga buwan sa Filipino."] },
    { t: "7 Aug 2026", bin: "c", why: ["Day, then month in words: 7 August.", "日在前、月份用文字：8 月 7 日。", "Araw, tapos buwan na nakasulat: 7 Agosto."] },
    { t: "Agosto 7, 2026", bin: "c", why: ["Agosto = August. Another Filipino month name to map.", "Agosto = 8 月，又一個需要對應的菲律賓語月份。", "Agosto = August. Isa pang buwan sa Filipino na kailangang i-map."] },
    { t: "2026/08/07", bin: "c", why: ["Year first with slashes: by convention year/month/day.", "以斜線分隔、年在前：慣例為年/月/日。", "Taon muna na may slash: karaniwang taon/buwan/araw."] },
    { t: "08/07/2026", bin: "x", why: ["8 July or 7 August? Both are valid. Don't let the computer guess (a silent mis-parse): check which system the row came from, or ask Jun.", "7 月 8 日還是 8 月 7 日？兩者都合理。別讓電腦猜（會悄悄解析錯）：查清楚這列來自哪個系統，或問 Jun。", "8 Hulyo o 7 Agosto? Parehong puwede. Huwag hayaang manghula ang computer (tahimik na mali): alamin kung saang sistema galing ang row, o tanungin si Jun."] }
  ];

  WIDGETS["date-fixer"] = function (ctx) {
    var title = L(["Date fixer", "日期修理站", "Date fixer"]);
    var intro = L(["Jun's export mixes date formats. Tap a messy date, then tap the ISO date it really means.", "Jun 匯出的資料混了好幾種日期格式。先點一個雜亂的日期，再點它真正代表的 ISO 日期。", "Halo-halo ang format ng petsa sa export ni Jun. I-tap ang magulong petsa, tapos i-tap ang tunay nitong ISO date."]);
    ctx.host.appendChild(shell(ctx, title, intro));
    var selected = null, score = 0, placed = 0, tried = {};
    function start() {
      selected = null; score = 0; placed = 0; tried = {};
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      ctx.setScore(0, DATE_CARDS.length);
      var tray = h("div", { class: "ph-tray", role: "group", "aria-label": L(["Messy dates", "雜亂的日期", "Magulong petsa"]) });
      var bins = h("div", { class: "ph-bins" });
      var cards = shuffle(DATE_CARDS).map(function (c) {
        var b = h("button", { type: "button", class: "ph-card", "aria-pressed": "false", onclick: function () { select(b); } }, c.t);
        b.card = c;
        return b;
      });
      append(tray, cards);
      DATE_BINS.forEach(function (bin) {
        var list = h("div", { class: "ph-bin-list" });
        var btn = h("button", { type: "button", class: "ph-bin-target", onclick: function () { place(bin, list, btn); } }, [h("span", { class: "ph-bin-label" }, L(bin.label))]);
        append(bins, h("div", { class: "ph-bin" + (bin.id === "x" ? " ph-bin-ask" : "") }, [btn, list]));
      });
      append(ctx.body, [tray, h("p", { class: "ph-hint" }, U("tapFirst")), bins]);
      ctx.tray = tray;
    }
    function select(b) {
      if (b.disabled) return;
      Array.prototype.forEach.call(ctx.tray.children, function (x) { x.setAttribute("aria-pressed", "false"); });
      selected = b;
      b.setAttribute("aria-pressed", "true");
      ctx.announce(b.textContent + " — " + U("selected"));
    }
    function place(bin, list, target) {
      if (!selected) { ctx.say("info", U("tapFirst")); return; }
      var card = selected.card, b = selected;
      var key = card.t;
      if (card.bin === bin.id) {
        if (!tried[key]) score++;
        placed++;
        b.parentNode.removeChild(b);
        append(list, h("span", { class: "ph-chip is-right" }, card.t));
        selected = null;
        ctx.setScore(score, DATE_CARDS.length);
        ctx.say("good", L(card.why), goodWord());
        var next = ctx.tray.querySelector(".ph-card");
        if (next) focusQuiet(next);
        if (placed === DATE_CARDS.length) finish();
      } else {
        tried[key] = true;
        b.classList.remove("ph-shake"); void b.offsetWidth; b.classList.add("ph-shake");
        target.classList.add("is-wrong");
        ctx.later(function () { target.classList.remove("is-wrong"); }, 700);
        ctx.say("bad", fmt(L(["'{d}' is not {b}. Read the parts: which can be the day, which the month?", "「{d}」不是 {b}。拆開看：哪一段可能是日、哪一段是月？", "Hindi {b} ang '{d}'. Hatiin: alin ang puwedeng araw, alin ang buwan?"]), { d: card.t, b: L(bin.label) }), badWord());
        focusQuiet(b);
      }
    }
    function finish() {
      ctx.celebrate(score === DATE_CARDS.length);
      clear(ctx.controls);
      var b = ctx.button("★ " + U("seeScore"), function () {
        endScreen(ctx, score, DATE_CARDS.length, start, ["In pandas, parse each known format explicitly (`format=`), map Filipino month names, convert Excel serials, and flag ambiguous rows instead of guessing.",
          "在 pandas 中，對每種已知格式明確指定 `format=`、對應菲律賓語月份、轉換 Excel 序號，並標記模稜兩可的資料而不是猜。",
          "Sa pandas, i-parse nang tahasan ang bawat kilalang format (`format=`), i-map ang mga buwan sa Filipino, i-convert ang Excel serial, at i-flag ang malabong rows imbes na manghula."]);
      }, "ph-primary");
      append(ctx.controls, b);
      focusQuiet(b);
    }
    start();
  };

  /* ============================================= epicurve-builder (ch 04) */
  var MONTHS = [
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    null,
    ["Ene", "Peb", "Mar", "Abr", "May", "Hun", "Hul", "Ago", "Set", "Okt", "Nob", "Dis"]
  ];
  /** Short date label for day offset k from a UTC start date. */
  function dayLabel(start, k, withMonth) {
    var d = new Date(Date.UTC(start[0], start[1] - 1, start[2] + k));
    var m = d.getUTCMonth(), day = d.getUTCDate();
    if (LI === 1) return withMonth ? (m + 1) + "/" + day : String(day);
    return withMonth ? day + " " + MONTHS[LI][m] : String(day);
  }
  var SHAPES = {
    point: ["Point source (one short, shared exposure)", "單一時點共同感染源（一次短暫的共同暴露）", "Point source (iisang maikling exposure)"],
    continuing: ["Continuing common source", "持續性共同感染源", "Continuing common source"],
    propagated: ["Propagated (spreads from case to case)", "連鎖傳播（由病例再傳給他人）", "Propagated (kumakalat mula kaso sa kaso)"]
  };
  var CURVES = [
    {
      id: "lepto", unit: "day", start: [2026, 7, 22],
      title: ["Leptospirosis in Santa Luz: one in four of the line list's cases", "Santa Luz 的鉤端螺旋體病：造冊病例每四例取一例", "Leptospirosis sa Santa Luz: isa sa bawat apat na kaso ng line list"],
      context: ["Typhoon Amihan flooded the riverside on 18–20 July; people waded in the flood and the clean-up until about 2 August. Incubation of leptospirosis: usually 7–10 days, range 2–30 (WHO).", "颱風 Amihan 於 7/18–20 淹沒河岸地區；居民在洪水與清理期間涉水，一直到 8/2 左右。鉤端螺旋體病潛伏期：通常 7–10 天，範圍 2–30 天（WHO）。", "Binaha ng Bagyong Amihan ang tabing-ilog noong 18–20 Hulyo; lumusong ang mga tao sa baha at sa paglilinis hanggang mga 2 Agosto. Incubation ng leptospirosis: karaniwang 7–10 araw, mula 2 hanggang 30 (WHO)."],
      pre: [0, 1, 1, 3, 3, 4, 3, 2, 3, 4, 3, 4, 2, 3, 2, 2, 1, 2, 2, 1], mine: [2, 5, 8, 10, 12, 15], answer: "continuing",
      why: ["One wave that rises, stays high for about two weeks — as long as people kept wading in the flood and the clean-up — and then fades: a continuing common source, as in chapter 04.", "只有一波：上升後維持高峰約兩週——正是民眾在洪水與清理期間持續涉水的時間——然後消退：持續性共同感染源，和第 04 章一致。", "Isang alon na tumaas, nanatiling mataas nang mga dalawang linggo — habang lumulusong pa ang mga tao sa baha at sa paglilinis — saka humupa: continuing common source, gaya sa kabanata 04."]
    },
    {
      id: "water", unit: "day", start: [2026, 7, 22], marker: 2,
      markerLabel: ["shared lunch", "共同午餐", "sabay-sabay na tanghalian"],
      title: ["Practice scenario: diarrhoea after one meal, evacuation centre", "練習情境：避難中心一餐之後的腹瀉", "Practice scenario: pagtatae pagkatapos ng isang kainan, evacuation center"],
      context: ["Evacuees at Santa Luz Central School all ate the same packed lunch on 24 July. In this made-up scenario the incubation is about 1–2 days.", "Santa Luz 中央小學的撤離民眾在 7/24 都吃了同一批便當。在這個虛構情境中，潛伏期約 1–2 天。", "Iisang packed lunch ang kinain ng lahat ng evacuee sa Santa Luz Central School noong 24 Hulyo. Sa gawa-gawang scenario na ito, mga 1–2 araw ang incubation."],
      pre: [0, 0, 0, 0, 5, 6, 2, 1, 0, 0, 0, 0], mine: [3, 4, 4, 5, 5, 6], answer: "point",
      why: ["One sharp peak that rises and falls within about one incubation period after the lunch: everyone was exposed at the same moment — a point source.", "午餐後約一個潛伏期內出現單一尖峰，隨即下降：大家在同一時刻暴露——單一時點共同感染源。", "Isang matulis na peak na tumaas at bumaba sa loob ng halos isang incubation period matapos ang tanghalian: sabay-sabay na na-expose ang lahat — point source."]
    },
    {
      id: "dengue", unit: "week", start: 27,
      title: ["Practice scenario: dengue in a made-up village, by morbidity week", "練習情境：虛構村落的登革熱，依流行病學週", "Practice scenario: dengue sa isang gawa-gawang nayon, ayon sa morbidity week"],
      context: ["Aedes mosquitoes carry dengue from person to person. One cycle (human → mosquito → human) takes about 2–3 weeks.", "登革熱靠斑蚊在人與人之間傳播。一個循環（人 → 蚊 → 人）約需 2–3 週。", "Dinadala ng lamok na Aedes ang dengue mula tao sa tao. Mga 2–3 linggo ang isang ikot (tao → lamok → tao)."],
      pre: [1, 0, 0, 1, 1, 0, 3, 2, 1, 6, 7, 4, 2, 1], mine: [3, 6, 7, 9, 10, 10], answer: "propagated",
      why: ["Successive waves about one cycle apart, each taller than the last: every generation of cases infects the next.", "連續數波、每波相隔約一個傳播週期，且一波比一波高：每一代病例再感染下一代。", "Sunud-sunod na alon na mga isang ikot ang pagitan, palaki nang palaki: bawat henerasyon ng kaso ay nakahahawa sa susunod."]
    }
  ];

  WIDGETS["epicurve-builder"] = function (ctx) {
    var title = L(["Build the epi curve", "動手畫流行曲線", "Buuin ang epi curve"]);
    ctx.host.appendChild(shell(ctx, title, null));
    var only = ctx.option("ph-curve-");
    var list = CURVES.filter(function (c) { return !only || c.id === only; });
    if (!list.length) list = CURVES;
    var ci = 0, total = 0, totalMax = 0;
    function begin() { ci = 0; total = 0; totalMax = list.length * 9; ctx.setScore(0, totalMax); play(list[0]); }
    function label(c, k, full) {
      return c.unit === "week" ? "W" + (c.start + k) : dayLabel(c.start, k, full);
    }
    function play(c) {
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      var counts = c.pre.slice();
      var queue = shuffle(c.mine);
      var firstTry = true, scenarioScore = 0;
      var maxY = Math.max.apply(null, c.pre.map(function (v, i) { return v + c.mine.filter(function (m) { return m === i; }).length; })) + 1;
      var cardEl = h("p", { class: "ph-case-card", "aria-live": "off" });
      var chart = h("div", { class: "ph-curve", role: "group", style: "--rows:" + maxY, "aria-label": L(["Epi curve: choose the column for the case", "流行曲線：為這位病例選擇欄位", "Epi curve: piliin ang column para sa kaso"]) });
      var cols = counts.map(function (n, k) {
        var stack = h("span", { class: "ph-pile", "aria-hidden": "true" });
        for (var j = 0; j < n; j++) stack.appendChild(h("i", { class: "ph-sq" }));
        var col = h("button", { type: "button", class: "ph-col" + (c.marker === k ? " ph-col-marker" : ""), onclick: function () { drop(k); } }, [
          stack,
          h("span", { class: "ph-col-label", "aria-hidden": "true" }, k === 0 || (c.unit === "day" && label(c, k) === "1") ? label(c, k, true) : label(c, k))
        ]);
        col.stack = stack;
        return col;
      });
      append(chart, cols);
      roving(chart, ".ph-col");
      function updateLabels() {
        cols.forEach(function (col, k) {
          col.setAttribute("aria-label", label(c, k, true) + ": " + counts[k] + " " + L(counts[k] === 1 ? ["case", "例", "kaso"] : ["cases", "例", "kaso"]));
        });
      }
      updateLabels();
      var head = h("div", { class: "ph-curve-head" }, [
        h("p", { class: "ph-progress" }, U("roundOf", { i: ci + 1, n: list.length })),
        h("p", { class: "ph-task", tabindex: "-1" }, [h("strong", null, L(c.title)), h("br"), L(c.context)])
      ]);
      var yLab = h("p", { class: "ph-axis-y" }, "▲ " + L(["cases (one square = one case)", "病例數（一格＝一位病例）", "kaso (isang kahon = isang kaso)"]));
      var xLab = h("p", { class: "ph-axis-x" }, c.unit === "week" ? L(["Morbidity week of onset, 2026", "發病週別（2026）", "Morbidity week ng onset, 2026"]) : L(["Date of onset, 2026", "發病日期（2026）", "Petsa ng onset, 2026"]));
      var legend = c.marker != null ? h("p", { class: "ph-hint" }, [h("span", { class: "ph-marker-key", "aria-hidden": "true" }), " " + label(c, c.marker, true) + ": " + L(c.markerLabel)]) : null;
      append(ctx.body, [head, cardEl, yLab, h("div", { class: "ph-curve-wrap" }, chart), xLab, legend]);
      function showCard() {
        if (!queue.length) { askShape(); return; }
        var k = queue[0];
        clear(cardEl);
        append(cardEl, [h("span", { class: "ph-case-tag" }, L(["Next case", "下一位病例", "Susunod na kaso"])), " SLC-" + (140 + queue.length * 7 + ci) + " · " +
          (c.unit === "week" ? L(["onset in", "發病於", "onset sa"]) + " MW" + (c.start + k) : L(["onset", "發病日", "onset"]) + " " + label(c, k, true))]);
        ctx.announce(cardEl.textContent);
      }
      function drop(k) {
        if (!queue.length) return;
        var want = queue[0];
        if (k === want) {
          queue.shift();
          counts[k]++;
          cols[k].stack.appendChild(h("i", { class: "ph-sq ph-mine" }));
          if (firstTry) scenarioScore++;
          firstTry = true;
          total = total; ctx.setScore(total + scenarioScore, totalMax);
          updateLabels();
          ctx.say("good", L(["Placed. Every case is one square; days with no cases still keep their place on the axis.", "放好了。每位病例是一個方格；沒有病例的日子在 x 軸上也要保留位置。", "Nailagay na. Isang kahon ang bawat kaso; may puwesto pa rin sa axis ang mga araw na walang kaso."]), goodWord());
          showCard();
        } else {
          firstTry = false;
          cols[k].classList.remove("ph-shake"); void cols[k].offsetWidth; cols[k].classList.add("ph-shake");
          ctx.say("bad", fmt(L(["That column is {a}; this case goes in {b}. Follow the axis labels.", "那一欄是 {a}；這位病例應放在 {b}。沿著 x 軸標籤找找看。", "{a} ang column na iyan; sa {b} dapat ang kasong ito. Sundan ang labels ng axis."]), { a: label(c, k, true), b: label(c, want, true) }), badWord());
        }
      }
      function askShape() {
        cols.forEach(function (col) { col.disabled = true; });
        clear(cardEl);
        append(cardEl, h("strong", null, L(["Curve complete! What kind of outbreak does its shape suggest?", "曲線完成！從形狀看，這是哪一種疫情？", "Kumpleto ang curve! Anong uri ng outbreak ang ipinapakita ng hugis nito?"])));
        var opts = ["point", "continuing", "propagated"].map(function (id) { return { label: L(SHAPES[id]), value: id }; });
        var ch = choiceButtons(opts, function (o, buttons, btn) {
          var ok = o.value === c.answer;
          lockChoices(buttons, c.answer, btn);
          if (ok) scenarioScore += 3;
          total += scenarioScore;
          ctx.setScore(total, totalMax);
          ctx.say(ok ? "good" : "bad", [h("span", null, ok ? "" : U("rightAnswer") + ": " + L(SHAPES[c.answer]) + ". "), h("span", null, L(c.why))], ok ? goodWord() : badWord());
          if (ok) ctx.celebrate(scenarioScore === 9);
          var last = ci === list.length - 1;
          var nb = ctx.button(last ? "★ " + U("seeScore") : U("nextRound") + " →", function () {
            if (last) endScreen(ctx, total, totalMax, begin, ["Read an epi curve by its shape: one peak (point source), a plateau (continuing source) or growing waves one incubation apart (propagated).", "從形狀判讀流行曲線：單一尖峰（單一時點共同感染源）、高原（持續性共同感染源），或相隔一個潛伏期、越來越高的波峰（連鎖傳播）。", "Basahin ang epi curve ayon sa hugis: isang peak (point source), patag (continuing source), o lumalaking alon na isang incubation ang pagitan (propagated)."]);
            else { ci++; play(list[ci]); }
          }, "ph-primary");
          clear(ctx.controls);
          append(ctx.controls, nb);
          focusQuiet(nb);
        }, "ph-stack");
        ctx.body.appendChild(ch);
        focusQuiet(ch.buttons[0]);
      }
      showCard();
    }
    begin();
  };

  /* ==================================================== two-by-two (ch 05) */
  var NAMES = ["Mang Dodong", "Kuya Ben", "Ate Lorna", "Jojo", "Rey", "Ate Joy", "Arnel", "Toto", "Bong", "Tess", "Edwin", "Nonoy", "Caloy", "Ate Weng", "Dante", "Jessie", "Lito", "Ramil", "Boyet", "Pido", "Mila", "Gener", "Ka Andoy", "Rhea"];
  function people(spec) {
    var out = [], n = 0;
    spec.forEach(function (g) { for (var i = 0; i < g[2]; i++) out.push({ name: NAMES[n++ % NAMES.length], exp: g[0], ill: g[1] }); });
    return out;
  }
  var ROUNDS_2X2 = [
    {
      id: "cohort", design: "cohort",
      title: ["Practice cohort: one Barangay Ilog clean-up crew (made-up numbers)", "練習用世代研究：Barangay Ilog 的一支清理隊（虛構數字）", "Practice cohort: isang clean-up crew ng Barangay Ilog (gawa-gawang bilang)"],
      context: ["All 24 volunteers who cleared debris after the flood were followed up. Exposure: waded without boots. Outcome: leptospirosis.", "追蹤洪水後清理雜物的全部 24 位志工。暴露：沒穿雨鞋涉水。結果：鉤端螺旋體病。", "Sinundan ang lahat ng 24 volunteer na naglinis ng kalat pagkatapos ng baha. Exposure: lumusong nang walang bota. Outcome: leptospirosis."],
      expLabel: ["Waded without boots", "沒穿雨鞋涉水", "Lumusong nang walang bota"],
      unexpLabel: ["Wore boots", "有穿雨鞋", "Naka-bota"],
      outLabel: ["Got leptospirosis", "得到鉤端螺旋體病", "Nagka-leptospirosis"], noOutLabel: ["Stayed well", "沒有發病", "Hindi nagkasakit"],
      people: people([[1, 1, 8], [1, 0, 4], [0, 1, 1], [0, 0, 11]]),
      q: ["What does this study show about wading without boots?", "關於沒穿雨鞋涉水，這項研究顯示了什麼？", "Ano ang ipinapakita ng pag-aaral tungkol sa paglusong nang walang bota?"],
      opts: [
        { v: "ok", t: ["It multiplied the risk of leptospirosis by about 8 (RR = 8.0)", "它讓得病風險增為約 8 倍（RR = 8.0）", "Mga 8 beses na tumaas ang risk ng leptospirosis (RR = 8.0)"] },
        { v: "or", t: ["It multiplied the risk by 22, because OR = 22", "因為 OR = 22，所以風險增為 22 倍", "22 beses ang risk, kasi OR = 22"] },
        { v: "no", t: ["It made no difference", "沒有差別", "Walang pinagkaiba"] }
      ],
      why: ["Risk 8/12 = 0.67 in the barefoot waders versus 1/12 = 0.08 with boots: RR = 8.0 (95% CI 1.2–55). The OR (22) is much larger because the illness was common in this crew; the OR only approximates the RR when the outcome is rare.",
        "沒穿雨鞋者風險 8/12 = 0.67，有穿雨鞋者 1/12 = 0.08：RR = 8.0（95% 信賴區間 1.2–55）。OR（22）大得多，是因為這群人發病很普遍；只有在結果罕見時，OR 才接近 RR。",
        "Risk 8/12 = 0.67 sa lumusong nang walang bota kumpara sa 1/12 = 0.08 sa naka-bota: RR = 8.0 (95% CI 1.2–55). Mas malaki ang OR (22) dahil karaniwan ang sakit sa crew na ito; lumalapit lang ang OR sa RR kapag bihira ang outcome."]
    },
    {
      id: "casecontrol", design: "cc",
      title: ["Practice case-control: a small pilot of 20 people (made-up numbers, not Maya's 360)", "練習用病例對照研究：20 人的小型試訪（虛構數字，不是 Maya 的 360 人研究）", "Practice case-control: maliit na pilot ng 20 tao (gawa-gawang bilang, hindi ang 360 ni Maya)"],
      context: ["10 leptospirosis cases and 10 neighbours without illness (controls) were asked: did you take doxycycline prophylaxis after the flood?", "訪問 10 位鉤端螺旋體病病例與 10 位沒有發病的鄰居（對照）：洪水後你有服用 doxycycline 預防性投藥嗎？", "Tinanong ang 10 kaso ng leptospirosis at 10 kapitbahay na hindi nagkasakit (controls): uminom ka ba ng doxycycline prophylaxis pagkatapos ng baha?"],
      expLabel: ["Took doxycycline", "有服用 doxycycline", "Uminom ng doxycycline"],
      unexpLabel: ["No doxycycline", "沒有服用", "Hindi uminom"],
      outLabel: ["Case", "病例", "Kaso"], noOutLabel: ["Control", "對照", "Control"],
      people: people([[1, 1, 2], [0, 1, 8], [1, 0, 7], [0, 0, 3]]),
      q: ["What can Maya conclude?", "Maya 可以得出什麼結論？", "Ano ang puwedeng ikonklusyon ni Maya?"],
      opts: [
        { v: "ok", t: ["Prophylaxis was protective: OR ≈ 0.11", "預防性投藥有保護效果：OR ≈ 0.11", "Protective ang prophylaxis: OR ≈ 0.11"] },
        { v: "rr", t: ["The risk ratio is 0.31", "風險比是 0.31", "Ang risk ratio ay 0.31"] },
        { v: "up", t: ["Doxycycline increased the odds of illness", "Doxycycline 增加了發病的勝算", "Pinataas ng doxycycline ang odds ng sakit"] }
      ],
      why: ["OR = (2×3)/(8×7) = 0.11 (95% CI 0.01–0.84): cases had much lower odds of having taken doxycycline. A risk ratio cannot be computed here — Maya chose how many cases and controls to include, so 2/9 is not anyone's risk.",
        "OR = (2×3)/(8×7) = 0.11（95% 信賴區間 0.01–0.84）：病例服用 doxycycline 的勝算低很多。這裡不能算風險比——病例與對照的人數是 Maya 自己決定的，2/9 不是任何人的風險。",
        "OR = (2×3)/(8×7) = 0.11 (95% CI 0.01–0.84): mas mababa ang odds na uminom ng doxycycline ang mga kaso. Hindi puwedeng i-compute ang risk ratio dito — si Maya ang pumili kung ilan ang kaso at control, kaya ang 2/9 ay hindi risk ng sinuman."]
    }
  ];

  function ci95(est, se) { return [Math.exp(Math.log(est) - 1.96 * se), Math.exp(Math.log(est) + 1.96 * se)]; }
  function round2(x) { return x == null || !isFinite(x) ? "—" : x >= 10 ? x.toFixed(1) : x.toFixed(2); }

  WIDGETS["two-by-two"] = function (ctx) {
    var title = L(["Fill the 2×2 table", "填好 2×2 表", "Punan ang 2×2 table"]);
    ctx.host.appendChild(shell(ctx, title, null));
    var only = ctx.option("ph-2x2-");
    var list = ROUNDS_2X2.filter(function (r) { return !only || r.id === only; });
    if (!list.length) list = ROUNDS_2X2;
    var ri = 0, total = 0, totalMax = 0;
    function begin() {
      ri = 0; total = 0; totalMax = 0;
      list.forEach(function (r) { totalMax += r.people.length + 2; });
      ctx.setScore(0, totalMax);
      play(list[0]);
    }
    function play(r) {
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      var deck = shuffle(r.people), n = { a: 0, b: 0, c: 0, d: 0 }, roundScore = 0, firstTry = true, streak = 0;
      var cardEl = h("div", { class: "ph-person", "aria-live": "off" });
      var cellBtns = {};
      function cell(id) {
        var b = h("button", { type: "button", class: "ph-cell", onclick: function () { put(id); } }, [h("span", { class: "ph-cell-id" }, id), h("b", null, "0")]);
        cellBtns[id] = b;
        return b;
      }
      var totals = {};
      function tot(id) { totals[id] = h("td", { class: "ph-total" }, "0"); return totals[id]; }
      var table = h("table", { class: "ph-2x2" }, [
        h("thead", null, h("tr", null, [h("th"), h("th", { scope: "col" }, L(r.outLabel)), h("th", { scope: "col" }, L(r.noOutLabel)), h("th", { scope: "col" }, L(["Total", "合計", "Kabuuan"]))])),
        h("tbody", null, [
          h("tr", null, [h("th", { scope: "row" }, L(r.expLabel)), h("td", null, cell("a")), h("td", null, cell("b")), tot("ab")]),
          h("tr", null, [h("th", { scope: "row" }, L(r.unexpLabel)), h("td", null, cell("c")), h("td", null, cell("d")), tot("cd")])
        ])
      ]);
      var stats = h("div", { class: "ph-stats", "aria-live": "off" });
      var autoBtn = null;
      append(ctx.body, [
        h("p", { class: "ph-progress" }, U("roundOf", { i: ri + 1, n: list.length })),
        h("p", { class: "ph-task", tabindex: "-1" }, [h("strong", null, L(r.title)), h("br"), L(r.context)]),
        cardEl, h("div", { class: "ph-scroll-x" }, table), stats
      ]);
      function want(p) { return p.exp ? (p.ill ? "a" : "b") : (p.ill ? "c" : "d"); }
      function showCard() {
        clear(cardEl);
        if (!deck.length) { finish(); return; }
        var p = deck[0];
        var initials = p.name.replace(/^(Mang|Kuya|Ate|Ka)\s/, "").slice(0, 2);
        append(cardEl, [
          h("span", { class: "ph-avatar", "aria-hidden": "true", style: "--hue:" + ((p.name.length * 47) % 360) }, initials),
          h("span", { class: "ph-person-text" }, [
            h("span", null, [h("strong", null, p.name), h("span", { class: "ph-left" }, " · " + deck.length + " " + L(["left", "人待分類", "natitira"]))]),
            h("span", { class: "ph-fact " + (p.exp ? "yes" : "no") }, (p.exp ? "● " : "○ ") + L(p.exp ? r.expLabel : r.unexpLabel)),
            h("span", { class: "ph-fact " + (p.ill ? "yes" : "no") }, (p.ill ? "● " : "○ ") + L(p.ill ? r.outLabel : r.noOutLabel))
          ])
        ]);
        ctx.announce(cardEl.textContent);
      }
      function put(id) {
        if (!deck.length) return;
        var p = deck[0], w = want(p);
        if (id !== w) {
          firstTry = false; streak = 0;
          cellBtns[id].classList.remove("ph-shake"); void cellBtns[id].offsetWidth; cellBtns[id].classList.add("ph-shake");
          ctx.say("bad", fmt(L(["Row = exposure ({e}), column = outcome ({o}). That is cell {w}.", "列＝暴露（{e}），欄＝結果（{o}）。應放在 {w} 格。", "Row = exposure ({e}), column = outcome ({o}). Cell {w} iyon."]), { e: L(p.exp ? r.expLabel : r.unexpLabel), o: L(p.ill ? r.outLabel : r.noOutLabel), w: w }), badWord());
          return;
        }
        if (firstTry) roundScore++;
        firstTry = true; streak++;
        deck.shift();
        n[id]++;
        refresh();
        cellBtns[id].classList.remove("ph-pop"); void cellBtns[id].offsetWidth; cellBtns[id].classList.add("ph-pop");
        ctx.setScore(total + roundScore, totalMax);
        if (streak === 6 && deck.length > 2 && !autoBtn) {
          autoBtn = ctx.button("⏩ " + L(["You've got it — fill the rest", "你會了——自動填完", "Gets mo na — punan ang natitira"]), autofill);
          append(ctx.controls, autoBtn);
        }
        showCard();
      }
      function autofill() {
        while (deck.length) { var p = deck.shift(); n[want(p)]++; roundScore++; }
        ctx.setScore(total + roundScore, totalMax);
        refresh();
        showCard();
      }
      function refresh() {
        ["a", "b", "c", "d"].forEach(function (k) { cellBtns[k].querySelector("b").textContent = n[k]; cellBtns[k].setAttribute("aria-label", L(["cell", "格", "cell"]) + " " + k + ": " + n[k]); });
        totals.ab.textContent = n.a + n.b; totals.cd.textContent = n.c + n.d;
        clear(stats);
        var a = n.a, b = n.b, c = n.c, d = n.d;
        var or = b * c ? (a * d) / (b * c) : null;
        var lines = [];
        if (r.design === "cohort") {
          var r1 = a + b ? a / (a + b) : null, r0 = c + d ? c / (c + d) : null;
          var rr = r1 != null && r0 ? r1 / r0 : null;
          lines.push(row(L(["Risk if exposed", "暴露組風險", "Risk kung exposed"]), "a/(a+b) = " + a + "/" + (a + b), round2(r1)));
          lines.push(row(L(["Risk if unexposed", "非暴露組風險", "Risk kung hindi exposed"]), "c/(c+d) = " + c + "/" + (c + d), round2(r0)));
          lines.push(row(L(["Risk ratio (RR)", "風險比（RR）", "Risk ratio (RR)"]), L(["risk exposed ÷ risk unexposed", "暴露組風險 ÷ 非暴露組風險", "risk exposed ÷ risk unexposed"]), round2(rr), true));
          if (!deck.length && rr && a && c) {
            var ci = ci95(rr, Math.sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d)));
            lines.push(row(L(["95% CI of RR", "RR 的 95% 信賴區間", "95% CI ng RR"]), "", round2(ci[0]) + " – " + round2(ci[1])));
          }
        } else {
          lines.push(row(L(["Odds of exposure, cases", "病例的暴露勝算", "Odds ng exposure, kaso"]), "a/c = " + a + "/" + c, c ? round2(a / c) : "—"));
          lines.push(row(L(["Odds of exposure, controls", "對照的暴露勝算", "Odds ng exposure, controls"]), "b/d = " + b + "/" + d, d ? round2(b / d) : "—"));
          lines.push(row(L(["Risk ratio (RR)", "風險比（RR）", "Risk ratio (RR)"]), L(["not valid in a case-control study", "病例對照研究不能計算", "hindi valid sa case-control study"]), "✕", false, true));
        }
        lines.push(row(L(["Odds ratio (OR)", "勝算比（OR）", "Odds ratio (OR)"]), "(a×d)/(b×c) = (" + a + "×" + d + ")/(" + b + "×" + c + ")", round2(or), true));
        if (!deck.length && or && a && b && c && d) {
          var ci2 = ci95(or, Math.sqrt(1 / a + 1 / b + 1 / c + 1 / d));
          lines.push(row(L(["95% CI of OR", "OR 的 95% 信賴區間", "95% CI ng OR"]), "", round2(ci2[0]) + " – " + round2(ci2[1])));
        }
        append(stats, h("table", { class: "ph-stat-table" }, h("tbody", null, lines)));
      }
      function row(name, formula, value, strong, muted) {
        return h("tr", { class: (strong ? "is-key" : "") + (muted ? " is-muted" : "") }, [h("th", { scope: "row" }, name), h("td", { class: "ph-formula" }, formula), h("td", { class: "ph-val" }, value)]);
      }
      function finish() {
        Object.keys(cellBtns).forEach(function (k) { cellBtns[k].disabled = true; });
        clear(ctx.controls);
        refresh();
        append(cardEl, h("strong", { class: "ph-q" }, L(r.q)));
        var ch = choiceButtons(shuffle(r.opts).map(function (o) { return { label: L(o.t), value: o.v }; }), function (o, buttons, btn) {
          var ok = o.value === "ok";
          lockChoices(buttons, "ok", btn);
          if (ok) roundScore += 2;
          total += roundScore;
          ctx.setScore(total, totalMax);
          ctx.say(ok ? "good" : "bad", L(r.why), ok ? goodWord() : badWord());
          if (ok) ctx.celebrate(roundScore === r.people.length + 2);
          var last = ri === list.length - 1;
          var nb = ctx.button(last ? "★ " + U("seeScore") : U("nextRound") + " →", function () {
            if (last) endScreen(ctx, total, totalMax, begin, ["Cohort study: compare risks (RR). Case-control study: compare odds of exposure (OR) — never an RR. Always look at the confidence interval.", "世代研究：比較風險（RR）。病例對照研究：比較暴露勝算（OR）——不能算 RR。永遠要看信賴區間。", "Cohort study: ikumpara ang risk (RR). Case-control study: ikumpara ang odds ng exposure (OR) — hindi RR. Laging tingnan ang confidence interval."]);
            else { ri++; play(list[ri]); }
          }, "ph-primary");
          clear(ctx.controls);
          append(ctx.controls, nb);
          focusQuiet(nb);
        }, "ph-stack");
        cardEl.appendChild(ch);
        focusQuiet(ch.buttons[0]);
      }
      refresh();
      showCard();
    }
    begin();
  };

  /* =============================================== threshold-watch (ch 06) */
  /* The Santa Luz series itself (santa_luz_dengue_weekly.csv): 2026-W20…W39 and
     the baseline years 2022–2025 from W19 to W40, so that every week has its
     window w−1, w, w+1 (12 values), exactly as in chapter 06. */
  var TW = {
    first: 20,
    hist: {
      2022: [4, 7, 2, 1, 2, 1, 5, 6, 12, 6, 7, 17, 9, 3, 12, 16, 13, 17, 9, 17, 20, 11],
      2023: [2, 2, 4, 8, 4, 4, 11, 5, 7, 8, 6, 9, 14, 6, 12, 10, 8, 12, 17, 13, 22, 17],
      2024: [5, 2, 4, 4, 4, 5, 5, 6, 5, 1, 3, 8, 16, 7, 6, 10, 19, 30, 39, 24, 30, 19],
      2025: [4, 4, 6, 2, 4, 3, 6, 3, 4, 4, 6, 10, 10, 10, 13, 14, 10, 9, 10, 24, 19, 14]
    },
    now: [5, 2, 1, 4, 2, 0, 2, 6, 4, 6, 14, 11, 33, 28, 48, 34, 58, 63, 54, 45]
  };
  /** Monday of ISO week w in 2026, as a UTC Date. */
  function isoMonday2026(w) { return new Date(Date.UTC(2025, 11, 29 + 7 * (w - 1))); }
  function dateText(d) {
    var m = d.getUTCMonth(), day = d.getUTCDate();
    if (LI === 1) return (m + 1) + "/" + day;
    return day + " " + MONTHS[LI][m];
  }
  function baseline(i) {
    var v = [];
    Object.keys(TW.hist).forEach(function (y) { v.push(TW.hist[y][i], TW.hist[y][i + 1], TW.hist[y][i + 2]); });
    var m = mean(v), sdev = sd(v);
    return { values: v, mean: m, sd: sdev, thr: m + 2 * sdev };
  }

  WIDGETS["threshold-watch"] = function (ctx) {
    var title = L(["Threshold watch & 7-1-7", "閾值監看與 7-1-7", "Threshold watch at 7-1-7"]);
    var intro = L(["Weekly dengue counts for Santa Luz arrive one week at a time. Raise the alert as soon as a week goes above the threshold (mean + 2 SD of weeks w−1, w and w+1 in 2022–2025).",
      "Santa Luz 的每週登革熱病例數一週一週送來。只要某週超過閾值（2022–2025 年第 w−1、w、w+1 週的平均值 + 2 個標準差），就立刻發出警戒。",
      "Isa-isang linggo dumarating ang bilang ng dengue sa Santa Luz. Mag-alert agad kapag lumampas ang isang linggo sa threshold (mean + 2 SD ng mga linggong w−1, w at w+1 noong 2022–2025)."]);
    ctx.host.appendChild(shell(ctx, title, intro));
    var n = TW.now.length, B = [];
    for (var i = 0; i < n; i++) B.push(baseline(i));
    var cross = -1;
    for (var k = 0; k < n; k++) { if (TW.now[k] > B[k].thr) { cross = k; break; } }
    var t, falseAlarms, timer, alertAt, score;
    var svgEl, barsG, curText, playBtn, alertBtn, stepBtn, detailBox, detailBtn;
    var X0 = 30, X1 = 352, Y0 = 186, Y1 = 14, YMAX = 80;
    function xs(i) { return X0 + (i + 0.5) * (X1 - X0) / n; }
    function ys(v) { return Y0 - (v / YMAX) * (Y0 - Y1); }
    function build() {
      t = 4; falseAlarms = 0; alertAt = -1; score = 0;
      stopPlay();
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      ctx.setScore(0, 5);
      var bw = (X1 - X0) / n;
      var grid = [];
      [0, 20, 40, 60, 80].forEach(function (v) {
        grid.push(s("line", { x1: X0, x2: X1, y1: ys(v), y2: ys(v), class: "ph-grid" }));
        grid.push(s("text", { x: X0 - 4, y: ys(v) + 3, class: "ph-tick", "text-anchor": "end" }, String(v)));
      });
      for (var i = 0; i < n; i += 2) grid.push(s("text", { x: xs(i), y: Y0 + 12, class: "ph-tick", "text-anchor": "middle" }, "W" + (TW.first + i)));
      var thrPts = [], meanPts = [];
      B.forEach(function (b, i) {
        thrPts.push((X0 + i * bw).toFixed(1) + "," + ys(b.thr).toFixed(1), (X0 + (i + 1) * bw).toFixed(1) + "," + ys(b.thr).toFixed(1));
        meanPts.push(xs(i).toFixed(1) + "," + ys(b.mean).toFixed(1));
      });
      barsG = s("g");
      var typhoon = s("g", { class: "ph-typhoon" }, [
        s("line", { x1: xs(9), x2: xs(9), y1: Y1, y2: Y0, class: "ph-event-line" }),
        s("text", { x: xs(9) + 3, y: Y1 + 8, class: "ph-tick" }, "🌀 Amihan")
      ]);
      svgEl = s("svg", { viewBox: "0 0 360 204", class: "ph-chart", role: "img", "aria-label": L(["Weekly dengue counts with the alert threshold", "每週登革熱病例數與警戒閾值", "Lingguhang bilang ng dengue at alert threshold"]) }, [
        s("g", null, grid),
        s("polyline", { points: meanPts.join(" "), class: "ph-mean-line" }),
        barsG,
        s("polyline", { points: thrPts.join(" "), class: "ph-thr-line" }),
        typhoon,
        s("line", { x1: X0, x2: X1, y1: Y0, y2: Y0, class: "ph-axis" })
      ]);
      curText = h("p", { class: "ph-readout", "aria-live": "polite" });
      var legend = h("p", { class: "ph-legend" }, [
        h("span", { class: "ph-key ph-key-bar" }), " " + L(["2026 cases", "2026 病例數", "Kaso 2026"]) + "  ",
        h("span", { class: "ph-key ph-key-thr" }), " " + L(["alert threshold", "警戒閾值", "alert threshold"]) + "  ",
        h("span", { class: "ph-key ph-key-mean" }), " " + L(["usual (mean)", "平常值（平均）", "karaniwan (mean)"])
      ]);
      detailBox = h("div", { class: "ph-detail", hidden: true });
      detailBtn = h("button", { type: "button", class: "ph-link-btn", "aria-expanded": "false", onclick: function () {
        var open = detailBox.hidden;
        detailBox.hidden = !open;
        detailBtn.setAttribute("aria-expanded", open ? "true" : "false");
        renderDetail();
      } }, L(["How is this week's threshold computed?", "這週的閾值怎麼算？", "Paano kinukuwenta ang threshold ngayong linggo?"]));
      append(ctx.body, [h("div", { class: "ph-chart-wrap" }, svgEl), legend, curText, detailBtn, detailBox]);
      stepBtn = ctx.button(L(["Next week ▶", "下一週 ▶", "Susunod na linggo ▶"]), function () { stopPlay(); step(); });
      playBtn = ctx.button(L(["Auto-play", "自動播放", "Auto-play"]), togglePlay);
      playBtn.setAttribute("aria-pressed", "false");
      alertBtn = ctx.button("🚨 " + L(["Raise the alert!", "發出警戒！", "Mag-alert!"]), raise, "ph-alarm");
      append(ctx.controls, [alertBtn, stepBtn, playBtn]);
      draw();
    }
    function renderDetail() {
      if (detailBox.hidden) return;
      clear(detailBox);
      var b = B[t];
      append(detailBox, [
        h("p", null, fmt(L(["Week W{w}: weeks W{a}–W{z} of 2022–2025 (12 values): {v}", "W{w}：2022–2025 年第 W{a}–W{z} 週（12 個數值）：{v}", "Linggo W{w}: mga linggong W{a}–W{z} noong 2022–2025 (12 value): {v}"]), { w: TW.first + t, a: TW.first + t - 1, z: TW.first + t + 1, v: b.values.join(", ") })),
        h("pre", { class: "ph-calc" }, "mean      = " + num(b.mean, 1) + "\nSD        = " + num(b.sd, 1) + "\nthreshold = mean + 2 × SD\n          = " + num(b.mean, 1) + " + 2 × " + num(b.sd, 1) + " = " + num(b.thr, 1))
      ]);
    }
    function draw() {
      clear(barsG);
      var bw = (X1 - X0) / n;
      for (var i = 0; i <= t; i++) {
        var over = TW.now[i] > B[i].thr;
        barsG.appendChild(s("rect", { x: X0 + i * bw + 1, y: ys(TW.now[i]), width: bw - 2, height: Y0 - ys(TW.now[i]), class: "ph-bar" + (over ? " is-over" : "") + (i === t ? " is-new" : "") }));
      }
      var b = B[t];
      clear(curText);
      append(curText, [h("strong", null, "W" + (TW.first + t) + ": "), TW.now[t] + " " + L(["cases", "例", "kaso"]) + " · " + L(["threshold", "閾值", "threshold"]) + " " + num(b.thr, 1) + " — ",
        TW.now[t] > b.thr ? h("strong", { class: "ph-over" }, L(["ABOVE", "超過", "LAMPAS"])) : L(["below", "未超過", "mas mababa"])]);
      renderDetail();
      if (t >= n - 1 && alertAt < 0) { stopPlay(); missed(); }
    }
    function step() { if (alertAt >= 0 || t >= n - 1) return; t++; draw(); }
    function togglePlay() {
      if (timer) { stopPlay(); return; }
      playBtn.setAttribute("aria-pressed", "true");
      playBtn.textContent = L(["Pause", "暫停", "Pause"]);
      timer = ctx.every(step, reduced() ? 2200 : 1400);
    }
    function stopPlay() {
      if (timer) ctx.stopEvery(timer);
      timer = null;
      if (playBtn) { playBtn.setAttribute("aria-pressed", "false"); playBtn.textContent = L(["Auto-play", "自動播放", "Auto-play"]); }
    }
    function raise() {
      if (alertAt >= 0) return;
      if (TW.now[t] <= B[t].thr && t < cross) {
        falseAlarms++;
        stopPlay();
        ctx.say("bad", fmt(L(["False alarm: W{w} has {c} cases, below the threshold of {th}. A rise is worth watching, but an alert sends a field team out. Keep watching.", "誤報：W{w} 有 {c} 例，低於閾值 {th}。上升值得留意，但發出警戒就要派出現場團隊。繼續監看。", "False alarm: {c} kaso ang W{w}, mas mababa sa threshold na {th}. Dapat bantayan ang pagtaas, pero magpapadala ng field team ang alert. Bantay lang."]), { w: TW.first + t, c: TW.now[t], th: num(B[t].thr, 1) }), badWord());
        return;
      }
      alertAt = t;
      stopPlay();
      var delay = t - cross;
      var pts = delay === 0 ? 3 : delay === 1 ? 1 : 0;
      score = Math.max(0, pts - falseAlarms);
      ctx.setScore(score, 5);
      var emergence = isoMonday2026(TW.first + cross);
      var detected = isoMonday2026(TW.first + t + 1);
      var days = Math.round((detected - emergence) / 864e5);
      var msg = delay === 0 ?
        fmt(L(["Alert raised the moment W{w} crossed the threshold.", "W{w} 一超過閾值就發出警戒。", "Nag-alert agad nang lumampas ang W{w} sa threshold."]), { w: TW.first + cross }) :
        fmt(L(["W{w} had already crossed the threshold {d} week(s) earlier.", "W{w} 早在 {d} 週前就已經超過閾值了。", "{d} linggo nang mas maaga lumampas ang W{w} sa threshold."]), { w: TW.first + cross, d: delay });
      if (falseAlarms) msg += " " + fmt(L(["({f} false alarm(s) cost points.)", "（{f} 次誤報扣分。）", "(Nabawasan ng puntos dahil sa {f} false alarm.)"]), { f: falseAlarms });
      ctx.say(delay === 0 ? "good" : "bad", msg, delay === 0 ? goodWord() : null);
      if (delay === 0) ctx.celebrate(false);
      phase717(emergence, detected, days);
    }
    function missed() {
      alertAt = t;
      var emergence = isoMonday2026(TW.first + cross);
      var detected = isoMonday2026(TW.first + t + 1);
      ctx.say("bad", fmt(L(["The season ended without an alert, although W{w} crossed the threshold.", "整個季節都沒有發出警戒，但 W{w} 其實已經超過閾值。", "Natapos ang season nang walang alert, kahit lumampas na ang W{w} sa threshold."]), { w: TW.first + cross }));
      phase717(emergence, detected, Math.round((detected - emergence) / 864e5));
    }
    function phase717(emergence, detected, dDays) {
      clear(ctx.controls);
      var card = h("div", { class: "ph-717" });
      ctx.body.appendChild(card);
      var rows = [];
      function addRow(label, target, days) {
        var ok = days <= target;
        rows.push(h("tr", { class: ok ? "is-ok" : "is-late" }, [h("th", { scope: "row" }, L(label)), h("td", null, "≤ " + target + " " + L(["d", "天", "araw"])), h("td", null, days + " " + L(["d", "天", "araw"])), h("td", { class: "ph-mark" }, ok ? "✓" : "✕")]));
        return ok;
      }
      var detectOk = addRow(["Detect", "偵測", "Detect"], 7, dDays);
      function table() {
        return h("table", { class: "ph-717-table" }, [
          h("thead", null, h("tr", null, [h("th", null, "7-1-7"), h("th", null, L(["Target", "目標", "Target"])), h("th", null, L(["Yours", "你的", "Iyo"])), h("th", null, "")])),
          h("tbody", null, rows.slice())
        ]);
      }
      var explain = h("p", { class: "ph-hint" }, fmt(L(["Emergence = {e} (first day of W{w}, the first week above the threshold). A week's count arrives the Monday after it ends, so detection = {d}.", "事件出現＝{e}（W{w} 的第一天，也就是第一個超過閾值的週）。每週數字在該週結束後的週一送達，所以偵測日＝{d}。", "Emergence = {e} (unang araw ng W{w}, ang unang linggong lampas sa threshold). Dumarating ang bilang tuwing Lunes pagkatapos ng linggo, kaya detection = {d}."]), { e: dateText(emergence), w: TW.first + cross, d: dateText(detected) }));
      var tableHolder = h("div", { class: "ph-scroll-x" }, table());
      append(card, [h("p", { class: "ph-task", tabindex: "-1" }, h("strong", null, L(["Now the 7-1-7 clock: detect ≤ 7 days, notify ≤ 1 day, complete the early response ≤ 7 days.", "接著是 7-1-7 計時：≤7 天偵測、≤1 天通報、≤7 天完成早期應變。", "Ngayon, ang orasan ng 7-1-7: detect ≤ 7 araw, notify ≤ 1 araw, tapusin ang early response ≤ 7 araw."]))), explain, tableHolder]);
      if (detectOk) score += 0;
      var q1 = h("div", { class: "ph-step" }, [h("p", { class: "ph-q" }, L(["When does Maya notify the PESU?", "Maya 什麼時候通報 PESU？", "Kailan ipapaalam ni Maya sa PESU?"]))]);
      var c1 = choiceButtons(shuffle([
        { label: L(["Today: phone Doc Mon and file the event report", "今天：打電話給 Doc Mon 並填報事件通報", "Ngayon din: tawagan si Doc Mon at mag-file ng event report"]), value: "0" },
        { label: L(["On Friday, with the weekly report", "週五，跟每週報告一起", "Sa Biyernes, kasabay ng weekly report"]), value: "4" },
        { label: L(["When the lab has confirmed the cases (~10 days)", "等實驗室確認病例後（約 10 天）", "Kapag na-confirm na ng lab ang mga kaso (~10 araw)"]), value: "10" }
      ]), function (o, buttons, btn) {
        lockChoices(buttons, "0", btn);
        var days = +o.value, ok = addRow(["Notify", "通報", "Notify"], 1, days);
        if (ok) score++;
        ctx.setScore(score, 5);
        clear(tableHolder); tableHolder.appendChild(table());
        ctx.say(ok ? "good" : "bad", L(["Notification means telling the next level right away. Waiting for a weekly report or for lab confirmation spends the 1-day budget many times over.", "通報就是立刻告知上一層級。等每週報告或實驗室確認，會把 1 天的期限用掉好幾倍。", "Ang notification ay agarang pagsabi sa susunod na antas. Kapag hinintay ang weekly report o lab confirmation, ilang beses na lampas ang 1 araw."]), ok ? goodWord() : badWord());
        askResponse();
      }, "ph-stack");
      q1.appendChild(c1);
      card.appendChild(q1);
      focusQuiet(c1.buttons[0]);
      function askResponse() {
        var q2 = h("div", { class: "ph-step" }, [h("p", { class: "ph-q" }, L(["Which plan completes the early response within 7 days?", "哪一個計畫能在 7 天內完成早期應變？", "Aling plano ang tatapos sa early response sa loob ng 7 araw?"]))]);
        var c2 = choiceButtons(shuffle([
          { label: L(["Within 5 days: case investigation, 4S clean-up with BHWs, clinics alerted, risk communication", "5 天內：疫調、與 BHW 一起進行 4S 清除孳生源、通知診所、風險溝通", "Sa loob ng 5 araw: case investigation, 4S clean-up kasama ang BHWs, alerto sa clinics, risk communication"]), value: "5" },
          { label: L(["Fog the whole city tomorrow — and that's it", "明天全市噴藥——就這樣", "I-fog ang buong lungsod bukas — tapos na"]), value: "fog" },
          { label: L(["Plan it at next month's Local Health Board meeting", "等下個月地方衛生委員會開會再規劃", "Planuhin sa pulong ng Local Health Board sa susunod na buwan"]), value: "30" }
        ]), function (o, buttons, btn) {
          lockChoices(buttons, "5", btn);
          var days = o.value === "5" ? 5 : o.value === "fog" ? 99 : 30;
          var ok = days <= 7;
          rows.push(h("tr", { class: ok ? "is-ok" : "is-late" }, [h("th", { scope: "row" }, L(["Respond", "應變", "Respond"])), h("td", null, "≤ 7 " + L(["d", "天", "araw"])), h("td", null, days === 99 ? L(["not done", "未完成", "hindi natapos"]) : days + " " + L(["d", "天", "araw"])), h("td", { class: "ph-mark" }, ok ? "✓" : "✕")]));
          if (ok) score++;
          ctx.setScore(score, 5);
          clear(tableHolder); tableHolder.appendChild(table());
          ctx.say(ok ? "good" : "bad", L(["An early response is a set of actions, not one spray: investigate, remove breeding sites (4S), alert clinics, inform the public. Fogging alone is not enough and is meant for outbreak hotspots.", "早期應變是一組行動，不是噴一次藥：疫調、清除孳生源（4S）、通知診所、告知民眾。單靠噴藥不夠，而且只用於疫情熱點。", "Hanay ng aksyon ang early response, hindi iisang spray: imbestigasyon, sirain ang breeding sites (4S), alertuhin ang clinics, ipaalam sa publiko. Hindi sapat ang fogging lang, at para lang ito sa outbreak hotspots."]), ok ? goodWord() : badWord());
          clear(ctx.controls);
          var b = ctx.button("★ " + U("seeScore"), function () {
            endScreen(ctx, score, 5, build, ["With weekly data, reacting the same day the week arrives is the only way to meet 'detect ≤ 7 days'. Then notify within a day and finish the early response within a week.", "使用每週資料時，唯有在數字送達當天就反應，才能達成「≤7 天偵測」。接著 1 天內通報，一週內完成早期應變。", "Sa lingguhang datos, ang pagkilos sa mismong araw na dumating ang bilang ang tanging paraan para maabot ang 'detect ≤ 7 araw'. Tapos notify sa loob ng isang araw at tapusin ang early response sa loob ng isang linggo."]);
          }, "ph-primary");
          append(ctx.controls, b);
          if (score === 5) ctx.celebrate(true);
          focusQuiet(b);
        }, "ph-stack");
        q2.appendChild(c2);
        card.appendChild(q2);
        focusQuiet(c2.buttons[0]);
      }
    }
    build();
  };

  /* =============================================== forecast-guess (ch 07) */
  /* Real Santa Luz weeks (santa_luz_dengue_weekly.csv) and the TimesFM 3.0
     forecasts cached for chapter 07 (data/tsfm_cache/ph07_dengue.json):
     round 1 = backtest origin 2025-W31, round 2 = the take-off forecast made
     with the history up to 2026-W31. Median and the 0.1/0.9 quantiles, rounded. */
  var FORECASTS = [
    {
      id: "normal", firstWeek: 19, year: 2025, yMax: 40,
      title: ["Round 1 — an ordinary year (2025)", "第 1 回合——平常的一年（2025）", "Round 1 — karaniwang taon (2025)"],
      hist: [4, 4, 6, 2, 4, 3, 6, 3, 4, 4, 6, 10],
      truth: [10, 10, 13, 14, 10, 9, 10, 24],
      model: [8, 9, 9, 10, 11, 11, 12, 12],
      lo: [4, 4, 4, 4, 5, 5, 5, 5], hi: [14, 16, 17, 19, 20, 21, 22, 23],
      seasonal: [16, 7, 6, 10, 19, 30, 39, 24],
      lesson: ["In an ordinary season TimesFM beat 'same weeks last year' easily, and its 80% band held the truth in 7 of the 8 weeks. Even so: always compare with a baseline before trusting a model.", "在平常的季節，TimesFM 輕鬆勝過「去年同期」，而且 8 週中有 7 週的真實值落在它的 80% 區間內。即使如此，信任模型之前一定要和基準比較。", "Sa karaniwang season, madaling tinalo ng TimesFM ang 'parehong linggo noong nakaraang taon', at nasa 80% band nito ang totoo sa 7 sa 8 linggo. Gayunman, laging ikumpara sa baseline bago pagkatiwalaan ang model."]
    },
    {
      id: "typhoon", firstWeek: 20, year: 2026, yMax: 80,
      title: ["Round 2 — after Typhoon Amihan (2026)", "第 2 回合——颱風 Amihan 之後（2026）", "Round 2 — pagkatapos ng Bagyong Amihan (2026)"],
      hist: [5, 2, 1, 4, 2, 0, 2, 6, 4, 6, 14, 11],
      truth: [33, 28, 48, 34, 58, 63, 54, 45],
      model: [10, 10, 10, 11, 11, 11, 11, 12],
      lo: [5, 5, 5, 5, 5, 5, 5, 5], hi: [17, 18, 19, 20, 21, 22, 23, 23],
      seasonal: [10, 13, 14, 10, 9, 10, 24, 19],
      lesson: ["The model only saw past counts — it could not know about the flood and the standing water. The truth fell outside its 80% band in all 8 weeks, as in chapter 07, and the last week (45) is still incomplete. An honest evaluation reports this. In chapter 07 even rainfall barely helped; a person who knows a typhoon just hit (like you!) can.", "模型只看過去的病例數——它不知道洪水和積水。8 週的真實值全都落在 80% 區間之外，和第 07 章一樣，而且最後一週（45）的資料還不完整。誠實的評估要把這點寫出來。第 07 章中連加入雨量都幫助不大；知道颱風剛來過的人（就是你！）才幫得上忙。", "Mga nakaraang bilang lang ang nakita ng model — hindi nito alam ang baha at stagnant na tubig. Nasa labas ng 80% band nito ang totoo sa lahat ng 8 linggo, gaya sa kabanata 07, at kulang pa ang huling linggo (45). Iniuulat ito ng tapat na ebalwasyon. Sa kabanata 07, halos hindi nakatulong kahit ang rainfall; ang taong alam na kakadaan lang ng bagyo (ikaw!) ang makatutulong."]
    }
  ];

  WIDGETS["forecast-guess"] = function (ctx) {
    var title = L(["Forecast challenge: you vs the model", "預測挑戰：你 vs 模型", "Forecast challenge: ikaw laban sa model"]);
    var intro = L(["Drag (or use the arrow keys on each dot) to draw your forecast for the next 8 weeks, then reveal what happened.", "拖曳（或在每個點上用方向鍵）畫出你對接下來 8 週的預測，再揭曉實際結果。", "I-drag (o gamitin ang arrow keys sa bawat tuldok) para iguhit ang forecast mo sa susunod na 8 linggo, tapos tingnan ang nangyari."]);
    ctx.host.appendChild(shell(ctx, title, intro));
    var only = ctx.option("ph-forecast-");
    var list = FORECASTS.filter(function (f) { return !only || f.id === only; });
    if (!list.length) list = FORECASTS;
    var ri = 0, total = 0;
    function begin() { ri = 0; total = 0; ctx.setScore(0, list.length * 3); play(list[0]); }
    function play(f) {
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      var H = f.hist.length, F = f.truth.length, N = H + F;
      var X0 = 30, X1 = 352, Y0 = 180, Y1 = 12;
      var guess = []; for (var i = 0; i < F; i++) guess.push(f.hist[H - 1]);
      var revealed = false;
      function xs(i) { return X0 + (i + 0.5) * (X1 - X0) / N; }
      function ys(v) { return Y0 - (v / f.yMax) * (Y0 - Y1); }
      function yToV(y) { return Math.max(0, Math.min(f.yMax, Math.round(((Y0 - y) / (Y0 - Y1)) * f.yMax))); }
      var bw = (X1 - X0) / N;
      var kids = [];
      var step = f.yMax > 40 ? 20 : 10;
      for (var v = 0; v <= f.yMax; v += step) {
        kids.push(s("line", { x1: X0, x2: X1, y1: ys(v), y2: ys(v), class: "ph-grid" }));
        kids.push(s("text", { x: X0 - 4, y: ys(v) + 3, class: "ph-tick", "text-anchor": "end" }, String(v)));
      }
      for (i = 0; i < N; i += 4) kids.push(s("text", { x: xs(i), y: Y0 + 12, class: "ph-tick", "text-anchor": "middle" }, "W" + (f.firstWeek + i)));
      kids.push(s("rect", { x: X0 + H * bw, y: Y1, width: F * bw, height: Y0 - Y1, class: "ph-future-bg" }));
      kids.push(s("text", { x: X0 + (H + F / 2) * bw, y: Y1 + 10, class: "ph-tick ph-draw-hint", "text-anchor": "middle" }, "✎ " + L(["draw here", "在這裡畫", "iguhit dito"])));
      f.hist.forEach(function (val, i2) {
        kids.push(s("rect", { x: X0 + i2 * bw + 1, y: ys(val), width: bw - 2, height: Y0 - ys(val), class: "ph-bar" }));
      });
      var overlay = s("g");
      var guessLine = s("polyline", { class: "ph-guess-line" });
      var handles = [];
      var drawRect = s("rect", { x: X0 + H * bw, y: Y1 - 6, width: F * bw, height: Y0 - Y1 + 12, class: "ph-draw-zone" });
      kids.push(overlay, s("line", { x1: X0, x2: X1, y1: Y0, y2: Y0, class: "ph-axis" }), drawRect, guessLine);
      for (i = 0; i < F; i++) {
        (function (k) {
          var c = s("circle", { r: 6.5, class: "ph-handle", tabindex: "0", role: "slider", "aria-valuemin": "0", "aria-valuemax": String(f.yMax),
            "aria-label": fmt(L(["Your forecast for week W{w}", "你對 W{w} 的預測", "Forecast mo para sa W{w}"]), { w: f.firstWeek + H + k }) });
          c.addEventListener("keydown", function (e) {
            if (revealed) return;
            var d = { ArrowUp: 1, ArrowRight: 1, ArrowDown: -1, ArrowLeft: -1, PageUp: 5, PageDown: -5 }[e.key];
            if (e.key === "Home") d = -guess[k];
            if (e.key === "End") d = f.yMax - guess[k];
            if (d == null) return;
            e.preventDefault();
            setGuess(k, guess[k] + d);
          });
          handles.push(c);
          kids.push(c);
        })(i);
      }
      var svgEl = s("svg", { viewBox: "0 0 360 196", class: "ph-chart ph-forecast", role: "group", "aria-label": L(["Weekly dengue counts and your forecast", "每週登革熱病例數與你的預測", "Lingguhang dengue at ang forecast mo"]) }, kids);
      function setGuess(k, v) {
        guess[k] = Math.max(0, Math.min(f.yMax, Math.round(v)));
        render();
      }
      function render() {
        guessLine.setAttribute("points", [xs(H - 1) + "," + ys(f.hist[H - 1])].concat(guess.map(function (g, k) { return xs(H + k) + "," + ys(g); })).join(" "));
        handles.forEach(function (c, k) {
          c.setAttribute("cx", xs(H + k)); c.setAttribute("cy", ys(guess[k]));
          c.setAttribute("aria-valuenow", String(guess[k]));
          c.setAttribute("aria-valuetext", guess[k] + " " + L(["cases", "例", "kaso"]));
        });
      }
      // Pointer drawing (mouse, pen and touch). touch-action:none is set on the draw zone only.
      var drawing = false;
      function toLocal(e) {
        var m = svgEl.getScreenCTM();
        if (!m) return null;
        var p = svgEl.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
        return p.matrixTransform(m.inverse());
      }
      function apply(e) {
        var p = toLocal(e);
        if (!p) return;
        var k = Math.floor((p.x - X0) / bw) - H;
        if (k < 0 || k >= F) return;
        setGuess(k, yToV(p.y));
      }
      function down(e) {
        if (revealed) return;
        drawing = true;
        try { e.target.setPointerCapture(e.pointerId); } catch (err) { /* ignore */ }
        e.preventDefault();
        apply(e);
      }
      [drawRect].concat(handles).forEach(function (el) {
        el.addEventListener("pointerdown", down);
        el.addEventListener("pointermove", function (e) { if (drawing) apply(e); });
        el.addEventListener("pointerup", function () { drawing = false; });
        el.addEventListener("pointercancel", function () { drawing = false; });
      });
      render();
      var legend = h("p", { class: "ph-legend" }, [h("span", { class: "ph-key ph-key-bar" }), " " + L(["observed", "已觀察", "naobserbahan"]) + "  ", h("span", { class: "ph-key ph-key-guess" }), " " + L(["your forecast", "你的預測", "forecast mo"])]);
      var result = h("div", { class: "ph-result" });
      append(ctx.body, [h("p", { class: "ph-progress" }, U("roundOf", { i: ri + 1, n: list.length })), h("p", { class: "ph-task", tabindex: "-1" }, h("strong", null, L(f.title))), h("div", { class: "ph-chart-wrap" }, svgEl), legend, result]);
      var revealBtn = ctx.button("👀 " + L(["Reveal the truth", "揭曉結果", "Ipakita ang totoo"]), reveal, "ph-primary");
      append(ctx.controls, revealBtn);
      function line(vals, cls) { return s("polyline", { class: cls, points: vals.map(function (v2, k) { return xs(H + k) + "," + ys(v2); }).join(" ") }); }
      function mae(a) { var t2 = 0; for (var k = 0; k < F; k++) t2 += Math.abs(a[k] - f.truth[k]); return t2 / F; }
      function reveal() {
        if (revealed) return;
        revealed = true;
        svgEl.classList.add("is-revealed");
        handles.forEach(function (c) { c.setAttribute("tabindex", "-1"); c.setAttribute("aria-disabled", "true"); });
        var band = f.lo.map(function (v2, k) { return xs(H + k) + "," + ys(v2); }).concat(f.hi.slice().reverse().map(function (v2, k) { return xs(H + F - 1 - k) + "," + ys(v2); }));
        append(overlay, [
          s("polygon", { class: "ph-band", points: band.join(" ") }),
          line(f.seasonal, "ph-seasonal-line"),
          line(f.model, "ph-model-line"),
          line(f.truth, "ph-truth-line")
        ]);
        f.truth.forEach(function (v2, k) { overlay.appendChild(s("circle", { cx: xs(H + k), cy: ys(v2), r: 3, class: "ph-truth-dot" })); });
        var last = []; for (var k = 0; k < F; k++) last.push(f.hist[H - 1]);
        var entries = [
          { who: L(["You", "你", "Ikaw"]), mae: mae(guess), me: true },
          { who: L(["TimesFM 3.0 (chapter 07 run)", "TimesFM 3.0（第 07 章的結果）", "TimesFM 3.0 (run ng kabanata 07)"]), mae: mae(f.model) },
          { who: L(["Same weeks last year", "去年同期", "Parehong linggo noong nakaraang taon"]), mae: mae(f.seasonal) },
          { who: L(["Last value carried forward", "沿用最後一週的值", "Huling value na inulit"]), mae: mae(last) }
        ];
        var beaten = entries.slice(1).filter(function (e) { return entries[0].mae < e.mae; }).length;
        total += beaten;
        ctx.setScore(total, list.length * 3);
        var sorted = entries.slice().sort(function (a, b) { return a.mae - b.mae; });
        var inBand = f.truth.filter(function (v2, k2) { return v2 >= f.lo[k2] && v2 <= f.hi[k2]; }).length;
        append(result, [
          h("p", { class: "ph-legend" }, [h("span", { class: "ph-key ph-key-truth" }), " " + L(["what happened", "實際結果", "ang nangyari"]) + "  ", h("span", { class: "ph-key ph-key-model" }), " " + L(["model + 80% band", "模型 + 80% 區間", "model + 80% band"]) + "  ", h("span", { class: "ph-key ph-key-seasonal" }), " " + L(["last year", "去年同期", "nakaraang taon"])]),
          h("table", { class: "ph-stat-table" }, [h("thead", null, h("tr", null, [h("th", null, "#"), h("th", null, L(["Forecast", "預測", "Forecast"])), h("th", null, L(["Mean absolute error (cases/week)", "平均絕對誤差（例/週）", "Mean absolute error (kaso/linggo)"]))])),
            h("tbody", null, sorted.map(function (e, r) { return h("tr", { class: e.me ? "is-key" : "" }, [h("td", null, String(r + 1)), h("td", null, e.who), h("td", { class: "ph-val" }, num(e.mae, 1))]); }))]),
          h("p", { class: "ph-hint" }, fmt(L(["The truth fell inside the model's 80% band in {k} of {n} weeks.", "真實值有 {k} / {n} 週落在模型的 80% 區間內。", "Nasa loob ng 80% band ng model ang totoo sa {k} sa {n} linggo."]), { k: inBand, n: F }))
        ]);
        var lead = beaten === 3 ? L(["You beat every forecast!", "你打敗了所有預測！", "Tinalo mo lahat ng forecast!"]) : beaten ? fmt(L(["You beat {b} of 3.", "你贏了 3 個中的 {b} 個。", "Natalo mo ang {b} sa 3."]), { b: beaten }) : L(["The others won this round.", "這回合其他預測贏了。", "Panalo ang iba ngayong round."]);
        ctx.say(beaten >= 2 ? "good" : "info", L(f.lesson), lead);
        if (beaten >= 2) ctx.celebrate(beaten === 3);
        clear(ctx.controls);
        var isLast = ri === list.length - 1;
        var nb = ctx.button(isLast ? "★ " + U("seeScore") : U("nextRound") + " →", function () {
          if (isLast) endScreen(ctx, total, list.length * 3, begin, ["Honest forecasting: compare against simple baselines, report the error, show the uncertainty band — and say when the world changed.", "誠實的預測：和簡單基準比較、報告誤差、呈現不確定性區間——世界改變時要說出來。", "Tapat na forecasting: ikumpara sa simpleng baselines, iulat ang error, ipakita ang uncertainty band — at sabihin kapag nagbago ang mundo."]);
          else { ri++; play(list[ri]); }
        }, "ph-primary");
        append(ctx.controls, nb);
        focusQuiet(nb);
      }
    }
    begin();
  };

  /* ===================================================== map-paint (ch 08) */
  // The 24 Santa Luz barangays (santa_luz_barangays.csv) with their dengue cases
  // from santa_luz_linelist.csv, as in chapter 08. Tile layout: two columns per
  // band, west to east down each pair. [name, band, column, row, population,
  // dengue cases, optional two-line label "line 1|line 2"]
  var BRGY = [
    ["San Pedro", "c", 0, 0, 7156, 18], ["Baybay", "c", 0, 1, 7579, 23], ["Dalampasigan", "c", 0, 2, 7403, 24, "Dalam-|pasigan"], ["Pantalan", "c", 0, 3, 8979, 19],
    ["Talaba", "c", 1, 0, 6688, 29], ["Buhangin", "c", 1, 1, 7037, 25], ["Laot", "c", 1, 2, 6367, 17], ["Wawa", "c", 1, 3, 7643, 19],
    ["Ilog", "r", 2, 0, 13411, 31], ["Tabing-Ilog", "r", 2, 1, 10417, 18, "Tabing-|Ilog"], ["Pampang", "r", 2, 2, 13214, 23], ["Poblacion", "r", 2, 3, 12288, 24],
    ["Santo Niño", "r", 3, 0, 10216, 23, "Santo|Niño"], ["San Isidro", "r", 3, 1, 11218, 23, "San|Isidro"], ["Bagong Silang", "r", 3, 2, 13127, 30, "Bagong|Silang"], ["Sapa", "r", 3, 3, 12173, 23],
    ["Bukid", "u", 4, 0, 4109, 0], ["Burol", "u", 4, 1, 4661, 5], ["Mataas na Lupa", "u", 4, 2, 3173, 3, "Mataas na|Lupa"], ["Kawayanan", "u", 4, 3, 5211, 5],
    ["San Roque", "u", 5, 0, 4145, 1, "San|Roque"], ["Maligaya", "u", 5, 1, 3288, 1], ["Bagong Pag-asa", "u", 5, 2, 3259, 2, "Bagong|Pag-asa"], ["Talahib", "u", 5, 3, 3238, 2]
  ];
  var BAND = { c: ["coastal", "沿海", "baybayin"], r: ["riverside", "河岸", "tabing-ilog"], u: ["upland", "山區", "kabundukan"] };
  var PALETTES = {
    seq: ["#fff4c2", "#fdd36f", "#f8a13c", "#e2552b", "#a50f24"],
    rainbow: ["#6a3d9a", "#1f78b4", "#33a02c", "#ffd92f", "#e31a1c"]
  };
  function breaks(values, method, k) {
    var v = values.slice().sort(function (a, b) { return a - b; });
    var out = [];
    if (method === "equal") {
      var lo = v[0], hi = v[v.length - 1];
      for (var i = 1; i < k; i++) out.push(lo + (hi - lo) * i / k);
    } else {
      for (var j = 1; j < k; j++) out.push(v[Math.min(v.length - 1, Math.round((v.length * j) / k))]);
    }
    return out;
  }
  function classOf(x, br) { var c = 0; while (c < br.length && x >= br[c]) c++; return c; }
  function darkFill(hex) {
    var r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);
    return 0.299 * r + 0.587 * g + 0.114 * b < 140;
  }

  WIDGETS["map-paint"] = function (ctx) {
    var title = L(["Paint the map", "幫地圖上色", "Kulayan ang mapa"]);
    var intro = L(["Dengue in Santa Luz's 24 barangays (the chapter 08 data, to 30 Sep). Change what is mapped, the class breaks and the colours — and watch the map's message change.",
      "Santa Luz 24 個 barangay 的登革熱（第 08 章的資料，至 9/30）。改變呈現的指標、分級方式與配色，看看地圖傳達的訊息如何改變。",
      "Dengue sa 24 barangay ng Santa Luz (ang datos ng kabanata 08, hanggang 30 Set). Palitan ang ipinapakita, ang class breaks at ang kulay — at panoorin kung paano nagbabago ang mensahe ng mapa."]);
    ctx.host.appendChild(shell(ctx, title, intro));
    var st, score, mission, firstTry, tiles, legendEl, msgEl, infoEl, missionEl, groups = {};
    function rate(b) { return (b[5] / b[4]) * 10000; }
    function topEqual() { var v = BRGY.map(value), br = breaks(v, "equal", 5); return v.filter(function (x) { return classOf(x, br) === 4; }).length; }
    function value(b) { return st.measure === "rate" ? rate(b) : b[5]; }
    function fmtV(x) { return st.measure === "rate" ? x.toFixed(1) : String(Math.round(x)); }
    var maxRate = BRGY.reduce(function (m, b) { return rate(b) > rate(m) ? b : m; });
    var maxCount = BRGY.reduce(function (m, b) { return b[5] > m[5] ? b : m; });
    function xpos(c) { return 24 + c * 58 + (c >= 3 ? 10 : 0); }
    function seg(key, opts) {
      var g = h("div", { class: "ph-seg", role: "group", "aria-label": L(opts.label) });
      opts.items.forEach(function (it) {
        var b = h("button", { type: "button", class: "ph-seg-btn", "aria-pressed": st[key] === it.v ? "true" : "false", onclick: function () {
          st[key] = it.v;
          Array.prototype.forEach.call(g.children, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
          paint();
        } }, L(it.t));
        g.appendChild(b);
      });
      groups[key] = g;
      return h("div", { class: "ph-seg-row" }, [h("span", { class: "ph-seg-label" }, L(opts.label)), g]);
    }
    function build() {
      st = { measure: "count", method: "equal", pal: "seq", sel: null };
      score = 0; mission = 0; firstTry = true;
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      ctx.setScore(0, 3);
      var kids = [
        s("rect", { x: 0, y: 0, width: 18, height: 224, class: "ph-sea" }),
        s("path", { d: "M4 20 q4 -4 8 0 M4 80 q4 -4 8 0 M4 140 q4 -4 8 0 M4 200 q4 -4 8 0", class: "ph-wave" }),
        s("path", { d: "M201 0 C 196 40, 207 70, 199 112 S 205 180, 200 224", class: "ph-river" })
      ];
      tiles = BRGY.map(function (b) {
        var x = xpos(b[2]), y = 4 + b[3] * 55;
        var rect = s("rect", { x: x, y: y, width: 54, height: 51, rx: 7, class: "ph-tile-bg" });
        var lines = (b[6] || b[0]).split("|");
        var name = s("text", { x: x + 27, y: y + (lines.length > 1 ? 14 : 20), class: "ph-tile-name", "text-anchor": "middle" },
          lines.length > 1 ? lines.map(function (ln, k) { return s("tspan", { x: x + 27, dy: k ? "9.5" : "0" }, ln); }) : b[0]);
        var val = s("text", { x: x + 27, y: y + 41, class: "ph-tile-val", "text-anchor": "middle" });
        var g = s("g", { class: "ph-tile", tabindex: "0", role: "button" }, [rect, name, val]);
        g.addEventListener("click", function () { choose(b, g); });
        g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choose(b, g); } });
        g.parts = { rect: rect, name: name, val: val };
        g.b = b;
        kids.push(g);
        return g;
      });
      kids.push(s("text", { x: 201, y: 236, class: "ph-tick", "text-anchor": "middle" }, "Marilag River"));
      var svgEl = s("svg", { viewBox: "0 0 382 242", class: "ph-map", role: "group", tabindex: "-1", focusable: "false", "aria-label": L(["Tile map of the 24 barangays of Santa Luz (left: coast, centre: river valley, right: uplands)", "Santa Luz 24 個 barangay 的方格地圖（左：沿海，中：河岸，右：山區）", "Tile map ng 24 barangay ng Santa Luz (kaliwa: baybayin, gitna: lambak ng ilog, kanan: kabundukan)"]) }, kids);
      roving(svgEl, ".ph-tile", { cols: 6 });
      legendEl = h("div", { class: "ph-map-legend" });
      msgEl = h("p", { class: "ph-map-msg" });
      infoEl = h("p", { class: "ph-map-info", "aria-live": "polite" }, L(["Tap a barangay for its numbers.", "點選 barangay 看數字。", "I-tap ang barangay para makita ang numero."]));
      missionEl = h("div", { class: "ph-mission" });
      var controls = h("div", { class: "ph-seg-wrap" }, [
        seg("measure", { label: ["Show", "顯示", "Ipakita"], items: [{ v: "count", t: ["Cases", "病例數", "Kaso"] }, { v: "rate", t: ["Rate per 10,000", "每 10,000 人侵襲率", "Rate bawat 10,000"] }] }),
        seg("method", { label: ["Classes", "分級", "Classes"], items: [{ v: "equal", t: ["Equal interval", "等距分級", "Equal interval"] }, { v: "quantile", t: ["Quantile", "分位數分級", "Quantile"] }] }),
        seg("pal", { label: ["Colours", "配色", "Kulay"], items: [{ v: "seq", t: ["Sequential", "單色漸層", "Sequential"] }, { v: "rainbow", t: ["Rainbow", "彩虹", "Rainbow"] }] })
      ]);
      append(ctx.body, [missionEl, controls, h("div", { class: "ph-map-wrap" }, svgEl), legendEl, infoEl, msgEl, h("p", { class: "ph-w-note" }, L(["Tile map, not to scale.", "方格示意地圖，非實際比例。", "Tile map, hindi eksaktong sukat."]))]);
      paint();
      showMission();
    }
    function paint() {
      var vals = BRGY.map(value);
      var br = breaks(vals, st.method, 5);
      var pal = PALETTES[st.pal];
      tiles.forEach(function (g, i) {
        var col = pal[classOf(vals[i], br)];
        g.parts.rect.setAttribute("fill", col);
        var dark = darkFill(col);
        g.parts.name.setAttribute("class", "ph-tile-name" + (dark ? " on-dark" : ""));
        g.parts.val.setAttribute("class", "ph-tile-val" + (dark ? " on-dark" : ""));
        g.parts.val.textContent = fmtV(vals[i]);
        g.setAttribute("aria-label", g.b[0] + ", " + L(BAND[g.b[1]]) + ": " + g.b[5] + " " + L(["cases", "例", "kaso"]) + ", " + g.b[4].toLocaleString("en") + " " + L(["people", "人", "tao"]) + ", " + rate(g.b).toFixed(1) + " " + L(["per 10,000", "每 10,000 人", "bawat 10,000"]));
        g.classList.toggle("is-selected", st.sel === g.b);
      });
      clear(legendEl);
      var min = Math.min.apply(null, vals), max = Math.max.apply(null, vals);
      var edges = [min].concat(br, [max]);
      for (var c = 0; c < 5; c++) {
        var n = vals.filter(function (v) { return classOf(v, br) === c; }).length;
        legendEl.appendChild(h("span", { class: "ph-legend-item" }, [h("i", { style: "background:" + pal[c] }), fmtV(edges[c]) + "–" + fmtV(edges[c + 1]) + " (" + n + ")"]));
      }
      var msgs = [];
      msgs.push(st.measure === "count" ?
        fmt(L(["Counts: {p} looks worst — but it is also the biggest barangay ({n} people). Counts mostly map where people live.", "病例數：{p} 看起來最嚴重——但它也是人口最多的 barangay（{n} 人）。病例數地圖大多只反映人住在哪裡。", "Bilang: {p} ang mukhang pinakamalala — pero ito rin ang pinakamalaking barangay ({n} tao). Kadalasan, kung saan nakatira ang tao lang ang ipinapakita ng bilang."]), { p: maxCount[0], n: maxCount[4].toLocaleString("en") }) :
        L(["Rates: the coastal band stands out, led by Talaba and Buhangin — the most cases are by the river, but the highest risk is on the coast.", "侵襲率：沿海帶最突出，以 Talaba 和 Buhangin 居首——病例最多的是河岸，風險最高的卻是沿海。", "Rates: tumatampok ang baybayin, nangunguna ang Talaba at Buhangin — nasa tabing-ilog ang pinakamaraming kaso, pero nasa baybayin ang pinakamataas na panganib."]));
      msgs.push(st.method === "equal" ?
        L(["Equal interval: every class spans the same range, so only the truly high barangays reach the darkest colour.", "等距分級：每一級的數值範圍相同，只有真正很高的 barangay 會塗上最深的顏色。", "Equal interval: pare-pareho ang saklaw ng bawat class, kaya ang talagang mataas lang ang nasa pinakamadilim na kulay."]) :
        L(["Quantile: every colour holds about the same number of barangays, so small differences can look large.", "分位數分級：每個顏色的 barangay 數量大致相同，因此小差異也可能看起來很大。", "Quantile: halos pare-pareho ang bilang ng barangay sa bawat kulay, kaya puwedeng magmukhang malaki ang maliit na pagkakaiba."]));
      if (st.pal === "rainbow") msgs.push(L(["Rainbow: is yellow more or less than green? Readers cannot tell without the legend, and red–green is hard for colour-blind readers.", "彩虹配色：黃色比綠色多還是少？沒有圖例讀者無從判斷，而紅綠色對色覺異常者也很難分辨。", "Rainbow: mas marami ba ang dilaw kaysa berde? Hindi masasabi nang walang legend, at mahirap ang pula–berde sa mga color-blind."]));
      clear(msgEl);
      append(msgEl, [h("strong", null, L(["What this map says: ", "這張地圖在說：", "Sinasabi ng mapang ito: "])), msgs.join(" ")]);
    }
    var MISSIONS = [
      ["Mission 1: tap the barangay where a resident had the HIGHEST RISK of dengue.", "任務 1：點選居民得到登革熱「風險最高」的 barangay。", "Mission 1: i-tap ang barangay kung saan PINAKAMATAAS ANG PANGANIB ng dengue para sa isang residente."],
      ["Mission 2: try both classifications. Which one gives every colour about the same number of barangays?", "任務 2：兩種分級都試試看。哪一種讓每個顏色的 barangay 數量大致相同？", "Mission 2: subukan ang dalawang classification. Alin ang nagbibigay ng halos parehong bilang ng barangay sa bawat kulay?"],
      ["Mission 3: which colours let the Local Health Board read low → high without looking at the legend?", "任務 3：哪一種配色讓地方衛生委員會不用看圖例也能讀出低 → 高？", "Mission 3: aling kulay ang makatutulong sa Local Health Board na mabasa ang mababa → mataas nang hindi tumitingin sa legend?"]
    ];
    function showMission() {
      clear(missionEl);
      firstTry = true;
      var dots = h("span", { class: "ph-dots", "aria-hidden": "true" }, MISSIONS.map(function (_, k) { return h("i", { class: k < mission ? "done" : k === mission ? "now" : "" }); }));
      append(missionEl, [dots, h("p", { class: "ph-task", tabindex: "-1" }, L(MISSIONS[mission]))]);
      if (mission === 1 || mission === 2) {
        var opts = mission === 1 ?
          [{ label: L(["Equal interval", "等距分級", "Equal interval"]), value: "equal" }, { label: L(["Quantile", "分位數分級", "Quantile"]), value: "quantile" }] :
          [{ label: L(["Sequential", "單色漸層", "Sequential"]), value: "seq" }, { label: L(["Rainbow", "彩虹", "Rainbow"]), value: "rainbow" }];
        var right = mission === 1 ? "quantile" : "seq";
        var ch = choiceButtons(opts, function (o, buttons, btn) {
          var ok = o.value === right;
          lockChoices(buttons, right, btn);
          if (ok) score++;
          ctx.setScore(score, 3);
          ctx.say(ok ? "good" : "bad", mission === 1 ?
            fmt(L(["Quantile classes split the 24 barangays into five groups of about 5 (count them in the legend). Equal interval splits the range of values instead — with these numbers only {n} barangays reach the top class.", "分位數分級把 24 個 barangay 分成五組、每組約 5 個（數數圖例）。等距分級則是平分數值範圍——以這組數字，只有 {n} 個 barangay 進入最高級。", "Hinahati ng quantile ang 24 barangay sa limang grupo na tig-~5 (bilangin sa legend). Ang equal interval naman ay hinahati ang saklaw ng values — {n} barangay lang dito ang umabot sa pinakamataas na class."]), { n: topEqual() }) :
            L(["A sequential palette goes from light to dark, so 'darker = more' needs no legend. Rainbow colours have no natural order.", "單色漸層由淺到深，「越深＝越多」不需要圖例。彩虹色沒有自然的順序。", "Mula maliwanag hanggang madilim ang sequential palette, kaya 'mas madilim = mas marami' kahit walang legend. Walang natural na pagkakasunod ang rainbow."]),
            ok ? goodWord() : badWord());
          if (ok) ctx.celebrate(false);
          nextMission();
        });
        missionEl.appendChild(ch);
      }
    }
    function nextMission() {
      clear(ctx.controls);
      var last = mission === MISSIONS.length - 1;
      var b = ctx.button(last ? "★ " + U("seeScore") : U("next") + " →", function () {
        if (last) endScreen(ctx, score, 3, build, ["Map rates, not counts; choose class breaks on purpose and say which; use a light-to-dark palette. And credit the boundaries you draw.", "地圖要呈現率而不是病例數；有意識地選擇分級方式並註明；使用由淺到深的配色。別忘了註明邊界資料來源。", "I-mapa ang rate, hindi bilang; piliin nang sadya ang class breaks at sabihin kung alin; gumamit ng maliwanag-hanggang-madilim na palette. At banggitin ang pinagmulan ng boundaries."]);
        else { mission++; showMission(); clear(ctx.controls); focusQuiet(missionEl.querySelector(".ph-task")); }
      }, "ph-primary");
      append(ctx.controls, b);
      focusQuiet(b);
    }
    function choose(b, g) {
      st.sel = b;
      paint();
      clear(infoEl);
      append(infoEl, [h("strong", null, b[0]), " (" + L(BAND[b[1]]) + "): " + b[5] + " " + L(["cases", "例", "kaso"]) + " ÷ " + b[4].toLocaleString("en") + " " + L(["people", "人", "tao"]) + " × 10,000 = ", h("strong", null, rate(b).toFixed(1)), " " + L(["per 10,000", "每 10,000 人", "bawat 10,000"])]);
      if (mission !== 0 || ctx.controls.firstChild) return;
      if (b === maxRate && st.measure === "rate") {
        if (firstTry) score++;
        ctx.setScore(score, 3);
        ctx.say("good", fmt(L(["{b}: {r} per 10,000 — the highest risk, though {p} has more cases. Risk needs a denominator.", "{b}：每 10,000 人 {r}——風險最高，雖然 {p} 的病例數更多。風險一定要有分母。", "{b}: {r} bawat 10,000 — pinakamataas ang panganib, kahit mas marami ang kaso ng {p}. Kailangan ng denominator ang risk."]), { b: b[0], r: rate(b).toFixed(1), p: maxCount[0] }), goodWord());
        ctx.celebrate(false);
        nextMission();
      } else if (b === maxRate) {
        firstTry = false;
        ctx.say("info", L(["Right barangay — now switch 'Show' to 'Rate per 10,000' to prove it, and tap it again.", "選對了——現在把「顯示」切換到「每 10,000 人侵襲率」證明一下，再點一次。", "Tamang barangay — ngayon gawing 'Rate bawat 10,000' ang 'Ipakita' para patunayan, at i-tap ulit."]));
      } else {
        firstTry = false;
        ctx.say("bad", b === maxCount ?
          fmt(L(["{b} has the most cases, but also {n} people. Risk = cases ÷ people. Try 'Rate per 10,000'.", "{b} 病例最多，但人口也有 {n} 人。風險＝病例數 ÷ 人口。試試「每 10,000 人侵襲率」。", "Pinakamarami ang kaso sa {b}, pero {n} din ang tao. Risk = kaso ÷ tao. Subukan ang 'Rate bawat 10,000'."]), { b: b[0], n: b[4].toLocaleString("en") }) :
          L(["Not the highest. Switch to rates and compare the numbers on the tiles.", "不是最高的。切換到侵襲率，比較方格上的數字。", "Hindi ito ang pinakamataas. Lumipat sa rates at ikumpara ang numero sa tiles."]), badWord());
      }
    }
    build();
  };

  /* ============================================= lamok-patrol (ch 08/09) */
  var WATER = "#4aa3df";
  var ICONS = {
    tyre: function () { return [s("ellipse", { cx: 32, cy: 38, rx: 26, ry: 16, fill: "#2b2b2b" }), s("ellipse", { cx: 32, cy: 37, rx: 14, ry: 7, fill: WATER }), wig(26, 36), wig(36, 38)]; },
    tyrePlant: function () { return [s("ellipse", { cx: 32, cy: 42, rx: 26, ry: 14, fill: "#2b2b2b" }), s("ellipse", { cx: 32, cy: 40, rx: 14, ry: 6, fill: "#7a5230" }), s("path", { d: "M32 40 C30 28 22 24 18 22 M32 40 C34 26 42 22 48 20 M32 40 V18", stroke: "#3c9a3c", "stroke-width": 3, fill: "none" })]; },
    coconut: function () { return [s("path", { d: "M8 30 A24 20 0 0 0 56 30 Z", fill: "#7b4a22" }), s("ellipse", { cx: 32, cy: 30, rx: 24, ry: 6, fill: "#f3e2c0" }), s("ellipse", { cx: 32, cy: 30, rx: 19, ry: 4, fill: WATER }), wig(30, 30)]; },
    vase: function () { return [s("path", { d: "M22 28 h20 l-3 28 h-14 z", fill: "#c06c84" }), s("ellipse", { cx: 32, cy: 28, rx: 10, ry: 3, fill: WATER }), s("path", { d: "M32 28 V10 M28 28 L22 14 M36 28 L42 12", stroke: "#3c9a3c", "stroke-width": 2.5 }), s("circle", { cx: 32, cy: 9, r: 4, fill: "#fff" }), s("circle", { cx: 22, cy: 13, r: 3.5, fill: "#FCD116" }), s("circle", { cx: 42, cy: 11, r: 3.5, fill: "#CE1126" })]; },
    drumOpen: function () { return [s("rect", { x: 14, y: 16, width: 36, height: 42, rx: 3, fill: "#2a7ab8" }), s("ellipse", { cx: 32, cy: 16, rx: 18, ry: 5, fill: WATER, stroke: "#1b5b8a", "stroke-width": 2 }), wig(28, 16), s("path", { d: "M14 30 h36 M14 44 h36", stroke: "#1b5b8a", "stroke-width": 2 })]; },
    drumLid: function () { return [s("rect", { x: 14, y: 16, width: 36, height: 42, rx: 3, fill: "#2a7ab8" }), s("ellipse", { cx: 32, cy: 15, rx: 20, ry: 6, fill: "#d9d9d9", stroke: "#888", "stroke-width": 2 }), s("rect", { x: 28, y: 8, width: 8, height: 5, rx: 2, fill: "#888" }), s("path", { d: "M14 30 h36 M14 44 h36", stroke: "#1b5b8a", "stroke-width": 2 })]; },
    bucket: function () { return [s("path", { d: "M16 22 h32 l-4 32 h-24 z", fill: "#e76f51" }), s("ellipse", { cx: 32, cy: 22, rx: 16, ry: 4, fill: WATER }), s("path", { d: "M16 22 C 16 4, 48 4, 48 22", stroke: "#555", "stroke-width": 2, fill: "none" }), wig(30, 22)]; },
    bucketDown: function () { return [s("path", { d: "M20 22 h24 l4 32 h-32 z", fill: "#e76f51" }), s("rect", { x: 14, y: 54, width: 36, height: 3, fill: "#a0522d" })]; },
    bottle: function () { return [s("path", { d: "M27 10 h10 v8 l5 7 v31 h-20 v-31 l5 -7 z", fill: "#9ad0a8", stroke: "#3c7d52", "stroke-width": 1.5 }), s("rect", { x: 23, y: 30, width: 18, height: 25, fill: WATER, opacity: 0.85 }), wig(29, 40)]; },
    bottlesDown: function () { return [s("rect", { x: 8, y: 40, width: 48, height: 18, rx: 2, fill: "#c48a3f" }), [14, 26, 38].map(function (x) { return s("path", { d: "M" + x + " 40 v-18 l3 -4 h6 l3 4 v18 z", transform: "rotate(180 " + (x + 6) + " 31)", fill: "#9ad0a8", stroke: "#3c7d52", "stroke-width": 1.2 }); })]; },
    saucer: function () { return [s("path", { d: "M22 18 h20 l-3 20 h-14 z", fill: "#b5651d" }), s("path", { d: "M24 18 C 20 6, 30 4, 32 14 C 34 4, 44 6, 40 18", fill: "#3c9a3c" }), s("ellipse", { cx: 32, cy: 46, rx: 22, ry: 7, fill: "#a0522d" }), s("ellipse", { cx: 32, cy: 44, rx: 17, ry: 4, fill: WATER })]; },
    saucerSand: function () { return [s("path", { d: "M22 18 h20 l-3 20 h-14 z", fill: "#b5651d" }), s("path", { d: "M24 18 C 20 6, 30 4, 32 14 C 34 4, 44 6, 40 18", fill: "#3c9a3c" }), s("ellipse", { cx: 32, cy: 46, rx: 22, ry: 7, fill: "#a0522d" }), s("ellipse", { cx: 32, cy: 44, rx: 17, ry: 4, fill: "#e9c46a" })]; },
    pond: function () { return [s("ellipse", { cx: 32, cy: 40, rx: 28, ry: 14, fill: "#8d6e63" }), s("ellipse", { cx: 32, cy: 39, rx: 24, ry: 10, fill: WATER }), s("path", { d: "M20 38 q6 -5 12 0 q-6 5 -12 0 z M32 38 l5 -3 v6 z", fill: "#f4a261" }), s("path", { d: "M38 44 q5 -4 10 0 q-5 4 -10 0 z M48 44 l4 -3 v6 z", fill: "#f4a261" })]; },
    can: function () { return [s("rect", { x: 20, y: 22, width: 24, height: 32, rx: 2, fill: "#b0b7bf" }), s("rect", { x: 20, y: 32, width: 24, height: 10, fill: "#CE1126" }), s("ellipse", { cx: 32, cy: 22, rx: 12, ry: 4, fill: WATER, stroke: "#8a9299", "stroke-width": 2 })]; },
    cup: function () { return [s("path", { d: "M18 30 h28 l-4 26 h-20 z", transform: "rotate(-12 32 42)", fill: "#f1f1f1", stroke: "#999", "stroke-width": 1.5 }), s("ellipse", { cx: 31, cy: 31, rx: 13, ry: 3.5, transform: "rotate(-12 32 42)", fill: WATER })]; },
    gutter: function () { return [s("path", { d: "M2 22 L62 10 V18 L2 30 Z", fill: "#a63d40" }), s("path", { d: "M2 30 L62 18 V26 C 62 32, 2 44, 2 38 Z", fill: "#9aa5ad" }), s("path", { d: "M8 35 L56 25", stroke: WATER, "stroke-width": 4 }), s("path", { d: "M14 33 q3 -6 7 -2 M38 28 q4 -6 8 -2", stroke: "#6b8e23", "stroke-width": 3, fill: "none" })]; },
    bamboo: function () { return [s("rect", { x: 22, y: 20, width: 20, height: 38, fill: "#9bbf4c" }), s("path", { d: "M22 40 h20", stroke: "#6d8b2f", "stroke-width": 2 }), s("ellipse", { cx: 32, cy: 20, rx: 10, ry: 4, fill: WATER, stroke: "#6d8b2f", "stroke-width": 2 }), wig(30, 20)]; }
  };
  function wig(x, y) { return s("path", { d: "M" + x + " " + y + " q1.5 -2 3 0 t3 0", stroke: "#1b3a57", "stroke-width": 1.2, fill: "none", class: "ph-larva" }); }
  var LAMOK_ITEMS = {
    tyre: { icon: "tyre", breed: true, n: ["Old tyre", "舊輪胎", "Lumang gulong"], e: ["Tyres hold rainwater for weeks: a favourite Aedes nursery. Drain, cover or recycle them.", "輪胎會積雨水好幾週，是斑蚊最愛的孳生地。倒掉積水、覆蓋或回收。", "Matagal nag-iipon ng ulan ang gulong: paboritong pugad ng Aedes. Patuyuin, takpan o i-recycle."] },
    tyrePlant: { icon: "tyrePlant", breed: false, n: ["Tyre planter with soil", "填土的輪胎花盆", "Gulong na taniman, may lupa"], e: ["Filled with soil, so no standing water.", "裝滿了土，不會積水。", "Puno ng lupa, kaya walang naiipong tubig."] },
    coconut: { icon: "coconut", breed: true, n: ["Coconut shell", "椰子殼", "Bao ng niyog"], e: ["A small cupful of water is enough for Aedes eggs. Turn shells over or throw them away.", "一小杯水就足夠斑蚊產卵。把椰子殼倒扣或丟掉。", "Sapat na ang kaunting tubig para sa itlog ng Aedes. Itaob o itapon ang bao."] },
    vase: { icon: "vase", breed: true, n: ["Flower vase", "花瓶", "Plorera"], e: ["Change vase water at least once a week and scrub the sides, where eggs stick.", "花瓶水至少每週換一次，並刷洗瓶壁——蟲卵會黏在那裡。", "Palitan ang tubig ng plorera kahit minsan sa isang linggo at kuskusin ang gilid, kung saan dumidikit ang itlog."] },
    drumOpen: { icon: "drumOpen", breed: true, n: ["Open water drum", "沒加蓋的儲水桶", "Drum na walang takip"], e: ["Stored water without a lid breeds mosquitoes. Cover it tightly.", "沒加蓋的儲水會孳生蚊子，要蓋緊。", "Nagpaparami ng lamok ang nakaimbak na tubig na walang takip. Takpan nang mahigpit."] },
    drumLid: { icon: "drumLid", breed: false, n: ["Covered water drum", "加蓋的儲水桶", "Drum na may takip"], e: ["Tightly covered: mosquitoes cannot reach the water.", "蓋緊了，蚊子碰不到水。", "Mahigpit ang takip: hindi maaabot ng lamok ang tubig."] },
    bucket: { icon: "bucket", breed: true, n: ["Pail of rainwater", "裝了雨水的水桶", "Baldeng may tubig-ulan"], e: ["Use it, empty it or cover it — never leave it sitting.", "用掉、倒掉或蓋起來——別放著不管。", "Gamitin, itapon ang tubig o takpan — huwag hayaang nakatiwangwang."] },
    bucketDown: { icon: "bucketDown", breed: false, n: ["Pail turned upside down", "倒扣的水桶", "Baldeng nakataob"], e: ["Turned over: it cannot collect water.", "倒扣著，不會積水。", "Nakataob: hindi makaiipon ng tubig."] },
    bottle: { icon: "bottle", breed: true, n: ["Open bottle with water", "裝水的開口瓶", "Bukas na boteng may tubig"], e: ["Empty it and store bottles upside down.", "倒掉積水，把瓶子倒放。", "Itapon ang tubig at itaob ang mga bote."] },
    bottlesDown: { icon: "bottlesDown", breed: false, n: ["Bottles stored upside down", "倒放的瓶子", "Mga boteng nakataob"], e: ["Stored upside down: exactly right.", "倒放收納，完全正確。", "Nakataob ang pagkakatago: tama!"] },
    saucer: { icon: "saucer", breed: true, n: ["Plant saucer with water", "積水的花盆底盤", "Platito ng paso na may tubig"], e: ["Saucers under pots collect water. Empty them weekly or fill them with sand.", "花盆底盤會積水。每週倒掉，或填入沙子。", "Nag-iipon ng tubig ang platito sa ilalim ng paso. Itapon linggu-linggo o lagyan ng buhangin."] },
    saucerSand: { icon: "saucerSand", breed: false, n: ["Plant saucer filled with sand", "填沙的花盆底盤", "Platitong may buhangin"], e: ["Sand keeps water from pooling. Good idea!", "沙子讓水無法積存，好方法！", "Pinipigilan ng buhangin ang pag-ipon ng tubig. Magandang ideya!"] },
    pond: { icon: "pond", breed: false, n: ["Pond with fish", "有魚的池塘", "Pond na may isda"], e: ["Fish such as guppies eat mosquito larvae — leave this one alone.", "孔雀魚等魚類會吃孑孓——這個不用動。", "Kinakain ng isda gaya ng guppy ang kiti-kiti — hayaan na ito."] },
    can: { icon: "can", breed: true, n: ["Empty can", "空罐", "Lata"], e: ["Discarded cans fill with rain. Crush them and put them in the trash.", "丟棄的空罐會積雨水。壓扁後丟進垃圾桶。", "Napupuno ng ulan ang mga itinapong lata. Pitpitin at ilagay sa basurahan."] },
    cup: { icon: "cup", breed: true, n: ["Plastic cup", "塑膠杯", "Plastik na baso"], e: ["Even a cup is enough. Pick up litter after the flood.", "連一個杯子都夠蚊子孳生。洪水後要撿拾垃圾。", "Kahit baso ay sapat na. Pulutin ang basura pagkatapos ng baha."] },
    gutter: { icon: "gutter", breed: true, n: ["Clogged roof gutter", "堵塞的屋簷排水槽", "Baradong alulod"], e: ["Leaves block the gutter and water sits on the roof. Clean gutters after storms.", "落葉堵住排水槽，水就積在屋頂上。暴風雨後要清理排水槽。", "Binabarahan ng dahon ang alulod kaya naiipon ang tubig. Linisin ang alulod pagkatapos ng bagyo."] },
    bamboo: { icon: "bamboo", breed: true, n: ["Cut bamboo stump", "竹子斷口", "Pinutol na kawayan"], e: ["Cut bamboo holds water in each node. Cut below the node or fill it with soil.", "竹子斷口的竹節會積水。在竹節下方切斷，或填土。", "Nag-iipon ng tubig ang pinutol na kawayan. Putulin sa ibaba ng buko o lagyan ng lupa."] }
  };
  var LAMOK_SCENES = [
    { title: ["Aling Nena's yard, Barangay Ilog", "Aling Nena 家的院子，Barangay Ilog", "Bakuran ni Aling Nena, Barangay Ilog"], items: ["tyre", "coconut", "vase", "drumOpen", "bucket", "saucer", "bottle", "drumLid", "bucketDown", "saucerSand", "tyrePlant", "pond"] },
    { title: ["Santa Luz Central School after the flood", "洪水過後的 Santa Luz 中央小學", "Santa Luz Central School pagkatapos ng baha"], items: ["tyre", "can", "cup", "gutter", "bamboo", "drumOpen", "bucket", "bottle", "bottlesDown", "drumLid", "bucketDown", "pond"] }
  ];

  WIDGETS["lamok-patrol"] = function (ctx) {
    var title = L(["Lamok patrol: search and destroy!", "Lamok 巡邏隊：找出並清除孳生源！", "Lamok patrol: hanapin at sirain!"]);
    var intro = L(["Tap every place where Aedes mosquitoes can breed before time runs out. Leave the safe ones alone.", "在時間結束前，點出所有斑蚊可能孳生的地方。安全的就別動。", "I-tap ang bawat lugar na puwedeng pamugaran ng lamok na Aedes bago maubos ang oras. Huwag galawin ang ligtas."]);
    ctx.host.appendChild(shell(ctx, title, intro));
    var relaxed = ctx.has("ph-lamok-relaxed");
    var si, points, totalPts, found, timer, left, running, missedAll;
    var SECONDS = 45;
    function intro0() {
      si = 0; totalPts = 0; missedAll = [];
      stop();
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      ctx.setScore(0);
      var relaxBtn = h("button", { type: "button", class: "ph-seg-btn", "aria-pressed": relaxed ? "true" : "false", onclick: function () {
        relaxed = !relaxed; relaxBtn.setAttribute("aria-pressed", relaxed ? "true" : "false");
      } }, "🐢 " + L(["Relaxed mode (no timer)", "輕鬆模式（不計時）", "Relaxed mode (walang timer)"]));
      append(ctx.body, h("div", { class: "ph-end" }, [talaStar(72),
        h("p", null, L(["Two scenes, 45 seconds each. +10 for every breeding site, −5 for disturbing a safe one, and a bonus for time left.", "兩個場景，各 45 秒。找到孳生源 +10，動到安全的 −5，剩餘時間另有加分。", "Dalawang eksena, 45 segundo bawat isa. +10 sa bawat breeding site, −5 kapag ginalaw ang ligtas, at bonus sa natirang oras."])),
        relaxBtn]));
      var go = ctx.button("🦟 " + L(["Start patrol", "開始巡邏", "Simulan ang patrol"]), function () { scene(0); }, "ph-primary");
      append(ctx.controls, go);
    }
    function stop() { if (timer) ctx.stopEvery(timer); timer = null; running = false; }
    function scene(k) {
      si = k; points = 0; found = 0; left = SECONDS; running = true;
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      var sc = LAMOK_SCENES[k];
      var items = shuffle(sc.items).map(function (id) { return { id: id, def: LAMOK_ITEMS[id], done: false }; });
      var need = items.filter(function (it) { return it.def.breed; }).length;
      var bar = h("span", { class: "ph-timebar-fill" });
      var timeText = h("span", { class: "ph-time-text" });
      var foundText = h("span", null);
      var hud = h("div", { class: "ph-hud" }, [
        h("span", { class: "ph-timebar", role: "timer", "aria-label": L(["Time left", "剩餘時間", "Natitirang oras"]) }, bar), timeText, foundText
      ]);
      var grid = h("div", { class: "ph-lamok-grid", role: "group", "aria-label": L(sc.title) });
      items.forEach(function (it) {
        var icon = s("svg", { viewBox: "0 0 64 64", class: "ph-icon", "aria-hidden": "true", focusable: "false" }, ICONS[it.def.icon]());
        var b = h("button", { type: "button", class: "ph-spot", "aria-label": L(it.def.n), onclick: function () { hit(it, b); } }, [icon, h("span", { class: "ph-spot-name" }, L(it.def.n))]);
        it.btn = b;
        grid.appendChild(b);
      });
      roving(grid, ".ph-spot", { cols: 3 });
      append(ctx.body, [h("p", { class: "ph-progress" }, U("roundOf", { i: k + 1, n: LAMOK_SCENES.length })), h("p", { class: "ph-task", tabindex: "-1" }, h("strong", null, "🏡 " + L(sc.title))), hud, grid]);
      function hudUpdate() {
        foundText.textContent = "🦟 " + found + " / " + need + " · " + points + " " + L(["pts", "分", "puntos"]);
        if (relaxed) { timeText.textContent = "🐢"; bar.style.width = "100%"; return; }
        timeText.textContent = left + " s";
        bar.style.width = (100 * left / SECONDS) + "%";
        hud.classList.toggle("is-hurry", left <= 10);
      }
      function hit(it, b) {
        if (!running || it.done) return;
        if (it.def.breed) {
          it.done = true; found++; points += 10;
          b.classList.add("is-cleared");
          b.setAttribute("aria-label", L(it.def.n) + " — " + L(["cleared", "已清除", "nalinis na"]));
          b.appendChild(h("span", { class: "ph-splash", "aria-hidden": "true" }, L(["Cleared!", "清除！", "Tinaob!"])));
          ctx.say("good", L(it.def.e), goodWord());
        } else {
          points = Math.max(0, points - 5);
          b.classList.remove("ph-shake"); void b.offsetWidth; b.classList.add("ph-shake");
          ctx.say("bad", L(it.def.e), L(["Safe one!", "這個是安全的！", "Ligtas iyan!"]));
        }
        hudUpdate();
        ctx.setScore(totalPts + points);
        if (found === need) end(true);
      }
      function end(all) {
        stop();
        items.forEach(function (it) { it.btn.disabled = true; if (it.def.breed && !it.done) { it.btn.classList.add("is-missed"); missedAll.push(it); } });
        var bonus = all && !relaxed ? Math.floor(left / 3) : 0;
        points += bonus;
        totalPts += points;
        ctx.setScore(totalPts);
        var msg = all ? fmt(L(["All {n} breeding sites cleared! Time bonus +{b}.", "{n} 個孳生源全部清除！時間加分 +{b}。", "Nalinis lahat ng {n} breeding site! Time bonus +{b}."]), { n: need, b: bonus }) :
          fmt(L(["Time's up — {f} of {n} found. The missed ones are marked; read why they matter.", "時間到——找到 {f} / {n} 個。漏掉的已標出，看看為什麼它們重要。", "Ubos na ang oras — {f} sa {n} ang nakita. Minarkahan ang hindi nakita; basahin kung bakit mahalaga sila."]), { f: found, n: need });
        ctx.say(all ? "party" : "bad", msg, all ? goodWord() : null);
        if (all) ctx.celebrate(true);
        clear(ctx.controls);
        var last = si === LAMOK_SCENES.length - 1;
        var nb = ctx.button(last ? "★ " + L(["Finish patrol", "完成巡邏", "Tapusin ang patrol"]) : U("nextRound") + " →", function () { if (last) finale(); else scene(si + 1); }, "ph-primary");
        append(ctx.controls, nb);
        focusQuiet(nb);
      }
      hudUpdate();
      ctx.setScore(totalPts);
      if (!relaxed) {
        timer = ctx.every(function () {
          if (!running) return;
          left--;
          hudUpdate();
          if (left <= 0) end(false);
        }, 1000);
      }
      focusQuiet(grid.querySelector(".ph-spot"));
    }
    function finale() {
      ctx.hush(); clear(ctx.body); clear(ctx.controls);
      var fours = [
        ["Search and destroy breeding sites", "搜尋並清除孳生源", "Search and destroy — hanapin at sirain ang pinamumugaran ng lamok"],
        ["Secure self-protection (long sleeves, repellent)", "做好自我防護（長袖、防蚊液）", "Secure self-protection (mahabang manggas, repellent)"],
        ["Seek early consultation for fever", "發燒及早就醫", "Seek early consultation kapag nilagnat"],
        ["Support fogging only in outbreak hotspots", "只在疫情熱區配合噴藥", "Suportahan ang fogging sa outbreak hotspots lamang"]
      ];
      var box = h("div", { class: "ph-end", tabindex: "-1" }, [talaStar(88),
        h("p", { class: "ph-end-score" }, fmt(L(["Patrol complete: {p} points!", "巡邏完成：{p} 分！", "Tapos ang patrol: {p} puntos!"]), { p: totalPts })),
        h("p", null, L(["Today you did the first S. Remember all four:", "今天你完成了第一個 S。四個 S 都要記得：", "Ginawa mo ngayon ang unang S. Tandaan ang apat:"])),
        h("ol", { class: "ph-4s" }, fours.map(function (f) { return h("li", null, L(f)); })),
        missedAll.length ? h("p", { class: "ph-hint" }, L(["Missed this time: ", "這次漏掉的：", "Hindi nakita ngayon: "]) + missedAll.map(function (it) { return L(it.def.n); }).join(", ")) : null
      ]);
      append(ctx.body, box);
      ctx.announce(box.textContent);
      if (!missedAll.length) ctx.celebrate(true);
      append(ctx.controls, ctx.button("↻ " + U("again"), intro0, "ph-primary"));
      focusQuiet(box);
    }
    intro0();
  };

  /* =========================================================== mounting */
  function widgetName(el) {
    var cls = (el.getAttribute("class") || "").split(/\s+/);
    for (var i = 0; i < cls.length; i++) {
      if (cls[i].indexOf("ph-game-") === 0 && cls[i] !== "ph-game-ready") return cls[i].slice(8);
    }
    return null;
  }
  function mount(el) {
    var name = widgetName(el);
    if (!name || !WIDGETS[name]) return;
    LI = LANGS[detectLang()] || 0;
    var ctx = makeCtx(el, name);
    el.__phGame = ctx;
    instances.push(ctx);
    try {
      var res = WIDGETS[name](ctx);
      if (res === false || !ctx.root) { destroyCtx(ctx); el.__phGame = false; return; }
      el.classList.add("ph-game-ready");
    } catch (err) {
      destroyCtx(ctx);
      el.__phGame = false; // keep the fallback; do not retry on every mutation
      if (W.console && W.console.warn) W.console.warn("[ph-games] could not start " + name + ":", err);
    }
  }
  function sweep() {
    instances.slice().forEach(function (ctx) {
      var gone = !D.documentElement.contains(ctx.host);
      var detached = !gone && ctx.root && ctx.root.parentNode !== ctx.host;
      if (gone || detached) {
        destroyCtx(ctx);
        if (detached) ctx.host.__phGame = null;
      }
    });
  }
  function scan() {
    sweep();
    var nodes = D.querySelectorAll(".ph-game");
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.__phGame === false) continue;
      if (el.__phGame && el.__phGame.alive) {
        if (!el.classList.contains("ph-game-ready")) el.classList.add("ph-game-ready");
        continue;
      }
      mount(el);
    }
    hooks();
  }

  /* ------------------------------------------- page hooks: reveal, stat */
  var io = null;
  function observer() {
    if (io || !("IntersectionObserver" in W)) return io;
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        if (en.target.__phReveal) { en.target.classList.add("ph-revealed"); en.target.classList.remove("ph-reveal-pending"); }
        if (en.target.__phStat) countUp(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.1 });
    return io;
  }
  function inView(el) {
    var r = el.getBoundingClientRect();
    return r.top < (W.innerHeight || 800) && r.bottom > 0;
  }
  /* ph.css already reveals `.ph-reveal` with scroll-driven CSS where the
     browser supports it; this JS reveal only fills in elsewhere. */
  var cssReveal = !!(W.CSS && W.CSS.supports && W.CSS.supports("animation-timeline: view()"));
  function hooks() {
    if (reduced() || !observer()) return;
    var rev = cssReveal ? [] : D.querySelectorAll(".ph-reveal");
    for (var i = 0; i < rev.length; i++) {
      var el = rev[i];
      if (el.__phReveal) continue;
      el.__phReveal = true;
      if (inView(el)) continue; // never hide what the reader already sees
      el.classList.add("ph-reveal-pending");
      io.observe(el);
    }
    // `.ph-stat`: count up each card title (the style guide's tiles), or the
    // element's own first number when it has no cards.
    var stats = D.querySelectorAll(".ph-stat");
    for (var j = 0; j < stats.length; j++) {
      var titles = stats[j].querySelectorAll(".myst-card-title");
      var targets = titles.length ? titles : [stats[j]];
      for (var k = 0; k < targets.length; k++) {
        if (targets[k].__phStat) continue;
        targets[k].__phStat = true;
        io.observe(targets[k]);
      }
    }
  }
  /** Animate the first number in the element's text from 0, in place. */
  function countUp(el) {
    var walker = D.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var node = null, m = null;
    while (walker.nextNode()) {
      m = /(\d[\d,]*)(\.\d+)?/.exec(walker.currentNode.nodeValue);
      if (m) { node = walker.currentNode; break; }
    }
    if (!node) return;
    var original = node.nodeValue;
    var target = parseFloat((m[1] + (m[2] || "")).replace(/,/g, ""));
    var decimals = m[2] ? m[2].length - 1 : 0;
    var commas = m[1].indexOf(",") >= 0;
    if (!isFinite(target) || target === 0) return;
    var start = null, dur = 1200;
    function fmtN(x) {
      var str = x.toFixed(decimals);
      if (commas) { var p = str.split("."); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ","); str = p.join("."); }
      return str;
    }
    function frame(t) {
      if (!D.documentElement.contains(node)) return;
      if (start == null) start = t;
      var k = Math.min(1, (t - start) / dur);
      var eased = 1 - Math.pow(1 - k, 3);
      if (k >= 1) { node.nodeValue = original; return; }
      node.nodeValue = original.slice(0, m.index) + fmtN(target * eased) + original.slice(m.index + m[0].length);
      W.requestAnimationFrame(frame);
    }
    W.requestAnimationFrame(frame);
  }

  /* ------------------------------------------------------------ start up */
  var started = false, pending = false;
  function schedule() {
    if (!started || pending) return;
    pending = true;
    W.setTimeout(function () { pending = false; scan(); }, 60);
  }
  function start() {
    if (started) return;
    started = true;
    scan();
    if ("MutationObserver" in W) new MutationObserver(schedule).observe(D.body, { childList: true, subtree: true });
    ["pushState", "replaceState"].forEach(function (k) {
      var orig = W.history[k];
      if (typeof orig !== "function") return;
      W.history[k] = function () { var r = orig.apply(this, arguments); schedule(); return r; };
    });
    W.addEventListener("popstate", schedule);
  }

  W.PHGames = {
    version: "1.0.0",
    scan: function () { if (!started) start(); else scan(); },
    widgets: function () { return Object.keys(WIDGETS); },
    instances: function () { return instances.length; },
    celebrate: function (el) {
      var host = el && el.closest ? el.closest(".ph-game") : null;
      if (host && host.__phGame) celebrate(host.__phGame, true);
    }
  };

  if (typeof W.epiWhenHydrated === "function") {
    W.epiWhenHydrated(start);
  } else {
    // epi-site.js missing (e.g. a test page): wait for load, then a beat.
    var later = function () { W.setTimeout(start, 300); };
    if (D.readyState === "complete") later();
    else W.addEventListener("load", later);
  }
})();
