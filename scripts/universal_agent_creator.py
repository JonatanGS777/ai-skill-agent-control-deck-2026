#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_SKILL_SOURCES = ["skills", "~/.claude/skills", "~/.codex/skills"]

DEFAULT_INPUTS = [
    "User intent, scope, and expected outcomes.",
    "Technical constraints (stack, security, performance, deadlines).",
    "Relevant files, systems, and integration boundaries.",
]

DEFAULT_OUTPUT_CONTRACT = (
    "Return: architecture/plan, concrete changes, validation evidence, risks, and next steps."
)

AGENT_TYPE_DEFAULT_WORKFLOW = {
    "orchestrator": [
        "Decompose the request into clear workstreams and dependencies.",
        "Select the minimum skill set needed for each workstream.",
        "Sequence or parallelize execution based on risk and coupling.",
        "Integrate outputs, resolve conflicts, and verify end-to-end quality.",
    ],
    "builder": [
        "Define architecture and implementation boundaries.",
        "Implement incrementally with strict quality gates.",
        "Validate behavior, security, and performance before finalizing.",
    ],
    "reviewer": [
        "Inspect changes with risk-first prioritization.",
        "Map findings to severity and reproducibility.",
        "Provide concrete remediations and verification steps.",
    ],
    "debugger": [
        "Reproduce and isolate the failure path.",
        "Trace root cause across code, config, data, and runtime.",
        "Apply minimal fix and validate against regressions.",
    ],
    "specialist": [
        "Establish domain constraints and success criteria.",
        "Execute domain-specific workflow with evidence-backed decisions.",
        "Deliver implementation and validation aligned with constraints.",
    ],
}

AGENT_TYPE_DEFAULT_GUARDRAILS = {
    "orchestrator": [
        "Never parallelize tasks that share mutable state without coordination.",
        "Never lose critical context when handing off between workstreams.",
        "Always validate integration points after composing outputs.",
    ],
    "builder": [
        "Never ship untyped or weakly validated interfaces in production paths.",
        "Never ignore security basics for implementation speed.",
        "Always keep changes testable, reviewable, and reversible.",
    ],
    "reviewer": [
        "Never prioritize style nits over correctness and security defects.",
        "Never report findings without actionable remediation.",
        "Always include residual risk and testing gaps.",
    ],
    "debugger": [
        "Never claim root cause without reproducible evidence.",
        "Never mask symptoms with temporary patches as final fixes.",
        "Always confirm fix behavior in the original failing scenario.",
    ],
    "specialist": [
        "Never bypass domain constraints or compliance requirements.",
        "Never present assumptions as verified facts.",
        "Always document tradeoffs and operational implications.",
    ],
}

AGENT_TYPE_SKILL_HINTS = {
    "orchestrator": ["plan", "architect", "review", "security", "verify", "tdd"],
    "builder": ["fullstack", "frontend", "backend", "next", "react", "api", "db"],
    "reviewer": ["review", "security", "test", "quality", "lint", "types"],
    "debugger": ["debug", "investigation", "verification", "logs", "runtime"],
    "specialist": ["domain", "expert", "pattern"],
}

TOKEN_ALIASES = {
    "seguridad": "security",
    "arquitectura": "architecture",
    "diseno": "design",
    "disenar": "design",
    "pruebas": "testing",
    "test": "testing",
    "depuracion": "debug",
    "rendimiento": "performance",
    "datos": "data",
    "infraestructura": "infra",
    "orquesta": "orchestrate",
    "orquestador": "orchestrator",
    "autenticacion": "auth",
    "autorizacion": "authorization",
}

PRIORITY_TOKENS = {
    "fullstack",
    "frontend",
    "backend",
    "orchestrator",
    "architect",
    "review",
    "verify",
    "verification",
    "scan",
    "quality",
    "testing",
    "tdd",
    "debug",
    "security",
}

LOGIC_FOUNDATION_ORDER = [
    "logic-propositional-reasoning",
    "logic-predicate-quantifiers",
    "logic-proof-strategies",
    "set-theory-foundations",
    "relations-functions-foundations",
    "discrete-structures-core",
    "complexity-analysis-foundations",
    "algorithm-correctness-invariants",
    "recursion-induction-foundations",
    "type-systems-foundations",
    "logic-of-programs-hoare",
    "testing-verification-foundations",
    "debugging-causal-reasoning-foundations",
    "distributed-systems-consistency-foundations",
    "security-threat-modeling-foundations",
]

LOGIC_FOUNDATION_PACKS: dict[str, list[str]] = {
    "none": [],
    "core": [
        "logic-propositional-reasoning",
        "algorithm-correctness-invariants",
        "testing-verification-foundations",
    ],
    "standard": [
        "logic-propositional-reasoning",
        "logic-proof-strategies",
        "complexity-analysis-foundations",
        "algorithm-correctness-invariants",
        "type-systems-foundations",
        "testing-verification-foundations",
        "debugging-causal-reasoning-foundations",
    ],
    "max": LOGIC_FOUNDATION_ORDER,
}


@dataclass(frozen=True)
class InstallTarget:
    name: str
    directory: Path


@dataclass(frozen=True)
class SkillMatch:
    name: str
    score: int
    tokens: tuple[str, ...]


def slugify(name: str) -> str:
    lowered = name.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    lowered = re.sub(r"-{2,}", "-", lowered).strip("-")
    if not lowered:
        raise ValueError("Agent name produced an empty slug. Use letters or numbers.")
    return lowered


def title_case_from_name(name: str) -> str:
    parts = re.split(r"[\s\-_]+", name.strip())
    parts = [part for part in parts if part]
    if not parts:
        return "Untitled Agent"
    return " ".join(part.capitalize() for part in parts)


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def remove_path(path: Path, dry_run: bool) -> None:
    if not path_exists(path):
        return
    if dry_run:
        print(f"[dry-run] remove {path}")
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)


def ensure_dir(path: Path, dry_run: bool) -> None:
    if path_exists(path):
        return
    if dry_run:
        print(f"[dry-run] mkdir -p {path}")
        return
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] write {path}")
        return
    path.write_text(content, encoding="utf-8")


def tokenize(text: str) -> set[str]:
    ascii_text = (
        unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    )
    raw_tokens = [part for part in re.split(r"[^a-z0-9]+", ascii_text.lower()) if part]
    normalized: set[str] = set()
    for token in raw_tokens:
        normalized.add(TOKEN_ALIASES.get(token, token))
    return normalized


def discover_skills(skill_sources: list[str]) -> list[str]:
    found: dict[str, None] = {}
    for raw in skill_sources:
        root = Path(raw).expanduser()
        if not root.exists() or not root.is_dir():
            continue
        for candidate in sorted(root.iterdir()):
            if not candidate.is_dir():
                continue
            if (candidate / "SKILL.md").exists() or (candidate / "skill.meta.json").exists():
                found[candidate.name] = None
    return list(found.keys())


def rank_skills(
    available_skills: list[str],
    context_tokens: set[str],
    hint_tokens: set[str],
    max_auto_skills: int,
) -> list[SkillMatch]:
    context_hint_tokens = hint_tokens & context_tokens
    matches: list[SkillMatch] = []
    for skill in available_skills:
        skill_tokens = tokenize(skill.replace("/", "-"))
        overlap = sorted(skill_tokens & context_tokens)
        score = len(overlap) * 4
        for hint in context_hint_tokens:
            if hint in skill_tokens or any(hint in tok for tok in skill_tokens):
                score += 2
        score += len(skill_tokens & PRIORITY_TOKENS)
        if score >= 4:
            matches.append(SkillMatch(name=skill, score=score, tokens=tuple(overlap)))
    matches.sort(key=lambda item: (-item.score, item.name))
    return matches[:max_auto_skills]


def dedupe_preserve(items: Iterable[str]) -> list[str]:
    seen: dict[str, None] = {}
    for item in items:
        if item not in seen:
            seen[item] = None
    return list(seen.keys())


def cap_list(items: list[str], maximum: int) -> list[str]:
    if maximum <= 0:
        return []
    return items[:maximum]


def pick_logic_foundation_skills(mode: str, available_skills: list[str]) -> list[str]:
    desired = LOGIC_FOUNDATION_PACKS.get(mode, [])
    available = set(available_skills)
    return [skill for skill in desired if skill in available]


def select_skills(
    explicit_skills: list[str],
    skill_mode: str,
    auto_matches: list[SkillMatch],
    fallback_skills: list[str],
) -> list[str]:
    auto_names = [match.name for match in auto_matches]
    if skill_mode == "explicit":
        selected = explicit_skills
    elif skill_mode == "auto":
        selected = auto_names
    else:
        selected = explicit_skills + auto_names

    selected = dedupe_preserve(selected)
    if selected:
        return selected
    return dedupe_preserve(fallback_skills)


def infer_fallback_skills(
    available_skills: list[str],
    agent_type: str,
    fallback_limit: int = 4,
) -> list[str]:
    hints = AGENT_TYPE_SKILL_HINTS[agent_type]
    ranked: list[tuple[int, str]] = []
    for skill in available_skills:
        skill_tokens = tokenize(skill)
        score = 0
        for hint in hints:
            if hint in skill_tokens or any(hint in token for token in skill_tokens):
                score += 1
        if score > 0:
            ranked.append((score, skill))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [name for _, name in ranked[:fallback_limit]]


def build_agent_md(
    slug: str,
    title: str,
    description: str,
    version: str,
    author: str,
    agent_type: str,
    skill_mode: str,
    logic_foundation_mode: str,
    selected_skills: list[str],
    logic_foundation_skills: list[str],
    input_items: list[str],
    workflow_steps: list[str],
    guardrail_items: list[str],
    output_contract: str,
) -> str:
    selected_skills_yaml = "\n".join(f"  - {yaml_quote(skill)}" for skill in selected_skills)
    input_bullets = "\n".join(f"- {item}" for item in input_items)
    workflow_steps_list = "\n".join(f"{idx + 1}. {item}" for idx, item in enumerate(workflow_steps))
    guardrail_bullets = "\n".join(f"- {item}" for item in guardrail_items)
    skill_profile_bullets = (
        "\n".join(f"- `{skill}`" for skill in selected_skills)
        if selected_skills
        else "- No skills selected. Add skills or enable auto selection."
    )
    logic_bullets = (
        "\n".join(f"- `{skill}`" for skill in logic_foundation_skills)
        if logic_foundation_skills
        else "- None"
    )

    return f"""---
name: {yaml_quote(slug)}
description: {yaml_quote(description)}
version: {yaml_quote(version)}
compatibility:
  - claude-code
  - codex
owner: {yaml_quote(author)}
agent_type: {yaml_quote(agent_type)}
skill_mode: {yaml_quote(skill_mode)}
logic_foundation_mode: {yaml_quote(logic_foundation_mode)}
skill_profile:
{selected_skills_yaml if selected_skills_yaml else "  - \"\""}
---

# {title} Agent

## Mission
{description}

## Inputs expected
{input_bullets}

## Skill Bootstrap Protocol
1. Parse the task into capabilities and constraints before writing code.
2. Select the minimum required skills from the skill profile.
3. Extract each selected skill's workflow and guardrails.
4. Build one merged execution plan that preserves all critical constraints.
5. Run a final consistency check to avoid conflicts between selected skills.

## Skill Profile
{skill_profile_bullets}

## Logical Reliability Core
{logic_bullets}

## Reasoning Control Protocol
1. Build an assumption ledger before implementation.
2. Convert assumptions into verifiable checks or tests.
3. Search for counterexamples and conflicting constraints.
4. Finalize only when checks are coherent and reproducible.

## Workflow
{workflow_steps_list}

## Output contract
{output_contract}

## Guardrails
{guardrail_bullets}

## Escalation policy
- Escalate when requirements conflict or have hidden tradeoffs.
- Escalate before destructive actions or irreversible migrations.
- Escalate when verification cannot be completed in the current environment.
"""


def build_readme_md(slug: str, title: str, description: str) -> str:
    return f"""# {title}

This folder contains a universal agent compatible with:

- Claude Code (`~/.claude/agents/{slug}.md`)
- Codex (`~/.codex/agents/{slug}.md`)

## Purpose
{description}

## Files
- `AGENT.md`: canonical behavior and skill bootstrap protocol
- `references/skill-index.md`: selected/auto skills + logic foundation details
- `examples/prompts.md`: prompt recipes to invoke this agent
- `agent.meta.json`: metadata for portability/versioning

## Usage
1. Mention this agent and provide task scope plus constraints.
2. Ask for architecture, implementation, and validation in one flow.
3. Let the agent compose skills using its `Skill Bootstrap Protocol`.
"""


def build_example_prompts(agent_slug: str) -> str:
    return f"""# Example Prompts for `{agent_slug}`

- "Use `{agent_slug}` and run it end-to-end with its skill bootstrap protocol."
- "Apply `{agent_slug}`. Show selected skills first, then implementation plan and execution."
- "Run `{agent_slug}` and include validation evidence plus residual risks."
"""


def build_meta_json(
    slug: str,
    title: str,
    description: str,
    version: str,
    agent_type: str,
    skill_mode: str,
    logic_foundation_mode: str,
    tags: list[str],
    selected_skills: list[str],
    logic_foundation_skills: list[str],
) -> str:
    payload = {
        "name": slug,
        "title": title,
        "description": description,
        "version": version,
        "agent_type": agent_type,
        "skill_mode": skill_mode,
        "logic_foundation_mode": logic_foundation_mode,
        "tags": tags,
        "compatibility": ["claude-code", "codex"],
        "entrypoint": "AGENT.md",
        "skills": selected_skills,
        "logic_foundation_skills": logic_foundation_skills,
    }
    return json.dumps(payload, indent=2) + "\n"


def build_skill_index_md(
    skill_mode: str,
    logic_foundation_mode: str,
    selected_skills: list[str],
    logic_foundation_skills: list[str],
    explicit_skills: list[str],
    auto_matches: list[SkillMatch],
    available_skills_count: int,
    skill_sources: list[str],
) -> str:
    lines: list[str] = []
    lines.append("# Skill Index")
    lines.append("")
    lines.append(f"- Available skills discovered: {available_skills_count}")
    lines.append(f"- Skill mode: `{skill_mode}`")
    lines.append(f"- Logic foundation mode: `{logic_foundation_mode}`")
    lines.append("- Skill source roots:")
    for source in skill_sources:
        lines.append(f"  - `{source}`")
    lines.append("")

    lines.append("## Selected Skills")
    if selected_skills:
        for skill in selected_skills:
            lines.append(f"- `{skill}`")
    else:
        lines.append("- None selected.")
    lines.append("")

    lines.append("## Explicit Skills")
    if explicit_skills:
        for skill in explicit_skills:
            lines.append(f"- `{skill}`")
    else:
        lines.append("- None.")
    lines.append("")

    lines.append("## Logic Foundation Skills")
    if logic_foundation_skills:
        for skill in logic_foundation_skills:
            lines.append(f"- `{skill}`")
    else:
        lines.append("- None.")
    lines.append("")

    lines.append("## Auto Matches")
    if auto_matches:
        for match in auto_matches:
            overlap = ", ".join(match.tokens) if match.tokens else "no direct overlap"
            lines.append(f"- `{match.name}` (score={match.score}, overlap={overlap})")
    else:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines) + "\n"


def create_agent_scaffold(
    agent_dir: Path,
    slug: str,
    title: str,
    description: str,
    version: str,
    author: str,
    agent_type: str,
    skill_mode: str,
    logic_foundation_mode: str,
    tags: list[str],
    selected_skills: list[str],
    logic_foundation_skills: list[str],
    explicit_skills: list[str],
    auto_matches: list[SkillMatch],
    available_skills_count: int,
    skill_sources: list[str],
    input_items: list[str],
    workflow_steps: list[str],
    guardrail_items: list[str],
    output_contract: str,
    overwrite: bool,
    dry_run: bool,
) -> None:
    if path_exists(agent_dir):
        if not overwrite:
            raise FileExistsError(
                f"Agent directory already exists: {agent_dir}. Use --overwrite to replace it."
            )
        remove_path(agent_dir, dry_run=dry_run)

    ensure_dir(agent_dir, dry_run=dry_run)
    ensure_dir(agent_dir / "references", dry_run=dry_run)
    ensure_dir(agent_dir / "examples", dry_run=dry_run)
    ensure_dir(agent_dir / "scripts", dry_run=dry_run)
    ensure_dir(agent_dir / "assets", dry_run=dry_run)

    write_text(
        agent_dir / "AGENT.md",
        build_agent_md(
            slug=slug,
            title=title,
            description=description,
            version=version,
            author=author,
            agent_type=agent_type,
            skill_mode=skill_mode,
            logic_foundation_mode=logic_foundation_mode,
            selected_skills=selected_skills,
            logic_foundation_skills=logic_foundation_skills,
            input_items=input_items,
            workflow_steps=workflow_steps,
            guardrail_items=guardrail_items,
            output_contract=output_contract,
        ),
        dry_run=dry_run,
    )
    write_text(agent_dir / "README.md", build_readme_md(slug, title, description), dry_run=dry_run)
    write_text(agent_dir / "examples" / "prompts.md", build_example_prompts(slug), dry_run=dry_run)
    write_text(
        agent_dir / "references" / "skill-index.md",
        build_skill_index_md(
            skill_mode=skill_mode,
            logic_foundation_mode=logic_foundation_mode,
            selected_skills=selected_skills,
            logic_foundation_skills=logic_foundation_skills,
            explicit_skills=explicit_skills,
            auto_matches=auto_matches,
            available_skills_count=available_skills_count,
            skill_sources=skill_sources,
        ),
        dry_run=dry_run,
    )
    write_text(
        agent_dir / "agent.meta.json",
        build_meta_json(
            slug=slug,
            title=title,
            description=description,
            version=version,
            agent_type=agent_type,
            skill_mode=skill_mode,
            logic_foundation_mode=logic_foundation_mode,
            tags=tags,
            selected_skills=selected_skills,
            logic_foundation_skills=logic_foundation_skills,
        ),
        dry_run=dry_run,
    )
    write_text(agent_dir / "scripts" / ".gitkeep", "", dry_run=dry_run)
    write_text(agent_dir / "assets" / ".gitkeep", "", dry_run=dry_run)


def install_agent_entry(
    source_agent_md: Path,
    destination_file: Path,
    method: str,
    overwrite: bool,
    dry_run: bool,
) -> None:
    if path_exists(destination_file):
        if not overwrite:
            raise FileExistsError(
                f"Destination exists: {destination_file}. Use --overwrite to replace it."
            )
        remove_path(destination_file, dry_run=dry_run)

    ensure_dir(destination_file.parent, dry_run=dry_run)

    if dry_run:
        print(f"[dry-run] install {source_agent_md} -> {destination_file} ({method})")
        return

    if method == "symlink":
        os.symlink(source_agent_md.resolve(), destination_file)
        return

    shutil.copy2(source_agent_md, destination_file)


def parse_targets(install_target: str, claude_dir: Path, codex_dir: Path) -> list[InstallTarget]:
    if install_target == "none":
        return []
    if install_target == "claude":
        return [InstallTarget("claude", claude_dir)]
    if install_target == "codex":
        return [InstallTarget("codex", codex_dir)]
    return [InstallTarget("claude", claude_dir), InstallTarget("codex", codex_dir)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a universal agent scaffold for Claude Code and Codex, with skill bootstrap support."
    )
    parser.add_argument("--name", required=True, help="Agent name, e.g. 'fullstack orchestrator'.")
    parser.add_argument("--description", required=True, help="Short agent description.")
    parser.add_argument("--agent-type", choices=["orchestrator", "builder", "reviewer", "debugger", "specialist"], default="orchestrator")
    parser.add_argument("--version", default="1.0.0", help="Agent version.")
    parser.add_argument("--author", default=os.environ.get("USER", "unknown"), help="Agent owner.")
    parser.add_argument("--agent-root", default="agents", help="Local directory where canonical agent folder is created.")
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Tag for discovery/categorization. Repeatable.",
    )

    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Explicit skill to include. Repeatable.",
    )
    parser.add_argument(
        "--skill-mode",
        choices=["explicit", "auto", "hybrid"],
        default="hybrid",
        help="How to compose skills for the generated agent.",
    )
    parser.add_argument(
        "--skill-source",
        action="append",
        default=[],
        help="Skill source directory. Repeatable. Defaults to local + Claude + Codex skill dirs.",
    )
    parser.add_argument(
        "--max-auto-skills",
        type=int,
        default=6,
        help="Maximum number of auto-selected skills.",
    )
    parser.add_argument(
        "--max-profile-skills",
        type=int,
        default=12,
        help="Maximum number of total skills in the final agent skill profile.",
    )
    parser.add_argument(
        "--logic-foundation",
        choices=["none", "core", "standard", "max"],
        default="standard",
        help="Attach a logic-focused foundation pack to the agent skill profile.",
    )

    parser.add_argument("--input", action="append", default=[], help="Input requirement bullet. Repeatable.")
    parser.add_argument("--workflow-step", action="append", default=[], help="Workflow step. Repeatable.")
    parser.add_argument("--guardrail", action="append", default=[], help="Guardrail bullet. Repeatable.")
    parser.add_argument("--output-contract", default=DEFAULT_OUTPUT_CONTRACT, help="Agent output contract.")

    parser.add_argument("--install-target", choices=["both", "claude", "codex", "none"], default="both")
    parser.add_argument("--install-method", choices=["symlink", "copy"], default="symlink")
    parser.add_argument("--claude-dir", default="~/.claude/agents", help="Claude agents directory.")
    parser.add_argument("--codex-dir", default="~/.codex/agents", help="Codex agents directory.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing agent directories/files.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if explicit skills are missing from discovered skill sources.",
    )
    args = parser.parse_args()

    slug = slugify(args.name)
    title = title_case_from_name(args.name)

    agent_root = Path(args.agent_root).expanduser().resolve()
    agent_dir = agent_root / slug
    source_agent_md = agent_dir / "AGENT.md"

    skill_sources = args.skill_source if args.skill_source else DEFAULT_SKILL_SOURCES
    available_skills = discover_skills(skill_sources)

    context = " ".join([args.name, args.description, args.agent_type, " ".join(args.skill)])
    context_tokens = tokenize(context)
    hint_tokens = set(AGENT_TYPE_SKILL_HINTS[args.agent_type])
    auto_matches = rank_skills(
        available_skills=available_skills,
        context_tokens=context_tokens,
        hint_tokens=hint_tokens,
        max_auto_skills=max(args.max_auto_skills, 0),
    )

    fallback_skills = infer_fallback_skills(available_skills, args.agent_type)
    selected_skills = select_skills(
        explicit_skills=args.skill,
        skill_mode=args.skill_mode,
        auto_matches=auto_matches,
        fallback_skills=fallback_skills,
    )
    logic_foundation_skills = pick_logic_foundation_skills(
        mode=args.logic_foundation,
        available_skills=available_skills,
    )
    selected_skills = dedupe_preserve(selected_skills + logic_foundation_skills)
    selected_skills = cap_list(selected_skills, args.max_profile_skills)

    missing_explicit: list[str] = []
    for skill in args.skill:
        if skill not in available_skills:
            missing_explicit.append(skill)
            print(
                f"Warning: explicit skill '{skill}' was not discovered in skill sources.",
                file=sys.stderr,
            )
    if args.strict and missing_explicit:
        print(
            "Error: strict mode enabled and explicit skills are missing: "
            + ", ".join(missing_explicit),
            file=sys.stderr,
        )
        return 2

    input_items = args.input if args.input else DEFAULT_INPUTS
    workflow_steps = (
        args.workflow_step
        if args.workflow_step
        else AGENT_TYPE_DEFAULT_WORKFLOW[args.agent_type]
    )
    guardrail_items = (
        args.guardrail
        if args.guardrail
        else AGENT_TYPE_DEFAULT_GUARDRAILS[args.agent_type]
    )

    print(f"Creating agent '{slug}' in {agent_dir}")
    create_agent_scaffold(
        agent_dir=agent_dir,
        slug=slug,
        title=title,
        description=args.description,
        version=args.version,
        author=args.author,
        agent_type=args.agent_type,
        skill_mode=args.skill_mode,
        logic_foundation_mode=args.logic_foundation,
        tags=dedupe_preserve(args.tag),
        selected_skills=selected_skills,
        logic_foundation_skills=logic_foundation_skills,
        explicit_skills=args.skill,
        auto_matches=auto_matches,
        available_skills_count=len(available_skills),
        skill_sources=skill_sources,
        input_items=input_items,
        workflow_steps=workflow_steps,
        guardrail_items=guardrail_items,
        output_contract=args.output_contract,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )

    targets = parse_targets(
        install_target=args.install_target,
        claude_dir=Path(args.claude_dir).expanduser(),
        codex_dir=Path(args.codex_dir).expanduser(),
    )
    destination_name = f"{slug}.md"
    for target in targets:
        destination_file = target.directory / destination_name
        try:
            install_agent_entry(
                source_agent_md=source_agent_md,
                destination_file=destination_file,
                method=args.install_method,
                overwrite=args.overwrite,
                dry_run=args.dry_run,
            )
            print(f"Installed in {target.name}: {destination_file}")
        except PermissionError as exc:
            print(
                f"Warning: could not install in {target.name} ({target.directory}): {exc}",
                file=sys.stderr,
            )
        except FileExistsError as exc:
            print(f"Warning: {exc}", file=sys.stderr)

    print("")
    print("Done.")
    print(f"Canonical agent folder: {agent_dir}")
    if args.install_target == "none":
        print("No installation target selected. Use --install-target both to install in Claude and Codex.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
