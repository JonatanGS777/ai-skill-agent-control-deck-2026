#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LOGIC_KEYWORDS = (
    "assumption",
    "assumptions",
    "proof",
    "invariant",
    "verify",
    "verification",
    "logic",
    "contradiction",
    "consistency",
    "auditable",
)

SECURITY_KEYWORDS = (
    "never",
    "security",
    "secure",
    "safety",
    "safe",
    "risk",
    "threat",
    "compliance",
    "privacy",
    "auth",
    "authorization",
    "hardening",
)

SKILL_SECTION_GROUPS: tuple[tuple[str, ...], ...] = (
    ("mission",),
    ("inputs expected", "inputs", "input"),
    ("workflow",),
    ("output contract",),
    ("guardrails", "guardrail"),
)

AGENT_SECTION_GROUPS: tuple[tuple[str, ...], ...] = (
    ("mission",),
    ("inputs expected", "inputs", "input"),
    ("skill bootstrap protocol",),
    ("workflow",),
    ("output contract",),
    ("guardrails", "guardrail"),
)


@dataclass(frozen=True)
class ArtifactScore:
    kind: str
    slug: str
    path: str
    total_score: float
    scores: dict[str, float]
    pass_thresholds: bool
    findings: list[str]
    metrics: dict[str, Any]


def read_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return payload
    except Exception:
        pass
    return {}


def read_json_list(path: Path) -> list[dict]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
    except Exception:
        pass
    return []


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def normalize_heading(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9\s]+", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered).strip()
    return lowered


def extract_sections(markdown: str) -> dict[str, str]:
    lines = markdown.splitlines()
    heading_positions: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = re.match(r"^#{1,6}\s+(.+)$", line)
        if not match:
            continue
        heading_positions.append((index, normalize_heading(match.group(1))))

    sections: dict[str, str] = {}
    if not heading_positions:
        return sections

    for pos, (start, heading) in enumerate(heading_positions):
        end = heading_positions[pos + 1][0] if pos + 1 < len(heading_positions) else len(lines)
        block = "\n".join(lines[start + 1 : end]).strip()
        sections[heading] = block
    return sections


def find_section(sections: dict[str, str], aliases: tuple[str, ...]) -> str:
    for heading, content in sections.items():
        if any(alias in heading for alias in aliases):
            return content
    return ""


def contains_section(sections: dict[str, str], aliases: tuple[str, ...]) -> bool:
    for heading in sections:
        if any(alias in heading for alias in aliases):
            return True
    return False


def count_bullets(block: str) -> int:
    return sum(1 for line in block.splitlines() if re.match(r"^\s*[-*]\s+", line))


def count_numbered_steps(block: str) -> int:
    return sum(1 for line in block.splitlines() if re.match(r"^\s*\d+\.\s+", line))


def count_keyword_hits(text: str, keywords: tuple[str, ...]) -> int:
    lowered = text.lower()
    hits = 0
    for keyword in keywords:
        if keyword in lowered:
            hits += 1
    return hits


def clamp_100(value: float) -> float:
    return max(0.0, min(100.0, value))


def average_artifact_score(items: list[ArtifactScore]) -> float:
    if not items:
        return 0.0
    return round(sum(item.total_score for item in items) / float(len(items)), 2)


def weighted_total(scores: dict[str, float], weights: dict[str, float]) -> float:
    total = 0.0
    for key, value in scores.items():
        total += value * float(weights.get(key, 0.0))
    return round(clamp_100(total), 2)


def prompt_metrics(prompt_path: Path, slug: str) -> dict[str, Any]:
    text = read_text(prompt_path)
    bullets = count_bullets(text)
    references_slug = slug.lower() in text.lower()
    return {
        "path": str(prompt_path),
        "bullets": bullets,
        "references_slug": references_slug,
    }


def section_clarity_score(sections: dict[str, str], groups: tuple[tuple[str, ...], ...]) -> float:
    found = 0
    for group in groups:
        if contains_section(sections, group):
            found += 1
    return round((found / float(len(groups))) * 100.0, 2)


def score_skill(skill_dir: Path, suite: dict) -> ArtifactScore | None:
    skill_md = skill_dir / "SKILL.md"
    meta_file = skill_dir / "skill.meta.json"
    prompts_file = skill_dir / "examples" / "prompts.md"
    quality_gates_file = skill_dir / "references" / "quality-gates.md"
    if not skill_md.exists() or not meta_file.exists():
        return None

    markdown = read_text(skill_md)
    meta = read_json(meta_file)
    sections = extract_sections(markdown)
    prompts = prompt_metrics(prompts_file, skill_dir.name)

    workflow_block = find_section(sections, ("workflow",))
    guardrails_block = find_section(sections, ("guardrails", "guardrail"))
    output_contract_block = find_section(sections, ("output contract",))

    logic_score = 0.0
    if contains_section(sections, ("logical reliability checklist",)):
        logic_score += 25.0
    foundation_skills = meta.get("foundation_skills", [])
    if isinstance(foundation_skills, list):
        foundation_count = len(foundation_skills)
    else:
        foundation_count = 0
    if foundation_count >= 5:
        logic_score += 25.0
    elif foundation_count >= 3:
        logic_score += 20.0
    elif foundation_count >= 1:
        logic_score += 10.0

    workflow_steps = count_numbered_steps(workflow_block)
    if workflow_steps >= 4:
        logic_score += 25.0
    elif workflow_steps >= 3:
        logic_score += 20.0
    elif workflow_steps >= 2:
        logic_score += 12.0

    logic_hits = count_keyword_hits(markdown, LOGIC_KEYWORDS)
    if logic_hits >= 3:
        logic_score += 25.0
    elif logic_hits >= 2:
        logic_score += 20.0
    elif logic_hits >= 1:
        logic_score += 10.0
    logic_score = round(clamp_100(logic_score), 2)

    clarity_score = section_clarity_score(sections, SKILL_SECTION_GROUPS)

    security_score = 0.0
    guardrail_bullets = count_bullets(guardrails_block)
    if guardrail_bullets >= 3:
        security_score += 40.0
    elif guardrail_bullets >= 2:
        security_score += 30.0
    elif guardrail_bullets >= 1:
        security_score += 15.0

    security_hits = count_keyword_hits(markdown, SECURITY_KEYWORDS)
    if security_hits >= 4:
        security_score += 35.0
    elif security_hits >= 2:
        security_score += 25.0
    elif security_hits >= 1:
        security_score += 20.0

    if isinstance(foundation_skills, list) and (
        "security-threat-modeling-foundations" in foundation_skills
        or "cryptography-primitives-foundations" in foundation_skills
    ):
        security_score += 25.0
    security_score = round(clamp_100(security_score), 2)

    utility_score = 0.0
    if prompts["bullets"] >= 4:
        utility_score += 30.0
    elif prompts["bullets"] >= 3:
        utility_score += 24.0
    elif prompts["bullets"] >= 2:
        utility_score += 15.0
    elif prompts["bullets"] >= 1:
        utility_score += 8.0

    if prompts["references_slug"]:
        utility_score += 20.0

    output_contract_len = len(output_contract_block.strip())
    if output_contract_len >= 90:
        utility_score += 20.0
    elif output_contract_len >= 45:
        utility_score += 12.0

    tags = meta.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    if len(tags) >= 4:
        utility_score += 15.0
    elif len(tags) >= 2:
        utility_score += 10.0
    elif len(tags) >= 1:
        utility_score += 5.0

    if meta.get("domain"):
        utility_score += 8.0
    if quality_gates_file.exists():
        utility_score += 7.0
    utility_score = round(clamp_100(utility_score), 2)

    scores = {
        "logic": logic_score,
        "clarity": clarity_score,
        "security": security_score,
        "utility": utility_score,
    }

    thresholds = suite.get("thresholds", {})
    overall_min = float(thresholds.get("overall_min", 72.0))
    dimension_min = float(thresholds.get("dimension_min", 55.0))
    total = weighted_total(scores, suite.get("weights", {}))
    pass_thresholds = total >= overall_min and all(
        value >= dimension_min for value in scores.values()
    )

    findings: list[str] = []
    if not pass_thresholds:
        if total < overall_min:
            findings.append(f"total score below threshold ({total} < {overall_min})")
        for key, value in scores.items():
            if value < dimension_min:
                findings.append(f"{key} score below threshold ({value} < {dimension_min})")

    metrics = {
        "domain": str(meta.get("domain") or "unknown"),
        "category": str(meta.get("quality_tier") or "unknown"),
        "workflow_steps": workflow_steps,
        "guardrail_bullets": guardrail_bullets,
        "logic_keyword_hits": logic_hits,
        "security_keyword_hits": security_hits,
        "output_contract_length": output_contract_len,
        "foundation_skills_count": foundation_count,
        "tags_count": len(tags),
        "prompts": prompts,
    }
    return ArtifactScore(
        kind="skill",
        slug=skill_dir.name,
        path=str(skill_dir),
        total_score=total,
        scores=scores,
        pass_thresholds=pass_thresholds,
        findings=findings,
        metrics=metrics,
    )


def score_agent(agent_dir: Path, suite: dict) -> ArtifactScore | None:
    agent_md = agent_dir / "AGENT.md"
    meta_file = agent_dir / "agent.meta.json"
    prompts_file = agent_dir / "examples" / "prompts.md"
    skill_index_file = agent_dir / "references" / "skill-index.md"
    if not agent_md.exists() or not meta_file.exists():
        return None

    markdown = read_text(agent_md)
    meta = read_json(meta_file)
    sections = extract_sections(markdown)
    prompts = prompt_metrics(prompts_file, agent_dir.name)

    workflow_block = find_section(sections, ("workflow",))
    guardrails_block = find_section(sections, ("guardrails", "guardrail"))
    output_contract_block = find_section(sections, ("output contract",))

    logic_score = 0.0
    if contains_section(sections, ("logical reliability core",)):
        logic_score += 25.0
    if contains_section(sections, ("reasoning control protocol",)):
        logic_score += 25.0

    logic_foundation_skills = meta.get("logic_foundation_skills", [])
    if not isinstance(logic_foundation_skills, list):
        logic_foundation_skills = []
    logic_foundation_count = len(logic_foundation_skills)
    if logic_foundation_count >= 10:
        logic_score += 25.0
    elif logic_foundation_count >= 7:
        logic_score += 22.0
    elif logic_foundation_count >= 4:
        logic_score += 15.0
    elif logic_foundation_count >= 1:
        logic_score += 8.0

    workflow_steps = count_numbered_steps(workflow_block)
    if workflow_steps >= 4:
        logic_score += 25.0
    elif workflow_steps >= 3:
        logic_score += 20.0
    elif workflow_steps >= 2:
        logic_score += 12.0
    logic_score = round(clamp_100(logic_score), 2)

    clarity_score = section_clarity_score(sections, AGENT_SECTION_GROUPS)

    security_score = 0.0
    guardrail_bullets = count_bullets(guardrails_block)
    if guardrail_bullets >= 3:
        security_score += 30.0
    elif guardrail_bullets >= 2:
        security_score += 20.0
    elif guardrail_bullets >= 1:
        security_score += 10.0

    security_hits = count_keyword_hits(markdown, SECURITY_KEYWORDS)
    if security_hits >= 4:
        security_score += 25.0
    elif security_hits >= 2:
        security_score += 20.0
    elif security_hits >= 1:
        security_score += 15.0

    agent_skills = meta.get("skills", [])
    if not isinstance(agent_skills, list):
        agent_skills = []
    if "security-threat-modeling-foundations" in agent_skills:
        security_score += 20.0

    if contains_section(sections, ("escalation policy",)):
        security_score += 30.0
    security_score = round(clamp_100(security_score), 2)

    utility_score = 0.0
    if prompts["bullets"] >= 4:
        utility_score += 20.0
    elif prompts["bullets"] >= 3:
        utility_score += 16.0
    elif prompts["bullets"] >= 2:
        utility_score += 10.0
    elif prompts["bullets"] >= 1:
        utility_score += 5.0

    if prompts["references_slug"]:
        utility_score += 15.0

    skill_profile_count = len(agent_skills)
    if skill_profile_count >= 8:
        utility_score += 30.0
    elif skill_profile_count >= 5:
        utility_score += 24.0
    elif skill_profile_count >= 2:
        utility_score += 16.0
    elif skill_profile_count >= 1:
        utility_score += 8.0

    if skill_index_file.exists():
        utility_score += 20.0

    output_contract_len = len(output_contract_block.strip())
    if output_contract_len >= 90:
        utility_score += 15.0
    elif output_contract_len >= 45:
        utility_score += 10.0
    utility_score = round(clamp_100(utility_score), 2)

    scores = {
        "logic": logic_score,
        "clarity": clarity_score,
        "security": security_score,
        "utility": utility_score,
    }

    thresholds = suite.get("thresholds", {})
    overall_min = float(thresholds.get("overall_min", 72.0))
    dimension_min = float(thresholds.get("dimension_min", 55.0))
    total = weighted_total(scores, suite.get("weights", {}))
    pass_thresholds = total >= overall_min and all(
        value >= dimension_min for value in scores.values()
    )

    findings: list[str] = []
    if not pass_thresholds:
        if total < overall_min:
            findings.append(f"total score below threshold ({total} < {overall_min})")
        for key, value in scores.items():
            if value < dimension_min:
                findings.append(f"{key} score below threshold ({value} < {dimension_min})")

    metrics = {
        "domain": str(meta.get("agent_type") or "unknown"),
        "category": str(meta.get("logic_foundation_mode") or "unknown"),
        "workflow_steps": workflow_steps,
        "guardrail_bullets": guardrail_bullets,
        "security_keyword_hits": security_hits,
        "output_contract_length": output_contract_len,
        "logic_foundation_skills_count": logic_foundation_count,
        "skill_profile_count": skill_profile_count,
        "prompts": prompts,
    }
    return ArtifactScore(
        kind="agent",
        slug=agent_dir.name,
        path=str(agent_dir),
        total_score=total,
        scores=scores,
        pass_thresholds=pass_thresholds,
        findings=findings,
        metrics=metrics,
    )


def score_all_skills(skills_root: Path, suite: dict) -> list[ArtifactScore]:
    scores: list[ArtifactScore] = []
    if not skills_root.exists():
        return scores
    for entry in sorted(skills_root.iterdir()):
        if not entry.is_dir():
            continue
        scored = score_skill(entry, suite=suite)
        if scored is not None:
            scores.append(scored)
    return scores


def score_all_agents(agents_root: Path, suite: dict) -> list[ArtifactScore]:
    scores: list[ArtifactScore] = []
    if not agents_root.exists():
        return scores
    for entry in sorted(agents_root.iterdir()):
        if not entry.is_dir():
            continue
        scored = score_agent(entry, suite=suite)
        if scored is not None:
            scores.append(scored)
    return scores


def build_regression_checks(
    skill_scores: list[ArtifactScore],
    agent_scores: list[ArtifactScore],
    suite: dict,
) -> dict:
    regression_cfg = suite.get("regression", {})
    skill_prompt_bullets_min = int(regression_cfg.get("skill_prompt_bullets_min", 3))
    agent_prompt_bullets_min = int(regression_cfg.get("agent_prompt_bullets_min", 3))
    skill_ref_slug = bool(regression_cfg.get("skill_prompt_must_reference_slug", True))
    agent_ref_slug = bool(regression_cfg.get("agent_prompt_must_reference_slug", True))

    checks: list[dict] = []

    skill_bullet_failures = [
        item.slug
        for item in skill_scores
        if int(item.metrics.get("prompts", {}).get("bullets", 0)) < skill_prompt_bullets_min
    ]
    checks.append(
        {
            "name": "skill_prompt_bullet_regression",
            "passed": len(skill_bullet_failures) == 0,
            "failed_count": len(skill_bullet_failures),
            "threshold": skill_prompt_bullets_min,
            "failed_examples": skill_bullet_failures[:20],
        }
    )

    agent_bullet_failures = [
        item.slug
        for item in agent_scores
        if int(item.metrics.get("prompts", {}).get("bullets", 0)) < agent_prompt_bullets_min
    ]
    checks.append(
        {
            "name": "agent_prompt_bullet_regression",
            "passed": len(agent_bullet_failures) == 0,
            "failed_count": len(agent_bullet_failures),
            "threshold": agent_prompt_bullets_min,
            "failed_examples": agent_bullet_failures[:20],
        }
    )

    if skill_ref_slug:
        skill_slug_ref_failures = [
            item.slug
            for item in skill_scores
            if not bool(item.metrics.get("prompts", {}).get("references_slug", False))
        ]
        checks.append(
            {
                "name": "skill_prompt_slug_reference_regression",
                "passed": len(skill_slug_ref_failures) == 0,
                "failed_count": len(skill_slug_ref_failures),
                "failed_examples": skill_slug_ref_failures[:20],
            }
        )

    if agent_ref_slug:
        agent_slug_ref_failures = [
            item.slug
            for item in agent_scores
            if not bool(item.metrics.get("prompts", {}).get("references_slug", False))
        ]
        checks.append(
            {
                "name": "agent_prompt_slug_reference_regression",
                "passed": len(agent_slug_ref_failures) == 0,
                "failed_count": len(agent_slug_ref_failures),
                "failed_examples": agent_slug_ref_failures[:20],
            }
        )

    status = "pass" if all(check["passed"] for check in checks) else "fail"
    return {"status": status, "checks": checks}


def build_coverage_checks(
    cases_file: Path,
    skills: list[ArtifactScore],
    agents: list[ArtifactScore],
) -> dict:
    cases = read_json_list(cases_file)
    skill_slugs = {item.slug for item in skills}
    agent_slugs = {item.slug for item in agents}

    evaluated_cases: list[dict] = []
    for case in cases:
        case_id = str(case.get("id", "unknown-case"))
        required_skills = case.get("required_skill_prefixes", [])
        required_agents = case.get("required_agent_fragments", [])
        if not isinstance(required_skills, list):
            required_skills = []
        if not isinstance(required_agents, list):
            required_agents = []

        missing_skills: list[str] = []
        for required in required_skills:
            matched = any(
                slug == required or slug.startswith(required) for slug in skill_slugs
            )
            if not matched:
                missing_skills.append(str(required))

        missing_agents: list[str] = []
        for required in required_agents:
            matched = any(
                slug == required or str(required) in slug for slug in agent_slugs
            )
            if not matched:
                missing_agents.append(str(required))

        passed = len(missing_skills) == 0 and len(missing_agents) == 0
        evaluated_cases.append(
            {
                "id": case_id,
                "description": case.get("description"),
                "passed": passed,
                "missing_skill_requirements": missing_skills,
                "missing_agent_requirements": missing_agents,
            }
        )

    status = "pass" if all(item["passed"] for item in evaluated_cases) else "fail"
    return {"status": status, "cases": evaluated_cases}


def serialize_scores(scores: list[ArtifactScore]) -> list[dict]:
    return [
        {
            "kind": item.kind,
            "slug": item.slug,
            "path": item.path,
            "total_score": item.total_score,
            "scores": item.scores,
            "pass_thresholds": item.pass_thresholds,
            "findings": item.findings,
            "metrics": item.metrics,
        }
        for item in scores
    ]


def build_rankings(scores: list[ArtifactScore], top_k: int, bottom_k: int) -> dict[str, list[dict]]:
    sorted_scores = sorted(scores, key=lambda item: (-item.total_score, item.slug))
    top = sorted_scores[: max(top_k, 0)]
    bottom = list(sorted(sorted_scores[-max(bottom_k, 0) :], key=lambda item: (item.total_score, item.slug)))

    def compact(items: list[ArtifactScore]) -> list[dict]:
        return [
            {
                "slug": item.slug,
                "total_score": item.total_score,
                "scores": item.scores,
                "pass_thresholds": item.pass_thresholds,
            }
            for item in items
        ]

    return {"top": compact(top), "bottom": compact(bottom), "full": compact(sorted_scores)}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_json_list(path: Path, payload: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_domain_kpis(skills: list[ArtifactScore], agents: list[ArtifactScore]) -> list[dict]:
    grouped: dict[str, dict[str, Any]] = {}
    for item in [*skills, *agents]:
        domain = str(item.metrics.get("domain") or "unknown")
        bucket = grouped.setdefault(
            domain,
            {
                "domain": domain,
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skills": 0,
                "agents": 0,
                "score_sum": 0.0,
            },
        )
        bucket["total"] += 1
        if item.pass_thresholds:
            bucket["passed"] += 1
        else:
            bucket["failed"] += 1
        if item.kind == "skill":
            bucket["skills"] += 1
        elif item.kind == "agent":
            bucket["agents"] += 1
        bucket["score_sum"] += item.total_score

    results: list[dict] = []
    for bucket in grouped.values():
        total = int(bucket["total"]) or 1
        average_score = round(float(bucket["score_sum"]) / float(total), 2)
        pass_rate = round((float(bucket["passed"]) / float(total)) * 100.0, 2)
        results.append(
            {
                "domain": bucket["domain"],
                "total": bucket["total"],
                "passed": bucket["passed"],
                "failed": bucket["failed"],
                "skills": bucket["skills"],
                "agents": bucket["agents"],
                "average_score": average_score,
                "pass_rate_percent": pass_rate,
            }
        )
    results.sort(key=lambda item: (-item["average_score"], item["domain"]))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run benchmark suite for skills and agents with scoring, regressions, and coverage checks."
    )
    parser.add_argument("--skills-root", default="skills", help="Canonical skills directory.")
    parser.add_argument("--agents-root", default="agents", help="Canonical agents directory.")
    parser.add_argument("--suite-file", default="benchmarks/suite.json", help="Benchmark suite config JSON.")
    parser.add_argument(
        "--cases-file",
        default="benchmarks/cases/real-world-process-cases.json",
        help="Real-world benchmark cases JSON.",
    )
    parser.add_argument("--output-file", default="catalog/benchmark-results.json", help="Main benchmark output JSON.")
    parser.add_argument(
        "--skills-ranking-file",
        default="catalog/skill-quality-ranking.json",
        help="Skill ranking output JSON.",
    )
    parser.add_argument(
        "--agents-ranking-file",
        default="catalog/agent-quality-ranking.json",
        help="Agent ranking output JSON.",
    )
    parser.add_argument(
        "--history-file",
        default="catalog/benchmark-history.json",
        help="Historical benchmark timeline JSON (list of snapshots).",
    )
    parser.add_argument(
        "--history-limit",
        type=int,
        default=240,
        help="Maximum number of snapshots to keep in benchmark history.",
    )
    parser.add_argument(
        "--no-history",
        action="store_true",
        help="Disable benchmark history write for this run.",
    )
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if any benchmark gate fails.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    skills_root = (base / args.skills_root).resolve()
    agents_root = (base / args.agents_root).resolve()
    suite_file = (base / args.suite_file).resolve()
    cases_file = (base / args.cases_file).resolve()
    output_file = (base / args.output_file).resolve()
    skills_ranking_file = (base / args.skills_ranking_file).resolve()
    agents_ranking_file = (base / args.agents_ranking_file).resolve()
    history_file = (base / args.history_file).resolve()

    suite = read_json(suite_file)
    if not suite:
        raise SystemExit(f"Suite file is missing or invalid: {suite_file}")

    weights = suite.get("weights", {})
    if not isinstance(weights, dict):
        raise SystemExit("Invalid suite config: 'weights' must be an object.")

    skill_scores = score_all_skills(skills_root, suite=suite)
    agent_scores = score_all_agents(agents_root, suite=suite)

    skill_failed = [item for item in skill_scores if not item.pass_thresholds]
    agent_failed = [item for item in agent_scores if not item.pass_thresholds]

    ranking_cfg = suite.get("ranking", {})
    top_k = int(ranking_cfg.get("top_k", 15))
    bottom_k = int(ranking_cfg.get("bottom_k", 10))

    skill_rankings = build_rankings(skill_scores, top_k=top_k, bottom_k=bottom_k)
    agent_rankings = build_rankings(agent_scores, top_k=top_k, bottom_k=bottom_k)

    regression = build_regression_checks(skill_scores, agent_scores, suite=suite)
    coverage = build_coverage_checks(cases_file=cases_file, skills=skill_scores, agents=agent_scores)

    total_artifacts = len(skill_scores) + len(agent_scores)
    passed_artifacts = (len(skill_scores) - len(skill_failed)) + (len(agent_scores) - len(agent_failed))
    pass_rate = round((passed_artifacts / float(total_artifacts)) * 100.0, 2) if total_artifacts else 0.0
    avg_all = average_artifact_score([*skill_scores, *agent_scores])
    avg_skills = average_artifact_score(skill_scores)
    avg_agents = average_artifact_score(agent_scores)

    status = "healthy"
    if skill_failed or agent_failed or regression["status"] != "pass" or coverage["status"] != "pass":
        status = "needs_attention"

    summary = {
        "status": status,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_total": len(skill_scores),
        "skills_passed": len(skill_scores) - len(skill_failed),
        "skills_failed": len(skill_failed),
        "agents_total": len(agent_scores),
        "agents_passed": len(agent_scores) - len(agent_failed),
        "agents_failed": len(agent_failed),
        "overall_pass_rate_percent": pass_rate,
        "average_score_all": avg_all,
        "average_score_skills": avg_skills,
        "average_score_agents": avg_agents,
    }

    executive = {
        "domain_kpis": build_domain_kpis(skill_scores, agent_scores),
    }

    result_payload = {
        "suite": {
            "suite_version": suite.get("suite_version"),
            "name": suite.get("name"),
            "weights": suite.get("weights"),
            "thresholds": suite.get("thresholds"),
            "regression": suite.get("regression"),
            "ranking": suite.get("ranking"),
        },
        "summary": summary,
        "regression": regression,
        "coverage": coverage,
        "executive": executive,
        "rankings": {
            "skills_top": skill_rankings["top"],
            "skills_bottom": skill_rankings["bottom"],
            "agents_top": agent_rankings["top"],
            "agents_bottom": agent_rankings["bottom"],
        },
        "artifacts": {
            "skills": serialize_scores(skill_scores),
            "agents": serialize_scores(agent_scores),
            "skills_failed": serialize_scores(skill_failed),
            "agents_failed": serialize_scores(agent_failed),
        },
    }

    write_json(output_file, result_payload)
    write_json(
        skills_ranking_file,
        {
            "generated_at": summary["generated_at"],
            "status": summary["status"],
            "items": skill_rankings["full"],
        },
    )
    write_json(
        agents_ranking_file,
        {
            "generated_at": summary["generated_at"],
            "status": summary["status"],
            "items": agent_rankings["full"],
        },
    )

    if not args.no_history:
        history = read_json_list(history_file)
        snapshot = {
            "generated_at": summary["generated_at"],
            "status": summary["status"],
            "skills_total": summary["skills_total"],
            "skills_passed": summary["skills_passed"],
            "agents_total": summary["agents_total"],
            "agents_passed": summary["agents_passed"],
            "overall_pass_rate_percent": summary["overall_pass_rate_percent"],
            "average_score_all": summary["average_score_all"],
            "average_score_skills": summary["average_score_skills"],
            "average_score_agents": summary["average_score_agents"],
            "regression_status": regression["status"],
            "coverage_status": coverage["status"],
        }
        history.append(snapshot)
        history_limit = max(int(args.history_limit), 1)
        if len(history) > history_limit:
            history = history[-history_limit:]
        write_json_list(history_file, history)

    print(f"Wrote {output_file}")
    print(f"Wrote {skills_ranking_file}")
    print(f"Wrote {agents_ranking_file}")
    if not args.no_history:
        print(f"Wrote {history_file}")
    print("")
    print(f"Benchmark status: {status}")
    print(
        f"Skills passed: {summary['skills_passed']}/{summary['skills_total']} | "
        f"Agents passed: {summary['agents_passed']}/{summary['agents_total']}"
    )
    print(f"Regression status: {regression['status']}")
    print(f"Coverage status: {coverage['status']}")

    if args.strict and status != "healthy":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
