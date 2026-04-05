#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


@dataclass(frozen=True)
class ReleaseSummary:
    version: str
    released_at: str
    channel: str
    benchmark_status: str
    benchmark_pass_rate: float
    repository_quality_status: str
    skills_count: int
    agents_count: int
    local_skills_count: int
    packs: list[dict]


def read_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return payload
    except Exception:
        pass
    return {}


def normalize_version(value: str) -> str:
    match = SEMVER_RE.match(value.strip())
    if not match:
        raise ValueError(f"Invalid version '{value}'. Expected format vX.Y.Z or X.Y.Z.")
    major, minor, patch = match.groups()
    return f"v{int(major)}.{int(minor)}.{int(patch)}"


def bump_patch(version: str) -> str:
    match = SEMVER_RE.match(version)
    if not match:
        return "v1.0.0"
    major, minor, patch = [int(item) for item in match.groups()]
    return f"v{major}.{minor}.{patch + 1}"


def parse_repository_quality_status(report_text: str) -> str:
    if "Status: **Healthy**" in report_text:
        return "healthy"
    if "Status: **Needs attention**" in report_text:
        return "needs_attention"
    return "unknown"


def get_next_version(index_payload: dict) -> str:
    releases = index_payload.get("releases", [])
    if not isinstance(releases, list) or not releases:
        return "v1.0.0"

    versions: list[str] = []
    for item in releases:
        if not isinstance(item, dict):
            continue
        value = item.get("version")
        if isinstance(value, str) and SEMVER_RE.match(value.strip()):
            versions.append(normalize_version(value))

    if not versions:
        return "v1.0.0"

    versions.sort(
        key=lambda v: tuple(int(part) for part in normalize_version(v).lstrip("v").split("."))
    )
    return bump_patch(versions[-1])


def detect_packs(catalog_dir: Path, skills_index: dict, agents_index: dict) -> list[dict]:
    packs: list[dict] = []

    ai_factory_file = catalog_dir / "ai-factory-pack-2026.json"
    if ai_factory_file.exists():
        payload = read_json(ai_factory_file)
        counts = payload.get("counts", {})
        packs.append(
            {
                "name": "ai-factory-pack-2026",
                "skills": int(counts.get("skills", 0)) if isinstance(counts, dict) else 0,
                "agents": int(counts.get("agents", 0)) if isinstance(counts, dict) else 0,
            }
        )

    skill_items = skills_index.get("items", [])
    agent_items = agents_index.get("items", [])
    exceptional_skills = 0
    exceptional_agents = 0
    if isinstance(skill_items, list):
        exceptional_skills = sum(
            1
            for item in skill_items
            if isinstance(item, dict)
            and isinstance(item.get("slug"), str)
            and item["slug"].endswith("-skill-2026")
            and (
                item["slug"].startswith("mathematics-")
                or item["slug"].startswith("programming-")
                or item["slug"].startswith("robotics-")
            )
        )
    if isinstance(agent_items, list):
        exceptional_agents = sum(
            1
            for item in agent_items
            if isinstance(item, dict)
            and isinstance(item.get("slug"), str)
            and item["slug"].endswith("-exceptional-agent-2026")
        )

    if exceptional_skills or exceptional_agents:
        packs.append(
            {
                "name": "exceptional-pack-2026",
                "skills": exceptional_skills,
                "agents": exceptional_agents,
            }
        )

    return packs


def build_release_summary(
    version: str,
    channel: str,
    benchmark: dict,
    repository_quality_text: str,
    skills_index: dict,
    agents_index: dict,
    packs: list[dict],
) -> ReleaseSummary:
    benchmark_summary = benchmark.get("summary", {})
    if not isinstance(benchmark_summary, dict):
        benchmark_summary = {}
    skills_count = int(skills_index.get("count", 0))
    agents_count = int(agents_index.get("count", 0))

    local_skills_count = 0
    items = skills_index.get("items", [])
    if isinstance(items, list):
        local_skills_count = sum(
            1 for item in items if isinstance(item, dict) and bool(item.get("is_local", False))
        )

    return ReleaseSummary(
        version=version,
        released_at=datetime.now(timezone.utc).isoformat(),
        channel=channel,
        benchmark_status=str(benchmark_summary.get("status", "unknown")),
        benchmark_pass_rate=float(benchmark_summary.get("overall_pass_rate_percent", 0.0)),
        repository_quality_status=parse_repository_quality_status(repository_quality_text),
        skills_count=skills_count,
        agents_count=agents_count,
        local_skills_count=local_skills_count,
        packs=packs,
    )


def build_release_notes(summary: ReleaseSummary, notes: str) -> str:
    pack_lines = (
        "\n".join(
            f"- `{pack['name']}`: skills={pack.get('skills', 0)}, agents={pack.get('agents', 0)}"
            for pack in summary.packs
        )
        if summary.packs
        else "- No themed packs detected."
    )
    notes_block = notes.strip() if notes.strip() else "No additional notes provided."
    return f"""# Release {summary.version}

- Released at: `{summary.released_at}`
- Channel: `{summary.channel}`

## Quality Snapshot
- Repository quality status: **{summary.repository_quality_status}**
- Benchmark status: **{summary.benchmark_status}**
- Benchmark pass rate: **{summary.benchmark_pass_rate}%**

## Repository Scale
- Skills discovered: **{summary.skills_count}**
- Local skills (repo-owned): **{summary.local_skills_count}**
- Agents discovered: **{summary.agents_count}**

## Themed Packs
{pack_lines}

## Notes
{notes_block}
"""


def update_changelog(changelog_file: Path, summary: ReleaseSummary) -> None:
    date_only = summary.released_at.split("T", 1)[0]
    entry = (
        f"## {summary.version} - {date_only}\n"
        f"- Channel: `{summary.channel}`\n"
        f"- Repository quality: **{summary.repository_quality_status}**\n"
        f"- Benchmark: **{summary.benchmark_status}** ({summary.benchmark_pass_rate}%)\n"
        f"- Skills: **{summary.skills_count}** | Agents: **{summary.agents_count}**\n\n"
    )

    if changelog_file.exists():
        existing = changelog_file.read_text(encoding="utf-8")
        if f"## {summary.version} -" in existing:
            return
        if existing.startswith("# Changelog"):
            content = existing.split("\n", 1)
            head = content[0]
            tail = content[1] if len(content) > 1 else ""
            changelog_file.write_text(f"{head}\n\n{entry}{tail}", encoding="utf-8")
            return
        changelog_file.write_text(f"# Changelog\n\n{entry}{existing}", encoding="utf-8")
        return

    changelog_file.write_text(f"# Changelog\n\n{entry}", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a versioned release bundle with changelog and catalog metadata."
    )
    parser.add_argument("--version", default="", help="Release version (vX.Y.Z). If omitted, auto-bump patch.")
    parser.add_argument("--channel", default="stable", help="Release channel label.")
    parser.add_argument("--notes", default="", help="Optional release notes text.")
    parser.add_argument("--catalog-dir", default="catalog", help="Catalog directory path.")
    parser.add_argument("--releases-dir", default="catalog/releases", help="Release output directory.")
    parser.add_argument("--index-file", default="catalog/releases/releases-index.json", help="Release index JSON file.")
    parser.add_argument("--changelog-file", default="CHANGELOG.md", help="Changelog file path.")
    parser.add_argument("--strict", action="store_true", help="Fail if benchmark/quality status is not healthy.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    catalog_dir = (base / args.catalog_dir).resolve()
    releases_dir = (base / args.releases_dir).resolve()
    index_file = (base / args.index_file).resolve()
    changelog_file = (base / args.changelog_file).resolve()

    benchmark_file = catalog_dir / "benchmark-results.json"
    quality_file = catalog_dir / "repository-quality.md"
    skills_index_file = catalog_dir / "skills.index.json"
    agents_index_file = catalog_dir / "agents.index.json"

    benchmark = read_json(benchmark_file)
    skills_index = read_json(skills_index_file)
    agents_index = read_json(agents_index_file)
    repository_quality_text = quality_file.read_text(encoding="utf-8") if quality_file.exists() else ""

    releases_index = read_json(index_file) if index_file.exists() else {"format_version": 1, "releases": []}
    if "releases" not in releases_index or not isinstance(releases_index.get("releases"), list):
        releases_index["releases"] = []
    releases_index.setdefault("format_version", 1)

    version = normalize_version(args.version) if args.version else get_next_version(releases_index)
    packs = detect_packs(catalog_dir, skills_index, agents_index)
    summary = build_release_summary(
        version=version,
        channel=args.channel,
        benchmark=benchmark,
        repository_quality_text=repository_quality_text,
        skills_index=skills_index,
        agents_index=agents_index,
        packs=packs,
    )

    if args.strict:
        if summary.benchmark_status != "healthy":
            raise SystemExit(
                f"Cannot create strict release: benchmark status is '{summary.benchmark_status}'."
            )
        if summary.repository_quality_status != "healthy":
            raise SystemExit(
                f"Cannot create strict release: repository quality status is '{summary.repository_quality_status}'."
            )

    release_dir = releases_dir / summary.version
    release_dir.mkdir(parents=True, exist_ok=True)
    notes_text = build_release_notes(summary, args.notes)
    release_payload = {
        "version": summary.version,
        "released_at": summary.released_at,
        "channel": summary.channel,
        "benchmark_status": summary.benchmark_status,
        "benchmark_pass_rate": summary.benchmark_pass_rate,
        "repository_quality_status": summary.repository_quality_status,
        "skills_count": summary.skills_count,
        "local_skills_count": summary.local_skills_count,
        "agents_count": summary.agents_count,
        "packs": summary.packs,
        "notes": args.notes.strip(),
    }
    assets_manifest = {
        "version": summary.version,
        "files": [
            str((catalog_dir / "repository-quality.md").relative_to(base)),
            str((catalog_dir / "benchmark-results.json").relative_to(base)),
            str((catalog_dir / "skills.index.json").relative_to(base)),
            str((catalog_dir / "agents.index.json").relative_to(base)),
            str((catalog_dir / "quality-dashboard.html").relative_to(base)),
        ],
    }

    (release_dir / "release-notes.md").write_text(notes_text, encoding="utf-8")
    (release_dir / "release.json").write_text(json.dumps(release_payload, indent=2) + "\n", encoding="utf-8")
    (release_dir / "assets-manifest.json").write_text(
        json.dumps(assets_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    releases = releases_index["releases"]
    releases = [item for item in releases if not (isinstance(item, dict) and item.get("version") == summary.version)]
    releases.append(
        {
            "version": summary.version,
            "released_at": summary.released_at,
            "channel": summary.channel,
            "benchmark_status": summary.benchmark_status,
            "benchmark_pass_rate": summary.benchmark_pass_rate,
            "repository_quality_status": summary.repository_quality_status,
            "skills_count": summary.skills_count,
            "agents_count": summary.agents_count,
            "path": str(release_dir.relative_to(base)),
        }
    )
    releases.sort(
        key=lambda item: tuple(
            int(part) for part in normalize_version(str(item.get("version", "v0.0.0"))).lstrip("v").split(".")
        )
    )
    releases_index["releases"] = releases
    index_file.parent.mkdir(parents=True, exist_ok=True)
    index_file.write_text(json.dumps(releases_index, indent=2) + "\n", encoding="utf-8")

    update_changelog(changelog_file, summary)

    print(f"Wrote {release_dir / 'release-notes.md'}")
    print(f"Wrote {release_dir / 'release.json'}")
    print(f"Wrote {release_dir / 'assets-manifest.json'}")
    print(f"Wrote {index_file}")
    print(f"Updated {changelog_file}")
    print("")
    print(f"Release generated: {summary.version}")
    print(f"Benchmark status: {summary.benchmark_status}")
    print(f"Repository quality status: {summary.repository_quality_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
