"""
Take a high-quality screenshot of catalog/quality-dashboard.html
and save it to docs/branding/dashboard-screenshot.png
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT   = Path(__file__).parent.parent
HTML   = ROOT / "catalog" / "quality-dashboard.html"
OUT    = ROOT / "docs" / "branding" / "dashboard-screenshot.png"

assert HTML.exists(), f"Not found: {HTML}"

url = HTML.as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page    = browser.new_page(viewport={"width": 1400, "height": 900})
    page.goto(url, wait_until="networkidle")
    # let any animations settle
    page.wait_for_timeout(1500)
    page.screenshot(path=str(OUT), full_page=False, type="png")
    browser.close()

print(f"Saved: {OUT}")
