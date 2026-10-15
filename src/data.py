"""Site data: tools, books, credentials. Edit here, then run `python3 src/build.py`."""

SITE = {
    "name": "NexagenLabs",
    "url": "https://nexagenlabs.com",
    "tagline": "Free research tools, companion code and field-tested guides for working scientists.",
    "founder": "Suryaprakash Tripathy",
    "author_page": "https://www.amazon.com/stores/Suryaprakash-Tripathy/author/B0CJ6VXV76",
    "ga_id": "G-LBG6BT3K02",  # set to G-XXXXXXX once GA4 property exists
    "gsc_verification": "",  # Google Search Console HTML-tag token (optional if verified by DNS)
    "location": "Nabarangpur, Odisha, India",
}

BM = "https://benchmate.nexagenlabs.com"

# BenchMate sub-tools (deep links into the app)
BENCHMATE_TOOLS = [
    ("Molarity & Dilution", "/molarity", "C1V1 dilutions, mass ↔ molarity, serial dilution tables.", "calc"),
    ("Unit Converter", "/converter", "Mass, volume and molarity units, plus ng/µL for nucleic acids.", "calc"),
    ("Molecular Weight Lookup", "/mw-lookup", "370 verified compounds with MW, formula and CAS number.", "data"),
    ("Buffer Recipe Generator", "/buffer", "40 common buffers, scaled by volume, pH and temperature.", "recipe"),
    ("Percent-Solution Generator", "/percent", "w/v, v/v and m/v recipes with safety and viscosity notes.", "recipe"),
    ("Reagent Log", "/reagent-log", "Save, search and export recipes. Stored only in your browser.", "data"),
    ("Recipe Audit", "/audit", "Scan saved recipes for likely bench errors, ranked by severity.", "data"),
    ("Cheat-Sheet Library", "/cheatsheets", "Printable one-page bench references.", "learn"),
    ("Bench Timer", "/timer", "Concurrent timers with PCR, digest, gel and blot presets.", "calc"),
    ("Technique Quiz", "/quiz", "100 questions across 8 categories of bench practice.", "learn"),
    ("Certificates", "/certificates", "Earn a Bench Fundamentals certificate through the quiz.", "learn"),
    ("Ask the Bible", "/ask", "Search 200+ curated bench answers from the Techniques Bible.", "learn"),
]

# Ecosystem: subdomain properties (GLP-1 intentionally excluded)
PROPERTIES = [
    {
        "slug": "benchmate", "name": "BenchMate", "url": BM + "/",
        "kind": "Bench calculator suite", "status": "live", "icon": "flask", "tone": "",
        "cats": "bench calculators",
        "desc": "Fast, offline, no-login calculators for molarity, dilutions, buffers, percent solutions and unit conversion. Built for people standing at the bench.",
        "book": "the-working-laboratory",
    },
    {
        "slug": "agentic-lab", "name": "The Agentic Lab: Companion Code", "url": "https://lab.nexagenlabs.com/",
        "kind": "AI agents · code companion", "status": "live", "icon": "agent", "tone": "violet",
        "cats": "ai companion",
        "desc": "Twelve tested builds for AI agents in biotech and pharma R&D: literature triage, data wrangling, plate mapping, docking loops, ELN bridges and run provenance.",
        "book": "the-agentic-lab",
    },
]

def amazon(asin):
    return {
        "us": f"https://www.amazon.com/dp/{asin}",
        "uk": f"https://www.amazon.co.uk/dp/{asin}",
        "de": f"https://www.amazon.de/dp/{asin}",
    }

COVER = "https://m.media-amazon.com/images/I/{}._SL600_.jpg"

BOOKS = [
    {
        "slug": "the-agentic-lab", "asin": "B0HJ8871VG", "cover": COVER.format("615sG+d591L"),
        "title": "The Agentic Lab",
        "subtitle": "Build AI Agents for Biotech and Pharma R&D",
        "formats": "Kindle · Paperback", "year": 2026, "topic": "AI agents for R&D",
        "companion": "https://lab.nexagenlabs.com/",
        "summary": "A hands-on book for bench scientists who want AI agents that can be checked, not just trusted. You write an agent loop in plain Python, then build twelve agents for the work that eats a research group's week: literature triage, cleaning instrument exports, protocol drafting, docking, ELN and LIMS links, and run provenance. Each chapter ends with a Validation Gate, a set of tests the build has to pass before its output is used. One real research question runs through the whole book.",
        "for": ["Wet-lab and computational scientists starting with AI agents", "R&D teams who need audit trails, not demos", "Readers who want working, tested code alongside the text"],
    },
    {
        "slug": "ai-for-biotech", "asin": "B0H65YFHNW", "cover": COVER.format("71NhdYxRYXL"),
        "title": "AI for Biotech",
        "subtitle": "The Practical Guide to Using AI Tools to Accelerate Your Research and Your Career: From ChatGPT and AlphaFold to Lab Automation and Beyond",
        "formats": "Kindle · Paperback · Hardcover", "year": 2026, "topic": "AI tools for biologists",
        "companion": None,
        "summary": "A practical playbook for using AI in day-to-day biology research, from ChatGPT and AlphaFold to RFdiffusion, CRISPR design, single-cell foundation models and lab automation. The examples come from real research on glioblastoma, hypoxia, prime editing and oncology rather than toy datasets. No programming background is assumed, and each chapter ends with a working notebook you can open in Colab.",
        "for": ["Graduate students who feel behind on AI", "Postdocs and PIs standardising AI use in a lab", "Biologists moving from the bench into computation"],
    },
    {
        "slug": "the-working-laboratory", "asin": "B0HDH78H39", "cover": COVER.format("71s5kZyN9uL"),
        "title": "The Working Laboratory",
        "subtitle": "Biotechnology Lab Techniques, Solutions, Buffers, Sterilization, and Laboratory Safety",
        "formats": "Kindle · Paperback · Hardcover", "year": 2026, "topic": "Bench fundamentals",
        "companion": BM + "/",
        "summary": "Volume 1 of The Biotechnology Techniques Bible. It covers 22 core techniques across four areas every lab depends on: units and concentration, solutions and dilutions, water and buffers, and sterilisation and safety. Written for the bench rather than the lecture hall, it pairs with the free BenchMate calculators and a certificate of completion.",
        "for": ["BS and MS students entering a research lab", "New research staff and technicians", "Anyone who makes buffers and stocks every week"],
    },
    {
        "slug": "demystifying-biotechnology", "asin": "B0CJ4ZLWQY", "cover": COVER.format("71FZrPL-n3L"),
        "title": "Demystifying Biotechnology",
        "subtitle": "A Comprehensive Guide to Mastering Biotechnology Techniques | 85+ QR Codes & Virtual Learning | 41 Experimental Scenarios",
        "formats": "Kindle · Paperback · Hardcover", "year": 2023, "topic": "Biotechnology techniques",
        "companion": None,
        "summary": "A self-paced guide that explains how core biotechnology techniques work and why. Concepts are built with analogies, comparison tables and 41 experimental scenarios, and more than 85 QR codes open curated video demonstrations so you can see each method before you run it.",
        "for": ["B.Sc and M.Sc students", "New research scholars", "Anyone stepping into a real lab for the first time"],
    },
    {
        "slug": "the-cancer-decade", "asin": "B0HKFYP9CB", "cover": COVER.format("71qAJ6G-LFL"),
        "title": "The Cancer Decade",
        "subtitle": "A Cancer Biologist's Guide to the Tumor Tests, Targeted Drugs, Cancer Vaccines and AI Medicine Arriving in the Next Ten Years, and How to Tell a Real Breakthrough From a False One",
        "formats": "Kindle · Paperback · Hardcover", "year": 2026, "topic": "Cancer medicine, for general readers",
        "companion": None,
        "summary": "A cancer biologist's guide to what is actually arriving in cancer care over the next ten years: tumour genetic tests, matched drugs, immunotherapy, cell therapies, personalised vaccines, early-detection blood tests and AI that designs drugs and reads scans. It shows readers how to tell a real advance from a headline.",
        "for": ["Patients and families following cancer news", "Readers who want evidence, not hype", "Students curious about where oncology is heading"],
    },
    {
        "slug": "the-machines-that-read-us", "asin": "B0HK3BDP4B", "cover": COVER.format("71JCcMQVOSL"),
        "title": "The Machines That Read Us",
        "subtitle": "How AI Learned to Read, Write, and Edit Life and What Comes Next for Medicine, Aging, Food, and You",
        "formats": "Kindle · Paperback · Hardcover", "year": 2026, "topic": "AI and biology, for general readers",
        "companion": None,
        "summary": "A clear, current account of what AI has really changed in biology, written for readers with no science background. It runs from the first human genome draft through protein folding, drug discovery, gene editing, self-driving labs, medical AI, ageing research and food. Each technology is placed on a six-rung evidence ladder, so you see the reasoning behind every verdict.",
        "for": ["Curious general readers", "Professionals tracking AI in health and food", "Anyone tired of AI-biology hype"],
    },
]
for b in BOOKS:
    b["stores"] = amazon(b["asin"])

CREDENTIALS = [
    ("115", "AIR", "ICMR-JRF fellowship, all-India rank"),
    ("52", "AIR", "DBT-GATB fellowship, all-India rank"),
    ("820", "AIR", "GATE Biotechnology, all-India rank"),
    ("9.0", "CGPA", "M.Sc. Biotechnology, Pondicherry University"),
    ("14", "papers", "Book chapters and review articles with Elsevier and Springer Nature"),
    ("6", "books", "Published on Amazon across biotech, AI and cancer"),
]
