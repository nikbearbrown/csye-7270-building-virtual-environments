# Exports the REAL checkpoint post (the final agent script, copied unchanged to _run/tools/blender/) in both glTF forms,
# then changes PostMetal's metallic value and exports both forms again, so version control can be asked what changed.
# Run:  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python export_forms.py
import bpy, os, runpy, shutil
here = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(here, "_run", "tools", "blender", "build_checkpoint_post.py"), run_name="__main__")
def export(dirname, fmt, name):
    d = os.path.join(here, "out", dirname); os.makedirs(d, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(d, name), export_format=fmt, export_yup=True, export_apply=True,
                              use_selection=False, export_materials='EXPORT', export_normals=True, export_texcoords=True)
for tag in ("a", "b"):
    if tag == "b":
        mat = bpy.data.materials["PostMetal"]
        mat.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.2   # was 0.8
    export(f"{tag}_gltf", 'GLTF_SEPARATE', "checkpoint_post.gltf")
    export(f"{tag}_glb", 'GLB', "checkpoint_post.glb")
print("EXPORT_FORMS_DONE")
