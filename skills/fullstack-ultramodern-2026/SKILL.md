---
name: "fullstack-ultramodern-2026"
description: "Construye productos full stack 2026 con React 19, TypeScript, Tailwind y arquitectura moderna de producción."
version: "1.2.0"
domain: "fullstack"
quality_tier: "expert"
compatibility:
  - claude-code
  - codex
owner: "yonatanguerrerosoriano"
tags:
  - "fullstack"
  - "react-19"
  - "typescript"
  - "tailwind"
  - "architecture"
  - "production-ready"
  - "2026"
foundation_skills:
  - "logic-of-programs-hoare"
  - "algorithm-correctness-invariants"
  - "type-systems-foundations"
  - "testing-verification-foundations"
  - "security-threat-modeling-foundations"
  - "distributed-systems-consistency-foundations"
---

# Fullstack Ultramodern 2026 Skill

## Mission
Construir productos full stack modernos de extremo a extremo con calidad de producción, usando React 19 + TypeScript + Tailwind como núcleo y un ecosistema actualizado de backend, datos, seguridad, testing y despliegue.

## When to use
- Cuando el usuario pide una feature o producto full stack completo (UI + API + DB + infra).
- Cuando se requiere stack moderno con React 19, TypeScript estricto y Tailwind.
- Cuando hay que pasar de idea/prototipo a implementación mantenible y escalable.

## Inputs expected
- Objetivo del producto, audiencia y flujo principal de usuario.
- Alcance: MVP, beta o producción.
- Requisitos no funcionales: seguridad, rendimiento, observabilidad, costo.
- Restricciones de plataforma (Vercel, Node runtime, edge, contenedores, etc.).
- Base existente (si hay repo) y convenciones que deben respetarse.

## Workflow
1. Arquitectura y decisiones de stack:
   - Definir arquitectura objetivo (monorepo o app única).
   - Establecer fronteras claras: `app`, `api`, `domain`, `data`, `infra`.
   - Seleccionar estrategia de APIs: Server Actions, route handlers, tRPC o REST según caso.
2. Implementación frontend moderna:
   - React 19 + TypeScript strict.
   - Tailwind para sistema visual consistente, con design tokens y componentes reutilizables.
   - Rendering strategy explícita (SSR, RSC, client islands, streaming).
   - Gestión de estado mínima y deliberada (evitar sobre-arquitectura).
3. Implementación backend y datos:
   - Validación de entradas/salidas con schemas (ej. Zod).
   - Capa de datos con tipado end-to-end (ORM/query builder) y migraciones controladas.
   - Autenticación/autorización por rol y protección de rutas sensibles.
   - Cache estratégica y manejo de errores uniforme.
4. Calidad de producción:
   - Tests críticos (unit/integration/e2e) en caminos de negocio.
   - Logging estructurado, métricas y trazas para debugging real.
   - Hardening básico: secretos, rate limiting, sanitización y permisos mínimos.
5. Revisión final:
   - Validar DX, mantenibilidad, y escalabilidad.
   - Documentar decisiones técnicas y trade-offs.
   - Entregar con checklist de verificación y próximos pasos.

## Output contract
Responder siempre en este orden:
1. Arquitectura propuesta y por qué.
2. Stack exacto por capa (UI, API, DB, auth, testing, deploy).
3. Cambios implementados (archivos/rutas/componentes/endpoints).
4. Validaciones realizadas (tipos, tests, seguridad, performance).
5. Riesgos residuales y siguientes pasos.

## Guardrails
- Nunca entregar boilerplate genérico sin criterio arquitectónico.
- Nunca desactivar TypeScript strict para “hacer que compile”.
- Nunca omitir validación de entrada/salida en APIs y acciones sensibles.
- Nunca priorizar velocidad sobre seguridad básica o integridad de datos.
- Preferir simplicidad escalable: menos abstracción, más claridad.

## Foundations
- `logic-of-programs-hoare`
- `algorithm-correctness-invariants`
- `type-systems-foundations`
- `testing-verification-foundations`
- `security-threat-modeling-foundations`
- `distributed-systems-consistency-foundations`

## Logical reliability checklist
- Supuestos de arquitectura y riesgo estan explicitados antes de implementar.
- Cada decision de stack se conecta con restricciones verificables del contexto.
- Seguridad, validacion y pruebas forman parte del flujo base, no de una fase final.
- El resultado final es auditable con evidencia tecnica y criterios reproducibles.

## Stack baseline (2026-oriented)
- Frontend: React 19 + TypeScript + Tailwind.
- Full stack framework recomendado: Next.js App Router (o equivalente moderno si el usuario lo pide).
- Data contracts: schemas tipados (ej. Zod).
- Data layer: PostgreSQL con migraciones y tipado end-to-end.
- API strategy: Route Handlers / Server Actions / tRPC según acoplamiento.
- Auth: sesiones seguras + RBAC mínimo.
- Testing: unit + integration + e2e en flujos críticos.
- Tooling: lint + typecheck + format + CI gates.
- Observabilidad: logs estructurados y errores accionables.

## Advanced elements to propose when relevant
- Streaming UI/AI responses.
- Queues/jobs para tareas largas.
- Caching por tags o llaves con invalidación explícita.
- Feature flags para rollouts graduales.
- Rate limiting y protección anti abuso.
- Auditoría de eventos sensibles.

## Definition of done
- Build pasa sin warnings críticos.
- Typecheck estricto en verde.
- Flujos core verificados por tests.
- Seguridad mínima implementada y documentada.
- UI responsive y accesible en escritorio y móvil.

## Example prompts
- "Usa `fullstack-ultramodern-2026` para construir un SaaS de gestión de proyectos con React 19, TypeScript y Tailwind, listo para producción."
- "Aplica `fullstack-ultramodern-2026` y diseña arquitectura + implementación de auth, billing y panel admin con validación end-to-end."
- "Corre `fullstack-ultramodern-2026` y refactoriza este proyecto legacy hacia stack moderno con migración incremental y sin romper producción."
