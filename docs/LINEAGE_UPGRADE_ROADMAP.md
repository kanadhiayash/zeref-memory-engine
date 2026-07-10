# Zeref 64-Repo Lineage Upgrade Roadmap

This roadmap documents the non-stacked `dev` integration program for the 64-row Zeref lineage intake. It is evidence-bound: the table below reflects local intake, council, implementation, and benchmark gates, not external-dataset verification of the referenced projects.

## Branch Model

- `main` remains the protected default branch.
- `dev` is the integration branch.
- Each upgrade branch starts from `dev` and opens one PR back to `dev`.
- The final promotion is one PR from `dev` to `main`.
- `.zeref-sandbox/` and runtime `memory/` outputs stay untracked.

## Executed Branch Map

| Order | Branch | Target | Gate |
|---:|---|---|---|
| 1 | `chore/zeref__clean-dev-worktree` | `local cleanup only` | removed duplicate scratch files; no tracked PR needed |
| 2 | `feat/zeref__lineage-intake-auditor` | `dev` | `zeref lineage audit --csv ...` |
| 3 | `feat/zeref__default-branch-sandbox-importer` | `dev` | `zeref lineage import --sandbox --latest-default --dry-run` |
| 4 | `feat/zeref__lineage-council-engine` | `dev` | `zeref lineage council --strict` |
| 5 | `feat/zeref__critical-lineage-implementations` | `dev` | `zeref lineage critical --strict` |
| 6 | `feat/zeref__high-lineage-implementations` | `dev` | `zeref lineage high --strict` |
| 7 | `feat/zeref__reference-only-battle-tests` | `dev` | `zeref lineage reference --strict` |
| 8 | `feat/zeref__benchmark-governor-v3` | `dev` | `python3 benchmarks/run-all.py` plus lineage axes |
| 9 | `docs/zeref__64-repo-upgrade-roadmap` | `dev` | this document plus standard gates |
| 10 | `release/zeref__dev-to-main-v3-upgrade` | `main` | final dev/main gates and promotion PR |

## Council Verdict Table

| Row | Source | Priority | Lens | Verdict | Implementation form | Boundary or gate |
|---:|---|---|---|---|---|---|
| 1 | Zeref Memory Engine | critical | Release | adopt | core-gate | lineage intake, council, and critical audit keep Zeref identity primary |
| 2 | Software 2.0 | medium | Memory | reference-only | principle-fixture | public claims require executable evidence |
| 3 | claude-obsidian | critical | Memory | adapt | core-gate | tracked memory scaffold and single-writer memory APIs |
| 4 | Graphify | high | Graph | adapt | optional-adapter | graph remains rebuildable from atoms |
| 5 | graphify | medium | Graph | reference-only | graph-contrast | no duplicate graph system in core |
| 6 | gstack | high | Agent Routing | adapt | routing-policy | capped team activation only |
| 7 | caveman | high | Release | adapt | handoff-policy | compression cannot remove exact constraints |
| 8 | ECC | high | Agent Routing | adapt | escalation-policy | no always-on council |
| 9 | council-of-high-intelligence | medium | Agent Routing | reference-only | council-guardrail | debate requires evidence and strict scope |
| 10 | stop-slop | high | Security Rails | adapt | quality-guardrail | fact/public-claim scans |
| 11 | mem0 | critical | Memory | adapt | core-gate | atom schema enforces active/stale/superseded/disputed/archived |
| 12 | ponytail | critical | Minimality | adopt | core-gate | foreign code containment and optional adapter boundaries |
| 13 | pm-skills | medium | Product Quality | adapt | monitor/reject | optional skill pack |
| 14 | Microsoft GraphRAG | critical | Graph | adapt | core | graph cache is rebuildable from atom JSONL and never canonical |
| 15 | Microsoft Kernel Memory | critical | Retrieval | adopt | core | atom schema requires source, evidence, and provenance fields |
| 16 | Meta Faiss | high | Retrieval | monitor | optional-adapter | stdlib lexical retrieval remains core |
| 17 | Google ScaNN | medium | Retrieval | monitor | monitor/reject | optional adapter later |
| 18 | Apple MLX | medium | Retrieval | monitor | monitor/reject | future optional adapter |
| 19 | Salesforce LAVIS | low | Memory | reference-only | scope-guardrail | no multimodal expansion before text memory is stable |
| 20 | Meta TRIBE v2 | low | Memory | reference-only | scope-guardrail | no neuroscience framing in public Zeref positioning |
| 21 | Google DeepMind Concordia | high | Benchmark | adapt | benchmark-fixture | no runtime dependency |
| 22 | claude-obsidian | critical | Memory | adapt | core-gate | legacy Markdown remains view/scaffold while JSONL atoms are machine source |
| 23 | Google ADK Python | high | Agent Routing | adapt | contract-reference | Zeref does not become an agent framework |
| 24 | OpenAI Agents SDK | high | Agent Routing | monitor | optional-adapter | permissioned and opt-in only |
| 25 | Microsoft Semantic Kernel | high | Agent Routing | adapt | plugin-boundary | orchestration stays outside core |
| 26 | AWS AgentCore Samples | medium | Agent Routing | reference-only | lifecycle-fixture | no cloud runtime assumption |
| 27 | Agent Squad | high | Agent Routing | adapt | routing-policy | route decisions require evidence |
| 28 | Salesforce Agentforce ADLC | medium | Agent Routing | reference-only | lifecycle-fixture | no platform-specific lifecycle assumption |
| 29 | pm-skills | medium | Product Quality | adapt | monitor/reject | optional skill pack |
| 30 | gstack | high | Agent Routing | adapt | routing-policy | caps prevent role bloat |
| 31 | caveman | high | Release | adapt | handoff-policy | source-backed compression |
| 32 | ECC | high | Agent Routing | adapt | escalation-policy | 5.5 High only for final arbitration/security/verdict |
| 33 | MCP Reference Servers | high | Connector Governance | adapt | connector-governance | external writes require approval |
| 34 | GitHub MCP Server | high | Connector Governance | monitor | optional-adapter | audit all external writes |
| 35 | Microsoft Playwright MCP | high | Benchmark | adapt | benchmark-fixture | outside memory core |
| 36 | Composio | medium | Connector Governance | reference-only | connector-guardrail | connectors cannot own Zeref trust boundary |
| 37 | Firecrawl | medium | Connector Governance | monitor | monitor/reject | optional ingest adapter |
| 38 | Hugo | low | Minimality | reference-only | export-guardrail | docs export must not leak private memory |
| 39 | GitHub Actions | critical | Release | adopt | ci-gate | pull requests to dev/main run pinned pytest, privacy, and version checks |
| 40 | NVIDIA NeMo Guardrails | critical | Security Rails | adapt | core-gate | privacy audit, fact/evidence guards, and release checks gate risky output |
| 41 | Meta Purple Llama | high | Security Rails | adapt | security-fixture | defensive eval only |
| 42 | raptor | medium | Security Rails | reference-only | security-containment | read-only defensive reference |
| 43 | mantishack | medium | Security Rails | reference-only | security-containment | no offensive capability bundled |
| 44 | hacker-bob | medium | Security Rails | reference-only | security-containment | permission gate every security workflow |
| 45 | hackingtool | low | Security Rails | reject | monitor/reject | reject code, keep policy lesson |
| 46 | Microsoft Responsible AI Toolbox | high | Benchmark | adapt | failure-analysis | expected/actual/fix/test fields |
| 47 | Microsoft PromptFlow | critical | Benchmark | adapt | eval-gate | benchmark runner plus failure analysis emits expected/actual/fix/test fields |
| 48 | Microsoft PromptBench | high | Benchmark | adapt | benchmark-fixture | fixture-only, archived reference |
| 49 | OpenAI simple-evals | high | Benchmark | adapt | benchmark-fixture | stdlib local runner |
| 50 | Netflix Metaflow | medium | Benchmark | reference-only | run-manifest-fixture | no workflow orchestrator dependency |
| 51 | Meta balance | medium | Benchmark | adapt | monitor/reject | scoring principle |
| 52 | Meta OpenApps | medium | Benchmark | monitor | monitor/reject | external benchmark adapter |
| 53 | Meta Agents Research Environments | medium | Benchmark | reference-only | benchmark-fixture | avoid overfitting to static sandboxes |
| 54 | Meta Habitat-Lab | low | Benchmark | reference-only | benchmark-fixture | do not ingest embodied-AI code |
| 55 | Salesforce CRMArena | medium | Benchmark | monitor | monitor/reject | external benchmark adapter |
| 56 | impeccable | low | Product Quality | reference-only | monitor/reject | optional skill reference |
| 57 | ui-ux-pro-max-skill | low | Product Quality | reference-only | monitor/reject | optional skill reference |
| 58 | taste-skill | low | Product Quality | reference-only | monitor/reject | optional skill reference |
| 59 | Motion | low | Product Quality | reference-only | downstream-ui-reference | frontend libraries stay outside core |
| 60 | HeroUI | low | Product Quality | reference-only | downstream-ui-reference | component libraries stay outside core |
| 61 | NotFair | low | Product Quality | reference-only | workflow-reference | Zeref is not marketing-specific |
| 62 | Apple AXLearn | low | Memory | reference-only | architecture-guardrail | training-stack complexity stays out of Zeref |
| 63 | Apple Core AI Models | low | Memory | monitor | monitor/reject | future optional path |
| 64 | Netflix Polynote | medium | Memory | adapt | monitor/reject | ordered-state principle |

## Verification Commands

```bash
python3 -m pytest -q
python3 benchmarks/run-all.py
python3 scripts/zeref-validate.py
python3 -m zeref.cli --version
python3 -m zeref audit-privacy --strict
python3 -m zeref.cli lineage audit --csv /path/to/ZRF_64_repo_lineage_intake.csv
python3 -m zeref.cli lineage import --sandbox --latest-default --dry-run
python3 -m zeref.cli lineage council --strict
python3 -m zeref.cli lineage critical --strict
python3 -m zeref.cli lineage high --strict
python3 -m zeref.cli lineage reference --strict
```

## Public-Safe Notes

- This roadmap does not claim external superiority, production readiness, or a perfect verdict.
- Lineage benchmark axes validate local intake metadata, implementation registries, and guardrails.
- Reference-only rows are implemented as evidence gates and guardrails only; their code is not bundled into runtime.
- Security-oriented references are defensive-only and permission-gated.
- Dependency additions remain out of scope unless approved in a dedicated PR.
