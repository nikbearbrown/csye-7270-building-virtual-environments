#!/usr/bin/env python3
"""make_crops_act4.py — the REAL captures Act IV shows, cropped (never altered) into REEL/pantry/a4_*.png.
Re-run:  python3 evidence/act4/make_crops_act4.py
Page captures are 3840x2160 (1600x900 css at 2.4x); the boxes below are in 1280-space (x3 = capture pixels).
Game frames are stepped out of the real capture clip (walker-claude-jumpman-gameplay.mp4, 1920x1080, 30 fps) at 10 fps and scaled to 1280x720.
"""
import subprocess
from pathlib import Path
from PIL import Image
REEL = Path(__file__).resolve().parents[2]
EVID = REEL.parent / "_conducting-series-evidence"
WEB, CAP = EVID / "web-captures", EVID / "godot-captures"
PAN = REEL / "pantry"; PAN.mkdir(exist_ok=True)


def crop(src, box, out):
    im = Image.open(WEB / src).convert("RGB")
    x0, y0, x1, y1 = [int(v * 3) for v in box]
    c = im.crop((x0, y0, x1, y1)); c.save(PAN / out)
    print(out, c.size)


# Unity docs (docs.unity3d.com, Assistant 2.0.0-pre.1): the 'Unity MCP' page head, and the changelog entry that made MCP public
crop("unity-mcp-docs.png", (420, 140, 980, 320), "a4_unity_docs.png")
crop("unity-ai-changelog.png", (420, 240, 980, 366), "a4_unity_changelog.png")
# GitHub repo-header buttons (Sponsor / Notifications / Fork / Star); the repo name is set as a label beside them
crop("github-coding-solo-godot-mcp.png", (785, 142, 1130, 188), "a4_godot_mcp_banner.png")
crop("github-coplay-unity-mcp.png", (845, 142, 1130, 188), "a4_unity_mcp_banner.png")
# Godot Foundation: title, byline, date of the contribution-policy post
crop("godot-contribution-policy.png", (300, 560, 980, 648), "a4_policy_title.png")

# real gameplay frames (jump over the first pit), 10 fps
mp4 = CAP / "walker-claude" / "walker-claude-jumpman-gameplay.mp4"
for i in range(15):
    t = 2.2 + i * 0.1
    out = PAN / f"a4_game_{i:02d}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1", "-vf", "scale=1280:720", str(out)], check=True)
print("game frames a4_game_00..14 from", mp4.name, "t=2.2..3.6 s")
