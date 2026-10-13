# One mesh (the post's base + pole, joined) under six names, plus a Blender EMPTY (cube) named like a collider, exported as one GLB.
# Run:  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python make_suffix_probe.py
import bpy, os, runpy, bmesh
here = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(here, "_run", "tools", "blender", "build_checkpoint_post.py"), run_name="__main__")   # builds the real post (re-exports its glb under _run/)
# keep Base + Pole, join them into ONE mesh
for n in ("Pennant", "Collision-convcolonly"):
    bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)
bpy.ops.object.select_all(action='DESELECT')
base, pole = bpy.data.objects["Base"], bpy.data.objects["Pole"]
base.select_set(True); pole.select_set(True); bpy.context.view_layer.objects.active = base
bpy.ops.object.join()
body = bpy.context.active_object
names = ["Mesh0", "Mesh1-col", "Mesh2-convcol", "Mesh3-colonly", "Mesh4-convcolonly", "Mesh5-noimp"]
body.name = names[0]; body.data.name = names[0]
for i, n in enumerate(names[1:], 1):
    o = body.copy(); o.data = body.data.copy(); o.name = n; o.data.name = n
    o.location.x = i * 1.0
    bpy.context.collection.objects.link(o)
e = bpy.data.objects.new("Marker-colonly", None); e.empty_display_type = 'CUBE'; e.empty_display_size = 0.3
e.location = (7.0, 0, 0.9); bpy.context.collection.objects.link(e)
out = os.path.join(here, "suffix_probe", "post_suffixes.glb")
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', export_yup=True, export_apply=True, use_selection=False,
                          export_materials='EXPORT', export_normals=True, export_texcoords=True)
print("SUFFIX_PROBE_GLB", out, [o.name for o in bpy.data.objects])
