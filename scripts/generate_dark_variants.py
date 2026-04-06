"""
Generate dark-theme variants of all light SVGs:
  - banner-slogan-dark.svg
  - chart-scorecard-dark.svg
  - chart-domain-pills-dark.svg
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "catalog" / "benchmark-results.json"
OUT  = ROOT / "docs" / "branding"

with open(DATA) as f:
    bench = json.load(f)

# ── dark palette ─────────────────────────────────────────────
D = {
    "bg":       "#0d1117",
    "card":     "#161b22",
    "border":   "#30363d",
    "text_pri": "#e6edf3",
    "text_sec": "#8b949e",
    "track":    "#21262d",
    "accent":   "#58a6ff",
}

# ════════════════════════════════════════════════════════════
#  1. BANNER SLOGAN DARK
# ════════════════════════════════════════════════════════════
W, H = 620, 110
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" rx="10" fill="{D['card']}" stroke="{D['border']}" stroke-width="1.5"/>
  <rect x="0" y="0" width="{W}" height="4" rx="10" fill="{D['accent']}"/>
  <text x="{W//2}" y="38" text-anchor="middle"
    font-family="ui-monospace,SFMono-Regular,monospace"
    font-size="13" font-weight="bold" fill="{D['text_pri']}">
    Build · Measure · Scale · Govern · Release
  </text>
  <text x="{W//2}" y="64" text-anchor="middle"
    font-family="ui-monospace,SFMono-Regular,monospace"
    font-size="12" fill="{D['accent']}">
    203 Skills  ·  196 Agents  ·  30 Logic Foundations
  </text>
  <text x="{W//2}" y="88" text-anchor="middle"
    font-family="ui-monospace,SFMono-Regular,monospace"
    font-size="11" fill="{D['text_sec']}">
    Benchmark-driven  ·  Regression-safe  ·  Release-ready
  </text>
</svg>"""
(OUT / "banner-slogan-dark.svg").write_text(svg)
print("✓ banner-slogan-dark.svg")

# ════════════════════════════════════════════════════════════
#  2. SCORECARD DARK
# ════════════════════════════════════════════════════════════
all_skills = bench["rankings"].get("skills_top", [])
sums   = {"logic": 0.0, "clarity": 0.0, "security": 0.0, "utility": 0.0}
counts = {k: 0 for k in sums}
for s in all_skills:
    for d in sums:
        if d in s.get("scores", {}):
            sums[d]   += s["scores"][d]
            counts[d] += 1
avgs = {d: (sums[d] / counts[d] if counts[d] else 0) for d in sums}

cards = [
    {"label":"Logic",    "icon":"&#9881;",  "weight":"35%", "desc":"Reasoning · Invariants · Proofs",    "color":"#22c1ff", "score":avgs["logic"]},
    {"label":"Clarity",  "icon":"&#128218;","weight":"25%", "desc":"Docs · Examples · Precision",        "color":"#4ade80", "score":avgs["clarity"]},
    {"label":"Security", "icon":"&#128274;","weight":"20%", "desc":"Guardrails · Boundaries · Threats",  "color":"#f97316", "score":avgs["security"]},
    {"label":"Utility",  "icon":"&#128640;","weight":"20%", "desc":"Real-world · Coverage · Value",      "color":"#a78bfa", "score":avgs["utility"]},
]

CARD_W=180; CARD_H=200; GAP=16; PAD_X=24; PAD_Y=24; COLS=4; CORNER=14
TW = PAD_X*2 + COLS*CARD_W + (COLS-1)*GAP
TH = PAD_Y*2 + CARD_H + 60

lines = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}">',
    f'<rect width="{TW}" height="{TH}" rx="12" fill="{D["bg"]}"/>',
    f'<text x="{TW//2}" y="34" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" font-size="14" font-weight="bold" fill="{D["text_pri"]}">4-Dimension Quality System</text>',
    f'<text x="{TW//2}" y="52" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" font-size="10" fill="{D["text_sec"]}">Average scores across all ranked skills · 100% pass rate</text>',
]
for i, card in enumerate(cards):
    cx = PAD_X + i*(CARD_W+GAP)
    cy = PAD_Y + 42
    pct   = max(0.0, min(1.0, (card["score"]-72)/28))
    bar_w = pct*(CARD_W-28)
    c = card["color"]
    lines += [
        f'<rect x="{cx}" y="{cy}" width="{CARD_W}" height="{CARD_H}" rx="{CORNER}" fill="{D["card"]}" stroke="{D["border"]}" stroke-width="1"/>',
        f'<rect x="{cx}" y="{cy}" width="{CARD_W}" height="4" rx="{CORNER}" fill="{c}"/>',
        f'<text x="{cx+CARD_W//2}" y="{cy+38}" text-anchor="middle" font-size="26" font-family="serif">{card["icon"]}</text>',
        f'<text x="{cx+CARD_W//2}" y="{cy+62}" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" font-size="13" font-weight="bold" fill="{c}">{card["label"]}</text>',
        f'<text x="{cx+CARD_W//2}" y="{cy+78}" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" font-size="10" fill="{D["text_sec"]}">weight: {card["weight"]}</text>',
        f'<text x="{cx+CARD_W//2}" y="{cy+118}" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" font-size="34" font-weight="bold" fill="{D["text_pri"]}">{card["score"]:.1f}</text>',
        f'<text x="{cx+CARD_W//2}" y="{cy+132}" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" font-size="9" fill="{D["text_sec"]}">/ 100</text>',
        f'<rect x="{cx+14}" y="{cy+CARD_H-36}" width="{CARD_W-28}" height="10" rx="5" fill="{D["track"]}"/>',
    ]
    if bar_w > 0:
        lines.append(f'<rect x="{cx+14}" y="{cy+CARD_H-36}" width="{bar_w:.1f}" height="10" rx="5" fill="{c}" opacity="0.9"/>')
    lines.append(f'<text x="{cx+CARD_W//2}" y="{cy+CARD_H-12}" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" font-size="8" fill="{D["text_sec"]}">{card["desc"]}</text>')
lines.append('</svg>')
(OUT / "chart-scorecard-dark.svg").write_text("\n".join(lines))
print("✓ chart-scorecard-dark.svg")

# ════════════════════════════════════════════════════════════
#  3. DOMAIN PILLS DARK
# ════════════════════════════════════════════════════════════
kpis = bench["executive"]["domain_kpis"]
kpis_sorted = sorted(kpis, key=lambda x: x["average_score"], reverse=True)

domain_meta = {
    "fullstack":              {"label":"Full Stack",        "icon":"&#9889;",  "cat":"engineering"},
    "domain-ai":              {"label":"Applied AI",        "icon":"&#129504;","cat":"ai"},
    "frontend":               {"label":"Frontend",          "icon":"&#127912;","cat":"engineering"},
    "programming":            {"label":"Programming",       "icon":"&#128187;","cat":"engineering"},
    "orchestrator":           {"label":"Orchestrator",      "icon":"&#128257;","cat":"agents"},
    "chatbot-ai":             {"label":"Chatbot AI",        "icon":"&#128172;","cat":"ai"},
    "automation-ai":          {"label":"Automation AI",     "icon":"&#9881;",  "cat":"ai"},
    "debugger":               {"label":"Debugger",          "icon":"&#128027;","cat":"agents"},
    "reviewer":               {"label":"Reviewer",          "icon":"&#128269;","cat":"agents"},
    "builder":                {"label":"Builder",           "icon":"&#127959;","cat":"agents"},
    "specialist":             {"label":"Specialist",        "icon":"&#127919;","cat":"agents"},
    "visual-architecture":    {"label":"Visual Arch",       "icon":"&#128208;","cat":"engineering"},
    "robotics":               {"label":"Robotics",          "icon":"&#129302;","cat":"ai"},
    "mathematics":            {"label":"Mathematics",       "icon":"&#8721;",  "cat":"logic"},
    "math-programming-logic": {"label":"Logic Foundations", "icon":"&#8866;",  "cat":"logic"},
}

# dark category colors
cat_dark = {
    "ai":          {"bg":"#0d1b2e","border":"#3b82f6","text":"#60a5fa","dot":"#3b82f6"},
    "engineering": {"bg":"#0d1f0f","border":"#22c55e","text":"#4ade80","dot":"#22c55e"},
    "agents":      {"bg":"#1a0d2e","border":"#a855f7","text":"#c084fc","dot":"#a855f7"},
    "logic":       {"bg":"#1f1006","border":"#f97316","text":"#fb923c","dot":"#f97316"},
}

COLS2=3; PW=240; PH=64; GX=16; GY=14; PX=28; PY=72; CR=12
items2 = []
for k in kpis_sorted:
    m = domain_meta.get(k["domain"], {"label":k["domain"].replace("-"," ").title(),"icon":"&#9642;","cat":"engineering"})
    items2.append({"label":m["label"],"icon":m["icon"],"cat":m["cat"],"score":k["average_score"],"total":k["total"]})

ROWS2 = (len(items2)+COLS2-1)//COLS2
W2    = PX*2 + COLS2*PW + (COLS2-1)*GX
H2    = PY + ROWS2*PH + (ROWS2-1)*GY + 48

lines2 = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}">']
css = '<defs><style>'
for i in range(len(items2)):
    css += f'.p{i}{{animation:fs 0.5s ease {i*0.07:.2f}s both;}}'
css += '@keyframes fs{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}</style></defs>'
lines2.append(css)
lines2.append(f'<rect width="{W2}" height="{H2}" rx="14" fill="{D["bg"]}" stroke="{D["border"]}" stroke-width="1"/>')
lines2.append(f'<text x="{W2//2}" y="30" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" font-size="14" font-weight="bold" fill="{D["text_pri"]}">Domain Coverage</text>')
lines2.append(f'<text x="{W2//2}" y="48" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,monospace" font-size="10" fill="{D["text_sec"]}">{len(items2)} domains · 399 artifacts · 100% pass rate</text>')

for i, item in enumerate(items2):
    cx2 = PX + (i%COLS2)*(PW+GX)
    cy2 = PY + (i//COLS2)*(PH+GY)
    c2  = cat_dark[item["cat"]]
    bmax= PW-32
    bw  = max(4.0, min(float(bmax), ((item["score"]-72)/28)*bmax))
    lines2 += [
        f'<g class="p{i}">',
        f'<rect x="{cx2}" y="{cy2}" width="{PW}" height="{PH}" rx="{CR}" fill="{c2["bg"]}" stroke="{c2["border"]}" stroke-width="1.2"/>',
        f'<rect x="{cx2}" y="{cy2}" width="5" height="{PH}" rx="{CR}" fill="{c2["dot"]}"/>',
        f'<text x="{cx2+20}" y="{cy2+26}" font-size="16" dominant-baseline="middle" font-family="serif">{item["icon"]}</text>',
        f'<text x="{cx2+42}" y="{cy2+21}" font-family="ui-monospace,SFMono-Regular,monospace" font-size="11" font-weight="bold" fill="{c2["text"]}">{item["label"]}</text>',
        f'<text x="{cx2+42}" y="{cy2+35}" font-family="ui-monospace,SFMono-Regular,monospace" font-size="9" fill="{D["text_sec"]}">{item["total"]} artifacts</text>',
        f'<text x="{cx2+PW-10}" y="{cy2+23}" text-anchor="end" font-family="ui-monospace,SFMono-Regular,monospace" font-size="16" font-weight="bold" fill="{c2["text"]}">{item["score"]:.1f}</text>',
        f'<rect x="{cx2+16}" y="{cy2+PH-14}" width="{bmax}" height="5" rx="3" fill="rgba(255,255,255,0.08)"/>',
        f'<rect x="{cx2+16}" y="{cy2+PH-14}" width="{bw:.1f}" height="5" rx="3" fill="{c2["dot"]}" opacity="0.85"/>',
        '</g>',
    ]

legend2 = [("AI","#3b82f6"),("Engineering","#22c55e"),("Agents","#a855f7"),("Logic","#f97316")]
lx2 = PX; ly2 = H2-18
for lbl, col in legend2:
    lines2.append(f'<circle cx="{lx2+5}" cy="{ly2-4}" r="5" fill="{col}"/>')
    lines2.append(f'<text x="{lx2+14}" y="{ly2}" font-family="ui-monospace,SFMono-Regular,monospace" font-size="9" fill="{D["text_sec"]}">{lbl}</text>')
    lx2 += len(lbl)*6+26
lines2.append('</svg>')
(OUT / "chart-domain-pills-dark.svg").write_text("\n".join(lines2))
print("✓ chart-domain-pills-dark.svg")
print("\nAll dark variants generated.")
