#!/usr/bin/env python3
"""make_pantry.py — cuts the pictures the scenes display (pantry/ev_*) from the REAL native captures in captures/ and from the example's own texture files.
Nothing is redrawn, recoloured or re-rendered: every file is a crop or a nearest-neighbour / Lanczos resize of a real engine capture or a real source texture.
Safe to re-run. Run from anywhere:  python3 evidence/make_pantry.py

Crop boxes were measured from the captures (3840 x 2160, Godot 4.7.2, Compatibility renderer, Apple M4 Pro; see EVIDENCE-INDEX.md):
  pad quad ............ (1110, 540, 2730, 1620)   1620 x 1080   (the signal shader on a flat 3 x 2 quad; UV.x 0.15625 -> x 253, UV.x 0.21875 -> x 354, both at y 540)
  hint fixture ........ (1110, 526, 2730, 1632)   1620 x 1106   (two rows of three bands: top = source_color, bottom = data)
  two spheres ......... (1164, 756, 2676, 1404)   1512 x 648    (matte left, coated right)
  one sphere .......... (1596, 756, 2244, 1404)    648 x 648
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
CAP = HERE / "captures" / "example-native"
PAN = HERE / "pantry"
PAN.mkdir(exist_ok=True)
WALKER = Path("/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/godot/course-series")


def crop(src, box, dst):
    im = Image.open(src).convert("RGB").crop(box)
    im.save(PAN / dst)
    print("wrote", dst, im.size)


for v in ("0.0", "0.5", "1.0", "2.0"):
    crop(CAP / f"signal-{v}.png", (1110, 540, 2730, 1620), f"ev_pad_{v}.png")
crop(CAP / "hint-native-3840.png", (1110, 526, 2730, 1632), "ev_hint_compat_example.png")
crop(CAP / "hint-screen-grid-native-3840.png", (1110, 526, 2730, 1632), "ev_hint_grid_example.png")
crop(CAP / "materials-baseline.png", (1164, 756, 2676, 1404), "ev_mat_baseline.png")
crop(CAP / "materials-shared-shader-edit.png", (1164, 756, 2676, 1404), "ev_mat_shared_edit.png")
crop(CAP / "materials-one-value-edit.png", (1164, 756, 2676, 1404), "ev_mat_one_edit.png")
for p in ("tint", "roughness_gain", "uv_scale", "metallic_gain"):
    for i in range(3):
        crop(CAP / f"sweep-{p}-{i}.png", (1596, 756, 2244, 1404), f"ev_sweep_{p}_{i}.png")

# the example's own textures, enlarged with nearest-neighbour so every texel stays a crisp square
for name, dst in (("gate-color.png", "ev_tex_color.png"), ("gate-roughness.png", "ev_tex_rough.png")):
    im = Image.open(WALKER / "material-textures" / name).convert("RGB")
    im.resize((im.width * 16, im.height * 16), Image.NEAREST).save(PAN / dst)
    print("wrote", dst, (im.width * 16, im.height * 16))
im = Image.open(WALKER / "material-textures" / "analytic-normal-gl.png").convert("RGB")
im.resize((768, 768), Image.NEAREST).save(PAN / "ev_normal_analytic.png"); print("wrote ev_normal_analytic.png (256 -> 768, nearest)")
for v in ("gl", "dx"):
    im = Image.open(WALKER / "normal-calibration" / f"stone_floor_nor_{v}_1k.png").convert("RGB")
    im.resize((768, 768), Image.LANCZOS).save(PAN / f"ev_normal_{v}.png"); print(f"wrote ev_normal_{v}.png (1024 -> 768, Lanczos)")


# ── captured for THIS film (evidence/EVIDENCE-NOTES.md, R7 R8 R9): same fixture and camera in both renderers, Godot 4.7.2, Apple M4 Pro ──
FP = HERE / "captures" / "forward-plus"
crop(FP / "hint_forward_plus.png", (1110, 526, 2730, 1633), "ev_hint_fp.png")                 # top row source_color, bottom row data: 64/128/192 and 137/188/225
crop(FP / "hint_compatibility.png", (1110, 526, 2730, 1633), "ev_hint_compat.png")            # both rows 64/128/192 (explicit WorldEnvironment; the example's own fixture has none)
for v in ("0.0", "0.5", "1.0", "2.0"):
    crop(FP / f"signal_fp_{v}.png", (1110, 540, 2730, 1620), f"ev_pad_fp_{v}.png")             # the pad shader on Forward+ (Compatibility twins are ev_pad_<v>.png)
for tag in ("forward_plus", "compatibility"):
    im = Image.open(FP / f"constant_albedo_{tag}.png").convert("RGB").crop((106, 54, 3734, 2106))
    im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    im.save(PAN / f"ev_probe_{tag}.png"); print(f"wrote ev_probe_{tag}.png", im.size)       # R9: constant ALBEDO patches, 4 rows x 10 values (half size)
