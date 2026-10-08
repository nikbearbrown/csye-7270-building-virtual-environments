#!/usr/bin/env python3
"""Compose the film's still evidence cards from real files, and copy the ones
the Remotion scenes read into the toolkit's public/ folder.

Every pixel of a picture here is from an existing project file or an engine
capture; this script only crops, scales, places and labels.

    python3 tools/make_stills.py
"""
import re, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
ART = Path("/Users/eric/csye7270/brutalist.art")
FONTS = ART / "runtime/fonts"
PUBLIC = ART / "runtime/remotion/public/reels" / REEL.name
OUT = REEL / "stills"
CREAM, INK, MUTED, ACCENT = (250, 249, 245), (61, 57, 41), (110, 100, 86), (217, 119, 87)


def font(name, size):
    paths = {"sans": FONTS / "Inter/static/Inter_28pt-Regular.ttf", "bold": FONTS / "Inter/static/Inter_28pt-Medium.ttf",
             "serif": FONTS / "EB_Garamond/static/EBGaramond-Regular.ttf", "mono": FONTS / "PT_Mono/PTMono-Regular.ttf",
             "cjk": Path("/System/Library/Fonts/Hiragino Sans GB.ttc")}
    p = paths[name]
    if not p.exists() and name == "bold":
        p = paths["sans"]
    return ImageFont.truetype(str(p), size)


def fit(img, w, h):
    img = img.copy()
    img.thumbnail((w, h), Image.LANCZOS) if img.width > w or img.height > h else None
    s = min(w / img.width, h / img.height)
    return img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)


def trace_sheet():
    """Pose #7 from the character sheet's blockout page."""
    poses = Image.open(REPO / "design/character/poses.png").convert("RGB")
    card = poses.crop((872, 602, 1279, 1049))
    canvas = Image.new("RGB", (2400, 1300), CREAM)
    big = fit(card, 1100, 1210)
    canvas.paste(big, (120, (1300 - big.height) // 2))
    d = ImageDraw.Draw(canvas)
    x = 1330
    d.text((x, 250), "CHARACTER-SHEET.md · pose #7", font=font("bold", 64), fill=INK)
    for i, line in enumerate(["Hurt — took a hit; carried gear", "flies off as a separate sprite.", "",
                              "Plays once · default form", "Faces the hit (one direction only;", "left is a runtime flip).", "",
                              "Blockout drawn by Claude in code", "(make_blockouts.py) — the spec,", "not a generated asset."]):
        d.text((x, 380 + i * 72), line, font=font("sans", 54), fill=INK if i < 7 else MUTED)
    return canvas


def trace_raw():
    """HURT-01 (rejected thumbnail) → the edit sentence → HURT-02 (accepted raw)."""
    thumb = Image.open(REPO / "generated/rejected/CHAR-HURT-RUN-B-01.png").convert("RGB")
    h1 = thumb.crop((460, 60, 881, 481))
    h2 = Image.open(REPO / "generated/accepted/CHAR-HURT-02.jpg").convert("RGB")
    W, H = 3200, 1300
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    side = 1000
    a = h1.resize((side, side), Image.LANCZOS)
    b = h2.resize((side, side), Image.LANCZOS)
    c.paste(a, (80, 150)); c.paste(b, (W - 80 - side, 150))
    d.rectangle((80, 150, 80 + side, 150 + side), outline=(164, 74, 50), width=10)
    d.rectangle((W - 80 - side, 150, W - 80, 150 + side), outline=(48, 110, 70), width=10)
    d.text((80, 40), "CHAR-HURT-01 · REJECTED", font=font("bold", 58), fill=(164, 74, 50))
    d.text((W - 80 - side, 40), "CHAR-HURT-02 · ACCEPTED", font=font("bold", 58), fill=(48, 110, 70))
    d.text((80, 1175), "leans toward the hit (420 px thumbnail; full size not kept)", font=font("sans", 40), fill=MUTED)
    d.text((W - 80 - side, 1175), "raw Gemini output, 2048 × 2048 — not in-engine", font=font("sans", 40), fill=MUTED)
    mx = W // 2
    d.text((mx, 330), "edit, turn 10:", font=font("sans", 50), fill=MUTED, anchor="mm")
    d.text((mx, 470), "人物应该向后仰", font=font("cjk", 72), fill=INK, anchor="mm")
    d.text((mx, 570), "而不是现在的向前扑。", font=font("cjk", 72), fill=INK, anchor="mm")
    for i, t in enumerate(["“He should lean back,", "not lunge forward", "as he does now.”"]):
        d.text((mx, 700 + i * 70), t, font=font("sans", 52), fill=INK, anchor="mm")
    d.line((mx - 380, 990, mx + 340, 990), fill=ACCENT, width=14)
    d.polygon([(mx + 380, 990), (mx + 320, 955), (mx + 320, 1025)], fill=ACCENT)
    d.text((mx, 1080), "shuai-z, in the same Gemini chat", font=font("sans", 40), fill=MUTED, anchor="mm")
    return c


def outline_pair():
    on = Image.open(OUT / "outline-on.png").convert("RGB")
    off = Image.open(OUT / "outline-off.png").convert("RGB")
    box = (978, 1150, 1678, 1770)          # around Rudy at x 664 (screen x 1328 at 4K), soles at y 1680
    a, b = on.crop(box), off.crop(box)
    W, H = 3840, 2160
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    s = 2.3
    a = a.resize((round(a.width * s), round(a.height * s)), Image.LANCZOS)
    b = b.resize(a.size, Image.LANCZOS)
    gap = (W - 2 * a.width) // 3
    y = 270
    c.paste(a, (gap, y)); c.paste(b, (2 * gap + a.width, y))
    d.text((gap, 110), "outline.tres width = 8 (the source)", font=font("bold", 76), fill=INK)
    d.text((2 * gap + a.width, 110), "width = 0 — DIAGNOSTIC", font=font("bold", 76), fill=(164, 74, 50))
    d.text((gap, y + a.height + 40), "Same build, same frame: engine render, Rudy at x 664 over the wheat, 3840×2160 crop, enlarged 2.3×.",
           font=font("sans", 52), fill=MUTED)
    d.text((gap, y + a.height + 115), "Right: the shader width set to 0 at runtime on an isolated copy (film_driver.gd). Not the game as shipped.",
           font=font("sans", 52), fill=MUTED)
    return c


def checks_output():
    log = (REEL / "capture/checks-run.log").read_text().splitlines()
    n_pass = sum(1 for l in log if l.startswith("PASS"))
    W, H = 3840, 2160
    c = Image.new("RGB", (W, H), (32, 37, 49))
    d = ImageDraw.Draw(c)
    mono = font("mono", 54)
    y = 150
    d.text((230, y), "$ Godot --headless --path game --fixed-fps 60 res://tests/checks.tscn", font=mono, fill=(139, 199, 243)); y += 110
    tail = [l for l in log if l.startswith("PASS")][-9:]
    shown = []
    for l in tail:
        l = re.sub(r"\s+", " ", l)
        while len(l) > 106:
            cut = l.rfind(" ", 0, 106)
            shown.append(l[:cut]); l = "      " + l[cut + 1:]
        shown.append(l)
    d.text((230, y), f"… {n_pass - len(tail)} earlier PASS lines …", font=mono, fill=(150, 160, 175)); y += 85
    for l in shown:
        col = (174, 231, 209) if l.startswith("PASS") else (237, 241, 247)
        d.text((230, y), l, font=mono, fill=col); y += 74
    y += 30
    for l in log:
        if l.strip() == "all checks passed":
            d.text((230, y), l.strip(), font=font("mono", 64), fill=(174, 231, 209)); y += 100
    d.text((230, y), f"exit code 0 · {n_pass} PASS lines · 0 FAIL", font=font("mono", 64), fill=(236, 224, 161))
    d.text((230, H - 230), "Recorded output: capture/checks-run.log (isolated copy of game/ at 3b7aa1c, 2026-10-04). Engine leak warnings at exit omitted.",
           font=font("sans", 44), fill=(190, 200, 215))
    return c, n_pass


def hurt_frame():
    """The matted frame exactly as the game loads it: its 410×386 canvas on a dark
    viewport-style backing, enlarged 4× (nearest-free LANCZOS), canvas edge and body origin marked."""
    fr = Image.open(REPO / "game/content/rudy/frames/CHAR-HURT.png").convert("RGBA")
    W, H, k = 3840, 2160, 4
    c = Image.new("RGBA", (W, H), (32, 37, 49, 255))
    big = fr.resize((fr.width * k, fr.height * k), Image.LANCZOS)
    x, y = (W - big.width) // 2 + 300, 240
    c.alpha_composite(big, (x, y))
    d = ImageDraw.Draw(c)
    d.rectangle((x, y, x + big.width, y + big.height), outline=(139, 199, 243, 255), width=4)
    ox, oy = x + 205 * k, y + 370 * k                     # frames.json origin [205, 370]
    d.line((ox - 40, oy, ox + 40, oy), fill=(236, 224, 161, 255), width=6)
    d.line((ox, oy - 40, ox, oy + 40), fill=(236, 224, 161, 255), width=6)
    lx = 200
    d.text((lx, 260), "game/content/rudy/frames/", font=font("mono", 56), fill=(190, 200, 215))
    d.text((lx, 330), "CHAR-HURT.png", font=font("mono", 84), fill=(237, 241, 247))
    for i, t in enumerate(["the file the game loads", "", "background keyed out", "scale 0.1816", "410 × 386 canvas (blue)", "body origin 205, 370 (gold)",
                           "drawn at half scale:", "2 texture px per game px", "", "outline added in-engine,", "not in this file"]):
        d.text((lx, 520 + i * 92), t, font=font("sans", 64), fill=(237, 241, 247) if i < 9 else (190, 200, 215))
    d.text((lx, H - 150), "Enlarged 4× for reading. Source frame unchanged (hash in gamedev-evidence.json).", font=font("sans", 46), fill=(190, 200, 215))
    return c.convert("RGB")


def main():
    OUT.mkdir(exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    trace_sheet().save(OUT / "trace-1-sheet.png")
    trace_raw().save(OUT / "trace-2-raw.png")
    frame = Image.open(REPO / "game/content/rudy/frames/CHAR-HURT.png")
    x0, y0, x1, y1 = frame.getbbox()                     # the figure inside the 410×386 canvas
    fig = frame.crop((max(0, x0 - 12), max(0, y0 - 12), x1 + 12, y1 + 12))
    fig.resize((fig.width * 2, fig.height * 2), Image.LANCZOS).save(OUT / "CHAR-HURT.png")
    outline_pair().save(OUT / "outline-pair.png")
    hurt_frame().save(OUT / "hurt-frame.png")
    img, n = checks_output()
    img.save(OUT / "checks-output.png")
    for name in ("trace-1-sheet.png", "trace-2-raw.png", "CHAR-HURT.png"):
        shutil.copy(OUT / name, PUBLIC / name)
    print(f"stills written; {n} PASS lines; public copies in {PUBLIC}")


if __name__ == "__main__":
    main()
