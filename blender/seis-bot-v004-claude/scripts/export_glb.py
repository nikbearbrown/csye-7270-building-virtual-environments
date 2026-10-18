"""Blender -b seis-bot-v004-standing.blend --python export_glb.py -- out.glb
Exports the robot only (meshes in PART_* collections + the SEIS_rig armature), skinned, no stage/lights.
Procedural materials are not carried: glTF gets each material's base colour/metal/roughness fallback only."""
import sys, collections
import bpy
out = sys.argv[sys.argv.index("--") + 1]
mods = collections.Counter(m.type for o in bpy.data.objects for m in o.modifiers)
print("MODS", dict(mods))
bpy.ops.object.select_all(action="DESELECT")
n = 0
for o in bpy.context.scene.objects:
    cols = [c.name for c in o.users_collection]
    if o.type == "ARMATURE" or (o.type == "MESH" and any(c.startswith("PART_") for c in cols)):
        o.hide_set(False); o.select_set(True); n += 1
print("SELECTED", n)
bpy.ops.export_scene.gltf(filepath=out, use_selection=True, export_format="GLB", export_apply=False, export_skins=True,
                          export_cameras=False, export_lights=False, export_yup=True)
