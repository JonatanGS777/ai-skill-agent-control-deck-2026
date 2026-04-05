# Anti-Patterns

## 1) Skills Without an Output Contract

Problem: ambiguous, non-auditable responses.
Fix: define output format, acceptance criteria, and a final checklist.

## 2) Agents With Too Many Active Skills and No Prioritization

Problem: incoherent or contradictory responses.
Fix: use domain-based selection + max limit + controlled `hybrid` mode.

## 3) Large Changes Without Benchmark/Regression

Problem: local improvements break previous behaviors.
Fix: run `make quality` before merging.

## 4) Inconsistent Manual Versioning

Problem: opaque change history.
Fix: use `semantic_version_manager.py` + automated release bundle.

## 5) Prompts Without a Logical Foundation

Problem: hallucinations and meaningless steps.
Fix: add math/programming foundations to skill and agent metadata.
