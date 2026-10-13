# build_coin.py - a gold coin from three basic shapes: a flat cylinder with a raised medallion on each face.
# Blender is Z-up, metric: 1 unit = 1 metre. Origin = centre of the underside, at the world origin. Lying flat.
# Run (no window):
#   /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python build_coin.py
import bpy, os, sys

NAME = "Coin"
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


def cylinder(name, radius, depth, z0, mat, vertices):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=(0, 0, z0 + depth / 2))
    o = bpy.context.active_object
    o.name = name
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
    """Builds the coin. Returns (object or parts, shape_count)."""
    clear_scene()
    gold = flat_material("CoinGold", "#FFC20A")
    face = flat_material("CoinFace", "#E39A00")
    parts = [
        cylinder("Coin_Body", 0.15, 0.030, 0.005, gold, 24),        # 0.30 m across, z 0.005 .. 0.035
        cylinder("Coin_FaceTop", 0.09, 0.005, 0.035, face, 12),     # raised medallion, z 0.035 .. 0.040
        cylinder("Coin_FaceBottom", 0.09, 0.005, 0.000, face, 12),  # raised medallion, z 0.000 .. 0.005
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
