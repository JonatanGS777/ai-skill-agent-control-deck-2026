#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

SKILL_CONTRACT_KEYS = (
    "inputs expected",
    "workflow",
    "output contract",
    "guardrails",
    "foundations",
    "logical reliability checklist",
)

AGENT_CONTRACT_KEYS = (
    "inputs expected",
    "skill bootstrap protocol",
    "logical reliability core",
    "reasoning control protocol",
    "workflow",
    "output contract",
    "guardrails",
)


@dataclass(frozen=True)
class Artifact:
    kind: str  # skill | agent
    slug: str
    dir_path: Path
    md_path: Path
    meta_path: Path
    current_version: str
    identity_hash: str
    contract_hash: str
    full_hash: str
    md_has_frontmatter: bool
    md_version: str | None
    meta_version: str | None

    @property
    def key(self) -> str:
        return f"{self.kind}:{self.slug}"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize_version(value: str | None) -> str:
    if value and SEMVER_RE.match(value):
        return value
    return "1.0.0"


def bump_version(version: str, bump: str) -> str:
    try:
        major, minor, patch = [int(part) for part in version.split(".")]
    except Exception:
        major, minor, patch = 1, 0, 0

    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    if bump == "patch":
        return f"{major}.{minor}.{patch + 1}"
    return version


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def detect_frontmatter(content: str) -> tuple[bool, str]:
    if not content.startswith("---\n"):
        return (False, "")
    idx = content.find("\n---\n", 4)
    if idx == -1:
        return (False, "")
    frontmatter = content[4:idx]
    return (True, frontmatter)


def parse_frontmatter_version(content: str) -> tuple[bool, str | None]:
    has_frontmatter, front = detect_frontmatter(content)
    if not has_frontmatter:
        return (False, None)
    for line in front.splitlines():
        stripped = line.strip()
        if stripped.startswith("version:"):
            value = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            return (True, value or None)
    return (True, None)


def update_markdown_frontmatter_version(content: str, new_version: str) -> str:
    has_frontmatter, front = detect_frontmatter(content)
    if not has_frontmatter:
        return content

    idx = content.find("\n---\n", 4)
    assert idx != -1
    front_lines = front.splitlines()
    replaced = False
    out_lines: list[str] = []
    for line in front_lines:
        if re.match(r"^\s*version\s*:", line):
            out_lines.append(f'version: "{new_version}"')
            replaced = True
        else:
            out_lines.append(line)
    if not replaced:
        insert_at = 0
        for i, line in enumerate(out_lines):
            if re.match(r"^\s*description\s*:", line):
                insert_at = i + 1
                break
        out_lines.insert(insert_at, f'version: "{new_version}"')

    new_front = "\n".join(out_lines)
    return f"---\n{new_front}\n---\n{content[idx + 5:]}"


def extract_sections(content: str, keys: tuple[str, ...]) -> str:
    lines = content.splitlines()
    heading_indexes: list[int] = []
    for i, line in enumerate(lines):
        if re.match(r"^#{1,6}\s+", line):
            heading_indexes.append(i)

    if not heading_indexes:
        return content

    selected_blocks: list[str] = []
    for pos, start in enumerate(heading_indexes):
        heading = re.sub(r"^#{1,6}\s+", "", lines[start]).strip().lower()
        if not any(key in heading for key in keys):
            continue
        end = heading_indexes[pos + 1] if pos + 1 < len(heading_indexes) else len(lines)
        block = "\n".join(lines[start:end]).strip()
        if block:
            selected_blocks.append(block)

    if not selected_blocks:
        return content
    return "\n\n".join(selected_blocks)


def sanitize_meta(meta: dict) -> dict:
    payload = copy.deepcopy(meta)
    payload.pop("version", None)
    return payload


def compute_identity_payload(kind: str, meta: dict) -> dict:
    base = {
        "name": meta.get("name"),
        "compatibility": meta.get("compatibility"),
        "entrypoint": meta.get("entrypoint"),
    }
    if kind == "agent":
        base["agent_type"] = meta.get("agent_type")
    return base


def compute_contract_payload(kind: str, meta: dict, markdown_content: str) -> dict:
    keys = SKILL_CONTRACT_KEYS if kind == "skill" else AGENT_CONTRACT_KEYS
    section_text = extract_sections(markdown_content, keys)
    payload = {"sections": section_text}
    if kind == "skill":
        payload["foundation_skills"] = meta.get("foundation_skills", [])
        payload["quality_tier"] = meta.get("quality_tier")
    else:
        payload["skills"] = meta.get("skills", [])
        payload["logic_foundation_skills"] = meta.get("logic_foundation_skills", [])
        payload["logic_foundation_mode"] = meta.get("logic_foundation_mode")
    return payload


def discover_artifacts(root: Path, kind: str) -> list[Artifact]:
    artifacts: list[Artifact] = []
    if not root.exists():
        return artifacts

    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        if kind == "skill":
            md_path = entry / "SKILL.md"
            meta_path = entry / "skill.meta.json"
        else:
            md_path = entry / "AGENT.md"
            meta_path = entry / "agent.meta.json"
        if not md_path.exists() or not meta_path.exists():
            continue

        markdown = md_path.read_text(encoding="utf-8")
        meta = read_json(meta_path)
        if not meta:
            continue

        md_has_frontmatter, md_version = parse_frontmatter_version(markdown)
        meta_version = meta.get("version")
        current_version = normalize_version(meta_version or md_version)

        identity_payload = compute_identity_payload(kind, meta)
        contract_payload = compute_contract_payload(kind, meta, markdown)
        full_payload = {
            "meta": sanitize_meta(meta),
            "markdown": markdown,
        }

        artifacts.append(
            Artifact(
                kind=kind,
                slug=entry.name,
                dir_path=entry,
                md_path=md_path,
                meta_path=meta_path,
                current_version=current_version,
                identity_hash=sha256_text(json.dumps(identity_payload, sort_keys=True)),
                contract_hash=sha256_text(json.dumps(contract_payload, sort_keys=True)),
                full_hash=sha256_text(json.dumps(full_payload, sort_keys=True)),
                md_has_frontmatter=md_has_frontmatter,
                md_version=md_version,
                meta_version=meta_version,
            )
        )
    return artifacts


def update_artifact_version(artifact: Artifact, new_version: str, dry_run: bool) -> None:
    meta = read_json(artifact.meta_path)
    meta["version"] = new_version
    meta_text = json.dumps(meta, indent=2) + "\n"

    md_content = artifact.md_path.read_text(encoding="utf-8")
    md_updated = update_markdown_frontmatter_version(md_content, new_version)

    if dry_run:
        print(f"[dry-run] set {artifact.key} -> {new_version}")
        return
    artifact.meta_path.write_text(meta_text, encoding="utf-8")
    artifact.md_path.write_text(md_updated, encoding="utf-8")


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"format_version": 1, "items": {}}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"format_version": 1, "items": {}}
    if not isinstance(payload, dict):
        return {"format_version": 1, "items": {}}
    payload.setdefault("format_version", 1)
    payload.setdefault("items", {})
    return payload


def save_state(path: Path, state: dict, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def choose_bump(prior: dict, current: Artifact) -> str | None:
    if prior.get("identity_hash") != current.identity_hash:
        return "major"
    if prior.get("contract_hash") != current.contract_hash:
        return "minor"
    if prior.get("full_hash") != current.full_hash:
        return "patch"
    return None


def record_for_state(artifact: Artifact, version: str) -> dict:
    return {
        "kind": artifact.kind,
        "slug": artifact.slug,
        "path": str(artifact.dir_path),
        "version": version,
        "identity_hash": artifact.identity_hash,
        "contract_hash": artifact.contract_hash,
        "full_hash": artifact.full_hash,
    }


def refresh_artifact(artifact: Artifact) -> Artifact:
    refreshed = discover_artifacts(artifact.dir_path.parent, artifact.kind)
    for item in refreshed:
        if item.slug == artifact.slug:
            return item
    return artifact


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Semantic version manager for local skill/agent repositories."
    )
    parser.add_argument(
        "--scope",
        choices=["skills", "agents", "both"],
        default="both",
        help="Which artifact sets to process.",
    )
    parser.add_argument(
        "--mode",
        choices=["apply", "check", "initialize"],
        default="apply",
        help="apply=write versions/state, check=report pending bumps, initialize=state baseline only.",
    )
    parser.add_argument("--skills-root", default="skills", help="Skills root directory.")
    parser.add_argument("--agents-root", default="agents", help="Agents root directory.")
    parser.add_argument("--state-file", default="catalog/version-state.json", help="State file path.")
    parser.add_argument("--strict", action="store_true", help="Fail if pending changes are detected.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    skills_root = (base / args.skills_root).resolve()
    agents_root = (base / args.agents_root).resolve()
    state_path = (base / args.state_file).resolve()

    artifacts: list[Artifact] = []
    if args.scope in ("skills", "both"):
        artifacts.extend(discover_artifacts(skills_root, "skill"))
    if args.scope in ("agents", "both"):
        artifacts.extend(discover_artifacts(agents_root, "agent"))
    artifacts.sort(key=lambda item: (item.kind, item.slug))

    state = load_state(state_path)
    state_items: dict = state.get("items", {})
    next_items: dict = {}

    initialized = 0
    changed = 0
    pending = 0
    mismatched_versions = 0
    untracked = 0

    for artifact in artifacts:
        prior = state_items.get(artifact.key)

        if artifact.meta_version and artifact.md_version and artifact.meta_version != artifact.md_version:
            mismatched_versions += 1

        if prior is None:
            untracked += 1
            if args.mode == "check":
                print(f"{artifact.key}: missing state entry (run initialize/apply)")
            initialized += 1
            next_items[artifact.key] = record_for_state(artifact, artifact.current_version)
            continue
        if args.mode == "initialize":
            initialized += 1
            next_items[artifact.key] = record_for_state(artifact, artifact.current_version)
            continue

        if (
            artifact.meta_version
            and artifact.md_version
            and artifact.meta_version != artifact.md_version
            and args.mode == "apply"
        ):
            print(f"{artifact.key}: syncing mismatched meta/md version to {artifact.current_version}")
            update_artifact_version(artifact, artifact.current_version, dry_run=args.dry_run)
            updated_artifact = refresh_artifact(artifact) if not args.dry_run else artifact
            changed += 1
            next_items[artifact.key] = record_for_state(updated_artifact, artifact.current_version)
            continue

        bump = choose_bump(prior, artifact)
        if not bump:
            next_items[artifact.key] = record_for_state(artifact, artifact.current_version)
            continue

        pending += 1
        new_version = bump_version(artifact.current_version, bump)
        print(f"{artifact.key}: {artifact.current_version} -> {new_version} ({bump})")

        if args.mode == "apply":
            update_artifact_version(artifact, new_version, dry_run=args.dry_run)
            updated_artifact = refresh_artifact(artifact) if not args.dry_run else artifact
            changed += 1
            next_items[artifact.key] = record_for_state(updated_artifact, new_version)
        else:
            next_items[artifact.key] = record_for_state(artifact, artifact.current_version)

    state["items"] = next_items
    if args.mode in ("apply", "initialize"):
        save_state(state_path, state, dry_run=args.dry_run)

    print("")
    print(f"Artifacts scanned: {len(artifacts)}")
    print(f"Initialized entries: {initialized}")
    print(f"Untracked artifacts: {untracked}")
    print(f"Pending bumps: {pending}")
    print(f"Applied bumps: {changed}")
    print(f"Version mismatches (meta vs markdown): {mismatched_versions}")

    if args.mode == "check" and args.strict and (pending > 0 or untracked > 0 or mismatched_versions > 0):
        return 2
    if args.strict and mismatched_versions > 0 and args.mode != "check":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
