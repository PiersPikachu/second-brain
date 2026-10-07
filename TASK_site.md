Task: static GEO-audit website
 
Place this file in the repository root and give Claude Code the command:
"Read TASK_site.md and GEO-audit-dark-factory_project-brief.md, ask clarifying questions one at a time, then proceed." 
 
1. Context
 
The service measures how often AI assistants (Perplexity, ChatGPT, etc.) mention Wildberries sellers' brands in answers to buyers. The business operates as a dark factory: no people on the line, everything automatic. Details — in GEO-audit-dark-factory_project-brief.md.
 
The website is needed for three purposes:
1. Publish the offer and the personal data processing policy (requirements of the law and the payment service).
2. Publish weekly "whom AI recommends" ratings by category — so they are found and cited by AI with web search.
3. Drive visitors to the Telegram bot (no sales on the site). 
The site is maintained without people: it is assembled automatically from data after each weekly measurement.
 
2. Main requirement: the site must be readable by AI
 
Many AI crawlers do not execute JavaScript. Therefore:
• All content — in ready HTML, assembled on the server. No client-side rendering.
• No React, Vue, Framer Motion, or frontend bundlers.
• Animations — CSS only, on top of ready content; respect prefers-reduced-motion.
• Check: the page with JavaScript disabled contains all text and all tables. 
3. Stack
• Python 3.12, Jinja2 — static page generator.
• Output: site/dist/ folder with ready HTML/CSS.
• Serving: Caddy container in Docker Compose (automatic HTTPS, domain from the SITE_DOMAIN environment variable).
• No external CDNs, Google fonts, counters, or trackers: everything of our own, from the same server. Font — system stack or one font hosted locally. 
4. Pages
Address Content
/ What the service does, how AI "sees" brands, an example rating, button to the Telegram bot
/ratings/ List of categories with ratings
/ratings/<marketplace>/<category>/ Current category rating
/ratings/<marketplace>/<category>/<YYYY-Wnn>/ Week archive — the address is permanent, never changes
/method/ Methodology: query types, models, 3 runs, share formula, versions
/pricing/ Tariffs (from data, do not hardcode)
/offer/ and /privacy/ Stubs marked "DRAFT — to be replaced by the digital lawyer's document". Do not compose legal text
/contacts/ Full name and INN of the self-employed person are substituted from settings, not stored in code

 
Rating page structure (answer first):
1. h1 heading with category and week.
2. Short conclusion in 2–3 sentences: leaders and changes over the week.
3. <table>: rank, brand, share in AI answers, change.
4. Measurement date and link to methodology. 
5. GEO and SEO
• schema.org markup in JSON-LD: Organization, WebSite; for a rating — Dataset (with dateModified, variableMeasured) and ItemList; for methodology — FAQPage.
• robots.txt: allow search and AI crawlers (YandexBot, Googlebot, PerplexityBot, OAI-SearchBot, GPTBot, ClaudeBot).
• sitemap.xml with lastmod, canonical on every page, an llms.txt file with a brief description of the site and links to ratings.
• Semantic markup, fast loading, mobile-first, light and dark theme. 
6. Data
 
There is no database yet, so the generator reads JSON from site/data/. The format must match the future PostgreSQL export (schema schema_v0_1.sql, tables core.scores, billing.tariffs), so that later the source can be swapped without reworking templates.
 
Example site/data/ratings/wb/palatki/2026-W39.json:
{
  "category": {"marketplace": "wb", "slug": "palatki", "name": "Tourist tents"},
  "week": "2026-W39",
  "measured_at": "2026-09-21",
  "method": {"queries": 40, "models": ["sonar"], "runs": 3, "formula_version": "1.0"},
  "brands": [
    {"rank": 1, "brand": "Testbrand A", "share": 0.31, "change": 0.02}
  ]
}
 
Important:
• Test data must contain only fictional brands. Publishing invented ratings of real brands is forbidden.
• No personal data: only brands, without names or titles of seller-sole proprietors. 
7. Checks (the site is deployed automatically, so the build fails on any error)
 
Tests on pytest:
• all pages build, HTML is valid;
• JSON-LD on every page parses;
• all rating text is present in the raw HTML (without JavaScript execution);
• there are no links to external resources in the HTML;
• there are no personal data patterns (e.g., "ИП " with a full name);
• archived pages' addresses have not changed compared to the previous build. 
8. Repository structure
site/
  generator/     # page assembly
  templates/     # Jinja2
  static/        # CSS, font, icons
  data/          # JSON (later — export from the database)
  tests/
  dist/          # result, not stored in git
Caddyfile
docker-compose.site.yml
Makefile         # make build, make test, make serve
 
9. Out of scope
 
Legal texts, real data, payment acceptance, domain purchase, deployment to the server (the server has not been ordered yet).
 
10. Deliverable
• A working generator: make build assembles the site from test data, make test passes, make serve shows the site locally.
• A short README: how to add a rating week and how the database will be connected.
• Work in small commits. If a decision is not obvious — ask, do not guess.