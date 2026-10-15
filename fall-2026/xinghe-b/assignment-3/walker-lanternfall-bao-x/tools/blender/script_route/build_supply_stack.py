"""Build Lanternfall's low-poly Supply Stack and export a binary glTF."""
from __future__ import annotations

import json
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "godot" / "a3" / "supply_stack.glb"
BLEND = ROOT / "blender" / "a3" / "supply_stack.blend"
LOG = ROOT / "evidence" / "a3" / "supply_stack-build.json"


def material(name, color, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = 0.62
    return mat


def cube(name, dims, centre, mat):
    bpy.ops.mesh.primitive_cube_add(location=centre)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return obj


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    timber = material("MarketTimber", (0.34, 0.13, 0.045, 1.0))
    brass = material("CrateBrass", (0.56, 0.31, 0.08, 1.0), metallic=0.65)

    cube("LowerCrate", (1.20, 0.80, 0.50), (0.0, 0.0, 0.25), timber)
    cube("UpperCrate", (0.72, 0.68, 0.50), (-0.22, 0.05, 0.75), timber)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.22, depth=1.10, location=(0.32, 0.0, 0.55))
    barrel = bpy.context.object
    barrel.name = "OilBarrel"
    barrel.data.materials.append(brass)

    bpy.context.view_layer.update()
    visual = [o for o in scene.objects if o.type == "MESH"]
    triangles = sum(len(p.vertices) - 2 for o in visual for p in o.data.polygons)
    mins = [min((o.matrix_world @ v.co)[i] for o in visual for v in o.data.vertices) for i in range(3)]
    maxs = [max((o.matrix_world @ v.co)[i] for o in visual for v in o.data.vertices) for i in range(3)]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    BLEND.parent.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND), check_existing=False)
    bpy.ops.export_scene.gltf(filepath=str(OUT), export_format="GLB", export_yup=True, export_apply=True, export_materials="EXPORT")
    record = {
        "asset": "Supply Stack",
        "output": str(OUT.relative_to(ROOT)),
        "blend_source": str(BLEND.relative_to(ROOT)),
        "visual_bounds_blender_xyz_m": [round(maxs[i] - mins[i], 4) for i in range(3)],
        "origin_blender_xyz_m": [0.0, 0.0, 0.0],
        "visual_triangles": triangles,
        "triangle_budget": 180,
        "visible_primitives": len(visual),
        "primitive_budget": 6,
        "materials": sorted([timber.name, brass.name]),
        "hand_edit_target": "UpperCrate Y location; baseline is 0.05 m",
    }
    LOG.write_text(json.dumps(record, indent=2) + "\n")
    print("A3_BUILD " + json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
