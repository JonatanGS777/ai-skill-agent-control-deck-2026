#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path


def read_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return payload
    except Exception:
        pass
    return {}


def to_float(value: object) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def to_int(value: object) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def sort_by_score(items: list[dict]) -> list[dict]:
    return sorted(
        items,
        key=lambda item: (-to_float(item.get("total_score", 0.0)), str(item.get("slug", ""))),
    )


def score_cell(item: dict, key: str) -> str:
    scores = item.get("scores", {})
    if not isinstance(scores, dict):
        return "0.0"
    return f"{to_float(scores.get(key, 0.0)):.1f}"


def slug_to_label(slug: str) -> str:
    return slug.replace("-", " ").strip().title()


def build_rank_rows(items: list[dict], limit: int) -> str:
    rows: list[str] = []
    for idx, item in enumerate(items[:limit], start=1):
        slug = html.escape(str(item.get("slug", "unknown")))
        label = html.escape(slug_to_label(str(item.get("slug", "unknown"))))
        total = f"{to_float(item.get('total_score', 0.0)):.1f}"
        logic = score_cell(item, "logic")
        clarity = score_cell(item, "clarity")
        security = score_cell(item, "security")
        utility = score_cell(item, "utility")
        passed = bool(item.get("pass_thresholds", False))
        status = "PASS" if passed else "FAIL"
        status_cls = "status-pass" if passed else "status-fail"

        rows.append(
            "<tr>"
            f"<td>{idx}</td>"
            f"<td><div class='artifact-name'>{label}</div><code>{slug}</code></td>"
            f"<td><strong>{total}</strong></td>"
            f"<td>{logic}</td>"
            f"<td>{clarity}</td>"
            f"<td>{security}</td>"
            f"<td>{utility}</td>"
            f"<td><span class='status-chip {status_cls}'>{status}</span></td>"
            "</tr>"
        )

    if not rows:
        rows.append("<tr><td colspan='8'>No ranking data available yet.</td></tr>")
    return "\n".join(rows)


def build_domain_rows(domain_kpis: list[dict]) -> str:
    rows: list[str] = []
    ordered = sorted(
        domain_kpis,
        key=lambda item: (-to_float(item.get("average_score", 0.0)), str(item.get("domain", ""))),
    )

    for item in ordered:
        domain = html.escape(str(item.get("domain", "unknown")))
        total = to_int(item.get("total", 0))
        skills = to_int(item.get("skills", 0))
        agents = to_int(item.get("agents", 0))
        avg = f"{to_float(item.get('average_score', 0.0)):.2f}"
        pass_rate_num = max(0.0, min(100.0, to_float(item.get("pass_rate_percent", 0.0))))
        pass_rate = f"{pass_rate_num:.2f}%"

        rows.append(
            "<tr>"
            f"<td>{domain}</td>"
            f"<td>{total}</td>"
            f"<td>{skills}</td>"
            f"<td>{agents}</td>"
            f"<td><strong>{avg}</strong></td>"
            f"<td><div class='meter'><span style='width:{pass_rate_num:.2f}%'></span></div><small>{pass_rate}</small></td>"
            "</tr>"
        )

    if not rows:
        rows.append("<tr><td colspan='6'>No domain KPI data available yet.</td></tr>")
    return "\n".join(rows)


def build_release_rows(releases: list[dict], limit: int) -> str:
    rows: list[str] = []
    ordered = list(releases)
    ordered.sort(key=lambda item: str(item.get("released_at", "")), reverse=True)

    for item in ordered[:limit]:
        version = html.escape(str(item.get("version", "n/a")))
        channel = html.escape(str(item.get("channel", "stable")))
        quality = html.escape(str(item.get("repository_quality_status", "unknown")))
        benchmark = html.escape(str(item.get("benchmark_status", "unknown")))
        released_at = html.escape(str(item.get("released_at", "")))
        path = html.escape(str(item.get("path", "")))

        rows.append(
            "<tr>"
            f"<td><strong>{version}</strong></td>"
            f"<td><span class='channel-chip'>{channel}</span></td>"
            f"<td>{quality}</td>"
            f"<td>{benchmark}</td>"
            f"<td><code>{released_at}</code></td>"
            f"<td><code>{path}</code></td>"
            "</tr>"
        )

    if not rows:
        rows.append("<tr><td colspan='6'>No releases found yet. Run <code>make release-auto</code>.</td></tr>")
    return "\n".join(rows)


def status_variant(status: str) -> str:
    value = status.strip().lower()
    if value == "healthy":
        return "badge-healthy"
    if value in {"pass", "ok"}:
        return "badge-pass"
    if value in {"fail", "failed"}:
        return "badge-fail"
    return "badge-neutral"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build repository documentation portal page.")
    parser.add_argument("--benchmark-file", default="catalog/benchmark-results.json", help="Benchmark JSON path")
    parser.add_argument("--skill-ranking-file", default="catalog/skill-quality-ranking.json", help="Skill ranking JSON path")
    parser.add_argument("--agent-ranking-file", default="catalog/agent-quality-ranking.json", help="Agent ranking JSON path")
    parser.add_argument("--release-index-file", default="catalog/releases/releases-index.json", help="Release index JSON path")
    parser.add_argument("--output-file", default="docs/portal/index.html", help="Output HTML file")
    parser.add_argument("--top-k", type=int, default=12, help="Top rows for ranking tables")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    benchmark_file = (base / args.benchmark_file).resolve()
    skill_ranking_file = (base / args.skill_ranking_file).resolve()
    agent_ranking_file = (base / args.agent_ranking_file).resolve()
    release_index_file = (base / args.release_index_file).resolve()
    output_file = (base / args.output_file).resolve()

    benchmark = read_json(benchmark_file)
    skill_ranking = read_json(skill_ranking_file)
    agent_ranking = read_json(agent_ranking_file)
    release_index = read_json(release_index_file)

    summary = benchmark.get("summary", {}) if isinstance(benchmark.get("summary"), dict) else {}
    executive = benchmark.get("executive", {}) if isinstance(benchmark.get("executive"), dict) else {}
    domain_kpis = executive.get("domain_kpis", []) if isinstance(executive.get("domain_kpis"), list) else []

    skill_items = skill_ranking.get("items", []) if isinstance(skill_ranking.get("items"), list) else []
    agent_items = agent_ranking.get("items", []) if isinstance(agent_ranking.get("items"), list) else []
    release_items = release_index.get("releases", []) if isinstance(release_index.get("releases"), list) else []

    top_skills = sort_by_score(skill_items)
    top_agents = sort_by_score(agent_items)

    generated_at = datetime.now(timezone.utc).isoformat()
    quality_status = str(summary.get("status", "unknown"))
    quality_status_safe = html.escape(quality_status)
    quality_badge = status_variant(quality_status)

    skills_total = to_int(summary.get("skills_total", len(skill_items)))
    skills_failed = to_int(summary.get("skills_failed", 0))
    agents_total = to_int(summary.get("agents_total", len(agent_items)))
    agents_failed = to_int(summary.get("agents_failed", 0))
    pass_rate = f"{to_float(summary.get('overall_pass_rate_percent', 0.0)):.2f}%"
    avg_score = f"{to_float(summary.get('average_score_all', 0.0)):.2f}"

    release_count = len(release_items)
    latest_release = "-"
    if release_items:
        latest = sorted(release_items, key=lambda item: str(item.get("released_at", "")), reverse=True)[0]
        latest_release = str(latest.get("version", "-"))
    latest_release_safe = html.escape(latest_release)

    html_body = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Repository Control Deck 2026</title>
  <style>
    :root {{
      --bg: #f5f8fb;
      --ink: #081824;
      --muted: #4a6474;
      --panel: rgba(255, 255, 255, 0.84);
      --line: #bdd0dc;
      --line-strong: #8aa4b4;
      --accent: #0b9ad1;
      --accent-strong: #0876a8;
      --accent-soft: #e3f5fb;
      --signal: #ff6b3d;
      --signal-soft: #ffe8df;
      --ok: #0f7d42;
      --ok-soft: #e9f9ef;
      --warn: #9b5f00;
      --warn-soft: #fff4de;
      --fail: #b3261e;
      --fail-soft: #ffe9e8;
      --shadow: 0 24px 60px rgba(8, 24, 36, 0.1);
      --radius-xl: 22px;
      --radius-lg: 16px;
      --radius-md: 12px;
    }}

    * {{ box-sizing: border-box; }}

    html, body {{ margin: 0; padding: 0; }}

    body {{
      font-family: "Space Grotesk", "Sora", "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(1200px 500px at 100% -10%, #d9f4ff 0%, transparent 65%),
        radial-gradient(900px 460px at -15% 8%, #ffe8df 0%, transparent 62%),
        var(--bg);
      min-height: 100vh;
      line-height: 1.4;
    }}

    code, pre {{
      font-family: "JetBrains Mono", "IBM Plex Mono", "SFMono-Regular", Menlo, monospace;
    }}

    .wrap {{
      width: min(1240px, 92vw);
      margin: 0 auto;
      padding: 22px 0 42px;
      position: relative;
      z-index: 1;
    }}

    .nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
    }}

    .brand {{
      font-weight: 700;
      letter-spacing: 0.03em;
      font-size: 13px;
      text-transform: uppercase;
      color: var(--accent-strong);
    }}

    .nav-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .nav-links a {{
      text-decoration: none;
      color: var(--ink);
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.72);
      border-radius: 999px;
      padding: 6px 12px;
      font-size: 12px;
      transition: all .22s ease;
    }}

    .nav-links a:hover {{
      border-color: var(--accent);
      background: var(--accent-soft);
      transform: translateY(-1px);
    }}

    .theme-toggle {{
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.72);
      color: var(--ink);
      border-radius: 999px;
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.02em;
      cursor: pointer;
      transition: all .22s ease;
    }}

    .theme-toggle:hover {{
      border-color: var(--accent);
      background: var(--accent-soft);
      transform: translateY(-1px);
    }}

    .hero {{
      border: 1px solid var(--line);
      border-radius: var(--radius-xl);
      background: linear-gradient(135deg, rgba(255,255,255,0.94), rgba(247,252,255,0.82));
      backdrop-filter: blur(10px);
      box-shadow: var(--shadow);
      overflow: hidden;
      position: relative;
      animation: fadeUp .55s ease both;
    }}

    .hero::before {{
      content: "";
      position: absolute;
      width: 420px;
      height: 420px;
      right: -160px;
      top: -220px;
      background: radial-gradient(circle at center, rgba(11,154,209,0.24), rgba(11,154,209,0));
      pointer-events: none;
    }}

    .hero-grid {{
      display: grid;
      grid-template-columns: 1.25fr .95fr;
      gap: 18px;
      padding: 26px;
    }}

    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--accent-strong);
      font-weight: 700;
      margin-bottom: 10px;
    }}

    .eyebrow::before {{
      content: "";
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--signal);
      box-shadow: 0 0 0 8px rgba(255, 107, 61, 0.15);
      animation: pulse 2.2s infinite;
    }}

    h1 {{
      margin: 0;
      font-family: "Sora", "Space Grotesk", "Avenir Next", sans-serif;
      font-size: clamp(30px, 5vw, 52px);
      line-height: 1.02;
      letter-spacing: -0.02em;
      max-width: 17ch;
    }}

    .title-accent {{
      color: var(--accent-strong);
    }}

    .hero p {{
      margin: 14px 0 0;
      color: var(--muted);
      font-size: clamp(14px, 1.4vw, 17px);
      max-width: 62ch;
    }}

    .chip-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 16px;
    }}

    .chip {{
      border-radius: 999px;
      padding: 6px 11px;
      font-size: 12px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.78);
    }}

    .hero-card {{
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.72);
      border-radius: var(--radius-lg);
      padding: 14px;
      display: grid;
      gap: 10px;
      align-content: start;
    }}

    .hero-card h3 {{
      margin: 0;
      font-size: 15px;
      letter-spacing: 0.01em;
    }}

    .hero-card ul {{
      margin: 0;
      padding-left: 16px;
      color: var(--muted);
      display: grid;
      gap: 6px;
      font-size: 13px;
    }}

    .quick-box {{
      border-radius: 12px;
      background: #091722;
      color: #dff3ff;
      border: 1px solid #203344;
      padding: 10px;
      overflow-x: auto;
      font-size: 12px;
    }}

    .kpi-grid {{
      margin-top: 16px;
      display: grid;
      grid-template-columns: repeat(6, minmax(140px, 1fr));
      gap: 10px;
      animation: fadeUp .7s ease both;
    }}

    .kpi {{
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      padding: 11px;
      background: var(--panel);
      backdrop-filter: blur(6px);
      min-height: 84px;
    }}

    .kpi-label {{
      margin: 0;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted);
    }}

    .kpi-value {{
      margin: 5px 0 0;
      font-size: 25px;
      line-height: 1;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}

    .kpi-meta {{
      margin: 6px 0 0;
      font-size: 12px;
      color: var(--muted);
    }}

    .quality-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 999px;
      font-size: 11px;
      padding: 4px 10px;
      border: 1px solid transparent;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      font-weight: 700;
      margin-top: 6px;
      width: fit-content;
    }}

    .badge-healthy {{ background: var(--ok-soft); color: var(--ok); border-color: #b9e8ca; }}
    .badge-pass {{ background: var(--accent-soft); color: var(--accent-strong); border-color: #acdced; }}
    .badge-fail {{ background: var(--fail-soft); color: var(--fail); border-color: #f2bdb9; }}
    .badge-neutral {{ background: #eef3f6; color: #49606e; border-color: #ccd8df; }}

    section {{
      margin-top: 14px;
      border: 1px solid var(--line);
      border-radius: var(--radius-lg);
      background: var(--panel);
      backdrop-filter: blur(7px);
      box-shadow: 0 14px 30px rgba(8, 24, 36, 0.06);
      animation: fadeUp .8s ease both;
    }}

    .section-head {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
      padding: 14px 16px 10px;
      border-bottom: 1px solid var(--line);
    }}

    .section-head h2 {{
      margin: 0;
      font-size: clamp(18px, 2vw, 24px);
      letter-spacing: -0.02em;
    }}

    .section-sub {{
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      max-width: 62ch;
    }}

    .section-body {{
      padding: 14px 16px 16px;
    }}

    .quick-grid {{
      display: grid;
      grid-template-columns: 1.1fr .9fr;
      gap: 12px;
    }}

    pre {{
      margin: 0;
      background: #091722;
      color: #dff3ff;
      border: 1px solid #203344;
      border-radius: 12px;
      padding: 12px;
      overflow-x: auto;
      font-size: 12px;
      line-height: 1.55;
    }}

    .flow-list {{
      margin: 0;
      padding-left: 18px;
      display: grid;
      gap: 8px;
      color: var(--muted);
    }}

    .docs-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(180px, 1fr));
      gap: 10px;
    }}

    .doc-card {{
      text-decoration: none;
      color: inherit;
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 12px;
      background: rgba(255,255,255,.78);
      transition: transform .22s ease, border-color .22s ease, background .22s ease;
      min-height: 118px;
      display: grid;
      align-content: start;
      gap: 6px;
    }}

    .doc-card strong {{
      letter-spacing: 0.01em;
      font-size: 14px;
    }}

    .doc-card span {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
    }}

    .doc-card:hover {{
      transform: translateY(-2px);
      border-color: var(--accent);
      background: var(--accent-soft);
    }}

    .pipeline {{
      display: grid;
      grid-template-columns: repeat(7, minmax(120px, 1fr));
      gap: 8px;
    }}

    .step {{
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 10px;
      background: rgba(255,255,255,.78);
    }}

    .step small {{
      display: block;
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: .05em;
      margin-bottom: 4px;
    }}

    .step strong {{
      font-size: 13px;
      line-height: 1.35;
    }}

    .dual {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}

    .table-wrap {{
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: rgba(255,255,255,.82);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      min-width: 700px;
    }}

    thead th {{
      position: sticky;
      top: 0;
      background: #eff6fa;
      color: #2d4758;
      text-align: left;
      padding: 8px 8px;
      border-bottom: 1px solid var(--line-strong);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: .05em;
      z-index: 1;
    }}

    tbody td {{
      border-bottom: 1px solid var(--line);
      padding: 8px;
      vertical-align: top;
    }}

    tbody tr:hover {{
      background: #f1f8fc;
    }}

    .artifact-name {{
      font-weight: 700;
      margin-bottom: 3px;
      line-height: 1.25;
    }}

    .status-chip {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 999px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: .05em;
      padding: 4px 8px;
      border: 1px solid transparent;
      text-transform: uppercase;
    }}

    .status-pass {{ background: var(--ok-soft); color: var(--ok); border-color: #b9e8ca; }}
    .status-fail {{ background: var(--fail-soft); color: var(--fail); border-color: #f2bdb9; }}

    .channel-chip {{
      display: inline-flex;
      padding: 4px 8px;
      border-radius: 999px;
      border: 1px solid #f3c9b9;
      background: var(--signal-soft);
      color: #a04728;
      text-transform: uppercase;
      font-size: 10px;
      letter-spacing: .05em;
      font-weight: 700;
    }}

    .meter {{
      width: 100%;
      height: 6px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #f7fbfd;
      overflow: hidden;
      margin-bottom: 4px;
    }}

    .meter span {{
      display: block;
      height: 100%;
      background: linear-gradient(90deg, #1eb572, #0b9ad1);
    }}

    .tri-grid {{
      display: grid;
      grid-template-columns: 1.2fr .8fr;
      gap: 12px;
    }}

    footer {{
      margin-top: 12px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.74);
      border-radius: 12px;
      padding: 10px 12px;
      color: var(--muted);
      font-size: 12px;
      display: flex;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
    }}

    html[data-theme="dark"] {{
      color-scheme: dark;
      --bg: #08131c;
      --ink: #e4edf5;
      --muted: #9cb2c3;
      --panel: rgba(11, 22, 31, 0.84);
      --line: #244051;
      --line-strong: #335469;
      --accent: #22c1ff;
      --accent-strong: #8bdfff;
      --accent-soft: rgba(34, 193, 255, 0.13);
      --signal: #ff8b63;
      --signal-soft: rgba(255, 139, 99, 0.12);
      --ok: #52d68f;
      --ok-soft: rgba(82, 214, 143, 0.14);
      --fail: #ff8a82;
      --fail-soft: rgba(255, 138, 130, 0.13);
      --shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
    }}

    html[data-theme="dark"] body {{
      background:
        radial-gradient(1200px 500px at 100% -10%, rgba(34,193,255,0.16) 0%, transparent 65%),
        radial-gradient(900px 460px at -15% 8%, rgba(255,139,99,0.12) 0%, transparent 62%),
        var(--bg);
    }}

    html[data-theme="dark"] .nav-links a,
    html[data-theme="dark"] .theme-toggle {{
      background: rgba(12, 26, 36, 0.72);
      color: var(--ink);
      border-color: var(--line);
    }}

    html[data-theme="dark"] .hero,
    html[data-theme="dark"] .kpi,
    html[data-theme="dark"] section,
    html[data-theme="dark"] .step,
    html[data-theme="dark"] .doc-card,
    html[data-theme="dark"] .table-wrap,
    html[data-theme="dark"] footer {{
      background: rgba(10, 20, 29, 0.78);
      border-color: var(--line);
    }}

    html[data-theme="dark"] .hero-card {{
      background: rgba(11, 23, 33, 0.78);
      border-color: var(--line);
    }}

    html[data-theme="dark"] .quick-box,
    html[data-theme="dark"] pre {{
      background: #06111a;
      color: #dbeeff;
      border-color: #1f394a;
    }}

    html[data-theme="dark"] thead th {{
      background: #10202c;
      color: #b6cfde;
      border-bottom-color: var(--line);
    }}

    html[data-theme="dark"] tbody tr:hover {{
      background: #0f1f2a;
    }}

    html[data-theme="dark"] .meter {{
      background: #0a1720;
      border-color: var(--line);
    }}

    html[data-theme="dark"] .badge-neutral {{
      background: rgba(178, 197, 210, 0.14);
      color: #b2c5d2;
      border-color: #3c5465;
    }}

    html[data-theme="dark"] .channel-chip {{
      border-color: #5a3b2f;
      background: rgba(255, 139, 99, 0.14);
      color: #ffc0ab;
    }}

    @media (max-width: 1120px) {{
      .kpi-grid {{ grid-template-columns: repeat(3, minmax(120px, 1fr)); }}
      .docs-grid {{ grid-template-columns: repeat(2, minmax(180px, 1fr)); }}
      .pipeline {{ grid-template-columns: repeat(4, minmax(120px, 1fr)); }}
    }}

    @media (max-width: 900px) {{
      .hero-grid,
      .quick-grid,
      .dual,
      .tri-grid {{
        grid-template-columns: 1fr;
      }}
      .hero {{ border-radius: 16px; }}
    }}

    @media (max-width: 640px) {{
      .wrap {{ width: min(1240px, 95vw); }}
      .kpi-grid {{ grid-template-columns: repeat(2, minmax(120px, 1fr)); }}
      .docs-grid {{ grid-template-columns: 1fr; }}
      .pipeline {{ grid-template-columns: repeat(2, minmax(120px, 1fr)); }}
      .section-head {{ padding: 12px; }}
      .section-body {{ padding: 12px; }}
      h1 {{ max-width: 100%; }}
    }}

    @keyframes pulse {{
      0% {{ transform: scale(1); opacity: .9; }}
      70% {{ transform: scale(1.08); opacity: .4; }}
      100% {{ transform: scale(1); opacity: .9; }}
    }}

    @keyframes fadeUp {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <header class=\"nav\">
      <div class=\"brand\">Repository Presentation 2026</div>
      <nav class=\"nav-links\">
        <a href=\"#quickstart\">Quickstart</a>
        <a href=\"#docs\">Docs</a>
        <a href=\"#pipeline\">Pipeline</a>
        <a href=\"#rankings\">Rankings</a>
        <a href=\"#ops\">Operations</a>
      </nav>
      <button id=\"themeToggle\" class=\"theme-toggle\" type=\"button\" aria-label=\"Toggle dark mode\" aria-pressed=\"false\">Dark</button>
    </header>

    <section class=\"hero\">
      <div class=\"hero-grid\">
        <div>
          <div class=\"eyebrow\">Live Quality Deck</div>
          <h1>Your AI Skill + Agent <span class=\"title-accent\">Control Deck</span></h1>
          <p>
            A focused presentation layer for benchmark health, release readiness, and contribution governance.
            The goal: make quality decisions faster and with zero ambiguity.
          </p>
          <div class=\"chip-row\">
            <span class=\"chip\">Benchmark-driven</span>
            <span class=\"chip\">Regression-safe</span>
            <span class=\"chip\">Release-ready</span>
            <span class=\"chip\">Governance-first</span>
          </div>
        </div>

        <aside class=\"hero-card\">
          <h3>Command Center</h3>
          <ul>
            <li>Run one command to validate full repository quality.</li>
            <li>Generate visual dashboard + docs portal in sync.</li>
            <li>Ship strict release bundles with changelog automation.</li>
          </ul>
          <div class=\"quick-box\"><code>make quality\nmake release-auto</code></div>
        </aside>
      </div>
    </section>

    <div class=\"kpi-grid\">
      <article class=\"kpi\">
        <p class=\"kpi-label\">Quality Status</p>
        <div class=\"quality-badge {quality_badge}\">{quality_status_safe}</div>
      </article>
      <article class=\"kpi\">
        <p class=\"kpi-label\">Skills</p>
        <p class=\"kpi-value\">{skills_total}</p>
        <p class=\"kpi-meta\">Failed: {skills_failed}</p>
      </article>
      <article class=\"kpi\">
        <p class=\"kpi-label\">Agents</p>
        <p class=\"kpi-value\">{agents_total}</p>
        <p class=\"kpi-meta\">Failed: {agents_failed}</p>
      </article>
      <article class=\"kpi\">
        <p class=\"kpi-label\">Pass Rate</p>
        <p class=\"kpi-value\">{pass_rate}</p>
        <p class=\"kpi-meta\">Global benchmark</p>
      </article>
      <article class=\"kpi\">
        <p class=\"kpi-label\">Average Score</p>
        <p class=\"kpi-value\">{avg_score}</p>
        <p class=\"kpi-meta\">Logic + Clarity + Security + Utility</p>
      </article>
      <article class=\"kpi\">
        <p class=\"kpi-label\">Release Stream</p>
        <p class=\"kpi-value\">{release_count}</p>
        <p class=\"kpi-meta\">Latest: {latest_release_safe}</p>
      </article>
    </div>

    <section id=\"quickstart\">
      <div class=\"section-head\">
        <h2>Quickstart Playbook</h2>
        <p class=\"section-sub\">Use this sequence to keep your repository healthy and release-ready every cycle.</p>
      </div>
      <div class=\"section-body quick-grid\">
        <pre><code>make quality
make dashboard
make docs-portal
make release-auto

# Optional explicit release
make release \\
  RELEASE_VERSION=v1.1.0 \\
  RELEASE_CHANNEL=stable \\
  RELEASE_NOTES="Quality uplift + new packs"</code></pre>
        <ol class=\"flow-list\">
          <li>Compile + semver + benchmark + catalog + dashboards.</li>
          <li>Review rankings and domain KPI deltas.</li>
          <li>Check governance docs and PR checklist alignment.</li>
          <li>Create strict release bundle + changelog entry.</li>
        </ol>
      </div>
    </section>

    <section id=\"docs\">
      <div class=\"section-head\">
        <h2>Documentation Hub</h2>
        <p class=\"section-sub\">Everything organized by onboarding, quality architecture, and contribution governance.</p>
      </div>
      <div class=\"section-body docs-grid\">
        <a class=\"doc-card\" href=\"../quickstart.md\"><strong>Quickstart Guide</strong><span>Bootstrapping and daily execution standards.</span></a>
        <a class=\"doc-card\" href=\"../patterns.md\"><strong>Patterns</strong><span>Reliable design and implementation patterns.</span></a>
        <a class=\"doc-card\" href=\"../anti-patterns.md\"><strong>Anti-patterns</strong><span>Risky shortcuts to avoid from day one.</span></a>
        <a class=\"doc-card\" href=\"../examples-top.md\"><strong>Top Examples</strong><span>Reference artifacts with high benchmark quality.</span></a>
        <a class=\"doc-card\" href=\"../governance/review-checklist.md\"><strong>Review Checklist</strong><span>PR review controls and approval criteria.</span></a>
        <a class=\"doc-card\" href=\"../governance/definition-of-done.md\"><strong>Definition of Done</strong><span>The exact gate before merge and release.</span></a>
        <a class=\"doc-card\" href=\"../../CONTRIBUTING.md\"><strong>Contributing</strong><span>Contribution workflow, coding standards, and validation.</span></a>
        <a class=\"doc-card\" href=\"../../.github/PULL_REQUEST_TEMPLATE.md\"><strong>PR Template</strong><span>Mandatory structure for clear, auditable pull requests.</span></a>
      </div>
    </section>

    <section id=\"pipeline\">
      <div class=\"section-head\">
        <h2>Quality Pipeline</h2>
        <p class=\"section-sub\">Top 7 impact path from correctness to publication.</p>
      </div>
      <div class=\"section-body pipeline\">
        <div class=\"step\"><small>01</small><strong>Benchmark Suite</strong></div>
        <div class=\"step\"><small>02</small><strong>Auto Evaluator</strong></div>
        <div class=\"step\"><small>03</small><strong>Regression Tests</strong></div>
        <div class=\"step\"><small>04</small><strong>Quality Ranking</strong></div>
        <div class=\"step\"><small>05</small><strong>Versioned Releases</strong></div>
        <div class=\"step\"><small>06</small><strong>Docs Portal</strong></div>
        <div class=\"step\"><small>07</small><strong>Contribution Governance</strong></div>
      </div>
    </section>

    <section id=\"rankings\">
      <div class=\"section-head\">
        <h2>Top Rankings</h2>
        <p class=\"section-sub\">Live quality leaderboard extracted from benchmark outputs.</p>
      </div>
      <div class=\"section-body dual\">
        <div>
          <h3>Top Skills</h3>
          <div class=\"table-wrap\">
            <table>
              <thead>
                <tr>
                  <th>#</th><th>Skill</th><th>Total</th><th>Logic</th><th>Clarity</th><th>Security</th><th>Utility</th><th>Status</th>
                </tr>
              </thead>
              <tbody>
                {build_rank_rows(top_skills, args.top_k)}
              </tbody>
            </table>
          </div>
        </div>

        <div>
          <h3>Top Agents</h3>
          <div class=\"table-wrap\">
            <table>
              <thead>
                <tr>
                  <th>#</th><th>Agent</th><th>Total</th><th>Logic</th><th>Clarity</th><th>Security</th><th>Utility</th><th>Status</th>
                </tr>
              </thead>
              <tbody>
                {build_rank_rows(top_agents, args.top_k)}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <section id=\"ops\">
      <div class=\"section-head\">
        <h2>Domain + Release Operations</h2>
        <p class=\"section-sub\">Execution KPIs by domain and audited release stream.</p>
      </div>
      <div class=\"section-body tri-grid\">
        <div>
          <h3>Domain KPIs</h3>
          <div class=\"table-wrap\">
            <table>
              <thead>
                <tr>
                  <th>Domain</th><th>Total</th><th>Skills</th><th>Agents</th><th>Avg Score</th><th>Pass Rate</th>
                </tr>
              </thead>
              <tbody>
                {build_domain_rows(domain_kpis)}
              </tbody>
            </table>
          </div>
        </div>

        <div>
          <h3>Release Stream</h3>
          <div class=\"table-wrap\">
            <table>
              <thead>
                <tr>
                  <th>Version</th><th>Channel</th><th>Repo Quality</th><th>Benchmark</th><th>Released At (UTC)</th><th>Bundle Path</th>
                </tr>
              </thead>
              <tbody>
                {build_release_rows(release_items, 15)}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <footer>
      <span>Generated at <code>{html.escape(generated_at)}</code></span>
      <span>Source: benchmark + catalog + releases index</span>
    </footer>
  </div>
  <script>
    (() => {{
      const storageKey = "control-deck-theme";
      const docEl = document.documentElement;
      const toggle = document.getElementById("themeToggle");
      if (!toggle) return;

      function applyTheme(theme) {{
        if (theme === "dark") {{
          docEl.setAttribute("data-theme", "dark");
          toggle.textContent = "Light";
          toggle.setAttribute("aria-pressed", "true");
        }} else {{
          docEl.removeAttribute("data-theme");
          toggle.textContent = "Dark";
          toggle.setAttribute("aria-pressed", "false");
        }}
      }}

      const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
      const stored = window.localStorage.getItem(storageKey);
      const initial = stored || (prefersDark ? "dark" : "light");
      applyTheme(initial === "dark" ? "dark" : "light");

      toggle.addEventListener("click", () => {{
        const active = docEl.getAttribute("data-theme") === "dark" ? "dark" : "light";
        const next = active === "dark" ? "light" : "dark";
        window.localStorage.setItem(storageKey, next);
        applyTheme(next);
      }});
    }})();
  </script>
</body>
</html>
"""

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html_body, encoding="utf-8")
    print(f"Wrote {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
