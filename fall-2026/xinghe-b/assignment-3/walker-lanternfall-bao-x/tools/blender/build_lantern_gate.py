"""Build Lanternfall's Assignment 3 Lantern Gate through the Blender MCP.

Each block below is one `execute_blender_code` body, verbatim and in the order
it was sent to Bao's live Blender 5.2.2 LTS on 2026-10-14 (mcp-for-blender 2.1.9,
add-on 1.8). In the session each object block was followed by
`get_scene_info`; those are tool calls, not code, and are not repeated here.
A call that failed is kept as a commented block with its error. Every block is
self-contained, so the file also runs headless from the repository root:

    /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_lantern_gate.py

The pre-MCP script route is kept in tools/blender/script_route/.
"""

# ==== MCP call 1 of 13 ====
# Step 1: empty the scene through bpy.data (never read_factory_settings in the
# live session) and create the gate's three materials.
import bpy

for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in list(bpy.data.meshes):
    bpy.data.meshes.remove(mesh)
for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat)

scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0


def material(name, color, metallic=0.0, emission=None):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = 0.45
    if emission:
        bsdf.inputs["Emission Color"].default_value = emission
        bsdf.inputs["Emission Strength"].default_value = 2.5
    return mat


material("AgedBrass", (0.42, 0.24, 0.08, 1.0), metallic=0.75)
material("DarkWood", (0.12, 0.045, 0.025, 1.0))
material("EmberGlass", (1.0, 0.34, 0.06, 1.0), emission=(1.0, 0.12, 0.01, 1.0))

view = bpy.context.preferences.view
print("objects", len(bpy.data.objects), "meshes", len(bpy.data.meshes),
      "materials", sorted(m.name for m in bpy.data.materials))
print("language", view.language, "translate_new_dataname",
      getattr(view, "use_translate_new_dataname", None))

# ==== MCP call 2 of 13 ====
# Step 2: GateBase, the dark wood plinth (0.80 x 0.80 x 0.18 m) on the floor.
# Scale is left unapplied here; step 10 applies rotation and scale.
import bpy

bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.09))
obj = bpy.context.active_object
obj.name = obj.data.name = "GateBase"
obj.dimensions = (0.80, 0.80, 0.18)
obj.data.materials.append(bpy.data.materials["DarkWood"])
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 3 of 13 ====
# Step 3: GatePost, an 8-sided brass cylinder from the base top (0.18 m) to the
# cross-arm centre (2.55 m).
import bpy

bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.12, depth=2.37, location=(0.0, 0.0, 1.365))
obj = bpy.context.active_object
obj.name = obj.data.name = "GatePost"
obj.data.materials.append(bpy.data.materials["AgedBrass"])
bpy.context.view_layer.update()
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 4 of 13 ====
# Step 4: GateCrossArm, the 1.20 m brass beam that sets the gate's full width.
import bpy

bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 2.55))
obj = bpy.context.active_object
obj.name = obj.data.name = "GateCrossArm"
obj.dimensions = (1.20, 0.16, 0.16)
obj.data.materials.append(bpy.data.materials["AgedBrass"])
bpy.context.view_layer.update()
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 5 of 13 ====
# Step 5: GateFinial, a brass block from 2.55 m to the gate's 2.85 m top.
import bpy

bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 2.70))
obj = bpy.context.active_object
obj.name = obj.data.name = "GateFinial"
obj.dimensions = (0.16, 0.16, 0.30)
obj.data.materials.append(bpy.data.materials["AgedBrass"])
bpy.context.view_layer.update()
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 6 of 13 ====
# Step 6: LeftLantern, one glowing EmberGlass block under the left arm.
import bpy

bpy.ops.mesh.primitive_cube_add(location=(-0.38, 0.0, 2.18))
obj = bpy.context.active_object
obj.name = obj.data.name = "LeftLantern"
obj.dimensions = (0.44, 0.40, 0.48)
obj.data.materials.append(bpy.data.materials["EmberGlass"])
bpy.context.view_layer.update()
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 7 of 13 ====
# Step 7: RightLantern, the mirror of LeftLantern; the post keeps the two apart.
import bpy

bpy.ops.mesh.primitive_cube_add(location=(0.38, 0.0, 2.18))
obj = bpy.context.active_object
obj.name = obj.data.name = "RightLantern"
obj.dimensions = (0.44, 0.40, 0.48)
obj.data.materials.append(bpy.data.materials["EmberGlass"])
bpy.context.view_layer.update()
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 8 of 13 ====
# Step 8: BaseCollider-convcolonly. Godot's importer turns the suffix into a
# collision-only static body (0.80 x 0.80 x 0.32 m). Wire display keeps the
# visible base readable in Blender; display type is not exported.
import bpy

bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.16))
obj = bpy.context.active_object
obj.name = obj.data.name = "BaseCollider-convcolonly"
obj.dimensions = (0.80, 0.80, 0.32)
obj.display_type = "WIRE"
bpy.context.view_layer.update()
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 9 of 13 ====
# Step 9: PostCollider-convcolonly (0.42 x 0.42 x 2.55 m) around the post only;
# the cross-arm and lanterns stay non-blocking.
import bpy

bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 1.275))
obj = bpy.context.active_object
obj.name = obj.data.name = "PostCollider-convcolonly"
obj.dimensions = (0.42, 0.42, 2.55)
obj.display_type = "WIRE"
bpy.context.view_layer.update()
print(obj.name, tuple(obj.location), tuple(obj.dimensions), tuple(obj.scale))

# ==== MCP call 10 of 13 ====
# Step 10: apply rotation and scale to every mesh (Ctrl+A > Rotation & Scale),
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

# ==== MCP call 11 of 13 ====
# Step 11: measure the visible parts, save blender/a3/lantern_gate.blend and
# write the build record. Through the MCP there is no __file__, so the
# repository is found from the open .blend instead.
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
BLEND = ROOT / "blender" / "a3" / "lantern_gate.blend"
LOG = ROOT / "evidence" / "a3" / "lantern_gate-build.json"

scene = bpy.context.scene
bpy.context.view_layer.update()
visual = [o for o in scene.objects if o.type == "MESH" and not o.name.endswith("-convcolonly")]
colliders = [o for o in scene.objects if o.type == "MESH" and o.name.endswith("-convcolonly")]
tri_count = sum(len(p.vertices) - 2 for o in visual for p in o.data.polygons)
mins = [min((o.matrix_world @ v.co)[i] for o in visual for v in o.data.vertices) for i in range(3)]
maxs = [max((o.matrix_world @ v.co)[i] for o in visual for v in o.data.vertices) for i in range(3)]

BLEND.parent.mkdir(parents=True, exist_ok=True)
LOG.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND), check_existing=False)
record = {
    "asset": "Lantern Gate",
    "route": "Blender MCP execute_blender_code (mcp-for-blender 2.1.9, add-on 1.8, Blender 5.2.2 LTS)",
    "output": "godot/a3/lantern_gate.glb",
    "blend_source": str(BLEND.relative_to(ROOT)),
    "visual_bounds_blender_xyz_m": [round(maxs[i] - mins[i], 4) for i in range(3)],
    "visual_min_blender_xyz_m": [round(v, 4) for v in mins],
    "origin_blender_xyz_m": [0.0, 0.0, 0.0],
    "visual_triangles": tri_count,
    "triangle_budget": 160,
    "visible_primitives": len(visual),
    "primitive_budget": 6,
    "materials": sorted({s.material.name for o in visual for s in o.material_slots if s.material}),
    "unit_scale": all(tuple(o.scale) == (1.0, 1.0, 1.0) for o in visual + colliders),
    "colliders": {o.name: [round(v, 4) for v in o.dimensions] for o in colliders},
}
LOG.write_text(json.dumps(record, indent=2) + "\n")
print("A3_BUILD " + json.dumps(record, sort_keys=True))

# ==== MCP call 12 of 13: FAILED, kept commented out ====
# Error returned: AssertionError: [] at line 21 (export_format enum items are dynamic, so the list read back empty; nothing was exported)
# # Step 12: export godot/a3/lantern_gate.glb: binary glTF, +Y up, modifiers
# # applied, materials exported. Selection/visibility filters are passed
# # explicitly so remembered exporter settings cannot drop the colliders.
# import hashlib
# from pathlib import Path
#
# import bpy
#
#
# def repo_root():
#     for start in (globals().get("__file__"), bpy.data.filepath):
#         if start:
#             for parent in Path(start).resolve().parents:
#                 if (parent / "godot" / "project.godot").is_file():
#                     return parent
#     raise RuntimeError("run headless from the repository, or open a blender/a3 file first")
#
#
# OUT = repo_root() / "godot" / "a3" / "lantern_gate.glb"
# formats = [i.identifier for i in bpy.ops.export_scene.gltf.get_rna_type().properties["export_format"].enum_items]
# assert "GLB" in formats, formats
# OUT.parent.mkdir(parents=True, exist_ok=True)
# bpy.ops.export_scene.gltf(
#     filepath=str(OUT),
#     export_format="GLB",
#     export_yup=True,
#     export_apply=True,
#     export_materials="EXPORT",
#     use_selection=False,
#     use_visible=False,
#     use_renderable=False,
#     use_active_collection=False,
# )
# print("exported", OUT.name, OUT.stat().st_size, "bytes sha256", hashlib.sha256(OUT.read_bytes()).hexdigest())

# ==== MCP call 13 of 13 ====
# Step 13: export godot/a3/lantern_gate.glb: binary glTF, +Y up, modifiers
# applied, materials exported. Selection/visibility filters are passed
# explicitly so remembered exporter settings cannot drop the colliders.
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


OUT = repo_root() / "godot" / "a3" / "lantern_gate.glb"
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
