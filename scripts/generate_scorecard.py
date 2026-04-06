"""
Generate docs/branding/chart-scorecard.svg
4 dimension cards in a single dark SVG — logic / clarity / security / utility
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "catalog" / "benchmark-results.json"
OUT  = ROOT / "docs" / "branding" / "chart-scorecard.svg"

with open(DATA) as f:
    bench = json.load(f)

# ── compute avg per dimension across all ranked skills ───────
all_skills = bench["rankings"].get("skills_top", [])
sums   = {"logic": 0.0, "clarity": 0.0, "security": 0.0, "utility": 0.0}
counts = {k: 0 for k in sums}
for s in all_skills:
    for d in sums:
        if d in s.get("scores", {}):
            sums[d]   += s["scores"][d]
            counts[d] += 1
avgs = {d: (sums[d] / counts[d] if counts[d] else 0) for d in sums}

# ── card data ────────────────────────────────────────────────
cards = [
    {
        "key":   "logic",
        "label": "Logic",
        "icon":  "⚙",
        "weight":"35%",
        "desc":  "Reasoning · Invariants · Proofs",
        "color": "#22c1ff",
        "score": avgs["logic"],
    },
    {
        "key":   "clarity",
        "label": "Clarity",
        "icon":  "📖",
        "weight":"25%",
        "desc":  "Docs · Examples · Precision",
        "color": "#4ade80",
        "score": avgs["clarity"],
    },
    {
        "key":   "security",
        "label": "Security",
        "icon":  "🔒",
        "weight":"20%",
        "desc":  "Guardrails · Boundaries · Threats",
        "color": "#f97316",
        "score": avgs["security"],
    },
    {
        "key":   "utility",
        "label": "Utility",
        "icon":  "🚀",
        "weight":"20%",
        "desc":  "Real-world · Coverage · Value",
        "color": "#a78bfa",
        "score": avgs["utility"],
    },
]

# ── layout constants ─────────────────────────────────────────
CARD_W   = 180
CARD_H   = 200
GAP      = 16
PAD_X    = 24
PAD_Y    = 24
COLS     = 4
BAR_H    = 10
BAR_R    = 5
CORNER   = 14

TOTAL_W  = PAD_X * 2 + COLS * CARD_W + (COLS - 1) * GAP
TOTAL_H  = PAD_Y * 2 + CARD_H + 60   # +60 for title

BG       = "#0d1117"
CARD_BG  = "#161b22"
BORDER   = "#30363d"
TEXT_PRI = "#e6edf3"
TEXT_SEC = "#8b949e"
TRACK    = "#21262d"

lines = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{TOTAL_W}" height="{TOTAL_H}" viewBox="0 0 {TOTAL_W} {TOTAL_H}">',
    # background
    f'<rect width="{TOTAL_W}" height="{TOTAL_H}" rx="12" fill="{BG}"/>',
    # title
    f'<text x="{TOTAL_W//2}" y="34" text-anchor="middle" '
    f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="14" '
    f'font-weight="bold" fill="{TEXT_PRI}">4-Dimension Quality System</text>',
    f'<text x="{TOTAL_W//2}" y="52" text-anchor="middle" '
    f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="10" '
    f'fill="{TEXT_SEC}">Average scores across all ranked skills · 100% pass rate</text>',
]

for i, card in enumerate(cards):
    cx    = PAD_X + i * (CARD_W + GAP)
    cy    = PAD_Y + 42
    score = card["score"]
    pct   = (score - 72) / (100 - 72)          # normalise 72–100 → 0–1
    pct   = max(0.0, min(1.0, pct))
    bar_w = pct * (CARD_W - 28)
    color = card["color"]

    # card background + border
    lines.append(
        f'<rect x="{cx}" y="{cy}" width="{CARD_W}" height="{CARD_H}" '
        f'rx="{CORNER}" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>'
    )

    # top colour accent bar
    lines.append(
        f'<rect x="{cx}" y="{cy}" width="{CARD_W}" height="4" '
        f'rx="{CORNER}" fill="{color}"/>'
    )

    # icon
    lines.append(
        f'<text x="{cx + CARD_W//2}" y="{cy + 38}" text-anchor="middle" '
        f'font-size="26">{card["icon"]}</text>'
    )

    # label
    lines.append(
        f'<text x="{cx + CARD_W//2}" y="{cy + 62}" text-anchor="middle" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="13" '
        f'font-weight="bold" fill="{color}">{card["label"]}</text>'
    )

    # weight
    lines.append(
        f'<text x="{cx + CARD_W//2}" y="{cy + 78}" text-anchor="middle" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="10" '
        f'fill="{TEXT_SEC}">weight: {card["weight"]}</text>'
    )

    # big score
    lines.append(
        f'<text x="{cx + CARD_W//2}" y="{cy + 118}" text-anchor="middle" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="34" '
        f'font-weight="bold" fill="{TEXT_PRI}">{score:.1f}</text>'
    )

    # /100
    lines.append(
        f'<text x="{cx + CARD_W//2}" y="{cy + 132}" text-anchor="middle" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="9" '
        f'fill="{TEXT_SEC}">/ 100</text>'
    )

    # progress bar track
    bar_x = cx + 14
    bar_y = cy + CARD_H - 36
    lines.append(
        f'<rect x="{bar_x}" y="{bar_y}" width="{CARD_W - 28}" height="{BAR_H}" '
        f'rx="{BAR_R}" fill="{TRACK}"/>'
    )
    # progress bar fill
    if bar_w > 0:
        lines.append(
            f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w:.1f}" height="{BAR_H}" '
            f'rx="{BAR_R}" fill="{color}" opacity="0.9"/>'
        )

    # desc
    lines.append(
        f'<text x="{cx + CARD_W//2}" y="{cy + CARD_H - 12}" text-anchor="middle" '
        f'font-family="ui-monospace,SFMono-Regular,monospace" font-size="8" '
        f'fill="{TEXT_SEC}">{card["desc"]}</text>'
    )

lines.append('</svg>')
OUT.write_text("\n".join(lines))
print(f"Saved: {OUT}")
