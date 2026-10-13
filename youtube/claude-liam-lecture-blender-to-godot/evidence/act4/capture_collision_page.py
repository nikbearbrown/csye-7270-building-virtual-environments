"""Capture Godot's public 'Collision shapes (3D)' docs page for the B42 BrowserCapture beat (lecture-blender-to-godot, Act IV).
Public page, no sign-in, nothing typed. A 1280x1000 CSS-px window at device scale 3 -> a 3840x3000 PNG, scrolled so the primitive,
convex and concave paragraphs are all in the picture. It also writes the rectangles (as fractions of the image) of the three
sentences the camera rings. If the site serves a bot-challenge page instead of the docs page the script STOPS: it never tries to get past one.
Run:  python3 capture_collision_page.py <out.png> <out.json>"""
import sys, json, asyncio
from playwright.async_api import async_playwright
URL = "https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_3d.html"
VW, VH, DPR, SCROLL_TO = 1280, 1000, 3, "We recommend favoring primitive"
SENT = {"static": "You can only use concave shapes within StaticBodies.",
        "prim": "They often provide better performance as well.",
        "slow": "Concave shapes are the slowest option"}
JS = r"""([anchor, sents]) => {
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n, a = null; while (n = w.nextNode()) { if (n.nodeValue.includes(anchor)) { a = n.parentElement; break; } }
  window.scrollTo(0, a.getBoundingClientRect().top + window.scrollY - 18);
  const out = {scrollY: window.scrollY};
  // whitespace-insensitive search: collapse runs of whitespace, remembering where each kept character came from
  const flatten = (s) => { let f = '', map = [], prev = false;
    for (let i = 0; i < s.length; i++) { const sp = /\s/.test(s[i]); if (sp) { if (!prev) { f += ' '; map.push(i); } prev = true; } else { f += s[i]; map.push(i); prev = false; } }
    return [f, map]; };
  for (const [k, t] of Object.entries(sents)) {
    const w2 = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let m;
    while (m = w2.nextNode()) { const [f, map] = flatten(m.nodeValue); const i = f.indexOf(t);
      if (i >= 0) { const r = document.createRange(); r.setStart(m, map[i]); r.setEnd(m, map[i + t.length - 1] + 1);
        const b = r.getBoundingClientRect(); out[k] = [b.x, b.y, b.width, b.height]; break; } }
  }
  return out;
}"""
async def main(png, js):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await (await b.new_context(viewport={"width": VW, "height": VH}, device_scale_factor=DPR)).new_page()
        await pg.goto(URL, wait_until="load"); await pg.wait_for_timeout(2500)
        title = await pg.title(); print("title:", title)
        if "moment" in title.lower() or "challenge" in title.lower() or "attention" in title.lower():
            print("BOT-CHALLENGE PAGE SERVED - stopping, not trying to get past it"); await b.close(); sys.exit(3)
        res = await pg.evaluate(JS, [SCROLL_TO, SENT]); await pg.wait_for_timeout(600)
        await pg.screenshot(path=png)
        frac = {k: [v[0] / VW, v[1] / VH, v[2] / VW, v[3] / VH] for k, v in res.items() if k != "scrollY"}
        json.dump({"url": URL, "viewport_css": [VW, VH], "dpr": DPR, "scrollY": res["scrollY"], "rects_frac": frac}, open(js, "w"), indent=1)
        print("saved", png, js); print(json.dumps(frac, indent=1)); await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
