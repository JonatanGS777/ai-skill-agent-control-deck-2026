.PHONY: help pycompile catalog benchmarks dashboard docs-portal semver-init semver-apply semver-check quality quality-strict logic-pack aliases aliases-created aliases-ai release-auto release bootstrap

GROUP_NAME ?= CEO Jonatan Agent
AGENT_ROOT ?= agents
INSTALL_TARGET ?= both
INSTALL_METHOD ?= symlink
RELEASE_VERSION ?=
RELEASE_CHANNEL ?= stable
RELEASE_NOTES ?=

PY_SCRIPTS = scripts/universal_skill_creator.py \
	scripts/universal_agent_creator.py \
	scripts/create_logic_foundation_skills.py \
	scripts/install_agent_group_aliases.py \
	scripts/install_created_agent_group.py \
	scripts/rebuild_repo_catalog.py \
	scripts/run_benchmarks.py \
	scripts/build_quality_dashboard.py \
	scripts/build_docs_portal.py \
	scripts/semantic_version_manager.py \
	scripts/generate_release_bundle.py \
	scripts/generate_exceptional_pack_2026.py \
	scripts/generate_ai_factory_pack_2026.py

help:
	@echo "Targets:"
	@echo "  make pycompile       - Compile-check Python scripts"
	@echo "  make catalog         - Rebuild catalog files"
	@echo "  make semver-init     - Initialize semantic version state baseline"
	@echo "  make semver-apply    - Apply semantic version bumps and update state"
	@echo "  make semver-check    - Check pending semantic bumps (strict)"
	@echo "  make benchmarks      - Run benchmark suite and quality score ranking"
	@echo "  make dashboard       - Build interactive local quality dashboard HTML"
	@echo "  make docs-portal     - Build documentation portal under docs/portal/"
	@echo "  make quality         - Compile-check + semver + benchmarks + catalog + dashboard + docs portal gate"
	@echo "  make release-auto    - Run quality gate and create next patch release bundle"
	@echo "  make release         - Run quality gate and create release bundle (optional RELEASE_VERSION=vX.Y.Z)"
	@echo "  make logic-pack      - Rebuild/install 30 logic foundation skills"
	@echo "  make aliases         - Install grouped agent aliases"
	@echo "  make aliases-created - Install dedicated group aliases for created exceptional agents"
	@echo "  make aliases-ai      - Install dedicated group aliases for AI factory agents"
	@echo "  make bootstrap       - logic-pack + aliases + semver-apply + quality"

pycompile:
	python3 -m py_compile $(PY_SCRIPTS)

catalog:
	python3 scripts/rebuild_repo_catalog.py

semver-init:
	python3 scripts/semantic_version_manager.py --mode initialize --scope both

semver-apply:
	python3 scripts/semantic_version_manager.py --mode apply --scope both

semver-check:
	python3 scripts/semantic_version_manager.py --mode check --scope both --strict

benchmarks:
	python3 scripts/run_benchmarks.py --strict

dashboard:
	python3 scripts/build_quality_dashboard.py

docs-portal:
	python3 scripts/build_docs_portal.py

quality:
	python3 -m py_compile $(PY_SCRIPTS)
	python3 scripts/semantic_version_manager.py --mode check --scope both --strict
	python3 scripts/run_benchmarks.py --strict
	python3 scripts/rebuild_repo_catalog.py --strict
	python3 scripts/build_quality_dashboard.py
	python3 scripts/build_docs_portal.py

quality-strict: quality

release-auto: quality
	python3 scripts/generate_release_bundle.py --strict
	python3 scripts/build_docs_portal.py

release: quality
	@if [ -n "$(RELEASE_VERSION)" ]; then \
		python3 scripts/generate_release_bundle.py --version "$(RELEASE_VERSION)" --channel "$(RELEASE_CHANNEL)" --notes "$(RELEASE_NOTES)" --strict; \
	else \
		python3 scripts/generate_release_bundle.py --channel "$(RELEASE_CHANNEL)" --notes "$(RELEASE_NOTES)" --strict; \
	fi
	python3 scripts/build_docs_portal.py

logic-pack:
	python3 scripts/create_logic_foundation_skills.py \
		--install-target $(INSTALL_TARGET) \
		--install-method $(INSTALL_METHOD) \
		--overwrite

aliases:
	python3 scripts/install_agent_group_aliases.py \
		--agent-root $(AGENT_ROOT) \
		--group-name "$(GROUP_NAME)" \
		--install-target $(INSTALL_TARGET) \
		--overwrite

aliases-created:
	python3 scripts/install_created_agent_group.py \
		--agent-root $(AGENT_ROOT) \
		--install-target $(INSTALL_TARGET) \
		--overwrite

aliases-ai:
	python3 scripts/install_created_agent_group.py \
		--agent-root $(AGENT_ROOT) \
		--suffix=-ai-agent-2026 \
		--group-prefix ceo-jonatan-ai-factory \
		--install-target $(INSTALL_TARGET) \
		--overwrite

bootstrap: logic-pack aliases semver-apply quality
