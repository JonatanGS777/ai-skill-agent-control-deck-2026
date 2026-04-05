#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


LOGIC_FOUNDATION_SKILLS = {
    "logic-propositional-reasoning",
    "logic-predicate-quantifiers",
    "logic-proof-strategies",
    "set-theory-foundations",
    "relations-functions-foundations",
    "discrete-structures-core",
    "combinatorics-counting-principles",
    "graph-theory-foundations",
    "number-theory-modular-arithmetic",
    "linear-algebra-foundations",
    "probability-foundations",
    "statistics-inference-foundations",
    "complexity-analysis-foundations",
    "algorithm-correctness-invariants",
    "recursion-induction-foundations",
    "data-structures-invariants",
    "formal-languages-automata",
    "computability-decidability",
    "optimization-foundations",
    "numerical-stability-foundations",
    "logic-of-programs-hoare",
    "type-systems-foundations",
    "functional-programming-foundations",
    "concurrency-memory-model-foundations",
    "database-theory-normalization",
    "distributed-systems-consistency-foundations",
    "cryptography-primitives-foundations",
    "security-threat-modeling-foundations",
    "testing-verification-foundations",
    "debugging-causal-reasoning-foundations",
}


@dataclass(frozen=True)
class SkillRecord:
    slug: str
    path: Path
    is_local: bool
    has_skill_md: bool
    has_meta: bool
    has_readme: bool
    meta: dict


@dataclass(frozen=True)
class AgentRecord:
    slug: str
    path: Path
    has_agent_md: bool
    has_meta: bool
    has_readme: bool
    meta: dict


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def extract_benchmark_maps(benchmark_payload: dict) -> tuple[dict[str, float], dict[str, bool], dict[str, float], dict[str, bool]]:
    skill_scores: dict[str, float] = {}
    skill_pass: dict[str, bool] = {}
    agent_scores: dict[str, float] = {}
    agent_pass: dict[str, bool] = {}

    artifacts = benchmark_payload.get("artifacts", {})
    if not isinstance(artifacts, dict):
        return skill_scores, skill_pass, agent_scores, agent_pass

    for item in artifacts.get("skills", []):
        if not isinstance(item, dict):
            continue
        slug = item.get("slug")
        if not isinstance(slug, str):
            continue
        score = item.get("total_score")
        if isinstance(score, (int, float)):
            skill_scores[slug] = round(float(score), 2)
        skill_pass[slug] = bool(item.get("pass_thresholds", False))

    for item in artifacts.get("agents", []):
        if not isinstance(item, dict):
            continue
        slug = item.get("slug")
        if not isinstance(slug, str):
            continue
        score = item.get("total_score")
        if isinstance(score, (int, float)):
            agent_scores[slug] = round(float(score), 2)
        agent_pass[slug] = bool(item.get("pass_thresholds", False))

    return skill_scores, skill_pass, agent_scores, agent_pass


def discover_skills(skill_sources: list[Path]) -> list[SkillRecord]:
    by_slug: dict[str, SkillRecord] = {}
    for source_index, source in enumerate(skill_sources):
        if not source.exists():
            continue
        for entry in sorted(source.iterdir()):
            if not entry.is_dir():
                continue
            skill_md = entry / "SKILL.md"
            meta_file = entry / "skill.meta.json"
            readme = entry / "README.md"
            if not skill_md.exists() and not meta_file.exists():
                continue
            if entry.name in by_slug:
                continue
            meta = read_json(meta_file) if meta_file.exists() else {}
            by_slug[entry.name] = SkillRecord(
                slug=entry.name,
                path=entry,
                is_local=(source_index == 0),
                has_skill_md=skill_md.exists(),
                has_meta=meta_file.exists(),
                has_readme=readme.exists(),
                meta=meta,
            )
    return [by_slug[key] for key in sorted(by_slug.keys())]


def discover_agents(agents_root: Path) -> list[AgentRecord]:
    records: list[AgentRecord] = []
    if not agents_root.exists():
        return records
    for entry in sorted(agents_root.iterdir()):
        if not entry.is_dir():
            continue
        agent_md = entry / "AGENT.md"
        meta_file = entry / "agent.meta.json"
        readme = entry / "README.md"
        meta = read_json(meta_file) if meta_file.exists() else {}
        records.append(
            AgentRecord(
                slug=entry.name,
                path=entry,
                has_agent_md=agent_md.exists(),
                has_meta=meta_file.exists(),
                has_readme=readme.exists(),
                meta=meta,
            )
        )
    return records


def build_skills_index(
    skills: list[SkillRecord],
    quality_score_map: dict[str, float] | None = None,
    quality_pass_map: dict[str, bool] | None = None,
) -> dict:
    quality_score_map = quality_score_map or {}
    quality_pass_map = quality_pass_map or {}
    return {
        "count": len(skills),
        "items": [
            {
                "slug": s.slug,
                "path": str(s.path),
                "is_local": s.is_local,
                "has_skill_md": s.has_skill_md,
                "has_meta": s.has_meta,
                "has_readme": s.has_readme,
                "domain": s.meta.get("domain"),
                "quality_tier": s.meta.get("quality_tier"),
                "tags": s.meta.get("tags", []),
                "foundation_skills": s.meta.get("foundation_skills", []),
                "quality_score": quality_score_map.get(s.slug),
                "benchmark_pass": quality_pass_map.get(s.slug),
            }
            for s in skills
        ],
    }


def build_agents_index(
    agents: list[AgentRecord],
    quality_score_map: dict[str, float] | None = None,
    quality_pass_map: dict[str, bool] | None = None,
) -> dict:
    quality_score_map = quality_score_map or {}
    quality_pass_map = quality_pass_map or {}
    return {
        "count": len(agents),
        "items": [
            {
                "slug": a.slug,
                "path": str(a.path),
                "has_agent_md": a.has_agent_md,
                "has_meta": a.has_meta,
                "has_readme": a.has_readme,
                "agent_type": a.meta.get("agent_type"),
                "skill_mode": a.meta.get("skill_mode"),
                "logic_foundation_mode": a.meta.get("logic_foundation_mode"),
                "skills": a.meta.get("skills", []),
                "logic_foundation_skills": a.meta.get("logic_foundation_skills", []),
                "tags": a.meta.get("tags", []),
                "quality_score": quality_score_map.get(a.slug),
                "benchmark_pass": quality_pass_map.get(a.slug),
            }
            for a in agents
        ],
    }


def build_quality_report(
    skills: list[SkillRecord],
    agents: list[AgentRecord],
    benchmark_payload: dict | None = None,
) -> tuple[str, list[str]]:
    issues: list[str] = []
    skill_set = {s.slug for s in skills}
    local_skills = [s for s in skills if s.is_local]

    missing_skill_docs = [s.slug for s in local_skills if not s.has_skill_md]
    missing_skill_meta = [s.slug for s in local_skills if not s.has_meta]
    missing_skill_readme = [s.slug for s in local_skills if not s.has_readme]

    missing_agent_docs = [a.slug for a in agents if not a.has_agent_md]
    missing_agent_meta = [a.slug for a in agents if not a.has_meta]
    missing_agent_readme = [a.slug for a in agents if not a.has_readme]

    if missing_skill_docs:
        issues.append(f"Skills missing SKILL.md: {', '.join(missing_skill_docs)}")
    if missing_skill_meta:
        issues.append(f"Skills missing skill.meta.json: {', '.join(missing_skill_meta)}")
    if missing_skill_readme:
        issues.append(f"Skills missing README.md: {', '.join(missing_skill_readme)}")
    if missing_agent_docs:
        issues.append(f"Agents missing AGENT.md: {', '.join(missing_agent_docs)}")
    if missing_agent_meta:
        issues.append(f"Agents missing agent.meta.json: {', '.join(missing_agent_meta)}")
    if missing_agent_readme:
        issues.append(f"Agents missing README.md: {', '.join(missing_agent_readme)}")

    unresolved_agent_skill_refs: list[str] = []
    for agent in agents:
        refs = agent.meta.get("skills", [])
        if not isinstance(refs, list):
            continue
        missing = [ref for ref in refs if ref not in skill_set]
        if missing:
            unresolved_agent_skill_refs.append(f"{agent.slug}: {', '.join(missing)}")
    if unresolved_agent_skill_refs:
        issues.append("Agents with unresolved skill refs: " + " | ".join(unresolved_agent_skill_refs))

    logic_skills_present = len([s for s in skills if s.slug in LOGIC_FOUNDATION_SKILLS])
    agents_with_logic = len(
        [
            a
            for a in agents
            if any(skill in LOGIC_FOUNDATION_SKILLS for skill in a.meta.get("skills", []))
        ]
    )

    lines: list[str] = []
    lines.append("# Repository Quality Report")
    lines.append("")
    lines.append(f"- Skills discovered: **{len(skills)}**")
    lines.append(f"- Local skills (repo-owned): **{len(local_skills)}**")
    lines.append(f"- Agents discovered: **{len(agents)}**")
    lines.append(f"- Logic foundation skills present: **{logic_skills_present}/{len(LOGIC_FOUNDATION_SKILLS)}**")
    lines.append(f"- Agents using at least one logic foundation skill: **{agents_with_logic}**")
    lines.append("")

    if benchmark_payload:
        summary = benchmark_payload.get("summary", {})
        regression = benchmark_payload.get("regression", {})
        coverage = benchmark_payload.get("coverage", {})
        rankings = benchmark_payload.get("rankings", {})

        benchmark_status = str(summary.get("status", "unknown"))
        regression_status = str(regression.get("status", "unknown"))
        coverage_status = str(coverage.get("status", "unknown"))

        if benchmark_status != "healthy":
            issues.append(f"Benchmark suite status is not healthy: {benchmark_status}")
        if regression_status != "pass":
            issues.append(f"Benchmark regression checks are failing: {regression_status}")
        if coverage_status != "pass":
            issues.append(f"Benchmark real-world coverage checks are failing: {coverage_status}")

        lines.append("## Benchmark Summary")
        lines.append(f"- Suite status: **{benchmark_status}**")
        lines.append(
            "- Artifact pass: "
            f"**skills {summary.get('skills_passed', 0)}/{summary.get('skills_total', 0)}**, "
            f"**agents {summary.get('agents_passed', 0)}/{summary.get('agents_total', 0)}**"
        )
        lines.append(f"- Overall pass rate: **{summary.get('overall_pass_rate_percent', 0)}%**")
        lines.append(f"- Regression checks: **{regression_status}**")
        lines.append(f"- Real-world coverage checks: **{coverage_status}**")
        lines.append("")

        skills_top = rankings.get("skills_top", []) if isinstance(rankings, dict) else []
        agents_top = rankings.get("agents_top", []) if isinstance(rankings, dict) else []

        lines.append("### Top Skill Quality Scores")
        if isinstance(skills_top, list) and skills_top:
            for item in skills_top[:5]:
                if not isinstance(item, dict):
                    continue
                lines.append(f"- `{item.get('slug')}`: **{item.get('total_score')}**")
        else:
            lines.append("- No benchmark ranking data available.")
        lines.append("")

        lines.append("### Top Agent Quality Scores")
        if isinstance(agents_top, list) and agents_top:
            for item in agents_top[:5]:
                if not isinstance(item, dict):
                    continue
                lines.append(f"- `{item.get('slug')}`: **{item.get('total_score')}**")
        else:
            lines.append("- No benchmark ranking data available.")
        lines.append("")

    lines.append("## Quality Status")
    if issues:
        lines.append("- Status: **Needs attention**")
        lines.append("")
        lines.append("## Issues")
        for issue in issues:
            lines.append(f"- {issue}")
    else:
        lines.append("- Status: **Healthy**")
        lines.append("- No structural issues detected in current scan.")
    lines.append("")
    return ("\n".join(lines) + "\n", issues)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild repo catalogs for skills and agents with quality checks.")
    parser.add_argument("--skills-root", default="skills", help="Canonical skills directory.")
    parser.add_argument(
        "--skill-source",
        action="append",
        default=[],
        help="Additional skill source path. Repeatable.",
    )
    parser.add_argument("--agents-root", default="agents", help="Canonical agents directory.")
    parser.add_argument("--output-dir", default="catalog", help="Catalog output directory.")
    parser.add_argument(
        "--benchmark-file",
        default="catalog/benchmark-results.json",
        help="Benchmark JSON output consumed for quality score and report summary.",
    )
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if quality issues are found.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    local_skills_root = (base / args.skills_root).resolve()
    agents_root = (base / args.agents_root).resolve()
    output_dir = (base / args.output_dir).resolve()
    benchmark_file = (base / args.benchmark_file).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    extra_sources = [Path(path).expanduser().resolve() for path in args.skill_source]
    default_sources = [Path.home() / ".claude" / "skills", Path.home() / ".codex" / "skills"]
    skill_sources = [local_skills_root, *extra_sources, *default_sources]
    skills = discover_skills(skill_sources)
    agents = discover_agents(agents_root)
    benchmark_payload = read_json(benchmark_file) if benchmark_file.exists() else {}
    skill_score_map, skill_pass_map, agent_score_map, agent_pass_map = extract_benchmark_maps(benchmark_payload)

    skills_index = build_skills_index(
        skills,
        quality_score_map=skill_score_map,
        quality_pass_map=skill_pass_map,
    )
    agents_index = build_agents_index(
        agents,
        quality_score_map=agent_score_map,
        quality_pass_map=agent_pass_map,
    )
    report_md, issues = build_quality_report(
        skills,
        agents,
        benchmark_payload=benchmark_payload if benchmark_payload else None,
    )

    (output_dir / "skills.index.json").write_text(
        json.dumps(skills_index, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "agents.index.json").write_text(
        json.dumps(agents_index, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "repository-quality.md").write_text(report_md, encoding="utf-8")

    print(f"Wrote {output_dir / 'skills.index.json'}")
    print(f"Wrote {output_dir / 'agents.index.json'}")
    print(f"Wrote {output_dir / 'repository-quality.md'}")
    if issues:
        print(f"Quality issues detected: {len(issues)}")
    else:
        print("Quality issues detected: 0")

    if args.strict and issues:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
