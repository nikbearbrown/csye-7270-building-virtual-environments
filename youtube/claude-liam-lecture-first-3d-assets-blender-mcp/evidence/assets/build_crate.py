# build_crate.py - a wooden crate from five basic shapes (a cube plus four thin bands).
# Blender is Z-up, metric: 1 unit = 1 metre. Origin = centre of the underside, at the world origin.
# Run (no window):
#   /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python build_crate.py
import bpy, os, sys

NAME = "Crate"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else HERE


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def flat_material(name, hex_colour):
    """One flat colour, no texture. Principled base colour (what glTF exports) + the viewport colour (what Workbench shows)."""
    lin = tuple(srgb_to_linear(int(hex_colour[i:i + 2], 16) / 255) for i in (1, 3, 5)) + (1.0,)
    m = bpy.data.materials.new(name)
    m.diffuse_color = lin
    b = m.node_tree.nodes["Principled BSDF"]       # Blender 5.x: a new material already has its node tree
    b.inputs["Base Color"].default_value = lin
    b.inputs["Metallic"].default_value = 0.0
    b.inputs["Roughness"].default_value = 0.9
    return m


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for m in list(bpy.data.materials):
        bpy.data.materials.remove(m)


def box(name, size, centre, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centre)
    o = bpy.context.active_object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)   # size baked into the vertices, scale back to 1
    o.data.materials.append(mat)
    return o


def join_at_origin(name, parts):
    """Join the shapes into one object whose origin is the world origin (the centre of the underside)."""
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    o = bpy.context.active_object
    o.name = name
    o.data.name = name
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return o


def build(join=True):
    """Builds the crate. Returns (object or parts, shape_count)."""
    clear_scene()
    wood = flat_material("CrateWood", "#C48A4F")
    band = flat_material("CrateBand", "#7E5128")
    parts = [
        box("Crate_Body", (0.76, 0.76, 0.76), (0, 0, 0.40), wood),            # the cube, z 0.02 .. 0.78
        box("Crate_BandLow", (0.80, 0.80, 0.10), (0, 0, 0.05), band),          # ring round the bottom, z 0.00 .. 0.10
        box("Crate_BandHigh", (0.80, 0.80, 0.10), (0, 0, 0.75), band),         # ring round the top, z 0.70 .. 0.80
        box("Crate_StrapX", (0.10, 0.80, 0.80), (0, 0, 0.40), band),           # strap over front and back
        box("Crate_StrapY", (0.80, 0.10, 0.80), (0, 0, 0.40), band),           # strap over left and right
    ]
    n = len(parts)
    if not join:
        return parts, n
    return join_at_origin(NAME, parts), n


def tri_count(o):
    o.data.calc_loop_triangles()
    return len(o.data.loop_triangles)


def report(o, n_shapes):
    zs = [(o.matrix_world @ v.co).z for v in o.data.vertices]
    d = o.dimensions
    print("Blender %s | metric, 1 unit = 1 m | Z up" % bpy.app.version_string)
    print("%-8s %-24s %5s %7s  %s" % ("name", "dimensions (x y z) m", "tris", "shapes", "materials"))
    print("%-8s %-24s %5d %7d  %s" % (o.name, "%.3f x %.3f x %.3f" % tuple(d), tri_count(o), n_shapes,
                                      ", ".join(s.material.name for s in o.material_slots)))
    print("origin at world (%.3f, %.3f, %.3f) | lowest point z = %.4f m | rotation %s | scale %s"
          % (*o.location, min(zs), tuple(round(v, 4) for v in o.rotation_euler), tuple(round(v, 4) for v in o.scale)))


def export(o, out_dir):
    path = os.path.join(out_dir, NAME.lower() + ".glb")
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', export_yup=True, use_selection=True)
    print("exported %s (%d bytes), +Y Up on" % (os.path.basename(path), os.path.getsize(path)))


if __name__ == "__main__":
    obj, n = build()
    report(obj, n)
    export(obj, OUT_DIR)
