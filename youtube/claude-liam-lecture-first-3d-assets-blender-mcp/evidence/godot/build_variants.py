# build_variants.py - the four deliberately WRONG exports that the Godot check is shown catching.
# Each one starts from the same build_*.py as the good asset and breaks exactly one thing.
#   Blender -b --factory-startup --python-exit-code 1 --python build_variants.py -- <out_dir>
import bpy, sys, os, runpy
from mathutils import Matrix

out_dir = sys.argv[sys.argv.index("--") + 1]
here = os.path.dirname(os.path.abspath(__file__))
assets = os.path.join(here, "..", "assets")
os.makedirs(out_dir, exist_ok=True)


def lib(asset):
    return runpy.run_path(os.path.join(assets, "build_%s.py" % asset), run_name="lib")


def export(name, yup=True):
    path = os.path.join(out_dir, name + ".glb")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', export_yup=yup, use_selection=True)
    print("  exported %s.glb | +Y Up %s" % (name, "ON" if yup else "OFF"))


def describe(o, what):
    d = o.dimensions
    print("%s: object %s | dimensions %.3f x %.3f x %.3f m | location %s | scale %s | rotation %s"
          % (what, o.name, d.x, d.y, d.z, tuple(round(v, 3) for v in o.location), tuple(round(v, 3) for v in o.scale),
             tuple(round(v, 3) for v in o.rotation_euler)))


print("Blender", bpy.app.version_string)

# (i) the lantern, exported with +Y Up OFF
ns = lib("lantern")
o, n = ns["build"]()
describe(o, "(i) lantern, +Y Up off")
export("lantern_yup_off", yup=False)

# (ii) the crate from a 2 m cube scaled to 0.4 and the scale NOT applied (origin at the base, so only the scale is wrong)
ns = lib("crate")
ns["clear_scene"]()
mat = ns["flat_material"]("CrateWood", "#C48A4F")
bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 0))
o = bpy.context.active_object
o.name = "Crate"
o.data.transform(Matrix.Translation((0, 0, 1)))        # cube spans z 0 .. 2 in its own space: the origin is the centre of the underside
o.data.materials.append(mat)
o.scale = (0.4, 0.4, 0.4)                               # <- the shortcut: scaled in Object Mode, never applied
bpy.context.view_layer.update()
describe(o, "(ii) crate from a 2 m cube, scale 0.4 NOT applied")
print("     mesh data spans %.3f m in z; the object's scale makes it %.3f m" % (max(v.co.z for v in o.data.vertices) - min(v.co.z for v in o.data.vertices), o.dimensions.z))
export("crate_scale_unapplied")

# (iii) the crate with its origin at its geometric centre
ns = lib("crate")
o, n = ns["build"]()
o.data.transform(Matrix.Translation((0, 0, -0.4)))     # geometry now spans z -0.4 .. +0.4 around the origin
bpy.context.view_layer.update()
describe(o, "(iii) crate, origin at its centre")
print("     lowest vertex z = %.3f m, highest = %.3f m" % (min(v.co.z for v in o.data.vertices), max(v.co.z for v in o.data.vertices)))
export("crate_origin_centre")

# (iv) the lantern built ten times too big (a unit slip)
ns = lib("lantern")
ns["build"].__globals__["SCALE"] = 10.0
o, n = ns["build"]()
describe(o, "(iv) lantern, ten times too big (applied, so scale reads 1)")
export("lantern_x10")

# (v) the crate whose colours were set ONLY as the viewport colour (Material > Settings > Viewport Display), so the Principled
#     "Base Color" the glTF exporter reads is still Blender's default grey. It looks brown in Blender's solid view and exports grey.
ns = lib("crate")
o, n = ns["build"]()
for slot in o.material_slots:
    slot.material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)
describe(o, "(v) crate, colour set as viewport colour only")
print("     viewport (display) colours:", [(s.material.name, tuple(round(c, 3) for c in s.material.diffuse_color)) for s in o.material_slots])
print("     Principled base colours   :", [(s.material.name, tuple(round(c, 3) for c in s.material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value)) for s in o.material_slots])
export("crate_colour_lost")
