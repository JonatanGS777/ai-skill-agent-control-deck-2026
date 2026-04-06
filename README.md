<div align="center">

# AI Skill & Agent Control Deck 2026

**Drop 203 benchmarked skills and 196 agents directly into Claude Code.**

<img src="docs/branding/social-preview.png" alt="AI Skill & Agent Control Deck 2026" width="860"/>

<br/>

[![Version](https://img.shields.io/badge/version-v1.0.0-22c1ff?style=for-the-badge&logo=semver&logoColor=white)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-95e6bc?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![CI Quality](https://img.shields.io/badge/CI%20Quality-passing-4ade80?style=for-the-badge&logo=githubactions&logoColor=white)](.github/workflows/repository-quality.yml)
[![Skills](https://img.shields.io/badge/Skills-203-ff8b63?style=for-the-badge&logo=lightning&logoColor=white)](skills/)
[![Agents](https://img.shields.io/badge/Agents-196-a78bfa?style=for-the-badge&logo=robot&logoColor=white)](agents/)
[![Benchmark](https://img.shields.io/badge/Benchmark-100%25-22c1ff?style=for-the-badge&logo=checkmarx&logoColor=white)](catalog/benchmark-results.json)
[![Avg Score](https://img.shields.io/badge/avg%20score-93.26%2F100-22c1ff?style=for-the-badge)](catalog/benchmark-results.json)

<br/>

```
╔══════════════════════════════════════════════════════════════════╗
║    Build · Measure · Scale · Govern · Release                    ║
║    203 Skills  ·  196 Agents  ·  30 Logic Foundations           ║
║    Benchmark-driven  ·  Regression-safe  ·  Release-ready       ║
╚══════════════════════════════════════════════════════════════════╝
```

[Quick Start](#install-in-3-commands) · [Documentation](#documentation) · [Skills](skills/) · [Agents](agents/) · [Dashboard](catalog/quality-dashboard.html) · [Contributing](CONTRIBUTING.md)

</div>

---

## Install in 3 commands

```bash
git clone https://github.com/JonatanGS777/ai-skill-agent-control-deck-2026.git
cd ai-skill-agent-control-deck-2026
make bootstrap
```

> **Requires:** [Claude Code CLI](https://claude.ai/code) + Python 3.9+

---

## What is this?

This repository is a production platform for creating and managing **skills** (reusable capabilities) and **agents** (skill orchestrators) for Claude Code and Codex, featuring:

- **Explicit logical foundation** — every skill/agent declares its formal and mathematical dependencies
- **Measurable quality** — scored by `logic`, `clarity`, `security`, and `utility` for each component
- **Automated governance** — CI blocks PRs that fail benchmarks and regression checks
- **Domain coverage** — from propositional logic to applied AI across 20+ industries

---

## Repository Stats

<div align="center">

| Component | Count | Status |
|:---:|:---:|:---:|
| Specialized skills | **203** | ✅ Healthy |
| Orchestration agents | **196** | ✅ Healthy |
| Logic foundation skills | **30** | ✅ 100% covered |
| Benchmark pass rate | **100%** | ✅ Passing |
| Current version | **v1.0.0** | ✅ Stable |

</div>

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTROL DECK 2026                        │
├──────────────┬──────────────┬──────────────┬───────────────┤
│   SKILLS     │   AGENTS     │   CATALOG    │    DOCS       │
│              │              │              │               │
│  203 skills  │  196 agents  │  Index JSON  │  Portal HTML  │
│  SKILL.md    │  AGENT.md    │  Benchmarks  │  Patterns     │
│  meta.json   │  meta.json   │  Dashboard   │  Governance   │
│  examples/   │  examples/   │  Releases    │  Quickstart   │
└──────┬───────┴──────┬───────┴──────┬───────┴───────┬───────┘
       │              │              │               │
       ▼              ▼              ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│               QUALITY AUTOMATION (Makefile)                 │
│  make quality · make benchmarks · make dashboard           │
│  make docs-portal · make release-auto · make bootstrap     │
└─────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│                    CI / GitHub Actions                       │
│  repository-quality.yml  ·  release-bundle.yml             │
│  Python compile · Semver validation · Benchmark gate       │
└─────────────────────────────────────────────────────────────┘
```

---

## Domain Coverage

<div align="center">

| Category | Included Skills |
|---|---|
| **Logic & Mathematics** | Propositional reasoning, predicate quantifiers, proof strategies, Hoare logic, set theory, discrete structures, complexity analysis |
| **Applied AI** | Customer success, agritech, biotech, climate analytics, cybersecurity, ecommerce, education, energy, healthcare, legal, finance, logistics |
| **Software Engineering** | Full-stack, automation, workflow orchestration, security, testing, debugging, frontend frameworks |
| **Agent Types** | Auditor, Builder, Strategist, Reviewer |

</div>

### Agent Archetypes

Each industry domain includes 3 ready-to-use agent roles:

<div align="center">

| Archetype | Purpose |
|:---:|---|
| **Strategist** | High-level planning, decision intelligence, opportunity analysis |
| **Builder** | Implementation pipelines, automation, system construction |
| **Auditor** | Quality control, compliance, risk analysis, governance |

</div>

---

## Available Make Commands

```bash
make bootstrap      # Full repository initialization
make quality        # Full gate: compile + semver + benchmarks + catalog + dashboard
make benchmarks     # Run benchmark suite (scored across 4 dimensions)
make dashboard      # Generate interactive HTML quality dashboard
make docs-portal    # Generate HTML documentation portal
make catalog        # Rebuild skills/agents index
make release-auto   # Create automatic patch release
make logic-pack     # Install the 30 logic foundation skills
```

---

## Project Structure

```
ai-skill-agent-control-deck-2026/
│
├── skills/                    # 203 specialized skills
│   └── [skill-name]/
│       ├── SKILL.md           # Main definition (frontmatter + workflow + guardrails)
│       ├── README.md          # Installation and usage
│       ├── skill.meta.json    # Metadata and version
│       ├── examples/          # Example prompts
│       └── references/        # Quality gates and criteria
│
├── agents/                    # 196 orchestration agents
│   └── [agent-name]/
│       ├── AGENT.md           # Skill profile + logical core
│       ├── agent.meta.json    # Metadata
│       └── references/        # Agent skill index
│
├── catalog/                   # Quality indexes and benchmarks
│   ├── skills.index.json      # Searchable skill index
│   ├── agents.index.json      # Searchable agent index
│   ├── benchmark-results.json # Current scores (logic/clarity/security/utility)
│   ├── quality-dashboard.html # Interactive dashboard
│   └── releases/v1.0.0/       # Release notes
│
├── scripts/                   # 13 Python automation scripts
├── docs/                      # Documentation and governance
│   ├── patterns.md
│   ├── anti-patterns.md
│   ├── quickstart.md
│   ├── governance/
│   └── claude-code-guide.md   # Complete Claude Code guide
│
├── .github/workflows/         # CI/CD
├── Makefile                   # Build and quality automation
└── CONTRIBUTING.md            # Contribution workflow
```

---

## 4-Dimension Quality System

Every skill and agent is scored across:

```
┌────────────┬──────────────────────────────────────────────────────┐
│ Dimension  │ Description                                          │
├────────────┼──────────────────────────────────────────────────────┤
│ logic      │ Formal soundness: correctness, invariants, proofs    │
│ clarity    │ Documentation, examples, understandable instructions │
│ security   │ Threat handling, guardrails, boundary validation     │
│ utility    │ Practical value, real-world case coverage            │
└────────────┴──────────────────────────────────────────────────────┘

Top current score: fullstack-ultramodern-2026 (98.6/100)
```

---

## Documentation

| Resource | Description |
|---|---|
| [Claude Code Guide](docs/claude-code-guide.md) | Complete bilingual (ES/EN) reference — 18 sections, tools, memory, hooks, MCP, agents |
| [Quick Start](docs/quickstart.md) | Setup in 5 minutes |
| [Recommended Patterns](docs/patterns.md) | 5 proven patterns (Skill, Agent, Quality, Release) |
| [Anti-patterns](docs/anti-patterns.md) | 5 common mistakes and how to fix them |
| [Definition of Done](docs/governance/definition-of-done.md) | Acceptance checklist for contributions |
| [Review Checklist](docs/governance/review-checklist.md) | PR review checklist |
| [Docs Portal](docs/portal/index.html) | Auto-generated HTML portal |
| [Quality Dashboard](catalog/quality-dashboard.html) | Interactive score visualization |

---

## Contribution Workflow

```bash
# 1. Fork and clone
git clone https://github.com/[your-username]/ai-skill-agent-control-deck-2026.git

# 2. Create a feature branch
git checkout -b feat/new-skill-domain

# 3. Create skill using the universal script
python scripts/universal_skill_creator.py

# 4. Run quality gate locally
make quality

# 5. Open a Pull Request
# CI will automatically run: compile + semver + benchmarks
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow and contribution standards.

---

## Releases

| Version | Date | Channel | Status |
|---|---|---|---|
| [v1.0.0](catalog/releases/v1.0.0/release-notes.md) | 2026-04-05 | stable | ✅ Healthy |

---

## License

MIT © 2026 Yonatan Guerrero Soriano — see [LICENSE](LICENSE)

---

<div align="center">

**Built with logical rigor, measured with benchmarks, released with confidence.**

[Back to top](#ai-skill--agent-control-deck-2026)

</div>
