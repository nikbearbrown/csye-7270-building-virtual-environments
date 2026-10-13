#!/usr/bin/env python3
"""Act IV, B31 evidence: capture the project's real, public README on GitHub where it leads with the one-line installer.
  https://github.com/ahujasid/mcp-for-blender   (public, no sign-in, no cookies set by us; nothing clicked)
1600x900 CSS viewport at device scale 2.4. The page is scrolled so the "One command sets up ..." paragraph sits near the top,
and the shot is clipped to the README column (x 200..1090 CSS px) so its text is large enough to read in BrowserCapture.
Outputs:
  TK/runtime/remotion/public/lecture-a3assets/a4_readme_installer.png   (the capture, for BrowserCapture in B31)
  capture_readme.json   (url, UTC time, the exact text of the three passages the beat rings, and their boxes as image fractions)
Run:  python3 evidence/act4/capture_readme.py      (Playwright + its Chromium; read-only)
"""
import json, datetime, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PUB = pathlib.Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/lecture-a3assets")
PUB.mkdir(parents=True, exist_ok=True)
URL = "https://github.com/ahujasid/mcp-for-blender"
CLIP_X0, CLIP_X1 = 200, 1090            # README column (article is x 225..1063 at this viewport)
TOP_PAD = 60                            # CSS px of page above the "One command" paragraph
log = {"url": URL, "viewport": "1600x900", "device_scale_factor": 2.4,
       "captured_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}

RANGE_JS = """([el, ph]) => {
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n; const nodes = [];
  while (n = w.nextNode()) nodes.push(n);
  const full = nodes.map(x => x.textContent).join(""); const i = full.indexOf(ph); if (i < 0) return null;
  let pos = 0; const rects = [];
  for (const nd of nodes) { const L = nd.textContent.length, a = Math.max(i, pos), b = Math.min(i + ph.length, pos + L);
    if (a < b) { const r = document.createRange(); r.setStart(nd, a - pos); r.setEnd(nd, b - pos);
                 for (const q of r.getClientRects()) rects.push([q.x, q.y, q.width, q.height]); }
    pos += L; }
  return rects; }"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=2.4, color_scheme="light")
    pg = ctx.new_page()
    pg.goto(URL, wait_until="load", timeout=90000); pg.wait_for_timeout(2500)
    log["final_url"] = pg.url; log["title"] = pg.title()
    art = pg.locator("article.markdown-body").first
    head = pg.get_by_text("One command sets up your AI apps and the Blender addon").first
    y_doc = pg.evaluate("el => el.getBoundingClientRect().top + window.scrollY", head.element_handle())
    pg.evaluate(f"window.scrollTo(0, {y_doc - TOP_PAD})")
    pg.wait_for_timeout(1200)
    passages = {
        "installer_intro": "One command sets up your AI apps and the Blender addon:",
        "installer_cmd": "curl -LsSf https://www.mcp-for-blender.com/install.sh | sh",
        "finds_clients": "finds the MCP clients on your machine",
        "lets_you_pick": "lets you pick which to set up",
        "manual_setup": "Manual setup, in case the automatic setup doesn't work",
        "starts_on_open": "The addon starts its server when Blender opens.",
    }
    ae = art.element_handle()
    full_text = art.inner_text()
    clip_h = 900
    found = {}
    for k, ph in passages.items():
        rects = pg.evaluate(RANGE_JS, [ae, ph])
        found[k] = {"text": ph, "in_page_text": ph in full_text,
                    "rects_css": rects,
                    "rects_frac": [[round((r[0] - CLIP_X0) / (CLIP_X1 - CLIP_X0), 4), round(r[1] / clip_h, 4),
                                    round(r[2] / (CLIP_X1 - CLIP_X0), 4), round(r[3] / clip_h, 4)] for r in (rects or [])]}
    # the whole paragraph that holds 'finds ... lets you pick', verbatim, for the factcheck
    para = pg.locator("article.markdown-body p", has_text="lets you pick which to set up").first
    log["paragraph_finds_clients"] = para.inner_text()
    log["passages"] = found
    log["clip_css"] = {"x0": CLIP_X0, "x1": CLIP_X1, "y0": 0, "y1": clip_h}
    pg.screenshot(path=str(PUB / "a4_readme_installer.png"),
                  clip={"x": CLIP_X0, "y": 0, "width": CLIP_X1 - CLIP_X0, "height": clip_h})
    log["image"] = "lecture-a3assets/a4_readme_installer.png"
    log["image_aspect"] = round((CLIP_X1 - CLIP_X0) / clip_h, 4)
    b.close()

(HERE / "capture_readme.json").write_text(json.dumps(log, indent=1))
print(json.dumps(log, indent=1))
