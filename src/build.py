#!/usr/bin/env python3
"""Static site generator for nexagenlabs.com. Output: ../public"""
import json, os, re, shutil, html
from datetime import date
from data import SITE, BM, BENCHMATE_TOOLS, PROPERTIES, BOOKS, CREDENTIALS
from guides import GUIDES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")
U = SITE["url"]
TODAY = date.today().isoformat()
PAGES = []  # (path, priority) for sitemap
e = html.escape

# ------------------------------------------------------------------ icons
ICONS = {
 "flask": '<path d="M9 3h6M10 3v6.5L4.6 18.2A2 2 0 0 0 6.3 21h11.4a2 2 0 0 0 1.7-2.8L14 9.5V3"/><path d="M7.5 15h9"/>',
 "agent": '<rect x="4" y="7" width="16" height="12" rx="3"/><path d="M12 3v4M9 12h.01M15 12h.01M9 16h6"/>',
 "molecule": '<circle cx="6" cy="7" r="2.2"/><circle cx="18" cy="7" r="2.2"/><circle cx="12" cy="17" r="2.2"/><path d="M8 8l3 7M16 8l-3 7M8.2 7h7.6"/>',
 "code": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
 "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/>',
 "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5z"/><path d="M4 19a2 2 0 0 1 2-2h13"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "ext": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
 "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01"/>',
 "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
}
def icon(name, cls=""):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" class="{cls}">{ICONS[name]}</svg>'

LOGO = '<img class="brand-mark" src="/assets/img/logo-mark-96.webp" alt="" width="34" height="34">'

NAV = [("/tools", "Tools"), ("/benchmate", "BenchMate"), ("/books/", "Books"), ("/guides/", "Guides"), ("/about", "About"), ("/contact", "Contact")]

# ------------------------------------------------------------------ JSON-LD helpers
ORG = {"@type": "Organization", "@id": U + "/#org", "name": "NexagenLabs", "url": U + "/",
       "logo": U + "/assets/img/logo-512.png", "description": SITE["tagline"],
       "founder": {"@id": U + "/about#person"}, "sameAs": [SITE["author_page"]]}
PERSON = {"@type": "Person", "@id": U + "/about#person", "name": SITE["founder"], "url": U + "/about",
          "jobTitle": "Biotechnology researcher and author", "image": U + "/assets/img/suryaprakash-tripathy.jpg",
          "alumniOf": {"@type": "CollegeOrUniversity", "name": "Pondicherry University"},
          "knowsAbout": ["Biotechnology", "Cancer biology", "Computational drug discovery", "Molecular docking", "AI for life sciences", "Laboratory techniques"],
          "worksFor": {"@id": U + "/#org"}, "sameAs": [SITE["author_page"]]}

def ld(*objs):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": list(objs)}, ensure_ascii=False) + "</script>"

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": U + p} for i, (n, p) in enumerate(items)]}

def crumbs_html(items):
    parts = [f'<a href="{p}">{e(n)}</a>' for n, p in items[:-1]] + [f'<span aria-current="page">{e(items[-1][0])}</span>']
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' &nbsp;/&nbsp; '.join(parts) + '</nav>'

# ------------------------------------------------------------------ layout
def page(path, title, desc, body, *, schema="", og_type="website", og_image=None, active=None, priority="0.7", noindex=False):
    canonical = U + path
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    og_image = og_image or U + "/assets/img/og-default.jpg"
    nav = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if active == h else ""}>{n}</a></li>' for h, n in NAV)
    gsc = f'<meta name="google-site-verification" content="{SITE["gsc_verification"]}">' if SITE["gsc_verification"] else ""
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    doc = f'''<!doctype html>
<html lang="en" data-ga="{SITE["ga_id"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
{robots}
<meta name="theme-color" content="#060a11">
<meta name="color-scheme" content="dark">
<meta property="og:site_name" content="NexagenLabs">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_image}">
{gsc}
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/space-grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preconnect" href="https://m.media-amazon.com">
<link rel="stylesheet" href="/assets/css/site.css?v={TODAY}">
<link rel="alternate" type="application/rss+xml" title="NexagenLabs Guides" href="/guides/feed.xml">
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap nav">
<a class="brand" href="/" aria-label="NexagenLabs home">{LOGO}<span>Nexagen<b>Labs</b></span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav-links" aria-label="Menu">{icon("menu")}</button>
<ul class="nav-links" id="nav-links">{nav}</ul>
<a class="btn btn-primary btn-sm nav-cta" href="{BM}/" data-ev="open_benchmate" data-label="header">Open BenchMate {icon("arrow")}</a>
</div></header>
<main id="main">
{body}
</main>
{footer()}
<div class="consent" id="consent" role="dialog" aria-label="Cookie preferences">
<p>We use Google Analytics cookies, only if you agree, to see which tools and guides help people most. No ads, no selling data. <a href="/privacy">Privacy</a></p>
<div class="row"><button class="btn btn-primary btn-sm" data-consent="yes">Accept analytics</button><button class="btn btn-ghost btn-sm" data-consent="no">Decline</button></div>
</div>
<script src="/assets/js/site.js?v={TODAY}" defer></script>
</body>
</html>'''
    write(path, doc)
    if not noindex:
        PAGES.append((path, priority))

def footer():
    tools = "".join(f'<li><a href="{p["url"]}">{e(p["name"].split(": ")[0])}</a></li>' for p in PROPERTIES)
    guides = "".join(f'<li><a href="/guides/{g["slug"]}">{e(g["short"])}</a></li>' for g in GUIDES[:5])
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="/">{LOGO}<span>Nexagen<b>Labs</b></span></a>
<p class="muted" style="margin-top:14px;max-width:340px;font-size:.92rem">{e(SITE["tagline"])} Built and maintained by {e(SITE["founder"])}.</p>
<form class="signup" name="bench-notes-footer" method="POST" data-netlify="true" netlify-honeypot="company" action="/thanks" data-ok="You're on the list. First Bench Note arrives soon.">
<input type="hidden" name="form-name" value="bench-notes-footer"><p class="hp"><label>Company <input name="company"></label></p>
<input type="email" name="email" required placeholder="you@lab.edu" aria-label="Email for Bench Notes"><button class="btn btn-primary btn-sm" type="submit">Get Bench Notes</button>
<p class="fine form-status" role="status" style="width:100%"></p></form></div>
<div><h4>Tools</h4><ul>{tools}<li><a href="/tools">All tools →</a></li></ul></div>
<div><h4>Guides</h4><ul>{guides}<li><a href="/guides/">All guides →</a></li></ul></div>
<div><h4>NexagenLabs</h4><ul><li><a href="/books/">Books</a></li><li><a href="/about">About the founder</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy">Privacy</a></li><li><a href="#" id="cookie-settings">Cookie settings</a></li></ul></div>
</div>
<div class="foot-base"><span>© <span id="year">{date.today().year}</span> NexagenLabs · {e(SITE["location"])}</span><span class="mono">Free tools. No login. No ads.</span></div>
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
def prop_card(p, cls=""):
    tone = p["tone"]
    book = ""
    if p.get("book"):
        b = next(x for x in BOOKS if x["slug"] == p["book"])
        book = f'Companion to <a href="/books/{b["slug"]}" style="position:relative;z-index:2">{e(b["title"])}</a>'
    elif p.get("book_title"):
        book = f'Companion to {e(p["book_title"])}'
    return f'''<article class="card {cls}" data-cat="{p["cats"]}">
<div class="icon {tone}">{icon(p["icon"])}</div>
<div class="tags"><span class="tag live">● Live</span><span class="tag">{e(p["kind"])}</span></div>
<h3><a href="{p["url"]}" data-ev="open_tool" data-label="{p["slug"]}">{e(p["name"])}</a></h3>
<p>{e(p["desc"])}</p>
<div class="meta"><span>{book}</span><span class="go">Open {icon("ext")}</span></div>
</article>'''

def store_buttons(b, where):
    s = b["stores"]
    t = e(b["title"])
    def btn(key, label, store):
        return (f'<a class="store" href="{s[key]}" target="_blank" rel="noopener" data-ev="amazon_click" '
                f'data-label="{b["slug"]}|{key}|{where}" aria-label="Explore {t} on {store}">'
                f'<span class="glow" aria-hidden="true"></span>Explore<span class="sep">·</span><b>{label}</b></a>')
    return ('<div class="stores">' + btn("us", "USA", "Amazon.com") + btn("uk", "UK", "Amazon.co.uk")
            + btn("de", "Germany", "Amazon.de") + '</div>')

def book_card(b, where="grid"):
    return f'''<article class="book reveal">
<a class="book-cover" href="/books/{b["slug"]}" aria-label="{e(b["title"])} details"><img src="{b["cover"]}" alt="Cover of {e(b["title"])} by Suryaprakash Tripathy" loading="lazy" decoding="async" width="400" height="600"></a>
<div class="book-body">
<div class="tags"><span class="tag">{e(b["topic"])}</span></div>
<h3><a href="/books/{b["slug"]}">{e(b["title"])}</a></h3>
<p class="sub">{e(b["subtitle"])}</p>
{store_buttons(b, where)}
</div></article>'''

def guide_card(g):
    return f'''<article class="card reveal" data-cat="guide">
<div class="icon amber">{icon("doc")}</div>
<div class="tags"><span class="tag">Guide</span><span class="tag">{g["minutes"]} min read</span></div>
<h3><a href="/guides/{g["slug"]}">{e(g["title"].split(":")[0])}</a></h3>
<p>{e(g["description"].split(". Free")[0].rstrip("."))}.</p>
<div class="meta"><span>Uses: {e(g["tool"][0])}</span><span class="go">Read {icon("arrow")}</span></div>
</article>'''

def newsletter(name="bench-notes"):
    return f'''<section><div class="wrap"><div class="newsletter reveal">
<div><span class="eyebrow">Bench Notes</span><h2>One useful bench tip a month.</h2>
<p class="lead mb-0">A short email with a technique that people quietly get wrong, a new BenchMate tool, or a new book chapter. No spam. Unsubscribe in one click.</p></div>
<form class="form" name="{name}" method="POST" data-netlify="true" netlify-honeypot="company" action="/thanks" data-ok="You're on the list. First Bench Note arrives soon.">
<input type="hidden" name="form-name" value="{name}"><p class="hp"><label>Company <input name="company"></label></p>
<div><label for="{name}-email">Email</label><input id="{name}-email" type="email" name="email" required placeholder="you@lab.edu" autocomplete="email"></div>
<div><label for="{name}-role">I am a…</label><select id="{name}-role" name="role"><option>BS / undergraduate student</option><option>MS student</option><option>PhD student</option><option>Postdoc / scientist</option><option>Lab manager / technician</option><option>Industry R&amp;D</option><option>Other</option></select></div>
<button class="btn btn-primary" type="submit">Subscribe {icon("arrow")}</button>
<p class="fine form-status" role="status">We store your email only to send Bench Notes. See <a href="/privacy">privacy</a>.</p>
</form></div></div></section>'''

def faq_html(items):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items) + '</div>'

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

# ------------------------------------------------------------------ pages
def home():
    props = "".join(prop_card(p, "reveal") for p in PROPERTIES)
    chips = "".join(f'<a class="toolchip" href="{BM}{path}" data-ev="open_benchmate" data-label="home-chip{path}"><span class="dot"></span><span>{e(n)}<small>{e(d.split(".")[0])}</small></span></a>' for n, path, d, _ in BENCHMATE_TOOLS[:8])
    books = "".join(book_card(b, "home") for b in BOOKS)
    guides = "".join(guide_card(g) for g in GUIDES[:3])
    creds = "".join(f'<div class="cred"><div class="n">{n}<small>{u}</small></div><div class="l">{e(l)}</div></div>' for n, u, l in CREDENTIALS[:3])
    faq = [
        ("Is everything on NexagenLabs free?", "Yes. BenchMate and every companion site are free to use with no login. The books are sold on Amazon; the tools work without them."),
        ("Does BenchMate store my data?", "No. Calculations run in your browser. The Reagent Log saves recipes only in your own browser storage, never on a server."),
        ("Who builds these tools?", "Suryaprakash Tripathy, a biotechnology researcher with an M.Sc. from Pondicherry University, national fellowships (ICMR-JRF, DBT-GATB, GATE BT), and research work at IISER Bhopal, IIT Guwahati and ICMR institutes."),
        ("Which countries can buy the books?", "Every title is on Amazon.com, Amazon.co.uk and Amazon.de, plus other Amazon stores, in Kindle and print editions."),
    ]
    body = f'''
<section class="hero"><div class="wrap hero-grid">
<div>
<span class="eyebrow">Research tools hub · free · no login</span>
<h1>Bench-tested tools for <span class="grad">the people who do the science.</span></h1>
<p class="lead">Calculators, companion code and field-tested guides for wet-lab and computational biologists. Built by a working researcher, checked against real protocols, free to use.</p>
<div class="hero-actions">
<a class="btn btn-primary" href="{BM}/" data-ev="open_benchmate" data-label="hero">Open BenchMate {icon("arrow")}</a>
<a class="btn btn-ghost" href="/tools">Explore all tools</a>
</div>
<div class="stats">
<div class="stat"><b>12</b><span>bench tools</span></div>
<div class="stat"><b>370</b><span>verified compounds</span></div>
<div class="stat"><b>40</b><span>buffer recipes</span></div>
<div class="stat"><b>6</b><span>books</span></div>
</div>
</div>
<div class="panel reveal" id="c1v1" aria-label="Live C1V1 dilution calculator">
<div class="panel-bar"><i></i><i></i><i></i>&nbsp; BENCHMATE / C1V1 DILUTION<span class="live">● LIVE</span></div>
<div class="panel-body">
<div class="calc-row">
<div class="field"><label for="c1">Stock (C₁)</label><div class="ctl"><input id="c1" inputmode="decimal" value="1"><select id="c1u" aria-label="C1 unit"><option>M</option><option selected>mM</option><option>µM</option><option>nM</option></select></div></div>
<div class="field"><label for="c2">Final (C₂)</label><div class="ctl"><input id="c2" inputmode="decimal" value="50"><select id="c2u" aria-label="C2 unit"><option>M</option><option>mM</option><option selected>µM</option><option>nM</option></select></div></div>
</div>
<div class="field"><label for="v2">Final volume (V₂)</label><div class="ctl"><input id="v2" inputmode="decimal" value="10"><select id="v2u" aria-label="V2 unit"><option>L</option><option selected>mL</option><option>µL</option></select></div></div>
<div class="readout" aria-live="polite"><div class="k">Volume of stock to add</div><div class="v" id="out">…</div><div class="s" id="sub"></div></div>
</div>
<div class="panel-foot"><span class="mono">C₁V₁ = C₂V₂ · runs in your browser</span><a href="{BM}/molarity" data-ev="open_benchmate" data-label="hero-panel">Full calculator →</a></div>
</div>
</div></section>

<section style="padding-top:40px"><div class="wrap">
<div class="split"><div class="section-head"><span class="eyebrow">The ecosystem</span><h2>Free tools, each tied to a book.</h2>
<p class="lead mb-0">Each tool solves one job well, and each links to the book that explains the science behind it.</p></div>
<a class="btn btn-ghost" href="/tools">Tool directory {icon("arrow")}</a></div>
<div class="grid g-2">{props}</div>
</div></section>

<section><div class="wrap"><div class="feature reveal">
<div><span class="eyebrow">Flagship · BenchMate</span><h2>The bench scientist's calculator.</h2>
<p class="lead">Molarity, dilutions, buffers and percent solutions, done right the first time. Offline-ready, no login, nothing to install.</p>
<ul class="checklist"><li>Verified molecular weights for 370 compounds, hydrates included</li><li>40 buffer recipes scaled to any volume and pH</li><li>Recipe audit that flags likely bench errors before you pipette</li><li>Technique quiz with a Bench Fundamentals certificate</li></ul>
<div class="hero-actions mb-0"><a class="btn btn-primary" href="{BM}/" data-ev="open_benchmate" data-label="feature">Open BenchMate {icon("arrow")}</a><a class="btn btn-ghost" href="/benchmate">What's inside</a></div></div>
<div class="toolchips">{chips}</div>
</div></div></section>

<section><div class="wrap">
<div class="split"><div class="section-head"><span class="eyebrow">Guides</span><h2>Learn the math behind the tools.</h2>
<p class="lead mb-0">Plain-language guides for the calculations every lab runs, each with worked examples and a free calculator.</p></div>
<a class="btn btn-ghost" href="/guides/">All guides {icon("arrow")}</a></div>
<div class="grid g-3">{guides}</div>
</div></section>

<section><div class="wrap">
<div class="split"><div class="section-head"><span class="eyebrow">Books</span><h2>Written at the bench, for the bench.</h2>
<p class="lead mb-0">Technical handbooks for researchers and clear science for everyone else. Available on Amazon in the US, UK and Germany.</p></div>
<a class="btn btn-ghost" href="/books/">All books {icon("arrow")}</a></div>
<div class="books">{books}</div>
</div></section>

<section><div class="wrap"><div class="feature reveal">
<div><div class="founder-row"><img class="portrait-sm" src="/assets/img/suryaprakash-tripathy.webp" alt="Suryaprakash Tripathy" width="88" height="88" loading="lazy"><span class="eyebrow mb-0">The founder</span></div><h2>Built by a researcher, not a marketing team.</h2>
<p class="lead">Suryaprakash Tripathy is a biotechnology researcher working across cancer biology, computational drug discovery and filariasis, with research stints at IISER Bhopal, IIT Guwahati and ICMR institutes.</p>
<a class="btn btn-ghost" href="/about">Read the full profile {icon("arrow")}</a></div>
<div class="cred-grid one">{creds}</div>
</div></div></section>

{newsletter("bench-notes")}

<section><div class="wrap" style="max-width:860px"><div class="section-head"><span class="eyebrow">FAQ</span><h2>Quick answers</h2></div>{faq_html(faq)}</div></section>
'''
    website = {"@type": "WebSite", "@id": U + "/#website", "url": U + "/", "name": "NexagenLabs", "publisher": {"@id": U + "/#org"}}
    page("/", "NexagenLabs: Free Lab Calculators, Research Tools & Guides for Scientists",
         "Free research tools for scientists: BenchMate lab calculators (molarity, dilution, buffers), AI-agent and docking companion code, evidence registers, guides and books by Suryaprakash Tripathy.",
         body, schema=ld(ORG, PERSON, website, faq_ld(faq)), priority="1.0")

def tools():
    cards = "".join(prop_card(p) for p in PROPERTIES)
    bm_cards = "".join(f'''<article class="card" data-cat="bench calculators {cat}">
<div class="icon">{icon("calc")}</div><div class="tags"><span class="tag live">● BenchMate</span></div>
<h3><a href="{BM}{path}" data-ev="open_benchmate" data-label="dir{path}">{e(n)}</a></h3><p>{e(d)}</p>
<div class="meta"><span>benchmate.nexagenlabs.com{path}</span><span class="go">Open {icon("ext")}</span></div></article>''' for n, path, d, cat in BENCHMATE_TOOLS)
    guide_cards = "".join(guide_card(g).replace(' reveal"', '"') for g in GUIDES)
    filters = [("all", "All"), ("bench", "Bench calculators"), ("ai", "AI & code"), ("companion", "Book companions"), ("guide", "Guides")]
    chips = "".join(f'<button class="chip" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{n}</button>' for k, n in filters)
    items = [{"@type": "ListItem", "position": i + 1, "url": p["url"], "name": p["name"]} for i, p in enumerate(PROPERTIES)]
    body = f'''<section class="page-hero"><div class="wrap">
{crumbs_html([("Home","/"),("Tools","/tools")])}
<span class="eyebrow">Tool directory</span><h1>Every NexagenLabs tool, in one place.</h1>
<p class="lead">Search across {len(PROPERTIES)} sites, {len(BENCHMATE_TOOLS)} BenchMate tools and {len(GUIDES)} guides. All free, no login.</p>
</div></section>
<section style="padding-top:10px"><div class="wrap">
<div class="filters"><label class="search">{icon("search")}<input id="dir-q" type="search" placeholder="Search: buffer, dilution, agents, molarity…" aria-label="Search tools"></label></div>
<div class="filters" role="group" aria-label="Filter by category">{chips}</div>
<div id="directory">
<h2 class="mono muted" style="font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;margin:10px 0 16px">Sites</h2>
<div class="grid g-3" style="margin-bottom:40px">{cards}</div>
<h2 class="mono muted" style="font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;margin:10px 0 16px">Inside BenchMate</h2>
<div class="grid g-3" style="margin-bottom:40px">{bm_cards}</div>
<h2 class="mono muted" style="font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;margin:10px 0 16px">Guides</h2>
<div class="grid g-3">{guide_cards}</div>
</div>
<p class="empty" id="dir-empty">No matches. Try a broader word, or <a href="/contact">suggest a tool</a>.</p>
</div></section>
{newsletter("bench-notes-tools")}'''
    page("/tools", "Free Research Tools for Scientists: Lab Calculators & Companion Code | NexagenLabs",
         "Directory of free NexagenLabs research tools: BenchMate molarity, dilution and buffer calculators, AI-agent and molecular docking companion code, and a cancer evidence register.",
         body, schema=ld(ORG, crumbs_ld([("Home","/"),("Tools","/tools")]), {"@type": "ItemList", "itemListElement": items}), active="/tools", priority="0.9")

def benchmate():
    rows = "".join(f'''<article class="card reveal"><div class="icon">{icon("calc")}</div>
<h3><a href="{BM}{p}" data-ev="open_benchmate" data-label="bm-page{p}">{e(n)}</a></h3><p>{e(d)}</p>
<div class="meta"><span>{p}</span><span class="go">Open {icon("ext")}</span></div></article>''' for n, p, d, _ in BENCHMATE_TOOLS)
    wl = next(b for b in BOOKS if b["slug"] == "the-working-laboratory")
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
           "author": {"@id": U + "/about#person"},
           "featureList": [n for n, *_ in BENCHMATE_TOOLS],
           "description": "Free, offline, no-login lab calculators for molarity, dilutions, buffers, percent solutions and unit conversion."}
    body = f'''<section class="hero"><div class="wrap hero-grid">
<div>{crumbs_html([("Home","/"),("BenchMate","/benchmate")])}
<span class="eyebrow">Free lab calculator · no login</span>
<h1>BenchMate: the <span class="grad">lab calculator</span> built for the bench.</h1>
<p class="lead">Molarity, C1V1 dilutions, serial dilutions, buffer recipes and percent solutions in one fast, offline-ready web app. Verified data, clear warnings, nothing to install.</p>
<div class="hero-actions"><a class="btn btn-primary" href="{BM}/" data-ev="open_benchmate" data-label="bm-hero">Open BenchMate {icon("arrow")}</a><a class="btn btn-ghost" href="#tools">See all {len(BENCHMATE_TOOLS)} tools</a></div>
<div class="stats"><div class="stat"><b>370</b><span>verified compounds</span></div><div class="stat"><b>40</b><span>buffers</span></div><div class="stat"><b>100</b><span>quiz questions</span></div><div class="stat"><b>0</b><span>logins</span></div></div>
</div>
<div class="panel reveal" id="c1v1" aria-label="Live C1V1 dilution calculator">
<div class="panel-bar"><i></i><i></i><i></i>&nbsp; TRY IT · C1V1<span class="live">● LIVE</span></div>
<div class="panel-body">
<div class="calc-row">
<div class="field"><label for="c1">Stock (C₁)</label><div class="ctl"><input id="c1" inputmode="decimal" value="10"><select id="c1u" aria-label="C1 unit"><option>M</option><option selected>mM</option><option>µM</option><option>nM</option></select></div></div>
<div class="field"><label for="c2">Final (C₂)</label><div class="ctl"><input id="c2" inputmode="decimal" value="100"><select id="c2u" aria-label="C2 unit"><option>M</option><option>mM</option><option selected>µM</option><option>nM</option></select></div></div>
</div>
<div class="field"><label for="v2">Final volume (V₂)</label><div class="ctl"><input id="v2" inputmode="decimal" value="1"><select id="v2u" aria-label="V2 unit"><option>L</option><option selected>mL</option><option>µL</option></select></div></div>
<div class="readout" aria-live="polite"><div class="k">Volume of stock to add</div><div class="v" id="out">…</div><div class="s" id="sub"></div></div>
</div>
<div class="panel-foot"><span class="mono">Full version: units, warnings, serial tables</span><a href="{BM}/molarity" data-ev="open_benchmate" data-label="bm-panel">Open →</a></div>
</div></div></section>
<section id="tools" style="padding-top:30px"><div class="wrap">
<div class="section-head"><span class="eyebrow">Inside BenchMate</span><h2>{len(BENCHMATE_TOOLS)} tools, one tab.</h2></div>
<div class="grid g-3">{rows}</div></div></section>
<section><div class="wrap"><div class="feature reveal">
<div><span class="eyebrow">Learn the why</span><h2>BenchMate is the calculator. The Working Laboratory is the manual.</h2>
<p class="lead">Volume 1 of The Biotechnology Techniques Bible covers 22 core techniques: units and concentration, solutions and dilutions, water and buffers, sterilisation and safety. Each chapter maps to a BenchMate tool.</p>
{store_buttons(wl, "benchmate-page")}</div>
<a class="book-cover" href="/books/the-working-laboratory" style="border-radius:16px;border:1px solid var(--line)"><img src="{wl["cover"]}" alt="Cover of The Working Laboratory" loading="lazy" width="400" height="600"></a>
</div></div></section>
<section><div class="wrap"><div class="section-head"><span class="eyebrow">Guides</span><h2>Worked examples for every tool</h2></div><div class="grid g-3">{"".join(guide_card(g) for g in GUIDES)}</div></div></section>
<section><div class="wrap" style="max-width:860px"><div class="section-head"><span class="eyebrow">FAQ</span><h2>BenchMate questions</h2></div>{faq_html(faq)}</div></section>
{newsletter("bench-notes-benchmate")}'''
    page("/benchmate", "BenchMate: Free Lab Calculator for Molarity, Dilutions & Buffers | NexagenLabs",
         "BenchMate is a free, offline, no-login lab calculator: molarity, C1V1 and serial dilutions, 40 buffer recipes, percent solutions, MW lookup for 370 compounds, and a technique quiz with certificate.",
         body, schema=ld(ORG, app, crumbs_ld([("Home","/"),("BenchMate","/benchmate")]), faq_ld(faq)), active="/benchmate", priority="0.95")

def books_index():
    cards = "".join(book_card(b, "books") for b in BOOKS)
    items = [{"@type": "ListItem", "position": i + 1, "url": f'{U}/books/{b["slug"]}', "name": b["title"]} for i, b in enumerate(BOOKS)]
    body = f'''<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("Books","/books/")])}
<span class="eyebrow">Books by Suryaprakash Tripathy</span><h1>Books for the bench, and for everyone else.</h1>
<p class="lead">Technical handbooks with tested companion code and free tools, plus clear, evidence-first science for general readers. Kindle, paperback and hardcover.</p>
<div class="hero-actions"><a class="btn btn-ghost" href="{SITE["author_page"]}" target="_blank" rel="noopener" data-ev="amazon_click" data-label="author-page">Amazon author page {icon("ext")}</a></div>
</div></section>
<section style="padding-top:10px"><div class="wrap"><div class="books">{cards}</div></div></section>
{newsletter("bench-notes-books")}'''
    page("/books/", "Books by Suryaprakash Tripathy: Biotech, AI & Cancer Science | NexagenLabs",
         "All books by Suryaprakash Tripathy: The Agentic Lab, AI for Biotech, The Working Laboratory, Demystifying Biotechnology, The Cancer Decade and The Machines That Read Us. Buy on Amazon US, UK and DE.",
         body, schema=ld(ORG, PERSON, crumbs_ld([("Home","/"),("Books","/books/")]), {"@type": "ItemList", "itemListElement": items}), active="/books/", priority="0.9")

def book_page(b):
    others = "".join(book_card(x, "related") for x in BOOKS if x["slug"] != b["slug"])[:]
    others = "".join(book_card(x, "related") for x in [x for x in BOOKS if x["slug"] != b["slug"]][:3])
    comp = f'<a class="btn btn-ghost" href="{b["companion"]}" data-ev="open_tool" data-label="book-companion-{b["slug"]}">Free companion tool {icon("ext")}</a>' if b["companion"] else ""
    path = f'/books/{b["slug"]}'
    schema = {"@type": "Book", "@id": U + path + "#book", "name": f'{b["title"]}: {b["subtitle"]}', "alternateName": b["title"],
              "author": {"@id": U + "/about#person"}, "image": b["cover"], "url": U + path, "inLanguage": "en",
              "description": b["summary"], "about": b["topic"], "datePublished": str(b["year"]),
              "sameAs": list(b["stores"].values()),
              "workExample": [{"@type": "Book", "bookFormat": "https://schema.org/EBook", "url": b["stores"]["us"], "identifier": {"@type": "PropertyValue", "propertyID": "ASIN", "value": b["asin"]}}]}
    for_list = "".join(f"<li>{e(x)}</li>" for x in b["for"])
    body = f'''<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("Books","/books/"),(b["title"], path)])}
<div class="book-detail">
<div class="book-cover"><img src="{b["cover"]}" alt="Cover of {e(b["title"])} by Suryaprakash Tripathy" width="400" height="600" fetchpriority="high"></div>
<div><span class="eyebrow">{e(b["topic"])} · {b["year"]}</span>
<h1 style="font-size:clamp(2rem,4.4vw,3.3rem)">{e(b["title"])}</h1>
<p class="lead">{e(b["subtitle"])}</p>
<p class="byline"><img class="avatar" src="/assets/img/suryaprakash-tripathy-96.webp" alt="Suryaprakash Tripathy" width="40" height="40"><span>by <a href="/about">Suryaprakash Tripathy</a> · {e(b["formats"])}</span></p>
<div style="max-width:520px;margin-bottom:26px">{store_buttons(b, "book-page")}</div>
<div class="hero-actions">{comp}<a class="btn btn-ghost" href="{SITE["author_page"]}" target="_blank" rel="noopener">More from the author {icon("ext")}</a></div>
<div class="prose"><h2 style="margin-top:.6em">About this book</h2><p>{e(b["summary"])}</p>
<h3>Who it's for</h3><ul class="checklist">{for_list}</ul></div>
</div></div></div></section>
<section><div class="wrap"><div class="section-head"><span class="eyebrow">More books</span><h2>You may also like</h2></div><div class="books">{others}</div></div></section>
{newsletter("bench-notes-book")}'''
    page(path, f'{b["title"]}: Book by Suryaprakash Tripathy',
         f'{b["title"]} by Suryaprakash Tripathy. {b["summary"].split(". ")[0]}. Buy on Amazon US, UK and DE.',
         body, schema=ld(ORG, PERSON, schema, crumbs_ld([("Home","/"),("Books","/books/"),(b["title"], path)])), og_type="book", og_image=b["cover"], active="/books/", priority="0.8")

def guides_index():
    cards = "".join(guide_card(g) for g in GUIDES)
    body = f'''<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("Guides","/guides/")])}
<span class="eyebrow">Guides</span><h1>Bench math, explained properly.</h1>
<p class="lead">Worked examples for the calculations every lab runs. Each guide links to a free BenchMate calculator so you can check your numbers.</p></div></section>
<section style="padding-top:10px"><div class="wrap"><div class="grid g-3">{cards}</div></div></section>
{newsletter("bench-notes-guides")}'''
    page("/guides/", "Lab Calculation Guides: Molarity, Dilutions, Buffers & DNA Concentration | NexagenLabs",
         "Free lab calculation guides with worked examples: molarity, C1V1 dilutions, serial dilutions, buffer preparation, percent solutions and DNA ng/µL to nM conversion.",
         body, schema=ld(ORG, crumbs_ld([("Home","/"),("Guides","/guides/")])), active="/guides/", priority="0.85")

def guide_page(g):
    path = f'/guides/{g["slug"]}'
    toc = "".join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t in g["toc"])
    tool_name, tool_url = g["tool"]
    wl = next(b for b in BOOKS if b["slug"] == "the-working-laboratory")
    related = "".join(guide_card(x) for x in [x for x in GUIDES if x["slug"] != g["slug"]][:3])
    article = {"@type": "TechArticle", "@id": U + path + "#article", "headline": g["title"], "description": g["description"],
               "author": {"@id": U + "/about#person"}, "publisher": {"@id": U + "/#org"}, "datePublished": g["date"], "dateModified": g["date"],
               "mainEntityOfPage": U + path, "keywords": g["keywords"], "image": U + "/assets/img/og-default.jpg", "proficiencyLevel": "Beginner"}
    cta = f'''<div class="cta-box"><div><strong>Check your numbers with {e(tool_name)}</strong><p>Free, no login, runs in your browser.</p></div>
<a class="btn btn-primary" href="{tool_url}" data-ev="open_benchmate" data-label="guide-{g["slug"]}">Open calculator {icon("arrow")}</a></div>'''
    # inject CTA after the 2nd h2
    parts = g["body"].split("<h2", 3)
    body_html = ("<h2".join(parts[:3]) + cta + "<h2" + parts[3]) if len(parts) == 4 else g["body"] + cta
    body = f'''<section class="page-hero" style="padding-bottom:10px"><div class="wrap">{crumbs_html([("Home","/"),("Guides","/guides/"),(g["short"], path)])}
<span class="eyebrow">Guide · {g["minutes"]} min read</span>
<h1 style="font-size:clamp(2rem,4.4vw,3.2rem);max-width:900px">{e(g["title"])}</h1>
<p class="byline"><img class="avatar" src="/assets/img/suryaprakash-tripathy-96.webp" alt="Suryaprakash Tripathy" width="40" height="40"><span>By <a href="/about">Suryaprakash Tripathy</a>, M.Sc. Biotechnology · Updated <time datetime="{g["date"]}">{date.fromisoformat(g["date"]).strftime("%d %b %Y")}</time></span></p>
</div></section>
<section style="padding-top:10px"><div class="wrap article-layout">
<article class="prose">{body_html}
<h2 id="faq">Frequently asked questions</h2>{faq_html(g["faq"])}
<div class="cta-box" style="border-color:rgba(245,176,76,.35)"><div><strong>Go deeper: The Working Laboratory</strong><p>22 core bench techniques, from molarity to sterilisation. Volume 1 of The Biotechnology Techniques Bible.</p></div>
<a class="btn btn-ghost" href="/books/the-working-laboratory">See the book {icon("arrow")}</a></div>
</article>
<aside><div class="aside-card"><h4>On this page</h4><ol>{toc}<li><a href="#faq">FAQ</a></li></ol>
<hr class="divider" style="margin:16px 0"><h4>Free tool</h4><a class="btn btn-primary btn-sm" href="{tool_url}" data-ev="open_benchmate" data-label="guide-aside-{g["slug"]}">{e(tool_name)}</a></div></aside>
</div></section>
<section><div class="wrap"><div class="section-head"><span class="eyebrow">Keep reading</span><h2>Related guides</h2></div><div class="grid g-3">{related}</div></div></section>
{newsletter("bench-notes-guide")}'''
    page(path, g["title"], g["description"], body,
         schema=ld(ORG, PERSON, article, faq_ld(g["faq"]), crumbs_ld([("Home","/"),("Guides","/guides/"),(g["short"], path)])),
         og_type="article", active="/guides/", priority="0.8")

def about():
    creds = "".join(f'<div class="cred reveal"><div class="n">{n}<small>{u}</small></div><div class="l">{e(l)}</div></div>' for n, u, l in CREDENTIALS)
    body = f'''<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("About","/about")])}
<div class="hero-grid" style="align-items:start">
<div><figure class="portrait"><img src="/assets/img/suryaprakash-tripathy.webp" alt="Portrait of Suryaprakash Tripathy" width="320" height="320" fetchpriority="high"></figure>
<span class="eyebrow">About the founder</span><h1>Suryaprakash Tripathy</h1>
<p class="lead">Biotechnology researcher, author and builder of NexagenLabs. My work sits where wet-lab biology meets computation: cancer biology, computational drug discovery and filariasis, and now AI tools that scientists can actually check.</p>
<p class="muted">I build these tools because I needed them myself. Most bench errors I have seen were not hard science. They were a wrong molecular weight, a skipped unit conversion, or a buffer set at the wrong temperature. NexagenLabs exists to catch those before they cost someone a week.</p>
<div class="hero-actions"><a class="btn btn-primary" href="/contact">Get in touch {icon("arrow")}</a><a class="btn btn-ghost" href="{SITE["author_page"]}" target="_blank" rel="noopener">Amazon author page {icon("ext")}</a></div></div>
<div class="cred-grid two">{creds}</div>
</div></div></section>
<section><div class="wrap" style="max-width:860px">
<div class="section-head"><span class="eyebrow">Record</span><h2>Training and research</h2></div>
<div class="timeline">
<div class="t"><b>M.Sc. Biotechnology, Pondicherry University</b><span>Graduated with a 9.0 CGPA.</span></div>
<div class="t"><b>National fellowships</b><span>ICMR-JRF (AIR 115), DBT-GATB (AIR 52) and GATE Biotechnology (AIR 820).</span></div>
<div class="t"><b>IAS-INSA-NASI Summer Research Fellow</b><span>Indian science academies' joint summer research fellowship.</span></div>
<div class="t"><b>Research at IISER Bhopal, IIT Guwahati and ICMR institutes</b><span>Cancer biology, glioblastoma and hypoxia, prime editing, computational drug discovery and filariasis.</span></div>
<div class="t"><b>Publications</b><span>14 book chapters and review articles with Elsevier and Springer Nature.</span></div>
<div class="t"><b>AI evaluation</b><span>Subject-matter expert for evaluating and training frontier AI models on biology and life-science reasoning.</span></div>
<div class="t"><b>Author</b><span>Six books on Amazon across bench techniques, AI for biotech, AI agents and cancer science. <a href="/books/">See the books</a>.</span></div>
</div></div></section>
{newsletter("bench-notes-about")}'''
    profile = {"@type": "ProfilePage", "mainEntity": {"@id": U + "/about#person"}, "url": U + "/about"}
    page("/about", "Suryaprakash Tripathy: Biotechnology Researcher & Author | NexagenLabs",
         "Suryaprakash Tripathy: M.Sc. Biotechnology (Pondicherry University), ICMR-JRF, DBT-GATB and GATE BT ranks, research at IISER Bhopal, IIT Guwahati and ICMR, author of six books and founder of NexagenLabs.",
         body, schema=ld(ORG, PERSON, profile, crumbs_ld([("Home","/"),("About","/about")])), og_type="profile", active="/about", priority="0.7")

def contact():
    body = f'''<section class="page-hero"><div class="wrap">{crumbs_html([("Home","/"),("Contact","/contact")])}
<div class="hero-grid" style="align-items:start">
<div><span class="eyebrow">Contact</span><h1>Say hello.</h1>
<p class="lead">Found a bug in a calculator, want a buffer added, spotted an error in a book, or want to collaborate? Send a note. I read every message.</p>
<ul class="checklist"><li>Tool requests and bug reports</li><li>Book errata and reader questions</li><li>Research, teaching and collaboration enquiries</li></ul></div>
<div class="panel"><div class="panel-bar"><i></i><i></i><i></i>&nbsp; MESSAGE</div><div class="panel-body">
<form class="form" name="contact" method="POST" data-netlify="true" netlify-honeypot="company" action="/thanks" data-ok="Thanks, your message is in. Expect a reply within a few days.">
<input type="hidden" name="form-name" value="contact"><p class="hp"><label>Company <input name="company"></label></p>
<div><label for="cn">Name</label><input id="cn" name="name" required autocomplete="name"></div>
<div><label for="ce">Email</label><input id="ce" type="email" name="email" required autocomplete="email"></div>
<div><label for="ct">Topic</label><select id="ct" name="topic"><option>BenchMate / tools</option><option>Books</option><option>Collaboration</option><option>Other</option></select></div>
<div><label for="cm">Message</label><textarea id="cm" name="message" required></textarea></div>
<button class="btn btn-primary" type="submit">Send message {icon("arrow")}</button>
<p class="fine form-status" role="status"></p>
</form></div></div>
</div></div></section>'''
    page("/contact", "Contact NexagenLabs", "Contact NexagenLabs and Suryaprakash Tripathy about BenchMate, the books, bug reports or collaboration.",
         body, schema=ld(ORG, {"@type": "ContactPage", "url": U + "/contact"}), active="/contact", priority="0.5")

def privacy():
    body = f'''<section class="page-hero"><div class="wrap prose">{crumbs_html([("Home","/"),("Privacy","/privacy")])}
<h1>Privacy</h1><p class="muted">Last updated {date.today().strftime("%d %B %Y")}</p>
<h2>The short version</h2><p>No accounts, no ads, no selling data. The tools run in your browser.</p>
<h2>What we collect</h2>
<ul><li><strong>Forms.</strong> If you subscribe to Bench Notes or send a message, we receive what you type (email, and name and message for contact). Forms are processed by Netlify, our host. We use it only to reply or to send Bench Notes.</li>
<li><strong>Analytics, only with consent.</strong> If you click "Accept analytics", Google Analytics 4 sets cookies to count visits and clicks, with IP anonymisation. If you decline, no analytics script loads. Change your choice any time via "Cookie settings" in the footer.</li>
<li><strong>Server logs.</strong> Netlify keeps standard request logs for security and reliability.</li>
<li><strong>BenchMate.</strong> Calculations and the Reagent Log stay in your browser's local storage on your device.</li></ul>
<h2>Amazon links</h2><p>Book buttons link to Amazon. Once you are on Amazon, Amazon's privacy policy applies.</p>
<h2>Your rights</h2><p>To see, correct or delete anything you sent us, or to unsubscribe, use the <a href="/contact">contact form</a> or the unsubscribe link in any email. If you are in the EU or UK, you have rights under GDPR and UK GDPR, including the right to complain to your data protection authority.</p>
<h2>Controller</h2><p>NexagenLabs, operated by {e(SITE["founder"])}, {e(SITE["location"])}.</p>
</div></section>'''
    page("/privacy", "Privacy Policy | NexagenLabs", "How NexagenLabs handles data: no accounts or ads, consent-based analytics, and forms processed by Netlify.", body, priority="0.2")

def thanks():
    body = f'''<section class="page-hero"><div class="wrap center" style="max-width:640px">
<span class="eyebrow">Received</span><h1>Thank you.</h1><p class="lead" style="margin-inline:auto">Your submission is in. While you're here, the tools are one click away.</p>
<div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="{BM}/">Open BenchMate {icon("arrow")}</a><a class="btn btn-ghost" href="/guides/">Read a guide</a></div></div></section>'''
    page("/thanks", "Thank you | NexagenLabs", "Thanks for getting in touch with NexagenLabs.", body, noindex=True)

def notfound():
    body = f'''<section class="page-hero"><div class="wrap center" style="max-width:640px">
<span class="eyebrow">404 · sample not found</span><h1>This page isn't on the bench.</h1>
<p class="lead" style="margin-inline:auto">The link may be old, or the page has moved. Try one of these instead.</p>
<div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="/">Home</a><a class="btn btn-ghost" href="/tools">All tools</a><a class="btn btn-ghost" href="/books/">Books</a></div></div></section>'''
    page("/404.html", "Page not found | NexagenLabs", "The page you were looking for isn't here.", body, noindex=True)

# ------------------------------------------------------------------ SEO files
def seo_files():
    urls = "".join(f'<url><loc>{U}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>' for p, pr in PAGES)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /thanks\n\nSitemap: {U}/sitemap.xml\nSitemap: {BM}/sitemap.xml\n")
    items = "".join(f'<item><title>{e(g["title"])}</title><link>{U}/guides/{g["slug"]}</link><guid>{U}/guides/{g["slug"]}</guid><pubDate>{date.fromisoformat(g["date"]).strftime("%a, %d %b %Y")} 00:00:00 +0000</pubDate><description>{e(g["description"])}</description></item>' for g in GUIDES)
    write("/guides/feed.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>NexagenLabs Guides</title><link>{U}/guides/</link><description>Lab calculation guides</description>{items}</channel></rss>\n')
    write("/site.webmanifest", json.dumps({"name": "NexagenLabs", "short_name": "NexagenLabs", "start_url": "/", "display": "standalone",
        "background_color": "#060a11", "theme_color": "#060a11",
        "icons": [{"src": "/assets/img/logo-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/logo-512.png", "sizes": "512x512", "type": "image/png"}]}))
    # llms.txt: helps AI assistants describe the site accurately
    lines = ["# NexagenLabs", "", f"> {SITE['tagline']}", "", "## Tools"] + [f"- [{p['name']}]({p['url']}): {p['desc']}" for p in PROPERTIES] + \
        ["", "## Guides"] + [f"- [{g['title']}]({U}/guides/{g['slug']}): {g['description']}" for g in GUIDES] + \
        ["", "## Books"] + [f"- [{b['title']}: {b['subtitle']}]({U}/books/{b['slug']})" for b in BOOKS] + \
        ["", "## About", f"- [{SITE['founder']}]({U}/about): biotechnology researcher and author; founder of NexagenLabs."]
    write("/llms.txt", "\n".join(lines) + "\n")

def static():
    for d in ["assets"]:
        src = os.path.join(ROOT, d)
        dst = os.path.join(OUT, d)
        shutil.copytree(src, dst, dirs_exist_ok=True)
    for f in ["favicon.ico", "favicon-32.png", "favicon-48.png", "apple-touch-icon.png", "_redirects", "_headers"]:
        sp = os.path.join(ROOT, "static", f)
        if os.path.exists(sp):
            shutil.copy(sp, os.path.join(OUT, f))

if __name__ == "__main__":
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    home(); tools(); benchmate(); books_index()
    for b in BOOKS: book_page(b)
    guides_index()
    for g in GUIDES: guide_page(g)
    about(); contact(); privacy(); thanks(); notfound()
    seo_files(); static()
    print(f"Built {len(PAGES)} indexable pages → {OUT}")
