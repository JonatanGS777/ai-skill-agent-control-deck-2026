# Universal Skill Creator (Claude Code + Codex)

Este documento explica como crear una sola skill reutilizable para:

- Claude Code (`~/.claude/skills`)
- Codex (`~/.codex/skills`)

La idea es tener una fuente canonica de la skill en tu repo y luego instalarla en ambos sistemas con `symlink` o `copy`.

## Archivo principal

- Script: `scripts/universal_skill_creator.py`

## Que crea el script

Cuando ejecutas el creador, genera una carpeta de skill con esta estructura:

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

`SKILL.md` incluye frontmatter y secciones de misión, uso, inputs, workflow, output contract y guardrails.

## Uso rapido

### 1) Crear skill e instalar en Claude y Codex (recomendado)

```bash
python3 scripts/universal_skill_creator.py \
  --name "api reviewer" \
  --description "Revisa APIs para seguridad, errores de contrato y mantenibilidad" \
  --install-target both \
  --install-method symlink
```

### 2) Crear solo en el repo (sin instalar)

```bash
python3 scripts/universal_skill_creator.py \
  --name "api reviewer" \
  --description "Revisa APIs para seguridad, errores de contrato y mantenibilidad" \
  --install-target none
```

### 3) Simular sin escribir nada

```bash
python3 scripts/universal_skill_creator.py \
  --name "api reviewer" \
  --description "Revisa APIs para seguridad, errores de contrato y mantenibilidad" \
  --dry-run
```

## Personalizacion avanzada

Puedes agregar bullets custom para `when`, `input`, `step` y `guardrail`.

```bash
python3 scripts/universal_skill_creator.py \
  --name "security gate" \
  --description "Bloquea cambios inseguros en PRs" \
  --when "When a pull request touches authentication or permissions." \
  --input "Changed files list and diff summary." \
  --step "Identify attack surfaces and trust boundaries." \
  --step "Validate authz, input handling, and secrets exposure." \
  --step "Return prioritized findings with remediation patches." \
  --guardrail "Never recommend disabling security controls in production." \
  --install-target both \
  --install-method symlink
```

## Flags mas importantes

- `--name`: nombre de la skill (obligatorio)
- `--description`: descripcion corta (obligatorio)
- `--domain`: dominio de la skill (ej. frontend, backend, math)
- `--quality-tier`: `core`, `advanced`, `expert`
- `--tag`: tags de catalogacion (repetible)
- `--foundation-skill`: skills fundacionales que esta skill debe respetar (repetible)
- `--skill-root`: carpeta local de skills (default: `skills`)
- `--install-target`: `both`, `claude`, `codex`, `none`
- `--install-method`: `symlink` (recomendado) o `copy`
- `--overwrite`: reemplaza skill existente
- `--dry-run`: muestra acciones sin escribir archivos
- `--strict`: valida payload de forma estricta y falla si no cumple calidad minima

## Estrategia recomendada para equipos

1. Crear skills en el repo (fuente canonica).
2. Instalar en Claude/Codex por `symlink`.
3. Versionar cambios de `SKILL.md` en git.
4. Probar con prompts reales.
5. Refinar workflow y guardrails cada semana.

## Solucion de problemas

- Error de permisos al instalar en `~/.claude/skills` o `~/.codex/skills`:
  usa `--install-target none`, luego instala manualmente con permisos adecuados.
- Ya existe la carpeta de la skill:
  usa `--overwrite` para reemplazar.
- Nombre invalido:
  usa letras/numeros/espacios; el script lo convierte a slug.

## Compatibilidad

La skill generada esta pensada para funcionar en ambos ecosistemas porque ambos consumen `SKILL.md` como entrada principal.

## Auditoria de repositorio

Para regenerar catalogos y reporte de calidad:

```bash
python3 scripts/rebuild_repo_catalog.py --strict
```

Salida:
- `catalog/skills.index.json`
- `catalog/agents.index.json`
- `catalog/repository-quality.md`

## Benchmark suite + evaluator automatico

Este repo incluye benchmark oficial con:
- score por `logic`, `clarity`, `security`, `utility`
- regression checks de prompts
- cobertura de casos reales

Runner:

```bash
python3 scripts/run_benchmarks.py --strict
```

Salida:
- `catalog/benchmark-results.json`
- `catalog/benchmark-history.json`
- `catalog/skill-quality-ranking.json`
- `catalog/agent-quality-ranking.json`

Dashboard visual local:

```bash
python3 scripts/build_quality_dashboard.py
```

Salida:
- `catalog/quality-dashboard.html`

El dashboard incluye:
- leaderboard filtrable por score/dominio/tipo
- KPIs ejecutivos por dominio
- tendencia historica por corrida (timeline de benchmark)

## Releases versionados + changelog automatico

Script:
- `scripts/generate_release_bundle.py`

Genera:
- `catalog/releases/<version>/release-notes.md`
- `catalog/releases/<version>/release.json`
- `catalog/releases/<version>/assets-manifest.json`
- `catalog/releases/releases-index.json`
- `CHANGELOG.md` (actualizado automaticamente)

Comandos:

```bash
make release-auto
make release RELEASE_VERSION=v1.0.0 RELEASE_CHANNEL=stable RELEASE_NOTES="Primer release estable"
```

Workflow dedicado:
- `.github/workflows/release-bundle.yml` (manual `workflow_dispatch`)

## Portal de documentacion + gobernanza

Generador:
- `scripts/build_docs_portal.py`

Salida:
- `docs/portal/index.html`

Documentacion base:
- `docs/quickstart.md`
- `docs/patterns.md`
- `docs/anti-patterns.md`
- `docs/examples-top.md`

Gobernanza:
- `CONTRIBUTING.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/governance/review-checklist.md`
- `docs/governance/definition-of-done.md`

## Versionado semantico automatico (skills + agents)

Script:
- `scripts/semantic_version_manager.py`

Reglas de bump:
- `major`: cambia identidad (nombre/compatibilidad/entrypoint/tipo de agente).
- `minor`: cambia contrato (secciones clave y bases logicas).
- `patch`: cambian metadatos o contenido general sin romper contrato.

Comandos directos:

```bash
python3 scripts/semantic_version_manager.py --mode initialize --scope both
python3 scripts/semantic_version_manager.py --mode apply --scope both
python3 scripts/semantic_version_manager.py --mode check --scope both --strict
```

Estado:
- `catalog/version-state.json`

Flujo recomendado:
1. Al iniciar repositorio o migrar: `initialize`.
2. Despues de cambios en skills/agentes: `apply`.
3. Antes de push/PR: `check --strict`.
4. Ejecutar `make quality`.

## Comandos Make (operacion rapida)

```bash
make semver-init
make semver-apply
make semver-check
make benchmarks
make dashboard
make docs-portal
make release-auto
make quality
make logic-pack
make bootstrap
```

- `make semver-init`: crea baseline en `catalog/version-state.json`.
- `make semver-apply`: aplica bumps y actualiza baseline.
- `make semver-check`: falla si hay bumps pendientes o artefactos sin baseline.
- `make benchmarks`: ejecuta benchmark suite con gate estricto.
- `make dashboard`: construye dashboard HTML interactivo de calidad.
- `make docs-portal`: construye portal de documentacion con datos del catalogo.
- `make release-auto`: corre quality y crea release bundle con siguiente patch.
- `make quality`: compile-check + semver + benchmarks + catalogo + dashboard + docs portal.
- `make logic-pack`: reconstruye e instala las 30 skills logicas.
- `make bootstrap`: logic-pack + aliases de agentes + semver-apply + quality.

## Generacion masiva (pack excepcional 2026)

Para crear 100 skills (matematicas/programacion/robotica) y 70 agentes excepcionales:

```bash
python3 scripts/generate_exceptional_pack_2026.py
```

Opciones:
- `--dry-run`: previsualiza sin escribir.
- `--overwrite`: regenera reemplazando.
- `--skip-quality`: omite `semver apply` y `make quality`.

## Generacion masiva (AI Factory 2026)

Para construir flujo completo de **proceso -> skills -> agentes**:
- 70 skills IA (automatizacion/chatbots/domain AI)
- 100 agentes IA especializados

```bash
python3 scripts/generate_ai_factory_pack_2026.py
```

Salida adicional:
- `catalog/ai-factory-pack-2026.json` (manifiesto del lote generado).
