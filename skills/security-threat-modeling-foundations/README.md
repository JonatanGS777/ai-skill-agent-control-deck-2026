# Security Threat Modeling Foundations

This folder contains a universal skill designed to work in both:

- Claude Code (`~/.claude/skills/security-threat-modeling-foundations`)
- Codex (`~/.codex/skills/security-threat-modeling-foundations`)

## Purpose
Builds threat models with attacker capability analysis and control-mapping logic.

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
