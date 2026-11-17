/* NexagenLabs site script: no dependencies */
(function () {
  "use strict";
  var root = document.documentElement;
  var GA_ID = root.getAttribute("data-ga") || "";
  var PREVIEW = !!window.NX_PREVIEW;
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function track(name, params) { if (window.gtag) window.gtag("event", name, params || {}); }

  /* ---------------- Theme ---------------- */
  function setTheme(t) { root.setAttribute("data-theme", t); store("nx-theme", t); var m = $('meta[name="theme-color"]'); if (m) m.content = t === "light" ? "#f4f6fa" : "#070c17"; }
  function toggleTheme() { setTheme(root.getAttribute("data-theme") === "light" ? "dark" : "light"); }
  $$("[data-theme-toggle]").forEach(function (b) { b.addEventListener("click", toggleTheme); });

  /* ---------------- Mobile menu ---------------- */
  var menuBtn = $(".menu-btn"), links = $(".nav-links");
  function closeMenu() { if (links) links.classList.remove("open"); if (menuBtn) menuBtn.setAttribute("aria-expanded", "false"); }
  if (menuBtn && links) {
    menuBtn.addEventListener("click", function () { var open = links.classList.toggle("open"); menuBtn.setAttribute("aria-expanded", open ? "true" : "false"); });
    links.addEventListener("click", function (e) { if (e.target.closest("a")) closeMenu(); });
  }

  /* ---------------- Calculators ---------------- */
  var CU = { M: 1, mM: 1e-3, "µM": 1e-6, nM: 1e-9 }, VU = { L: 1, mL: 1e-3, "µL": 1e-6 };
  function num(w, n) { var el = w.querySelector("[name=" + n + "]"); return el ? parseFloat(el.value) : NaN; }
  function val(w, n) { var el = w.querySelector("[name=" + n + "]"); return el ? el.value : ""; }
  function trim(x, d) { return (+x.toFixed(d)).toString(); }
  function mass(g) {
    if (!(g > 0) || !isFinite(g)) return "…";
    if (g >= 1) return trim(g, 3) + " g"; if (g >= 1e-3) return trim(g * 1e3, 2) + " mg"; return trim(g * 1e6, 1) + " µg";
  }
  function vol(l) {
    if (!(l > 0) || !isFinite(l)) return "…";
    if (l >= 1) return trim(l, 3) + " L"; if (l >= 1e-3) return trim(l * 1e3, 3) + " mL"; return trim(l * 1e6, 2) + " µL";
  }
  function conc(m) {
    if (!(m > 0) || !isFinite(m)) return "…";
    if (m >= 1) return trim(m, 3) + " M"; if (m >= 1e-3) return trim(m * 1e3, 3) + " mM"; if (m >= 1e-6) return trim(m * 1e6, 3) + " µM"; return trim(m * 1e9, 3) + " nM";
  }
  function sci(x) { if (!isFinite(x) || x <= 0) return "…"; var e = Math.floor(Math.log10(x)); return (x / Math.pow(10, e)).toFixed(2) + " × 10<sup>" + e + "</sup>"; }
  function out(w, label, main, sub) {
    w.querySelector(".readout .k").textContent = label;
    w.querySelector(".w-out").innerHTML = main; var s = w.querySelector(".w-sub"); if (s) s.innerHTML = sub || "";
  }
  /* The tube drawing shows how much of the final volume is stock. */
  function tube(w, frac) {
    var st = w.querySelector(".tube .stock"), pct = w.querySelector(".w-pct"); if (!st) return;
    var ok = frac > 0 && frac <= 1, h = ok ? Math.max(3, 98 * frac) : 0;
    st.setAttribute("y", 128 - h); st.setAttribute("height", h);
    if (pct) pct.textContent = ok ? (frac >= 0.01 ? trim(frac * 100, 1) : "<1") + "% stock" : "";
  }
  var W = {
    molarity: function (w) {
      var pre = val(w, "preset"); if (pre && w.__pre !== pre) { w.querySelector("[name=mw]").value = pre; } w.__pre = pre;
      var M = num(w, "m") * CU[val(w, "mu")], V = num(w, "v") * VU[val(w, "vu")], mw = num(w, "mw");
      if (!(M > 0 && V > 0 && mw > 0)) return out(w, "Mass to weigh", "…", "Enter a molarity, a volume and a molecular weight.");
      out(w, "Mass to weigh", mass(M * V * mw), "Dissolve in less than " + vol(V) + ", then make up to " + vol(V) + ".");
    },
    c1v1: function (w) {
      var c1 = num(w, "c1") * CU[val(w, "c1u")], c2 = num(w, "c2") * CU[val(w, "c2u")], v2 = num(w, "v2") * VU[val(w, "v2u")];
      if (!(c1 > 0 && c2 > 0 && v2 > 0)) { tube(w, 0); return out(w, "Volume of stock to add", "…", "Enter positive values."); }
      if (c2 > c1) { tube(w, 0); return out(w, "Volume of stock to add", "Check C<sub>2</sub>", "The final concentration can't be higher than the stock."); }
      var v1 = c2 * v2 / c1, warn = v1 < 1e-6 ? " <b>Under 1 µL:</b> make an intermediate dilution first." : "";
      tube(w, v1 / v2);
      out(w, "Volume of stock to add", "V<sub>1</sub> = " + vol(v1), "Take " + vol(v1) + " of stock and add " + vol(v2 - v1) + " of diluent to reach " + vol(v2) + "." + warn);
    },
    serial: function (w) {
      var c0 = num(w, "c0") * CU[val(w, "cu")], f = num(w, "f"), n = Math.min(12, Math.max(1, Math.round(num(w, "n")))), t = num(w, "t");
      if (!(c0 > 0 && f > 1 && t > 0)) return out(w, "Per tube", "…", "Enter a start concentration, a factor above 1 and a transfer volume.");
      var dil = t * (f - 1), rows = "";
      for (var i = 1; i <= n; i++) rows += "<tr><td>" + i + "</td><td>1:" + trim(Math.pow(f, i), 0) + "</td><td>" + conc(c0 / Math.pow(f, i)) + "</td></tr>";
      out(w, "Per tube", trim(t, 1) + " µL into " + trim(dil, 1) + " µL", "<table><thead><tr><th>Tube</th><th>Total dilution</th><th>Concentration</th></tr></thead><tbody>" + rows + "</tbody></table>");
    },
    pbs: function (w) {
      var V = num(w, "v") * VU[val(w, "vu")], x = num(w, "x"), hyd = parseFloat(val(w, "hyd"));
      if (!(V > 0 && x > 0)) return out(w, "Recipe", "…", "Enter a volume and a strength.");
      var k = V * x, na2 = 1.44 * hyd / 141.96;
      var r = [["NaCl", 8.0], ["KCl", 0.2], ["Na₂HPO₄", na2], ["KH₂PO₄", 0.24]].map(function (a) { return "<tr><td>" + a[0] + "</td><td>" + mass(a[1] * k) + "</td></tr>"; }).join("");
      out(w, "Recipe", trim(x, 1) + "X PBS, " + vol(V), "<table><thead><tr><th>Component</th><th>Weigh</th></tr></thead><tbody>" + r + "</tbody></table>Dissolve in about 80% of the volume, check pH 7.4, then make up to volume.");
    },
    percent: function (w) {
      var pc = num(w, "p"), V = num(w, "v"), type = val(w, "type"), mw = num(w, "mw"), d = num(w, "d");
      if (!(pc > 0 && V > 0)) return out(w, "Result", "…", "Enter a percent and a volume.");
      if (type === "wv") {
        var g = pc / 100 * V, M = mw > 0 ? pc * 10 / mw : NaN;
        out(w, "Mass to weigh", mass(g), "Make up to " + trim(V, 1) + " mL." + (mw > 0 ? " That is " + conc(M) + "." : " Add an MW to see molarity."));
      } else if (type === "vv") {
        out(w, "Volume to measure", trim(pc / 100 * V, 2) + " mL", "Then make up to " + trim(V, 1) + " mL with diluent. Do not just add the remainder; volumes do not add exactly.");
      } else {
        var M2 = mw > 0 && d > 0 ? pc * d * 10 / mw : NaN;
        out(w, "Molarity", isFinite(M2) ? conc(M2) : "…", "The molarity of a % w/w reagent needs its density (g/mL) and MW.");
      }
    },
    dna: function (w) {
      var c = num(w, "c"), L = num(w, "len"), per = parseFloat(val(w, "type"));
      if (!(c > 0 && L > 0)) return out(w, "Molar concentration", "…", "Enter a concentration and a length.");
      var nM = c * 1e6 / (L * per), cp = c * 6.022e23 / (L * per * 1e9);
      out(w, "Molar concentration", trim(nM, 2) + " nM", "Copies per µL: <b>" + sci(cp) + "</b>");
    }
  };
  $$("[data-widget]").forEach(function (w) {
    var fn = W[w.getAttribute("data-widget")]; if (!fn) return;
    var run = function () { try { fn(w); } catch (e) { } };
    w.addEventListener("input", run); w.addEventListener("change", run); run();
  });
  /* Tabbed console */
  $$("[data-console]").forEach(function (c) {
    var tabs = $$("[role=tab]", c), full = $(".console-full", c);
    function pick(tab, focus) {
      tabs.forEach(function (t) { t.setAttribute("aria-selected", t === tab ? "true" : "false"); t.tabIndex = t === tab ? 0 : -1; });
      $$("[data-widget]", c).forEach(function (w) {
        var on = w.getAttribute("data-widget") === tab.getAttribute("data-tab"); w.hidden = !on;
        if (on && full) full.href = w.getAttribute("data-full");
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (t, i) {
      t.tabIndex = i === 0 ? 0 : -1;
      t.addEventListener("click", function () { pick(t); track("console_tab", { label: t.getAttribute("data-tab") }); });
      t.addEventListener("keydown", function (e) {
        if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
        e.preventDefault(); pick(tabs[(i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length], true);
      });
    });
  });

  /* ---------------- Finder ---------------- */
  $$("[data-finder]").forEach(function (f) {
    var jobs = $$(".job", f);
    jobs.forEach(function (j) { j.addEventListener("click", function () {
      jobs.forEach(function (x) { x.setAttribute("aria-pressed", x === j ? "true" : "false"); });
      $$("[data-job-out]", f).forEach(function (o) { o.hidden = o.getAttribute("data-job-out") !== j.getAttribute("data-job"); });
      track("finder_pick", { label: j.textContent });
    }); });
  });

  /* ---------------- Directory filter ---------------- */
  var dir = document.getElementById("directory");
  if (dir) {
    var items = $$("[data-cat]", dir), groups = $$("[data-group]", dir), input = document.getElementById("dir-q"),
      chips = $$(".chip[data-filter]"), empty = document.getElementById("dir-empty"), cat = "all";
    var apply = function () {
      var t = (input.value || "").trim().toLowerCase(), shown = 0;
      items.forEach(function (it) {
        var ok = (cat === "all" || it.getAttribute("data-cat").indexOf(cat) > -1) && (!t || it.textContent.toLowerCase().indexOf(t) > -1);
        it.hidden = !ok; if (ok) shown++;
      });
      groups.forEach(function (g) { g.hidden = !g.querySelector("[data-cat]:not([hidden])"); });
      empty.style.display = shown ? "none" : "block";
    };
    input.addEventListener("input", apply);
    chips.forEach(function (c) { c.addEventListener("click", function () {
      chips.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
      c.setAttribute("aria-pressed", "true"); cat = c.getAttribute("data-filter"); apply();
    }); });
  }

  /* ---------------- Netlify forms via fetch (works without JS too) ---------------- */
  $$("form[data-netlify]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status"), b = form.querySelector("button[type=submit]");
      function done() {
        form.reset();
        if (status) { status.textContent = form.getAttribute("data-ok") || "Received."; status.classList.add("ok"); }
        var rv = form.getAttribute("data-reveal"); if (rv) { var el = document.getElementById(rv); if (el) { el.hidden = false; el.focus && el.focus(); } }
        track("generate_lead", { form: form.getAttribute("name") });
      }
      if (PREVIEW) { if (status) { status.textContent = "Preview only: this form starts working once the site is on Netlify."; status.classList.add("ok"); } return; }
      if (b) b.disabled = true;
      fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(new FormData(form)).toString() })
        .then(function (r) { if (!r.ok) throw new Error(r.status); done(); })
        .catch(function () { if (status) { status.classList.remove("ok"); status.textContent = "That didn't send. Check your connection and try again."; } })
        .finally(function () { if (b) b.disabled = false; });
    });
  });

  /* ---------------- Outbound click tracking ---------------- */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-ev]");
    if (a) track(a.getAttribute("data-ev"), { label: a.getAttribute("data-label") || a.href });
  });

  /* ---------------- Consent + GA4 (loads only after explicit accept) ---------------- */
  function loadGA() {
    if (!GA_ID || window.__ga) return; window.__ga = 1;
    var s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID; document.head.appendChild(s);
    window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date()); gtag("config", GA_ID, { anonymize_ip: true });
  }
  var banner = document.getElementById("consent");
  if (GA_ID && banner) {
    var c = store("nx-consent");
    if (c === "yes") loadGA(); else if (c !== "no") banner.classList.add("show");
    banner.addEventListener("click", function (e) {
      var v = e.target.getAttribute && e.target.getAttribute("data-consent");
      if (!v) return; store("nx-consent", v); banner.classList.remove("show"); if (v === "yes") loadGA();
    });
  }
  var reopen = document.getElementById("cookie-settings");
  if (reopen && banner) reopen.addEventListener("click", function (e) { e.preventDefault(); banner.classList.add("show"); });
  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();

  /* ---------------- Search and commands (Ctrl/Cmd+K or /) ---------------- */
  var dlg = document.getElementById("search"), sInput, sList, idx = window.NX_IDX || null, sel = 0, hits = [];
  var ACTIONS = [{ t: "Switch theme", d: "Toggle between dark and light", k: "Action", run: toggleTheme, x: "dark light mode theme", f: 1 }];
  var ORDER = ["BenchMate", "VeriHelix", "Site", "Guide", "Free guide", "Certificate", "Book", "Page", "Action", "Section", "FAQ"];
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;"); }
  function openSearch() {
    if (!dlg) return; dlg.hidden = false; document.body.style.overflow = "hidden";
    sInput = dlg.querySelector("input"); sList = dlg.querySelector(".s-results"); sInput.value = ""; sInput.focus();
    if (!idx) fetch("/search-index.json").then(function (r) { return r.json(); }).then(function (j) { idx = j; render(); }).catch(function () { idx = []; render(); }); else render();
  }
  function closeSearch() { if (!dlg) return; dlg.hidden = true; document.body.style.overflow = ""; }
  function score(it, terms) {
    var t = it.t.toLowerCase(), b = (it.t + " " + it.d + " " + (it.x || "")).toLowerCase(), s = 0;
    for (var i = 0; i < terms.length; i++) { var q = terms[i]; if (b.indexOf(q) < 0) return 0; s += t.indexOf(q) > -1 ? 3 : 1; if (t.indexOf(q) === 0) s += 2; }
    return s + (it.w || 0);
  }
  function render() {
    if (!idx) return;
    var all = ACTIONS.concat(idx), q = (sInput.value || "").trim().toLowerCase(), terms = q.split(/\s+/).filter(Boolean);
    hits = terms.length ? all.map(function (it) { return [score(it, terms), it]; }).filter(function (a) { return a[0] > 0; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 14).map(function (a) { return a[1]; })
      : all.filter(function (it) { return it.f; });
    /* group by kind, keeping the best-ranked kind first when searching */
    var kinds = [];
    hits.forEach(function (h) { if (kinds.indexOf(h.k) < 0) kinds.push(h.k); });
    if (!terms.length) kinds.sort(function (a, b) { return ORDER.indexOf(a) - ORDER.indexOf(b); });
    var ordered = [], htmlOut = "";
    kinds.forEach(function (k) {
      htmlOut += '<div class="s-group">' + esc(k === "Page" ? "Pages" : k === "Action" ? "Actions" : k) + "</div>";
      hits.filter(function (h) { return h.k === k; }).forEach(function (it) {
        var i = ordered.push(it) - 1, ext = it.u && /^https?:/.test(it.u);
        var inner = '<span class="s-t">' + esc(it.t) + '</span><span class="s-d">' + esc(it.d) + '</span><span class="s-k">' + (ext ? "Opens in a new tab" : "") + "</span>";
        htmlOut += it.run ? '<button type="button" class="s-item" data-i="' + i + '">' + inner + "</button>"
          : '<a class="s-item" data-i="' + i + '" href="' + it.u + '"' + (ext ? ' target="_blank" rel="noopener"' : "") + ">" + inner + "</a>";
      });
    });
    hits = ordered; sel = 0;
    sList.innerHTML = hits.length ? htmlOut : '<p class="s-empty">Nothing matches "' + esc(q) + '". Try "buffer", "dilution", "citation" or a book title.</p>';
    mark();
  }
  function mark() { $$(".s-item", sList).forEach(function (el, i) { el.classList.toggle("on", i === sel); }); }
  function move(d) { var n = hits.length; if (!n) return; sel = (sel + d + n) % n; mark(); var el = $$(".s-item", sList)[sel]; if (el) el.scrollIntoView({ block: "nearest" }); }
  function go(i) { var it = hits[i]; if (!it) return; if (it.run) { it.run(); closeSearch(); return true; } closeSearch(); return false; }
  if (dlg) {
    $$("[data-open-search]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); openSearch(); }); });
    dlg.addEventListener("click", function (e) {
      if (e.target === dlg || e.target.closest("[data-close-search]")) return closeSearch();
      var it = e.target.closest(".s-item"); if (it) go(+it.getAttribute("data-i"));
    });
    dlg.querySelector("input").addEventListener("input", render);
    document.addEventListener("keydown", function (e) {
      var typing = /INPUT|TEXTAREA|SELECT/.test((e.target.tagName || "")) && e.target !== dlg.querySelector("input");
      if ((e.key === "k" && (e.metaKey || e.ctrlKey)) || (e.key === "/" && !typing && dlg.hidden)) { e.preventDefault(); openSearch(); return; }
      if (dlg.hidden) return;
      if (e.key === "Escape") closeSearch();
      else if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") { var el = $$(".s-item", sList)[sel]; if (el) { e.preventDefault(); el.click(); } }
    });
  }

  /* ---------------- Preview bundle: every page lives in one file, routed on the hash ---------------- */
  if (PREVIEW) {
    var pages = $$("[data-page]"), current = null;
    var show = function (scrollTo) {
      var id = (location.hash || "#home").slice(1), pg = pages.filter(function (p) { return p.getAttribute("data-page") === id; })[0];
      if (!pg) {
        var target = current && id ? current.querySelector("#" + (window.CSS && CSS.escape ? CSS.escape(id) : id)) : null;
        if (target) { target.scrollIntoView(); return; }
        if (current) return; pg = pages[0];
      }
      pages.forEach(function (p) { p.hidden = p !== pg; }); current = pg;
      document.title = pg.getAttribute("data-title");
      var act = pg.getAttribute("data-active");
      $$(".nav-links a").forEach(function (a) { if (act && a.getAttribute("href") === "#" + act) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current"); });
      var el = scrollTo ? pg.querySelector("#" + scrollTo) : null;
      if (el) el.scrollIntoView(); else window.scrollTo(0, 0);
    };
    var pendingScroll = null;
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[href^='#']"); if (!a) return;
      pendingScroll = a.getAttribute("data-scroll");
      if (a.getAttribute("href") === location.hash) { e.preventDefault(); show(pendingScroll); pendingScroll = null; }
    });
    window.addEventListener("hashchange", function () { show(pendingScroll); pendingScroll = null; });
    show();
  }
})();
