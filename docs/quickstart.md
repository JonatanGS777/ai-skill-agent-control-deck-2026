# Quickstart del Repositorio

## 1) Preparacion inicial

```bash
make semver-init
make logic-pack
make aliases GROUP_NAME="CEO Jonatan Agent"
```

## 2) Validacion de calidad

```bash
make quality
```

Incluye:
- compile-check de scripts Python
- semver gate
- benchmark + regression + coverage
- catalogo de calidad
- dashboard visual
- portal de documentacion

## 3) Releases

Release automatico (patch):

```bash
make release-auto
```

Release explicito:

```bash
make release RELEASE_VERSION=v1.0.0 RELEASE_CHANNEL=stable RELEASE_NOTES="Primer release estable"
```

## 4) Artefactos clave

- `catalog/benchmark-results.json`
- `catalog/benchmark-history.json`
- `catalog/skill-quality-ranking.json`
- `catalog/agent-quality-ranking.json`
- `catalog/repository-quality.md`
- `catalog/quality-dashboard.html`
- `docs/portal/index.html`
- `catalog/releases/releases-index.json`
