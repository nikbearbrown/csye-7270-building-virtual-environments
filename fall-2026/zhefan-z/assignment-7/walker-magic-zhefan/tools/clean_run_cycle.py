"""Clean the Gemini 4-frame run cycle into a sprite sheet (Assignment 7, run cycle).

Input (never modified): design/a7/mage_run_cycle_gemini_raw.jpg, four upscaled pixel-art figures in one row on #00FF00.
Output: assets/sprites/mage/mage_run_cycle_sheet.png, 248x69 RGBA, hframes 4 (cell 62x69, feet anchor 31, 67).
The A2 sprites are only read.

Steps:
1. Grid: the column and row edge profiles are scored against every pitch 12.00-60.00 px (step 0.01) and phase; a
   pitch of 1/2 or 1/3 of the winner that scores at least 80 % as well is taken instead (the fundamental).
2. Sampling: each cell's colour is the per-channel median of its central 40 %.
3. Key: a cell is background when green exceeds red and blue by 80 or more; opaque specks under 3 cells are dropped.
4. Frames: the four largest 8-connected components of non-green raw pixels are the four figures (their column
   ranges overlap: one figure's staff reaches past the next one's hair), left to right = frames 1-4; each cell
   belongs to the figure that covers most of its central 40 %.
5. Palette: every opaque cell takes the nearest colour (CIELAB) used in the nine A2 mage sprites.
6. Scale: one factor for all four frames, 60 / (frame 1's height in cells), applied by nearest neighbour to the colour
   labels (no new colours). Frame 1 is the contact pose "at normal height" in the prompt; contact A is 60 px tall.
7. Placement: one vertical shift for all frames puts Gemini's common ground line (the lowest opaque row over the four
   frames) on row 66, the row above the anchor, so the body bob Gemini drew is kept. Horizontally each frame's torso
   (median x of its capelet-indigo and tunic pixels in the band 40-75 % down the figure) goes to contact A's torso x.

Run from walker-magic-zhefan/ with the ComfyUI venv (Pillow, NumPy 2, SciPy):
    E:/7270/tools/ComfyUI/.venv/Scripts/python.exe tools/clean_run_cycle.py
Prints a JSON report: grid, frames, scale, shifts, palette-mapping counts, pixels cut off, feet on the ground.
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "design" / "a7" / "mage_run_cycle_gemini_raw.jpg"
MAGE = REPO / "assets" / "sprites" / "mage"
A2_SPRITES = ["mage_idle", "mage_run_contact", "mage_run_passing", "mage_rise", "mage_fall", "mage_cast", "mage_hurt",
              "mage_fail", "mage_win"]
REF_A = MAGE / "mage_run_contact.png"
OUT = MAGE / "mage_run_cycle_sheet.png"
CELL = (62, 69)
GROUND_ROW = 66            # the anchor is (31, 67): feet occupy row 66, as in contact A
TARGET_HEIGHT = 60         # contact A: rows 7-66
GREEN_MARGIN = 80
TORSO_COLOURS = [(58, 64, 160), (38, 30, 138), (107, 90, 78)]   # capelet indigo, indigo shade, tunic


def srgb_to_lab(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def comb_at(prof, pitch):
    n = len(prof)
    ks = np.arange(0, n / pitch)
    best = (0.0, -1.0)
    for phase in np.arange(0.0, pitch, 0.5):
        idx = np.rint(phase + ks * pitch).astype(int)
        idx = idx[idx < n]
        if len(idx) < 8:
            continue
        score = prof[idx].mean() - prof.mean()
        if score > best[1]:
            best = (float(phase), float(score))
    return best


def comb(profile, lo=12.0, hi=60.0):
    prof = profile / (profile.max() + 1e-9)
    best = (0.0, 0.0, -1.0)
    for pitch in np.arange(lo, hi, 0.01):
        phase, score = comb_at(prof, pitch)
        if score > best[2]:
            best = (float(pitch), phase, score)
    for k in (3, 2):
        sub = best[0] / k
        if sub < lo:
            continue
        cand = max(((p,) + comb_at(prof, p) for p in np.arange(sub - 0.2, sub + 0.2, 0.01)), key=lambda c: c[2])
        if cand[2] >= 0.8 * best[2]:
            return float(cand[0]), cand[1], cand[2]
    return best


def torso_x(rgba):
    """Median x of capelet/tunic pixels in the band 40-75 % down the figure."""
    rows = np.where(rgba[..., 3].any(axis=1))[0]
    top, bottom = rows.min(), rows.max()
    y0, y1 = int(top + 0.40 * (bottom - top)), int(top + 0.75 * (bottom - top))
    band = rgba[y0:y1 + 1]
    m = np.zeros(band.shape[:2], bool)
    for c in TORSO_COLOURS:
        m |= np.all(band[..., :3] == c, axis=-1) & (band[..., 3] > 0)
    return float(np.median(np.where(m)[1])), int(m.sum())


def main():
    raw = np.asarray(Image.open(RAW).convert("RGB")).astype(np.float64)
    h, w, _ = raw.shape
    px, ox, sx = comb(np.abs(np.diff(raw, axis=1)).sum(axis=(0, 2)))
    py, oy, sy = comb(np.abs(np.diff(raw, axis=0)).sum(axis=(1, 2)))
    ox, oy = (ox + 1.0) % px, (oy + 1.0) % py
    nx, ny = int((w - ox) // px), int((h - oy) // py)
    green = (raw[..., 1] - np.maximum(raw[..., 0], raw[..., 2])) >= GREEN_MARGIN
    comp, n_comp = ndimage.label(~green, structure=np.ones((3, 3)))
    comp_sizes = ndimage.sum(~green, comp, range(1, n_comp + 1))
    figures = np.argsort(comp_sizes)[::-1][:4] + 1
    figures = sorted(figures, key=lambda c: np.where(comp == c)[1].mean())   # left to right
    cells = np.zeros((ny, nx, 3))
    owner = np.full((ny, nx), -1, dtype=int)
    for j in range(ny):
        y0, y1 = int(round(oy + (j + 0.3) * py)), int(round(oy + (j + 0.7) * py))
        for i in range(nx):
            x0, x1 = int(round(ox + (i + 0.3) * px)), int(round(ox + (i + 0.7) * px))
            cells[j, i] = np.median(raw[y0:y1, x0:x1].reshape(-1, 3), axis=0)
            ids = comp[y0:y1, x0:x1].ravel()
            counts = [int((ids == c).sum()) for c in figures]
            if max(counts) > 0:
                owner[j, i] = int(np.argmax(counts))
    fg = ~((cells[..., 1] - np.maximum(cells[..., 0], cells[..., 2])) >= GREEN_MARGIN)
    lab, n = ndimage.label(fg)
    sizes = ndimage.sum(fg, lab, range(1, n + 1))
    specks = np.isin(lab, np.where(sizes < 3)[0] + 1)
    fg &= ~specks

    # Palette of the nine A2 mage sprites; nearest colour in CIELAB.
    pal = sorted({tuple(int(v) for v in p[:3]) for s in A2_SPRITES
                  for p in np.asarray(Image.open(MAGE / f"{s}.png").convert("RGBA")).reshape(-1, 4) if p[3] > 0})
    pal_arr = np.array(pal, dtype=np.float64)
    src = cells[fg]
    d = ((srgb_to_lab(src)[:, None, :] - srgb_to_lab(pal_arr)[None]) ** 2).sum(-1)
    nearest = d.argmin(1)
    de = np.sqrt(d[np.arange(len(src)), nearest])
    labels = np.full(fg.shape, -1, dtype=int)
    labels[fg] = nearest

    # Four frames: each figure's cells, cropped to its bounding box.
    frames = []
    orphan = int((fg & (owner < 0)).sum())
    for k in range(4):
        mine = np.where(fg & (owner == k), labels, -1)
        ys, xs = np.where(mine >= 0)
        sub = mine[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        frames.append({"x": [int(xs.min()), int(xs.max())], "y": [int(ys.min()), int(ys.max())], "labels": sub,
                       "raw_component_px": int(comp_sizes[figures[k] - 1])})
    ground_cells = max(f["y"][1] for f in frames)
    scale = TARGET_HEIGHT / (frames[0]["y"][1] - frames[0]["y"][0] + 1)

    # Contact A's torso.
    ref = np.asarray(Image.open(REF_A).convert("RGBA"))
    ref_tx, _ = torso_x(ref)

    sheet = np.zeros((CELL[1], CELL[0] * 4, 4), dtype=np.uint8)
    report_frames = []
    for k, f in enumerate(frames):
        sub = f["labels"]
        hh, ww = sub.shape
        th, tw = int(round(hh * scale)), int(round(ww * scale))
        yi = np.minimum((np.arange(th) / scale).astype(int), hh - 1)
        xi = np.minimum((np.arange(tw) / scale).astype(int), ww - 1)
        big = sub[yi][:, xi]
        rgba = np.zeros((th, tw, 4), dtype=np.uint8)
        rgba[big >= 0, :3] = pal_arr[big[big >= 0]].astype(np.uint8)
        rgba[big >= 0, 3] = 255
        # The common ground row, counted from this frame's top row and scaled, lands on GROUND_ROW.
        ground_in_frame = int(round((ground_cells - f["y"][0] + 1) * scale)) - 1
        top = GROUND_ROW - ground_in_frame
        tx, n_torso = torso_x(rgba)
        left = int(round(ref_tx - tx))
        cell = np.zeros((CELL[1], CELL[0], 4), dtype=np.uint8)
        y0, y1 = max(top, 0), min(top + th, CELL[1])
        x0, x1 = max(left, 0), min(left + tw, CELL[0])
        cell[y0:y1, x0:x1] = rgba[y0 - top:y1 - top, x0 - left:x1 - left]
        cut = int((rgba[..., 3] > 0).sum() - (cell[..., 3] > 0).sum())
        sheet[:, CELL[0] * k:CELL[0] * (k + 1)] = cell
        rows = np.where(cell[..., 3].any(axis=1))[0]
        feet_cols = np.where(cell[GROUND_ROW, :, 3] > 0)[0]
        report_frames.append({
            "frame": k + 1, "raw_cells_x": f["x"], "raw_cells_y": f["y"], "raw_component_px": f["raw_component_px"],
            "size_cells": [ww, hh], "size_scaled": [tw, th],
            "placed_top_left": [left, top], "torso_x_scaled": round(tx, 1), "torso_pixels": n_torso,
            "rows_in_cell": [int(rows.min()), int(rows.max())] if len(rows) else None,
            "pixels_cut_off": cut,
            "ground_row_66_columns": [int(feet_cols.min()), int(feet_cols.max())] if len(feet_cols) else [],
        })
    Image.fromarray(sheet, "RGBA").save(OUT)
    report = {
        "raw": f"{RAW.relative_to(REPO).as_posix()} {w}x{h}",
        "grid": {"pitch_x_px": round(px, 2), "pitch_y_px": round(py, 2), "origin_px": [round(ox, 2), round(oy, 2)],
                 "cells": [nx, ny], "comb_score": [round(sx, 3), round(sy, 3)]},
        "key": {"opaque_cells": int(fg.sum()), "specks_removed": int(specks.sum()),
                "opaque_cells_in_no_figure": orphan},
        "palette": {"colours_available": len(pal), "colours_used": int(len(set(nearest.tolist()))),
                    "pixels_mapped": int(len(src)), "changed_by_dE_over_5": int((de > 5).sum()),
                    "changed_by_dE_over_10": int((de > 10).sum()), "changed_by_dE_over_20": int((de > 20).sum()),
                    "dE_median": round(float(np.median(de)), 2), "dE_max": round(float(de.max()), 2)},
        "scale": {"factor": round(scale, 4), "frame1_height_cells": frames[0]["y"][1] - frames[0]["y"][0] + 1,
                  "common_ground_cell_row": ground_cells, "contact_a_torso_x": ref_tx},
        "frames": report_frames,
        "out": f"{OUT.relative_to(REPO).as_posix()} {sheet.shape[1]}x{sheet.shape[0]} RGBA, hframes 4",
    }
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
