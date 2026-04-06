"""
Generate SVG charts for the README:
  1. docs/branding/chart-top10-scores.svg   — horizontal bar chart, top 10 skills/agents
  2. docs/branding/chart-domains.svg        — horizontal bar chart, domain KPIs
  3. docs/branding/chart-radar.svg          — radar/spider chart of avg dimension scores
"""

import json, math, textwrap
from pathlib import Path

ROOT   = Path(__file__).parent.parent
DATA   = ROOT / "catalog" / "benchmark-results.json"
OUT    = ROOT / "docs" / "branding"
OUT.mkdir(parents=True, exist_ok=True)

with open(DATA) as f:
    bench = json.load(f)

# ── colour palette ──────────────────────────────────────────
BG        = "#0d1117"
CARD      = "#161b22"
BORDER    = "#30363d"
TEXT_PRI  = "#e6edf3"
TEXT_SEC  = "#8b949e"
ACCENT1   = "#22c1ff"   # blue
ACCENT2   = "#4ade80"   # green
ACCENT3   = "#f97316"   # orange
ACCENT4   = "#a78bfa"   # purple
GRID      = "#21262d"

# ════════════════════════════════════════════════════════════
#  1. TOP-10 SKILLS  (horizontal bars)
# ════════════════════════════════════════════════════════════
top_skills = bench["rankings"]["skills_top"][:10]

labels = []
scores = []
for item in top_skills:
    slug = item["slug"]
    # shorten label
    slug = (slug
        .replace("-skill-2026","")
        .replace("ai-domain-","")
        .replace("-"," ")
        .title()
    )
    if len(slug) > 30:
        slug = slug[:28] + "…"
    labels.append(slug)
    scores.append(item["total_score"])

W, H    = 780, 380
PAD_L   = 220
PAD_R   = 60
PAD_T   = 60
PAD_B   = 50
BAR_H   = 22
GAP     = 10
CHART_W = W - PAD_L - PAD_R

svg_lines = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>',
    # title
    f'<text x="{W//2}" y="36" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" '
    f'font-size="15" font-weight="bold" fill="{TEXT_PRI}">Top 10 Skills — Quality Score</text>',
    # subtitle
    f'<text x="{W//2}" y="52" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" '
    f'font-size="10" fill="{TEXT_SEC}">logic 35% · clarity 25% · security 20% · utility 20%</text>',
]

# grid lines
for v in [80, 85, 90, 95, 100]:
    x = PAD_L + (v - 72) / (100 - 72) * CHART_W
    svg_lines.append(
        f'<line x1="{x:.1f}" y1="{PAD_T}" x2="{x:.1f}" y2="{H-PAD_B}" '
        f'stroke="{GRID}" stroke-width="1"/>'
    )
    svg_lines.append(
        f'<text x="{x:.1f}" y="{H-PAD_B+14}" text-anchor="middle" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="9" fill="{TEXT_SEC}">{v}</text>'
    )

for i, (label, score) in enumerate(zip(labels, scores)):
    y      = PAD_T + i * (BAR_H + GAP)
    bar_w  = (score - 72) / (100 - 72) * CHART_W
    color  = ACCENT1 if i == 0 else ACCENT2 if score >= 97 else ACCENT3

    # bar bg
    svg_lines.append(
        f'<rect x="{PAD_L}" y="{y}" width="{CHART_W}" height="{BAR_H}" '
        f'rx="4" fill="{CARD}"/>'
    )
    # bar fill
    svg_lines.append(
        f'<rect x="{PAD_L}" y="{y}" width="{bar_w:.1f}" height="{BAR_H}" '
        f'rx="4" fill="{color}" opacity="0.85"/>'
    )
    # label
    svg_lines.append(
        f'<text x="{PAD_L-8}" y="{y+BAR_H//2+4}" text-anchor="end" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="10" fill="{TEXT_PRI}">{label}</text>'
    )
    # score
    svg_lines.append(
        f'<text x="{PAD_L + bar_w + 6:.1f}" y="{y+BAR_H//2+4}" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="10" '
        f'font-weight="bold" fill="{color}">{score}</text>'
    )

svg_lines.append('</svg>')
(OUT / "chart-top10-scores.svg").write_text("\n".join(svg_lines))
print("✓ chart-top10-scores.svg")

# ════════════════════════════════════════════════════════════
#  2. DOMAIN KPIs  (horizontal bars)
# ════════════════════════════════════════════════════════════
kpis = bench["executive"]["domain_kpis"]
# sort by average_score desc, take top 12
kpis_sorted = sorted(kpis, key=lambda x: x["average_score"], reverse=True)[:12]

dom_labels = []
dom_scores = []
dom_totals = []
for k in kpis_sorted:
    lbl = k["domain"].replace("-"," ").title()
    if len(lbl) > 22:
        lbl = lbl[:20] + "…"
    dom_labels.append(lbl)
    dom_scores.append(k["average_score"])
    dom_totals.append(k["total"])

W2, H2  = 780, 440
PAD_L2  = 170
CHART_W2 = W2 - PAD_L2 - PAD_R

svg2 = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}">',
    f'<rect width="{W2}" height="{H2}" rx="12" fill="{BG}"/>',
    f'<text x="{W2//2}" y="36" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" '
    f'font-size="15" font-weight="bold" fill="{TEXT_PRI}">Domain Coverage — Avg Score by Category</text>',
    f'<text x="{W2//2}" y="52" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" '
    f'font-size="10" fill="{TEXT_SEC}">All 399 artifacts · 100% pass rate</text>',
]

for v in [75, 80, 85, 90, 95, 100]:
    x = PAD_L2 + (v - 72) / (100 - 72) * CHART_W2
    svg2.append(
        f'<line x1="{x:.1f}" y1="{PAD_T}" x2="{x:.1f}" y2="{H2-PAD_B}" '
        f'stroke="{GRID}" stroke-width="1"/>'
    )
    svg2.append(
        f'<text x="{x:.1f}" y="{H2-PAD_B+14}" text-anchor="middle" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="9" fill="{TEXT_SEC}">{v}</text>'
    )

colors_cycle = [ACCENT1, ACCENT2, ACCENT3, ACCENT4]
for i, (label, score, total) in enumerate(zip(dom_labels, dom_scores, dom_totals)):
    y     = PAD_T + i * (BAR_H + GAP)
    bw    = (score - 72) / (100 - 72) * CHART_W2
    color = colors_cycle[i % len(colors_cycle)]

    svg2.append(f'<rect x="{PAD_L2}" y="{y}" width="{CHART_W2}" height="{BAR_H}" rx="4" fill="{CARD}"/>')
    svg2.append(f'<rect x="{PAD_L2}" y="{y}" width="{bw:.1f}" height="{BAR_H}" rx="4" fill="{color}" opacity="0.8"/>')
    svg2.append(
        f'<text x="{PAD_L2-8}" y="{y+BAR_H//2+4}" text-anchor="end" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="10" fill="{TEXT_PRI}">{label}</text>'
    )
    svg2.append(
        f'<text x="{PAD_L2+bw+6:.1f}" y="{y+BAR_H//2+4}" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="10" font-weight="bold" fill="{color}">'
        f'{score} <tspan fill="{TEXT_SEC}" font-weight="normal">({total})</tspan></text>'
    )

svg2.append('</svg>')
(OUT / "chart-domains.svg").write_text("\n".join(svg2))
print("✓ chart-domains.svg")

# ════════════════════════════════════════════════════════════
#  3. RADAR CHART — 4 dimensions (from top skill scores avg)
# ════════════════════════════════════════════════════════════
# Compute average per dimension across all ranked skills
all_skills = bench["rankings"].get("skills_top", [])
dim_sums   = {"logic": 0, "clarity": 0, "security": 0, "utility": 0}
dim_counts = {"logic": 0, "clarity": 0, "security": 0, "utility": 0}

for s in all_skills:
    for d in dim_sums:
        if d in s["scores"]:
            dim_sums[d]   += s["scores"][d]
            dim_counts[d] += 1

dim_avgs = {d: (dim_sums[d] / dim_counts[d] if dim_counts[d] else 0) for d in dim_sums}

dimensions = ["Logic", "Clarity", "Security", "Utility"]
dim_keys   = ["logic", "clarity", "security", "utility"]
values     = [dim_avgs[k] for k in dim_keys]
weights    = [35, 25, 20, 20]

W3 = H3 = 420
CX = CY = 210
R_MAX  = 140
R_MIN  = 20
N      = len(dimensions)

def polar(angle_deg, r, cx=CX, cy=CY):
    a = math.radians(angle_deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)

svg3 = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W3}" height="{H3}" viewBox="0 0 {W3} {H3}">',
    f'<rect width="{W3}" height="{H3}" rx="12" fill="{BG}"/>',
    f'<text x="{W3//2}" y="28" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" '
    f'font-size="14" font-weight="bold" fill="{TEXT_PRI}">Quality Dimensions</text>',
    f'<text x="{W3//2}" y="44" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" '
    f'font-size="9" fill="{TEXT_SEC}">Average across all ranked skills</text>',
]

# concentric grid rings
for pct in [0.25, 0.50, 0.75, 1.0]:
    r = R_MIN + pct * (R_MAX - R_MIN)
    pts = [polar(i * 360 / N, r) for i in range(N)]
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    svg3.append(f'<polygon points="{pts_str}" fill="none" stroke="{GRID}" stroke-width="1"/>')
    # ring label
    lx, ly = polar(0, r)
    val = 72 + pct * 28
    svg3.append(
        f'<text x="{lx+4:.1f}" y="{ly:.1f}" font-family="ui-monospace,SFMono-Regular,monospace" '
        f'font-size="8" fill="{TEXT_SEC}">{val:.0f}</text>'
    )

# axis lines
for i in range(N):
    x1, y1 = polar(i * 360 / N, R_MIN)
    x2, y2 = polar(i * 360 / N, R_MAX)
    svg3.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{BORDER}" stroke-width="1"/>')

# data polygon
data_pts = []
for i, (v, key) in enumerate(zip(values, dim_keys)):
    angle = i * 360 / N
    r = R_MIN + (v - 72) / (100 - 72) * (R_MAX - R_MIN)
    r = max(R_MIN, min(R_MAX, r))
    data_pts.append(polar(angle, r))

pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in data_pts)
svg3.append(f'<polygon points="{pts_str}" fill="{ACCENT1}" fill-opacity="0.2" stroke="{ACCENT1}" stroke-width="2"/>')

# data dots
for (x, y) in data_pts:
    svg3.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{ACCENT1}" stroke="{BG}" stroke-width="2"/>')

# axis labels
label_colors = [ACCENT1, ACCENT2, ACCENT3, ACCENT4]
for i, (dim, w, v) in enumerate(zip(dimensions, weights, values)):
    angle = i * 360 / N
    lx, ly = polar(angle, R_MAX + 24)
    anchor = "middle"
    if lx < CX - 10:
        anchor = "end"
    elif lx > CX + 10:
        anchor = "start"
    color = label_colors[i]
    svg3.append(
        f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="11" font-weight="bold" fill="{color}">'
        f'{dim}</text>'
    )
    svg3.append(
        f'<text x="{lx:.1f}" y="{ly+13:.1f}" text-anchor="{anchor}" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="9" fill="{TEXT_SEC}">'
        f'{v:.1f} · {w}%</text>'
    )

svg3.append('</svg>')
(OUT / "chart-radar.svg").write_text("\n".join(svg3))
print("✓ chart-radar.svg")
print("\nAll charts generated in docs/branding/")
