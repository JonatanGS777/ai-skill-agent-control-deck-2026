#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


def slugify(text: str) -> str:
    lowered = text.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    lowered = re.sub(r"-{2,}", "-", lowered).strip("-")
    return lowered or "group"


def path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def safe_link(source: Path, destination: Path, overwrite: bool, dry_run: bool) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if path_exists(destination):
        if destination.is_symlink() and destination.resolve() == source.resolve():
            return "kept"
        if not overwrite:
            return "skipped"
        if dry_run:
            return "would-replace"
        destination.unlink()
    if dry_run:
        return "would-link"
    os.symlink(source.resolve(), destination)
    return "linked"


def discover_agents(agent_root: Path, includes: list[str]) -> list[tuple[str, Path]]:
    include_set = set(includes)
    agents: list[tuple[str, Path]] = []
    if not agent_root.exists():
        return agents
    for entry in sorted(agent_root.iterdir()):
        if not entry.is_dir():
            continue
        slug = entry.name
        if include_set and slug not in include_set:
            continue
        agent_md = entry / "AGENT.md"
        if agent_md.exists():
            agents.append((slug, agent_md))
    return agents


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install agent entrypoints and group aliases in Claude/Codex agent directories."
    )
    parser.add_argument("--agent-root", default="agents", help="Canonical agents directory in this repo.")
    parser.add_argument(
        "--group-name",
        default="CEO Jonatan Agent",
        help="Human group name used to build alias prefix.",
    )
    parser.add_argument(
        "--group-prefix",
        default=None,
        help="Optional explicit alias prefix. If omitted, derived from --group-name.",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Agent slug to include. Repeatable. If omitted, includes all agents in --agent-root.",
    )
    parser.add_argument("--claude-dir", default="~/.claude/agents", help="Claude agents directory.")
    parser.add_argument("--codex-dir", default="~/.codex/agents", help="Codex agents directory.")
    parser.add_argument(
        "--install-target",
        choices=["both", "claude", "codex"],
        default="both",
        help="Where to install aliases.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace existing files/symlinks if needed.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    agent_root = (base / args.agent_root).resolve()
    group_prefix = args.group_prefix or slugify(args.group_name)

    targets: list[tuple[str, Path]] = []
    if args.install_target in ("both", "claude"):
        targets.append(("claude", Path(args.claude_dir).expanduser()))
    if args.install_target in ("both", "codex"):
        targets.append(("codex", Path(args.codex_dir).expanduser()))

    agents = discover_agents(agent_root, args.include)
    if not agents:
        print("No agents found for installation.")
        return 1

    print(f"Installing {len(agents)} agents with group alias prefix: {group_prefix}")
    for target_name, target_dir in targets:
        print(f"Target: {target_name} -> {target_dir}")
        for slug, source_md in agents:
            canonical_dest = target_dir / f"{slug}.md"
            alias_dest = target_dir / f"{group_prefix}--{slug}.md"

            canonical_state = safe_link(source_md, canonical_dest, args.overwrite, args.dry_run)
            alias_state = safe_link(source_md, alias_dest, args.overwrite, args.dry_run)

            print(
                f"  - {slug}: canonical={canonical_state}, alias={alias_state}"
            )

    print("")
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
