import bpy, bmesh
def tris(op, **kw):
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    op(**kw); o = bpy.context.active_object
    bm = bmesh.new(); bm.from_mesh(o.data)
    n = len(bmesh.ops.triangulate(bm, faces=bm.faces[:])["faces"]); bm.free(); return n
print("BLENDER", bpy.app.version_string)
print("cube", tris(bpy.ops.mesh.primitive_cube_add))
print("plane", tris(bpy.ops.mesh.primitive_plane_add))
print("cylinder(default)", tris(bpy.ops.mesh.primitive_cylinder_add))
print("cone(default)", tris(bpy.ops.mesh.primitive_cone_add))
print("uv_sphere(default)", tris(bpy.ops.mesh.primitive_uv_sphere_add))
print("uv_sphere(12x6)", tris(bpy.ops.mesh.primitive_uv_sphere_add, segments=12, ring_count=6))
print("cylinder(12)", tris(bpy.ops.mesh.primitive_cylinder_add, vertices=12))
