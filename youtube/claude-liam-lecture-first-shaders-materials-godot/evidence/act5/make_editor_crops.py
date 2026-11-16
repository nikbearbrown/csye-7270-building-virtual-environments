#!/usr/bin/env python3
"""make_editor_crops.py — cut the REAL Godot editor frames (captures/editor/, 3456 x 1944, recorded by the editor agent) into the pantry pictures
the Act V and Act VII scenes show. Pure crops (no scaling, no redrawing); boxes are from evidence/editor/EDITOR-NOTES.md section 5 and the
code-line centre formulas there (F1a line n at y = 206 + 45 (n - 1); F1b line n at y = 938 + 45 (n - 31); line pitch 45 px).
Run from the reel folder:  python3 evidence/act5/make_editor_crops.py"""
from PIL import Image
C = "captures/editor/"
F = {
 "F1a": C + "ed_F1a_shader-editor_standard-generated_lines-1-35.png",
 "F1b": C + "ed_F1b_shader-editor_standard-generated_fragment-lines-14-49.png",
 "F3a": C + "ed_F3a_inspector_matte-tres.png",
 "F3b": C + "ed_F3b_inspector_coated-tres.png",
 "F4a": C + "ed_F4a_import-dock_gate-color-png.png",
 "F5b": C + "ed_F5b_inspector_standard-source-tres_albedo-roughness-normal-unfolded.png",
 "F5e": C + "ed_F5e_inspector_material-override-menu_convert-entry-highlighted.png",
 "F2": C + "ed_F2_shader-editor_signal_cursor-on-line-10.png",
}
CODE_X, CODE_W = 582, 1800
def line_y(frame, n):
    return 206 + 45 * (n - 1) if frame == "F1a" else 938 + 45 * (n - 31)
def strip(frame, n0, n1):
    y0 = line_y(frame, n0) - 22; y1 = line_y(frame, n1) + 23
    return (CODE_X, y0, CODE_W, y1 - y0)
OUT = [
 ("pantry/a5_ed_import_compress.png", "F4a", (8, 372, 760, 283)),
 ("pantry/a5_ed_matte_params.png", "F3a", (2548, 640, 900, 670)),
 ("pantry/a5_ed_coated_params.png", "F3b", (2548, 640, 900, 670)),
 ("pantry/a7_ed_f5b_textures.png", "F5b", (2548, 380, 900, 1005)),
 ("pantry/a7_ed_f5e_menu.png", "F5e", (2548, 760, 900, 1050)),
 ("pantry/a7_ed_gen_l3_7.png", "F1a", strip("F1a", 3, 7)),
 ("pantry/a7_ed_gen_l19.png", "F1a", strip("F1a", 19, 19)),
 ("pantry/a7_ed_gen_l35.png", "F1a", strip("F1a", 35, 35)),
 ("pantry/a7_ed_gen_l43.png", "F1b", strip("F1b", 43, 43)),
 ("pantry/a7_ed_gen_l46.png", "F1b", strip("F1b", 46, 46)),
 ("pantry/a7_ed_matte_sliders.png", "F3a", (2548, 1075, 900, 228)),
 ("pantry/a7_ed_signal_l1.png", "F2", (582 + 406, 1023 - 22, 1500, 45)),
]
for out, key, (x, y, w, h) in OUT:
    Image.open(F[key]).convert("RGB").crop((x, y, x + w, y + h)).save(out)
    print("wrote", out, (w, h), "from", key)
