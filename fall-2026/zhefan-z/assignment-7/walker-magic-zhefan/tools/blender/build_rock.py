# build_rock.py — Asset 1 (Rock), Assignment 3.
# Verbatim record of every execute_blender_code body Claude Code ran through MCP for Blender 2.1.9
# (add-on 1.8) in Blender 5.2.2 LTS on 2026-10-14, in run order. Only this header, the "# --- call N"
# separator lines and the "# --- Revision 1" line were added. Call 4 is a second run of Rock_A after
# call 3's size check; it replaces call 3's object, so the file can run top to bottom. Revision 1
# (calls R1-R6) removes the first-build Rock and rebuilds it.

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

# --- call 2: materials
# Materials: brief hex values are sRGB; Principled BSDF Base Color takes linear values.
import bpy

def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def make_material(name, hex_srgb):
    rgb = [srgb_to_linear(int(hex_srgb[i:i + 2], 16)) for i in (0, 2, 4)]
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.9
    mat.diffuse_color = (*rgb, 1.0)  # viewport (Solid mode) colour only
    print(name, "#" + hex_srgb, "-> linear", tuple(round(v, 4) for v in rgb))

make_material("Rock_Main", "343539")
make_material("Rock_Top", "797069")

# --- call 3: Rock_A, first run (world box came out 0.80 x 0.92 x 0.50 m; replaced by call 4)
# Rock_A, main body: ico sphere (subdivisions 1), turned in mesh data so a flat face points down,
# sized by measured dimensions (not radius), base on Z = 0, small turn around Z.
import bpy, math
from mathutils import Vector

NAME, MAT = "Rock_A", "Rock_Main"
TARGET = (0.65, 0.80, 0.50)          # W x D x H in metres, before the final fit
LOC_XY = (-0.15, 0.0)
ROT_Z_DEG = 12.0

old = bpy.data.objects.get(NAME)
if old:
    bpy.data.objects.remove(old, do_unlink=True)

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME

# Turn the mesh so its lowest face is exactly horizontal, facing -Z.
me = ob.data
low = min(me.polygons, key=lambda p: p.normal.z)
q = low.normal.rotation_difference(Vector((0, 0, -1)))
me.transform(q.to_matrix().to_4x4())
me.update()

xs, ys, zs = zip(*(v.co for v in me.vertices))
dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
ob.scale = tuple(t / d for t, d in zip(TARGET, dims))
ob.rotation_euler = (0.0, 0.0, math.radians(ROT_Z_DEG))
ob.location = (LOC_XY[0], LOC_XY[1], -min(zs) * ob.scale.z)

ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

bottom = [v for v in me.vertices if abs(v.co.z - min(zs)) < 1e-5]
print(NAME, "triangles:", sum(len(p.vertices) - 2 for p in me.polygons),
      "| vertices on the floor:", len(bottom), "| bottom face normal:", tuple(round(c, 4) for c in low.normal))

# --- call 4: Rock_A, second run
# Rock_A, main body (second run): the first run's Z turn widened the world box to 0.80 x 0.92 m,
# so the pre-turn target is reduced. Same method: ico sphere (subdivisions 1), flat face down,
# sized by measured dimensions, base on Z = 0, small turn around Z.
import bpy, math
from mathutils import Vector

NAME, MAT = "Rock_A", "Rock_Main"
TARGET = (0.50, 0.68, 0.50)          # local W x D x H in metres, before the Z turn and the final fit
LOC_XY = (-0.15, 0.0)
ROT_Z_DEG = 12.0

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME

# Turn the mesh so its lowest face is exactly horizontal, facing -Z.
me = ob.data
low = min(me.polygons, key=lambda p: p.normal.z)
q = low.normal.rotation_difference(Vector((0, 0, -1)))
me.transform(q.to_matrix().to_4x4())
me.update()

xs, ys, zs = zip(*(v.co for v in me.vertices))
dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
ob.scale = tuple(t / d for t, d in zip(TARGET, dims))
ob.rotation_euler = (0.0, 0.0, math.radians(ROT_Z_DEG))
ob.location = (LOC_XY[0], LOC_XY[1], -min(zs) * ob.scale.z)

ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

bottom = [v for v in me.vertices if abs(v.co.z - min(zs)) < 1e-5]
print(NAME, ob.data.name, "triangles:", sum(len(p.vertices) - 2 for p in me.polygons),
      "| vertices on the floor:", len(bottom), "| meshes in file:", [m.name for m in bpy.data.meshes])

# --- call 5: Rock_B
# Rock_B, side stone: ico sphere (subdivisions 1), flat face down, sized by measured dimensions,
# base on Z = 0, right of centre and overlapping Rock_A, small turn around Z the other way.
import bpy, math
from mathutils import Vector

NAME, MAT = "Rock_B", "Rock_Main"
TARGET = (0.37, 0.47, 0.38)          # local W x D x H in metres, before the Z turn and the final fit
LOC_XY = (0.27, 0.06)
ROT_Z_DEG = -20.0

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME

# Turn the mesh so its lowest face is exactly horizontal, facing -Z.
me = ob.data
low = min(me.polygons, key=lambda p: p.normal.z)
q = low.normal.rotation_difference(Vector((0, 0, -1)))
me.transform(q.to_matrix().to_4x4())
me.update()

xs, ys, zs = zip(*(v.co for v in me.vertices))
dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
ob.scale = tuple(t / d for t, d in zip(TARGET, dims))
ob.rotation_euler = (0.0, 0.0, math.radians(ROT_Z_DEG))
ob.location = (LOC_XY[0], LOC_XY[1], -min(zs) * ob.scale.z)

ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

bottom = [v for v in me.vertices if abs(v.co.z - min(zs)) < 1e-5]
print(NAME, ob.data.name, "triangles:", sum(len(p.vertices) - 2 for p in me.polygons),
      "| vertices on the floor:", len(bottom))

# --- call 6: Rock_C
# Rock_C, top stone: ico sphere (subdivisions 1) in the highlight colour, tilted slightly on all three
# axes, resting sunk into Rock_A with its top at Z = 0.70 m. It does not touch the floor.
import bpy, math
from mathutils import Vector

NAME, MAT = "Rock_C", "Rock_Top"
TARGET = (0.38, 0.34, 0.27)          # local W x D x H in metres, before the tilt and the final fit
LOC_XY = (-0.08, 0.0)
ROT_DEG = (8.0, -10.0, 35.0)
TOP_Z = 0.70

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
me = ob.data

xs, ys, zs = zip(*(v.co for v in me.vertices))
dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
ob.scale = tuple(t / d for t, d in zip(TARGET, dims))
ob.rotation_euler = tuple(math.radians(a) for a in ROT_DEG)
ob.location = (LOC_XY[0], LOC_XY[1], 0.0)
bpy.context.view_layer.update()

world = [ob.matrix_world @ v.co for v in me.vertices]
ob.location.z = TOP_Z - max(w.z for w in world)
bpy.context.view_layer.update()

ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

# Is Rock_C's lowest vertex inside Rock_A (so the top stone is sunk in, not floating)?
a = bpy.data.objects["Rock_A"]
lowest = min((ob.matrix_world @ v.co for v in me.vertices), key=lambda w: w.z)
p_local = a.matrix_world.inverted() @ lowest
ok, hit, normal, _ = a.closest_point_on_mesh(p_local)
inside = ok and (p_local - hit).dot(normal) < 0
print(NAME, ob.data.name, "triangles:", sum(len(p.vertices) - 2 for p in me.polygons),
      "| lowest vertex z:", round(lowest.z, 3), "| inside Rock_A:", inside)

# --- call 7: join, apply rotation and scale, fit to the brief, origin to the centre of the underside
# Join Rock_A/B/C into one object "Rock", apply rotation and scale, fit the mesh to the brief's
# size, and put the origin at the centre of the underside, at the world origin (base on Z = 0).
import bpy
from mathutils import Matrix, Vector

BRIEF = (1.0, 0.8, 0.7)              # W x D x H in metres, from CHANGE-BRIEF.md

parts = [bpy.data.objects[n] for n in ("Rock_A", "Rock_B", "Rock_C")]
for ob in bpy.context.view_layer.objects:
    ob.select_set(False)
for ob in parts:
    ob.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()

rock = bpy.context.active_object
rock.name = rock.data.name = "Rock"
for m in list(bpy.data.meshes):
    if m.users == 0:
        bpy.data.meshes.remove(m)

bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

me = rock.data
xs, ys, zs = zip(*(v.co for v in me.vertices))
before = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
factors = tuple(b / d for b, d in zip(BRIEF, before))
bottom_centre = Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, min(zs)))

# Move the bottom centre to the mesh origin, then scale the mesh to the brief's size about that point.
me.transform(Matrix.Translation(-bottom_centre))
me.transform(Matrix.Diagonal((*factors, 1.0)))
me.update()
rock.location = (0.0, 0.0, 0.0)
bpy.context.view_layer.update()

xs, ys, zs = zip(*(v.co for v in me.vertices))
print("size before fit:", tuple(round(d, 4) for d in before))
print("fit factors:", tuple(round(f, 4) for f in factors))
print("x", round(min(xs), 4), round(max(xs), 4), "| y", round(min(ys), 4), round(max(ys), 4),
      "| z", round(min(zs), 4), round(max(zs), 4))
print("dimensions:", tuple(round(d, 4) for d in rock.dimensions))
print("location:", tuple(rock.location), "| rotation:", tuple(rock.rotation_euler), "| scale:", tuple(rock.scale))
me.calc_loop_triangles()
print("objects:", [o.name for o in bpy.data.objects], "| triangles:", len(me.loop_triangles),
      "| faces:", len(me.polygons), "| materials:", [m.name for m in me.materials])

# --- Revision 1 (2026-10-14): parts overlap as one mass; sized from mesh bounds

# --- call R1: remove the first-build Rock, keep the materials
# R1: remove the first-build Rock (object and mesh); keep the two materials.
import bpy

old = bpy.data.objects.get("Rock")
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

print("objects:", [o.name for o in bpy.data.objects], "| meshes:", [m.name for m in bpy.data.meshes],
      "| materials:", [(m.name, m.users) for m in bpy.data.materials])

# --- call R2: Rock_A
# R2: Rock_A, main body. Ico sphere (subdivisions 1); the face-down turn and the Z turn are baked into
# the mesh, so object rotation stays 0 and scaling along world axes sets the world size exactly.
# Sized and placed from the real world-space vertex bounds.
import bpy, math
from mathutils import Matrix, Vector

NAME, MAT = "Rock_A", "Rock_Main"
TARGET = (0.62, 0.80, 0.52)          # world W x D x H in metres
X_MIN, Y_CENTRE = -0.50, 0.0         # left edge and depth centre, in world space
ROT_Z_DEG = 12.0

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
me = ob.data

# Bake: lowest face exactly horizontal facing -Z, then the turn around Z (keeps that face horizontal).
low = min(me.polygons, key=lambda p: p.normal.z)
q = low.normal.rotation_difference(Vector((0, 0, -1)))
me.transform(Matrix.Rotation(math.radians(ROT_Z_DEG), 4, "Z") @ q.to_matrix().to_4x4())
me.update()

xs, ys, zs = zip(*(v.co for v in me.vertices))
dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
s = tuple(t / d for t, d in zip(TARGET, dims))
ob.scale = s
ob.rotation_euler = (0.0, 0.0, 0.0)
ob.location = (X_MIN - min(xs) * s[0],
               Y_CENTRE - (min(ys) + max(ys)) / 2 * s[1],
               -min(zs) * s[2])
bpy.context.view_layer.update()

ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in me.vertices]
wx, wy, wz = zip(*w)
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4))
print("world size:", round(max(wx) - min(wx), 4), round(max(wy) - min(wy), 4), round(max(wz) - min(wz), 4),
      "| vertices on the floor:", sum(1 for z in wz if abs(z) < 1e-5),
      "| triangles:", sum(len(p.vertices) - 2 for p in me.polygons))

# --- call R3: Rock_B and the Rock_A/Rock_B intersection check
# R3: Rock_B, side stone. Same method as R2 (turns baked into the mesh, sized from world vertex bounds),
# placed so it overlaps Rock_A by 0.20 m in X. Then checks that the two meshes really intersect.
import bpy, math
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

NAME, MAT = "Rock_B", "Rock_Main"
TARGET = (0.58, 0.66, 0.42)          # world W x D x H in metres
X_MIN, Y_CENTRE = -0.08, 0.04        # left edge and depth centre, in world space
ROT_Z_DEG = -20.0

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
me = ob.data

# Bake: lowest face exactly horizontal facing -Z, then the turn around Z (keeps that face horizontal).
low = min(me.polygons, key=lambda p: p.normal.z)
q = low.normal.rotation_difference(Vector((0, 0, -1)))
me.transform(Matrix.Rotation(math.radians(ROT_Z_DEG), 4, "Z") @ q.to_matrix().to_4x4())
me.update()

xs, ys, zs = zip(*(v.co for v in me.vertices))
dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
s = tuple(t / d for t, d in zip(TARGET, dims))
ob.scale = s
ob.rotation_euler = (0.0, 0.0, 0.0)
ob.location = (X_MIN - min(xs) * s[0],
               Y_CENTRE - (min(ys) + max(ys)) / 2 * s[1],
               -min(zs) * s[2])
bpy.context.view_layer.update()

ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in me.vertices]
wx, wy, wz = zip(*w)
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4))
print("world size:", round(max(wx) - min(wx), 4), round(max(wy) - min(wy), 4), round(max(wz) - min(wz), 4),
      "| vertices on the floor:", sum(1 for z in wz if abs(z) < 1e-5),
      "| triangles:", sum(len(p.vertices) - 2 for p in me.polygons))

# Do Rock_A and Rock_B intersect? Compare the two meshes in world space.
def world_bvh(o):
    m = o.matrix_world
    return BVHTree.FromPolygons([m @ v.co for v in o.data.vertices], [p.vertices[:] for p in o.data.polygons])

a = bpy.data.objects["Rock_A"]
pairs = world_bvh(a).overlap(world_bvh(ob))
b_inside_a = 0
for v in me.vertices:
    p = a.matrix_world.inverted() @ (ob.matrix_world @ v.co)
    ok, hit, normal, _ = a.closest_point_on_mesh(p)
    b_inside_a += ok and (p - hit).dot(normal) < 0
print("Rock_A/Rock_B intersecting face pairs:", len(pairs), "| Rock_B vertices inside Rock_A:", b_inside_a)

# --- call R4: Rock_C and the sunk-in check
# R4: Rock_C, top stone. Ico sphere (subdivisions 1) with the 8, -10, 35 degree tilt baked into the mesh,
# sized from world vertex bounds, centred over the Rock_A/Rock_B joint with its top at Z = 0.70 m.
# Then checks that its lowest vertex is inside Rock_A or Rock_B (sunk in, not floating).
import bpy, math
from mathutils import Euler, Vector

NAME, MAT = "Rock_C", "Rock_Top"
TARGET = (0.46, 0.42, 0.30)          # world W x D x H in metres
X_CENTRE, Y_CENTRE, TOP_Z = -0.02, 0.0, 0.70
ROT_DEG = (8.0, -10.0, 35.0)

old = bpy.data.objects.get(NAME)
if old:
    old_mesh = old.data
    bpy.data.objects.remove(old, do_unlink=True)
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(0, 0, 0))
ob = bpy.context.active_object
ob.name = ob.data.name = NAME
me = ob.data
me.transform(Euler([math.radians(a) for a in ROT_DEG], "XYZ").to_matrix().to_4x4())
me.update()

xs, ys, zs = zip(*(v.co for v in me.vertices))
dims = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
s = tuple(t / d for t, d in zip(TARGET, dims))
ob.scale = s
ob.rotation_euler = (0.0, 0.0, 0.0)
ob.location = (X_CENTRE - (min(xs) + max(xs)) / 2 * s[0],
               Y_CENTRE - (min(ys) + max(ys)) / 2 * s[1],
               TOP_Z - max(zs) * s[2])
bpy.context.view_layer.update()

ob.data.materials.clear()
ob.data.materials.append(bpy.data.materials[MAT])

w = [ob.matrix_world @ v.co for v in me.vertices]
wx, wy, wz = zip(*w)
print(NAME, "world vertex bounds: x", round(min(wx), 4), round(max(wx), 4), "| y", round(min(wy), 4), round(max(wy), 4),
      "| z", round(min(wz), 4), round(max(wz), 4))
print("world size:", round(max(wx) - min(wx), 4), round(max(wy) - min(wy), 4), round(max(wz) - min(wz), 4),
      "| triangles:", sum(len(p.vertices) - 2 for p in me.polygons))

lowest = min(w, key=lambda p: p.z)
def inside(o, p_world):
    p = o.matrix_world.inverted() @ p_world
    ok, hit, normal, _ = o.closest_point_on_mesh(p)
    return bool(ok and (p - hit).dot(normal) < 0)
print("Rock_C lowest vertex", tuple(round(c, 3) for c in lowest),
      "| inside Rock_A:", inside(bpy.data.objects["Rock_A"], lowest),
      "| inside Rock_B:", inside(bpy.data.objects["Rock_B"], lowest))

# --- call R5: join, apply rotation and scale, fit to the brief, origin to the centre of the underside
# R5: same as call 7. Join Rock_A/B/C into one object "Rock", apply rotation and scale, fit the mesh to the
# brief's size, and put the origin at the centre of the underside, at the world origin (base on Z = 0).
import bpy
from mathutils import Matrix, Vector

BRIEF = (1.0, 0.8, 0.7)              # W x D x H in metres, from CHANGE-BRIEF.md

parts = [bpy.data.objects[n] for n in ("Rock_A", "Rock_B", "Rock_C")]
for ob in bpy.context.view_layer.objects:
    ob.select_set(False)
for ob in parts:
    ob.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()

rock = bpy.context.active_object
rock.name = rock.data.name = "Rock"
for m in list(bpy.data.meshes):
    if m.users == 0:
        bpy.data.meshes.remove(m)

bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

me = rock.data
xs, ys, zs = zip(*(v.co for v in me.vertices))
before = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
factors = tuple(b / d for b, d in zip(BRIEF, before))
bottom_centre = Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, min(zs)))

# Move the bottom centre to the mesh origin, then scale the mesh to the brief's size about that point.
me.transform(Matrix.Translation(-bottom_centre))
me.transform(Matrix.Diagonal((*factors, 1.0)))
me.update()
rock.location = (0.0, 0.0, 0.0)
bpy.context.view_layer.update()

xs, ys, zs = zip(*(v.co for v in me.vertices))
print("size before fit:", tuple(round(d, 4) for d in before))
print("fit factors:", tuple(round(f, 4) for f in factors))
print("x", round(min(xs), 4), round(max(xs), 4), "| y", round(min(ys), 4), round(max(ys), 4),
      "| z", round(min(zs), 4), round(max(zs), 4))
print("dimensions:", tuple(round(d, 4) for d in rock.dimensions))
print("location:", tuple(rock.location), "| rotation:", tuple(rock.rotation_euler), "| scale:", tuple(rock.scale))
me.calc_loop_triangles()
print("objects:", [o.name for o in bpy.data.objects], "| triangles:", len(me.loop_triangles),
      "| faces:", len(me.polygons), "| materials:", [m.name for m in me.materials])

# --- call R6: notch check (read-only)
# R6: read-only notch check on the joined Rock, as seen from the front or back (both share this outline).
# Rays on a 1 cm grid: down from above for the top outline, up from below for the floor outline.
# Top notch: deepest dip of the top outline below the peaks on both sides of it.
# Floor notch: highest rise of the floor outline above the lowest points on both sides of it
# (a gap between two stones that both stand on the floor). Threshold 0.03 m, agreed 2026-10-14.
import bpy
from mathutils import Vector

THRESHOLD = 0.03
rock = bpy.data.objects["Rock"]
inv = rock.matrix_world.inverted()

xs = [round(-0.5 + i * 0.01, 2) for i in range(101)]
ys = [round(-0.4 + j * 0.01, 2) for j in range(81)]

def cast(x, y, z0, dz):
    ok, loc, _, _ = rock.ray_cast(inv @ Vector((x, y, z0)), Vector((0, 0, dz)))
    return (rock.matrix_world @ loc).z if ok else None

top, bottom = [], []
for x in xs:
    t = [z for z in (cast(x, y, 2.0, -1) for y in ys) if z is not None]
    b = [z for z in (cast(x, y, -1.0, 1) for y in ys) if z is not None]
    top.append(max(t) if t else None)
    bottom.append(min(b) if b else None)

cols = [i for i, z in enumerate(top) if z is not None]
def worst(profile, sign):
    # sign=+1: dip below both side maxima (top); sign=-1: rise above both side minima (floor).
    best = (0.0, None)
    for k in range(1, len(cols) - 1):
        i = cols[k]
        left = [sign * profile[j] for j in cols[:k]]
        right = [sign * profile[j] for j in cols[k + 1:]]
        depth = min(max(left), max(right)) - sign * profile[i]
        if depth > best[0]:
            best = (depth, xs[i])
    return best

top_notch, top_x = worst(top, +1)
floor_notch, floor_x = worst(bottom, -1)
print("columns hit:", len(cols), "of", len(xs))
print("top outline every 0.1 m:", [(xs[i], round(top[i], 3)) for i in range(0, 101, 10) if top[i] is not None])
print("floor outline every 0.1 m:", [(xs[i], round(bottom[i], 3)) for i in range(0, 101, 10) if bottom[i] is not None])
print("top notch depth:", round(top_notch, 4), "m at x =", top_x, "| pass:", top_notch <= THRESHOLD)
print("floor notch height:", round(floor_notch, 4), "m at x =", floor_x, "| pass:", floor_notch <= THRESHOLD)

# 2026-10-14, my decision (Zhefan) after my own viewport look, including low angles: Revision 1 accepted as is; the 0.066 m floor gap under the Rock_A/Rock_B joint (R6 fail) is a known limitation: it sits at the base, in shadow at game camera height, and the planned box collider covers it.

# --- call S1: save the .blend source
# Save the .blend source for the Rock. Refuses to overwrite an existing file.
import bpy, os

PATH = r"E:\7270\csye-7270-course\fall-2026\zhefan-z\assignment-3\walker-magic-zhefan\tools\blender\rock.blend"

if os.path.exists(PATH):
    raise RuntimeError("refusing to overwrite " + PATH)
print("objects:", [(o.name, o.type) for o in bpy.data.objects], "| meshes:", [m.name for m in bpy.data.meshes],
      "| materials:", [(m.name, m.users) for m in bpy.data.materials])
bpy.ops.wm.save_as_mainfile(filepath=PATH)
print("saved:", bpy.data.filepath, "|", os.path.getsize(PATH), "bytes",
      "| save versions setting:", bpy.context.preferences.filepaths.save_version)

# --- Export

# --- call E1: read the glTF exporter's version and defaults (read-only)
# Read-only: the glTF exporter's version and the defaults of the settings this export depends on.
import bpy, addon_utils

for mod in addon_utils.modules():
    if mod.__name__.endswith("io_scene_gltf2"):
        print("glTF add-on:", mod.__name__, "version", mod.bl_info.get("version"),
              "| enabled:", addon_utils.check(mod.__name__))

props = bpy.ops.export_scene.gltf.get_rna_type().properties
for key in ("export_format", "export_yup", "export_materials", "use_selection", "export_apply",
            "export_normals", "export_texcoords", "export_cameras", "export_lights",
            "export_extras", "export_animations", "export_skins", "export_morph"):
    if key not in props:
        print(key, "-> not in this version")
        continue
    p = props[key]
    if p.type == "ENUM":
        print(key, "default:", p.default, "| options:", [i.identifier for i in p.enum_items])
    else:
        print(key, "default:", p.default)

# --- call E2: export rock.glb
# Export the Rock as binary glTF (.glb), +Y Up on, materials included. Refuses to overwrite.
import bpy, os

PATH = r"E:\7270\csye-7270-course\fall-2026\zhefan-z\assignment-3\walker-magic-zhefan\assets\models\rock.glb"

if os.path.exists(PATH):
    raise RuntimeError("refusing to overwrite " + PATH)
os.makedirs(os.path.dirname(PATH), exist_ok=True)

rock = bpy.data.objects["Rock"]
for ob in bpy.context.view_layer.objects:
    ob.select_set(False)
rock.select_set(True)
bpy.context.view_layer.objects.active = rock

settings = dict(
    filepath=PATH,
    export_format="GLB",            # dynamic enum; an invalid value raises TypeError listing the valid ones
    use_selection=True,
    export_yup=True,
    export_materials="EXPORT",
    export_apply=False,             # Rock has no modifiers
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
