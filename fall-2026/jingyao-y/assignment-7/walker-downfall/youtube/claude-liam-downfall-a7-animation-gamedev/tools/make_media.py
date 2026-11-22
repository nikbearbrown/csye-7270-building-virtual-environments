"""Build the A7 film's evidence clips from real engine output (no redrawn frames).

Stills: actual capture PNGs, the actual sheet and rig parts, and verbatim log
lines laid out on a 3840x2160 board; enlargements are nearest-neighbour and
labelled. Motion: Movie Maker PNG sequences at their recorded 30 fps (never
retimed); a take shorter than its beat is replayed, labelled REPLAY on screen.

    python tools/make_media.py [KEY ...]
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


def onpaper(path):
    p = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", p.size, (250, 249, 245, 255)); bg.alpha_composite(p)
    return bg.convert("RGB")


def r0(n):
    return Image.open(CAP / "wave_release/r0" / f"frame{n:08d}.png").convert("RGB")


def newframe(take, n):
    return Image.open(NEW / take / f"frame{n:08d}.png").convert("RGB")


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
    return (px, y0, px + pic.width, y0 + pic.height)


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
    OUT.mkdir(exist_ok=True)
    IMG.mkdir(exist_ok=True)
    bid = BEAT[key]["beat_id"]
    total = dur(key)
    parts = []
    for i, im in enumerate(boards):
        path = IMG / f"{bid}-{i}.png"
        im.save(path)
        part = OUT / f"_{bid}_{i}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", str(path), "-t", f"{total / len(boards):.6f}",
             "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(part)])
        parts.append(part)
    listing = OUT / f"_{bid}.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(OUT / f"{bid}.mp4")])
    for p in parts:
        p.unlink()
    listing.unlink()
    print("built", bid, flush=True)
    MANIFEST[bid] = {"film_key": key, "kind": "still boards (held, equal shares)", "duration": total,
                     "sources": [str(Path(s).relative_to(GAME)) if str(s).startswith(str(GAME)) else str(s) for s in sources], "boards": len(boards)}


def motion(key, take, title, side, zoom_box, provenance, start=0, end=None):
    """take: folder under capture/. Full frame 2x nearest + zoom crop."""
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
    bg = IMG / f"{bid}-bg.png"
    im.save(bg)
    raw = NEW / take / f"take_{start}_{end}.mp4"
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


def log_lines(rel, needles, base_dir=GAME):
    text = (base_dir / rel).read_text(encoding="utf-8", errors="replace").splitlines()
    out = []
    for n in needles:
        hit = next((l.strip() for l in text if n in l), None)
        assert hit is not None, (rel, n)
        out.append(hit)
    return out


FIX = "FIXTURE capture (preview scene, not human play) · Godot 4.7.2 Movie Maker, 30 fps, RTX 4060 Laptop, D3D12 Forward+ · "
RB = (560, 300, 720, 420)  # r0 crop around Lappland and the stand-in (TUNING.md frames)
NPC = json.loads((REEL / "capture/npc_ranges.json").read_text(encoding="utf-8")) if (REEL / "capture/npc_ranges.json").exists() else {}


def build(key):
    if key == "B02":
        im, d = base("Two Clips, Two Routes", "Source: CHANGE-BRIEF.md (The two clips), animations/*.tscn, README.md. Images: the actual sheet art/characters/npc/npc_closure_idle.png and rig parts animations/lappland_rig/*.png, enlarged (nearest neighbour).")
        panel(d, (X0, 330, 1880, 1300), "npc_idle — the cycle (loops)",
              ["Route: Sprite3D + AnimationPlayer frame track", "Node: NpcIdle in animations/npc_idle.tscn, instanced by FieldArt.npc_idle",
               "12 fps · keys 0/4/8/12 → cells 0–3 · LOOP_LINEAR", "One writer: its own AnimationPlayer (autoplay)"], size=58)
        panel(d, (1960, 330, 3630, 1300), "wave_release — the committing action",
              ["Route: 2D cutout rig keyed as resource text, in a SubViewport drawn by a Sprite3D billboard",
               "Node: WaveRig in animations/lappland_wave_rig.tscn, a child of the Player",
               "30 fps · startup 6 / active 4 / recovery 10 · LOOP_NONE", "Driven by the player's wave state machine (entities/player.gd)"], size=58)
        tile(im, d, onpaper(GAME / "art/characters/npc/npc_closure_idle.png"), (X0, 1360, 1880, 1820), "the NPC sheet: 4 cells of 64×64", 40)
        parts = Image.new("RGB", (192, 64), (250, 249, 245))
        for i, n in enumerate(("body", "blade_front", "blade_back")):
            p = Image.open(GAME / f"animations/lappland_rig/{n}.png").convert("RGBA")
            parts.paste(p, (i * 64, 0), p)
        tile(im, d, parts, (1960, 1360, 3630, 1820), "rig parts: body · front blade · back blade (64×64 each)", 40)
        still("B02", [im], [GAME / "art/characters/npc/npc_closure_idle.png", GAME / "animations/lappland_rig"])
    elif key == "B04":
        a, b = NPC["base"]
        motion("B04", "npc_in_game", "The Loop In The Running Game",
               ["previews/npc_idle_in_game.tscn (fixture: the player is placed for framing)", "Closure at the base store",
                "Clip npc_idle: one cell per 10 capture frames (1/3 s)", "The wrap 3 → 0 takes one interval, like every step",
                "User, in the game: “All fine”"], NPC["base_zoom"], FIX + f"capture/npc_in_game/ frames {a}–{b} (new).", a, b)
    elif key == "B06":
        im, d = base("The Slicing Names The Cell", "The actual sheet art/characters/npc/npc_closure_idle.png (256×64) enlarged 6× with its cell numbers; capture frames from capture/npc_in_game (FIXTURE), crop enlarged 4× (nearest neighbour); one frame per cell change (every 10 frames, measured).")
        sh = Image.open(GAME / "art/characters/npc/npc_closure_idle.png").convert("RGBA")
        bgc = Image.new("RGBA", sh.size, (226, 222, 212, 255)); bgc.alpha_composite(sh)
        big = bgc.convert("RGB").resize((256 * 6, 64 * 6), Image.Resampling.NEAREST)
        dd = ImageDraw.Draw(big)
        for c in range(4):
            dd.rectangle((c * 384, 0, c * 384 + 383, 383), outline=ACCENT, width=6)
            dd.text((c * 384 + 18, 10), str(c), font=font(SANSB, 70), fill=ACCENT)
        tile(im, d, big, (X0, 330, 2300, 1000), "hframes 4 × vframes 1 → frame 0, 1, 2, 3", 46)
        panel(d, (2400, 330, 3630, 1000), "Keys → cells", ["t 0.000 s → 0", "t 0.333 s → 1", "t 0.667 s → 2", "t 1.000 s → 3", "length 1.333 s, LOOP_LINEAR"], size=48, mono=True)
        z = NPC["base_zoom"]
        for box, (n, c) in zip(grid(4, 4, top=1080, bottom=1840), NPC["cells"]):
            tile(im, d, crop(newframe("npc_in_game", n), z, 4), box, f"capture frame {n} · {c}", 40)
        still("B06", [im], [GAME / "art/characters/npc/npc_closure_idle.png", NEW / "npc_in_game"])
    elif key == "B08":
        im, d = base("Mutations: Each Fails Its Test", "Recorded output, verbatim from logs/a7_mutations/ (scripts/a7_mutations.sh: each mutation in its own sparse git worktree, imported from an empty cache).")
        m = GAME / "logs/a7_mutations"
        panel(d, (X0, 330, 3630, 1860), "logs/a7_mutations",
              ["m1  ArmFront:rotation → ArmFront:rotaton (wave_release only)",
               log_lines("logs/a7_mutations/m1.test_wave_rig_readback.log", ["track_problems is empty"])[0],
               log_lines("logs/a7_mutations/summary.txt", ["m1 test_wave_rig_readback"])[0],
               "m2  npc_idle loop_mode → LOOP_NONE",
               log_lines("logs/a7_mutations/m2.test_npc_idle_readback.log", ["FAIL  loop_mode"])[0],
               "m3  npc_idle key 3 → 4 (= hframes × vframes)",
               log_lines("logs/a7_mutations/m3.test_npc_idle_readback.log", ["key 3 value inside the sheet"])[0],
               "m4  empty cache, --import, no mutation (the rig is keyed, not imported)",
               log_lines("logs/a7_mutations/summary.txt", ["m4 test_wave_rig_readback"])[0] + " · " + log_lines("logs/a7_mutations/summary.txt", ["m4 test_npc_idle_readback"])[0]],
              size=46, mono=True)
        still("B08", [im], [m])
    elif key == "B10":
        a, b = NPC["field"]
        motion("B10", "npc_in_game", "One Writer: The Squad Breathes Out Of Step",
               ["previews/npc_idle_in_game.tscn (fixture: player placed beside the set piece)", "Seed-1729 Chernobog mine floor, Rhodes Island squad",
                "Each figure: one seek of its own clip, then only its AnimationPlayer writes frame",
                "Structure test S7: " + log_lines("logs/test_wave_state_machine_60fps.log", ["S7 squad phases"])[0][3:]],
               NPC["field_zoom"], FIX + f"capture/npc_in_game/ frames {a}–{b} (new).", a, b)
    elif key == "B12":
        im, d = base("The Sprite Gives Way To The Rig", "The user's FIXTURE capture captures/wave_release/r0/ (crop enlarged 6×, nearest neighbour). Log lines verbatim from this film's scripted-input capture capture/wave_dodges/capture.log (take 1).")
        for box, (n, c) in zip(grid(4, 4, bottom=1250), ((27, "27 · click · sprite"), (29, "29 · STARTUP · rig"), (49, "49 · RECOVERY · rig"), (50, "50 · READY · sprite"))):
            tile(im, d, crop(r0(n), RB, 6), box, c, 42)
        lg = (NEW / "wave_dodges/capture.log").read_text(encoding="utf-8").splitlines()
        pick = [l for l in lg if l.startswith("FILM frame ") and int(l.split()[2]) in (28, 29, 49, 50)]
        panel(d, (X0, 1320, 3630, 1860), "capture/wave_dodges/capture.log (take 1)", [p.replace(" phase watch", "").replace(" phase rest", "") for p in pick], size=38, mono=True)
        still("B12", [im], [CAP / "wave_release/r0", NEW / "wave_dodges/capture.log"])
    elif key == "B14":
        im, d = base("Two Clocks Measured", "Recorded output, verbatim from logs/test_wave_state_machine_60fps.log (headless, --fixed-fps 60, real input via Input.parse_input_event).")
        L = "logs/test_wave_state_machine_60fps.log"
        panel(d, (X0, 330, 3630, 1700), "Per-tick record, both rates",
              log_lines(L, ["[r=1] r=1.0000", "[r=1] D4 STARTUP>ACTIVE", "[r=1] D4 RECOVERY>READY", "[r=1] D4 every wave tick",
                            "D10a attack speed", "[r=1.50] r=1.5000", "[r=1.50] D4 every wave tick"]), size=46, mono=True)
        d.text((X0, 1760), "npc_idle: ANIMATION_CALLBACK_MODE_PROCESS_IDLE (process tick) — no gameplay reads it.", font=font(SANS, 50), fill=INK)
        still("B14", [im], [GAME / L])
    elif key == "B16":
        motion("B16", "rig_turntable", "The Rig Alone, Frame By Frame",
               ["previews/wave_rig_turntable.tscn (fixture: grey plane)", "wave_release from capture frame 10, advanced 1/30 s per frame",
                "Frames 10–15 startup · 16–19 active · 20–29 recovery · 30 end", "Parts cut unchanged from lappland_combat_64.png row west, column 10"],
               (520, 230, 760, 470), FIX + "capture/rig_turntable/ (new).", 0, 45)
    elif key == "B18":
        im, d = base("Strip r0, Read At Each Boundary", "The user's FIXTURE capture captures/wave_release/r0/ (previews/wave_release_preview.tscn, run by the user), crop enlarged 4×. Verdict quoted verbatim from TUNING.md.")
        lab = [(29, "29 · first STARTUP"), (36, "36 · f5, last STARTUP"), (37, "37 · f6, ACTIVE: wave leaves"),
               (40, "40 · f9, last ACTIVE"), (41, "41 · f10, RECOVERY"), (50, "50 · READY")]
        for box, (n, c) in zip(grid(6, 3, right=2560, bottom=1500), lab):
            tile(im, d, crop(r0(n), RB, 4), box, c, 40)
        panel(d, (2640, 330, 3630, 1500), "Phase table (30 fps)", ["Startup 6 frames (+2 hitstop)", "Active 4 frames", "Recovery 10 frames", "Keys: 0 · 0.2 · 0.333 · 0.667 s"], size=48)
        panel(d, (X0, 1560, 3630, 1880), "The user (TUNING.md)", ["“I saw the record. everything is nice, we did a good job.” — then — “Keep r0, no revision”"], size=50)
        still("B18", [im], [CAP / "wave_release/r0", GAME / "TUNING.md"])
    elif key == "B20":
        motion("B20", "wave_dodges", "A Dodge In Each Phase",
               ["SCRIPTED-INPUT (previews/film_wave_dodges.tscn): real click and dash events",
                "T1 (26): full release", "T2 (114): dodge in STARTUP — no wave, charge kept", "T3 (202): dodge on 1st ACTIVE frame — wave out",
                "T4 (290): dodge in RECOVERY — cut short", "Between: ground click back; charge refilled (fixture)"],
               (576, 292, 736, 412), FIX.replace("preview scene", "film fixture") + "capture/wave_dodges/ (new).", 20, 380)
    elif key == "B21":
        im, d = base("What The Tests Proved", "Recorded output, verbatim from logs/ (headless, --fixed-fps 60, Godot 4.7.2). TEST-REPORT.md has the full account.")
        panel(d, (X0, 330, 1960, 1860), "A7 suites",
              ["npc_idle read-back: " + log_lines("logs/test_npc_idle_readback_60fps.log", ["test_npc_idle_readback:"])[0].split(": ")[1] + " (55 checks)",
               "rig read-back: " + log_lines("logs/test_wave_rig_readback_60fps.log", ["test_wave_rig_readback:"])[0].split(": ")[1] + " (136 checks)",
               log_lines("logs/test_a7_pins_after_step3_60fps.log", ["A7_PINS"])[0] + "  (after wiring)",
               log_lines("logs/test_a7_pins_60fps.log", ["A7_PINS"])[0] + "  (re-pinned)",
               log_lines("logs/test_wave_state_machine_60fps.log", ["TEST_WAVE_STATE_MACHINE"])[0],
               log_lines("logs/test_wave_edges_60fps.log", ["TEST_WAVE_EDGES"])[0]], size=54, mono=True)
        panel(d, (2040, 330, 3630, 1860), "Whole suite · limits",
              ["Before: " + log_lines("logs/baseline-before/summary.txt", ["of 103 pass"])[0],
               "After: " + log_lines("logs/baseline-after/summary.txt", ["of 108 pass"])[0],
               "Headless draws nothing: not the motion, the seam, the swap, the facing, the background.",
               "Untested: death, stuns, operator swap, leaving mid-release; edges at r > 1."], size=64)
        still("B21", [im], [GAME / "logs"])
    elif key == "B22":
        head = subprocess.run(["git", "-C", str(GAME), "log", "-1", "--format=%h"], capture_output=True, text=True).stdout.strip()
        im, d = base("Human Checks, And Who Did What", "Sources: evidence/a7/human-checks.md (the user's words; Chinese replies translated by the agent), TUNING.md, FRICTIONAL.md, SOURCES.md, animations/ATTRIBUTION.md, git log.")
        panel(d, (X0, 330, 1960, 1500), "The user's checks",
              ["NPC loop in the game: “All fine”", "Release in play: “Reads well”",
               "Interrupts (translated): “I tried interrupting it during all combat states, during item searching, and while standing still; pass.”",
               "Contrast (translated): “The light/dark contrast is clear; pass.”"], size=56)
        panel(d, (2040, 330, 3630, 1500), "Who did what",
              ["Claude (agent): the brief and revisions, predictions, reviews, previews, records, commits.",
               "Delegated agent sessions: the clips, the state machine, the tests, the re-pin (the claude CLI is not installed).",
               "The user: every choice and verdict; ran the r0 capture; kept r0."], size=56)
        panel(d, (X0, 1560, 3630, 1880), "Source · revision",
              ["Art: fan art generated with gpt sol 6.1 (terms, date and prompts not supplied by the user).",
               f"Filmed at commit {head}; game source unchanged since 45cf5845 (TEST-REPORT.md)."], size=46)
        MANIFEST.setdefault("_", {})["filmed_commit"] = head
        still("B22", [im], [GAME / "evidence/a7/human-checks.md", GAME / "FRICTIONAL.md", GAME / "SOURCES.md"])
    else:
        raise SystemExit("no media for " + key)


if __name__ == "__main__":
    keys = sys.argv[1:] or [k for k in BEAT if BEAT[k]["shot"].get("evidence_media")]
    for k in keys:
        build(k)
        manifest_path.write_text(json.dumps(MANIFEST, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
