# build_chest.py — Asset 3 (Treasure chest), Assignment 3.
# Verbatim record of every execute_blender_code body Claude Code ran through MCP for Blender 2.1.9
# (add-on 1.8) in Blender 5.2.2 LTS on 2026-10-14, in run order. Only this header, the
# "# --- call N" / "# --- Export" separator lines and the dated decision note were added. Approved split: body 0.376 m + lid 0.224 m (the brief's
# 0.35 + 0.25 does not fit an 8-vertex lid as deep as the body inside 0.5 m); total 0.8 x 0.5 x 0.6 m.

# --- call 1: clear the scene and confirm metric units
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

# --- call 2: wood and gold materials
# Chest materials: brief hex values are sRGB; Principled BSDF Base Color takes linear values.
# Wood: metallic 0, roughness 0.8. Gold: metallic 1.0, roughness 0.35 (approved 2026-10-14).
import bpy

def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def make_material(name, hex_srgb, metallic, roughness):
    rgb = [srgb_to_linear(int(hex_srgb[i:i + 2], 16)) for i in (0, 2, 4)]
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = (*rgb, 1.0)  # viewport (Solid mode) colour only
    print(name, "#" + hex_srgb, "-> linear", tuple(round(v, 4) for v in rgb),
          "| metallic", bsdf.inputs["Metallic"].default_value, "| roughness", round(bsdf.inputs["Roughness"].default_value, 3))

make_material("Chest_Wood", "8A5A2B", 0.0, 0.8)
make_material("Chest_Gold", "D4A73A", 1.0, 0.35)

# --- call 3: Chest_Body
# Chest_Body: cube placed by its world extents (metres). Object scale sets the size, rotation stays 0,
# and the result is checked from the real world-space vertex bounds.
import bpy

NAME, MAT = "Chest_Body", "Chest_Wood"
X, Y, Z = (-0.400, 0.400), (-0.225, 0.225), (0.000, 0.376)

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
ob.scale = (X[1] - X[0], Y[1] - Y[0], Z[1] - Z[0])
ob.rotation_euler = (0.0, 0.0, 0.0)
ob.location = ((X[0] + X[1]) / 2, (Y[0] + Y[1]) / 2, (Z[0] + Z[1]) / 2)
bpy.context.view_layer.update()
ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in ob.data.vertices]
wx, wy, wz = zip(*w)
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4),
      "| size", round(max(wx) - min(wx), 4), round(max(wy) - min(wy), 4), round(max(wz) - min(wz), 4),
      "| triangles", sum(len(p.vertices) - 2 for p in ob.data.polygons))

# --- call 4: Chest_Lid (and the true-top check)
# Chest_Lid: 8-vertex cylinder laid along X with one side face pointing exactly up (flat top). Both turns
# are baked into the mesh, so object rotation stays 0; object scale sets the size across the flats.
# Centre on the body top (z 0.376), so the lower half is sunk into the body. Checks the true top height.
import bpy, math
from mathutils import Matrix, Vector

NAME, MAT = "Chest_Lid", "Chest_Wood"
SIZE = (0.798, 0.448, 0.448)          # world X length, Y and Z across the flats, in metres
CENTRE = (0.0, 0.0, 0.376)
TOTAL_HEIGHT = 0.600                  # brief: the lid top must reach this

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.0, depth=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
me = ob.data

# Bake: axis along X, then turn about X until a side face points exactly up.
me.transform(Matrix.Rotation(math.radians(90.0), 4, "Y"))
me.update()
sides = [p for p in me.polygons if len(p.vertices) == 4]
up = max(sides, key=lambda p: p.normal.z)
q = up.normal.rotation_difference(Vector((0, 0, 1)))
me.transform(q.to_matrix().to_4x4())
me.update()

xs, ys, zs = zip(*(v.co for v in me.vertices))
dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
s = tuple(t / d for t, d in zip(SIZE, dims))
ob.scale = s
ob.rotation_euler = (0.0, 0.0, 0.0)
ob.location = tuple(c - (lo + hi) / 2 * k for c, lo, hi, k in
                    zip(CENTRE, (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs)), s))
bpy.context.view_layer.update()
ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in me.vertices]
wx, wy, wz = zip(*w)
top = max(me.polygons, key=lambda p: (ob.matrix_world.to_3x3() @ p.normal).normalized().z)
top_z = [round((ob.matrix_world @ me.vertices[i].co).z, 5) for i in top.vertices]
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4),
      "| size", round(max(wx) - min(wx), 4), round(max(wy) - min(wy), 4), round(max(wz) - min(wz), 4))
print("true top z:", round(max(wz), 4), "| reaches", TOTAL_HEIGHT, ":", abs(max(wz) - TOTAL_HEIGHT) < 1e-4,
      "| top face normal:", tuple(round(c, 4) for c in (ob.matrix_world.to_3x3() @ top.normal).normalized()),
      "| top face vertex z:", top_z)
print("faces:", len(me.polygons), "| triangles:", sum(len(p.vertices) - 2 for p in me.polygons))

# --- call 5: Chest_Lock
# Chest_Lock: small cube on the front (Blender -Y), sunk 5 mm into the body, straddling the lid line
# (z 0.376). Placed by its world extents, checked from the real world-space vertex bounds.
import bpy

NAME, MAT = "Chest_Lock", "Chest_Gold"
X, Y, Z = (-0.050, 0.050), (-0.265, -0.220), (0.310, 0.430)

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
ob.scale = (X[1] - X[0], Y[1] - Y[0], Z[1] - Z[0])
ob.rotation_euler = (0.0, 0.0, 0.0)
ob.location = ((X[0] + X[1]) / 2, (Y[0] + Y[1]) / 2, (Z[0] + Z[1]) / 2)
bpy.context.view_layer.update()
ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in ob.data.vertices]
wx, wy, wz = zip(*w)
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4),
      "| size", round(max(wx) - min(wx), 4), round(max(wy) - min(wy), 4), round(max(wz) - min(wz), 4),
      "| triangles", sum(len(p.vertices) - 2 for p in ob.data.polygons))

# --- call 6: Chest_Band_L
# Chest_Band_L: thin cube metal band around the body (10 mm proud of front and back), left of centre.
# Placed by its world extents, checked from the real world-space vertex bounds.
import bpy

NAME, MAT = "Chest_Band_L", "Chest_Gold"
X, Y, Z = (-0.270, -0.210), (-0.235, 0.235), (0.000, 0.376)

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
ob.scale = (X[1] - X[0], Y[1] - Y[0], Z[1] - Z[0])
ob.rotation_euler = (0.0, 0.0, 0.0)
ob.location = ((X[0] + X[1]) / 2, (Y[0] + Y[1]) / 2, (Z[0] + Z[1]) / 2)
bpy.context.view_layer.update()
ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in ob.data.vertices]
wx, wy, wz = zip(*w)
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4),
      "| size", round(max(wx) - min(wx), 4), round(max(wy) - min(wy), 4), round(max(wz) - min(wz), 4),
      "| triangles", sum(len(p.vertices) - 2 for p in ob.data.polygons))

# --- call 7: Chest_Band_R, then the combined bounds and the front (lock on -Y) check
# Chest_Band_R: thin cube metal band around the body (10 mm proud of front and back), right of centre.
# Placed by its world extents, checked from the real world-space vertex bounds. Then reports the
# combined bounds of all five parts and checks that the lock is the front-most part, on the -Y side.
import bpy

NAME, MAT = "Chest_Band_R", "Chest_Gold"
X, Y, Z = (0.210, 0.270), (-0.235, 0.235), (0.000, 0.376)

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
ob.scale = (X[1] - X[0], Y[1] - Y[0], Z[1] - Z[0])
ob.rotation_euler = (0.0, 0.0, 0.0)
ob.location = ((X[0] + X[1]) / 2, (Y[0] + Y[1]) / 2, (Z[0] + Z[1]) / 2)
bpy.context.view_layer.update()
ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in ob.data.vertices]
wx, wy, wz = zip(*w)
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4),
      "| size", round(max(wx) - min(wx), 4), round(max(wy) - min(wy), 4), round(max(wz) - min(wz), 4),
      "| triangles", sum(len(p.vertices) - 2 for p in ob.data.polygons))

names = ("Chest_Body", "Chest_Lid", "Chest_Lock", "Chest_Band_L", "Chest_Band_R")
per = {}
for n in names:
    o = bpy.data.objects[n]
    per[n] = [o.matrix_world @ v.co for v in o.data.vertices]
allw = [p for pts in per.values() for p in pts]
ax, ay, az = zip(*allw)
print("combined: x", round(min(ax), 4), round(max(ax), 4), "| y", round(min(ay), 4), round(max(ay), 4),
      "| z", round(min(az), 4), round(max(az), 4),
      "| size", round(max(ax) - min(ax), 4), round(max(ay) - min(ay), 4), round(max(az) - min(az), 4),
      "| triangles", sum(sum(len(p.vertices) - 2 for p in bpy.data.objects[n].data.polygons) for n in names))
front = min(names, key=lambda n: min(p.y for p in per[n]))
lock_cy = sum(p.y for p in per["Chest_Lock"]) / len(per["Chest_Lock"])
print("front-most part (smallest y):", front, "| lock centre y:", round(lock_cy, 4), "| lock on -Y side:", lock_cy < 0)

# --- call 8: join, apply rotation and scale, fit check, origin to the centre of the underside
# Join the five parts into one object "Chest" (Chest_Body active), apply rotation and scale, check the
# fit factors against the brief (fit only if every factor is within 0.95-1.05), then move the mesh so
# the lowest point is at Z = 0 and the centre of the underside is the origin, at the world origin.
import bpy
from mathutils import Matrix, Vector

BRIEF = (0.8, 0.5, 0.6)              # W x D x H in metres, from CHANGE-BRIEF.md
FIT_LIMITS = (0.95, 1.05)
NAMES = ("Chest_Body", "Chest_Lid", "Chest_Lock", "Chest_Band_L", "Chest_Band_R")

parts = [bpy.data.objects[n] for n in NAMES]
for ob in bpy.context.view_layer.objects:
    ob.select_set(False)
for ob in parts:
    ob.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()

chest = bpy.context.active_object
chest.name = chest.data.name = "Chest"
for m in list(bpy.data.meshes):
    if m.users == 0:
        bpy.data.meshes.remove(m)

bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

me = chest.data
me.transform(Matrix.Translation(chest.location))   # bake the location too, then work in world space
chest.location = (0.0, 0.0, 0.0)
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
print("size before fit:", tuple(round(d, 4) for d in before), "| bottom centre moved from", tuple(round(c, 4) for c in bottom_centre))
print("fit factors:", tuple(round(f, 4) for f in factors), "| within", FIT_LIMITS, ":", fit_ok,
      "| fit applied:", fit_ok)
print("x", round(min(xs), 4), round(max(xs), 4), "| y", round(min(ys), 4), round(max(ys), 4),
      "| z", round(min(zs), 4), round(max(zs), 4))
print("dimensions:", tuple(round(d, 4) for d in chest.dimensions))
print("location:", tuple(chest.location), "| rotation:", tuple(chest.rotation_euler), "| scale:", tuple(chest.scale))
me.calc_loop_triangles()
print("objects:", [o.name for o in bpy.data.objects], "| triangles:", len(me.loop_triangles),
      "| faces:", len(me.polygons), "| materials:", [m.name for m in me.materials])
by_mat = {}
for t in me.loop_triangles:
    by_mat[me.materials[t.material_index].name] = by_mat.get(me.materials[t.material_index].name, 0) + 1
print("triangles per material:", by_mat)
gold_y = [me.vertices[i].co.y for p in me.polygons if me.materials[p.material_index].name == "Chest_Gold" for i in p.vertices]
print("front-most point y:", round(min(ys), 4), "| is gold (lock):", abs(min(gold_y) - min(ys)) < 1e-6)

# 2026-10-14, Zhefan's decision after looking at the joined chest: Chest_Gold lowered from metallic 1.0 /
# roughness 0.35 to metallic 0.3 / roughness 0.5, because fully metallic gold read dark olive without
# reflections and the cave scene has only one light. Chest_Wood unchanged.

# --- call 9: lower Chest_Gold to metallic 0.3, roughness 0.5
# Lower Chest_Gold to metallic 0.3, roughness 0.5 (Zhefan's change, 2026-10-14): fully metallic gold read
# dark olive without reflections, and the cave scene has only one light. Chest_Wood is left as it is.
# First checks that the open scene is still the joined Chest.
import bpy

objs = [(o.name, o.type) for o in bpy.data.objects]
if objs != [("Chest", "MESH")]:
    raise RuntimeError("open scene is not the joined Chest: " + repr(objs))

for name, metallic, roughness in (("Chest_Gold", 0.3, 0.5),):
    bsdf = next(n for n in bpy.data.materials[name].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    print(name, "before: metallic", bsdf.inputs["Metallic"].default_value,
          "roughness", round(bsdf.inputs["Roughness"].default_value, 3))
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness

for name in ("Chest_Wood", "Chest_Gold"):
    bsdf = next(n for n in bpy.data.materials[name].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    print(name, "now: base", tuple(round(v, 4) for v in bsdf.inputs["Base Color"].default_value),
          "| metallic", round(bsdf.inputs["Metallic"].default_value, 3),
          "| roughness", round(bsdf.inputs["Roughness"].default_value, 3))

# --- call S1: save the .blend source
# Save the .blend source for the Chest. Refuses to overwrite an existing file, and refuses if the open
# scene is not the joined Chest.
import bpy, os

PATH = r"E:\7270\csye-7270-course\fall-2026\zhefan-z\assignment-3\walker-magic-zhefan\tools\blender\chest.blend"

objs = [(o.name, o.type) for o in bpy.data.objects]
if objs != [("Chest", "MESH")]:
    raise RuntimeError("open scene is not the joined Chest: " + repr(objs))
if os.path.exists(PATH):
    raise RuntimeError("refusing to overwrite " + PATH)
print("objects:", objs, "| meshes:", [m.name for m in bpy.data.meshes],
      "| materials:", [(m.name, m.users) for m in bpy.data.materials])
bpy.ops.wm.save_as_mainfile(filepath=PATH)
print("saved:", bpy.data.filepath, "|", os.path.getsize(PATH), "bytes",
      "| save versions setting:", bpy.context.preferences.filepaths.save_version)

# --- Export

# --- call E1: export chest.glb
# Export the Chest as binary glTF (.glb) with the same settings as rock.glb: +Y Up on, materials
# included. Refuses to overwrite, and refuses if the open scene is not the saved chest.blend.
import bpy, os

PATH = r"E:\7270\csye-7270-course\fall-2026\zhefan-z\assignment-3\walker-magic-zhefan\assets\models\chest.glb"

if not bpy.data.filepath.endswith("chest.blend") or "Chest" not in bpy.data.objects:
    raise RuntimeError("open file is not chest.blend with Chest: " + repr(bpy.data.filepath))
if os.path.exists(PATH):
    raise RuntimeError("refusing to overwrite " + PATH)
os.makedirs(os.path.dirname(PATH), exist_ok=True)

chest = bpy.data.objects["Chest"]
for ob in bpy.context.view_layer.objects:
    ob.select_set(False)
chest.select_set(True)
bpy.context.view_layer.objects.active = chest

settings = dict(
    filepath=PATH,
    export_format="GLB",            # dynamic enum; an invalid value raises TypeError listing the valid ones
    use_selection=True,
    export_yup=True,
    export_materials="EXPORT",
    export_apply=False,             # Chest has no modifiers
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
print("result:", result, "|", PATH, os.path.getsize(PATH), "bytes", "| unsaved changes after export:", bpy.data.is_dirty)
print("settings:", {k: v for k, v in settings.items() if k != "filepath"})
