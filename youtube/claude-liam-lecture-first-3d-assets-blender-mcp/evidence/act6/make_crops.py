"""make_crops.py - act VI's pantry crops (pantry/a6_*.png), cut from the real captures and renders with PIL. Pixel boxes are in each
source PNG's own pixels (origin top-left), taken from evidence/gui/NOTES.md and from looking at the images. No pixel is altered.
Run from the reel folder: python3 evidence/act6/make_crops.py"""
from PIL import Image
P = "pantry/"
CROPS = {
    # the glTF export dialog's right-hand column: Format "glTF Binary (.glb)" ... Transform > "+Y Up" (ticked) ... Animation
    "a6_export_opts.png":   ("ev_bl_export_gltf.png", (2540, 292, 3456, 1080)),
    # Blender's File menu with Export open and its submenu (glTF 2.0 (.glb/.gltf) is the last row); see run_file_export.sh
    "a6_file_menu.png":     ("a6_bl_file_export.png", (0, 0, 1800, 1330)),
    # inside the Export submenu panel only (no icons, no row highlight): Alembic ... glTF 2.0 (.glb/.gltf)
    "a6_export_submenu.png": ("a6_bl_file_export.png", (862, 500, 1778, 1312)),
    # the status bar strip with Scene Statistics on: "Collection | Lantern | Verts:111 | Faces:91 | Tris:202 | Objects:1/1"
    "a6_statusbar.png":     ("ev_bl_status_stats.png", (1830, 1915, 3166, 2004)),
    # the lantern renders (transparent), one shared box so the three views keep one scale
    "a6_lantern_34.png":    ("ev_lantern_34.png", (927, 275, 1475, 1142)),
    "a6_lantern_back.png":  ("ev_lantern_back.png", (927, 275, 1475, 1142)),
    "a6_lantern_below.png": ("ev_lantern_below.png", (927, 275, 1475, 1142)),
}
for out, (src, box) in CROPS.items():
    im = Image.open(P + src).crop(box)
    im.save(P + out)
    print(out, "<-", src, box, im.size, im.mode)
