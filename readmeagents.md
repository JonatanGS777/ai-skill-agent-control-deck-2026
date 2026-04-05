# Universal Agent Creator (Claude Code + Codex)

This generator creates universal agents compatible with Claude Code and Codex,
and configures them to work with skills via their internal protocol.

## Main File

- `scripts/universal_agent_creator.py`

## What It Creates

For each agent it generates:

```text
agents/<agent-name>/
├── AGENT.md
├── README.md
├── agent.meta.json
├── references/
│   └── skill-index.md
├── examples/
│   └── prompts.md
├── scripts/
│   └── .gitkeep
└── assets/
    └── .gitkeep
```

It also installs an entrypoint at:

- `~/.claude/agents/<agent-name>.md`
- `~/.codex/agents/<agent-name>.md`

## Skill Bootstrap Protocol

Each generated agent includes an internal block to:

1. Detect capabilities required by the task.
2. Select relevant skills (manual and/or auto).
3. Merge rules and guardrails from those skills.
4. Execute with a unified plan and final validation.

## Skill Modes

- `--skill-mode explicit`: only uses manual `--skill` entries.
- `--skill-mode auto`: detects skills automatically from sources.
- `--skill-mode hybrid` (default): combines manual + auto.
- `--logic-foundation`: adds logical foundation (`none`, `core`, `standard`, `max`) for reasoning robustness.

Default skill sources:

- `skills`
- `~/.claude/skills`
- `~/.codex/skills`

## Quick Usage

### 1) Create an orchestrator agent with auto + manual skills

```bash
python3 scripts/universal_agent_creator.py \
  --name "product orchestrator 2026" \
  --description "Orchestrates full-stack implementations with a production quality focus." \
  --agent-type orchestrator \
  --skill fullstack-ultramodern-2026 \
  --skill frontend-ultramodern-2026 \
  --skill-mode hybrid \
  --install-target both \
  --install-method symlink
```

### 2) Create an agent without installing (repo only)

```bash
python3 scripts/universal_agent_creator.py \
  --name "api quality reviewer" \
  --description "Technical API reviewer focused on risk and maintainability." \
  --agent-type reviewer \
  --install-target none
```

### 3) Dry run without writing files

```bash
python3 scripts/universal_agent_creator.py \
  --name "debug commander" \
  --description "Complex production incident diagnostics." \
  --agent-type debugger \
  --dry-run
```

## Key Flags

- `--name`, `--description`: required.
- `--agent-type`: `orchestrator`, `builder`, `reviewer`, `debugger`, `specialist`.
- `--skill`: manual skill (repeatable).
- `--skill-mode`: `explicit`, `auto`, `hybrid`.
- `--logic-foundation`: `none`, `core`, `standard`, `max`.
- `--max-profile-skills`: limits final profile skills to avoid overload.
- `--skill-source`: skill sources (repeatable).
- `--max-auto-skills`: auto-selection limit.
- `--strict`: fails if explicit skills don't exist in detected sources.
- `--install-target`: `both`, `claude`, `codex`, `none`.
- `--install-method`: `symlink` (recommended) or `copy`.
- `--overwrite`, `--dry-run`.

## Team Recommendations

1. Create agents in `agents/` as the canonical source.
2. Install via `symlink` so local changes propagate to both ecosystems.
3. Version `AGENT.md` + `references/skill-index.md`.
4. Periodically review skills selected by `auto` mode.

## Group Aliases for Activation

To activate agents with a group name (e.g. `ceo-jonatan-agent--...`):

```bash
python3 scripts/install_agent_group_aliases.py \
  --agent-root agents \
  --group-name "CEO Jonatan Agent" \
  --install-target both \
  --overwrite
```

With Makefile:

```bash
make aliases GROUP_NAME="CEO Jonatan Agent"
```

To keep batch-created agents in a separate group:

```bash
make aliases-created
```

This installs aliases with prefix:
- `ceo-jonatan-creados--<agent>.md`

To keep the 100 AI Factory agents separate:

```bash
make aliases-ai
```

This installs aliases with prefix:
- `ceo-jonatan-ai-factory--<agent>.md`

## CI Quality Gate

GitHub Actions workflows are included at:

- `.github/workflows/repository-quality.yml`
- `.github/workflows/release-bundle.yml`

This workflow runs:
1. `py_compile` on main scripts.
2. `python scripts/semantic_version_manager.py --mode check --scope both --strict`.
3. `python scripts/run_benchmarks.py --strict`.
4. `python scripts/rebuild_repo_catalog.py --strict`.
5. `python scripts/build_quality_dashboard.py`.
6. Publishes `catalog/*` as a workflow artifact.

Includes visual dashboard:
- `catalog/quality-dashboard.html`
- `docs/portal/index.html`

And contribution governance:
- `CONTRIBUTING.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/governance/review-checklist.md`
- `docs/governance/definition-of-done.md`

## Semantic Versioning for Agents

To maintain consistent versioning in `AGENT.md` + `agent.meta.json`:

```bash
python3 scripts/semantic_version_manager.py --mode apply --scope agents
python3 scripts/semantic_version_manager.py --mode check --scope agents --strict
```

You can also use:

```bash
make semver-apply
make semver-check
make benchmarks
make docs-portal
make release-auto
```
