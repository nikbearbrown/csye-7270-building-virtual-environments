#!/usr/bin/env python3
"""Act II B11/B12 evidence: capture the two real, public, sign-in-free pages that carry the no-authentication / no-guards warnings.
  community README : https://github.com/ahujasid/mcp-for-blender            (the blockquote that says the socket has no authentication)
  Blender Lab page : https://www.blender.org/lab/mcp-server/                (the 'Security Warning' paragraph)
1600x900 viewport at device scale 2.4 (3840-wide PNG). No login, no cookies accepted/declined beyond what the page does by default.
Outputs: TK/runtime/remotion/public/lecture-blender-to-godot/a2_community_readme.png  (for BrowserCapture, B11)
         ../../pantry/a2_lab_warning.png                                              (a crop of the Security Warning, for B12)
         capture_log.json (url, UTC time, what was found)
"""
import json, datetime, pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
REEL = HERE.parent.parent
PUB = pathlib.Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/lecture-blender-to-godot")
PUB.mkdir(parents=True, exist_ok=True)
log = {"captured_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "viewport": "1600x900", "device_scale_factor": 2.4}

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=2.4, color_scheme="light")
    pg = ctx.new_page()

    # ── community README ──
    url = "https://github.com/ahujasid/mcp-for-blender"
    pg.goto(url, wait_until="networkidle", timeout=60000)
    log["community_url"] = url; log["community_final_url"] = pg.url; log["community_title"] = pg.title()
    bq = pg.locator("article.markdown-body blockquote", has_text="no authentication or encryption").first
    bq.scroll_into_view_if_needed()
    pg.evaluate("el => el.scrollIntoView({block:'center'})", bq.element_handle())
    pg.wait_for_timeout(1200)
    log["community_note_text"] = bq.inner_text()
    log["community_note_box"] = bq.bounding_box()
    # where the two phrases the narration names sit on screen (css px in the 1600x900 viewport), for the BrowserCapture rings
    log["community_phrase_boxes"] = bq.evaluate("""el => {
      const out = {};
      const want = ["has no authentication or encryption", "anyone who can reach that port can run Python inside Blender"];
      const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      let n; const nodes = []; while (n = w.nextNode()) nodes.push(n);
      const full = nodes.map(x => x.textContent).join("");
      for (const ph of want) {
        const i = full.indexOf(ph); if (i < 0) { out[ph] = null; continue; }
        let pos = 0, rects = [];
        for (const nd of nodes) {
          const L = nd.textContent.length, a = Math.max(i, pos), b = Math.min(i + ph.length, pos + L);
          if (a < b) { const r = document.createRange(); r.setStart(nd, a - pos); r.setEnd(nd, b - pos);
                       for (const q of r.getClientRects()) rects.push([q.x, q.y, q.width, q.height]); }
          pos += L;
        }
        out[ph] = rects;
      }
      return out; }""")
    pg.screenshot(path=str(PUB / "a2_community_readme.png"))

    # ── Blender Lab page ──
    url2 = "https://www.blender.org/lab/mcp-server/"
    pg.goto(url2, wait_until="networkidle", timeout=60000)
    log["lab_url"] = url2; log["lab_final_url"] = pg.url; log["lab_title"] = pg.title()
    h = pg.get_by_text("Security Warning", exact=True).first
    h.scroll_into_view_if_needed()
    pg.evaluate("el => el.scrollIntoView({block:'center'})", h.element_handle())
    pg.wait_for_timeout(1200)
    log["lab_heading_box"] = h.bounding_box()
    para = pg.get_by_text("The MCP server will execute LLM generated code").first
    log["lab_warning_text"] = para.inner_text(); log["lab_warning_box"] = para.bounding_box()
    pg.screenshot(path=str(PUB / "a2_lab_page.png"))
    b.close()

(HERE / "capture_log.json").write_text(json.dumps(log, indent=1))
print(json.dumps(log, indent=1))
