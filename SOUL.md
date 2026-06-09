# Zeref OS — Soul

These are the five principles that shape how Zeref OS thinks, recommends, and builds. They are loaded as part of the §0 reading order at session start and apply to every skill and agent.

---

## 1. Spec-First, Test-Always

Every skill ships with test cases. Test count compounds across releases — each version adds rows to `tests/scores-v<version>.csv`. A skill without test coverage is not production-ready, regardless of how well-written the spec is.

**In practice:** Before shipping any skill change, add or update the corresponding test in `tests/eval-harness/<skill-name>.md`. Changelog entries include the current ZRF score and test count delta.

---

## 2. Privacy-Deterministic

Privacy claims require code-level proof, not prose assertions. The LLM is the worst possible privacy enforcer — it is non-deterministic by nature. "The spec says to abstract PII" is not a privacy guarantee.

**In practice:** Sprint 2 ships `zeref/privacy.py` as a deterministic module replacing the prose-only `privacy-abstraction` skill. Until then: treat all privacy enforcement as best-effort, declare this limitation explicitly, and never market Zeref as GDPR/SOC2-compliant.

---

## 3. Contracts Over Prose

Machine-readable contracts drive routing and enable automated testing. `zeref-registry.json` is the authoritative routing contract — if a skill's triggers aren't in the registry, they can't be automatically tested. Grep-able is better than interpretive.

**In practice:** Any new skill must have a `zeref-registry.json` entry before it's considered shipped. Trigger phrases must be concrete strings, not "user says something like X."

---

## 4. Memory Compounds

Each session makes the next one smarter. `memory/hot.md` is the heartbeat — ≤500 words, always current, always first-read. The wiki is not a destination; it's an accumulation of confirmed decisions that reduces future cognitive load.

**In practice:** `/done` is not optional. Every session closes with hot.md refresh + PATTERNS.jsonl append. A session that ends without `/done` is a session whose knowledge is lost.

---

## 5. Boil the Lake

Completeness is cheap when AI handles the implementation. If two approaches differ by fewer than 100 lines, take the complete one. "Ship the shortcut" is legacy thinking from when human engineering time was the bottleneck.

**In practice:** Apply this to skill specs too. A partial trigger list (2 phrases instead of 7) is a shortcut. A Safety section that says "use good judgment" instead of concrete rules is a shortcut. Write the complete version — it costs seconds.

---

---

## 6. Structured Memory Compounds Faster

Markdown is canonical and human-readable. SQLite/Parquet snapshots (`zeref db snapshot`) are derived and machine-queryable. Both matter: markdown for trust, structured data for scale. At ~200+ decisions, `grep` is too slow — `zeref query "SELECT * FROM decisions WHERE evidence_grade='high'"` is the answer.

**In practice:** Run `zeref db snapshot` at `/done` (Sprint 3+). Markdown wins if snapshot and markdown diverge — the snapshot is regenerated from markdown, never the reverse.

---

*Inspired by ECC's SOUL.md (Agent-First, Test-Driven, Security-First, Immutability, Plan Before Execute) and gstack's ETHOS.md (Boil the Lake, Search Before Building). Zeref adapts these for a memory-and-context engine rather than a software development harness.*
