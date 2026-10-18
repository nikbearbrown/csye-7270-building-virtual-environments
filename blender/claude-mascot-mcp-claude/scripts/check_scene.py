import bpy
print("objects:", sorted(o.name for o in bpy.data.objects))
tot = 0
for o in sorted(bpy.data.objects, key=lambda o: o.name):
    if o.type != 'MESH': continue
    o.data.calc_loop_triangles(); tot += len(o.data.loop_triangles)
    zs = [(o.matrix_world @ v.co).z for v in o.data.vertices]
    print("%-6s loc (%.3f %.3f %.3f) dim (%.3f %.3f %.3f) rot %s scale %s min z %.4f mat %s" % (
        o.name, *o.location, *o.dimensions, tuple(round(v, 4) for v in o.rotation_euler), tuple(round(v, 4) for v in o.scale), min(zs),
        o.material_slots[0].material.name if o.material_slots else None))
print("triangles:", tot)
for m in bpy.data.materials:
    if m.node_tree:
        b = m.node_tree.nodes.get("Principled BSDF")
        if b:
            c = b.inputs["Base Color"].default_value
            srgb = [round(((v * 12.92) if v <= 0.0031308 else (1.055 * v ** (1 / 2.4) - 0.055)) * 255) for v in c[:3]]
            print("material", m.name, "linear", tuple(round(v, 4) for v in c[:3]), "-> sRGB", srgb, "= #%02x%02x%02x" % tuple(srgb))
