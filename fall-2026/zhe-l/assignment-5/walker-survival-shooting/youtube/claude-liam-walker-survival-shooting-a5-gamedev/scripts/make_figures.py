"""Compose the A5 film's result figures from real engine captures and real test logs.

Every pixel of a game image here is engine output (captures listed below); this script only
places captures side by side, crops, and adds English labels. Log figures print log lines
verbatim (no edits). Output: <reel>/figures/*.png, also copied to the Remotion public folder.
Run: python -I scripts/make_figures.py
"""
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
A5 = REEL.parents[1]                                   # <film-work>
CAP = A5 / "captures"
PROJ_CAP = Path("<working-folder>/submission-a5/captures")   # user's own captures
LOGS = Path("<working-folder>/logs")                          # submitted test logs
PUB = Path("<brutalist.art>/runtime/remotion/public/claude-liam-walker-survival-shooting-a5-gamedev")
FONTS = Path("<brutalist.art>/runtime/fonts")
OUT = REEL / "figures"
W, H = 3840, 2160
INK, PAGE, ACCENT = (61, 57, 41), (250, 249, 245), (217, 119, 87)


def font(size, mono=False):
    if mono:
        return ImageFont.truetype(str(next((FONTS / "PT_Mono").glob("*.ttf"))), size)
    return ImageFont.truetype(str(FONTS / "Lato" / "static" / "Lato-Bold.ttf"), size)


def label(img, text, size=54):
    d = ImageDraw.Draw(img)
    f = font(size)
    h = size + 40
    d.rectangle([0, img.height - h, img.width, img.height], fill=(0, 0, 0))
    d.text((24, img.height - h + 18), text, font=f, fill=(255, 255, 255))
    return img


def tile(path, w, h, text, crop=None, size=54, burn=True):
    im = Image.open(path).convert("RGB")
    if crop:
        im = im.crop(crop)
    # keep the aspect ratio: centre-crop to w:h, then scale (never stretch an engine image)
    if im.width / im.height > w / h:
        nw = round(im.height * w / h)
        im = im.crop(((im.width - nw) // 2, 0, (im.width - nw) // 2 + nw, im.height))
    else:
        nh = round(im.width * h / w)
        im = im.crop((0, (im.height - nh) // 2, im.width, (im.height - nh) // 2 + nh))
    im = im.resize((w, h), Image.LANCZOS)
    return label(im, text, size) if burn else im


def grid(tiles, cols, tw, th, gap=24, bg=PAGE):
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
                      "sources": [str(s).replace("\\", "/") for s in sources]}


def log_figure(name, title, log_path, wanted, size=46):
    """Draw the chosen lines of a real log verbatim on a page."""
    text = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    picked = [ln for ln in text if any(w in ln for w in wanted)]
    img = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(img)
    d.text((120, 90), title, font=font(72), fill=INK)
    d.text((120, 190), f"log: logs/{log_path.name} (lines copied verbatim)", font=font(44), fill=ACCENT)
    y = 300
    for ln in picked:
        d.text((120, y), ln[:150], font=font(size, mono=True), fill=INK)
        y += size + 18
    save(img, name, [log_path])
    return picked


MANIFEST = {}
PAIR_CROP = (380, 560, 3140, 1560)       # the two crates only: no wall corner, tablet or long shadows
GLINT_CROP = (1407, 760, 2296, 1260)     # top face of crate_cube only (the long crate is above y 760)

# 1. context: the tablet in two hands (scripted input) + the two crates
f200 = CAP / "tablet-run-02/frames/f00200.png"
f110 = CAP / "tablet-run-02/frames/f00110.png"
# no burned-in strip: the figure's own status line and cards carry the labels (GATE T text-overlap check)
save(grid([tile(f110, 1896, 1066, "", crop=(850, 950, 2050, 1625), burn=False),   # tablet + player only
           tile(CAP / "crate/pair.png", 1896, 1066, "", crop=PAIR_CROP, burn=False)], 2, 1896, 1066),
     "fig_context.png", [f110, CAP / "crate/pair.png"])

# 2. controlled values (user's own in-engine captures, 2048x1152)
vals = [("0.00", "(0, 0, 0)", "(0, 0, 0)"), ("0.39", "(151, 162, 162)", "(151, 162, 162)"),
        ("1.00", "(230, 247, 247)", "(230, 247, 247)"), ("2.00", "(255, 255, 255)", "(255, 255, 255)")]
tiles = [tile(PROJ_CAP / f"screen_pad_{v}_marked.png", 1896, 1066,
              f"pad_light_data = {v}   P1 measured {m}   predicted {p}", size=46) for v, m, p in vals]
save(grid(tiles, 2, 1896, 1066), "fig_controlled.png", [PROJ_CAP / f"screen_pad_{v}_marked.png" for v, _, _ in vals])

# 3. one shader, two materials
save(Image.open(CAP / "crate/pair.png").convert("RGB").crop(PAIR_CROP),     # crates only (GATE T)
     "fig_pair.png", [CAP / "crate/pair.png"])


def sweep(param, values, names, crop=None, folder="crate"):
    return [tile(CAP / folder / f"crate_cube_{param}_{n}.png", 1248, 702, f"{param} = {v}", crop=crop)
            for v, n in zip(values, names)]


# 4. wear_amount sweep, 5. texture_scale sweep
save(grid(sweep("wear_amount", ["0.0 (min)", "0.1 (default)", "1.0 (max)"], ["0.0", "0.1", "1.0"]), 3, 1248, 702),
     "fig_wear.png", [CAP / f"crate/crate_cube_wear_amount_{n}.png" for n in ["0.0", "0.1", "1.0"]])
save(grid(sweep("texture_scale", ["0.1 (min)", "2.0 (default)", "10.0 (max)"], ["0.1", "2.0", "10.0"]), 3, 1248, 702),
     "fig_scale.png", [CAP / f"crate/crate_cube_texture_scale_{n}.png" for n in ["0.1", "2.0", "10.0"]])

# 6. the rest of the interface: paint_color; paint_roughness and wear_softness at the highlight angle
rows = (sweep("paint_color", ["black (min)", "olive (default)", "white (max)"],
              ["0-0-0-1", "0.26-0.283-0.19-1", "1-1-1-1"])
        + sweep("paint_roughness", ["0.0 (min)", "0.85 (default)", "1.0 (max)"], ["0.0", "0.85", "1.0"],
                crop=GLINT_CROP, folder="crate-glint")
        + sweep("wear_softness", ["0.0 (min = default)", "0.2 (max)"], ["0.0", "0.2"],
                crop=GLINT_CROP, folder="crate-glint") + [None])
save(grid(rows, 3, 1248, 702), "fig_interface.png",
     [CAP / "crate" / f"crate_cube_paint_color_{n}.png" for n in ["0-0-0-1", "0.26-0.283-0.19-1", "1-1-1-1"]]
     + [CAP / "crate-glint" / f"crate_cube_paint_roughness_{n}.png" for n in ["0.0", "0.85", "1.0"]]
     + [CAP / "crate-glint" / f"crate_cube_wear_softness_{n}.png" for n in ["0.0", "0.2"]])

# 7. hint experiment: 4K capture, band values written next to each band
hint = Image.open(CAP / "hint/hint_4k_3840x2160.png").convert("RGB")
d = ImageDraw.Draw(hint)
bands_x = [1639, 1920, 2201]
for y, row, pred, meas in [(834, "with source_color", [64, 128, 192], [64, 128, 192]),
                           (1326, "without source_color", [137, 188, 225], [137, 188, 225])]:
    d.text((300, y - 40), row, font=font(64), fill=(255, 255, 255))
    for x, p, m in zip(bands_x, pred, meas):
        d.text((x - 110, y + 150), f"pred {p}", font=font(52), fill=(255, 255, 255))
        d.text((x - 110, y + 215), f"meas {m}", font=font(52), fill=ACCENT)
d.text((300, 300), "file values: 64 · 128 · 192 (one 3x1 PNG, both quads)", font=font(64), fill=(255, 255, 255))
save(label(hint, "Native Godot render, 3840x2160, hint_experiment.tscn unchanged  ·  pixels read at band centres "
                 "(3x3 uniform)"), "fig_hint.png", [CAP / "hint/hint_4k_3840x2160.png"])

# 8. source_color removed from my line 3, in a film-only mutated copy
save(grid([tile(CAP / "crate-glint-wear/crate_cube_wear_amount_0.1.png", 1896, 1066,
                "crate_wear.gdshader line 3 as committed (source_color)", crop=GLINT_CROP),
           tile(CAP / "mutation-source-color/crate_cube_wear_amount_0.1.png", 1896, 1066,
                "source_color removed (film-only mutated copy)", crop=GLINT_CROP)], 2, 1896, 1066),
     "fig_mutation.png", [CAP / "crate-glint-wear/crate_cube_wear_amount_0.1.png",
                          CAP / "mutation-source-color/crate_cube_wear_amount_0.1.png"])

# 9-11. real test output
def screen_logs():
    img = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(img)
    d.text((120, 90), "screen_glow_check.gd at 30, 60 and 144 fps (real Tab key events)", font=font(72), fill=INK)
    d.text((120, 190), "lines copied verbatim from logs/screen_glow_check_{30,60,144}fps_final.log",
           font=font(44), fill=ACCENT)
    y, paths = 290, []
    for fps in (30, 60, 144):
        p = LOGS / f"screen_glow_check_{fps}fps_final.log"
        paths.append(p)
        d.text((120, y), f"{fps} fps", font=font(52), fill=ACCENT)
        y += 70
        for ln in p.read_text(encoding="utf-8").splitlines():
            if any(w in ln for w in ["after the state change (", "PASS  10", "PASS  8 ", "ALL PASS", "FAILED"]):
                d.text((160, y), ln.strip()[:140], font=font(44, mono=True), fill=INK)
                y += 60
        y += 30
    save(img, "fig_log_screen.png", paths)


screen_logs()
log_figure("fig_log_normal.png", "normal_map_check.gd: curl ratio, both conventions",
           LOGS / "normal_map_check_60fps_final.log", ["curl_ratio", "PASS", "FAIL"])
log_figure("fig_log_mutation.png", "test_materials.gd with source_color deleted from line 3",
           LOGS / "mutation_source_color_60fps.log", ["FAIL", "FAILED"])

(REEL / "figures" / "MANIFEST.json").write_text(json.dumps(MANIFEST, indent=1) + "\n", encoding="utf-8")
for k, v in MANIFEST.items():
    print(k, v["size"], v["sha256"][:12])
