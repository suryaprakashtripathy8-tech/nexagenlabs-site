/* NexagenLabs site script: no dependencies */
(function () {
  "use strict";
  var GA_ID = document.documentElement.getAttribute("data-ga") || "";

  /* Mobile menu */
  var btn = document.querySelector(".menu-btn"), links = document.querySelector(".nav-links");
  if (btn && links) btn.addEventListener("click", function () {
    var open = links.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });

  /* Reveal on scroll */
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add("in"); });

  /* Hero C1V1 calculator */
  var calc = document.getElementById("c1v1");
  if (calc) {
    var f = { 2: { M: 1, mM: 1e-3, "µM": 1e-6, nM: 1e-9 }, v: { L: 1, mL: 1e-3, "µL": 1e-6 } };
    var q = function (id) { return calc.querySelector("#" + id); };
    var fmt = function (x) {
      if (!isFinite(x) || x <= 0) return "…";
      if (x >= 1) return x.toFixed(3).replace(/\.?0+$/, "") + " L";
      if (x >= 1e-3) return (x * 1e3).toFixed(3).replace(/\.?0+$/, "") + " mL";
      return (x * 1e6).toFixed(2).replace(/\.?0+$/, "") + " µL";
    };
    var run = function () {
      var c1 = parseFloat(q("c1").value) * f[2][q("c1u").value];
      var c2 = parseFloat(q("c2").value) * f[2][q("c2u").value];
      var v2 = parseFloat(q("v2").value) * f.v[q("v2u").value];
      var out = q("out"), sub = q("sub");
      if (!(c1 > 0 && c2 > 0 && v2 > 0)) { out.textContent = "…"; sub.textContent = "Enter positive values."; return; }
      if (c2 > c1) { out.textContent = "Check C₂"; sub.textContent = "Final concentration can't exceed the stock."; return; }
      var v1 = (c2 * v2) / c1;
      out.textContent = "V₁ = " + fmt(v1);
      sub.textContent = "Take " + fmt(v1) + " of stock, then add diluent to " + fmt(v2) + " (" + fmt(v2 - v1) + " diluent).";
    };
    calc.addEventListener("input", run); calc.addEventListener("change", run); run();
  }

  /* Directory filter */
  var dir = document.getElementById("directory");
  if (dir) {
    var items = dir.querySelectorAll("[data-cat]"), input = document.getElementById("dir-q"),
      chips = document.querySelectorAll(".chip[data-filter]"), empty = document.getElementById("dir-empty"), cat = "all";
    var apply = function () {
      var t = (input.value || "").trim().toLowerCase(), shown = 0;
      items.forEach(function (it) {
        var ok = (cat === "all" || it.getAttribute("data-cat").indexOf(cat) > -1) && (!t || it.textContent.toLowerCase().indexOf(t) > -1);
        it.style.display = ok ? "" : "none"; if (ok) shown++;
      });
      empty.style.display = shown ? "none" : "block";
    };
    input.addEventListener("input", apply);
    chips.forEach(function (c) { c.addEventListener("click", function () {
      chips.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
      c.setAttribute("aria-pressed", "true"); cat = c.getAttribute("data-filter"); apply();
    }); });
  }

  /* Netlify forms via fetch (graceful: works without JS too) */
  document.querySelectorAll("form[data-netlify]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status"), b = form.querySelector("button[type=submit]");
      if (b) b.disabled = true;
      fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(new FormData(form)).toString() })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          if (status) status.textContent = form.getAttribute("data-ok") || "Thanks: received.";
          var rv = form.getAttribute("data-reveal"); if (rv) { var el = document.getElementById(rv); if (el) { el.hidden = false; el.focus && el.focus(); } }
          track("generate_lead", { form: form.getAttribute("name") });
        })
        .catch(function () { if (status) status.textContent = "Something went wrong. Please try again."; })
        .finally(function () { if (b) b.disabled = false; });
    });
  });

  /* Outbound click tracking (Amazon, tools) */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-ev]");
    if (a) track(a.getAttribute("data-ev"), { label: a.getAttribute("data-label") || a.href });
  });

  /* Consent + GA4 (loads only after explicit accept) */
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function loadGA() {
    if (!GA_ID || window.__ga) return; window.__ga = 1;
    var s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID; document.head.appendChild(s);
    window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date()); gtag("config", GA_ID, { anonymize_ip: true });
  }
  function track(name, params) { if (window.gtag) window.gtag("event", name, params || {}); }
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

  /* ---------------- Guide calculator widgets ---------------- */
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
  function out(w, main, sub) { w.querySelector(".w-out").textContent = main; var s = w.querySelector(".w-sub"); if (s) s.innerHTML = sub || ""; }
  var W = {
    molarity: function (w) {
      var pre = val(w, "preset"); if (pre && w.__pre !== pre) { w.querySelector("[name=mw]").value = pre; } w.__pre = pre;
      var M = num(w, "m") * CU[val(w, "mu")], V = num(w, "v") * VU[val(w, "vu")], mw = num(w, "mw");
      var g = M * V * mw; out(w, "Weigh " + mass(g), "Dissolve in less than " + vol(V) + ", then make up to " + vol(V) + ".");
    },
    c1v1: function (w) {
      var c1 = num(w, "c1") * CU[val(w, "c1u")], c2 = num(w, "c2") * CU[val(w, "c2u")], v2 = num(w, "v2") * VU[val(w, "v2u")];
      if (!(c1 > 0 && c2 > 0 && v2 > 0)) return out(w, "…", "Enter positive values.");
      if (c2 > c1) return out(w, "Check C₂", "The final concentration can't exceed the stock.");
      var v1 = c2 * v2 / c1, warn = v1 < 1e-6 ? "<br><b>Under 1 µL:</b> do an intermediate dilution first." : "";
      out(w, "V₁ = " + vol(v1), "Take " + vol(v1) + " of stock and add " + vol(v2 - v1) + " diluent." + warn);
    },
    serial: function (w) {
      var c0 = num(w, "c0") * CU[val(w, "cu")], f = num(w, "f"), n = Math.min(12, Math.max(1, Math.round(num(w, "n")))), t = num(w, "t");
      if (!(c0 > 0 && f > 1 && t > 0)) return out(w, "…", "Enter a start concentration, a factor above 1 and a transfer volume.");
      var dil = t * (f - 1), rows = "";
      for (var i = 1; i <= n; i++) rows += "<tr><td>" + i + "</td><td>1:" + trim(Math.pow(f, i), 0) + "</td><td>" + conc(c0 / Math.pow(f, i)) + "</td></tr>";
      out(w, "Transfer " + trim(t, 1) + " µL into " + trim(dil, 1) + " µL diluent per tube", "<table><thead><tr><th>Tube</th><th>Total dilution</th><th>Concentration</th></tr></thead><tbody>" + rows + "</tbody></table>");
    },
    pbs: function (w) {
      var V = num(w, "v") * VU[val(w, "vu")], x = num(w, "x"), hyd = parseFloat(val(w, "hyd"));
      if (!(V > 0 && x > 0)) return out(w, "…", "");
      var k = V * x, na2 = 1.44 * hyd / 141.96;
      var r = [["NaCl", 8.0], ["KCl", 0.2], ["Na₂HPO₄", na2], ["KH₂PO₄", 0.24]].map(function (a) { return "<tr><td>" + a[0] + "</td><td>" + mass(a[1] * k) + "</td></tr>"; }).join("");
      out(w, trim(x, 1) + "X PBS, " + vol(V), "<table><thead><tr><th>Component</th><th>Weigh</th></tr></thead><tbody>" + r + "</tbody></table>Dissolve in about 80% of the volume, check pH 7.4, then make up to volume.");
    },
    percent: function (w) {
      var pc = num(w, "p"), V = num(w, "v"), type = val(w, "type"), mw = num(w, "mw"), d = num(w, "d");
      if (!(pc > 0 && V > 0)) return out(w, "…", "");
      if (type === "wv") {
        var g = pc / 100 * V, M = mw > 0 ? pc * 10 / mw : NaN;
        out(w, "Weigh " + mass(g), "Make up to " + trim(V, 1) + " mL." + (mw > 0 ? " That is " + conc(M) + "." : " Add an MW to see molarity."));
      } else if (type === "vv") {
        out(w, "Measure " + trim(pc / 100 * V, 2) + " mL", "Then make up to " + trim(V, 1) + " mL with diluent. Do not just add the remainder; volumes do not add exactly.");
      } else {
        var M2 = mw > 0 && d > 0 ? pc * d * 10 / mw : NaN;
        out(w, isFinite(M2) ? conc(M2) : "…", "Molarity of a % w/w reagent needs density (g/mL) and MW.");
      }
    },
    dna: function (w) {
      var c = num(w, "c"), L = num(w, "len"), per = parseFloat(val(w, "type"));
      if (!(c > 0 && L > 0)) return out(w, "…", "");
      var nM = c * 1e6 / (L * per), cp = c * 6.022e23 / (L * per * 1e9);
      out(w, trim(nM, 2) + " nM", "Copies per µL: <b>" + sci(cp) + "</b>");
    }
  };
  document.querySelectorAll("[data-widget]").forEach(function (w) {
    var fn = W[w.getAttribute("data-widget")]; if (!fn) return;
    var run = function () { try { fn(w); } catch (e) { } };
    w.addEventListener("input", run); w.addEventListener("change", run); run();
  });

  /* ---------------- Site search (Ctrl/Cmd+K or /) ---------------- */
  var dlg = document.getElementById("search"), sInput, sList, idx = null, sel = 0, hits = [];
  function openSearch() {
    if (!dlg) return; dlg.hidden = false; document.body.style.overflow = "hidden";
    sInput = dlg.querySelector("input"); sList = dlg.querySelector(".s-results"); sInput.value = ""; sInput.focus();
    if (!idx) fetch("/search-index.json").then(function (r) { return r.json(); }).then(function (j) { idx = j; render(); }); else render();
  }
  function closeSearch() { if (!dlg) return; dlg.hidden = true; document.body.style.overflow = ""; }
  function score(it, terms) {
    var t = it.t.toLowerCase(), b = (it.t + " " + it.d + " " + (it.x || "")).toLowerCase(), s = 0;
    for (var i = 0; i < terms.length; i++) { var q = terms[i]; if (b.indexOf(q) < 0) return 0; s += t.indexOf(q) > -1 ? 3 : 1; if (t.indexOf(q) === 0) s += 2; }
    return s + (it.w || 0);
  }
  function render() {
    if (!idx) return;
    var q = (sInput.value || "").trim().toLowerCase(), terms = q.split(/\s+/).filter(Boolean);
    hits = terms.length ? idx.map(function (it) { return [score(it, terms), it]; }).filter(function (a) { return a[0] > 0; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 12).map(function (a) { return a[1]; })
      : idx.filter(function (it) { return it.f; });
    sel = 0;
    sList.innerHTML = hits.length ? hits.map(function (it, i) {
      return '<a class="s-item' + (i === 0 ? " on" : "") + '" href="' + it.u + '"' + (/^https?:/.test(it.u) ? ' target="_blank" rel="noopener"' : "") + '><span class="s-k">' + it.k + '</span><span class="s-t">' + it.t.replace(/</g, "&lt;") + '</span><span class="s-d">' + it.d.replace(/</g, "&lt;") + "</span></a>";
    }).join("") : '<p class="s-empty">No matches. Try "buffer", "dilution" or a book title.</p>';
  }
  function move(d) {
    var items = sList.querySelectorAll(".s-item"); if (!items.length) return;
    items[sel].classList.remove("on"); sel = (sel + d + items.length) % items.length; items[sel].classList.add("on"); items[sel].scrollIntoView({ block: "nearest" });
  }
  if (dlg) {
    document.querySelectorAll("[data-open-search]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); openSearch(); }); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.closest("[data-close-search]")) closeSearch(); });
    dlg.querySelector("input").addEventListener("input", render);
    document.addEventListener("keydown", function (e) {
      var typing = /INPUT|TEXTAREA|SELECT/.test((e.target.tagName || "")) && e.target !== (dlg && dlg.querySelector("input"));
      if ((e.key === "k" && (e.metaKey || e.ctrlKey)) || (e.key === "/" && !typing && dlg.hidden)) { e.preventDefault(); openSearch(); return; }
      if (dlg.hidden) return;
      if (e.key === "Escape") closeSearch();
      else if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") { var a = sList.querySelectorAll(".s-item")[sel]; if (a) { e.preventDefault(); a.click(); } }
    });
  }
})();
