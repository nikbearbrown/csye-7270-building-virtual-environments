#!/usr/bin/env python3
"""Compose the film's still evidence cards from real files, and copy the ones
the Remotion scenes read into the toolkit's public/ folder.

Every picture here is an existing engine capture (the committed frame strips in
captures/, Codex's Use It captures in evidence/use-it-code/, the film's own
Movie Maker capture in capture/), or a recorded log; this script only crops,
scales, places and labels. Strip crops are enlarged with nearest-neighbour, so
no pixel is blended. Code lines, log lines and the brief's sentences are read
from the files, not retyped; the numbers quoted from TUNING.md are asserted to
be in it.

    python3 tools/make_stills.py        # from the reel folder
"""
import re, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
A6 = REEL.parents[1]                        # fall-2026/shuai-z/assignment-6
ART = Path("/Users/eric/csye7270/brutalist.art")
FONTS = ART / "runtime/fonts"
PUBLIC = ART / "runtime/remotion/public/reels" / REEL.name
OUT = REEL / "stills"
USE = A6 / "evidence/use-it-code"
W, H = 3840, 2160
CREAM, INK, MUTED, ACCENT = (250, 249, 245), (61, 57, 41), (110, 100, 86), (217, 119, 87)
RED, GREEN, LINE = (164, 74, 50), (48, 110, 70), (214, 207, 194)
DARK, DTEXT, DMUTED = (32, 37, 49), (237, 241, 247), (190, 200, 215)
DBLUE, DGREEN, DYELLOW, DRED = (139, 199, 243), (174, 231, 209), (236, 224, 161), (255, 150, 130)
TUNING = (A6 / "TUNING.md").read_text()
BRIEF = (A6 / "CHANGE-BRIEF.md").read_text()

SPARK_BOX = (560, 410, 890, 600)            # window px of the 1280 × 720 strip frames: the hitbox at (673, 509) and the spray
DUST_BOX = (400, 455, 720, 575)             # behind his boots: the walk line is at y ≈ 560


def font(name, size):
    paths = {"sans": FONTS / "Inter/static/Inter_28pt-Regular.ttf", "bold": FONTS / "Inter/static/Inter_28pt-Medium.ttf",
             "mono": FONTS / "PT_Mono/PTMono-Regular.ttf", "cjk": Path("/System/Library/Fonts/Hiragino Sans GB.ttc")}
    return ImageFont.truetype(str(paths[name]), size)


CJK = re.compile(r"([\u3000-\u9fff\uff00-\uffef]+)")


def mtext(d, xy, text, f, fill):
    """Text that may hold the user's Chinese words: CJK runs in Hiragino Sans GB (macOS), the rest in f."""
    x, y = xy
    for run in CJK.split(text):
        if not run:
            continue
        ff = font("cjk", f.size) if CJK.fullmatch(run) else f
        d.text((x, y + (round(f.size * 0.04) if ff is not f else 0)), run, font=ff, fill=fill)
        x += d.textlength(run, font=ff)


def scaled(img, k, nearest=False):
    return img.resize((round(img.width * k), round(img.height * k)), Image.NEAREST if nearest else Image.LANCZOS)


def lines(path, a, b):
    return (A6 / path).read_text().splitlines()[a - 1:b]


def log(path):
    return (A6 / path).read_text().splitlines()


def tuning(*phrases):
    """Every number a card quotes from TUNING.md must be written there."""
    for p in phrases:
        assert p in TUNING, f"not in TUNING.md: {p!r}"


def frame_of(mp4, n):
    """One frame of a capture, decoded from the hashed MP4."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(REEL / mp4), "-vf", f"select=eq(n\\,{n})", "-vframes", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (W, H), raw)


def strip(effect, rnd, frame, box, k):
    im = Image.open(A6 / f"captures/{effect}/{rnd}/frame{frame:08d}.png").convert("RGB").crop(box)
    return scaled(im, k, nearest=True)


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
        d.text((x + size * 2.6, y), ln.replace("\t", "  ").strip() if len(ln) > 90 else ln.replace("\t", "  "),
               font=font("mono", size), fill=(186, 197, 188) if ln.lstrip().startswith("//") else DTEXT)
        y += round(size * 1.42)
    return y


def wrap(d, text, f, width):
    words, rows, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textbbox((0, 0), t, font=f)[2] > width and cur:
            rows.append(cur); cur = w
        else:
            cur = t
    rows.append(cur)
    return rows


def para(d, x, y, text, f, width, fill, gap=1.38):
    for r in wrap(d, text, f, width):
        d.text((x, y), r, font=f, fill=fill)
        y += round(f.size * gap)
    return y


# ── B02 ─────────────────────────────────────────────────────────────────────
GAME_FRAMES = {"sparks": 281, "dust": 90}   # set from capture/play-01-run.log: two bursts alive; running with the trail


def game_card():
    a = frame_of("capture/play-01.mp4", GAME_FRAMES["sparks"]).crop((1100, 1050, 2900, 2010))   # around Rudy, 4K pixels
    b = frame_of("capture/play-01.mp4", GAME_FRAMES["dust"]).crop((850, 1050, 2650, 2010))
    k = 1640 / a.width
    a, b = scaled(a, k), scaled(b, k)
    c, d = card("Walker Rudy: Two Effects, Two Jobs")
    y = 290
    c.paste(a, (200, y)); c.paste(b, (W - 200 - b.width, y))
    for x, rows in ((200, [("Effect A · SlashSparks · a burst", "bold"), ("Job: where and when the cut can land", "sans"),
                           ("Event: the sword's hitbox goes live", "bold"), ("Shape.disabled true → false, once per swing", "sans"),
                           ("Retrigger: overlap · at most 2 alive", "sans")]),
                    (W - 200 - b.width, [("Effect B · RunDust · a trail", "bold"), ("Job: he is running, which way, where his feet are", "sans"),
                                         ("Condition: running on the ground, in control", "bold"), ("mode PLAY · is_on_floor() · |velocity.x| > 1", "sans"),
                                         ("Feature A doesn't use: damping", "sans")])):
        yy = y + a.height + 50
        for t, f in rows:
            d.text((x, yy), t, font=font(f, 56 if f == "bold" else 50), fill=INK if f == "bold" else MUTED)
            yy += 82
    foot(d, [f"Crops (1800 × 960 around Rudy) of frames {GAME_FRAMES['sparks']} and {GAME_FRAMES['dust']} of the film's own engine capture, capture/play-01.mp4: the real Main in Godot 4.7.2,",
             "GL Compatibility, Movie Maker at 3840 × 2160 and 30 fps, scripted input from a film-only driver on a copy; scaled 0.91×. The run log counts two bursts alive in the left frame."])
    return c


# ── B03 (figure) ────────────────────────────────────────────────────────────
def three_parts():
    S, G = "game/effects/slash_sparks.tscn", "game/shaders/particles_generated.gdshader"
    rows = [("EMISSION — how many, how often, how long", S, 108, "the node: 28 sparks, all at once (explosiveness 1.0), one shot"),
            ("PROCESS — how each one moves and changes", S, 79, "the ParticleProcessMaterial: 700 px/s² pulls every spark down"),
            ("", G, 311, "the same setting in the generated process shader: the GPU runs this per particle"),
            ("DRAW — what each one looks like", S, 109, "a 12 × 40 gradient streak with a dark rim, mix blending")]
    c = Image.new("RGB", (3300, 1260), CREAM)
    d = ImageDraw.Draw(c)
    y = 30
    for head, path, n, note in rows:
        if head:
            d.text((60, y), head, font=font("bold", 58), fill=INK); y += 84
        d.rounded_rectangle((60, y, 3240, y + 112), radius=14, fill=DARK)
        d.text((100, y + 26), f"{Path(path).name}:{n}", font=font("mono", 48), fill=DBLUE)
        d.text((1080, y + 26), lines(path, n, n)[0].strip(), font=font("mono", 48), fill=DTEXT)
        d.text((100, y + 128), note, font=font("sans", 44), fill=MUTED)
        y += 230
    return c


# ── B04, B11 (figures) ──────────────────────────────────────────────────────
def intent(section_head, next_head, title, phase_head, extra):
    text = BRIEF.splitlines()
    i = text.index(section_head)
    j = text.index(next_head, i)
    sec = text[i:j]
    k = next(n for n, l in enumerate(sec) if l.startswith("### The intent"))
    body = sec[k:]
    p = next(n for n, l in enumerate(body) if l.startswith(phase_head))
    items = []                                   # the phase bullets, and a sub-list after an indented lead-in line
    for l in body[p + 1:]:
        if l.startswith("- **"):
            break
        if l.startswith("  - "):
            items.append(("– " + re.sub(r"\*\*|`", "", l[4:]), 90))
        elif l.startswith("  ") and l.strip():
            items.append((re.sub(r"\*\*|`", "", l.strip()), 60))
    for size in range(64, 38, -2):               # the largest type that fits the figure
        c = Image.new("RGB", (3300, 1260), CREAM)
        d = ImageDraw.Draw(c)
        d.text((60, 20), title, font=font("bold", 50), fill=INK)
        y = 110
        for t, x in items:
            y = para(d, x, y, t, font("sans", size), 3240 - x, INK, 1.28) + 12
        y += 24
        d.text((60, y), "Summarised from the same section and the revisions (not verbatim):", font=font("bold", 44), fill=MUTED)
        y += 74
        for lab, t in extra:
            d.text((60, y), lab, font=font("bold", size - 4), fill=INK)
            y = para(d, 520, y, t, font("sans", size - 4), 2720, MUTED, 1.28) + 14
        if y < 1240:
            return c
    raise SystemExit(f"intent figure does not fit: {title}")


def intent_a():
    return intent("## 2. Effect A — sword-swing sparks (`SlashSparks`)", "## 3. Effect B — running dust trail (`RunDust`)",
                  "CHANGE-BRIEF.md §2 · Effect A · The intent — timing phases, verbatim (revision 1)", "- **Timing phases**",
                  [("Contrast", "yellow is 1.1:1 on the sky, 1.5:1 on the wheat, so every spark and the flash carry a rim in the art's line colour #290F0D (about 14:1 and 10:1)."),
                   ("Scale", "a flash about 64 px across, 0.4 of Rudy's 160 px; streaks 28–44 px long, up to about 190 px forward."),
                   ("Revision 3", "Sparks amount 14 → 28 after shuai-z's first look; two overlapping bursts peak at 58 particles.")])


def intent_b():
    return intent("## 3. Effect B — running dust trail (`RunDust`)", "## 4. Boundaries",
                  "CHANGE-BRIEF.md §3 · Effect B · The intent — timing phases, verbatim (revision 1)", "- **Timing phases**",
                  [("Contrast", "darker than the wheat: earth brown #7A6448, about 2.9:1 against the wheat (revision 1's assumption: opaque, over the wheat)."),
                   ("Scale", "puffs 11 → 37 px; a band about 280 px long, no taller than about 40 px, below his knees."),
                   ("Revision 4", "after three rounds: ramp #5C4A35 at α 1.0, amount 40, velocity 80/160; the band rises to about 55–60 px.")])


# ── B06 ─────────────────────────────────────────────────────────────────────
def strip_a_r0():
    tuning("The flash is about 49 px across", "About 9–10 yellow streaks 15–35 px out", "About 11 streaks spread over 20–70 px forward",
           "only 2 specks about 6 px long are left", "too sparse, too few", "感觉火花可以再多一些，现在太稀疏，太少了")
    c, d = card("Effect A · the First Strip, r0", "FIXTURE CAPTURE")
    cells = [(10, "trigger: flash 64 px, rim; sparks inside", "flash ≈ 49 px, already see-through; 6–8 streaks"),
             (12, "flash 1.2×, half faded; 14 streaks fanned", "no flash; 9–10 streaks in one flat clump"),
             (15, "no flash; streaks 40–70 px, bending down", "≈ 11 streaks over 20–70 px, already orange"),
             (20, "2nd flash + 6–10 orange sparks of the 1st", "2nd flash; only 2 specks of the 1st left"),
             (30, "1st gone; the 2nd burst's sparks falling", "2–3 specks by the grass"),
             (50, "background and Rudy only", "background and Rudy only")]
    kx = 2.8
    for i, (f, pred, saw) in enumerate(cells):
        im = strip("slash_sparks", "r0", f, SPARK_BOX, kx)
        x = 200 + (i % 3) * (im.width + 90)
        y = 270 + (i // 3) * (im.height + 200)
        c.paste(im, (x, y))
        d.text((x, y + im.height + 14), f"frame {f}", font=font("bold", 46), fill=INK)
        d.text((x + 250, y + im.height + 18), "brief: " + pred, font=font("sans", 36), fill=MUTED)
        d.text((x + 250, y + im.height + 70), "r0: " + saw, font=font("sans", 36), fill=INK)
    mtext(d, (200, 1700), "My verdict, before Claude read a frame: “too sparse, too few” [感觉火花可以再多一些，现在太稀疏，太少了]",
          font("bold", 50), RED)
    foot(d, ["Fixture: game/previews/slash_sparks_preview.tscn (Level 1 frozen, a still Rudy), Movie Maker 1280 × 720 at 30 fps, seeds 1 and 2, bursts on frames 10 and 20",
             "(captures/slash_sparks/r0/, b348f6d4). Crops enlarged 2.8× nearest. Predictions: CHANGE-BRIEF.md §6; readings: Claude's, TUNING.md r1 — a claim, not a check."])
    return c


# ── B08 ─────────────────────────────────────────────────────────────────────
def strip_a_r1():
    tuning("`Sparks` `amount` 14 → 28", "16–20 yellow streaks 15–35 px out", "About 14–18 streaks in the same place",
           "18–22 orange streaks", "About 20 orange streaks", "3–5 specks of the first burst", "About 8 specks of the first burst", "**kept**")
    c, d = card("Effect A · Tuning r1: amount 14 → 28", "FIXTURE CAPTURES")
    cols = [(12, "predicted 16–20 streaks", "≈ 14–18 · yes"), (15, "predicted 18–22, gaps halved", "≈ 20 · yes"),
            (20, "predicted 3–5 specks of burst 1", "≈ 8, higher · no")]
    k = 2.6
    for j, (f, pred, got) in enumerate(cols):
        a = strip("slash_sparks", "r0", f, SPARK_BOX, k)
        b = strip("slash_sparks", "r1", f, SPARK_BOX, k)
        x = 360 + j * (a.width + 80)
        c.paste(a, (x, 330)); c.paste(b, (x, 330 + a.height + 30))
        d.text((x, 270), f"frame {f}", font=font("bold", 46), fill=INK)
        yy = 330 + 2 * a.height + 50
        d.text((x, yy), pred, font=font("sans", 40), fill=MUTED)
        d.text((x, yy + 56), "r1: " + got, font=font("bold", 42), fill=GREEN if "yes" in got else RED)
    a_h = round((SPARK_BOX[3] - SPARK_BOX[1]) * k)
    d.text((200, 330 + a_h // 2 - 30), "r0", font=font("bold", 64), fill=INK)
    d.text((200, 360 + a_h + a_h // 2 - 30), "r1", font=font("bold", 64), fill=INK)
    d.text((200, 1560), "One setting, proposed by Claude, approved by me: Sparks amount 14 → 28. Speed, spread, size, colour and timing unchanged.",
           font=font("sans", 46), fill=INK)
    d.text((200, 1640), "My verdict after three plays at real speed: kept (no further reason given).", font=font("bold", 50), fill=GREEN)
    foot(d, ["Fixture captures of game/previews/slash_sparks_preview.tscn, the same seeds: captures/slash_sparks/r0/ and r1/ (b348f6d4, fed848b8). Crops enlarged 2.6×",
             "nearest. Prediction and comparison: Claude's, TUNING.md r1. Frame 20 kept more specks than predicted: lifetimes 0.27–0.45 s, not a doubling of r0."])
    return c


# ── B13 ─────────────────────────────────────────────────────────────────────
def strip_b_r0():
    tuning("| 13 | A line of 3–5 puffs about 55 px long", "596; 8; 26", "1,973; 136; 52", "2,168; 224; 49", "884; 45; 28",
           "我肉眼完全没看到尘土拖尾的效果")
    c, d = card("Effect B · the First Strip, r0", "FIXTURE CAPTURE")
    cells = [(10, "at most 1–2 faint puffs", "nothing found"), (13, "3–5 puffs, about 55 px", "8 px changed ≥ 20 levels"),
             (25, "a band about 280 px, dark at his boots", "136 px changed ≥ 20 levels"), (40, "the same band", "224 px changed ≥ 20 levels"),
             (46, "about 170 px, paler", "45 px changed ≥ 20 levels"), (56, "nothing", "nothing")]
    k = 3.2
    for i, (f, pred, got) in enumerate(cells):
        im = strip("run_dust", "r0", f, DUST_BOX, k)
        x = 200 + (i % 3) * (im.width + 66)
        y = 280 + (i // 3) * (im.height + 220)
        c.paste(im, (x, y))
        d.text((x, y + im.height + 14), f"frame {f}", font=font("bold", 46), fill=INK)
        d.text((x + 250, y + im.height + 18), "brief: " + pred, font=font("sans", 36), fill=MUTED)
        d.text((x + 250, y + im.height + 70), "r0: " + got, font=font("sans", 36), fill=INK)
    d.text((200, 1430), "How Claude measured what I could not see: the same preview rendered with RunDust hidden, in a scratch copy, and diffed",
           font=font("sans", 46), fill=INK)
    d.text((200, 1500), "frame by frame. At frame 25 the dust changes 136 of 921,600 pixels by 20 levels or more; the largest change is 52.",
           font=font("sans", 46), fill=INK)
    mtext(d, (200, 1610), "My verdict, before Claude read a frame: “I could not see the dust trail at all” [我肉眼完全没看到尘土拖尾的效果]",
          font("bold", 50), RED)
    d.text((200, 1690), "The brief's 2.9 : 1 assumed opaque dust over the wheat; the puffs are born in the green grass strip, at 0.75 opacity, soft-edged.",
           font=font("sans", 44), fill=MUTED)
    foot(d, ["Fixture: game/previews/run_dust_preview.tscn (Level 1 frozen; Rudy's sprite and the emitter move at 560 px/s from frame 10, stop at frame 40), Movie Maker",
             "1280 × 720 at 30 fps, seed 1 (captures/run_dust/r0/, c69523ca). Crops enlarged 3.2× nearest. Measurements: Claude's, TUNING.md B r1 (pixels changed; ≥ 20; largest)."])
    return c


# ── B14–B16 ─────────────────────────────────────────────────────────────────
def strip_b_round(before, after, title, change, frames, verdict, verdict_cn, verdict_colour, phrases, source, shown_cn=None):
    tuning(*phrases, verdict_cn)
    c, d = card(title, "FIXTURE CAPTURES")
    k = 3.0
    for j, (f, pred, got, ok) in enumerate(frames):
        a = strip("run_dust", before, f, DUST_BOX, k)
        b = strip("run_dust", after, f, DUST_BOX, k)
        x = 340 + j * (a.width + 70)
        c.paste(a, (x, 340)); c.paste(b, (x, 340 + a.height + 30))
        d.text((x, 275), f"frame {f}", font=font("bold", 46), fill=INK)
        yy = 340 + 2 * a.height + 50
        d.text((x, yy), pred, font=font("sans", 40), fill=MUTED)
        d.text((x, yy + 56), f"{after}: " + got, font=font("bold", 42), fill=GREEN if ok else RED)
    a_h = round((DUST_BOX[3] - DUST_BOX[1]) * k)
    d.text((200, 340 + a_h // 2 - 30), before, font=font("bold", 60), fill=INK)
    d.text((200, 370 + a_h + a_h // 2 - 30), after, font=font("bold", 60), fill=INK)
    d.text((200, 1330), change, font=font("sans", 46), fill=INK)
    d.text((200, 1440), f"My verdict after three plays at real speed: “{verdict}”", font=font("bold", 50), fill=verdict_colour)
    mtext(d, (200, 1520), shown_cn or f"[{verdict_cn}]", font("sans", 44), MUTED)
    foot(d, [f"Fixture captures of game/previews/run_dust_preview.tscn, seed 1: captures/run_dust/{before}/ and {after}/ ({source}). Crops enlarged 3× nearest.",
             "Predictions and measurements (pixels changed by ≥ 20 levels against a no-dust render; top in game px): Claude's, TUNING.md — claims, not checks."])
    return c


def strip_b_r1():
    return strip_b_round("r0", "r1", "Effect B · Tuning r1: a darker, opaque ramp",
        "One setting: color_ramp #7A6448 at α 0.75 → #5C4A35 at α 1.0 (Claude proposed, I approved). Size, speed, number and life unchanged.",
        [(13, "predicted 3–5 dark puffs, ~55 px", "2–3 smudges · partly", False),
         (25, "predicted ≥ 500 px ≥ 20; largest ≥ 90", "612 met; 87 missed", False),
         (46, "predicted a pale line ~90 px", "a patch ~40 px · partly", False)],
        "I can see it now, but there is still not enough dust, and it is not obvious enough", "现在能看到了，但我觉得尘土还不够多，还不够明显", RED,
        ["2,084; 612; 87", "at least 500 pixels changed by 20 levels or more", "625; 187; 51", "917; 152; 52"], "c69523ca, 0c45ac1e")


def strip_b_r2():
    return strip_b_round("r1", "r2", "Effect B · Tuning r2: amount 20 → 40",
        "One setting: amount 20 → 40, so puffs are born every 7 px and overlap into one band (Claude proposed, I approved).",
        [(13, "predicted one short dark streak", "~55 px streak · yes", True),
         (25, "predicted ≥ 1,000 px ≥ 20; largest ≥ 90", "1,054; 105 · both met", True),
         (46, "predicted a pale patch 40–70 px", "~35 px, darker · partly", False)],
        "the dust could rise at a steeper angle; right now it nearly all stays on the ground", "尘土扬起的角度还可以高一些，现在基本都只是在地面上", RED,
        ["2,940; 1,054; 105", "885; 356; 80", "1,581; 354; 109"], "0c45ac1e, ed46992c")


def strip_b_r3():
    return strip_b_round("r2", "r3", "Effect B · Tuning r3: initial velocity 40/90 → 80/160",
        "One setting: initial_velocity_min / _max doubled; damping unchanged, so each puff still slows to a hang, about twice as high.",
        [(13, "predicted top 30–35 px", "top 26 px · no", False),
         (25, "predicted top 50–62 px; ≥ 1,000 px", "58 px; 1,501 · both met", True),
         (46, "predicted top about 55 px", "top 48 px · partly", False)],
        "kept", "检查过了，没问题", GREEN,
        ["(1,501; 110; 58)", "(388; 106; 26)", "(548; 89; 48)", "**kept**", "I gave no further reason"], "ed46992c, 9a3d1c16",
        "No further reason given. Once Step 5 wired it into the game, I played it: “checked, no problem” [检查过了，没问题]")


# ── B22 ─────────────────────────────────────────────────────────────────────
def shader_lines():
    G = "game/shaders/particles_generated.gdshader"
    c, d = card("Two Lines of the Generated Process Shader", "TWO ANNOTATED LINES")
    d.rounded_rectangle((200, 280, 3640, 1060), radius=20, fill=DARK)
    d.text((250, 305), "Generated by Godot 4.7.2's editor from a copy of Sparks' ParticleProcessMaterial, by shuai-z (8b795772); the game does not use it",
           font=font("bold", 40), fill=DMUTED)
    d.text((250, 380), G, font=font("mono", 40), fill=DBLUE)
    y = 450
    def row(n, hl=False):
        nonlocal y
        if hl:
            d.rectangle((234, y - 6, 3606, y + 52), fill=(69, 90, 113))
        d.text((250, y), f"{n:>3}", font=font("mono", 38), fill=(120, 130, 145))
        d.text((370, y), lines(G, n, n)[0].strip(), font=font("mono", 42), fill=DTEXT)
        y += 62
    for n in (10, 11, 43):
        row(n)
    y += 40
    row(139, True)
    d.text((370, y), "↳ each particle's speed, picked at random between the two uniforms  ←  the brief: 260 / 420 px/s", font=font("sans", 44), fill=DYELLOW)
    y += 110
    row(311, True)
    d.text((370, y), "↳ the force starts from the gravity uniform; line 324 adds force × DELTA to the velocity  ←  the brief: (0, 700, 0) px/s²",
           font=font("sans", 44), fill=DYELLOW)
    brief = BRIEF.splitlines()
    vel = next(l for l in brief if l.startswith("| `initial_velocity_min` / `_max` | 0 / 0 |"))
    grav = next(l for l in brief if l.startswith("| `gravity` | (0, 0, 0) | (0, 700, 0)"))
    d.rounded_rectangle((200, 1120, 3640, 1440), radius=20, fill=(238, 233, 222))
    d.text((250, 1145), "CHANGE-BRIEF.md §2, the settings table — Flash | Sparks (verbatim rows)", font=font("bold", 42), fill=INK)
    d.text((250, 1220), vel.replace("`", ""), font=font("mono", 50), fill=INK)
    d.text((250, 1310), grav.replace("`", ""), font=font("mono", 50), fill=INK)
    d.text((200, 1520), "The numbers are not in the shader's text: they arrive as uniforms, from the material's parameters.", font=font("sans", 48), fill=INK)
    foot(d, ["Verbatim lines of game/shaders/particles_generated.gdshader (383 lines; leading spaces trimmed).",
             "Line references and reading: shuai-z, TEST-REPORT.md \"The process shader\"; Claude checked each line."])
    return c


# ── B24 ─────────────────────────────────────────────────────────────────────
def tests():
    c, d = card("What the Tests Proved", "HEADLESS TEST OUTPUT", dark=True)
    rows = [("test_slash_sparks_config.gd 60", "logs/test_slash_sparks_config_60fps.log", "108 checks: every setting of Flash and Sparks, Godot 4 names"),
            ("test_run_dust_config.gd 60", "logs/test_run_dust_config_60fps.log", "61 checks: every setting of RunDust, damping and the box shape"),
            ("test_slash_sparks_state.tscn 60", "logs/test_slash_sparks_state_60fps.log", "14 checks, real slash input: one burst per live edge, place, facing, overlap"),
            ("test_run_dust_state.tscn 60", "logs/test_run_dust_state_60fps.log", "14 checks, real move/jump/pause input: emitting follows the condition"),
            ("checks.tscn 60", "logs/checks_60fps.log", "the existing 141 checks, unchanged"),
            ("invulnerable_tint_checks.tscn 30 | 60 | 144", "logs/invulnerable_tint_checks_60fps.log", "the existing 15 checks at each rate, unchanged")]
    y = 280
    for cmd, path, what in rows:
        L = log(path)
        n = sum(1 for l in L if l.startswith("PASS") and "failure(s)" not in l)
        fails = sum(1 for l in L if l.startswith("FAIL"))
        d.text((200, y), "$ scripts/run-test.sh " + cmd, font=font("mono", 44), fill=DBLUE)
        d.text((2350, y), f"{n} PASS · {fails} FAIL", font=font("mono", 44), fill=DGREEN if not fails else DRED)
        d.text((260, y + 62), what, font=font("sans", 40), fill=DMUTED)
        y += 150
    L = log("logs/test_slash_sparks_state_60fps.log")
    for key in ("S7", "S8"):
        l = next(x for x in L if x.startswith(f"PASS  {key} "))
        d.text((200, y), (l[:132] + " …") if len(l) > 134 else l, font=font("mono", 38), fill=DTEXT); y += 58
    L = log("logs/test_run_dust_state_60fps.log")
    l = next(x for x in L if x.startswith("PASS  D11 "))
    d.text((200, y), (l[:132] + " …") if len(l) > 134 else l, font=font("mono", 38), fill=DTEXT)
    foot(d, ["Recorded headless output, Godot 4.7.2 --headless, through scripts/run-test.sh at a pinned --fixed-fps (the logs named above). The configuration tests",
             "read the loaded _min/_max values and scan the scene text for Godot 3 names. The state tests run the real Main and never call the driver."], dark=True)
    return c


# ── B25 ─────────────────────────────────────────────────────────────────────
def mutations():
    c, d = card("Can the Checks Fail? Eight Mutations", "HEADLESS TEST OUTPUT", dark=True)
    rows = [("A scene · initial_velocity_min → initial_velocity (a Godot 3 name)", "logs/mutation_godot3_name_60fps.log"),
            ("A scene · spread 30 → 45, the brief not", "logs/mutation_value_drift_60fps.log"),
            ("A driver · one reused burst, emitting = true again", "logs/mutation_driver_reuse_60fps.log"),
            ("A driver · Effects moved before Rudy: one tick late", "logs/mutation_driver_order_60fps.log"),
            ("B scene · damping_min → damping (a Godot 3 name)", "logs/mutation_dust_godot3_name_60fps.log"),
            ("B scene · spread 50 → 70, the brief not", "logs/mutation_dust_value_drift_60fps.log"),
            ("B driver · is_visible_in_tree() dropped", "logs/mutation_dust_visibility_60fps.log"),
            ("B driver · DustTrail moved after Effects", "logs/mutation_dust_tree_order_60fps.log")]
    y = 270
    for title, path in rows:
        L = log(path)
        fails = [l for l in L if l.startswith("FAIL") and "failure(s)" not in l]
        d.text((200, y), title, font=font("bold", 46), fill=DTEXT)
        d.text((2900, y), f"exit 1 · {len(fails)} FAIL", font=font("mono", 44), fill=DRED)
        l = fails[0]
        d.text((260, y + 62), (l[:140] + " …") if len(l) > 142 else l, font=font("mono", 34), fill=DRED)
        y += 158
    foot(d, ["Each mutation changed one line or node, ran through scripts/run-test.sh at 60 fps, and was restored (SHA-1 checked before and after). Scene mutations: Claude;",
             "driver mutations: the scoped implementation sessions, copied out of their transcripts. TEST-REPORT.md, Steps 2, 3 and 5."], dark=True)
    return c


# ── B26 ─────────────────────────────────────────────────────────────────────
def prices():
    c, d = card("Two Prices Against the Budget", "HEADLESS LOG + EDITOR CAPTURE")
    L = log("logs/cost_effects_60fps_rerun.log")
    def mean(label):
        l = next(x for x in L if x.strip().startswith(label) and "mean" in x)
        return re.search(r"mean ([\d.]+) ms", l)[1], re.search(r"round means ([\d.–]+) ms", l)[1]
    d.text((200, 270), "1 · Headless CPU price, ms per frame (game/tests/cost_effects.gd, --fixed-fps 60, 5 × 300 frames)", font=font("bold", 50), fill=INK)
    y = 360
    for lab, key in (("Empty scene (control)", "Empty scene"), ("Game, both effects off, idle", "Game, both effects off, Rudy idle"),
                     ("Game, both effects off, running", "Game, both effects off, Rudy running"),
                     ("Effect A, 2 bursts alive (58 particles)", "Effect A, 2 bursts alive"), ("Effect B, running, emitting (40)", "Effect B, Rudy running")):
        m, r = mean(key)
        d.text((260, y), lab, font=font("sans", 46), fill=INK)
        d.text((1400, y), f"{m}   (round means {r})", font=font("mono", 46), fill=INK)
        y += 70
    for l in L:
        if l.strip().startswith(("effect_a ", "effect_b ")) and "game_off" in l:
            d.text((260, y), l.strip(), font=font("mono", 40), fill=RED); y += 62
    d.text((200, y + 30), "Near zero by construction: the dummy renderer runs no particle process and draws nothing; only node bookkeeping is left.",
           font=font("sans", 44), fill=MUTED)
    shot = Image.open(USE / "02_A_heavy_editor.png").convert("RGB").crop((288, 715, 1422, 960))
    shot = scaled(shot, 1.55)
    y2 = 1170
    d.text((200, y2 - 75), "2 · GPU price: the editor's Visual Profiler (Codex's capture, A heaviest)", font=font("bold", 50), fill=INK)
    c.paste(shot, (200, y2))
    x = 200 + shot.width + 90
    d.text((x, y2), "Budget: 0.25 ms of GPU time per effect", font=font("bold", 48), fill=INK)
    d.text((x, y2 + 75), "GPU column: 0.0 ms in every row, all four states", font=font("sans", 44), fill=RED)
    d.text((x, y2 + 140), "— failure 12, predicted. Not a pass.", font=font("sans", 44), fill=RED)
    d.text((x, y2 + 230), "Fallback, vsync off (F9), Monitors FPS median:", font=font("bold", 44), fill=INK)
    d.text((x, y2 + 300), "A off 438 · A heaviest 239", font=font("mono", 46), fill=INK)
    d.text((x, y2 + 365), "B off 357 · B heaviest 311", font=font("mono", 46), fill=INK)
    d.text((x, y2 + 440), "FPS is not GPU time; the two idle", font=font("sans", 42), fill=MUTED)
    d.text((x, y2 + 495), "baselines alone differ by about 80.", font=font("sans", 42), fill=MUTED)
    foot(d, ["logs/cost_effects_60fps_rerun.log (Claude's rerun of the agent's script; its own run read +0.0079 and +0.0039). Editor: evidence/use-it-code/02_A_heavy_editor.png",
             "(half-size copy, crop enlarged 1.55×) and summary.json, recorded by Codex at shuai-z's request at d60fb037, Apple M3, GL Compatibility. TEST-REPORT.md, Use It."])
    return c


# ── B27 ─────────────────────────────────────────────────────────────────────
def headless_limits():
    c, d = card("What No Headless Run Can Show", "FIXTURE + ENGINE CAPTURES")
    k = 2.3
    a = strip("slash_sparks", "r1", 15, SPARK_BOX, k)
    b = strip("slash_sparks", "mutation_godot3_name", 15, SPARK_BOX, k)
    c.paste(a, (200, 300)); c.paste(b, (200 + a.width + 50, 300))
    d.text((200, 300 + a.height + 16), "r1, frame 15", font=font("bold", 44), fill=INK)
    d.text((250 + a.width, 300 + a.height + 16), "Godot 3 name mutation, frame 15", font=font("bold", 44), fill=INK)
    para(d, 200, 300 + a.height + 80, "Still a spray, with a few slow sparks near the flash. Nothing in the picture or the log announces it; only the configuration test does. (Fixture captures.)",
         font("sans", 42), 2 * a.width + 40, INK)
    crop = (210, 150, 450, 290)                 # around Rudy and his sparks, in the 640 × 360 copies
    p1 = Image.open(USE / "supplement/80_sparks_visible_paused_a.png").convert("RGB").crop(crop)
    p2 = Image.open(USE / "supplement/81_sparks_visible_paused_b.png").convert("RGB").crop(crop)
    k2 = 3.2
    p1, p2 = scaled(p1, k2, nearest=True), scaled(p2, k2, nearest=True)
    x0 = 200 + 2 * a.width + 160
    c.paste(p1, (x0, 300)); c.paste(p2, (x0, 300 + p1.height + 30))
    d.text((x0 + p1.width + 30, 330), "Paused, 0.7 s apart:", font=font("bold", 42), fill=INK)
    d.text((x0 + p1.width + 30, 390), "pixel-identical;", font=font("sans", 42), fill=INK)
    d.text((x0 + p1.width + 30, 445), "they change", font=font("sans", 42), fill=INK)
    d.text((x0 + p1.width + 30, 500), "on resume.", font=font("sans", 42), fill=INK)
    d.text((x0 + p1.width + 30, 580), "(Codex's engine", font=font("sans", 38), fill=MUTED)
    d.text((x0 + p1.width + 30, 630), "capture, half size)", font=font("sans", 38), fill=MUTED)
    y = 1320
    for t in ["Headless, the dummy renderer draws nothing and runs no particle process: a burst's 27-tick life is the node's clock, not the sparks.",
              "No test sees the sparks fly the way Rudy faces, the dust read against the wheat, a paused puff hold still, or an effect clip at a screen edge.",
              "Those were eyes: Codex's captures, and shuai-z's own play in the 1280 × 720 window — “大小和手感都没问题” (size and feel are fine)."]:
        mtext(d, (200, y), "· " + t, font("sans", 46), INK); y += 84
    foot(d, ["captures/slash_sparks/r1/ and mutation_godot3_name/ (fixture captures of the preview; logs/capture_mutation_godot3_name.log). evidence/use-it-code/supplement/80–81",
             "(pixel-identical in pixel-checks.json; crops of the half-size copies, enlarged 3.2× nearest). TEST-REPORT.md, Step 2 and Use It; CLAUDE.md, Headless facts."])
    return c


def main():
    OUT.mkdir(exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    figures = {"three-parts.png": three_parts(), "intent-a.png": intent_a(), "intent-b.png": intent_b()}
    for name, im in figures.items():
        im.save(OUT / name)
        shutil.copy(OUT / name, PUBLIC / name)
    for name, fn in [("game-card.png", game_card), ("strip-a-r0.png", strip_a_r0), ("strip-a-r1.png", strip_a_r1),
                     ("strip-b-r0.png", strip_b_r0), ("strip-b-r1.png", strip_b_r1), ("strip-b-r2.png", strip_b_r2),
                     ("strip-b-r3.png", strip_b_r3), ("shader-lines.png", shader_lines), ("tests.png", tests),
                     ("mutations.png", mutations), ("prices.png", prices), ("headless-limits.png", headless_limits)]:
        if name == "game-card.png" and not (REEL / "capture/play-01.mp4").exists():
            print("skip game-card.png: capture/play-01.mp4 not made yet"); continue
        fn().save(OUT / name)
    print(f"stills written to {OUT}; public copies of {len(figures)} figures in {PUBLIC}")


if __name__ == "__main__":
    main()
