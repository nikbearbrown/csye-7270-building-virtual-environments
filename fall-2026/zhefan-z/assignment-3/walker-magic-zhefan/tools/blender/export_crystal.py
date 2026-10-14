# export_crystal.py — headless export of the Crystal from tools/blender/crystal.blend to
# assets/models/crystal.glb, with the same glTF settings as rock.glb (binary, +Y Up, materials).
# Written 2026-10-14 after the live-session export (build_crystal.py, call E1) failed because the open
# Blender file had been reset. Opens crystal.blend, selects only "Crystal", exports, and never saves.
#
# Run from any folder, in a separate windowless Blender (no add-ons, so no MCP socket):
#   E:\7270\blender\blender.exe -b --factory-startup --python-exit-code 1 --python tools/blender/export_crystal.py
import bpy, os, addon_utils

HERE = os.path.dirname(os.path.abspath(__file__))
BLEND = os.path.join(HERE, "crystal.blend")
GLB = os.path.normpath(os.path.join(HERE, "..", "..", "assets", "models", "crystal.glb"))

if os.path.exists(GLB):
    raise RuntimeError("refusing to overwrite " + GLB)

bpy.ops.wm.open_mainfile(filepath=BLEND)
print("opened:", bpy.data.filepath, "| objects:", [(o.name, o.type) for o in bpy.data.objects])

for mod in addon_utils.modules():
    if mod.__name__.endswith("io_scene_gltf2"):
        print("glTF add-on:", mod.__name__, "version", mod.bl_info.get("version"),
              "| enabled:", addon_utils.check(mod.__name__))

crystal = bpy.data.objects["Crystal"]
for ob in bpy.context.view_layer.objects:
    ob.select_set(False)
crystal.select_set(True)
bpy.context.view_layer.objects.active = crystal

settings = dict(
    filepath=GLB,
    export_format="GLB",
    use_selection=True,
    export_yup=True,
    export_materials="EXPORT",
    export_apply=False,             # Crystal has no modifiers
    export_normals=True,
    export_texcoords=True,
    export_cameras=False,
    export_lights=False,
    export_extras=False,
    export_animations=False,
)
result = bpy.ops.export_scene.gltf(**settings)
print("result:", result, "|", GLB, os.path.getsize(GLB), "bytes")
print("settings:", {k: v for k, v in settings.items() if k != "filepath"})
print("selected:", [o.name for o in bpy.context.selected_objects])
# No save call: crystal.blend is left exactly as it was.
