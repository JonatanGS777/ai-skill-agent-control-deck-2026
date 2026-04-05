# Fullstack Stack Guide 2026

Guía de referencia para tomar decisiones de stack cuando se use `fullstack-ultramodern-2026`.

## Core stack

- UI: React 19 + TypeScript strict + Tailwind.
- Framework full stack: Next.js App Router (preferido para equipos web product).
- DB principal: PostgreSQL.
- Contracts: validación por schema en boundary de entrada/salida.

## Architecture pattern

1. `app/` para UI + rutas.
2. `server/` o `lib/server/` para casos de uso y reglas de negocio.
3. `data/` para acceso DB, repositorios y transacciones.
4. `shared/` para tipos, utilidades y contratos.
5. `infra/` para observabilidad, colas, caché y adaptadores externos.

## API strategy selector

- Server Actions: ideal para flujos de formulario y mutaciones acopladas a UI.
- Route Handlers REST: ideal para integraciones externas o clientes múltiples.
- tRPC: ideal cuando controlas cliente y servidor TS de punta a punta.

## State strategy

- Estado local primero.
- Server state con fetch/cache del framework o librería de data fetching.
- Estado global solo cuando exista necesidad real cross-route.

## Security minimum baseline

- Validar/sanitizar todas las entradas en server boundary.
- Autenticación sólida y autorización por rol/capacidad.
- Secrets solo en variables de entorno.
- Rate limiting en endpoints expuestos.
- Logs sin filtrar datos sensibles.

## Testing matrix

- Unit: utilidades, validadores, reglas de negocio.
- Integration: API + DB + auth boundaries.
- E2E: onboarding, auth, checkout/flujo crítico equivalente.

## Performance checklist

- Evitar over-hydration y JS innecesario en cliente.
- Definir estrategia de caché e invalidación explícita.
- Optimizar imágenes y fuentes.
- Medir métricas de Web Vitals y latencia de endpoints críticos.

## Delivery checklist

1. Typecheck estricto en verde.
2. Lint en verde.
3. Tests críticos pasando.
4. Migraciones versionadas.
5. Rollback plan básico documentado.
