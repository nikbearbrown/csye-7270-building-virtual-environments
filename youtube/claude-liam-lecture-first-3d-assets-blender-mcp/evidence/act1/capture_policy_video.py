#!/usr/bin/env python3
"""Act I B14 evidence: capture the public YouTube page of the required AI-policy video, with NO sign-in.
  https://www.youtube.com/watch?v=8Ut0Cdl6vMw   (the assignment's link, without its share-tracking parameter)
1600x900 viewport at device scale 2.4 (3840-wide PNG). No login; no consent button is clicked (if a consent wall appears, the
capture is abandoned and B14 falls back to a card with the video's real title).
Outputs: TK/runtime/remotion/public/lecture-a3assets/a1_policy_video.png  (for BrowserCapture, B14)
         capture_policy_video.json (url, UTC time, final url, page title, the video title element's text and box)
"""
import json, datetime, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PUB = pathlib.Path("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/public/lecture-a3assets")
PUB.mkdir(parents=True, exist_ok=True)
URL = "https://www.youtube.com/watch?v=8Ut0Cdl6vMw"
log = {"captured_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
       "viewport": "1600x900", "device_scale_factor": 2.4, "url": URL}
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=2.4, color_scheme="light", locale="en-US")
    pg = ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(6000)
    log["final_url"] = pg.url
    log["page_title"] = pg.title()
    log["consent_wall"] = "consent." in pg.url
    t = pg.locator("ytd-watch-metadata h1").first
    try:
        t.wait_for(timeout=15000)
        log["video_title"] = t.inner_text()
        log["video_title_box"] = t.bounding_box()
    except Exception as e:
        log["video_title"] = None; log["error"] = str(e)[:300]
    try:
        ch = pg.locator("ytd-watch-metadata ytd-channel-name").first
        log["channel"] = ch.inner_text(); log["channel_box"] = ch.bounding_box()
    except Exception as e:
        log["channel"] = None
    pg.screenshot(path=str(PUB / "a1_policy_video.png"))
    b.close()
(HERE / "capture_policy_video.json").write_text(json.dumps(log, indent=1))
print(json.dumps(log, indent=1))
