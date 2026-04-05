#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def discover_slugs(agent_root: Path, suffix: str) -> list[str]:
    slugs: list[str] = []
    if not agent_root.exists():
        return slugs
    for entry in sorted(agent_root.iterdir()):
        if entry.is_dir() and entry.name.endswith(suffix) and (entry / "AGENT.md").exists():
            slugs.append(entry.name)
    return slugs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install a dedicated alias group for created exceptional agents."
    )
    parser.add_argument("--agent-root", default="agents", help="Canonical agents directory.")
    parser.add_argument(
        "--suffix",
        default="-exceptional-agent-2026",
        help="Agent slug suffix to include in the dedicated group.",
    )
    parser.add_argument(
        "--group-prefix",
        default="ceo-jonatan-creados",
        help="Alias group prefix for created agents.",
    )
    parser.add_argument(
        "--install-target",
        choices=["both", "claude", "codex"],
        default="both",
        help="Where to install aliases.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace existing links.")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions only.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    agent_root = (base / args.agent_root).resolve()
    includes = discover_slugs(agent_root, args.suffix)
    if not includes:
        print(
            f"No agents found with suffix '{args.suffix}' under {agent_root}",
            file=sys.stderr,
        )
        return 1

    cmd = [
        "python3",
        str(base / "scripts" / "install_agent_group_aliases.py"),
        "--agent-root",
        args.agent_root,
        "--group-prefix",
        args.group_prefix,
        "--install-target",
        args.install_target,
    ]
    if args.overwrite:
        cmd.append("--overwrite")
    if args.dry_run:
        cmd.append("--dry-run")
    for slug in includes:
        cmd.extend(["--include", slug])

    print(
        f"Installing created-agent group '{args.group_prefix}' with {len(includes)} agents."
    )
    result = subprocess.run(cmd)
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
