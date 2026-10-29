#!/usr/bin/env python3
"""Compose the film's still evidence cards from real files, and copy the ones
the Remotion scenes read into the toolkit's public/ folder.

Every picture here is an existing engine capture (evidence/use-it/, the
film's own captures in capture/), a texture file, or a recorded log; this
script only crops, scales, places and labels. Pixel crops of the hearts and
the grey bands are enlarged with nearest-neighbour, so no value is blended.
Code lines and log lines are read from the files, not retyped.

    python3 tools/make_stills.py        # from the reel folder
"""
import re, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
A5 = REEL.parents[1]                        # fall-2026/shuai-z/assignment-5
ART = Path("/Users/eric/csye7270/brutalist.art")
FONTS = ART / "runtime/fonts"
PUBLIC = ART / "runtime/remotion/public/reels" / REEL.name
OUT = REEL / "stills"
USE = A5 / "evidence/use-it"
W, H = 3840, 2160
CREAM, INK, MUTED, ACCENT = (250, 249, 245), (61, 57, 41), (110, 100, 86), (217, 119, 87)
RED, GREEN, LINE = (164, 74, 50), (48, 110, 70), (214, 207, 194)
DARK, DTEXT, DMUTED = (32, 37, 49), (237, 241, 247), (190, 200, 215)
DBLUE, DGREEN, DYELLOW, DRED = (139, 199, 243), (174, 231, 209), (236, 224, 161), (255, 150, 130)


def font(name, size):
    paths = {"sans": FONTS / "Inter/static/Inter_28pt-Regular.ttf", "bold": FONTS / "Inter/static/Inter_28pt-Medium.ttf",
             "mono": FONTS / "PT_Mono/PTMono-Regular.ttf"}
    return ImageFont.truetype(str(paths[name]), size)


def scaled(img, k, nearest=False):
    return img.resize((round(img.width * k), round(img.height * k)), Image.NEAREST if nearest else Image.LANCZOS)


def lines(path, a, b):
    return (A5 / path).read_text().splitlines()[a - 1:b]


def log(path):
    return (A5 / path).read_text().splitlines()


def frame_of(mp4, n):
    """One frame of a capture, decoded from the hashed MP4."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(REEL / mp4), "-vf", f"select=eq(n\\,{n})", "-vframes", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (W, H), raw)


def card(title, banner=None, dark=False):
    c = Image.new("RGB", (W, H), DARK if dark else CREAM)
    d = ImageDraw.Draw(c)
    if banner:
        bw = d.textbbox((0, 0), banner, font=font("bold", 50))[2] + 80
        d.rounded_rectangle((200, 110, 200 + bw, 210), radius=16, fill=ACCENT if dark else (48, 61, 52))
        d.text((240, 132), banner, font=font("bold", 50), fill=(255, 255, 255))
        d.text((200 + bw + 50, 128), title, font=font("bold", 66 if dark else 72), fill=DTEXT if dark else INK)
    else:
        d.text((200, 110), title, font=font("bold", 84), fill=DTEXT if dark else INK)
    return c, d


def foot(d, rows, dark=False):
    for i, t in enumerate(rows):
        d.text((200, H - 200 - 64 * (len(rows) - 1 - i)), t, font=font("sans", 42), fill=DMUTED if dark else MUTED)


def code_block(d, x, y, path, a, b, size=44, width=None, hl=()):
    d.text((x, y), path, font=font("mono", size - 4), fill=DBLUE)
    y += size + 30
    for n, ln in enumerate(lines(path, a, b), a):
        if n in hl:
            d.rectangle((x - 16, y - 6, x + (width or 1600), y + size + 8), fill=(69, 90, 113))
        d.text((x, y), f"{n:>3}", font=font("mono", size - 6), fill=(120, 130, 145))
        d.text((x + size * 2.6, y), ln.replace("\t", "  "), font=font("mono", size), fill=(186, 197, 188) if ln.lstrip().startswith("//") else DTEXT)
        y += round(size * 1.42)
    return y


# ── B02 ─────────────────────────────────────────────────────────────────────
def game_card():
    a = frame_of("capture/play-01.mp4", 134)       # three frames after hit 1: the hearts tinted
    b = frame_of("capture/stone-01.mp4", 20)       # the props scene from its own camera
    k = 1640 / W
    a, b = scaled(a, k), scaled(b, k)
    c, d = card("The Game, the State and the Object")
    y = 300
    c.paste(a, (200, y)); c.paste(b, (W - 200 - b.width, y))
    for x, rows in ((200, [("walker-rudy · game/ · 2D", "bold"), ("GL Compatibility renderer", "sans"),
                           ("State: Rudy is invulnerable", "bold"), ("1.2 s after a hit or a respawn; hits are ignored", "sans"),
                           ("The hearts tint toward the waystone's glow", "sans")]),
                    (W - 200 - b.width, [("walker-rudy props · godot/ · 3D", "bold"), ("Forward+ renderer", "sans"),
                                         ("Object: the waystone's Stone surface", "bold"), ("and the teleport circle's DarkStone surface", "sans"),
                                         ("weathered_stone.gdshader, two materials", "sans")])):
        yy = y + a.height + 60
        for t, f in rows:
            d.text((x, yy), t, font=font(f, 56 if f == "bold" else 50), fill=INK if f == "bold" else MUTED)
            yy += 84
    foot(d, ["Frames from the film's own engine captures: capture/play-01.mp4 frame 134 (Movie Maker, scripted input, 3 frames after hit 1) and",
             "capture/stone-01.mp4 frame 20 (Movie Maker, the scene's own camera). Both at revision a2a3a77; reduced to fit, not cropped."])
    return c


# ── B03 ─────────────────────────────────────────────────────────────────────
def four_questions():
    rows = [("1  What does a shader do?", "game/shaders/invulnerable_tint.gdshader", 8),
            ("2  How does a material differ from a shader?", "godot/materials/circle_darkstone.tres", 9),
            ("3  Why is a texture information?", "godot/shaders/weathered_stone.gdshader", 4),
            ("4  What is the Godot shading language?", "godot/shaders/weathered_stone.gdshader", 7)]
    c = Image.new("RGB", (3300, 1250), CREAM)
    d = ImageDraw.Draw(c)
    y = 40
    for q, path, n in rows:
        d.text((60, y), q, font=font("bold", 66), fill=INK)
        d.rounded_rectangle((60, y + 96, 3240, y + 216), radius=14, fill=DARK)
        d.text((100, y + 122), f"{Path(path).name}:{n}", font=font("mono", 52), fill=DBLUE)
        d.text((1000, y + 122), lines(path, n, n)[0].strip(), font=font("mono", 52), fill=DTEXT)
        y += 300
    return c


# ── B04 ─────────────────────────────────────────────────────────────────────
def brief_figure():
    text = (A5 / "CHANGE-BRIEF.md").read_text().splitlines()
    i = text.index("### The colour line")
    colour = next(l for l in text[i:] if l.startswith("COLOR.rgb"))
    c = Image.new("RGB", (3300, 1260), CREAM)
    d = ImageDraw.Draw(c)
    d.text((60, 30), "CHANGE-BRIEF.md, section 2 — Uniforms and The colour line (verbatim)", font=font("bold", 54), fill=INK)
    hdr = ["Name", "Type", "Hint", "Default", "Set by"]
    xs = [60, 640, 960, 1700, 2380]
    rows = [("tint_amount", "float", "hint_range(0.0, 1.0)", "0.0", "the driver, every frame"),
            ("tint_color", "vec4", "source_color", "vec4(0.6, 0.88, 1.0, 1.0)", "the material only, never code"),
            ("tint_strength", "float", "hint_range(0.0, 1.0)", "0.4", "the material only, never code")]
    for r in rows:   # each row must be in the brief's table as written
        assert any(f"`{r[0]}`" in l and f"`{r[2]}`" in l for l in text), r
    y = 140
    for j, h in enumerate(hdr):
        d.text((xs[j], y), h, font=font("bold", 44), fill=MUTED)
    y += 80
    for r in rows:
        for j, v in enumerate(r):
            d.text((xs[j], y), v, font=font("mono" if j < 4 else "sans", 44 if j == 3 else 48), fill=INK)
        y += 86
        d.line((60, y - 14, 3240, y - 14), fill=LINE, width=3)
    y += 50
    d.text((60, y), "The colour line — the one line inside fragment() that changes the colour:", font=font("bold", 50), fill=INK)
    d.rounded_rectangle((60, y + 90, 3240, y + 230), radius=16, fill=DARK)
    d.text((110, y + 122), colour, font=font("mono", 64), fill=DTEXT)
    y += 300
    for t in ["0.4, not more: at 0.6 the outline falls to 2.1:1 against the sky; at 0.4 it is 3.5:1 (rule 9 asks for 3:1).",
              "Rule 4: the tint shows for 1.183 s ± one frame, the same at 30, 60 and 144 fps."]:
        d.text((60, y), t, font=font("sans", 50), fill=INK); y += 80
    return c


# ── B06 ─────────────────────────────────────────────────────────────────────
def tint_captures():
    got = {}
    for l in log("logs/capture_tint.log"):
        m = re.match(r"PIXEL tint ([\d.]+) (P\d|B) at .*?: (#[0-9A-F]{6})(?:, predicted (#[0-9A-F]{6}))?", l)
        if m:
            got[(m[1], m[2])] = (m[3], m[4])
    c, d = card("Line 8 at Controlled Values", "ENGINE CAPTURE · WINDOW")
    box = (24, 20, 216, 90)                        # the three hearts, 1920 × 1080 layout
    k = 5
    vals = ["0.0", "0.5", "1.0", "2.0"]
    x0, y0 = 200, 330
    for i, v in enumerate(vals):
        im = Image.open(USE / f"hearts-tint-{v}.png").convert("RGB").crop(box)
        im = scaled(im, k, nearest=True)
        x = x0 + (i % 2) * 1760
        y = y0 + (i // 2) * 830
        c.paste(im, (x, y))
        for name, (px, py) in (("P1", (54, 58)), ("P2", (77, 56)), ("P3", (183, 49))):
            cx, cy = x + (px - box[0]) * k + k // 2, y + (py - box[1]) * k + k // 2
            d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), outline=(255, 255, 255), width=6)
            d.text((cx + 22, cy - 62), name, font=font("bold", 40), fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
        d.text((x, y + im.height + 22), f"tint_amount {v}" + ("  (set from code; the slider stops at 1.0)" if v == "2.0" else ""),
               font=font("bold", 50), fill=INK)
        p1, p2 = got[(v, "P1")], got[(v, "P2")]
        d.text((x, y + im.height + 92), f"P1 {p1[0]} (predicted {p1[1]})   P2 {p2[0]} (predicted {p2[1]})",
               font=font("mono", 42), fill=INK)
        d.text((x, y + im.height + 152), f"P3, inside the empty heart: {got[(v, 'P3')][0]}, the sky, at every value",
               font=font("sans", 40), fill=MUTED)
    foot(d, ["game/tests/capture_tint.tscn in a window, Compatibility renderer, the driver stopped; viewport image saved as drawn, 1920 × 1080",
             "(evidence/use-it/hearts-tint-*.png, 2026-10-27). Crops enlarged 5× nearest-neighbour. Values: logs/capture_tint.log. If hint_range clamped, 2.0 would show #B58086."])
    return c


# ── B09 ─────────────────────────────────────────────────────────────────────
def rock_textures():
    t = A5 / "godot/assets/textures/rock_01"
    files = [("rock_01_diff_1k.png", "Colour", "albedo_tex : source_color", "decoded from sRGB"),
             ("rock_01_nor_gl_1k.png", "Normal (OpenGL, Y+)", "normal_tex : hint_normal", "directions, not colours"),
             ("rock_01_rough_1k.png", "Roughness", "roughness_tex : no colour hint", "numbers as stored")]
    c = Image.new("RGB", (3300, 1260), CREAM)
    d = ImageDraw.Draw(c)
    side = 820
    for i, (f, a, b, e) in enumerate(files):
        im = Image.open(t / f)
        if im.mode.startswith("I"):           # the roughness map is 16-bit grey: scale to 8 bits, do not clip
            im = im.point(lambda v: v / 257).convert("L")
        im = im.convert("RGB").resize((side, side), Image.LANCZOS)
        x = 80 + i * (side + 230)
        c.paste(im, (x, 40))
        d.text((x, side + 80), a, font=font("bold", 56), fill=INK)
        d.text((x, side + 160), b, font=font("mono", 40), fill=INK)
        d.text((x, side + 225), e, font=font("sans", 44), fill=MUTED)
    return c


# ── B11 ─────────────────────────────────────────────────────────────────────
def sweep():
    means = {}
    for l in log("logs/capture_sweep.log"):
        m = re.match(r"CHANGE close (\w+) (min|max|default) .*?close mean ([\d.]+)", l)
        if m:
            means[(m[1], m[2])] = m[3]
    c, d = card("The Interface, Swept", "ENGINE CAPTURE · WINDOW")
    rows = [("albedo_tint", ["min", "default"], ["black", "white (default = max)"]),
            ("uv_scale", ["min", "default", "max"], ["0.25", "1.0", "4.0"]),
            ("normal_strength", ["min", "default", "max"], ["0.0", "1.0", "2.0"]),
            ("roughness_offset", ["min", "default", "max"], ["−0.5", "0.0", "0.5"])]

    for r, (u, keys, labels) in enumerate(rows):
        x0 = 200 + (r % 2) * 1760
        y0 = 300 + (r // 2) * 820
        d.text((x0, y0), u, font=font("mono", 52), fill=INK)
        for j, (key, lab) in enumerate(zip(keys, labels)):
            im = scaled(Image.open(USE / f"sweep/close-{u}-{key}.png").convert("RGB"), 560 / 586)
            x = x0 + j * (im.width + 40)
            c.paste(im, (x, y0 + 80))
            mean = "0.00" if key == "default" else means[(u, key)]
            d.text((x, y0 + 80 + im.height + 14), f"{lab} · {mean} steps", font=font("sans", 38), fill=INK if key != "default" else MUTED)
    foot(d, ["godot/tests/capture_sweep.gd in a window, Forward+, the scene's own lighting; Claude moved the camera close, in memory (TEST-REPORT.md §7).",
             "Each value set on the loaded material only, never saved. Steps: mean of each pixel's largest channel change against the default frame (logs/capture_sweep.log)."])
    return c


# ── B15 ─────────────────────────────────────────────────────────────────────
def hint_result():
    bands = []
    for l in log("logs/capture_hint.log"):
        m = re.match(r"BAND (Quad[AB]) (\d) \(file (\d+)\) at .*?: shows (\d+), .*?predicted (\d+)", l)
        if m:
            bands.append(m.groups())
    c, d = card("The Hint Experiment, Measured", "ENGINE CAPTURE · WINDOW")
    im = Image.open(USE / "hint-experiment.png").convert("RGB")
    im = im.crop((100, 220, 1360, 860))
    im = scaled(im, 1.35, nearest=True)
    c.paste(im, (200, 290))
    x = 200 + im.width + 140
    d.text((x, 330), "Band   file   predicted   on screen", font=font("bold", 50), fill=MUTED)
    y = 430
    for quad, name in (("QuadA", "A · source_color"), ("QuadB", "B · no hint")):
        d.text((x, y), name, font=font("bold", 58), fill=INK); y += 96
        for q, n, f, shown, pred in bands:
            if q == quad:
                d.text((x, y), f"{n}      {f:>3}       {pred:>3}          {shown:>3}", font=font("mono", 56), fill=INK); y += 84
        y += 70
    d.text((x, y), "6 of 6 exactly as predicted;", font=font("bold", 54), fill=GREEN); y += 76
    d.text((x, y), "each flat over 9 × 9 pixels", font=font("sans", 50), fill=INK)
    foot(d, ["godot/tests/capture_hint.gd: godot/scenes/hint_experiment.tscn in a window, Forward+, unshaded, Linear tonemap; frame saved as drawn, 1920 × 1080",
             "(evidence/use-it/hint-experiment.png, 2026-10-27; crop enlarged 1.35×, nearest). Band centres and values: logs/capture_hint.log. Predictions: CHANGE-BRIEF.md §4."])
    return c


# ── B17 ─────────────────────────────────────────────────────────────────────
def two_materials():
    ch = {}
    for l in log("logs/capture_sweep.log"):
        m = re.match(r"CHANGE (shader line 18|circle_darkstone \w+) .*?waystone mean ([\d.]+).*?circle mean ([\d.]+)", l)
        if m:
            ch[m[1]] = (m[2], m[3])
    c, d = card("One Shader, Two Materials", "ENGINE CAPTURE · WINDOW")
    items = [("two-materials-default.png", "As saved", None),
             ("two-materials-shader-line.png", "Shader line 18: ALBEDO × 0.5", "shader line 18"),
             ("two-materials-circle-normal_strength.png", "Circle's material: normal_strength 2.0", "circle_darkstone normal_strength"),
             ("two-materials-circle-albedo_tint.png", "Circle's material: albedo_tint white", "circle_darkstone albedo_tint")]
    for i, (f, lab, key) in enumerate(items):
        im = scaled(Image.open(USE / f"sweep/{f}").convert("RGB"), 1.5)
        x = 200 + (i % 2) * 1760
        y = 290 + (i // 2) * 820
        c.paste(im, (x, y))
        d.text((x, y + im.height + 20), lab, font=font("bold", 50), fill=INK)
        if key:
            w_, c_ = ch[key]
            d.text((x, y + im.height + 90), f"waystone {w_} steps · circle {c_} steps", font=font("mono", 44),
                   fill=MUTED if float(c_) < 3 else INK)
        else:
            d.text((x, y + im.height + 90), "the reference frame", font=font("sans", 44), fill=MUTED)
    foot(d, ["godot/tests/capture_sweep.gd, from the scene's Camera, the scene's lighting. Both materials use one Shader object (SHARED … true). Every change was",
             "in memory and restored; the shader file and both .tres files were never written (git status clean). Crops enlarged 1.5×. logs/capture_sweep.log."])
    return c


# ── B18 ─────────────────────────────────────────────────────────────────────
def generated_vs_mine():
    c, d = card("The Generated Shader Beside Mine", "TWO ANNOTATED LINES")
    G, S = "godot/shaders/standard_generated.gdshader", "godot/shaders/weathered_stone.gdshader"
    d.rounded_rectangle((200, 290, 3640, 1010), radius=20, fill=DARK)
    d.text((250, 320), "Generated by Godot 4.7.2 from a StandardMaterial3D, annotated by shuai-z", font=font("bold", 44), fill=DMUTED)
    y = code_block(d, 250, 400, G, 10, 11, size=44, width=3340, hl=(11,))
    y = code_block(d, 250, y + 20, G, 69, 72, size=44, width=3340, hl=(70, 72))
    d.rounded_rectangle((200, 1060, 3640, 1640), radius=20, fill=DARK)
    d.text((250, 1090), "weathered_stone.gdshader, hand-written by shuai-z", font=font("bold", 44), fill=DMUTED)
    y = code_block(d, 250, 1170, S, 3, 4, size=44, width=3340, hl=(3,))
    code_block(d, 250, y + 20, S, 19, 20, size=44, width=3340, hl=(19, 20))
    d.text((200, 1700), "Same: the colour sampler is source_color; the normal goes to NORMAL_MAP, its strength to NORMAL_MAP_DEPTH.", font=font("sans", 50), fill=INK)
    d.text((200, 1775), "Different: the normal's hint, hint_roughness_normal against hint_normal; 16 uniforms against 7.", font=font("sans", 50), fill=INK)
    foot(d, ["Verbatim lines: standard_generated.gdshader 10–11 and 69–72 (fe795908; comments by shuai-z), weathered_stone.gdshader 3–4 and 19–20 (a87a18be).",
             "16 uniforms: logs/probe_standard_generated.log line 6. Nothing uses the generated shader. LANGUAGE-NOTES.md §A and question 6."])
    return c


# ── B20 ─────────────────────────────────────────────────────────────────────
def tint_tests():
    c, d = card("Three Frame Rates, One Duration", "HEADLESS TEST OUTPUT", dark=True)
    d.text((200, 270), "$ scripts/run-test.sh game invulnerable_tint_checks.tscn <30 | 60 | 144>", font=font("mono", 52), fill=DBLUE)
    y = 400
    for fps in (30, 60, 144):
        L = log(f"logs/game_invulnerable_tint_checks_{fps}fps.log")
        n = sum(1 for l in L if l.startswith("PASS"))
        last = [l for l in L if l in ("all checks passed",) or l.endswith("FAILED")][-1]
        d.text((200, y), f"{fps:>3} fps", font=font("bold", 60), fill=DTEXT)
        d.text((520, y + 6), f"{n} PASS · {last}", font=font("mono", 52), fill=DGREEN)
        y += 92
        for key in ("A9", "A10", "A11", "A12"):
            l = next(x for x in L if x.startswith(f"PASS  {key} "))
            detail = l[l.find("  (") + 3:-1] if "  (" in l else ""
            head = {"A9": "shown for", "A10": "back on the spikes", "A11": "respawn", "A12": "pause"}[key]
            parts, cur = [], ""
            for word in detail.split(" "):
                if len(cur) + len(word) > 100:
                    parts.append(cur); cur = ""
                cur += ("" if not cur else " ") + word
            parts.append(cur)
            for i, part in enumerate(parts):
                d.text((560, y), (f"{key} {head}: " if i == 0 else "    ") + part, font=font("mono", 40), fill=DTEXT)
                y += 56
        y += 40
    foot(d, ["Recorded headless output, Godot 4.7.2 --headless, through scripts/run-test.sh at pinned --fixed-fps (logs/game_invulnerable_tint_checks_30fps.log,",
             "_60fps.log, _144fps.log; run 2026-10-27 at 5db11399, game source unchanged since bd797945). Excerpted lines; the rest of each log passes too."], dark=True)
    return c


# ── B21 ─────────────────────────────────────────────────────────────────────
def mutations():
    c, d = card("Can the Checks Fail?", "HEADLESS TEST OUTPUT", dark=True)
    rows = [("1 · invulnerable_tint.gdshader line 1: the semicolon deleted", "logs/game_invulnerable_tint_checks_60fps_no_semicolon.log",
             ["SHADER ERROR", "FAILED"]),
            ("2 · tint_amount renamed tint_amt (it still parses)", "logs/game_invulnerable_tint_checks_60fps_renamed.log", ["FAIL  A1", "FAILED"]),
            ("3 · weathered_stone.gdshader line 3: source_color deleted", "logs/godot_test_materials_60fps_no_source_color.log", ["FAIL ", "FAILED"])]
    y = 300
    for title, path, keys in rows:
        L = log(path)
        d.text((200, y), title, font=font("bold", 54), fill=DTEXT); y += 86
        for k in keys:
            l = next(x for x in L if x.startswith(k) or (k == "FAILED" and x.endswith("FAILED")))
            d.text((260, y), (l[:118] + " …") if len(l) > 120 else l, font=font("mono", 40), fill=DRED if "FAIL" in l or "ERROR" in l else DTEXT); y += 60
        d.text((260, y), "exit 1, from the wrapper (FRICTIONAL.md)  ·  " + path, font=font("mono", 38), fill=DYELLOW); y += 110
    L = log("logs/godot_test_materials_60fps.log")
    n = sum(1 for l in L if l.startswith("PASS"))
    d.text((200, y), "Clean: 125 of 125 after a fresh import from an empty .godot cache (2026-10-27), and again at 5db11399:", font=font("bold", 54), fill=DTEXT); y += 86
    d.text((260, y), f"test_materials.gd: {n} PASS · {L[-1] if L[-1] else L[-2]}", font=font("mono", 44), fill=DGREEN)
    foot(d, ["Mutations made by shuai-z, run by Claude through scripts/run-test.sh at 60 fps; each shader restored and checked byte for byte against its commit.",
             "A shader error does not change Godot's exit code; the wrapper fails on any SHADER ERROR line (CLAUDE.md, Headless facts)."], dark=True)
    return c


# ── B22 ─────────────────────────────────────────────────────────────────────
def headless_limits():
    os_rows = [l for l in log("logs/capture_hint_vs_os.log") if l.startswith("BAND")]
    c, d = card("What No Headless Run Shows", "ENGINE CAPTURE vs OS SCREENSHOT")
    a = Image.open(USE / "os-compare/engine.png").convert("RGB").crop((100, 220, 1360, 860))
    b = Image.open(USE / "os-compare/os-screenshot.png").convert("RGB").crop((100, 220, 1360, 860))
    a, b = scaled(a, 0.9), scaled(b, 0.9)
    c.paste(a, (200, 300)); c.paste(b, (200 + a.width + 80, 300))
    d.text((200, 300 + a.height + 20), "Engine capture (the frame Godot drew)", font=font("bold", 46), fill=INK)
    d.text((280 + a.width, 300 + a.height + 20), "macOS screenshot of the same window", font=font("bold", 46), fill=INK)
    x = 200 + 2 * a.width + 200
    y = 320
    d.text((x, y), "Band  predicted  engine  OS", font=font("bold", 44), fill=MUTED); y += 80
    for l in os_rows:
        m = re.match(r"BAND Quad([AB]) (\d): predicted (\d+); engine (\d+).*?OS screenshot (\d+)", l)
        d.text((x, y), f"{m[1]}{m[2]}     {m[3]:>3}      {m[4]:>3}    {m[5]:>3}", font=font("mono", 50), fill=INK); y += 74
    d.text((x, y + 30), "The screenshot carries the display's", font=font("sans", 44), fill=INK)
    d.text((x, y + 92), "colour profile; converted to sRGB,", font=font("sans", 44), fill=INK)
    d.text((x, y + 154), "all six match the engine exactly.", font=font("sans", 44), fill=INK)
    y = 300 + a.height + 140
    for t in ["--headless runs the shader parser but draws nothing: no frame can be read back (logs/probe_headless.log).",
              "No test says the hearts read well or the stone looks like stone: shuai-z played the game, watched the fade-in, checked the materials in the editor.",
              "Under the scene's light, normal_strength and roughness_offset move the stone by under 3 steps: below what an eye can judge."]:
        d.text((200, y), "· " + t, font=font("sans", 48), fill=INK); y += 84
    foot(d, ["godot/tests/capture_hint_vs_os.gd (logs/capture_hint_vs_os.log; evidence/use-it/os-compare/, 2026-10-27); TEST-REPORT.md §§5, 7, 12, 14.",
             "Crops of the same region, reduced to 0.9×. The OS screenshot's profile conversion was done by Claude with Pillow ImageCms."])
    return c


def main():
    OUT.mkdir(exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    figures = {"four-questions.png": four_questions(), "brief-colour-line.png": brief_figure(), "rock-textures.png": rock_textures()}
    for name, im in figures.items():
        im.save(OUT / name)
        shutil.copy(OUT / name, PUBLIC / name)
    for name, fn in [("game-card.png", game_card), ("tint-captures.png", tint_captures), ("sweep.png", sweep),
                     ("hint-result.png", hint_result), ("two-materials.png", two_materials), ("generated-vs-mine.png", generated_vs_mine),
                     ("tint-tests.png", tint_tests), ("mutations.png", mutations), ("headless-limits.png", headless_limits)]:
        fn().save(OUT / name)
    print(f"stills written to {OUT}; public copies of {len(figures)} figures in {PUBLIC}")


if __name__ == "__main__":
    main()
