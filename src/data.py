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

VH = "https://verihelix.nexagenlabs.com"

# VeriHelix tools that are live, in the groups VeriHelix itself uses.
# Add a row here when a new tool ships: (name, path, one-line description, group id).
VERIHELIX_GROUPS = [
    ("research", "Research and writing"),
    ("molecules", "Proteins and molecules"),
    ("sequences", "Sequences, omics and editing"),
    ("validation", "Validation and clinical AI"),
    ("career", "Career"),
]
VERIHELIX_TOOLS = [
    ("Citation Verifier", "/tools/citation-verifier/", "Check whether AI-written references exist, match their titles, and have been retracted.", "research"),
    ("Prompt Lab", "/tools/prompt-lab/", "Build an expert research prompt and open it in ChatGPT, Claude or Gemini.", "research"),
    ("AI Disclosure Generator", "/tools/disclosure/", "Write the AI-use statement your journal or funder asks for.", "research"),
    ("Figure Accessibility Checker", "/tools/figure-check/", "See your figure through colour-blind eyes and check it against journal size rules.", "research"),
    ("Can I Paste This?", "/tools/can-i-paste/", "Find out which AI tools are safe to use with your kind of data.", "research"),
    ("Structure Confidence Reader", "/tools/structure-reader/", "Read an AlphaFold model: which regions to trust, which to doubt, and why.", "molecules"),
    ("Molecule Desk", "/tools/molecule-desk/", "Paste a SMILES string. Get properties, drug-likeness rules and structural alerts.", "molecules"),
    ("Protein Design Triage", "/tools/design-triage/", "Sort RFdiffusion and ProteinMPNN designs into pass, borderline and fail.", "molecules"),
    ("Sequence Toolkit", "/tools/sequence-toolkit/", "Clean, translate, reverse-complement and scan DNA in one place.", "sequences"),
    ("CRISPR Guide Design", "/tools/crispr-guides/", "Where to design guides, and why this job needs a genome-aware tool.", "sequences"),
    ("Variant Lookup", "/tools/variant-lookup/", "Look up a human variant's consequence and population frequency.", "sequences"),
    ("Colab Notebook Starter", "/tools/notebook-starter/", "Pick an analysis and download a commented starter notebook.", "sequences"),
    ("Clinical Metrics Calculator", "/tools/clinical-metrics/", "Turn a confusion matrix into the numbers reviewers ask for, at your real prevalence.", "validation"),
    ("Data Leakage Audit", "/tools/leakage-audit/", "Check an ML study for the eight ways test data leaks into training.", "validation"),
    ("Reporting Checklist Builder", "/tools/reporting-checklists/", "Get the right AI reporting checklist for your study, ready to fill in.", "validation"),
    ("AI-Biotech Readiness Score", "/tools/readiness/", "A three-minute skills check with a personal 90-day study plan.", "career"),
]

# Ecosystem: subdomain properties (GLP-1 intentionally excluded)
PROPERTIES = [
    {
        "slug": "benchmate", "name": "BenchMate", "url": BM + "/",
        "kind": "Bench calculator suite", "status": "live", "icon": "flask", "tone": "",
        "cats": "bench calculators",
        "desc": "Fast, offline, no-login calculators for molarity, dilutions, buffers, percent solutions and unit conversion. Built for people standing at the bench.",
        "book": "the-working-laboratory", "page": "/benchmate",
    },
    {
        "slug": "verihelix", "name": "VeriHelix", "url": VH + "/",
        "kind": "AI-biotech workbench", "status": "new", "icon": "shield", "tone": "blue",
        "cats": "ai companion",
        "desc": "16 tools for using AI in biotech research and checking what it gives you: references, prompts, AlphaFold models, molecules, sequences, variants and ML study audits.",
        "book": "ai-for-biotech", "page": "/verihelix",
    },
    {
        "slug": "agentic-lab", "name": "The Agentic Lab: Companion Code", "url": "https://lab.nexagenlabs.com/",
        "kind": "Companion code for AI agents", "status": "live", "icon": "agent", "tone": "violet",
        "cats": "ai companion",
        "desc": "Twelve tested builds for AI agents in biotech and pharma R&D: literature triage, data wrangling, plate mapping, docking loops, ELN bridges and run provenance.",
        "book": "the-agentic-lab", "page": None,
    },
]

def amazon(asin):
    return {
        "us": f"https://www.amazon.com/dp/{asin}",
        "uk": f"https://www.amazon.co.uk/dp/{asin}",
        "de": f"https://www.amazon.de/dp/{asin}",
    }

# 400 px covers are sharp at the sizes the site shows and about half the weight of the 600 px ones.
COVER = "https://m.media-amazon.com/images/I/{}._SL400_.jpg"

BOOKS = [
    {
        "slug": "the-agentic-lab", "tone": "violet", "asin": "B0HJ8871VG", "cover": COVER.format("615sG+d591L"),
        "title": "The Agentic Lab",
        "subtitle": "Build AI Agents for Biotech and Pharma R&D",
        "formats": "Kindle · Paperback", "year": 2026, "topic": "AI agents for R&D",
        "companion": "https://lab.nexagenlabs.com/",
        "summary": "A hands-on book for bench scientists who want AI agents that can be checked, not just trusted. You write an agent loop in plain Python, then build twelve agents for the work that eats a research group's week: literature triage, cleaning instrument exports, protocol drafting, docking, ELN and LIMS links, and run provenance. Each chapter ends with a Validation Gate, a set of tests the build has to pass before its output is used. One real research question runs through the whole book.",
        "for": ["Wet-lab and computational scientists starting with AI agents", "R&D teams who need audit trails, not demos", "Readers who want working, tested code alongside the text"],
    },
    {
        "slug": "ai-for-biotech", "tone": "blue", "asin": "B0H65YFHNW", "cover": COVER.format("71NhdYxRYXL"),
        "title": "AI for Biotech",
        "subtitle": "The Practical Guide to Using AI Tools to Accelerate Your Research and Your Career: From ChatGPT and AlphaFold to Lab Automation and Beyond",
        "formats": "Kindle · Paperback · Hardcover", "year": 2026, "topic": "AI tools for biologists",
        "companion": VH + "/",
        "summary": "A practical playbook for using AI in day-to-day biology research, from ChatGPT and AlphaFold to RFdiffusion, CRISPR design, single-cell foundation models and lab automation. The examples come from real research on glioblastoma, hypoxia, prime editing and oncology rather than toy datasets. No programming background is assumed, and each chapter ends with a working notebook you can open in Colab.",
        "for": ["Graduate students who feel behind on AI", "Postdocs and PIs standardising AI use in a lab", "Biologists moving from the bench into computation"],
    },
    {
        "slug": "the-working-laboratory", "tone": "teal", "asin": "B0HDH78H39", "cover": COVER.format("71s5kZyN9uL"),
        "title": "The Working Laboratory",
        "subtitle": "Biotechnology Lab Techniques, Solutions, Buffers, Sterilization, and Laboratory Safety",
        "formats": "Kindle · Paperback · Hardcover", "year": 2026, "topic": "Bench fundamentals",
        "companion": BM + "/",
        "summary": "Volume 1 of The Biotechnology Techniques Bible. It covers 22 core techniques across four areas every lab depends on: units and concentration, solutions and dilutions, water and buffers, and sterilisation and safety. Written for the bench rather than the lecture hall, it pairs with the free BenchMate calculators and a certificate of completion.",
        "for": ["BS and MS students entering a research lab", "New research staff and technicians", "Anyone who makes buffers and stocks every week"],
    },
    {
        "slug": "demystifying-biotechnology", "tone": "slate", "asin": "B0CJ4ZLWQY", "cover": COVER.format("71FZrPL-n3L"),
        "title": "Demystifying Biotechnology",
        "subtitle": "A Comprehensive Guide to Mastering Biotechnology Techniques | 85+ QR Codes & Virtual Learning | 41 Experimental Scenarios",
        "formats": "Kindle · Paperback · Hardcover", "year": 2023, "topic": "Biotechnology techniques",
        "companion": None,
        "summary": "A self-paced guide that explains how core biotechnology techniques work and why. Concepts are built with analogies, comparison tables and 41 experimental scenarios, and more than 85 QR codes open curated video demonstrations so you can see each method before you run it.",
        "for": ["B.Sc and M.Sc students", "New research scholars", "Anyone stepping into a real lab for the first time"],
    },
    {
        "slug": "the-cancer-decade", "tone": "rose", "asin": "B0HKFYP9CB", "cover": COVER.format("71qAJ6G-LFL"),
        "title": "The Cancer Decade",
        "subtitle": "A Cancer Biologist's Guide to the Tumor Tests, Targeted Drugs, Cancer Vaccines and AI Medicine Arriving in the Next Ten Years, and How to Tell a Real Breakthrough From a False One",
        "formats": "Kindle · Paperback · Hardcover", "year": 2026, "topic": "Cancer medicine, for general readers",
        "companion": None,
        "summary": "A cancer biologist's guide to what is actually arriving in cancer care over the next ten years: tumour genetic tests, matched drugs, immunotherapy, cell therapies, personalised vaccines, early-detection blood tests and AI that designs drugs and reads scans. It shows readers how to tell a real advance from a headline.",
        "for": ["Patients and families following cancer news", "Readers who want evidence, not hype", "Students curious about where oncology is heading"],
    },
    {
        "slug": "the-machines-that-read-us", "tone": "amber", "asin": "B0HK3BDP4B", "cover": COVER.format("71JCcMQVOSL"),
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

# Free guides, delivered through the Gumroad store on books.nexagenlabs.com
GUM = "https://books.nexagenlabs.com/l/"
FREE_BOOKS = [
    {"slug": "bench-ready", "title": "A Lab RA's First 90 Days", "series": "Bench Ready", "for": "New research assistants", "pages": 78,
     "desc": "Before day 1 through day 90: orientation, notebook, freezer and reagent habits, your first independent experiment, and a method for troubleshooting failures.",
     "extras": ["Excel workbook with 90-day tracker", "Printable kit pages", "Message templates"]},
    {"slug": "bench-ready-undergrad", "title": "Your First Semester in a Research Lab", "series": "Bench Ready", "for": "Undergraduates joining a lab", "pages": 64,
     "desc": "A 15-week plan for fitting a few lab hours around classes and exams, from finding a lab to leaving it properly.",
     "extras": ["Excel workbook with semester tracker", "Printable kit pages", "Message templates"]},
    {"slug": "bench-ready-phd", "title": "Your First Year in a Life-Science PhD", "series": "Bench Ready", "for": "First-year PhD students, US and India", "pages": 67,
     "desc": "Rotations, choosing a thesis lab, working with an advisor and running a project, with one action to take each week.",
     "extras": ["Excel workbook with rotation scorecard", "Printable kit pages", "Message templates"]},
    {"slug": "pcr-qpcr-troubleshooting", "title": "PCR & qPCR, From Symptom to Fix", "series": "Bench Ready Troubleshooting, Vol 1", "for": "Anyone running PCR or qPCR", "pages": 102,
     "desc": "22 symptoms, each with what to check first, the test that separates the causes, the fix, and what to log. Includes a MIQE 2.0 checklist.",
     "extras": ["12-tab troubleshooting workbook", "Printable log sheets and decision cards", "Message templates"]},
    {"slug": "dna-rna-troubleshooting", "title": "DNA & RNA, From Symptom to Fix", "series": "Bench Ready Troubleshooting, Vol 2", "for": "Anyone extracting DNA or RNA", "pages": 117,
     "desc": "Start from what you measured (NanoDrop, Qubit, gel) and work back to the cause: low yield, degradation, bad 260/230, gDNA carry-over, FFPE and plant samples.",
     "extras": ["9-tab QC and yield workbook", "Printable reading and decision cards", "Message templates"]},
]
FREE_SERIES = [
    ("Bench Ready", "Your first months in a lab", ["bench-ready", "bench-ready-undergrad", "bench-ready-phd"]),
    ("Bench Ready Troubleshooting", "From symptom to fix", ["pcr-qpcr-troubleshooting", "dna-rna-troubleshooting"]),
]
for f in FREE_BOOKS:
    f["url"] = GUM + f["slug"]

PROFILES = [
    ("Amazon author page", SITE["author_page"]),
    ("Google Scholar", "https://scholar.google.com/citations?user=EQkaGLAAAAAJ&hl=en"),
    ("LinkedIn", "https://www.linkedin.com/in/suryaprakash-tripathy-09b7751b6/"),
    ("GitHub", "https://github.com/nexagenlabs"),
]

# Home page finder: a job, then (kind, title, note, url) picks. Up to three per job.
JOBS = [
    ("Dilute a stock", [("Tool", "Molarity & Dilution", "C1V1 with unit handling and warnings", BM + "/molarity"), ("Guide", "C1V1 = C2V2", "Worked examples, 6 min", "/guides/c1v1-c2v2-dilution-guide"), ("Book", "The Working Laboratory", "Solutions and dilutions, in depth", "/books/the-working-laboratory")]),
    ("Make a molar solution", [("Tool", "Molarity & Dilution", "Mass from molarity, volume and MW", BM + "/molarity"), ("Tool", "Molecular Weight Lookup", "370 verified compounds, hydrates included", BM + "/mw-lookup"), ("Guide", "How to calculate molarity", "Worked examples, 7 min", "/guides/how-to-calculate-molarity")]),
    ("Prepare a buffer", [("Tool", "Buffer Recipe Generator", "40 buffers scaled by volume, pH and temperature", BM + "/buffer"), ("Guide", "How to prepare lab buffers", "PBS and Tris-HCl recipes, 8 min", "/guides/how-to-prepare-buffers"), ("Book", "The Working Laboratory", "Water and buffers, in depth", "/books/the-working-laboratory")]),
    ("Plan a serial dilution", [("Tool", "Molarity & Dilution", "Serial dilution tables", BM + "/molarity"), ("Guide", "Serial dilutions made simple", "Tables and plating maths, 6 min", "/guides/serial-dilution-guide")]),
    ("Convert ng/µL to nM", [("Tool", "Unit Converter", "Mass, volume, molarity and nucleic acids", BM + "/converter"), ("Guide", "ng/µL to nM and copy number", "A260 basics and worked examples, 7 min", "/guides/dna-concentration-ng-ul-to-nm")]),
    ("Fix a failed PCR", [("Free guide", "PCR & qPCR, From Symptom to Fix", "102 pages, workbook and decision cards", GUM + "pcr-qpcr-troubleshooting"), ("Tool", "Bench Timer", "PCR, digest, gel and blot presets", BM + "/timer")]),
    ("Rescue a bad DNA or RNA prep", [("Free guide", "DNA & RNA, From Symptom to Fix", "117 pages, QC workbook and decision cards", GUM + "dna-rna-troubleshooting"), ("Tool", "Unit Converter", "ng/µL, nM and copy number", BM + "/converter"), ("Guide", "ng/µL to nM and copy number", "A260 basics, 7 min", "/guides/dna-concentration-ng-ul-to-nm")]),
    ("Check AI-written references", [("Tool", "Citation Verifier", "Looks each reference up in Crossref and PubMed", VH + "/tools/citation-verifier/"), ("Book", "AI for Biotech", "AI-powered literature review", "/books/ai-for-biotech")]),
    ("Write a research prompt", [("Tool", "Prompt Lab", "Role, task, context and format, ready to paste", VH + "/tools/prompt-lab/"), ("Book", "AI for Biotech", "Prompt engineering for researchers", "/books/ai-for-biotech")]),
    ("Read an AlphaFold model", [("Tool", "Structure Confidence Reader", "Which regions to trust, and why", VH + "/tools/structure-reader/"), ("Book", "AI for Biotech", "Protein structure prediction", "/books/ai-for-biotech")]),
    ("Write an AI-use statement", [("Tool", "AI Disclosure Generator", "For journals and funders", VH + "/tools/disclosure/"), ("Tool", "Reporting Checklist Builder", "The checklist that fits your study", VH + "/tools/reporting-checklists/")]),
    ("Screen a molecule", [("Tool", "Molecule Desk", "Lipinski, Veber, PAINS and Brenk from a SMILES", VH + "/tools/molecule-desk/"), ("Tool", "Protein Design Triage", "Pass, borderline or fail for designs", VH + "/tools/design-triage/"), ("Book", "AI for Biotech", "AI in drug discovery", "/books/ai-for-biotech")]),
    ("Build an AI agent for lab work", [("Code", "The Agentic Lab: Companion Code", "Twelve tested builds", "https://lab.nexagenlabs.com/"), ("Book", "The Agentic Lab", "Agents you can validate", "/books/the-agentic-lab")]),
    ("Check an ML study for leakage", [("Tool", "Data Leakage Audit", "Eight ways test data leaks into training", VH + "/tools/leakage-audit/"), ("Tool", "Clinical Metrics Calculator", "Metrics at your real prevalence", VH + "/tools/clinical-metrics/")]),
    ("Start in a new lab", [("Free guide", "A Lab RA's First 90 Days", "For new research assistants", GUM + "bench-ready"), ("Free guide", "Your First Semester in a Research Lab", "For undergraduates", GUM + "bench-ready-undergrad"), ("Free guide", "Your First Year in a Life-Science PhD", "For first-year PhD students", GUM + "bench-ready-phd")]),
]

# Free certificates on the tool sites, gathered on /certification.
# (name, how to earn it, target, kind, link). kind: "quiz" or "habit".
BM_CERTS = [
    ("Bench Fundamentals", "Answer 50 foundation-level questions correctly, across every category of the Technique Quiz.", "50 correct answers", "quiz", BM + "/quiz"),
    ("Buffer Preparation", "Answer 30 buffer-chemistry questions correctly in the Technique Quiz.", "30 correct answers", "quiz", BM + "/quiz"),
    ("Dilution Mastery", "Answer 20 dilution questions correctly in the Technique Quiz.", "20 correct answers", "quiz", BM + "/quiz"),
    ("Daily Practice", "Read Today's Technique on BenchMate on 30 days in a row.", "30-day streak", "habit", BM + "/"),
    ("BenchMate Explorer", "Use three different BenchMate tools.", "3 features used", "habit", BM + "/"),
]
VH_CERTS = [
    ("AI Foundations for Biotechnologists", "Prompt engineering, hallucination checks, AI literature review, AI writing ethics, scientific figures, lab data and reproducibility.", "Chapters 1 to 8", VH + "/certificates/take/?track=foundations"),
    ("AI for Protein Science and Drug Discovery", "Structure prediction, pLDDT and PAE, complex prediction, de novo protein design, docking, ADMET and drug-likeness.", "Chapters 9 to 11", VH + "/certificates/take/?track=protein-drug"),
    ("AI for Omics, Sequencing and Genome Editing", "Single-cell QC and annotation, spatial transcriptomics, NGS quality metrics, variant interpretation, CRISPR and prime editing.", "Chapters 12 to 14", VH + "/certificates/take/?track=omics-editing"),
    ("Responsible AI in Biotech Research", "Clinical evaluation metrics, prevalence and PPV, data leakage, reporting standards, bias and fairness, regulatory pathways.", "Chapters 16 and 19", VH + "/certificates/take/?track=responsible-ai"),
]
JOBS.append(("Earn a free certificate", [("Certificate", "Bench Fundamentals", "50 correct answers in the Technique Quiz", BM + "/quiz"), ("Certificate", "AI Foundations for Biotechnologists", "VeriHelix track 1", VH + "/certificates/take/?track=foundations"), ("Page", "All free certificates", "Seven certificates and a capstone", "/certification")]))
