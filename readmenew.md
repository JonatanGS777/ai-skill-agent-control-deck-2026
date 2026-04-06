# Universal Skill Creator (Claude Code + Codex)

This document explains how to create a single reusable skill for:

- Claude Code (`~/.claude/skills`)
- Codex (`~/.codex/skills`)

The idea is to have a canonical source for the skill in your repo and then install it in both systems via `symlink` or `copy`.

## Main File

- Script: `scripts/universal_skill_creator.py`

## What the Script Creates

When you run the creator, it generates a skill folder with the following structure:

```text
skills/<skill-name>/
├── SKILL.md
├── README.md
├── skill.meta.json
├── examples/
│   └── prompts.md
├── references/
│   └── .gitkeep
├── scripts/
│   └── .gitkeep
└── assets/
    └── .gitkeep
```

## SKILL.md Format

```markdown
---
name: skill-name
version: 1.0.0
domain: domain
foundation_skills:
  - logic-propositional-reasoning
compatibility:
  - claude-code
  - codex
---

# Skill Name

## Mission
Clear, verifiable objective.

## When to Use
Triggering conditions for this skill.

## Workflow
1. Step one.
2. Step two.
3. Step three.

## Output Contract
Expected result format and acceptance criteria.

## Guardrails
- Safety boundary 1
- Safety boundary 2
```

## Usage

```bash
python scripts/universal_skill_creator.py \
  --name my-skill \
  --domain engineering \
  --title "My Skill" \
  --description "What this skill does"
```

## Installing in Claude Code

```bash
# Via symlink (recommended — changes sync automatically)
ln -s $(pwd)/skills/my-skill ~/.claude/skills/my-skill

# Via copy
cp -r skills/my-skill ~/.claude/skills/
```

## Installing in Codex

```bash
ln -s $(pwd)/skills/my-skill ~/.codex/skills/my-skill
```
