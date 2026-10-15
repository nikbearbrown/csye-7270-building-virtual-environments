# COMPUTER-DESK straight computer desk (built 2026-10-15)
# Every execute_blender_code body Claude Code (Claude Opus 5.5) ran through the
# Blender MCP for this asset, copied verbatim from the session transcript.
# Copy for the course repo: the absolute output paths on my machine were replaced with paths
# relative to this folder (run Blender from walker-survival-shooting/); nothing else was changed.

# ======================================================================
# Call 1 of 1, run at 2026-10-15T20:32:11.117Z (UTC)
# ======================================================================
import bpy, bmesh, os
from mathutils import Vector
# ---- computer_desk: straight computer desk, footprint 1.5 x 0.5 m = 15 x 5 grid cells (1 cell = 0.1 m) ----
# Desktop 0.70 m high; dark-grey metal top, dark legs, monitor riser along the back edge.
# 6 shapes: desktop, 4 legs, monitor riser. Front of the desk (where the player sits) is -Y.
NAME = "ComputerDesk"
L, Wd = 1.50, 0.50              # length (X), width (Y), metres
TOP_H, TOP_T = 0.70, 0.03       # desktop surface height, desktop thickness
LEG = 0.04                      # square leg size
RISER = (1.20, 0.22, 0.08)      # monitor riser: length, depth, height
OUT = r".\design\item_resource\computer_desk"
os.makedirs(OUT, exist_ok=True)

for o in list(bpy.data.objects): bpy.data.objects.remove(o)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.actions, bpy.data.cameras, bpy.data.lights):
    for b in list(coll): coll.remove(b)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 1.0
col = bpy.data.collections.new(NAME); sc.collection.children.link(col)

def mk(name, rgb, rough, metal):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    m.diffuse_color = (*rgb, 1); return m
GREY = mk("Desk_DarkGreyMetal", (0.045, 0.048, 0.052), 0.55, 0.6)   # desktop
DARK = mk("Desk_Dark",          (0.012, 0.012, 0.014), 0.70, 0.3)   # legs and riser

def box_bm(bm, size, center):
    r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r["verts"]:
        v.co = Vector((v.co.x*size[0], v.co.y*size[1], v.co.z*size[2])) + Vector(center)
    return r["verts"]

bm = bmesh.new(); dark = []
box_bm(bm, (L, Wd, TOP_T), (0, 0, TOP_H - TOP_T/2))                       # 1 desktop
LH = TOP_H - TOP_T
for sx in (-1, 1):
    for sy in (-1, 1):                                                     # 2-5 legs, flush with the corners
        dark += box_bm(bm, (LEG, LEG, LH), (sx*(L/2 - LEG/2), sy*(Wd/2 - LEG/2), LH/2))
dark += box_bm(bm, RISER, (0, Wd/2 - RISER[1]/2 - 0.02, TOP_H + RISER[2]/2))  # 6 monitor riser, 2 cm in from the back
dk = set(dark)
me = bpy.data.meshes.new(NAME); me.materials.append(GREY); me.materials.append(DARK)
for f in bm.faces: f.material_index = 1 if all(v in dk for v in f.verts) else 0
bm.to_mesh(me); bm.free()
desk = bpy.data.objects.new(NAME, me); col.objects.link(desk)

bpy.ops.object.select_all(action='DESELECT'); desk.select_set(True); bpy.context.view_layer.objects.active = desk
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "computer_desk.blend"), check_existing=False)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "computer_desk.glb"), export_format='GLB',
    use_selection=True, export_apply=True, export_yup=True)

dg = bpy.context.evaluated_depsgraph_get(); m = desk.evaluated_get(dg).to_mesh(); m.calc_loop_triangles()
bb = [desk.matrix_world @ Vector(c) for c in desk.bound_box]
lo = Vector(map(min, *bb)); hi = Vector(map(max, *bb))
print("bounds min", tuple(round(c,4) for c in lo), "max", tuple(round(c,4) for c in hi), "tris", len(m.loop_triangles), "scale", tuple(desk.scale))
