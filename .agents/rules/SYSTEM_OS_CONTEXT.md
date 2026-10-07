Second Brain v4.1.0 Production Context

You are an expert in local Agent Skills. When working with this project, follow the strict audit rules v4.1.0:

1. Storage: SQLite WASM + IndexedDB with mandatory handling of onerror and reject for Promise.
2. Offline-First: Complete isolation from the network. All binary dependencies — in scripts/vendor/.
3. Security: Parameterized SQL. No LIKE '%${query}%' — only db.exec(query, [params]).
4. Native Bridge: Call the OS via Intent URI Android/HarmonyOS 2026 (window.open('intent://...')).
5. RKC: Discovered bugs and architectural decisions are recorded in SKILL.md immediately.