# Recommended Patterns

## Skill Pattern: Logic First

1. Define a verifiable objective.
2. Declare preconditions and assumptions.
3. Specify a workflow with finite steps.
4. Enforce final validation with measurable criteria.
5. Add security and scope guardrails.

## Agent Pattern: Skill Bootstrap Protocol

1. Interpret objective and constraints.
2. Select skills by domain.
3. Merge rules without contradictions.
4. Execute plan in stages.
5. Verify output against the contract.

## Quality Pattern: Everything Measurable

1. Publish scores for `logic`, `clarity`, `security`, `utility`.
2. Maintain prompt regression checks.
3. Run benchmarks in CI as a mandatory gate.
4. Display rankings and KPIs in the catalog/dashboard.

## Release Pattern: Quality Before Versioning

1. Run `make quality`.
2. Generate versioned bundle.
3. Update `CHANGELOG.md` and releases index.
4. Publish artifacts with the release workflow.
