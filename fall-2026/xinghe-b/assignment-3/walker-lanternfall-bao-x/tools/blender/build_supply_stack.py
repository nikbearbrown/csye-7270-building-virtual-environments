"""Build Lanternfall's Assignment 3 Supply Stack through the Blender MCP.

Each block below is one `execute_blender_code` body, verbatim and in the order
it was sent to Bao's live Blender 5.2.2 LTS on 2026-10-14 (mcp-for-blender 2.1.9,
add-on 1.8). In the session each object block was followed by
`get_scene_info`; those are tool calls, not code, and are not repeated here.
Every block is
self-contained, so the file also runs headless from the repository root:

    /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_supply_stack.py

The pre-MCP script route is kept in tools/blender/script_route/.
"""

# ==== MCP call 1 of 7 ====
# Step 1: empty the scene through bpy.data (never read_factory_settings in the
# live session) and create the stack's two materials.
import bpy

print("open file before clearing:", bpy.data.filepath, "unsaved changes:", bpy.data.is_dirty)
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in list(bpy.data.meshes):
    bpy.data.meshes.remove(mesh)
for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat)

scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0


def material(name, color, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = 0.62
    return mat


material("MarketTimber", (0.34, 0.13, 0.045, 1.0))
material("CrateBrass", (0.56, 0.31, 0.08, 1.0), metallic=0.65)
print("objects", len(bpy.data.objects), "meshes", len(bpy.data.meshes),
      "materials", sorted(m.name for m in bpy.data.materials))

# ==== MCP call 2 of 7 ====
# Step 2: LowerCrate, the 1.20 x 0.80 x 0.50 m crate that sets the full
# footprint. Scale is left unapplied here; step 5 applies rotation and scale.
import bpy

bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.25))
obj = bpy.context.active_object
obj.name = obj.data.name = "LowerCrate"
obj.dimensions = (1.20, 0.80, 0.50)
obj.data.materials.append(bpy.data.materials["MarketTimber"])
bpy.context.view_layer.update()
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 3 of 7 ====
# Step 3: UpperCrate, a smaller crate set back-left on top of LowerCrate.
import bpy

bpy.ops.mesh.primitive_cube_add(location=(-0.22, 0.05, 0.75))
obj = bpy.context.active_object
obj.name = obj.data.name = "UpperCrate"
obj.dimensions = (0.72, 0.68, 0.50)
obj.data.materials.append(bpy.data.materials["MarketTimber"])
bpy.context.view_layer.update()
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 4 of 7 ====
# Step 4: OilBarrel, a 12-sided brass cylinder standing from the floor to the
# stack's 1.10 m top (as in the script route, its lower half is inside
# LowerCrate).
import bpy

bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.22, depth=1.10, location=(0.32, 0.0, 0.55))
obj = bpy.context.active_object
obj.name = obj.data.name = "OilBarrel"
obj.data.materials.append(bpy.data.materials["CrateBrass"])
bpy.context.view_layer.update()
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 5 of 7 ====
# Step 5: apply rotation and scale to every mesh (Ctrl+A > Rotation & Scale),
# so Godot receives unit node scale. Locations stay as each part's centre.
import bpy

meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for obj in bpy.context.scene.objects:
    obj.select_set(obj in meshes)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.context.view_layer.update()
for obj in meshes:
    print(obj.name, tuple(round(v, 4) for v in obj.rotation_euler), tuple(round(v, 4) for v in obj.scale),
          tuple(round(v, 4) for v in obj.dimensions))

# ==== MCP call 6 of 7 ====
# Step 6: measure the parts, save blender/a3/supply_stack.blend and write the
# build record, including each part's location as the baseline for any later
# hand edit. Through the MCP there is no __file__, so the repository is found
# from the open .blend instead.
import json
from pathlib import Path

import bpy


def repo_root():
    for start in (globals().get("__file__"), bpy.data.filepath):
        if start:
            for parent in Path(start).resolve().parents:
                if (parent / "godot" / "project.godot").is_file():
                    return parent
    raise RuntimeError("run headless from the repository, or open a blender/a3 file first")


ROOT = repo_root()
BLEND = ROOT / "blender" / "a3" / "supply_stack.blend"
LOG = ROOT / "evidence" / "a3" / "supply_stack-build.json"

scene = bpy.context.scene
bpy.context.view_layer.update()
visual = [o for o in scene.objects if o.type == "MESH"]
triangles = sum(len(p.vertices) - 2 for o in visual for p in o.data.polygons)
mins = [min((o.matrix_world @ v.co)[i] for o in visual for v in o.data.vertices) for i in range(3)]
maxs = [max((o.matrix_world @ v.co)[i] for o in visual for v in o.data.vertices) for i in range(3)]

BLEND.parent.mkdir(parents=True, exist_ok=True)
LOG.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND), check_existing=False)
record = {
    "asset": "Supply Stack",
    "route": "Blender MCP execute_blender_code (mcp-for-blender 2.1.9, add-on 1.8, Blender 5.2.2 LTS)",
    "output": "godot/a3/supply_stack.glb",
    "blend_source": str(BLEND.relative_to(ROOT)),
    "visual_bounds_blender_xyz_m": [round(maxs[i] - mins[i], 4) for i in range(3)],
    "visual_min_blender_xyz_m": [round(v, 4) for v in mins],
    "origin_blender_xyz_m": [0.0, 0.0, 0.0],
    "visual_triangles": triangles,
    "triangle_budget": 180,
    "visible_primitives": len(visual),
    "primitive_budget": 3,
    "materials": sorted({s.material.name for o in visual for s in o.material_slots if s.material}),
    "unit_scale": all(tuple(o.scale) == (1.0, 1.0, 1.0) for o in visual),
    "parts": {o.name: {"location": [round(v, 4) for v in o.location],
                       "size": [round(v, 4) for v in o.dimensions]} for o in visual},
}
LOG.write_text(json.dumps(record, indent=2) + "\n")
print("A3_BUILD " + json.dumps(record, sort_keys=True))

# ==== MCP call 7 of 7 ====
# Step 7: export godot/a3/supply_stack.glb: binary glTF, +Y up, modifiers
# applied, materials exported, with selection/visibility filters off.
import hashlib
from pathlib import Path

import bpy


def repo_root():
    for start in (globals().get("__file__"), bpy.data.filepath):
        if start:
            for parent in Path(start).resolve().parents:
                if (parent / "godot" / "project.godot").is_file():
                    return parent
    raise RuntimeError("run headless from the repository, or open a blender/a3 file first")


OUT = repo_root() / "godot" / "a3" / "supply_stack.glb"
OUT.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.export_scene.gltf(
    filepath=str(OUT),
    export_format="GLB",
    export_yup=True,
    export_apply=True,
    export_materials="EXPORT",
    use_selection=False,
    use_visible=False,
    use_renderable=False,
    use_active_collection=False,
)
print("exported", OUT.name, OUT.stat().st_size, "bytes sha256", hashlib.sha256(OUT.read_bytes()).hexdigest())
