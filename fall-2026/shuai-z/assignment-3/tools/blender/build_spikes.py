# build_spikes.py — the spikes, Assignment 3 (walker-rudy)
#
# Every execute_blender_code body that Claude Code ran through MCP for Blender
# (mcp-for-blender 2.1.9, add-on 1.8) in Blender 5.2.2 LTS on 2026-10-13, in
# order and unchanged. Each step was its own call; the steps are separated
# below. The spec is CHANGE-BRIEF.md.
#
# Hand edits made in Blender's window are not in this file; see FRICTIONAL.md.

# ---------------------------------------------------------------------------
# Step 0 — a new file for the spikes. teleport_circle.blend was saved (21:15:05); save this session
# under the new name first, so teleport_circle.blend is never touched, then empty it.
import bpy

path = "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-3/blender/spikes.blend"
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
# Step 1 — Spikes_Base: a cube, 0.80 x 0.30 x 0.12 m, Z 0 to 0.12, wood
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

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.06))
base = bpy.context.active_object
base.name = "Spikes_Base"
base.scale = (0.80, 0.30, 0.12)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
base.data.materials.append(flat_material("Wood", "7A5838"))

ws = [base.matrix_world @ v.co for v in base.data.vertices]
print(base.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(base.rotation_euler), "scale", tuple(base.scale))

# ---------------------------------------------------------------------------
# Step 2 — Spike_1: an 8-sided cone, base radius 0.07 m, 0.35 m tall, at X = -0.32, Z 0.12 to 0.47, iron
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

X = -0.32
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.07, radius2=0.0, depth=0.35, location=(X, 0, 0.12 + 0.175))
spike = bpy.context.active_object
spike.name = "Spike_1"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
spike.data.materials.append(flat_material("Iron", "5C6168"))

ws = [spike.matrix_world @ v.co for v in spike.data.vertices]
print(spike.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(spike.rotation_euler), "scale", tuple(spike.scale))

# ---------------------------------------------------------------------------
# Step 3 — Spike_2: the same cone at X = -0.16
import bpy

X = -0.16
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.07, radius2=0.0, depth=0.35, location=(X, 0, 0.12 + 0.175))
spike = bpy.context.active_object
spike.name = "Spike_2"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
spike.data.materials.append(bpy.data.materials["Iron"])

ws = [spike.matrix_world @ v.co for v in spike.data.vertices]
print(spike.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(spike.rotation_euler), "scale", tuple(spike.scale))

# ---------------------------------------------------------------------------
# Step 4 — Spike_3: the same cone at X = 0
import bpy

X = 0.0
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.07, radius2=0.0, depth=0.35, location=(X, 0, 0.12 + 0.175))
spike = bpy.context.active_object
spike.name = "Spike_3"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
spike.data.materials.append(bpy.data.materials["Iron"])

ws = [spike.matrix_world @ v.co for v in spike.data.vertices]
print(spike.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(spike.rotation_euler), "scale", tuple(spike.scale))

# ---------------------------------------------------------------------------
# Step 5 — Spike_4: the same cone at X = 0.16
import bpy

X = 0.16
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.07, radius2=0.0, depth=0.35, location=(X, 0, 0.12 + 0.175))
spike = bpy.context.active_object
spike.name = "Spike_4"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
spike.data.materials.append(bpy.data.materials["Iron"])

ws = [spike.matrix_world @ v.co for v in spike.data.vertices]
print(spike.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(spike.rotation_euler), "scale", tuple(spike.scale))

# ---------------------------------------------------------------------------
# Step 6 — Spike_5: the same cone at X = 0.32
import bpy

X = 0.32
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.07, radius2=0.0, depth=0.35, location=(X, 0, 0.12 + 0.175))
spike = bpy.context.active_object
spike.name = "Spike_5"
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
spike.data.materials.append(bpy.data.materials["Iron"])

ws = [spike.matrix_world @ v.co for v in spike.data.vertices]
print(spike.name, "x", round(min(w.x for w in ws), 4), round(max(w.x for w in ws), 4),
      "y", round(min(w.y for w in ws), 4), round(max(w.y for w in ws), 4),
      "z", round(min(w.z for w in ws), 4), round(max(w.z for w in ws), 4),
      "rot", tuple(spike.rotation_euler), "scale", tuple(spike.scale))

# ---------------------------------------------------------------------------
# Step 7 — check: objects, triangles, overall extent, colours read back from the nodes; then save
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
print("objects:", len(parts), "total triangles:", total, "(budget 100)")
print("extent X", round(lo.x, 4), round(hi.x, 4), "Y", round(lo.y, 4), round(hi.y, 4), "Z", round(lo.z, 4), round(hi.z, 4))
print("size", tuple(round(c, 4) for c in (hi - lo)))
to_srgb = lambda c: 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
for m in bpy.data.materials:
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    lin = bsdf.inputs["Base Color"].default_value
    print(m.name, "base colour back to sRGB hex: #" + "".join(f"{round(to_srgb(c) * 255):02X}" for c in lin[:3]))
bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath)

# ---------------------------------------------------------------------------
# Step 8 — join the six parts into one object, Spikes, with its origin at the world origin
# (the centre of its underside), then apply transforms
import bpy

names = ("Spikes_Base", "Spike_1", "Spike_2", "Spike_3", "Spike_4", "Spike_5")
parts = [bpy.data.objects[n] for n in names]
bpy.ops.object.select_all(action='DESELECT')
for o in parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()

spikes = bpy.context.active_object
spikes.name = "Spikes"
spikes.data.name = "Spikes"
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

print("objects:", [o.name for o in bpy.data.objects])
print(spikes.name, "loc", tuple(spikes.location), "rot", tuple(spikes.rotation_euler),
      "scale", tuple(spikes.scale), "dims", tuple(round(d, 4) for d in spikes.dimensions),
      "materials", [m.name for m in spikes.data.materials])

# ---------------------------------------------------------------------------
# Step 9 — check the joined spikes: triangles, extent, origin, faces per material; then save
import bpy, os, time
from mathutils import Vector

s = bpy.data.objects["Spikes"]
s.data.calc_loop_triangles()
ws = [s.matrix_world @ v.co for v in s.data.vertices]
lo = Vector((min(p.x for p in ws), min(p.y for p in ws), min(p.z for p in ws)))
hi = Vector((max(p.x for p in ws), max(p.y for p in ws), max(p.z for p in ws)))
print("triangles:", len(s.data.loop_triangles), "(budget 100)")
print("extent X", round(lo.x, 4), round(hi.x, 4), "Y", round(lo.y, 4), round(hi.y, 4), "Z", round(lo.z, 4), round(hi.z, 4))
print("origin", tuple(s.location), "underside centre", (round((lo.x + hi.x) / 2, 4), round((lo.y + hi.y) / 2, 4), round(lo.z, 4)))
counts = {}
for p in s.data.polygons:
    name = s.data.materials[p.material_index].name
    counts[name] = counts.get(name, 0) + 1
print("faces per material:", counts)
bpy.ops.wm.save_mainfile()
print("saved", bpy.data.filepath, "file mtime", time.ctime(os.path.getmtime(bpy.data.filepath)))
