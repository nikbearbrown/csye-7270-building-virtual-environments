# units.py - ACT III evidence (B24): what a factory-fresh Blender 5.1.2 scene uses for units, and the crate's size in those units.
#   Blender -b --factory-startup --python-exit-code 1 --python units.py
import bpy, os, runpy
u = bpy.context.scene.unit_settings
print("Blender", bpy.app.version_string, "| factory startup scene units: system", u.system, "| unit scale", u.scale_length, "| length unit", u.length_unit)
ns = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "build_crate.py"), run_name="lib")
o, n = ns["build"](join=True)
print("crate dimensions in Blender units:", tuple(round(v, 4) for v in o.dimensions), "| unit scale", u.scale_length, "-> metres:", tuple(round(v * u.scale_length, 4) for v in o.dimensions))
