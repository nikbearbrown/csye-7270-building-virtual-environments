# ENV-SEAT-TEST-01 test chair (built 2026-10-07 local time)
# Every execute_blender_code body Claude Code (Claude Opus 5.5) ran through the
# Blender MCP for this asset, copied verbatim from the session transcript, in order.
# Each section was a separate call in the same live Blender session; run top to bottom.
# Call 3 exports to an absolute path on my machine; change it before running elsewhere.
# Copy for the course repo: the absolute output paths on my machine were replaced with paths
# relative to this folder (run Blender from walker-survival-shooting/); nothing else was changed.

# ======================================================================
# Call 1 of 3, run at 2026-10-08T01:54:36.945Z (UTC)
# ======================================================================
import bpy, bmesh
from mathutils import Vector

cube = bpy.data.objects.get("Cube")
if cube:
    cube.hide_set(True); cube.hide_render = True

col = bpy.data.collections.get("TestChair") or bpy.data.collections.new("TestChair")
if col.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(col)

# matte dark material (Principled BSDF looked up by type)
mat = bpy.data.materials.get("TestChair_Matte") or bpy.data.materials.new("TestChair_Matte")
mat.use_nodes = True
bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
bsdf.inputs["Base Color"].default_value = (0.08, 0.085, 0.1, 1)
bsdf.inputs["Roughness"].default_value = 0.85
bsdf.inputs["Metallic"].default_value = 0.0

def box(name, size, loc):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x*size[0], v.co.y*size[1], v.co.z*size[2]))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    col.objects.link(ob)
    return ob

# dimensions in metres (typical dining chair)
seat_h, seat_w, seat_d, seat_t = 0.45, 0.44, 0.42, 0.04
leg = 0.035
parts = []
parts.append(box("seat", (seat_w, seat_d, seat_t), (0, 0, seat_h - seat_t/2)))
for sx in (-1, 1):
    for sy in (-1, 1):
        x = sx*(seat_w/2 - leg/2); y = sy*(seat_d/2 - leg/2)
        h = seat_h - seat_t if sy < 0 else 0.90   # back legs run up into the backrest
        parts.append(box("leg", (leg, leg, h), (x, y, h/2)))
# backrest: two horizontal slats between the back legs
for z in (0.62, 0.82):
    parts.append(box("slat", (seat_w - 2*leg, 0.02, 0.07), (0, seat_d/2 - leg/2, z)))
# stretchers between legs
parts.append(box("stretcher", (seat_w - 2*leg, 0.02, 0.025), (0, -(seat_d/2 - leg/2), 0.15)))
parts.append(box("stretcher", (seat_w - 2*leg, 0.02, 0.025), (0, (seat_d/2 - leg/2), 0.15)))

for o in bpy.context.view_layer.objects: o.select_set(False)
for p in parts: p.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
chair = bpy.context.view_layer.objects.active
chair.name = "TestChair"
chair.data.name = "TestChair"
chair.data.materials.clear(); chair.data.materials.append(mat)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
chair.location.z = chair.dimensions.z/2   # sit on the ground
bpy.ops.object.origin_set(type='ORIGIN_CURSOR') if False else None
print(chair.name, tuple(round(d,3) for d in chair.dimensions), "faces:", len(chair.data.polygons))

# ======================================================================
# Call 2 of 3, run at 2026-10-08T01:54:47.366Z (UTC)
# ======================================================================
import bpy
from mathutils import Vector
ch = bpy.data.objects["TestChair"]
me = ch.data
xs=[v.co.x for v in me.vertices]; ys=[v.co.y for v in me.vertices]; zs=[v.co.z for v in me.vertices]
off = Vector(((min(xs)+max(xs))/2, (min(ys)+max(ys))/2, min(zs)))
for v in me.vertices: v.co -= off   # origin = bottom centre (good for Godot placement)
ch.location = (0, 0, 0)
me.update()
print([round(c,3) for c in ch.bound_box[0]], [round(c,3) for c in ch.bound_box[6]])

# ======================================================================
# Call 3 of 3, run at 2026-10-08T02:44:01.707Z (UTC)
# ======================================================================
import bpy, os
out_dir = r".\godot\assets\furniture"
os.makedirs(out_dir, exist_ok=True)
path = os.path.join(out_dir, "test_chair.glb")
ch = bpy.data.objects["TestChair"]
for o in bpy.context.view_layer.objects: o.select_set(False)
ch.select_set(True); bpy.context.view_layer.objects.active = ch
bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
print(path, os.path.getsize(path), "bytes")

# --- 2026-10-15 revision (later session) ---

# ======================================================================
# Call 4 of 4, run at 2026-10-15T04:18:42.270Z (UTC)
# Fresh scene, re-run calls 1-2 above, rename to Chair, save chair.blend and export chair.glb to design/item_resource/chair/. (An earlier attempt the same minute failed: it split this file on the wrong marker.)
# ======================================================================
import bpy, os, re
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.actions):
    for b in list(coll): coll.remove(b)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
sc = bpy.context.scene
sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 1.0

# Rebuild the chair with the exact code that built it on 2026-10-07 (build_chair.py calls 1 and 2)
src = open(r".\tools\blender\build_chair.py", encoding="utf-8").read()
calls = re.split(r"# =+\n# Call \d of \d, run at .*\n# =+\n", src)[1:]
for code in calls[:2]:
    exec(compile(code, "chair", "exec"), {"__name__": "__main__"})

ch = bpy.data.objects["TestChair"]
ch.name = "Chair"; ch.data.name = "Chair"
for c in bpy.data.collections: c.name = "Chair"
OUT = r".\design\item_resource\chair"
bpy.ops.object.select_all(action='DESELECT'); ch.select_set(True); bpy.context.view_layer.objects.active = ch
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "chair.blend"), check_existing=False)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "chair.glb"), export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
dg = bpy.context.evaluated_depsgraph_get(); m = ch.evaluated_get(dg).to_mesh(); m.calc_loop_triangles()
print(ch.name, tuple(round(d,3) for d in ch.dimensions), "tris", len(m.loop_triangles), "loc", tuple(ch.location), "rot", tuple(ch.rotation_euler), "scale", tuple(ch.scale))
