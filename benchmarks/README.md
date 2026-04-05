# Benchmark Suite 2026

This folder defines the first functional benchmark layer for the repository.

Goals:
- Evaluate every local skill and agent with a consistent quality rubric.
- Track regression checks for prompt templates and core structural contracts.
- Validate real-world scenario coverage across automation, chatbot, and domain AI.
- Export machine-readable benchmark outputs used by CI and catalog reports.

## Files

- `suite.json`: scoring weights, thresholds, and regression constraints.
- `cases/real-world-process-cases.json`: real-world benchmark scenarios with expected capability coverage.

## Runner

Run:

```bash
python3 scripts/run_benchmarks.py --strict
```

Outputs:
- `catalog/benchmark-results.json`
- `catalog/benchmark-history.json`
- `catalog/skill-quality-ranking.json`
- `catalog/agent-quality-ranking.json`

When `--strict` is enabled, the script exits non-zero if:
- Any skill/agent fails the score thresholds.
- Any regression check fails.
- Any real-world coverage case fails.
