# nexagenlabs.com

Static site for NexagenLabs (research tools hub). No dependencies — plain Python 3 builds HTML into `public/`.

- Edit content: `src/data.py` (tools, books, credentials) and `src/guides.py` (guides)
- Templates and SEO: `src/build.py`
- Styles/scripts: `assets/css/site.css`, `assets/js/site.js`
- Netlify files: `static/_redirects`, `static/_headers`
- Build locally: `python3 src/build.py` then open `public/index.html`

Set `ga_id` and `gsc_verification` in `src/data.py` once GA4 / Search Console exist.
Netlify runs the build automatically on every push.
