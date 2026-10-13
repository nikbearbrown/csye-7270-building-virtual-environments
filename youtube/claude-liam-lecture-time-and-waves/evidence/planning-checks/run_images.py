#!/usr/bin/env python3
"""run_images.py: whole-picture checks of the displacement and scaling shaders in ../../lab-shaders/, in real Godot 4.7.2 (the Shader Lab).

A Python reference renderer draws what each formula says the picture should be (the Lab's 128 px checker texture, scaled to 288 px in a
640 x 360 window, nearest-neighbour), and the Lab's PNG is compared with it pixel by pixel. For the checker, a pixel may differ only at a
cell edge (within one pixel of a colour change in the reference). Also: the flag stays pinned on the left, the breath scales about the
middle, the smear at a large amplitude, the banner at wind 0 and 1, and a raw sine used as a colour.
Writes image-results.jsonl and image-summary.txt; exit code 1 if any check fails.   Usage: python3 run_images.py
"""
import math
import sys

import numpy as np

import twin_lib as L

TAU = L.TAU
lab_png, record = L.lab_png, L.record

W, H = 640, 360
S = 288                        # the sprite is the 128 px texture scaled by 2.25 and centred
X0, Y0 = (W - S) // 2, (H - S) // 2
CELL = 16                      # checker cell size in the 128 px texture
TEAL8 = np.array([0x5F, 0xA3, 0x91])
CREAM8 = np.array([0xFA, 0xF9, 0xF5])


def checker_tex(u, v):
    """u, v arrays of normalised texture addresses -> colour array (nearest neighbour, clamp to edge)."""
    x = np.clip(np.floor(u * 128).astype(int), 0, 127)
    y = np.clip(np.floor(v * 128).astype(int), 0, 127)
    on = ((x // CELL) + (y // CELL)) % 2 == 0
    out = np.where(on[..., None], CREAM8, TEAL8)
    return out


def reference_displaced(wave_fn):
    """The picture the checker would give if the lookup is (u, v + wave(u))."""
    ys, xs = np.mgrid[0:S, 0:S]
    u = (xs + 0.5) / S
    v = (ys + 0.5) / S
    return checker_tex(u, v + wave_fn(u))


def sprite_region(img):
    return img[Y0:Y0 + S, X0:X0 + S]


def edge_mask(ref):
    """Pixels within one pixel of a colour change in the reference."""
    d = np.zeros(ref.shape[:2], dtype=bool)
    diff_x = np.abs(np.diff(ref, axis=1)).sum(axis=2) > 0
    diff_y = np.abs(np.diff(ref, axis=0)).sum(axis=2) > 0
    d[:, :-1] |= diff_x
    d[:, 1:] |= diff_x
    d[:-1, :] |= diff_y
    d[1:, :] |= diff_y
    # dilate by one more pixel
    e = d.copy()
    e[1:, :] |= d[:-1, :]
    e[:-1, :] |= d[1:, :]
    e[:, 1:] |= d[:, :-1]
    e[:, :-1] |= d[:, 1:]
    return e


def compare_to_reference(label, img, ref):
    act = sprite_region(img)
    mism = np.abs(act - ref).sum(axis=2) > 24
    edges = edge_mask(ref)
    off_edge = mism & ~edges
    pct = 100.0 * mism.sum() / mism.size
    record(label, off_edge.sum() == 0 and pct < 3.0,
           {"mismatching_pixels": int(mism.sum()), "percent_of_picture": round(float(pct), 2), "mismatches_away_from_a_cell_edge": int(off_edge.sum())})


base_args = ["--kind", "sprite", "--sprite-tex", "checker"]

# ---- 09-ripple, 10-flag, 11-two-waves against the reference renderer
AMP, FREQ, SPEED, OFFSET, TV = 0.08, 3.0, 0.5, 0.0, 0.3
flat, _ = lab_png("ripple-flat", "09-ripple.gdshader", base_args + ["--set", "amplitude=0.0", "--set", f"tv={TV}"])
rip, _ = lab_png("ripple-0.08", "09-ripple.gdshader", base_args + ["--set", f"amplitude={AMP}", "--set", f"tv={TV}"])
pin, _ = lab_png("flag-0.08", "10-flag.gdshader", base_args + ["--set", f"amplitude={AMP}", "--set", f"tv={TV}"])
big, _ = lab_png("ripple-0.20", "09-ripple.gdshader", base_args + ["--set", "amplitude=0.20", "--set", f"tv={TV}"])
rip_off, _ = lab_png("ripple-offset-0.25", "09-ripple.gdshader", base_args + ["--set", f"amplitude={AMP}", "--set", f"tv={TV}", "--set", "offset=0.25"])
two, _ = lab_png("two-waves", "11-two-waves.gdshader", base_args + ["--set", f"tv={TV}"])

if flat is not None:
    compare_to_reference("09-ripple at amplitude 0: the checker, untouched", flat, reference_displaced(lambda u: 0 * u))
if rip is not None:
    compare_to_reference("09-ripple (amplitude 0.08, frequency 3, speed 0.5, tv 0.3) equals the formula picture",
                         rip, reference_displaced(lambda u: AMP * np.sin(TAU * ((u - TV * SPEED) * FREQ + OFFSET))))
if rip_off is not None:
    compare_to_reference("09-ripple with offset 0.25 equals the formula picture",
                         rip_off, reference_displaced(lambda u: AMP * np.sin(TAU * ((u - TV * SPEED) * FREQ + 0.25))))
if big is not None:
    compare_to_reference("09-ripple at amplitude 0.20 equals the formula picture (the smear included)",
                         big, reference_displaced(lambda u: 0.20 * np.sin(TAU * ((u - TV * SPEED) * FREQ + OFFSET))))
if pin is not None:
    compare_to_reference("10-flag (wave * UV.x) equals the formula picture",
                         pin, reference_displaced(lambda u: AMP * np.sin(TAU * ((u - TV * SPEED) * FREQ + OFFSET)) * u))
if two is not None:
    compare_to_reference("11-two-waves (two sines added) equals the formula picture",
                         two, reference_displaced(lambda u: 0.04 * np.sin(TAU * (u - TV * 0.4) * 2.0) + 0.015 * np.sin(TAU * (u - TV * 0.7) * 5.0)))

# ---- the flag is pinned: columns near the left edge do not move, the right end does
if flat is not None and rip is not None and pin is not None:
    def col_diff(a, b):
        return np.abs(sprite_region(a)[6:S - 6] - sprite_region(b)[6:S - 6]).sum(axis=(0, 2))
    d_rip, d_pin = col_diff(flat, rip), col_diff(flat, pin)
    left, right = slice(0, 12), slice(S - 60, S)
    record("09-ripple (not pinned) moves the picture at the left edge too", d_rip[left].mean() > 3000 and d_rip[right].mean() > 3000,
           {"mean_column_difference_left_12": round(float(d_rip[left].mean()), 1), "right_60": round(float(d_rip[right].mean()), 1)})
    record("10-flag (pinned by * UV.x): the left edge holds still and the right end moves", d_pin[left].mean() < 0.12 * d_pin[right].mean() and d_pin[right].mean() > 3000,
           {"mean_column_difference_left_12": round(float(d_pin[left].mean()), 1), "right_60": round(float(d_pin[right].mean()), 1)})
    quarters = [float(d_pin[i * S // 4:(i + 1) * S // 4].mean()) for i in range(4)]
    record("10-flag: the movement grows from the left to the right", quarters == sorted(quarters), {"mean_column_difference_by_quarter": [round(q, 1) for q in quarters]})

# ---- smear: a large amplitude on an opaque picture with no margin repeats the edge row
if big is not None:
    top = sprite_region(big)[:24]
    row0 = top[0]
    same_rows = [int((np.abs(top[i] - row0).sum(axis=1) == 0).mean() * 100) for i in range(24)]
    record("09-ripple at amplitude 0.20 on a picture with no margin: rows near the top repeat the edge row (smear)", max(same_rows[3:12]) > 25,
           {"percent_of_columns_identical_to_row_0_for_rows_3_to_11": same_rows[3:12]})

# ---- 08-rings against the formula (a continuous picture: every pixel within a few steps)
RTV, RF, RS = 0.8, 4.0, 0.25
rings, _ = lab_png("rings", "08-rings.gdshader", ["--kind", "sprite", "--sprite-tex", "white", "--set", f"tv={RTV}", "--set", f"frequency={RF}", "--set", f"speed={RS}"])
if rings is not None:
    ys, xs = np.mgrid[0:S, 0:S]
    u, v = (xs + 0.5) / S, (ys + 0.5) / S
    d = np.sqrt((u - 0.5) ** 2 + (v - 0.5) ** 2)
    wave = 0.5 + 0.5 * np.sin(TAU * ((d - RTV * RS) * RF))
    exp = (np.array(L.TEAL)[None, None, :] * (1 - wave[..., None]) + np.array(L.CREAM)[None, None, :] * wave[..., None]) * 255
    err = np.abs(sprite_region(rings) - exp).max(axis=2)
    record("08-rings equals the formula picture (every pixel within 3 steps)", err.max() <= 3.0, {"max_pixel_error_steps": round(float(err.max()), 2), "mean": round(float(err.mean()), 3)})
    # the rings are round: crest radius along the x axis and along the y axis agree
    cx = int(S / 2)
    row = sprite_region(rings)[cx, :, 0]
    col = sprite_region(rings)[:, cx, 0]
    record("08-rings are circles on a square shape: the picture is the same along the x axis and the y axis", np.abs(row.astype(int) - col.astype(int)).max() <= 3,
           {"max_difference_steps_between_the_row_and_the_column_through_the_middle": int(np.abs(row.astype(int) - col.astype(int)).max())})

# ---- 12-breath: the picture is scaled about its middle; an identity strip stands in for the curve (k = fract(tv * 0.4))
def blob_width(img):
    row = img[H // 2]
    teal = (np.abs(row[:, 0] - 95) < 8) & (np.abs(row[:, 1] - 163) < 8) & (np.abs(row[:, 2] - 145) < 8)
    xs = np.where(teal)[0]
    return (int(xs.min()), int(xs.max())) if len(xs) else (0, 0)


widths = {}
for tv, k in ((0.0, 0.0), (1.25, 0.5), (2.0, 0.8)):
    im, _ = lab_png(f"breath-k{k}", "12-breath.gdshader", ["--kind", "sprite", "--sprite-tex", "sprite", "--sprite-scale", "1.0", "--tex", "curve=gradient", "--set", f"tv={tv}"])
    if im is not None:
        widths[k] = blob_width(im)
if len(widths) == 3:
    want = {k: 76.8 * (1 + 0.25 * k) for k in widths}
    got = {k: widths[k][1] - widths[k][0] + 1 for k in widths}
    centres = {k: (widths[k][0] + widths[k][1]) / 2 for k in widths}
    ok = all(abs(got[k] - want[k]) <= 3 for k in widths) and all(abs(centres[k] - centres[0.0]) <= 1.5 for k in widths)
    record("12-breath scales the picture about its middle: blob width = 76.8 px * (1 + 0.25 k), centre unchanged", ok,
           {"measured_width_px": got, "expected_px": {k: round(v, 1) for k, v in want.items()}, "centre_px": centres})

# ---- 13-banner: wind 0 is the flat picture; wind 1 moves the right end and not the left
fl, _ = lab_png("banner-wind0", "13-banner.gdshader", base_args + ["--set", "wind=0.0", "--set", f"tv={TV}"])
w1, _ = lab_png("banner-wind1", "13-banner.gdshader", base_args + ["--set", "wind=1.0", "--set", f"tv={TV}"])
fa, _ = lab_png("banner-amp0", "13-banner.gdshader", base_args + ["--set", "wind=1.0", "--set", "amplitude=0.0", "--set", f"tv={TV}"])
if fl is not None and w1 is not None and fa is not None:
    same = int(np.abs(fl - fa).sum())
    d = np.abs(sprite_region(fl)[6:S - 6] - sprite_region(w1)[6:S - 6]).sum(axis=(0, 2))
    record("13-banner: wind 0 draws the flat picture (identical to amplitude 0)", same == 0, {"pixel_difference": same})
    record("13-banner at wind 1: the left edge holds still and the right end moves", d[:12].mean() < 0.12 * d[-60:].mean() and d[-60:].mean() > 3000,
           {"left_12": round(float(d[:12].mean()), 1), "right_60": round(float(d[-60:].mean()), 1)})
    ref_wind = reference_displaced(lambda u: 0.06 * 1.0 * np.sin(TAU * ((u - TV * 0.5) * 3.0)) * u)
    compare_to_reference("13-banner (wind 1, amplitude 0.06) equals the formula picture", w1, ref_wind)

# ---- a raw sine used as a colour: the negative half is clamped to zero (a colour cannot go below zero)
raw = L.TWINS / "extra-raw-sine.twin.gdshader"
raw.write_text("shader_type canvas_item;\nuniform float tv = 0.0;\nvoid fragment() {\n\tCOLOR = vec4(vec3(sin(TAU * tv)), 1.0);\n}\n")
for tv, want in ((0.25, 1.0), (0.5, 0.0), (0.75, 0.0), (0.875, 0.0), (0.125, math.sin(TAU * 0.125))):
    rr = L.lab(raw, ["--kind", "rect", "--set", f"tv={tv}", "--probe", "0.5,0.5"])
    got = rr["probes"][0]["rgba"][0] if rr.get("ok") else None
    ok = got is not None and abs(got * 255 - want * 255) <= 1.01
    record(f"a raw sine as a colour, tv={tv}: sin = {math.sin(TAU * tv):+.3f} shows as {want:.3f}", ok, {"got": got, "expected": round(want, 4)}, rr.get("cmd", ""))

sys.exit(L.finish("image"))
