#!/usr/bin/env python3
from __future__ import annotations

import argparse
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


MATH_TOPICS = [
    "formal-proof-strategy",
    "axiomatic-set-reasoning",
    "predicate-logic-modeling",
    "combinatorial-optimization-design",
    "graph-spectral-analysis",
    "discrete-probability-modeling",
    "stochastic-process-derivation",
    "statistical-estimation-rigour",
    "hypothesis-testing-design",
    "bayesian-inference-systems",
    "linear-algebraic-transforms",
    "matrix-factorization-reasoning",
    "eigen-structure-analysis",
    "numerical-method-stability",
    "convex-optimization-toolkit",
    "nonlinear-programming-analysis",
    "dynamic-programming-math",
    "recurrence-relation-solving",
    "induction-proof-engineering",
    "number-theory-algorithms",
    "modular-arithmetic-design",
    "diophantine-equation-logic",
    "information-theory-foundations",
    "entropy-and-divergence-analysis",
    "measure-theory-for-engineers",
    "calculus-of-variations-core",
    "differential-equation-modeling",
    "control-theoretic-math",
    "signal-processing-mathematics",
    "geometric-computation-math",
    "topological-data-insight",
    "category-theory-programming-bridge",
    "formal-verification-mathematics",
    "mathematical-model-audit",
]

PROGRAMMING_TOPICS = [
    "algorithm-design-architectures",
    "advanced-data-structures",
    "type-system-driven-design",
    "compiler-pipeline-construction",
    "parser-and-ast-engineering",
    "static-analysis-frameworks",
    "program-analysis-correctness",
    "api-contract-governance",
    "distributed-backend-patterns",
    "event-driven-system-design",
    "concurrency-safe-programming",
    "memory-model-practice",
    "high-performance-computing-patterns",
    "observability-driven-debugging",
    "reliability-engineering-for-services",
    "secure-coding-and-hardening",
    "authentication-authorization-flows",
    "database-system-design",
    "query-optimization-practice",
    "testing-strategy-at-scale",
    "property-based-testing-engineering",
    "continuous-delivery-architecture",
    "ci-cd-quality-automation",
    "infrastructure-as-code-patterns",
    "cloud-native-service-design",
    "microservices-resilience-patterns",
    "domain-driven-design-workflows",
    "refactoring-large-codebases",
    "legacy-modernization-tactics",
    "ai-assisted-software-delivery",
    "fullstack-product-engineering",
    "react-typescript-architecture",
    "tailwind-design-system-engineering",
]

ROBOTICS_TOPICS = [
    "robot-kinematics-modeling",
    "robot-dynamics-simulation",
    "trajectory-planning-systems",
    "motion-planning-search",
    "optimal-control-robotics",
    "nonlinear-control-robotics",
    "state-estimation-and-filtering",
    "sensor-fusion-pipelines",
    "slam-system-architecture",
    "visual-slam-engineering",
    "lidar-perception-pipelines",
    "computer-vision-for-robotics",
    "robot-manipulation-planning",
    "grasp-synthesis-methods",
    "robot-navigation-stack",
    "autonomous-mission-orchestration",
    "multi-robot-coordination",
    "swarm-robotics-protocols",
    "humanoid-motion-intelligence",
    "legged-robot-stability",
    "mobile-robot-safety",
    "industrial-robot-automation",
    "ros2-architecture-practice",
    "real-time-robotic-systems",
    "embedded-ai-robotics",
    "edge-compute-for-robotics",
    "digital-twin-robotics",
    "robotics-testing-verification",
    "fault-tolerant-robot-control",
    "human-robot-interaction-design",
    "ethical-robotic-deployment",
    "robotics-systems-integration",
    "robotics-performance-benchmarking",
]


def topic_to_title(topic: str) -> str:
    return topic.replace("-", " ")


def build_skill_specs() -> list[SkillSpec]:
    specs: list[SkillSpec] = []

    math_foundations = (
        "logic-propositional-reasoning",
        "logic-proof-strategies",
        "set-theory-foundations",
        "relations-functions-foundations",
        "complexity-analysis-foundations",
        "testing-verification-foundations",
    )
    programming_foundations = (
        "algorithm-correctness-invariants",
        "complexity-analysis-foundations",
        "type-systems-foundations",
        "debugging-causal-reasoning-foundations",
        "testing-verification-foundations",
        "security-threat-modeling-foundations",
    )
    robotics_foundations = (
        "optimization-foundations",
        "probability-foundations",
        "graph-theory-foundations",
        "numerical-stability-foundations",
        "testing-verification-foundations",
        "distributed-systems-consistency-foundations",
    )

    for idx, topic in enumerate(MATH_TOPICS):
        tier = "expert" if idx % 3 != 0 else "advanced"
        specs.append(
            SkillSpec(
                name=f"mathematics-{topic}-skill-2026",
                description=(
                    f"Desarrolla soluciones matematicas avanzadas para {topic_to_title(topic)} "
                    "con rigor formal, validacion reproducible y decisiones auditables."
                ),
                domain="mathematics",
                quality_tier=tier,
                tags=("mathematics", "logic", "proof", "2026", "high-rigor"),
                foundation_skills=math_foundations,
            )
        )

    for idx, topic in enumerate(PROGRAMMING_TOPICS):
        tier = "expert" if idx % 2 == 0 else "advanced"
        specs.append(
            SkillSpec(
                name=f"programming-{topic}-skill-2026",
                description=(
                    f"Aplica ingenieria de software moderna para {topic_to_title(topic)} "
                    "con foco en robustez, mantenibilidad y excelencia operacional."
                ),
                domain="programming",
                quality_tier=tier,
                tags=("programming", "software-engineering", "architecture", "2026", "production"),
                foundation_skills=programming_foundations,
            )
        )

    for idx, topic in enumerate(ROBOTICS_TOPICS):
        tier = "expert" if idx % 4 != 0 else "advanced"
        specs.append(
            SkillSpec(
                name=f"robotics-{topic}-skill-2026",
                description=(
                    f"Implementa practicas de robotica de alto nivel para {topic_to_title(topic)} "
                    "con seguridad, precision y control verificable de extremo a extremo."
                ),
                domain="robotics",
                quality_tier=tier,
                tags=("robotics", "autonomy", "control", "2026", "systems"),
                foundation_skills=robotics_foundations,
            )
        )

    return specs


def build_agent_specs(skill_specs: list[SkillSpec]) -> list[AgentSpec]:
    skill_names = [spec.name for spec in skill_specs]

    math_skills = [name for name in skill_names if name.startswith("mathematics-")]
    programming_skills = [name for name in skill_names if name.startswith("programming-")]
    robotics_skills = [name for name in skill_names if name.startswith("robotics-")]

    agents: list[AgentSpec] = []
    agent_types = ("specialist", "builder", "orchestrator", "reviewer", "debugger")

    def skill_window(items: list[str], i: int) -> tuple[str, str, str]:
        size = len(items)
        return (items[i % size], items[(i + 1) % size], items[(i + 2) % size])

    for i in range(25):
        s1, s2, s3 = skill_window(math_skills, i)
        agents.append(
            AgentSpec(
                name=f"mathematics-{MATH_TOPICS[i]}-exceptional-agent-2026",
                description=(
                    "Agente matematico excepcional para modelar, demostrar y validar soluciones "
                    "de alta complejidad con precision formal."
                ),
                agent_type=agent_types[i % len(agent_types)],
                tags=("mathematics", "proof", "analysis", "exceptional", "2026"),
                explicit_skills=(
                    s1,
                    s2,
                    s3,
                    "logic-proof-strategies",
                    "algorithm-correctness-invariants",
                    "testing-verification-foundations",
                ),
                logic_foundation="max",
            )
        )

    for i in range(25):
        s1, s2, s3 = skill_window(programming_skills, i)
        agents.append(
            AgentSpec(
                name=f"programming-{PROGRAMMING_TOPICS[i]}-exceptional-agent-2026",
                description=(
                    "Agente de programacion excepcional para arquitectura, implementacion y "
                    "verificacion de software moderno de produccion."
                ),
                agent_type=agent_types[(i + 1) % len(agent_types)],
                tags=("programming", "engineering", "architecture", "exceptional", "2026"),
                explicit_skills=(
                    s1,
                    s2,
                    s3,
                    "fullstack-ultramodern-2026",
                    "debugging-causal-reasoning-foundations",
                    "security-threat-modeling-foundations",
                ),
                logic_foundation="max",
            )
        )

    for i in range(20):
        s1, s2, s3 = skill_window(robotics_skills, i)
        agents.append(
            AgentSpec(
                name=f"robotics-{ROBOTICS_TOPICS[i]}-exceptional-agent-2026",
                description=(
                    "Agente de robotica excepcional para disenar sistemas autonomos robustos "
                    "con control seguro, observabilidad y validacion integral."
                ),
                agent_type=agent_types[(i + 2) % len(agent_types)],
                tags=("robotics", "autonomy", "control", "exceptional", "2026"),
                explicit_skills=(
                    s1,
                    s2,
                    s3,
                    "optimization-foundations",
                    "probability-foundations",
                    "numerical-stability-foundations",
                ),
                logic_foundation="max",
            )
        )

    return agents


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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate an exceptional 2026 pack of math/programming/robotics skills and agents."
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace existing generated items.")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without writing.")
    parser.add_argument(
        "--skip-quality",
        action="store_true",
        help="Skip catalog and semantic version quality steps after generation.",
    )
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]

    skill_specs = build_skill_specs()
    if len(skill_specs) != 100:
        raise RuntimeError(f"Expected 100 skills, got {len(skill_specs)}")

    agent_specs = build_agent_specs(skill_specs)
    if len(agent_specs) != 70:
        raise RuntimeError(f"Expected 70 agents, got {len(agent_specs)}")

    print("Generating 100 skills...")
    generate_skills(base=base, specs=skill_specs, overwrite=args.overwrite, dry_run=args.dry_run)
    print("Generating 70 agents...")
    generate_agents(base=base, specs=agent_specs, overwrite=args.overwrite, dry_run=args.dry_run)

    if args.skip_quality or args.dry_run:
        print("Skipped post-generation quality steps.")
        return 0

    print("Running semantic version apply + quality gate...")
    run_command(
        ["python3", str(base / "scripts" / "semantic_version_manager.py"), "--mode", "apply", "--scope", "both"],
        dry_run=False,
    )
    run_command(["make", "quality"], dry_run=False)
    print("Generation and quality checks completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
