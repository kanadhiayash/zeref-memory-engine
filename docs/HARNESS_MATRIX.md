# Harness Matrix — Zeref OS v1.0.0

Portability evidence: which harnesses Zeref OS has been booted in, what
worked, what didn't.

Schema:
- **Boot:** does the harness pick up `AGENTS.md` and the per-harness stub?
- **Memory read:** does `memory/hot.md` get loaded first?
- **Tool surface:** can the harness call `python3 -m zeref status` and the
  rest of the CLI?
- **Handoff:** can the harness produce `STATE.json` + `SUMMARY.md` + `NEXT.md`?

| Harness | Stub | Boot | Memory read | Tool surface | Handoff | Notes |
|---|---|:---:|:---:|:---:|:---:|---|
| Claude Code | `CLAUDE.md` | ✅ | ✅ | ✅ | ✅ | Reference harness. Plugin: `claude plugin install zeref-os@zeref-os`. |
| Codex | `CODEX.md` | ✅ | ✅ | ✅ | ⚠ | Slash-command syntax depends on Codex CLI version; raw `python3 -m zeref` always works. |
| Cursor | `.cursor/rules/zeref.mdc` | ✅ | ✅ | ✅ | ✅ | `git clone … .zeref && cp .zeref/.cursor/rules/zeref.mdc .cursor/rules/`. |
| Windsurf | `.windsurfrules` | ✅ | ✅ | ✅ | ✅ | `cp .zeref/.windsurfrules .`. |
| Aider | `.aider.conf.yml.example` | ✅ | ✅ | ✅ | ⚠ | Handoff requires shelling out to `python3 -m zeref`. |
| Gemini CLI / Antigravity | `GEMINI.md` | ✅ | ✅ | ✅ | ⚠ | Same as Codex — depends on CLI version. |
| Llama-family (Ollama, vLLM, Open WebUI) | `LLAMA.md` | ⚠ | ⚠ | ✅ via shell-tool | ⚠ | Reading order enforced via system prompt wrapper. |
| Hermes, Amp, Zed, Perplexity | — (read `AGENTS.md` directly) | ✅ | ✅ | ✅ | ⚠ | No stub needed; harnesses follow `AGENTS.md` directly. |

Legend:
- ✅ — verified in v1.0.0 smoke-test loop.
- ⚠ — works in principle, requires the wrapping harness to surface the
  command. Not a Zeref OS defect.

## Verification commands

Each cell above was verified by `scripts/harness-probe.py` plus a manual
smoke-test of `python3 -m zeref status` and one `write-decision` round
trip inside the host harness's terminal pane.

```bash
# in any harness, from your project root:
python3 scripts/harness-probe.py
python3 -m zeref status
python3 -m zeref write-decision \
  --title "Harness smoke test" --why "Verifying boot" \
  --evidence "harness-matrix" --grade medium
python3 -m zeref audit-privacy --strict
```

If the harness's stub is missing on a fresh checkout, the probe reports
which one and exits non-zero with `--all`.
