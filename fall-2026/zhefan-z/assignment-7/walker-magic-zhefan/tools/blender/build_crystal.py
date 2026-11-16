# build_crystal.py — Asset 2 (Crystal), Assignment 3.
# Verbatim record of every execute_blender_code body Claude Code ran through MCP for Blender 2.1.9
# (add-on 1.8) in Blender 5.2.2 LTS on 2026-10-14, in run order. Only this header, the
# "# --- call N" separator lines and the "# --- (stopped here ...)" note were added.

# --- call 1: start a new Blender file (asked for by Zhefan before the Crystal; prints the state before)
# Start a new Blender file from the factory/home startup (no app template). Prints the state before.
import bpy

print("before: file", repr(bpy.data.filepath), "| unsaved changes:", bpy.data.is_dirty,
      "| objects:", [o.name for o in bpy.data.objects])
bpy.ops.wm.read_homefile(app_template="")
print("after: file", repr(bpy.data.filepath), "| objects:", [o.name for o in bpy.data.objects])

# --- call 2: clear the scene and confirm metric units
# Clear the scene: remove every object, then the mesh/material/light/camera data left unused.
import bpy

for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
    for block in list(coll):
        if block.users == 0:
            coll.remove(block)

us = bpy.context.scene.unit_settings
us.system = 'METRIC'
us.scale_length = 1.0
us.length_unit = 'METERS'

print("objects:", len(bpy.data.objects), "meshes:", len(bpy.data.meshes),
      "materials:", [m.name for m in bpy.data.materials])
print("units:", us.system, us.length_unit, us.scale_length)

# --- call 3: Crystal material
# Crystal material: #3558C8 is sRGB; Principled BSDF Base Color and Emission Color take linear values.
# Weak emission in the same colour (strength 0.5), roughness 0.3, metallic 0.
import bpy

def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

NAME, HEX = "Crystal", "3558C8"
EMISSION_STRENGTH, ROUGHNESS = 0.5, 0.3

rgb = [srgb_to_linear(int(HEX[i:i + 2], 16)) for i in (0, 2, 4)]
mat = bpy.data.materials.get(NAME) or bpy.data.materials.new(NAME)
mat.use_nodes = True
bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
bsdf.inputs["Emission Strength"].default_value = EMISSION_STRENGTH
bsdf.inputs["Metallic"].default_value = 0.0
bsdf.inputs["Roughness"].default_value = ROUGHNESS
mat.diffuse_color = (*rgb, 1.0)  # viewport (Solid mode) colour only

print(NAME, "#" + HEX, "-> linear", tuple(round(v, 4) for v in rgb))
print("Base Color", tuple(round(v, 4) for v in bsdf.inputs["Base Color"].default_value),
      "| Emission Color", tuple(round(v, 4) for v in bsdf.inputs["Emission Color"].default_value),
      "| Emission Strength", bsdf.inputs["Emission Strength"].default_value,
      "| Roughness", round(bsdf.inputs["Roughness"].default_value, 3),
      "| Metallic", bsdf.inputs["Metallic"].default_value)

# --- call 4: Crystal_Tall
# Crystal_Tall: 6-vertex cone, origin at its base centre (so a mouse rotation pivots at the base).
# Defined by base centre and tip; length and lean are solved from the real world-space vertices,
# then the cone is lifted so its lowest vertex is at Z = 0 and the tip lands on TIP.
import bpy, math
from mathutils import Vector

NAME, MAT = "Crystal_Tall", "Crystal"
RADIUS = 0.08
BASE_XY = (0.0, 0.0)
TIP = Vector((-0.01, 0.175, 0.60))

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=RADIUS, radius2=0.0, depth=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
me = ob.data

# Unit-length cone with its base centre at the mesh origin: base ring at z = 0, tip at z = 1.
unit = [v.co.copy() + Vector((0, 0, 0.5)) for v in me.vertices]
tip_i = max(range(len(unit)), key=lambda i: unit[i].z)

base = Vector((BASE_XY[0], BASE_XY[1], 0.0))
aim = TIP.copy()
for _ in range(20):
    d = aim - base
    length = d.length
    for v, u in zip(me.vertices, unit):
        v.co = Vector((u.x, u.y, u.z * length))
    me.update()
    ob.rotation_mode = "XYZ"
    ob.rotation_euler = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_euler("XYZ")
    ob.location = base
    bpy.context.view_layer.update()
    lift = -min((ob.matrix_world @ v.co).z for v in me.vertices)
    ob.location = base + Vector((0, 0, lift))
    bpy.context.view_layer.update()
    err = TIP - ob.matrix_world @ me.vertices[tip_i].co
    if err.length < 1e-6:
        break
    aim += err

ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in me.vertices]
wx, wy, wz = zip(*w)
lean = math.degrees((ob.matrix_world.to_3x3() @ Vector((0, 0, 1))).angle(Vector((0, 0, 1))))
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4))
print("length", round(length, 4), "| lean", round(lean, 1), "deg | tip", tuple(round(c, 4) for c in w[tip_i]),
      "| base centre", tuple(round(c, 4) for c in ob.location), "| triangles:", sum(len(p.vertices) - 2 for p in me.polygons))

# --- call 5: Crystal_Short_A
# Crystal_Short_A: 6-vertex cone, origin at its base centre (so a mouse rotation pivots at the base).
# Same method as Crystal_Tall: length and lean solved from the real world-space vertices,
# lifted so its lowest vertex is at Z = 0, tip on TIP. Leans front-right.
import bpy, math
from mathutils import Vector

NAME, MAT = "Crystal_Short_A", "Crystal"
RADIUS = 0.065
BASE_XY = (0.02, -0.02)
TIP = Vector((0.175, -0.175, 0.34))

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=RADIUS, radius2=0.0, depth=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
me = ob.data

# Unit-length cone with its base centre at the mesh origin: base ring at z = 0, tip at z = 1.
unit = [v.co.copy() + Vector((0, 0, 0.5)) for v in me.vertices]
tip_i = max(range(len(unit)), key=lambda i: unit[i].z)

base = Vector((BASE_XY[0], BASE_XY[1], 0.0))
aim = TIP.copy()
for _ in range(20):
    d = aim - base
    length = d.length
    for v, u in zip(me.vertices, unit):
        v.co = Vector((u.x, u.y, u.z * length))
    me.update()
    ob.rotation_mode = "XYZ"
    ob.rotation_euler = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_euler("XYZ")
    ob.location = base
    bpy.context.view_layer.update()
    lift = -min((ob.matrix_world @ v.co).z for v in me.vertices)
    ob.location = base + Vector((0, 0, lift))
    bpy.context.view_layer.update()
    err = TIP - ob.matrix_world @ me.vertices[tip_i].co
    if err.length < 1e-6:
        break
    aim += err

ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in me.vertices]
wx, wy, wz = zip(*w)
lean = math.degrees((ob.matrix_world.to_3x3() @ Vector((0, 0, 1))).angle(Vector((0, 0, 1))))
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4))
print("length", round(length, 4), "| lean", round(lean, 1), "deg | tip", tuple(round(c, 4) for c in w[tip_i]),
      "| base centre", tuple(round(c, 4) for c in ob.location), "| triangles:", sum(len(p.vertices) - 2 for p in me.polygons))

# --- call 6: Crystal_Short_B, then the "before" values of all three cones
# Crystal_Short_B: 6-vertex cone, origin at its base centre (so a mouse rotation pivots at the base).
# Same method as Crystal_Tall: length and lean solved from the real world-space vertices,
# lifted so its lowest vertex is at Z = 0, tip on TIP. Leans left. Then reports all three cones
# ("before" values for the hand edit) and their combined world vertex bounds.
import bpy, math
from mathutils import Vector

NAME, MAT = "Crystal_Short_B", "Crystal"
RADIUS = 0.055
BASE_XY = (-0.02, -0.01)
TIP = Vector((-0.175, -0.05, 0.28))

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=RADIUS, radius2=0.0, depth=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
me = ob.data

# Unit-length cone with its base centre at the mesh origin: base ring at z = 0, tip at z = 1.
unit = [v.co.copy() + Vector((0, 0, 0.5)) for v in me.vertices]
tip_i = max(range(len(unit)), key=lambda i: unit[i].z)

base = Vector((BASE_XY[0], BASE_XY[1], 0.0))
aim = TIP.copy()
for _ in range(20):
    d = aim - base
    length = d.length
    for v, u in zip(me.vertices, unit):
        v.co = Vector((u.x, u.y, u.z * length))
    me.update()
    ob.rotation_mode = "XYZ"
    ob.rotation_euler = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_euler("XYZ")
    ob.location = base
    bpy.context.view_layer.update()
    lift = -min((ob.matrix_world @ v.co).z for v in me.vertices)
    ob.location = base + Vector((0, 0, lift))
    bpy.context.view_layer.update()
    err = TIP - ob.matrix_world @ me.vertices[tip_i].co
    if err.length < 1e-6:
        break
    aim += err

ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in me.vertices]
wx, wy, wz = zip(*w)
lean = math.degrees((ob.matrix_world.to_3x3() @ Vector((0, 0, 1))).angle(Vector((0, 0, 1))))
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4))
print("length", round(length, 4), "| lean", round(lean, 1), "deg | tip", tuple(round(c, 4) for c in w[tip_i]),
      "| base centre", tuple(round(c, 4) for c in ob.location), "| triangles:", sum(len(p.vertices) - 2 for p in me.polygons))

# "Before" values for the hand edit, and the combined bounds of all three cones.
print("--- before the hand edit")
allw = []
for n in ("Crystal_Tall", "Crystal_Short_A", "Crystal_Short_B"):
    o = bpy.data.objects[n]
    pw = [o.matrix_world @ v.co for v in o.data.vertices]
    allw += pw
    px, py, pz = zip(*pw)
    print(n, "| location", tuple(round(c, 4) for c in o.location),
          "| rotation deg", tuple(round(math.degrees(a), 2) for a in o.rotation_euler),
          "| scale", tuple(round(c, 4) for c in o.scale),
          "| world size", round(max(px) - min(px), 4), round(max(py) - min(py), 4), round(max(pz) - min(pz), 4))
ax, ay, az = zip(*allw)
print("combined: x", round(min(ax), 4), round(max(ax), 4), "| y", round(min(ay), 4), round(max(ay), 4),
      "| z", round(min(az), 4), round(max(az), 4),
      "| size", round(max(ax) - min(ax), 4), round(max(ay) - min(ay), 4), round(max(az) - min(az), 4),
      "| triangles", sum(sum(len(p.vertices) - 2 for p in bpy.data.objects[n].data.polygons)
                         for n in ("Crystal_Tall", "Crystal_Short_A", "Crystal_Short_B")))

# --- call 7: shared-base check (read-only)
# Read-only: do the three cones meet in a shared base? Pairwise mesh intersection in world space.
import bpy
from mathutils.bvhtree import BVHTree

def world_bvh(o):
    m = o.matrix_world
    return BVHTree.FromPolygons([m @ v.co for v in o.data.vertices], [p.vertices[:] for p in o.data.polygons])

names = ("Crystal_Tall", "Crystal_Short_A", "Crystal_Short_B")
trees = {n: world_bvh(bpy.data.objects[n]) for n in names}
for i, a in enumerate(names):
    for b in names[i + 1:]:
        print(a, "x", b, "intersecting face pairs:", len(trees[a].overlap(trees[b])))

# --- (stopped here 2026-10-14 for Zhefan's hand edit in the viewport: rotating one cone with the mouse)

# --- call 8: re-measure after the hand edit (read-only); every value came back identical to call 6
# Read-only: re-measure the three cones after Zhefan's hand edit ("after" values), the combined bounds,
# the shared-base intersections, and anything else in the scene that changed.
import bpy, math
from mathutils.bvhtree import BVHTree

names = ("Crystal_Tall", "Crystal_Short_A", "Crystal_Short_B")
print("mode:", bpy.context.mode, "| file:", repr(bpy.data.filepath), "| unsaved changes:", bpy.data.is_dirty)
print("objects:", [(o.name, o.type) for o in bpy.data.objects], "| meshes:", [m.name for m in bpy.data.meshes],
      "| materials:", [m.name for m in bpy.data.materials])
print("--- after the hand edit")
allw = []
for n in names:
    o = bpy.data.objects[n]
    pw = [o.matrix_world @ v.co for v in o.data.vertices]
    allw += pw
    px, py, pz = zip(*pw)
    tip = max(pw, key=lambda p: (p - o.matrix_world.translation).length)
    print(n, "| location", tuple(round(c, 4) for c in o.location),
          "| rotation deg", tuple(round(math.degrees(a), 2) for a in o.rotation_euler), o.rotation_mode,
          "| scale", tuple(round(c, 4) for c in o.scale),
          "| world size", round(max(px) - min(px), 4), round(max(py) - min(py), 4), round(max(pz) - min(pz), 4),
          "| lowest z", round(min(pz), 4), "| tip", tuple(round(c, 4) for c in tip),
          "| vertices", len(o.data.vertices), "| triangles", sum(len(p.vertices) - 2 for p in o.data.polygons),
          "| delta rot", tuple(round(math.degrees(a), 2) for a in o.delta_rotation_euler),
          "| parent", o.parent.name if o.parent else None)
ax, ay, az = zip(*allw)
print("combined: x", round(min(ax), 4), round(max(ax), 4), "| y", round(min(ay), 4), round(max(ay), 4),
      "| z", round(min(az), 4), round(max(az), 4),
      "| size", round(max(ax) - min(ax), 4), round(max(ay) - min(ay), 4), round(max(az) - min(az), 4))

def world_bvh(o):
    m = o.matrix_world
    return BVHTree.FromPolygons([m @ v.co for v in o.data.vertices], [p.vertices[:] for p in o.data.polygons])
trees = {n: world_bvh(bpy.data.objects[n]) for n in names}
for i, a in enumerate(names):
    for b in names[i + 1:]:
        print(a, "x", b, "intersecting face pairs:", len(trees[a].overlap(trees[b])))

# --- call 9: re-measure after the redone hand edit (read-only; same body as call 8); every value again identical to call 6
# Read-only: re-measure the three cones after Zhefan's hand edit ("after" values), the combined bounds,
# the shared-base intersections, and anything else in the scene that changed.
import bpy, math
from mathutils.bvhtree import BVHTree

names = ("Crystal_Tall", "Crystal_Short_A", "Crystal_Short_B")
print("mode:", bpy.context.mode, "| file:", repr(bpy.data.filepath), "| unsaved changes:", bpy.data.is_dirty)
print("objects:", [(o.name, o.type) for o in bpy.data.objects], "| meshes:", [m.name for m in bpy.data.meshes],
      "| materials:", [m.name for m in bpy.data.materials])
print("--- after the hand edit")
allw = []
for n in names:
    o = bpy.data.objects[n]
    pw = [o.matrix_world @ v.co for v in o.data.vertices]
    allw += pw
    px, py, pz = zip(*pw)
    tip = max(pw, key=lambda p: (p - o.matrix_world.translation).length)
    print(n, "| location", tuple(round(c, 4) for c in o.location),
          "| rotation deg", tuple(round(math.degrees(a), 2) for a in o.rotation_euler), o.rotation_mode,
          "| scale", tuple(round(c, 4) for c in o.scale),
          "| world size", round(max(px) - min(px), 4), round(max(py) - min(py), 4), round(max(pz) - min(pz), 4),
          "| lowest z", round(min(pz), 4), "| tip", tuple(round(c, 4) for c in tip),
          "| vertices", len(o.data.vertices), "| triangles", sum(len(p.vertices) - 2 for p in o.data.polygons),
          "| delta rot", tuple(round(math.degrees(a), 2) for a in o.delta_rotation_euler),
          "| parent", o.parent.name if o.parent else None)
ax, ay, az = zip(*allw)
print("combined: x", round(min(ax), 4), round(max(ax), 4), "| y", round(min(ay), 4), round(max(ay), 4),
      "| z", round(min(az), 4), round(max(az), 4),
      "| size", round(max(ax) - min(ax), 4), round(max(ay) - min(ay), 4), round(max(az) - min(az), 4))

def world_bvh(o):
    m = o.matrix_world
    return BVHTree.FromPolygons([m @ v.co for v in o.data.vertices], [p.vertices[:] for p in o.data.polygons])
trees = {n: world_bvh(bpy.data.objects[n]) for n in names}
for i, a in enumerate(names):
    for b in names[i + 1:]:
        print(a, "x", b, "intersecting face pairs:", len(trees[a].overlap(trees[b])))

# --- call 10: does the Blender window show the same scene the MCP measures? (read-only)
# Read-only diagnosis: does the Blender window show the same scene and objects the MCP measures?
import bpy, math

print("scenes:", [(s.name, [o.name for o in s.objects]) for s in bpy.data.scenes])
print("context scene:", bpy.context.scene.name, "| view layer:", bpy.context.view_layer.name)
for i, win in enumerate(bpy.context.window_manager.windows):
    vl = win.view_layer
    print("window", i, "| scene:", win.scene.name, "| workspace:", win.workspace.name, "| screen:", win.screen.name,
          "| view layer:", vl.name, "| active object:", vl.objects.active.name if vl.objects.active else None,
          "| selected:", [o.name for o in vl.objects if o.select_get(view_layer=vl)])
    for area in win.screen.areas:
        if area.type == "VIEW_3D":
            sp = area.spaces.active
            print("   3D viewport", area.width, "x", area.height, "| local view:", sp.local_view is not None,
                  "| shading:", sp.shading.type)
print("objects not in the context scene:", [o.name for o in bpy.data.objects if o.name not in bpy.context.scene.objects])
print("libraries:", [l.filepath for l in bpy.data.libraries])

# --- call 11: re-measure after the third hand edit (read-only; same body as calls 8 and 9); every value again identical to call 6
# Read-only: re-measure the three cones after Zhefan's hand edit ("after" values), the combined bounds,
# the shared-base intersections, and anything else in the scene that changed.
import bpy, math
from mathutils.bvhtree import BVHTree

names = ("Crystal_Tall", "Crystal_Short_A", "Crystal_Short_B")
print("mode:", bpy.context.mode, "| file:", repr(bpy.data.filepath), "| unsaved changes:", bpy.data.is_dirty)
print("objects:", [(o.name, o.type) for o in bpy.data.objects], "| meshes:", [m.name for m in bpy.data.meshes],
      "| materials:", [m.name for m in bpy.data.materials])
print("--- after the hand edit")
allw = []
for n in names:
    o = bpy.data.objects[n]
    pw = [o.matrix_world @ v.co for v in o.data.vertices]
    allw += pw
    px, py, pz = zip(*pw)
    tip = max(pw, key=lambda p: (p - o.matrix_world.translation).length)
    print(n, "| location", tuple(round(c, 4) for c in o.location),
          "| rotation deg", tuple(round(math.degrees(a), 2) for a in o.rotation_euler), o.rotation_mode,
          "| scale", tuple(round(c, 4) for c in o.scale),
          "| world size", round(max(px) - min(px), 4), round(max(py) - min(py), 4), round(max(pz) - min(pz), 4),
          "| lowest z", round(min(pz), 4), "| tip", tuple(round(c, 4) for c in tip),
          "| vertices", len(o.data.vertices), "| triangles", sum(len(p.vertices) - 2 for p in o.data.polygons),
          "| delta rot", tuple(round(math.degrees(a), 2) for a in o.delta_rotation_euler),
          "| parent", o.parent.name if o.parent else None)
ax, ay, az = zip(*allw)
print("combined: x", round(min(ax), 4), round(max(ax), 4), "| y", round(min(ay), 4), round(max(ay), 4),
      "| z", round(min(az), 4), round(max(az), 4),
      "| size", round(max(ax) - min(ax), 4), round(max(ay) - min(ay), 4), round(max(az) - min(az), 4))

def world_bvh(o):
    m = o.matrix_world
    return BVHTree.FromPolygons([m @ v.co for v in o.data.vertices], [p.vertices[:] for p in o.data.polygons])
trees = {n: world_bvh(bpy.data.objects[n]) for n in names}
for i, a in enumerate(names):
    for b in names[i + 1:]:
        print(a, "x", b, "intersecting face pairs:", len(trees[a].overlap(trees[b])))

# 2026-10-14, Zhefan's hand edit in the Blender window (after three attempts that did not take; see calls 8, 9, 11):
# Crystal_Short_B rotation Z typed into the sidebar, -2.5379 deg -> 20 deg, confirmed with Enter.

# --- call 12: re-measure after the hand edit took effect (read-only; same body as calls 8, 9 and 11)
# Read-only: re-measure the three cones after Zhefan's hand edit ("after" values), the combined bounds,
# the shared-base intersections, and anything else in the scene that changed.
import bpy, math
from mathutils.bvhtree import BVHTree

names = ("Crystal_Tall", "Crystal_Short_A", "Crystal_Short_B")
print("mode:", bpy.context.mode, "| file:", repr(bpy.data.filepath), "| unsaved changes:", bpy.data.is_dirty)
print("objects:", [(o.name, o.type) for o in bpy.data.objects], "| meshes:", [m.name for m in bpy.data.meshes],
      "| materials:", [m.name for m in bpy.data.materials])
print("--- after the hand edit")
allw = []
for n in names:
    o = bpy.data.objects[n]
    pw = [o.matrix_world @ v.co for v in o.data.vertices]
    allw += pw
    px, py, pz = zip(*pw)
    tip = max(pw, key=lambda p: (p - o.matrix_world.translation).length)
    print(n, "| location", tuple(round(c, 4) for c in o.location),
          "| rotation deg", tuple(round(math.degrees(a), 2) for a in o.rotation_euler), o.rotation_mode,
          "| scale", tuple(round(c, 4) for c in o.scale),
          "| world size", round(max(px) - min(px), 4), round(max(py) - min(py), 4), round(max(pz) - min(pz), 4),
          "| lowest z", round(min(pz), 4), "| tip", tuple(round(c, 4) for c in tip),
          "| vertices", len(o.data.vertices), "| triangles", sum(len(p.vertices) - 2 for p in o.data.polygons),
          "| delta rot", tuple(round(math.degrees(a), 2) for a in o.delta_rotation_euler),
          "| parent", o.parent.name if o.parent else None)
ax, ay, az = zip(*allw)
print("combined: x", round(min(ax), 4), round(max(ax), 4), "| y", round(min(ay), 4), round(max(ay), 4),
      "| z", round(min(az), 4), round(max(az), 4),
      "| size", round(max(ax) - min(ax), 4), round(max(ay) - min(ay), 4), round(max(az) - min(az), 4))

def world_bvh(o):
    m = o.matrix_world
    return BVHTree.FromPolygons([m @ v.co for v in o.data.vertices], [p.vertices[:] for p in o.data.polygons])
trees = {n: world_bvh(bpy.data.objects[n]) for n in names}
for i, a in enumerate(names):
    for b in names[i + 1:]:
        print(a, "x", b, "intersecting face pairs:", len(trees[a].overlap(trees[b])))

# --- call J1: lengthen Crystal_Short_B along its own axis (Zhefan chose option 1, 2026-10-14)
# J1: lengthen Crystal_Short_B along its own axis (local Z, base ring at local z = 0) so its tip reaches
# world x = -0.175. Object location, rotation (Zhefan's hand edit) and scale are not touched; only the
# mesh's local z coordinates are multiplied, so the base ring and the lowest point stay where they are.
import bpy, math
from mathutils import Vector

NAME = "Crystal_Short_B"
TIP_X = -0.175

ob = bpy.data.objects[NAME]
me = ob.data
rot_before = tuple(round(math.degrees(a), 4) for a in ob.rotation_euler)
loc_before, scale_before = tuple(ob.location), tuple(ob.scale)

tip_i = max(range(len(me.vertices)), key=lambda i: me.vertices[i].co.z)
tip_before = ob.matrix_world @ me.vertices[tip_i].co
length_before = me.vertices[tip_i].co.z
k = (TIP_X - ob.matrix_world.translation.x) / (tip_before.x - ob.matrix_world.translation.x)
for v in me.vertices:
    v.co.z *= k
me.update()
bpy.context.view_layer.update()

w = [ob.matrix_world @ v.co for v in me.vertices]
wx, wy, wz = zip(*w)
print(NAME, "length factor", round(k, 4), "| length", round(length_before, 4), "->", round(me.vertices[tip_i].co.z, 4))
print("tip", tuple(round(c, 4) for c in tip_before), "->", tuple(round(c, 4) for c in w[tip_i]))
print("world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4))
print("rotation unchanged:", tuple(round(math.degrees(a), 4) for a in ob.rotation_euler) == rot_before, rot_before,
      "| location unchanged:", tuple(ob.location) == loc_before, "| scale unchanged:", tuple(ob.scale) == scale_before)

allw = []
for n in ("Crystal_Tall", "Crystal_Short_A", "Crystal_Short_B"):
    o = bpy.data.objects[n]
    allw += [o.matrix_world @ v.co for v in o.data.vertices]
ax, ay, az = zip(*allw)
print("combined: x", round(min(ax), 4), round(max(ax), 4), "| y", round(min(ay), 4), round(max(ay), 4),
      "| z", round(min(az), 4), round(max(az), 4),
      "| size", round(max(ax) - min(ax), 4), round(max(ay) - min(ay), 4), round(max(az) - min(az), 4))

# --- call J2: join, apply rotation and scale, fit check, origin to the centre of the underside
# J2: join the three cones into one object "Crystal" (Crystal_Tall active), apply rotation and scale,
# check the fit factors against the brief (fit only if every factor is within 0.95-1.05), then move the
# mesh so the lowest point is at Z = 0 and the centre of the underside is the origin, at the world origin.
import bpy
from mathutils import Matrix, Vector

BRIEF = (0.35, 0.35, 0.6)            # W x D x H in metres, from CHANGE-BRIEF.md
FIT_LIMITS = (0.95, 1.05)

parts = [bpy.data.objects[n] for n in ("Crystal_Tall", "Crystal_Short_A", "Crystal_Short_B")]
for ob in bpy.context.view_layer.objects:
    ob.select_set(False)
for ob in parts:
    ob.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()

crystal = bpy.context.active_object
crystal.name = crystal.data.name = "Crystal"
for m in list(bpy.data.meshes):
    if m.users == 0:
        bpy.data.meshes.remove(m)

bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

me = crystal.data
me.transform(Matrix.Translation(crystal.location))   # bake the location too, then work in world space
crystal.location = (0.0, 0.0, 0.0)
xs, ys, zs = zip(*(v.co for v in me.vertices))
before = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
factors = tuple(b / d for b, d in zip(BRIEF, before))
fit_ok = all(FIT_LIMITS[0] <= f <= FIT_LIMITS[1] for f in factors)
bottom_centre = Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, min(zs)))

me.transform(Matrix.Translation(-bottom_centre))
if fit_ok:
    me.transform(Matrix.Diagonal((*factors, 1.0)))
me.update()
bpy.context.view_layer.update()

xs, ys, zs = zip(*(v.co for v in me.vertices))
print("size before fit:", tuple(round(d, 4) for d in before))
print("fit factors:", tuple(round(f, 4) for f in factors), "| within", FIT_LIMITS, ":", fit_ok,
      "| fit applied:", fit_ok)
print("x", round(min(xs), 4), round(max(xs), 4), "| y", round(min(ys), 4), round(max(ys), 4),
      "| z", round(min(zs), 4), round(max(zs), 4))
print("dimensions:", tuple(round(d, 4) for d in crystal.dimensions))
print("location:", tuple(crystal.location), "| rotation:", tuple(crystal.rotation_euler), "| scale:", tuple(crystal.scale))
me.calc_loop_triangles()
print("objects:", [o.name for o in bpy.data.objects], "| triangles:", len(me.loop_triangles),
      "| faces:", len(me.polygons), "| materials:", [m.name for m in me.materials])

mat = bpy.data.materials["Crystal"]
bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
print("material Crystal: base", tuple(round(v, 4) for v in bsdf.inputs["Base Color"].default_value),
      "| emission", tuple(round(v, 4) for v in bsdf.inputs["Emission Color"].default_value),
      "| strength", bsdf.inputs["Emission Strength"].default_value,
      "| roughness", round(bsdf.inputs["Roughness"].default_value, 3))

# --- call S1: save the .blend source
# Save the .blend source for the Crystal. Refuses to overwrite an existing file.
import bpy, os

PATH = r"E:\7270\csye-7270-course\fall-2026\zhefan-z\assignment-3\walker-magic-zhefan\tools\blender\crystal.blend"

if os.path.exists(PATH):
    raise RuntimeError("refusing to overwrite " + PATH)
print("objects:", [(o.name, o.type) for o in bpy.data.objects], "| meshes:", [m.name for m in bpy.data.meshes],
      "| materials:", [(m.name, m.users) for m in bpy.data.materials])
bpy.ops.wm.save_as_mainfile(filepath=PATH)
print("saved:", bpy.data.filepath, "|", os.path.getsize(PATH), "bytes",
      "| save versions setting:", bpy.context.preferences.filepaths.save_version)

# --- Export

# --- call E1: export crystal.glb (FAILED 2026-10-14: KeyError, no object "Crystal"; between S1 and E1 the open
# --- Blender file had been replaced by a new default file, not by any call in this record; nothing was written)
# Export the Crystal as binary glTF (.glb) with the same settings as rock.glb: +Y Up on, materials
# included. Refuses to overwrite.
import bpy, os

PATH = r"E:\7270\csye-7270-course\fall-2026\zhefan-z\assignment-3\walker-magic-zhefan\assets\models\crystal.glb"

if os.path.exists(PATH):
    raise RuntimeError("refusing to overwrite " + PATH)
os.makedirs(os.path.dirname(PATH), exist_ok=True)

crystal = bpy.data.objects["Crystal"]
for ob in bpy.context.view_layer.objects:
    ob.select_set(False)
crystal.select_set(True)
bpy.context.view_layer.objects.active = crystal

settings = dict(
    filepath=PATH,
    export_format="GLB",            # dynamic enum; an invalid value raises TypeError listing the valid ones
    use_selection=True,
    export_yup=True,
    export_materials="EXPORT",
    export_apply=False,             # Crystal has no modifiers
    export_normals=True,
    export_texcoords=True,
    export_cameras=False,
    export_lights=False,
    export_extras=False,
    export_animations=False,
)
try:
    result = bpy.ops.export_scene.gltf(**settings)
except TypeError as e:
    print("export refused:", e)
    raise
print("result:", result, "|", PATH, os.path.getsize(PATH), "bytes")
print("settings:", {k: v for k, v in settings.items() if k != "filepath"})

# 2026-10-14 note: E1 never wrote crystal.glb. Zhefan had started a new Blender file (File > New > General)
# between S1 and E1. crystal.glb was then exported headlessly from the saved crystal.blend by
# tools/blender/export_crystal.py, in a separate windowless Blender (-b --factory-startup), with the same
# settings as E1; crystal.blend's SHA-256 was unchanged by that run.

# --- call E1b: what is open in Blender now? (read-only, after E1 failed)
# Read-only: what is open in Blender now?
import bpy
print("file:", repr(bpy.data.filepath), "| unsaved changes:", bpy.data.is_dirty, "| mode:", bpy.context.mode)
print("objects:", [(o.name, o.type) for o in bpy.data.objects], "| meshes:", [m.name for m in bpy.data.meshes],
      "| materials:", [(m.name, m.users) for m in bpy.data.materials])
print("scenes:", [s.name for s in bpy.data.scenes])
