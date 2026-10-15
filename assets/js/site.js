/* NexagenLabs site script — no dependencies */
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
      if (!isFinite(x) || x <= 0) return "—";
      if (x >= 1) return x.toFixed(3).replace(/\.?0+$/, "") + " L";
      if (x >= 1e-3) return (x * 1e3).toFixed(3).replace(/\.?0+$/, "") + " mL";
      return (x * 1e6).toFixed(2).replace(/\.?0+$/, "") + " µL";
    };
    var run = function () {
      var c1 = parseFloat(q("c1").value) * f[2][q("c1u").value];
      var c2 = parseFloat(q("c2").value) * f[2][q("c2u").value];
      var v2 = parseFloat(q("v2").value) * f.v[q("v2u").value];
      var out = q("out"), sub = q("sub");
      if (!(c1 > 0 && c2 > 0 && v2 > 0)) { out.textContent = "—"; sub.textContent = "Enter positive values."; return; }
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
          if (status) status.textContent = form.getAttribute("data-ok") || "Thanks — received.";
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
})();
