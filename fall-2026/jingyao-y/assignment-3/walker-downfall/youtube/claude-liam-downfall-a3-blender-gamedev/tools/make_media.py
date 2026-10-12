"""Build every result/evidence clip media/<BID>.mp4 for the A3 film.

  python tools/make_media.py <snapshot-of-ceada15>

Narration (actual_duration_s, measured by Kokoro) is the master clock. Engine
footage is trimmed only, never retimed. Stills are labelled holds. Every frame
carries a burned label saying where the picture came from and who made it:
Godot Movie Maker capture, Claude's Blender MCP `look`, recorded tool output,
or the author's own screenshot. Text panels draw only lines that appear in the
recorded logs or in the conversation's recorded MCP output.
"""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
SNAP = Path(sys.argv[1])
IMG, MEDIA, CAP = REEL / "images", REEL / "media", REEL / "capture"
sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
dur = {b["beat_id"]: b.get("actual_duration_s") for b in sheet["beats"]}
W, H = 3840, 2160
F = "C:/Windows/Fonts/"
serif = lambda s: ImageFont.truetype(F + "georgia.ttf", s)
sans = lambda s: ImageFont.truetype(F + "segoeui.ttf", s)
mono = lambda s: ImageFont.truetype(F + "consola.ttf", s)
cjk = lambda s: ImageFont.truetype(F + "msyh.ttc", s)
INK, PAPER, MUTED = "#2f2b26", "#FAF9F5", "#6b645a"
FFONT = "C\\:/Windows/Fonts/msyh.ttc"


def run(cmd):
    subprocess.run(cmd, check=True)


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,")


def label(d, text, y=H - 205):
    # Burned provenance label, inside title-safe, dark box like the capture labels.
    f = cjk(46)
    w = d.textlength(text, font=f)
    d.rectangle([230, y, 230 + w + 72, y + 96], fill="#000000")
    d.text((266, y + 18), text, font=f, fill="#ffffff")


def fit(im, box_w, box_h):
    s = min(box_w / im.width, box_h / im.height)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def canvas(dark=False):
    o = Image.new("RGB", (W, H), "#15161a" if dark else PAPER)
    return o, ImageDraw.Draw(o)


def still_mp4(bid, frames):
    """frames: list of (png path, seconds or None for the remainder)."""
    total = dur[bid]
    used = sum(s for _, s in frames if s)
    parts = []
    for i, (png, s) in enumerate(frames):
        s = s if s else total - used
        part = MEDIA / f"_{bid}_{i}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-t", f"{s:.3f}", "-i", str(png),
             "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(part)])
        parts.append(part)
    concat(bid, parts)


def concat(bid, parts):
    listing = MEDIA / f"_{bid}.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
         "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(MEDIA / f"{bid}.mp4")])
    for p in parts: p.unlink()
    listing.unlink()
    print(bid, dur[bid])


def clip_mp4(bid, avi, start, text):
    """A contiguous window of a native 4K capture, trimmed only, with a burned label."""
    end = start + dur[bid]
    vf = (f"drawbox=x=230:y=ih-205:w=iw*0.62:h=96:color=black@0.85:t=fill,"
          f"drawtext=fontfile='{FFONT}':text='{esc(text)}':x=266:y=h-187:fontsize=46:fontcolor=white")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(CAP / avi),
         "-vf", vf, "-r", "30", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(MEDIA / f"{bid}.mp4")])
    print(bid, dur[bid], f"{avi} {start:.2f}-{end:.2f}s")


def full_still(src, text, out):
    o, d = canvas(dark=True)
    im = fit(Image.open(src).convert("RGB"), W, H)
    o.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    label(d, text)
    o.save(out)
    return out


MEDIA.mkdir(exist_ok=True)
gen = REEL / "_qc" / "gen"
gen.mkdir(parents=True, exist_ok=True)

# B02 — the assignment's limits (as the author gave them in chat) beside the real terraced floor.
o, d = canvas()
d.text((210, 150), "Assignment 3 limits, per asset", font=serif(96), fill=INK)
limits = ["≤ 6 primitives", "< 500 triangles", "flat-colour materials only",
          "no sculpting · no textures", "no rigging · no animation",
          "one .blend per asset", "modelled around the world origin", "bottom on the ground"]
for i, t in enumerate(limits):
    d.text((230, 360 + i * 150), "·  " + t, font=sans(72), fill=INK)
game = fit(Image.open(IMG / "game-terrace-4k.png").convert("RGB"), 1900, 1069)
o.paste(game, (1760, 380))
d.text((1760, 1475), "Mine floor, map seed 1729: a ramp climbing one 2.2 m terrace", font=sans(50), fill=MUTED)
label(d, "Limits as given by the author · real Godot capture, isolated clone of ceada15 (teleported into place)")
o.save(gen / "B02.png")
still_mp4("B02", [(gen / "B02.png", None)])

# B04 — the two real game frames, each held for half the narration.
LBL = "Real Godot capture · 3840×2160 · teleported into place (test shortcut) · isolated clone of ceada15"
a = full_still(IMG / "game-ramp-4k.png", "Ramp foot (seed 1729) · " + LBL, gen / "B04a.png")
b = full_still(IMG / "game-cliff-4k.png", "Below a cliff between terraces (seed 1333) · " + LBL, gen / "B04b.png")
still_mp4("B04", [(a, dur["B04"] / 2), (b, None)])

# B06 — Claude's look views: cliff and rubble, before and after the fix.
o, d = canvas(dark=True)
cells = [("blender-cliff-before.png", "cliff · before (call 5)"), ("blender-cliff-after.png", "cliff · after (call 6)"),
         ("blender-rubble-before.png", "rubble · before (call 4)"), ("blender-rubble-after.png", "rubble · after (call 5)")]
for i, (name, cap) in enumerate(cells):
    im = fit(Image.open(IMG / name).convert("RGB"), 1700, 800)
    x = 160 + (i % 2) * 1820
    y = 70 + (i // 2) * 900
    o.paste(im, (x + (1700 - im.width) // 2, y))
    d.text((x + (1700 - im.width) // 2, y + im.height + 8), cap, font=sans(48), fill="#e9e4d8")
label(d, "Blender look views (front · right · top · three-quarter; the after views skip top) · captured by Claude through Blender MCP")
o.save(gen / "B06.png")
still_mp4("B06", [(gen / "B06.png", None)])

# B08 — the ramp's look views.
full_still(IMG / "blender-ramp.png",
           "Blender look views (front · right · three-quarter · low front) · captured by Claude through Blender MCP · before the kerb edit",
           gen / "B08.png")
still_mp4("B08", [(gen / "B08.png", None)])

# B10 — recorded MCP output after the author's kerb edit (verbatim; the one file path is shortened, and says so).
o, d = canvas()
d.text((210, 150), "After the author's edit: Claude reads the file back", font=serif(92), fill=INK)
d.rectangle([210, 330, 3630, 1830], fill="#202531")
rec = [("get_scene_info", "#9fb8d0"),
       ("arched_ramp_segment | mesh | at (0.0, 0.0, 0.0) | rot (0, 0, 0) | scale (1.0, 1.0, 1.0)", "#d7e4ef"),
       ("    | size 7.0x6.5x2.47 | on ground | 34 faces", "#9fe08a"),
       ("", None),
       ("execute_blender_code (read-only check)", "#9fb8d0"),
       ("file …\\art\\blender\\arched_ramp_segment.blend dirty False mode OBJECT", "#d7e4ef"),
       ("piece verts 8  x -3.5000 .. -3.2000  median x -3.3500", "#9fe08a"),
       ("piece verts 24  x -3.4000 .. 3.4000  median x 0.0000", "#d7e4ef"),
       ("piece verts 8  x 3.2000 .. 3.5000  median x 3.3500", "#9fe08a"),
       ("arched_ramp_segment.blend True 99943", "#d7e4ef"),
       ("arched_ramp_segment.blend1 True 99943", "#d7e4ef")]
for i, (t, c) in enumerate(rec):
    if c: d.text((280, 400 + i * 118), t, font=mono(60), fill=c)
d.text((210, 1880), "Recorded output, verbatim except the shortened file path (…).", font=sans(48), fill=MUTED)
label(d, "Recorded MCP output · 2026-10-12 · the edit itself was made by the author by hand")
o.save(gen / "B10.png")
still_mp4("B10", [(gen / "B10.png", None)])

# B12 — the orbit: a moment through the game camera, then one full turn (trimmed so the turn completes).
clip_mp4("B12", "orbit.avi", 18.0 - dur["B12"], "Real Godot render · Movie Maker 3840×2160 · isolated clone of ceada15 · captured by Claude")

# B14 — the recorded test log from a fresh copy of ceada15 (only lines from the log).
log = (REEL / "evidence" / "test_a3_assets-ceada15.log").read_text(encoding="utf-8").splitlines()
keep = [l for l in log if re.match(r"(PASS|FAIL|RESULT) ", l)]
o, d = canvas()
d.text((210, 110), "tests/test_a3_assets.gd on a fresh copy of ceada15", font=serif(84), fill=INK)
d.rectangle([210, 260, 3630, 1880], fill="#202531")
for i, t in enumerate(keep):
    short = t if len(t) <= 118 else t[:117] + "…"
    d.text((260, 290 + i * 59), short, font=mono(44), fill="#ff8a7a" if t.startswith("FAIL") else ("#9fe08a" if t.startswith("RESULT") else "#d7e4ef"))
label(d, "Recorded test output · Godot 4.7.2 headless · long lines cut with …")
o.save(gen / "B14.png")
still_mp4("B14", [(gen / "B14.png", None)])

# B16 — the light bug, re-rendered: a frame from each half of capture/light.avi.
for n, frame in (("before", 50), ("after", 110)):
    run(["ffmpeg", "-v", "error", "-y", "-i", str(CAP / "light.avi"), "-vf", f"select=eq(n\\,{frame})", "-frames:v", "1",
         str(gen / f"light-{n}.png")])
# Side by side, so the pair fills the frame: left the basis as first written, right the corrected one.
o, d = canvas()
for i, (n, cap) in enumerate((("before", "Sun basis as first written: light points up"), ("after", "Corrected basis (ceada15)"))):
    im = fit(Image.open(gen / f"light-{n}.png").convert("RGB"), 1700, 1500)
    x = 230 + i * 1720
    o.paste(im, (x, 200))
    d.text((x, 200 + im.height + 20), cap, font=sans(60), fill=INK)
label(d, "Real Godot renders · re-rendered from capture/light.avi frames 50 and 110 · captured by Claude")
o.save(gen / "B16.png")
still_mp4("B16", [(gen / "B16.png", None)])

# B17 — the author's own screenshot and the author's report.
o, d = canvas()
shot = fit(Image.open(IMG / "user-01-blender-ui.png").convert("RGB"), 2700, 1690)
o.paste(shot, (150, 150))
d.text((3000, 330), "Author's human check", font=serif(64), fill=INK)
d.text((3000, 450), "“都是对的”", font=cjk(96), fill=INK)
d.text((3000, 590), "(“everything is correct”)", font=sans(52), fill=MUTED)
d.text((3000, 800), "Recorded as given,", font=sans(52), fill=INK)
d.text((3000, 870), "no detail added.", font=sans(52), fill=INK)
label(d, "Screenshot taken by the author · Blender 5.4 Alpha · scene statistics in the status bar")
o.save(gen / "B17.png")
still_mp4("B17", [(gen / "B17.png", None)])
