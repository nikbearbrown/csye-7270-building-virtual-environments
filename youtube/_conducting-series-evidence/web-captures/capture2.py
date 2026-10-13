import json
from pathlib import Path
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright
OUT = Path(__file__).resolve().parent
PAGES = {"unity-ai-features": "https://unity.com/features/ai",
         "unity-mcp-docs": "https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.0/manual/unity-mcp-overview.html",
         "unity-ai-changelog": "https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.0/changelog/CHANGELOG.html",
         "unreal-5-8-release-notes": "https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes"}
rec = json.loads((OUT/"receipts.json").read_text())
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    page = b.new_page(viewport={"width":1600,"height":900}, device_scale_factor=2.4)
    for n,u in PAGES.items():
        try:
            r = page.goto(u, wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(4000)
            page.screenshot(path=str(OUT/f"{n}.png"))
            rec.append({"name":n,"url":u,"final_url":page.url,"status":r.status if r else None,"title":page.title(),"at":datetime.now(timezone.utc).isoformat()})
            print(n, r.status if r else None, page.title())
        except Exception as e:
            rec.append({"name":n,"url":u,"error":str(e)[:200]}); print(n,"ERR",str(e)[:100])
    b.close()
(OUT/"receipts.json").write_text(json.dumps(rec, indent=2)+"\n")
