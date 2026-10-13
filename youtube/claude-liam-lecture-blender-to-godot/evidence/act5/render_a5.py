# Act V evidence: re-renders the REAL checkpoint post (the script the first agent actually produced, run 1: collision BOX)
# with Blender's own Workbench engine, same camera + materials as evidence/render_post.py, at 2x resolution, and exports the
# camera projection of the key 3D points so every dimension mark in the film sits on the real pixels.
#
# Run:  Blender -b --factory-startup --python-exit-code 1 --python render_a5.py -- <out_dir>
# Writes: <out_dir>/a5_post_full.png, a5_box_full.png (transparent, 4800x2700), post_anchors_full.json
#         (post-processing to cropped pantry files + crop-space anchors: crop_a5.py)
import bpy, sys, os, shutil, tempfile, runpy, json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

out = sys.argv[sys.argv.index("--") + 1]
os.makedirs(out, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
EXAMPLES = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "examples", "03-blender-mcp-to-godot"))
SRC = os.path.join(EXAMPLES, "scripts", "agent", "build_checkpoint_post.run1.py")

# the agent's script writes its .glb relative to its own location, so run a COPY inside a scratch folder (examples/ stays untouched)
tmp = tempfile.mkdtemp(prefix="a5_post_")
os.makedirs(os.path.join(tmp, "tools", "blender"))
dst = os.path.join(tmp, "tools", "blender", "build_checkpoint_post.py")
shutil.copy(SRC, dst)
runpy.run_path(dst, run_name="__main__")

sc = bpy.context.scene
col = bpy.data.objects["Collision-convcolonly"]
for m in bpy.data.materials:
    if m.name == "PostMetal": m.diffuse_color = (0.50, 0.52, 0.58, 1.0)
    if m.name == "FlagCloth": m.diffuse_color = (0.85, 0.30, 0.20, 1.0)

RES = (4800, 2700)
LOC, TARGET, LENS = (3.9, -4.6, 2.0), (0.12, 0.0, 0.9), 42     # same camera as evidence/render_post.py 'post_visual'
cd = bpy.data.cameras.new("RenderCam"); cam = bpy.data.objects.new("RenderCam", cd)
bpy.context.collection.objects.link(cam)
cam.data.lens = LENS; cam.location = LOC
tgt = bpy.data.objects.new("RenderTarget", None); bpy.context.collection.objects.link(tgt); tgt.location = TARGET
c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
sc.camera = cam
sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.film_transparent = True
sc.render.resolution_x, sc.render.resolution_y = RES
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sh = sc.display.shading
sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'; sh.show_cavity = False; sh.show_object_outline = True
sh.object_outline_color = (0.24, 0.22, 0.16)
bpy.context.view_layer.update()

def render(name, only_box, everything=False):
    col.hide_render = not (only_box or everything)
    for n in ("Base", "Pole", "Pennant"):
        bpy.data.objects[n].hide_render = only_box
    sc.render.filepath = os.path.join(out, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", sc.render.filepath)

render("a5_post_full", only_box=False)
render("a5_box_full", only_box=True)
# What the imported collider looks like when Godot keeps it as a MeshInstance3D (use_node_type_suffixes=false): an opaque default-grey box
# standing around the post. The box is enlarged 0.4% for THIS render only, so its faces do not z-fight with the base's coplanar sides.
col.scale = (1.004, 1.004, 1.004)
render("a5_boxopaque_full", only_box=False, everything=True)
col.scale = (1.0, 1.0, 1.0)

def px(p):
    v = world_to_camera_view(sc, cam, Vector(p))
    return [round(v.x * RES[0], 2), round((1.0 - v.y) * RES[1], 2)]     # pixel coords, origin top-left

pts = {}
for zi, z in (("0", 0.0), ("1", 0.1)):
    for xi, x in (("m", -0.3), ("p", 0.3)):
        for yi, y in (("m", -0.3), ("p", 0.3)):
            pts[f"base_{xi}{yi}_{zi}"] = px((x, y, z))
for xi, x in (("m", -0.3), ("p", 0.3)):
    for yi, y in (("m", -0.3), ("p", 0.3)):
        for zi, z in (("0", 0.0), ("18", 1.8)):
            pts[f"box_{xi}{yi}_{zi}"] = px((x, y, z))
pts["pole_top_c"] = px((0, 0, 1.8)); pts["pole_bot_c"] = px((0, 0, 0.1))
import math
for i in range(8):
    a = 2 * math.pi * i / 8
    pts[f"pole_top_{i}"] = px((0.08 * math.cos(a), 0.08 * math.sin(a), 1.8))
pts["pen_tl"] = px((0.08, 0, 1.8)); pts["pen_tr"] = px((0.48, 0, 1.8))
pts["pen_br"] = px((0.48, 0, 1.55)); pts["pen_bl"] = px((0.08, 0, 1.55))
# dimension-line carriers (offset in 3D, then projected)
pts["w_a"] = px((-0.3, -0.55, 0.0)); pts["w_b"] = px((0.3, -0.55, 0.0))            # base width, 0.6 m, in front of the front-left edge
pts["h_a"] = px((-0.55, -0.55, 0.0)); pts["h_b"] = px((-0.55, -0.55, 1.8))          # height, 1.8 m, left of the post
pts["t_edge"] = px((-0.3, -0.3, 0.05))                                              # base thickness: the corner edge's midpoint
pts["pen_len_a"] = px((0.08, -0.12, 1.8)); pts["pen_len_b"] = px((0.48, -0.12, 1.8))  # pennant 0.4 m, along +X, just above... see film
pts["pen_h_a"] = px((0.55, 0.0, 1.8)); pts["pen_h_b"] = px((0.55, 0.0, 1.55))        # pennant 0.25 m tall, beside its free edge
# floor plane for the ghost tile and the ray
for k, (x, y) in {"floor_a": (-0.95, -0.95), "floor_b": (0.95, -0.95), "floor_c": (0.95, 0.95), "floor_d": (-0.95, 0.95)}.items():
    pts[k] = px((x, y, 0.0))
pts["ray_top"] = px((0, 0, 2.0)); pts["ray_bot"] = px((0, 0, 0.0))
pts["lift16"] = px((0, 0, 0.16))                                                      # the 16 cm the post floated, projected at the pole's foot
pts["z0_c"] = px((0, 0, 0.0))
pts["lift158"] = px((0, 0, 0.15811)); pts["ray_start158"] = px((0, 0, 2.15811))        # base y -3.84189 vs floor y -4.0; ray starts 2 m above the base
json.dump({"res": RES, "camera": {"loc": LOC, "target": TARGET, "lens_mm": LENS}, "pts": pts}, open(os.path.join(out, "post_anchors_full.json"), "w"), indent=1)
print("anchors", len(pts))
shutil.rmtree(tmp, ignore_errors=True)
