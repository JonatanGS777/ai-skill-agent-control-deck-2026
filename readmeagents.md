# Universal Agent Creator (Claude Code + Codex)

Este generador crea agentes universales compatibles con Claude Code y Codex,
y los configura para trabajar con skills desde su protocolo interno.

## Archivo principal

- `scripts/universal_agent_creator.py`

## Que crea

Por cada agente genera:

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

Ademas instala un entrypoint en:

- `~/.claude/agents/<agent-name>.md`
- `~/.codex/agents/<agent-name>.md`

## Skill Bootstrap Protocol

Cada agente generado incluye un bloque interno para:

1. Detectar capacidades requeridas por la tarea.
2. Seleccionar skills relevantes (manuales y/o auto).
3. Fusionar reglas y guardrails de esas skills.
4. Ejecutar con plan unificado y validacion final.

## Modo de skills

- `--skill-mode explicit`: solo usa `--skill` manuales.
- `--skill-mode auto`: detecta skills automaticamente desde las fuentes.
- `--skill-mode hybrid` (default): combina manual + auto.
- `--logic-foundation`: agrega base logica (`none`, `core`, `standard`, `max`) para robustez de razonamiento.

Fuentes default de skills:

- `skills`
- `~/.claude/skills`
- `~/.codex/skills`

## Uso rapido

### 1) Crear un agente orquestador con skills auto + manual

```bash
python3 scripts/universal_agent_creator.py \
  --name "product orchestrator 2026" \
  --description "Orquesta implementaciones full stack con foco en calidad de produccion." \
  --agent-type orchestrator \
  --skill fullstack-ultramodern-2026 \
  --skill frontend-ultramodern-2026 \
  --skill-mode hybrid \
  --install-target both \
  --install-method symlink
```

### 2) Crear un agente sin instalar (solo repo)

```bash
python3 scripts/universal_agent_creator.py \
  --name "api quality reviewer" \
  --description "Revisor tecnico de APIs orientado a riesgo y mantenibilidad." \
  --agent-type reviewer \
  --install-target none
```

### 3) Simular sin escribir archivos

```bash
python3 scripts/universal_agent_creator.py \
  --name "debug commander" \
  --description "Diagnostico de incidentes complejos en produccion." \
  --agent-type debugger \
  --dry-run
```

## Flags clave

- `--name`, `--description`: obligatorios.
- `--agent-type`: `orchestrator`, `builder`, `reviewer`, `debugger`, `specialist`.
- `--skill`: skill manual (repetible).
- `--skill-mode`: `explicit`, `auto`, `hybrid`.
- `--logic-foundation`: `none`, `core`, `standard`, `max`.
- `--max-profile-skills`: limita skills finales del perfil para evitar sobrecarga.
- `--skill-source`: fuentes de skills (repetible).
- `--max-auto-skills`: limite de autoseleccion.
- `--strict`: falla si skills explicitas no existen en fuentes detectadas.
- `--install-target`: `both`, `claude`, `codex`, `none`.
- `--install-method`: `symlink` (recomendado) o `copy`.
- `--overwrite`, `--dry-run`.

## Recomendacion de equipo

1. Crear agentes en `agents/` como fuente canonica.
2. Instalar por `symlink` para que cambios locales impacten ambos ecosistemas.
3. Versionar `AGENT.md` + `references/skill-index.md`.
4. Revisar periodicamente skills seleccionadas por el modo `auto`.

## Alias de grupo para activacion

Para activar agentes con nombre de grupo (ej. `ceo-jonatan-agent--...`):

```bash
python3 scripts/install_agent_group_aliases.py \
  --agent-root agents \
  --group-name "CEO Jonatan Agent" \
  --install-target both \
  --overwrite
```

Con Makefile:

```bash
make aliases GROUP_NAME="CEO Jonatan Agent"
```

Para mantener los agentes creados en lote en un grupo aparte:

```bash
make aliases-created
```

Esto instala aliases con prefijo:
- `ceo-jonatan-creados--<agent>.md`

Para mantener separados los 100 agentes del AI Factory:

```bash
make aliases-ai
```

Esto instala aliases con prefijo:
- `ceo-jonatan-ai-factory--<agent>.md`

## CI Quality Gate

Se incluye workflow de GitHub Actions en:

- `.github/workflows/repository-quality.yml`
- `.github/workflows/release-bundle.yml`

Este workflow ejecuta:
1. `py_compile` de scripts principales.
2. `python scripts/semantic_version_manager.py --mode check --scope both --strict`.
3. `python scripts/run_benchmarks.py --strict`.
4. `python scripts/rebuild_repo_catalog.py --strict`.
5. `python scripts/build_quality_dashboard.py`.
6. Publica `catalog/*` como artifact del workflow.

Incluye dashboard visual:
- `catalog/quality-dashboard.html`
- `docs/portal/index.html`

Y gobernanza de contribuciones:
- `CONTRIBUTING.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/governance/review-checklist.md`
- `docs/governance/definition-of-done.md`

## Versionado semantico de agentes

Para mantener versionado consistente en `AGENT.md` + `agent.meta.json`:

```bash
python3 scripts/semantic_version_manager.py --mode apply --scope agents
python3 scripts/semantic_version_manager.py --mode check --scope agents --strict
```

Tambien puedes usar:

```bash
make semver-apply
make semver-check
make benchmarks
make docs-portal
make release-auto
```
