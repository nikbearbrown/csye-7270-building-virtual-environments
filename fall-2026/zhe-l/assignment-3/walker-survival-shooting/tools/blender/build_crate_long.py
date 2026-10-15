# CRATE-LONG long weapon crate (built 2026-10-15)
# Every execute_blender_code body Claude Code (Claude Opus 5.5) ran through the
# Blender MCP for this asset, copied verbatim from the session transcript, in order.
# Call 1 builds, saves crate_long.blend and exports crate_long.glb with the open/close animations.
# Copy for the course repo: the absolute output paths on my machine were replaced with paths
# relative to this folder (run Blender from walker-survival-shooting/); nothing else was changed.

# ======================================================================
# Call 1 of 2, run at 2026-10-15T04:19:30.560Z (UTC)
# ======================================================================
import bpy, bmesh, os, math
from mathutils import Vector
# ---- crate_long: long military weapon crate with a hinged lid and open/close animations ----
NAME = "CrateLong"
W, D, H = 1.20, 0.50, 0.40      # width (X), depth (Y), total height (Z), metres
LID_H = 0.08                    # lid thickness
WALL = 0.02                     # body wall thickness
OUT = r".\design\item_resource\crate_long"

for o in list(bpy.data.objects): bpy.data.objects.remove(o)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.actions):
    for b in list(coll): coll.remove(b)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 1.0
sc.render.fps = 24
col = bpy.data.collections.new(NAME); sc.collection.children.link(col)

def mk(name, rgb, rough):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    m.diffuse_color = (*rgb, 1); return m
OD = mk("Crate_OliveDrab", (0.055, 0.065, 0.030), 0.85)   # matte olive drab shell
HW = mk("Crate_Hardware",  (0.018, 0.018, 0.020), 0.60)   # dark handles and latches

def box_bm(bm, size, center):
    r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r["verts"]:
        v.co = Vector((v.co.x*size[0], v.co.y*size[1], v.co.z*size[2])) + Vector(center)
    return r["verts"]

HB = H - LID_H                  # body height
# Shape 1: body = one cube with the top face removed, given wall thickness (open box)
bm = bmesh.new()
box_bm(bm, (W, D, HB), (0, 0, HB/2))
top = [f for f in bm.faces if f.normal.z > 0.9]
bmesh.ops.delete(bm, geom=top, context='FACES_ONLY')
me = bpy.data.meshes.new(NAME + "_Body"); bm.to_mesh(me); bm.free()
body = bpy.data.objects.new(NAME + "_Body", me); col.objects.link(body)
sol = body.modifiers.new("wall", 'SOLIDIFY'); sol.thickness = WALL; sol.offset = -1.0
bpy.context.view_layer.objects.active = body; bpy.ops.object.select_all(action='DESELECT'); body.select_set(True)
bpy.ops.object.modifier_apply(modifier=sol.name)
me.materials.append(OD); me.materials.append(HW)

# Shapes 2-5: two end handles (X sides) and two front latches (-Y side), dark hardware
bm = bmesh.new(); bm.from_mesh(me)
hw_verts = []
hw_verts += box_bm(bm, (0.03, 0.14, 0.03), ( W/2 + 0.015, 0, HB*0.70))
hw_verts += box_bm(bm, (0.03, 0.14, 0.03), (-W/2 - 0.015, 0, HB*0.70))
for sx in (-1, 1):
    hw_verts += box_bm(bm, (0.06, 0.015, 0.07), (sx*W*0.30, -D/2 - 0.0075, HB - 0.035))
hw = set(hw_verts)
for f in bm.faces:
    f.material_index = 1 if all(v in hw for v in f.verts) else 0
bm.to_mesh(me); bm.free()

# Shape 6: lid. Its origin is the hinge (back top edge of the body) so it rotates open about X.
bm = bmesh.new(); box_bm(bm, (W, D, LID_H), (0, -D/2, LID_H/2))
lme = bpy.data.meshes.new(NAME + "_Lid"); bm.to_mesh(lme); bm.free(); lme.materials.append(OD)
lid = bpy.data.objects.new(NAME + "_Lid", lme); col.objects.link(lid)
lid.location = (0, D/2, HB)

# Animations: "open" (0 -> 100 deg) and "close" (100 -> 0 deg), 15 frames each (0.625 s at 24 fps)
OPEN = math.radians(-100)
def make_action(act_name, a0, a1):
    lid.animation_data_create(); lid.animation_data.action = None
    lid.rotation_euler = (a0, 0, 0); lid.keyframe_insert("rotation_euler", index=0, frame=1)
    lid.rotation_euler = (a1, 0, 0); lid.keyframe_insert("rotation_euler", index=0, frame=15)
    act = lid.animation_data.action; act.name = act_name; act.use_fake_user = True
    slot = lid.animation_data.action_slot
    tr = lid.animation_data.nla_tracks.new(); tr.name = act_name
    st = tr.strips.new(act_name, 1, act)
    try: st.action_slot = slot
    except Exception: pass
    tr.mute = True
    lid.animation_data.action = None
    return act
make_action("open", 0.0, OPEN)
make_action("close", OPEN, 0.0)
lid.rotation_euler = (0, 0, 0)          # rest pose = closed
sc.frame_start, sc.frame_end = 1, 15

bpy.ops.object.select_all(action='DESELECT')
for o in (body, lid): o.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "crate_long.blend"), check_existing=False)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "crate_long.glb"), export_format='GLB',
    use_selection=True, export_apply=True, export_yup=True,
    export_animations=True, export_animation_mode='ACTIONS')

dg = bpy.context.evaluated_depsgraph_get(); tot = 0
for o in (body, lid):
    m = o.evaluated_get(dg).to_mesh(); m.calc_loop_triangles(); tot += len(m.loop_triangles)
    print(o.name, "dim", tuple(round(d,3) for d in o.dimensions), "loc", tuple(round(v,3) for v in o.location), "rot", tuple(o.rotation_euler), "scale", tuple(o.scale), "tris", len(m.loop_triangles))
print("TOTAL tris", tot, "actions", [a.name for a in bpy.data.actions])

# ======================================================================
# Call 2 of 2, run at 2026-10-15T04:19:36.112Z (UTC)
# Preview only: opened the lid in the live scene to look at it; not saved to the .blend or .glb.
# ======================================================================
import bpy, math
lid = bpy.data.objects["CrateLong_Lid"]
lid.rotation_euler = (math.radians(-100), 0, 0)

# --- 2026-10-15 revision v2: footprint on the 0.1 m grid ---

# ======================================================================
# Call 3 of 3, run at 2026-10-15T06:06:19.418Z (UTC)
# Rebuilt from scratch at 1.0 x 0.5 x 0.4 m; handles and latches fit inside the footprint. Replaces call 1's .blend and .glb.
# ======================================================================
import bpy, bmesh, os, math
from mathutils import Vector
# ---- big_box (crate_long) v2: footprint exactly 1.0 x 0.5 m = 10 x 5 grid cells (1 cell = 0.1 m) ----
# Handles and latches now sit inside the footprint: the body is shrunk by what sticks out,
# so the whole closed crate (body + handles + latches + lid) fits 1.0 x 0.5 exactly.
NAME = "CrateLong"
L, Wd, H = 1.00, 0.50, 0.40     # length (X), width (Y), total height (Z), metres
LID_H = 0.08                    # lid thickness
WALL = 0.02                     # body wall thickness
HANDLE = 0.03                   # how far each end handle sticks out (X)
LATCH = 0.015                   # how far the front latches stick out (-Y)
OUT = r".\design\item_resource\crate_long"

for o in list(bpy.data.objects): bpy.data.objects.remove(o)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.actions, bpy.data.cameras, bpy.data.lights):
    for b in list(coll): coll.remove(b)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 1.0
sc.render.fps = 24
col = bpy.data.collections.new(NAME); sc.collection.children.link(col)

def mk(name, rgb, rough):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    m.diffuse_color = (*rgb, 1); return m
OD = mk("Crate_OliveDrab", (0.055, 0.065, 0.030), 0.85)   # matte olive drab shell
HW = mk("Crate_Hardware",  (0.018, 0.018, 0.020), 0.60)   # dark handles and latches

def box_bm(bm, size, center):
    r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r["verts"]:
        v.co = Vector((v.co.x*size[0], v.co.y*size[1], v.co.z*size[2])) + Vector(center)
    return r["verts"]

BW = L - 2*HANDLE               # body length without handles
BD = Wd - LATCH                 # body width without latches
CY = LATCH/2                    # body centre shifted back so latch fronts end at y = -Wd/2
HB = H - LID_H                  # body height
# Shape 1: body = one cube with the top face removed, given wall thickness (open box)
bm = bmesh.new()
box_bm(bm, (BW, BD, HB), (0, CY, HB/2))
top = [f for f in bm.faces if f.normal.z > 0.9]
bmesh.ops.delete(bm, geom=top, context='FACES_ONLY')
me = bpy.data.meshes.new(NAME + "_Body"); bm.to_mesh(me); bm.free()
body = bpy.data.objects.new(NAME + "_Body", me); col.objects.link(body)
sol = body.modifiers.new("wall", 'SOLIDIFY'); sol.thickness = WALL; sol.offset = -1.0
bpy.context.view_layer.objects.active = body; bpy.ops.object.select_all(action='DESELECT'); body.select_set(True)
bpy.ops.object.modifier_apply(modifier=sol.name)
me.materials.append(OD); me.materials.append(HW)

# Shapes 2-5: two end handles (X ends) and two front latches (-Y side), dark hardware
bm = bmesh.new(); bm.from_mesh(me)
hw_verts = []
hw_verts += box_bm(bm, (HANDLE, 0.14, 0.03), ( BW/2 + HANDLE/2, CY, HB*0.70))
hw_verts += box_bm(bm, (HANDLE, 0.14, 0.03), (-BW/2 - HANDLE/2, CY, HB*0.70))
for sx in (-1, 1):
    hw_verts += box_bm(bm, (0.06, LATCH, 0.07), (sx*BW*0.30, -Wd/2 + LATCH/2, HB - 0.035))
hw = set(hw_verts)
for f in bm.faces:
    f.material_index = 1 if all(v in hw for v in f.verts) else 0
bm.to_mesh(me); bm.free()

# Shape 6: lid, same footprint as the body. Origin on the hinge (back top edge) so it rotates about X.
bm = bmesh.new(); box_bm(bm, (BW, BD, LID_H), (0, -BD/2, LID_H/2))
lme = bpy.data.meshes.new(NAME + "_Lid"); bm.to_mesh(lme); bm.free(); lme.materials.append(OD)
lid = bpy.data.objects.new(NAME + "_Lid", lme); col.objects.link(lid)
lid.location = (0, CY + BD/2, HB)

# Animations: "open" (0 -> 100 deg) and "close" (100 -> 0 deg), 15 frames each at 24 fps
OPEN = math.radians(-100)
def make_action(act_name, a0, a1):
    lid.animation_data_create(); lid.animation_data.action = None
    lid.rotation_euler = (a0, 0, 0); lid.keyframe_insert("rotation_euler", index=0, frame=1)
    lid.rotation_euler = (a1, 0, 0); lid.keyframe_insert("rotation_euler", index=0, frame=15)
    act = lid.animation_data.action; act.name = act_name; act.use_fake_user = True
    slot = lid.animation_data.action_slot
    tr = lid.animation_data.nla_tracks.new(); tr.name = act_name
    st = tr.strips.new(act_name, 1, act)
    try: st.action_slot = slot
    except Exception: pass
    tr.mute = True
    lid.animation_data.action = None
    return act
make_action("open", 0.0, OPEN)
make_action("close", OPEN, 0.0)
lid.rotation_euler = (0, 0, 0)          # rest pose = closed
sc.frame_start, sc.frame_end = 1, 15

bpy.ops.object.select_all(action='DESELECT')
for o in (body, lid): o.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "crate_long.blend"), check_existing=False)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "crate_long.glb"), export_format='GLB',
    use_selection=True, export_apply=True, export_yup=True,
    export_animations=True, export_animation_mode='ACTIONS')

dg = bpy.context.evaluated_depsgraph_get(); tot = 0; lo = Vector((9,9,9)); hi = Vector((-9,-9,-9))
for o in (body, lid):
    m = o.evaluated_get(dg).to_mesh(); m.calc_loop_triangles(); tot += len(m.loop_triangles)
    for v in m.vertices:
        w = o.matrix_world @ v.co; lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
print("bounds min", tuple(round(c,4) for c in lo), "max", tuple(round(c,4) for c in hi), "size", tuple(round(c,4) for c in hi-lo))
print("TOTAL tris", tot, "actions", [a.name for a in bpy.data.actions])

# --- 2026-10-15 revision v3: my hand edit on the small crate applied to the big crate ---

# ======================================================================
# Call 4 of 4 (script route, not the MCP): run headless by Claude Code with
#   blender -b --factory-startup --python-exit-code 1 --python <this section>
# ======================================================================
import bpy, bmesh, os, math
from mathutils import Vector
# ---- big_box (crate_long) v3 (2026-10-15): my hand edit on the small crate copied over.
#      Handles moved up (centre 0.048 m below the body rim, same as the small crate) and the
#      latches centred on the lid/body seam (half on the lid, half on the body). Was v2: footprint exactly 1.0 x 0.5 m = 10 x 5 grid cells (1 cell = 0.1 m) ----
# Handles and latches now sit inside the footprint: the body is shrunk by what sticks out,
# so the whole closed crate (body + handles + latches + lid) fits 1.0 x 0.5 exactly.
NAME = "CrateLong"
L, Wd, H = 1.00, 0.50, 0.40     # length (X), width (Y), total height (Z), metres
LID_H = 0.08                    # lid thickness
WALL = 0.02                     # body wall thickness
HANDLE = 0.03                   # how far each end handle sticks out (X)
LATCH = 0.015                   # how far the front latches stick out (-Y)
OUT = r".\design\item_resource\crate_long"

for o in list(bpy.data.objects): bpy.data.objects.remove(o)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.actions, bpy.data.cameras, bpy.data.lights):
    for b in list(coll): coll.remove(b)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 1.0
sc.render.fps = 24
col = bpy.data.collections.new(NAME); sc.collection.children.link(col)

def mk(name, rgb, rough):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    m.diffuse_color = (*rgb, 1); return m
OD = mk("Crate_OliveDrab", (0.055, 0.065, 0.030), 0.85)   # matte olive drab shell
HW = mk("Crate_Hardware",  (0.018, 0.018, 0.020), 0.60)   # dark handles and latches

def box_bm(bm, size, center):
    r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r["verts"]:
        v.co = Vector((v.co.x*size[0], v.co.y*size[1], v.co.z*size[2])) + Vector(center)
    return r["verts"]

BW = L - 2*HANDLE               # body length without handles
BD = Wd - LATCH                 # body width without latches
CY = LATCH/2                    # body centre shifted back so latch fronts end at y = -Wd/2
HB = H - LID_H                  # body height
# Shape 1: body = one cube with the top face removed, given wall thickness (open box)
bm = bmesh.new()
box_bm(bm, (BW, BD, HB), (0, CY, HB/2))
top = [f for f in bm.faces if f.normal.z > 0.9]
bmesh.ops.delete(bm, geom=top, context='FACES_ONLY')
me = bpy.data.meshes.new(NAME + "_Body"); bm.to_mesh(me); bm.free()
body = bpy.data.objects.new(NAME + "_Body", me); col.objects.link(body)
sol = body.modifiers.new("wall", 'SOLIDIFY'); sol.thickness = WALL; sol.offset = -1.0
bpy.context.view_layer.objects.active = body; bpy.ops.object.select_all(action='DESELECT'); body.select_set(True)
bpy.ops.object.modifier_apply(modifier=sol.name)
me.materials.append(OD); me.materials.append(HW)

# Shapes 2-5: two end handles (X ends) and two front latches (-Y side), dark hardware
bm = bmesh.new(); bm.from_mesh(me)
hw_verts = []
HANDLE_Z = HB - 0.048           # handle centre: 0.048 m below the body rim (from the small crate edit)
hw_verts += box_bm(bm, (HANDLE, 0.14, 0.03), ( BW/2 + HANDLE/2, CY, HANDLE_Z))
hw_verts += box_bm(bm, (HANDLE, 0.14, 0.03), (-BW/2 - HANDLE/2, CY, HANDLE_Z))
for sx in (-1, 1):
    hw_verts += box_bm(bm, (0.06, LATCH, 0.07), (sx*BW*0.30, -Wd/2 + LATCH/2, HB))   # latch centred on the seam
hw = set(hw_verts)
for f in bm.faces:
    f.material_index = 1 if all(v in hw for v in f.verts) else 0
bm.to_mesh(me); bm.free()

# Shape 6: lid, same footprint as the body. Origin on the hinge (back top edge) so it rotates about X.
bm = bmesh.new(); box_bm(bm, (BW, BD, LID_H), (0, -BD/2, LID_H/2))
lme = bpy.data.meshes.new(NAME + "_Lid"); bm.to_mesh(lme); bm.free(); lme.materials.append(OD)
lid = bpy.data.objects.new(NAME + "_Lid", lme); col.objects.link(lid)
lid.location = (0, CY + BD/2, HB)

# Animations: "open" (0 -> 100 deg) and "close" (100 -> 0 deg), 15 frames each at 24 fps
OPEN = math.radians(-100)
def make_action(act_name, a0, a1):
    lid.animation_data_create(); lid.animation_data.action = None
    lid.rotation_euler = (a0, 0, 0); lid.keyframe_insert("rotation_euler", index=0, frame=1)
    lid.rotation_euler = (a1, 0, 0); lid.keyframe_insert("rotation_euler", index=0, frame=15)
    act = lid.animation_data.action; act.name = act_name; act.use_fake_user = True
    slot = lid.animation_data.action_slot
    tr = lid.animation_data.nla_tracks.new(); tr.name = act_name
    st = tr.strips.new(act_name, 1, act)
    try: st.action_slot = slot
    except Exception: pass
    tr.mute = True
    lid.animation_data.action = None
    return act
make_action("open", 0.0, OPEN)
make_action("close", OPEN, 0.0)
lid.rotation_euler = (0, 0, 0)          # rest pose = closed
sc.frame_start, sc.frame_end = 1, 15

bpy.ops.object.select_all(action='DESELECT')
for o in (body, lid): o.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "crate_long.blend"), check_existing=False)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "crate_long.glb"), export_format='GLB',
    use_selection=True, export_apply=True, export_yup=True,
    export_animations=True, export_animation_mode='ACTIONS')

dg = bpy.context.evaluated_depsgraph_get(); tot = 0; lo = Vector((9,9,9)); hi = Vector((-9,-9,-9))
for o in (body, lid):
    m = o.evaluated_get(dg).to_mesh(); m.calc_loop_triangles(); tot += len(m.loop_triangles)
    for v in m.vertices:
        w = o.matrix_world @ v.co; lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
print("bounds min", tuple(round(c,4) for c in lo), "max", tuple(round(c,4) for c in hi), "size", tuple(round(c,4) for c in hi-lo))
print("TOTAL tris", tot, "actions", [a.name for a in bpy.data.actions])
