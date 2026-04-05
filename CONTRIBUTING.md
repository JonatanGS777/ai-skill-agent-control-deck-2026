# Contributing

Thank you for contributing to this repository.

## Required Workflow

1. Create a working branch.
2. Implement small, focused changes.
3. Run:

```bash
make quality
```

4. If the change involves a release, run:

```bash
make release-auto
```

5. Open a PR using the official template.

## Standards

- Maintain compatibility between Claude Code and Codex.
- Prioritize logic, clarity, security, and utility.
- Avoid generic prompts/agents without a solid foundation.
- Add/update documentation whenever behavior changes.

## Reviews

Before merging, validate against:
- `docs/governance/review-checklist.md`
- `docs/governance/definition-of-done.md`

## Commit Conventions

Suggested format:
- `feat: ...`
- `fix: ...`
- `docs: ...`
- `chore: ...`
- `refactor: ...`
- `test: ...`
