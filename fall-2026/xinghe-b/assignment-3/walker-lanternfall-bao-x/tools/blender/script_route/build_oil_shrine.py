"""Build Lanternfall's low-poly Lamp-oil Shrine and export a binary glTF."""
from __future__ import annotations

import json
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "godot" / "a3" / "oil_shrine.glb"
BLEND = ROOT / "blender" / "a3" / "oil_shrine.blend"
LOG = ROOT / "evidence" / "a3" / "oil_shrine-build.json"


def material(name, color, metallic=0.0, emission=None):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = 0.48
    if emission:
        bsdf.inputs["Emission Color"].default_value = emission
        bsdf.inputs["Emission Strength"].default_value = 3.0
    return mat


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    stone = material("ShrineStone", (0.055, 0.07, 0.12, 1.0))
    brass = material("ShrineBrass", (0.48, 0.25, 0.06, 1.0), metallic=0.72)
    glow = material("OilGlow", (1.0, 0.30, 0.035, 1.0), emission=(1.0, 0.10, 0.01, 1.0))

    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.125))
    base = bpy.context.object
    base.name = "ShrineBase"
    base.dimensions = (0.80, 0.80, 0.25)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    base.data.materials.append(stone)

    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.12, depth=0.70, location=(0.0, 0.0, 0.60))
    stem = bpy.context.object
    stem.name = "ShrineStem"
    stem.data.materials.append(brass)

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.30, location=(0.0, 0.0, 1.15))
    gem = bpy.context.object
    gem.name = "OilGem"
    gem.data.materials.append(glow)

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
        "asset": "Lamp-oil Shrine",
        "output": str(OUT.relative_to(ROOT)),
        "blend_source": str(BLEND.relative_to(ROOT)),
        "visual_bounds_blender_xyz_m": [round(maxs[i] - mins[i], 4) for i in range(3)],
        "origin_blender_xyz_m": [0.0, 0.0, 0.0],
        "visual_triangles": triangles,
        "triangle_budget": 120,
        "visible_primitives": len(visual),
        "primitive_budget": 6,
        "materials": sorted([stone.name, brass.name, glow.name]),
    }
    LOG.write_text(json.dumps(record, indent=2) + "\n")
    print("A3_BUILD " + json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
