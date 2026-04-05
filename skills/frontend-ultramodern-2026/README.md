# Frontend Ultramodern 2026

This folder contains a universal skill designed to work in both:

- Claude Code (`~/.claude/skills/frontend-ultramodern-2026`)
- Codex (`~/.codex/skills/frontend-ultramodern-2026`)

## Purpose
Diseña interfaces frontend ultramodernas, adaptables al brief, con lenguaje visual distintivo y sin patrones genéricos de IA.

## Files
- `SKILL.md`: core behavior, workflow, and anti-generic audit
- `references/style-matrix-2026.md`: style selection matrix by brief
- `examples/prompts.md`: production-ready prompt recipes
- `skill.meta.json`: metadata for portability/versioning

## Usage
1. Trigger it by name in your prompt: `frontend-ultramodern-2026`.
2. Provide product goal + audience + desired tone + constraints.
3. Ask for both implementation and anti-generic audit.

## Recommended Prompt Pattern
`Use frontend-ultramodern-2026. Build [screen/page] for [audience] with [tone]. Tech stack: [stack]. Constraints: [a11y/performance/brand]. Avoid generic AI patterns and justify style direction.`

## Notes
- Installed for Claude and Codex through symlink, so edits here propagate to both.
- Keep the style matrix updated as your product language evolves.
