"""
build_checkpoint_post.py  —  run with Blender in background mode:

    Blender -b --factory-startup --python tools/blender/build_checkpoint_post.py

Builds a low-poly checkpoint post and exports godot/props/checkpoint_post.glb.

Coordinate origin: centre of the base's underside  (Blender Z=0)
Blender +Z up is converted to glTF/Godot +Y up by the exporter.

Geometry (Blender / +Z-up):
  Base          0.6 x 0.6 x 0.1 m   Z 0.00 → 0.10
  Pole          8-sided, r=0.08 m    Z 0.10 → 1.80
  Pennant       flat XZ-plane quad   X 0.08 → 0.48, Z 1.55 → 1.80
  Collider      convex tapered hull  base ±0.30, pole ±0.08, Z 0.00 → 1.80

Materials: PostMetal (Base + Pole), FlagCloth (Pennant)
"""

import bpy
import bmesh
import math
import os
import sys

# ── helpers ──────────────────────────────────────────────────────────────────

def new_obj(name: str, mesh: bpy.types.Mesh) -> bpy.types.Object:
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    return obj


def build_box_mesh(name: str, corners_lo, corners_hi) -> bpy.types.Mesh:
    """Axis-aligned box from two corner tuples."""
    x0, y0, z0 = corners_lo
    x1, y1, z1 = corners_hi
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    v = [
        bm.verts.new((x0, y0, z0)), bm.verts.new((x1, y0, z0)),
        bm.verts.new((x1, y1, z0)), bm.verts.new((x0, y1, z0)),
        bm.verts.new((x0, y0, z1)), bm.verts.new((x1, y0, z1)),
        bm.verts.new((x1, y1, z1)), bm.verts.new((x0, y1, z1)),
    ]
    bm.verts.ensure_lookup_table()
    face_idx = [
        [0, 1, 2, 3],   # -Z  bottom
        [7, 6, 5, 4],   # +Z  top
        [0, 4, 5, 1],   # -Y  front
        [1, 5, 6, 2],   # +X  right
        [2, 6, 7, 3],   # +Y  back
        [3, 7, 4, 0],   # -X  left
    ]
    for fi in face_idx:
        bm.faces.new([v[i] for i in fi])
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return mesh


# ── clear factory scene ───────────────────────────────────────────────────────

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.meshes):   bpy.data.meshes.remove(m)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)

# ── metric units ─────────────────────────────────────────────────────────────

scene = bpy.context.scene
scene.unit_settings.system       = 'METRIC'
scene.unit_settings.length_unit  = 'METERS'
scene.unit_settings.scale_length = 1.0

# ── materials ─────────────────────────────────────────────────────────────────

def make_pbr(name: str, base_color, metallic: float, roughness: float):
    mat = bpy.data.materials.new(name)
    # In Blender 5.x, materials use nodes by default; force it on for older builds.
    try:
        mat.use_nodes = True
    except Exception:
        pass
    if mat.node_tree and mat.node_tree.nodes.get("Principled BSDF"):
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value  = (*base_color, 1.0)
        bsdf.inputs["Metallic"].default_value    = metallic
        bsdf.inputs["Roughness"].default_value   = roughness
    return mat

mat_metal = make_pbr("PostMetal", (0.50, 0.50, 0.55), metallic=0.8, roughness=0.4)
mat_cloth = make_pbr("FlagCloth", (0.80, 0.10, 0.10), metallic=0.0, roughness=0.9)

# ── Base  (0.6 × 0.6 × 0.1, Z 0 → 0.1) ─────────────────────────────────────

base_mesh = build_box_mesh("Base", (-0.3, -0.3, 0.0), (0.3, 0.3, 0.1))
base_obj  = new_obj("Base", base_mesh)
base_mesh.materials.append(mat_metal)

# ── Pole  (8-sided cyl, r=0.08, Z 0.1 → 1.8) ────────────────────────────────

pole_mesh = bpy.data.meshes.new("Pole")
bm = bmesh.new()
n, r, z0, z1 = 8, 0.08, 0.1, 1.8
bot, top = [], []
for i in range(n):
    a = 2 * math.pi * i / n
    x, y = r * math.cos(a), r * math.sin(a)
    bot.append(bm.verts.new((x, y, z0)))
    top.append(bm.verts.new((x, y, z1)))
bm.faces.new(bot[::-1])   # bottom cap (normal −Z)
bm.faces.new(top)          # top cap    (normal +Z)
for i in range(n):
    j = (i + 1) % n
    bm.faces.new([bot[i], bot[j], top[j], top[i]])
bm.to_mesh(pole_mesh)
bm.free()
pole_mesh.update()
pole_obj = new_obj("Pole", pole_mesh)
pole_mesh.materials.append(mat_metal)

# ── Pennant  (flat XZ-plane, X 0.08→0.48, Z 1.55→1.80) ─────────────────────

pennant_mesh = bpy.data.meshes.new("Pennant")
bm = bmesh.new()
pv = [
    bm.verts.new((0.08, 0.0, 1.80)),
    bm.verts.new((0.48, 0.0, 1.80)),
    bm.verts.new((0.48, 0.0, 1.55)),
    bm.verts.new((0.08, 0.0, 1.55)),
]
bm.faces.new(pv)           # single face; glTF renders both sides via material
bm.to_mesh(pennant_mesh)
bm.free()
pennant_mesh.update()
pennant_obj = new_obj("Pennant", pennant_mesh)
pennant_mesh.materials.append(mat_cloth)

# ── Collision box  (base + pole only, Godot -convcolonly suffix) ──────────────
# X ±0.3, Y ±0.3, Z 0 → 1.8   (no pennant at X 0.08→0.48)

# Name both the mesh data AND the object with the suffix so Godot's importer
# detects it regardless of whether it checks the glTF mesh name or node name.
col_mesh = bpy.data.meshes.new("Collision")
bm = bmesh.new()
for x in (-0.3, 0.3):
    for y in (-0.3, 0.3):
        for z in (0.0, 0.1):
            bm.verts.new((x, y, z))
for x in (-0.08, 0.08):
    for y in (-0.08, 0.08):
        for z in (0.1, 1.8):
            bm.verts.new((x, y, z))
bmesh.ops.convex_hull(bm, input=list(bm.verts))
bm.to_mesh(col_mesh)
bm.free()
col_mesh.update()
col_obj  = new_obj("Collision-convcolonly", col_mesh)
# No visual material — collision-only mesh

# ── Apply rotation + scale on every object ───────────────────────────────────
# All origins are at world (0,0,0); transforms are already identity after
# BMesh creation, so this is a no-op but satisfies the spec.

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# ── Print info ───────────────────────────────────────────────────────────────

def obj_mats(obj):
    return [s.material.name for s in obj.material_slots if s.material]

print("\n=== Checkpoint Post Objects ===")
for obj in bpy.data.objects:
    dims = obj.dimensions
    sc   = obj.scale
    mats = obj_mats(obj)
    print(
        f"  {obj.name:30s}  "
        f"dims=({dims.x:.4f}, {dims.y:.4f}, {dims.z:.4f})  "
        f"scale=({sc.x:.3f}, {sc.y:.3f}, {sc.z:.3f})  "
        f"materials={mats}"
    )
print()

# ── Export ───────────────────────────────────────────────────────────────────

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root  = os.path.dirname(os.path.dirname(script_dir))   # tools/ → root
out_path   = os.path.join(repo_root, "godot", "props", "checkpoint_post.glb")

os.makedirs(os.path.dirname(out_path), exist_ok=True)
print(f"Exporting to: {out_path}")

bpy.ops.export_scene.gltf(
    filepath=out_path,
    export_format='GLB',
    export_yup=True,          # Blender +Z → glTF/Godot +Y
    export_apply=True,        # apply modifiers
    use_selection=False,      # export all objects
    export_materials='EXPORT',
    export_normals=True,
    export_texcoords=True,
)

print("Done.\n")
