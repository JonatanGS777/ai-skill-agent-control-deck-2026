<div align="center">

# AI Skill & Agent Control Deck 2026

**El sistema definitivo para construir, medir y escalar skills y agentes de IA con base lógica sólida**

[![Version](https://img.shields.io/badge/version-v1.0.0-22c1ff?style=for-the-badge&logo=semver&logoColor=white)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-95e6bc?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![CI Quality](https://img.shields.io/badge/CI%20Quality-passing-4ade80?style=for-the-badge&logo=githubactions&logoColor=white)](.github/workflows/repository-quality.yml)
[![Skills](https://img.shields.io/badge/Skills-203-ff8b63?style=for-the-badge&logo=lightning&logoColor=white)](skills/)
[![Agents](https://img.shields.io/badge/Agents-196-a78bfa?style=for-the-badge&logo=robot&logoColor=white)](agents/)
[![Benchmark](https://img.shields.io/badge/Benchmark-100%25-22c1ff?style=for-the-badge&logo=checkmarx&logoColor=white)](catalog/benchmark-results.json)

<br/>

```
╔══════════════════════════════════════════════════════════════════╗
║    Build · Measure · Scale · Govern · Release                    ║
║    203 Skills  ·  196 Agents  ·  30 Logic Foundations           ║
║    Benchmark-driven  ·  Regression-safe  ·  Release-ready       ║
╚══════════════════════════════════════════════════════════════════╝
```

[Inicio Rápido](#-inicio-rápido) · [Documentación](#-documentación) · [Skills](skills/) · [Agentes](agents/) · [Dashboard](catalog/quality-dashboard.html) · [Contribuir](CONTRIBUTING.md)

</div>

---

## ¿Qué es esto?

Este repositorio es una plataforma de producción para crear y gestionar **skills** (capacidades reutilizables) y **agentes** (orquestadores de skills) para Claude Code y Codex, con:

- **Base lógica explícita** — cada skill/agente declara sus dependencias matemáticas y formales
- **Calidad medible** — score por `logic`, `clarity`, `security`, `utility` en cada componente
- **Gobierno automatizado** — CI bloquea PRs que no pasan benchmarks y regression checks
- **Cobertura de dominio** — desde lógica proposicional hasta IA aplicada en 20+ industrias

---

## Estadísticas del Repositorio

<div align="center">

| Componente | Cantidad | Estado |
|:---:|:---:|:---:|
| Skills especializadas | **203** | ✅ Healthy |
| Agentes de orquestación | **196** | ✅ Healthy |
| Logic foundation skills | **30** | ✅ 100% cubiertos |
| Benchmark pass rate | **100%** | ✅ Passing |
| Versión actual | **v1.0.0** | ✅ Stable |

</div>

---

## Arquitectura del Sistema

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

## Dominios Cubiertos

<div align="center">

| Categoría | Skills Incluidas |
|---|---|
| **Lógica & Matemáticas** | Propositional reasoning, predicate quantifiers, proof strategies, Hoare logic, set theory, discrete structures, complexity analysis |
| **IA Aplicada** | Customer success, agritech, biotech, climate analytics, cybersecurity, ecommerce, education, energy, healthcare, legal, finance, logistics |
| **Ingeniería de Software** | Full-stack, automation, workflow orchestration, security, testing, debugging, frontend frameworks |
| **Tipos de Agentes** | Auditor, Builder, Strategist, Reviewer |

</div>

---

## Inicio Rápido

### 1. Clonar y bootstrap

```bash
git clone https://github.com/jonatangs777/ai-skill-agent-control-deck-2026.git
cd ai-skill-agent-control-deck-2026

# Inicialización completa: logic pack + aliases + semver + quality gate
make bootstrap
```

### 2. Instalar una skill en Claude Code

```bash
# Copiar skill a tu instalación local de Claude Code
cp -r skills/automation-agentic-workflow-automation-skill-2026 ~/.claude/skills/

# Recargar Claude Code para activar la skill
claude
```

### 3. Ver el dashboard de calidad

```bash
make dashboard
open catalog/quality-dashboard.html
```

### 4. Correr el gate completo de calidad

```bash
make quality
```

### 5. Crear un release

```bash
make release-auto
```

---

## Comandos Make Disponibles

```bash
make bootstrap      # Inicialización completa del repositorio
make quality        # Gate completo: compile + semver + benchmarks + catalog + dashboard
make benchmarks     # Ejecutar suite de benchmarks (score por 4 dimensiones)
make dashboard      # Generar dashboard HTML interactivo de calidad
make docs-portal    # Generar portal de documentación HTML
make catalog        # Reconstruir índice de skills/agentes
make release-auto   # Crear patch release automático
make logic-pack     # Instalar las 30 logic foundation skills
```

---

## Estructura del Proyecto

```
ai-skill-agent-control-deck-2026/
│
├── skills/                    # 203 skills especializadas
│   └── [nombre-skill]/
│       ├── SKILL.md           # Definición principal (frontmatter + workflow + guardrails)
│       ├── README.md          # Instalación y uso
│       ├── skill.meta.json    # Metadata y versión
│       ├── examples/          # Prompts de ejemplo
│       └── references/        # Quality gates y criterios
│
├── agents/                    # 196 agentes de orquestación
│   └── [nombre-agente]/
│       ├── AGENT.md           # Perfil de skills + núcleo lógico
│       ├── agent.meta.json    # Metadata
│       └── references/        # Índice de skills del agente
│
├── catalog/                   # Índices de calidad y benchmarks
│   ├── skills.index.json      # Índice de búsqueda de skills
│   ├── agents.index.json      # Índice de búsqueda de agentes
│   ├── benchmark-results.json # Scores actuales (logic/clarity/security/utility)
│   ├── quality-dashboard.html # Dashboard interactivo
│   └── releases/v1.0.0/       # Release notes
│
├── scripts/                   # 13 scripts Python de automatización
├── docs/                      # Documentación y governance
│   ├── patterns.md
│   ├── anti-patterns.md
│   ├── quickstart.md
│   ├── governance/
│   └── claude-code-guide.md   # Guía completa de Claude Code (ES/EN)
│
├── .github/workflows/         # CI/CD
├── Makefile                   # Automatización de build y calidad
└── CONTRIBUTING.md            # Flujo de contribución
```

---

## Sistema de Calidad en 4 Dimensiones

Cada skill y agente recibe un score en:

```
┌────────────┬──────────────────────────────────────────────────────┐
│ Dimensión  │ Descripción                                          │
├────────────┼──────────────────────────────────────────────────────┤
│ logic      │ Solidez formal: correctness, invariants, proofs      │
│ clarity    │ Documentación, ejemplos, instrucciones comprensibles │
│ security   │ Manejo de amenazas, guardrails, boundary validation  │
│ utility    │ Valor práctico, cobertura de casos reales            │
└────────────┴──────────────────────────────────────────────────────┘

Top scores actuales: fullstack-ultramodern-2026 (98.6/100)
```

---

## Documentación

| Recurso | Descripción |
|---|---|
| [Guía de Claude Code](docs/claude-code-guide.md) | Guía completa bilingüe (ES/EN) de Claude Code |
| [Inicio Rápido](docs/quickstart.md) | Setup en 5 minutos |
| [Patrones Recomendados](docs/patterns.md) | 5 patrones probados (Skill, Agent, Quality, Release) |
| [Anti-patrones](docs/anti-patterns.md) | 5 errores comunes y cómo corregirlos |
| [Definition of Done](docs/governance/definition-of-done.md) | Checklist de aceptación para contribuciones |
| [Review Checklist](docs/governance/review-checklist.md) | Checklist de revisión de PRs |
| [Portal de Docs](docs/portal/index.html) | Portal HTML auto-generado |
| [Dashboard de Calidad](catalog/quality-dashboard.html) | Visualización interactiva de scores |

---

## Flujo de Contribución

```bash
# 1. Fork y clonar
git clone https://github.com/[tu-usuario]/ai-skill-agent-control-deck-2026.git

# 2. Crear rama de feature
git checkout -b feat/nueva-skill-dominio

# 3. Crear skill usando el script universal
python scripts/universal_skill_creator.py

# 4. Correr quality gate localmente
make quality

# 5. Abrir Pull Request
# El CI correrá: compile + semver + benchmarks automáticamente
```

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para el flujo completo y estándares de contribución.

---

## Releases

| Versión | Fecha | Canal | Estado |
|---|---|---|---|
| [v1.0.0](catalog/releases/v1.0.0/release-notes.md) | 2026-04-05 | stable | ✅ Healthy |

---

## Licencia

MIT © 2026 Yonatan Guerrero Soriano — ver [LICENSE](LICENSE)

---

<div align="center">

**Construido con rigor lógico, medido con benchmarks, publicado con confianza.**

[Subir al inicio](#ai-skill--agent-control-deck-2026)

</div>
