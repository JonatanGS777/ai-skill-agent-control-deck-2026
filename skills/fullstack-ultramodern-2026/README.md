# Fullstack Ultramodern 2026

This folder contains a universal skill designed to work in both:

- Claude Code (`~/.claude/skills/fullstack-ultramodern-2026`)
- Codex (`~/.codex/skills/fullstack-ultramodern-2026`)

## Purpose
Construye productos full stack 2026 con React 19, TypeScript, Tailwind y arquitectura moderna de producción.

## Files
- `SKILL.md`: core behavior and delivery contract
- `references/fullstack-stack-2026.md`: stack guidance by layer and scenario
- `examples/prompts.md`: prompt recipes for common full stack tasks
- `skill.meta.json`: metadata for compatibility/versioning

## Usage
1. Mention `fullstack-ultramodern-2026` in your prompt.
2. Provide scope, stack constraints, and production expectations.
3. Request architecture + implementation + validation in one pass.

## Prompt template
`Use fullstack-ultramodern-2026. Build [feature/product] with React 19 + TypeScript + Tailwind. Include API, data model, auth/security baseline, testing plan, and production-readiness checks.`

## Notes
- This skill is symlinked into both Claude and Codex, so edits here update both.
- Keep `references/fullstack-stack-2026.md` aligned with your team standards.
