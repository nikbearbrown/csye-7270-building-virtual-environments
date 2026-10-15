#!/usr/bin/env python3
"""Compose the film's still evidence cards from real files, and copy the ones
the Remotion scenes read into the toolkit's public/ folder.

Every picture here is an existing project file, a Blender viewport image that
Claude captured through the MCP's look tool (blender-looks/), or a recorded
log; this script only crops, scales, places and labels.

    python3 tools/make_stills.py        # from the reel folder
"""
import re, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
A3 = REEL.parents[1]                        # fall-2026/shuai-z/assignment-3
A2GAME = A3.parent / "assignment-2/game"    # the 2D game the props come from
ART = Path("/Users/eric/csye7270/brutalist.art")
FONTS = ART / "runtime/fonts"
PUBLIC = ART / "runtime/remotion/public/reels" / REEL.name
OUT = REEL / "stills"
LOOKS = REEL / "blender-looks"
W, H = 3840, 2160
CREAM, INK, MUTED, ACCENT = (250, 249, 245), (61, 57, 41), (110, 100, 86), (217, 119, 87)
RED, GREEN = (164, 74, 50), (48, 110, 70)
DARK, DTEXT, DMUTED = (32, 37, 49), (237, 241, 247), (190, 200, 215)


def font(name, size):
    paths = {"sans": FONTS / "Inter/static/Inter_28pt-Regular.ttf", "bold": FONTS / "Inter/static/Inter_28pt-Medium.ttf",
             "mono": FONTS / "PT_Mono/PTMono-Regular.ttf", "cjk": Path("/System/Library/Fonts/Hiragino Sans GB.ttc")}
    return ImageFont.truetype(str(paths[name]), size)


def scaled(img, k):
    return img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)


def tile(name, i, cols):
    """One view from a look image: tiles of equal size separated by 4 px lines."""
    im = Image.open(LOOKS / name).convert("RGB")
    rows = round(im.height / (im.width / cols))
    tw, th = (im.width - 4 * (cols - 1)) // cols, (im.height - 4 * (rows - 1)) // rows
    x, y = (i % cols) * (tw + 4), (i // cols) * (th + 4)
    return im.crop((x, y, x + tw, y + th))


def game_props():
    """Rudy and the three props from the 2D game, at one common scale: every
    file is drawn at 1/density, so 1 game px = the same on-screen size."""
    items = [("content/rudy/frames/CHAR-IDLE.png", (205, 370), "Rudy", "160 px = 1.2 m"),
             ("content/level_1/art/ENV-SPIKES.png", (118, 140), "Spikes · hazard", "touching them costs a heart"),
             ("content/level_1/art/ENV-WAYSTONE-LIT.png", (106, 235), "Waystone · checkpoint", "he gets back up here"),
             ("content/level_1/art/ENV-PORTAL.png", (312, 99), "Teleport circle · the end", "stepping on it ends Level 1")]
    k = 2.0                      # screen px per texture px (density 2 → 4 per game px)
    c = Image.new("RGB", (3300, 1260), CREAM)
    d = ImageDraw.Draw(c)
    ground = 880
    x = 120
    line_end = None
    for path, (ox, oy), name, role in items:
        src = Image.open(A2GAME / path).convert("RGBA")
        bx = src.getbbox()
        big = scaled(src.crop(bx), k)
        ox2, oy2 = (ox - bx[0]) * k, (oy - bx[1]) * k
        if path.endswith("PORTAL.png"):
            line_end = round(x) - 40          # the circle lies on the ground: the line stops short of it
        c.paste(big, (round(x), round(ground - oy2)), big)
        cx = x + ox2
        below = max(ground, round(ground - oy2) + big.height)
        d.text((cx, below + 80), name, font=font("bold", 54), fill=INK, anchor="mm")
        d.text((cx, below + 150), role, font=font("sans", 44), fill=MUTED, anchor="mm")
        x += big.width + 230
    d.line((60, ground, line_end, ground), fill=(204, 196, 182), width=4)
    d.text((60, 30), "walker-rudy, Level 1 — the game's own 2D files, all drawn at one scale", font=font("bold", 50), fill=INK)
    return c


def game_card():
    """B02 as a full 4K still: the game-props figure with its title and source."""
    fig = game_props()
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    d.text((200, 110), "The Game, and Why These Three", font=font("bold", 84), fill=INK)
    d.rounded_rectangle((200, 250, 1660, 340), radius=12, fill=(48, 61, 52))
    d.text((230, 270), "ASSIGNMENT 2'S 2D ART — the source of each size", font=font("bold", 44), fill=(255, 253, 248))
    fig = scaled(fig, 3440 / fig.width)
    c.paste(fig, (200, 420))
    d.text((200, H - 230), "Source: assignment-2/game/ CHAR-IDLE.png, ENV-SPIKES.png, ENV-WAYSTONE-LIT.png, ENV-PORTAL.png, each drawn at 1/density",
           font=font("sans", 44), fill=MUTED)
    d.text((200, H - 170), "(props.json, frames.json: density 2). Rudy = 160 game px = 1.2 m (CHANGE-BRIEF.md).", font=font("sans", 44), fill=MUTED)
    return c


def brief():
    rows = [("", "Size W × D × H (m)", "Origin", "Shapes", "Triangle budget"),
            ("Waystone", "0.70 × 0.40 × 0.84", "underside centre", "4 → 5", "60 → 130 (rev. 2)"),
            ("Teleport circle", "2.25 × 2.25 × 0.08", "underside centre", "6", "300"),
            ("Spikes", "0.80 × 0.30 × 0.47", "underside centre", "6", "100")]
    c = Image.new("RGB", (3300, 1260), CREAM)
    d = ImageDraw.Draw(c)
    xs = [80, 720, 1500, 2160, 2560]
    y = 70
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            d.text((xs[j], y), v, font=font("bold" if i == 0 or j == 0 else "sans", 58 if i else 46), fill=INK if i else MUTED)
        y += 120 if i else 90
        d.line((80, y - 22, 3220, y - 22), fill=(214, 207, 194), width=3)
    y += 30
    d.text((80, y), "Predicted failures (each with its check):", font=font("bold", 52), fill=INK); y += 90
    preds = ["1 lying on its side (Z-up vs Y-up)", "2 wrong size by a factor", "3 origin in the middle: floats or sinks",
             "4 over the triangle budget", "5 a colour lost in the export", "6 more detail than asked"]
    for i, p in enumerate(preds):
        d.text((80 + (i % 2) * 1600, y + (i // 2) * 82), p, font=font("sans", 50), fill=INK)
    return c


def blender_own():
    a = Image.open(A3 / "evidence/blender-notes-cube-selected.png").convert("RGB")
    b = Image.open(A3 / "evidence/mcp-panel-connected.png").convert("RGB")
    hgt = 1060
    a, b = scaled(a, hgt / a.height), scaled(b, hgt / b.height)
    c = Image.new("RGB", (a.width + b.width + 180, hgt + 230), CREAM)
    d = ImageDraw.Draw(c)
    c.paste(a, (40, 40)); c.paste(b, (a.width + 140, 40))
    d.text((40, hgt + 70), "Blender 5.2.2: the default Cube selected, sidebar (N) on Item", font=font("sans", 46), fill=INK)
    d.text((a.width + 140, hgt + 70), "MCP for Blender tab:", font=font("sans", 46), fill=INK)
    d.text((a.width + 140, hgt + 130), "connected, port 9876", font=font("sans", 46), fill=INK)
    return c


def code_lines(path, a, b):
    return (A3 / path).read_text().splitlines()[a - 1:b]


def prompt_code():
    """shuai-z's prompt (verbatim) → the code Claude then ran (verbatim lines)."""
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    d.text((200, 120), "One prompt → the code Claude ran in my Blender", font=font("bold", 84), fill=INK)
    d.rounded_rectangle((200, 300, 1500, 1180), radius=28, fill=(240, 236, 226), outline=(214, 207, 194), width=4)
    d.text((260, 350), "shuai-z → Claude Code, 2026-10-13 20:14 EDT", font=font("sans", 44), fill=MUTED)
    d.text((260, 470), "现在不好看，不用R，", font=font("cjk", 84), fill=INK)
    d.text((260, 590), "把符文换成一个圆环试试", font=font("cjk", 84), fill=INK)
    for i, t in enumerate(["“It does not look good now. No R —", "try turning the rune into a ring.”"]):
        d.text((260, 760 + i * 74), t, font=font("sans", 58), fill=INK)
    d.text((260, 1010), "verbatim from the session; translation by Claude", font=font("sans", 40), fill=MUTED)
    d.line((1560, 740, 1700, 740), fill=ACCENT, width=14)
    d.polygon([(1740, 740), (1690, 705), (1690, 775)], fill=ACCENT)
    a, b = 301, 311
    lines = code_lines("tools/blender/build_waystone.py", a, b)
    d.rounded_rectangle((1800, 300, 3640, 1500), radius=20, fill=DARK)
    d.text((1850, 330), "tools/blender/build_waystone.py", font=font("mono", 44), fill=(139, 199, 243))
    y = 420
    for n, line in enumerate(lines, a):
        while len(line) > 58:
            cut = line.rfind(" ", 0, 58) if line.rfind(" ", 0, 58) > 10 else 58
            d.text((1850, y), f"{n:>3}", font=font("mono", 38), fill=(120, 130, 145))
            d.text((1960, y), line[:cut], font=font("mono", 38), fill=DTEXT); y += 54
            line, n = "    " + line[cut:].lstrip(), ""
        d.text((1850, y), f"{n:>3}" if n != "" else "", font=font("mono", 38), fill=(120, 130, 145))
        d.text((1960, y), line, font=font("mono", 38), fill=(186, 197, 188) if line.lstrip().startswith("#") else DTEXT)
        y += 54
    d.text((200, 1600), f"Code: lines {a}–{b}, verbatim — one execute_blender_code call, run through MCP for Blender 2.1.9.",
           font=font("sans", 50), fill=INK)
    d.text((200, 1690), "Every call Claude ran is kept, in order, in tools/blender/ (Assignment 3 requirement).", font=font("sans", 50), fill=MUTED)
    return c


def prompt_result():
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    d.text((200, 120), "What it built — Blender viewport, material preview", font=font("bold", 84), fill=INK)
    a = scaled(Image.open(LOOKS / "4-trial-ring-8.png").convert("RGB"), 2.1)
    c.paste(a, ((W - a.width) // 2, 330))
    d.text((W // 2, 330 + a.height + 90), "An 8-sided ring, as asked: 5 shapes, 86 triangles. My next prompt asked for 12 sides and a thinner band.",
           font=font("sans", 58), fill=INK, anchor="mm")
    d.text((200, H - 260), "Captured by Claude through the MCP's look tool during the live session, 2026-10-13 20:15 EDT "
           "(front and three-quarter views).", font=font("sans", 46), fill=MUTED)
    d.text((200, H - 190), "Not my own screenshot, and not a recording: the tool's image, enlarged 2.1× for reading.",
           font=font("sans", 46), fill=MUTED)
    return c


def hand_edit():
    """Before/after stills (the user's option b): no recording of the edit exists."""
    before, after = tile("1-built-rectangle.png", 0, 2), tile("2-after-hand-edit.png", 0, 2)
    k = 1250 / before.height
    before, after = scaled(before, k), scaled(after, k)
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    d.text((200, 100), "My hand edit: the rune moved up 0.034 m", font=font("bold", 84), fill=INK)
    y0 = 300
    xb, xa = 200, 200 + before.width + 160
    c.paste(before, (xb, y0)); c.paste(after, (xa, y0))
    d.text((xb, y0 + before.height + 30), "BEFORE — as Claude built it", font=font("bold", 56), fill=INK)
    d.text((xb, y0 + before.height + 105), "captured 19:58 EDT, live session", font=font("sans", 44), fill=MUTED)
    d.text((xa, y0 + after.height + 30), "AFTER — my edit, the saved file", font=font("bold", 56), fill=GREEN)
    d.text((xa, y0 + after.height + 105), "evidence/waystone-after-hand-edit.blend", font=font("sans", 44), fill=MUTED)
    # Guide at the top of the rune in the "before" image, carried across both.
    col = before.convert("RGB").load()
    top = next(yy for yy in range(before.height) if col[before.width // 2, yy][2] > col[before.width // 2, yy][0] + 25)
    top2 = next(yy for yy in range(after.height) if after.load()[after.width // 2, yy][2] > after.load()[after.width // 2, yy][0] + 25)
    for yy in (top,):
        d.line((xb, y0 + yy, xa + after.width + 30, y0 + yy), fill=ACCENT, width=5)
    d.line((xa - 30, y0 + top2, xa + after.width + 30, y0 + top2), fill=GREEN, width=5)
    tx = xa + after.width + 110
    for i, (t, f, col_) in enumerate([("In Blender's window:", "bold", INK), ("G, then Z, then drag", "sans", INK),
                                      ("G starts a move;", "sans", MUTED), ("Z locks it to the Z axis", "sans", MUTED), ("", "sans", INK),
                                      ("Rune centre:", "bold", INK), ("Z 0.42 → 0.4537 m", "sans", INK),
                                      ("X, Y, size unchanged", "sans", MUTED), ("(read back by Claude)", "sans", MUTED)]):
        d.text((tx, 360 + i * 88), t, font=font(f, 54), fill=col_)
    d.text((200, H - 200), "Comparison stills, option (b): no recording of the edit was made. Both images are the MCP look tool's, "
           "same views and settings; the after image was", font=font("sans", 42), fill=MUTED)
    d.text((200, H - 140), "captured on 2026-10-13 at 22:27 EDT from a copy of the saved file. Front view, enlarged.",
           font=font("sans", 42), fill=MUTED)
    return c


def revision_strip():
    steps = [("1-built-rectangle.png", 0, 2, "Built (Claude)", "rectangle · 42 tris"),
             ("2-after-hand-edit.png", 0, 2, "My hand edit", "moved up 0.034 m"),
             ("3-trial-R.png", 0, 2, "Trial: an R", "rejected · 82 tris"),
             ("4-trial-ring-8.png", 0, 2, "Trial: a ring", "8 sides · 86 tris"),
             ("5-ring-12.png", 0, 2, "Kept", "12 sides · 118 tris")]
    side = 600
    c = Image.new("RGB", (5 * side + 4 * 60 + 120, side + 240), CREAM)
    d = ImageDraw.Draw(c)
    for i, (f, t, cols, a, b) in enumerate(steps):
        im = tile(f, t, cols)
        im = scaled(im, side / im.height)
        x = 60 + i * (side + 60)
        c.paste(im, (x, 30))
        d.rectangle((x, 30, x + im.width, 30 + im.height), outline=RED if "rejected" in b else GREEN if a == "Kept" else (204, 196, 182), width=8)
        d.text((x + im.width // 2, side + 100), a, font=font("bold", 54), fill=INK, anchor="mm")
        d.text((x + im.width // 2, side + 175), b, font=font("sans", 46), fill=MUTED, anchor="mm")
    return c


def other_props():
    circ = tile("7-teleport-circle.png", 2, 2)    # the three-quarter view from above
    sp = tile("8-spikes.png", 4, 3)               # a three-quarter view from below the front
    sp2 = tile("8-spikes.png", 0, 3)              # front
    hgt = 900
    ims = [scaled(x, hgt / x.height) for x in (circ, sp2, sp)]
    c = Image.new("RGB", (sum(i.width for i in ims) + 4 * 70, hgt + 260), CREAM)
    d = ImageDraw.Draw(c)
    x = 70
    labels = [("Teleport circle", "2.25 × 2.25 × 0.08 m · 6 shapes · 280 tris"), ("Spikes, front", "0.80 × 0.30 × 0.47 m"),
              ("Spikes, from below", "6 shapes · 82 tris")]
    for im, (a, b) in zip(ims, labels):
        c.paste(im, (x, 30))
        d.text((x + im.width // 2, hgt + 110), a, font=font("bold", 54), fill=INK, anchor="mm")
        d.text((x + im.width // 2, hgt + 185), b, font=font("sans", 44), fill=MUTED, anchor="mm")
        x += im.width + 70
    return c


def parse_log(path):
    return (REEL / path).read_text().splitlines()


def headless_numbers():
    log = parse_log("capture/checks-pass.log")
    got = {}
    cur = None
    for l in log:
        m = re.match(r"-- (\w+) ", l)
        if m:
            cur = m.group(1)
        m = re.search(r"bounding box: .* size \(([\d.]+), ([\d.]+), ([\d.]+)\)", l)
        if m and cur:
            got[cur] = tuple(float(v) for v in m.groups())    # Godot X, Y, Z
        m = re.search(r"triangles within budget (\d+)\s+\((\d+)\)", l)
        if m and cur:
            got[cur + "_tris"] = (int(m.group(2)), int(m.group(1)))
    n_ok = sum(1 for l in log if l.startswith("   ok "))
    last = [l for l in log if l.startswith(("PASS:", "FAIL:"))][-1]
    c = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((200, 140, 1100, 240), radius=16, fill=(217, 119, 87))
    d.text((650, 190), "HEADLESS CHECK OUTPUT", font=font("bold", 54), fill=(255, 255, 255), anchor="mm")
    d.text((1180, 155), "no window, no picture: numbers only", font=font("sans", 54), fill=DMUTED)
    d.text((200, 270), "$ timeout 120 Godot --headless --path godot --script res://tests/check_props.gd --fixed-fps 60",
           font=font("mono", 50), fill=(139, 199, 243))
    hdr = ["Prop", "Brief W × D × H (m)", "Blender Dimensions", "Godot bounding box X × Z × Y", "Triangles"]
    xs = [200, 860, 1640, 2340, 3330]
    y = 420
    for j, h in enumerate(hdr):
        d.text((xs[j], y), h, font=font("bold", 46), fill=DMUTED)
    rows = [("Waystone", "Waystone", "0.70 × 0.40 × 0.84"), ("Teleport circle", "TeleportCircle", "2.25 × 2.25 × 0.08"),
            ("Spikes", "Spikes", "0.80 × 0.30 × 0.47")]
    y += 100
    for name, key, br in rows:
        gx, gy, gz = got[key]
        t, budget = got[key + "_tris"]
        vals = [name, br, br, f"{gx:.4f} × {gz:.4f} × {gy:.4f}", f"{t} / {budget}"]
        for j, v in enumerate(vals):
            d.text((xs[j], y), v, font=font("bold" if j == 0 else "mono", 58), fill=(174, 231, 209) if j == 3 else DTEXT)
        y += 110
    y += 40
    d.text((200, y), "From the log, unedited:", font=font("sans", 46), fill=DMUTED); y += 80
    picks = [l for l in log if l.startswith("   bounding box")][:1] + [l for l in log if "stands along Y" in l][:1] \
        + [l for l in log if "origin at the centre" in l][:1] + [l for l in log if "Waystone sits on the floor" in l]
    for l in picks:
        d.text((200, y), l.rstrip(), font=font("mono", 48), fill=DTEXT); y += 70
    y += 30
    d.text((200, y), f"{last}   ·   {n_ok} ok lines   ·   exit code 0", font=font("mono", 64), fill=(236, 224, 161))
    d.text((200, H - 230), "Recorded for this film: capture/checks-pass.log, an isolated copy of godot/ at f6f8acf, 2026-10-13. "
           "Blender column: each object's", font=font("sans", 42), fill=DMUTED)
    d.text((200, H - 170), "dimensions, read by code through the MCP (TEST-REPORT.md), not a sidebar screenshot. "
           "Godot is Y-up, so its height is Y.", font=font("sans", 42), fill=DMUTED)
    return c, n_ok


def fail_diagnostic():
    ok = parse_log("capture/checks-pass.log")
    bad = parse_log("capture/checks-fail-diagnostic.log")
    c = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((200, 140, 1100, 240), radius=16, fill=(217, 119, 87))
    d.text((650, 190), "HEADLESS CHECK OUTPUT", font=font("bold", 54), fill=(255, 255, 255), anchor="mm")
    d.text((1180, 155), "can this check fail?", font=font("sans", 54), fill=DMUTED)
    y = 300
    d.text((200, y), "The scene as built:", font=font("bold", 56), fill=DTEXT); y += 100
    for l in [x for x in ok if "Waystone sits on the floor" in x] + [x for x in ok if x.startswith("PASS:")]:
        d.text((260, y), l.strip(), font=font("mono", 56), fill=(174, 231, 209)); y += 84
    y += 100
    d.text((200, y), "DIAGNOSTIC — an isolated copy with the waystone raised 0.3 m in props_room.tscn:", font=font("bold", 56), fill=(236, 160, 140)); y += 100
    d.text((260, y), "- transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.8, 0, 0)", font=font("mono", 50), fill=(236, 160, 140)); y += 74
    d.text((260, y), "+ transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.8, 0.3, 0)", font=font("mono", 50), fill=(174, 231, 209)); y += 110
    for l in [x for x in bad if x.lstrip().startswith("FAIL")]:
        d.text((260, y), l.strip(), font=font("mono", 56), fill=(255, 140, 120)); y += 84
    code = [x for x in bad if x.startswith("exit")][-1]
    d.text((260, y), code.replace("exit", "exit code"), font=font("mono", 56), fill=(236, 224, 161)); y += 84
    d.text((200, H - 230), "Recorded for this film: capture/checks-pass.log and capture/checks-fail-diagnostic.log (diff: capture/fail-diagnostic.diff).",
           font=font("sans", 42), fill=DMUTED)
    d.text((200, H - 170), "The project's scene was not changed. The raised waystone is a test of the test, not the game.",
           font=font("sans", 42), fill=DMUTED)
    return c


def main():
    OUT.mkdir(exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    figures = {"game-props.png": game_props(), "brief.png": brief(), "blender-own.png": blender_own(),
               "revision-strip.png": revision_strip(), "other-props.png": other_props()}
    for name, im in figures.items():
        im.save(OUT / name)
        shutil.copy(OUT / name, PUBLIC / name)
    game_card().save(OUT / "game-card.png")
    prompt_code().save(OUT / "prompt-code.png")
    prompt_result().save(OUT / "prompt-result.png")
    hand_edit().save(OUT / "hand-edit.png")
    img, n = headless_numbers()
    img.save(OUT / "headless-numbers.png")
    fail_diagnostic().save(OUT / "fail-diagnostic.png")
    print(f"stills written; {n} ok lines; public copies of {len(figures)} figures in {PUBLIC}")


if __name__ == "__main__":
    main()
