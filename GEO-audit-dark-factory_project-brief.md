GEO audit for sellers: dark factory
 
Summary of project decisions. Document for the Claude Project knowledge base. Status: concept approved, technical implementation underway. Version 2 (23.09.2026): added self-learning, reinvestment rule, autonomous category selection, unified query sets.
 
1. Essence of the service
 
An automated service that measures and increases a seller’s product visibility in AI assistant answers (ChatGPT, Perplexity, Alisa, GigaChat, etc.). Evolution logic: SEO → marketplace promotion → promotion for AI agents (GEO).
 
The main product metric is share in AI answers: in what percentage of answers to typical buyer queries the client’s brand is mentioned (weighted by position).
 
2. Business model (result of the tournament of 55 templates)
 
Tournament based on the book “Business Models: 55 Best Templates.” Criteria: automatability, speed to first money, margin and recurring revenue, protection from competitors (equal weights). Estimates are expert.
 
Winning core (maximum points):
• Freemium — free mini-audit as entry.
• Cash machine — prepayment: full audit and monitoring paid upfront.
• Subscription — monthly monitoring of share in AI answers.
• Customer lock-in — measurement history stored by the service.
• Data management — consolidated database of AI answers by category as the main barrier for competitors. 
The final bundle added “No frills” and “Digitization” — these are execution style, not pillars. Tournament conclusion: more than 5 models — complexity eats the benefit.
 
Product ladder (prices are hypotheses):
• Mini-audit — free (10 queries, one metric). Built as a slice of the weekly category measurement, without separate API calls.
• Full audit — one-time payment (50 queries, all models, gaps in sources, work plan).
• Monitoring — subscription, price by number of SKUs/categories; annual plan with discount for prepayment.
• Implementation — product card improvement per SKU; external content — through partners for commission. 
Rejected at start: payment for share growth (noisy metric), agency retainer (manual labor).
 
3. Strategy (backcasting)
 
Goal in 12–18 months: standard for measuring AI visibility in several marketplace categories; clients come on their own, most pay upfront, measurement base is an insurmountable asset.
• Months 9–12: public ratings “whom AI recommends”; expansion to new categories happens automatically according to the rules of section 10.
• Months 5–8: retention, reports with dynamics, annual plans, upsells.
• Months 2–4: debugging conversion from free audit to paid.
• Month 1: auditor for one category; weekly measurement of two tourism subcategories from the first month (needed so mini-audits in the funnel are always fresh). 
Rules: data is collected from day one and across the entire category; at start 2–3 categories densely, then the ceiling grows with revenue (section 10); prepayment is built into tariffs from the very beginning.
 
4. Architecture of the auditor agent
 
Two branches converge in scoring:
• Product card branch: card parser → analysis of attribute completeness against the category top.
• AI answers branch: query generator → model polling → mention extractor. 
Query generator: ~50 queries of five types — general, constrained, comparative, problem, branded.
• General, constrained, comparative, and problem — unified set per category, the same for all clients.
• Branded — separate client set.
• 10 mini-audit queries — fixed subset of the category set.
• Sets are frozen; change = new version, old measurements are not rewritten. 
Result: client and category measurements are directly comparable, each client measurement replenishes the shared base.
 
Model polling: only models with web search; each query × 3 runs (answers are unstable).
 
Extractor: cheap model with strict JSON schema — brands, products, positions, tone, sources; then mapping name variants to brands.
 
Scoring (three numbers for the client): share in answers; gap with leader; gaps in sources.
 
Report: one page — three numbers, top 3 fixes, details in attachment.
 
Data: all raw material is stored (clients, queries, runs, answers, mentions, scores) to recalculate metrics. The extractor and scoring formula have versions.
 
5. Dark factory: a line of 6 shops
1. Lead reconnaissance — measurement of the entire category.
2. Mini-audit — report for each seller.
3. Funnel — Telegram bot (instead of mailing and correspondence).
4. Sale and prepayment — offer, payment, receipt.
5. Monitoring — measurements and reports by subscription.
6. Retention and upsells — renewals, product card improvements. 
Control loop: QC (output check), andon (exceptions), dispatch (line metrics).
 
Principles: standard work of agents; error protection (result does not pass further without schema check); QC reconciles mentions with raw answers; the part stops, not the line.
 
Andon without people (decision: 0 minutes per day):
• AI “shift master” on a strong model handles complex cases.
• Safe mode by default: standard polite answer; complaint → automatic refund; dubious report is not sent, measurement is repeated; discounts — refusal with reference to tariffs.
• To the human — only an emergency signal in Telegram: bot blocking, legal claim, change in platform rules, irreparable model drift, approaching the self-employment limit.
• Separately from andon — a monthly summary of decisions by category in Telegram, no response required. 
Bottlenecks: dependence on model providers (need a backup); model drift (daily reference run as calibration).
 
6. Toyota kanban on the line
 
Two flows: acquisition (shops 1→4) and service (shops 5→6, pulled by the subscription calendar).
 
Supermarket buffers: lead warehouse (measurement older than 2 weeks — defect), mini-audit warehouse (older than a week — do not send), onboarding queue (first measurement within 24 hours).
 
Number of cards: N = D × L × (1 + α) / C, where D — demand per day, L — batch production time, α — safety stock 10–20%, C — batch size. Limit N is hardcoded in the database: a card cannot be placed in a full buffer.
 
Since there are no people on the line, limits are determined by the advertising budget, aggregator API limits, and QC defect percentage.
 
Heijunka: subscriber measurements evenly across days of the month; uniform advertising volume.
 
Metrics: lead time, WIP in buffers, output; Little’s law: time = WIP / output.
 
Visual dispatch board (e.g., Trello), real queues — in the database.
 
7. Accepted decisions
Question Decision
Acquisition Own Telegram channel with automatic ratings + advertising in seller channels (selection via Telemetr); both roads lead to the bot. No personal messages.
Andon 0 minutes per day, safe mode, emergency signals.
Lawyer Only AI lawyer: primary sources (laws, Roskomnadzor recommendations), cross-check by two models, document versions, monthly monitoring of laws.
Personal data Analytical database without PD; Telegram ID — in a separate pd schema of the same database, access only for the bot role, other shops see only an anonymized account id; payment data — with the payment service. Names of seller-sole proprietors (full name) are not saved by the parser — only brand and seller ID. Database — on a server in Russia.
Platform Wildberries first; data schema is platform-independent. Entry to Ozon is decided by the system itself (section 10).
Category Start: sports and tourism (tourist equipment), two subcategories with weekly measurement; priority — where AI answers are less concentrated on 2–3 brands. Further category selection — autonomous (section 10).
Models Aggregator AITUNNEL (rubles): Perplexity sonar line with search. Check: search versions of GPT, YandexGPT/GigaChat, request limits.
Parsing Own parser of public WB data (mini-audit, category measurements) + official Seller API with client token (paying clients) + Russian analytics service in reserve.
Sales channel Sellers directly; agencies (white-label) later. The database immediately supports many stores per account.
Legal form Self-employment at start; payment service with automatic receipts to “My Tax”; tax on all revenue (expenses are not deducted); signal to switch to sole proprietorship when approaching the limit.
Pilot No pilot. Diagnostics is sold first, not growth; starting price with automatic refund; cases from shared category measurements.
Accounting Online service, without employees.
Query sets Unified category set + client branded queries; mini-audit — subset of the category set.
Reinvestment 60% of net result — to the development fund (section 9).
Code changes Auto-deploy: tests, canary release, auto-rollback on defect increase.

 
8. Self-learning and self-development
 
The system develops itself, but by levels:
• Full autonomy: brand dictionary; buffer limits N based on actual D and L; bot texts, screen order, sending time, ad distribution (A/B by conversion); new safe mode rules from shift master analyses; category selection model.
• Through versions and shadow run (PDCA): extractor prompts, query generator, scoring formula, model selection. The new version works in parallel with the old, QC compares on the same raw answers, into production only if better. Old measurements are not rewritten.
• Does not change itself: money and refund logic, shares 60% and 15%, ramp-up period, forbidden category list, access to PD, offer and policy (only through the digital lawyer), frozen client query sets, obligations on paid subscriptions.
• Code: auto-deploy with tests, canary release, and auto-rollback. 
9. Finance: reinvestment
 
Net result = revenue − refunds − tax − operating expenses. 60% — to the development fund, 40% — to the owner.
 
Operating expenses: API, server, payment service commission, measurements of existing categories.
 
From the development fund: advertising, reconnaissance and ramp-up of new categories, backup model provider, entry to new platforms.
 
Period closing — once a month (API expenses are known by the end of the month).
 
Only the accumulated fund can be spent; if net result is negative, nothing goes to the fund.
 
Starting advertising — by the owner’s initial contribution to the fund.
 
Limiters: limit per experiment; stop-loss on customer cost; signal on the self-employment limit.
 
10. Autonomous category selection
 
Goal: net result per category with minimum data — not less than 15% of the development fund for reconnaissance (measurements of candidate categories).
 
Hierarchy: categories and subcategories; the system searches, evaluates, and opens itself.
 
Platforms: WB and Ozon; entry to Ozon (new parser, Ozon Seller API) is decided by the system.
 
Forbidden list: medicines, supplements, alcohol, tobacco, 18+.
 
Ceiling of categories on sale: at start 2–3, then grows. A new category opens only if simultaneously:
• the development fund covers the entire 3-month ramp-up — after the advertising reserve of existing profitable categories;
• all current categories outside ramp-up are profitable. 
Ramp-up cost: first estimate — by the starting advertising and measurement budget, then refined by actual previous ramp-ups.
 
Ramp-up: 3 months. If not profitable — closed completely: advertising, sales, and weekly measurement stop. Paid subscriber monitoring continues until the end of the term; raw data is saved; later the category may become a candidate again.
 
Self-analysis: decision journal — forecast and grounds when deciding, actual after ramp-up, discrepancy goes to training the selection model. No pauses after a series of errors: losses are limited by the development fund.
 
Reporting to the owner: monthly summary of decisions in Telegram without response.
 
11. Infrastructure
 
Server: one Russian VPS (recommended Timeweb Cloud; alternative — Selectel). Ubuntu 24.04, 2 vCPU, 4 GB RAM, 40–60 GB NVMe, Moscow or St. Petersburg, automatic backups.
 
Setup: setup_server.sh script — update, factory user, SSH-key-only login, firewall, fail2ban, swap, Docker, check access to Telegram, aggregator, and parser.
 
Stack: Python, PostgreSQL, Docker Compose. Kanban queues — in PostgreSQL (FOR UPDATE SKIP LOCKED), without a separate broker.
 
Database: schema_v0_1.sql — schemas core (measurements without PD), line (kanban, defect isolator, andon), billing (tariffs, payments, funds), growth (categories, decision journal), pd (only Telegram ID, access only for the bot role).
 
Website (approved): minimal static website on the same server — offer and PD policy, payment service requirements, public ratings as a source for AI with search. Generated from the database as ready HTML (content available to AI crawlers without JavaScript execution), animations — only on top, via CSS. No maintenance required.
 
Secrets (API keys, bot token) — only in the settings file on the server, not in chats.
 
12. Next steps
• Check in the AITUNNEL panel: search versions of GPT, Russian models, limits.
• Order server, run setup_server.sh, get access check results.
• Database schema — draft v0.1 ready; refine based on the results of the first shop.
• Docker configuration: database, bot, shop workers with one command.
• First shop: WB parser + query generator + model polling for two tourism subcategories, weekly.
• Telegram bot as the entrance door of the line.
• Digital lawyer: offer, PD policy.