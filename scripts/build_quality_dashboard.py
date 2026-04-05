#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Cannot read JSON file: {path} ({exc})") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"Invalid JSON object in file: {path}")
    return payload


def read_json_list(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Cannot read JSON file: {path} ({exc})") from exc
    if not isinstance(payload, list):
        raise RuntimeError(f"Invalid JSON list in file: {path}")
    return [item for item in payload if isinstance(item, dict)]


def safe_float(value: object, default: float = 0.0) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return default


def build_entries(benchmark: dict, skills_index: dict, agents_index: dict) -> list[dict]:
    skill_map: dict[str, dict] = {}
    for item in skills_index.get("items", []):
        if isinstance(item, dict) and isinstance(item.get("slug"), str):
            skill_map[item["slug"]] = item

    agent_map: dict[str, dict] = {}
    for item in agents_index.get("items", []):
        if isinstance(item, dict) and isinstance(item.get("slug"), str):
            agent_map[item["slug"]] = item

    entries: list[dict] = []
    artifacts = benchmark.get("artifacts", {})
    if not isinstance(artifacts, dict):
        return entries

    for item in artifacts.get("skills", []):
        if not isinstance(item, dict):
            continue
        slug = item.get("slug")
        if not isinstance(slug, str):
            continue
        meta = skill_map.get(slug, {})
        scores = item.get("scores", {})
        if not isinstance(scores, dict):
            scores = {}
        entries.append(
            {
                "slug": slug,
                "kind": "skill",
                "score": round(safe_float(item.get("total_score")), 2),
                "logic": round(safe_float(scores.get("logic")), 2),
                "clarity": round(safe_float(scores.get("clarity")), 2),
                "security": round(safe_float(scores.get("security")), 2),
                "utility": round(safe_float(scores.get("utility")), 2),
                "pass": bool(item.get("pass_thresholds", False)),
                "domain": str(meta.get("domain") or "unknown"),
                "category": str(meta.get("quality_tier") or "unknown"),
                "path": str(item.get("path") or ""),
            }
        )

    for item in artifacts.get("agents", []):
        if not isinstance(item, dict):
            continue
        slug = item.get("slug")
        if not isinstance(slug, str):
            continue
        meta = agent_map.get(slug, {})
        scores = item.get("scores", {})
        if not isinstance(scores, dict):
            scores = {}
        entries.append(
            {
                "slug": slug,
                "kind": "agent",
                "score": round(safe_float(item.get("total_score")), 2),
                "logic": round(safe_float(scores.get("logic")), 2),
                "clarity": round(safe_float(scores.get("clarity")), 2),
                "security": round(safe_float(scores.get("security")), 2),
                "utility": round(safe_float(scores.get("utility")), 2),
                "pass": bool(item.get("pass_thresholds", False)),
                "domain": str(meta.get("agent_type") or "unknown"),
                "category": str(meta.get("logic_foundation_mode") or "unknown"),
                "path": str(item.get("path") or ""),
            }
        )

    entries.sort(key=lambda item: (-item["score"], item["slug"]))
    return entries


def average_score(items: list[dict]) -> float:
    if not items:
        return 0.0
    return round(sum(item.get("score", 0.0) for item in items) / len(items), 2)


def build_domain_kpis(entries: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for entry in entries:
        domain = str(entry.get("domain") or "unknown")
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
        if bool(entry.get("pass", False)):
            bucket["passed"] += 1
        else:
            bucket["failed"] += 1
        if entry.get("kind") == "skill":
            bucket["skills"] += 1
        elif entry.get("kind") == "agent":
            bucket["agents"] += 1
        bucket["score_sum"] += safe_float(entry.get("score"), 0.0)

    kpis: list[dict] = []
    for bucket in grouped.values():
        total = int(bucket["total"]) or 1
        kpis.append(
            {
                "domain": bucket["domain"],
                "total": bucket["total"],
                "passed": bucket["passed"],
                "failed": bucket["failed"],
                "skills": bucket["skills"],
                "agents": bucket["agents"],
                "average_score": round(float(bucket["score_sum"]) / float(total), 2),
                "pass_rate_percent": round((float(bucket["passed"]) / float(total)) * 100.0, 2),
            }
        )
    kpis.sort(key=lambda item: (-item["average_score"], item["domain"]))
    return kpis


def build_html(benchmark: dict, entries: list[dict], history: list[dict], domain_kpis: list[dict]) -> str:
    summary = benchmark.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    regression = benchmark.get("regression", {})
    if not isinstance(regression, dict):
        regression = {}
    coverage = benchmark.get("coverage", {})
    if not isinstance(coverage, dict):
        coverage = {}

    skills = [entry for entry in entries if entry["kind"] == "skill"]
    agents = [entry for entry in entries if entry["kind"] == "agent"]
    passed = [entry for entry in entries if entry["pass"]]
    failed = [entry for entry in entries if not entry["pass"]]

    dashboard_summary = {
        "status": summary.get("status", "unknown"),
        "generated_at": summary.get("generated_at", "unknown"),
        "total_entries": len(entries),
        "skills_total": len(skills),
        "agents_total": len(agents),
        "passed_total": len(passed),
        "failed_total": len(failed),
        "average_score_all": average_score(entries),
        "average_score_skills": average_score(skills),
        "average_score_agents": average_score(agents),
        "regression_status": regression.get("status", "unknown"),
        "coverage_status": coverage.get("status", "unknown"),
        "history_points": len(history),
    }

    payload = {
        "summary": dashboard_summary,
        "entries": entries,
        "history": history,
        "domain_kpis": domain_kpis,
    }
    payload_json = json.dumps(payload, ensure_ascii=False)

    template = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Repository Quality Control Deck 2026</title>
  <style>
    :root {
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
      --fail: #b3261e;
      --fail-soft: #ffe9e8;
      --shadow: 0 24px 60px rgba(8, 24, 36, 0.1);
      --radius-xl: 22px;
      --radius-lg: 16px;
      --radius-md: 12px;
    }

    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; }

    body {
      font-family: "Space Grotesk", "Sora", "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(1200px 500px at 100% -10%, #d9f4ff 0%, transparent 65%),
        radial-gradient(900px 460px at -15% 8%, #ffe8df 0%, transparent 62%),
        var(--bg);
      min-height: 100vh;
      line-height: 1.4;
    }

    code, pre {
      font-family: "JetBrains Mono", "IBM Plex Mono", "SFMono-Regular", Menlo, monospace;
    }

    .wrap {
      width: min(1280px, 92vw);
      margin: 0 auto;
      padding: 22px 0 40px;
    }

    .topbar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
    }

    .brand {
      font-weight: 700;
      letter-spacing: 0.03em;
      font-size: 13px;
      text-transform: uppercase;
      color: var(--accent-strong);
    }

    .nav {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .nav a {
      text-decoration: none;
      color: var(--ink);
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.72);
      border-radius: 999px;
      padding: 6px 12px;
      font-size: 12px;
      transition: all .2s ease;
    }

    .nav a:hover {
      border-color: var(--accent);
      background: var(--accent-soft);
      transform: translateY(-1px);
    }

    .theme-toggle {
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.72);
      color: var(--ink);
      border-radius: 999px;
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.02em;
      cursor: pointer;
      transition: all .2s ease;
    }

    .theme-toggle:hover {
      border-color: var(--accent);
      background: var(--accent-soft);
      transform: translateY(-1px);
    }

    .hero {
      border: 1px solid var(--line);
      border-radius: var(--radius-xl);
      background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(247,252,255,0.82));
      backdrop-filter: blur(10px);
      box-shadow: var(--shadow);
      overflow: hidden;
      position: relative;
      padding: 24px;
    }

    .hero::before {
      content: "";
      position: absolute;
      width: 420px;
      height: 420px;
      right: -180px;
      top: -240px;
      background: radial-gradient(circle at center, rgba(11,154,209,0.24), rgba(11,154,209,0));
      pointer-events: none;
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--accent-strong);
      font-weight: 700;
      margin-bottom: 10px;
    }

    .eyebrow::before {
      content: "";
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--signal);
      box-shadow: 0 0 0 8px rgba(255, 107, 61, 0.15);
    }

    .hero h1 {
      margin: 0;
      font-family: "Sora", "Space Grotesk", "Avenir Next", sans-serif;
      font-size: clamp(30px, 5vw, 46px);
      letter-spacing: -0.02em;
      line-height: 1.05;
      max-width: 18ch;
    }

    .hero h1 span {
      color: var(--accent-strong);
    }

    .hero p {
      margin: 12px 0 0;
      color: var(--muted);
      max-width: 72ch;
    }

    .hero-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
    }

    .hero-chip {
      border-radius: 999px;
      padding: 6px 11px;
      font-size: 12px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.78);
    }

    .grid {
      margin-top: 14px;
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 10px;
    }

    .card {
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      padding: 11px;
      background: var(--panel);
      backdrop-filter: blur(6px);
      min-height: 84px;
    }

    .k {
      margin: 0;
      font-size: 11px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .v {
      margin: 6px 0 0;
      font-size: 24px;
      line-height: 1;
      font-weight: 700;
      letter-spacing: -0.02em;
    }

    .sub {
      margin-top: 6px;
      font-size: 12px;
      color: var(--muted);
    }

    .quality-pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      font-weight: 700;
      border: 1px solid transparent;
      margin-top: 6px;
      width: fit-content;
    }

    .status-healthy { background: var(--ok-soft); color: var(--ok); border-color: #b9e8ca; }
    .status-pass { background: var(--accent-soft); color: var(--accent-strong); border-color: #acdced; }
    .status-fail { background: var(--fail-soft); color: var(--fail); border-color: #f2bdb9; }
    .status-neutral { background: #eef3f6; color: #49606e; border-color: #ccd8df; }

    .panel {
      margin-top: 12px;
      border: 1px solid var(--line);
      border-radius: var(--radius-lg);
      background: var(--panel);
      backdrop-filter: blur(7px);
      box-shadow: 0 14px 30px rgba(8, 24, 36, 0.06);
    }

    .panel-head {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
      padding: 14px 16px 10px;
      border-bottom: 1px solid var(--line);
    }

    .panel-head h2 {
      margin: 0;
      font-size: clamp(18px, 2vw, 24px);
      letter-spacing: -0.02em;
    }

    .panel-head p {
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      max-width: 64ch;
    }

    .panel-body {
      padding: 14px 16px 16px;
    }

    .executive-grid {
      display: grid;
      grid-template-columns: 1.5fr 1fr;
      gap: 12px;
    }

    .exec-panel {
      border: 1px solid var(--line);
      border-radius: 12px;
      background: rgba(255,255,255,0.82);
      padding: 10px;
    }

    .panel-title {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      margin-bottom: 8px;
      font-weight: 700;
    }

    #trendSvg {
      width: 100%;
      height: 220px;
      border-radius: 10px;
      background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
      border: 1px solid #edf2f8;
    }

    .legend {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 8px;
      font-size: 12px;
      color: var(--muted);
    }

    .legend .dot {
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 999px;
      margin-right: 4px;
    }

    .domain-table-wrap {
      max-height: 260px;
      overflow: auto;
      border: 1px solid #edf2f8;
      border-radius: 10px;
    }

    .domain-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      min-width: 430px;
    }

    .domain-table th,
    .domain-table td {
      padding: 8px;
      border-bottom: 1px solid #edf2f8;
      text-align: left;
      white-space: nowrap;
    }

    .domain-table th {
      position: sticky;
      top: 0;
      background: #f9fbff;
      color: #334155;
      z-index: 1;
      text-transform: uppercase;
      letter-spacing: .05em;
      font-size: 11px;
    }

    .filters {
      display: grid;
      grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
      gap: 10px;
      align-items: end;
    }

    label {
      display: block;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      margin-bottom: 5px;
    }

    input[type="text"], select {
      width: 100%;
      border-radius: 10px;
      border: 1px solid var(--line);
      padding: 9px 10px;
      font-size: 14px;
      color: var(--ink);
      background: #fff;
    }

    input[type="range"] {
      width: 100%;
      accent-color: var(--accent-strong);
    }

    .table-wrap {
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: rgba(255,255,255,.82);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      min-width: 980px;
    }

    thead th {
      text-align: left;
      position: sticky;
      top: 0;
      z-index: 1;
      background: #eff6fa;
      color: #2d4758;
      border-bottom: 1px solid var(--line-strong);
      padding: 9px 8px;
      white-space: nowrap;
      text-transform: uppercase;
      letter-spacing: .05em;
      font-size: 11px;
    }

    tbody td {
      border-bottom: 1px solid #edf2f8;
      padding: 9px 8px;
      vertical-align: top;
    }

    tbody tr:hover {
      background: #f1f8fc;
    }

    .slug {
      font-weight: 600;
      line-height: 1.3;
      word-break: break-word;
      max-width: 460px;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 4px 8px;
      border-radius: 999px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .04em;
      border: 1px solid #c8deea;
      background: #eaf6fc;
      color: #0a5271;
    }

    .status {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 4px 8px;
      border-radius: 999px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .05em;
      border: 1px solid transparent;
    }

    .status.pass {
      color: var(--ok);
      border-color: #b9e8ca;
      background: var(--ok-soft);
    }

    .status.fail {
      color: var(--fail);
      border-color: #f2bdb9;
      background: var(--fail-soft);
    }

    .footer {
      color: var(--muted);
      font-size: 12px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: space-between;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: rgba(255,255,255,.72);
      padding: 10px 12px;
    }

    html[data-theme="dark"] {
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
    }

    html[data-theme="dark"] body {
      background:
        radial-gradient(1200px 500px at 100% -10%, rgba(34,193,255,0.16) 0%, transparent 65%),
        radial-gradient(900px 460px at -15% 8%, rgba(255,139,99,0.12) 0%, transparent 62%),
        var(--bg);
    }

    html[data-theme="dark"] .nav a,
    html[data-theme="dark"] .theme-toggle {
      background: rgba(12, 26, 36, 0.72);
      color: var(--ink);
      border-color: var(--line);
    }

    html[data-theme="dark"] .hero,
    html[data-theme="dark"] .card,
    html[data-theme="dark"] .panel,
    html[data-theme="dark"] .exec-panel,
    html[data-theme="dark"] .table-wrap,
    html[data-theme="dark"] .footer {
      background: rgba(10, 20, 29, 0.78);
      border-color: var(--line);
    }

    html[data-theme="dark"] #trendSvg {
      background: linear-gradient(180deg, #0a1721 0%, #0d1c28 100%);
      border-color: var(--line);
    }

    html[data-theme="dark"] input[type="text"],
    html[data-theme="dark"] select {
      background: #0c1d2a;
      color: var(--ink);
      border-color: var(--line);
    }

    html[data-theme="dark"] .domain-table-wrap {
      border-color: var(--line);
    }

    html[data-theme="dark"] .domain-table th,
    html[data-theme="dark"] thead th {
      background: #10202c;
      color: #b6cfde;
      border-bottom-color: var(--line);
    }

    html[data-theme="dark"] tbody tr:hover {
      background: #0f1f2a;
    }

    html[data-theme="dark"] .chip {
      border-color: #2f5a70;
      background: rgba(11, 154, 209, 0.14);
      color: #9adfff;
    }

    @media (max-width: 1120px) {
      .grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
      .filters { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .executive-grid { grid-template-columns: 1fr; }
    }

    @media (max-width: 760px) {
      .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .filters { grid-template-columns: 1fr; }
      .hero { padding: 18px; }
      .hero h1 { font-size: 30px; }
    }

    @media (max-width: 520px) {
      .wrap { width: min(1280px, 95vw); }
      .grid { grid-template-columns: 1fr; }
      .panel-head, .panel-body { padding-left: 12px; padding-right: 12px; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <div class="brand">Quality Dashboard 2026</div>
      <nav class="nav">
        <a href="#overview">Overview</a>
        <a href="#executive">Executive</a>
        <a href="#filters">Filters</a>
        <a href="#leaderboard">Leaderboard</a>
      </nav>
      <button id="themeToggle" class="theme-toggle" type="button" aria-label="Toggle dark mode" aria-pressed="false">Dark</button>
    </header>

    <section class="hero" id="overview">
      <div class="eyebrow">Live Benchmark Monitor</div>
      <h1>Repository Quality <span>Control Deck</span></h1>
      <p>Interactive benchmark leaderboard for skills and agents with logic, clarity, security, and utility scoring.</p>
      <div class="hero-chips">
        <span class="hero-chip">Benchmark-driven</span>
        <span class="hero-chip">Regression-safe</span>
        <span class="hero-chip">Release-aware</span>
        <span class="hero-chip">Governance-ready</span>
      </div>
    </section>

    <div class="grid">
      <div class="card"><p class="k">Status</p><div id="statusValue" class="quality-pill status-neutral">-</div><div class="sub">Benchmark suite</div></div>
      <div class="card"><p class="k">Total</p><div class="v" id="totalValue">-</div><div class="sub">Artifacts scored</div></div>
      <div class="card"><p class="k">Skills</p><div class="v" id="skillsValue">-</div><div class="sub">Scored skills</div></div>
      <div class="card"><p class="k">Agents</p><div class="v" id="agentsValue">-</div><div class="sub">Scored agents</div></div>
      <div class="card"><p class="k">Pass / Fail</p><div class="v" id="passFailValue">-</div><div class="sub">Threshold checks</div></div>
      <div class="card"><p class="k">Average</p><div class="v" id="avgValue">-</div><div class="sub">Global score</div></div>
    </div>

    <section class="panel" id="executive">
      <div class="panel-head">
        <h2>Executive View</h2>
        <p>Historical trend lines and domain-level KPIs from the current benchmark run.</p>
      </div>
      <div class="panel-body">
        <div class="executive-grid">
          <div class="exec-panel">
            <div class="panel-title">Historical Trend (By Run)</div>
            <svg id="trendSvg" viewBox="0 0 920 220" preserveAspectRatio="none"></svg>
            <div class="legend">
              <span><span class="dot" style="background:#0b9ad1"></span>Average All</span>
              <span><span class="dot" style="background:#0f7d42"></span>Average Skills</span>
              <span><span class="dot" style="background:#ff6b3d"></span>Average Agents</span>
            </div>
          </div>
          <div class="exec-panel">
            <div class="panel-title">Domain KPIs (Current Run)</div>
            <div class="domain-table-wrap">
              <table class="domain-table">
                <thead>
                  <tr>
                    <th>Domain</th>
                    <th>Avg</th>
                    <th>Pass%</th>
                    <th>Total</th>
                    <th>S</th>
                    <th>A</th>
                  </tr>
                </thead>
                <tbody id="domainRows"></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="panel" id="filters">
      <div class="panel-head">
        <h2>Filter Controls</h2>
        <p>Slice leaderboard data by artifact type, status, domain, and score threshold.</p>
      </div>
      <div class="panel-body">
        <div class="filters">
          <div>
            <label for="search">Search</label>
            <input id="search" type="text" placeholder="slug, domain, category">
          </div>
          <div>
            <label for="kind">Kind</label>
            <select id="kind">
              <option value="all">All</option>
              <option value="skill">Skill</option>
              <option value="agent">Agent</option>
            </select>
          </div>
          <div>
            <label for="status">Status</label>
            <select id="status">
              <option value="all">All</option>
              <option value="pass">Pass</option>
              <option value="fail">Fail</option>
            </select>
          </div>
          <div>
            <label for="domain">Domain / Agent Type</label>
            <select id="domain"></select>
          </div>
          <div>
            <label for="sort">Sort</label>
            <select id="sort">
              <option value="score_desc">Score ↓</option>
              <option value="score_asc">Score ↑</option>
              <option value="logic_desc">Logic ↓</option>
              <option value="security_desc">Security ↓</option>
              <option value="name_asc">Name A-Z</option>
              <option value="name_desc">Name Z-A</option>
            </select>
          </div>
          <div>
            <label for="minScore">Min Score <span id="minScoreValue">0</span></label>
            <input id="minScore" type="range" min="0" max="100" step="1" value="0">
          </div>
        </div>
      </div>
    </section>

    <section class="panel" id="leaderboard">
      <div class="panel-head">
        <h2>Leaderboard</h2>
        <p>Sortable quality table across all scored skills and agents.</p>
      </div>
      <div class="panel-body">
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Artifact</th>
                <th>Kind</th>
                <th>Status</th>
                <th>Score</th>
                <th>Logic</th>
                <th>Clarity</th>
                <th>Security</th>
                <th>Utility</th>
                <th>Domain / Type</th>
                <th>Category</th>
              </tr>
            </thead>
            <tbody id="rows"></tbody>
          </table>
        </div>
      </div>
    </section>

    <div class="footer" id="footerText"></div>
  </div>

  <script>
    const DATA = __PAYLOAD_JSON__;
    const state = {
      search: "",
      kind: "all",
      status: "all",
      domain: "all",
      sort: "score_desc",
      minScore: 0
    };

    const els = {
      statusValue: document.getElementById("statusValue"),
      totalValue: document.getElementById("totalValue"),
      skillsValue: document.getElementById("skillsValue"),
      agentsValue: document.getElementById("agentsValue"),
      passFailValue: document.getElementById("passFailValue"),
      avgValue: document.getElementById("avgValue"),
      search: document.getElementById("search"),
      kind: document.getElementById("kind"),
      status: document.getElementById("status"),
      domain: document.getElementById("domain"),
      sort: document.getElementById("sort"),
      minScore: document.getElementById("minScore"),
      minScoreValue: document.getElementById("minScoreValue"),
      domainRows: document.getElementById("domainRows"),
      rows: document.getElementById("rows"),
      footerText: document.getElementById("footerText"),
      themeToggle: document.getElementById("themeToggle")
    };

    function statusClass(raw) {
      const value = String(raw || "").toLowerCase();
      if (value === "healthy") return "status-healthy";
      if (value === "pass" || value === "ok") return "status-pass";
      if (value === "fail" || value === "failed") return "status-fail";
      return "status-neutral";
    }

    function isDarkTheme() {
      return document.documentElement.getAttribute("data-theme") === "dark";
    }

    function trendPalette() {
      if (isDarkTheme()) {
        return {
          average_score_all: "#22c1ff",
          average_score_skills: "#52d68f",
          average_score_agents: "#ff8b63",
          grid: "#2a4152",
          text: "#9cb2c3",
        };
      }
      return {
        average_score_all: "#0b9ad1",
        average_score_skills: "#0f7d42",
        average_score_agents: "#ff6b3d",
        grid: "#e2e8f0",
        text: "#64748b",
      };
    }

    function fillSummary() {
      const s = DATA.summary;
      const statusRaw = String(s.status || "unknown");
      els.statusValue.textContent = statusRaw.replaceAll("_", " ");
      els.statusValue.className = `quality-pill ${statusClass(statusRaw)}`;
      els.totalValue.textContent = String(s.total_entries || 0);
      els.skillsValue.textContent = String(s.skills_total || 0);
      els.agentsValue.textContent = String(s.agents_total || 0);
      els.passFailValue.textContent = `${s.passed_total || 0} / ${s.failed_total || 0}`;
      els.avgValue.textContent = String(s.average_score_all || 0);
    }

    function fillDomainOptions() {
      const domainSet = new Set();
      for (const item of DATA.entries) {
        domainSet.add(item.domain || "unknown");
      }
      const domains = Array.from(domainSet).sort((a, b) => a.localeCompare(b));
      els.domain.innerHTML = "";
      const base = document.createElement("option");
      base.value = "all";
      base.textContent = "All";
      els.domain.appendChild(base);
      for (const domain of domains) {
        const opt = document.createElement("option");
        opt.value = domain;
        opt.textContent = domain;
        els.domain.appendChild(opt);
      }
    }

    function renderDomainKpis() {
      const rows = Array.isArray(DATA.domain_kpis) ? DATA.domain_kpis : [];
      els.domainRows.innerHTML = "";
      for (const item of rows.slice(0, 24)) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${item.domain}</td>
          <td>${Number(item.average_score || 0).toFixed(2)}</td>
          <td>${Number(item.pass_rate_percent || 0).toFixed(2)}%</td>
          <td>${item.total || 0}</td>
          <td>${item.skills || 0}</td>
          <td>${item.agents || 0}</td>
        `;
        els.domainRows.appendChild(tr);
      }
    }

    function renderTrend() {
      const svg = document.getElementById("trendSvg");
      const history = Array.isArray(DATA.history) ? DATA.history : [];
      const palette = trendPalette();
      svg.innerHTML = "";
      if (history.length < 2) {
        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", "18");
        text.setAttribute("y", "38");
        text.setAttribute("fill", palette.text);
        text.setAttribute("font-size", "12");
        text.textContent = "Not enough history points yet.";
        svg.appendChild(text);
        return;
      }

      const W = 920;
      const H = 220;
      const padLeft = 38;
      const padRight = 20;
      const padTop = 14;
      const padBottom = 26;
      const points = history.slice(-80);
      const scoreKeys = ["average_score_all", "average_score_skills", "average_score_agents"];
      const colors = {
        average_score_all: palette.average_score_all,
        average_score_skills: palette.average_score_skills,
        average_score_agents: palette.average_score_agents,
      };
      const innerW = W - padLeft - padRight;
      const innerH = H - padTop - padBottom;

      function x(i) {
        if (points.length === 1) return padLeft;
        return padLeft + (innerW * i) / (points.length - 1);
      }
      function y(v) {
        const clamped = Math.max(0, Math.min(100, Number(v || 0)));
        return padTop + ((100 - clamped) / 100) * innerH;
      }

      for (let grid = 0; grid <= 5; grid++) {
        const value = grid * 20;
        const yPos = y(value);
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", String(padLeft));
        line.setAttribute("x2", String(W - padRight));
        line.setAttribute("y1", String(yPos));
        line.setAttribute("y2", String(yPos));
        line.setAttribute("stroke", palette.grid);
        line.setAttribute("stroke-width", "1");
        svg.appendChild(line);
      }

      for (const key of scoreKeys) {
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        let d = "";
        points.forEach((point, index) => {
          const xx = x(index);
          const yy = y(point[key]);
          d += `${index === 0 ? "M" : "L"}${xx},${yy} `;
        });
        path.setAttribute("d", d.trim());
        path.setAttribute("fill", "none");
        path.setAttribute("stroke", colors[key]);
        path.setAttribute("stroke-width", "2.4");
        path.setAttribute("stroke-linecap", "round");
        svg.appendChild(path);
      }
    }

    function initTheme() {
      const storageKey = "control-deck-theme";
      const toggle = els.themeToggle;

      function applyTheme(theme) {
        if (theme === "dark") {
          document.documentElement.setAttribute("data-theme", "dark");
          if (toggle) {
            toggle.textContent = "Light";
            toggle.setAttribute("aria-pressed", "true");
          }
        } else {
          document.documentElement.removeAttribute("data-theme");
          if (toggle) {
            toggle.textContent = "Dark";
            toggle.setAttribute("aria-pressed", "false");
          }
        }
        renderTrend();
      }

      const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
      const stored = window.localStorage.getItem(storageKey);
      const initial = stored || (prefersDark ? "dark" : "light");
      applyTheme(initial === "dark" ? "dark" : "light");

      if (!toggle) return;
      toggle.addEventListener("click", () => {
        const active = isDarkTheme() ? "dark" : "light";
        const next = active === "dark" ? "light" : "dark";
        window.localStorage.setItem(storageKey, next);
        applyTheme(next);
      });
    }

    function applyFilters() {
      const q = state.search.trim().toLowerCase();
      let items = DATA.entries.filter((item) => {
        if (state.kind !== "all" && item.kind !== state.kind) return false;
        if (state.status === "pass" && !item.pass) return false;
        if (state.status === "fail" && item.pass) return false;
        if (state.domain !== "all" && item.domain !== state.domain) return false;
        if (item.score < state.minScore) return false;
        if (!q) return true;
        const hay = `${item.slug} ${item.domain} ${item.category} ${item.kind}`.toLowerCase();
        return hay.includes(q);
      });

      switch (state.sort) {
        case "score_asc":
          items.sort((a, b) => a.score - b.score || a.slug.localeCompare(b.slug));
          break;
        case "logic_desc":
          items.sort((a, b) => b.logic - a.logic || b.score - a.score || a.slug.localeCompare(b.slug));
          break;
        case "security_desc":
          items.sort((a, b) => b.security - a.security || b.score - a.score || a.slug.localeCompare(b.slug));
          break;
        case "name_asc":
          items.sort((a, b) => a.slug.localeCompare(b.slug));
          break;
        case "name_desc":
          items.sort((a, b) => b.slug.localeCompare(a.slug));
          break;
        default:
          items.sort((a, b) => b.score - a.score || a.slug.localeCompare(b.slug));
          break;
      }
      return items;
    }

    function renderRows() {
      const items = applyFilters();
      els.rows.innerHTML = "";
      for (const item of items) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td class="slug">${item.slug}</td>
          <td><span class="chip">${item.kind}</span></td>
          <td><span class="status ${item.pass ? "pass" : "fail"}">${item.pass ? "pass" : "fail"}</span></td>
          <td>${item.score.toFixed(2)}</td>
          <td>${item.logic.toFixed(2)}</td>
          <td>${item.clarity.toFixed(2)}</td>
          <td>${item.security.toFixed(2)}</td>
          <td>${item.utility.toFixed(2)}</td>
          <td>${item.domain}</td>
          <td>${item.category}</td>
        `;
        els.rows.appendChild(tr);
      }
      els.footerText.textContent =
        `Showing ${items.length} of ${DATA.entries.length} artifacts. ` +
        `Generated at: ${DATA.summary.generated_at} | ` +
        `Regression: ${DATA.summary.regression_status} | Coverage: ${DATA.summary.coverage_status}`;
    }

    function bindEvents() {
      els.search.addEventListener("input", (event) => {
        state.search = event.target.value || "";
        renderRows();
      });
      els.kind.addEventListener("change", (event) => {
        state.kind = event.target.value;
        renderRows();
      });
      els.status.addEventListener("change", (event) => {
        state.status = event.target.value;
        renderRows();
      });
      els.domain.addEventListener("change", (event) => {
        state.domain = event.target.value;
        renderRows();
      });
      els.sort.addEventListener("change", (event) => {
        state.sort = event.target.value;
        renderRows();
      });
      els.minScore.addEventListener("input", (event) => {
        const value = Number(event.target.value || "0");
        state.minScore = Number.isFinite(value) ? value : 0;
        els.minScoreValue.textContent = String(state.minScore);
        renderRows();
      });
    }

    fillSummary();
    fillDomainOptions();
    renderDomainKpis();
    bindEvents();
    initTheme();
    renderRows();
  </script>
</body>
</html>
"""
    return template.replace("__PAYLOAD_JSON__", payload_json)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build local HTML dashboard from benchmark and catalog outputs."
    )
    parser.add_argument(
        "--benchmark-file",
        default="catalog/benchmark-results.json",
        help="Benchmark results JSON file.",
    )
    parser.add_argument(
        "--skills-index-file",
        default="catalog/skills.index.json",
        help="Skills index JSON file.",
    )
    parser.add_argument(
        "--agents-index-file",
        default="catalog/agents.index.json",
        help="Agents index JSON file.",
    )
    parser.add_argument(
        "--history-file",
        default="catalog/benchmark-history.json",
        help="Historical benchmark timeline JSON file.",
    )
    parser.add_argument(
        "--output-file",
        default="catalog/quality-dashboard.html",
        help="Output dashboard HTML file.",
    )
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    benchmark_file = (base / args.benchmark_file).resolve()
    skills_index_file = (base / args.skills_index_file).resolve()
    agents_index_file = (base / args.agents_index_file).resolve()
    history_file = (base / args.history_file).resolve()
    output_file = (base / args.output_file).resolve()

    benchmark = read_json(benchmark_file)
    skills_index = read_json(skills_index_file)
    agents_index = read_json(agents_index_file)
    history = read_json_list(history_file)
    entries = build_entries(benchmark, skills_index, agents_index)
    executive = benchmark.get("executive", {})
    if not isinstance(executive, dict):
        executive = {}
    domain_kpis = executive.get("domain_kpis", [])
    if not isinstance(domain_kpis, list) or not domain_kpis:
        domain_kpis = build_domain_kpis(entries)

    html = build_html(benchmark, entries, history, domain_kpis)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html, encoding="utf-8")
    print(f"Wrote {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
