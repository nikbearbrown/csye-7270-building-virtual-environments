# export_glb.py — export the three assets as binary glTF, Assignment 3 (walker-rudy)
#
# Every execute_blender_code body that Claude Code ran through MCP for Blender
# (mcp-for-blender 2.1.9, add-on 1.8) in Blender 5.2.2 LTS (glTF add-on 5.2.40)
# on 2026-10-13, in order and unchanged. Blender had spikes.blend open; the other
# two assets were appended from their own files, exported and removed again, so
# no .blend file was changed or saved.

# ---------------------------------------------------------------------------
# Check — the exporter's option names and defaults in this Blender
import bpy
props = bpy.ops.export_scene.gltf.get_rna_type().properties
want = ["export_format", "use_selection", "export_yup", "export_apply", "export_materials",
        "export_cameras", "export_lights", "export_texcoords", "export_normals", "export_extras",
        "export_animations", "export_skins", "export_morph", "use_active_scene", "export_import_convert_lighting_mode"]
for k in want:
    if k in props:
        p = props[k]
        d = p.default if not hasattr(p, "enum_items") or p.type != 'ENUM' else p.default
        extra = [i.identifier for i in p.enum_items] if p.type == 'ENUM' else ""
        print(k, "default:", d, extra)
    else:
        print(k, "MISSING")
print("gltf addon version:", [m for m in __import__("addon_utils").modules() if m.__name__ == "io_scene_gltf2"][0].bl_info.get("version"))

# ---------------------------------------------------------------------------
# Export 1 — spikes.glb from the open spikes.blend: binary glTF, +Y Up, selected object only
import bpy, os

out_dir = "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-3/godot/assets/props"
os.makedirs(out_dir, exist_ok=True)
obj = bpy.data.objects["Spikes"]
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.gltf(
    filepath=os.path.join(out_dir, "spikes.glb"),
    export_format='GLB', use_selection=True, export_yup=True, export_apply=True,
    export_materials='EXPORT', export_cameras=False, export_lights=False, export_animations=False)
print("exported", os.path.join(out_dir, "spikes.glb"), os.path.getsize(os.path.join(out_dir, "spikes.glb")), "bytes")
print("spikes.blend dirty:", bpy.data.is_dirty)

# ---------------------------------------------------------------------------
# Export 2 — waystone.glb: append Waystone from waystone.blend into this session (waystone.blend is
# only read), export it alone, then remove it and its data again. Nothing here is saved.
import bpy, os

src = "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-3/blender/waystone.blend"
out = "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-3/godot/assets/props/waystone.glb"
with bpy.data.libraries.load(src, link=False) as (data_from, data_to):
    data_to.objects = ["Waystone"]
obj = data_to.objects[0]
bpy.context.scene.collection.objects.link(obj)
print("appended", obj.name, "loc", tuple(obj.location), "rot", tuple(obj.rotation_euler), "scale", tuple(obj.scale),
      "dims", tuple(round(d, 4) for d in obj.dimensions), "materials", [m.name for m in obj.data.materials])

bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.gltf(
    filepath=out, export_format='GLB', use_selection=True, export_yup=True, export_apply=True,
    export_materials='EXPORT', export_cameras=False, export_lights=False, export_animations=False)
print("exported", out, os.path.getsize(out), "bytes")

mesh, mats = obj.data, list(obj.data.materials)
bpy.data.objects.remove(obj, do_unlink=True)
bpy.data.meshes.remove(mesh)
for m in mats:
    if m.users == 0:
        bpy.data.materials.remove(m)
print("objects now:", [o.name for o in bpy.data.objects], "materials now:", [m.name for m in bpy.data.materials])

# ---------------------------------------------------------------------------
# Export 3 — teleport_circle.glb: the same, from teleport_circle.blend
import bpy, os

src = "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-3/blender/teleport_circle.blend"
out = "/Users/eric/csye7270/course-fork/fall-2026/shuai-z/assignment-3/godot/assets/props/teleport_circle.glb"
with bpy.data.libraries.load(src, link=False) as (data_from, data_to):
    data_to.objects = ["TeleportCircle"]
obj = data_to.objects[0]
bpy.context.scene.collection.objects.link(obj)
print("appended", obj.name, "loc", tuple(obj.location), "rot", tuple(obj.rotation_euler), "scale", tuple(obj.scale),
      "dims", tuple(round(d, 4) for d in obj.dimensions), "materials", [m.name for m in obj.data.materials])

bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.gltf(
    filepath=out, export_format='GLB', use_selection=True, export_yup=True, export_apply=True,
    export_materials='EXPORT', export_cameras=False, export_lights=False, export_animations=False)
print("exported", out, os.path.getsize(out), "bytes")

mesh, mats = obj.data, list(obj.data.materials)
bpy.data.objects.remove(obj, do_unlink=True)
bpy.data.meshes.remove(mesh)
for m in mats:
    if m.users == 0:
        bpy.data.materials.remove(m)
print("objects now:", [o.name for o in bpy.data.objects], "materials now:", [m.name for m in bpy.data.materials])
