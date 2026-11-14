"""Figures for the README and the film (Assignment 7), drawn from the committed logs with Pillow only.

Writes captures/figures/*.png (paths relative to assignment-7/):
  pin_timeline.png    hit_growl before (a9b4bc1) and after the growl cancel (logs/pin): wolf state lane, hitbox lane,
                      hit tick; the other pin scenarios marked changed / unchanged.
  growl_window.png    logs/probe_growl_cancel_60fps.log: 31 growl ticks, the fireball's travel per cast tick, the window.
  two_clocks.png      the wolf's removal tick at 30 / 60 / 144 fps (pin logs at 72e8d21, before the re-pin).
  lunge_onion.png     the seven key poses of the lunge, rendered from wolf_lunge.png with the rig values logged in
                      captures/lunge/game-r0/ticks_take_lunge.jsonl, overlaid; the captured frames; the phase table.
  run_cycle.png       r0 (two frames, mage_run_sheet.png) against r2 (four frames, mage_run_cycle_sheet.png) with the
                      measured ticks per frame (captures/run/game-r0, captures/run/game-r2-ticks).
Run from assignment-7/ with the ComfyUI venv (Pillow, NumPy):
    E:/7270/tools/ComfyUI/.venv/Scripts/python.exe walker-magic-zhefan/tools/make_figures.py
"""

import json
import math
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

A7 = Path(__file__).resolve().parents[2]
GAME = A7 / "walker-magic-zhefan"
OUT = A7 / "captures" / "figures"
BG, FG, DIM = (18, 19, 24), (232, 232, 236), (130, 132, 142)
STATE_COL = {"PATROL": (92, 104, 128), "GROWL": (214, 160, 48), "LUNGE": (214, 64, 52), "RECOVER": (72, 156, 112),
             "DEAD": (60, 60, 60), "FREED": (30, 30, 30)}


def font(size):
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size)


F, FS, FB = font(18), font(14), font(24)


def git_show(rev, rel):
    return subprocess.run(["git", "show", f"{rev}:./{rel}"], cwd=A7, capture_output=True, text=True, check=True).stdout


def runs(values):
    out = []
    for i, v in enumerate(values):
        if out and out[-1][0] == v:
            out[-1][2] += 1
        else:
            out.append([v, i, 1])
    return out


def legend(d, x, y, items):
    for name, col in items:
        d.rectangle([x, y + 3, x + 16, y + 17], fill=col)
        d.text((x + 22, y), name, font=FS, fill=FG)
        x += 30 + d.textlength(name, font=FS)


# ------------------------------------------------------------------ pin timeline
def pin_timeline():
    old = json.loads(git_show("a9b4bc1", "logs/pin/hit_growl.json"))["ticks"]
    new = json.loads((A7 / "logs/pin/hit_growl.json").read_text())["ticks"]
    n = len(new)
    S, X0 = 7, 170
    img = Image.new("RGB", (X0 + n * S + 40, 530), BG)
    d = ImageDraw.Draw(img)
    d.text((20, 14), "Pin: hit_growl before and after the growl cancel (player 680, wolf 800; one cast at tick 4)", font=FB, fill=FG)
    for row, (label, ticks) in enumerate((("before (a9b4bc1)", old), ("after (ff71bbb)", new))):
        y = 80 + row * 150
        d.text((20, y + 6), label, font=F, fill=FG)
        d.text((20, y + 46), "hitbox armed", font=FS, fill=DIM)
        for state, start, length in runs([t[4] for t in ticks]):
            d.rectangle([X0 + start * S, y, X0 + (start + length) * S - 1, y + 34], fill=STATE_COL[state])
            if length * S > 60:
                d.text((X0 + start * S + 4, y + 8), state, font=FS, fill=(0, 0, 0))
        for armed, start, length in runs([t[7] for t in ticks]):
            if armed:
                d.rectangle([X0 + start * S, y + 44, X0 + (start + length) * S - 1, y + 62], fill=(240, 220, 90))
        hits = [i for i in range(1, n) if ticks[i][6] < ticks[i - 1][6]]
        for h in hits:
            d.line([X0 + h * S, y - 8, X0 + h * S, y + 70], fill=(255, 255, 255), width=2)
            d.text((X0 + h * S + 4, y - 22), f"hit, tick {h}", font=FS, fill=FG)
    for t in range(0, n + 1, 10):
        d.line([X0 + t * S, 380, X0 + t * S, 386], fill=DIM)
        d.text((X0 + t * S - 8, 390), str(t), font=FS, fill=DIM)
    d.text((X0, 410), "physics tick", font=FS, fill=DIM)
    legend(d, 20, 440, [(s, STATE_COL[s]) for s in ("PATROL", "GROWL", "LUNGE", "RECOVER")] + [("hitbox monitoring", (240, 220, 90))])
    status = []
    for name in ("walk_right_stop", "jump", "cast", "take_lunge", "hit_growl", "hit_lunge", "hit_recover", "kill"):
        same = git_show("a9b4bc1", f"logs/pin/{name}.json") == (A7 / f"logs/pin/{name}.json").read_text() \
            or json.loads(git_show("a9b4bc1", f"logs/pin/{name}.json"))["ticks"] == json.loads((A7 / f"logs/pin/{name}.json").read_text())["ticks"]
        status.append(f"{name}: {'unchanged' if same else 'CHANGED'}")
    d.text((20, 470), "Pin scenarios after the change (re-pinned in ff71bbb):", font=FS, fill=FG)
    d.text((20, 492), "   ".join(status), font=FS, fill=FG)
    img.save(OUT / "pin_timeline.png")


# ------------------------------------------------------------------ growl window
def growl_window():
    lines = [json.loads(l) for l in (A7 / "logs/probe_growl_cancel_60fps.log").read_text().splitlines() if l.startswith("{")]
    dry = lines[0]["dry_run"]
    casts = lines[1:]
    g0 = dry["first_growl_tick"]
    S, X0, Y0 = 16, 120, 120
    img = Image.new("RGB", (X0 + 60 * S + 60, Y0 + len(casts) * 22 + 160), BG)
    d = ImageDraw.Draw(img)
    d.text((20, 14), "Growl window: a fireball cast from where the wolf first sees the mage (dx 118.75)", font=FB, fill=FG)
    d.text((20, 46), f"Wolf phases from its first growl tick ({g0}); each row is one real click, cast k ticks after the growl began.",
           font=FS, fill=DIM)
    for state, start, length in (("GROWL", 0, 31), ("LUNGE", 31, 22)):
        d.rectangle([X0 + start * S, Y0 - 34, X0 + (start + length) * S - 1, Y0 - 10], fill=STATE_COL[state])
        d.text((X0 + start * S + 6, Y0 - 32), f"{state} {length} ticks", font=FS, fill=(0, 0, 0))
    d.rectangle([X0, Y0 - 4, X0 + 12 * S, Y0 + len(casts) * 22], outline=(120, 220, 140), width=2)
    for i, c in enumerate(casts):
        y = Y0 + i * 22 + 4
        k, travel = c["cast_after_growl_start"], c["travel_ticks"]
        cancel = c["state_on_hit_tick"] == "RECOVER"
        col = (120, 220, 140) if cancel else (230, 110, 90)
        d.text((20, y - 2), f"cast +{k}", font=FS, fill=DIM)
        d.line([X0 + k * S, y + 7, X0 + (k + travel) * S, y + 7], fill=col, width=3)
        d.ellipse([X0 + k * S - 4, y + 3, X0 + k * S + 4, y + 11], fill=FG)
        d.ellipse([X0 + (k + travel) * S - 5, y + 2, X0 + (k + travel) * S + 5, y + 12], fill=col)
        d.text((X0 + (k + travel) * S + 10, y - 2), f"{travel} ticks -> {'cancel' if cancel else 'lunge continues'}", font=FS, fill=col)
    yb = Y0 + len(casts) * 22 + 20
    d.text((X0, yb), "The window: casts in the first 12 growl ticks (0.2 s) land during GROWL and cancel the lunge;", font=F, fill=(120, 220, 140))
    d.text((X0, yb + 26), "later casts arrive after tick 31 and meet a committed lunge. Travel from sight distance: 20 ticks (0.33 s).", font=F, fill=FG)
    img.save(OUT / "growl_window.png")


# ------------------------------------------------------------------ two clocks
def two_clocks():
    rows = []
    for fps in (30, 60, 144):
        log = git_show("72e8d21", f"logs/test_pin_behaviour_{fps}fps.log")
        obs = next(json.loads(l) for l in log.splitlines() if '"kill-phases"' in l)["observation"]["wolf"]
        dead = int(re.search(r"DEAD@(\d+)", " ".join(obs)).group(1))
        freed = int(re.search(r"FREED@(\d+)", " ".join(obs)).group(1))
        rows.append((fps, dead, freed))
    S, X0 = 22, 170
    t0, t1 = 38, 86
    img = Image.new("RGB", (X0 + (t1 - t0) * S + 80, 420), BG)
    d = ImageDraw.Draw(img)
    d.text((20, 14), "Two clocks: the wolf's removal after its death, measured in physics ticks", font=FB, fill=FG)
    d.text((20, 48), "Death and the clips run on the physics tick; the removal is a SceneTree timer on the process (frame) clock (wolf.gd).",
           font=FS, fill=DIM)
    for i, (fps, dead, freed) in enumerate(rows):
        y = 100 + i * 80
        d.text((20, y + 8), f"--fixed-fps {fps}", font=F, fill=FG)
        d.rectangle([X0 + (dead - t0) * S, y, X0 + (freed - t0) * S - 1, y + 34], fill=STATE_COL["DEAD"], outline=DIM)
        d.text((X0 + (dead - t0) * S + 6, y + 8), f"DEAD from tick {dead}: {freed - dead} ticks", font=FS, fill=FG)
        d.rectangle([X0 + (freed - t0) * S, y, X0 + (t1 - t0) * S, y + 34], fill=(30, 30, 30))
        d.line([X0 + (freed - t0) * S, y - 6, X0 + (freed - t0) * S, y + 40], fill=(255, 200, 80), width=3)
        d.text((X0 + (freed - t0) * S + 6, y + 40), f"removed at tick {freed}", font=FS, fill=(255, 200, 80))
        frame_ticks = 60 / fps
        k = 0
        while True:
            t = dead + k * frame_ticks
            if t > t1:
                break
            if t >= t0:
                d.line([X0 + (t - t0) * S, y + 34, X0 + (t - t0) * S, y + 38], fill=DIM)
            k += 1
    for t in range(t0, t1 + 1, 4):
        d.text((X0 + (t - t0) * S - 8, 345), str(t), font=FS, fill=DIM)
    d.text((X0, 370), "physics tick (small marks under each lane: process frames)", font=FS, fill=DIM)
    img.save(OUT / "two_clocks.png")


# ------------------------------------------------------------------ lunge onion skin
def render_pose(tex, row, scale=6):
    """The wolf's two rig parts at one logged pose, facing right, on a 200x80 canvas (feet at (100, 64))."""
    W, H, ox, oy = 200, 80, 100, 64
    canvas = Image.new("RGBA", (W * scale, H * scale), (0, 0, 0, 0))
    parts = [((0, 0, 40, 40), (-11, -22), (-29, -16), row["rear_deg"]),
             ((36, 0, 80, 40), (15, -22), (-19, -16), row["front_deg"])]
    sx, sy = row["rig_scale"]
    for region, pivot, offset, deg in parts:
        part = tex.crop(region)
        a = math.radians(deg)
        # local part pixel p -> world: rig_pos + S * (pivot + R(a) * (offset + p)), then canvas origin and display scale
        m00, m01 = sx * math.cos(a), -sx * math.sin(a)
        m10, m11 = sy * math.sin(a), sy * math.cos(a)
        tx = row["rig_x"] + sx * (pivot[0] + math.cos(a) * offset[0] - math.sin(a) * offset[1]) + ox
        ty = sy * (pivot[1] + math.sin(a) * offset[0] + math.cos(a) * offset[1]) + oy
        M = [[m00 * scale, m01 * scale, tx * scale], [m10 * scale, m11 * scale, ty * scale]]
        det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
        inv = [M[1][1] / det, -M[0][1] / det, (M[0][1] * M[1][2] - M[1][1] * M[0][2]) / det,
               -M[1][0] / det, M[0][0] / det, (M[1][0] * M[0][2] - M[0][0] * M[1][2]) / det]
        layer = part.transform(canvas.size, Image.AFFINE, inv, resample=Image.NEAREST)
        canvas.alpha_composite(layer)
    return canvas


def lunge_onion():
    rows = [json.loads(l) for l in (A7 / "captures/lunge/game-r0/ticks_take_lunge.jsonl").read_text().splitlines()]
    g0 = next(r["tick"] for r in rows if r["w_state"] == "GROWL")
    tex = Image.open(GAME / "assets/sprites/wolf/wolf_lunge.png").convert("RGBA")
    keys = [(0, "start: neutral", "GROWL entered"), (25, "crouch", "GROWL"), (31, "crouch held", "GROWL -> LUNGE"),
            (37, "stretch", "LUNGE"), (53, "stretch held", "LUNGE -> RECOVER"), (65, "overshoot", "RECOVER"),
            (89, "end: neutral (rig hidden, PATROL)", "RECOVER -> PATROL")]
    tint = {0: (200, 200, 210), 25: (214, 160, 48), 31: (214, 160, 48), 37: (214, 64, 52), 53: (214, 64, 52),
            65: (72, 156, 112), 89: (200, 200, 210)}
    scale = 6
    onion = Image.new("RGBA", (200 * scale, 80 * scale), BG + (255,))
    import numpy as np
    for k, _, _ in keys[:-1]:   # frame 89 is PATROL: the rig is hidden, nothing to draw
        if k in (31, 53):       # "held" keys repeat the previous pose exactly
            continue
        pose = np.asarray(render_pose(tex, rows[g0 + k], scale))
        solid = pose[..., 3] > 0
        inner = solid.copy()
        for dy, dx in ((scale, 0), (-scale, 0), (0, scale), (0, -scale)):
            inner &= np.roll(np.roll(solid, dy, 0), dx, 1)
        edge = solid & ~inner
        layer = np.zeros(pose.shape, dtype=np.uint8)
        layer[edge] = tint[k] + (255,)
        layer[inner] = tint[k] + (38,)
        onion.alpha_composite(Image.fromarray(layer, "RGBA"))
    strip_h = 200
    img = Image.new("RGB", (onion.width, 70 + onion.height + strip_h + 60 + 34 * (len(keys) + 1)), BG)
    d = ImageDraw.Draw(img)
    d.text((20, 14), "Lunge key poses: rig values logged in the real game (take_lunge, Movie Maker capture), overlaid", font=FB, fill=FG)
    d.text((20, 44), "Outlines: neutral (frame 0) grey, crouch (25) amber, stretch (37) red, overshoot (65) green; the held keys"
           " 31 and 53 repeat 25 and 37. Facing shown right.", font=FS, fill=DIM)
    img.paste(onion.convert("RGB"), (0, 70))
    y = 70 + onion.height + 10
    cw = onion.width // 7
    for i, (k, _, _) in enumerate(keys):
        fr = Image.open(A7 / f"captures/lunge/game-r0/take_lunge_g+{k:02d}.png").convert("RGB")
        x_w = 860 - (780 - 320)
        cx = x_w if k < 31 else int(x_w - min(k - 31, 22) * 220 / 60)
        crop = fr.crop((cx - 60, 268, cx + 60, 332)).resize((cw - 8, int((cw - 8) * 64 / 120)), Image.NEAREST)
        img.paste(crop, (i * cw + 4, y))
        d.text((i * cw + 8, y + crop.height + 4), f"g+{k}", font=FS, fill=FG)
    y += strip_h
    cols = [20, 140, 400, 700, 900]
    for x, h in zip(cols, ("frame", "phase / state", "pose at the key", "Rig scale, x", "Front / Rear")):
        d.text((x, y), h, font=F, fill=FG)
    for i, (k, pose, state) in enumerate(keys):
        r = rows[g0 + k]
        yy = y + 30 + i * 34
        d.text((cols[0], yy), f"{k}  ({k / 60:.4f} s)", font=FS, fill=FG)
        d.text((cols[1], yy), f"{state} [{r['w_state']}]", font=FS, fill=FG)
        d.text((cols[2], yy), pose, font=FS, fill=FG)
        d.text((cols[3], yy), f"({r['rig_scale'][0]:.2f}, {r['rig_scale'][1]:.2f}), {r['rig_x']:+.0f}", font=FS, fill=FG)
        d.text((cols[4], yy), f"{r['front_deg']:+.0f} / {r['rear_deg']:+.0f} deg" + ("" if r["rig_visible"] else "  (rig hidden)"), font=FS, fill=FG)
    img.save(OUT / "lunge_onion.png")


# ------------------------------------------------------------------ run cycle
def run_cycle():
    def ticks_per_frame(path):
        rows = [json.loads(l) for l in path.read_text().splitlines()]
        return [(f, n) for (clip, f), _, n in runs([(r["clip"], r["frame"]) for r in rows]) if clip == "run"]

    r0 = ticks_per_frame(A7 / "captures/run/game-r0/ticks.jsonl")
    r2 = ticks_per_frame(A7 / "captures/run/game-r2-ticks/ticks.jsonl")
    s0 = Image.open(GAME / "assets/sprites/mage/mage_run_sheet.png").convert("RGBA")
    s2 = Image.open(GAME / "assets/sprites/mage/mage_run_cycle_sheet.png").convert("RGBA")
    S = 4
    img = Image.new("RGB", (4 * 62 * S + 80, 2 * (69 * S + 150) + 80), BG)
    d = ImageDraw.Draw(img)
    d.text((20, 14), "Run cycle: r0 (two A2 frames, 8 fps) against r2 (four frames, 10 fps, kept after play)", font=FB, fill=FG)
    for row, (name, sheet, cells, seq, note) in enumerate((
            ("r0: contact, passing", s0, 2, r0, "0.25 s loop; measured ticks per frame"),
            ("r2: contact, down, passing, up", s2, 4, r2, "0.4 s loop; measured ticks per frame"))):
        y = 60 + row * (69 * S + 150)
        d.text((20, y), name, font=F, fill=FG)
        for c in range(cells):
            cell = sheet.crop((62 * c, 0, 62 * (c + 1), 69)).resize((62 * S, 69 * S), Image.NEAREST)
            plate = Image.new("RGBA", cell.size, (40, 42, 52, 255))
            plate.alpha_composite(cell)
            img.paste(plate.convert("RGB"), (20 + c * (62 * S + 10), y + 30))
            d.text((24 + c * (62 * S + 10), y + 34), f"frame {c}", font=FS, fill=(255, 255, 0))
        yt = y + 30 + 69 * S + 12
        x = 20
        for f, n in seq[:12]:
            col = [(214, 160, 48), (72, 156, 112), (90, 140, 214), (214, 64, 52)][f]
            d.rectangle([x, yt, x + n * 10 - 2, yt + 22], fill=col)
            d.text((x + 3, yt + 3), f"{f}:{n}", font=FS, fill=(0, 0, 0))
            x += n * 10
        d.text((20, yt + 30), note + ": " + " ".join(str(n) for _, n in seq[:12]) + " ...", font=FS, fill=DIM)
    img.save(OUT / "run_cycle.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for fig in (pin_timeline, growl_window, two_clocks, lunge_onion, run_cycle):
        fig()
        print("wrote", fig.__name__)
