#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SkillSpec:
    name: str
    description: str
    domain: str
    quality_tier: str
    tags: tuple[str, ...]
    foundation_skills: tuple[str, ...]


@dataclass(frozen=True)
class AgentSpec:
    name: str
    description: str
    agent_type: str
    tags: tuple[str, ...]
    explicit_skills: tuple[str, ...]
    logic_foundation: str


AUTOMATION_TOPICS = [
    "workflow-orchestration",
    "rpa-pipeline-design",
    "event-driven-automation",
    "api-integration-automation",
    "data-pipeline-automation",
    "qa-automation-systems",
    "devops-automation",
    "incident-response-automation",
    "crm-automation",
    "sales-funnel-automation",
    "finance-ops-automation",
    "hr-ops-automation",
    "document-processing-automation",
    "etl-observability-automation",
    "process-mining-automation",
    "enterprise-policy-automation",
    "no-code-automation-architecture",
    "agentic-workflow-automation",
    "task-prioritization-engines",
    "automation-risk-controls",
]

CHATBOT_TOPICS = [
    "conversational-design",
    "retrieval-augmented-chat",
    "multi-turn-memory",
    "tool-calling-orchestration",
    "omnichannel-chat-platform",
    "voice-chatbot-orchestration",
    "support-chatbot-operations",
    "sales-chatbot-operations",
    "multilingual-chatbot-systems",
    "compliance-chatbot-guardrails",
    "chatbot-evaluation-metrics",
    "chatbot-fallback-escalation",
    "persona-consistency-engine",
    "prompt-routing-strategies",
    "sentiment-aware-dialog",
    "chatbot-analytics-pipeline",
    "realtime-chat-infrastructure",
    "chatbot-security-hardening",
    "chatbot-ab-testing",
    "enterprise-knowledge-chatbots",
]

AI_AREA_TOPICS = [
    "healthcare-assistant-systems",
    "legal-research-assistants",
    "education-tutoring-platforms",
    "finance-analysis-copilots",
    "retail-personalization-engines",
    "logistics-optimization-control",
    "manufacturing-quality-intelligence",
    "cybersecurity-operations-ai",
    "media-content-studio-ai",
    "marketing-campaign-intelligence",
    "product-management-copilot",
    "hr-recruiting-intelligence",
    "real-estate-market-intelligence",
    "government-service-automation",
    "agritech-decision-intelligence",
    "climate-risk-analytics",
    "biotech-research-acceleration",
    "insurance-claims-automation",
    "energy-demand-forecasting",
    "research-lab-orchestration",
    "customer-success-ai-operations",
    "ecommerce-conversion-intelligence",
    "travel-planning-assistants",
    "hospitality-service-assistants",
    "nonprofit-impact-analytics",
    "sports-performance-intelligence",
    "public-safety-intelligence",
    "entertainment-production-ai",
    "supply-chain-control-tower-ai",
    "mobility-routing-intelligence",
]


def topic_to_text(topic: str) -> str:
    return topic.replace("-", " ")


def dedupe(items: tuple[str, ...]) -> tuple[str, ...]:
    seen: dict[str, None] = {}
    for item in items:
        if item not in seen:
            seen[item] = None
    return tuple(seen.keys())


def build_skill_specs() -> list[SkillSpec]:
    automation_foundations = (
        "logic-of-programs-hoare",
        "algorithm-correctness-invariants",
        "distributed-systems-consistency-foundations",
        "testing-verification-foundations",
        "security-threat-modeling-foundations",
        "debugging-causal-reasoning-foundations",
    )
    chatbot_foundations = (
        "logic-propositional-reasoning",
        "logic-predicate-quantifiers",
        "type-systems-foundations",
        "probability-foundations",
        "testing-verification-foundations",
        "security-threat-modeling-foundations",
    )
    area_foundations = (
        "optimization-foundations",
        "probability-foundations",
        "statistics-inference-foundations",
        "testing-verification-foundations",
        "security-threat-modeling-foundations",
        "debugging-causal-reasoning-foundations",
    )

    specs: list[SkillSpec] = []

    for index, topic in enumerate(AUTOMATION_TOPICS):
        specs.append(
            SkillSpec(
                name=f"automation-{topic}-skill-2026",
                description=(
                    f"Disena procesos automatizados para {topic_to_text(topic)} con control logico, "
                    "trazabilidad completa y validacion operativa de extremo a extremo."
                ),
                domain="automation-ai",
                quality_tier="expert" if index % 2 == 0 else "advanced",
                tags=("automation", "process", "ai", "orchestration", "2026"),
                foundation_skills=automation_foundations,
            )
        )

    for index, topic in enumerate(CHATBOT_TOPICS):
        specs.append(
            SkillSpec(
                name=f"chatbot-{topic}-skill-2026",
                description=(
                    f"Construye chatbots de alto rendimiento para {topic_to_text(topic)} con dialogo robusto, "
                    "guardrails claros y monitoreo continuo de calidad."
                ),
                domain="chatbot-ai",
                quality_tier="expert" if index % 3 != 0 else "advanced",
                tags=("chatbot", "conversational-ai", "llm", "guardrails", "2026"),
                foundation_skills=chatbot_foundations,
            )
        )

    for index, topic in enumerate(AI_AREA_TOPICS):
        specs.append(
            SkillSpec(
                name=f"ai-domain-{topic}-skill-2026",
                description=(
                    f"Despliega soluciones de IA para {topic_to_text(topic)} con arquitectura modular, "
                    "metricas auditables y decisiones alineadas al contexto del dominio."
                ),
                domain="domain-ai",
                quality_tier="expert" if index % 4 != 0 else "advanced",
                tags=("domain-ai", "industry-ai", "automation", "decision-systems", "2026"),
                foundation_skills=area_foundations,
            )
        )

    return specs


def build_agent_specs() -> list[AgentSpec]:
    specs: list[AgentSpec] = []

    for topic in AUTOMATION_TOPICS:
        base_skill = f"automation-{topic}-skill-2026"
        specs.append(
            AgentSpec(
                name=f"automation-{topic}-orchestrator-ai-agent-2026",
                description=(
                    "Orquesta procesos automatizados con enfoque en confiabilidad, observabilidad "
                    "y alineacion con objetivos operativos."
                ),
                agent_type="orchestrator",
                tags=("automation", "orchestrator", "ai-agent", "2026", "process"),
                explicit_skills=dedupe(
                    (
                        base_skill,
                        "automation-agentic-workflow-automation-skill-2026",
                        "automation-enterprise-policy-automation-skill-2026",
                        "logic-of-programs-hoare",
                        "testing-verification-foundations",
                        "distributed-systems-consistency-foundations",
                        "security-threat-modeling-foundations",
                        "debugging-causal-reasoning-foundations",
                    )
                ),
                logic_foundation="max",
            )
        )
        specs.append(
            AgentSpec(
                name=f"automation-{topic}-executor-ai-agent-2026",
                description=(
                    "Ejecuta implementaciones automatizadas con foco en integracion segura, "
                    "pruebas verificables y despliegue mantenible."
                ),
                agent_type="builder",
                tags=("automation", "builder", "ai-agent", "2026", "execution"),
                explicit_skills=dedupe(
                    (
                        base_skill,
                        "automation-api-integration-automation-skill-2026",
                        "automation-task-prioritization-engines-skill-2026",
                        "algorithm-correctness-invariants",
                        "type-systems-foundations",
                        "testing-verification-foundations",
                        "debugging-causal-reasoning-foundations",
                    )
                ),
                logic_foundation="max",
            )
        )

    for topic in CHATBOT_TOPICS[:15]:
        base_skill = f"chatbot-{topic}-skill-2026"
        specs.append(
            AgentSpec(
                name=f"chatbot-{topic}-designer-ai-agent-2026",
                description=(
                    "Disena experiencias conversacionales modernas con coherencia de persona, "
                    "contexto persistente y contratos de salida robustos."
                ),
                agent_type="specialist",
                tags=("chatbot", "designer", "ai-agent", "2026", "conversation"),
                explicit_skills=dedupe(
                    (
                        base_skill,
                        "chatbot-conversational-design-skill-2026",
                        "chatbot-prompt-routing-strategies-skill-2026",
                        "chatbot-persona-consistency-engine-skill-2026",
                        "logic-predicate-quantifiers",
                        "type-systems-foundations",
                        "testing-verification-foundations",
                    )
                ),
                logic_foundation="max",
            )
        )
        specs.append(
            AgentSpec(
                name=f"chatbot-{topic}-operator-ai-agent-2026",
                description=(
                    "Opera chatbots en produccion con monitoreo activo, controles de riesgo "
                    "y estrategias de fallback verificables."
                ),
                agent_type="debugger",
                tags=("chatbot", "operations", "ai-agent", "2026", "production"),
                explicit_skills=dedupe(
                    (
                        base_skill,
                        "chatbot-support-chatbot-operations-skill-2026",
                        "chatbot-chatbot-fallback-escalation-skill-2026",
                        "chatbot-chatbot-security-hardening-skill-2026",
                        "debugging-causal-reasoning-foundations",
                        "security-threat-modeling-foundations",
                        "probability-foundations",
                        "testing-verification-foundations",
                    )
                ),
                logic_foundation="max",
            )
        )

    role_cycle = [
        ("strategist", "orchestrator"),
        ("builder", "builder"),
        ("auditor", "reviewer"),
    ]
    for index, topic in enumerate(AI_AREA_TOPICS):
        role_name, agent_type = role_cycle[index % len(role_cycle)]
        base_skill = f"ai-domain-{topic}-skill-2026"
        specs.append(
            AgentSpec(
                name=f"ai-{topic}-{role_name}-ai-agent-2026",
                description=(
                    "Construye y gobierna soluciones de IA por dominio con objetivos claros, "
                    "controles logicos y validacion continua del impacto."
                ),
                agent_type=agent_type,
                tags=("domain-ai", role_name, "ai-agent", "2026", "governance"),
                explicit_skills=dedupe(
                    (
                        base_skill,
                        "automation-workflow-orchestration-skill-2026",
                        "chatbot-enterprise-knowledge-chatbots-skill-2026",
                        "optimization-foundations",
                        "probability-foundations",
                        "statistics-inference-foundations",
                        "testing-verification-foundations",
                        "security-threat-modeling-foundations",
                    )
                ),
                logic_foundation="max",
            )
        )

    return specs


def run_command(cmd: list[str], dry_run: bool) -> None:
    if dry_run:
        print("[dry-run]", " ".join(cmd))
        return
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        if result.stdout.strip():
            print(result.stdout.strip(), file=sys.stderr)
        if result.stderr.strip():
            print(result.stderr.strip(), file=sys.stderr)
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}")


def generate_skills(base: Path, specs: list[SkillSpec], overwrite: bool, dry_run: bool) -> None:
    creator = base / "scripts" / "universal_skill_creator.py"
    for index, spec in enumerate(specs, start=1):
        cmd = [
            "python3",
            str(creator),
            "--name",
            spec.name,
            "--description",
            spec.description,
            "--domain",
            spec.domain,
            "--quality-tier",
            spec.quality_tier,
            "--install-target",
            "none",
            "--strict",
        ]
        for tag in spec.tags:
            cmd.extend(["--tag", tag])
        for foundation in spec.foundation_skills:
            cmd.extend(["--foundation-skill", foundation])
        if overwrite:
            cmd.append("--overwrite")
        run_command(cmd, dry_run=dry_run)
        print(f"[skill {index:03d}/{len(specs)}] {spec.name}")


def generate_agents(base: Path, specs: list[AgentSpec], overwrite: bool, dry_run: bool) -> None:
    creator = base / "scripts" / "universal_agent_creator.py"
    for index, spec in enumerate(specs, start=1):
        cmd = [
            "python3",
            str(creator),
            "--name",
            spec.name,
            "--description",
            spec.description,
            "--agent-type",
            spec.agent_type,
            "--skill-mode",
            "explicit",
            "--logic-foundation",
            spec.logic_foundation,
            "--max-profile-skills",
            "16",
            "--install-target",
            "none",
            "--strict",
        ]
        for tag in spec.tags:
            cmd.extend(["--tag", tag])
        for skill in spec.explicit_skills:
            cmd.extend(["--skill", skill])
        if overwrite:
            cmd.append("--overwrite")
        run_command(cmd, dry_run=dry_run)
        print(f"[agent {index:03d}/{len(specs)}] {spec.name}")


def write_manifest(base: Path, skills: list[SkillSpec], agents: list[AgentSpec], dry_run: bool) -> None:
    manifest_path = base / "catalog" / "ai-factory-pack-2026.json"
    payload = {
        "name": "ai-factory-pack-2026",
        "skills_generated": [spec.name for spec in skills],
        "agents_generated": [spec.name for spec in agents],
        "counts": {
            "skills": len(skills),
            "agents": len(agents),
        },
    }
    if dry_run:
        print(f"[dry-run] write {manifest_path}")
        return
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate an AI factory pack: process-first skills, then 100 AI agents."
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace existing generated items.")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without writing.")
    parser.add_argument(
        "--skip-quality",
        action="store_true",
        help="Skip semantic version apply and quality checks after generation.",
    )
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]

    skill_specs = build_skill_specs()
    if len(skill_specs) != 70:
        raise RuntimeError(f"Expected 70 skills, got {len(skill_specs)}")

    agent_specs = build_agent_specs()
    if len(agent_specs) != 100:
        raise RuntimeError(f"Expected 100 agents, got {len(agent_specs)}")

    print("Generating 70 AI process-first skills...")
    generate_skills(base=base, specs=skill_specs, overwrite=args.overwrite, dry_run=args.dry_run)
    print("Generating 100 AI agents from those skills...")
    generate_agents(base=base, specs=agent_specs, overwrite=args.overwrite, dry_run=args.dry_run)
    write_manifest(base=base, skills=skill_specs, agents=agent_specs, dry_run=args.dry_run)

    if args.skip_quality or args.dry_run:
        print("Skipped semantic version and quality gates.")
        return 0

    print("Running semantic version apply + repository quality...")
    run_command(
        ["python3", str(base / "scripts" / "semantic_version_manager.py"), "--mode", "apply", "--scope", "both"],
        dry_run=False,
    )
    run_command(["make", "quality"], dry_run=False)
    print("AI factory pack generation completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
