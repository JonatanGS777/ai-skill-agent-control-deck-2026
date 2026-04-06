# Claude Code — Guía Completa / Complete Guide

> **Versión / Version:** Claude Code (claude-sonnet-4-6 / claude-opus-4-6 / claude-haiku-4-5)  
> **Fecha / Date:** 2026-04-04

---

## ÍNDICE / TABLE OF CONTENTS

1. [¿Qué es Claude Code? / What is Claude Code?](#1-qué-es-claude-code--what-is-claude-code)
2. [Instalación y Plataformas / Installation & Platforms](#2-instalación-y-plataformas--installation--platforms)
3. [Interfaz y Controles / Interface & Controls](#3-interfaz-y-controles--interface--controls)
4. [Herramientas Principales / Core Tools](#4-herramientas-principales--core-tools)
5. [Sistema de Memoria / Memory System](#5-sistema-de-memoria--memory-system)
6. [Archivo CLAUDE.md — Configuración del Proyecto](#6-archivo-claudemd--project-configuration)
7. [MCP (Model Context Protocol)](#7-mcp-model-context-protocol)
8. [Hooks — Automatización de Eventos](#8-hooks--event-automation)
9. [Comandos Slash / Slash Commands](#9-comandos-slash--slash-commands)
10. [Sistema de Skills / Skills System](#10-sistema-de-skills--skills-system)
11. [Atajos de Teclado / Keyboard Shortcuts](#11-atajos-de-teclado--keyboard-shortcuts)
12. [Integración con IDEs / IDE Integration](#12-integración-con-ides--ide-integration)
13. [Subagentes / Sub-Agents](#13-subagentes--sub-agents)
14. [Selección de Modelos / Model Selection](#14-selección-de-modelos--model-selection)
15. [Estrategias Avanzadas / Advanced Strategies](#15-estrategias-avanzadas--advanced-strategies)
16. [Seguridad y Permisos / Security & Permissions](#16-seguridad-y-permisos--security--permissions)
17. [Flujo de Trabajo Completo / Complete Workflow](#17-flujo-de-trabajo-completo--complete-workflow)
18. [Referencia Rápida / Quick Reference](#18-referencia-rápida--quick-reference)

---

## 1. ¿Qué es Claude Code? / What is Claude Code?

**ES:** Claude Code es el CLI oficial de Anthropic para Claude, diseñado como un agente de ingeniería de software interactivo y autónomo. Opera directamente en tu terminal con acceso completo a tu sistema de archivos, repositorios git, entornos de ejecución y herramientas externas. Va más allá de un simple chat: actúa, ejecuta código, modifica archivos, y orquesta agentes especializados.

**EN:** Claude Code is Anthropic's official CLI for Claude, designed as an interactive and autonomous software engineering agent. It operates directly in your terminal with full access to your file system, git repositories, execution environments, and external tools. It goes beyond simple chat: it acts, executes code, modifies files, and orchestrates specialized agents.

### Capacidades Fundamentales / Core Capabilities

| Capacidad / Capability | Descripción ES | Description EN |
|---|---|---|
| **Lectura de archivos** | Lee cualquier archivo del sistema | Reads any file in the system |
| **Escritura/Edición** | Crea y modifica archivos con precisión | Creates and modifies files precisely |
| **Ejecución de código** | Corre comandos bash, scripts, tests | Runs bash commands, scripts, tests |
| **Búsqueda avanzada** | Busca por patrón glob o regex en todo el repo | Searches by glob pattern or regex across repo |
| **Git completo** | Commits, PRs, branches, blame, log | Commits, PRs, branches, blame, log |
| **Orquestación de agentes** | Lanza subagentes especializados en paralelo | Launches specialized subagents in parallel |
| **Memoria persistente** | Recuerda preferencias entre sesiones | Remembers preferences across sessions |
| **MCP / Herramientas externas** | Se conecta a Canva, Gmail, APIs, DBs | Connects to Canva, Gmail, APIs, DBs |

---

## 2. Instalación y Plataformas / Installation & Platforms

### Plataformas Disponibles / Available Platforms

```
┌─────────────────────────────────────────────────────────┐
│               CLAUDE CODE PLATFORMS                      │
├──────────────────┬──────────────────┬───────────────────┤
│   CLI Terminal   │  Desktop App     │   Web App         │
│   Mac/Linux/Win  │  Mac / Windows   │  claude.ai/code   │
├──────────────────┴──────────────────┴───────────────────┤
│         IDE Extensions                                   │
│   VS Code  │  JetBrains  │  (más en desarrollo)         │
└─────────────────────────────────────────────────────────┘
```

### Instalación CLI / CLI Installation

```bash
# Instalar via npm / Install via npm
npm install -g @anthropic-ai/claude-code

# Verificar instalación / Verify installation
claude --version

# Iniciar / Start
claude
```

### Modos de Ejecución / Execution Modes

```bash
claude                    # Modo interactivo / Interactive mode
claude "tarea aquí"       # Modo una sola vez / One-shot mode
claude -p "prompt"        # Modo programático / Programmatic mode
claude --print            # Sin interacción / Non-interactive
claude -c                 # Continuar sesión anterior / Continue last session
claude --resume [id]      # Reanudar sesión específica / Resume specific session
```

---

## 3. Interfaz y Controles / Interface & Controls

### Modos de la Interfaz / Interface Modes

**ES:** Claude Code tiene tres modos principales de operación que determinan qué acciones puede tomar automáticamente:

**EN:** Claude Code has three main operating modes that determine what actions it can take automatically:

| Modo / Mode | Comportamiento ES | Behavior EN |
|---|---|---|
| **Default** | Pide confirmación para acciones de riesgo | Asks confirmation for risky actions |
| **Auto-approve** | Aprueba automáticamente herramientas seguras | Auto-approves safe tools |
| **Full autonomy** | Ejecuta todo sin confirmaciones | Executes everything without confirmations |

### Comandos de Control / Control Commands

```
/help          → Ayuda general / General help
/clear         → Limpiar conversación / Clear conversation  
/compact       → Compactar contexto / Compact context
/cost          → Ver uso de tokens / View token usage
/status        → Estado del sistema / System status
/doctor        → Diagnóstico de instalación / Installation diagnosis
/logout        → Cerrar sesión / Logout
/login         → Iniciar sesión / Login
```

### Modos Especiales / Special Modes

```
/fast          → Activar modo rápido (mismo modelo, output más rápido)
                 Enable fast mode (same model, faster output)
               
Plan Mode      → Planificar antes de ejecutar (ExitPlanMode)
                 Plan before executing

Extended Thinking → Opción+T (macOS) / Alt+T (Windows/Linux)
                    Hasta 31,999 tokens de razonamiento interno
                    Up to 31,999 tokens of internal reasoning
```

---

## 4. Herramientas Principales / Core Tools

**ES:** Claude Code dispone de herramientas especializadas optimizadas para tareas de ingeniería. Siempre usa la herramienta específica en lugar de comandos bash equivalentes.

**EN:** Claude Code has specialized tools optimized for engineering tasks. Always use the specific tool instead of equivalent bash commands.

### Herramientas de Archivos / File Tools

| Herramienta | Uso ES | Use EN | Equivalente evitado |
|---|---|---|---|
| `Read` | Leer archivos con números de línea | Read files with line numbers | `cat`, `head`, `tail` |
| `Write` | Crear/sobreescribir archivos | Create/overwrite files | `echo >`, `cat <<EOF` |
| `Edit` | Reemplazos exactos de strings | Exact string replacements | `sed`, `awk` |
| `Glob` | Buscar archivos por patrón | Find files by pattern | `find`, `ls` |
| `Grep` | Buscar contenido con regex | Search content with regex | `grep`, `rg` |

### Herramientas de Ejecución / Execution Tools

| Herramienta | Descripción ES | Description EN |
|---|---|---|
| `Bash` | Comandos shell, git, npm, etc. | Shell commands, git, npm, etc. |
| `Bash (background)` | Procesos en segundo plano | Background processes |
| `NotebookEdit` | Editar Jupyter notebooks | Edit Jupyter notebooks |

### Herramientas de Agentes / Agent Tools

| Herramienta | Descripción ES | Description EN |
|---|---|---|
| `Agent` | Lanzar subagente especializado | Launch specialized subagent |
| `TodoWrite` | Gestionar lista de tareas | Manage task list |
| `WebSearch` | Buscar en la web | Search the web |
| `WebFetch` | Obtener contenido de URL | Fetch URL content |

### Herramientas de Contexto / Context Tools

| Herramienta | Descripción ES | Description EN |
|---|---|---|
| `Skill` | Invocar skill por nombre | Invoke skill by name |
| `ToolSearch` | Buscar herramientas diferidas | Search deferred tools |
| `ReadMcpResource` | Leer recursos MCP | Read MCP resources |
| `ListMcpResources` | Listar recursos MCP | List MCP resources |

---

## 5. Sistema de Memoria / Memory System

**ES:** El sistema de memoria persiste información entre conversaciones usando archivos Markdown en un directorio dedicado. Tiene cuatro tipos de memorias especializadas.

**EN:** The memory system persists information between conversations using Markdown files in a dedicated directory. It has four specialized memory types.

### Tipos de Memoria / Memory Types

```
~/.claude/projects/[project-name]/memory/
├── MEMORY.md              ← Índice / Index (siempre cargado / always loaded)
├── user_*.md              ← Sobre el usuario / About the user
├── feedback_*.md          ← Correcciones y confirmaciones / Corrections & confirmations
├── project_*.md           ← Estado del proyecto / Project state
└── reference_*.md         ← Referencias externas / External references
```

#### Memoria de Usuario / User Memory
```markdown
---
name: user-profile
description: Perfil del usuario — experiencia, stack, preferencias
type: user
---
Usuario es ingeniero senior de Kotlin/Android con 8 años de experiencia.
Trabaja con Spring Boot en backend. Nuevo en SwiftUI.
```

#### Memoria de Feedback / Feedback Memory
```markdown
---
name: feedback-terse-responses
description: No añadir resúmenes al final de cada respuesta
type: feedback
---
No resumir lo que se acaba de hacer al final de respuestas.
**Why:** El usuario puede leer el diff directamente.
**How to apply:** Terminar respuestas de manera directa, sin "En resumen..."
```

#### Memoria de Proyecto / Project Memory
```markdown
---
name: project-auth-rewrite
description: Reescritura del módulo auth — razón legal/compliance
type: project
---
El middleware de auth se está reescribiendo por requerimiento legal.
**Why:** Legal flagueó almacenamiento inseguro de session tokens.
**How to apply:** Priorizar compliance sobre ergonomía en decisiones de scope.
```

#### Memoria de Referencia / Reference Memory
```markdown
---
name: reference-linear-bugs
description: Bugs de pipeline trackeados en Linear proyecto INGEST
type: reference
---
Pipeline bugs → Linear proyecto "INGEST"
Dashboard de latencia → grafana.internal/d/api-latency
```

### Cuándo Guarda Memorias / When Claude Saves Memories

- Usuario corrige comportamiento → `feedback_*.md`
- Usuario confirma un enfoque no obvio → `feedback_*.md`
- Se aprenden detalles del rol/preferencias → `user_*.md`
- Se conocen fechas límite o decisiones del proyecto → `project_*.md`
- Se descubren sistemas externos relevantes → `reference_*.md`

---

## 6. Archivo CLAUDE.md — Project Configuration

**ES:** El archivo `CLAUDE.md` en la raíz del proyecto es la configuración maestra que guía a Claude en cada sesión. Es leído automáticamente al inicio de cada conversación.

**EN:** The `CLAUDE.md` file at the project root is the master configuration that guides Claude in every session. It is automatically read at the start of each conversation.

### Ubicaciones / Locations

```
~/.claude/CLAUDE.md          ← Global (todas las sesiones / all sessions)
~/proyecto/CLAUDE.md         ← Proyecto raíz / Project root
~/proyecto/src/CLAUDE.md     ← Subdirectorio específico / Specific subdirectory
```

### Plantilla Completa / Complete Template

```markdown
# Project: [Nombre del Proyecto]

## Commands
- Run: `npm run dev`
- Test: `npm test -- --watch`
- Build: `npm run build`
- Lint: `npm run lint`
- Type check: `npx tsc --noEmit`

## Architecture
- Framework: Next.js 14 App Router
- State: Zustand + React Query
- DB: PostgreSQL via Prisma
- Auth: NextAuth.js

## Code Style
- TypeScript strict mode — siempre
- Functional components + hooks
- Early returns para manejo de errores
- No any — usar tipos explícitos
- Nombrar con camelCase (variables), PascalCase (componentes)

## Workflow
1. Leer README.md primero para contexto
2. Antes de editar, leer el archivo actual
3. Después de editar, correr tests
4. Commits en conventional format: feat/fix/refactor/docs

## Important Notes
- No mockear la base de datos en tests (incidente Q4 2025)
- Siempre usar Prisma transactions para operaciones multi-tabla
- API routes en /app/api/, no en /pages/api/
```

### Jerarquía de CLAUDE.md / CLAUDE.md Hierarchy

```
Global ~/.claude/CLAUDE.md
    ↓ (se combina / combined with)
Proyecto ~/repo/CLAUDE.md
    ↓ (se combina / combined with)
Subdirectorio ~/repo/src/CLAUDE.md
```

---

## 7. MCP (Model Context Protocol)

**ES:** MCP es el protocolo estándar que permite a Claude Code conectarse con servicios externos, bases de datos, APIs y herramientas personalizadas. Convierte herramientas externas en capacidades nativas de Claude.

**EN:** MCP is the standard protocol that allows Claude Code to connect with external services, databases, APIs, and custom tools. It turns external tools into native Claude capabilities.

### Configuración MCP / MCP Configuration

```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "canva": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-canva"],
      "env": { "CANVA_API_KEY": "tu-api-key" }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "ghp_..." }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "postgresql://..." }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/ruta/permitida"]
    }
  }
}
```

### Servidores MCP Populares / Popular MCP Servers

| Servidor / Server | Capacidad ES | Capability EN |
|---|---|---|
| `@anthropic-ai/mcp-server-canva` | Diseño y edición en Canva | Design and editing in Canva |
| `mcp-server-github` | Issues, PRs, repos de GitHub | GitHub issues, PRs, repos |
| `mcp-server-postgres` | Consultas SQL directas | Direct SQL queries |
| `mcp-server-filesystem` | Acceso controlado a archivos | Controlled file access |
| `mcp-server-brave-search` | Búsqueda web con Brave | Web search with Brave |
| `mcp-server-slack` | Leer/escribir en Slack | Read/write in Slack |
| `context7` | Documentación de librerías | Library documentation |
| `mcp-server-gmail` | Gestión de email | Email management |
| `mcp-server-google-calendar` | Eventos del calendario | Calendar events |

### Diagrama de Flujo MCP / MCP Flow Diagram

```
Claude Code CLI
      │
      ├── Tool: mcp__canva__create-design
      ├── Tool: mcp__github__create-issue  
      ├── Tool: mcp__postgres__query
      └── Tool: mcp__context7__query-docs
            │
            ↓
      MCP Protocol (JSON-RPC)
            │
            ↓
   ┌────────────────────┐
   │   MCP Server       │
   │  (proceso local    │
   │   o remoto)        │
   └────────────────────┘
            │
            ↓
   API Externa / Base de Datos / Herramienta
```

---

## 8. Hooks — Event Automation

**ES:** Los hooks son comandos shell que se ejecutan automáticamente en respuesta a eventos del ciclo de vida de Claude Code. Permiten automatizar comportamientos sin intervención manual.

**EN:** Hooks are shell commands that execute automatically in response to Claude Code lifecycle events. They enable automating behaviors without manual intervention.

### Tipos de Hooks / Hook Types

| Hook | Cuándo se ejecuta ES | When it fires EN |
|---|---|---|
| `PreToolUse` | Antes de que Claude use una herramienta | Before Claude uses a tool |
| `PostToolUse` | Después de que Claude usa una herramienta | After Claude uses a tool |
| `Notification` | Cuando hay notificaciones del sistema | When there are system notifications |
| `Stop` | Cuando Claude termina su respuesta | When Claude finishes responding |
| `SubagentStop` | Cuando un subagente termina | When a subagent finishes |

### Configuración de Hooks / Hook Configuration

```json
// ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "echo 'Ejecutando bash: $CLAUDE_TOOL_INPUT' >> ~/claude_log.txt"
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [{
          "type": "command",
          "command": "npx prettier --write $CLAUDE_FILE_PATH"
        }]
      }
    ],
    "Stop": [
      {
        "hooks": [{
          "type": "command",
          "command": "osascript -e 'display notification \"Claude terminó\" with title \"Claude Code\"'"
        }]
      }
    ]
  }
}
```

### Casos de Uso de Hooks / Hook Use Cases

```
✅ Auto-formatear código después de escribir un archivo
   Auto-format code after writing a file

✅ Notificación de escritorio cuando Claude termina
   Desktop notification when Claude finishes

✅ Logging de todos los comandos ejecutados
   Logging of all executed commands

✅ Bloquear comandos peligrosos (rm -rf, etc.)
   Block dangerous commands (rm -rf, etc.)

✅ Ejecutar linters automáticamente
   Run linters automatically

✅ Guardar historial de sesiones
   Save session history

✅ Sincronizar archivos a repositorio remoto
   Sync files to remote repository
```

---

## 9. Comandos Slash / Slash Commands

**ES:** Los comandos slash son atajos predefinidos que invocan skills o flujos de trabajo complejos con una sola instrucción.

**EN:** Slash commands are predefined shortcuts that invoke skills or complex workflows with a single instruction.

### Comandos del Sistema / System Commands

```bash
/help                    # Ayuda de Claude Code / Claude Code help
/clear                   # Limpiar historial de conversación / Clear conversation history
/compact                 # Comprimir contexto para ahorrar tokens / Compress context to save tokens
/cost                    # Ver uso de tokens y costos / View token usage and costs
/status                  # Estado de la sesión / Session status
/doctor                  # Diagnóstico del sistema / System diagnostics
/fast                    # Alternar modo rápido / Toggle fast mode
/logout / /login         # Gestión de sesión / Session management
```

### Comandos de Skills / Skill Commands

```bash
# Desarrollo / Development
/commit                  # Crear commit con formato convencional
/plan                    # Crear plan de implementación
/tdd                     # Iniciar flujo TDD
/code-review             # Revisar código modificado
/security-review         # Análisis de seguridad
/build-fix               # Resolver errores de build

# Documentación / Documentation
/docs                    # Actualizar documentación
/update-docs             # Actualizar docs del proyecto
/update-codemaps         # Actualizar mapas de código

# Testing / Testing
/test-coverage           # Analizar cobertura de tests
/e2e                     # Correr tests E2E
/verify                  # Verificar implementación

# Sesiones / Sessions
/save-session            # Guardar estado de sesión
/resume-session          # Reanudar sesión guardada
/sessions                # Listar sesiones disponibles

# Agentes / Agents
/orchestrate             # Orquestar múltiples agentes
/multi-plan              # Planificación multi-agente
/devfleet                # Desplegar flota de agentes

# Contenido / Content
/article-writing         # Escribir artículo estructurado
/docx                    # Crear documento Word
/beamer-academic-presentation  # Presentación académica LaTeX
```

### Crear Skill Personalizado / Create Custom Skill

```bash
/skill-create            # Asistente para crear nueva skill

# Estructura de un skill / Skill structure:
~/.claude/skills/mi-skill/
├── SKILL.md              # Documentación y lógica
└── assets/               # Recursos opcionales
```

---

## 10. Sistema de Skills / Skills System

**ES:** Las skills son capacidades especializadas que extienden lo que Claude Code puede hacer. Se organizan en skills activas (cargadas en cada conversación) y archivadas (no consumen contexto).

**EN:** Skills are specialized capabilities that extend what Claude Code can do. They are organized into active skills (loaded in every conversation) and archived (don't consume context).

### Estructura / Structure

```
~/.claude/skills/         ← Skills activas (~105 max recomendado)
~/claude_skills_archive/  ← Skills archivadas (no consumen contexto)
```

### Comandos de Gestión / Management Commands

```bash
# Listar skills activas / List active skills
ls ~/.claude/skills/

# Listar skills archivadas / List archived skills
ls ~/claude_skills_archive/

# Buscar skill específica / Find specific skill
ls ~/claude_skills_archive/ | grep "KEYWORD"

# Activar skill archivada / Activate archived skill
mv ~/claude_skills_archive/SKILL_NAME ~/.claude/skills/

# Archivar skill activa / Archive active skill
mv ~/.claude/skills/SKILL_NAME ~/claude_skills_archive/

# Ver catálogo completo / View full catalog
cat ~/claude_skills_archive/CATALOGO_SKILLS.md
```

### Categorías de Skills / Skill Categories

```
AI/Agents:       agent-eval, agentic-engineering, claude-api, team-builder
Backend:         backend-patterns, api-design, postgres-patterns, springboot-patterns
Frontend:        frontend-patterns, react-expert, nextjs-turbopack, vue, nuxt4
Mobile:          android-clean-architecture, swiftui-patterns, kotlin-patterns
Testing:         tdd, verification-loop, python-testing, e2e, test-coverage
Documentation:   docx, article-writing, beamer-academic-presentation, docs
Security:        security-review, security-scan, django-security, laravel-security
DevOps:          docker-patterns, deployment-patterns, devfleet
```

### Construcción de Skills / Building Skills

**ES:** Una skill debe ser específica, reutilizable y activarse solo cuando agrega valor real. Evita skills gigantes que mezclen muchos dominios.

**EN:** A skill should be specific, reusable, and trigger only when it adds clear value. Avoid giant skills that mix many domains.

#### Estructura Recomendada / Recommended Structure

```
~/.claude/skills/mi-skill/
├── SKILL.md                 ← Reglas y flujo principal / Main rules and flow
├── scripts/                 ← Automatizaciones opcionales / Optional automation
└── assets/                  ← Plantillas o recursos / Templates or resources
```

#### Plantilla Base de SKILL.md / SKILL.md Starter Template

```markdown
---
name: "mi-skill"
description: "Qué resuelve y cuándo usarla"
---

# When to use
- Caso 1
- Caso 2

# Inputs expected
- Qué información necesita del usuario

# Workflow
1. Paso de descubrimiento
2. Paso de implementación
3. Paso de verificación

# Output format
- Cómo debe responder (breve, checklist, patch, etc.)
```

#### Ciclo de Vida y Gestión / Lifecycle and Management

| Etapa / Stage | Acción ES | Action EN |
|---|---|---|
| **Diseño** | Definir problema, input mínimo y resultado esperado | Define problem, minimum input, and expected output |
| **Implementación** | Crear `SKILL.md` + scripts solo si reducen trabajo manual | Create `SKILL.md` + scripts only if they reduce manual work |
| **Validación** | Probar con 3-5 prompts reales del equipo | Test with 3-5 real team prompts |
| **Evolución** | Ajustar reglas según feedback recurrente | Adjust rules based on recurring feedback |
| **Archivo** | Mover skills poco usadas a `~/claude_skills_archive/` | Move low-usage skills to `~/claude_skills_archive/` |

#### Buenas Prácticas de Operación / Skill Operational Best Practices

```
✅ Una skill = un problema bien delimitado
✅ Incluir ejemplos de input/output esperados
✅ Documentar límites explícitos (qué NO hace)
✅ Evitar dependencias externas innecesarias
✅ Versionar cambios en un CHANGELOG breve (opcional)
```

---

## 11. Atajos de Teclado / Keyboard Shortcuts

### Atajos Universales / Universal Shortcuts

| Atajo / Shortcut | Acción ES | Action EN |
|---|---|---|
| `Enter` | Enviar mensaje / Send message | |
| `Shift+Enter` | Nueva línea / New line | |
| `↑` / `↓` | Navegar historial / Navigate history | |
| `Ctrl+C` | Interrumpir Claude / Interrupt Claude | |
| `Ctrl+D` | Salir / Exit | |
| `Ctrl+L` | Limpiar pantalla / Clear screen | |

### Atajos Especiales / Special Shortcuts

| Atajo / Shortcut | Acción ES | Action EN |
|---|---|---|
| `Option+T` (macOS) / `Alt+T` | Alternar Extended Thinking | Toggle Extended Thinking |
| `Ctrl+O` | Modo verbose (ver thinking) / Verbose mode (see thinking) | |
| `Ctrl+R` | Buscar en historial / Search history | |

### Modos de Entrada / Input Modes

```bash
# Modo multilínea / Multi-line mode
claude
> [pegar código aquí]   # Ctrl+D para terminar / Ctrl+D to finish

# Pipe desde stdin / Pipe from stdin
echo "Explica este código" | claude -p -
cat archivo.py | claude -p "Revisa esto:"

# Archivos como contexto / Files as context
claude -p "Optimiza:" < main.py
```

---

## 12. Integración con IDEs / IDE Integration

### Visual Studio Code

**ES:** La extensión oficial de Claude Code para VS Code integra el agente directamente en el editor.

**EN:** The official Claude Code extension for VS Code integrates the agent directly into the editor.

#### Instalación / Installation
```
1. Abrir VS Code / Open VS Code
2. Extensions (Ctrl+Shift+X)
3. Buscar / Search: "Claude Code" by Anthropic
4. Instalar / Install
5. Autenticar con cuenta Anthropic / Authenticate with Anthropic account
```

#### Características de la Integración VS Code / VS Code Integration Features

```
┌─────────────────────────────────────────────────────────┐
│                   VS CODE + CLAUDE CODE                  │
├──────────────────────────────────────────────────────────┤
│ • Panel integrado en sidebar / Integrated sidebar panel  │
│ • Links clickeables a archivos/líneas / Clickable links  │
│ • Selección de código como contexto / Code as context    │
│ • Diff visual de cambios / Visual diff of changes        │
│ • Terminal integrado / Integrated terminal               │
│ • Acceso a problemas/errores del editor / Editor errors  │
│ • Git integrado / Integrated git                         │
│ • Múltiples tabs de Claude / Multiple Claude tabs        │
└──────────────────────────────────────────────────────────┘
```

#### Uso con Selección de Código / Usage with Code Selection

```
1. Seleccionar código en el editor / Select code in editor
2. Abrir panel de Claude / Open Claude panel
3. El código seleccionado aparece como contexto / Selected code appears as context
4. Hacer pregunta específica / Ask specific question

Ejemplo / Example:
[Seleccionar función buggy] → "¿Qué está causando este null pointer exception?"
[Select buggy function] → "What's causing this null pointer exception?"
```

### JetBrains (IntelliJ IDEA, Android Studio, PyCharm, etc.)

#### Instalación / Installation
```
1. File → Settings → Plugins
2. Marketplace → Buscar "Claude Code" / Search "Claude Code"
3. Instalar y reiniciar / Install and restart
4. Tools → Claude Code → Connect
```

#### Características Específicas JetBrains / JetBrains-Specific Features

```
• Integración con sistema de build (Maven/Gradle)
  Integration with build system (Maven/Gradle)

• Acceso al árbol de proyecto / Access to project tree
• Indexación de código para contexto / Code indexing for context  
• Refactoring colaborativo / Collaborative refactoring
• Soporte para múltiples lenguajes del IDE / Multi-language IDE support
```

### Configuración del Entorno para IDEs / IDE Environment Setup

```bash
# .vscode/settings.json — Configuración de workspace Claude
{
  "claude-code.defaultModel": "claude-sonnet-4-6",
  "claude-code.autoApproveReadonlyTools": true,
  "claude-code.statusBarEnabled": true
}

# Variables de entorno útiles / Useful environment variables
export ANTHROPIC_API_KEY="sk-ant-..."
export CLAUDE_CODE_MAX_TOKENS=8096
export MAX_THINKING_TOKENS=10000
```

### Comparativa IDE vs Terminal / IDE vs Terminal Comparison

| Aspecto | IDE Extension | Terminal CLI |
|---|---|---|
| **Contexto visual** | Selección de código directa | Rutas de archivo manuales |
| **Diff** | Visual side-by-side | Texto en terminal |
| **Navegación** | Links clickeables | Abrir manualmente |
| **Múltiples archivos** | Workspace integrado | Comandos glob/grep |
| **Velocidad setup** | Inmediata | Requiere configuración |
| **Automatización** | Limitada | Total (hooks, scripts) |
| **Flujos complejos** | Bueno para archivos individuales | Mejor para proyectos completos |

---

## 13. Subagentes / Sub-Agents

**ES:** Claude Code puede lanzar agentes especializados como subprocesos. Cada agente tiene herramientas específicas y conocimiento de dominio profundo.

**EN:** Claude Code can launch specialized agents as subprocesses. Each agent has specific tools and deep domain knowledge.

### Agentes Disponibles / Available Agents

```
PLANIFICACIÓN / PLANNING
├── planner          — Planes de implementación con fases
├── architect        — Diseño de sistemas y arquitectura
└── plan             — Planificación rápida

DESARROLLO / DEVELOPMENT
├── general-purpose  — Tareas complejas multi-paso
├── fullstack-developer — Features completas DB+API+UI
├── backend-developer — APIs, microservicios, backend
├── frontend-developer — React, Vue, Angular
└── nextjs-developer  — Next.js 14+ App Router

REVISIÓN / REVIEW
├── code-reviewer    — Calidad, seguridad, mantenibilidad
├── security-reviewer — Análisis de seguridad OWASP
├── typescript-reviewer — TypeScript/JavaScript
├── python-reviewer  — PEP8, type hints, seguridad
├── java-reviewer    — Spring Boot, JPA, arquitectura
├── rust-reviewer    — Ownership, lifetimes, unsafe
└── go-reviewer      — Idiomatic Go, concurrencia

TESTING / TESTING
├── tdd-guide        — Test-Driven Development
├── test-automator   — Frameworks de testing, CI/CD
└── e2e-runner       — Tests end-to-end

LENGUAJES / LANGUAGES
├── python-pro       — Python moderno, async, tipos
├── typescript-pro   — TypeScript avanzado
├── golang-pro       — Go concurrente, cloud-native
├── rust-engineer    — Sistemas, memoria, zero-cost
├── java-architect   — Enterprise Java, Spring
├── kotlin-specialist — Coroutines, Multiplatform
└── swift-expert     — iOS/macOS, async/await

INFRAESTRUCTURA / INFRA
├── docker-expert    — Contenedores, optimización
├── kubernetes-specialist — Orquestación K8s
├── terraform-engineer — IaC, multi-cloud
└── devops-engineer  — CI/CD, pipelines

ESPECIALISTAS / SPECIALISTS
├── database-administrator — PostgreSQL, MySQL, Oracle
├── ml-engineer      — Pipelines ML, servido de modelos
├── security-engineer — ZTA, compliance, hardening
└── debugger         — Diagnóstico de bugs complejos
```

### Uso de Agentes / Agent Usage

```
# Secuencial (cuando hay dependencias)
planner → tdd-guide → code-reviewer → security-reviewer

# Paralelo (cuando son independientes)
security-reviewer + performance-engineer + typescript-reviewer
(se lanzan simultáneamente / launched simultaneously)

# En worktree aislado (para no afectar repo principal)
Agent con isolation: "worktree"
```

### Decisión: ¿Cuándo usar un agente? / When to use an agent?

```
✅ USAR AGENTE cuando:              USE AGENT when:
   - Tarea multi-paso compleja       Multi-step complex task
   - Necesita dominio especializado  Needs specialized domain
   - Proteger contexto principal     Protect main context window
   - Trabajo paralelo independiente  Independent parallel work

❌ NO USAR AGENTE cuando:           DON'T USE AGENT when:
   - Búsqueda simple de archivo      Simple file search
   - Leer 1-3 archivos específicos   Reading 1-3 specific files
   - Edición menor de código         Minor code edit
   - Pregunta conversacional         Conversational question
```

### Construcción de Agentes / Building Agents

**ES:** Diseña agentes con una responsabilidad clara, entradas explícitas y un formato de salida estricto. Un agente ambiguo produce resultados inconsistentes.

**EN:** Design agents with a clear responsibility, explicit inputs, and a strict output format. An ambiguous agent leads to inconsistent results.

#### Archivo de Agente / Agent File

```
~/.claude/agents/mi-agente.md
```

#### Plantilla Base de Agente / Agent Starter Template

```markdown
# Agent: mi-agente

## Mission
Resolver [tipo de tarea] con foco en [criterio principal].

## Inputs Required
- Contexto mínimo del usuario
- Archivos o rutas clave
- Restricciones (tiempo, seguridad, stack)

## Process
1. Analizar contexto disponible
2. Ejecutar pasos técnicos en orden
3. Verificar resultados y riesgos

## Output Contract
- Findings críticos primero
- Cambios propuestos con rutas de archivo
- Lista de verificación final

## Guardrails
- No ejecutar acciones destructivas sin confirmación
- No asumir datos no verificados
```

#### Orquestación y Manejo Diario / Orchestration and Daily Operations

| Escenario / Scenario | Patrón recomendado / Recommended pattern |
|---|---|
| Dependencias entre tareas | Secuencial: `planner -> implementer -> reviewer` |
| Tareas independientes | Paralelo: `security-reviewer + typescript-reviewer + test-automator` |
| Código de alto riesgo | Revisión dual: `code-reviewer` + `security-reviewer` |
| Cambios grandes | Aislar en `worktree` y consolidar al final |

#### Checklist de Gestión de Agentes / Agent Management Checklist

```
1. Definir owner y alcance del agente antes de lanzarlo
2. Especificar archivos o módulos bajo su responsabilidad
3. Exigir formato de salida consistente (hallazgos, diff, riesgos)
4. Cerrar agentes que ya terminaron para evitar ruido de contexto
5. Reusar agentes efectivos y retirar los que no aportan
```

---

## 14. Selección de Modelos / Model Selection

### Modelos Disponibles / Available Models

| Modelo / Model | ID | Fortaleza ES | Strength EN | Uso Recomendado |
|---|---|---|---|---|
| **Opus 4.6** | `claude-opus-4-6` | Razonamiento profundo | Deep reasoning | Arquitectura, análisis complejo |
| **Sonnet 4.6** | `claude-sonnet-4-6` | Mejor para código | Best for coding | Desarrollo principal |
| **Haiku 4.5** | `claude-haiku-4-5-20251001` | Velocidad y costo | Speed and cost | Agentes frecuentes, workers |

### Estrategia de Selección / Selection Strategy

```
┌─────────────────────────────────────────────────────────┐
│              CUÁNDO USAR CADA MODELO                     │
│              WHEN TO USE EACH MODEL                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  HAIKU 4.5 (3x ahorro vs Sonnet / 3x savings vs Sonnet)│
│  ├── Agentes worker en sistemas multi-agente            │
│  ├── Pair programming y generación de código simple     │
│  └── Tareas con invocación muy frecuente                │
│                                                          │
│  SONNET 4.6 (El mejor para código / Best for code)      │
│  ├── Trabajo de desarrollo principal                     │
│  ├── Orquestar flujos multi-agente                      │
│  └── Tareas de codificación complejas                   │
│                                                          │
│  OPUS 4.6 (Razonamiento máximo / Maximum reasoning)     │
│  ├── Decisiones arquitectónicas complejas               │
│  ├── Investigación y análisis profundo                  │
│  └── Cuando se necesita el máximo razonamiento          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Configuración de Modelo / Model Configuration

```bash
# Línea de comando / Command line
claude --model claude-opus-4-6 "Diseña la arquitectura..."

# En settings.json
{
  "defaultModel": "claude-sonnet-4-6",
  "agents": {
    "workerModel": "claude-haiku-4-5-20251001",
    "orchestratorModel": "claude-sonnet-4-6"
  }
}

# Variables de entorno / Environment variables
export ANTHROPIC_MODEL=claude-sonnet-4-6
```

---

## 15. Estrategias Avanzadas / Advanced Strategies

### Extended Thinking (Pensamiento Extendido)

**ES:** Extended Thinking reserva hasta 31,999 tokens para razonamiento interno antes de responder. Ideal para problemas complejos.

**EN:** Extended Thinking reserves up to 31,999 tokens for internal reasoning before responding. Ideal for complex problems.

```bash
# Activar/Desactivar / Enable/Disable
Option+T (macOS) | Alt+T (Windows/Linux)

# Configurar límite / Configure limit
export MAX_THINKING_TOKENS=10000

# Ver el thinking / See the thinking
Ctrl+O (verbose mode)

# Usar en prompts / Use in prompts
"Think step-by-step about..."
"Analyze the root cause before suggesting a fix"
"Plan before executing"
"Verify your assumptions first"
```

### Gestión del Contexto / Context Management

```
# La ventana de contexto se llena con:
# The context window fills with:
- Historial de conversación / Conversation history
- Contenido de archivos leídos / Read file contents
- Resultados de herramientas / Tool results
- Skills cargadas / Loaded skills

# Estrategias para conservar contexto:
# Strategies to conserve context:
/compact           → Comprime sin perder esencia / Compress without losing essence
/clear             → Limpia todo (usar con cuidado) / Clear all (use carefully)
Nuevo proyecto     → Sesión fresca / Fresh session
Últimas 20% del contexto → Evitar tareas complejas / Avoid complex tasks
```

### Prompts de Alta Efectividad / High-Effectiveness Prompts

```
❌ VAGO:    "Arregla el bug"
✅ PRECISO: "En src/auth/middleware.ts:45, el guard JWT no 
             valida la expiración. Agregar verificación de 
             exp claim y lanzar UnauthorizedException si expiró."

❌ VAGO:    "Mejorar el rendimiento"
✅ PRECISO: "El endpoint GET /api/users tarda 3s. El profiler
             muestra que getUsersWithRoles() hace N+1 queries.
             Convertir a un JOIN con eager loading."

❌ VAGO:    "Escribir tests"
✅ PRECISO: "Escribir tests unitarios para AuthService.validateToken()
             en src/auth/auth.service.ts. Cubrir: token válido,
             expirado, malformado y usuario no encontrado. Jest."
```

### Workflow TDD Completo / Complete TDD Workflow

```
FASE RED (Rojo):
  /tdd → Escribir tests que fallan primero
  "Escribe tests para [función] cubriendo [casos edge]"
  Verificar que fallan con el mensaje correcto

FASE GREEN (Verde):
  "Implementa [función] para pasar los tests"
  Mínimo código necesario / Minimum code needed
  Verificar que todos los tests pasan

FASE REFACTOR (Mejorar):
  /simplify → Revisar código para calidad
  /code-review → Revisión completa
  /security-review → Si maneja datos sensibles
  Tests deben seguir pasando
```

### Multi-Agente Paralelo / Parallel Multi-Agent

```
# Estrategia: lanzar agentes independientes en paralelo
# Strategy: launch independent agents in parallel

EJEMPLO / EXAMPLE:
Tarea: "Hacer PR-ready el módulo de pagos"

→ PARALELO (simultáneamente / simultaneously):
   Agent 1: security-reviewer → Analizar vulnerabilidades
   Agent 2: typescript-reviewer → Revisar tipos y patrones  
   Agent 3: test-automator → Evaluar cobertura de tests

→ SECUENCIAL (esperando resultados / waiting for results):
   Agent 4: code-reviewer → Consolida todos los hallazgos
   Agent 5: tdd-guide → Implementar tests faltantes
```

---

## 16. Seguridad y Permisos / Security & Permissions

### Modelo de Permisos / Permission Model

```
HERRAMIENTAS DE SOLO LECTURA (siempre permitidas):
READ-ONLY TOOLS (always allowed):
  Read, Glob, Grep, Bash (read-only commands)

HERRAMIENTAS DE MODIFICACIÓN (piden confirmación por defecto):
MODIFICATION TOOLS (ask confirmation by default):
  Write, Edit, Bash (write commands), Agent

ACCIONES DE ALTO RIESGO (siempre piden confirmación):
HIGH-RISK ACTIONS (always ask confirmation):
  git push, rm -rf, DROP TABLE, force operations
```

### Configuración de Permisos / Permission Configuration

```json
// ~/.claude/settings.json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob", 
      "Grep",
      "Bash(git status)",
      "Bash(npm test)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force)"
    ]
  }
}
```

### Buenas Prácticas de Seguridad / Security Best Practices

```
✅ Revisar diffs antes de aceptar cambios
   Review diffs before accepting changes

✅ Usar CLAUDE.md para documentar restricciones del proyecto
   Use CLAUDE.md to document project restrictions

✅ No commitear .env, credentials, o secrets
   Don't commit .env, credentials, or secrets

✅ Para operaciones destructivas, confirmar manualmente
   For destructive operations, confirm manually

✅ Usar hooks para bloquear comandos peligrosos
   Use hooks to block dangerous commands

✅ Revisar permisos de MCP servers antes de conectar
   Review MCP server permissions before connecting

✅ Secrets en variables de entorno, nunca en código
   Secrets in environment variables, never in code
```

---

## 17. Flujo de Trabajo Completo / Complete Workflow

### Pipeline de Desarrollo Recomendado / Recommended Development Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│          PIPELINE DE DESARROLLO CON CLAUDE CODE             │
│          DEVELOPMENT PIPELINE WITH CLAUDE CODE              │
└─────────────────────────────────────────────────────────────┘

0. INVESTIGACIÓN / RESEARCH
   ├── gh search repos/code → Buscar implementaciones existentes
   ├── /documentation-lookup → Consultar docs de librerías
   └── WebSearch → Investigación amplia

1. PLANIFICACIÓN / PLANNING
   ├── /plan → Crear plan de implementación
   ├── Genera: PRD, arquitectura, diseño, tasks
   └── Identifica dependencias y riesgos

2. TDD
   ├── /tdd → Escribir tests primero (RED)
   ├── Implementar código (GREEN)
   └── Refactorizar (IMPROVE)

3. REVISIÓN / REVIEW
   ├── /code-review → Calidad general
   ├── /security-review → Análisis de seguridad
   └── Resolver CRITICAL y HIGH issues

4. COMMIT & PUSH
   ├── /commit → Commit con mensaje convencional
   ├── gh pr create → Pull request estructurado
   └── CI/CD pipeline automático
```

### Comandos para Cada Fase / Commands for Each Phase

```bash
# Fase 0: Research
gh search code "función similar" --language typescript
/documentation-lookup "librería específica"

# Fase 1: Plan
/plan
/blueprint  # Vista de arquitectura

# Fase 2: TDD
/tdd
/test-coverage  # Verificar cobertura

# Fase 3: Review  
/code-review
/security-review
/verify

# Fase 4: Commit
/commit
/docs  # Actualizar documentación
/update-codemaps  # Actualizar mapas de código
```

---

## 18. Referencia Rápida / Quick Reference

### Cheatsheet de Comandos / Commands Cheatsheet

```
INICIO / START
  claude                     → Modo interactivo / Interactive mode
  claude -c                  → Continuar última sesión / Continue last session
  claude --resume [id]       → Reanudar sesión / Resume session

GESTIÓN DE CONTEXTO / CONTEXT MANAGEMENT
  /compact                   → Comprimir contexto / Compress context
  /clear                     → Limpiar todo / Clear all
  /cost                      → Ver tokens usados / View tokens used

DESARROLLO / DEVELOPMENT
  /plan                      → Planificar feature / Plan feature
  /tdd                       → Test-driven development
  /commit                    → Crear commit / Create commit
  /code-review               → Revisar código / Review code
  /security-review           → Análisis seguridad / Security analysis

DOCUMENTACIÓN / DOCUMENTATION
  /docs                      → Actualizar docs / Update docs
  /docx                      → Crear Word doc / Create Word doc
  /article-writing           → Escribir artículo / Write article

MODELOS / MODELS
  Haiku 4.5    → Workers, tareas frecuentes / Workers, frequent tasks
  Sonnet 4.6   → Desarrollo principal / Main development
  Opus 4.6     → Análisis profundo / Deep analysis

EXTENDED THINKING
  Option+T     → Toggle (macOS)
  Alt+T        → Toggle (Windows/Linux)
  Ctrl+O       → Ver reasoning / See reasoning

MCP TOOLS (si configurados / if configured)
  mcp__canva__*              → Diseño en Canva / Canva design
  mcp__github__*             → GitHub operations
  mcp__postgres__*           → Database queries
```

### Estructura de Archivos de Configuración / Configuration Files Structure

```
~/.claude/
├── settings.json            ← Config global (hooks, permissions, MCP)
├── CLAUDE.md                ← Instrucciones globales
├── keybindings.json         ← Atajos personalizados
├── skills/                  ← Skills activas
│   ├── docx/
│   ├── claude-code-guide/
│   └── ...
├── agents/                  ← Definiciones de agentes
│   ├── planner.md
│   ├── code-reviewer.md
│   └── ...
├── rules/                   ← Reglas globales
│   ├── development-workflow.md
│   ├── git-workflow.md
│   └── performance.md
└── projects/
    └── [proyecto]/
        └── memory/
            ├── MEMORY.md
            └── *.md
```

---

## Recursos Adicionales / Additional Resources

- **Documentación oficial / Official docs:** `claude.ai/docs`
- **GitHub Issues:** `anthropics/claude-code`
- **Comunidad / Community:** `claude.ai/community`
- **Changelog:** `/status` en la CLI
- **MCP Registry:** `modelcontextprotocol.io`

---

*Generado con Claude Code — claude-sonnet-4-6 | 2026-04-04*
