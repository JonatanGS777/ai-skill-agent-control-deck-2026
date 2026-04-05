# Algorithm Correctness Invariants

This folder contains a universal skill designed to work in both:

- Claude Code (`~/.claude/skills/algorithm-correctness-invariants`)
- Codex (`~/.codex/skills/algorithm-correctness-invariants`)

## Purpose
Validates algorithm correctness using invariants, preconditions, and postconditions.

## Files
- `SKILL.md`: main behavior and rules
- `references/`: optional docs and examples
- `references/quality-gates.md`: logical/quality acceptance criteria
- `scripts/`: optional automation helpers
- `assets/`: optional static resources
- `skill.meta.json`: metadata for portability/versioning

## Usage
1. Install the skill in Claude/Codex (symlink or copy).
2. Trigger it by name from your prompt.
3. Iterate on `SKILL.md` based on real outcomes.
