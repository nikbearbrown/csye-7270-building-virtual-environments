"""Capture the public pages the three CSYE 7270 Start Here films name. Real pages, real date; nothing invented."""
import json
from pathlib import Path
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
PAGES = {
    "godot-home": "https://godotengine.org/",
    "godot-license": "https://godotengine.org/license/",
    "godot-download-mac": "https://godotengine.org/download/macos/",
    "godot-contribution-policy": "https://godotengine.org/article/contribution-policy-2026/",
    "godot-cli-docs": "https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html",
    "godot-tscn-docs": "https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html",
    "unity-mcp-blog": "https://unity.com/blog/unity-ai-mcp-how-to-get-started",
    "unreal-mcp-docs": "https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor",
    "github-coding-solo-godot-mcp": "https://github.com/Coding-Solo/godot-mcp",
    "github-coplay-unity-mcp": "https://github.com/CoplayDev/unity-mcp",
    "github-walker": "https://github.com/nikbearbrown/walker",
    "github-walker-jumpman-clawd": "https://github.com/nikbearbrown/walker-jumpman-clawd",
}
receipts = []
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, channel="chrome")
    page = b.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=2.4)
    for name, url in PAGES.items():
        try:
            r = page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3500)
            page.screenshot(path=str(OUT / f"{name}.png"))
            receipts.append({"name": name, "url": url, "final_url": page.url, "status": r.status if r else None,
                             "title": page.title(), "at": datetime.now(timezone.utc).isoformat()})
        except Exception as e:
            receipts.append({"name": name, "url": url, "error": str(e)[:200]})
    b.close()
(OUT / "receipts.json").write_text(json.dumps(receipts, indent=2) + "\n")
for r in receipts: print(r["name"], r.get("status"), r.get("title") or r.get("error"))
