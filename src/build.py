#!/usr/bin/env python3
"""Static site generator for nexagenlabs.com. No dependencies.

  python3 src/build.py                 -> public/   (what Netlify publishes)
  NX_PREVIEW=1 python3 src/build.py    -> preview/  (one-file bundle for offline review)
"""
import json, os, re, shutil, html, hashlib
from datetime import date
from data import (SITE, BM, VH, BENCHMATE_TOOLS, VERIHELIX_TOOLS, VERIHELIX_GROUPS, PROPERTIES, BOOKS, CREDENTIALS,
                  FREE_BOOKS, FREE_SERIES, PROFILES, JOBS, BM_CERTS, VH_CERTS)
from guides import GUIDES

PREVIEW = os.environ.get("NX_PREVIEW") == "1"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "preview" if PREVIEW else "public")
U = SITE["url"]
TODAY = date.today().isoformat()
def _h(rel):
    return hashlib.md5(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()[:10]
CSS_V = _h("assets/css/site.css")
JS_V = _h("assets/js/site.js")
PAGES = []      # (path, priority) for the sitemap
RENDERED = []   # (path, title, body) for the preview bundle
e = html.escape
AUTHOR = SITE["founder"]

# ------------------------------------------------------------------ icons
ICONS = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "ext": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 "down": '<path d="M12 4v12M6 11l6 6 6-6M5 20h14"/>',
 "seal": '<circle cx="12" cy="9" r="6"/><path d="M9.5 9l1.8 1.8L14.8 7.3M8.5 14L7 22l5-3 5 3-1.5-8"/>',
}
def icon(name, cls=""):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" class="{cls}">{ICONS[name]}</svg>'
EXT = icon("ext", "ext-ico")
ARROW = icon("arrow")

LOGO = '<img class="brand-mark" src="/assets/img/logo-mark-96.webp" alt="" width="34" height="34">'
KIT = "/assets/kit/nexagenlabs-bench-starter-kit.pdf"
NAV = [("/tools", "Tools"), ("/benchmate", "BenchMate"), ("/verihelix", "VeriHelix"), ("/books/", "Books"), ("/guides/", "Guides"), ("/certification", "Free Certification"), ("/about", "About")]

def book_by(slug):
    return next(b for b in BOOKS if b["slug"] == slug)

# ------------------------------------------------------------------ JSON-LD helpers
SAME_AS = [u for _, u in PROFILES]
ORG = {"@type": "Organization", "@id": U + "/#org", "name": "NexagenLabs", "alternateName": ["Nexagen Labs", "NexaGenLabs", "Nexagenlabs", "nexagenlabs.com"], "url": U + "/",
       "logo": U + "/assets/img/logo-512.png", "description": SITE["tagline"],
       "founder": {"@id": U + "/about#person"}, "sameAs": [SITE["author_page"], "https://github.com/nexagenlabs", "https://benchmate.nexagenlabs.com/", "https://verihelix.nexagenlabs.com/", "https://www.linkedin.com/in/suryaprakash-tripathy-09b7751b6/"]}
PERSON = {"@type": "Person", "@id": U + "/about#person", "name": AUTHOR, "url": U + "/about",
          "jobTitle": "Biotechnology researcher and author", "image": U + "/assets/img/suryaprakash-tripathy.jpg",
          "alumniOf": {"@type": "CollegeOrUniversity", "name": "Pondicherry University"},
          "knowsAbout": ["Biotechnology", "Cancer biology", "Computational drug discovery", "Molecular docking", "AI for life sciences", "Laboratory techniques"],
          "worksFor": {"@id": U + "/#org"}, "sameAs": SAME_AS}

def ld(*objs):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": list(objs)}, ensure_ascii=False) + "</script>"

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": U + p} for i, (n, p) in enumerate(items)]}

def crumbs_html(items):
    parts = [f'<a href="{p}">{e(n)}</a>' for n, p in items[:-1]] + [f'<span aria-current="page">{e(items[-1][0])}</span>']
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(parts) + '</nav>'

# ------------------------------------------------------------------ layout
THEME_BOOT = '<script>try{var t=localStorage.getItem("nx-theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>'

def header_html(active=None):
    nav = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if active == h else ""}>{n}</a></li>' for h, n in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap nav">
<a class="brand" href="/" aria-label="NexagenLabs home">{LOGO}<span>Nexagen<b>Labs</b></span></a>
<ul class="nav-links" id="nav-links">{nav}</ul>
<button class="search-btn" data-open-search aria-label="Search the site">{icon("search")}<span>Search</span><kbd>Ctrl K</kbd></button>
<button class="icon-btn theme-btn" data-theme-toggle aria-label="Switch between dark and light theme">{icon("moon", "moon")}{icon("sun", "sun")}</button>
<button class="icon-btn menu-btn" aria-expanded="false" aria-controls="nav-links" aria-label="Menu">{icon("menu")}</button>
</div></header>'''

def chrome_html():
    return f'''<div class="s-overlay" id="search" hidden role="dialog" aria-modal="true" aria-label="Search NexagenLabs">
<div class="s-box"><div class="s-head">{icon("search")}<input type="search" placeholder="Search tools, guides, books, buffers" aria-label="Search" autocomplete="off"><button class="s-close" data-close-search aria-label="Close search">Esc</button></div>
<div class="s-results" role="listbox"></div>
<div class="s-foot"><span><kbd>↑</kbd> <kbd>↓</kbd> move</span><span><kbd>Enter</kbd> open</span><span><kbd>Esc</kbd> close</span></div></div></div>
<div class="consent" id="consent" role="dialog" aria-label="Cookie preferences">
<p>We use Google Analytics cookies, only if you agree, to see which tools and guides help people most. No ads, no selling data. <a href="/privacy">Privacy</a></p>
<div class="actions"><button class="btn btn-primary btn-sm" data-consent="yes">Accept analytics</button><button class="btn btn-ghost btn-sm" data-consent="no">Decline</button></div>
</div>'''

def page(path, title, desc, body, *, schema="", og_type="website", og_image=None, active=None, priority="0.7", noindex=False):
    RENDERED.append((path, title, body, active))
    if PREVIEW:
        return
    canonical = U + path
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    og_image = og_image or U + "/assets/img/og-default.jpg"
    gsc = f'<meta name="google-site-verification" content="{SITE["gsc_verification"]}">' if SITE["gsc_verification"] else ""
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    doc = f'''<!doctype html>
<html lang="en" data-theme="dark" data-ga="{SITE["ga_id"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="{e(AUTHOR)}">
<link rel="canonical" href="{canonical}">
{robots}
<meta name="theme-color" content="#070c17">
<meta name="color-scheme" content="dark light">
{THEME_BOOT}
<meta property="og:site_name" content="NexagenLabs">
<meta name="application-name" content="NexagenLabs">
<meta name="apple-mobile-web-app-title" content="NexagenLabs">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_image}">
{gsc}
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/plex-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
<link rel="alternate" type="application/rss+xml" title="NexagenLabs Guides" href="/guides/feed.xml">
{schema}
</head>
<body>
{header_html(active)}
<main id="main">
{body}
</main>
{footer()}
{chrome_html()}
<script src="/assets/js/site.js?v={JS_V}" defer></script>
</body>
</html>'''
    write(path, doc)
    if not noindex:
        PAGES.append((path, priority))

def footer():
    tools = "".join(f'<li><a href="{p["page"] or p["url"]}">{e(p["name"].split(": ")[0])}</a></li>' for p in PROPERTIES)
    guides = "".join(f'<li><a href="/guides/{g["slug"]}">{e(g["short"])}</a></li>' for g in GUIDES[:5])
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="/">{LOGO}<span>Nexagen<b>Labs</b></span></a>
<p class="foot-about">{e(SITE["tagline"])} Built and maintained by {e(AUTHOR)}.</p>
<form class="signup" name="bench-notes-footer" method="POST" data-netlify="true" netlify-honeypot="company" action="/kit-download" data-reveal="footer-kit" data-ok="You're on the list. Your kit is ready.">
<input type="hidden" name="form-name" value="bench-notes-footer"><p class="hp"><label>Company <input name="company"></label></p>
<input type="email" name="email" required placeholder="you@lab.edu" aria-label="Email for the Bench Starter Kit"><button class="btn btn-primary btn-sm" type="submit">Get the kit</button>
<p class="fine form-status" role="status" style="width:100%"></p><a id="footer-kit" class="kit-link text-link" hidden href="{KIT}" download>Download the Bench Starter Kit (PDF)</a></form>
<p class="fine">Six printable cheat sheets, plus one bench tip a month.</p></div>
<div><h4>Tools</h4><ul>{tools}<li><a href="/tools">All tools</a></li></ul></div>
<div><h4>Guides</h4><ul>{guides}<li><a href="/guides/">All guides</a></li></ul></div>
<div><h4>NexagenLabs</h4><ul><li><a href="/books/">Books and free guides</a></li><li><a href="/starter-kit">Bench Starter Kit</a></li><li><a href="/certification">Free certificates</a></li><li><a href="/about">About the founder</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy">Privacy</a></li><li><a href="#" id="cookie-settings">Cookie settings</a></li></ul></div>
</div>
<div class="foot-base"><span>© <span id="year">{date.today().year}</span> NexagenLabs, {e(SITE["location"])}</span><span>Free tools. No login. No ads.</span></div>
</div></footer>'''

def write(path, content):
    if path.endswith("/"):
        fp = os.path.join(OUT, path.strip("/"), "index.html")
    elif path.endswith((".xml", ".txt", ".json", ".webmanifest", ".html")):
        fp = os.path.join(OUT, path.lstrip("/"))
    else:
        fp = os.path.join(OUT, path.lstrip("/") + ".html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)

# ------------------------------------------------------------------ components
def cover(b, eager=False):
    """Typeset cover that sits under the real Amazon cover. If the image can't load, the typeset one shows."""
    img = "" if PREVIEW else (f'<img src="{b["cover"]}" alt="Cover of {e(b["title"])} by {e(AUTHOR)}" width="267" height="400" decoding="async" '
                              + ('fetchpriority="high"' if eager else 'loading="lazy"') + ' onerror="this.remove()">')
    return f'<div class="cover" data-tone="{b["tone"]}"><span class="cover-t">{e(b["title"])}</span><span class="cover-a">{e(AUTHOR)}</span>{img}</div>'

def explore_btn(b, where, cls="btn btn-ghost btn-sm"):
    return (f'<a class="{cls}" href="{b["stores"]["us"]}" target="_blank" rel="noopener" data-ev="amazon_click" '
            f'data-label="{b["slug"]}|us|{where}" aria-label="Explore {e(b["title"])} on Amazon">Explore {EXT}</a>')

def book_card(b, where="grid"):
    return f'''<article class="book">
<a href="/books/{b["slug"]}" tabindex="-1" aria-hidden="true">{cover(b)}</a>
<div><p class="book-topic">{e(b["topic"])}</p>
<h3><a href="/books/{b["slug"]}">{e(b["title"])}</a></h3>
<p class="sub">{e(b["subtitle"])}</p>
<div class="book-actions">{explore_btn(b, where)}</div></div></article>'''

def free_card(f, where="books"):
    extras = "".join(f"<li>{e(x)}</li>" for x in f["extras"])
    return f'''<article class="free">
<div class="cover paper"><span><span class="cover-rule"></span><span class="cover-t">{e(f["title"])}</span><span class="cover-s">{e(f["series"])}</span></span><span class="cover-a">{e(AUTHOR)}</span></div>
<p class="for">{e(f["for"])}</p>
<h3>{e(f["title"])}</h3>
<p>{e(f["desc"])}</p>
<ul class="inc"><li>Book, {f["pages"]} pages (PDF)</li>{extras}</ul>
<a class="btn btn-primary btn-sm" href="{f["url"]}" target="_blank" rel="noopener" data-ev="free_guide_click" data-label="{f["slug"]}|{where}">Get it free {EXT}</a>
</article>'''

FB = {f["slug"]: f for f in FREE_BOOKS}
def free_shelves(where):
    out = ""
    for name, note, slugs in FREE_SERIES:
        cards = "".join(free_card(FB[x], where) for x in slugs)
        out += f'<h3 class="dir-h">{e(name)} <small>{e(note)}</small></h3><div class="free-shelf">{cards}</div>'
    return out

def vh_grouped(where, label):
    out = ""
    for gid, gname in VERIHELIX_GROUPS:
        rows = "".join(row_card(n, VH + p, d, "verihelix.nexagenlabs.com" + p, "ai companion", "open_tool", label + p) for n, p, d, g in VERIHELIX_TOOLS if g == gid)
        out += f'<{where} class="dir-h">{e(gname)}</{where}><div class="grid g-3">{rows}</div>'
    return out

def guide_row(g):
    return f'''<li><a class="guide-row" href="/guides/{g["slug"]}">
<h3>{e(g["title"].split(":")[0])}</h3><span class="min">{g["minutes"]} min read</span>
<p>{e(g["description"].split(". Free")[0].rstrip("."))}.</p>
<span class="uses">Pairs with the {e(g["tool"][0])}</span></a></li>'''

def guide_list(gs):
    return '<ul class="list">' + "".join(guide_row(g) for g in gs) + "</ul>"

def row_card(name, url, desc, where, cat, ev="open_tool", label=""):
    ext = url.startswith("http")
    return f'''<article class="row-card" data-cat="{cat}">
<h3><a href="{url}"{' target="_blank" rel="noopener"' if ext else ""} data-ev="{ev}" data-label="{label or url}">{e(name)}</a></h3>
<p>{e(desc)}</p><span class="where">{e(where)}</span></article>'''

def site_panel(p, tool_rows, extra_actions="", one=False):
    b = book_by(p["book"])
    tag = '<span class="tag new">New</span>' if p["status"] == "new" else ""
    lis = "".join(f'<li><a href="{u}" target="_blank" rel="noopener" data-ev="open_tool" data-label="{p["slug"]}-list"><b>{e(n)}</b>{e(d)}</a></li>' for n, u, d in tool_rows)
    more = f'<a class="btn btn-ghost" href="{p["page"]}">What\'s inside</a>' if p["page"] else ""
    return f'''<article class="site" data-tone="{p["tone"] or "teal"}">
<div class="site-main">
<p class="site-kind">{e(p["kind"])} {tag}</p>
<h3>{e(p["name"])}</h3>
<p>{e(p["desc"])}</p>
<p class="site-book">Companion to <a href="/books/{b["slug"]}">{e(b["title"])}</a></p>
<div class="actions"><a class="btn btn-primary" href="{p["url"]}" target="_blank" rel="noopener" data-ev="open_tool" data-label="{p["slug"]}-panel">Open {e(p["name"].split(":")[0])} {EXT}</a>{more}{extra_actions}</div>
</div>
<ul class="site-list{" one" if one else ""}">{lis}</ul>
</article>'''

AGENT_BUILDS = [("Literature triage", "Rank and summarise papers against your question."), ("Data wrangling", "Clean instrument exports into tidy tables."),
                ("Plate mapping", "Lay out plates and track what went where."), ("Docking loops", "Run and score docking jobs in a loop."),
                ("ELN and LIMS bridges", "Move results into the notebook of record."), ("Run provenance", "Log every run so it can be audited.")]

def sites_block():
    bm, vh, lab = PROPERTIES
    bm_rows = [(n, BM + pth, d.rstrip(".")) for n, pth, d, _ in BENCHMATE_TOOLS]
    vh_rows = [(n, VH + pth, d.rstrip(".")) for n, pth, d, _ in VERIHELIX_TOOLS]
    lab_rows = [(n, lab["url"], d.rstrip(".")) for n, d in AGENT_BUILDS]
    return f'''<div class="site-stack">{site_panel(bm, bm_rows)}{site_panel(vh, vh_rows)}{site_panel(lab, lab_rows)}</div>'''

SHEETS = ["Molarity and mass", "C1V1 dilutions", "Serial dilutions and CFU", "Buffers and pKa table", "Percent solutions", "Nucleic acid conversions"]
ROLES = "<option>BS / undergraduate student</option><option>MS student</option><option>PhD student</option><option>Postdoc / scientist</option><option>Lab manager / technician</option><option>Industry R&amp;D</option><option>Other</option>"

def newsletter(name="bench-notes"):
    rid = name + "-kit"
    sheets = "".join(f"<li>{s}</li>" for s in SHEETS)
    return f'''<section class="sec"><div class="wrap"><div class="kit">
<div class="kit-copy"><h2>Six bench cheat sheets, free.</h2>
<p class="lead">The calculations you redo every week, on one printable page each. Pin them above the bench.</p>
<ul class="sheets">{sheets}</ul></div>
<form class="form kit-form" name="{name}" method="POST" data-netlify="true" netlify-honeypot="company" action="/kit-download" data-ok="Done. Your kit is ready below." data-reveal="{rid}">
<input type="hidden" name="form-name" value="{name}"><p class="hp"><label>Company <input name="company"></label></p>
<div><label for="{name}-email">Email</label><input id="{name}-email" type="email" name="email" required placeholder="you@lab.edu" autocomplete="email"></div>
<div><label for="{name}-role">I am a</label><select id="{name}-role" name="role">{ROLES}</select></div>
<button class="btn btn-primary" type="submit">Send me the kit</button>
<p class="fine form-status" role="status"></p>
<a class="btn btn-ghost kit-link" id="{rid}" hidden href="{KIT}" download data-ev="kit_download" data-label="{name}">{icon("down")} Download the Bench Starter Kit (PDF)</a>
<p class="fine">You also get Bench Notes, one useful bench tip a month. Unsubscribe in one click. <a href="/privacy">Privacy</a></p>
</form></div></div></section>'''

def faq_html(items):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items) + '</div>'

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def rail(title, lead, content, cls="sec", extra=""):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f'''<section class="{cls}"><div class="wrap rail"><div class="rail-head"><h2>{title}</h2>{lead_html}{extra}</div><div>{content}</div></div></section>'''

# ------------------------------------------------------------------ live calculators
_wid = [0]
def _sel(name, opts, sel=None, label=""):
    o = "".join(f'<option value="{v}"{" selected" if v == sel else ""}>{t}</option>' for v, t in opts)
    return f'<select name="{name}" aria-label="{label or name}">{o}</select>'
def _f(label, inner):
    return f'<div class="field"><label>{label}</label><div class="ctl">{inner}</div></div>'
def _inp(name, v, label):
    return f'<input name="{name}" inputmode="decimal" value="{v}" aria-label="{label}">'
CU = [("M","M"),("mM","mM"),("µM","µM"),("nM","nM")]
VU = [("L","L"),("mL","mL"),("µL","µL")]
WIDGET_FULL = {"molarity": ("Molarity & Dilution", "/molarity"), "c1v1": ("Molarity & Dilution", "/molarity"), "serial": ("Molarity & Dilution", "/molarity"),
               "pbs": ("Buffer Recipe Generator", "/buffer"), "percent": ("Percent-Solution Generator", "/percent"), "dna": ("Unit Converter", "/converter")}
WIDGET_TITLE = {"molarity": "Molarity to mass", "c1v1": "C1V1 dilution", "serial": "Serial dilution table", "pbs": "PBS recipe scaler", "percent": "Percent solutions", "dna": "ng/µL to nM and copies"}

def tube():
    _wid[0] += 1
    cid = f"tube{_wid[0]}"
    shape = "M12 6V84L25 122Q29 128 33 122L46 84V6"
    return f'''<figure class="tube" aria-hidden="true"><svg viewBox="0 0 58 132"><defs><clipPath id="{cid}"><path d="{shape}Z"/></clipPath></defs>
<g clip-path="url(#{cid})"><rect class="dil" x="0" y="30" width="58" height="98"/><rect class="stock" x="0" y="118" width="58" height="10"/></g>
<path class="glass" d="{shape}"/><path class="glass" d="M8 6H50"/></svg><figcaption><span class="w-pct"></span></figcaption></figure>'''

def widget(kind, d=None, hidden=False, title=True):
    d = d or {}
    g = lambda k, v: d.get(k, v)
    if kind == "molarity":
        presets = [("", "Pick a compound"), ("58.44","NaCl (58.44)"), ("74.55","KCl (74.55)"), ("121.14","Tris base (121.14)"), ("372.24","Na₂EDTA·2H₂O (372.24)"), ("203.30","MgCl₂·6H₂O (203.30)"), ("147.01","CaCl₂·2H₂O (147.01)"), ("180.16","Glucose (180.16)"), ("238.30","HEPES (238.30)")]
        fields = (_f("Compound", _sel("preset", presets, "", "Compound preset")) +
            '<div class="calc-row">' + _f("Molarity", _inp("m", "1", "Molarity") + _sel("mu", CU, "M", "Molarity unit")) +
            _f("Final volume", _inp("v", "500", "Volume") + _sel("vu", VU, "mL", "Volume unit")) + '</div>' +
            _f("MW (g/mol, from your bottle)", _inp("mw", "58.44", "Molecular weight")))
    elif kind == "c1v1":
        fields = ('<div class="calc-row">' + _f("Stock (C<sub>1</sub>)", _inp("c1", g("c1", "10"), "C1") + _sel("c1u", CU, g("c1u", "mM"), "C1 unit")) +
            _f("Final (C<sub>2</sub>)", _inp("c2", g("c2", "25"), "C2") + _sel("c2u", CU, g("c2u", "µM"), "C2 unit")) + '</div>' +
            _f("Final volume (V<sub>2</sub>)", _inp("v2", g("v2", "200"), "V2") + _sel("v2u", VU, g("v2u", "µL"), "V2 unit")))
    elif kind == "serial":
        fields = ('<div class="calc-row">' + _f("Start concentration", _inp("c0", "10", "Start") + _sel("cu", CU, "mM", "Unit")) +
            _f("Dilution factor per step", _inp("f", "10", "Factor")) + '</div><div class="calc-row">' +
            _f("Number of tubes", _inp("n", "6", "Tubes")) + _f("Transfer volume (µL)", _inp("t", "100", "Transfer volume")) + '</div>')
    elif kind == "pbs":
        fields = ('<div class="calc-row">' + _f("Final volume", _inp("v", "1", "Volume") + _sel("vu", VU, "L", "Volume unit")) +
            _f("Strength (X)", _inp("x", "1", "Strength")) + '</div>' +
            _f("Your Na₂HPO₄ form", _sel("hyd", [("141.96","Anhydrous (141.96)"), ("268.07","Heptahydrate (268.07)"), ("358.14","Dodecahydrate (358.14)")], "141.96", "Hydrate form")))
    elif kind == "percent":
        fields = (_f("Type", _sel("type", [("wv","% w/v (solid in liquid)"), ("vv","% v/v (liquid in liquid)"), ("ww","% w/w to molarity")], "wv", "Percent type")) +
            '<div class="calc-row">' + _f("Percent", _inp("p", "10", "Percent")) + _f("Final volume (mL)", _inp("v", "100", "Volume")) + '</div><div class="calc-row">' +
            _f("MW (optional)", _inp("mw", "", "MW")) + _f("Density g/mL (w/w only)", _inp("d", "", "Density")) + '</div>')
    else:  # dna
        fields = ('<div class="calc-row">' + _f("Concentration (ng/µL)", _inp("c", "50", "Concentration")) + _f("Length (bp or nt)", _inp("len", "500", "Length")) + '</div>' +
            _f("Molecule", _sel("type", [("650","dsDNA (650 g/mol per bp)"), ("330","ssDNA (330 g/mol per nt)"), ("340","RNA (340 g/mol per nt)")], "650", "Molecule type")))
    head = f'<p class="widget-title">{WIDGET_TITLE[kind]} <span>Live, runs in your browser</span></p>' if title else ""
    full = WIDGET_FULL[kind]
    return f'''<div class="widget" data-widget="{kind}" data-full="{BM}{full[1]}" data-full-name="{full[0]}"{" hidden" if hidden else ""}>{head}{fields}
<div class="readout" aria-live="polite"><div><div class="k">Result</div><div class="v w-out">…</div><div class="s w-sub"></div></div>{tube() if kind == "c1v1" else ""}</div></div>'''

def console(tabs, defaults=None, label="Live bench calculators"):
    """Tabbed calculator console. tabs: [(kind, tab label)]"""
    btns = "".join(f'<button role="tab" aria-selected="{"true" if i == 0 else "false"}" data-tab="{k}">{e(t)}</button>' for i, (k, t) in enumerate(tabs))
    panels = "".join(widget(k, (defaults or {}).get(k), hidden=i > 0, title=False) for i, (k, _) in enumerate(tabs))
    first = WIDGET_FULL[tabs[0][0]]
    return f'''<div class="console" data-console aria-label="{label}">
<div class="console-tabs" role="tablist">{btns}</div>{panels}
<div class="console-foot"><span>Runs in your browser. Nothing is uploaded.</span><a class="console-full" href="{BM}{first[1]}" target="_blank" rel="noopener" data-ev="open_benchmate" data-label="console">Full calculator {EXT}</a></div></div>'''

GUIDE_WIDGET = {"how-to-calculate-molarity": "molarity", "c1v1-c2v2-dilution-guide": "c1v1", "serial-dilution-guide": "serial",
                "how-to-prepare-buffers": "pbs", "percent-solutions-w-v-v-v": "percent", "dna-concentration-ng-ul-to-nm": "dna"}
HERO_TABS = [("c1v1", "Dilute a stock"), ("molarity", "Molarity to mass"), ("dna", "ng/µL to nM"), ("pbs", "Scale PBS")]

# ------------------------------------------------------------------ pages
def finder():
    jobs = "".join(f'<button class="job" data-job="{i}" aria-pressed="{"true" if i == 0 else "false"}">{e(n)}</button>' for i, (n, _) in enumerate(JOBS))
    outs = ""
    for i, (_, picks) in enumerate(JOBS):
        cards = ""
        for kind, t, note, url in picks:
            ext = url.startswith("http")
            cards += f'<a class="pick" href="{url}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""} data-ev="finder_click" data-label="{e(t)}"><span class="what">{kind}</span><b>{e(t)}</b><span>{e(note)}</span></a>'
        outs += f'<div class="job-out" data-job-out="{i}"{" hidden" if i else ""}>{cards}</div>'
    return f'''<section class="sec-tight"><div class="wrap"><div class="finder" data-finder>
<h2>What do you need to do today?</h2>
<div class="jobs" role="group" aria-label="Pick a task">{jobs}</div>{outs}</div></div></section>'''

def home():
    books = "".join(book_card(b, "home") for b in BOOKS)
    creds = "".join(f'<li><span class="n">{n}<small>{u}</small></span><span class="l">{e(l)}</span></li>' for n, u, l in CREDENTIALS[:4])
    faq = [
        ("Is everything on NexagenLabs free?", "Yes. BenchMate, VeriHelix, every companion site and every certificate are free to use with no login. The books are sold on Amazon; the tools work without them."),
        ("Are the free guides really free?", "Yes. Each Bench Ready guide is listed at $0 on our store at books.nexagenlabs.com. Enter 0 as the price and you get the book, the Excel workbook, the printable kit and the message templates."),
        ("Does BenchMate store my data?", "No. Calculations run in your browser. The Reagent Log saves recipes only in your own browser storage, never on a server."),
        ("Who builds these tools?", "Suryaprakash Tripathy, a biotechnology researcher with an M.Sc. from Pondicherry University, national fellowships (ICMR-JRF, DBT-GATB, GATE BT), and research work at IISER Bhopal, IIT Guwahati and ICMR institutes."),
        ("Which countries can buy the books?", "Every title is on Amazon.com, Amazon.co.uk and Amazon.de, plus other Amazon stores, in Kindle and print editions."),
    ]
    n_tools = len(BENCHMATE_TOOLS) + len(VERIHELIX_TOOLS)
    body = f'''
<section class="hero"><div class="wrap hero-grid">
<div>
<h1 class="rise">Bench-tested tools for the people who do the science.</h1>
<p class="lead rise">NexagenLabs makes free calculators, AI-checking tools, companion code and field-tested guides for wet-lab and computational biologists. Built by a working researcher, checked against real protocols, free to use.</p>
<div class="actions rise">
<a class="btn btn-primary" href="{BM}/" target="_blank" rel="noopener" data-ev="open_benchmate" data-label="hero">Open BenchMate {EXT}</a>
<a class="btn btn-ghost" href="/tools">See all {n_tools} tools</a>
</div>
<ul class="facts rise">
<li><b>{n_tools}</b>free tools</li><li><b>370</b>verified compounds</li><li><b>40</b>buffer recipes</li><li><b>0</b>logins</li>
</ul>
</div>
{console(HERO_TABS, {"c1v1": {"c1": "1", "c1u": "mM", "c2": "50", "c2u": "µM", "v2": "10", "v2u": "mL"}})}
</div></section>

{finder()}

<section class="sec"><div class="wrap">
<div class="sec-head-row"><div class="sec-head"><h2>Three free sites, each tied to a book.</h2>
<p class="lead">Each site does one kind of job well, and each links to the book that explains the science behind it.</p></div>
<a class="btn btn-ghost" href="/tools">Tool directory</a></div>
{sites_block()}
</div></section>

<section class="sec sec-alt" id="free"><div class="wrap">
<div class="sec-head-row"><div class="sec-head"><h2>Free guides for life at the bench.</h2>
<p class="lead">Each one is a short book with an Excel workbook, printable pages and message templates. Free to download.</p></div>
<a class="btn btn-ghost" href="/books/">All books and guides</a></div>
{free_shelves("home")}
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head-row"><div class="sec-head"><h2>Written at the bench, for the bench.</h2>
<p class="lead">Technical handbooks for researchers and clear science for everyone else. Available on Amazon in the US, UK and Germany.</p></div>
<a class="btn btn-ghost" href="/books/">All books</a></div>
<div class="shelf">{books}</div>
</div></section>

{rail("Learn the maths behind the tools.", "Plain-language guides for the calculations every lab runs, each with worked examples and a live calculator.", guide_list(GUIDES[:4]), cls="sec sec-alt", extra='<p style="margin-top:18px"><a class="btn btn-ghost" href="/guides/">All guides</a></p>')}

{rail("Built by a researcher, not a marketing team.", "", f"""<div class="founder"><img class="portrait" src="/assets/img/suryaprakash-tripathy.webp" alt="{e(AUTHOR)}" width="104" height="104" loading="lazy">
<p class="lead mb-0">{e(AUTHOR)} is a biotechnology researcher working across cancer biology, computational drug discovery and filariasis, with research stints at IISER Bhopal, IIT Guwahati and ICMR institutes.</p></div>
<ul class="creds">{creds}</ul>
<p style="margin-top:22px"><a class="btn btn-ghost" href="/about">Read the full profile</a></p>""")}

{newsletter("bench-notes")}

{rail("Quick answers", "", faq_html(faq), cls="sec sec-alt")}
'''
    website = {"@type": "WebSite", "@id": U + "/#website", "url": U + "/", "name": "NexagenLabs", "alternateName": ["Nexagen Labs", "NexaGenLabs", "Nexagenlabs", "nexagenlabs.com"], "publisher": {"@id": U + "/#org"}, "inLanguage": "en"}
    page("/", "NexagenLabs: Free Lab Calculators, AI-Biotech Tools & Guides for Scientists",
         "Free research tools for scientists: BenchMate lab calculators (molarity, dilution, buffers), 16 VeriHelix AI-biotech tools, companion code, free lab guides and books by Suryaprakash Tripathy.",
         body, schema=ld(ORG, PERSON, website, faq_ld(faq)), priority="1.0")

def tools():
    site_cards = "".join(row_card(p["name"], p["url"], p["desc"], p["url"].replace("https://", "").rstrip("/"), p["cats"], label=p["slug"]) for p in PROPERTIES)
    bm_cards = "".join(row_card(n, BM + pth, d, "benchmate.nexagenlabs.com" + pth, "bench calculators " + cat, "open_benchmate", "dir" + pth) for n, pth, d, cat in BENCHMATE_TOOLS)
    guide_cards = "".join(row_card(g["title"].split(":")[0], f'/guides/{g["slug"]}', g["description"].split(". Free")[0].rstrip(".") + ".", f'Guide, {g["minutes"]} min read', "guide", "open_guide") for g in GUIDES)
    free_cards = "".join(row_card(f["title"], f["url"], f["desc"], f'Free guide, {f["pages"]} pages', "guide free", "free_guide_click", f["slug"] + "|tools") for f in FREE_BOOKS)
    filters = [("all", "All"), ("bench", "Bench calculators"), ("ai", "AI and code"), ("guide", "Guides"), ("free", "Free downloads")]
    chips = "".join(f'<button class="chip" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{n}</button>' for k, n in filters)
    items = [{"@type": "ListItem", "position": i + 1, "url": p["url"], "name": p["name"]} for i, p in enumerate(PROPERTIES)]
    n_tools = len(BENCHMATE_TOOLS) + len(VERIHELIX_TOOLS)
    body = f'''<section class="page-hero"><div class="wrap">
{crumbs_html([("Home","/"),("Tools","/tools")])}
<h1>Every NexagenLabs tool, in one place.</h1>
<p class="lead">{len(PROPERTIES)} sites, {n_tools} tools, {len(GUIDES)} guides and {len(FREE_BOOKS)} free downloads. All free, no login.</p>
</div></section>
<section class="sec-tight" style="padding-top:8px"><div class="wrap">
<div class="filters"><label class="search-field">{icon("search")}<input id="dir-q" type="search" placeholder="Search: buffer, dilution, citations, SMILES, PCR" aria-label="Search tools"></label></div>
<div class="filters" role="group" aria-label="Filter by category">{chips}</div>
<div id="directory">
<div data-group><h2 class="dir-h">Sites</h2><div class="grid g-3">{site_cards}</div></div>
<div data-group><h2 class="dir-h">Inside BenchMate <small>bench calculators and references</small></h2><div class="grid g-3">{bm_cards}</div></div>
<div data-group><h2 class="dir-h">Inside VeriHelix <small>use AI, then check it</small></h2>{vh_grouped("h3", "dir-vh")}</div>
<div data-group><h2 class="dir-h">Guides</h2><div class="grid g-3">{guide_cards}</div></div>
<div data-group><h2 class="dir-h">Free downloads</h2><div class="grid g-3">{free_cards}</div></div>
</div>
<p class="empty" id="dir-empty">Nothing matches that. Try a broader word, or <a href="/contact">suggest a tool</a>.</p>
</div></section>
{newsletter("bench-notes-tools")}'''
    page("/tools", "Free Research Tools for Scientists: Lab Calculators & AI-Biotech Tools | NexagenLabs",
         "Directory of free NexagenLabs research tools: BenchMate molarity, dilution and buffer calculators, VeriHelix citation, prompt and molecule tools, AI-agent companion code and free lab guides.",
         body, schema=ld(ORG, crumbs_ld([("Home","/"),("Tools","/tools")]), {"@type": "ItemList", "itemListElement": items}), active="/tools", priority="0.9")

def benchmate():
    rows = "".join(row_card(n, BM + p, d, p, "bm", "open_benchmate", "bm-page" + p) for n, p, d, _ in BENCHMATE_TOOLS)
    wl = book_by("the-working-laboratory")
    faq = [
        ("Is BenchMate free?", "Yes. Every BenchMate tool is free with no login, no account and no ads."),
        ("Does BenchMate work offline?", "Yes. Once loaded, the calculators run entirely in your browser, so they keep working on a lab computer with a patchy connection."),
        ("Where are my saved recipes stored?", "The Reagent Log saves recipes only in your own browser's storage. Nothing is uploaded to a server. Export them if you switch computers."),
        ("How accurate are the molecular weights?", "BenchMate uses a verified list of 370 compounds with formula and CAS number, including common hydrate forms, so you can match the exact reagent on your bottle."),
        ("Which calculations does BenchMate cover?", "Molarity and mass, C1V1 dilutions, serial dilutions, unit conversions including ng/µL for nucleic acids, buffer recipes for 40 buffers, and w/v, v/v and m/v percent solutions."),
        ("Is there a certificate?", "Yes. Pass the Technique Quiz challenges to earn a Bench Fundamentals certificate."),
    ]
    app = {"@type": "SoftwareApplication", "name": "BenchMate", "url": BM + "/", "applicationCategory": "EducationalApplication",
           "applicationSubCategory": "Laboratory calculator", "operatingSystem": "Any (web browser)",
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": U + "/#org"},
           "author": {"@id": U + "/about#person"}, "featureList": [n for n, *_ in BENCHMATE_TOOLS],
           "description": "Free, offline, no-login lab calculators for molarity, dilutions, buffers, percent solutions and unit conversion."}
    body = f'''<section class="hero"><div class="wrap hero-grid">
<div>{crumbs_html([("Home","/"),("BenchMate","/benchmate")])}
<h1 class="rise">BenchMate: the lab calculator built for the bench.</h1>
<p class="lead rise">Molarity, C1V1 dilutions, serial dilutions, buffer recipes and percent solutions in one fast, offline-ready web app. Verified data, clear warnings, nothing to install.</p>
<div class="actions rise"><a class="btn btn-primary" href="{BM}/" target="_blank" rel="noopener" data-ev="open_benchmate" data-label="bm-hero">Open BenchMate {EXT}</a><a class="btn btn-ghost" href="#bm-tools">See all {len(BENCHMATE_TOOLS)} tools</a></div>
<ul class="facts rise"><li><b>370</b>verified compounds</li><li><b>40</b>buffers</li><li><b>100</b>quiz questions</li><li><b>0</b>logins</li></ul>
</div>
{console([("c1v1", "Dilute a stock"), ("serial", "Serial dilution"), ("percent", "Percent solution")], {"c1v1": {"c1": "10", "c2": "100", "v2": "1", "v2u": "mL"}})}
</div></section>
<section class="sec" id="bm-tools"><div class="wrap">
<div class="sec-head"><h2>{len(BENCHMATE_TOOLS)} tools, one tab.</h2></div>
<div class="grid g-3">{rows}</div></div></section>
<section class="sec sec-alt"><div class="wrap"><div class="book-detail" style="grid-template-columns:minmax(0,220px) minmax(0,1fr);align-items:center">
<a href="/books/the-working-laboratory" tabindex="-1" aria-hidden="true">{cover(wl)}</a>
<div><h2>BenchMate is the calculator. The Working Laboratory is the manual.</h2>
<p class="lead">Volume 1 of The Biotechnology Techniques Bible covers 22 core techniques: units and concentration, solutions and dilutions, water and buffers, sterilisation and safety. Each chapter maps to a BenchMate tool.</p>
<div class="actions"><a class="btn btn-ghost" href="/books/the-working-laboratory">About the book</a>{explore_btn(wl, "benchmate-page", "btn btn-ghost")}</div></div>
</div></div></section>
{rail("Worked examples for every tool", "Each guide walks through the maths, then lets you check your numbers with a live calculator.", guide_list(GUIDES))}
{rail("BenchMate questions", "", faq_html(faq), cls="sec sec-alt")}
{newsletter("bench-notes-benchmate")}'''
    page("/benchmate", "BenchMate: Free Lab Calculator for Molarity, Dilutions & Buffers | NexagenLabs",
         "BenchMate is a free, offline, no-login lab calculator: molarity, C1V1 and serial dilutions, 40 buffer recipes, percent solutions, MW lookup for 370 compounds, and a technique quiz with certificate.",
         body, schema=ld(ORG, app, crumbs_ld([("Home","/"),("BenchMate","/benchmate")]), faq_ld(faq)), active="/benchmate", priority="0.95")

def verihelix():
    ab = book_by("ai-for-biotech")
    extra = "".join(row_card(n, VH + p, d, "verihelix.nexagenlabs.com" + p, "vh", "open_tool", "vh-extra" + p) for n, p, d in [
        ("AI Tool Atlas", "/atlas/", "Which AI tools exist for each biotech job, and what each one is good for."),
        ("Certificates", "/certificates/", "Take a short assessment and earn a verifiable VeriHelix certificate."),
        ("Verify a certificate", "/verify/", "Check that a VeriHelix certificate someone shows you is genuine.")])
    faq = [
        ("Is VeriHelix free?", "Yes. Every VeriHelix tool is free to use with no login and no account."),
        ("What does the Citation Verifier check?", "It looks up each reference in Crossref and PubMed and reports whether the paper exists, whether the DOI matches the title, and whether it has been retracted."),
        ("Can it help me read an AlphaFold model?", "Yes. The Structure Confidence Reader explains which regions of a predicted structure to trust, which to doubt, and why."),
        ("What does Molecule Desk calculate?", "From a SMILES string it reports molecular weight, cLogP, TPSA, Lipinski and Veber rules, an ESOL solubility estimate, and PAINS and Brenk structural alerts, for one molecule or a batch."),
        ("Is it safe to paste my data into AI tools?", "Can I Paste This? tells you which AI tools are suitable for your kind of data before you paste anything."),
        ("How does VeriHelix relate to AI for Biotech?", "VeriHelix is the free companion to the book. Each tool points to the chapter that explains the method behind it."),
    ]
    app = {"@type": "SoftwareApplication", "name": "VeriHelix", "url": VH + "/", "applicationCategory": "EducationalApplication",
           "applicationSubCategory": "AI tools for biotechnology research", "operatingSystem": "Any (web browser)",
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": U + "/#org"},
           "author": {"@id": U + "/about#person"}, "featureList": [n for n, *_ in VERIHELIX_TOOLS],
           "description": "Free, no-login tools that help biotechnologists use AI and check what AI gives them."}
    body = f'''<section class="hero"><div class="wrap">
{crumbs_html([("Home","/"),("VeriHelix","/verihelix")])}
<h1 class="rise" style="max-width:17ch">VeriHelix: use AI in your research, then check it.</h1>
<p class="lead rise">A free workbench for AI-era biotechnology. Verify the references an AI gave you, read an AlphaFold model properly, screen a molecule, look up a variant and audit an ML study for leakage.</p>
<div class="actions rise"><a class="btn btn-primary" href="{VH}/" target="_blank" rel="noopener" data-ev="open_tool" data-label="vh-hero">Open VeriHelix {EXT}</a><a class="btn btn-ghost" href="/books/ai-for-biotech">The book behind it</a></div>
<ul class="facts rise"><li><b>{len(VERIHELIX_TOOLS)}</b>tools</li><li><b>{len(VERIHELIX_GROUPS)}</b>areas of work</li><li><b>0</b>logins</li></ul>
</div></section>
<section class="sec" style="padding-top:20px"><div class="wrap">
<div class="sec-head" style="margin-bottom:0"><h2>All {len(VERIHELIX_TOOLS)} tools</h2></div>
{vh_grouped("h3", "vh-page")}
<h3 class="dir-h">Also on VeriHelix</h3><div class="grid g-3">{extra}</div>
</div></section>
<section class="sec sec-alt"><div class="wrap"><div class="book-detail" style="grid-template-columns:minmax(0,220px) minmax(0,1fr);align-items:center">
<a href="/books/ai-for-biotech" tabindex="-1" aria-hidden="true">{cover(ab)}</a>
<div><h2>VeriHelix is the workbench. AI for Biotech is the method.</h2>
<p class="lead">The book covers prompt engineering, AI-assisted literature review, protein structure prediction, drug discovery and more, with examples from real research. Each VeriHelix tool links to the chapter it comes from.</p>
<div class="actions"><a class="btn btn-ghost" href="/books/ai-for-biotech">About the book</a>{explore_btn(ab, "verihelix-page", "btn btn-ghost")}</div></div>
</div></div></section>
{rail("VeriHelix questions", "", faq_html(faq))}
{newsletter("bench-notes-verihelix")}'''
    page("/verihelix", "VeriHelix: 16 Free AI-Biotech Tools for Citations, AlphaFold, Molecules & ML Audits | NexagenLabs",
         "VeriHelix is a free, no-login AI-biotech workbench: verify AI-written references, read AlphaFold confidence, screen molecules, look up variants and audit ML studies for data leakage.",
         body, schema=ld(ORG, app, crumbs_ld([("Home","/"),("VeriHelix","/verihelix")]), faq_ld(faq)), active="/verihelix", priority="0.9")

def cert_card(name, how, target, url, site, tone, soon=False):
    action = ('<span class="tag">Coming soon</span>' if soon else
              f'<a class="btn btn-ghost btn-sm" href="{url}" target="_blank" rel="noopener" data-ev="cert_start" data-label="{e(name)}">Start {EXT}</a>')
    return f'''<article class="cert{" soon" if soon else ""}" data-tone="{tone}">
<div class="cert-top">{icon("seal", "cert-seal")}<span class="cert-site">{site}</span></div>
<h3>{e(name)}</h3>
<p>{e(how)}</p>
<p class="cert-target">{e(target)}</p>
{action}
</article>'''

def certification():
    quiz = [c for c in BM_CERTS if c[3] == "quiz"]
    habit = [c for c in BM_CERTS if c[3] == "habit"]
    bm_quiz = "".join(cert_card(n, h, t, u, "BenchMate quiz", "teal") for n, h, t, _, u in quiz)
    bm_habit = "".join(cert_card(n, h, t, u, "BenchMate habit", "teal", soon=True) for n, h, t, _, u in habit)
    vh = "".join(cert_card(n, h, t, u, f"VeriHelix track {i+1}", "blue") for i, (n, h, t, u) in enumerate(VH_CERTS))
    total = len(quiz) + len(VH_CERTS)
    faq = [
        ("Are the certificates really free?", "Yes. Every certificate on BenchMate and VeriHelix is free. There is no fee, no account and no login."),
        ("Why do I need to add my name on BenchMate?", "BenchMate issues certificates in the name you set on its quiz dashboard. If you qualify before adding a name, the certificate is issued as soon as you add it and answer your next question."),
        ("Do I need to create an account?", "No. Your progress is saved in your own browser on the device you use. Download your certificate, or keep its verification link, as your permanent copy."),
        ("How does someone check my VeriHelix certificate is genuine?", "Every VeriHelix certificate has a verification link and ID. Anyone can check it on the Verify a certificate page at verihelix.nexagenlabs.com/verify."),
        ("Can I add a certificate to LinkedIn?", "Yes. VeriHelix certificates are designed to be added to LinkedIn with their verification link. BenchMate certificates can be downloaded and shared."),
        ("What are the questions based on?", "BenchMate questions come from Volume 1 of The Biotechnology Techniques Bible, The Working Laboratory. VeriHelix tracks follow the chapters of AI for Biotech."),
        ("What is the capstone?", "Earn all four VeriHelix track certificates under the same name and you receive the AI-Augmented Biotechnologist capstone. It needs no extra exam."),
    ]
    creds = [{"@type": "EducationalOccupationalCredential", "name": n, "credentialCategory": "certificate", "url": u,
              "educationalLevel": "Beginner", "recognizedBy": {"@id": U + "/#org"}, "description": h} for n, h, *_, u in BM_CERTS] + \
            [{"@type": "EducationalOccupationalCredential", "name": n, "credentialCategory": "certificate", "url": u,
              "recognizedBy": {"@id": U + "/#org"}, "description": h} for n, h, _, u in VH_CERTS]
    items = {"@type": "ItemList", "name": "Free NexagenLabs certificates", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": c} for i, c in enumerate(creds)]}
    wl, ab = book_by("the-working-laboratory"), book_by("ai-for-biotech")
    body = f'''<section class="hero"><div class="wrap">
{crumbs_html([("Home","/"),("Free Certification","/certification")])}
<h1 class="rise" style="max-width:16ch">Free certificates for bench and AI skills.</h1>
<p class="lead rise">Answer bench-skills quiz questions or pass an AI-for-biotech track. Every certificate is free, needs no account, and can be downloaded and shared.</p>
<div class="actions rise"><a class="btn btn-primary" href="{BM}/quiz" target="_blank" rel="noopener" data-ev="cert_start" data-label="hero-bm">Start the BenchMate quiz {EXT}</a><a class="btn btn-ghost" href="{VH}/certificates/" target="_blank" rel="noopener" data-ev="cert_start" data-label="hero-vh">VeriHelix tracks {EXT}</a></div>
<ul class="facts rise"><li><b>{total}</b>certificates</li><li><b>1</b>capstone</li><li><b>0</b>fees</li><li><b>0</b>logins</li></ul>
</div></section>

<section class="sec-tight"><div class="wrap">
<ol class="cert-steps">
<li><b>Pick a certificate</b><span>Bench skills on BenchMate, AI skills on VeriHelix.</span></li>
<li><b>Add your name</b><span>Certificates are issued in the name you enter. Progress saves in your browser.</span></li>
<li><b>Answer the questions</b><span>Reach the target and your certificate is ready to download.</span></li>
<li><b>Share the proof</b><span>VeriHelix certificates carry a link anyone can verify.</span></li>
</ol></div></section>

<section class="sec" id="bench"><div class="wrap">
<div class="sec-head-row"><div class="sec-head"><h2>Bench skills, on BenchMate</h2>
<p class="lead">Built on <a href="/books/the-working-laboratory">{e(wl["title"])}</a>. Questions come from 100+ items across 8 categories of bench practice, at three difficulty levels.</p></div>
<a class="btn btn-ghost" href="{BM}/quiz/dashboard" target="_blank" rel="noopener" data-ev="cert_start" data-label="bm-dashboard">Your progress {EXT}</a></div>
<h3 class="dir-h">Earned through the Technique Quiz</h3><div class="cert-grid">{bm_quiz}</div>
<h3 class="dir-h">Earned through regular use <small>coming soon on BenchMate</small></h3><div class="cert-grid">{bm_habit}</div>
</div></section>

<section class="sec sec-alt" id="ai"><div class="wrap">
<div class="sec-head-row"><div class="sec-head"><h2>AI-for-biotech skills, on VeriHelix</h2>
<p class="lead">Four tracks that follow the chapters of <a href="/books/ai-for-biotech">{e(ab["title"])}</a>. Each certificate has a verification ID and link.</p></div>
<a class="btn btn-ghost" href="{VH}/verify/" target="_blank" rel="noopener" data-ev="cert_verify" data-label="vh-verify">Verify a certificate {EXT}</a></div>
<div class="cert-grid cert-grid-4">{vh}</div>
<div class="capstone"><div>{icon("seal", "cert-seal")}</div><div><h3>Capstone: AI-Augmented Biotechnologist</h3>
<p>Earn all four VeriHelix track certificates under the same name and the capstone is awarded automatically. No extra exam.</p></div>
<a class="btn btn-primary" href="{VH}/certificates/" target="_blank" rel="noopener" data-ev="cert_start" data-label="capstone">See your tracks {EXT}</a></div>
</div></section>

{rail("Certificate questions", "", faq_html(faq))}
{newsletter("bench-notes-certification")}'''
    page("/certification", "Free Biotech & Lab Skills Certificates: Bench and AI-for-Biotech Quizzes | NexagenLabs",
         "Earn free certificates in bench skills and AI for biotech: three BenchMate Technique Quiz certificates (Bench Fundamentals, Buffer Preparation, Dilution Mastery) and four verifiable VeriHelix tracks. No login.",
         body, schema=ld(ORG, items, crumbs_ld([("Home","/"),("Free Certification","/certification")]), faq_ld(faq)), active="/certification", priority="0.85")

def books_index():
    cards = "".join(book_card(b, "books") for b in BOOKS)
    items = [{"@type": "ListItem", "position": i + 1, "url": f'{U}/books/{b["slug"]}', "name": b["title"]} for i, b in enumerate(BOOKS)]
    free_items = {"@type": "ItemList", "name": "Free Bench Ready guides", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "Book", "name": f'{f["series"]}: {f["title"]}', "url": f["url"], "author": {"@id": U + "/about#person"},
         "numberOfPages": f["pages"], "bookFormat": "https://schema.org/EBook", "isAccessibleForFree": True, "description": f["desc"]}} for i, f in enumerate(FREE_BOOKS)]}
    body = f'''<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("Books","/books/")])}
<h1>Books and free guides</h1>
<p class="lead">Start with a free guide. When you want the full method, the books go deeper: technical handbooks with tested code and free tools, and clear, evidence-first science for general readers.</p>
</div></section>
<section class="sec-tight" id="free"><div class="wrap">
<div class="sec-head"><h2>Free guides</h2><p class="lead">Each one is a short book with an Excel workbook, printable pages and message templates. Downloads are delivered by our store on Gumroad at $0.</p></div>
{free_shelves("books")}</div></section>
<section class="sec" id="amazon"><div class="wrap">
<div class="sec-head-row"><div class="sec-head"><h2>On Amazon</h2><p class="lead">Kindle, paperback and hardcover.</p></div>
<a class="btn btn-ghost" href="{SITE["author_page"]}" target="_blank" rel="noopener" data-ev="amazon_click" data-label="author-page">Amazon author page {EXT}</a></div>
<div class="shelf">{cards}</div></div></section>
{newsletter("bench-notes-books")}'''
    page("/books/", "Books & Free Lab Guides by Suryaprakash Tripathy: Biotech, AI & Cancer Science | NexagenLabs",
         "Free Bench Ready lab guides and all books by Suryaprakash Tripathy: The Agentic Lab, AI for Biotech, The Working Laboratory, Demystifying Biotechnology, The Cancer Decade and The Machines That Read Us.",
         body, schema=ld(ORG, PERSON, crumbs_ld([("Home","/"),("Books","/books/")]), {"@type": "ItemList", "name": "Books", "itemListElement": items}, free_items), active="/books/", priority="0.9")

def res_link(kind, title, note, url, ev="open_tool", label=""):
    ext = url.startswith("http")
    return f'<a class="pick" href="{url}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""} data-ev="{ev}" data-label="{label or url}"><span class="what">{kind}</span><b>{e(title)}</b><span>{e(note)}</span></a>'

COMPANION = {
    "the-working-laboratory": {"guides": ["how-to-calculate-molarity","c1v1-c2v2-dilution-guide","serial-dilution-guide","how-to-prepare-buffers","percent-solutions-w-v-v-v","dna-concentration-ng-ul-to-nm"],
        "tools": [(n, BM + p, d) for n, p, d, _ in BENCHMATE_TOOLS[:5] + [BENCHMATE_TOOLS[9]]]},
    "demystifying-biotechnology": {"guides": ["how-to-prepare-buffers","serial-dilution-guide","dna-concentration-ng-ul-to-nm"], "tools": [(n, BM + p, d) for n, p, d, _ in [BENCHMATE_TOOLS[0], BENCHMATE_TOOLS[3], BENCHMATE_TOOLS[9]]]},
    "the-agentic-lab": {"guides": [], "tools": []},
    "ai-for-biotech": {"guides": ["dna-concentration-ng-ul-to-nm"], "tools": [(n, VH + p, d) for n, p, d, _ in VERIHELIX_TOOLS if p.strip("/").split("/")[-1] in ("citation-verifier", "prompt-lab", "structure-reader", "molecule-desk", "disclosure")]},
}
def companion_section(b):
    c = COMPANION.get(b["slug"], {"guides": [], "tools": []})
    cards = []
    if b["companion"]:
        label = {"lab.": "Companion code: tested builds for every chapter", "verihelix.": "VeriHelix: free AI-biotech workbench"}
        name = next((v for k, v in label.items() if k in b["companion"]), "BenchMate: free companion calculators")
        cards.append(res_link("Companion", name, b["companion"].replace("https://", "").rstrip("/"), b["companion"], label="companion-" + b["slug"]))
    for gs in c["guides"]:
        g = next(x for x in GUIDES if x["slug"] == gs)
        cards.append(res_link("Guide", g["short"], "Worked examples with a live calculator", f"/guides/{gs}", "open_guide"))
    for n, url, d in c["tools"]:
        cards.append(res_link("Tool", n, d, url, label=f'companion-{b["slug"]}'))
    res = f'<div class="res-grid">{"".join(cards)}</div>' if cards else '<p class="muted">Chapter resources for this title are being added. Use the form to ask for anything you need.</p>'
    fname = "reader-" + b["slug"]
    return f"""<section class="sec sec-alt" id="companion"><div class="wrap">
<div class="sec-head"><h2>For readers of {e(b["title"])}</h2>
<p class="lead">Free material that goes with the book. If you spot an error or have a question about a chapter, send it below. Corrections are listed here once confirmed.</p></div>
{res}
<div class="kit" style="margin-top:28px">
<div class="kit-copy"><h3 style="font-size:1.2rem">Errata and reader questions</h3><p class="muted">Found a mistake, a broken QR code or a confusing passage? Tell me the chapter and page. Every report is read, and confirmed corrections go into the next printing.</p>
<p class="fine mb-0">Confirmed errata: none listed yet.</p></div>
<form class="form kit-form" name="{fname}" method="POST" data-netlify="true" netlify-honeypot="company" action="/thanks" data-ok="Thank you. Your note is in and I'll look at it soon.">
<input type="hidden" name="form-name" value="{fname}"><input type="hidden" name="book" value="{e(b["title"])}"><p class="hp"><label>Company <input name="company"></label></p>
<div class="two"><div><label for="{fname}-type">Type</label><select id="{fname}-type" name="type"><option>Erratum</option><option>Question</option><option>Broken QR code or link</option><option>Suggestion</option></select></div>
<div><label for="{fname}-ch">Chapter / page</label><input id="{fname}-ch" name="where" placeholder="e.g. Ch 4, p 87"></div></div>
<div><label for="{fname}-msg">Details</label><textarea id="{fname}-msg" name="message" required style="min-height:110px"></textarea></div>
<div><label for="{fname}-em">Email (optional, for a reply)</label><input id="{fname}-em" type="email" name="email" autocomplete="email"></div>
<button class="btn btn-primary" type="submit">Send report</button><p class="fine form-status" role="status"></p>
</form></div></div></section>"""

def book_page(b):
    others = "".join(book_card(x, "related") for x in [x for x in BOOKS if x["slug"] != b["slug"]][:3])
    comp = f'<a class="btn btn-ghost" href="{b["companion"]}" target="_blank" rel="noopener" data-ev="open_tool" data-label="book-companion-{b["slug"]}">Free companion tool {EXT}</a>' if b["companion"] else ""
    path = f'/books/{b["slug"]}'
    schema = {"@type": "Book", "@id": U + path + "#book", "name": f'{b["title"]}: {b["subtitle"]}', "alternateName": b["title"],
              "author": {"@id": U + "/about#person"}, "image": b["cover"], "url": U + path, "inLanguage": "en",
              "description": b["summary"], "about": b["topic"], "datePublished": str(b["year"]),
              "sameAs": list(b["stores"].values()),
              "workExample": [{"@type": "Book", "bookFormat": "https://schema.org/EBook", "url": b["stores"]["us"], "identifier": {"@type": "PropertyValue", "propertyID": "ASIN", "value": b["asin"]}}]}
    for_list = "".join(f"<li>{e(x)}</li>" for x in b["for"])
    body = f'''<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("Books","/books/"),(b["title"], path)])}
<div class="book-detail">
{cover(b, eager=True)}
<div><span class="kicker">{e(b["topic"])}, {b["year"]}</span>
<h1>{e(b["title"])}</h1>
<p class="lead">{e(b["subtitle"])}</p>
<p class="byline"><img class="avatar" src="/assets/img/suryaprakash-tripathy-96.webp" alt="" width="40" height="40"><span>by <a href="/about">{e(AUTHOR)}</a>. {e(b["formats"].replace(" · ", ", "))}.</span></p>
<div class="actions" style="margin-bottom:34px">{explore_btn(b, "book-page", "btn btn-primary")}{comp}<a class="btn btn-ghost" href="#companion">Reader resources</a></div>
<div class="prose"><h2 style="margin-top:0">About this book</h2><p>{e(b["summary"])}</p>
<h3>Who it's for</h3><ul class="checklist">{for_list}</ul></div>
</div></div></div></section>
{companion_section(b)}
<section class="sec"><div class="wrap"><div class="sec-head-row"><div class="sec-head"><h2>More books</h2></div><a class="btn btn-ghost" href="/books/">All books and free guides</a></div><div class="shelf">{others}</div></div></section>
{newsletter("bench-notes-book")}'''
    page(path, f'{b["title"]}: Book by Suryaprakash Tripathy',
         f'{b["title"]} by Suryaprakash Tripathy. {b["summary"].split(". ")[0]}. Buy on Amazon US, UK and DE.',
         body, schema=ld(ORG, PERSON, schema, crumbs_ld([("Home","/"),("Books","/books/"),(b["title"], path)])), og_type="book", og_image=b["cover"].replace("_SL400_", "_SL600_"), active="/books/", priority="0.8")

def guides_index():
    body = f'''<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("Guides","/guides/")])}
<h1>Bench maths, explained properly.</h1>
<p class="lead">Worked examples for the calculations every lab runs. Each guide has a live calculator in the page, and links to the full BenchMate tool.</p></div></section>
<section class="sec-tight" style="padding-top:8px"><div class="wrap" style="max-width:900px">{guide_list(GUIDES)}</div></section>
{newsletter("bench-notes-guides")}'''
    page("/guides/", "Lab Calculation Guides: Molarity, Dilutions, Buffers & DNA Concentration | NexagenLabs",
         "Free lab calculation guides with worked examples: molarity, C1V1 dilutions, serial dilutions, buffer preparation, percent solutions and DNA ng/µL to nM conversion.",
         body, schema=ld(ORG, crumbs_ld([("Home","/"),("Guides","/guides/")])), active="/guides/", priority="0.85")

def guide_page(g):
    path = f'/guides/{g["slug"]}'
    toc = "".join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t in g["toc"])
    tool_name, tool_url = g["tool"]
    related = guide_list([x for x in GUIDES if x["slug"] != g["slug"]][:3])
    article = {"@type": "TechArticle", "@id": U + path + "#article", "headline": g["title"], "description": g["description"],
               "author": {"@id": U + "/about#person"}, "publisher": {"@id": U + "/#org"}, "datePublished": g["date"], "dateModified": g["date"],
               "mainEntityOfPage": U + path, "keywords": g["keywords"], "image": U + "/assets/img/og-default.jpg", "proficiencyLevel": "Beginner"}
    cta = f'<div class="console">{widget(GUIDE_WIDGET.get(g["slug"], "c1v1"))}</div>' + f'''<p class="fine" style="margin-top:-14px">Want saved recipes, more units and warnings? <a href="{tool_url}" target="_blank" rel="noopener" data-ev="open_benchmate" data-label="guide-{g["slug"]}">Open the full {e(tool_name)} in BenchMate</a>.</p>'''
    parts = g["body"].split("<h2", 3)
    body_html = ("<h2".join(parts[:3]) + cta + "<h2" + parts[3]) if len(parts) == 4 else g["body"] + cta
    fname = "kit-guide-aside"
    body = f'''<section class="page-hero" style="padding-bottom:6px"><div class="wrap">{crumbs_html([("Home","/"),("Guides","/guides/"),(g["short"], path)])}
<h1 style="max-width:22ch">{e(g["title"])}</h1>
<p class="byline"><img class="avatar" src="/assets/img/suryaprakash-tripathy-96.webp" alt="" width="40" height="40"><span>By <a href="/about">{e(AUTHOR)}</a>, M.Sc. Biotechnology. {g["minutes"]} min read. Updated <time datetime="{g["date"]}">{date.fromisoformat(g["date"]).strftime("%d %b %Y")}</time>.</span></p>
</div></section>
<section class="sec-tight" style="padding-top:6px"><div class="wrap article-layout">
<article class="prose">{body_html}
<h2 id="faq">Frequently asked questions</h2>{faq_html(g["faq"])}
<div class="cta-box"><div><strong>Go deeper: The Working Laboratory</strong><p>22 core bench techniques, from molarity to sterilisation. Volume 1 of The Biotechnology Techniques Bible.</p></div>
<a class="btn btn-ghost" href="/books/the-working-laboratory">See the book</a></div>
</article>
<aside>
<div class="aside-card toc-card"><h4>On this page</h4><ol>{toc}<li><a href="#faq">FAQ</a></li></ol></div>
<div class="aside-card"><h4>Free tool</h4><p>Check your numbers with the full calculator.</p><a class="btn btn-primary btn-sm" href="{tool_url}" target="_blank" rel="noopener" data-ev="open_benchmate" data-label="guide-aside-{g["slug"]}">{e(tool_name)} {EXT}</a></div>
<div class="aside-card"><h4>Print it</h4><p>This guide's cheat sheet is in the free Bench Starter Kit, with five others.</p>
<form class="signup" style="margin-top:0" name="{fname}" method="POST" data-netlify="true" netlify-honeypot="company" action="/kit-download" data-ok="Done. Your kit is ready." data-reveal="{fname}-{g["slug"]}">
<input type="hidden" name="form-name" value="{fname}"><input type="hidden" name="guide" value="{g["slug"]}"><p class="hp"><label>Company <input name="company"></label></p>
<input type="email" name="email" required placeholder="you@lab.edu" aria-label="Email for the Bench Starter Kit"><button class="btn btn-ghost btn-sm" type="submit">Get the kit</button>
<p class="fine form-status" role="status" style="width:100%"></p><a id="{fname}-{g["slug"]}" class="kit-link text-link" hidden href="{KIT}" download>Download the kit (PDF)</a></form></div>
</aside>
</div></section>
{rail("Keep reading", "", related, cls="sec sec-alt")}
{newsletter("bench-notes-guide")}'''
    page(path, g["title"], g["description"], body,
         schema=ld(ORG, PERSON, article, faq_ld(g["faq"]), crumbs_ld([("Home","/"),("Guides","/guides/"),(g["short"], path)])),
         og_type="article", active="/guides/", priority="0.8")

def profiles_html():
    return '<ul class="profiles">' + "".join(f'<li><a href="{u}" target="_blank" rel="noopener me" data-ev="profile_click" data-label="{e(n)}">{e(n)} {EXT}</a></li>' for n, u in PROFILES) + "</ul>"

def about():
    creds = "".join(f'<li><span class="n">{n}<small>{u}</small></span><span class="l">{e(l)}</span></li>' for n, u, l in CREDENTIALS)
    sites = "".join(f'<li><a class="guide-row" href="{p["page"] or p["url"]}"><h3>{e(p["name"])}</h3><span class="min">{e(p["kind"])}</span><p>{e(p["desc"])}</p></a></li>' for p in PROPERTIES)
    books = "".join(f'<li><a class="guide-row" href="/books/{b["slug"]}"><h3>{e(b["title"])}</h3><span class="min">{b["year"]}</span><p>{e(b["topic"])}</p></a></li>' for b in BOOKS)
    body = f'''<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("About","/about")])}
<div class="rail" style="align-items:center">
<div><img class="portrait portrait-lg" src="/assets/img/suryaprakash-tripathy.webp" alt="Portrait of {e(AUTHOR)}" width="168" height="168" fetchpriority="high"></div>
<div><h1>{e(AUTHOR)}</h1>
<p class="lead">Biotechnology researcher, author and builder of NexagenLabs. My work sits where wet-lab biology meets computation: cancer biology, computational drug discovery and filariasis, and now AI tools that scientists can actually check.</p>
<p class="muted" style="max-width:62ch">I build these tools because I needed them myself. Most bench errors I have seen were not hard science. They were a wrong molecular weight, a skipped unit conversion, or a buffer set at the wrong temperature. NexagenLabs exists to catch those before they cost someone a week.</p>
<div class="actions"><a class="btn btn-primary" href="/contact">Get in touch</a></div>
{profiles_html()}</div>
</div></div></section>
{rail("By the numbers", "Fellowship ranks, training and published work.", f'<ul class="creds">{creds}</ul>', cls="sec sec-alt")}
{rail("Training and research", "", """<ol class="timeline">
<li><b>M.Sc. Biotechnology, Pondicherry University</b><span>Graduated with a 9.0 CGPA.</span></li>
<li><b>National fellowships</b><span>ICMR-JRF (AIR 115), DBT-GATB (AIR 52) and GATE Biotechnology (AIR 820).</span></li>
<li><b>IAS-INSA-NASI Summer Research Fellow</b><span>Indian science academies' joint summer research fellowship.</span></li>
<li><b>Research at IISER Bhopal, IIT Guwahati and ICMR institutes</b><span>Cancer biology, glioblastoma and hypoxia, prime editing, computational drug discovery and filariasis.</span></li>
<li><b>Publications</b><span>14 book chapters and review articles with Elsevier and Springer Nature.</span></li>
<li><b>AI evaluation</b><span>Subject-matter expert for evaluating and training frontier AI models on biology and life-science reasoning.</span></li>
<li><b>Author</b><span>Six books on Amazon across bench techniques, AI for biotech, AI agents and cancer science.</span></li>
</ol>""")}
{rail("What I build", "Free tools, each one tied to a book that explains the method.", f'<ul class="list">{sites}</ul>', cls="sec sec-alt")}
{rail("What I write", "Six books on Amazon, and a free guide series for people new to the lab.", f'<ul class="list">{books}</ul><p style="margin-top:22px"><a class="btn btn-ghost" href="/books/">Books and free guides</a></p>')}
{newsletter("bench-notes-about")}'''
    profile = {"@type": "ProfilePage", "mainEntity": {"@id": U + "/about#person"}, "url": U + "/about"}
    page("/about", "Suryaprakash Tripathy: Biotechnology Researcher & Author | NexagenLabs",
         "Suryaprakash Tripathy: M.Sc. Biotechnology (Pondicherry University), ICMR-JRF, DBT-GATB and GATE BT ranks, research at IISER Bhopal, IIT Guwahati and ICMR, author of six books and founder of NexagenLabs.",
         body, schema=ld(ORG, PERSON, profile, crumbs_ld([("Home","/"),("About","/about")])), og_type="profile", active="/about", priority="0.7")

def contact():
    body = f'''<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("Contact","/contact")])}
<div class="rail">
<div><h1>Say hello.</h1>
<p class="lead">Found a bug in a calculator, want a buffer added, spotted an error in a book, or want to collaborate? Send a note. I read every message.</p>
<ul class="checklist"><li>Tool requests and bug reports</li><li>Book errata and reader questions</li><li>Research, teaching and collaboration enquiries</li></ul></div>
<div class="panel">
<form class="form" name="contact" method="POST" data-netlify="true" netlify-honeypot="company" action="/thanks" data-ok="Message sent. Expect a reply within a few days.">
<input type="hidden" name="form-name" value="contact"><p class="hp"><label>Company <input name="company"></label></p>
<div class="two"><div><label for="cn">Name</label><input id="cn" name="name" required autocomplete="name"></div>
<div><label for="ce">Email</label><input id="ce" type="email" name="email" required autocomplete="email"></div></div>
<div><label for="ct">Topic</label><select id="ct" name="topic"><option>BenchMate / tools</option><option>VeriHelix</option><option>Books and free guides</option><option>Collaboration</option><option>Other</option></select></div>
<div><label for="cm">Message</label><textarea id="cm" name="message" required></textarea></div>
<button class="btn btn-primary" type="submit">Send message</button>
<p class="fine form-status" role="status"></p>
</form></div>
</div></div></section>'''
    page("/contact", "Contact NexagenLabs", "Contact NexagenLabs and Suryaprakash Tripathy about BenchMate, VeriHelix, the books, bug reports or collaboration.",
         body, schema=ld(ORG, {"@type": "ContactPage", "url": U + "/contact"}), priority="0.5")

def privacy():
    body = f'''<section class="page-hero"><div class="wrap prose">{crumbs_html([("Home","/"),("Privacy","/privacy")])}
<h1>Privacy</h1><p class="muted">Last updated {date.today().strftime("%d %B %Y")}</p>
<h2>The short version</h2><p>No accounts, no ads, no selling data. The tools run in your browser.</p>
<h2>What we collect</h2>
<ul><li><strong>Forms.</strong> If you subscribe to Bench Notes or send a message, we receive what you type (email, and name and message for contact). Forms are processed by Netlify, our host. We use it only to reply or to send Bench Notes.</li>
<li><strong>Analytics, only with consent.</strong> If you click "Accept analytics", Google Analytics 4 sets cookies to count visits and clicks, with IP anonymisation. If you decline, no analytics script loads. Change your choice any time via "Cookie settings" in the footer.</li>
<li><strong>Server logs.</strong> Netlify keeps standard request logs for security and reliability.</li>
<li><strong>BenchMate.</strong> Calculations and the Reagent Log stay in your browser's local storage on your device.</li>
<li><strong>Display preference.</strong> If you switch between the dark and light theme, that choice is saved in your browser so the site remembers it. It is not sent anywhere.</li></ul>
<h2>Free guides</h2><p>The Bench Ready guides are delivered by Gumroad at books.nexagenlabs.com. If you download one, Gumroad's privacy policy applies to what you enter there.</p>
<h2>Amazon links</h2><p>Book buttons link to Amazon. Once you are on Amazon, Amazon's privacy policy applies.</p>
<h2>Your rights</h2><p>To see, correct or delete anything you sent us, or to unsubscribe, use the <a href="/contact">contact form</a> or the unsubscribe link in any email. If you are in the EU or UK, you have rights under GDPR and UK GDPR, including the right to complain to your data protection authority.</p>
<h2>Controller</h2><p>NexagenLabs, operated by {e(AUTHOR)}, {e(SITE["location"])}.</p>
</div></section>'''
    page("/privacy", "Privacy Policy | NexagenLabs", "How NexagenLabs handles data: no accounts or ads, consent-based analytics, and forms processed by Netlify.", body, priority="0.2")

def thanks():
    body = f'''<section class="page-hero"><div class="wrap center" style="max-width:640px">
<h1>Thank you.</h1><p class="lead" style="margin-inline:auto">Your submission is in. While you're here, the tools are one click away.</p>
<div class="actions" style="justify-content:center"><a class="btn btn-primary" href="{BM}/">Open BenchMate</a><a class="btn btn-ghost" href="/guides/">Read a guide</a></div></div></section>'''
    page("/thanks", "Thank you | NexagenLabs", "Thanks for getting in touch with NexagenLabs.", body, noindex=True)

def notfound():
    body = f'''<section class="page-hero"><div class="wrap center" style="max-width:640px">
<h1>This page isn't on the bench.</h1>
<p class="lead" style="margin-inline:auto">The link may be old, or the page has moved. Search the site with Ctrl K, or start from one of these.</p>
<div class="actions" style="justify-content:center"><a class="btn btn-primary" href="/">Home</a><a class="btn btn-ghost" href="/tools">All tools</a><a class="btn btn-ghost" href="/books/">Books and free guides</a></div></div></section>'''
    page("/404.html", "Page not found | NexagenLabs", "The page you were looking for isn't here.", body, noindex=True)

KIT_ITEMS = [("Molarity and mass", "mass = M × V × MW, hydrate MWs for common salts, purity correction."),
             ("C1V1 dilutions", "Rearranged forms, unit-match table, when to do an intermediate dilution."),
             ("Serial dilutions and CFU", "Dilution factor, 10-fold and 2-fold plate layouts, CFU/mL back-calculation."),
             ("Buffers", "pKa table for common buffers, 1X PBS recipe with hydrate swaps, Tris temperature shift."),
             ("Percent solutions", "w/v, v/v, w/w, percent to molarity, 70% ethanol, concentrated acid molarity."),
             ("Nucleic acids", "A260 factors, purity ratios, ng/µL to nM and copies, ligation insert maths.")]
def starter_kit():
    items = "".join(f'<li><div class="guide-row"><h3>{e(t)}</h3><span class="min">1 page</span><p>{e(d)}</p></div></li>' for t, d in KIT_ITEMS)
    body = f"""<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("Bench Starter Kit","/starter-kit")])}
<h1>The Bench Starter Kit</h1>
<p class="lead">Six one-page cheat sheets for the calculations you do every week. Print them, pin them above the bench, stop re-deriving C1V1 at 7 pm.</p></div></section>
{rail("What's on each sheet", "Built from the NexagenLabs guides and checked against the same numbers BenchMate uses.", f'<ul class="list">{items}</ul>', cls="sec-tight")}
{newsletter("starter-kit")}"""
    page("/starter-kit", "Free Bench Starter Kit: Lab Calculation Cheat Sheets (PDF) | NexagenLabs",
         "Free printable lab cheat sheets: molarity, C1V1, serial dilution and CFU, buffer pKa table and PBS recipe, percent solutions and DNA ng/µL to nM.",
         body, schema=ld(ORG, crumbs_ld([("Home","/"),("Bench Starter Kit","/starter-kit")])), priority="0.7")

def kit_download():
    body = f"""<section class="page-hero"><div class="wrap center" style="max-width:640px"><h1>Your Bench Starter Kit</h1>
<p class="lead" style="margin-inline:auto">Thanks for signing up. Download the kit below. The first Bench Note arrives next month.</p>
<div class="actions" style="justify-content:center"><a class="btn btn-primary" href="{KIT}" download>{icon("down")} Download PDF</a><a class="btn btn-ghost" href="{BM}/">Open BenchMate</a></div></div></section>"""
    page("/kit-download", "Your Bench Starter Kit | NexagenLabs", "Download the NexagenLabs Bench Starter Kit.", body, noindex=True)

def search_items():
    items = []
    add = lambda **k: items.append(k)
    for path, title, d, f in [("/tools", "All tools", "Directory of every NexagenLabs tool", 1), ("/benchmate", "BenchMate overview", "Free lab calculator suite", 1),
                              ("/verihelix", "VeriHelix overview", "Free AI-biotech workbench", 1), ("/books/", "Books and free guides", "Free Bench Ready guides and six books", 1),
                              ("/guides/", "All guides", "Lab calculation guides", 1), ("/starter-kit", "Bench Starter Kit (free PDF)", "Printable lab cheat sheets", 1),
                              ("/certification", "Free Certification", "Free certificates from BenchMate and VeriHelix", 1),
                              ("/", "Home", "NexagenLabs research tools hub", 0), ("/about", "About Suryaprakash Tripathy", "Founder, credentials, research", 0),
                              ("/contact", "Contact", "Questions, bugs, collaboration", 0), ("/privacy", "Privacy", "How data is handled", 0)]:
        add(t=title, u=path, d=d, k="Page", f=f, w=1)
    for n, pth, d, cat in BENCHMATE_TOOLS:
        add(t=n, u=BM + pth, d=d, k="BenchMate", x="calculator tool " + cat, w=2, f=1 if pth in ("/molarity", "/buffer") else 0)
    for n, pth, d, _ in VERIHELIX_TOOLS:
        add(t=n, u=VH + pth, d=d, k="VeriHelix", x="ai tool " + dict(VERIHELIX_GROUPS)[_], w=2, f=1 if "citation" in pth else 0)
    for p_ in PROPERTIES:
        add(t=p_["name"], u=p_["url"], d=p_["desc"], k="Site", x=p_["kind"], w=1)
    for n, h, t, kind, u in BM_CERTS:
        add(t=n + " certificate" + (" (coming soon)" if kind == "habit" else ""), u=u, d=h, k="Certificate", x="certificate certification quiz free benchmate " + t, w=1)
    for n, h, t, u in VH_CERTS:
        add(t=n + " certificate", u=u, d=h, k="Certificate", x="certificate certification quiz free verihelix track " + t, w=1)
    for fb in FREE_BOOKS:
        add(t=fb["title"], u=fb["url"], d=f'{fb["series"]}. {fb["desc"]}', k="Free guide", x="free pdf download bench ready " + fb["for"], w=2)
    for g in GUIDES:
        add(t=g["title"], u=f"/guides/{g['slug']}", d=g["description"], k="Guide", x=g["keywords"], w=2, f=0)
        for i, t in g["toc"]:
            add(t=t, u=f"/guides/{g['slug']}#{i}", d=g["short"], k="Section", x=g["keywords"], w=0)
        for q, a in g["faq"]:
            add(t=q, u=f"/guides/{g['slug']}#faq", d=a[:120], k="FAQ", x=g["keywords"], w=0)
    for b in BOOKS:
        add(t=b["title"], u=f"/books/{b['slug']}", d=b["subtitle"], k="Book", x=b["topic"] + " " + b["summary"][:200], w=2)
    return items

# ------------------------------------------------------------------ SEO files
def seo_files():
    urls = "".join(f'<url><loc>{U}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>' for p, pr in PAGES)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /thanks\n\nSitemap: {U}/sitemap.xml\nSitemap: {BM}/sitemap.xml\n")
    items = "".join(f'<item><title>{e(g["title"])}</title><link>{U}/guides/{g["slug"]}</link><guid>{U}/guides/{g["slug"]}</guid><pubDate>{date.fromisoformat(g["date"]).strftime("%a, %d %b %Y")} 00:00:00 +0000</pubDate><description>{e(g["description"])}</description></item>' for g in GUIDES)
    write("/guides/feed.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>NexagenLabs Guides</title><link>{U}/guides/</link><description>Lab calculation guides</description>{items}</channel></rss>\n')
    write("/site.webmanifest", json.dumps({"name": "NexagenLabs", "short_name": "NexagenLabs", "start_url": "/", "display": "standalone",
        "background_color": "#070c17", "theme_color": "#070c17",
        "icons": [{"src": "/assets/img/logo-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/logo-512.png", "sizes": "512x512", "type": "image/png"}]}))
    # llms.txt: helps AI assistants describe the site accurately
    lines = ["# NexagenLabs", "", f"> {SITE['tagline']}", "", "## Sites"] + [f"- [{p['name']}]({p['url']}): {p['desc']}" for p in PROPERTIES] + \
        ["", "## BenchMate tools"] + [f"- [{n}]({BM}{p}): {d}" for n, p, d, _ in BENCHMATE_TOOLS] + \
        ["", "## VeriHelix tools"] + [f"- [{n}]({VH}{p}): {d}" for n, p, d, _ in VERIHELIX_TOOLS] + \
        ["", "## Guides"] + [f"- [{g['title']}]({U}/guides/{g['slug']}): {g['description']}" for g in GUIDES] + \
        ["", "## Free guides"] + [f"- [{f['series']}: {f['title']}]({f['url']}): {f['desc']}" for f in FREE_BOOKS] + \
        ["", "## Books"] + [f"- [{b['title']}: {b['subtitle']}]({U}/books/{b['slug']})" for b in BOOKS] + \
        ["", "## About", f"- [{AUTHOR}]({U}/about): biotechnology researcher and author; founder of NexagenLabs."]
    write("/llms.txt", "\n".join(lines) + "\n")

def static():
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"), dirs_exist_ok=True)
    if PREVIEW:
        return
    for f in [f for f in os.listdir(os.path.join(ROOT, "static")) if f.endswith(".txt")] + ["favicon.ico", "favicon-32.png", "favicon-48.png", "apple-touch-icon.png", "_redirects", "_headers"]:
        sp = os.path.join(ROOT, "static", f)
        if os.path.exists(sp):
            shutil.copy(sp, os.path.join(OUT, f))

# ------------------------------------------------------------------ preview bundle (one HTML file, hash-routed)
def pv_id(path):
    return "home" if path == "/" else path.strip("/").replace(".html", "").replace("/", "-")

def preview_bundle():
    ids = {p: pv_id(p) for p, *_ in RENDERED}
    def fix(m):
        attr, target, frag = m.group(1), m.group(2), m.group(3) or ""
        if target in ids:
            scroll = f' data-scroll="{frag[1:]}"' if frag else ""
            return f'{attr}="#{ids[target]}"{scroll}'
        if target.startswith("/assets/"):
            return f'{attr}="{target[1:]}{frag}"'
        return m.group(0)
    rx = re.compile(r'(href|src)="(/[^"#]*)(#[^"]*)?"')
    sections = ""
    for path, title, body, active in RENDERED:
        sections += f'<div data-page="{ids[path]}" data-title="{e(title)}" data-active="{ids.get(active, "") if active else ""}" hidden>{rx.sub(fix, body)}</div>\n'
    shell = rx.sub(fix, header_html() + '\n<main id="main">\n' + sections + "</main>\n" + footer() + "\n" + chrome_html())
    idx = [dict(it, u=("#" + ids[it["u"].split("#")[0]]) if it["u"].split("#")[0] in ids else it["u"]) for it in search_items()]
    doc = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark" data-ga="">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NexagenLabs redesign preview</title>
{THEME_BOOT}
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
{shell}
<script>window.NX_PREVIEW=true;window.NX_IDX={json.dumps(idx, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")};</script>
<script src="assets/js/site.js" defer></script>
</body>
</html>'''
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)

if __name__ == "__main__":
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    home(); tools(); benchmate(); verihelix(); certification(); books_index()
    for b in BOOKS: book_page(b)
    guides_index()
    for g in GUIDES: guide_page(g)
    about(); contact(); privacy(); thanks(); notfound(); starter_kit(); kit_download()
    static()
    if PREVIEW:
        preview_bundle()
        print(f"Preview bundle with {len(RENDERED)} pages → {OUT}")
    else:
        write("/search-index.json", json.dumps(search_items(), ensure_ascii=False, separators=(",", ":")))
        seo_files()
        print(f"Built {len(PAGES)} indexable pages → {OUT}")
