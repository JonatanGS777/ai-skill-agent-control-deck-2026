#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_WHEN = [
    "When the user asks for a repeatable workflow in this domain.",
    "When a specialized checklist improves speed or quality.",
]

DEFAULT_INPUTS = [
    "Task objective and expected output.",
    "Relevant files, paths, or system constraints.",
    "Any non-negotiable requirements (security, style, deadlines).",
]

DEFAULT_STEPS = [
    "Understand scope, assumptions, and risks.",
    "Execute the workflow in a deterministic order.",
    "Verify outcomes and report any limitations clearly.",
]

DEFAULT_GUARDRAILS = [
    "Never fabricate facts, outputs, or tool results.",
    "Ask for confirmation before destructive operations.",
    "Prefer minimal, reversible changes when uncertain.",
]

DEFAULT_OUTPUT_FORMAT = (
    "Provide results in this order: key outcome, concrete changes, validation status, next steps."
)

DEFAULT_DOMAIN = "general"
DEFAULT_QUALITY_TIER = "advanced"

MIN_DESCRIPTION_LENGTH = 24
MIN_ITEM_LENGTH = 10
MIN_WHEN_ITEMS = 2
MIN_INPUT_ITEMS = 2
MIN_STEPS = 3
MIN_GUARDRAILS = 2


@dataclass(frozen=True)
class InstallTarget:
    name: str
    directory: Path


def slugify(name: str) -> str:
    lowered = name.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    lowered = re.sub(r"-{2,}", "-", lowered).strip("-")
    if not lowered:
        raise ValueError("Skill name produced an empty slug. Use letters or numbers.")
    return lowered


def title_case_from_name(name: str) -> str:
    parts = re.split(r"[\s\-_]+", name.strip())
    parts = [part for part in parts if part]
    if not parts:
        return "Untitled Skill"
    return " ".join(part.capitalize() for part in parts)


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def normalize_items(items: list[str]) -> list[str]:
    seen: dict[str, None] = {}
    for item in items:
        cleaned = re.sub(r"\s+", " ", item.strip())
        if cleaned and cleaned not in seen:
            seen[cleaned] = None
    return list(seen.keys())


def validate_payload(
    description: str,
    when_items: list[str],
    input_items: list[str],
    step_items: list[str],
    guardrail_items: list[str],
    output_format: str,
    strict: bool,
) -> None:
    if len(description.strip()) < MIN_DESCRIPTION_LENGTH:
        raise ValueError(
            f"Description is too short. Minimum length is {MIN_DESCRIPTION_LENGTH} characters."
        )
    if len(output_format.strip()) < MIN_ITEM_LENGTH:
        raise ValueError("Output contract is too short. Make it explicit and actionable.")

    checks = [
        ("when items", when_items, MIN_WHEN_ITEMS),
        ("input items", input_items, MIN_INPUT_ITEMS),
        ("workflow steps", step_items, MIN_STEPS),
        ("guardrails", guardrail_items, MIN_GUARDRAILS),
    ]
    for label, items, minimum in checks:
        if len(items) < minimum:
            raise ValueError(f"Not enough {label}. Minimum required is {minimum}.")

    if not strict:
        return

    for label, items, _ in checks:
        for item in items:
            if len(item) < MIN_ITEM_LENGTH:
                raise ValueError(
                    f"Strict mode: {label} item is too short ('{item}')."
                )


def build_skill_md(
    slug: str,
    title: str,
    description: str,
    version: str,
    author: str,
    domain: str,
    quality_tier: str,
    tags: list[str],
    foundation_skills: list[str],
    when_items: list[str],
    input_items: list[str],
    step_items: list[str],
    guardrail_items: list[str],
    output_format: str,
) -> str:
    def bullets(items: Iterable[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

    workflow = "\n".join(f"{idx + 1}. {item}" for idx, item in enumerate(step_items))
    tags_yaml = "\n".join(f"  - {yaml_quote(tag)}" for tag in tags)
    foundations_yaml = "\n".join(f"  - {yaml_quote(skill)}" for skill in foundation_skills)
    tags_section = (
        "tags:\n" + tags_yaml + "\n"
        if tags_yaml
        else "tags:\n  - \"\"\n"
    )
    foundations_section = (
        "\n## Foundations\n"
        + "\n".join(f"- `{skill}`" for skill in foundation_skills)
        + "\n"
        if foundation_skills
        else ""
    )

    return f"""---
name: {yaml_quote(slug)}
description: {yaml_quote(description)}
version: {yaml_quote(version)}
domain: {yaml_quote(domain)}
quality_tier: {yaml_quote(quality_tier)}
compatibility:
  - claude-code
  - codex
owner: {yaml_quote(author)}
{tags_section}foundation_skills:
{foundations_yaml if foundations_yaml else "  - \"\""}
---

# {title} Skill

## Mission
{description}

## When to use
{bullets(when_items)}

## Inputs expected
{bullets(input_items)}

## Workflow
{workflow}

## Output contract
{output_format}

## Guardrails
{bullets(guardrail_items)}
{foundations_section}

## Logical reliability checklist
- Assumptions are explicit and separated from verified facts.
- The solution path is justified with clear reasoning steps.
- Edge cases and contradiction checks are included.
- Output is testable, auditable, and reversible when possible.

## Example prompts
- "Apply the {slug} skill to handle this task end-to-end."
- "Run {slug} and produce a production-ready output with validation notes."
"""


def build_readme_md(slug: str, title: str, description: str) -> str:
    return f"""# {title}

This folder contains a universal skill designed to work in both:

- Claude Code (`~/.claude/skills/{slug}`)
- Codex (`~/.codex/skills/{slug}`)

## Purpose
{description}

## Files
- `SKILL.md`: main behavior and rules
- `references/`: optional docs and examples
- `references/quality-gates.md`: logical/quality acceptance criteria
- `scripts/`: optional automation helpers
- `assets/`: optional static resources
- `skill.meta.json`: metadata for portability/versioning

## Usage
1. Install the skill in Claude/Codex (symlink or copy).
2. Trigger it by name from your prompt.
3. Iterate on `SKILL.md` based on real outcomes.
"""


def build_example_prompts(slug: str) -> str:
    return f"""# Example Prompts for `{slug}`

- "Use `{slug}` for this task and follow its workflow exactly."
- "Apply `{slug}` and return findings first, then implementation steps."
- "Run `{slug}` with strict validation and call out residual risks."
"""


def build_meta_json(
    slug: str,
    title: str,
    description: str,
    version: str,
    domain: str,
    quality_tier: str,
    tags: list[str],
    foundation_skills: list[str],
) -> str:
    payload = {
        "name": slug,
        "title": title,
        "description": description,
        "version": version,
        "domain": domain,
        "quality_tier": quality_tier,
        "tags": tags,
        "foundation_skills": foundation_skills,
        "compatibility": ["claude-code", "codex"],
        "entrypoint": "SKILL.md",
    }
    return json.dumps(payload, indent=2) + "\n"


def build_quality_gates_md(
    slug: str,
    domain: str,
    quality_tier: str,
    foundation_skills: list[str],
) -> str:
    foundations = "\n".join(f"- `{skill}`" for skill in foundation_skills) or "- None"
    return f"""# Quality Gates for `{slug}`

- Domain: `{domain}`
- Quality tier: `{quality_tier}`

## Required checks
1. Logical consistency: no contradiction between assumptions and output.
2. Verifiability: output can be validated through explicit checks/tests.
3. Traceability: key decisions are justified and reproducible.
4. Safety: no destructive action without explicit user confirmation.

## Foundation dependencies
{foundations}
"""


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


def create_skill_scaffold(
    skill_dir: Path,
    slug: str,
    title: str,
    description: str,
    version: str,
    author: str,
    domain: str,
    quality_tier: str,
    tags: list[str],
    foundation_skills: list[str],
    when_items: list[str],
    input_items: list[str],
    step_items: list[str],
    guardrail_items: list[str],
    output_format: str,
    overwrite: bool,
    dry_run: bool,
) -> None:
    if path_exists(skill_dir):
        if not overwrite:
            raise FileExistsError(
                f"Skill directory already exists: {skill_dir}. Use --overwrite to replace it."
            )
        remove_path(skill_dir, dry_run=dry_run)

    ensure_dir(skill_dir, dry_run=dry_run)
    ensure_dir(skill_dir / "assets", dry_run=dry_run)
    ensure_dir(skill_dir / "scripts", dry_run=dry_run)
    ensure_dir(skill_dir / "references", dry_run=dry_run)
    ensure_dir(skill_dir / "examples", dry_run=dry_run)

    write_text(
        skill_dir / "SKILL.md",
        build_skill_md(
            slug=slug,
            title=title,
            description=description,
            version=version,
            author=author,
            domain=domain,
            quality_tier=quality_tier,
            tags=tags,
            foundation_skills=foundation_skills,
            when_items=when_items,
            input_items=input_items,
            step_items=step_items,
            guardrail_items=guardrail_items,
            output_format=output_format,
        ),
        dry_run=dry_run,
    )
    write_text(skill_dir / "README.md", build_readme_md(slug, title, description), dry_run=dry_run)
    write_text(skill_dir / "examples" / "prompts.md", build_example_prompts(slug), dry_run=dry_run)
    write_text(
        skill_dir / "skill.meta.json",
        build_meta_json(
            slug,
            title,
            description,
            version,
            domain,
            quality_tier,
            tags,
            foundation_skills,
        ),
        dry_run=dry_run,
    )
    write_text(
        skill_dir / "references" / "quality-gates.md",
        build_quality_gates_md(
            slug=slug,
            domain=domain,
            quality_tier=quality_tier,
            foundation_skills=foundation_skills,
        ),
        dry_run=dry_run,
    )
    write_text(skill_dir / "assets" / ".gitkeep", "", dry_run=dry_run)
    write_text(skill_dir / "scripts" / ".gitkeep", "", dry_run=dry_run)
    write_text(skill_dir / "references" / ".gitkeep", "", dry_run=dry_run)


def install_skill(
    source_skill_dir: Path,
    target: InstallTarget,
    method: str,
    overwrite: bool,
    dry_run: bool,
) -> None:
    destination = target.directory / source_skill_dir.name
    if path_exists(destination):
        if not overwrite:
            raise FileExistsError(
                f"Destination exists for {target.name}: {destination}. Use --overwrite to replace it."
            )
        remove_path(destination, dry_run=dry_run)

    ensure_dir(target.directory, dry_run=dry_run)

    if dry_run:
        print(f"[dry-run] install {source_skill_dir} -> {destination} ({method})")
        return

    if method == "symlink":
        os.symlink(source_skill_dir.resolve(), destination, target_is_directory=True)
        return

    shutil.copytree(source_skill_dir, destination)


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
        description="Create a universal skill scaffold for Claude Code and Codex."
    )
    parser.add_argument("--name", required=True, help="Skill name, e.g. 'api reviewer'.")
    parser.add_argument("--description", required=True, help="Short skill description.")
    parser.add_argument("--version", default="1.0.0", help="Skill version.")
    parser.add_argument("--author", default=os.environ.get("USER", "unknown"), help="Skill owner.")
    parser.add_argument("--domain", default=DEFAULT_DOMAIN, help="Skill domain, e.g. frontend, backend, math.")
    parser.add_argument(
        "--quality-tier",
        choices=["core", "advanced", "expert"],
        default=DEFAULT_QUALITY_TIER,
        help="Quality expectation tier for this skill.",
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Tag for discovery/categorization. Repeatable.",
    )
    parser.add_argument(
        "--foundation-skill",
        action="append",
        default=[],
        help="Foundational skill dependency. Repeatable.",
    )
    parser.add_argument(
        "--skill-root",
        default="skills",
        help="Local directory where the canonical skill folder will be created.",
    )
    parser.add_argument(
        "--install-target",
        choices=["both", "claude", "codex", "none"],
        default="both",
        help="Where to install the skill after creation.",
    )
    parser.add_argument(
        "--install-method",
        choices=["symlink", "copy"],
        default="symlink",
        help="Install by symlink (recommended) or copy.",
    )
    parser.add_argument(
        "--claude-dir",
        default="~/.claude/skills",
        help="Claude skills directory.",
    )
    parser.add_argument(
        "--codex-dir",
        default="~/.codex/skills",
        help="Codex skills directory.",
    )
    parser.add_argument(
        "--when",
        action="append",
        default=[],
        help="Add a 'when to use' bullet. Repeatable.",
    )
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        help="Add an input requirement bullet. Repeatable.",
    )
    parser.add_argument(
        "--step",
        action="append",
        default=[],
        help="Add a workflow step. Repeatable. Minimum 3.",
    )
    parser.add_argument(
        "--guardrail",
        action="append",
        default=[],
        help="Add a guardrail bullet. Repeatable.",
    )
    parser.add_argument(
        "--output-format",
        default=DEFAULT_OUTPUT_FORMAT,
        help="Output contract sentence for SKILL.md.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing skill directories if they already exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without writing files.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict quality validation for payload fields.",
    )
    args = parser.parse_args()

    when_items = normalize_items(args.when if args.when else DEFAULT_WHEN)
    input_items = normalize_items(args.input if args.input else DEFAULT_INPUTS)
    guardrail_items = normalize_items(args.guardrail if args.guardrail else DEFAULT_GUARDRAILS)
    step_items = normalize_items(args.step if args.step else DEFAULT_STEPS)
    tags = normalize_items(args.tag)
    foundation_skills = normalize_items(args.foundation_skill)
    if len(step_items) < 3:
        print("Error: provide at least 3 --step entries (or omit --step to use defaults).", file=sys.stderr)
        return 2

    try:
        validate_payload(
            description=args.description,
            when_items=when_items,
            input_items=input_items,
            step_items=step_items,
            guardrail_items=guardrail_items,
            output_format=args.output_format,
            strict=args.strict,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    slug = slugify(args.name)
    title = title_case_from_name(args.name)
    skill_root = Path(args.skill_root).expanduser().resolve()
    skill_dir = skill_root / slug

    claude_dir = Path(args.claude_dir).expanduser()
    codex_dir = Path(args.codex_dir).expanduser()
    targets = parse_targets(args.install_target, claude_dir, codex_dir)

    print(f"Creating skill '{slug}' in {skill_dir}")
    create_skill_scaffold(
        skill_dir=skill_dir,
        slug=slug,
        title=title,
        description=args.description,
        version=args.version,
        author=args.author,
        domain=args.domain,
        quality_tier=args.quality_tier,
        tags=tags,
        foundation_skills=foundation_skills,
        when_items=when_items,
        input_items=input_items,
        step_items=step_items,
        guardrail_items=guardrail_items,
        output_format=args.output_format,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )

    for target in targets:
        try:
            install_skill(
                source_skill_dir=skill_dir,
                target=target,
                method=args.install_method,
                overwrite=args.overwrite,
                dry_run=args.dry_run,
            )
            print(f"Installed in {target.name}: {target.directory / slug}")
        except PermissionError as exc:
            print(
                f"Warning: could not install in {target.name} ({target.directory}): {exc}",
                file=sys.stderr,
            )
        except FileExistsError as exc:
            print(f"Warning: {exc}", file=sys.stderr)

    print("")
    print("Done.")
    print(f"Canonical skill folder: {skill_dir}")
    if args.install_target == "none":
        print("No installation target selected. Use --install-target both to install in Claude and Codex.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
