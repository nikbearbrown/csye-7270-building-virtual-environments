# build_lantern.py - a lantern from five basic shapes: cylinder base, cylinder body, cone roof, sphere flame, small cylinder finial.
# Blender is Z-up, metric: 1 unit = 1 metre. Origin = centre of the underside, at the world origin.
# Run (no window):
#   /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python build_lantern.py
import bpy, os, sys

NAME = "Lantern"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else HERE
SCALE = 1.0          # only the failure demo (build_variants.py) changes this


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


def finish_part(o, name, mat):
    o.name = name
    o.data.materials.append(mat)
    return o


def cylinder(name, radius, depth, z0, mat, vertices=12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=(0, 0, z0 + depth / 2))
    return finish_part(bpy.context.active_object, name, mat)


def cone(name, radius, depth, z0, mat, vertices=12):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=0.0, depth=depth, location=(0, 0, z0 + depth / 2))
    return finish_part(bpy.context.active_object, name, mat)


def sphere(name, radius, zc, mat, segments=8, rings=5):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius, location=(0, 0, zc))
    return finish_part(bpy.context.active_object, name, mat)


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
    """Builds the lantern. Returns (object or parts, shape_count)."""
    clear_scene()
    iron = flat_material("DarkIron", "#3A3A42")
    glass = flat_material("WarmGlass", "#FFB41F")
    flame = flat_material("Flame", "#FF5400")
    parts = [
        cylinder("Lantern_Base", 0.15, 0.04, 0.00, iron),        # z 0.00 .. 0.04, 0.30 m across
        cylinder("Lantern_Glass", 0.10, 0.23, 0.04, glass),      # z 0.04 .. 0.27
        sphere("Lantern_Flame", 0.06, 0.32, flame),              # z 0.26 .. 0.38, in the open gap between glass and roof
        cone("Lantern_Roof", 0.14, 0.10, 0.37, iron),            # z 0.37 .. 0.47
        cylinder("Lantern_Finial", 0.02, 0.03, 0.47, iron, vertices=8),    # z 0.47 .. 0.50
    ]
    n = len(parts)
    if SCALE != 1.0:
        for p in parts:                                          # scale the whole lantern about the world origin
            p.location *= SCALE
            p.scale = (SCALE, SCALE, SCALE)
        bpy.context.view_layer.update()
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
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
