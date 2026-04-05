# Repository Quickstart

## 1) Initial Setup

```bash
make semver-init
make logic-pack
make aliases GROUP_NAME="CEO Jonatan Agent"
```

## 2) Quality Validation

```bash
make quality
```

Includes:
- Python script compile check
- Semver gate
- Benchmark + regression + coverage
- Quality catalog
- Visual dashboard
- Documentation portal

## 3) Releases

Automatic release (patch):

```bash
make release-auto
```

Explicit release:

```bash
make release RELEASE_VERSION=v1.0.0 RELEASE_CHANNEL=stable RELEASE_NOTES="First stable release"
```

## 4) Key Artifacts

- `catalog/benchmark-results.json`
- `catalog/benchmark-history.json`
- `catalog/skill-quality-ranking.json`
- `catalog/agent-quality-ranking.json`
- `catalog/repository-quality.md`
- `catalog/quality-dashboard.html`
- `docs/portal/index.html`
- `catalog/releases/releases-index.json`
