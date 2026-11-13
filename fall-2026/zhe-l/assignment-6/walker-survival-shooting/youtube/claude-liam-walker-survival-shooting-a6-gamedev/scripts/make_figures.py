"""Compose the A6 film's result figures from real engine output and real test logs.

Game pixels come only from (a) the submitted fixture frame strips in the course repository's captures/
(preview scenes, 2048x1152, Movie Maker) and (b) this film's native-4K scripted-input captures (CAPTURE.md).
This script crops, scales (never stretches), places side by side and adds English labels. "Difference" tiles
are computed: |frame - reference frame| x gain, labelled as such; they are analysis, not screenshots.
Log figures print log lines verbatim. Output: <reel>/figures/*.png, copied to the Remotion public folder.
Run: python -I scripts/make_figures.py
"""
import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REEL = Path(__file__).resolve().parents[1]
A6 = REEL.parents[1]                                     # <film-work>/a6
CAP = A6 / "captures"                                    # this film's 4K captures
COURSE = Path("<course-repo>/fall-2026/zhe-l/assignment-6/walker-survival-shooting")
STRIP = COURSE / "captures"                              # submitted fixture strips
LOGS = COURSE / "logs"                                   # submitted logs
PUB = Path("<brutalist.art>/runtime/remotion/public/claude-liam-walker-survival-shooting-a6-gamedev")
FONTS = Path("<brutalist.art>/runtime/fonts")
OUT = REEL / "figures"
W, H = 3840, 2160
INK, PAGE, ACCENT = (61, 57, 41), (250, 249, 245), (217, 119, 87)
MANIFEST = {}


def font(size, mono=False):
    if mono:
        return ImageFont.truetype(str(next((FONTS / "PT_Mono").glob("*.ttf"))), size)
    return ImageFont.truetype(str(FONTS / "Lato" / "static" / "Lato-Bold.ttf"), size)


def rel(p):
    p = Path(p).as_posix()
    return (p.replace(COURSE.as_posix(), "<course-repo>/assignment-6/walker-survival-shooting")
             .replace(A6.as_posix(), "<film-work>/a6"))


def label(img, text, size=40):
    if not text:
        return img
    d = ImageDraw.Draw(img)
    h = size + 26
    d.rectangle([0, img.height - h, img.width, img.height], fill=(0, 0, 0))
    d.text((16, img.height - h + 11), text, font=font(size), fill=(255, 255, 255))
    return img


def fit(im, w, h):
    """Centre-crop to w:h, then scale (never stretch an engine image)."""
    if im.width / im.height > w / h:
        nw = round(im.height * w / h)
        im = im.crop(((im.width - nw) // 2, 0, (im.width - nw) // 2 + nw, im.height))
    else:
        nh = round(im.width * h / w)
        im = im.crop((0, (im.height - nh) // 2, im.width, (im.height - nh) // 2 + nh))
    return im.resize((w, h), Image.LANCZOS)


def tile(path, w, h, text, crop=None, size=40):
    im = Image.open(path).convert("RGB")
    if crop:
        im = im.crop(crop)
    return label(fit(im, w, h), text, size)


def diff_tile(path, ref, w, h, text, gain=8, crop=None, size=40):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int32)
    b = np.asarray(Image.open(ref).convert("RGB")).astype(np.int32)
    d = np.clip(np.abs(a - b).max(axis=2) * gain, 0, 255).astype(np.uint8)
    im = Image.fromarray(d)
    if crop:
        im = im.crop(crop)
    # each 1-2 px speck is grown to about 5 px (max filter) so it survives the downscale; positions are unchanged
    im = im.filter(ImageFilter.MaxFilter(5)).convert("RGB")
    return label(fit(im, w, h), text, size)


def grid(tiles, cols, tw, th, gap=70, bg=PAGE):
    rows = (len(tiles) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * tw + (cols - 1) * gap, rows * th + (rows - 1) * gap), bg)
    for i, t in enumerate(tiles):
        if t is not None:
            canvas.paste(t, ((i % cols) * (tw + gap), (i // cols) * (th + gap)))
    return canvas


def save(img, name, sources):
    OUT.mkdir(parents=True, exist_ok=True)
    PUB.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    img.save(p)
    shutil.copy2(p, PUB / name)
    MANIFEST[name] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "size": list(img.size),
                      "sources": [rel(s) for s in sources]}


def text_page(name, title, sub, rows, sources, size=52):
    """A page of short lines summarised from a submitted document (the subtitle says which)."""
    img = Image.new("RGB", (W, 1500), PAGE)
    d = ImageDraw.Draw(img)
    d.text((110, 60), title, font=font(84), fill=INK)
    d.text((110, 170), sub, font=font(46), fill=ACCENT)
    y = 290
    for head, body in rows:
        d.text((110, y), head, font=font(size + 2), fill=ACCENT)
        d.text((720, y), body, font=font(size), fill=INK)
        y += size + 76
    save(img.crop((0, 0, W, y + 40)), name, sources)


def log_page(name, title, blocks, size=44):
    """blocks: [(log path, [substrings])]. Lines are copied verbatim from the logs."""
    img = Image.new("RGB", (W, 2000), PAGE)
    d = ImageDraw.Draw(img)
    d.text((110, 60), title, font=font(80), fill=INK)
    d.text((110, 165), "lines copied verbatim from the submitted logs", font=font(44), fill=ACCENT)
    y, paths = 270, []
    for p, wanted in blocks:
        paths.append(p)
        d.text((110, y), "logs/" + p.name, font=font(48), fill=ACCENT)
        y += 68
        for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if any(w in ln for w in wanted):
                d.text((150, y), ln.rstrip()[:155], font=font(size, mono=True), fill=INK)
                y += size + 16
        y += 24
    save(img.crop((0, 0, W, y + 30)), name, paths)


def sframe(sub, n):
    return STRIP / sub / f"frame{n:08d}.png"


# ---------------- crops (pixel boxes in the 2048x1152 strips) ----------------
A_CROP = (624, 830, 1184, 1145)          # the feet in the landing preview (dust bbox 798-1010 x 862-1006)
A_RE_CROP = (560, 640, 1440, 1135)       # wider: the second landing is 0.5 m away
B_CROP = (700, 330, 1380, 712)           # under ceiling light 1 in the light-dust preview ("dark" set)

# 1. the game, both effects (this film's native 4K scripted captures)
land = CAP / "landing-run-02/frames/f00062.png"
lit = CAP / "lights-film-01/frames/f00290.png"
save(grid([tile(land, 1890, 1063, "", crop=(900, 860, 2860, 1963)),
           tile(lit, 1890, 1063, "", crop=(600, 0, 3267, 1500))], 2, 1890, 1063),
     "fig_game.png", [land, lit])

# 2. intent blocks (summaries of CHANGE-BRIEF.md)
text_page("fig_a_intent.png", "Effect A intent: landing dust", "CHANGE-BRIEF.md, Effect A, Intent (my words, summarised)", [
    ("Timing", "clear by 0.10 s, strongest at 0.15 s, gone at 1.6 s; ring done at 0.30 s, gone at 0.45 s"),
    ("Contrast", "open floor near ceiling light 1 (bright); front of the room by the furniture (dark)"),
    ("Scale", "ankle height (0.10 m); spread about 0.9 m, 1.5 x the 0.6 m capsule"),
    ("Change over life", "same hue; appears fast, fades slowly; each quad grows; ring grows as it fades"),
    ("Variation", "random spawn, direction, speed, size, rotation; the ring is fixed, a steady cue"),
    ("Layering", "two emitters: Dust (24 puffs) + GroundRing (one flat ring)"),
    ("Retrigger", "restart(): a second landing clears the old burst; peak 24 + 1 = 25 particles"),
    ("Budget", "<= 0.2 ms GPU time; headless CPU predicted within 0.05 ms"),
], [COURSE / "CHANGE-BRIEF.md"])
text_page("fig_b_intent.png", "Effect B intent: dust in the air", "CHANGE-BRIEF.md, Effect B, and its 2026-11-12 revision (summarised)", [
    ("Job", "ambience: dust hanging in an old base; condition = the ceiling lights are on"),
    ("Timing", "preprocess 6 s: settled on the first visible frame; gone at once with the light"),
    ("Paused / hidden", "frozen while paused; hidden = stopped, preprocessed again when shown"),
    ("First version", "under ceiling light 1 only: 1.8 x 1.6 x 1.2 m box, 150 specks, unshaded"),
    ("Revised", "whole room 14 x 2.6 x 9 m, lit by the lights, sparser, specks 0.003-0.03 m"),
    ("Features A lacks", "box emission, turbulence, multi-peak opacity ramp, additive blend, preprocess"),
    ("Budget", "<= 0.3 ms GPU time (written for 150 specks; re-measured at 1300)"),
], [COURSE / "CHANGE-BRIEF.md"])

# 3. Effect A r0: the first strip (fixture), bright and dark sets
fr = [12, 15, 30, 50]


def a_row(sub, rnd):
    return [tile(sframe(f"landing_dust/{rnd}/{sub}", n), 940, 528, f"{rnd} {sub.split('-')[0]} f{n}",
                 crop=A_CROP, size=36) for n in fr]


save(grid(a_row("bright-fade", "r0") + a_row("dark-fade", "r0"), 4, 940, 528), "fig_a_r0.png",
     [sframe(f"landing_dust/r0/{s}", n) for s in ("bright-fade", "dark-fade") for n in fr])

# 4. Effect A r0 -> r1 (quad 0.08 -> 0.32 m), bright set, same frames
save(grid(a_row("bright-fade", "r0") + a_row("bright-fade", "r1"), 4, 940, 528), "fig_a_r1.png",
     [sframe(f"landing_dust/{r}/bright-fade", n) for r in ("r0", "r1") for n in fr])

# 5. Effect A r1 retrigger (second landing at frame 25, 0.5 m away)
rf = [24, 25, 26, 27, 30, 35]
save(grid([tile(sframe("landing_dust/r1/bright-retrigger", n), 1250, 700, "", crop=A_RE_CROP)
           for n in rf], 3, 1250, 700),
     "fig_a_retrigger.png", [sframe("landing_dust/r1/bright-retrigger", n) for n in rf])


# 6. Effect B r0 / r1: raw crop under light 1, and the computed difference against frame 61 (dust hidden)
def b_pair(rnd, sub="dark", n=40):
    return [tile(sframe(f"light_dust/{rnd}/{sub}", n), 1100, 620, f"{rnd} f{n} (raw crop)", crop=B_CROP, size=36),
            diff_tile(sframe(f"light_dust/{rnd}/{sub}", n), sframe(f"light_dust/{rnd}/{sub}", 61), 1100, 620,
                      f"{rnd}: |f{n} - f61| x 8, specks enlarged (computed)", crop=B_CROP, size=36)]


save(grid(b_pair("r0") + b_pair("r1"), 2, 1100, 620), "fig_b_r0r1.png",
     [sframe(f"light_dust/{r}/dark", n) for r in ("r0", "r1") for n in (40, 61)])

# 7. Effect B redesign: 3000 (first pass) vs 1300 at half brightness (final), whole-frame differences
save(grid([diff_tile(sframe(f"light_dust/{r}/dark", 40), sframe(f"light_dust/{r}/dark", 61), 1890, 1063,
                     f"{r}: |f40 - f61| x 8, specks enlarged, whole frame (computed)") for r in ("redesign", "redesign-2")],
          2, 1890, 1063),
     "fig_b_redesign.png", [sframe(f"light_dust/{r}/dark", n) for r in ("redesign", "redesign-2") for n in (40, 61)])

# 8. Effect B timeline on the final strip (fixture): lights on 10, pause 45-55, hide 60-65, off 70
tl = [(9, "lights off"), (11, "first dust"), (40, "1 s on"), (46, "paused"), (54, "paused"),
      (61, "hidden"), (66, "shown"), (71, "lights off")]
TL_CROP = (420, 200, 1628, 880)          # the middle of the room, where most specks are lit
tiles = []
for n, what in tl:
    ref = sframe("light_dust/redesign-2/dark", 9 if n in (9, 71) else 61)
    tiles.append(diff_tile(sframe("light_dust/redesign-2/dark", n), ref, 940, 528, f"f{n} {what} (diff x 12, cropped)",
                           gain=12, crop=TL_CROP, size=36))
save(grid(tiles, 4, 940, 528), "fig_b_timeline.png",
     [sframe("light_dust/redesign-2/dark", n) for n, _ in tl])

# 9-12. real logs
log_page("fig_log_tests.png", "Read-back and state tests (60 fps, headless)", [
    (LOGS / "test_landing_dust_config_60fps.log", ["Dust top including", "lists initial_velocity", " passed,"]),
    (LOGS / "test_landing_dust_events_60fps.log", ["first Dust burst", "Dust finished exactly", " passed,"]),
    (LOGS / "test_light_dust_config_60fps.log", [" passed,"]),
    (LOGS / "test_light_dust_state_60fps.log", ["4 on that frame", "5 paused", "6 shown again", " passed,"]),
])
log_page("fig_log_mutations.png", "Two mutations of landing_dust.tscn (restored after each)", [
    (LOGS / "mutation_1_godot3_name_60fps.log", ["FAIL", "lists initial_velocity", " passed,"]),
    (LOGS / "mutation_2_value_drift_60fps.log", ["FAIL", " passed,"]),
])
log_page("fig_log_cost.png", "Headless CPU price: cost_effects.gd at 60 fps", [
    (LOGS / "cost_effects_60fps.log", ["dummy renderer", "mean 0.", "mean 1.", "->"]),
], size=38)
log_page("fig_log_gpu.png", "GPU price: gpu_price.gd, windowed, vsync off, lights on", [
    (LOGS / "gpu_price.log", ["GPU:", "GPU mean", "cost:"]),
])

(REEL / "figures" / "MANIFEST.json").write_text(json.dumps(MANIFEST, indent=1) + "\n", encoding="utf-8")
for k, v in MANIFEST.items():
    print(k, v["size"], v["sha256"][:12])
