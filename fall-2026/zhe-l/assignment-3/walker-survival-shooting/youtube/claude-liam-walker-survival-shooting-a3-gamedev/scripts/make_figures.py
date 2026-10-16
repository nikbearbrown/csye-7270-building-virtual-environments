"""Build the film's figure PNGs from real inputs only.

Every figure is an arrangement of (a) Claude's Blender MCP `look` viewport captures,
(b) the designer's own Blender screenshot, (c) native 4K Godot renders made by
capture/capture_driver.gd, or (d) text copied from the submitted documents and the
re-run check log (evidence/a3-check.log) at source revision b370626.
Prompts are the designer's words, translated from Chinese, exactly as SOURCES.md gives them.
Run:  python -I scripts/make_figures.py <toolkit-fonts-dir>
"""
import re
import sys
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
FONTS = Path(sys.argv[1])
FIG = REEL / "figures"
LOOK = REEL / "inputs" / "look"
STILL = REEL / "capture" / "stills"
PAGE, INK, SOFT, SPARK, LINE, CARD = "#FFFDF8", "#3D3929", "#665A4A", "#D97757", "#CFC6B5", "#F4EEE4"
W, H = 3456, 1330          # ~2.6:1, the image slot of GodotDesignFigure


def font(name, size):
    return ImageFont.truetype(str(sorted(FONTS.rglob(name))[0]), size)


SERIF = lambda s: font("EBGaramond-Regular.ttf", s)
SANS = lambda s: font("Lato-Regular.ttf", s)
SANSB = lambda s: font("Lato-Bold.ttf", s)
MONO = lambda s: font("PTMono-Regular.ttf", s)


def canvas():
    im = Image.new("RGB", (W, H), PAGE)
    return im, ImageDraw.Draw(im)


def fit(im, w, h):
    im = im.convert("RGB")
    s = min(w / im.width, h / im.height)
    return im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)


def panel(out, d, im, x, y, w, h, caption, sub):
    """Image fitted into a box, bold caption above, provenance line below."""
    d.text((x, y), caption, font=SANSB(56), fill=INK)
    im = fit(im, w, h - 200)
    px = x + (w - im.width) // 2
    out.paste(im, (px, y + 80))
    d.rectangle((px - 2, y + 78, px + im.width + 1, y + 80 + im.height + 1), outline=LINE, width=3)
    yy = y + 100 + im.height
    for line in textwrap.wrap(sub, 58):
        d.text((x, yy), line, font=SANS(40), fill=SOFT)
        yy += 50


def prompt_card(d, x, y, w, h, head, text, foot):
    d.rounded_rectangle((x, y, x + w, y + h), 24, fill=CARD, outline=SPARK, width=5)
    d.text((x + 50, y + 40), head, font=SANSB(50), fill="#8F452D")
    yy = y + 130
    for para in text.split("\n"):
        for line in textwrap.wrap(para, max(18, int(w / 46))):
            d.text((x + 50, yy), line, font=SERIF(84), fill=INK)
            yy += 100
        yy += 20
    d.text((x + 50, y + h - 80), foot, font=SANS(40), fill=SOFT)


LOOK_SUB = "viewport capture by Claude through the MCP look tool"


def tablet_prompt():
    out, d = canvas()
    prompt_card(d, 40, 40, 1500, H - 80, "My prompt (translated from Chinese)",
                "“Blender is open; make me a tablet, reference images: design/pad. Block it out with cubes; "
                "a greybox is enough. Because it is made from cubes, you can lose some detail.”",
                "SOURCES.md · PROP-TABLET-01 · 2026-10-12")
    panel(out, d, Image.open(LOOK / "2026-10-12_tablet_grey.png"), 1640, 40, 1780, H - 40,
          "What Claude built: 21 bevelled boxes, 804 triangles",
          f"2026-10-12 · {LOOK_SUB}")
    return out


def tablet_versions():
    out, d = canvas()
    prompt_card(d, 40, 40, 1180, H - 80, "My next prompt (translated)",
                "“The shape is fine, but it is hard to tell the front from the back. Use dark green and black "
                "for the shell, and one large black area for the screen.”",
                "SOURCES.md · PROP-TABLET-01")
    panel(out, d, Image.open(LOOK / "2026-10-12_tablet_green-black.png"), 1290, 40, 1050, H - 40,
          "2026-10-12 · 804 triangles", f"three materials · {LOOK_SUB}")
    panel(out, d, Image.open(LOOK / "2026-10-15_tablet_388tris.png"), 2390, 40, 1050, H - 40,
          "2026-10-15 · 388 triangles", f"bevels kept on body + 4 bumpers only · {LOOK_SUB}")
    return out


def chair():
    out, d = canvas()
    panel(out, d, Image.open(LOOK / "2026-10-07_chair_v1.png"), 60, 40, 1600, H - 40,
          "Version 1 (2026-10-07): 9 boxes, 108 triangles",
          f"Blender MCP · {LOOK_SUB}")
    row = Image.open(STILL / "row.png").crop((2150, 760, 2850, 1340))
    panel(out, d, row, 1800, 40, 1600, H - 40,
          "Version 2 (2026-10-15): 6 shapes, 72 triangles",
          "script route (headless Blender), so no viewport capture exists; shown here as a crop of a native "
          "Godot 4.7.2 render of base.tscn")
    return out


def crates():
    out, d = canvas()
    prompt_card(d, 40, 40, 1240, H - 80, "My prompt (translated)",
                "“…since the square crate is 0.5, from now on every 0.1 is one grid cell … the "
                "rectangular crate should become 1 × 0.5.”",
                "SOURCES.md · CRATE-LONG-02 (shortened …)")
    panel(out, d, Image.open(LOOK / "2026-10-15_crate_cube_v1.png"), 1350, 40, 1000, H - 40,
          "v1 · footprint 0.56 × 0.515 m", f"handles stick out · {LOOK_SUB}")
    panel(out, d, Image.open(LOOK / "2026-10-15_crate_cube_v2_grid.png"), 2410, 40, 1020, H - 40,
          "v2 · footprint 0.50 × 0.50 m", f"hardware inside the 5 × 5 cells · {LOOK_SUB}")
    return out


def my_screenshot():
    src = Image.open(REEL / "inputs" / "own" / "blender-session-01.png").convert("RGB")
    # Crop the window title bar only (it shows a local file path); the rest is unchanged.
    shot = src.crop((0, 22, src.width, src.height))
    out, d = canvas()
    full = fit(shot, 2380, H - 40)
    out.paste(full, (20, (H - full.height) // 2))
    # Enlarged insets of the same pixels: the sidebar Transform panel and the selected latch.
    side = src.crop((1432, 84, 1616, 168)).resize((184 * 5, 84 * 5), Image.LANCZOS)
    latch = src.crop((830, 360, 970, 500)).resize((140 * 3, 140 * 3), Image.LANCZOS)
    x = 2440
    d.text((x, 30), "Sidebar, enlarged (median point)", font=SANSB(48), fill=INK)
    out.paste(side, (x, 100))
    d.rectangle((x - 2, 98, x + side.width + 1, 100 + side.height + 1), outline=SPARK, width=4)
    d.text((x, 560), "Selected latch, enlarged", font=SANSB(48), fill=INK)
    out.paste(latch, (x, 630))
    d.rectangle((x - 2, 628, x + latch.width + 1, 630 + latch.height + 1), outline=SPARK, width=4)
    d.text((x, 1080), "Same screenshot pixels, scaled up;", font=SANS(40), fill=SOFT)
    d.text((x, 1130), "Chinese interface labels unchanged.", font=SANS(40), fill=SOFT)
    return out


def godot_wide(name, top, left=0):
    im = Image.open(STILL / f"{name}.png").convert("RGB")
    w = 3840 - left
    h = int(w / (W / H))
    return im.crop((left, top, 3840, top + h))


def parse_log():
    rows = {}
    for line in (REEL / "evidence" / "a3-check.log").read_text(encoding="utf-8").splitlines():
        m = re.match(r"(\w+): size \((.*)\), lowest y (\S+), triangles (\d+)", line)
        if m:
            rows[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    return rows


BRIEF = [("chair", "0.44 × 0.42 × 0.90", "0.0", "≤ 500"),
         ("tablet", "0.242 × 0.028 × 0.162", "−0.081", "≤ 500"),
         ("crate_long", "1.0 × 0.5 × 0.4", "0.0", "≤ 500"),
         ("crate_cube", "0.5 × 0.5 × 0.5", "0.0", "≤ 500")]


def brief_vs_headless():
    out, d = canvas()
    rows = parse_log()
    cols = [60, 560, 1360, 2240, 2780]
    d.text((cols[0], 40), "Brief (CHANGE-BRIEF, w × d × h, Blender Z-up)", font=SANSB(52), fill=INK)
    d.text((cols[2], 40), "HEADLESS: Godot bounding box (x, y, z), Y-up", font=SANSB(52), fill="#8F452D")
    hdr = ["asset", "size (m)", "size (m)", "lowest y", "triangles"]
    y = 200
    for c, t in zip(cols, hdr):
        d.text((c, y), t, font=SANSB(48), fill=SOFT)
    d.line((cols[0], y + 70, W - 60, y + 70), fill=LINE, width=4)
    y += 100
    for name, size, low, budget in BRIEF:
        s, ly, tri = rows[name]
        d.text((cols[0], y), name, font=MONO(64), fill=INK)
        d.text((cols[1], y), size, font=SANS(64), fill=INK)
        d.text((cols[2], y), f"({s})", font=MONO(64), fill=INK)
        d.text((cols[3], y), ly, font=MONO(64), fill=INK)
        d.text((cols[4], y), f"{tri}  ({budget})", font=MONO(64), fill=INK)
        y += 200
    d.line((cols[1] + 720, 170, cols[1] + 720, y - 40), fill=SPARK, width=5)
    d.text((cols[0], H - 110), "Recorded output: evidence/a3-check.log · re-run on a fresh export of b370626 · "
           "Godot 4.7.2 --headless · 55 PASS, 0 FAIL, exit code 0", font=SANS(42), fill=SOFT)
    return out


def log_part2():
    out, d = canvas()
    lines = (REEL / "evidence" / "a3-check.log").read_text(encoding="utf-8").splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith("== Part 2"))
    keep = lines[i:i + 18]
    d.rounded_rectangle((40, 40, W - 40, H - 40), 20, fill="#202531")
    y = 80
    for l in keep:
        l = re.sub(r", footprint (\S+) x (\S+) at x .*", r", \1 x \2 m", l).replace("world ", "")
        d.text((110, y), l, font=MONO(56), fill="#edf1f7" if "PASS" not in l else "#aee7d1")
        y += 66
    return out


FIGS = {"tablet_prompt": tablet_prompt, "tablet_versions": tablet_versions, "chair": chair, "crates": crates,
        "my_screenshot": my_screenshot, "brief_vs_headless": brief_vs_headless, "log_part2": log_part2,
        "godot_asset_cam": lambda: godot_wide("asset_cam", 330, 640), "godot_latch": lambda: godot_wide("latch_close", 200),
        "godot_tablet": lambda: godot_wide("tablet_close", 0), "godot_row": lambda: godot_wide("row", 480)}

if __name__ == "__main__":
    FIG.mkdir(exist_ok=True)
    for name, fn in FIGS.items():
        fn().save(FIG / f"{name}.png", optimize=True)
        print("figures/%s.png" % name)
