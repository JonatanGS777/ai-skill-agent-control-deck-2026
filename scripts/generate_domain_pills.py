"""
Generate docs/branding/chart-domain-pills.svg
Animated pills grid — domain coverage with fade+slide-in stagger
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "catalog" / "benchmark-results.json"
OUT  = ROOT / "docs" / "branding" / "chart-domain-pills.svg"

with open(DATA) as f:
    bench = json.load(f)

kpis = bench["executive"]["domain_kpis"]
kpis_sorted = sorted(kpis, key=lambda x: x["average_score"], reverse=True)

domain_meta = {
    "fullstack":              {"label": "Full Stack",        "icon": "&#9889;", "cat": "engineering"},
    "domain-ai":              {"label": "Applied AI",        "icon": "&#129504;","cat": "ai"},
    "frontend":               {"label": "Frontend",          "icon": "&#127912;","cat": "engineering"},
    "programming":            {"label": "Programming",       "icon": "&#128187;","cat": "engineering"},
    "orchestrator":           {"label": "Orchestrator",      "icon": "&#128257;","cat": "agents"},
    "chatbot-ai":             {"label": "Chatbot AI",        "icon": "&#128172;","cat": "ai"},
    "automation-ai":          {"label": "Automation AI",     "icon": "&#9881;",  "cat": "ai"},
    "debugger":               {"label": "Debugger",          "icon": "&#128027;","cat": "agents"},
    "reviewer":               {"label": "Reviewer",          "icon": "&#128269;","cat": "agents"},
    "builder":                {"label": "Builder",           "icon": "&#127959;","cat": "agents"},
    "specialist":             {"label": "Specialist",        "icon": "&#127919;","cat": "agents"},
    "visual-architecture":    {"label": "Visual Arch",       "icon": "&#128208;","cat": "engineering"},
    "robotics":               {"label": "Robotics",          "icon": "&#129302;","cat": "ai"},
    "mathematics":            {"label": "Mathematics",       "icon": "&#8721;",  "cat": "logic"},
    "math-programming-logic": {"label": "Logic Foundations", "icon": "&#8866;",  "cat": "logic"},
}

cat_colors = {
    "ai":          {"bg": "#dbeafe", "border": "#3b82f6", "text": "#1d4ed8", "dot": "#3b82f6"},
    "engineering": {"bg": "#dcfce7", "border": "#22c55e", "text": "#15803d", "dot": "#22c55e"},
    "agents":      {"bg": "#f3e8ff", "border": "#a855f7", "text": "#7e22ce", "dot": "#a855f7"},
    "logic":       {"bg": "#fff7ed", "border": "#f97316", "text": "#c2410c", "dot": "#f97316"},
}

COLS   = 3
PILL_W = 240
PILL_H = 64
GAP_X  = 16
GAP_Y  = 14
PAD_X  = 28
PAD_Y  = 72
CORNER = 12

items = []
for k in kpis_sorted:
    d    = k["domain"]
    meta = domain_meta.get(d, {"label": d.replace("-"," ").title(), "icon": "&#9642;", "cat": "engineering"})
    items.append({
        "label": meta["label"],
        "icon":  meta["icon"],
        "cat":   meta["cat"],
        "score": k["average_score"],
        "total": k["total"],
    })

ROWS = (len(items) + COLS - 1) // COLS
W    = PAD_X * 2 + COLS * PILL_W + (COLS - 1) * GAP_X
H    = PAD_Y + ROWS * PILL_H + (ROWS - 1) * GAP_Y + 48

BG       = "#ffffff"
TEXT_PRI = "#1f2328"
TEXT_SEC = "#656d76"

lines = []
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

# CSS
css = '<defs><style>'
for i in range(len(items)):
    delay = i * 0.07
    css += f'.p{i}{{animation:fs 0.5s ease {delay:.2f}s both;}}'
css += '@keyframes fs{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}'
css += '</style></defs>'
lines.append(css)

# background
lines.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}" stroke="#d0d7de" stroke-width="1"/>')

# title
lines.append(
    f'<text x="{W//2}" y="30" text-anchor="middle" '
    f'font-family="ui-monospace,SFMono-Regular,monospace" '
    f'font-size="14" font-weight="bold" fill="{TEXT_PRI}">Domain Coverage</text>'
)
lines.append(
    f'<text x="{W//2}" y="48" text-anchor="middle" '
    f'font-family="ui-monospace,SFMono-Regular,monospace" '
    f'font-size="10" fill="{TEXT_SEC}">{len(items)} domains · 399 artifacts · 100% pass rate</text>'
)

# pills
for i, item in enumerate(items):
    col_i = i % COLS
    row_i = i // COLS
    x = PAD_X + col_i * (PILL_W + GAP_X)
    y = PAD_Y + row_i * (PILL_H + GAP_Y)

    c       = cat_colors[item["cat"]]
    bar_max = PILL_W - 32
    bar_w   = max(4.0, min(float(bar_max), ((item["score"] - 72) / 28) * bar_max))

    lines.append(f'<g class="p{i}">')
    lines.append(f'<rect x="{x}" y="{y}" width="{PILL_W}" height="{PILL_H}" rx="{CORNER}" fill="{c["bg"]}" stroke="{c["border"]}" stroke-width="1.2"/>')
    lines.append(f'<rect x="{x}" y="{y}" width="5" height="{PILL_H}" rx="{CORNER}" fill="{c["dot"]}"/>')
    lines.append(f'<text x="{x+20}" y="{y+26}" font-size="16" dominant-baseline="middle" font-family="serif">{item["icon"]}</text>')
    lines.append(f'<text x="{x+42}" y="{y+21}" font-family="ui-monospace,SFMono-Regular,monospace" font-size="11" font-weight="bold" fill="{c["text"]}">{item["label"]}</text>')
    lines.append(f'<text x="{x+42}" y="{y+35}" font-family="ui-monospace,SFMono-Regular,monospace" font-size="9" fill="{TEXT_SEC}">{item["total"]} artifacts</text>')
    lines.append(f'<text x="{x+PILL_W-10}" y="{y+23}" text-anchor="end" font-family="ui-monospace,SFMono-Regular,monospace" font-size="16" font-weight="bold" fill="{c["text"]}">{item["score"]:.1f}</text>')
    lines.append(f'<rect x="{x+16}" y="{y+PILL_H-14}" width="{bar_max}" height="5" rx="3" fill="rgba(0,0,0,0.08)"/>')
    lines.append(f'<rect x="{x+16}" y="{y+PILL_H-14}" width="{bar_w:.1f}" height="5" rx="3" fill="{c["dot"]}" opacity="0.85"/>')
    lines.append('</g>')

# legend
legend_items = [("AI", "#3b82f6"), ("Engineering", "#22c55e"), ("Agents", "#a855f7"), ("Logic", "#f97316")]
lx = PAD_X
ly = H - 18
for lbl, col in legend_items:
    lines.append(f'<circle cx="{lx+5}" cy="{ly-4}" r="5" fill="{col}"/>')
    lines.append(f'<text x="{lx+14}" y="{ly}" font-family="ui-monospace,SFMono-Regular,monospace" font-size="9" fill="{TEXT_SEC}">{lbl}</text>')
    lx += len(lbl) * 6 + 26

lines.append('</svg>')

OUT.write_text("\n".join(lines))
print(f"Saved: {OUT}  ({OUT.stat().st_size//1024} KB)")
