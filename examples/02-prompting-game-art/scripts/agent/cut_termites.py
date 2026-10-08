#!/usr/bin/env python3
"""Cut three termite soldiers from TERM-REF-02.jpg into a 144×48 horizontal strip.

Usage: python3 tools/cut_termites.py
Output: godot/features/termite/termite_soldiers.png (144×48, RGBA)

Finds soldiers by non-white pixels; never uses a fixed grid.
Scales all three by one shared factor so the largest fits 48×48.
Does not rotate, redraw, or recolour.
"""

import sys
import numpy as np
from PIL import Image
from pathlib import Path

WHITE_THRESHOLD = 230  # JPEG background: all channels above this = white


def make_mask(arr: np.ndarray) -> np.ndarray:
    rgb = arr[:, :, :3]
    return ~(
        (rgb[:, :, 0] > WHITE_THRESHOLD)
        & (rgb[:, :, 1] > WHITE_THRESHOLD)
        & (rgb[:, :, 2] > WHITE_THRESHOLD)
    )


def label_largest(mask: np.ndarray, n: int = 3):
    """DFS connected-component; return bboxes of the n largest components."""
    rows, cols = mask.shape
    labeled = np.zeros_like(mask, dtype=np.int32)
    sizes: dict[int, int] = {}
    current = 0

    fg_r, fg_c = np.where(mask)
    fg_pixels = list(zip(fg_r.tolist(), fg_c.tolist()))

    for r0, c0 in fg_pixels:
        if labeled[r0, c0]:
            continue
        current += 1
        stack = [(r0, c0)]
        labeled[r0, c0] = current
        size = 0
        while stack:
            r, c = stack.pop()
            size += 1
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and mask[nr, nc]
                    and not labeled[nr, nc]
                ):
                    labeled[nr, nc] = current
                    stack.append((nr, nc))
        sizes[current] = size

    top_labels = sorted(sizes, key=sizes.__getitem__, reverse=True)[:n]
    bboxes = []
    for lbl in top_labels:
        where = np.where(labeled == lbl)
        bboxes.append(
            (int(where[0].min()), int(where[1].min()),
             int(where[0].max()), int(where[1].max()))
        )
    return bboxes


def classify_by_position(
    bb: tuple[int, int, int, int], img_h: int, img_w: int
) -> str:
    """Classify soldier by centroid position in TERM-REF-02's triangular layout.

    Bottom-centre → black head.  Top-left → red head.  Top-right → yellow head.
    This is layout-specific; colour sampling fails for the dark-maroon red head.
    """
    r_min, c_min, r_max, c_max = bb
    centroid_r = (r_min + r_max) / 2
    centroid_c = (c_min + c_max) / 2
    if centroid_r > img_h * 0.5:
        return "black"
    return "red" if centroid_c < img_w * 0.5 else "yellow"


def measure_body(scaled_rgba: np.ndarray, threshold_frac: float = 0.30):
    """Return (col_lo, col_hi, row_lo, row_hi) of the dense body core.

    Rows/cols where opaque-pixel count exceeds threshold_frac × max_count
    are 'body'; the rest are thin legs or antennae.
    """
    alpha = scaled_rgba[:, :, 3]
    row_counts = (alpha > 0).sum(axis=1)
    col_counts = (alpha > 0).sum(axis=0)
    row_thresh = row_counts.max() * threshold_frac
    col_thresh = col_counts.max() * threshold_frac
    body_rows = np.where(row_counts > row_thresh)[0]
    body_cols = np.where(col_counts > col_thresh)[0]
    if body_rows.size == 0 or body_cols.size == 0:
        return 0, int(scaled_rgba.shape[1] - 1), 0, int(scaled_rgba.shape[0] - 1)
    return int(body_cols[0]), int(body_cols[-1]), int(body_rows[0]), int(body_rows[-1])


def main() -> None:
    repo = Path(__file__).resolve().parent.parent
    src = repo / "source-art" / "TERM-REF-02.jpg"
    out_dir = repo / "godot" / "features" / "termite"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "termite_soldiers.png"

    img = Image.open(src).convert("RGBA")
    arr = np.array(img)
    print(f"Source: {src.name}  {img.width}×{img.height} px")

    mask = make_mask(arr)
    print(f"Non-white pixels: {mask.sum():,}")

    print("Labelling components (DFS)…", flush=True)
    bboxes = label_largest(mask, 3)

    labelled = []
    for bb in bboxes:
        r_min, c_min, r_max, c_max = bb
        crop_arr = arr[r_min : r_max + 1, c_min : c_max + 1]
        name = classify_by_position(bb, img.height, img.width)
        labelled.append((name, bb, crop_arr))

    order = {"black": 0, "red": 1, "yellow": 2, "unknown": 3}
    labelled.sort(key=lambda x: order.get(x[0], 3))

    max_dim = max(
        max(bb[2] - bb[0] + 1, bb[3] - bb[1] + 1) for _, bb, _ in labelled
    )
    scale = 48.0 / max_dim
    print(f"\nScale factor: {scale:.6f}  (largest source dim {max_dim} px → 48 px)")

    strip = Image.new("RGBA", (144, 48), (0, 0, 0, 0))

    for slot, (name, bb, crop_arr) in enumerate(labelled):
        r_min, c_min, r_max, c_max = bb
        src_w = c_max - c_min + 1
        src_h = r_max - r_min + 1
        dst_w = max(1, round(src_w * scale))
        dst_h = max(1, round(src_h * scale))

        crop_img = Image.fromarray(crop_arr)
        scaled_img = crop_img.resize((dst_w, dst_h), Image.NEAREST)
        scaled_arr = np.array(scaled_img)

        rgb = scaled_arr[:, :, :3]
        is_white = (
            (rgb[:, :, 0] > WHITE_THRESHOLD)
            & (rgb[:, :, 1] > WHITE_THRESHOLD)
            & (rgb[:, :, 2] > WHITE_THRESHOLD)
        )
        scaled_arr[:, :, 3] = np.where(is_white, 0, 255)

        final_img = Image.fromarray(scaled_arr)
        x_off = (48 - dst_w) // 2
        y_off = (48 - dst_h) // 2
        strip.paste(final_img, (slot * 48 + x_off, y_off), final_img)

        print(f"\nSoldier '{name}' (slot {slot}):")
        print(f"  Source bbox: ({c_min},{r_min})–({c_max},{r_max})  {src_w}×{src_h} px")
        print(f"  Scaled size: {dst_w}×{dst_h} px  cell offset: ({x_off},{y_off})")

        if name == "black":
            col_lo, col_hi, row_lo, row_hi = measure_body(scaled_arr)
            body_w = col_hi - col_lo + 1
            body_h = row_hi - row_lo + 1
            print(f"  Body core (≥30% row/col density):")
            print(f"    crop-relative  cols {col_lo}–{col_hi}, rows {row_lo}–{row_hi}")
            print(f"    body size in scaled crop: {body_w}×{body_h} px")
            print(f"  → RectangleShape2D size suggestion: Vector2({body_w}, {body_h})")

    strip.save(str(out), optimize=False)
    print(f"\nWrote: godot/features/termite/termite_soldiers.png  (144×48 RGBA)")


if __name__ == "__main__":
    main()
