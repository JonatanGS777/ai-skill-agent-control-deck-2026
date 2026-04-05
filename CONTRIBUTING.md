# Contributing

Gracias por contribuir a este repositorio.

## Flujo obligatorio

1. Crea una rama de trabajo.
2. Implementa cambios pequeños y enfocados.
3. Ejecuta:

```bash
make quality
```

4. Si el cambio es de release, ejecuta:

```bash
make release-auto
```

5. Abre PR usando el template oficial.

## Estandares

- Mantener compatibilidad entre Claude Code y Codex.
- Priorizar logica, claridad, seguridad y utilidad.
- Evitar prompts/agentes genericos sin fundamento.
- Añadir/actualizar documentacion cuando cambie comportamiento.

## Revisiones

Antes de merge, valida:
- `docs/governance/review-checklist.md`
- `docs/governance/definition-of-done.md`

## Convenciones de commits

Formato sugerido:
- `feat: ...`
- `fix: ...`
- `docs: ...`
- `chore: ...`
- `refactor: ...`
- `test: ...`
