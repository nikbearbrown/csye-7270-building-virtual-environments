# build_teleport_circle.py — the teleport circle, Assignment 3 (walker-rudy)
#
# Every execute_blender_code body that Claude Code ran through MCP for Blender
# (mcp-for-blender 2.1.9, add-on 1.8) in Blender 5.2.2 LTS on 2026-10-13, in
# order and unchanged. Each step was its own call; the steps are separated
# below. The spec is CHANGE-BRIEF.md.
#
# Hand edits made in Blender's window are not in this file; see FRICTIONAL.md.

# ---------------------------------------------------------------------------
# Step 0 — a new file for the teleport circle. waystone.blend was saved (20:43:06); save this session
# under the new name first, so waystone.blend is never touched, then empty it.
import bpy

path = "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-3/blender/teleport_circle.blend"
print("was", bpy.data.filepath, "dirty", bpy.data.is_dirty)
bpy.ops.wm.save_as_mainfile(filepath=path)

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
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.ops.wm.save_mainfile()

print("now", bpy.data.filepath)
print("objects:", len(bpy.data.objects), "meshes:", len(bpy.data.meshes), "materials:", len(bpy.data.materials))
print("units:", units.system, units.length_unit, units.scale_length)

# ---------------------------------------------------------------------------
# Step 1 — Circle_Rim: a 24-sided cylinder, Ø 2.25 m, Z 0 to 0.04, gold
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

bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1.125, depth=0.04, location=(0, 0, 0.02))
rim = bpy.context.active_object
rim.name = "Circle_Rim"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
rim.data.materials.append(flat_material("Gold", "F0A830"))

ws = [rim.matrix_world @ v.co for v in rim.data.vertices]
print(rim.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(rim.rotation_euler), "scale", tuple(rim.scale))

# ---------------------------------------------------------------------------
# Step 2 — Circle_Inner: a 24-sided cylinder, Ø 1.95 m, Z 0.01 to 0.06, dark stone.
# Its underside is 0.01 m up, inside the rim disc, so it never shares the floor plane with the rim's.
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

bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.975, depth=0.05, location=(0, 0, 0.035))
inner = bpy.context.active_object
inner.name = "Circle_Inner"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
inner.data.materials.append(flat_material("DarkStone", "4A4440"))

ws = [inner.matrix_world @ v.co for v in inner.data.vertices]
print(inner.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(inner.rotation_euler), "scale", tuple(inner.scale))

# ---------------------------------------------------------------------------
# Step 3 — Circle_Centre: a 16-sided cylinder, Ø 0.60 m, Z 0.02 to 0.08, pale gold
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

bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.30, depth=0.06, location=(0, 0, 0.05))
centre = bpy.context.active_object
centre.name = "Circle_Centre"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
centre.data.materials.append(flat_material("PaleGold", "FFD76E"))

ws = [centre.matrix_world @ v.co for v in centre.data.vertices]
print(centre.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(centre.rotation_euler), "scale", tuple(centre.scale))

# ---------------------------------------------------------------------------
# Step 4 — Circle_Rune_1: a cube 0.20 x 0.08 x 0.02 m on the dark disc, 0.62 m from the centre at 90°,
# its long side along the circle; Z 0.06 to 0.08, gold
import bpy, math

ANGLE = 90
a = math.radians(ANGLE)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.62 * math.cos(a), 0.62 * math.sin(a), 0.07))
rune = bpy.context.active_object
rune.name = "Circle_Rune_1"
rune.scale = (0.20, 0.08, 0.02)
rune.rotation_euler = (0, 0, a + math.pi / 2)  # long (X) side along the tangent
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
rune.data.materials.append(bpy.data.materials["Gold"])

ws = [rune.matrix_world @ v.co for v in rune.data.vertices]
print(rune.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(round(r, 4) for r in rune.rotation_euler), "scale", tuple(rune.scale))

# ---------------------------------------------------------------------------
# Step 5 — Circle_Rune_2: the same, at 210°
import bpy, math

ANGLE = 210
a = math.radians(ANGLE)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.62 * math.cos(a), 0.62 * math.sin(a), 0.07))
rune = bpy.context.active_object
rune.name = "Circle_Rune_2"
rune.scale = (0.20, 0.08, 0.02)
rune.rotation_euler = (0, 0, a + math.pi / 2)  # long (X) side along the tangent
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
rune.data.materials.append(bpy.data.materials["Gold"])

ws = [rune.matrix_world @ v.co for v in rune.data.vertices]
print(rune.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(round(r, 4) for r in rune.rotation_euler), "scale", tuple(rune.scale))

# ---------------------------------------------------------------------------
# Step 6 — Circle_Rune_3: the same, at 330°
import bpy, math

ANGLE = 330
a = math.radians(ANGLE)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.62 * math.cos(a), 0.62 * math.sin(a), 0.07))
rune = bpy.context.active_object
rune.name = "Circle_Rune_3"
rune.scale = (0.20, 0.08, 0.02)
rune.rotation_euler = (0, 0, a + math.pi / 2)  # long (X) side along the tangent
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
rune.data.materials.append(bpy.data.materials["Gold"])

ws = [rune.matrix_world @ v.co for v in rune.data.vertices]
print(rune.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(round(r, 4) for r in rune.rotation_euler), "scale", tuple(rune.scale))

# ---------------------------------------------------------------------------
# Step 7 — check: objects, triangles, overall extent, colours read back from the nodes
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
    print(f"{o.name}: {tris} triangles, rot {tuple(o.rotation_euler)}, scale {tuple(o.scale)}, modifiers {len(o.modifiers)}")
print("objects:", len(parts), "total triangles:", total, "(budget 300)")
print("extent X", round(lo.x, 4), round(hi.x, 4), "Y", round(lo.y, 4), round(hi.y, 4), "Z", round(lo.z, 4), round(hi.z, 4))
print("size", tuple(round(c, 4) for c in (hi - lo)))
to_srgb = lambda c: 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
for m in bpy.data.materials:
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    lin = bsdf.inputs["Base Color"].default_value
    print(m.name, "base colour back to sRGB hex: #" + "".join(f"{round(to_srgb(c) * 255):02X}" for c in lin[:3]))

# ---------------------------------------------------------------------------
# Step 8 — save before joining, so the six parts can still be seen separately
import bpy

bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath)

# ---------------------------------------------------------------------------
# I asked for more rune blocks; the course limit is six basic shapes and the circle already had six,
# so Claude offered three options and I chose to keep it as it is ("选c，保持现状").
# Step 9 — join the six parts into one object, TeleportCircle, with its origin at the world origin
# (the centre of its underside), then apply transforms
import bpy

names = ("Circle_Rim", "Circle_Inner", "Circle_Centre", "Circle_Rune_1", "Circle_Rune_2", "Circle_Rune_3")
parts = [bpy.data.objects[n] for n in names]
bpy.ops.object.select_all(action='DESELECT')
for o in parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()

circle = bpy.context.active_object
circle.name = "TeleportCircle"
circle.data.name = "TeleportCircle"
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

print("objects:", [o.name for o in bpy.data.objects])
print(circle.name, "loc", tuple(circle.location), "rot", tuple(circle.rotation_euler),
      "scale", tuple(circle.scale), "dims", tuple(round(d, 4) for d in circle.dimensions),
      "materials", [m.name for m in circle.data.materials])

# ---------------------------------------------------------------------------
# Step 10 — check the joined teleport circle: triangles, extent, origin, faces per material; then save
import bpy, os, time
from mathutils import Vector

c = bpy.data.objects["TeleportCircle"]
c.data.calc_loop_triangles()
ws = [c.matrix_world @ v.co for v in c.data.vertices]
lo = Vector((min(p.x for p in ws), min(p.y for p in ws), min(p.z for p in ws)))
hi = Vector((max(p.x for p in ws), max(p.y for p in ws), max(p.z for p in ws)))
print("triangles:", len(c.data.loop_triangles), "(budget 300)")
print("extent X", round(lo.x, 4), round(hi.x, 4), "Y", round(lo.y, 4), round(hi.y, 4), "Z", round(lo.z, 4), round(hi.z, 4))
print("origin", tuple(c.location), "underside centre", (round((lo.x + hi.x) / 2, 4), round((lo.y + hi.y) / 2, 4), round(lo.z, 4)))
counts = {}
for p in c.data.polygons:
    name = c.data.materials[p.material_index].name
    counts[name] = counts.get(name, 0) + 1
print("faces per material:", counts)
bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath, "file mtime", time.ctime(os.path.getmtime(bpy.data.filepath)))
