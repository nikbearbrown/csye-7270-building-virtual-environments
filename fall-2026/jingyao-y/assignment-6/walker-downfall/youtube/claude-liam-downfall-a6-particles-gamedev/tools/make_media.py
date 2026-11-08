"""Build the A6 film's evidence clips from real engine output (no redrawn frames).

Stills: actual capture PNGs, user screenshots and verbatim log lines laid out on a
3840x2160 board; enlargements use nearest-neighbour only and are labelled.
Motion: Movie Maker PNG sequences at their recorded 30 fps (never retimed); a
take shorter than its beat is replayed once, labelled REPLAY on screen.

    python tools/make_media.py [KEY ...]     # keys are film keys (B03, B13b, ...)
"""
from pathlib import Path
import json
import math
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1]
CAP = GAME / "captures"
NEW = REEL / "capture"
OUT = REEL / "media"
IMG = REEL / "images"
SERIF = "C:/Windows/Fonts/georgia.ttf"
EB = str(GAME.parents[4] / "brutalist.art/runtime/fonts/EB_Garamond/static/EBGaramond-Regular.ttf")
SANS = "C:/Windows/Fonts/segoeui.ttf"
SANSB = "C:/Windows/Fonts/segoeuib.ttf"
MONO = "C:/Windows/Fonts/consola.ttf"
PAPER, INK, SOFT, ACCENT, RULE = "#FAF9F5", "#302d27", "#5b564c", "#D97757", "#d8d3c6"
W, H = 3840, 2160
X0, X1 = 210, 3630

sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
BEAT = {b["film_key"]: b for b in sheet["beats"]}
manifest_path = REEL / "media-provenance.json"
MANIFEST = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}


def dur(key):
    b = BEAT[key]
    return math.ceil(b.get("actual_duration_s", b["estimated_duration_s"]) * 30) / 30


def font(path, size):
    return ImageFont.truetype(path, size)


def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)


def frame(rel, n):
    return Image.open(CAP / rel / f"frame{n:08d}.png").convert("RGB")


def crop(img, box, k):
    c = img.crop(box)
    return c.resize((c.width * k, c.height * k), Image.Resampling.NEAREST)


def wrap(draw, text, f, width):
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            t = (line + " " + word).strip()
            if draw.textlength(t, font=f) <= width:
                line = t
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def base(title, provenance):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.text((X0, 120), title, font=font(EB, 108), fill=INK)
    y = 1905
    for line in wrap(d, provenance, font(SANS, 40), 2900):
        d.text((X0, y), line, font=font(SANS, 40), fill=SOFT)
        y += 52
    brand = font(EB, 56)
    d.text((3590 - d.textlength("@NikBearBrown", font=brand), 1975), "@NikBearBrown", font=brand, fill=INK)
    return im, d


def tile(im, d, img, box, caption=None, label_size=46):
    x0, y0, x1, y1 = box
    avail_h = y1 - y0 - (70 if caption else 0)
    s = min((x1 - x0) / img.width, avail_h / img.height)
    pic = img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))),
                     Image.Resampling.NEAREST if s >= 1 else Image.Resampling.LANCZOS)
    px = x0 + (x1 - x0 - pic.width) // 2
    im.paste(pic, (px, y0))
    d.rectangle((px - 2, y0 - 2, px + pic.width + 1, y0 + pic.height + 1), outline=RULE, width=3)
    if caption:
        d.text((px, y0 + pic.height + 16), caption, font=font(SANS, label_size), fill=INK)
    return y0 + pic.height


def panel(d, box, heading, lines, size=44, mono=False, accent_first=False):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill="#F1EEE6", outline=RULE, width=3)
    d.text((x0 + 36, y0 + 26), heading, font=font(SANSB, 46), fill=INK)
    f = font(MONO if mono else SANS, size)
    y = y0 + 110
    for i, raw in enumerate(lines):
        for line in wrap(d, raw, f, x1 - x0 - 80):
            if y + size * 1.3 > y1 - 10:
                raise SystemExit(f"panel overflow: {heading}")
            d.text((x0 + 40, y), line, font=f, fill=ACCENT if (accent_first and i == 0) else INK)
            y += int(size * 1.32)
        y += int(size * 0.45)


def grid(n, cols, top=330, bottom=1860, gap=40, left=X0, right=X1):
    rows = math.ceil(n / cols)
    cw = (right - left - gap * (cols - 1)) / cols
    ch = (bottom - top - gap * (rows - 1)) / rows
    return [(int(left + (i % cols) * (cw + gap)), int(top + (i // cols) * (ch + gap)),
             int(left + (i % cols) * (cw + gap) + cw), int(top + (i // cols) * (ch + gap) + ch)) for i in range(n)]


def still(key, boards, sources):
    """boards: list of PIL images shown in equal shares of the beat."""
    OUT.mkdir(exist_ok=True)
    IMG.mkdir(exist_ok=True)
    bid = BEAT[key]["beat_id"]
    total = dur(key)
    parts = []
    for i, im in enumerate(boards):
        path = IMG / f"{bid}-{key}-{i}.png"
        im.save(path)
        part = OUT / f"_{bid}_{i}.mp4"
        seconds = total / len(boards)
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", str(path), "-t", f"{seconds:.6f}",
             "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(part)])
        parts.append(part)
    concat(bid, parts)
    MANIFEST[bid] = {"film_key": key, "kind": "still boards (held, equal shares)", "duration": total,
                     "sources": [str(s) for s in sources], "boards": len(boards)}


def concat(bid, parts):
    listing = OUT / f"_{bid}.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(OUT / f"{bid}.mp4")])
    for p in parts:
        p.unlink()
    listing.unlink()
    print("built", bid, flush=True)


def motion(key, take, title, side, zoom_box, provenance, start=0, end=None):
    """take: folder under capture/ (new Movie Maker frames). Full frame 2x nearest + zoom 5x."""
    OUT.mkdir(exist_ok=True)
    IMG.mkdir(exist_ok=True)
    bid = BEAT[key]["beat_id"]
    total = dur(key)
    frames = sorted((NEW / take).glob("frame*.png"))
    end = len(frames) if end is None else end
    length = (end - start) / 30
    replay = total > length + 1e-6
    im, d = base(title, provenance + (f" Take shown at recorded speed; after {length:.1f} s the same take is replayed (labelled REPLAY)." if replay else " Shown at recorded speed."))
    zx, zy, zx1, zy1 = zoom_box
    k = 800 // (zx1 - zx)
    d.text((2840, 330 + (zy1 - zy) * k + 20), f"crop {zx1 - zx}×{zy1 - zy} px, enlarged {k}× (nearest neighbour)", font=font(SANS, 36), fill=SOFT)
    panel(d, (2840, 330 + (zy1 - zy) * k + 90, 3630, 1860), "On screen", side, size=40)
    d.text((X0, 1790), "1280×720 Movie Maker frames, enlarged 2× (nearest neighbour)", font=font(SANS, 36), fill=SOFT)
    bg = IMG / f"{bid}-{key}-bg.png"
    im.save(bg)
    raw = NEW / take / "take.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", str(start), "-i", str(NEW / take / "frame%08d.png"),
         "-frames:v", str(end - start), "-c:v", "libx264", "-preset", "fast", "-crf", "10", "-pix_fmt", "yuv444p", str(raw)])
    L = end - start
    counter = (f"drawtext=fontfile='C\\:/Windows/Fonts/consola.ttf':text='capture frame %{{eif\\:mod(n\\,{L})+{start}\\:d}}':"
               f"x=2080:y=1790:fontsize=40:fontcolor=white:box=1:boxcolor=black@0.75:boxborderw=10")
    rep = (f",drawtext=fontfile='C\\:/Windows/Fonts/segoeuib.ttf':text='REPLAY of the same take':x=1500:y=1782:fontsize=46:"
           f"fontcolor=white:box=1:boxcolor=0xD97757@0.9:boxborderw=12:enable='gte(n\\,{L})'") if replay else ""
    fc = (f"[1:v]split[a][b];[a]scale=2560:1440:flags=neighbor[full];"
          f"[b]crop={zx1 - zx}:{zy1 - zy}:{zx}:{zy},scale={(zx1 - zx) * k}:{(zy1 - zy) * k}:flags=neighbor[zoom];"
          f"[0:v][full]overlay=200:330[t];[t][zoom]overlay=2840:330,{counter}{rep},format=yuv420p[v]")
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", str(bg), "-stream_loop", "-1", "-i", str(raw),
         "-filter_complex", fc, "-map", "[v]", "-t", f"{total:.6f}", "-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "16",
         "-an", str(OUT / f"{bid}.mp4")])
    print("built", bid, flush=True)
    MANIFEST[bid] = {"film_key": key, "kind": "native capture (Movie Maker, 30 fps), not retimed", "take": f"capture/{take}",
                     "frames": [start, end], "take_seconds": length, "beat_seconds": total, "replayed": replay,
                     "zoom_box": zoom_box, "enlargement": "2x full frame, %dx crop, nearest neighbour" % k}


HS = (560, 300, 720, 420)       # hit_spark strip crop (TUNING.md)
FP = (580, 290, 700, 410)       # fire strip crop (TUNING.md)
FIX = "FIXTURE capture (preview scene, not gameplay) · Godot 4.7.2 Movie Maker, 30 fps, RTX 4060 Laptop, D3D12 Forward+ · "


def log_lines(rel, needles):
    text = (GAME / rel).read_text(encoding="utf-8", errors="replace").splitlines()
    out = []
    for n in needles:
        hit = next((l.strip() for l in text if n in l), None)
        assert hit is not None, (rel, n)
        out.append(hit)
    return out


def build(key):
    if key == "B03":
        motion("B03", "a_play", "Effect A In The Real Game Loop",
               ["SCRIPTED-INPUT capture, not human play: held left mouse on fixture dummies (as in the state test)",
                "City floor, seed 2026; Amiya (guard)",
                "8 HitSparks while held; the 3rd and 7th cuts 3 frames after the one before (overlap)",
                "Frame ~176: a 1-HP dummy dies on the blow; its burst plays on",
                "Pink arcs: the older mesh spark, kept"],
               (620, 290, 780, 410), FIX.replace("preview scene", "film helper tools/capture_play.gd") + "capture/a_play/ (new; hit_spark.tscn at r1, Puff 1.0).")
    elif key == "B05":
        motion("B05", "b_loop", "Effect B: The Feedback Loop On Screen",
               ["previews/fire_pit_flames_preview.tscn -- --loop", "Sami snow, seed 2026, pit 1, fixed particle seed",
                "Frame 10: fed 120 s, ratio 1.0", "Frame 250: burn_left 24 s, ratio 0.44", "Frame 400: burn_left 0, emitting false"],
               (560, 290, 720, 410), FIX + "capture/b_loop/ (new).")
    elif key == "B07":
        r = "hit_spark/r0"
        pred = {10: "trigger frame", 12: "Δt 0.067 s · throw", 15: "Δt 0.167 s · settle", 20: "Δt 0.333 s · 2nd burst",
                30: "Δt 0.667 s · clear", 50: "Δt 1.333 s · 0 nodes"}
        im, d = base("Strip r0: The City, Frame By Frame", FIX + "captures/hit_spark/r0/ (bursts fired at frames 10 and 16; seeds 7370/7371). Full 1280×720 frames.")
        for box, (n, p) in zip(grid(6, 3), pred.items()):
            tile(im, d, frame(r, n), box, f"frame {n} · {p}")
        still("B07", [im], [CAP / r])
    elif key == "B09":
        r = "hit_spark/r0"
        im, d = base("Stills Versus Motion", FIX + "captures/hit_spark/r0/, crop 560–720 × 300–420 enlarged 5× (nearest neighbour). Quotes: TUNING.md, translated from Chinese.")
        for box, n in zip(grid(4, 2, right=2380), (10, 12, 15, 20)):
            tile(im, d, crop(frame(r, n), HS, 5), box, f"frame {n}")
        panel(d, (2460, 330, 3630, 1860), "Two readings of r0",
              ["Claude, reading the stills:", "“the sparks look too small and travel too little to read as an outward throw.”",
               "The user, watching the running preview:", "“I can see it splashing outward.”",
               "Outcome: the user's verdict stands. Nothing was changed on Claude's reading."], size=58)
        still("B09", [im], [CAP / r])
    elif key == "B11":
        motion("B11", "a_loop_city", "Process In Motion",
               ["previews/hit_spark_preview.tscn -- --loop", "City floor, seed 2026, stand-in enemy, fixed particle seed",
                "Two bursts 6 frames apart; the pair repeats every 90 frames",
                "Captured after the r1 edit (Puff 1.0); Flash and Sparks settings are the same as r0"],
               (560, 290, 720, 410), FIX + "capture/a_loop_city/ (new).")
    elif key == "B13":
        r = "hit_spark/r0-snow"
        im, d = base("Strip r0-snow: Where Is The Puff?", FIX + "captures/hit_spark/r0-snow/, crop 560–720 × 300–420 enlarged 4×. Luminance and quotes: TUNING.md (user quotes translated from Chinese).")
        for box, n in zip(grid(6, 3, right=2560), (10, 12, 15, 20, 30, 50)):
            tile(im, d, crop(frame(r, n), HS, 4), box, f"frame {n}")
        panel(d, (2640, 330, 3630, 1860), "Recorded",
              ["Snow patch below the body (x 630–650, y 378–386): 158.3 on every frame, 10 to 50.",
               "The user: “I can see it.” On the puff: “Barely see a little.”",
               "Claude's arithmetic: 0.5-unit quad × scale 0.6→1.4 = 9→21 px, centred on a ~30 px body."], size=52)
        still("B13", [im], [CAP / r])
    elif key == "B15":
        im, d = base("A Wrong Diagnosis, Then A Fixture Fix", FIX + "captures/fire_pit_flames/r0/ and r0b/, crop 580–700 × 290–410 enlarged 4×; user screenshot evidence/a6/user/. Quotes translated from Chinese.")
        for box, n in zip(grid(3, 3, top=330, bottom=1000, right=2480), (12, 54, 70)):
            tile(im, d, crop(frame("fire_pit_flames/r0", n), FP, 4), box, f"r0 · frame {n}")
        for box, n in zip(grid(3, 3, top=1150, bottom=1860, right=2480), (12, 54, 70)):
            tile(im, d, crop(frame("fire_pit_flames/r0b", n), FP, 4), box, f"r0b · frame {n}")
        user = Image.open(GAME / "evidence/a6/user/fire_pit_preview_occluded_by_boulders.png").convert("RGB")
        tile(im, d, user, (2560, 330, 3630, 1000), "USER SCREENSHOT (running preview)", label_size=38)
        panel(d, (2560, 1150, 3630, 1860), "Recorded",
              ["User: “Blocked by the stones, can't see it.”", "Claude: emitter too low inside the pit model. Withdrawn.",
               "Cause: the fixture. 3 or 4 pits, moving run to run; fix: seed_rng + open pit 1 → r0b."], size=44)
        still("B15", [im], [CAP / "fire_pit_flames/r0", CAP / "fire_pit_flames/r0b", GAME / "evidence/a6/user/fire_pit_preview_occluded_by_boulders.png"])
    elif key == "B17":
        im, d = base("r0b → r1: Prediction, Match, Miss", FIX + "captures/fire_pit_flames/r0b/ and r1/, crop 580–700 × 290–410 enlarged 4×. Warm-pixel counts and verdict: TUNING.md (Claude's measurement; user quote translated).")
        warm = {"r0b": {12: 72, 40: 58, 54: 76, 70: 36}, "r1": {12: 170, 40: 164, 54: 162, 70: 108}}
        for row, r in enumerate(("r0b", "r1")):
            top = 330 + row * 770
            for box, n in zip(grid(3, 3, top=top, bottom=top + 720, right=2480), (12, 54, 70)):
                tile(im, d, crop(frame(f"fire_pit_flames/{r}", n), FP, 4), box, f"{r} · {n} · {warm[r][n]} warm px", label_size=40)
        panel(d, (2560, 330, 3630, 1860), "Flames quad 0.30 → 0.55",
              ["Predicted: ≥ 2× warm px on full-fire frames; top ≥ 5 px higher.",
               "Measured: 2.2–2.8× — match.", "Top rose 2–3 px — MISS. Height comes from speed × lifetime; a bigger quad thickens the core.",
               "User, running preview: “Keep.”"], size=50)
        still("B17", [im], [CAP / "fire_pit_flames/r0b", CAP / "fire_pit_flames/r1"])
    elif key == "B19":
        motion("B19", "b_states", "Start, Pause, Hide, Thin, Out",
               ["Film helper tools/capture_fire_states.gd (label on screen)", "10 fed 120 s · 60–105 tree paused",
                "140–170 effect hidden · 200 burn_left 24 s", "260 burn_left 0: emitting false",
                "State test B1–B6: 0 failures (headless)"],
               (633, 295, 793, 415), FIX.replace("preview scene", "film helper") + "capture/b_states/ (new).")
    elif key == "B21":
        r = "fire_pit_flames/r1"
        im, d = base("Turbulence: Same Seed, Different Lean", FIX + "captures/fire_pit_flames/r1/, crop 580–700 × 290–410 enlarged 6× (nearest neighbour).")
        for box, n in zip(grid(3, 3, bottom=1500), (12, 40, 54)):
            tile(im, d, crop(frame(r, n), FP, 6), box, f"frame {n} · ratio 1.0")
        d.text((X0, 1600), "Embers: 0.05-unit quads ≈ 1.5 px at default zoom — barely visible (README, Known limitations).", font=font(SANS, 50), fill=INK)
        still("B21", [im], [CAP / r])
    elif key == "B23":
        im, d = base("Mutation M1: A Godot 3 Name", "FIXTURE captures: captures/hit_spark/r0/frame00000012.png and evidence/a6/mutations/m1_godot3_name_frame12_fixture.png, crop 560–720 × 300–420 enlarged 5×. Log lines verbatim from evidence/a6/mutations/.")
        tile(im, d, crop(frame("hit_spark/r0", 12), HS, 5), (X0, 330, 1850, 1180), "r0 · frame 12 · initial_velocity_min = 3.0")
        tile(im, d, crop(Image.open(GAME / "evidence/a6/mutations/m1_godot3_name_frame12_fixture.png").convert("RGB"), HS, 5),
             (1990, 330, 3630, 1180), "M1 · frame 12 · initial_velocity = 3.0")
        panel(d, (X0, 1290, 3630, 1860), "Recorded output",
              log_lines("evidence/a6/mutations/m1_godot3_name.log", ["FAIL Sparks", "checks,"]) +
              ["m1b (initial_velocity = Vector2(3, 6)): " + log_lines("evidence/a6/mutations/m1b_compat_vector2.log", ["checks,"])[0]],
              size=48, mono=True)
        still("B23", [im], [CAP / "hit_spark/r0", GAME / "evidence/a6/mutations"])
    elif key == "B25":
        diff = subprocess.run(["diff", str(GAME / "evidence/a6/step6/attempt1_particles_generated.gdshader.txt"),
                               str(GAME / "shaders/particles_generated.gdshader")], capture_output=True, text=True, encoding="utf-8").stdout
        lines = [l.replace("\t", "  ") for l in diff.splitlines()]
        im, d = base("Attempt 1 Was A Stale Default Shader", "Recorded output: diff evidence/a6/step6/attempt1_particles_generated.gdshader.txt shaders/particles_generated.gdshader (verbatim). Crops: FIXTURE captures/hit_spark/r0/, enlarged 4×.")
        panel(d, (X0, 330, 2620, 1860), "diff attempt1 attempt2 (complete)", lines, size=40, mono=True)
        for box, n in zip(grid(3, 1, left=2700, right=3630), (12, 15, 20)):
            tile(im, d, crop(frame("hit_spark/r0", n), HS, 4), box, f"r0 · frame {n}", label_size=40)
        still("B25", [im], [GAME / "evidence/a6/step6/attempt1_particles_generated.gdshader.txt", GAME / "shaders/particles_generated.gdshader", CAP / "hit_spark/r0"])
    elif key == "B27":
        r = "fire_pit_flames/r1"
        im, d = base("Amount Ratio: Thinner, Not Restarted", FIX + "captures/fire_pit_flames/r1/, enlarged 6×. Warm px: TUNING.md. Monitor line verbatim from logs/test_fire_pit_flames_state_60fps.log.")
        tile(im, d, crop(frame(r, 54), FP, 6), (X0, 330, 1850, 1330), "frame 54 · ratio 1.0 · 162 warm px")
        tile(im, d, crop(frame(r, 70), FP, 6), (1990, 330, 3630, 1330), "frame 70 · ratio 0.44 · 108 warm px")
        panel(d, (X0, 1430, 3630, 1860), "Recorded output (headless state test)",
              log_lines("logs/test_fire_pit_flames_state_60fps.log", ["MONITOR samples", "PASS B3 every frame"]), size=46, mono=True)
        still("B27", [im], [CAP / r, GAME / "logs/test_fire_pit_flames_state_60fps.log"])
    elif key == "B29":
        im, d = base("What The Tests Proved", "Recorded output, verbatim lines from logs/ and evidence/a6/mutations/ (headless, fixed 60 fps, Godot 4.7.2).")
        panel(d, (X0, 330, 1920, 1860), "Config, mutations, state",
              ["test_hit_spark_config: " + log_lines("logs/test_hit_spark_config_60fps.log", ["checks,"])[0].split(": ", 1)[1],
               "test_fire_pit_flames_config: " + log_lines("logs/test_fire_pit_flames_config_60fps.log", ["checks,"])[0].split(": ", 1)[1],
               "M1 Godot 3 float: " + log_lines("evidence/a6/mutations/m1_godot3_name.log", ["exit="])[0],
               "M1b Vector2 compat: " + log_lines("evidence/a6/mutations/m1b_compat_vector2.log", ["exit="])[0],
               "M2 drift: " + log_lines("evidence/a6/mutations/m2_value_drift.log", ["FAIL"])[0],
               "Parent mutation: " + log_lines("logs/test_hit_spark_state_60fps_mutation_parent.log", ["HIT_SPARK_STATE"])[0],
               "A state: " + log_lines("logs/test_hit_spark_state_60fps.log", ["HIT_SPARK_STATE"])[0] + " (22 PASS)",
               "B state: " + log_lines("logs/test_fire_pit_flames_state_60fps.log", ["FIRE_PIT_FLAMES_STATE"])[0]],
              size=54, mono=True)
        panel(d, (2000, 330, 3630, 1860), "Whole suite, 60 fps, parallel",
              ["Before A6: " + log_lines("logs/baseline-before/summary.txt", ["of 89 pass"])[0],
               "After A6: " + log_lines("logs/baseline-after-step5/summary.txt", ["of 93 pass"])[0],
               "The failures are the pre-existing ones (TEST-REPORT.md); the four new suites pass.",
               "Headless cannot show: that bursts look right, legibility, screen-edge clipping, freezing on screen."], size=66)
        still("B29", [im], [GAME / "logs", GAME / "evidence/a6/mutations"])
    elif key == "B31":
        lines = (GAME / "logs/cost_effects_60fps.log").read_text(encoding="utf-8").splitlines()
        i = next(k for k, l in enumerate(lines) if l.startswith("case "))
        block = [l for l in lines[i:i + 6]] + [l.strip() for l in lines if l.strip().startswith(("A_8 ", "B_1 ", "B_all ")) and "ms  sd" in l]
        block += [l for l in lines if l.startswith("CHECK")]
        im, d = base("Headless Price: Indistinguishable From Off", "Recorded output, verbatim from logs/cost_effects_60fps.log (tests/cost_effects.gd, fixed 60 fps, 5 rounds × 300 frames, Sami floor, seed 2026).")
        panel(d, (X0, 330, 3630, 1860), "SUMMARY (wall-clock ms per frame)", block, size=40, mono=True)
        still("B31", [im], [GAME / "logs/cost_effects_60fps.log"])
    elif key == "B32":
        g = GAME / "evidence/a6/gpu"
        im, d = base("GPU Price: The User's Visual Profiler", "USER SCREENSHOTS, Godot 4.7.2 editor Visual Profiler, previews/gpu_price.tscn (fixture), RTX 4060 Laptop, 1280×720, vsync on. Single selected frames; readings from TEST-REPORT.md.")
        shots = [("visual_profiler_round3_both_off.png", "both off · row absent"), ("visual_profiler_round2_U_A_on.png", "A on (≈8 bursts)"),
                 ("visual_profiler_round2_I_B_on.png", "B on (3 pits full)")]
        rows = {"visual_profiler_round3_both_off.png": (25, 145, 450, 330), "visual_profiler_round2_U_A_on.png": (25, 30, 450, 215),
                "visual_profiler_round2_I_B_on.png": (5, 125, 440, 310)}
        for box, (n, c) in zip(grid(3, 3, bottom=860), shots):
            tile(im, d, Image.open(g / n).convert("RGB"), box, "user screenshot · " + c, label_size=40)
        for box, (n, c) in zip(grid(3, 3, top=930, bottom=1440), shots):
            tile(im, d, Image.open(g / n).convert("RGB").crop(rows[n]), box, "crop of the same screenshot (top rows)", label_size=36)
        panel(d, (X0, 1490, 3630, 1880), "Update GPU Particles (the process step) against the budget",
              ["Effect A: 0.14 ms ≤ 0.25 ms budget   (predicted 0.05)",
               "Effect B: 0.09 ms ≤ 0.15 ms budget   (predicted 0.06; budget set for 4 pits, 3 measured)",
               "Not measured: the draw step, multi-frame averages, vsync-off FPS. Taken before Effect A r1 (Puff 1.0, a draw-step change); not re-priced."], size=42)
        still("B32", [im], [g / n for n, _ in shots])
    elif key == "B33":
        head = subprocess.run(["git", "-C", str(GAME), "log", "-1", "--format=%H"], capture_output=True, text=True).stdout.strip()
        im, d = base("Who Did What, And What Was Filmed", "Sources: FRICTIONAL.md (“Who did what”), SOURCES.md, git log. Working-tree notes: gamedev-evidence.json source_revision.")
        panel(d, (X0, 330, 1880, 1450), "Agent (Claude Code + delegated sessions)",
              ["Brief and revisions, every prediction and strip reading, reviews, fixtures, documents, commits.",
               "Effect scenes, tests, previews, wiring and cost script: delegated agent sessions — the claude CLI is not installed, so steps ran as delegated sessions given the prompt verbatim."], size=56)
        panel(d, (1980, 330, 3630, 1450), "User",
              ["Chose both effects and the upload scope.", "Every runtime verdict and tuning decision.",
               "The editor conversion of the process shader.", "The Visual Profiler GPU readings."], size=60)
        panel(d, (X0, 1520, 3630, 1880), "Textures · revision",
              ["No textures sourced: GradientTexture2D/1D and CurveTexture are written inside the scene files.",
               "Filmed from git commit " + head + " (plus working-tree hashes in the ledger)."], size=50)
        MANIFEST.setdefault("_", {})["filmed_commit"] = head
        still("B33", [im], [GAME / "FRICTIONAL.md", GAME / "SOURCES.md"])
    elif key == "B13b":
        im, d = base("r0 → r1: The Puff Grows Inside The Body", FIX + "captures/hit_spark/r0-snow/ and r1-snow/, crop 560–720 × 300–420 enlarged 4×. Measurements and verdict: TUNING.md (Claude's measurement; user quote translated from Chinese).")
        for row, r in enumerate(("r0-snow", "r1-snow")):
            top = 330 + row * 770
            for box, n in zip(grid(3, 3, top=top, bottom=top + 720, right=2480), (12, 15, 20)):
                tile(im, d, crop(frame(f"hit_spark/{r}", n), HS, 4), box, f"{r} · frame {n}", label_size=40)
        panel(d, (2560, 330, 3630, 1860), "Puff quad 0.5 → 1.0",
              ["Predicted: snow below the body ≤ 150 on frames 15 and 20.",
               "Measured: 158.3 on every frame in r0-snow and r1-snow — MISS.",
               "Changed: only 621–661 × 340–376, the stand-in's body: a larger, darker haze.",
               "City: ≤ 3 levels in the patch, as predicted.",
               "User, running preview: “Keep.”"], size=50)
        still("B13b", [im], [CAP / "hit_spark/r0-snow", CAP / "hit_spark/r1-snow"])
    else:
        raise SystemExit("no media for " + key)


if __name__ == "__main__":
    keys = sys.argv[1:] or [k for k in BEAT if BEAT[k]["shot"].get("evidence_media")]
    for k in keys:
        build(k)
        manifest_path.write_text(json.dumps(MANIFEST, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
