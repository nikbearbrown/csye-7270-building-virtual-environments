import asyncio, json
from playwright.async_api import async_playwright
URL = "https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_3d.html"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await (await b.new_context(viewport={"width":1280,"height":900}, device_scale_factor=3)).new_page()
        await pg.goto(URL, wait_until="load"); await pg.wait_for_timeout(2500)
        js = """() => {
          const out = {};
          const find = (t) => { const ps=[...document.querySelectorAll('div[itemprop=articleBody] p, div[itemprop=articleBody] h2')]; return ps.find(e=>e.innerText.includes(t)); };
          for (const [k,t] of Object.entries({prim:'We recommend favoring primitive', convexH:'Convex collision shapes', convexP:'compromise', concaveH:'Concave or trimesh collision shapes', concaveP:'You can only use concave shapes'})) {
            const e = (k==='convexH') ? [...document.querySelectorAll('div[itemprop=articleBody] h2')].find(h=>h.innerText.startsWith('Convex')) : (k==='concaveH') ? [...document.querySelectorAll('div[itemprop=articleBody] h2')].find(h=>h.innerText.startsWith('Concave')) : find(t);
            if (!e) { out[k]=null; continue; }
            const r = e.getBoundingClientRect();
            out[k] = {x:r.x+window.scrollX, y:r.y+window.scrollY, w:r.width, h:r.height};
          }
          const art = document.querySelector('div[itemprop=articleBody]').getBoundingClientRect();
          out.article = {x:art.x, y:art.y+window.scrollY, w:art.width, h:art.height};
          out.docH = document.documentElement.scrollHeight;
          return out;
        }"""
        print(json.dumps(await pg.evaluate(js), indent=1))
        await b.close()
asyncio.run(main())
