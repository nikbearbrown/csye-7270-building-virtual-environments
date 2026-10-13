"""Fetch the visible text of a public Godot docs page (for the factcheck). Stops if a bot-challenge page is served.
Run: python3 fetch_docs_text.py <url> <out.txt>"""
import sys, asyncio
from playwright.async_api import async_playwright
async def main(url, out):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await (await b.new_context(viewport={"width":1280,"height":720})).new_page()
        await pg.goto(url, wait_until="load"); await pg.wait_for_timeout(2000)
        t = await pg.title(); print("title:", t)
        if "moment" in t.lower() or "challenge" in t.lower():
            print("BOT-CHALLENGE PAGE - stopping"); await b.close(); sys.exit(3)
        txt = await pg.inner_text("div[itemprop=articleBody]")
        open(out, "w").write(f"SOURCE: {url}\n\n" + txt); print("saved", out, len(txt))
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
