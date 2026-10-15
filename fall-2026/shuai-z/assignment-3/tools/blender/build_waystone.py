# build_waystone.py — the waystone, Assignment 3 (walker-rudy)
#
# Every execute_blender_code body that Claude Code ran through MCP for Blender
# (mcp-for-blender 2.1.9, add-on 1.8) in Blender 5.2.2 LTS on 2026-10-13, in
# order and unchanged. Each step was its own call; the steps are separated
# below. The spec is CHANGE-BRIEF.md, revision 1.
#
# Hand edits made in Blender's window are not in this file; see FRICTIONAL.md.

# ---------------------------------------------------------------------------
# Step 0 — empty scene, metric units in metres
import bpy

for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    for block in list(coll):
        if block.users == 0:
            coll.remove(block)

units = bpy.context.scene.unit_settings
units.system = 'METRIC'
units.length_unit = 'METERS'
units.scale_length = 1.0

print("objects:", len(bpy.data.objects), "meshes:", len(bpy.data.meshes), "materials:", len(bpy.data.materials))
print("units:", units.system, units.length_unit, units.scale_length)

# ---------------------------------------------------------------------------
# Step 1 — Waystone_Body: a cube, 0.60 x 0.36 x 0.72 m, base on Z = 0
import bpy

def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def flat_material(name, hex_code):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = [srgb_to_linear(int(hex_code[i:i + 2], 16) / 255) for i in (0, 2, 4)]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    mat.diffuse_color = (*rgb, 1.0)  # viewport colour only; the exporter reads the node
    return mat

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.36))
body = bpy.context.active_object
body.name = "Waystone_Body"
body.scale = (0.60, 0.36, 0.72)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
body.data.materials.append(flat_material("Stone", "8C8A80"))

print(body.name, "dims", tuple(round(d, 4) for d in body.dimensions),
      "loc", tuple(round(v, 4) for v in body.location),
      "rot", tuple(body.rotation_euler), "scale", tuple(body.scale))

# ---------------------------------------------------------------------------
# Step 2 — Waystone_Top: a four-sided cone (pyramid), base 0.60 x 0.36 m, 0.12 m tall, on the body
import bpy, math

bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=math.sqrt(0.5), radius2=0.0, depth=1.0,
                                location=(0, 0, 0.78))
top = bpy.context.active_object
top.name = "Waystone_Top"
top.rotation_euler = (0, 0, math.radians(45))  # corners onto the axes -> edges along X and Y
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
top.scale = (0.60, 0.36, 0.12)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
top.data.materials.append(bpy.data.materials["Stone"])

zs = [(top.matrix_world @ v.co).z for v in top.data.vertices]
print(top.name, "dims", tuple(round(d, 4) for d in top.dimensions),
      "loc", tuple(round(v, 4) for v in top.location),
      "rot", tuple(round(r, 4) for r in top.rotation_euler), "scale", tuple(top.scale),
      "z from", round(min(zs), 4), "to", round(max(zs), 4))

# ---------------------------------------------------------------------------
# Step 3 — Waystone_Rune: a thin cube, 0.20 x 0.02 x 0.30 m, set into the front (-Y) face
import bpy

def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def flat_material(name, hex_code):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = [srgb_to_linear(int(hex_code[i:i + 2], 16) / 255) for i in (0, 2, 4)]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    mat.diffuse_color = (*rgb, 1.0)  # viewport colour only; the exporter reads the node
    return mat

# The body's front face is at Y = -0.18; the rune runs from -0.195 to -0.175,
# so it stands 0.015 m proud of the face and 0.005 m into it.
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.185, 0.42))
rune = bpy.context.active_object
rune.name = "Waystone_Rune"
rune.scale = (0.20, 0.02, 0.30)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
rune.data.materials.append(flat_material("Rune", "99E0FF"))

print(rune.name, "dims", tuple(round(d, 4) for d in rune.dimensions),
      "loc", tuple(round(v, 4) for v in rune.location),
      "rot", tuple(rune.rotation_euler), "scale", tuple(rune.scale))

# ---------------------------------------------------------------------------
# Step 4 — Waystone_Moss: a flattened cube, 0.70 x 0.40 x 0.06 m, around the foot
import bpy

def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def flat_material(name, hex_code):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = [srgb_to_linear(int(hex_code[i:i + 2], 16) / 255) for i in (0, 2, 4)]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    mat.diffuse_color = (*rgb, 1.0)  # viewport colour only; the exporter reads the node
    return mat

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.03))
moss = bpy.context.active_object
moss.name = "Waystone_Moss"
moss.scale = (0.70, 0.40, 0.06)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
moss.data.materials.append(flat_material("Moss", "6E7F3C"))

print(moss.name, "dims", tuple(round(d, 4) for d in moss.dimensions),
      "loc", tuple(round(v, 4) for v in moss.location),
      "rot", tuple(moss.rotation_euler), "scale", tuple(moss.scale))

# ---------------------------------------------------------------------------
# Step 5 — check: triangles, overall extent, material colours
import bpy
from mathutils import Vector

parts = [o for o in bpy.data.objects if o.type == 'MESH']
total = 0
lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
for o in parts:
    o.data.calc_loop_triangles()
    tris = len(o.data.loop_triangles)
    total += tris
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    print(f"{o.name}: {tris} triangles, modifiers {len(o.modifiers)}")
print("objects:", len(parts), "total triangles:", total, "(budget 60)")
print("extent X", round(lo.x, 4), round(hi.x, 4), "Y", round(lo.y, 4), round(hi.y, 4), "Z", round(lo.z, 4), round(hi.z, 4))
print("size", tuple(round(c, 4) for c in (hi - lo)))
for m in bpy.data.materials:
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    lin = bsdf.inputs["Base Color"].default_value
    to_srgb = lambda c: 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    print(m.name, "base colour back to sRGB hex: #" + "".join(f"{round(to_srgb(c) * 255):02X}" for c in lin[:3]))

# ---------------------------------------------------------------------------
# Step 6 — save the source file before the hand edit
import bpy, os

path = "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-3/blender/waystone.blend"
os.makedirs(os.path.dirname(path), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=path)
print("saved", bpy.data.filepath)

# ---------------------------------------------------------------------------
# My hand edit, in Blender's window (not code): I moved Waystone_Rune up,
# from Z = 0.42 to Z = 0.4537 (+0.034 m), and saved. Claude then read it back:
import bpy
r = bpy.data.objects["Waystone_Rune"]
zs = [(r.matrix_world @ v.co).z for v in r.data.vertices]
ys = [(r.matrix_world @ v.co).y for v in r.data.vertices]
print("rune loc", tuple(round(c, 4) for c in r.location), "z", round(min(zs), 4), round(max(zs), 4),
      "y", round(min(ys), 4), round(max(ys), 4), "dims", tuple(round(d, 4) for d in r.dimensions))
print("file", bpy.data.filepath, "dirty", bpy.data.is_dirty)

# ---------------------------------------------------------------------------
# Step 7 (trial) — remove the rectangular rune; the R takes its place (my hand-moved height: Z 0.3037-0.6037)
import bpy

bpy.data.objects.remove(bpy.data.objects["Waystone_Rune"], do_unlink=True)
for m in list(bpy.data.meshes):
    if m.users == 0:
        bpy.data.meshes.remove(m)
print("objects:", [o.name for o in bpy.data.objects], "Rune material kept:", "Rune" in bpy.data.materials)

# ---------------------------------------------------------------------------
# Step 8 (trial) — Rune_Stem: the R's upright, a cube 0.05 x 0.02 x 0.30 m, left side of the rune area
import bpy

Z_BOTTOM, Z_TOP = 0.3037, 0.6037  # the rune's height after my hand edit
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.075, -0.185, (Z_BOTTOM + Z_TOP) / 2))
stem = bpy.context.active_object
stem.name = "Rune_Stem"
stem.scale = (0.05, 0.02, Z_TOP - Z_BOTTOM)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
stem.data.materials.append(bpy.data.materials["Rune"])

ws = [stem.matrix_world @ v.co for v in stem.data.vertices]
print(stem.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(stem.rotation_euler), "scale", tuple(stem.scale))

# ---------------------------------------------------------------------------
# Step 9 (trial) — Rune_Bowl: the R's bowl, an 8-sided cylinder lying along Y, 0.016 m deep,
# its flat top level with the stem's top and its left side on the stem's left edge.
# It sits 0.004 m behind the stem's front face, so the stem hides the bowl's left curve.
import bpy, math
from mathutils import Vector

Z_TOP = 0.6037
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.0, depth=1.0, location=(0, 0, 0))
bowl = bpy.context.active_object
bowl.name = "Rune_Bowl"
bowl.rotation_euler = (math.radians(90), math.radians(22.5), 0)  # axis along Y; a flat edge on top
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bowl.scale = (0.10, 0.016, 0.08)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

ws = [bowl.matrix_world @ v.co for v in bowl.data.vertices]
lo = Vector((min(w.x for w in ws), min(w.y for w in ws), min(w.z for w in ws)))
hi = Vector((max(w.x for w in ws), max(w.y for w in ws), max(w.z for w in ws)))
bowl.location = (-0.10 - lo.x, -0.175 - hi.y, Z_TOP - hi.z)  # left on -0.10, back on -0.175, top on Z_TOP
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bowl.data.materials.append(bpy.data.materials["Rune"])

ws = [bowl.matrix_world @ v.co for v in bowl.data.vertices]
print(bowl.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "loc", tuple(round(c, 4) for c in bowl.location),
      "rot", tuple(round(r, 4) for r in bowl.rotation_euler), "scale", tuple(bowl.scale))

# ---------------------------------------------------------------------------
# Step 10 (trial) — Rune_Leg: the R's diagonal leg, a cube 0.05 m wide and 0.016 m deep,
# from under the bowl down to the bottom right of the rune area
import bpy, math
from mathutils import Vector

Z_BOTTOM = 0.3037
p1 = Vector((-0.01, 0.4759))   # (x, z): inside the bowl's lower edge, so the two overlap
p2 = Vector((0.07, Z_BOTTOM))
d = p2 - p1
mid = (p1 + p2) / 2
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(mid.x, -0.183, mid.y))
leg = bpy.context.active_object
leg.name = "Rune_Leg"
leg.scale = (0.05, 0.016, d.length)
leg.rotation_euler = (0, math.atan2(d.x, d.y), 0)  # turn the cube's long (Z) axis onto p1 -> p2
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

ws = [leg.matrix_world @ v.co for v in leg.data.vertices]
dx = min(0.0, 0.10 - max(w.x for w in ws))   # keep it inside X <= 0.10
dz = Z_BOTTOM - min(w.z for w in ws)         # its lowest corner on the rune's bottom
leg.location = (leg.location.x + dx, leg.location.y, leg.location.z + dz)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
leg.data.materials.append(bpy.data.materials["Rune"])

ws = [leg.matrix_world @ v.co for v in leg.data.vertices]
print(leg.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(round(r, 4) for r in leg.rotation_euler), "scale", tuple(leg.scale))

# ---------------------------------------------------------------------------
# Step 11 (trial) — check: objects, triangles, overall extent
import bpy
from mathutils import Vector

parts = [o for o in bpy.data.objects if o.type == 'MESH']
total = 0
lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
for o in sorted(parts, key=lambda o: o.name):
    o.data.calc_loop_triangles()
    tris = len(o.data.loop_triangles)
    total += tris
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    print(f"{o.name}: {tris} triangles, modifiers {len(o.modifiers)}")
print("objects:", len(parts), "total triangles:", total, "(revision-1 budget 60)")
print("size", tuple(round(c, 4) for c in (hi - lo)), "z from", round(lo.z, 4))

# ---------------------------------------------------------------------------
# I looked at the R in Blender and rejected it ("现在不好看" — it does not look good).
# Step 12 (trial) — remove the R's three parts; a ring takes their place
import bpy

for name in ("Rune_Stem", "Rune_Bowl", "Rune_Leg"):
    bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
for m in list(bpy.data.meshes):
    if m.users == 0:
        bpy.data.meshes.remove(m)
print("objects:", sorted(o.name for o in bpy.data.objects))

# ---------------------------------------------------------------------------
# Step 13 (trial) — Rune_Ring: an 8-sided cylinder lying along Y, Ø 0.22 m, 0.02 m deep,
# centred on my hand-moved rune height (Z = 0.4537), 0.015 m proud of the front face
import bpy, math

Z_CENTRE = 0.4537
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.11, depth=0.02, location=(0, -0.185, Z_CENTRE))
ring = bpy.context.active_object
ring.name = "Rune_Ring"
ring.rotation_euler = (math.radians(90), math.radians(22.5), 0)  # axis along Y; flat edges top and bottom
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
ring.data.materials.append(bpy.data.materials["Rune"])

ws = [ring.matrix_world @ v.co for v in ring.data.vertices]
print(ring.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(round(r, 4) for r in ring.rotation_euler), "scale", tuple(ring.scale))

# ---------------------------------------------------------------------------
# Step 14 (trial) — Rune_Hole: a stone-coloured 8-sided cylinder, Ø 0.12 m, in front of the ring's
# middle, so the ring reads as a band 0.05 m wide. Its face is 0.002 m in front of the ring's,
# so the two front faces never share a plane.
import bpy, math

Z_CENTRE = 0.4537
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.06, depth=0.022, location=(0, -0.186, Z_CENTRE))
hole = bpy.context.active_object
hole.name = "Rune_Hole"
hole.rotation_euler = (math.radians(90), math.radians(22.5), 0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
hole.data.materials.append(bpy.data.materials["Stone"])

ws = [hole.matrix_world @ v.co for v in hole.data.vertices]
print(hole.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(round(r, 4) for r in hole.rotation_euler), "scale", tuple(hole.scale))

# ---------------------------------------------------------------------------
# Step 15 (trial) — check: objects, triangles, overall extent
import bpy
from mathutils import Vector

parts = [o for o in bpy.data.objects if o.type == 'MESH']
total = 0
lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
for o in sorted(parts, key=lambda o: o.name):
    o.data.calc_loop_triangles()
    tris = len(o.data.loop_triangles)
    total += tris
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    print(f"{o.name}: {tris} triangles, modifiers {len(o.modifiers)}")
print("objects:", len(parts), "total triangles:", total, "(revision-1 budget 60)")
print("size", tuple(round(c, 4) for c in (hi - lo)), "z from", round(lo.z, 4))

# ---------------------------------------------------------------------------
# I asked for 12 sides and a thinner ring ("改成12边……圆环再细一点").
# Step 16 — remove the 8-sided ring and hole; rebuild both with 12 sides and a thinner band
import bpy

for name in ("Rune_Ring", "Rune_Hole"):
    bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
for m in list(bpy.data.meshes):
    if m.users == 0:
        bpy.data.meshes.remove(m)
print("objects:", sorted(o.name for o in bpy.data.objects))

# ---------------------------------------------------------------------------
# Step 17 — Rune_Ring: a 12-sided cylinder lying along Y, Ø 0.22 m, 0.02 m deep,
# centred on my hand-moved rune height (Z = 0.4537), 0.015 m proud of the front face
import bpy, math

Z_CENTRE = 0.4537
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.11, depth=0.02, location=(0, -0.185, Z_CENTRE))
ring = bpy.context.active_object
ring.name = "Rune_Ring"
ring.rotation_euler = (math.radians(90), math.radians(15), 0)  # axis along Y; flat edges top and bottom
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
ring.data.materials.append(bpy.data.materials["Rune"])

ws = [ring.matrix_world @ v.co for v in ring.data.vertices]
print(ring.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(round(r, 4) for r in ring.rotation_euler), "scale", tuple(ring.scale))

# ---------------------------------------------------------------------------
# Step 18 — Rune_Hole: a stone-coloured 12-sided cylinder, Ø 0.16 m, in front of the ring's middle,
# so the ring reads as a band 0.03 m wide (was 0.05). Its face is 0.002 m in front of the ring's.
import bpy, math

Z_CENTRE = 0.4537
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.08, depth=0.022, location=(0, -0.186, Z_CENTRE))
hole = bpy.context.active_object
hole.name = "Rune_Hole"
hole.rotation_euler = (math.radians(90), math.radians(15), 0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
hole.data.materials.append(bpy.data.materials["Stone"])

ws = [hole.matrix_world @ v.co for v in hole.data.vertices]
print(hole.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(round(r, 4) for r in hole.rotation_euler), "scale", tuple(hole.scale))

# ---------------------------------------------------------------------------
# Step 19 — check: objects, triangles, overall extent
import bpy
from mathutils import Vector

parts = [o for o in bpy.data.objects if o.type == 'MESH']
total = 0
lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
for o in sorted(parts, key=lambda o: o.name):
    o.data.calc_loop_triangles()
    tris = len(o.data.loop_triangles)
    total += tris
    for v in o.data.vertices:
        w = o.matrix_world @ v.co
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    print(f"{o.name}: {tris} triangles, modifiers {len(o.modifiers)}")
print("objects:", len(parts), "total triangles:", total, "(revision-2 budget 130)")
print("size", tuple(round(c, 4) for c in (hi - lo)), "z from", round(lo.z, 4))

# ---------------------------------------------------------------------------
# Step 20 — save the waystone with the 12-sided ring (the hand-edited file is kept as
# evidence/waystone-after-hand-edit.blend)
import bpy

bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath, "dirty", bpy.data.is_dirty)

# ---------------------------------------------------------------------------
# Step 21 — join the five parts into one object, Waystone, with its origin at the world origin
# (the centre of its underside), then apply transforms
import bpy

parts = [bpy.data.objects[n] for n in ("Waystone_Body", "Waystone_Top", "Waystone_Moss", "Rune_Ring", "Rune_Hole")]
bpy.ops.object.select_all(action='DESELECT')
for o in parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()

waystone = bpy.context.active_object
waystone.name = "Waystone"
waystone.data.name = "Waystone"
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

print("objects:", [o.name for o in bpy.data.objects])
print(waystone.name, "loc", tuple(waystone.location), "rot", tuple(waystone.rotation_euler),
      "scale", tuple(waystone.scale), "dims", tuple(round(d, 4) for d in waystone.dimensions),
      "materials", [m.name for m in waystone.data.materials])

# ---------------------------------------------------------------------------
# Step 22 — check the joined waystone: triangles, extent, origin, materials per face; then save
import bpy
from mathutils import Vector

w = bpy.data.objects["Waystone"]
w.data.calc_loop_triangles()
ws = [w.matrix_world @ v.co for v in w.data.vertices]
lo = Vector((min(p.x for p in ws), min(p.y for p in ws), min(p.z for p in ws)))
hi = Vector((max(p.x for p in ws), max(p.y for p in ws), max(p.z for p in ws)))
print("triangles:", len(w.data.loop_triangles), "(revision-2 budget 130)")
print("extent X", round(lo.x, 4), round(hi.x, 4), "Y", round(lo.y, 4), round(hi.y, 4), "Z", round(lo.z, 4), round(hi.z, 4))
print("origin", tuple(w.location), "underside centre", (round((lo.x + hi.x) / 2, 4), round((lo.y + hi.y) / 2, 4), round(lo.z, 4)))
counts = {}
for p in w.data.polygons:
    name = w.data.materials[p.material_index].name
    counts[name] = counts.get(name, 0) + 1
print("faces per material:", counts)
bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath, "dirty", bpy.data.is_dirty)

# ---------------------------------------------------------------------------
# Step 23 — Step 22 printed "dirty True" right after saving; read it again to see whether the save took
import bpy, os, time
print("dirty", bpy.data.is_dirty, "file mtime", time.ctime(os.path.getmtime(bpy.data.filepath)))
