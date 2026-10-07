-- Reference data without which the line does not start. Executed once when the database is created.

INSERT INTO core.marketplaces (code) VALUES ('wb');

-- Six shops (brief section 5). The funnel (3) is served by the Telegram bot.
INSERT INTO line.workshops (id, code, stream) VALUES
  (1, 'leads',      'acquisition'),
  (2, 'mini_audit', 'acquisition'),
  (3, 'funnel',     'acquisition'),
  (4, 'sales',      'acquisition'),
  (5, 'monitoring', 'service'),
  (6, 'retention',  'service');

-- Supermarket buffers before the consumer shop (brief section 6).
-- card_limit — starting value: D and L are unknown until the first weeks of operation,
-- later the limit is recalculated as N = D × L × (1 + α) / C (self-learning, section 8).
INSERT INTO line.buffers (code, workshop_id, card_limit, max_age, params) VALUES
  ('leads_store',      2, 200, interval '14 days',
   '{"D": null, "L": null, "alpha": 0.15, "C": null, "note": "measurement older than 2 weeks is a defect"}'),
  ('mini_audit_store', 3, 100, interval '7 days',
   '{"D": null, "L": null, "alpha": 0.15, "C": null, "note": "mini-audit older than a week is not sent"}'),
  ('onboarding',       5,  20, interval '1 day',
   '{"D": null, "L": null, "alpha": 0.15, "C": null, "note": "first measurement within 24 hours"}');