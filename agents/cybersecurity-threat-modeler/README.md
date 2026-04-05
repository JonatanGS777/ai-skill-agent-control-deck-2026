# Cybersecurity Threat Modeler

This folder contains a universal agent compatible with:

- Claude Code (`~/.claude/agents/cybersecurity-threat-modeler.md`)
- Codex (`~/.codex/agents/cybersecurity-threat-modeler.md`)

## Purpose
Realiza modelado de amenazas, priorización de riesgos y diseño de contramedidas de seguridad.

## Files
- `AGENT.md`: canonical behavior and skill bootstrap protocol
- `references/skill-index.md`: selected/auto skills + logic foundation details
- `examples/prompts.md`: prompt recipes to invoke this agent
- `agent.meta.json`: metadata for portability/versioning

## Usage
1. Mention this agent and provide task scope plus constraints.
2. Ask for architecture, implementation, and validation in one flow.
3. Let the agent compose skills using its `Skill Bootstrap Protocol`.
