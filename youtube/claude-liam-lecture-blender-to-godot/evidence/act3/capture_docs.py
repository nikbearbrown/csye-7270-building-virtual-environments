# ACT III capture (B28): two public Godot documentation pages, as themselves. No sign-in, no cookies edited.
#   python3 capture_docs.py   -> pantry/a3_docs_collision.png, pantry/a3_docs_export.png (the section's heading + paragraph,
#                                 DPR 3.2 clip of the live page) and capture_docs.json (page URLs, capture date, and the
#                                 phrase's rectangle as fractions of each crop, for the ring)
import json, os, datetime
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
PANTRY = os.path.abspath(os.path.join(HERE, "..", "..", "pantry"))
PAGES = [
  # name, url, heading text (None = none), the phrase to ring (inside one paragraph)
  ("a3_docs_collision", "https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_3d.html",
   "Performance caveats", "avoid translating, rotating, or scaling CollisionShapes"),
  ("a3_docs_export", "https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/model_export_considerations.html",
   None, "apply the object transform in the 3D modeling software before exporting the scene"),
]
meta = {"captured": datetime.date.today().isoformat()}
JS = """([needle, heading]) => {
  const ps = [...document.querySelectorAll('p')].filter(e => e.innerText.includes(needle));
  const p = ps[ps.length - 1]; p.scrollIntoView({block: 'center'});
  const pr = p.getBoundingClientRect();
  let top = pr.top;
  if (heading) { const h = [...document.querySelectorAll('h2')].find(e => e.innerText.includes(heading)); if (h) top = h.getBoundingClientRect().top; }
  // the phrase's line boxes
  const w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT); let n, rects = [];
  const full = p.innerText; const start = full.indexOf(needle);
  let acc = 0;
  while ((n = w.nextNode())) {
    const t = n.textContent; const s = Math.max(start, acc), e = Math.min(start + needle.length, acc + t.length);
    if (s < e) { const r = document.createRange(); r.setStart(n, s - acc); r.setEnd(n, e - acc); for (const b of r.getClientRects()) rects.push([b.left, b.top, b.right, b.bottom]); }
    acc += t.length;
  }
  return {left: pr.left, right: pr.right, top, bottom: pr.bottom, rects, text: p.innerText};
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=3.2)
    for name, url, heading, needle in PAGES:
        pg = ctx.new_page(); pg.goto(url, wait_until="networkidle"); pg.wait_for_timeout(800)
        r = pg.evaluate(JS, [needle, heading]); pg.wait_for_timeout(500)
        pad = 14
        clip = {"x": r["left"] - pad, "y": r["top"] - pad, "width": (r["right"] - r["left"]) + 2 * pad, "height": (r["bottom"] - r["top"]) + 2 * pad}
        pg.screenshot(path=os.path.join(PANTRY, name + ".png"), clip=clip)
        # the phrase as fractions of the crop (one box per line it wraps over)
        boxes = [[(x0 - clip["x"]) / clip["width"], (y0 - clip["y"]) / clip["height"], (x1 - clip["x"]) / clip["width"], (y1 - clip["y"]) / clip["height"]] for x0, y0, x1, y1 in r["rects"]]
        meta[name] = {"url": url, "crop_css": clip, "phrase_line_boxes_frac": boxes, "paragraph": r["text"]}
        print(name, clip, len(boxes), "line box(es)")
        pg.close()
    b.close()
json.dump(meta, open(os.path.join(HERE, "capture_docs.json"), "w"), indent=1)
