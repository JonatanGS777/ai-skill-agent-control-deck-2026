# Patrones Recomendados

## Skill Pattern: Logica primero

1. Definir objetivo verificable.
2. Declarar precondiciones y supuestos.
3. Especificar workflow con pasos finitos.
4. Forzar validacion final con criterios medibles.
5. Añadir guardrails de seguridad y alcance.

## Agent Pattern: Skill Bootstrap Protocol

1. Interpretar objetivo y restricciones.
2. Seleccionar skills por dominio.
3. Fusionar reglas sin contradicciones.
4. Ejecutar plan por etapas.
5. Verificar salida contra contrato.

## Quality Pattern: Todo medible

1. Publicar score por `logic`, `clarity`, `security`, `utility`.
2. Mantener regression checks de prompts.
3. Ejecutar benchmark en CI como gate obligatorio.
4. Mostrar ranking y KPIs en catalogo/dashboard.

## Release Pattern: Calidad antes de versionar

1. Ejecutar `make quality`.
2. Generar bundle versionado.
3. Actualizar `CHANGELOG.md` y releases index.
4. Publicar artifacts con workflow de release.
