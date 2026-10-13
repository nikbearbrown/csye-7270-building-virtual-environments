# ACT III probe (B26/B27/B29): what "apply scale" changes, in Blender 5.1.2.
#   Blender -b --factory-startup --python-exit-code 1 --python apply_probe.py
import bpy
bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 0.9))   # a 2 m cube...
o = bpy.context.active_object
o.scale = (0.1, 0.1, 0.9)                                         # ...scaled down to a pole
def vertex_extent(obj):
    xs = [v.co.x for v in obj.data.vertices]; ys = [v.co.y for v in obj.data.vertices]; zs = [v.co.z for v in obj.data.vertices]
    return tuple(round(max(a) - min(a), 4) for a in (xs, ys, zs))
def show(tag):
    bpy.context.view_layer.update()
    print("%s scale %s  vertices span %s  object dimensions %s" % (
        tag, tuple(round(v, 4) for v in o.scale), vertex_extent(o), tuple(round(v, 4) for v in o.dimensions)))
show("BEFORE apply:")
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
show("AFTER  apply:")
