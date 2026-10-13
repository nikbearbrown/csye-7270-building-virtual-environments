#!/usr/bin/env python3
"""analyze_scenes.py: measures the scene frames from run_scenes.py against what the narration claims, one line per claim, writes scenes-summary.txt.
Times come from the specs themselves (0.3 s after each keyframe), so the check follows the planned timing. Frames are 1280 x 720; sprites are drawn at
whole-number scales, so canvas px = image px x scale."""
import json
from collections import Counter
from pathlib import Path
import numpy as np
import ol_measure as M
from run_scenes import key_times

HERE = Path(__file__).resolve().parent
PNG = HERE / "png" / "scenes"
L = []
def say(s=""):
    print(s); L.append(s)

def spec(sid):
    return json.loads((HERE / "scenes" / f"{sid}.json").read_text())

def frame(sid, t):
    cands = sorted(PNG.glob(f"{sid}-t*.png"), key=lambda p: abs(float(p.stem.split("-t")[-1]) - t))
    return M.load(cands[0]), float(cands[0].stem.split("-t")[-1])

def after(sid, k):                      # the settled frame 0.3 s after keyframe time k
    return frame(sid, k + 0.3)

def last(sid):
    return frame(sid, spec(sid)["duration"] - 0.05)

def crop(im, cx, cy, half=300):
    return im[max(cy - half, 0):cy + half, max(cx - half, 0):cx + half]

def lineish(im):
    c = M.classes(im)
    return c["line"] | c["over"]

def keys_of(sid, sprite, field, sub=None):
    sp = spec(sid)["sprites"][sprite]
    v = sp[field] if sub is None else sp[field][sub]
    return [float(k[0]) for k in v["keys"]]

say("canvas px = image px x scale; line colour (64, 64, 191); frames from run_scene.sh at the times the specs plan")

im, t = frame("C01-hook", 0.05); say(f"C01 at t={t}: outline px before the shader switches on: {int(lineish(im).sum())}")
im, t = last("C01-hook"); say(f"C01 at t={t}: axis widths {M.axis_widths(im)} (thickness 3 x scale 4 = 12)")

im, t = last("C02-bigcopy")
back = M.mask_of(im, (64, 64, 191), 8); sol = M.mask_of(im, M.TEAL, 6)
def walk(dx, dy, x, y):
    while sol[y, x]: x += dx; y += dy
    n = 0
    while back[y, x]: n += 1; x += dx; y += dy
    return n
tip = walk(1, 0, 640, 360); side = walk(0, -1, 640 + 90, 360)
say(f"C02 at t={t}: border at an arm's tip {tip} px, along an arm's side {side} px, ratio {tip / max(side, 1):.2f} (copy 7.2x on a 6x sprite: tip 0.2 x 24 x 6 = 28.8, side 0.2 x 8 x 6 = 9.6)")

base = M.solid(frame("C01-hook", 0.05)[0])
im, t = frame("C07-paints-the-sprite", 0.05)
say(f"C07 at t={t} (plain sprite, before the switch): outline px {int(lineish(im).sum())}")
im, t = last("C07-paints-the-sprite"); c = M.classes(im)
say(f"C07 (x4) at t={t}: sprite pixels painted line colour {int((c['line'] & base).sum())} of {int(base.sum())} = {100 * (c['line'] & base).sum() / base.sum():.1f}%   (at 1:1: 95.0%)")
im, t = frame("C08-one-question", 0.05); c = M.classes(im)
say(f"C08 (x4) at t={t} (the first try still on): sprite pixels painted line colour {int((c['line'] & base).sum())} of {int(base.sum())} = {100 * (c['line'] & base).sum() / base.sum():.1f}%")
im, t = last("C08-one-question"); c = M.classes(im); ys, xs = np.nonzero(c["line"] | c["over"])
say(f"C08 (x4) at t={t} (after the fix): outline px {len(xs)}; left of the sprite centre {int((xs < 640).sum())}, right {int((xs > 640).sum())}; sprite pixels painted line colour {int((c['line'] & base).sum())}")
im, t = frame("C09-lighter-diagonals", 0.05); c = M.classes(im); ys, xs = np.nonzero(c["line"] | c["over"])
say(f"C09 (x4) at t={t} (the one-sided line still on): outline px {len(xs)}, left of the centre {int((xs < 640).sum())}, right {int((xs > 640).sum())}")
im, t = last("C09-lighter-diagonals"); c = M.classes(im); tot = int((c["line"] | c["over"]).sum())
say(f"C09 (x4) at t={t}: ring px {tot}, wrong-colour px {int(c['over'].sum())} = {100 * c['over'].sum() / max(tot, 1):.1f}%")
im, t = frame("C10-four-questions", 0.05); c = M.classes(im); tot = int((c["line"] | c["over"]).sum())
say(f"C10 (x4) at t={t} (before the cap): ring px {tot}, wrong-colour px {int(c['over'].sum())} = {100 * c['over'].sum() / max(tot, 1):.1f}%")
im, t = last("C10-four-questions"); c = M.classes(im); tot = int((c["line"] | c["over"]).sum())
say(f"C10 (x4) at t={t} (after the cap): ring px {tot}, wrong-colour px {int(c['over'].sum())} = {100 * c['over'].sum() / max(tot, 1):.1f}%")

for k, th in zip(keys_of("C13-thickness-steps", 0, "uniforms", "thickness"), (1, 2, 3, 4)):
    im, t = after("C13-thickness-steps", k)
    say(f"C13 at t={t}: axis widths {M.axis_widths(im)}  (thickness {th} x 4 = {th * 4})")
ks = keys_of("C14-line-color", 0, "uniforms", "line_color")
for k, name in zip(ks, ("indigo (64, 64, 191)", "magenta (204, 64, 140)", "amber (242, 179, 26)")):
    im, t = after("C14-line-color", k)
    cnt = Counter(map(tuple, im.reshape(-1, 3)))
    for col in (M.STAGE, M.TEAL, M.CREAM): cnt.pop(tuple(col), None)
    say(f"C14 at t={t}: ring colour {tuple(int(v) for v in cnt.most_common(1)[0][0])}  (expected {name})")
for k, sc in zip(keys_of("C16-scales", 0, "scale"), (1, 2, 3)):
    im, t = after("C16-scales", k)
    say(f"C16 at t={t}: thickness 2 at scale {sc}: axis widths {M.axis_widths(im)}  (expected {2 * sc})")

th_keys = keys_of("C17-corners", 0, "uniforms", "thickness")
for k, th in zip(th_keys, (1, 2, 3)):
    im, t = after("C17-corners", k)
    left, right = crop(im, 340, 360, 200), crop(im, 940, 360, 200)
    d = int(lineish(right).sum() - lineish(left).sum())
    say(f"C17 at t={t}: thickness {th}: four-read ring {int(lineish(left).sum())} px, eight-read ring {int(lineish(right).sum())} px, difference {d} px (expected 4 x t^2 x 16 = {4 * th * th * 16})")

im18a, ta = frame("C18-eight-reads", 0.05); im18b, tb = last("C18-eight-reads"); im19, t19 = frame("C19-loop", 0.05)
say(f"C18 (square sprite, x4) at t={ta} (four reads): line px {int(lineish(im18a).sum())}; at t={tb} (after the corners switch on): line px {int(lineish(im18b).sum())}; difference {int(lineish(im18b).sum()) - int(lineish(im18a).sum())} (expected 576 = 4 x 3 x 3 x 16)")
say(f"C19 (square sprite, loop, x4) line px {int(lineish(im19).sum())}; pixels that differ from C18's final frame (the eight written-out reads): {int((np.abs(im19 - im18b).max(axis=2) > 0).sum())}")

for k, th in zip(keys_of("C21-same-picture", 0, "uniforms", "thickness"), (1, 2, 3, 4, 8)):
    im, t = after("C21-same-picture", k)
    left, right = crop(im, 340, 360, 280), crop(im, 940, 360, 280)
    say(f"C21 at t={t}: thickness {th}: pixels that differ between the eight-read and loop sprites: {int((np.abs(left - right).max(axis=2) > 0).sum())}")

def tinted(img):
    c = M.classes(img); return int((~(c["stage"] | c["teal"] | c["cream"])).sum())
sp = spec("C25-zero-means-zero"); k_off = float(sp["sprites"][0]["uniforms"]["thickness"]["keys"][1][0])
def differing(img):
    return int((np.abs(crop(img, 330, 360, 300) - crop(img, 950, 360, 300)).max(axis=2) > 0).sum())
im, t = frame("C25-zero-means-zero", 0.3)
say(f"C25 at t={t} (thickness 2, both ringed): pixels that differ between the no-guard sprite and the guard sprite: {differing(im)}")
im, t = after("C25-zero-means-zero", k_off)
say(f"C25 at t={t} (thickness 0): pixels that differ between the no-guard sprite and the guard sprite: {differing(im)}  (the tinted rim; 224 rim pixels x 16 canvas px each = 3584)")

sp = spec("C26-select"); kt = [float(e["t"]) for e in sp["input"]]
for label, tt in (("before any key", 0.5), ("after the first key", kt[0] + 0.4), ("after the second key", kt[1] + 0.4)):
    im, t = frame("C26-select", tt); say(f"C26 at t={t} ({label}): outline px {int(lineish(im).sum())}")
sp = spec("C27-shared-material"); l_on = float(sp["sprites"][0]["uniforms"]["thickness"]["keys"][1][0]); i_on = float(sp["sprites"][0]["instance_from"])
for label, tt in (("before the dial is set", 0.5), ("dial set on the left, ordinary uniform", l_on + 0.4), ("instance uniform: left 2, right 0", i_on + 0.4)):
    im, t = frame("C27-shared-material", tt)
    say(f"C27 at t={t} ({label}): outline px left unit {int(lineish(crop(im, 340, 360, 300)).sum())}, right unit {int(lineish(crop(im, 940, 360, 300)).sum())}")

d0, d1 = keys_of("C28-slide-clip", 0, "uniforms", "look")
look_at = lambda f: (f - d0) / (d1 - d0) * 0.4
for label, f in (("a third of the way", 0.35), ("two thirds", 0.7), ("the end", 1.0)):
    tt = d0 + (d1 - d0) * f
    im, t = frame("C28-slide-clip", tt); sol = M.solid(im); ys, xs = np.nonzero(sol)
    say(f"C28 at t={t} ({label}, look about {look_at((t - d0) / (d1 - d0) * (d1 - d0) + d0):.2f}): the sprite's left-most solid column is x = {xs.min()} (the image rectangle's left edge is x = 384; the uncut sprite would start at {486 - int(look_at(t) * 512)})")
im, t = last("C29-tight"); say(f"C29 at t={t}: axis widths {M.axis_widths(im)}  (nothing at the four places the shape touches the edge)")
im, t = last("C31-padding")
for name, cx, pad in (("pad 0", 240, 0), ("pad 2", 640, 2), ("pad 4", 1040, 4)):
    say(f"C31 at t={t}: {name}: axis widths {M.axis_widths(crop(im, cx, 360, 150))}  (padding {pad} x 3 = {pad * 3}; thickness 4 x 3 = 12)")

def stray(img):                         # line pixels in the 16-px-wide strip along frame 1's left edge (x 772 to 788) over the frame's height
    return int(lineish(img[232:488, 772:788]).sum())
def ring_total(img):
    return int(lineish(img[:, 740:1060]).sum())
sp = spec("C32-sheet"); r0, r1 = (float(k[0]) for k in sp["sprites"][1]["uniforms"]["thickness"]["keys"][1:3])
for label, tt in (("outline off", 0.3), ("outline on", r1 + 0.4)):
    im, t = frame("C32-sheet", tt); say(f"C32 at t={t} ({label}): stray-line strip {stray(im)} line px (a full strip is 16 x 256 = 4096), ring px in the frame {ring_total(im)}")
sp = spec("C33-sheet-clamp"); q0 = float(sp["sprites"][1]["shader_at"]["keys"][1][0])
im1, t1 = frame("C33-sheet-clamp", 0.05); im2, t2 = frame("C33-sheet-clamp", q0 + 0.5)
say(f"C33 before the clamp (t={t1}): stray strip {stray(im1)} px, outline px in the frame panel {ring_total(im1)}; after (t={t2}): strip {stray(im2)}, outline px {ring_total(im2)}; before minus the strip = {ring_total(im1) - stray(im1)} (equal to the after count: the disc's own ring is untouched)")

im, t = last("C34-brushes")
for name, cx in (("four reads", 215), ("eight reads", 640), ("ring of sixteen", 1065)):
    sub = crop(im, cx, 360, 190)
    th = {a: M.ring_thickness(sub, a, spread=3.0) for a in (0, 45)}
    say(f"C34 at t={t}: {name}: axis {th[0]:.1f} px, diagonal {th[45]:.1f} px, ratio {th[45] / max(th[0], 1e-9):.2f}  (thickness 8 x 3 = 24)")
im, t = last("C36-ring"); say(f"C36 at t={t}: axis widths {M.axis_widths(im)} (thickness 8 x 4 = 32)")
im, t = last("C37-stem")
for name, cx in (("eight reads", 330), ("ring of sixteen", 950)):
    y = 360 - 256 + 17 * 4 + 2           # image row 17 (stem only), middle of its four canvas rows
    row = im[y, cx - 120:cx + 120]
    s = "".join("#" if M.mask_of(row[None, i:i + 1], M.LINE, 6)[0, 0] else ("S" if M.mask_of(row[None, i:i + 1], M.TEAL, 6)[0, 0] else ".") for i in range(0, row.shape[0], 4))
    say(f"C37 at t={t}: {name}: the stem row, one character per image pixel: {s}")

def panel(im, cx, cy=360, half=192):
    return im[cy - half:cy + half, cx - half:cx + half]
def blended(im, cx):
    """pixels in the 384 x 384 panel (a 12x look at a 32 x 32 piece of the rim) whose colour is none of stage, teal, cream, line: the blurred ones"""
    c = M.classes(panel(im, cx))
    return int((~(c["stage"] | c["teal"] | c["cream"] | c["line"] | c["over"])).sum())
def changed(a, b, cx):
    return int((np.abs(panel(a, cx) - panel(b, cx)).max(axis=2) > 0).sum())
sid = "C38-soft-edges"
im0, t0 = frame(sid, spec(sid)["duration"] * 0.5); im1, t1 = last(sid)
say(f"C38 (a 12x look at the soft rim, 147,456 px per panel): canvas pixels that differ between t={t0} (both panels plain mix) and t={t1} (right panel switched to the composite): left panel {changed(im0, im1, 330)}, right panel {changed(im0, im1, 950)}")
sid = "C39-filter"
im0, t0 = frame(sid, spec(sid)["duration"] * 0.5); im1, t1 = last(sid)
say(f"C39 (a 12x look at the rim, 147,456 px per panel) panels with a colour that is neither stage, teal, cream nor line (blurred px): at t={t0} (both linear) left {blended(im0, 330)}, right {blended(im0, 950)}; "
    f"at t={t1} (left switched to nearest) left {blended(im1, 330)}, right {blended(im1, 950)}")

def alpha_note(sid):
    return ""
im_a, ta = frame("C40-modulate", 0.05); im_b, tb = last("C40-modulate")
def solid_px(img, cx): c = M.classes(crop(img, cx, 360, 300)); return int((c["teal"] | c["cream"]).sum()), int((c["line"] | c["over"]).sum())
say(f"C40 before the fade (t={ta}): left (sprite px, line px) {solid_px(im_a, 340)}, right {solid_px(im_a, 940)}")
cl = crop(im_b, 340, 360, 300); cr = crop(im_b, 940, 360, 300)
say(f"C40 after the fade (t={tb}): left sprite centre pixel {tuple(int(v) for v in cl[300, 300])}, right sprite centre pixel {tuple(int(v) for v in cr[300, 300])}  (stage (217,213,202); teal (95,163,145); half faded teal over stage = (156,188,174))")
(HERE / "scenes-summary.txt").write_text("\n".join(L) + "\n")
