# External benchmark harness — honest methodology

**No external benchmark scores are claimed until full-dataset runs are
published.** Everything in this directory is infrastructure (WS5 Phase A).
The numbers produced by the internal quality axes (`benchmarks/run-all.py`)
are fixture-based self-checks and are NOT external benchmark results.

## What this is

A reproducible, provenance-bound harness for running the Zeref memory engine
and two honest baselines against real external datasets:

- Supported: **LoCoMo, LongMemEval, PersonaMem, RULER, HELMET** (`loaders/`).
- Explicitly unsupported, with reasons: see [`UNSUPPORTED.md`](UNSUPPORTED.md).
- Baselines (`baselines/`): `plain_files` (naive keyword-overlap file store)
  and `sqlite_fts` (simple SQLite FTS store). Phase B publishes zeref numbers
  **next to** these baselines or not at all.
- Providers (`providers/`): adapter interface with mandatory cost recording.
  The Anthropic adapter reads `ANTHROPIC_API_KEY` from the environment and in
  Phase A only supports dry-run token/cost estimation — live calls raise.

## Downloading datasets (manual, never automatic)

No code here downloads anything. For each benchmark, follow the loader's
docstring (official source URL + file placement), then validate offline:

```bash
python3 -m benchmarks.external.loaders.locomo --check /path/to/locomo
python3 -m benchmarks.external.loaders.longmemeval --check /path/to/longmemeval
python3 -m benchmarks.external.loaders.personamem --check /path/to/personamem
python3 -m benchmarks.external.loaders.ruler --check /path/to/ruler
python3 -m benchmarks.external.loaders.helmet --check /path/to/helmet
```

`--check` reports the dataset's sha256 so the hash can be pinned in the loader
(`PINNED_SHA256`) before any published run. A published result whose dataset
hash does not match the pin is invalid.

## Running (Phase A: dry-run only)

```bash
python3 -m benchmarks.external.harness \
  --benchmark locomo --data /path/to/locomo \
  --backend plain_files --provider anthropic --dry-run \
  --out benchmarks/external/results/locomo-dryrun.json
```

Dry-run ingests the haystack into the backend, performs recall, builds the
prompts, and estimates tokens/cost — with zero API calls. The only number it
produces is `retrieval_hit_proxy`, which is an infrastructure sanity signal,
not the benchmark's official metric, and must never be quoted as a score.

Every results JSON is bound to: git SHA, dataset name/version/sha256, model
id, prompts hash, token/cost record, timestamp, and mode (`dry_run`/`live`).

## What Phase B will publish (budget-gated)

- Full-dataset runs of zeref AND both baselines with the same provider,
  prompts, and recall budget, scored by each benchmark's own metric
  (exact match / token F1 / choice accuracy as defined per loader).
- Provenance for every number: dataset hash pinned, git SHA, model id,
  prompts hash, and the real (not estimated) token/cost record.
- Failures and losses included — if a baseline beats zeref on an axis, that
  is published too.

Until those runs exist, the only honest claim is: "the harness exists and the
loaders validate the datasets". Nothing here supports a ranking claim.
