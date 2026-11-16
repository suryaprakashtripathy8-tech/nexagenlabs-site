# nexagenlabs.com

Static site for NexagenLabs (research tools hub). No dependencies: plain Python 3 builds HTML into `public/`.

## Where things live

- Content: `src/data.py` (sites, BenchMate and VeriHelix tools, books, free guides, credentials, profile links, home-page finder) and `src/guides.py` (guides)
- Templates and SEO: `src/build.py`
- Styles and scripts: `assets/css/site.css`, `assets/js/site.js` (dark and light themes, calculators, search, forms)
- Netlify files: `static/_redirects`, `static/_headers`

## Common edits

- New VeriHelix tool goes live: add one row to `VERIHELIX_TOOLS` in `src/data.py`. The home page, tool directory, VeriHelix page, search and counts update themselves.
- New free guide on the Gumroad store: add one entry to `FREE_BOOKS`.
- New Amazon book: add one entry to `BOOKS` (pick a `tone` for the typeset fallback cover).

## Build

- `python3 src/build.py` then open `public/index.html`. Netlify runs this on every push to the production branch.
- `NX_PREVIEW=1 python3 src/build.py` writes `preview/`, a single-file bundle of every page for review without a server. It is not deployed.

## Netlify free plan

Each production deploy costs 15 of the 300 monthly credits, so batch changes into one push. Book covers load from Amazon's image CDN, not from Netlify, so they use no bandwidth credits; a typeset cover shows if one fails to load.

Fonts: Newsreader, IBM Plex Sans and IBM Plex Mono, all under the SIL Open Font License.
