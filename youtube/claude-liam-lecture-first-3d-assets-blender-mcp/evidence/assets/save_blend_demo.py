# save_blend_demo.py - saves each asset as <name>.blend TWICE, so Blender writes its own backup <name>.blend1 on the second save.
#   Blender -b --factory-startup --python-exit-code 1 --python save_blend_demo.py
# It builds each asset with the same build_*.py the film shows (run as a library, so nothing is exported).
import bpy, os, runpy

here = os.path.dirname(os.path.abspath(__file__))
print("Blender %s | Preferences > Save & Load > Save Versions (filepaths.save_version) = %d  (how many backups Blender keeps: .blend1, .blend2, ...)" % (bpy.app.version_string, bpy.context.preferences.filepaths.save_version))
for name in ("crate", "lantern", "coin"):
    ns = runpy.run_path(os.path.join(here, "build_%s.py" % name), run_name="lib")
    obj, n = ns["build"]()
    path = os.path.join(here, "%s.blend" % name)
    bpy.ops.wm.save_as_mainfile(filepath=path)       # first save: <name>.blend
    print("saved 1 of 2:", os.path.basename(path))
    bpy.ops.wm.save_as_mainfile(filepath=path)       # second save: Blender moves the old file to <name>.blend1 first
    print("saved 2 of 2:", os.path.basename(path), "| backup now exists:", os.path.exists(path + "1"))
