#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


LOGIC_SKILLS = [
    (
        "logic-propositional-reasoning",
        "Builds solutions using propositional logic, truth conditions, and contradiction checks.",
    ),
    (
        "logic-predicate-quantifiers",
        "Applies first-order logic with quantifiers, domains, and formally scoped predicates.",
    ),
    (
        "logic-proof-strategies",
        "Uses direct proof, contraposition, contradiction, and constructive proof techniques.",
    ),
    (
        "set-theory-foundations",
        "Models problems with sets, subsets, unions, intersections, and cardinal reasoning.",
    ),
    (
        "relations-functions-foundations",
        "Formalizes relations and functions with properties, mappings, and compositional reasoning.",
    ),
    (
        "discrete-structures-core",
        "Applies core discrete math structures for rigorous software and algorithm design.",
    ),
    (
        "combinatorics-counting-principles",
        "Uses permutations, combinations, and counting arguments to validate solution spaces.",
    ),
    (
        "graph-theory-foundations",
        "Reasons about connectivity, paths, cycles, and graph properties for system models.",
    ),
    (
        "number-theory-modular-arithmetic",
        "Applies modular arithmetic and divisibility logic for correctness and crypto-adjacent tasks.",
    ),
    (
        "linear-algebra-foundations",
        "Uses vector and matrix reasoning for transformations, constraints, and model formulation.",
    ),
    (
        "probability-foundations",
        "Models uncertainty with probability axioms, conditional reasoning, and distribution checks.",
    ),
    (
        "statistics-inference-foundations",
        "Applies statistical inference, estimation, and hypothesis testing with explicit assumptions.",
    ),
    (
        "complexity-analysis-foundations",
        "Performs asymptotic analysis and tradeoff justification for algorithmic decisions.",
    ),
    (
        "algorithm-correctness-invariants",
        "Validates algorithm correctness using invariants, preconditions, and postconditions.",
    ),
    (
        "recursion-induction-foundations",
        "Solves problems with recursion and validates them through induction principles.",
    ),
    (
        "data-structures-invariants",
        "Maintains structural invariants in data structures and checks edge-case integrity.",
    ),
    (
        "formal-languages-automata",
        "Uses automata and grammar reasoning for parsing, validation, and language constraints.",
    ),
    (
        "computability-decidability",
        "Evaluates what is computable, semi-decidable, or undecidable under formal models.",
    ),
    (
        "optimization-foundations",
        "Frames optimization problems with objective functions, constraints, and feasibility logic.",
    ),
    (
        "numerical-stability-foundations",
        "Ensures numerical methods are stable, bounded, and robust against floating-point error.",
    ),
    (
        "logic-of-programs-hoare",
        "Uses Hoare-style reasoning and contracts for program correctness and safety.",
    ),
    (
        "type-systems-foundations",
        "Applies type-theoretic reasoning for sound interfaces and compile-time correctness.",
    ),
    (
        "functional-programming-foundations",
        "Uses functional abstractions, immutability, and compositional reasoning rigorously.",
    ),
    (
        "concurrency-memory-model-foundations",
        "Reasons about concurrency using ordering, visibility, and memory-model constraints.",
    ),
    (
        "database-theory-normalization",
        "Applies normalization, keys, dependencies, and integrity constraints to schema design.",
    ),
    (
        "distributed-systems-consistency-foundations",
        "Uses consistency models and failure semantics for correct distributed behavior.",
    ),
    (
        "cryptography-primitives-foundations",
        "Applies primitive-level crypto reasoning for secure protocols and key handling.",
    ),
    (
        "security-threat-modeling-foundations",
        "Builds threat models with attacker capability analysis and control-mapping logic.",
    ),
    (
        "testing-verification-foundations",
        "Combines testing strategy and formal verification checks for dependable systems.",
    ),
    (
        "debugging-causal-reasoning-foundations",
        "Uses causal reasoning to isolate root causes and avoid symptom-only fixes.",
    ),
]


COMMON_WHEN = [
    "When the task requires strict logical correctness and defensible reasoning.",
    "When assumptions, constraints, and proof obligations must be made explicit.",
]

COMMON_INPUTS = [
    "Formal problem statement, constraints, and success criteria.",
    "Known assumptions, unknowns, and boundary conditions.",
]

COMMON_STEPS = [
    "Translate the task into formal entities, assumptions, and constraints.",
    "Derive the solution through explicit logical rules or proof structure.",
    "Validate with edge cases, contradiction checks, and consistency tests.",
]

COMMON_GUARDRAILS = [
    "Never skip logical steps or present intuition as proof.",
    "Never mix assumptions with verified facts.",
    "Always provide at least one explicit validation or counterexample check.",
]

COMMON_OUTPUT = (
    "Return: formal framing, reasoning chain, verification evidence, and residual uncertainty."
)


def build_command(
    creator_script: Path,
    name: str,
    description: str,
    skill_root: str,
    install_target: str,
    install_method: str,
    overwrite: bool,
    dry_run: bool,
) -> list[str]:
    cmd = [
        "python3",
        str(creator_script),
        "--name",
        name,
        "--description",
        description,
        "--domain",
        "math-programming-logic",
        "--quality-tier",
        "expert",
        "--tag",
        "logic",
        "--tag",
        "mathematics",
        "--tag",
        "programming-foundation",
        "--skill-root",
        skill_root,
        "--install-target",
        install_target,
        "--install-method",
        install_method,
        "--output-format",
        COMMON_OUTPUT,
    ]

    for item in COMMON_WHEN:
        cmd += ["--when", item]
    for item in COMMON_INPUTS:
        cmd += ["--input", item]
    for item in COMMON_STEPS:
        cmd += ["--step", item]
    for item in COMMON_GUARDRAILS:
        cmd += ["--guardrail", item]

    if overwrite:
        cmd.append("--overwrite")
    if dry_run:
        cmd.append("--dry-run")
    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a 30-skill logic foundation pack for math + programming."
    )
    parser.add_argument("--skill-root", default="skills", help="Canonical skills root in this repo.")
    parser.add_argument(
        "--install-target",
        choices=["both", "claude", "codex", "none"],
        default="both",
        help="Where to install skills after creation.",
    )
    parser.add_argument(
        "--install-method",
        choices=["symlink", "copy"],
        default="symlink",
        help="Install by symlink or copy.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace existing skills if present.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    creator_script = base / "scripts" / "universal_skill_creator.py"
    if not creator_script.exists():
        print(f"Error: missing creator script at {creator_script}", file=sys.stderr)
        return 2

    total = len(LOGIC_SKILLS)
    print(f"Creating logic foundation pack ({total} skills)")
    for index, (name, description) in enumerate(LOGIC_SKILLS, start=1):
        print(f"[{index:02d}/{total}] {name}")
        cmd = build_command(
            creator_script=creator_script,
            name=name,
            description=description,
            skill_root=args.skill_root,
            install_target=args.install_target,
            install_method=args.install_method,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
        )
        subprocess.run(cmd, cwd=base, check=True)

    print("")
    print("Done. Logic foundation pack created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
